# Running multiple sessions

<a id="tldrbluf"></a>

Choose the client, communication channels, and merge owner before running parallel sessions. A
lander is the session that handles merges; no script implements the role.

Parallel sessions can fail without visible warnings. Prepare before starting the second session;
several controls reach only sessions started after installation.

[Concepts](CONCEPTS.md) explains the shared model. Use the four preparations below when moving beyond one
session at a time.

---

The setup follows three rules from [Concepts](CONCEPTS.md):

- A worktree per session -- one directory and one branch each.
- One shared state root that every worktree of a clone resolves identically.
- A liveness fence that may only veto -- it can refuse an action, never authorize one.

Complete these four preparations before starting another session. Install the gates and steering
hook first; they affect only sessions started afterwards.

1. Pick the surface, deliberately -- see [below](#which-surface-to-run-several-sessions-on).
2. Give each session its own worktree, cut from a freshly fetched remote tip ([Worktrees](WORKTREES.md)).
3. Install the gates into every config root the client uses, then verify with the three commands in
   the surface section ([INSTALL.md](INSTALL.md), [Hooks](HOOKS.md)).
4. Wire the steering hook now if you will ever want it. It only takes effect in sessions started
   after it was wired ([Steering](STEERING.md)).

---

## The problems, and which page owns each

These problems roughly follow the order in which they arise. Each linked page provides the fix.

| The problem | What it looks like | Owned by |
|---|---|---|
| Two sessions share one working tree | Both edit the same files, and each believes it owns the directory. | [Worktrees](WORKTREES.md) -- one worktree per session, cut from a freshly fetched remote tip |
| A session runs a checkout inside another session's checkout | Every file under the other session swaps to a different commit's content, mid-task, with nothing on either screen saying so. | [Worktrees](WORKTREES.md) for the repair path and the rule; [Hooks](HOOKS.md) for the refusal that stops the tree-swapping verb in the first place |
| The shared primary checkout drifts onto someone else's branch | A peer put it there, or the harness's own auto-worktree half-failed and left a ghost stub. | [Worktrees](WORKTREES.md) -- `restore-primary.ps1`, and the SessionStart backstop whose dirty-tree refusal is its only safety property |
| Your tests pass against code you are not editing | A shared editable install binds every worktree to whichever checkout was installed last. | [Worktrees](WORKTREES.md) -- one dependency environment per worktree, built inside it from the lockfile |
| Two sessions edit the same file in parallel | Found at merge, after both built on divergent assumptions. | [Coordination](COORDINATION.md) -- overlap for the pull direction, the collision gate for the refusal |
| Two sessions build the **same thing** in **different files** | Zero conflicts, two green pull requests, one thrown away. This is the residual no gate can compute: announce and claims are both best-effort. | [Coordination](COORDINATION.md) |
| Two sessions reach for the same next number in a shared sequence | Two records numbered `0004`. Git merges both cleanly and nothing in the graph can see it. | [Sequence allocation](SEQUENCE-ALLOC.md) -- atomic allocation plus a commit-time gate; neither half suffices alone, and no installer wires the commit-time half |
| A session is a long way into the wrong approach | Typing at its prompt only queues your message for after the turn. | [Steering](STEERING.md) -- a note delivered at the target session's next tool call |
| A peer cannot be reached at all | An editor-extension session, or one under a different login, is invisible to the realtime channel. | [Session mail](SESSION-MAIL.md) -- **ships**: a sender, a drain, and one shared key function |
| Two sessions write the same last-write-wins state outside git | Project memory, a shared note, a ledger. One write vanishes with no error anywhere. | **No shipped mechanism.** Named in [Worktrees](WORKTREES.md) and [Concepts](CONCEPTS.md) as something a worktree does not isolate; the remedy is single-writer convention. An accepted residual -- see [lander](#using-a-lander-session). |
| Several branches all have to land in one trunk | "Can't merge" is four different states with three different fixes. | [PRs and merges](PR-AND-MERGE.md) -- read the state before touching the branch; it also owns what squash-merge does to reachability |
| Cleanup deletes a worktree a session is still working in | Or it half-fails, stranding commits in no ref and no reflog. | [Pruning](PRUNING.md) -- merged AND clean AND NOT occupied, two occupancy signals either of which may veto, and an orphan ledger |
| Everything is green and you cannot tell whether any of it is running | Every failure mode here is byte-identical to success. | [Hooks](HOOKS.md) for the event map and each control's posture; the instrument is `bin/ccx-doctor.ps1`; [the drift audit](CASE-STUDY-drift-audit.md) for the method |

---

## Which surface to run several sessions on

KORUS requires Claude Code for Desktop. CLI-only and editor-extension setups are unsupported.

The coordination layer depends on the desktop client ([Limits and requirements](LIMITS.md), [Install](INSTALL.md)). Success
on another client does not change that requirement.

Announce uses a desktop-only MCP server and the desktop app's session roster. These dependencies
establish the client requirement independently of measurements.

> **Separately, one operator's observation, dated 2026-08-06. Not a benchmark.** Running several
> sessions at once in the **VS Code extension** has run into worktree hijacking: one session checking
> its own branch out inside another session's directory. Nothing here measures a hijack rate per
> surface, so that part is an anecdote. It is a reason the requirement is not a hardship, not the
> reason for it.

The following mechanisms have different evidence: upstream reports, local measurements, or one
observation.

- *Cited upstream, not reproduced here.* The hijack is harness-side, and nothing here ties it to a
  surface. A per-session auto-worktree can half-fail on Windows, flipping the *primary's* HEAD onto
  the session's branch ([claude-code#76590](https://github.com/anthropics/claude-code/issues/76590)).

This repository cites that issue rather than reproducing it, and records no observation of the
extension's worktree layout either way. The bullet removes an easy assumption. It does not establish
that the defect is surface-neutral.
- *Measured here.* An extension session is absent from the desktop app's own `list_sessions`. It
  enumerates only sessions that app spawned; an extension session is never registered, not filtered
  out. Verified on a live extension session sharing the **default** config root: not a login split.
- *Measured here.* Project-scoped settings are commonly git-ignored and cannot reach a new worktree.
  A large share of this repo's worktrees had no project settings file, and a live editor session was
  working in one with **zero** coordination context. So the hooks here install at **user** scope.
- *Observed once.* **User scope means *per config root*, and the gate fails open.** An unwired root
  refuses nothing and says nothing, so from inside the session it is byte-identical to a governed
  one.

This is the only bullet tied to an observed hijack. A session under an ungoverned config root
checked out its branch inside a peer's linked worktree. The gate that could refuse it was absent.

Installers cite editor-hosted chats on extra config roots as the reason to wire every root
([INSTALL.md](INSTALL.md)). The observed hijack used that setup. Nothing here counts roots by surface:
rationale, not a measured distribution.

An extension session's absence from `list_sessions` does not make it invisible to every control.

The worktree gate uses the write target and git's report of the affected tree. It reads no session
list ([Hooks](HOOKS.md)).

The reaper and presence roster read the on-disk registry for every surface. Extension sessions
remain visible to worktree cleanup ([Pruning](PRUNING.md)); `list_sessions` limits messaging.

The observed hijack used an editor-hosted session under an ungoverned config root. No measurement
here separates the client from the missing wiring as the cause.

Project-scoped hooks were measured running in the extension ([Session mail](SESSION-MAIL.md)). Installers write
user-scoped hooks; whether those fire there remains unmeasured.

Test whether controls actually run on the client you use.

Start a session through your intended client, then run:

```powershell
pwsh -NoProfile -File scripts/coord/presence.ps1                 # does the roster carry this session?
pwsh -NoProfile -File bin/ccx-doctor.ps1                         # are the gates live for THIS repo, by attack?
pwsh -NoProfile -File scripts/worktree/install-gate.ps1 -Status  # wired, and current, in EVERY config root?
```

Current wiring in every config root covers the known installation gap. It still does not prove the
gate fires on that client:

- `-Status` answers "is it wired", not "does it fire".
- `ccx-doctor.ps1` attacks each control rather than reading config, so trust it over the wiring
  report.

The client choice does not replace the gate. A refused hijack produces a message; an unwired gate
lets it proceed silently.

---

## How sessions talk to each other

Most signals wait for someone to read them. One channel pushes between sessions; three more arrive
without the recipient looking, including two delivered by the harness.

Some channels reach only future sessions. Choose by timing so a message arrives before the relevant
decision; the table groups channels into five bands:

- **A** -- already running, mid-turn.
- **B** -- a running peer, if it is in the desktop roster.
- **C** -- anyone who looks, whenever they look, including sessions that start later.
- **D** -- at commit: after the work, before it lands.
- **E** -- only a session that starts later; never a running one.

The table lists available channels and links to their documentation.

| Channel | Reaches whom, and when | Push or pull | Shipped here |
|---|---|---|---|
| [Cross-session messaging](https://code.claude.com/docs/en/cross-session-messaging) | **A** -- a **busy** peer between tool calls; an idle one at a new turn. Not another login: nothing can name it. | addressed by name, never by path | yes, built into the harness; nothing to install |
| [Steering note](STEERING.md) | **A** -- a **busy** session, at its next tool call. The only one here a non-Claude process can send. | addressed to one worktree | yes, opt-in per worktree; nothing wires it |
| [Collision gate](COORDINATION.md) | **A** -- a **busy** session, at the tool call: while the outcome can still change. | addressed to whoever attempts the edit; delivered by the harness, not a peer | yes |
| [Kill-switch files](COORDINATION.md) | **A** -- sessions already running, because the hook re-reads the file on every run. | broadcast, one bit | yes |
| [Announce](COORDINATION.md) | **B** -- a peer already running **and** in the desktop session list. Not an extension session, not another login. | addressed; one note per peer, same content to each | yes; delivery needs a desktop-only server |
| [Claims](COORDINATION.md) | **C** -- anyone who looks; also surfaced to joining sessions in preference to the worktree name. | broadcast to a place, not sent to anyone | yes |
| [Overlap](COORDINATION.md) | **C** -- you, about live peers, at the moment you ask. | pull; nobody sends | yes |
| [Presence and occupancy](COORDINATION.md) | **C** -- you, about who is live and where, right now. | pull | yes |
| [Locks](COORDINATION.md) | **C** -- whichever session attempts the same operation, as it attempts it. | broadcast; the file's existence is the signal | yes (a library -- dot-source it) |
| [Sequence allocation](SEQUENCE-ALLOC.md) | **C** -- every session, present and future, when it asks for a number. | broadcast to a shared registry | the allocator, yes; **no installer writes the `pre-commit` gate** -- until you wire it, nothing at commit time catches a reused number |
| [Commit-time claim gate](COORDINATION.md) | **D** -- the committing session, at commit; it reaches one that never asked for anything. | addressed to the committing session | yes, installed per clone into the shared git hooks directory, so one copy governs every worktree; `--no-verify` bypasses it |
| [SessionStart context](HOOKS.md) | **E** -- only a session that starts later. | broadcast | yes |
| The working agreement ([`CLAUDE.md`](https://claude-multisession.pages.dev/CLAUDE.md.template)) | **E** -- only sessions that start later; an edit misses a running one. | broadcast | template only; nothing installs it |
| [Session mail](SESSION-MAIL.md) | **E** -- a session that starts later; a mid-turn wake-up is possible and is one-shot. | addressed to a worktree box, keyed by normalized path | **yes** -- `scripts/coord/mail.ps1` sends, `scripts/hooks/mail-drain.ps1` delivers |

Every band A channel shipped here uses a file reread on each hook run. Environment variables and
settings changes reach only later sessions.

The built-in cross-session channel is an exception. Claude Code reads arriving messages between tool
calls, with no hook or file required.

Announce is band B: its desktop-only MCP server reaches peers in the desktop session list.

A delivered message can stall a recipient's query without output. The watchdog force-ends it about
16 minutes later, showing only an `Error` badge.

Upstream: [claude-code#86012](https://github.com/anthropics/claude-code/issues/86012), observed on the machine this page was written on. Each channel's page
carries its costs.

### Choosing one

- Change a running peer's course **now** -> steering note, if it is wired in that worktree.
- Tell a running peer what you are **about to do** -> announce.
- The recipient does not exist yet -> a claim, an allocated number, or the SessionStart context.
- You want the answer **yourself** -> presence, overlap, `claim.ps1 -List`. Nothing pushes.
- You want a rule **enforced** rather than communicated -> a gate. Anything else is a request. So if
  what you want to say is "do not touch X", publish something a gate consumes rather than something
  a human reads.

Pull queries read git and a roster keyed by launch directory. They miss an absolute-path write from
elsewhere, so cleanup needs another signal ([Pruning](PRUNING.md)).

Peer messages are data and authorize no push, merge, delete, or config change. Broadcasts need an
expiry or recipient-checkable condition; one freeze kept announcing hours after its PR merged.

### The degenerate channels

Fallback channels have weak delivery and cannot replace the intended controls.

Relaying through the operator takes unbounded time and one conversation per session. It also makes
peer assertions sound like user instructions.

A shared note has no delivery receipt, and no tool acts on it. Two sessions agreed to hand over a
file, but the gate still refused because it reads git; branch switches can also move the note.

Git names and conflicts arrive too late to coordinate work. A conflict reports completed overlap;
worktree names can be stale, and squash-merge breaks reachability as a merge-status signal.

Humans can interpret these fallbacks, but tools cannot act on them. Each arrives after the decision.

---

## Using a lander session

Give the lander responsibility for tracking work and choosing merge order while other sessions
build.

The lander exists through a prompt and rule, without a script, role flag, or routing mechanism. It
takes responsibility delegated by the human owner; sessions keep control of commits.

[Run a KORUS build](KORUS-BUILD.md) step 3 supplies the prompt and daily procedure. The rules below define its
authority.

The lander arbitrates; it does not execute.

### Why the role exists

- Almost every signal here is pull, and pull needs somebody to look. Under load, the sessions doing
  the building are the least likely to stop and look.
- Outward-facing actions want a single owner, and with auto-merge armed a pull request *is* a merge.
  Measured: the trunk moved **seven times** during one pair of pull requests. Two branches that each
  merge cleanly against the trunk they were cut from need not merge cleanly in either order.
- Some shared state is last-write-wins and outside git: project memory, shared notes, a ledger. The
  rule there is single-writer, and single-writer needs a writer.

### What routes through it, and what does not

The last two table rows state the general rule; earlier rows give specific cases.

| Routes through the lander | Does **not** route through it |
|---|---|
| Merging, and arming or disarming auto-merge | **Pushing its own branch, and opening its own pull request.** Owner ruling 2026-08-29: sessions push their own |
| The **order** decision: which of two branches on the same ground lands first, and who re-syncs after | **Committing** -- the worker's own judgment, at logical stops, one layer each. A lander asked before a commit is a queue. |
| Which of two overlapping **efforts** continues, and which stops | Editing, running tests, iterating on its own branch |
| Writes to any shared last-write-wins state outside git | Creating its own worktree -- already serialized by a mutex |
| Anything whose answer must be identical for every session and no gate can compute | **Allocating a sequence number**, **taking a claim**, taking a lock, any read-only query |

Exclusive file creation already serializes allocation; a lander handing out numbers would risk lost
updates. Claims belong to worktrees, so a lander's claim can block the worker's commit.

Keep machine-serialized operations with their tools. Single-owner judgment belongs with a session;
routing both through it creates a queue.

### The route is absolute, and the authority is not transferable

Until 2026-08-29, the rule sent pushes, pull requests, and merges through the lander. The owner then
returned pushes and pull requests to workers, retaining only merges.

A running lander must handle merges. Sessions may adopt that routing on sight; pushes and pull
requests have stayed with workers since 2026-08-29.

Only the human owner grants authority, in words, to one session. A successor inherits the route but
cannot inherit that grant from the previous lander.

Without a running lander, merges go to the owner. An unreachable lander blocks a worker's merge
authority but never its own push or pull request.

An override must name the route it overrides. "Yes", "go ahead", or "use your best judgment"
requires clarification about which route was meant.

### How a worker talks to it

Take a claim with a note before starting. Announce carries it to joining sessions, and the lander
reads the recorded state.

Refresh the claim note when ready to land. A push is routine worker activity, so it proves no
readiness; before 2026-08-29, it meant the lander had already acted.

### When you do not need one

Use a lander when merge order matters or efforts overlap. Three sessions on unrelated subsystems may
need none; two rewriting the same index do.

### How the role fails

- **Bottleneck.** If a worker must ask before it can commit, you have built a queue. An explicit
  claim tool sat here and was used exactly **zero** times: a coordination step you must remember is
  one you will skip. A lander that says wait when it needn't destroys the channel it depends on.
- A worker bypasses it -- assume it will. Claims are advisory and the push guard is a guardrail, not
  a boundary. So the role sits **behind** enforcing gates rather than instead of them: a lander that
  is the only control is not a control.
- Stale state, in two symmetric directions. A broadcast that never lapses: a freeze note still
  announced itself long after its pull request merged. Its mirror: a claim was reported stale while
  its holder was committing minutes earlier. Report what the holder is doing, not how old the record
  is.
- Phrasing a ruling as restraint. "Do not merge" does not reach armed auto-merge; nobody has to
  click anything for those to land. "Disarm auto-merge on your pull request" does.
- **Authority confusion.** A lander's message is still peer data. Being central is not being
  authorized.
- State that lives only in one context. Whatever it decides must end up in a claim, a number, a
  branch or a gate; a cleared context takes the rest with it.
- It inherits the timing table, but a busy session is now reachable. Cross-session messaging reaches
  a busy peer between tool calls, and not through the note. [Steering](STEERING.md#the-trust-boundary) forbids that use: "Do
  not route machine-to-machine traffic through it."

Its premise is "this came from the user". A lander writing one puts words in the operator's mouth,
which is the bullet above.

Earlier guidance made the lander wait for the turn to end. The supported cross-session channel now
reaches a named busy peer; `steer.txt` remains forbidden for peer traffic.

---

## Related

| For | Read |
|---|---|
| The model everything here applies | [Concepts](CONCEPTS.md) |
| Creating, rescuing, restoring and removing checkouts | [Worktrees](WORKTREES.md) |
| Presence, overlap, claims, locks and announce | [Coordination](COORDINATION.md) |
| Reaching a session that is already mid-task | [Steering](STEERING.md) |
| Reaching a peer the realtime channel cannot see | [Session mail](SESSION-MAIL.md) |
| The collision class git cannot see | [Sequence allocation](SEQUENCE-ALLOC.md) |
| Landing several branches in one trunk | [PRs and merges](PR-AND-MERGE.md) |
| Removing worktrees without destroying a session | [Pruning](PRUNING.md) |
| Every control mapped to its event and its failure posture | [Hooks](HOOKS.md) |
| The things that bite, in the order they bite | [Tips and tricks](TIPS-AND-TRICKS.md) |
| Proving the controls are actually running | [Drift audit case study](CASE-STUDY-drift-audit.md) |

The [handoff diagram](KORUS-BUILD.md#g04) connects roles, while the [mail timeline](SESSION-MAIL.md#g09) explains delivery events.
