---
name: "fleet-anchor-work"
description: "Anchor, stash, restore, or go near another session's uncommitted work. Use before any act that could disturb a shared worktree or the shared stash stack."
user-invocable: true
disable-model-invocation: false
---

# fleet-anchor-work

> Shared fleet rules, split out of [COMMON.md](../../../roles/COMMON.md) on 2026-09-05.
> Prohibitions that bind before this task starts stay in that file. Read it first.

### Anchor with plumbing and a narrow tree

```
git hash-object -w <file>   # per file
git mktree                  # over just those entries
git commit-tree
git update-ref refs/<ns>/<name>
```

No checkout, no index, and the shared stash stack is untouched.

**The tree contains only what you listed, and that is what makes it better than a whole-tree
snapshot.** A `read-tree HEAD` plus `add -A` anchor carries stale copies of every file its author
was not working on. Restoring one whole silently reverts finished work while looking like a rescue.

A narrow tree has nothing stale in it to restore. Recover one path with `git cat-file -p
<ref>:<file>`. Verified independently: vault `git status` md5 identical before and after, stash
entries unchanged, three other seats' dirty files untouched.

**Verify an anchor by reading its content back, never by `update-ref`'s exit code -- it returns 0
either way.** Read a file back out through the ref and search it for something you know you just
wrote.

Verified with a control that must stay absent. Two strings written minutes earlier were found
through the ref, a nonsense token was absent, and the read returned `rc=0` over 113,189 bytes.

The seat that contributed this stated its own limit unprompted: of its 73 anchors it applied the
read-back check to **two**.

The other 71 were verified only by "the command exited 0 and the working trees were unchanged". That
proves it disturbed nothing. It does not prove any ref holds what it thinks.

**Anchoring is necessary and not sufficient. An anchor itself can be poisoned, and you cannot filter
by when it was taken.** Three contaminated rescue refs, not two.

One was taken at rung 1, three minutes **before** anything was stopped, so a poisoned anchor is not
a stop-time artefact. Any anchor taken while a round is running can capture a planted mutation.

Contamination is not uniform either. Two anchors from the same sweep, same second, same command,
came out one clean and one not. One item's mutation was already planted, and the other's arrived
three minutes later.

**"Anchors taken during a round are suspect" is the right instinct and a useless filter. Read each
one's content.** Rename rather than delete: `refs/rescue/POISONED-DO-NOT-RESTORE-*` keeps the
objects and stops a recovery reaching one by accident.

**And the inverse is the claim a recoverer actually depends on:** not "I marked the bad ones" but
"no bad one is still innocuously named".

The first is a statement about your own diligence. The second is a statement about the population,
and only the second is what someone reaching for a rescue ref needs to be true. Proving the first
proves nothing about the second.

This is `SDS-3.6` -- a completeness claim is a liability -- pointed at a cleanup instead of at
prose. Verify that direction explicitly, and if you cannot, say the population is unswept rather
than reporting the count you fixed.

**A 1-line diff in a worktree you just halted is as likely to be sabotage as progress.** A stop that
ended four adversarial rounds left two worktrees with one modified file each, 1 insertion and 1
deletion -- the shape of half-done repair work.

**Both were deliberately planted mutations left unrestored: the stop caught a verify lens between
plant and restore.** One had swapped a stderr receipt to `$null = (...)`, the exact defect its item
exists to remove, re-inserted on purpose to test a test.

**Size and shape cannot tell sabotage from progress. Read what the line does.**

Two corrections came with it. *"Commit what is built"* is unsafe across a halted round.

*"Uncommitted work is what the dark destroys"* does not apply to anchored work. `refs/rescue/*` are
real commit objects and survive like any branch commit. What dies is unanchored, uncommitted diffs.

Those rescue anchors had themselves captured the mutated state, so restoring from them restores
sabotage while looking like a rescue. **Verify a restore by content, never by a revert's exit
code.**

**When you probe someone else's defect inventory, your token is the instrument.** Two probes failed
in five minutes. The first called a known-poisoned anchor clean: it tested one file across all three
refs when the sabotage was per-item and sat in a different file.

The second tested both files and reported the defect present on `origin/main` too, so the token was
wrong, not the refs. Both times the control is the only thing that said so, and both times the
failure was silent and plausible.

**A probe for a defect you did not plant needs the exact discriminating string from whoever planted
it.** A token you inferred is a guess wearing a measurement's clothes. The right move was to stop
and hand the question back.

**Do not delegate anchoring to the automatic capture. Its success line reads like coverage and it
covers 9 percent.** Measured twice on 2026-08-29: run one saved 23 worktrees and left about 147 of
170 never scanned; run two saved 15 and left about 155 unscanned -- 91 percent unchecked.

Its **first** line says "23 dirty worktree(s) saved as patches", which reads as a completed job. Its
**second** line says it stopped after 12 seconds with 147 unscanned.

It is time-boxed, so the slower the machine the less it covers -- it covers least exactly when the
fleet is busiest, which is when a ceiling arrives.

**And the at-risk directory tells you about the capture, not about you.** A patch named for your
worktree means it was captured. No patch means only that it was not scanned. It says nothing about
whether you are clean. **Do not check the directory. Check your own tree.**

**The commit author field cannot separate seats, and it varies just enough to look like it can.**
One human owns every commit in these repositories.

Measured 2026-08-29: all 5 commits under `docs/boards` are authored under one human name. The last
200 vault commits carry four distinct author values: a full name 105, the GitHub handle 86, a given
name 5, `dependabot[bot]` 4.

**That is worse than a single constant: a field that varies looks informative, and none of its
values maps to a seat.** An attribution check reading the author field will confirm any guess you
bring to it. What actually distinguishes seats: the pull request number, the branch, or the seat
record.

**Refusing to act on someone else's work in a shared structure is correct even when you are
certain.**

A seat found another seat's files in a parked autostash. It inspected them with `git stash show
--stat` and `git show stash@{0}:<path>`, and did not pop, because the stack is shared and the work
was not its own. The addressee was wrong.

The handling was right, and a pop would have conflicted and could have reverted the real owner's
newer boards.

**For a generated file, byte size is the wrong discriminator.** A 39,850-byte stashed page against a
93,445-byte tip read as an older generation.

It is not. It is a different build mode of the same generator, same day: a `--local` build that
loads a sibling `burn-data.js`, against a `--snapshot` build that inlines the whole record.

Verified: the expired-instant guard added that morning is present in both, and a control token is
absent from both. **Two builds minutes apart differ in every timestamp; two modes differ by 54 KB
with identical behaviour.** From outside the generator, smaller genuinely looks older.

**And a generated file differs from every commit by construction, so "matches no commit" is evidence
of nothing.** A stashed page's md5 matched none of its ten commits, and that briefly read as "unique
work at risk".

A generated artefact embeds its own build stamp, so byte-difference from every commit is the
expected state. A recovery check treating "matches no commit" as "unsaved" will flag every generated
file in the repository, forever, and be right about none of them.

**What actually made that stash safe to ignore is simpler and stronger than "it is older".** Both
files are generated and reproducible in one command; the generator is
`scripts/coord/board_index.py`. Neither is a source.

There is nothing in it to recover at any age. That is a property of the artefact rather than a
judgement about which copy is newer, and it would have been right even with the sizes reversed.
**Ask first whether the thing is a source.**

An age comparison you did not need is an age comparison you can get wrong. And if a shared stash
entry must go, drop it by SHA (`535a8761`), never by `stash@{0}` -- that index moves when any
session pushes.

**Pre-register the control before the change, and say that you did.** A seat landed a six-commit
ASVS record repair. It reported the verdict distribution unchanged at **176 pass / 99 partial / 2
fail / 65 na**, writing the expected pair down before merging, not after.

A record repair that moved a verdict would have meant the change did something other than what its
author said, and only a number fixed in advance can catch that. A check chosen after seeing the
result cannot fail: whatever came out becomes the expectation.

It also disclosed a caveat that weakened its own report -- the tree read `+dirty` on both refs --
rather than letting a clean-looking number stand. The dirt was two board files, neither feeding the
scorecard.

**When you clear yourself of a defect, check the commit before your FIRST edit of that content, not
before your last batch.** Four bare `0xb7` bytes crashed a required gate on every vault pull
request. A seat checked `a19c891d~1`, found the bytes already there, and told the reporter "not my
bytes".

True, and wrong: they were there because that seat wrote them in `ce389a39` earlier the same
morning. `a19c891d~1` was the commit before the last batch, and the question was about the first.

**The instrument answered a neighbouring question and the answer was exculpatory, which is the
direction that gets the least scrutiny.**
