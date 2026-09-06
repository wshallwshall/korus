#Requires -Version 7.3
<#
.SYNOPSIS
    Write this session's EPISODE RECORD: the durable answer to "what was this seat doing".

.DESCRIPTION
    WHAT IT IS FOR. A session's seat and its goal live in the conversation, and the conversation is
    the one thing that does not survive. A compaction summarises it, an account switch ends it, and
    a crash takes it. Afterwards nothing on disk says what that worktree was in the middle of, so
    the next session either starts over or guesses.

    ONE RECORD PER (WORKTREE, SESSION), at <state-root>/seats/<boxKey>/<sessionKey>.json.

        seat.ps1 -Declare -Seat builder -Goal "port the role cards"
        seat.ps1 -Declare -Seat builder -Goal "..." -Handoff docs/HANDOFF-x.md
        seat.ps1 -Record                     # the hook path: derive what it can, never invent
        seat.ps1 -Close
        seat.ps1 -List

    THE SEAT CAN BE WRITTEN BY A MACHINE. THE GOAL CANNOT. That distinction is the whole design.
    `-Declare` requires a goal because a machine that invents one writes a record that LOOKS
    declared and says nothing -- which is worse than an absent record, because an absent record
    prompts somebody to write one. `-Record` therefore never writes a goal it was not given; it
    updates the mechanical fields and leaves the declaration alone.

    IT LIVES INSIDE `.git`, so there is no history, no merge and no conflict. That is the point: a
    per-session record in a tracked file would conflict every time two sessions ran, and the
    conflict would be in the one file nobody wants to resolve. The corollary is that state OUTLIVES
    the worktree, which is why `-List` reports a record whose worktree is gone rather than hiding it.

    IT WRITES THE ROLE-CARD MARKER TOO. `-Declare -Seat` sets `.claude/seat.local.txt`, which is
    what `scripts/hooks/role-card-inject.ps1` resolves first. docs/ROLE-CARDS.md records that a
    fourth resolution rung reading the seat record was designed and dropped, because the cheaper end
    state is for a declaration to write the marker. This is that end state.

.PARAMETER Seat
    One of the live seats in docs/roles/seats.json. An unknown value is refused rather than
    recorded: 46 distinct role strings for a six-seat roster is what happens when it is not.
#>

[CmdletBinding(DefaultParameterSetName = 'List')]
param(
    [Parameter(ParameterSetName = 'Declare')][switch] $Declare,
    [Parameter(ParameterSetName = 'Declare')][string] $Seat,
    [Parameter(ParameterSetName = 'Declare')][string] $Goal,
    [Parameter(ParameterSetName = 'Declare')][string] $Done,
    [Parameter(ParameterSetName = 'Declare')][string] $OutOfScope,
    [Parameter(ParameterSetName = 'Declare')][string] $Handoff,
    [Parameter(ParameterSetName = 'Record')][switch] $Record,
    [Parameter(ParameterSetName = 'Close')][switch] $Close,
    [Parameter(ParameterSetName = 'List')][switch] $List,
    [string] $SessionId
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

. (Join-Path $PSScriptRoot '_mail.ps1')

function Fail {
    param([string] $Message)
    Write-Host "seat: $Message"
    exit 1
}

function Get-SeatsRoster {
    $path = Join-Path (Split-Path -Parent (Split-Path -Parent $PSScriptRoot)) 'docs/roles/seats.json'
    if (-not (Test-Path -LiteralPath $path)) { return $null }
    try { return Get-Content -LiteralPath $path -Raw | ConvertFrom-Json } catch { return $null }
}

# The state root the coordination scripts already use. Seats are HELD STATE, not messages, so they
# belong beside claims and allocations rather than in the mail root, which expires things.
$common = Get-CcxMailGitCommonDir
if (-not $common) { Fail "not inside a git clone, so there is no state root to write to." }
$seatsRoot = Join-Path (Join-Path $common 'ccx-coord') 'seats'

$myTree = Get-CcxMailWorktreeRoot
if (-not $myTree) { Fail "this directory is not inside a git worktree." }
$boxKey = Get-CcxMailBoxKey -WorktreeRoot $myTree

$branch = ''
Push-Location -LiteralPath $myTree
try { $branch = (& git rev-parse --abbrev-ref HEAD 2>$null); if ($branch) { $branch = $branch.Trim() } }
finally { Pop-Location }

# A session id is supplied by the caller or the harness. Falling back to the worktree means one
# record per worktree rather than one per session, which is a weaker but honest degradation.
$sessionKey = if ($SessionId) { $SessionId } elseif ($env:CLAUDE_SESSION_ID) { $env:CLAUDE_SESSION_ID } else { 'unnamed-session' }
$sessionKey = ($sessionKey -replace '[^A-Za-z0-9._-]', '-')
if ($sessionKey.Length -gt 64) { $sessionKey = $sessionKey.Substring(0, 64) }

$boxDir = Join-Path $seatsRoot $boxKey
$recordPath = Join-Path $boxDir "$sessionKey.json"

function Read-Record {
    if (-not (Test-Path -LiteralPath $recordPath)) { return $null }
    try { return Get-Content -LiteralPath $recordPath -Raw | ConvertFrom-Json } catch { return $null }
}

function Get-StampString {
    <#
    .SYNOPSIS
        A stamp read back out of a record, rendered as the string it was written as.
    .DESCRIPTION
        `ConvertFrom-Json` PARSES an ISO-8601 field into a [datetime], so any stamp carried forward
        by -Record or -Close is re-rendered on the way out. `[string]` on a [datetime] uses the
        CURRENT CULTURE, which turned `2026-09-05T16:14:07.5348854+00:00` into `09/05/2026
        11:14:07` -- ambiguous between day and month, carrying no offset, and parseable by nothing
        downstream. Re-serialising the parsed value is the milder half of the same defect: it
        rewrote a UTC stamp in the writer's local offset. Both were caught by tests/test_seat.py.
    #>
    param($Value)
    if ($null -eq $Value) { return '' }
    if ($Value -is [datetime]) { return ([datetimeoffset]$Value).ToUniversalTime().ToString('o') }
    if ($Value -is [datetimeoffset]) { return $Value.ToUniversalTime().ToString('o') }
    return [string]$Value
}

function Write-Record {
    param([hashtable] $Fields)
    if (-not (Test-Path -LiteralPath $boxDir)) {
        New-Item -ItemType Directory -Force -Path $boxDir -ErrorAction Stop | Out-Null
    }
    # Write-then-replace. A torn record parses as "no declaration", which would silently discard a
    # goal nothing else holds a copy of.
    $tmp = "$recordPath.$PID.tmp"
    ($Fields | ConvertTo-Json -Depth 6) | Set-Content -LiteralPath $tmp -Encoding utf8NoBOM -ErrorAction Stop
    Move-Item -LiteralPath $tmp -Destination $recordPath -Force -ErrorAction Stop
}

# --------------------------------------------------------------------------------------- list
if (-not $Declare -and -not $Record -and -not $Close) {
    Write-Host "seats root : $seatsRoot"
    Write-Host "as of      : $(Get-CcxMailStamp)"
    if (-not (Test-Path -LiteralPath $seatsRoot)) { Write-Host "no records yet."; exit 0 }

    $any = $false
    foreach ($d in (Get-ChildItem -LiteralPath $seatsRoot -Directory | Sort-Object Name)) {
        foreach ($f in (Get-ChildItem -LiteralPath $d.FullName -Filter '*.json' -File | Sort-Object LastWriteTimeUtc -Descending)) {
            $any = $true
            $rec = $null
            try { $rec = Get-Content -LiteralPath $f.FullName -Raw | ConvertFrom-Json } catch { }
            if (-not $rec) { Write-Host "  $($d.Name)/$($f.Name)  UNREADABLE"; continue }

            $seatName = if ($rec.PSObject.Properties['seat'] -and $rec.seat) { $rec.seat } else { '(undeclared)' }
            $goalText = if ($rec.PSObject.Properties['goal'] -and $rec.goal) { $rec.goal } else { '(no goal declared)' }
            $wt = if ($rec.PSObject.Properties['worktree']) { [string]$rec.worktree } else { '' }
            $gone = if ($wt -and -not (Test-Path -LiteralPath $wt)) { '  [WORKTREE GONE]' } else { '' }
            $state = if ($rec.PSObject.Properties['closed_at'] -and $rec.closed_at) { 'closed' } else { 'open  ' }

            Write-Host ("  {0}  {1,-10} {2}{3}" -f $state, $seatName, (Split-Path -Leaf $wt), $gone)
            Write-Host ("      goal: {0}" -f $goalText)
        }
    }
    if (-not $any) { Write-Host "no records yet." }
    Write-Host ""
    Write-Host "State outlives the worktree, deliberately. A record whose worktree is GONE is shown"
    Write-Host "rather than hidden: it is the only remaining evidence of what that seat was doing."
    exit 0
}

# ------------------------------------------------------------------------------------ declare
if ($Declare) {
    if ([string]::IsNullOrWhiteSpace($Seat)) { Fail "-Seat is required. A record with no seat cannot be grouped by seat." }
    if ([string]::IsNullOrWhiteSpace($Goal)) {
        Fail ("-Goal is required and NO MACHINE MAY SUPPLY IT. A goal this script invented would " +
            "produce a record that looks declared and says nothing, which is worse than no record: " +
            "an absent record prompts somebody to write one.")
    }

    $roster = Get-SeatsRoster
    $seatLower = $Seat.Trim().ToLowerInvariant()
    if ($roster) {
        $live = @($roster.live)
        if ($live -notcontains $seatLower) {
            $aliases = $roster.aliases
            if ($aliases.PSObject.Properties.Name -contains $seatLower) {
                $seatLower = $aliases.$seatLower
            }
            elseif ($roster.retired.PSObject.Properties.Name -contains $seatLower) {
                Fail "'$seatLower' is a RETIRED seat. $($roster.retired.$seatLower)"
            }
            else {
                Fail ("'$seatLower' is not a live seat. Live seats: $($live -join ', '). " +
                    "An unrecognised label is refused rather than recorded, because a roster of " +
                    "free-text labels cannot be grouped by seat and stops being an instrument.")
            }
        }
    }

    $existing = Read-Record
    Write-Record @{
        seat         = $seatLower
        goal         = $Goal
        done_when    = $Done
        out_of_scope = $OutOfScope
        handoff      = $Handoff
        worktree     = $myTree
        branch       = $branch
        session      = $sessionKey
        declared_at  = if ($existing -and $existing.PSObject.Properties['declared_at'] -and $existing.declared_at) { Get-StampString $existing.declared_at } else { Get-CcxMailStamp }
        updated_at   = Get-CcxMailStamp
        closed_at    = ''
    }

    # Collapse the role-card marker into the declaration. docs/ROLE-CARDS.md files this as the
    # cheaper end state than a fourth resolution rung that reads this record.
    $marker = Join-Path $myTree '.claude/seat.local.txt'
    try {
        $markerDir = Split-Path -Parent $marker
        if (-not (Test-Path -LiteralPath $markerDir)) { New-Item -ItemType Directory -Force -Path $markerDir | Out-Null }
        Set-Content -LiteralPath $marker -Value $seatLower -Encoding ascii -ErrorAction Stop
        Write-Host "seat marker written: .claude/seat.local.txt = $seatLower"
    }
    catch {
        Write-Host "NOTE: the record was written but the role-card marker was NOT ($($_.Exception.Message))."
        Write-Host "      Sessions here will start with no role card until it is set by hand."
    }

    Write-Host "declared: $seatLower in $(Split-Path -Leaf $myTree) on $branch"
    Write-Host "goal    : $Goal"
    Write-Host "record  : $recordPath"
    exit 0
}

# ------------------------------------------------------------------------------------- record
if ($Record) {
    # THE HOOK PATH. It updates what a machine can know and NEVER writes a goal. An existing
    # declaration is preserved exactly; an absent one stays absent and visibly so.
    $existing = Read-Record
    $fields = @{
        seat         = if ($existing -and $existing.PSObject.Properties['seat']) { [string]$existing.seat } else { '' }
        goal         = if ($existing -and $existing.PSObject.Properties['goal']) { [string]$existing.goal } else { '' }
        done_when    = if ($existing -and $existing.PSObject.Properties['done_when']) { [string]$existing.done_when } else { '' }
        out_of_scope = if ($existing -and $existing.PSObject.Properties['out_of_scope']) { [string]$existing.out_of_scope } else { '' }
        handoff      = if ($existing -and $existing.PSObject.Properties['handoff']) { [string]$existing.handoff } else { '' }
        worktree     = $myTree
        branch       = $branch
        session      = $sessionKey
        declared_at  = if ($existing -and $existing.PSObject.Properties['declared_at']) { Get-StampString $existing.declared_at } else { '' }
        updated_at   = Get-CcxMailStamp
        closed_at    = if ($existing -and $existing.PSObject.Properties['closed_at']) { Get-StampString $existing.closed_at } else { '' }
    }

    # If no marker exists but a seat was declared earlier, restore it. A worktree that lost its
    # marker otherwise runs without a role card while its own record says which seat it holds.
    if ($fields.seat) {
        $marker = Join-Path $myTree '.claude/seat.local.txt'
        if (-not (Test-Path -LiteralPath $marker)) {
            try {
                $markerDir = Split-Path -Parent $marker
                if (-not (Test-Path -LiteralPath $markerDir)) { New-Item -ItemType Directory -Force -Path $markerDir | Out-Null }
                Set-Content -LiteralPath $marker -Value $fields.seat -Encoding ascii -ErrorAction Stop
            }
            catch { }
        }
    }

    Write-Record $fields
    exit 0
}

# -------------------------------------------------------------------------------------- close
if ($Close) {
    $existing = Read-Record
    if (-not $existing) { Fail "no record for this session, so there is nothing to close." }
    $fields = @{}
    foreach ($prop in $existing.PSObject.Properties) {
        $fields[$prop.Name] = if ($prop.Name -like '*_at') { Get-StampString $prop.Value } else { $prop.Value }
    }
    $fields['closed_at'] = Get-CcxMailStamp
    $fields['updated_at'] = Get-CcxMailStamp
    Write-Record $fields
    Write-Host "closed: $recordPath"
    Write-Host "The record is KEPT. Closing says the episode ended, not that it never happened."
    exit 0
}
