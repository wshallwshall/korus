"""The api-burn guard denies `gh` polling loops, and denies nothing else.

WHAT THIS EXISTS FOR. Every seat here acts as ONE GitHub identity against ONE 5000-requests-per-hour
budget. `gh run watch` polls every 3 seconds, about 1200 requests an hour from a single seat. The
seat that pays is not the seat that spent: the budget runs out and some unrelated session's next
`gh` call fails with an opaque rate-limit error it cannot trace.

WHY THE ARMS ARE DISJOINT AND BOTH ARE REQUIRED. A guard is two claims, and a suite that tests one
of them is worth very little. MUST_TRIP alone passes for a guard that denies everything.
MUST_NOT_TRIP alone passes for a guard that denies nothing. Only the pair pins the boundary, and
only re-running BOTH after a pattern change catches an over-correction.

THE FALSE POSITIVE THIS FILE IS REALLY ABOUT. A pattern for a claim also matches the sentence
disclaiming it. A first draft of the upstream guard denied `echo "gh run watch is banned"` -- it
would have blocked the writing of its own documentation. This repository has the same scar in a
different gate: `scripts/hooks/block-blanket-git-stage.ps1` records that `echo "git add -A"` was a
deny before it moved to the shared splitter. Both are in MUST_NOT_TRIP below, because the fix is
structural -- `_command.ps1` blanks inert quoted spans -- and a structural fix that nothing tests
is one refactor from being lost.
"""

import json
import subprocess
import unittest

import _ccxtest as t

TIMEOUT_SECONDS = 120
GUARD = t.REPO_ROOT / "scripts" / "hooks" / "block-api-burn.ps1"

#: Each of these MUST be denied. The comment says which cost it is buying back.
MUST_TRIP = [
    ("gh run watch", "the measured 1200/hr offender"),
    ("gh run watch 12345", "same, with a run id"),
    ("gh run watch --exit-status", "same, with a flag"),
    ("gh pr checks 5 --watch", "the same loop wearing a flag"),
    ("gh run list --watch", "--watch on another subcommand"),
    ("while true; do gh pr view 1; sleep 3; done", "a hand-rolled poll loop"),
    ("until gh run view 9 --json conclusion; do sleep 5; done", "the same loop, spelled with until"),
    ('bash -c "gh run watch"', "the same command behind an interpreter"),
    ("cd /tmp && gh run watch", "after a separator, which is still command position"),
]

#: Each of these MUST be allowed. Anything here that starts failing is an OVER-CORRECTION, which is
#: the expensive direction: a gate that denies ordinary work trains sessions to route around it.
MUST_NOT_TRIP = [
    ('echo "gh run watch is banned"', "THE ONE THAT MATTERS. Documenting the rule is not breaking it"),
    ('echo "do not use gh pr checks --watch"', "same, for the flag"),
    ("gh run view 12345", "the single-shot replacement the denial recommends"),
    ("gh run list --branch main --limit 5", "a single-shot list"),
    ("gh pr checks 5", "checks WITHOUT the flag"),
    ("gh pr view 48 --json statusCheckRollup", "the recommended rollup read"),
    ("gh pr comment 48 --body-file x.md", "an ordinary gh write"),
    ("git add README.md", "not a gh command at all"),
    ("sleep 3", "a bare sleep with no gh anywhere"),
    ("while true; do echo tick; sleep 1; done", "a poll loop that never calls gh"),
    ("for f in *.md; do wc -l $f; done", "a loop with no gh and no sleep"),
    ('grep -r "watch" docs/', "the word watch in an unrelated command"),
]


def _decision(result: subprocess.CompletedProcess) -> str | None:
    """The permissionDecision, or None when the guard stayed silent (which means allow)."""
    out = (result.stdout or "").strip()
    if not out:
        return None
    try:
        return json.loads(out)["hookSpecificOutput"]["permissionDecision"]
    except (ValueError, KeyError):
        return None


class TheGuardDeniesPollingAndNothingElse(unittest.TestCase):
    def setUp(self):
        pwsh = t.find_pwsh()
        if not pwsh:
            self.skipTest("pwsh is not on PATH, so the guard cannot be executed here")
        self.pwsh: str = pwsh

    def run_guard(self, command: str) -> subprocess.CompletedProcess:
        payload = {"tool_name": "Bash", "tool_input": {"command": command}}
        return subprocess.run(
            [self.pwsh, "-NoProfile", "-File", str(GUARD)],
            input=json.dumps(payload),
            capture_output=True,
            text=True,
            cwd=str(t.REPO_ROOT),
            timeout=TIMEOUT_SECONDS,
        )

    def test_every_polling_command_is_denied(self):
        for command, why in MUST_TRIP:
            with self.subTest(command=command):
                r = self.run_guard(command)
                self.assertEqual(0, r.returncode, f"the guard must always exit 0. stderr: {r.stderr}")
                self.assertEqual("deny", _decision(r), f"NOT denied, and it buys back: {why}")

    def test_no_ordinary_command_is_denied(self):
        for command, why in MUST_NOT_TRIP:
            with self.subTest(command=command):
                r = self.run_guard(command)
                self.assertEqual(0, r.returncode, f"the guard must always exit 0. stderr: {r.stderr}")
                self.assertIsNone(_decision(r), f"OVER-CORRECTION. This must be allowed because: {why}")

    def test_the_two_arms_are_disjoint(self):
        """A command in both arms would make the suite pass whatever the guard does."""
        overlap = {c for c, _ in MUST_TRIP} & {c for c, _ in MUST_NOT_TRIP}
        self.assertEqual(set(), overlap, f"a command is in both arms: {overlap}")

    def test_both_arms_are_populated(self):
        """The empty-corpus guard. Either arm emptied would pass while measuring nothing."""
        self.assertGreaterEqual(len(MUST_TRIP), 5)
        self.assertGreaterEqual(len(MUST_NOT_TRIP), 5)

    def test_every_denial_names_a_replacement(self):
        """A denial that only forbids leaves the session to guess, and the guess is the same
        command with a flag moved. Every reason must hand back a command that does the job."""
        for command, _ in MUST_TRIP:
            with self.subTest(command=command):
                out = json.loads(self.run_guard(command).stdout)
                reason = out["hookSpecificOutput"]["permissionDecisionReason"]
                self.assertIn("gh ", reason, "the denial reason names no replacement command")


class TheGuardFailsOpen(unittest.TestCase):
    """A broken guard must never wedge every gh call. Each of these exits 0 and denies nothing."""

    def setUp(self):
        pwsh = t.find_pwsh()
        if not pwsh:
            self.skipTest("pwsh is not on PATH, so the guard cannot be executed here")
        self.pwsh: str = pwsh

    def run_raw(self, stdin_text: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [self.pwsh, "-NoProfile", "-File", str(GUARD)],
            input=stdin_text,
            capture_output=True,
            text=True,
            cwd=str(t.REPO_ROOT),
            timeout=TIMEOUT_SECONDS,
        )

    def test_empty_input_allows(self):
        r = self.run_raw("")
        self.assertEqual(0, r.returncode)
        self.assertIsNone(_decision(r))

    def test_junk_input_allows(self):
        r = self.run_raw("this is not json at all {{{")
        self.assertEqual(0, r.returncode)
        self.assertIsNone(_decision(r))

    def test_a_payload_with_no_command_allows(self):
        r = self.run_raw(json.dumps({"tool_name": "Bash", "tool_input": {}}))
        self.assertEqual(0, r.returncode)
        self.assertIsNone(_decision(r))

    def test_a_whitespace_command_allows(self):
        r = self.run_raw(json.dumps({"tool_input": {"command": "   "}}))
        self.assertEqual(0, r.returncode)
        self.assertIsNone(_decision(r))


class TheGuardReusesTheSharedSplitter(unittest.TestCase):
    """Pinned at the source, not only in behaviour.

    The quoted-span defence is a property of `_command.ps1`. A future edit that reintroduces a local
    regex would pass every behavioural test above that happens to be spelled the same way, and lose
    the interpreter recursion and the separator handling silently.
    """

    def test_it_dot_sources_the_shared_splitter(self):
        self.assertIn("_command.ps1", t.read(GUARD))

    def test_it_calls_split_ccx_command(self):
        self.assertIn("Split-CcxCommand", t.strip_ps_comments(t.read(GUARD)))

    def test_it_declares_its_posture(self):
        self.assertIn("FAILS OPEN", t.read(GUARD))


if __name__ == "__main__":
    unittest.main()
