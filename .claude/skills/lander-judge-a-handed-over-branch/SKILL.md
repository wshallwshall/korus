---
name: "lander-judge-a-handed-over-branch"
description: "Judge a branch handed over by another session or a dead lane. Use to decide whether its content already landed, and whether the tip has diverged."
user-invocable: true
disable-model-invocation: false
---

# lander-judge-a-handed-over-branch

> Task rules for the Lander seat, split out of [LANDER.md](../../../roles/LANDER.md) on 2026-09-05.
> The prohibitions that bind before this task starts stay in that file. Read it first.

### 13a. A handed-off tip is not necessarily a descendant of what is already pushed

A lane hands you a tip in good faith and it can still have DIVERGED from the PR head rather than
advanced from it, because the lane committed while the remote also moved.

**Measured 2026-08-20: four commits on origin against five on the lane.** Force-pushing the handed-off
tip would have silently discarded four, including an ADR-index collision resolution and a
lander-authored banner. **The lane was not wrong and its tip was not stale.** The two lines were
simply not on one path.

```
git merge-base --is-ancestor <pushed-head> <handed-off-tip>          # rc=0 -> safe to fast-forward
git rev-list --count --left-right <pushed-head>...<handed-off-tip>   # "4  5" means DIVERGED
```

| Item | Rule |
| --- | --- |
| The count is the PRIMARY instrument | `--is-ancestor` is DIRECTIONAL, and a backwards asking returns rc=1, which is indistinguishable from real divergence. |
| Measured 2026-08-20, one turn after this entry was written | A lander almost cancelled a safe push over it. It asked *"is the NEWER tip an ancestor of the OLDER"*, got rc=1, and read divergence. |
| What was actually wrong | The instrument was fine and the direction was inverted: a true answer to the question actually typed, which was not the question meant. |
| Reproduced | `git merge-base --is-ancestor aa025d73 a0d9c1b4` gives rc=1, backwards. `git merge-base --is-ancestor a0d9c1b4 aa025d73` gives rc=0, correct. |
| The unambiguous form | `git rev-list --count --left-right a0d9c1b4...aa025d73` prints `0       1`: zero behind, one ahead. |
| Why the count cannot lie | It prints BOTH sides, so a fast-forward shows a zero and divergence shows two non-zero numbers whichever order you type. |
| What swapping the arguments does | Swaps the columns and changes nothing else. Run the count even when `--is-ancestor` answers. |
| When they have diverged, MERGE, do not force | In that instance the merge was itself a fast-forward and needed no force at all. The destructive option was just the one that came to mind first. |
| Then verify | That the result carries the lane's work byte-identically, rather than trusting a clean merge. |
| The tell | A push REJECTED non-fast-forward is the gate working. The reflex it provokes, force, is the one action that turns a caught problem into a silent loss. |

### 14b. The instrument ledger for "is this change already on `main`"

Assembled 2026-08-20 from a tree-identity pass over 21 local-only commits: novel 8, no-op 2,
conflict-in-isolation 11. Four seats asked this one question and three instruments answered the
neighbouring one.

| Instrument | Verdict | What it actually answers |
| --- | --- | --- |
| `git merge-tree <main> <commit>` | **WRONG QUESTION** | merges the commit's WHOLE ANCESTRY, not its change |
| blob OID of a touched file | **WRONG QUESTION** | is the FILE identical -- a file can differ while the change is present |
| `git cherry` | **UNUSABLE HERE** | **100 percent false positive under squash-merge: 30 of 30 on a branch known landed** |
| line-presence of the ADDED lines | **WORKS** | are those exact lines on `main` |
| **tree identity**: apply onto `origin/main`, compare the resulting tree to main's | **WORKS, within the scope limit below** | *would landing this change anything* |

| Rule | Detail |
| --- | --- |
| Reach for tree identity first | A byte-identical resulting tree settles the question without any argument about which lines matter. |
| And it makes NO-OP a first-class outcome | Two commits in that pass produced a tree byte-identical to main's, so the work was already there under a different subject. |
| **Its scope limit, corrected by its own author within the hour** | Without this the row above over-promises. A tree test catches a NO-OP; it does NOT catch a redundant-but-differently-worded change. |
| The measured pair | Two commits adding **the same marker to the same test with different comments** both read NOVEL, because the resulting trees genuinely differ. |
| The patch-id landedness test | `git diff $(git merge-base main <branch>) <branch> \| git patch-id --stable`, compared against the candidate squash's patch-id. |
| Its asymmetry, which gets dropped | **A MATCH PROVES LANDED. A NO-MATCH PROVES NOTHING.** A rebase or an amended squash breaks the equality without the work being missing. |
| Patch-id's one direction | Identical patch-ids correctly proved a double-land and saved a duplicate landing. |
| The other direction, inside the same hour | Different patch-ids would have called two same-marker commits non-duplicates. **PATCH-ID ANSWERS "SAME DIFF", NEVER "SAME CHANGE".** |
| No byte-level instrument closes the gap | Reading the target is what catches a redundant-but-reworded change. A human or an agent reads the target. |

**The positive discriminator those instruments cannot supply: ask which merged PRs came *from* the
branch.** Every row above asks a CONTENT question that squash-merge breaks. PR provenance asks a
different question squash cannot touch, because the PR record keeps the head branch name.

**INSTRUMENTS 4.6.8b owns the query and the caveat that makes two commit counts of one branch
disagree. Use it rather than re-deriving it here.**

| Rule | Detail |
| --- | --- |
| Run it before judging a handed-over branch | Measured 2026-08-22 on two dead lanes routed in the same window. |
| What it separated | One had several merged PRs from the branch, so most commits were squash residue and only a handful were genuinely unlanded. The other had none. |
| Why that matters | **Both were handed over with the identical description: "N unpushed commits of built work".** That phrase is ambiguous by construction. |
| State its limit | It tells you what LANDED from that branch, never what the remaining commits contain. |
| Conflict-in-isolation is a finding, not an obstacle | A commit that will not apply to `main` without its predecessors makes selective cherry-picking impossible rather than unwise. |
| What it proved in that pass | Five commits SUPERSEDED rather than pending, because they refined a comment added by a commit that should not land. Do not route around it; read it. |
| **The enumeration read as the branch** | A new shape of SDS-3.6, *a completeness claim is a liability*. A branch triaged commit-by-commit covered **5 of 23**, and three of the eighteen never considered fixed a race that then redded one of the lander's own PRs. |
| Why the gap was invisible | Every one of the five decisions was individually correct. |
| The check is one command | `git rev-list --count origin/main..<branch>` against the length of the list you were handed. Run it before you report on a branch. |

### 14m. A stable count and a verified chain are both weaker than they look

| Trap | Detail |
| --- | --- |
| A count stable across two readings is not thereby verified | A held branch was recorded as *"tip `a5276a39`, 3 commits"*, then *"tip moved to `ed8a09d7`, still 3 commits"*. |
| What was reported as the finding | The moving tips, **because the counts agreed**. `a5276a39` was **one** commit off main; the 3 belonged to a tip that did not exist yet. |
| Why it is the worst way to be wrong | The number was wrong at both readings and agreed with itself, so a second look confirms it. Re-derive from the ref, never from the note. |
| A chain of verified links is not a verified chain | A five-step argument toward a security re-score had every premise independently true and the conclusion false. |
| Where it broke | One function *between* two correctly-measured facts had never been opened. It wrapped the call in `except Exception`, logged, and returned, and the quantity was recomputed from scratch each pass. |
| So the real behaviour | The failure was **deferred and self-healing**, not lost. |
| The rule | When a chain of true facts reaches an alarming conclusion, open the one thing in the middle nobody has read. The gaps BETWEEN the links are invisible precisely because every link you checked held. |
| A retracted finding is worth more than a filed one | And is much harder to produce, because a filed finding looks like output. |
