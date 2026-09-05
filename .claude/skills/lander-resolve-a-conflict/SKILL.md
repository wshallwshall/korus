---
name: "lander-resolve-a-conflict"
description: "Resolve a merge conflict on a pull request you are landing. Use when a PR reads DIRTY or a merge is refused, including disarming before you resolve."
user-invocable: true
disable-model-invocation: false
---

# lander-resolve-a-conflict

> Task rules for the Lander seat, split out of [LANDER.md](../../../roles/LANDER.md) on 2026-09-05.
> The prohibitions that bind before this task starts stay in that file. Read it first.

### 4c-bis. On an ARMED PR, resolving the conflict IS the merge, so disarm before you resolve

DIRTY plus ARMED plus zero required reviews is a loaded trigger. DIRTY is the only thing still
stopping the merge, so resolving it merges, with no review and no pause. Read
`required_approving_review_count` before assuming otherwise.

That composition turns a queue **ordering decision** into a **race**, and the race is invisible: the
PR looks blocked right up until someone helpfully fixes it.

| Item | Rule |
| --- | --- |
| Disarm first | Disarm before resolving any conflicted PR whose landing you want to sequence. Disarming is cheap and reversible; an unintended merge is neither. |
| Never resolve against a moving base | Do not resolve a conflict against a shared file another session is about to rewrite. |
| Why | A mechanical keep-both-sides resolution across a large reorganisation produces the silent revert under *Classify a conflicted row by WHO CHANGED it*. |
| Ordering for a queued bulk rewrite | Disarm the conflicted PRs, land the bulk rewrite, then re-resolve them against the resulting file. The reverse order resolves twice and risks merging mid-rewrite. |
| Any mutation of an armed head merges | A push clears the same last gate a resolution does. Bracket every push to an armed PR with a disarm and a re-arm. |
| Read the head back between them | A resolution shows its own result; a push does not. |
| The sequence measured 2026-08-22 | The author mails before pushing, the lander disarms, the lander pushes, the lander reads the head back, the lander re-arms. |
| A superseded tip: cherry-pick forward, never force-push | A server-side `update-branch` creates a merge commit the holding session never fetched, so its push is rejected non-fast-forward. |
| Why force is wrong here | It would drop the `update-branch` MERGE as well as the peer's commit, re-BEHINDing the PR you just cleared. |
| The recovery, in order | 1. Disarm. 2. Cherry-pick the peer's commit onto the current tip. 3. Fast-forward push, then read the head back. 4. Re-arm. |
| Then prove identity | `git patch-id --stable` on both sides, under the limits stated in *Arming auto-merge freezes the PR at that SHA*. |

### 4c-quater. A force-push safe in CONTENT is still an AUTHORITY question, so push a fresh ref

| Item | Rule |
| --- | --- |
| Separate the two questions | "Would this lose anything" is yours to answer. "May I rewrite a pushed ref" is the owner's. |
| What every other warning covers | Every force-push warning in this file and in COMMON warns about what a force-push would DESTROY. None says what to do when the content check comes back safe. |
| The zero-cost path | Measured 2026-08-22 on a rebase of a dead lane's branch: the force-push was provably safe in content and went to a FRESH REF instead. |
| Why that settles it | The original branch was left untouched and inspectable. That satisfies both questions at zero cost and needs no ask. |
| Gate available | `push_guard` rejecting a non-fast-forward push to any lane branch. Route it to whoever builds gates. |
| **EXPIRY** | The owner delegates force-push, at which point the content check stands alone and the fresh ref becomes optional. |

## 8. Merge conflict resolution -- the part no merge tool can answer

### 8a. Classify a conflicted row by WHO CHANGED it, never by which side the merged content equals

The sharpest control failure recorded here, and it was found only because its author attacked their
own control. An audit asked, per row, *"does merged match ours or theirs?"* Then reverting a row to
base **PASSED**: 3 of 5 planted attacks slipped through.

Reverting a row to base is indistinguishable from "ours won" whenever `ours == base` for that row, and
`ours == base` is exactly when **theirs** was the only side to edit it. **So the control passed
precisely in the case it existed to catch, and its green was strongest where it was weakest.**
Re-attacked after the fix: 5 of 5 caught.

| relative to base | merged must equal |
| --- | --- |
| only ours changed | ours, else SILENT-REVERT |
| only theirs changed | theirs, else SILENT-REVERT |
| both changed | ours or theirs -- a real call; log which |
| neither changed | base |

| Item | Rule |
| --- | --- |
| Assert the mutation landed | Every attack must prove its mutation actually applied before judging the audit. A no-op mutation makes a blind control look sound. |
| Enumerate from a diff | Compute the rows in play from the merge base, never from memory of one. |
| The measured case | The first pass reported three rows and an audit found a fourth. |
| What the base showed | Ours and theirs had touched **disjoint** sets, so every row had one owner and the correct merge was fully determined with no judgement call. |
| What a hand-resolver sees | Only the rows inside the markers. |

### 8b. "Keep both sides" is a semantic instruction, not a mechanical one

A keep-every-line merge can auto-merge clean, leave no markers, pass every check, and still **restore
the defect the branch removes**, because the other side's insertion carries your pre-fix line in as
context. **Verify a resolution for INTENT, not cleanliness.**

Verify a ledger merge in **three** directions, over `parse_items`, and never on a total:

1. Nothing lost from `main`.
2. Nothing lost from the branch.
3. The set of items present beyond `main` is EXACTLY the set you intended, compared by item number and
   not by count.

| Item | Rule |
| --- | --- |
| Why direction 3 is not optional | Presence tests and row counts CANCEL on "added correctly and quietly dropped something else". |
| Where that failure is already named | The census rule under *The ledger reconcile pass* names it, and nothing named it for the merge. |
| The rest of the worked check | All items asserted present by heading; heading count with zero duplicated numbers; the canonical status checker green with every item declaring exactly one status. |
| And two more | A check for a line-ending mass-rewrite, and **one section read end to end**, because two cleanly merged edits can still leave it incoherent. |
| Measured 2026-08-22 | Zero lost either way, and added-beyond-main was exactly the two numbers that branch was filing. |
| Gate available | Script the three set comparisons over `parse_items` output and run it as a pre-push check on any branch touching `docs/BACKLOG.md`. |

### 8c. Resolve against the right base

| Item | Rule |
| --- | --- |
| The trigger | "My base is an unmerged PR HEAD", not "old branch", so it fires on brand-new stacked branches too. |
| What it hides | A pre-squash base hides a revert behind a clean three-dot diff. |
| The rule | Never stack; branch off `origin/main`. |
| The symptom pair | Resolving against the wrong base yields a PAIR of opposite symptoms, one loud and one silent. Fix the base; the silent half is the one that corrupts a safety check. |

### 14n. `git merge-tree --write-tree` prints a valid tree OID even when the merge conflicts

It signals the conflict **only in the return code**. Reproduced: on a genuinely conflicting pair it
printed `018888f5d959653388a588c6f7c4379f5548e99f`, which `git cat-file -t` confirms is a **real tree
object**, while returning `rc=1`.

So a check testing whether the output *"looks like a 40-hex SHA"* reports **CLEAN on a conflicted
merge**. A peer used it as their will-this-land-safely instrument for a whole session. It was right
every previous time only because those merges were genuinely clean.

**Read the rc, and capture it with no pipe in between.** Measured the same day: piping merge-tree
through `Select-Object` printed `exit=0` on a merge that had conflicted, because `$LASTEXITCODE`
reflects the last element of the pipeline. Same family as `$?` after a pipe (SDS-3.8, *confirm your instrument answers the question you asked*).

### 14p. Git raised the cosmetic conflict and merged the semantic one silently -- a shared version integer

The worst instance of the keep-both-sides family measured so far, because **resolving the visible
conflict correctly still ships the defect.**

Two unmerged branches off the same merge-base each bumped `ENGINE_UI_SEAM` 18 to 19, for two
**different** contract changes: `SystemStatus.log_sinks` and `SecurityPosture.store_privilege`.
Trial-merging them:

- `messagefoundry/api/_ui_seam.py` conflicts, **but only in the adjacent comment blocks**, 2 markers.
- `tests/golden/webconsole_seam.snapshot` **auto-merges clean: 196 lines, ZERO conflict markers,
  carrying BOTH fields at seam 19.**

So the natural keep-both-comments resolution yields seam 19 describing two independent contract
changes, the golden gate whose whole purpose is catching seam contract changes **agrees**, and
`SUPPORTED_ENGINE_SEAMS={19}` accepts it. Whichever branch lands second must re-bump to 20 and
**nothing enforces that**.

**A monotonic counter shared across branches is not protected by conflict detection.** Git conflicts
on the LINE, and both sides wrote the same line, `= 19`, so there is nothing to conflict. Two sides
agreeing on a value is indistinguishable from two sides making the same change.

Whenever a version integer, migration number or protocol seam is bumped on more than one branch, check
it across all unmerged branches **by value**: `git grep '^CONST' <every ref>`. One command, and no gate
does it for you.

### 14w. Three plumbing traps from one conflict resolution, 2026-08-20

| Trap | Detail |
| --- | --- |
| `git read-tree -m` is a TRIVIAL merge only | It left two **content-mergeable** files unmerged, which reads as "these conflict" when it means "I do not do that". |
| `git merge-tree`'s CONFLICT output is MULTI-LINE and the tree OID is line 1 | Capturing the whole thing and passing it on yields `not a valid object name`, an error about your capture, not your tree. |
| A truncated `diff --stat` reads exactly like an absence | The lander briefly believed ledger edits had been lost. **Nothing shown is not nothing there.** |

## 16l. A GATE YOU HAND A PEER IS A CLAIM, and a COUNT cannot answer a WHICH-VERSION question

**Measured 2026-08-13, and the peer was right.** Resolving a backlog conflict, a lander correctly
warned a lane that main had corrected two lines their branch predated, so a hand-assembled union could
reinstate retracted text with no marker. The lander then issued a gate to prove the merge safe:

    grep -c "THE REMEDY IS STRONGER THAN THIS ITEM CREDITS"  -> expect 0
    grep -c "| 50 | **#1020**"                               -> expect 0

**Both assertions were false about `main` itself**, which has one occurrence of each. The lander had
read `+79 -2` in a diffstat and inferred deletion. **A modification is a delete plus an add**, so those
two minuses were the old halves of two in-place rewrites.

The lane checked all three trees -- base, main and their branch, 1 and 1 everywhere -- refused to push
against a gate they had disproved, and asked.

| Item | Rule |
| --- | --- |
| The inverse trap, reached BY COMPLYING | Forcing that assertion to 0 would have DELETED two lines main deliberately keeps: the exact defect being warned about, arrived at by complying. |
| Why | A gate handed downstream is executed by someone who did not derive it and cannot see the premise it rests on. |
| So | **When you issue a gate, you own its premise. State what you measured it against and on which ref.** |
| Wrong dimension, not weak check | The question was never *does this line exist* but **which version survived**: main's corrected text, or the pre-correction text from the branch's base. |
| Why the count could never work | Both worlds contain exactly one occurrence, so it prints `1` whether the merge is safe or carries precisely the feared defect. |
| The distinction from a gate that cannot fail | This one *could* have failed, if the line were absent. It measures the wrong **dimension**: cardinality where the question is **identity**. |
| The stated form | AN INSTRUMENT THAT RETURNS THE SAME VALUE IN THE SAFE WORLD AND THE FAILING WORLD IS NOT A WEAK CHECK. IT IS NOT A CHECK. |
| The operative test, one sentence | Before trusting a green, ask **what value this instrument would have printed had the thing I fear been true.** Same value means the green carries no information. |
| The correct gate, which the lane wrote | Compare the merged line **byte-for-byte against BOTH** main's version and the pre-correction base's version, and report which it equals. |
| The guard that makes it sound | **Assert those two differ.** A comparison whose sides are identical passes for the wrong reason, so without that guard the check is a tautology dressed as evidence. |
| When to adopt this shape | Whenever the risk is *which version survived* rather than *whether something is present*. |
| Absorbing churn | Advancing another PR mid-resolution staled that lane's merge and forced a re-merge. |
| The rule | **Mechanical updates are the lander's to absorb. A peer mid-resolution is the one party whose work should not be invalidated by queue management.** Hold the queue while someone is resolving, then drain. |
