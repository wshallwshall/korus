"""TEMPORARY diagnostic. Delete before this branch lands.

`test_an_anchor_names_which_queue_to_read` fails on gates (windows-latest) and nowhere
else. The drain reports an empty box for a message the send reported as delivered, which
is the byte-identical silence scripts/coord/_mail.ps1 was written after.

Canonicalising the non-worktree fallback of Get-CcxMailAddressRoot did not change it
(260f78c, reverted in 976c6e9). That rules the change out; it does not rule the box key
out, because nothing has yet printed what the two ends actually compute.

This prints it. The SENDER addresses `-To <root>` with the path Python hands it. The
DRAIN runs with that same directory as its working directory and computes its own
identity. If the two address roots or the two box keys differ, the key is the cause and
the difference names itself. If they agree, the key is exonerated and the fault is
downstream of it.

Fails on purpose so the values reach the CI log.
"""

import os
import subprocess
import tempfile
import unittest
from pathlib import Path

import _ccxtest as t

MAIL = Path(__file__).resolve().parents[1] / "scripts" / "coord" / "_mail.ps1"

# Print, from one pwsh process, what each end computes. CCX_PROBE_TO is the sender's -To
# string exactly as Python spells it; the process itself is started in that directory, so
# $PWD is what the drain sees. Passed by environment because `pwsh -Command` does not bind
# trailing arguments to $args, which silently emptied an earlier run of this probe.
SCRIPT = r"""
. $env:CCX_PROBE_MAIL
$toRaw = $env:CCX_PROBE_TO
$rootSend  = Get-CcxMailAddressRoot -Path $toRaw
$rootDrain = Get-CcxMailAddressRoot -Path $PWD.Path
$keySend   = if ($rootSend)  { Get-CcxMailBoxKey -WorktreeRoot $rootSend }  else { '<null>' }
$keyDrain  = if ($rootDrain) { Get-CcxMailBoxKey -WorktreeRoot $rootDrain } else { '<null>' }
"to (python spelling) = $toRaw"
"PWD.Path             = $($PWD.Path)"
"addressRoot(send)    = $rootSend"
"addressRoot(drain)   = $rootDrain"
"comparable(send)     = $(ConvertTo-CcxMailComparablePath -Path $rootSend)"
"comparable(drain)    = $(ConvertTo-CcxMailComparablePath -Path $rootDrain)"
"boxKey(send)         = $keySend"
"boxKey(drain)        = $keyDrain"
"ROOTS MATCH          = $($rootSend -eq $rootDrain)"
"KEYS MATCH           = $($keySend -eq $keyDrain)"
"""


class WhatEachEndComputesForOneDirectory(unittest.TestCase):
    def test_probe(self):
        pwsh = t.find_pwsh()
        if not pwsh:
            self.skipTest("pwsh is not on PATH")

        tmp = tempfile.TemporaryDirectory(prefix="ccx-boxprobe-")
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)

        # The failing case addresses the CONTAINER, which is not a worktree -- that is what
        # sends Get-CcxMailAddressRoot down its Resolve-Path fallback. A clone inside it
        # reproduces that shape.
        primary = root / "primary"
        primary.mkdir()
        subprocess.run(["git", "init", "-q", "-b", "main", str(primary)], capture_output=True)

        env = dict(os.environ, CCX_PROBE_TO=str(root), CCX_PROBE_MAIL=str(MAIL))
        r = subprocess.run(
            [pwsh, "-NoProfile", "-Command", SCRIPT],
            cwd=str(root), env=env, capture_output=True, text=True, timeout=120,
        )
        self.fail(
            "BOX PROBE (temporary, delete before landing)\n  "
            + "\n  ".join((r.stdout or "").strip().splitlines())
            + ("\n  STDERR: " + r.stderr.strip() if r.stderr.strip() else "")
        )


if __name__ == "__main__":
    unittest.main()
