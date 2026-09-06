#!/usr/bin/env python3
"""Expiry-clause audit: does the artifact a standing rule depends on still exist?

WHY THIS EXISTS. This repository requires a standing prohibition to carry its expiry condition --
what would have to become true for it to stop being right. The role playbooks follow that rule and
the constitution states it. **Nothing ever evaluated one.**

A rule that names its own expiry and is never re-read is worse than a rule with no expiry at all. It
reads as current because it was written carefully, and the care is the thing that makes it
convincing. The measured failure this pattern comes from: a playbook trap told builders that a
pre-commit hook was `language: system`, and stated its own expiry verbatim -- "stops mattering only
if the hook stops using --fix or stops being language: system". A commit moved both hooks upstream.
The condition fired, the commit announced it in its own subject line, and three days later a session
was still citing the stale trap as live.

WHAT IT DOES NOT DO, and this is the whole reason it is safe to run. **It never decides that a rule
has expired.** A rule expires for reasons only a reader can weigh. What it can do mechanically is
answer a narrower question: does the artifact the clause POINTS AT still exist? A clause resting on
a file that is gone is a clause nobody can evaluate, and that is reportable without judgment.

Three verdicts, and they need different responses:

    DANGLING     the clause names a path that is not in the tree. Either the condition fired, or
                 the reference rotted. Both need a human; they are not the same fix.
    UNCHECKABLE  the clause names no artifact at all, so nothing mechanical can ever evaluate it.
                 Not a defect. It is the population that will never be audited, and knowing its
                 size is the point.
    LIVE         every path it names resolves. This says the clause is still CHECKABLE. It does
                 NOT say the rule is still right.

Exit code is 0 unless --strict is given, because a DANGLING clause is a prompt to read, not a
build break.

    python scripts/quality/expiry_audit.py
    python scripts/quality/expiry_audit.py --strict
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

#: Where standing rules live here. CLAUDE.md and the constitution are in scope because both carry
#: prohibitions, and excluding them would audit the playbooks while exempting the documents that
#: govern them.
SCAN_ROOTS = ("roles", "docs", ".specify/memory")
SCAN_FILES = ("CLAUDE.md",)

#: Phrases this repository actually uses to introduce an expiry condition. Each was taken from the
#: corpus rather than invented, so a zero here is a reading rather than a pattern that never fires.
MARKERS = (
    "expiry",
    "expires",
    "stops being right",
    "stop being right",
    "stops mattering",
    "stops being true",
    "until this is",
    "no longer true when",
    "retired",
)

#: A backticked token. Paths, commands and grep strings all arrive this way in these files.
TICKED = re.compile(r"`([^`\n]{2,160})`")

#: A path, optionally with :LINE. Requires a real suffix so a prose token like `Get-Mine` is not
#: read as a file, which would make every clause look DANGLING and the report worthless.
PATHISH = re.compile(
    r"^(?P<path>[\w./\\-]*[\w-]+\.(?:py|ps1|yml|yaml|md|txt|json|cfg|ini|lock))"
    r"(?::(?P<line>\d+)(?:-\d+)?)?$"
)

#: Not scanned for clauses: generated Word copies, and retired playbooks, which are a record
#: rather than a live rule.
SCAN_SKIP = {".git", "node_modules", "__pycache__", ".venv", "word", "retired"}

#: Not indexed as resolvable artifacts. DELIBERATELY SMALLER than SCAN_SKIP: a live rule cites
#: `PM.md` precisely to say that seat is retired, and excluding retired files from the index
#: reported that correct citation as a rotted reference.
INDEX_SKIP = {".git", "node_modules", "__pycache__", ".venv"}


@dataclass
class Clause:
    source: str
    line: int
    text: str
    paths: list[str] = field(default_factory=list)
    verdict: str = "UNCHECKABLE"
    detail: str = ""


def paragraphs(text: str) -> list[tuple[int, str]]:
    """(1-based start line, joined text) per blank-line-separated block.

    Joined rather than read line by line, because prose here wraps near 100 characters and a
    marker regularly lands on a different line from the path it governs. A line-based scan reports
    a confident zero on a corpus full of clauses, which is the failure mode this file exists to
    avoid in others.
    """
    out: list[tuple[int, str]] = []
    buf: list[str] = []
    start = 1
    for n, line in enumerate(text.split("\n"), 1):
        if line.strip():
            if not buf:
                start = n
            buf.append(line.strip())
        elif buf:
            out.append((start, " ".join(buf)))
            buf = []
    if buf:
        out.append((start, " ".join(buf)))
    return out


def extract(text: str, source: str) -> list[Clause]:
    found: list[Clause] = []
    for start, para in paragraphs(text):
        low = para.lower()
        if not any(m in low for m in MARKERS):
            continue
        paths = []
        for tok in TICKED.findall(para):
            m = PATHISH.match(tok.strip())
            if m:
                paths.append(m.group("path"))
        found.append(Clause(source=source, line=start, text=para[:300], paths=paths))
    return found


def build_index(root: Path) -> dict[str, list[str]]:
    """basename -> every tracked path with that basename.

    WHY A BARE NAME MUST RESOLVE. These documents cite `alloc.ps1` and `COMMON.md` far more often
    than they cite full paths, and both exist -- at `scripts/coord/alloc.ps1` and `roles/COMMON.md`.
    A root-relative-only check calls all of those DANGLING, and a report that is mostly false
    positives gets skimmed, which is the same as not having one.
    """
    index: dict[str, list[str]] = {}
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        rel = p.relative_to(root)
        if any(part in INDEX_SKIP for part in rel.parts):
            continue
        index.setdefault(p.name.lower(), []).append(str(rel).replace("\\", "/"))
    return index


def ignored(root: Path, rel: str) -> bool:
    """Is this path deliberately absent? A git-ignored path is not a rotted reference.

    `.claude/seat.local.txt` is the per-worktree seat marker. It is SUPPOSED not to be in the tree,
    and reporting it as dangling would train a reader to ignore the column it appears in.
    """
    import subprocess

    try:
        return (
            subprocess.run(
                ["git", "check-ignore", "-q", rel],
                cwd=root,
                capture_output=True,
                timeout=20,
            ).returncode
            == 0
        )
    except (OSError, subprocess.SubprocessError):
        return False


def judge(clause: Clause, root: Path, index: dict[str, list[str]]) -> None:
    """Set the verdict from whether the paths resolve. NEVER decides that a rule has expired."""
    if not clause.paths:
        clause.verdict = "UNCHECKABLE"
        clause.detail = "names no artifact, so nothing mechanical can evaluate it"
        return

    missing = []
    for p in clause.paths:
        if (root / p).exists():
            continue
        if index.get(Path(p).name.lower()):
            continue  # cited by bare name and present elsewhere in the tree
        if ignored(root, p):
            continue  # deliberately absent, not rotted
        missing.append(p)

    if missing:
        clause.verdict = "DANGLING"
        clause.detail = "names path(s) not in the tree: " + ", ".join(sorted(set(missing)))
        return

    clause.verdict = "LIVE"
    clause.detail = "every path resolves; still CHECKABLE, which is not the same as still right"


def collect(root: Path) -> list[Clause]:
    files: list[Path] = []
    for rel in SCAN_ROOTS:
        base = root / rel
        if not base.is_dir():
            continue
        for p in base.rglob("*.md"):
            # SKIP ON THE PATH RELATIVE TO THE ROOT, never on the absolute one. The first version
            # tested `p.parts`, and every checkout of this repository under a harness worktree lives
            # below a directory literally named `worktrees` -- so the skip matched an ANCESTOR of
            # the repository and the scan silently read nothing but CLAUDE.md. It reported "3
            # clauses across 1 file" and looked like a result. This file exists to catch that shape
            # of failure in prose rules, and it shipped with the failure in its own scanner.
            if any(part in SCAN_SKIP for part in p.relative_to(root).parts):
                continue
            files.append(p)
    for rel in SCAN_FILES:
        p = root / rel
        if p.is_file():
            files.append(p)

    clauses: list[Clause] = []
    for f in sorted(files):
        try:
            text = f.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        clauses.extend(extract(text, str(f.relative_to(root)).replace("\\", "/")))
    index = build_index(root)
    for c in clauses:
        judge(c, root, index)
    return clauses


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", default=str(REPO_ROOT))
    ap.add_argument("--strict", action="store_true", help="exit 1 when any clause is DANGLING")
    args = ap.parse_args(argv)

    root = Path(args.root).resolve()
    clauses = collect(root)

    if not clauses:
        # An empty corpus and a corpus with no clauses look identical, and one of them is a broken
        # scanner. Say which this is rather than printing a clean-looking zero.
        print("expiry audit: NO CLAUSES FOUND across", ", ".join(SCAN_ROOTS))
        print("  That is either a corpus with no expiry conditions, or a scan that read nothing.")
        print("  Check the roots above before reading this as a clean result.")
        return 0

    by = {"DANGLING": [], "UNCHECKABLE": [], "LIVE": []}
    for c in clauses:
        by[c.verdict].append(c)

    print(f"expiry audit: {len(clauses)} clause(s) across {len(set(c.source for c in clauses))} file(s)")
    print(f"  DANGLING    {len(by['DANGLING']):4}  the artifact is gone; read these")
    print(f"  UNCHECKABLE {len(by['UNCHECKABLE']):4}  names no artifact; nothing can ever check them")
    print(f"  LIVE        {len(by['LIVE']):4}  still checkable, which is not still right")

    for c in by["DANGLING"]:
        print(f"\nDANGLING {c.source}:{c.line}")
        print(f"  {c.detail}")
        print(f"  {c.text[:200]}")

    if args.strict and by["DANGLING"]:
        print(f"\nEXIT 1 -- {len(by['DANGLING'])} dangling clause(s) under --strict.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
