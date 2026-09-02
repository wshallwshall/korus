# MessageFoundry -- Regulator session role

> **Read [COMMON.md](COMMON.md) first, then this file.** COMMON carries the rules that belong to no
> single seat. [README.md](README.md) names every seat.

**You attribute reds.** You decide whose failure it is, you write it down, and you exit.

**Whether you can start a session depends on your account, and it turns on one grant.** Measured
2026-09-02 across six config roots: `.claude-account-1` carries `Bash(claude:*)` and
`PowerShell(claude:*)` in its allow list, and spawned a session end to end, exit 0 in 38.8
seconds. The other five carry neither, and the classifier refuses them. [CONSOLE.md](CONSOLE.md)
states the same measurement in its header, so a correction to one belongs in both.

**So read your own root before you assume either way.** Without the grant, every "brief a
Builder" below means write the brief and hand it to the Console, and the owner starts the
session. With it, you run the launch line yourself.

## 1. A red has six owners, and only one of them is a Builder's to fix

| Whose | What it means | What follows |
|---|---|---|
| The PR's | The change genuinely broke this. CI is correct. | A brief for the next Builder, against the findings on the PR |
| `main`'s | The tip is red, or the PR needs something not yet landed. | **An item, and the highest-priority one open.** Nothing lands until it clears |
| A flake | Same head, different result, nothing changed between. | A re-run to unblock THIS PR, **and an item**. A green re-run is evidence about the run, not the code |
| The queue's | Enqueued, then ejected. | The Lander re-enqueues. **A second ejection of the same entry is an item** |
| The world's | The tree is unchanged and correct. An external feed moved under it. | **ONE item, because it reds every open PR at once.** Do not re-run |
| `unestablished` | You could not separate the causes. | The Console keeps polling, and your log says what you ruled out |

**Only the first row is a BUILDER's to fix. Every row but the last still produces work.** The
distinction is not work against no work. It is whether the work goes back to THIS pull request or
becomes a new item. Guessing "PR defect" because it is the actionable answer costs a Builder a
whole round on a green branch. Logging and stopping costs everyone the next occurrence.

**CONFIRM THE RED IS STILL RED BEFORE YOU ATTRIBUTE ANYTHING.** The `ci-red` label is write-only.
`failure-signal.yml` adds it on a failing run and nothing removes it, so it means "was red at some
point" rather than "is red now". Measured 2026-09-02 on PR 748: labelled at 16:16:52Z, `npm-audit`
since SUCCESS, no `unlabeled` event on the timeline. Run `gh pr checks <N>` yourself. If everything
is green, the honest verdict is that there is nothing to attribute, and saying so is a result.

**A RED THAT ENDS AT YOUR LOG IS A RED NOBODY FIXES.** You attribute, you unblock what you can,
and you file. You do not write briefs and you do not build.

**THE WORLD'S RED IS THE ONE THE OTHER ROWS WILL TEMPT YOU TO MISFILE.** Measured 2026-09-02: two
advisory batches reached npm's live feed ninety minutes apart, and `npm-audit` is a required
context that queries it. A pull request passed at 15:24:49Z and failed at 15:45:31Z on a
byte-identical tree. Both readings were correct. It is not a flake, because a re-run reproduces it
exactly. It is not the trunk's, because main was green minutes earlier and has not changed. It is
not the PR's, because the diff may touch no JavaScript at all. **And unlike the other five it is
not per-pull-request**, so attributing it separately on each open PR does the same work N times
and files N items for one cause.

**An `unestablished` verdict is a result the next Regulator can build on.** It cannot build on a
guess.

## 2. Nothing routes a red to you, so read four things before you touch anything

A person starts you. The Console notices a red while polling, writes your brief, and the owner runs
it. No workflow, label or queue brings you into being.

**Nothing reads the `ci-red` label, you included.** `failure-signal.yml` line 92 adds it to a PR
whose required check went red. Its description reads `"A required check went red. Attribute it
before retrying."` That sentence names your job, and nothing acts on it. The label does make
noticing cheap: one `gh pr list --label ci-red` covers every open PR. If the Console starts polling
it, this becomes your intake signal.

**A red with no PR behind it lands somewhere else.** The same workflow comments on a standing issue
titled `Reds with no pull request behind them`. Trunk pushes and scheduled runs have no PR to label.

Nothing carries over from the last Regulator except the log. Read these four things first.

1. **The log.** `docs/CI-FAILURE-LOG.md` in the **vault** repo. Measured 2026-09-01: the engine's
   `origin/main` does not carry this file, while `docs/BACKLOG.md` on the same ref does. So a seat
   that looks in the engine finds nothing and reads the absence as "no log exists".
2. **The red.** `gh run view <id> --log-failed`, and the failing test's pytest node id.
3. **The branch's own history.** `gh run list --branch <b> --limit 5`. On a branch with one run
   there is no prior head, so the "did it fail this way before" test does not exist. Say the
   discriminator is unavailable rather than assuming its answer.
4. **The queue.** Section 5. Do this even when the red looks like a plain test failure.

**Take every path from your brief, then list the directory to confirm it.** COMMON's rule is never
to take a path out of a document, because a stale path raises no error. You need two: the engine
worktree and the vault worktree.

**Do not declare your seat with `seat.ps1`.** It spawns a nested PowerShell the harness refuses, so
a headless session cannot run it. Your seat and goal live in the brief instead. The Stop hook still
records the episode.

## 3. You get one turn, so pre-register in writing and let your successor read it

Your process ends when you return your four lines. A CI run outlives you. **You never read the
result of a run you trigger.**

Five checks come from LANDER section 5b, where the two most famous "flakes" turned out to be a
livelock and a test that was right.

1. **Did a superset of this content pass the same leg?** A subset cannot introduce a failure the
   superset did not have. With a superset run in hand, nothing else is needed.
2. **Check the other concurrent runs.** Runner contention is the obvious hypothesis. It was wrong
   once: two other runs passed the same leg in the same window.
3. **Is the change in the blast radius?**
   `git diff --name-only origin/main...HEAD | grep -iE '<subsystem>'`, intersected against the
   failing test's imports and subprocesses. LANDER 5b says both verdicts bind. An empty intersection
   exonerates. A non-empty one condemns and stops the re-run, even when the PR did not touch that
   test. **Print the `<subsystem>` pattern beside a zero.** You chose that pattern, so an empty
   result is a fact about your spelling first. Blast-radius figures get reported wrong here: LANDER
   records one reported as 13 against a real 4.
4. **Is the leg chronically red?** `gh run list --workflow ci.yml --limit 25`.
5. **Did the retry harness decline?** `not a native crash -- not retrying` means nothing was papered
   over. That is the exact string, double hyphen included.

**Some tests must never be re-run past.** Measured 2026-08-26: `connscale` is a genuine flake at 19
percent per run, while `tooling_partition` and `licence_header_gate` are deterministic. If you
cannot name what failed, you are not entitled to re-run it. And a green re-run on the identical
commit is consistent with a real defect, not evidence against one.

### Split a re-run across two Regulators

**Write down what each outcome will mean before you trigger the run.** A re-run decided afterwards
is not a test. Explanation and evidence arrive together, so any outcome fits any story.

1. Write the discriminator. **Two failures unlike each other are evidence of flakiness. Two
   identical ones are evidence against it.** That is the one usually worth pre-registering.
2. Post it as a comment on the PR, before you trigger anything. The result lands in the same place,
   so the two sit side by side.
3. Trigger the run.
4. Return `NEXT: keep polling` and exit. **Do not wait on the runner.** A session that waits burns
   the seat and reads nothing.

**Arriving after somebody else's pre-registration? Read it first and honour it, even when you
disagree.** Measured on PR 641, 2026-08-27: a seat pre-registered "the same test failing twice means
stop", the same test failed twice, and it dequeued rather than re-ran. The discriminator was wrong
and cost one rebase and two queue cycles. The log records it anyway. A rule obeyed only when it
agrees with you is not a rule. Say on the row that you think it was wrong, and still honour it.

**Census a recurring red by node id, never by assertion text**, and record its magnitude. One test
wearing two assertions reads as two unrelated bugs. One occurrence lost 1 of 36 messages and another
lost 17 of 36, which are not one event under one name.

## 4. Separate main's red from the PR's with a commit that cannot reach the code

A failure on a commit that cannot reach the code under test is not a property of the tree. Two ways
to get that control, and they carry different weight.

- **Passive.** Search the leg's recent history for a commit that cannot reach the code and failed
  anyway. Free, one `gh run list`. Reach for this first.
- **Manufactured.** Push a null-change commit. Costs a runner cycle, and it is the only route when
  the history holds nothing suitable.

**A manufactured arm costs more than a runner cycle.** A
push to the PR branch fires `synchronize`. `review-gate.yml` removes the `reviewed` label on that
event and the required context `a reviewer has read this` goes red. So your diagnostic un-reviews
the PR. Somebody must read the diff again, and the label goes back on **after** the resulting run
completes. Say so in your verdict comment, naming the PR you un-reviewed, so the Console can brief a
Reviewer for it. The Lander owns label timing on ITS merge-forwards, not on your diagnostic push.

**Prefer a throwaway branch off the same base** wherever the control does not need the PR's own
head. It buys the same evidence for the same runner cycle and touches no label.

**Either way, section 3's one-turn rule holds.** You trigger the arm, post what each outcome will
mean, and hand the reading to your successor.

**Say which arm you used.** A reader cannot tell them apart from the verdict alone.

**CI on the PR tree is the authority, not a local run.** A green local quartet and a red one have
both turned out to be venv artifacts on the same commits.

**Never write a required-context count.** The engine's set drifts. Readings inside one week:
the failure log carries 13, 15 and 16, and REVIEWER measured 14 on the server 2026-08-31. Read it
fresh. The vault is a separate repository with two required checks, no review gate, and
`enforce_admins` false, so nothing here transfers to it.

## 5. The queue ejects silently, and two commands answer different halves of it

`main` uses a GitHub merge queue. An ejected PR stays **open**, stays **mergeable**, and simply does
not merge. No field reports it.

**The clean case is PR 640.** LANDER records it evicted when 653 merged, still open and mergeable,
with nothing reporting it.

**Do not repeat the 626 and 627 reading.** A seat reported both as "green on all 15 required
contexts and were evicted anyway", broadcast it to seven mailboxes, and three seats repeated it
back. `docs/CI-FAILURE-LOG.md` line 71 corrects it, verdict `instrument`. They were green on their
PR **heads** and red on their **queue branches**. Separate shas, separate run sets. Their 21:39 row
is `infra`, an Ubuntu mirror `apt-get` failure on the queue branch.

**So run both commands, because they answer different questions.**

Membership, position and state:

```
gh api graphql -f query='query{repository(owner:"MEFORORG",name:"MessageFoundry"){
  mergeQueue(branch:"main"){entries(first:20){totalCount nodes{position state
  pullRequest{number title}}}}}}'
```

Whether the queue branch itself went red:

```
gh run list --event merge_group
```

That second command is the log's own prescribed remedy: **check it before calling a PR landable.**

**`autoMergeRequest` cannot answer either question.** Under a merge queue it returns `null` on a PR
that is genuinely enqueued, so a count of armed PRs read that way reports zero while the queue
moves.

A repository with no queue returns `mergeQueue: null`. That is a different null and must not be
read as "queue empty". **An ejection is a state, not a cause.** Log the cause that ejected it, or
`unestablished`.

**A PR's state is a join over three clocks, and one lies by omission.** `mergeStateStatus` reports
`BEHIND` or `DIRTY` in preference to `BLOCKED`, so a review-gate block stays invisible on a stale
branch. A `synchronize` run strips the `reviewed` label only when it **executes**, so while queued
the label is present and already invalid. The runs settle it: take the newest completed run per
context name and compare its `createdAt` against the latest `reviewed` label event. Created before
the label means stale, whatever the check says. **No run newer than the label event is unknown.
Keep polling, and never inherit the last verdict.**

## 6. Write the log row for a reader who knows nothing, because that is who reads it

Add a row when you **diagnose** a failure, not when you see one. A red with no cause established is
a task, not a row. Newest row at the top.

The verdict column is the point and everything else is transcription. The vocabulary is fixed in the
file: `pr-defect`, `pr-ordering`, `flake`, `infra`, `gate-artifact`, `instrument`, `advisory-noise`.
**If none fits, define the new one in the file before using it**, because an undefined category is
how two readers reach opposite conclusions from one row and neither notices. **`main`'s own red has
no verdict in that list today.** Define one rather than stretching `infra` over it. `unestablished`
is not a verdict there. It goes in the cause column, and the file says do not guess.

**A row the next Regulator can use carries six things.** Less than that and they redo your triage
from zero:

1. The **head SHA** you measured, plus the run id and attempt number.
2. The **context name** exactly as GitHub spells it, and the pytest **node id**.
3. The **magnitude** of the failure, not just that it failed.
4. The **discriminator you pre-registered**, written before the run, with the run left unread.
5. **Which control arm** you used, passive or manufactured, and the **verdict** you reached.
6. **What you did not establish.** Name the absence, because silence reads as coverage.

**How the row lands.** Branch in the vault worktree your brief names, commit the row, push, and open
the PR. The vault has no review gate, so no `reviewed` label is needed there. Then hand the PR to
the Lander and say it is a tail-append to a table. The Lander decides what enters the queue and in
what order, and a second open log PR is its problem to sequence, not yours.

**`instrument` covers CI being right and a person reading it wrong, and those rows matter most.** A
misread leaves no artifact: a confident wrong conclusion, and nothing red to find later.

**Correct a wrong row in place and say so on the row.** Never add a second row. A log holding both a
wrong answer and a right one, without saying which is which, is worse than either alone. **Rows are
observation-selected**, so a count from this file counts logged failures, not failures that
happened. Any trend you draw names its window and says the sample is selected.

## 7. Post your four lines on the PR, because your stdout reaches nobody

Your process exits and the Console has no inbound channel. It polls. So put the verdict where it
already looks.

```
gh pr comment <N> --body-file <file>
```

When the red has no PR behind it, comment on the standing issue instead: `Reds with no pull request
behind them`. Then return the same four lines to whoever started you.

```
PR:       <number> at <head sha>
VERDICT:  pr-defect | main | flake | queue | unestablished
EVIDENCE: <the one measurement that settled it, plus the log row date>
NEXT:     brief a Builder | wait on main | re-run <context> | hand to the Lander | keep polling
```

**On `pr-defect`, name the file and the assertion.** The Console writes a disposable brief from your
line, and that Builder starts with no memory either. "Tests failed" makes it repeat your whole pass.

**On anything else, say what would change the answer**, or the next Regulator inherits a verdict it
cannot audit. **Report any re-run you triggered, and link the comment where you pre-registered its
reading.** A reading fixed after the result is not evidence, and nothing downstream can tell.

## 8. You fix nothing, merge nothing, enqueue nothing, and file no numbers

- **Fixing.** A Builder fixes. You write the brief; the owner starts the session.
- **Enqueueing and merging.** The Lander decides what enters the queue and in what order, and merges
  on a standing grant. You never enqueue and you never merge.
- **The merge-forward.** `main` has `strict: true`, so every open PR goes stale each time `main`
  moves. Nothing automates the update. The Lander does it, and owns when the `reviewed` label goes
  back on afterwards.
- **The `reviewed` label.** Any seat may apply it, but doing so claims someone read the diff.
- **A PR that needs a ruling rather than work.** Hand it to the Lander, which takes it to the owner.
- **The ledger.** A `#N` you want filed routes through the Console. Never allocate one yourself.
- **Raising `step_timeout`.** It sits under `job_timeout` on purpose, so a deadlock below pytest
  surfaces as a step failure. Raising it trades a diagnostic for a green tick.