"""The context-budget hook reports window fullness, and refuses to report a figure it cannot trust.

WHAT THIS EXISTS FOR. A Builder gets one turn and cannot ask for another. The working agreement
tells a session not to grind on in a polluted context, but nothing tells it the context IS polluted.
This hook is that trigger.

THE TEST THAT MATTERS MOST IS `TheCeilingIsAnAssumptionAndSaysSo`. The window size is a DEFAULT,
not a reading: nothing in the transcript states it, and it varies by model. The first version of
this hook upstream shipped without that branch and reported "172.9% spent" to its own author within
the hour. It was caught ONLY because the number was impossible. Had the real window been 250k it
would have printed something wrong and plausible, and nobody would have looked. So the branch that
refuses to divide is the one under test here, not the arithmetic that works.

THE SECOND THING PINNED IS THAT IT NEVER BLOCKS. The upstream guard hard-gates named roles at the
top threshold. A Builder blocked at its own prompt has no next turn in which to be told why, so
blocking burns the brief rather than saving it. Every assertion below checks for
`additionalContext` and no `permissionDecision`.
"""

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

import _ccxtest as t

TIMEOUT_SECONDS = 120
HOOK = t.REPO_ROOT / "scripts" / "hooks" / "context-budget.ps1"

WINDOW = 200_000


def _context(result: subprocess.CompletedProcess) -> str | None:
    out = (result.stdout or "").strip()
    if not out:
        return None
    try:
        return json.loads(out)["hookSpecificOutput"]["additionalContext"]
    except (ValueError, KeyError):
        return None


def _ctx(result: subprocess.CompletedProcess) -> str:
    """The context text, required to be present. Use where the test inspects the text itself."""
    out = _context(result)
    if out is None:
        raise AssertionError("the hook stayed silent, but this test needs it to report")
    return out


class _HookCase(unittest.TestCase):
    def setUp(self):
        pwsh = t.find_pwsh()
        if not pwsh:
            self.skipTest("pwsh is not on PATH, so the hook cannot be executed here")
        self.pwsh: str = pwsh

    def run_hook(self, *, tokens=None, stdin=None, max_tokens=None, extra_env=None):
        env = dict(os.environ)
        for k in list(env):
            if k.startswith("KORUS_CONTEXT_BUDGET"):
                del env[k]
        if tokens is not None:
            env["KORUS_CONTEXT_BUDGET_TOKENS"] = str(tokens)
        if max_tokens is not None:
            env["KORUS_CONTEXT_BUDGET_MAX_TOKENS"] = str(max_tokens)
        if extra_env:
            env.update(extra_env)
        return subprocess.run(
            [self.pwsh, "-NoProfile", "-File", str(HOOK)],
            input="{}" if stdin is None else stdin,
            capture_output=True,
            text=True,
            env=env,
            cwd=str(t.REPO_ROOT),
            timeout=TIMEOUT_SECONDS,
        )


class TheLadderFiresAtItsThresholds(_HookCase):
    #: (fraction of the window, the level it must report)
    LADDER = [
        (0.50, None),
        (0.74, None),
        (0.76, "WARN"),
        (0.84, "WARN"),
        (0.86, "SOFT"),
        (0.91, "SOFT"),
        (0.93, "HARD"),
        (0.99, "HARD"),
    ]

    def test_each_rung_reports_its_level(self):
        for frac, expected in self.LADDER:
            with self.subTest(fraction=frac):
                r = self.run_hook(tokens=int(WINDOW * frac))
                self.assertEqual(0, r.returncode, r.stderr)
                ctx = _context(r)
                if expected is None:
                    self.assertIsNone(ctx, f"{frac} is below the warn threshold and must stay silent")
                else:
                    self.assertIsNotNone(ctx, f"{frac} must report {expected}")
                    assert ctx is not None  # narrows for the type checker; the line above is the test
                    self.assertIn(expected, ctx)

    def test_the_ladder_covers_silence_and_all_three_levels(self):
        """A ladder missing a rung would pass while measuring only the rungs it kept."""
        self.assertEqual({None, "WARN", "SOFT", "HARD"}, {lvl for _, lvl in self.LADDER})

    def test_it_never_blocks(self):
        """Reporting is the whole design. A permissionDecision here would burn a Builder's brief."""
        for frac, expected in self.LADDER:
            if expected is None:
                continue
            with self.subTest(fraction=frac):
                out = json.loads(self.run_hook(tokens=int(WINDOW * frac)).stdout)
                self.assertNotIn("permissionDecision", json.dumps(out))

    def test_a_reported_figure_carries_its_absolute_count(self):
        """A percentage with no absolute number beside it cannot be checked against anything."""
        ctx = _ctx(self.run_hook(tokens=int(WINDOW * 0.9)))
        self.assertIn("k of", ctx)

    def test_it_distinguishes_the_window_from_pool_headroom(self):
        """Both get called 'usage'. A seat with a fresh pool can still be one turn from compaction."""
        ctx = _ctx(self.run_hook(tokens=int(WINDOW * 0.9)))
        self.assertIn("NOT account pool headroom", ctx)


class TheCeilingIsAnAssumptionAndSaysSo(_HookCase):
    """The branch that exists because a real one shipped wrong and was believed for an hour."""

    def test_over_the_ceiling_it_refuses_to_give_a_percentage(self):
        ctx = _ctx(self.run_hook(tokens=int(WINDOW * 1.73)))
        self.assertIsNotNone(ctx, "an over-ceiling count must still say something")
        self.assertNotIn("%", ctx, "it printed a percentage of a denominator it does not trust")

    def test_over_the_ceiling_it_names_the_ceiling_as_the_fault(self):
        ctx = _ctx(self.run_hook(tokens=int(WINDOW * 1.73)))
        self.assertIn("CEILING WRONG", ctx)

    def test_over_the_ceiling_it_still_reports_the_absolute_size(self):
        """The session IS large. Losing the gauge must not lose the signal."""
        ctx = _ctx(self.run_hook(tokens=int(WINDOW * 1.73)))
        self.assertIn("346k", ctx)

    def test_over_the_ceiling_it_names_the_setting_that_fixes_it(self):
        ctx = _ctx(self.run_hook(tokens=int(WINDOW * 1.73)))
        self.assertIn("KORUS_CONTEXT_BUDGET_MAX_TOKENS", ctx)

    def test_a_corrected_ceiling_restores_the_gauge(self):
        """The control for the four tests above: with a right ceiling the same count is ordinary."""
        ctx = _ctx(self.run_hook(tokens=int(WINDOW * 1.73), max_tokens=400_000))
        self.assertIsNotNone(ctx)
        self.assertNotIn("CEILING WRONG", ctx)
        self.assertIn("%", ctx)


class TheHookFailsOpen(_HookCase):
    def test_empty_stdin_is_silent(self):
        r = self.run_hook(stdin="")
        self.assertEqual(0, r.returncode)
        self.assertIsNone(_context(r))

    def test_junk_stdin_is_silent(self):
        r = self.run_hook(stdin="not json {{{")
        self.assertEqual(0, r.returncode)
        self.assertIsNone(_context(r))

    def test_a_missing_transcript_is_silent(self):
        r = self.run_hook(stdin=json.dumps({"transcript_path": "X:/nope/does-not-exist.jsonl"}))
        self.assertEqual(0, r.returncode)
        self.assertIsNone(_context(r))

    def test_no_transcript_path_is_silent(self):
        r = self.run_hook(stdin=json.dumps({"session_id": "abc"}))
        self.assertEqual(0, r.returncode)
        self.assertIsNone(_context(r))

    def test_the_disable_switch_silences_it(self):
        r = self.run_hook(tokens=int(WINDOW * 0.99), extra_env={"KORUS_CONTEXT_BUDGET_DISABLE": "1"})
        self.assertEqual(0, r.returncode)
        self.assertIsNone(_context(r))


class ItReadsATranscriptAndSumsTheCachedPrefix(_HookCase):
    """input_tokens alone makes the FULLEST sessions look nearly empty, because on a long session
    the cached prefix is most of the window. That is the exact inversion this hook exists to avoid,
    so the sum is tested against a transcript rather than only through the override."""

    def write_transcript(self, usage: dict) -> str:
        tmp = tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False, encoding="utf-8")
        self.addCleanup(lambda: Path(tmp.name).unlink(missing_ok=True))
        tmp.write(json.dumps({"type": "user", "message": {"content": "hi"}}) + "\n")
        tmp.write(json.dumps({"type": "assistant", "message": {"usage": usage}}) + "\n")
        tmp.close()
        return tmp.name

    def test_it_sums_all_four_token_fields(self):
        path = self.write_transcript(
            {
                "input_tokens": 1_000,
                "cache_read_input_tokens": 170_000,
                "cache_creation_input_tokens": 5_000,
                "output_tokens": 2_000,
            }
        )
        ctx = _ctx(self.run_hook(stdin=json.dumps({"transcript_path": path})))
        self.assertIsNotNone(ctx, "178k of 200k is 89% and must report")
        self.assertIn("SOFT", ctx)

    def test_input_tokens_alone_would_have_read_as_empty(self):
        """The control. The same record with only input_tokens is 0.5% and stays silent, which is
        what the naive read would have reported for the session above."""
        path = self.write_transcript({"input_tokens": 1_000})
        self.assertIsNone(_context(self.run_hook(stdin=json.dumps({"transcript_path": path}))))


if __name__ == "__main__":
    unittest.main()
