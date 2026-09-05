#Requires -Version 7.3
<#
.SYNOPSIS
    PreToolUse guard: deny GitHub CLI commands that POLL in a loop and burn the shared API budget.

.DESCRIPTION
    POSTURE: FAILS OPEN. Any parse error, any missing dependency, any unexpected input exits 0 and
    allows the command. A guardrail must never wedge every `gh` call in the fleet.

    Reads the tool-call JSON on stdin. If a command watches a run in a polling loop it returns a
    PreToolUse `deny` NAMING THE SINGLE-SHOT REPLACEMENT. Anything else passes silently.

    WHY THIS IS A SHARED-RESOURCE PROBLEM AND NOT A STYLE ONE. Every seat here acts as the same
    GitHub identity, so all of them draw on ONE 5000-requests-per-hour budget. `gh run watch` polls
    every 3 seconds, which is about 1200 requests an hour from a SINGLE seat. Three seats watching
    runs exhaust the hour for everybody, and the failure then surfaces on some unrelated seat's next
    `gh` call as an opaque rate-limit error -- a cost paid by a session that did nothing wrong and
    cannot see the cause.

    THE REASON STRING NAMES THE REPLACEMENT, and that is not politeness. A denial that only forbids
    leaves the session to guess, and the guess is usually the same command with a flag moved.

    COMMAND ANALYSIS IS DELEGATED TO _command.ps1, which is what makes this safe to write. The
    splitter segments on shell separators and blanks inert quoted spans, so `gh` in COMMAND POSITION
    is decided by the segmentation rather than by an anchor pattern this file would have to get
    right. That matters here more than usual: a pattern for a claim also matches the sentence
    disclaiming it, so a naive spelling denies `echo "gh run watch is banned"` and blocks the
    writing of this very documentation. block-blanket-git-stage.ps1 records the same failure with
    `echo "git add -A"`, from before it moved to the shared splitter.

    The loop rule is the one exception to reading per-segment. `while ...; do gh ...; sleep 3; done`
    splits into segments that separate `gh` from `sleep`, so the loop shape is read from the WHOLE
    scannable command while the `gh` invocation is still required to be a real one.

    WIRING IS NOT ASSERTED HERE ON PURPOSE. Whether this script is referenced by a PreToolUse
    matcher is a property of a settings file, not of this script. .claude/settings.example.json in
    this checkout carries the row, with the path left as a loud placeholder to replace.

    Adopted from beads' block-gh-watch.sh, whose own comment records that `gh run watch`
    "repeatedly exhausted the quota during releases".
#>

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

try {
    . (Join-Path $PSScriptRoot '_command.ps1')
}
catch {
    [Console]::Error.WriteLine("[ccx] api-burn guard could not load _command.ps1; it is NOT enforcing.")
    exit 0
}

function Deny {
    param([string] $Reason)
    $payload = [pscustomobject]@{
        hookSpecificOutput = [pscustomobject]@{
            hookEventName            = 'PreToolUse'
            permissionDecision       = 'deny'
            permissionDecisionReason = $Reason
        }
    }
    [Console]::Out.Write(($payload | ConvertTo-Json -Compress -Depth 6))
    exit 0
}

try {
    $raw = [Console]::In.ReadToEnd()
    if (-not $raw) { exit 0 }

    $payload = $raw | ConvertFrom-Json
    $cmd = [string]$payload.tool_input.command
    if ([string]::IsNullOrWhiteSpace($cmd)) { exit 0 }

    $segments = @(Split-CcxCommand -Command $cmd)
    if (-not $segments) { exit 0 }

    # A `gh` invocation is a segment whose SCAN form starts with the `gh` token. Segmentation has
    # already stripped the separators and blanked quoted text, so no anchor pattern is needed and a
    # mention inside a string cannot reach this test.
    #
    # THE KEYWORD PREFIX IS NOT COSMETIC. The splitter cuts on `;`, so
    # `while true; do gh pr view 1; sleep 3; done` yields a segment reading `do gh pr view 1`, and a
    # bare `^gh` anchor misses every loop body -- which is to say it misses the exact shape this
    # guard exists for. Found by the must-trip arm; a suite of single commands would have shipped it.
    $ghSegments = @($segments | Where-Object { $_.Scan -match '^(?:(?:do|then|else|while|until)\s+)*gh(\s|$)' })
    if (-not $ghSegments) { exit 0 }

    foreach ($seg in $ghSegments) {
        $s = $seg.Scan

        if ($s -match '\brun\s+watch\b') {
            Deny (
                "BLOCKED: 'gh run watch' polls every 3 seconds, about 1200 of the 5000 hourly " +
                "GitHub API requests, and every seat here shares ONE budget as the same identity. " +
                "Read once instead: 'gh run view <run-id>' for status now, or " +
                "'gh run list --branch <branch> --limit 5 --json status,conclusion,createdAt' for " +
                "the branch. To wait, sleep once and then read once. Never poll."
            )
        }

        if ($s -match '(^|\s)--watch(\s|$)') {
            Deny (
                "BLOCKED: a '--watch' flag on a 'gh' command polls in a loop and draws on the " +
                "shared 5000/hr GitHub API budget. Drop it and read once. For a run: " +
                "'gh run view <run-id>'. For a PR's checks: 'gh pr checks <N>' or " +
                "'gh pr view <N> --json statusCheckRollup'."
            )
        }
    }

    # A hand-rolled poll loop costs the same as the flag, and it is exactly what gets written the
    # moment the two rules above deny. Read the loop shape from the whole command, because splitting
    # separates the `gh` call from the `sleep` that paces it.
    $whole = ($segments | ForEach-Object { $_.Scan }) -join ' ; '
    if ($whole -match '\b(while|until|for)\b' -and $whole -match '\bsleep\b') {
        Deny (
            "BLOCKED: this is a hand-rolled polling loop around 'gh', which costs the shared " +
            "GitHub API budget the same way 'gh run watch' does. Make ONE call per turn and let " +
            "the next turn make the next one. If you must wait inside a turn, sleep once and read " +
            "once. Do not loop."
        )
    }

    exit 0
}
catch {
    # Fail open, always.
    exit 0
}
