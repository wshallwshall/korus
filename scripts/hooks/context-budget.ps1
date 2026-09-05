#Requires -Version 7.3
<#
.SYNOPSIS
    UserPromptSubmit hook: report how much of THIS SESSION'S CONTEXT WINDOW is spent.

.DESCRIPTION
    POSTURE: FAILS OPEN, AND NEVER BLOCKS. Any parse error, any missing transcript, any unexpected
    shape exits 0 in silence.

    Reads the tool-call JSON on stdin, opens the transcript the harness names there, and takes the
    token counts from the last assistant message's usage object.

    WHAT THIS MEASURES, AND WHAT IT DOES NOT. This is the CONTEXT WINDOW of one session: how full
    the conversation is. It is NOT account pool headroom, which is the Steward's quantity. Both get
    called "usage" and they are different numbers. A seat with a fresh pool can still be one turn
    from a compaction, and a seat with plenty of window can be on an exhausted account.

    WHY A BUILDER NEEDS IT. A Builder gets one turn and cannot ask for another. The working
    agreement tells a session not to grind on in a polluted context, but nothing tells it the
    context IS polluted, so the rule has no trigger. This is the trigger.

    IT REPORTS AND NEVER BLOCKS. The upstream guard hard-gates named roles at the top threshold. A
    Builder blocked at its own prompt has no next turn in which to be told why, so blocking burns
    the brief rather than saving it. The decision to stop belongs to the seat reading the warning.

    IT REFUSES TO PRINT A FIGURE IT CANNOT TRUST. The window size is a DEFAULT, not a reading.
    Nothing in the transcript states the real window, and it varies by model and deployment. When
    the count exceeds the assumed ceiling, the ceiling is what failed, not the arithmetic. The first
    version of this shipped without that branch and reported "172.9% spent" to its own author within
    the hour. It was caught only because the number was impossible: had the real window been 250k it
    would have printed something wrong and plausible, and been believed.

    WIRING IS NOT ASSERTED HERE ON PURPOSE. Whether this script is referenced by a
    UserPromptSubmit matcher is a property of a settings file, not of this script.

    Adopted from gastown's context-budget-guard.sh. The thresholds are theirs, so they carry a
    provenance rather than being invented here. See docs/HOOKS.md for the event map.
#>

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Get-Threshold {
    param([string] $Name, [double] $Default)
    $v = [Environment]::GetEnvironmentVariable($Name)
    if (-not $v) { return $Default }
    $parsed = 0.0
    if ([double]::TryParse($v, [ref]$parsed) -and $parsed -gt 0 -and $parsed -le 1) { return $parsed }
    return $Default
}

function Write-Context {
    param([string] $Text)
    $payload = [pscustomobject]@{
        hookSpecificOutput = [pscustomobject]@{
            hookEventName     = 'UserPromptSubmit'
            additionalContext = $Text
        }
    }
    [Console]::Out.Write(($payload | ConvertTo-Json -Compress -Depth 6))
}

try {
    if ($env:KORUS_CONTEXT_BUDGET_DISABLE -eq '1') { exit 0 }

    $warn = Get-Threshold 'KORUS_CONTEXT_BUDGET_WARN' 0.75
    $soft = Get-Threshold 'KORUS_CONTEXT_BUDGET_SOFT' 0.85
    $hard = Get-Threshold 'KORUS_CONTEXT_BUDGET_HARD' 0.92

    $maxTokens = 200000
    if ($env:KORUS_CONTEXT_BUDGET_MAX_TOKENS) {
        $parsed = 0
        if ([int]::TryParse($env:KORUS_CONTEXT_BUDGET_MAX_TOKENS, [ref]$parsed) -and $parsed -gt 0) {
            $maxTokens = $parsed
        }
    }

    $raw = [Console]::In.ReadToEnd()
    if (-not $raw) { exit 0 }
    $payloadIn = $raw | ConvertFrom-Json

    # An explicit override exists so the hook can be exercised without a transcript, and so a caller
    # that already knows the count does not pay for a re-parse.
    $used = 0
    if ($env:KORUS_CONTEXT_BUDGET_TOKENS) {
        $parsed = 0
        if ([int]::TryParse($env:KORUS_CONTEXT_BUDGET_TOKENS, [ref]$parsed)) { $used = $parsed }
    }

    if ($used -le 0) {
        $tp = [string]$payloadIn.transcript_path
        if (-not $tp -or -not (Test-Path -LiteralPath $tp)) { exit 0 }

        # WALK BACKWARDS. The last assistant message carries the running total, so reading forward
        # and keeping the last hit costs the whole transcript on every prompt. A long session's
        # transcript runs to tens of megabytes and this hook runs on every turn.
        $lines = [System.IO.File]::ReadAllLines($tp)
        for ($i = $lines.Length - 1; $i -ge 0; $i--) {
            $line = $lines[$i]
            if (-not $line -or $line -notmatch '"usage"') { continue }
            try { $rec = $line | ConvertFrom-Json } catch { continue }
            $u = $rec.message.usage
            if (-not $u) { continue }
            # input_tokens EXCLUDES the cached prefix, and on a long session the cache IS most of
            # the window. Reading input alone makes the fullest sessions look nearly empty, which is
            # the exact opposite of what this hook is for. Sum all four.
            foreach ($f in 'input_tokens', 'cache_read_input_tokens', 'cache_creation_input_tokens', 'output_tokens') {
                $prop = $u.PSObject.Properties[$f]
                if ($prop -and $prop.Value) { $used += [int]$prop.Value }
            }
            if ($used -gt 0) { break }
        }
    }

    if ($used -le 0) { exit 0 }

    $frac = [double]$used / [double]$maxTokens
    $windowK = [int]($maxTokens / 1000)

    # THE DENOMINATOR IS AN ASSUMPTION AND IT CAN BE WRONG. See the header: an impossible percentage
    # is visible, a merely wrong one is believed. Report the absolute figure and name the fix.
    if ($frac -gt 1.0) {
        $k = [math]::Round($used / 1000.0, 1)
        Write-Context (
            "[context-budget] CEILING WRONG, and this is not a reading. This session reports about " +
            "${k}k tokens against an assumed ${windowK}k window, which is impossible as a " +
            "percentage -- so the assumed window is wrong for this model, not the count. No " +
            "fullness figure is given, because none can be trusted. The session IS large, and that " +
            "is the signal. Set KORUS_CONTEXT_BUDGET_MAX_TOKENS to this model's real window to " +
            "restore the gauge."
        )
        exit 0
    }

    if ($frac -lt $warn) { exit 0 }

    $pct = [math]::Round($frac * 100, 1)
    $k = [math]::Round($used / 1000.0, 1)

    if ($frac -ge $hard) {
        $level = 'HARD'
        $advice = 'Stop taking new work. Push what is green, write the PR body, and say in it what is unfinished. A fresh seat with a better brief beats one more turn here.'
    }
    elseif ($frac -ge $soft) {
        $level = 'SOFT'
        $advice = 'Finish the change in hand and push. Do not start a new line of investigation in this session.'
    }
    else {
        $level = 'WARN'
        $advice = 'Land what you can before a compaction. A compaction drops the seat, the goal and the brief, and nothing re-declares them for you.'
    }

    Write-Context (
        "[context-budget] $level -- this session's CONTEXT WINDOW is ${pct}% spent (about ${k}k of " +
        "${windowK}k tokens). $advice This is the conversation's own window, NOT account pool " +
        "headroom, which is the Steward's number. A full pool does not buy room here."
    )
    exit 0
}
catch {
    # Fail open, always. See the header.
    exit 0
}
