"""A page of this repository must not name a workflow that is no longer in the tree.

THE FAILURE THIS EXISTS FOR, and it is not hypothetical. `.github/workflows/review-gate.yml` was
deleted in #47. `CLAUDE.md` went on describing the gate that file implemented for two days: a three
state `reviewed` label, a push that strips it, and the instruction "do not merge an unlabelled PR".
The constitution and `roles/README.md` already recorded the deletion in the same tree, so the
repository contradicted itself and nothing said so.

WHY NOTHING CAUGHT IT. `test_internal_links_resolve.py` reads markdown links, and the reference sat
in a backtick span. `test_docs_do_not_drift.py` compares documents against each other, and both
copies of this claim were wrong together. No test compared a documented workflow name against the
workflows that exist. This one does.

THE COST IS THE DIRECTION, not the drift. The stale sentence told every seat to hold a pull request
it was entitled to merge, and it gave an authoritative-sounding reason. A wrong rule that stops work
is more expensive than a wrong rule that permits it, because nobody investigates a stall.

HOW SCOPE IS DERIVED, NOT LISTED. A workflow name is one that either sits in `.github/workflows/`
today, or appears anywhere in the tree written with that prefix. That second half is what puts a
DELETED workflow in scope at all, and it is why no hand-maintained list is needed here. A name that
never appears with the prefix is not a workflow of this repository: `sprint-status.yaml` in
`docs/FRAMEWORK-bmad.md` names another framework's file, and stays out.

THE CORPUS IS THIS REPOSITORY'S OWN PAGES. `CLAUDE.md`, `docs/*.md` and the constitution describe
this tree, so a claim in one of them is a claim about this tree. `roles/` is excluded on purpose: it
came across from a private vault and legitimately describes MessageFoundry's workflows, which are
absent here by design and not by drift.

RETRACTION IN PLACE IS ALLOWED, and has to be. The point of the correction that motivated this file
is that a seat remembering the old rule meets the retraction rather than re-deriving it, so a
paragraph saying a workflow was deleted must not be what trips the guard. The marker is checked over
the whole paragraph rather than the line, because prose wraps and a line-oriented test cannot tell
"absent" from "present but wrapped".

BOTH ARMS RUN. A planted assertion about an absent workflow must trip, a planted retraction of the
same workflow must not, and the scan states how much it read. Without the must-not arm this file
would pass by refusing everything; without the coverage floor it would pass by reading nothing.

Run: python -m unittest discover -s tests
"""

from __future__ import annotations

import re
import subprocess
import unittest

import _ccxtest as t

WORKFLOW_DIR = ".github/workflows/"

# A workflow named with its directory, anywhere in the tree. This is what admits a name whose file
# has been deleted -- the whole point of the check.
PREFIXED = re.compile(r"\.github/workflows/([A-Za-z0-9._-]+\.ya?ml)")

# A `...whatever.yml` span. The name is taken from the end so that both `review-gate.yml` and
# `.github/workflows/review-gate.yml` resolve to one key.
BACKTICKED = re.compile(r"`[^`\n]*?([A-Za-z0-9._-]+\.ya?ml)`")

# Words that mark a reference as a record of something gone rather than a claim that it runs.
RETIRED = re.compile(
    r"\b(deleted|retired|removed|no longer|never existed|does not exist)\b", re.I
)


def tracked_files() -> list[str]:
    """Every path git is tracking, as forward-slash repo-relative strings."""
    out = subprocess.run(
        ["git", "ls-files"],
        cwd=t.REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    return [line.strip() for line in out.stdout.splitlines() if line.strip()]


def describes_this_repository(path: str) -> bool:
    """The pages whose claims are claims about THIS tree."""
    if not path.endswith(".md"):
        return False
    return (
        path == "CLAUDE.md"
        or path.startswith("docs/")
        or path == ".specify/memory/constitution.md"
    )


def paragraphs(raw: str) -> list[str]:
    """Blank-line-separated blocks. Prose wraps, so a claim spans lines, not one line."""
    return [block for block in re.split(r"\n\s*\n", raw) if block.strip()]


def workflows_on_disk(paths: list[str]) -> set[str]:
    return {
        p[len(WORKFLOW_DIR) :] for p in paths if p.startswith(WORKFLOW_DIR)
    }


def workflow_names(paths: list[str]) -> set[str]:
    """On disk, plus every name the tree writes with the `.github/workflows/` prefix."""
    names = workflows_on_disk(paths)
    for path in paths:
        try:
            raw = (t.REPO_ROOT / path).read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        names |= set(PREFIXED.findall(raw))
    return names


def offences(paths: list[str], known: set[str], present: set[str]):
    """Every in-scope reference, split into what it asserts and what it retracts."""
    asserted, retracted = [], []
    for path in paths:
        if not describes_this_repository(path):
            continue
        raw = (t.REPO_ROOT / path).read_text(encoding="utf-8")
        for block in paragraphs(raw):
            marked = bool(RETIRED.search(block))
            for name in set(BACKTICKED.findall(block)):
                if name not in known:
                    continue
                if name in present:
                    continue
                row = (path, name, " ".join(block.split())[:160])
                (retracted if marked else asserted).append(row)
    return asserted, retracted


class ADocNeverNamesADeletedWorkflow(unittest.TestCase):
    """The live case, plus the two arms that make its green mean something."""

    def setUp(self):
        self.paths = tracked_files()
        self.present = workflows_on_disk(self.paths)
        self.known = workflow_names(self.paths)

    def test_the_scan_can_reach_an_absent_workflow_at_all(self):
        """The coverage floor. An empty scan and a clean scan print the same thing.

        If every known name were also on disk, the failing branch below could never execute and its
        green would be a statement about the tree's shape rather than about its documents.
        """
        self.assertTrue(self.present, "no workflows found on disk at all -- the scan is blind")
        self.assertTrue(
            self.known - self.present,
            "every known workflow name is on disk, so the absent-workflow branch of this test "
            "cannot run. That is not a pass; it means this file is measuring nothing. Re-derive "
            "the scope before deleting the case.",
        )
        corpus = [p for p in self.paths if describes_this_repository(p)]
        self.assertTrue(corpus, "the corpus resolved to zero files -- the path filter is wrong")

    def test_no_page_asserts_a_workflow_that_is_not_in_the_tree(self):
        asserted, _ = offences(self.paths, self.known, self.present)
        self.assertEqual(
            [],
            asserted,
            "a page of this repository names a workflow that is not in `.github/workflows/` and "
            "does not say it is gone. Either restore the file, or retract the claim in place the "
            "way the constitution does, naming what replaced it:\n"
            + "\n".join(f"  {p}: `{n}`\n    | {b}" for p, n, b in asserted),
        )

    def test_a_planted_assertion_trips_and_a_planted_retraction_does_not(self):
        """Both arms, against one absent workflow taken from the tree rather than invented."""
        absent = sorted(self.known - self.present)[0]

        claims_it_runs = f"The `gate` job from `{absent}` is not among the required contexts."
        says_it_is_gone = f"`{absent}` was deleted, so nothing reads the label any more."

        self.assertTrue(
            BACKTICKED.search(claims_it_runs)
            and BACKTICKED.findall(claims_it_runs)[0] == absent,
            f"the reference pattern no longer matches `{absent}` in a sentence, so the check "
            "above would pass by matching nothing",
        )
        self.assertFalse(
            RETIRED.search(claims_it_runs),
            "MUST-TRIP arm: a sentence asserting the workflow runs was read as a retraction",
        )
        self.assertTrue(
            RETIRED.search(says_it_is_gone),
            "MUST-NOT-TRIP arm: a correct retraction in place would be reported as a defect, "
            "which would make correcting a stale rule impossible",
        )

    def test_the_marker_is_read_over_a_wrapped_paragraph(self):
        """A retraction split across lines is still a retraction. Prose wraps; line greps do not."""
        absent = sorted(self.known - self.present)[0]
        wrapped = f"The Owner removed the gate, and `{absent}` was\ndeleted from the tree in #47."
        self.assertEqual(1, len(paragraphs(wrapped)), "the splitter broke one paragraph into two")
        self.assertTrue(
            RETIRED.search(paragraphs(wrapped)[0]),
            "a retraction wrapped across two lines read as an assertion",
        )
        self.assertIsNone(
            RETIRED.search("deleted"[:4]),
            "control: a fragment that is not the whole word must not match",
        )


if __name__ == "__main__":
    unittest.main()
