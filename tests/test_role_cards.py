"""Role cards: a seat's rules belong to the worktree, not to the session that was told them.

WHAT THIS EXISTS FOR. A session is told its seat in its first message. That instruction is an
ordinary user turn, so it competes with everything else in the context and it does not survive a
compaction. Binding the seat to the worktree instead, and injecting the card at SessionStart,
makes the rules present for every session that opens in that tree.

THE FAILURE THESE TESTS PIN. A card injected at CLAUDE.md weight is load-bearing, so a WRONG one
is worse than none. The resolution order must therefore be able to stay SILENT, and the silence
is what most of this file measures. A branch or directory name is a creation-time label that
nothing keeps current -- this repository has one right now whose name describes a question its
session answered in two minutes -- so no rung may read one.

THE LEAK HALF IS NOT DECORATION. These cards are derived from playbooks that came out of a private
vault, and that transfer has already put six user-home paths and two private artifact URLs into
this public tree past a gate that returned zero. Every absence check below is therefore paired
with a planted control that MUST fire, because a scan that reads nothing passes silently.
"""

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

import _ccxtest as t

TIMEOUT_SECONDS = 120

HOOK = t.REPO_ROOT / "scripts" / "hooks" / "role-card-inject.ps1"
SEATS_JSON = t.REPO_ROOT / "docs" / "roles" / "seats.json"
CARD_DIR = t.REPO_ROOT / "docs" / "roles"
SETTINGS_EXAMPLE = t.REPO_ROOT / ".claude" / "settings.example.json"
AGREEMENT = t.REPO_ROOT / "CLAUDE.md"

#: The marker and the injected copy. BOTH MUST BE GIT-IGNORED HERE, and the paths differ from the
#: ones a sibling project uses because this repository's ignore rules are the inverse of that
#: project's: `.claude/` is deliberately TRACKED here, and machine-local files are named `.local.`.
MARKER_RELPATH = ".claude/seat.local.txt"
ROLE_COPY_RELPATH = ".claude/ROLE.local.md"

#: Section 5 of the working agreement governs the roster. Seven seats, not the six a sibling
#: project runs: this repository added the Manager as an alternative to the Console.
EXPECTED_SEATS = frozenset(
    {"console", "manager", "builder", "reviewer", "regulator", "steward", "lander"}
)

#: Each card carries all five. A card missing one is a card that answers a question by omission.
REQUIRED_SECTIONS = (
    "What this seat owns",
    "What it must not do",
    "Its authority",
    "On arrival",
    "The full playbook",
)

CARD_MAX_LINES = 150
CARD_MAX_BYTES = 6 * 1024


def seats() -> dict:
    return json.loads(t.read(SEATS_JSON))


def card_paths() -> list[Path]:
    return sorted(CARD_DIR.glob("*.card.md"))


class TheRosterIsGovernedByTheWorkingAgreement(unittest.TestCase):
    """CLAUDE.md governs, and `roles/README.md` is the stale one.

    That README came across from a private vault. It still lists seven RETIRED seats as live and
    describes itself as a partial list, so a roster derived from it would hand a session rules for
    a seat that no longer exists.
    """

    def test_seats_json_lists_exactly_the_live_seats(self):
        self.assertEqual(EXPECTED_SEATS, set(seats()["live"]))

    def test_every_live_seat_has_a_card(self):
        missing = sorted(s for s in EXPECTED_SEATS if not (CARD_DIR / f"{s}.card.md").is_file())
        self.assertEqual([], missing, f"live seats with no card: {missing}")

    def test_no_card_exists_for_a_seat_that_is_not_live(self):
        stray = sorted(p.name for p in card_paths() if p.name[: -len(".card.md")] not in EXPECTED_SEATS)
        self.assertEqual([], stray, f"cards for seats that are not live: {stray}")

    def test_the_working_agreement_names_every_live_seat(self):
        """The roster in CLAUDE.md and the roster in seats.json cannot drift apart silently."""
        text = t.read(AGREEMENT).lower()
        absent = sorted(s for s in EXPECTED_SEATS if f"| {s} |" not in text)
        self.assertEqual([], absent, f"seats.json declares these but CLAUDE.md's table omits them: {absent}")

    def test_the_agreement_states_which_document_wins(self):
        """A reader who finds the two rosters disagreeing must be told which one governs."""
        text = t.read(AGREEMENT)
        self.assertIn("This table governs the roster.", text)


class RetiredSeatsResolveToNothingAndSayWhy(unittest.TestCase):
    """A retired label must not silently behave like an unknown one.

    Ten worktree records in the sibling project still declare seats that were retired. Resolving
    one to silence is correct; resolving it to silence WITHOUT saying it was retired sends the
    reader looking for a card that was deliberately removed.
    """

    def test_every_retired_seat_carries_a_reason(self):
        reasonless = sorted(k for k, v in seats()["retired"].items() if not str(v).strip())
        self.assertEqual([], reasonless, f"retired seats with no reason: {reasonless}")

    def test_no_retired_seat_is_also_live(self):
        both = sorted(set(seats()["retired"]) & set(seats()["live"]))
        self.assertEqual([], both, f"declared retired AND live: {both}")

    def test_no_retired_seat_has_a_card(self):
        present = sorted(s for s in seats()["retired"] if (CARD_DIR / f"{s}.card.md").is_file())
        self.assertEqual([], present, f"retired seats that still have a card: {present}")


class TheAliasMapCollapsesDrift(unittest.TestCase):
    """46 distinct role strings for a six-seat roster were counted in the sibling project.

    Eight of them were spellings of one seat. An alias map is the only thing that lets an
    instrument group by seat, because 46 labels do not group.
    """

    def test_every_alias_resolves_to_a_live_seat(self):
        live = set(seats()["live"])
        broken = sorted(f"{k} -> {v}" for k, v in seats()["aliases"].items() if v not in live)
        self.assertEqual([], broken, f"aliases pointing at no live seat: {broken}")

    def test_the_known_builder_spellings_all_collapse(self):
        aliases = seats()["aliases"]
        for spelling in ("builder1", "builder2", "builder-2", "builder3", "BUILDER1", "Builder"):
            with self.subTest(spelling=spelling):
                self.assertEqual("builder", aliases.get(spelling.lower(), spelling.lower()))

    def test_an_alias_never_shadows_a_live_seat_name(self):
        """`builder` must not appear as an alias key. A canonical name resolves to itself."""
        shadow = sorted(set(seats()["aliases"]) & set(seats()["live"]))
        self.assertEqual([], shadow, f"alias keys that are already canonical seat names: {shadow}")


class EveryCardStaysWithinItsBudget(unittest.TestCase):
    """A budget that is not enforced drifts.

    Only one card is ever injected, so the cost to a session is one card. The cap is what keeps
    that true as cards are edited by sessions that cannot see the other six.
    """

    def test_no_card_exceeds_the_line_cap(self):
        over = [
            f"{p.name}: {len(t.read(p).splitlines())} lines"
            for p in card_paths()
            if len(t.read(p).splitlines()) > CARD_MAX_LINES
        ]
        self.assertEqual([], over, f"cards over {CARD_MAX_LINES} lines: {over}")

    def test_no_card_exceeds_the_byte_cap(self):
        over = [f"{p.name}: {p.stat().st_size} bytes" for p in card_paths() if p.stat().st_size > CARD_MAX_BYTES]
        self.assertEqual([], over, f"cards over {CARD_MAX_BYTES} bytes: {over}")

    def test_every_card_carries_every_required_section(self):
        offenders = []
        for p in card_paths():
            text = t.read(p)
            for section in REQUIRED_SECTIONS:
                if section not in text:
                    offenders.append(f"{p.name} is missing '{section}'")
        self.assertEqual([], offenders, "\n  ".join(offenders))

    def test_every_card_names_the_marker_that_selected_it(self):
        """A reader who did not expect this card must be able to find out why it arrived."""
        silent = [p.name for p in card_paths() if MARKER_RELPATH not in t.read(p)]
        self.assertEqual([], silent, f"cards that do not say what selected them: {silent}")

    def test_the_card_scan_actually_reads_cards(self):
        """The empty-corpus guard. Every absence test above passes trivially against no cards."""
        self.assertGreaterEqual(len(card_paths()), len(EXPECTED_SEATS))


class NoCardCarriesPrivateContent(unittest.TestCase):
    """These cards derive from a private vault, and that transfer has leaked twice already.

    Each check below is paired with a planted control in
    `test_each_leak_pattern_fires_on_a_planted_example`. Without it a broken pattern and a clean
    corpus are indistinguishable, which is exactly how six user-home paths reached this tree.
    """

    PATTERNS = {
        "artifact URL": r"claude\.ai/(?:code/)?artifact",
        "bare UUID": r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
        "user home path": r"(?:[A-Za-z]:[\\/]Users|/home|/Users)[\\/][A-Za-z]",
    }

    def test_no_card_carries_a_leak_pattern(self):
        import re

        offenders = []
        for p in card_paths():
            text = t.read(p)
            for label, pattern in self.PATTERNS.items():
                for m in re.finditer(pattern, text, re.I):
                    offenders.append(f"{p.name}: {label}: {m.group(0)!r}")
        self.assertEqual([], offenders, "\n  ".join(offenders))

    def test_each_leak_pattern_fires_on_a_planted_example(self):
        """The armed half. A pattern that matches nothing would pass the test above in silence."""
        planted = {
            "artifact URL": "see https://claude.ai/code/artifact/<uuid>",
            "bare UUID": "id aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee here",
            # `example` is one of the placeholder names scripts/security/scan_forbidden.py
            # allowlists. A name it does not allowlist makes THIS file trip the leak gate, which is
            # how that was found: the planted control fired the real gate, not just this pattern.
            "user home path": r"C:\Users\example\vault",
        }
        for label, pattern in self.PATTERNS.items():
            with self.subTest(label=label):
                self.assertRegex(planted[label], pattern)

    def test_no_card_points_at_a_vault_absolute_path(self):
        offenders = [p.name for p in card_paths() if "<vault>/" not in t.read(p) and "vault/" in t.read(p).lower()]
        self.assertEqual([], offenders, f"cards naming a vault path outside the <vault> placeholder: {offenders}")

    def test_every_card_is_ascii(self):
        offenders = []
        for p in card_paths():
            for n, line in enumerate(t.read(p).splitlines(), 1):
                if any(ord(c) > 127 for c in line):
                    offenders.append(f"{p.name}:{n}")
        self.assertEqual([], offenders, f"non-ASCII in cards: {offenders}")


class TheMarkerCannotRideIntoACommit(unittest.TestCase):
    """Both generated paths must be ignored BY THIS REPOSITORY'S OWN RULES, which are unusual.

    `.gitignore` states at the top of the file that `.claude/` is DELIBERATELY NOT IGNORED, and
    that anything tracked under it must carry `.example.` in its name. Machine-local files are
    ignored by `*.local.*` instead. A path copied from a project that ignores `.claude/**` would
    be untracked here and could be committed by a blanket stage.
    """

    def check_ignored(self, relpath: str) -> bool:
        return (
            subprocess.run(
                ["git", "check-ignore", "-q", relpath],
                cwd=t.REPO_ROOT,
                capture_output=True,
                timeout=TIMEOUT_SECONDS,
            ).returncode
            == 0
        )

    def test_the_marker_is_ignored(self):
        self.assertTrue(self.check_ignored(MARKER_RELPATH), f"{MARKER_RELPATH} is not ignored")

    def test_the_injected_copy_is_ignored(self):
        self.assertTrue(self.check_ignored(ROLE_COPY_RELPATH), f"{ROLE_COPY_RELPATH} is not ignored")

    def test_the_check_can_report_a_path_that_is_not_ignored(self):
        """The armed half. `check_ignored` returning True for everything would pass both tests."""
        self.assertFalse(self.check_ignored("README.md"))

    def test_a_marker_without_a_trailing_segment_would_not_be_ignored(self):
        """`*.local.*` needs a segment AFTER `.local.`, so `.claude/seat.local` is TRACKED.

        This is the near-miss that makes the chosen filename look arbitrary. It is not.
        """
        self.assertFalse(self.check_ignored(".claude/seat.local"))


class TheHookIsWiredAndNeverBreaksATurn(unittest.TestCase):
    def test_the_hook_exists(self):
        self.assertTrue(HOOK.is_file(), f"{HOOK} is missing")

    def test_the_example_settings_wire_it_at_session_start(self):
        wired = json.loads(t.read(SETTINGS_EXAMPLE))
        commands = [
            h.get("command", "")
            for entry in wired.get("hooks", {}).get("SessionStart", [])
            for h in entry.get("hooks", [])
        ]
        self.assertTrue(
            any("role-card-inject.ps1" in c for c in commands),
            f"SessionStart does not run the hook; found {commands}",
        )

    def test_the_example_settings_stay_inert(self):
        """An example file that could be loaded is a control that looks installed.

        `.gitignore` states the rule: anything tracked under `.claude/` carries `.example.`, and
        the harness loads `settings.json` and `settings.local.json` only.
        """
        self.assertIn(".example.", SETTINGS_EXAMPLE.name)


class TheHookNeverGuessesASeat(unittest.TestCase):
    """The resolution order must be able to end in SILENCE.

    A wrong card is injected at the weight of the working agreement, so it outranks the thing a
    session should have been reading. Silence costs one printed command; a wrong card costs a
    session that confidently follows the wrong rules.
    """

    def setUp(self):
        pwsh = t.find_pwsh()
        if not pwsh:
            self.skipTest("pwsh is not on PATH, so the hook cannot be executed here")
        self.pwsh: str = pwsh
        self.tmp = tempfile.TemporaryDirectory(prefix="ccx-rolecard-")
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / ".claude").mkdir(parents=True)

    def run_hook(self, *, marker: str | None = None, env_seat: str | None = None):
        if marker is not None:
            (self.root / ".claude" / "seat.local.txt").write_text(marker, encoding="ascii")
        env = dict(os.environ)
        env.pop("KORUS_SEAT", None)
        if env_seat is not None:
            env["KORUS_SEAT"] = env_seat
        return subprocess.run(
            [self.pwsh, "-NoProfile", "-File", str(HOOK), "-WorktreeRoot", str(self.root)],
            input="{}",
            capture_output=True,
            text=True,
            env=env,
            cwd=str(self.root),
            timeout=TIMEOUT_SECONDS,
        )

    def test_a_missing_marker_exits_zero_and_injects_no_card(self):
        r = self.run_hook()
        self.assertEqual(0, r.returncode, r.stderr)
        self.assertNotIn("What this seat owns", r.stdout)

    def test_a_missing_marker_prints_the_command_that_sets_one(self):
        r = self.run_hook()
        self.assertIn("seat.local.txt", r.stdout)

    def test_an_unknown_label_exits_zero_and_injects_no_card(self):
        r = self.run_hook(marker="archivist")
        self.assertEqual(0, r.returncode, r.stderr)
        self.assertNotIn("What this seat owns", r.stdout)

    def test_a_retired_label_says_it_was_retired(self):
        retired = next(iter(seats()["retired"]))
        r = self.run_hook(marker=retired)
        self.assertEqual(0, r.returncode, r.stderr)
        self.assertIn("retired", r.stdout.lower())

    def test_a_branch_that_looks_like_a_seat_yields_no_card(self):
        """No rung reads a branch or directory name. This is the trap rung, and it stays unbuilt.

        The temporary root is created inside a directory named for a seat, which is the strongest
        form of the hint a name-reading rung would have taken.
        """
        seatish = self.root / "claude" / "lander-x"
        (seatish / ".claude").mkdir(parents=True)
        r = subprocess.run(
            [self.pwsh, "-NoProfile", "-File", str(HOOK), "-WorktreeRoot", str(seatish)],
            input="{}",
            capture_output=True,
            text=True,
            env={k: v for k, v in os.environ.items() if k != "KORUS_SEAT"},
            cwd=str(seatish),
            timeout=TIMEOUT_SECONDS,
        )
        self.assertEqual(0, r.returncode, r.stderr)
        self.assertNotIn("What this seat owns", r.stdout)

    def test_the_hook_source_reads_no_branch_name(self):
        """Pins the absence at the source, not only in behaviour.

        The behavioural test above passes against a hook that reads a branch and happens to find
        nothing. This one fails if the rung is ever added.
        """
        source = t.strip_ps_comments(t.read(HOOK))
        for forbidden in ("rev-parse", "symbolic-ref", "git branch"):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, source)


class TheHookResolvesInOrder(unittest.TestCase):
    def setUp(self):
        pwsh = t.find_pwsh()
        if not pwsh:
            self.skipTest("pwsh is not on PATH, so the hook cannot be executed here")
        self.pwsh: str = pwsh
        self.tmp = tempfile.TemporaryDirectory(prefix="ccx-rolecard-order-")
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / ".claude").mkdir(parents=True)

    def run_hook(self, *, marker=None, env_seat=None):
        if marker is not None:
            (self.root / ".claude" / "seat.local.txt").write_text(marker, encoding="ascii")
        env = dict(os.environ)
        env.pop("KORUS_SEAT", None)
        if env_seat is not None:
            env["KORUS_SEAT"] = env_seat
        return subprocess.run(
            [self.pwsh, "-NoProfile", "-File", str(HOOK), "-WorktreeRoot", str(self.root)],
            input="{}",
            capture_output=True,
            text=True,
            env=env,
            cwd=str(self.root),
            timeout=TIMEOUT_SECONDS,
        )

    def test_a_marker_injects_that_seats_card(self):
        r = self.run_hook(marker="reviewer")
        self.assertEqual(0, r.returncode, r.stderr)
        self.assertIn("What this seat owns", r.stdout)
        self.assertIn("Reviewer", r.stdout)

    def test_a_marker_is_case_and_space_insensitive(self):
        r = self.run_hook(marker="  Reviewer\n")
        self.assertIn("Reviewer", r.stdout)

    def test_an_alias_injects_the_canonical_card(self):
        r = self.run_hook(marker="builder2")
        self.assertIn("Builder", r.stdout)

    def test_the_env_var_is_used_when_no_marker_exists(self):
        r = self.run_hook(env_seat="lander")
        self.assertIn("Lander", r.stdout)

    def test_the_marker_outranks_the_env_var(self):
        r = self.run_hook(marker="reviewer", env_seat="lander")
        self.assertIn("Reviewer", r.stdout)
        self.assertNotIn("| Lander --", r.stdout)

    def test_the_card_is_written_where_a_compacted_session_can_re_read_it(self):
        self.run_hook(marker="reviewer")
        copy = self.root / ".claude" / "ROLE.local.md"
        self.assertTrue(copy.is_file(), "the hook did not write the re-readable copy")
        self.assertIn("What this seat owns", copy.read_text(encoding="utf-8"))


class RetiredRulesDoNotSurviveInACard(unittest.TestCase):
    """A retired SEAT resolving to silence is already guarded above. A retired RULE is not.

    The distinction cost something. Two cards reached `main` asserting the `reviewed` label as a
    live merge gate, which the owner removed on 2026-09-04. `roles/COMMON.md`, `roles/LANDER.md`,
    `roles/BUILDER.md` and `roles/MANAGER.md` all carry it as a RETIRED row; the cards carried it
    as a rule, and one of them as a MUST NOT.

    That direction is the expensive one: a Lander reading its own card holds a merge it is entitled
    to make, and the card supplies an authoritative-sounding reason. `docs/ROLE-CARDS.md` names the
    mechanism -- a card is injected at SessionStart, so it outranks the document that corrects it.

    NARROW ON PURPOSE. This guards one retired rule by name rather than pretending to a general
    test, because no registry of retired rules exists to check against. Widen it by adding a row
    when the next rule retires, and the pair below keeps it honest meanwhile.
    """

    #: (pattern, why it is retired). Matched case-insensitively, line by line.
    RETIRED = [
        ("reviewed", "the `reviewed` merge gate was removed 2026-09-04; an unlabelled PR merges"),
    ]

    def _live_hits(self, text: str) -> list[str]:
        """Lines naming a retired rule without marking it retired."""
        out = []
        for line in text.splitlines():
            low = line.lower()
            for pattern, _ in self.RETIRED:
                if pattern in low and "retired" not in low and "read *\"" not in line:
                    out.append(line.strip())
        return out

    def test_no_card_asserts_a_retired_rule_as_live(self):
        offenders = {}
        for path in card_paths():
            hits = self._live_hits(path.read_text(encoding="utf-8"))
            if hits:
                offenders[path.name] = hits
        self.assertEqual(
            {},
            offenders,
            "a role card names a retired rule without marking it retired:\n"
            + "\n".join(f"  {name}: {h}" for name, hs in offenders.items() for h in hs)
            + "\n\nThe reasons: "
            + "; ".join(why for _, why in self.RETIRED),
        )

    def test_the_scan_fires_on_the_shape_it_exists_to_catch(self):
        """The positive control. Without it, a pattern that matches nothing passes silently."""
        planted = "- **Merge an unlabelled PR.** `reviewed` is the gate, so re-check after any push."
        self.assertTrue(
            self._live_hits(planted),
            "the scan did not fire on the exact line that shipped to main, so it guards nothing",
        )

    def test_the_scan_accepts_a_correctly_retracted_line(self):
        """The negative arm. A retraction names the rule on purpose and must not be flagged."""
        retracted = "- **Wait for a `reviewed` label. RETIRED 2026-09-04.** An unlabelled PR merges."
        self.assertFalse(
            self._live_hits(retracted),
            "the scan flagged a correct retraction, which would make retracting in place impossible",
        )


if __name__ == "__main__":
    unittest.main()
