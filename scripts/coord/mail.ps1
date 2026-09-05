#Requires -Version 7.3
<#
.SYNOPSIS
    Session mail: send, list and inspect a file-drop queue that reaches a peer announce cannot.

.DESCRIPTION
    WHO NEEDS THIS. The realtime channel can LIST an editor-extension session or a session under a
    second Claude account, but it cannot SEND to either: delivery runs through a desktop-only map
    holding sessions that app itself spawned, under the account it authenticated against. A file
    drop is blind to both axes, which is the whole reason this lane is a file.

    QUEUED IS NOT DELIVERED, and this command reports that on every send. Delivery happens when the
    recipient's drain next runs. docs/SESSION-MAIL.md records an entire build in which every send
    reported success and nothing was ever delivered.

    THE LENGTH AND SHAPE CHECKS HERE ARE A COURTESY, NEVER A CONTROL. Whoever can write a file into
    an inbox never runs this script. Every binding cap belongs to scripts/hooks/mail-drain.ps1.

    NOTHING SENSITIVE GOES IN A BODY. Delivery copies it into the recipient's transcript, which no
    cleanup in this design reaches. The write side is unauthenticated by design: any process under
    this OS account can write any inbox, so every `from` field is an unverified self-assertion.

.PARAMETER To
    A path to the recipient's worktree, or `all`. Resolved to a worktree ROOT before addressing,
    so a relative path or a subdirectory of the recipient both land in the right box.

.PARAMETER Body
    Deliberately NOT [Parameter(Mandatory)]. A mandatory string parameter given "" throws a
    ParameterBindingException BEFORE the body runs, and docs/SESSION-MAIL.md records that throw
    landing in a bare catch and killing a diagnostic path. It is validated below instead.

.PARAMETER Anchor
    For a session outside a clone: names WHICH QUEUE to use. It never answers which box.

.EXAMPLE
    pwsh -NoProfile -File scripts/coord/mail.ps1 -Send -To ..\peer-worktree -Body "the ADR is 0161"
.EXAMPLE
    pwsh -NoProfile -File scripts/coord/mail.ps1 -List
#>

[CmdletBinding(DefaultParameterSetName = 'List')]
param(
    [Parameter(ParameterSetName = 'Send')][switch] $Send,
    [Parameter(ParameterSetName = 'Send')][string] $To,
    [Parameter(ParameterSetName = 'Send')][string] $Body,
    [Parameter(ParameterSetName = 'Send')][string] $Kind = 'note',
    [Parameter(ParameterSetName = 'Send')][int] $TtlMinutes = 0,
    [Parameter(ParameterSetName = 'List')][switch] $List,
    [Parameter(ParameterSetName = 'Status')][switch] $Status,
    [string] $Anchor
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

. (Join-Path $PSScriptRoot '_mail.ps1')

function Fail {
    param([string] $Message)
    Write-Host "mail: $Message"
    exit 1
}

$mailRoot = Get-CcxMailRoot -Anchor $Anchor
if (-not $mailRoot) {
    Fail ("not inside a git clone, so there is no queue to use. A directory that CONTAINS clones " +
        "has no common dir. Name the repository whose queue you mean:  -Anchor <path-to-clone>")
}

# ------------------------------------------------------------------------------------------ status
if ($Status) {
    Write-Host "mail root : $mailRoot"
    Write-Host "delivery  : $(if (Test-CcxMailOff -MailRoot $mailRoot) { 'OFF (suppressed; nothing is lost)' } else { 'on' })"
    Write-Host "default ttl: $script:CcxMailDefaultTtlMinutes minutes"
    Write-Host "as of     : $(Get-CcxMailStamp)"
    $boxDir = Join-Path $mailRoot 'box'
    $n = if (Test-Path -LiteralPath $boxDir) { @(Get-ChildItem -LiteralPath $boxDir -Directory).Count } else { 0 }
    Write-Host "boxes     : $n"
    exit 0
}

# -------------------------------------------------------------------------------------------- list
if (-not $Send) {
    $boxDir = Join-Path $mailRoot 'box'
    Write-Host "mail root : $mailRoot   (as of $(Get-CcxMailStamp))"
    if (-not (Test-Path -LiteralPath $boxDir)) { Write-Host "no boxes yet."; exit 0 }

    foreach ($b in (Get-ChildItem -LiteralPath $boxDir -Directory | Sort-Object Name)) {
        $inbox = Join-Path $b.FullName 'inbox'
        $queued = if (Test-Path -LiteralPath $inbox) { @(Get-ChildItem -LiteralPath $inbox -Filter '*.json' -File).Count } else { 0 }
        $seen = Join-Path $b.FullName 'seen'
        $done = if (Test-Path -LiteralPath $seen) { @(Get-ChildItem -LiteralPath $seen -Filter '*.json' -File).Count } else { 0 }
        Write-Host ("{0,-40} queued {1,3}   seen {2,3}" -f $b.Name, $queued, $done)
    }
    Write-Host ""
    Write-Host "Queued is NOT delivered. A message leaves an inbox when that recipient's drain runs."
    exit 0
}

# -------------------------------------------------------------------------------------------- send
if ([string]::IsNullOrWhiteSpace($Body)) {
    Fail "-Body is empty. A message with no body tells the recipient nothing; nothing was queued."
}
if ([string]::IsNullOrWhiteSpace($To)) {
    Fail "-To is empty. Give a path to the recipient's worktree, or 'all'."
}

# The sender's own identity, recorded as an UNVERIFIED self-assertion. The drain renders it as one.
$myTree = Get-CcxMailWorktreeRoot
$myBranch = ''
if ($myTree) {
    Push-Location -LiteralPath $myTree
    try { $myBranch = (& git rev-parse --abbrev-ref HEAD 2>$null); if ($myBranch) { $myBranch = $myBranch.Trim() } }
    finally { Pop-Location }
}

$targets = [System.Collections.Generic.List[string]]::new()
if ($To -eq 'all') {
    # Every worktree of THIS clone. The mail root is per-clone, so a box outside it is unreachable
    # through this root anyway -- which makes the clone's own worktree list the honest roster here.
    $anchorPath = if ($Anchor) { $Anchor } else { $PWD.Path }
    Push-Location -LiteralPath $anchorPath
    try {
        foreach ($line in (& git worktree list --porcelain 2>$null)) {
            if ($line -match '^worktree\s+(.+)$') {
                $wt = $Matches[1].Trim()
                if ($myTree -and (ConvertTo-CcxMailComparablePath $wt) -eq (ConvertTo-CcxMailComparablePath $myTree)) { continue }
                $targets.Add($wt)
            }
        }
    }
    finally { Pop-Location }
    if ($targets.Count -eq 0) { Fail "-To all matched no other worktree of this clone." }
}
else {
    $resolved = Get-CcxMailAddressRoot -Path $To
    if (-not $resolved) {
        Fail ("'$To' does not resolve to a git worktree, so nothing was queued. Addressing a path " +
            "that is not a worktree is how a message lands in a box nobody drains -- and every " +
            "observable reports success when it does.")
    }
    $targets.Add($resolved)
}

$ttl = if ($TtlMinutes -gt 0) { $TtlMinutes } else { $script:CcxMailDefaultTtlMinutes }
$tmpDir = Join-Path $mailRoot 'tmp'
if (-not (Test-Path -LiteralPath $tmpDir)) { New-Item -ItemType Directory -Force -Path $tmpDir | Out-Null }

$queuedTo = [System.Collections.Generic.List[string]]::new()
foreach ($target in $targets) {
    $box = Get-CcxMailBox -MailRoot $mailRoot -WorktreeRoot $target
    $stamp = [DateTimeOffset]::UtcNow.ToString('yyyyMMddTHHmmssfff')
    $name = "$stamp-$([guid]::NewGuid().ToString('n').Substring(0,8)).json"

    $record = [ordered]@{
        # The FILENAME is authoritative for identity. Nothing reads an id out of this record to
        # build a path with: an id used that way is a path-traversal primitive.
        sent_at     = Get-CcxMailStamp
        ttl_minutes = $ttl
        kind        = $Kind
        body        = $Body
        to          = [ordered]@{ worktree = $target }
        from        = [ordered]@{
            # UNVERIFIED. Any process under this OS account can write any inbox.
            cwd    = [string]$myTree
            branch = [string]$myBranch
        }
    } | ConvertTo-Json -Depth 6

    # Atomic publish: write to tmp, then move in one step, so no drain ever reads half a message.
    $staged = Join-Path $tmpDir $name
    Set-Content -LiteralPath $staged -Value $record -Encoding utf8NoBOM -ErrorAction Stop
    Move-Item -LiteralPath $staged -Destination (Join-Path (Join-Path $box 'inbox') $name) -ErrorAction Stop
    $queuedTo.Add((Split-Path -Leaf $box))
}

Write-Host "queued $($queuedTo.Count) message(s) at $(Get-CcxMailStamp)"
foreach ($b in $queuedTo) { Write-Host "  -> $b" }
Write-Host ""
Write-Host "QUEUED IS NOT DELIVERED. It sits in that inbox until the recipient's drain runs, which"
Write-Host "happens at that session's next SessionStart or Stop. Expires in $ttl minutes."
if (Test-CcxMailOff -MailRoot $mailRoot) {
    Write-Host "NOTE: delivery is currently OFF for this queue. Nothing is lost, but nothing renders."
}
exit 0
