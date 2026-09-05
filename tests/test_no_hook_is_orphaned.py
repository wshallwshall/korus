"""Every hook script is wired somewhere, or is named as deliberately unwired.

WHAT THIS EXISTS FOR. An unwired hook passes every other assertion in this suite VACUOUSLY. Its
unit tests run it directly, so they stay green forever while the hook decides nothing for anybody.
Nothing else here can tell the difference between a guard that is enforcing and a guard that was
written, tested, committed, and never referenced by a matcher.

That is not hypothetical in this repository. `scripts/hooks/seq_check.py` is a fail-closed gate that
NO INSTALLER WIRES, and `docs/HOOKS.md` has to say so in prose because nothing enforced it.

THE UNWIRED LIST IS THE POINT, NOT AN ESCAPE HATCH. A hook may legitimately be unwired -- opt-in,
superseded, or deliberately manual. What may not happen is that nobody notices. Adding a name below
costs a sentence saying why, which is the whole mechanism: the choice becomes visible instead of
being the default.

THIS FILE MUST BE MUTATION-TESTED, and `TheCheckHasPower` is that. A wiring check that cannot fail
is worse than no check, because it reports agreement. The class below removes a real wiring from a
copy of the settings and requires the orphan check to name that exact file.
"""

import json
import re
import unittest

import _ccxtest as t

HOOKS_DIR = t.REPO_ROOT / "scripts" / "hooks"
SETTINGS_EXAMPLE = t.REPO_ROOT / ".claude" / "settings.example.json"

#: Scripts that install a hook into somebody's settings. A hook named in one of these is wired.
INSTALLERS = (
    t.REPO_ROOT / "scripts" / "coord" / "install-coordination.ps1",
    t.REPO_ROOT / "scripts" / "worktree" / "install-gate.ps1",
    t.REPO_ROOT / "scripts" / "worktree" / "install-selfheal.ps1",
)

#: Deliberately unwired, each with the reason. A name here is a decision, not an oversight.
UNWIRED = {
    "steer-inject.ps1": (
        "Opt-in. It delivers a queued steering note and matches every tool call, so it costs a "
        "pwsh spawn per call and is wired by hand only when someone is steering a session. "
        "docs/HOOKS.md marks it opt-in in the event map."
    ),
}


def hook_scripts() -> list[str]:
    """PowerShell hooks, excluding the `_`-prefixed shared helpers, which are dot-sourced."""
    return sorted(p.name for p in HOOKS_DIR.glob("*.ps1") if not p.name.startswith("_"))


def wired_names(settings_text: str) -> set[str]:
    """Every `*.ps1` basename referenced by the example settings or by any installer."""
    found = set(re.findall(r"([A-Za-z0-9_.-]+\.ps1)", settings_text))
    for installer in INSTALLERS:
        if installer.is_file():
            found |= set(re.findall(r"([A-Za-z0-9_.-]+\.ps1)", t.read(installer)))
    return found


class NoHookIsOrphaned(unittest.TestCase):
    def test_every_hook_is_wired_or_declared_unwired(self):
        wired = wired_names(t.read(SETTINGS_EXAMPLE))
        orphans = [h for h in hook_scripts() if h not in wired and h not in UNWIRED]
        self.assertEqual(
            [],
            orphans,
            f"these hook scripts are referenced by no matcher and named in no unwired list: "
            f"{orphans}. An unwired hook passes its own unit tests forever while deciding nothing. "
            f"Wire it, or add it to UNWIRED in this file with the reason.",
        )

    def test_the_unwired_list_names_only_hooks_that_exist(self):
        """A stale exemption silently re-opens the gap it was written to declare."""
        stale = sorted(set(UNWIRED) - set(hook_scripts()))
        self.assertEqual([], stale, f"UNWIRED names scripts that are not there: {stale}")

    def test_every_unwired_entry_carries_a_reason(self):
        reasonless = sorted(k for k, v in UNWIRED.items() if len(str(v).strip()) < 40)
        self.assertEqual([], reasonless, f"unwired without a real reason: {reasonless}")

    def test_the_scan_actually_finds_hooks(self):
        """The empty-corpus guard. With no hooks found, the orphan list is empty and means nothing."""
        self.assertGreaterEqual(len(hook_scripts()), 5, f"only found {hook_scripts()}")

    def test_the_example_settings_parse(self):
        """A settings file that does not parse wires nothing, and would read as 'no orphans'."""
        self.assertIsInstance(json.loads(t.read(SETTINGS_EXAMPLE)), dict)


class TheCheckHasPower(unittest.TestCase):
    """The mutation test. Without it, a check that never fails would report agreement forever."""

    def test_removing_a_wiring_makes_the_check_name_that_hook(self):
        text = t.read(SETTINGS_EXAMPLE)
        target = "block-api-burn.ps1"
        self.assertIn(target, text, "the mutation target is not wired, so this proves nothing")

        mutated = text.replace(target, "REMOVED-BY-MUTATION-TEST.ps1")
        wired = wired_names(mutated)
        orphans = [h for h in hook_scripts() if h not in wired and h not in UNWIRED]
        self.assertIn(target, orphans, "unwiring a hook did NOT red the orphan check")

    def test_the_unmutated_settings_have_no_orphans(self):
        """The other half. The mutation above means nothing if the baseline is already red."""
        wired = wired_names(t.read(SETTINGS_EXAMPLE))
        self.assertEqual([], [h for h in hook_scripts() if h not in wired and h not in UNWIRED])

    def test_an_exempted_hook_is_not_reported(self):
        """Proves UNWIRED is consulted, rather than every hook happening to be wired."""
        self.assertTrue(UNWIRED, "the unwired list is empty, so this test measures nothing")
        exempt = next(iter(UNWIRED))
        wired = wired_names(t.read(SETTINGS_EXAMPLE))
        orphans = [h for h in hook_scripts() if h not in wired and h not in UNWIRED]
        self.assertNotIn(exempt, orphans)


if __name__ == "__main__":
    unittest.main()
