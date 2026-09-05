"""The expiry audit reads the corpus, and says so when it cannot.

WHY THE AUDIT EXISTS. This repository requires a standing prohibition to carry its expiry
condition. The playbooks follow that rule. Nothing ever evaluated one, so a rule that named its own
expiry could go on reading as current indefinitely -- and it reads convincingly, because the care
that went into stating the expiry is what makes it persuasive.

WHY THIS TEST FILE EXISTS SEPARATELY FROM THE AUDIT. The audit is a scan for a condition, and a scan
for a condition passes trivially against a corpus it never read. That is not hypothetical here: the
first working version of `expiry_audit.py` tested its skip-list against the ABSOLUTE path, and every
checkout of this repository under a harness worktree sits below a directory literally named
`worktrees`. So the skip matched an ANCESTOR of the repository, the scan read nothing but
`CLAUDE.md`, and it printed "3 clauses across 1 file" -- a number, formatted like a result,
measuring almost nothing. The corpus floor below is what stops that shipping again.

THE AUDIT NEVER DECIDES THAT A RULE HAS EXPIRED, and `TheAuditNeverJudgesTheRuleItself` pins that.
Expiry is a judgment about meaning. What a machine can answer is the narrower question of whether
the artifact a clause POINTS AT still exists, and conflating the two would produce confident wrong
retirements of rules that are still right.
"""

import subprocess
import sys
import unittest

import _ccxtest as t

sys.path.insert(0, str(t.REPO_ROOT / "scripts" / "quality"))

import expiry_audit as audit  # noqa: E402

TIMEOUT_SECONDS = 120
SCRIPT = t.REPO_ROOT / "scripts" / "quality" / "expiry_audit.py"


class TheScanActuallyReadsTheCorpus(unittest.TestCase):
    """The empty-corpus guard, and the reason this file exists."""

    def setUp(self):
        self.clauses = audit.collect(t.REPO_ROOT)

    def test_it_finds_clauses_across_many_files(self):
        files = {c.source for c in self.clauses}
        self.assertGreaterEqual(
            len(files),
            8,
            f"the audit read only {len(files)} file(s): {sorted(files)}. The corpus is roles/, "
            "docs/ and the constitution. A scan this narrow is a broken skip-list reporting a "
            "clean-looking number, which is exactly how this shipped the first time.",
        )

    def test_it_reads_the_role_playbooks(self):
        """roles/ is where standing prohibitions actually live, so its absence is the loud case."""
        sources = {c.source for c in self.clauses}
        self.assertTrue(
            any(s.startswith("roles/") for s in sources),
            f"no clause came from roles/. Sources were: {sorted(sources)}",
        )

    def test_it_reads_the_working_agreement(self):
        self.assertIn("CLAUDE.md", {c.source for c in self.clauses})

    def test_the_skip_list_is_matched_on_the_relative_path(self):
        """Pinned at the source. This repository's own checkout path contains `worktrees`, so an
        absolute-path skip silently excludes the entire tree and nothing looks wrong."""
        source = t.read(SCRIPT)
        self.assertIn("p.relative_to(root).parts", source)


class ScanningAndIndexingUseDifferentSkipLists(unittest.TestCase):
    """They answer different questions and must not share a list.

    SCANNING excludes retired playbooks: they are a record, not a live rule. INDEXING must include
    them, because a live rule cites `PM.md` precisely to say that seat is retired -- and excluding
    retired files from the index reported that correct citation as a rotted reference.
    """

    def test_the_index_skip_is_a_subset_of_the_scan_skip(self):
        self.assertTrue(audit.INDEX_SKIP.issubset(audit.SCAN_SKIP | audit.INDEX_SKIP))
        self.assertLess(len(audit.INDEX_SKIP), len(audit.SCAN_SKIP))

    def test_retired_playbooks_are_not_scanned(self):
        sources = {c.source for c in audit.collect(t.REPO_ROOT)}
        self.assertFalse([s for s in sources if "retired" in s], sorted(sources))

    def test_a_retired_playbook_still_resolves_as_an_artifact(self):
        """The control for the rule above: citing a retired file must not read as dangling."""
        index = audit.build_index(t.REPO_ROOT)
        self.assertIn("pm.md", index, "roles/retired/PM.md is not indexed, so citing it looks broken")


class ABareFilenameResolves(unittest.TestCase):
    """These documents cite `alloc.ps1` far more often than `scripts/coord/alloc.ps1`."""

    def setUp(self):
        self.index = audit.build_index(t.REPO_ROOT)

    def test_a_bare_script_name_is_indexed(self):
        self.assertIn("alloc.ps1", self.index)
        self.assertTrue(any("scripts/coord" in p for p in self.index["alloc.ps1"]))

    def test_a_clause_citing_a_bare_name_is_not_dangling(self):
        c = audit.Clause(source="x.md", line=1, text="expiry: see `alloc.ps1`", paths=["alloc.ps1"])
        audit.judge(c, t.REPO_ROOT, self.index)
        self.assertEqual("LIVE", c.verdict, c.detail)

    def test_a_clause_citing_a_real_absence_is_dangling(self):
        """The control. Without it the test above passes for a judge that never reports anything."""
        c = audit.Clause(
            source="x.md", line=1, text="expiry: see `no-such-file-anywhere.ps1`",
            paths=["no-such-file-anywhere.ps1"],
        )
        audit.judge(c, t.REPO_ROOT, self.index)
        self.assertEqual("DANGLING", c.verdict, c.detail)

    def test_a_git_ignored_path_is_not_dangling(self):
        """`.claude/seat.local.txt` is the seat marker. It is SUPPOSED to be absent from the tree,
        and reporting it would train a reader to skim the column it appears in."""
        c = audit.Clause(
            source="x.md", line=1, text="expiry: the marker `.claude/seat.local.txt`",
            paths=[".claude/seat.local.txt"],
        )
        audit.judge(c, t.REPO_ROOT, self.index)
        self.assertNotEqual("DANGLING", c.verdict, c.detail)


class TheAuditNeverJudgesTheRuleItself(unittest.TestCase):
    """It answers whether a clause is CHECKABLE, never whether it is still right."""

    def test_a_resolvable_clause_is_reported_as_live_not_as_valid(self):
        index = audit.build_index(t.REPO_ROOT)
        c = audit.Clause(source="x.md", line=1, text="expiry: `alloc.ps1`", paths=["alloc.ps1"])
        audit.judge(c, t.REPO_ROOT, index)
        self.assertIn("not the same as still right", c.detail)

    def test_a_clause_naming_no_artifact_is_uncheckable_not_a_defect(self):
        c = audit.Clause(source="x.md", line=1, text="this expires when the owner says so", paths=[])
        audit.judge(c, t.REPO_ROOT, {})
        self.assertEqual("UNCHECKABLE", c.verdict)

    def test_no_verdict_claims_a_rule_expired(self):
        source = t.read(SCRIPT)
        for c in audit.collect(t.REPO_ROOT):
            with self.subTest(source=c.source, line=c.line):
                self.assertIn(c.verdict, {"DANGLING", "UNCHECKABLE", "LIVE"})
        self.assertIn("NEVER decides that a rule has expired", source)


class TheMarkersFireOnPlantedProseAndDeclineTheNeighbour(unittest.TestCase):
    """Without the negative half, this passes for a marker list that matches everything."""

    PLANTED = [
        "This stops mattering only if the gate stops being wired.",
        "RETIRED 2026-09-01 by owner decision.",
        "Its expiry condition is that `alloc.ps1` gains a -Peek flag.",
    ]
    DECLINED = [
        "The gate reads the target path rather than the working directory.",
        "Two sessions in one working tree clobber each other.",
    ]

    def test_each_planted_paragraph_yields_a_clause(self):
        for text in self.PLANTED:
            with self.subTest(text=text):
                self.assertEqual(1, len(audit.extract(text, "planted.md")), f"no clause from: {text}")

    def test_ordinary_prose_yields_no_clause(self):
        for text in self.DECLINED:
            with self.subTest(text=text):
                self.assertEqual([], audit.extract(text, "planted.md"), f"false positive on: {text}")


class TheCommandRuns(unittest.TestCase):
    def test_it_exits_zero_by_default(self):
        r = subprocess.run(
            [sys.executable, str(SCRIPT)],
            capture_output=True, text=True, cwd=str(t.REPO_ROOT), timeout=TIMEOUT_SECONDS,
        )
        self.assertEqual(0, r.returncode, r.stderr)
        self.assertIn("expiry audit:", r.stdout)

    def test_it_reports_all_three_verdicts(self):
        r = subprocess.run(
            [sys.executable, str(SCRIPT)],
            capture_output=True, text=True, cwd=str(t.REPO_ROOT), timeout=TIMEOUT_SECONDS,
        )
        for verdict in ("DANGLING", "UNCHECKABLE", "LIVE"):
            self.assertIn(verdict, r.stdout)

    def test_an_empty_corpus_says_it_read_nothing(self):
        """A clean-looking zero and a scan that read nothing must not render the same."""
        import tempfile

        with tempfile.TemporaryDirectory(prefix="ccx-expiry-") as tmp:
            r = subprocess.run(
                [sys.executable, str(SCRIPT), "--root", tmp],
                capture_output=True, text=True, timeout=TIMEOUT_SECONDS,
            )
            self.assertEqual(0, r.returncode, r.stderr)
            self.assertIn("NO CLAUSES FOUND", r.stdout)
            self.assertIn("read nothing", r.stdout)


if __name__ == "__main__":
    unittest.main()
