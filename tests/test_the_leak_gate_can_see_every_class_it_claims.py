"""Every structural detector in the leak gate, proved against a line it MUST flag and one it must not.

THE DEFECT THIS EXISTS FOR, and it is a measured one rather than a worry. Commit `a3df144` brought
two private artifact URLs into the tracked tree, at `roles/LANDER.md:4027` and
`roles/retired/PM.md:200`. The gate ran over both and exited `0`. They came out again in PR #48
because a person read the diff -- the same review the gate exists to make cheaper, doing the entire
job unaided. Nothing about that run looked wrong: the receipt said `structural=8`, the scan counted
every file, and the exit code was the one a clean tree produces.

That is the failure this directory is about, in the one script whose only job is to prevent it.
`docs/LEAK-GATE.md` states the rule the gate could not keep for itself:

    A green gate is evidence only if you have proved it can SEE that class.

Until this file existed, `scripts/security/scan_forbidden.py` had no test of any kind. Every green
run it had ever produced was unfalsifiable -- a detector that never compiled, a regex quietly
narrowed, a whole branch deleted: all three exit `0` and print a healthy receipt.

TWO CORPORA PER DETECTOR, BECAUSE ONE PROVES HALF. A detector hard-wired to fire passes the planted
case perfectly. A detector hard-wired to stay silent -- or one whose reader found no files -- passes
the clean case perfectly. Only running both rules out both, which is the rule
`test_every_validation_check_is_proven_by_a_control.py` already imposes on `scripts/validation/`.
This file brings `scripts/security/` under the same one.

THE TABLE IS DRIVEN OFF THE DETECTOR COUNT, so tomorrow's detector is covered the day it is added.
`_STRUCTURAL_COUNT` is the number the gate prints on its own receipt; a detector added without a
planted line makes `TheTableCoversEveryDetectorTheGateClaims` fail, rather than quietly shipping a
column nobody proved. A control pinned to one detector is a control the next detector is written
without.

EVERY FIXTURE IS ASSEMBLED FROM FRAGMENTS, and that is load-bearing rather than a matter of taste.
The gate scans this repository, `tests/` included. A planted home path or artifact URL written as
one literal would make this file a hit -- the control would break the gate it exists to prove, and
the obvious repair is an allowlist line, which is a per-line veto over every other detector on that
line. So no single source line here is a violation; only the joined value is.
`ThePlantedFixturesNeverBecomeALeakThemselves` keeps that true under editing, instead of trusting
that whoever adds the next fixture notices.

Run: python -m unittest discover -s tests
"""

from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import _ccxtest as t

GATE = t.REPO_ROOT / "scripts" / "security" / "scan_forbidden.py"


def load_gate():
    """Import the gate by path. It is a script, not a package, and deliberately has no __init__."""
    spec = importlib.util.spec_from_file_location("ccx_scan_forbidden", GATE)
    if spec is None or spec.loader is None:
        raise AssertionError(f"cannot load {GATE} as a module -- the control cannot measure it")
    module = importlib.util.module_from_spec(spec)
    sys.modules["ccx_scan_forbidden"] = module
    spec.loader.exec_module(module)
    return module


#: An obviously synthetic UUID: version-4 shaped, all-zero payload. Never a real artifact id, and
#: deterministic, so a failure names a detector rather than a random draw.
FAKE_UUID = "00000000-0000-4000-8000-000000000000"

#: One row per structural detector: (label, reason substring the hit must carry, line fragments).
#: The fragments are joined to build the planted line. The module docstring says why they are
#: fragments: written as single literals, these would make this file a leak.
FIRES: tuple[tuple[str, str, tuple[str, ...]], ...] = (
    (
        "private artifact URL",
        "private artifact URL",
        ("https://claude.ai/code/", "artifact/", FAKE_UUID),
    ),
    (
        "absolute user-home path",
        "absolute user-home path",
        ("C:", r"\Users", r"\ccxleak", r"\notes.md"),
    ),
    (
        "routable IPv4",
        "routable IP address",
        # RFC 2544 benchmarking range: it routes nowhere, so the fixture names no real host, and it
        # sits outside every range _ALLOWED_IP excuses, so the detector must read it as routable.
        ("198.18.", "0.1"),
    ),
    ("private key block", "private key block", ("-----BEGIN ", "PRIVATE KEY-----")),
    ("cloud access key id", "cloud access key id", ("AKIA", "EXAMPLEKEY000000")),
    ("forge access token (classic)", "forge access token", ("ghp_", "A" * 36)),
    ("forge access token (fine-grained)", "forge access token", ("github_pat_", "A" * 22)),
    ("chat platform token", "chat platform token", ("xoxb-", "A" * 12)),
    ("model API key", "model API key", ("sk-ant-", "A" * 32)),
)

#: Near misses. Each is a line a detector could plausibly over-reach onto, and must not. A gate that
#: fires on these earns an allowlist entry, and an allowlist entry vetoes every detector on the
#: lines it covers -- so a false positive here costs more than the coverage it buys.
QUIET: tuple[tuple[str, tuple[str, ...]], ...] = (
    (
        "the placeholder form the documentation has to print. A detector whose own manual trips it "
        "earns an allowlist line, and that line switches off every detector on those lines",
        ("https://claude.ai/code/", "artifact/", "<uuid>"),
    ),
    (
        "a deliberately shared artifact: that path segment is plural, and a published URL is not a "
        "disclosure",
        ("https://claude.ai/public/", "artifacts/", FAKE_UUID),
    ),
    (
        "a bare UUID, which the gate deliberately does not detect. It names no host, no account and "
        "no project, and becomes a capability only when something says what it addresses. This case "
        "is that recorded decision made executable, so a later widening has to face it",
        (FAKE_UUID,),
    ),
    (
        "an ordinary claude.ai link with no artifact path. roles/REVIEWER.md carries one",
        ("https://claude.ai/", "code"),
    ),
    (
        "a home path written with the placeholder the detector exempts",
        ("C:", r"\Users", r"\<name>", r"\notes.md"),
    ),
    (
        "the well-known CI account, which is not a person's login",
        ("/home", "/runner", "/work"),
    ),
    ("an RFC1918 private address, which identifies no host on the internet", ("192.168.", "1.1")),
    ("a dotted OID, which the IPv4 look-arounds exist to keep out", ("1.3.6.", "1.4.1")),
)


def scan_line(gate, text: str, *, show_context: bool = False) -> list[str]:
    """Write one line to a file OUTSIDE the repository and return the gate's hits on it.

    Outside on purpose, and for the reason `docs/LEAK-GATE.md` gives when it tells a person to plant
    a violation by hand: a fixture written inside the tree is a fixture that has to be cleaned up,
    and the run that forgets is the run that commits it.
    """
    with tempfile.TemporaryDirectory(prefix="ccx-leakgate-") as tmp:
        planted = Path(tmp) / "planted.md"
        planted.write_text(text + "\n", encoding="utf-8")
        return gate.scan_file(planted, show_context=show_context)


class EveryDetectorFiresOnItsPlantedLine(unittest.TestCase):
    """The half `a3df144` failed. Without it every green run the gate produces is unfalsifiable."""

    def setUp(self):
        self.gate = load_gate()

    def test_each_structural_detector_flags_a_line_planted_for_it(self):
        for label, reason, parts in FIRES:
            with self.subTest(detector=label):
                hits = scan_line(self.gate, "".join(parts))
                self.assertTrue(
                    any(reason in h for h in hits),
                    f"the {label} detector did not fire on a line planted for it. Hits: {hits!r}. "
                    "A detector that cannot fire is not an instrument, and every clean run it has "
                    "ever produced means nothing.",
                )

    def test_the_artifact_detector_sees_every_form_of_the_same_capability(self):
        """`a3df144` used the /code/ form. The others address the same artifact."""
        for parts in (
            ("https://claude.ai/code/", "artifact/", FAKE_UUID),
            ("https://claude.ai/", "artifact/", FAKE_UUID),
            ("claude.ai/code/", "artifact/", FAKE_UUID.upper()),
            ("[the handoff](https://claude.ai/code/", "artifact/", FAKE_UUID + ")"),
        ):
            with self.subTest(form="".join(parts)[:36]):
                hits = scan_line(self.gate, "".join(parts))
                self.assertTrue(
                    any("private artifact URL" in h for h in hits),
                    f"no artifact-URL hit on {''.join(parts)!r}. Hits: {hits!r}",
                )


class EveryDetectorStaysQuietOnItsNearMiss(unittest.TestCase):
    """The other half. A detector that fires on everything is as useless as one firing on nothing."""

    def setUp(self):
        self.gate = load_gate()

    def test_no_detector_fires_on_a_line_that_discloses_nothing(self):
        for why, parts in QUIET:
            with self.subTest(case=why[:48]):
                hits = scan_line(self.gate, "".join(parts))
                self.assertEqual(
                    [],
                    hits,
                    f"the gate flagged a line it must not: {why}. Hits: {hits!r}",
                )


class TheTableCoversEveryDetectorTheGateClaims(unittest.TestCase):
    """A control pinned to one detector is a control the next detector is written without."""

    def test_there_is_one_planted_line_per_structural_detector(self):
        gate = load_gate()
        self.assertEqual(
            gate._STRUCTURAL_COUNT,
            len(FIRES),
            f"the gate reports structural={gate._STRUCTURAL_COUNT} on every receipt it prints, and "
            f"this file plants {len(FIRES)} line(s). The mismatch means a detector was added or "
            "removed without its control, so the printed count is no longer backed by evidence. "
            "Add the planted line and its near miss to FIRES/QUIET rather than editing this number.",
        )


class ThePlantedFixturesNeverBecomeALeakThemselves(unittest.TestCase):
    """This file is scanned by the gate it tests. A fixture written as one literal breaks CI."""

    def test_this_control_file_is_clean_under_the_gate_it_proves(self):
        gate = load_gate()
        hits = gate.scan_file(Path(__file__), rel_posix="tests/" + Path(__file__).name)
        self.assertEqual(
            [],
            hits,
            f"this control file is itself a leak-gate hit: {hits!r}. A fixture was written as one "
            "source line instead of joined fragments. Split it -- do NOT allowlist this file, "
            "because an allowlist entry vetoes every detector on the lines it covers.",
        )


class AnArtifactHitNeverEchoesTheCapability(unittest.TestCase):
    """The URL is the artifact. Printing it into a log publishes what the hit is reporting."""

    def test_show_context_does_not_print_the_url(self):
        gate = load_gate()
        planted = "".join(("https://claude.ai/code/", "artifact/", FAKE_UUID))
        hits = scan_line(gate, planted, show_context=True)
        artifact_hits = [h for h in hits if "private artifact URL" in h]
        self.assertTrue(artifact_hits, f"no artifact hit to check. Hits: {hits!r}")
        for hit in artifact_hits:
            self.assertNotIn(
                FAKE_UUID,
                hit,
                "--show-context echoed the artifact UUID into the hit line. Anyone reading that log "
                "can then fetch the artifact, so the report would publish the capability it exists "
                "to report, to a wider audience than the tree it was found in.",
            )


class TheGateExitsNonZeroOverAPlantedFile(unittest.TestCase):
    """End to end. `scan_file` returning hits proves nothing if the exit code stays 0."""

    def test_a_planted_artifact_url_exits_1_and_the_placeholder_form_exits_0(self):
        with tempfile.TemporaryDirectory(prefix="ccx-leakgate-e2e-") as tmp:
            leaky = Path(tmp) / "leaky.md"
            leaky.write_text(
                "".join(("https://claude.ai/code/", "artifact/", FAKE_UUID)) + "\n",
                encoding="utf-8",
            )
            clean = Path(tmp) / "clean.md"
            clean.write_text(
                "".join(("https://claude.ai/code/", "artifact/", "<uuid>")) + "\n",
                encoding="utf-8",
            )

            refused = subprocess.run(
                [sys.executable, str(GATE), str(leaky)],
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=120,
            )
            self.assertEqual(
                1,
                refused.returncode,
                "the gate did not exit 1 over a planted artifact URL.\n"
                f"exit: {refused.returncode}\nstdout:\n{refused.stdout}\nstderr:\n{refused.stderr}",
            )
            self.assertIn("private artifact URL", refused.stdout + refused.stderr)

            passed = subprocess.run(
                [sys.executable, str(GATE), str(clean)],
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=120,
            )
            self.assertEqual(
                0,
                passed.returncode,
                "the gate refused the placeholder form, so the documentation describing this "
                "detector could not be committed.\n"
                f"stdout:\n{passed.stdout}\nstderr:\n{passed.stderr}",
            )
