#Requires -Version 7.3
<#
.SYNOPSIS
    Shared resolution for the session-mail lane. Dot-sourced by BOTH ends.

.DESCRIPTION
    THIS FILE EXISTS SO THE TWO ENDS CANNOT DISAGREE. docs/SESSION-MAIL.md step 2 asks for one
    function computing the box key, dot-sourced by the sender and the drain, because two ends that
    each compute a key will diverge and the divergence is SILENT: a message addressed to a peer's
    primary checkout instead of its worktree queued, reported success, and landed in a box nobody
    drains. Every observable said it had worked.

    STEP 0 IS THE WHOLE GUARANTEE. The promise is that both ends agree FROM THE SAME PATH. It says
    nothing about them starting from the same path, and by default they do not: `-To ..\peer` and a
    session launched in a subdirectory are both routine and neither is the recipient's own cwd. So
    every key resolves to the worktree ROOT first, and only then normalises and hashes.

    WHY THE QUEUE LIVES UNDER `.git`. Nothing there can enter a commit, and it is not a ref
    namespace, so `push --mirror` cannot carry it either. The leak guarantee is a property of the
    PATH, not of the design, and it does not survive moving the queue anywhere else.

    IT IS A MAIL ROOT OF ITS OWN, not the `ccx-coord` state root the coordination scripts use. The
    two have different lifetimes: coordination state is held state that must not expire, and a
    message is the one thing here that should.
#>

Set-StrictMode -Version Latest

#: The bounds the DRAIN enforces. They live here so the sender can report them, but the sender
#: never enforces them: whoever can write a file into an inbox never runs the sender's code.
$script:CcxMailBounds = @{
    MessagesPerInjection = 5
    BodyBytesRendered    = 2000
    BytesPerInjection    = 8000
    PerMessageFrame      = 560
    LineChars            = 240
    FromCwdChars         = 200
    FromBranchChars      = 120
    KindChars            = 16
}

#: docs/SESSION-MAIL.md step 6 asks for one number chosen against the moments delivery can happen,
#: which are SessionStart and Stop. The page measures both ends of the range: at 720 minutes an
#: ordinary overnight gap expired a real message, and at 4320 a three-day-old instruction still
#: refused to expire. 1440 clears an overnight gap with room to spare and still expires a weekend.
$script:CcxMailDefaultTtlMinutes = 1440

function Get-CcxMailGitCommonDir {
    <#
    .SYNOPSIS
        The clone's git common directory, or $null when the caller is not inside a clone.
    .DESCRIPTION
        Returning $null rather than throwing is deliberate. A session rooted at a directory that
        CONTAINS clones has no common dir, and that case must be reported rather than crashed on:
        the page records a container of ~25 clones where mail queued, nothing was ever delivered,
        and every send reported success. The silence was byte-identical to a healthy empty channel.
    #>
    [CmdletBinding()]
    param([string] $From)

    $target = if ($From) { $From } else { $PWD.Path }
    if (-not (Test-Path -LiteralPath $target)) { return $null }

    Push-Location -LiteralPath $target
    try {
        $common = (& git rev-parse --path-format=absolute --git-common-dir 2>$null)
        if ($LASTEXITCODE -ne 0 -or -not $common) { return $null }
        return $common.Trim()
    }
    finally { Pop-Location }
}

function Get-CcxMailRoot {
    <#
    .SYNOPSIS
        <git-common-dir>/mail, created on demand. $null when there is no clone to anchor to.
    .PARAMETER Anchor
        Names WHICH QUEUE to read, for a session outside a clone. It never answers which BOX --
        keep the box key a function of the session's own cwd, or an anchored session reads the
        anchor repository's mail.
    #>
    [CmdletBinding()]
    param([string] $Anchor, [switch] $NoCreate)

    $common = Get-CcxMailGitCommonDir -From $Anchor
    if (-not $common) { return $null }

    $root = Join-Path $common 'mail'
    if (-not $NoCreate -and -not (Test-Path -LiteralPath $root)) {
        New-Item -ItemType Directory -Force -Path $root -ErrorAction Stop | Out-Null
        New-Item -ItemType Directory -Force -Path (Join-Path $root 'tmp') -ErrorAction Stop | Out-Null
    }
    return $root
}

function Get-CcxMailWorktreeRoot {
    <#
    .SYNOPSIS
        STEP 0. Resolve any path to the worktree root that contains it, or $null.
    #>
    [CmdletBinding()]
    param([string] $Path)

    $target = if ($Path) { $Path } else { $PWD.Path }
    try { $target = (Resolve-Path -LiteralPath $target -ErrorAction Stop).Path }
    catch { return $null }

    if (Test-Path -LiteralPath $target -PathType Leaf) {
        $target = Split-Path -Parent $target
    }

    Push-Location -LiteralPath $target
    try {
        $top = (& git rev-parse --path-format=absolute --show-toplevel 2>$null)
        if ($LASTEXITCODE -ne 0 -or -not $top) { return $null }
        return $top.Trim()
    }
    finally { Pop-Location }
}

function Get-CcxMailAddressRoot {
    <#
    .SYNOPSIS
        The path a box is keyed on: the worktree root when there is one, else the directory itself.
    .DESCRIPTION
        WHY THE FALLBACK EXISTS. docs/SESSION-MAIL.md records a container holding roughly 25 clones
        being addressed: it has no common dir, so it is not a worktree. The page notes that the key
        "needed no change" for it, because step 2 keys on a NORMALIZED PATH HASH rather than a name,
        so the container gets a valid box with no code written. This function is that observation
        made explicit rather than accidental.

        A path that does not exist still returns $null. That distinction is the whole value: an
        unresolvable destination must FAIL LOUDLY at send time, because a message addressed to a
        path nobody drains queues, reports success, and is never delivered.
    #>
    [CmdletBinding()]
    param([string] $Path)

    $worktree = Get-CcxMailWorktreeRoot -Path $Path
    if ($worktree) { return $worktree }

    $target = if ($Path) { $Path } else { $PWD.Path }
    try { $resolved = (Resolve-Path -LiteralPath $target -ErrorAction Stop).Path }
    catch { return $null }
    if (Test-Path -LiteralPath $resolved -PathType Leaf) { $resolved = Split-Path -Parent $resolved }
    return $resolved
}

function ConvertTo-CcxMailComparablePath {
    <#
    .SYNOPSIS
        Normalise separators and trailing slash, and fold case ONLY where the filesystem does.
    #>
    [CmdletBinding()]
    param([string] $Path)

    if (-not $Path) { return '' }
    $p = ($Path -replace '/', '\').TrimEnd('\')
    if ($IsWindows) { $p = $p.ToLowerInvariant() }
    return $p
}

function Get-CcxMailBoxKey {
    <#
    .SYNOPSIS
        The box name for a worktree root: `<slug>-<hash16>`.
    .DESCRIPTION
        HASHED FOR INJECTIVITY, so two different paths can never land in one box. The slug is
        beside it ONLY so a human can tell boxes apart in a listing; nothing addresses by it.

        NOT KEYED ON A NAME OR A SESSION ID. A context clear re-mints the id and strands mail
        addressed to the old one. A name is a creation-time label nothing keeps current -- one
        worktree was observed on four branches in a single day.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory)][string] $WorktreeRoot)

    $norm = ConvertTo-CcxMailComparablePath $WorktreeRoot
    $sha = [System.Security.Cryptography.SHA256]::Create()
    try {
        $bytes = $sha.ComputeHash([System.Text.Encoding]::UTF8.GetBytes($norm))
        $hash = -join ($bytes[0..7] | ForEach-Object { $_.ToString('x2') })
    }
    finally { $sha.Dispose() }

    $leaf = Split-Path -Leaf $norm
    $slug = ($leaf -replace '[^A-Za-z0-9._-]', '-').Trim('-')
    if ($slug.Length -gt 24) { $slug = $slug.Substring(0, 24) }
    if (-not $slug) { $slug = 'tree' }

    return "$slug-$hash"
}

function Get-CcxMailBox {
    <#
    .SYNOPSIS
        The box directory for a worktree, with its four sub-directories, created on demand.
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)][string] $MailRoot,
        [Parameter(Mandatory)][string] $WorktreeRoot,
        [switch] $NoCreate
    )

    $box = Join-Path (Join-Path $MailRoot 'box') (Get-CcxMailBoxKey -WorktreeRoot $WorktreeRoot)
    if (-not $NoCreate) {
        foreach ($sub in 'inbox', 'claiming', 'seen', 'expired', 'shown', 'receipts') {
            $d = Join-Path $box $sub
            if (-not (Test-Path -LiteralPath $d)) {
                New-Item -ItemType Directory -Force -Path $d -ErrorAction Stop | Out-Null
            }
        }
    }
    return $box
}

function Test-CcxMailOff {
    <#
    .SYNOPSIS
        Is delivery suppressed? The OFF file's mere presence suppresses it for every worktree,
        WITHOUT losing what is queued.
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory)][string] $MailRoot)
    return (Test-Path -LiteralPath (Join-Path $MailRoot 'OFF'))
}

function Get-CcxMailStamp {
    <#
    .SYNOPSIS
        A round-trippable UTC stamp. Every observation carries its as-of time; an undated one reads
        as current and is not usable for anything.
    #>
    return [DateTimeOffset]::UtcNow.ToString('o')
}
