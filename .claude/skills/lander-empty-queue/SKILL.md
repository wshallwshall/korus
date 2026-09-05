---
name: "lander-empty-queue"
description: "Act when the merge queue reads empty or frozen. Use to tell a real drain from a stall, and to pick the next useful work."
user-invocable: true
disable-model-invocation: false
---

# lander-empty-queue

> Task rules for the Lander seat, split out of [LANDER.md](../../../roles/LANDER.md) on 2026-09-05.
> The prohibitions that bind before this task starts stay in that file. Read it first.

### 4g. If you build a drain, these are its failure modes

| Item | Rule |
| --- | --- |
| A snapshot drain cannot see later work | Hardcode the PR list and a PR opened five minutes later is invisible. On "queue empty" it exits and leaves that PR armed and stalled forever. |
| Widening the snapshot is not the fix | That is a fresher guess. Re-read `gh pr list --state open` every pass. |
| One PR per pass | Every merge re-behinds its siblings. |
| Validate the probe's output SHAPE | A `gh --jq --arg` error printed usage to stderr and the empty stdout was read as "nothing eligible" while two PRs sat eligible. |
| Why that matters | Otherwise "looked and found nothing" is indistinguishable from "did not look". |
| Starvation looks like a hang | While three PRs merged in sequence, two others could never catch up. Each time they finished a run, `main` had moved. Nothing was broken. |

### 4g-bis. An edge-triggered watch reports transitions, and EMPTY is not one

A watch keyed on `main` MOVING fires when a landing happens. It cannot fire when landings stop,
because "quiet" and "idle with work waiting" arrive identically. Both are an absence of transitions.

**Measured 2026-09-05.** The queue drained at 13:16 CT. PR 818 then went CLEAN and sat un-enqueued
for ninety minutes, and nothing reported it: two hours with no landings and a green pull request
waiting.

| Item | Rule |
| --- | --- |
| The failure direction is SILENT | A watch that has stopped firing looks exactly like a fleet with nothing to do. It goes quiet at the moment a Lander is most needed. |
| So | A watch whose job is to keep a queue moving must ALSO fire on the queue reaching EMPTY, never only on `main` moving. |
| The general form | An edge-triggered instrument cannot report a steady state. Where the condition you care about is a LEVEL rather than a TRANSITION, key the watch on the level. |
| Never read quiet as drained | Count open PRs yourself each pass. "No transitions" is not "no work", and only one of those two needs you. |
| **EXPIRY** | The watch fires on EMPTY as well as on a landing, and a drained queue holding an eligible PR raises within one poll. |

### 4h. Coupled cross-repo pairs (engine + vault)

A change that edits text an ASVS evidence anchor resolves against is one change in two repos, and the
vault gate resolves anchors against engine `main`, not against a PR.

1. Build both halves; verify the gate against the engine worktree carrying the uncommitted change.
2. Run the published (pre-push) scorecard against the changed tree and confirm it FAILS on the
   specific anchor. If it does not fail, the pair was never coupled and you invented a dependency.
   This is the negative control for the coupling itself, and it earns the rest.
3. Engine PR merges FIRST. Never push the vault ahead of it.
4. Gate the vault push on `git log --oneline origin/main..main` containing EXACTLY your commit.
5. Re-verify against both published trees.

| Item | Rule |
| --- | --- |
| Encode a gate as the CONDITION | Never as output you read: `count==1 AND head==<sha> AND tree clean`. |
| Why | A stranger's commit at HEAD then skips the push instead of relying on you reading correctly. |
| Both halves need an owner present | Between merge and push the two repos disagree with nothing detecting it. |
| So | Arm a waiter that fires on ANY terminal state, and hand the next session a narrowly-scoped fallback authorisation that expires on completion. |

### 4h-bis. The vault and the engine are separate repositories with separate queues

| Item | Rule |
| --- | --- |
| The independence is structural | Read both clones with `git remote -v`. The engine clone carries `origin` plus a second, personal remote, and the vault clone's `origin` is that personal account. |
| What follows | Two repositories, two PR queues, two branch protection configurations. Nothing a merge in one does can BEHIND a PR in the other. |
| Where to work during a freeze | When the engine queue is stalled or deliberately frozen, land on the vault. It advances nothing on the engine side and blocks nothing there. |
| Read each repo's protection live | Never from a count written down. The two configurations differ, and the read-fresh rule covers the vault too. |
| Before hand-landing into a mirrored path | The vault carries a tracked copy of `messagefoundry/` kept current by an automated job. |
| The related hazard | A non-stdlib import in a mirrored tool STRANDS that mirror rather than redding a gate. |
| This is a stated PRECONDITION, not a measured finding | Whether a hand-landed engine-shaped change fights the job has not been answered here. |
| So | Read the mirror job's trigger and its path binding before you land one, and say which you read. |
| **EXPIRY** | The auto-mirror is retired, or the vault stops tracking a `messagefoundry/` copy. |
