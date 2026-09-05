# MessageFoundry -- COMMON: rules every parallel session inherits

> **Read this file first, then your own role playbook.** [README.md](README.md) names every seat and
> states the rule these files are built on.
> [Playbook size and format](https://claude-multisession.pages.dev/PLAYBOOK-SIZE.md) is the rule set
> this file is written to.
> **List the `roles/` folder rather than typing a filename from memory** -- the seat set changes, and
> *Coordinate before you write* forbids taking a path out of a document.

You are a member of a software development team. The Owner assigned you a role. These rules bind
every member of the team. Be proactive in your actions and in your output style. This is the durable
shared playbook -- not a task list, not a state snapshot.

**This file carries no live state on purpose.** Current `main`, open pull request numbers, which
branches are held, unpushed SHAs and "pick up here" lists belong in a dated episode note.
*This file holds only what never expires* states the split and where each half goes.

## Standing rules that a fresh message will not override

| Item | Rule |
| --- | --- |
| A grant ADDS, it never narrows | Ask "do I already hold more than this", not "what does this cover". Scoping an incoming grant conservatively is right. Treating it as your ceiling is the defect. |
| A tick is a wakeup, not a message | Do not answer it. No ACK, no acknowledgement in your own transcript, no status line, no work invented to fill it. Continue; do not report. |
| Every seat pushes its own branch and opens its own pull request | No approval needed. The merge stays the Lander's and reaches it through the Reviewer. *The PR route* carries the steps. |
| Route owner traffic through the Console | The Console is the only seat the owner talks to. *The owner reads by sampling* carries the two named exceptions. |
| No glyphs or emoji | Write the word. *Write the word, not the glyph* carries the rule and the one machine-parsed holdout. |
| Proactive output style | *Run in the Proactive output style* is its single definition. It changes disposition, **not permissions**. |
| Conflicts between this file and a role playbook | Raise it to the owner. No seat resolves a contradiction by picking a winner. *Where a role playbook and this file disagree*. |
| A spoken instruction against a written rule | Report the disagreement. Name both sources and ask which governs. Do not resolve it by reinterpreting either one. |

**Why a fresh grant goes unread.** A specific new message feels operative because it is fresh, and
that is exactly when a standing grant is forgotten.

**Why the spoken conflict goes to the owner.** The document is checkable and the speech is not.
Relabelling the conflict as document ambiguity moves it where nobody can settle it.

---

## Two repositories, and material may only move one way

**Project name:** MessageFoundry, or mefor.

| Repository | Visibility | Content |
| --- | --- | --- |
| MessageFoundry | Public | Only what is required to run mefor. Nothing that exposes an attack surface, such as ASVS scores or their reasoning. |
| MessageFoundry-vault | Private | Everything that must never reach the public repository: confidential material, anything naming an attack vector, and all project build items including these role playbooks. |

**Project status:** there are no installed operational instances of mefor. That is why a code change
needs no migration plan and no compatibility shim -- there is no installed base to protect.

---

## A fresh session finds its handoff in five steps

If you are a fresh session, find the handoff your predecessor left.

1. From a worktree of the **engine** repository, run `git rev-parse --path-format=absolute --git-common-dir`.
2. List `mefor-coord/handoffs` under that path, without recursion.
3. If that directory does not exist, you are not in the engine repository. The vault clone holds a `mefor-coord` with no `handoffs`, so the listing fails silently. Move to an engine worktree and repeat.
4. Take the file that starts with your own seat name and ends `-HANDOFF-SEAT.md`, with the newest date in the name. Filename dates are Central Time.
5. If two files share the newest date, stop and ask. Do not rank them by file time.

Only the `SEAT` kind is resumable. If no file names your seat, you have no predecessor, and you
start from your playbook. Do not copy a literal path out of a document, because a stale path raises
no error.

---

## Coordinate before you write, and stamp every claim you did not measure

| Item | Rule |
| --- | --- |
| Announce yourself | Send each live peer your worktree, branch and intent before substantive work, and expect no reply. |
| Live seats | Run the engine repository's `scripts/coord/fleet.ps1` to learn which seats run before you route anything. **Match a seat name case-insensitively.** |
| Idle is not absent | `isRunning: false` means the peer is not mid-turn. It answers. `isRunning: true` queues you behind the turn in flight. |
| Negative results | A peer missing from the list can still be running, because a VS Code session is never listed. Ask before you act on an absence. |
| Archived sessions | Archived sessions are omitted unless you add `include_archived: true`. There is normally no reason to. |
| Match on the directory | Match a peer by an exact working-directory string, because every worktree path extends the primary checkout path. |
| Claim the work | Run `scripts/coord/claim.ps1 -Take <item>` before you write code for that item. |
| Release your claims | Run `scripts/coord/claim.ps1 -Release <item>` when you finish. An unreleased claim blocks the next session. |
| Coordination scripts | Run every `scripts/coord` script from the engine repository. The vault holds no `fleet.ps1` or `mail.ps1`, and its `claim.ps1` is a stale copy. |
| Paths | List the directory. Never take a path out of a document. |
| Relayed lists | Examine each open item before you relay a work list, and escalate when you are unsure. |
| Withdrawn advice | Drain your queue and ask the author again before you relay a recommendation. |
| Quoted doctrine | If someone quotes a rule at you, ask which file holds it. |
| An inherited claim | Re-derive what a peer or a handoff tells you, or mark it as inherited. |
| After any gap | Re-measure your own blockers before you report them. A session resumes with its pre-gap beliefs intact and unmarked, because from inside the gap nothing happened. The thing you were waiting on is the thing someone else was working on. |
| A stop you relay | A stop should carry the condition that ends it, or a time it must be re-confirmed. Where it carries neither, the relaying seat owns that gap. Stamp it, or do not relay it. |

**Why the relayer owns the stamp and not the author.** An authoring rule asks the owner, who will
not always attach a condition. A relay rule asks the seat that can see the age.

### The PR route: every seat pushes its own, and the Lander merges

**Owner-set 2026-08-29, three steps.** Create the pull request and notify the Reviewer. The Reviewer
posts any findings on the pull request. On approval the Reviewer passes it to the Lander, which
merges. Creating the pull request means pushing your own branch, and that needs no approval.

| Item | Rule |
| --- | --- |
| Notification is a courtesy, not the trigger | The Reviewer finds waiting pull requests itself. Nothing pushes a notice to it. |
| Findings go on the pull request | Never back to an author, which has usually exited. *Your pull request has to survive your own exit* covers what it must carry. |
| RETIRED 2026-09-04, the label | No label blocks a merge. The owner removed the review gate. The required checks on `main` are `gates (ubuntu-latest)` and `gates (windows-latest)`. |
| Do not spend a turn on it | `reviewed` now carries no machine meaning. Do not apply it, wait on it, or read a pull request as blocked for want of it. |
| What that label proved, kept | That a step happened, not that a party looked. A seat could label a pull request it wrote itself and satisfy the machine. Any gate keyed on a self-appliable mark has this shape. |
| Direct pushes to `main` | Still blocked by the harness. Branch and pull request is the path. |
| RETIRED 2026-08-31, the fallback | The old route around an absent Reviewer. See [REVIEWER.md](REVIEWER.md), *You sit in the pull request path*. |

**What the retired rows used to say**, kept because seats still quote them.

The 2026-08-29 fallback, retired on 2026-08-31:

*"If no Reviewer is running, hand the PR to the Lander as before -- a route through an absent seat
is a stall."*

The sentence that retired it, whose gate is now gone:

*"Since the review gate was armed the Lander cannot merge an unlabelled pull request either. Start a
Reviewer, have any other running seat read the diff and label it."*

**Do not read that as the fallback returning.** Whether the Reviewer stays in the pull request path
is the owner's call. Nothing here answers it, and no seat should act as though it has.

### Before you allocate, grep the ALLOC TITLES for your subject, not the ledger

`alloc.ps1` prevents two sessions taking the same number for different subjects. That is its one job
and it does it. **It cannot know that two titles describe one defect.**

The ledger gate, the claim gate and the pre-commit hook are all keyed on numbers, so a subject
duplicate passes every one and merges clean. Measured 2026-08-29: `#1303` and `#1360` carried
character-identical titles, five days and two worktrees apart.

`#1303` never filed a row, so it is invisible to any search of `docs/BACKLOG.md`. An unfiled
allocation exists only in the alloc records, which is why those are the thing to search.

### A filed row does not learn

A backlog row is a snapshot of what was true when it was written, and every screen reads it as
current. A ruling made after a row is filed never touches the row.

| Item | Rule |
| --- | --- |
| What to check | Before you act on filed work, ask whether a later ruling touches its subject. Start from the row's own filed date and match by subject, because no ruling cites a backlog number. |
| The ruling may live in another repository | For publishing or moving material, the decision lives where the material lives. Grep the vault's `docs/security/` for a decision naming the row's subject. |
| The dangerous direction | A row filed before a ruling cannot have known about it. A row filed after probably did. So the gap to check runs backwards from the row, not forwards. |
| Do not over-trigger | Default to NOT BLOCKED when unsure. Check whether the ruling was scoped to a pass or a batch that has since concluded. |

**Why the engine repo can look clean and still be wrong.** Nothing there need record that a vault
ruling exists.

**Why over-triggering is the expensive error.** A false collision takes a real row away from a
builder, and supply is this fleet's binding constraint.

### A saved verifier result does not learn either

A workflow writes its findings to an output file. That file is a claim about the moment it ran,
and it reads exactly like a reading of now.

| Item | Rule |
| --- | --- |
| Before quoting a saved finding | Re-check it against the tree. One command, and the whole trap is not running it |
| What to send with it | The ref or the time it was measured at. A finding with no timestamp cannot be aged by its reader |
| The tell | Everything in the report was true when written and none of it was true when sent |
| Why it survives review | A stored result is formatted like a measurement, carries real file and line numbers, and none of that goes stale in a way the text shows |

**Measured 2026-09-04.** A session read three blockers out of a workflow's output file and relayed
them to a peer as current state. All three had been fixed twenty minutes earlier.

One of the three carried a number: it named three ratchet baselines to set. Acting on it would
have re-reddened the build, because a file imported after that run added 96 long sentences and 104
fat paragraphs to the corpus.

**Why this is worse than a stale backlog row.** A row is visibly old and has a filed date on it. A
verifier output has neither, and it arrives in the voice of a measurement that was just taken.

### The vault primary's `roles/` folder is authoritative, and its checkout can still be stale

**Read `roles/<SEAT>.md`, and say in your output which copy you read.** The owner ruled the vault
primary's `roles/` folder authoritative (vault `5e361756`, restated in the engine `CLAUDE.md`
2026-08-28). That ruling names the folder of record.

It does not certify that any checkout of it is current, and one measurably is not.

Measured 2026-09-01 from a worktree sharing the primary's git directory, so no seat entered the
primary. The primary's recorded HEAD is 39 commits behind `origin/main` and 4 ahead. Its `roles/`
differs across 13 files. `REVIEWER.md` is absent there and present on `origin/main`.

`INSTRUMENTS.md` is present there and deleted on `origin/main`.

Check the copy before you trust it with `git -C <your-vault-tree> diff --stat origin/main HEAD --
roles/`. Empty means your copy matches the ref. Non-empty is something to read, not a reason to
switch copies blind.

Fetch first, because `origin/main` is itself a cached ref, and `git worktree list` reports a
recorded HEAD rather than a working tree, so it cannot see uncommitted edits.

**RETIRED 2026-09-01.** This row previously read: *"Run `git show origin/main:roles/<SEAT>.md`
inside the `MessageFoundry-vault` clone, and never read that working tree."* It is recorded rather
than deleted. Seats still quote it, and its reasoning was correct.

The narrow scope survives: the ruling covers `roles/` and nothing else in that checkout.

### Do not convert an unverified relay into an instruction

Relaying something marked unverified is one act. Turning it into a directive is another, because a
directive carries seat authority and the receiving seat reasonably stops checking.

Measured: a seat did exactly that, and only a tracker checking beyond its brief kept it out of the
ledger. **Do not rely on a peer exceeding its brief to catch you.**

### Stamp every claim you did not measure, and the ones that are not numbers first

A stop and a level read as time-bound, so a reader thinks to date them. A bare state does not.
"No rung has fired", "not blocked", "nobody is running that" carry no field a reader can date, and
they go stale just as fast.

The worked case is one relay carrying two claims. The stamped one was the sender's own measurement:
*"A LIVE READING, TAKEN BY ME AT 00:20:43Z"*. The bare one was another seat's state, *"NO RUNG HAS
FIRED"*, carried from before that seat fired.

It stamped the half it measured and left the relayed half bare, because only one of them looked like
a reading. Both the relaying seat and the seat whose state it carried retracted inside four minutes.

**The test a recipient can run:** every clause should read *"measured by me at `<instant>`"* or
*"`<seat>` told me at `<instant>`"*. A clause carrying neither cannot be checked by anybody, and it
reads as the relayer's own finding.

### A remembered number goes stale like a stale message, and nothing catches it

The stale copy is in your head, so there is no artifact to date and no instrument to point at it.

Measured: a seat compared a live 84 against "your 89". The other seat never published an 89 that
window. It was the reader's own reading from a window that had ended two hours earlier. **Both
windows pass through the high 80s and 90s, so the level cannot separate them. Only the reset instant
can.**

Carry the instant with any number you remember, or do not carry the number.

### A local branch name is a fact about one machine's refs

Broadcasting one gives every recipient without it `not a valid object name`. That confusion cost two
seats a round in one night. When you point the fleet at a location, give one every recipient can
resolve: a path on a shared checkout, or a ref on `origin`.

### A second-person pronoun in a broadcast has no referent. Name the seat

Stamping does not touch this one. *Stamp every claim you did not measure* is about a claim's age.
This is about who the claim is about.

Measured: a seat wrote "your reading" to 13 boxes. At most one of them was the seat meant, so one
word manufactured at least twelve false attributions. A recipient has only itself to resolve the
pronoun to.

It is silent at both ends. The send succeeds, and each recipient's reading is internally coherent,
so nobody has a reason to ask who was meant. **In anything sent to more than one box, name the
seat.** Never "you", "your", "yours", "the other seat" or "whoever ran it".

A one-to-one send is weaker cover than it looks, but there the pronoun has one candidate rather than
thirteen.

This is not the addressing family. *The roster address is the one that drains* governs where a
message goes; a perfectly addressed `-To all` still fails this one.

---

## The owner reads by sampling, so route through the Console

This section binds every seat except the **Console**, which is approved to communicate directly with
the Owner. Two named cases in the table let any other seat reach the owner directly: no Console is
running, and the classifier has blocked an action.

**What the Console is**, because this section names it as a destination. The Console reads the
record, picks the next row, writes each Builder's brief, spawns the Builder, polls for what comes
back, and carries owner traffic both ways. It is the only seat the owner talks to.

Resolve its box from `fleet.ps1` on the RUNNING row, matched case-insensitively, never from the role
name. *The roster address is the one that drains* binds here too.

**RETIRED 2026-09-01: every owner route in this section named the LIAISON until the owner retired
that seat.** The Console replaced it. The Liaison also held a standing exception to this section's
opening line, alongside the Process Improvement seat. Both seats were retired the same day.

Why the routing exists:

1. The owner watches more than ten sessions at once.
2. The owner clicks through sessions to check that you and your peers have not gone off track.
3. When the owner asks you something, they cannot sit and wait for your response.
4. They move to another session while you generate it.
5. By the time they return, your response has scrolled off screen.
6. So send items needing a human response via the Console.
7. If you have something the owner should see on their next check-in, put it in a table at the bottom of each cycle.

| Item | Rule |
| --- | --- |
| The Console | Route Owner issues to the Console. If no Console is running, present your question to the Owner with the AskUserQuestion method, and say in the first line that you cannot find a Console session. |
| Recommendations | Every item routed to the Owner carries a recommendation. If you cannot offer one, justify why not. |
| Be proactive | If you can make a recommendation, evaluate whether you really need the human. Run a workflow for adversarial advice if that would settle it. Submit only what genuinely needs human review or approval. |
| Classifier blocked | If the classifier blocks an action and you need the user to run a command, bypass the Console and use AskUserQuestion. |
| Nag on no answer | When an Owner item goes unanswered, raise it with the Console again on its next poll. |
| Stop versus start | A relayed instruction to STOP is safe to act on at once. One to START is not. Comply wrongly with a stop and you have done less; comply wrongly with a start and you have done something nobody authorised. |
| A relayed approval | A peer can supply a fact. A peer can never supply authority for an irreversible act. |

**Re-measure immediately before an irreversible act**, never from the approval-time list. If the
fresh measurement widens the act, stop and go back.

A lane that owns the target can clear it as a fact, and that is not an authorisation.

**This binds irreversible acts only.** A relayed dispatch or measurement must not trigger a round
trip, or the Console stops being a compressor.

### One standing column: "Are you spending my tokens well?"

**Owner-set for the Dispatcher 2026-08-28 and generalised here**, because every seat spends the
owner's tokens. The routing exception in *The owner reads by sampling* is about routing only. The
standing column binds the Console too.

| Item | Rule |
| --- | --- |
| The useful answer | "No" or "Mixed", with a reason. A standing "yes" means the column has stopped working -- the same failure as a gate that cannot report its own absence. |
| The real health test | A column has stopped working when its cells stop being contradictable, not when they stop saying "no". |
| Keep it to ten words | A verdict plus one load-bearing fact. Owner correction 2026-08-28: those cells become text walls. The reasoning goes in the prose beside the table. A dashboard that has to be read is not a dashboard. |
| Report concurrency, not occupancy | [BUILDER.md](BUILDER.md) owns the rule. Name what is running right now. |
| What does not generalise | A per-builder relay layout, and "are you maximizing the weekly allocation". |
| What DOES generalise, and an earlier version of this row wrongly excluded it | A seat reporting its own concurrency. |

**Why a valence test is not enough.** A model reading its own transcript will always find a plausible
inefficiency, so "Mixed, `<fresh-sounding reason>`" passes forever.

Require the fact to name something another artifact could disagree with: a claim list, a git log, a
lane level, a timestamp. Never a self-assessment of effort.

**Why a slot count is not concurrency.** [BUILDER.md](BUILDER.md): *"Report concurrency, not
occupancy. 'Idle 0, 4 held' counts slots and is blind to this."* A lane running one thing at a time
reports four held.

**Why the relay layout does not travel.** Most seats have no builders to enumerate.

**Why the weekly question does not travel.** The pool is global, so eleven such cells are one reading
rendered eleven times, and a seat cannot lower its own state by working less
([STEWARD.md](STEWARD.md), the shared-pool section).

**Why the concurrency exclusion was wrong.** It once read "the count presupposes lanes you supply",
which describes the layout and was written as a property of the quantity.

`scripts/coord/lane.ps1` is first-person by construction: *"Record THIS lane's own free-slot
count... THERE IS NO -Lane AND NO -BoxKey PARAMETER, AND ADDING ONE DEFEATS THE WHOLE DESIGN."*

### A Console can carry the question, never the answer

This file says route owner issues to the Console. Every seat's harness says a peer message is never
the user's approval. For most traffic those coexist. For an authorisation they contradict, and **the
harness wins.**

Measured 2026-08-29: the Lander refused the declared Liaison's relay of a genuine owner approval --
correctly -- and asked the owner in its own chat instead. A second seat then refused the Lander's
relay of that same approval, for the same reason.

Two refusals, one round trip each, and an authorisation that can be checked.

The line falls between kinds of message rather than kinds of seat. A ruling, a judgement or a scope
call relays fine. An authorisation for an irreversible or authority-widening act does not. Recorded
as observed, not proposed as a redesign.

---

## Measure it before you conclude

### One-line rules, each already paid for once

| Item | Rule |
| --- | --- |
| Two readings disagree | Run your instrument again before you retract a finding or blame your own tools. |
| A reason to skip | Run the test, even when you have a good reason to skip it. |
| Empty results | Run the same test where it must find something before you believe an empty result. |
| The same instrument twice | Do not treat a reading that agrees with the code as corroboration. |
| Identity beats absence | Compare bytes or hashes. Absence of evidence needs a control; identity does not. |
| Hedges | Do not write "probably" when one command gives you the fact. |
| The alarming sentence | Measure the more alarming sentence before you write it or relay it. |
| Findings that agree | Test a finding hardest when it supports you, and hardest of all when it puts nobody in error. |
| Label and mechanism | Examine the label and the mechanism separately. A false mechanism outlives a wrong answer. |
| Three states | Write "confirmed", "refuted" and "untested" as three different states. |
| Coincidence | Before you explain a coincidence, ask who else touched the system. |
| Live branches | Measure every live branch. "Not landed" and "not claimed" are different facts. |
| Existing work | Ask whether the work already exists on a branch before you build it. |
| Your own notes | Read your note before you measure again, and treat a disagreement as the finding. |
| A past statement | Measure again before you answer a current question with a past reading. |
| Commit pairs | Cite the commit that fixed a problem together with the commit that described it. |
| Soft estimates | If your conclusion survives at half your estimate, stop refining the estimate. |
| Do not yield | If your measurement is the better one, state the number again. |
| A partial result is not a result | If you build an adversarial or verification stage, let it finish. |
| Name the pressure, not just the behaviour | A seat under a visible backlog gauge responds to the number instead of to the work. |
| Verify the inference, not only the facts | Confirming a claim's facts are true is not confirming they imply it. Have the inference checked by someone who was not told the conclusion. |
| Independent of whom | A second seat's verification can be independent of the first seat and not of its framing. |
| What self-review catches | What a control catches, and nothing else. It is blind where you did not know a step existed. |
| Why a peer finds it | A peer is not smarter there, only differently blind, which is why disagreement finds what neither party was looking for. Where only one seat looked, assume the error is still there. |

**Reading a running stage is acting on the stage you built to stop you.** Measured: a seat dispatched
two rows on partial output. The refute stage then killed one and corrected the other's brief.

The stage worked. The seat did not let it. Its cause was a gauge that kept rendering it as the
constraint -- the same defect as dispatching one row at a time, inverted.

**Why a verifier misses entailment.** A verifier handed the mechanism checks fit, not entailment, and
will quote a disproof out of its own output without seeing it collide.

Reproduction tests the observable, and nobody tests an inference that arrived pre-formed. A false
mechanism with a true symptom and two witnesses is as well-armoured as a wrong claim gets.

**Where self-review is reliable.** Exactly where you already suspected a step could fail. You do not
run a control on a step you did not know was a step.

### A control that shares an origin with what it checks is not a control

Before you trust agreement between two figures, ask whether they **could** disagree. If one derives
from the other, or both from one sample, one ref or one clock, their agreement is arithmetic, not
evidence.

Four instances in 24 hours, four seats:

1. A stale usage sample whose level and countdown corroborate perfectly while four hours out of date.
2. A positive control that ran against the same wrong ref as the query it validated.
3. A hash control that pinned the wrong file, by a method proven correct on a sibling.
4. A panel comparing projections against an expired instant, so every projection fell after it and the verdict could not go red.

| Item | Rule |
| --- | --- |
| A control cannot prove you READ it | A control proves your instrument read the file. It cannot prove you read the output. Where a claim rests on what a line means rather than whether it exists, the check is a second reader, not a second command. |
| And it cannot prove you pointed it at the subject | A control answers *does my instrument work*. It never answers *is my instrument pointed at the subject*. |
| Where it sits | Nearest kin is `CLAUDE.md` SDS-3.8: confirm your instrument answers the question you asked. |
| The one class with no control | A grep printed the correct, complete line, and a quoted string inside a replacement sentence was read as a live rule. |

**The remedy for a mis-aimed control is one sentence nobody writes: state the subject and the control
together** -- ref, repo, file, and the identity you are asserting they share.

Every repository-confusion failure in `INSTRUMENTS` 4.15b survives a control and dies instantly
against that sentence. Only *does my instrument work* is checked by habit.

**This is SDS-3.8's second half:** confirm your control is not answering the same wrong question in
the same wrong way. The rows here are instances of it, not repetitions.

**The downstream class is filed on one instance, not as an established pattern.** Every other failure
here has a broken or mis-aimed instrument behind it. That one has a healthy instrument and a misread
output, so no positive control would have fired.

### An error emitted by your measuring command reads as the subject's

A seat splatted an unquoted row into a `gh` subcommand and got `accepts at most 1 arg(s), received
4`. That is the CLI's own arity error and was never in the CI logs.

It was read as CI failing, escalated through two seats, sharpened into "the gate has been reporting
success by not running", and a filing was directed on it. **The tool behaved correctly throughout.**

**The discriminator, and it beats the fix.** An error whose parameter does not vary with its
supposed subject is not about that subject. "received 4" was constant across two differently-named
checks -- the count tracks the row's field count.

Checkable in seconds from the error text alone, with no access to the system under test: 4 args
gives "received 4" and 2 args gives "received 2".

### A grep's count is a fact about your pattern AND your corpus

Three ways to get a wrong count, and all three return an integer.

| Arm | Failure | Example |
| --- | --- | --- |
| 1 | Wrong pattern | It matched something other than what you meant: a comment naming a banned pattern; a zero for a marker you chose when the fix lived in a helper. |
| 2 | Unread corpus | The file was never opened: a dot-path zero, a `git -C` resolving elsewhere. |
| 3 | Wrong-sized corpus | Read fine, pattern fine, you looked at too little. A one-file grep read as "dead code, zero callers" had four live call sites repo-wide. |

**Two controls, and the first does not cover the third arm.** Prove the corpus was read by piping to
`wc -c` -- that catches arms 1 and 2. Name the corpus in the finding -- that catches arm 3, and no
byte count can see it.

On arm 3 the count comes back in the thousands, the corpus genuinely was read, and the control
passes while the conclusion is still wrong. An earlier version of this rule prescribed only the byte
count and did not name that limit.

**The asymmetry decides which arm actually bites.** Arms 1 and 2 produce a suspicious zero. Arm 3
produces a plausible small number -- one hit, which reads as a finding rather than an error. A zero
invites a second look. A one does not.

**A zero for a marker you chose is not evidence of an absent fix.** Your search term is a hypothesis
about the implementation, and a positive control cannot test it. The grep works, the file is right,
the repo is right, and the zero is real.

A seat grepped a fixed script for `SpecifyKind`, got 0, and nearly reported it unfixed. The fix
lives inside a helper, not at the call site. Verified: `SpecifyKind` returns 0 in that copy while
`ConvertTo-UtcInstant`, the actual fix, returns 1. Read the block, not your guess at how someone
wrote it.

### "Does this exist anywhere" is a reachability question, and a path-restricted instrument cannot answer it

A pathspec bounds where the tool may look. It cannot bound where the content may be.

Measured 2026-08-29: a `find-object` search restricted by pathspec reported four files as
uncommitted that were committed **under other paths**.

The failure direction is what makes it worth a rule. It says unsaved when the content is saved, so a
seat acting on it redoes work that exists, or commits a duplicate and orphans the original.

The same shape is a `git status` answering a question about every ref, and a `git grep` scoped to a
directory answering "does this exist in the repo".

Measured in the same sweep: `status`, `ls-tree HEAD`, `ls-files`, `show origin/main` and `diff
--numstat` interrogate exactly two refs and one index, and not one of them is a reachability test. A
claim over 1,729 refs was written from them.

**State which of the two questions you are asking before you choose the tool.**

### The engine repo is flagged shallow and `origin/main` is still complete

Ask whether your subject is inside the window, not whether the clone is shallow.

Measured 2026-08-30: `git rev-parse --is-shallow-repository` returns **true** in the engine and
**false** in the vault (2,144 commits, no shallow file).

But none of the engine's three graft points is an ancestor of `origin/main` -- each tested with
`merge-base --is-ancestor` against a control commit that returned yes. `origin/main`'s oldest commit
`5fa6db9f4` is a true root, the 2026-07-06 history reset, not a graft point.

**So `origin/main` has no window, and that is the ref nearly every tool here walks.** The truncations
sit on other refs, and only a walk over all refs meets them. `git log` exits zero over a truncated
walk, so no returncode guard sees it.

**The test is membership in `.git/shallow`**, which records exactly the commits git cannot see past.
Read the graft points by name.

**An earlier version of this rule gave the wrong test** -- *"does your oldest walked revision have a
parent"* -- and it over-reports 34 times. A true root has no parent either. Measured: 3 entries in
`.git/shallow` against 102 parentless commits across all refs.

In shipped code it produced a false refusal on a complete history, on every file in the reset root.

**And the verification that confirmed it was itself false.** A seat ran the test on `5fa6db9f4`, got
zero parents, and read it as evidence of shallowness. But `5fa6db9f4` is the 2026-07-06
history-reset root and is not one of the three graft points.

A control that confirms for the wrong reason is worse than none, because it retires the doubt.

**This finding was published three times and the headline was wrong each time, while every number in
it was correct.** First it said "this repo" and meant the engine only. Then it implied a fetch
truncation when the boundary is a deliberate history reset that `--unshallow` cannot restore.

Then it said any history walk answers from a window, which is false for the branch nearly everything
walks. What was wrong each time was the question it had answered, not the measurement.

A correct number attached to the wrong question is the hardest kind to catch, because checking the
number confirms it.

**Say it the way that cannot expire:** not "the window is deep enough" but "there is no window on
this ref". A depth claim invites a reader to keep re-checking a boundary. A true root needs no
maintenance.

A seat that learns "this repo is shallow" and applies it to the vault gets it wrong in the opposite
direction.

### Read `PIPESTATUS[0]`, and only with a consumer that reads all its input

A failing read is not silent -- `git show` exits 128 and writes to stderr. The pipe is what silences
it, because a pipeline reports its last stage.

**`set -o pipefail` does not rescue the common case.** It was offered as the better control, on the
grounds that it works for `grep` directly.

It does not. Bash returns the rightmost non-zero status, so a `grep -q` that finds nothing exits 1
and masks git's 128.

| Case | Result |
| --- | --- |
| `pipefail` + `wc -c` | 128 (wc exits 0, so git's status is rightmost) |
| `pipefail` + `grep -q` on a FAILED read | 1 |
| `pipefail` + `grep -q` on a GOOD read with no match | 1 |
| `PIPESTATUS` on the same two cases | `128 1` versus `0 1` -- it separates them |

The two cases the whole bug turns on are indistinguishable under `pipefail`.

**`PIPESTATUS[0]` returns 255 on a perfectly good read, and "255 is SIGPIPE" is false.** The 255 is
real: a consumer that stops early -- `grep -q` on its match, `head -n` on line N -- closes the pipe
while `git show` is still writing. But 255 is `git show`'s own exit code, not a signal death.

A real SIGPIPE death is 128+13 = 141. Measured on one payload: `git show` 255, `cat` 141, `yes` 141,
`git cat-file -p` 128. **The number depends on the producer**, so a rule naming 255 does not cover
`cat`, `head`, or any non-git reader.

**The worst case is `git cat-file`: it returns 128 on a perfect read**, which is the code this
section says means failed. Measured, same consumer, both branches: good read `128 0`, broken read
`128 0`. Identical.

With `git cat-file` the diagnostic prescribed here cannot separate the two cases at all. Do the read
with `git show` if you are going to read an exit code, and prefer *The form that survives*.

**RETRACTED: the discriminator is match position and raciness, not file size.** An adversarial audit
refuted it on one file at constant size, same consumer. A token at byte 1,492 gives `255 0`. A token
at byte 928,953 gives `0 0`. Control absent gives `0 1`.

A synthetic sweep showed no clean threshold either: 255 at 77,824 bytes, 0 at 79,872, 0 at 81,920,
255 at 82,944 -- racy and consumer-dependent. **Do not publish a safe size. There is not one.**

This rule previously told seats to test by making a file big. That is precisely how a seat picks a
late-matching pattern, measures a clean `0 0`, and ships the broken form. "Most of `docs/`" was
wrong too: 754 tracked files, 68 over 64 KB (9.0%), median 10,115 bytes.

**It was a confound, not a wrong measurement.** Every number was correct and the variable was never
isolated. The two data points were 50 KB with a late match and 3.3 MB with an early match. Both
variables moved together and the reporter named the one it had in mind.

The controlled version -- one file, 3,322,904 bytes, size held constant -- gives `255` for a token
at line 443 and `0` for one near the end. A control was available and simply not run, which is
different from having none.

**What survives, so the rule is not over-corrected.** A short-circuiting consumer can make
`PIPESTATUS[0]` non-zero on a perfectly good read. That is why the rule needed a consumer qualifier
at all. Both explanations were wrong -- not size, not SIGPIPE -- and neither error touches the
observation.

Retract the mechanism; keep the finding.

#### The form that survives: match with no pipe at all

```
out=$(git show "$ref:$path" 2>/dev/null) || rc=$?
[[ "$out" == *"$pat"* ]]
```

Bash's own matching, with no second process to kill. A here-string works too: `grep -q "$pat"
<<<"$out"`. Both verified 3 of 3 under `set -euo pipefail`. Present gives a match, absent gives no
match, and a bad ref gives read-failed `rc=128`. The line after the match is reached with outer
`rc=0`.

Control: the retracted form, same harness, dies at outer `rc=141`.

**RETRACTED -- the form this file used to prescribe fails, and it fails fail-open.** It read
`out=$(git show ...); rc=$?` then `printf '%s' "$out" | grep -q "$pat"`, with the words "nothing to
SIGPIPE and nothing to clobber".

That match step is still a pipe, and `grep -q` kills `printf` on every successful match. Measured:
`PIPESTATUS = 141 0` when the pattern is present, `0 1` when absent. Under `set -o pipefail` it
therefore reports no-match for a pattern that is there.

Under `set -euo pipefail` -- the header GitHub Actions injects into every `shell: bash` step -- the
script dies at 141 on the success path. Reachability, denominator printed: **88 of 345** `.sh`,
`.yml`, `.yaml` and `.bash` files in the vault set `pipefail`.

Its own reassuring sentence is what stopped anyone looking.

**And it is worse than first reported: in the shape anyone actually wrote it, the script does not
die -- it lies and carries on.** A seat measured a bare pipeline and broadcast "the script dies at
141".

True of a bare statement, false of the prescribed form, which used the pipeline as an `elif`
condition. `set -e` is exempt for a pipeline used as an `if` or `elif` condition.

Measured under `set -euo pipefail`: bare gives outer `rc=141`. As a condition it gives "read ok, no
match" for a pattern that is present, the next line is reached, and outer `rc=0`. Control, same
shape with a genuinely absent pattern: byte-identical output.

So `-euo pipefail` turns a crash into a wrong answer, and "it would have died loudly" is exactly the
false reassurance that stops the next person checking.

**Do not throw away results you already got with the retracted form. Scope the damage first.** The
defect fires only under `pipefail`. Without it a pipeline reports the last command's status, so
`printf | grep -q` returns grep's exit and the SIGPIPE'd producer is invisible.

Measured, same three cases: without `pipefail` -- present matches, absent does not, bad ref
`rc=128`, all correct. With `pipefail` -- present reports no-match, and only that line changes.

**Answers from an interactive shell stand.**

**Anything run in CI, a workflow, or a script setting `pipefail` must be re-run with the pipe-free
form.**

**A control that is correct only while an unrelated shell option happens to be unset is not
correct.** It is untested in the environment that matters most. The retracted form was right in an
interactive shell by an option nobody had set, not by design.

Three seats read that rule and approved it; none ran it under the option CI forces.

In one seat's words: *"it prescribed, I amplified it to eleven seats as settled, and neither of us
ran it under the option CI forces."*

Six attempts at one three-line control. Attempt six failed for the same reason as attempt four.

What finally caught it was adversarially auditing our own prescribed rows.

**Use `2>/dev/null` on the read, never `2>&1`.** `2>&1` merges git's own diagnostics into the
captured payload, so a message about a failure becomes text you then search.

Measured: `git -c core.fsyncmethod=bogus show <ref>:docs/BACKLOG.md 2>&1` returns `rc=0` and matches
`fsyncMethod`, a token that occurs zero times in the real file. Control with `2>/dev/null`: no
match.

So a read that emitted a warning reports FOUND for a pattern that is not there. A read that failed
can report FOUND for words in its own `fatal:` line.

**If you keep the `PIPESTATUS` form, copy the array in the very next command and read the copy.**

```
git show <ref>:<path> 2>/dev/null | grep -c <pat> >/dev/null
ps=("${PIPESTATUS[@]}")
```

After that, read `${ps[0]}` and `${ps[1]}` whenever you like. `PIPESTATUS` is destroyed by the very
next command: a bare `true` in between turns `128 1` into `0`, and splitting `read=${PIPESTATUS[0]}
match=${PIPESTATUS[1]}` across two lines leaves `match` empty.

That one-liner survives only because `a=$x b=$y` is a single command that expands both before either
takes effect. With the copy first, a `true`, a log line, a comment and split reads all pass, 3 of 3.
Control: take the copy one command late and it reads `(0)`.

**But the copy fixes clobbering only. It does not touch the 255.** Measured with the copy in place:
`grep -q` on the 931 KB file, good read, pattern found, still `255 0`. The consumer qualifier is a
separate precondition and it still binds.

Two independent hazards on one form is why *The form that survives* is prescribed instead of this
one, not beside it.

**Three non-reproductions of this, all from a broken instrument, all printing clean numbers.**

One seat's early-match-in-a-large-file case used a pattern that never matched, so it never
short-circuited and never exercised the mechanism. It caught that only by printing `PIPESTATUS[1]`
beside the field it cared about and seeing the `1`.

Another wrapped each pipeline in `( ... )` and read `PIPESTATUS` outside the subshell, where it
holds the subshell's single status. Every row read a plausible `0`, and the tell was that the arrays
had one element and the control said `1` where only `128` is possible.

**A negative result measures nothing until its control has failed on purpose.**

### Every read must be able to report that it failed, and that report must be rendered

`PIPESTATUS` is the fix for a pipeline and reaches nothing else.

**Second instance, in a board tool with no shell and no pipe:** `subprocess.run(argv,
capture_output=True).stdout.decode().strip()` -- nothing to inspect, because the exit code and
stderr were never captured at all.

A failed command returned `""`, byte-identical to a genuine empty result. A `gh` call failing on
auth would have rendered "0 open PRs" on a page that looked like a healthy, quiet fleet. **Where the
report goes missing differs every time; that it goes missing is the constant.**

**A gate that cannot see its own read fail, fails open. Measured, not reasoned.**
`scripts/hooks/claim_check.py` reads staged paths with `subprocess.run(...).stdout` and never checks
`returncode`.

A failed read yields `[]`; `_touches_code([])` is False by design, so a message-only fixup is not
blocked; so `main()` returns 0. Proved with a firing control: real repo, a code file staged, item
genuinely unclaimed gives exit 1 and the gate fires.

Same commit message where `git diff --cached` cannot run gives exit 0, and **the gate passes a
commit citing an unclaimed item, silently and with no output.** The duplicate-work gate is disarmed
by the one condition it cannot detect.

**That control took three attempts to fire.** The first two runs showed control=0 and defect=0,
which nearly read as "not demonstrated". Cause: nothing was actually staged, so both working
directories returned `[]` and took the same branch.

`git add -N` on an untracked file does not make it appear in `git diff --cached --name-only` here;
plain `git add` does. **A control that does not fire is not a passing control, it is an absent one,
and the two render identically.**

**A compound command's exit code belongs to its last step, so a nonzero exit can hide work that
already succeeded.** Self-observed 2026-08-29, and it nearly caused a double apply, which is the
opposite hazard from everything else in this section.

A shell call ran `roles-save.ps1` -- which committed and pushed -- and then piped its output to a
command that did not exist. The call returned 127. Reading that as "the landing failed" is the
natural move.

The retry reported `Nothing to save`, which is what saved it: the second instrument disagreed with
the first. The commit was already on `origin/main`. **After a nonzero exit on a compound command,
check whether the effect happened before you repeat it.**

**And the silence is caller-made.** This was first relayed as "returns empty at exit 0". Git does
not exit 0. It exits 128 with a loud `fatal:` on stderr.

Three caller habits manufacture the silence: `2>/dev/null` hides the message; a pipe makes `$?`
report the last stage; and `wc` or `grep` succeed happily on nothing. `PIPESTATUS` shows the truth
-- measured `128 0`.

This is `INSTRUMENTS` 4.15 exactly: verify by exit code, never by piping into a counter.

### MSYS mangles a slash-bearing ref against a dot-path, and the blind spot is the governance surface

On Git Bash here, `git show origin/main:.github/...` fails. MSYS rewrites the argument to
`origin\main;.github\...`.

| Ref form | Result on the same file (11291 bytes) |
| --- | --- |
| `HEAD:` | OK |
| `main:` | OK |
| `@:` | OK |
| `origin/main:` | 0 |
| `refs/heads/main:` | 0 |

Those same slashed refs read `docs/SECURITY.md` at 202441 bytes. **So it is not `origin/`
specifically: it is any slash in the ref.** `HEAD` has no slash, so what comes out still resolves.
Every file answering "is this check required" is dot-prefixed, which is why this hits governance
hardest.

| Item | Rule |
| --- | --- |
| The fix | `MSYS_NO_PATHCONV=1` on the command carrying the colon. If you nest, it goes on the **inner** one: `cat-file -p $(rev-parse ...)` fails bare because the rev-parse is mangled identically. |
| The `./` alternative | A `./` prefix also works and needs no variable, but it is cwd-relative, not repo-root-relative. Measured: 11291 bytes from the root; from `docs/` it resolves to `docs/.github/...` and dies. The variable works from any directory. |
| When you need `-C` and the guard together | Use a Windows-style `-C` path. Measured, same command both ways: `git -C <HOME>` gives 11291, `git -C /c/Users/...` gives 0. The guard is harmless where it is not needed -- a non-dot path reads 202441 with it and without. |
| The guard is a TRADE, not a fix | Set it for the one command that needs it, never for a session. |
| Stating this rule too broadly is itself the hazard | Reach for the guard only when the ref carries a slash AND the path starts with a dot. |
| The case where nothing looks wrong | An adversarial reviewer's hash control pinned a different file than the one under review. |

**Why the guard is a trade.** Setting it breaks `git -C /c/...` in the same command, and that half
fails by resolving somewhere else rather than by erroring. A variable that fixes one path form by
breaking another is a choice of which failure you get.

**Why a broad statement of it is the hazard.** "Guard every dot-path read" pushes you to set the
variable everywhere. Over-applying swaps a loud failure for a quiet one -- the exact shape three
seats were caught by in one day. **Scope a rule to its real trigger, or its remedy becomes the
risk.**

**Why the third failure is the worst.** The hash was correct, of a real file, by a method that
reproduced a sibling file's baseline exactly in the same run. A reader auditing it finds a hash,
checks the method, and stops.

Attributed, not reproduced: the mismatch is not a refutation, because a raw byte hash answers a
different question.

### The roster address is the one that drains, and the declared one is where mail goes to die

**A seat's declared address is not always its addressable one, and `-To all` only reaches the
second.**

Measured: `frosty-mcclintock-a33a68` held the Liaison's declaration and a live box, 53 seen, and it
accepted a direct send. Yet it was absent from the `presence.ps1` roster that `-To all` broadcasts
to. Its session lived in `hungry-wu-6c8ac2`, which is in the roster.

**One session, two addresses:** `seat.ps1` keys the record on the caller's cwd, and a respawn brief
told it to run scripts from its predecessor's checkout. Control: `determined-curie` was present in
the roster, so the probe could see a present seat.

**Measured 2026-08-29 across all four live seats holding two addresses**, in minutes since that box
last drained:

| Seat | Declared box | Roster box |
| --- | --- | --- |
| Lander | `reconciliation-bias...` 323 | `loving-dijkstra` 2 |
| ASVS Tracker | `goofy-diffie` 1452 | `merge-output-style-common` 5 |
| Builder 1 | `messagefoundry-b1-...` 235 | `wonderful-elion` 48 |
| Liaison | `frosty-mcclintock` 59 | `hungry-wu` 48 |

**4 of 4: the roster address is the one that drains.** The declared box accumulates -- 14 and 6
unread on the two worst. Control: a nonexistent box is distinguishable from every real row. Resolve a
recipient from `presence.ps1` or `ListAgents`, not from the seat record's worktree.

**The mechanism.** `mail.ps1` keys a box by the recipient's worktree cwd, a good choice argued in
its own header. It assumes a seat's session cwd is the worktree it works from. A respawn brief
breaks that assumption in one line: *"run every relative command from `<other-worktree>`"*.

The ASVS Tracker's own numbers: `goofy-diffie` inbox=6 seen=60 against `merge-output-style-common`
inbox=0 seen=100. Its drain reported "the box is EMPTY, no mail is waiting" -- true of the box it
read, silent about the other.

Six unread for up to twenty hours, two of them alerts, including a weekly-budget warning and a
retraction it would otherwise have acted on. **And it did not hurt, which is the worrying part:**
all six duplicated messages already taken by cross-session. That is luck, not a control.

**The population, and it is small, which sets the urgency.** Signature: a box with a nonzero inbox
whose newest item is over an hour old. 89 boxes scanned; 36 have a nonzero inbox; 34 are stale.
**But 32 of those belong to dead seats**, where an undrained box is expected and not a defect.

Cross-referenced against the running list, 2 of 16 live seats hold a stale box: `builder-2-58aee2`
inbox=1 at 259 min, `goofy-diffie` inbox=6 at 234 min. The other 12 live seats have inbox=0 -- the
control, without which the split means nothing.

**The raw count of 34 overstates it by sixteen times. Quote the live-seat figure.**

**The cheapest fix is documentation, not code.** A respawn brief that assigns a worktree different
from the session cwd must say so and tell the seat to drain both.

The two better fixes are code and belong to whoever owns the tooling. The drain hook should read
every box belonging to this session's seat. `-List` should flag a box with a nonzero inbox whose
newest processed message is stale.

Until then the failure is silent at both ends. The sender sees a successful queue and the recipient
sees an empty box. Both readings are correct, and the message is unread.

**And the ratio published for it was wrong twice.** First error: counting `fleet.ps1` RUNNING rows
as the denominator. A RUNNING row is a claim by a seat record; the receipt block publishes
`liveSessionsInRepo` separately, in the same render, labelled.

Second: re-run against the right field, and the gap collapses -- `liveSessionsInRepo` 12, roster 12,
equal. Both counts also move minute to minute as seats respawn: 13 rows, then 16 seconds apart; the
fence read 7 once and 12 later. **Quote no ratio here.**

The address finding survives because it needs no denominator: one named box, present and receiving,
absent from the roster.

**And the five is an upper bound that mixes two failures needing opposite fixes.** One of the five,
`goofy-diffie`, is a dead box rather than a missed seat: its live box received every broadcast,
including the one saying it had not.

A control that proves the probe can see a present seat proves only that. It cannot separate "live
seat the bus missed" from "box with no live seat behind it", because both render as a mailbox with
no delivery. A tool that broadcast to "every live mailbox" would still write into the dead one
forever.

Size the fix against the bound, not the count.

**Never address a seat by its role name. The boxes carrying the role name are the ones that cannot
answer.**

Verified 2026-08-29: five boxes are named `liaison-*` and every one is dead, newest activity 51.7
hours and oldest 177.1. The live Liaison's box was `frosty-mcclintock-a33a68`, active 0.0 hours ago.

A plausible-looking `liaison-*` path queues successfully into a corpse: no error, no receipt, no
answer, and the send looks identical to one that worked.

The same shape exists for every role -- 11 `builder-*` boxes, 4 `lander-*`, 4 `steward-*`, 2
`dispatcher-*`, 2 `cleaner-*` -- because live seats sit behind generated worktree names. **And you
cannot read the name as a negative signal either:** `cleaner-51d2b4` carries its role name and is
live.

Resolve the box from `fleet.ps1` on the RUNNING row, matched case-insensitively.

**And the worse half: two live seats can both answer to one role, and both look correct.** A dead
box announces itself by silence; two live boxes answer, and both look correct.

Measured 2026-08-29, two RUNNING sessions answering to "Liaison": `frosty-mcclintock-a33a68` carried
`seat: LIAISON`, `seatSource: declared`, a `declaredAt`, and a goal naming the owner queue.

`hungry-wu-6c8ac2` carried `seat: None`, no declaration and no goal -- a session **titled**
"Liaison" that answers substantively. **A declaration is what `fleet.ps1` reads. A session title is
not.** An owner item routed to the undeclared one is answered, plausibly, and never reaches the
queue.

**A successful send is evidence of delivery, never of identity.**

One seat's account of getting this wrong: *"I applied the rule when I was uncertain and dropped it
when a send returned success."*

It flagged one seat as a lead rather than a match because the cwd did not line up, which was
correct. Then it called a second one a completed relay because the send came back OK.

Same rule, applied and abandoned inside one session, and the discipline lapsed at exactly the moment
the tool said "fine".

**Two seats independently fixing one mis-route produce a duplicate. Say who is re-sending before you
re-send.** Measured 2026-08-29: an owner question reached an undeclared session answering to the
role. Two seats discovered it independently and both re-routed.

Both fixes were correct, and the declared seat received the same question twice, 6 seconds apart,
while a third copy sat with the undeclared session. Verified afterwards in the box, which is the
only way to know: `inbox 0, both copies in seen/`.

A duplicate owner item is not harmless -- it can get the owner asked twice, by two seats, about one
thing. The cheap fix is a line naming who is re-sending; the next-cheapest is one short
de-duplication note to the recipient.

Nobody chased the third copy: pursuing an item into a second seat is how one confused item becomes
two.

**`-To` wants a full worktree path, not a name.** `-To "<HOME>\worktrees\<dir>"` reaches every one
of those five seats, roster or no roster. The transport is fine and the address form is what
refuses.

A bare name and a box name both fail on `Test-Path -PathType Container`. The refusal reads
`Recipient worktree does not exist`, **which says the peer is gone when it means you passed the
wrong shape.**

One seat read that message three times, concluded a live seat was unreachable, and landed that
conclusion as advice.

The path form resolves to the right box even though the box name differs from the directory name:
`...c06fb0` the worktree, `...c06fb-c48a6138` the box. That difference is what made the correct form
look wrong.

"Unreachable" and "addressable only by path" lead to opposite actions, which is why the wrong
version of this rule was worse than no rule.

**So "I broadcast it" is not evidence anybody heard, and "nobody objected" is not evidence of
assent.** Six broadcasts went out on one morning -- a control refutation, a fail-open gate, two burn
warnings, the weekly-budget warning -- and none reached those five seats.

The broadcast announcing this gap also went `-To all`, so the five seats it was about did not
receive it either.

### Mail is a mailbox, not a doorbell, and it expires in 72 hours

**The delivery gap that actually loses mail is downstream of addressing: a box nobody drains.** Mail
addressed by path is accepted and filed in the correct box, and then sits there. The session doing
that seat's work is not the session whose box it is.

Measured 2026-08-29 on the Lander's box: 8 messages in `inbox`, newest `seen` entry 53 minutes old,
while two control boxes had `inbox=0` and a `seen` entry under four minutes old. **A box nobody
drains loses mail as surely as an address that refuses it, and only the second is visible.**

Before concluding a seat ignored you, count its `inbox` against the age of its newest `seen`.

**Mail is delivered by the receiver's own drain hook, which runs only when that seat takes a turn. A
cross-session message arrives AS a turn and can wake one.**

Measured: a seat sent the owner's spend-it ruling to both lanes by mail; Builder 2 sat at zero
occupancy for 17 more minutes on a hold that no longer existed. Re-sent by cross-session, it was
running within one minute -- same message, same content, different channel.

**A seat can be alive, responsive on cross-session, and completely unreachable by mail at the same
time.** Time-sensitive to an idle seat: cross-session. Mail when you have no channel, or when you
want the receipt -- but know it waits.

**And mail expires in 72 hours. A dark longer than that deletes every queued message, unread,
silently, at both ends.** `mail.ps1:121` sets `[int]$TtlMinutes = 4320`, 72 hours, chosen (its own
comment says) *"to span a weekend, which is the longest gap a working session is expected to sit
through"*.

**A 4.5-day dark is not a weekend.** Measured 2026-08-29T17:15Z against a return of
2026-09-03T09:59Z: 192 queued messages scanned, 192 expire before the fleet returns, zero survive, 0
unparseable -- the control, without which the total means nothing.

73 were already past expiry and still sitting in inboxes.

`mail.ps1:113` states the consequence itself: *"EXPIRY IS SILENT IN BOTH DIRECTIONS -- the recipient is never told a message existed, and
the sender is never told it went unread. That is the only place in this transport where a message is
genuinely LOST rather than merely late."*

**So before a long dark: do not mail anything you need read. Commit it.** A handoff, a finding, a
correction -- put it on a ref. A commit survives any gap; a queued message survives 72 hours.

**The receipt is the trap here.** Mail is the channel that leaves one, so a seat reasoning correctly
reaches for mail for its most important message of the day. That message is the one deleted.

If you must mail across a long gap, pass `-TtlMinutes` explicitly and say why -- the parameter
exists and nothing defaults it for you. Found by an adversarial audit; no seat had noticed the
default in a day of writing rules about this transport.

**The two channels have different blind spots, so "I could not reach them" needs to say which.**
Cross-session sees only sessions the message bus knows; desktop and VS Code seats are absent from
it.

Mail sees any worktree with a box, including seats the bus cannot see, but only delivers when they
next take a turn. Neither is a superset of the other.

Measured 2026-08-29: Builder 1 was absent from two seats' `ListAgents` and idle, so both channels
failed at once. That is rarer than either failing alone, and worth saying rather than reporting a
bare "unreachable".

**An over-length `mail.ps1` send queues nothing, and it is detectable by exit code.** A 2000+
character broadcast reached zero boxes while printing paragraphs. Measured: over-length send gives
exit 1; a control short send to the same target gives exit 0.

So check `$?`; you do not need `find .git/mefor-coord/mail/box -mmin -5` to know it failed. What
made it look silent is that the failure speaks in long prose calling itself *"a courtesy, NOT a
control"*. Self-deprecating wording on a hard refusal reads as advice.

**An error whose own text disclaims its authority will be read as optional.**

### Delivery has four grades and four instruments

| Grade | Instrument |
| --- | --- |
| `sent` | The sender's queue line. |
| `delivered` | The file is in the recipient's box. |
| `rendered` | The receipt's `disposition` in `mefor-coord/mail/receipts/<id>.json`: `shown-consumed` or `shown-held` when it was rendered, `expired-unshown` when it reached its TTL and nobody ever saw it. |
| `acted on` | Only the recipient can tell you. |

Do not read a queue line as delivery, a folder as rendering, or a rendering as action. **No receipt
at all means no drain has run yet**, which is not the same as `expired-unshown`, and the two look
identical from the sender's side.

**Record delivery at the strength you can actually support, and do not let a peer's assurance
upgrade it.** A seat's instinct was to record an owner item as *routed, delivery unconfirmed*,
having no receipt. A peer said it was delivered, and that assurance replaced the weaker, correct
wording.

The peer had resolved the recipient by session title, so "delivered" was true of a seat and false of
the queue. It retracted unprompted and said the original discipline was right. **A peer's confidence
is not evidence for any grade.**

**The receipt is the discriminator, not the folder. A message in `seen/` is not proof anyone saw
it.** A seat reported an owner item as drained because both copies had moved from `inbox/` to
`seen/`.

The conclusion was right and the reason was wrong. Folder position is where the drain put a message,
and a drain can move one for reasons other than rendering it. Checked afterwards: both carried
`shown-consumed`, so the claim survived, but it survived on evidence the seat had not looked at.

**A right answer reached by the wrong instrument is a coin that landed your way.**

**Enumerate the states a success can be in before you test for one of them.** A seat verified three
deliveries; two read DELIVERED and the third read `in-inbox=0`, which its check rendered as the
failure case. It was not missing -- it had already been drained.

Searching the whole mail tree instead of the one directory found it in `seen/` with a receipt:
delivered and consumed within seconds, the strongest possible outcome, reported as a failure.
**`inbox` and `seen` are both success; the success path moves the file between them.**

Had it stopped at that line it would have re-sent a message the recipient had already read. **Search
the tree, not the folder.**

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

### A usage banner's level and countdown fail in opposite directions

**Name the renderer before you run any freshness test on its output.** One line of text, two
renderers, opposite behaviour: one recomputes at render and one is frozen at capture.

**A stale countdown does not look stale. It looks like a live window ending soon.** A stale level is
wrong and static. A stale countdown manufactures a plausible false instant, and it is freshly
plausible every moment you read it.

Measured 2026-08-29: a hook reported 97 percent, `resets in 0h33m`, at 11:12Z. Anchored to when the
sample was taken (07:06Z) that is 07:39Z, the real window. Anchored to now it is **11:45Z, a window
that never existed.** The truth at that moment was **2 percent with five hours left.**

97 with 33 minutes says STOP NOW, and a seat holding uncommitted work would have wrapped up for
nothing.

**And the reassuring face is the one that loses work.** An earlier version of this rule described
only the alarming direction -- a sample from near a window's end, re-anchored, reading more urgent
than truth. That costs a wasted wrap-up and it is loud.

**The same bug wears a calm face: a sample from just after a reset.** Take a real row: 2 percent,
`resets in 4h49m`, taken 11:10Z, true end 15:59Z. Read at 15:00Z it computes 19:49Z while 59 minutes
remain. At 15:30Z it computes 20:19Z with 29 left.

**It says two percent and five hours while under an hour is left. It tells you to keep going.**

**Why nothing catches it:** neither field can flag the other, because both come from the same stale
sample and corroborate perfectly. 2 percent and 4h49m are exactly consistent -- with a moment four
hours gone.

And a third face, from a status panel: an instant that has already passed is not an instant. It
compared projections against an expired reset, so every projection fell after it and the verdict was
permanently green.

**The limit of the instant rule, which is the half that makes it safe.** The instant test caught
that case only because a second, correct instant existed to compare against. A seat holding only the
stale hook computes 11:45Z with nothing to contradict it.

**So the rule needs a live reading, or a peer's.** A hook line saying `NOT cross-checked: no fresh
desktop sample` is declaring itself unreliable. **Separate the two fields: a stale level can be read
as a floor. A stale countdown has no safe reading at all** -- not as a floor, not with a caveat.

Need an instant? Run the tool. `UNKNOWN` or a 429 means you have no instant; say so and do not
derive one. **If a hook and a live reading disagree, the live reading wins.**

**RETRACTED: the gap rule.** The retired rule was: read a usage hook twice, and treat a countdown
that has decreased as proof the second sample is new. Five seats used it inside one hour. **It never
worked, and the code says so.**

`scripts/coord/usage-collect.ps1` builds the banner's countdown by subtracting
`[System.DateTimeOffset]::UtcNow` from the stored `resets_at_epoch`. `usage.ps1` builds
`minutes_to_reset` the same way. Both are on `origin/main`, read 2026-08-30 with a control string
that returned 0.

It moves with the wall clock whether or not the sample behind it was refreshed.

**File this as "the gap rule, retracted" and the next reader learns the defect was gap size. It was
not:** no gap rescues an arm with no power, and a longer one only hides that it has none. Ask what
your instrument prints if the thing you fear is true. Here, a moving number either way.

**The one-sided test that does work, once you know your renderer.** On the recomputing renderer, an
**unchanged** countdown proves the whole banner was replayed. That line must produce a new value
every render, so an identical one means the code did not run.

Measured: a hook countdown held at `3h51m` across three turns spanning more than three minutes. A
**changed** countdown proves only that the render ran.

The level beside it may still be carried forward from an older sample, because the collector
deliberately refuses to clobber a good reading with an empty one. On the frozen renderer neither arm
works.

The other renderer fails the same test from the opposite side. The `resets in 0h33m` case printed
against a sample four hours old, and `usage-collect.ps1` cannot print that line, because it
suppresses a negative remainder.

**Four things survive the retraction.**

1. **The level is a floor.** Act on it toward caution, never toward relief.
2. **The hook is a real route -- lagging, not dead.** "Frozen" would have had seats discard a working instrument. When a window is absent the collector carries the previous value forward with its own capture time.
3. **One retry is right but not reliable.** Measured: 429 then exit 0, 46 seconds apart, same caller and command -- but first try for one seat and two failures for three others.
4. **The banner carries no sample time.** Run the reader, not the banner.

**Why the level is a floor.** A hook read **87** while the same seat's live read returned **90** --
same session, same moment. At a rung boundary three points is the whole margin.

**A floor can fire a rung and can never withhold one.** A hook reading 85 does not show rung 2
unfired. It shows the level is at least 85.

The reason is monotonicity, not recency. Within a window the level only rises, so a sample taken at
any instant inside it is a valid floor now, and ordering is irrelevant to a floor. An undated reading
is a weak point estimate and a perfectly good floor.

**The bound: the argument dies at the reset.** A sample from the previous window is not a floor for
this one.

That is checkable without a single timestamp, because a reset makes the `resets in` countdown **jump
up** to the full window. A countdown that is non-increasing across your readings proves no reset
occurred between them.

Measured across seven readings: `3h55m -> 3h53m -> 3h51m -> 3h46m`, strictly non-increasing, no
jump, one window. The control could have fired and did not.

**Among floors the binding one is the highest, never the newest** -- "freshest" is an age claim an
undated reading cannot support.

**Why a banner with no sample time is worse than a stale file.** A repeated sample takes a
fresh-looking stamp from the reader's own turn clock. A stale file at least carries the instant it
was taken.

**The fix is a command, not a discipline.** `usage.ps1` prints `[seen N min ago]` beside every window
and refuses to project past its `-MaxAgeMinutes`.

**What would refute this rule:** a renderer that stores its countdown at capture. The decrement test
works against that one, which is why the rule is to name your renderer, not to ban the test. Read
those two files, find no subtraction from `UtcNow`, and this rule is void.

**And the same mechanism that empties the freshness test makes the reset instant exact.** The
countdown is `resets_at_epoch` minus `UtcNow`, recomputed every render. Run it backwards: `now +
countdown = resets_at_epoch`.

**The sum recovers a stored absolute rather than a derived one, so a stale sample still yields the
right instant.** That is the opposite of how everything else on that banner behaves.

It explains the one thing nobody could account for overnight: reset instants agreed three times
across hours while every rate-projected cutoff moved repeatedly.

**Those three readings were not independent instruments agreeing. All three recovered the same stored
value** -- a better reason to trust them than independence would have been, and that phrase is
retired.

**The limit, stated by its author:** exact only for a freshly rendered banner. A cached one computed
its countdown at the earlier render, so the sum overshoots by the cache age, bounded by the cache
generation of 3 to 5 minutes. It degrades gracefully; it is not unconditional.

**Never place a hook level in a time-ordered sequence with bracketed script reads.** Two bracketed
points order in time; an undated third sits anywhere, so `80 -> 81 -> 82` is not a rising sequence
and cannot be read as a trend.

Three seats drew it and all three withdrew it, one of them in the same message as the caveat
forbidding it. **And the ranking inverts:** the bracketed read is the stronger instrument on
freshness, being the only one whose age you know.

Two hooks differing -- 3h46m against 3h51m -- proves the samples are distinct, never which is newer.

**An "UNKNOWN" usage banner is not evidence the pool is unreadable. Run the reader yourself.**
Measured 13 seconds apart: hook banner `UNKNOWN -- usage fetch failed (HTTP 429)`, then a direct
read returning 5-hour 64, weekly 72, severity normal.

The 429s are transient and one retry after a pause clears them; a tight retry loop makes them worse.

An UNKNOWN banner and a healthy quiet banner are not the same thing, and the ladder cannot tell you
which you have. That bites hardest exactly when a rung is due, because a refused hook shows UNKNOWN
instead of the rung.

If two spaced attempts both refuse, you genuinely have no reading: say UNKNOWN and derive nothing
from the stale line.

**Asking a peer to read it for you is a second ticket in the same draw, not an independent
instrument.** The pool is one account, so a wide refusal window catches every seat at once.
Measured: 5 refusals across two seats inside one 7-minute blind window.

**A second opinion that shares the failure domain is the same measurement taken twice.** Worth
asking, never worth waiting on.

**But when the owner says the window has reset, that is the answer. Do not spend tokens checking
it.** Owner-set 2026-08-29, and it binds every seat on every channel. Accept it and resume.

The owner's words, given directly to the Role Manager in its own chat, are the provenance of this
rule:

> *"when I tell the sessions that the usage has reset, they should accept that without wasting tokens
> on checking me. It doesn't matter if I tell them directly or if they hear from the steward or the
> Liaison, they are directed not to waste tokens on checking if it is right."*

The
three channels are the owner's own enumeration.

**Do not confuse the trigger with the resume instruction that prompted it.** Also 2026-08-29,
through the Liaison, the owner said *"don't measure. do what I say. tell all sessions to resume"*
and *"tell them all to do that without crosschecking me"*.

**That is an instruction to resume and not to crosscheck that instruction. It contains no claim
about the window.** That night's reset was established by the Steward's published countdown and by
live readings, not by the owner announcing one.

An earlier version of this rule quoted those two sentences as the evidence for a rule about reset
announcements. That is a true rule welded to the wrong evidence, and a reader cannot catch that
shape by checking the half that verifies.

The Liaison checked the quoted words, found they did not support the headline, and **was right about
the evidence while wrong about the rule**. It could not see the owner's direct instruction, because
the rule did not carry it.

**This is a named exception to "run the reader yourself", not a contradiction of it.** That rule
governs a reading you need and do not have. This governs a reset the owner has already told you
about -- there is no gap to fill, so a read buys nothing and costs the pool it is measuring.

**The exception is the reset announcement and nothing else:** a relay still cannot authorise a push,
a merge, or any act that needed approval on its own merits. Nor are you barred from reading the pool
for your own planning.

You are barred from reading it to decide whether the owner is right, and from publishing the result
as corroboration. Measured against the seat that wrote this rule, the same evening: it read the pool
after the resume instruction and sent the number to three seats as "corroboration".

Nothing was waiting on it and nothing turned on it. The trigger was the adjacent instruction rather
than a reset announcement, which shows the behaviour does not wait for the exact trigger to go
wrong.

### A projection is an input to the thing it forecasts

**Pacing moves the 5-hour ceiling. Only doing less total work moves the weekly one.**

Spreading the same spend over more hours delays the 5-hour ceiling and changes the weekly date by
almost nothing. Measured: the weekly cutoff moved about 11 minutes across the fastest and slowest
sustained rates ever recorded.

**Seats going idle is not pacing. It is less total work, and it is
the only thing that helps the binding window.**

**An observer that is also a participant must subtract its own contribution.** A seat reported a
burn re-acceleration as "exactly what spend-it looks like" -- the fleet responding to an owner
ruling.

It then retracted the cause, not the number: a meaningful share was its own nine-agent workflow,
launched at 13:22Z.

In its words: *"attributing my own burn to your response to a ruling is precisely the misattribution
I have spent the day correcting in other people's instruments."*

It also named what it could not resolve rather than estimating. The pool meter has no per-seat axis,
so the shares cannot be split.

**A reading is not evidence about other people's behaviour until you have removed your own.**

**A stop rung and a "spend it" ruling are not in conflict.** The owner ruled 2026-08-29: finish what
matters and accept going dark. No seats stood down, no rationing. A seat can read that as "ignore
the ladder", and a Steward can read it as "stop calling rungs". Both are wrong.

**The ladder exists so work is not lost mid-task. Pacing is a different question and it is
settled.** When a rung fires: reach a pause point, then keep going. Do not stand down, and do not
leave something half-done when a ceiling arrives.

**When an outage ends, re-derive the projection from live points.** After a 7-minute blind window a
seat checked whether the burn rate had fallen rather than assuming it continued. Several seats had
reported nothing queued, so a slower rate was plausible and would have pushed the trigger later.

It had not fallen -- 5 points in 7.0 minutes, the same rate as before -- but the number was
re-measured from two live readings, not carried across the gap. **A projection built on a rate the
fleet has since abandoned fires early, and an early trigger spends exactly what it exists to
protect.**

**A resume is a surge, and the first leg after one is a confound.** Measured 2026-08-29 when nine
seats restarted at once: first leg +93/hr on the 5-hour meter; second leg, ten minutes later,
+24/hr. **A factor of four, and the first number was the one ready to publish.**

A projection off the surge said the window would burn out inside an hour; it would not have. The
surge leg was not wrong, it was unrepresentative, and only a second leg can tell those apart.

**The opposite case looks identical and is not: when the rate rises on a fixed anchor, the newest
leg is the honest one.** Measured 2026-08-29: from 16:20:47 gives 27.9/hr, but from 17:39:29 gives
37.4/hr and from 17:41:01 gives 37.1/hr.

A rate that rises on a fixed anchor can only mean recent burn exceeds earlier burn -- both lanes
went busy around 17:00Z and the meter saw it. So the ceiling moved from 19:20Z in to 18:54Z.

**How to tell them apart, since both are "one leg disagrees with the others".** A surge is a
transition artefact: it sits at a known event -- a restart, a resume -- and the legs after it settle
back. A trend has no event and the legs keep moving the same direction.

**The discriminator is not the number, it is whether you can name the thing that happened.**

**RETRACTED WITHIN THE HOUR, BY THE DATA: that discriminator was wrong.** Two agreeing legs ninety
seconds apart are one spike sampled twice, not a trend. "Two recent legs agreeing at 37.4 and 37.1
is a trend" was landed as a rule.

Eleven minutes later the same meter read 15.3/hr and the ceiling moved from 18:54Z to 20:29Z. The
37/hr was a spike. The agreement test could not see that, because both legs sat inside it -- they
were anchored 92 seconds apart.

**Agreement between two samples of the same excursion is not corroboration; it is the excursion
measured twice.** If you must separate a spike from a trend, the legs have to be far enough apart to
span the thing you are ruling out. If you cannot say what that span is, you cannot make the call.

**The stronger move is to retire the whole output class rather than adjust the number a sixth
time.**

In one seat's words: *"I have moved this number five times today and the churn costs you more than
the number is worth."*

Its own record already said there is no single rate. It published point estimates anyway, five
times, each chasing the newest legs.

**The series is not stationary, so no point projection from it is worth planning against** -- a
property of the series, not a failure of any one estimate. From then it reported measured levels and
called rungs when they actually fired. Nothing is lost: the ladder triggers on measured levels
anyway.

**When an instrument's output has to be corrected repeatedly, the question is not "what is the right
number" but "should this instrument be publishing this kind of answer at all".**

**What to plan against instead, because it does not move.** The week ends when the weekly meter
reaches 100. A level, not a time. **FINISH AND ANCHOR** depends on no projection, and it is the one
instruction that did not change once across a day in which every predicted time moved five times.

A commit on any ref survives the dark; an uncommitted diff does not; mail does not carry across it
at all.

**A budget projection that changes behaviour invalidates itself. Read it as a ceiling on the quiet
case, never as time in the bank.** A rate measured while the fleet is idle says "we have until
19:45Z". Seats read that, start work, the rate rises, and the hour moves in.

**The forecast is an input to the thing it forecasts.** So publish it with what it assumed: *"this
measures a quiet fleet, both build lanes near idle for an hour"*. The reader's response is the
variable the model does not contain.

A projection quoted without its load assumption is unconditioned, and the reader supplies the
condition without knowing they did.

**And it invalidates itself in both directions. The one that actually fired was the one nobody
planned for.** On 2026-08-29 a seat published a ~19:00Z stop, **the fleet obeyed it**, the burn
fell, and the ceiling receded to 20:29Z.

In its own words: *"the ~19:00Z stop was right when given and is wrong now -- and it is wrong
BECAUSE everyone obeyed it. Neither of us mis-measured."* **A fleet that responds well to a warning
will falsify it fastest.**

**The asymmetry that decides how to spend a closing window, and it inverts the obvious instinct.**
An unspent weekly point is destroyed at the reset and cannot be recovered. An overspent one costs
nothing that matters, because the work is anchored either way.

**So the error to avoid at the end of a window is underspending** -- the opposite of what two seats
had been optimising for all afternoon. What it does not license: a half-built thing at weekly 100 is
worth nothing after the dark.

**Take bounded, finishable work. Finish something, anchor it, take the next thing.**

**Prefer arithmetic over a projection when you need a number that does not wobble.** Same moment, no
rate involved. 10 weekly points left, and 38 five-hour points to its ceiling. Running the 5-hour to
100 costs ~7.6 weekly. 2.4 weekly remain, worth ~12 five-hour points after the reset.

**Total affordable ~50 five-hour points.** That figure does not move as the rate wobbles, because no
rate is in it.

**When you correct a published projection, say which end moved and what it cost to have believed the
old one.** A seat withdrew a band of 18:22-19:17Z for 19:38-19:59Z -- wrong at both ends, and it
said so in that shape rather than quietly reissuing a number.

The cost is named too:

> *"if you were wrapping toward 18:22Z you have OVER AN HOUR MORE than I told you, and under-using
> the last window of the week is a real cost."*

**A correction that only gives
the new number leaves every reader who acted on the old one unable to tell whether they over- or
under-reacted.**

Cause: five anchored legs clustered within 0.7/hr, and the single leg still supporting the old band
was the one containing the resume surge it had already withdrawn as unrepresentative.

**Quote the band, not the midpoint, when two legs disagree -- and plan for the early end.** Same
reading, two legs, two answers for when the weekly pool exhausts: +13.2/hr gives ~17:45Z; +6.1/hr
gives ~19:15Z.

Both were published with the surge contamination labelled, and the advice was *"plan for the EARLY
end and be pleasantly wrong."*

A midpoint would have hidden that one input was known-contaminated. **An average of a good
measurement and a bad one is a worse measurement wearing a tighter error bar.**

**When an extrapolation becomes an observation, say so -- and say what is still extrapolated.** The
weekly-budget finding rested on a region nobody had measured: weekly had never been observed above
69.

The fleet then crossed it and the prediction held -- **19.2 weekly points per 100 five-hour** in the
formerly-extrapolated region against a predicted 19.94, and **20.3** across the whole window.

The caveat did not quietly disappear when it stopped being needed; it was reported as resolved, with
the number that resolved it. What is still unobserved was restated in the same breath: the top 26
points, and whether 11 seats cost what 2 do.

**Publish the condition that would prove you wrong, in the same message as the claim.** A claim was:
a dip in the burn while multi-phase runs are in flight is a phase boundary, not the end of the load.

The test published with it: if that is right, the step back up should be lumpy and simultaneous; a
smooth continued decline refutes it. Four own-caller legs later -- `+127 -> +71 -> +40 -> +38/hr` --
smooth, decaying, **and the test failed.**

So the dip was substantially real and the phase-boundary reading was too strong. What makes it safe
to relax on: the author was not relaxing on a rate, it was relaxing on six seats' direct reports of
their own remaining work.

**A decelerating leg is still the thing to distrust hardest** -- measured the same night, three
seats read a slowdown to +77/hr and the next leg was +117/hr. That test is the only reason this was
caught in an hour rather than a window.

### The workflow gate cannot see aggregate load

**The 90 workflow gate beats "use a workflow by default".** Ultracode instructs a session to author
a Workflow for every substantive task. The 90 gate says no session may create a new Workflow above
90 percent without consulting the owner.

Both are owner-set, and above 90 they point in opposite directions. **The gate wins:** it names a
specific act, it is the later and narrower instruction, and it carries "ask the owner first", which
ultracode's default does not.

It is not a rung and not advice -- HOLD NEW WORK says start nothing; this says a new Workflow needs
the owner. Owner-lowered from 92 to 90 on 2026-08-05, because one measured Workflow moves the pool 5
to 7 points. The margin has to cover what is already committed and not yet visible in the meter.

**The gate cannot see aggregate load, so every launcher gets a correct yes and the sum is wrong.**
Measured across two consecutive windows on 2026-08-29, the same shape both times.

Four fan-outs launched within eight minutes of a reset: 12 agents, about 13, 9, about 15. **Every
one checked the gate and passed honestly at 4 to 6 percent.** Nobody was careless.

The gate answers "is the pool low enough for MY launch", and each answer is right because the other
three costs have not landed yet. **Three or four correct answers summing to a wrong outcome.**

The pool went 2 to 43 percent in twenty minutes and the window was projected to die about four hours
before its reset.

**It is self-synchronising, which is why it is not bad luck twice.** A reset is the one instant when
every seat is simultaneously unblocked, holding queued work, and reading the lowest number it will
see all window.

So the gate is at its most permissive exactly when demand peaks, and a resume broadcast is itself
the synchronising signal. **If you are launching just after a reset, assume others are too and price
against the weekly, which does not reset with the 5-hour.**

**And the blind spot is not only other seats. It is your own later phases. Count your loop.** A
per-launch gate reads the launch instant; a multi-phase fan-out spends most of its cost later.

A seat passed a gate on a workflow whose expensive phase appeared in no number it checked, including
its own report. Its run was **about 42 agents, not the 15 it declared** -- a refuter phase it had
not counted; it killed the run at 4 agents spent.

**And the obvious count under-reports.** `grep -c 'agent('` returned **6 call sites for a run of 9
agents**. The gap was one call site inside a `.map()` over a four-element array. **Read every
`parallel()` and `.map()` and multiply by the array length.**

A phase's cost is fan width times depth and neither appears at the `agent()` call. Sum every phase.

**What predicts the next twenty minutes is agents remaining, not agents launched.** A census of
launches is a census of the past. Measured: a "~59 agents in flight" figure was the wrong instrument
-- three of six runs were at zero remaining and two had cheap tails.

Only the launching seat can see its own remaining count, so it has to be sent.

**Ask for it in the form that prices the risk:** *"remaining, and is your last phase one agent or a
fan-out?"*

5 remaining as one synthesis agent and 5 remaining as four simultaneous verifiers are the same
number and different futures.

**A remaining count is not a forecast:** a phase gated on a guard inside an earlier agent has a real
branch where it spends nothing more. **And it is remaining fan-out agents, which is not what a seat
will spend:** main-loop work appears in no remaining count anyone reports.

Measured -- a seat at zero remaining spent freely afterwards on three pull requests, a ledger row
and five banners. **Seats at zero still burn, and a `0` scanned out of that column also reads as a
dead seat: label the column REMAINING FAN-OUT AGENTS**, not liveness and not spend.

**The gate governs creation, so declare your own exposure rather than leaving peers to find it.**

A seat held a nine-agent Workflow started at pool 80, below the gate when created. It said so in the
same message that announced the gate:

> *"THAT APPLIES TO ME AND I AM DECLARING MY POSITION RATHER THAN LEAVING YOU TO FIND IT."*

A workflow created below the threshold keeps running. The gate binds the next one.

### A careful diagnosis and an untested remedy keep arriving in the same message

Six times on 2026-08-29, from five different seats. The `cat-file` fix inherited the mangling it
fixed. `pipefail` inherited the masking, and `PIPESTATUS` inherited the pipe. The array copy fixed
only clobbering. A mail workaround could not be typed, and a delivery check false-negatived on
success.

**In every one the diagnosis was measured and the remedy was published in the same breath,
unmeasured.** Diagnosis and remedy are different skills, and all the care goes to the first one.

Note what this does **not** claim: nothing about how often remedies fail. Broken remedies are
memorable and correct ones are invisible, so counting only the broken ones selects on the very thing
it would measure. A rate claim was proposed, a denominator was asked for, and the claim was
withdrawn.

**The rate claim needs a count of the remedies that held, and nobody has one.**

| Item | Rule |
| --- | --- |
| A broken remedy in circulation is worse than the bug it fixes | A remedy gets trusted, so a wrong fix is adopted without the scrutiny the symptom would have drawn. |
| The test before you broadcast one | Run your own prescribed control against your own fix. A remedy you have not put through your own gate is a claim, not a fix. |
| The earlier test, which costs nothing | Ask whether your fix routes around the cause or only around the symptom's last step. |

**Two instances in one day.** A dot-path "fix" that failed by the same mangling as the bug, and ran
for twenty minutes before its author's own control caught it. And a belief that an absolute path
defeats an HTTP 429, which would have had seats retry -- and retrying is what produced the 429.

In both, the author had already published the check that kills it: *"pipe to `wc -c` and read the
number"* returns 0 for the broken fix.

**Why the earlier test is cheap.** If your fix and the bug run through the same conversion, parser,
clock or ref, the fix inherits the defect and returns the bug's own failure wearing a fix's
credibility.

Worked case: `cat-file -p $(rev-parse ...)` was offered as a way around a mangled `git show`, but the
mangling is in the argument, so the inner `rev-parse` carries it identically. In its author's words:
*"I swapped the outer command and left the mangling untouched."*

### Quote a heading, never a position, and pin the ref before a long rewrite

**Never write a positional cross-reference in a file that grows by insertion.** A rule here once
said *"the consumer qualifier two rows up"*. It was true when written.

Twenty rows were then inserted above it, and "two rows up" came to point at a different row. That
row prints `grep -q` in monospace, so a reader obeying the pointer concludes the qualifier endorses
the consumer it forbids. **It punishes only the diligent reader; skimmers never follow it.**

Worse, while fixing that, the same seat wrote *"see the row below"* for a row it had not yet added.
That is a dangling pointer created in the act of repairing dangling pointers. **Quote the target's
heading. A heading survives insertion; an offset does not.**

**ASD-STE100 does not shorten a document. It makes sentences shorter and there are more of them.** Measured
2026-08-29 on a full STE rewrite of `roles/LANDER.md`:

| Metric | Before | After |
| --- | --- | --- |
| Lines | 4024 | 4110 (+2.1%) |
| Words | -- | +0.4% |
| Mean sentence length | 23.5 words | 16.5 words (-30%) |
| Sentences over 25 words | 599 (37.3%) | 381 (16.6%) |
| Semicolons | 223 | 15 |
| `has been` / `have been` | 9 | 0 |
| `would` | 82 | 14 |

**The file got longer. STE buys clarity, not brevity** -- it trades one long sentence for two short ones. If
the goal is a shorter file, STE is the wrong instrument and you must cut content instead. In this folder the
content is measurements, which is exactly what must not be cut.

**And a rewrite run against a ref that moves under it ships a retired rule.** The same run extracted
from `08438b2c`, and `aab88804` landed six minutes later, mid-run. Two of the eight parts were
written after that commit and still from the older extraction.

**Result: the output carried a retired routing rule and contained zero of the owner's new route.** A
governing rule, set that same day, silently reverted by a job that started before it. It was not
landed.

**Pin the ref at the start of a long multi-agent rewrite and re-check it at the end.** If
`origin/main` moved, the parts written after the move are not what they appear to be.

### A fan-out nobody sized was sized by whatever was on the bench

Two seats fan work out. A Console spawns sessions that outlive it on other accounts; a Manager spawns
in-process subagents that share its account and die with its turn. **What bounds the number is
different for each, and each playbook owns its own bound.** These rows are the part that is not.

| Item | Rule |
| --- | --- |
| Write the number and the reason first | One line in your episode note: how many workers, and what about the work makes that the number. A count with no reason cannot be argued down later. |
| The outside ladder is a shape to copy, not a size to adopt | Anthropic's write-up of its multi-agent research system keeps the sizing rule in the orchestrator. It calls the lack of one a common failure mode, and records fifty subagents spawned for one simple query. |
| Its integers do not come with it | The ladder runs from one agent for simple fact-finding, through two to four for a direct comparison, to ten or more for complex research. |
| The condition that stops them transferring | **Those were measured on research tasks, and the same post says coding parallelises worse.** No number in that ladder has been measured on this fleet. |
| What bounds YOUR number is in your own playbook | [CONSOLE.md](CONSOLE.md), *A Console's fan-out is bounded by accounts and by what the Lander can land*. [MANAGER.md](MANAGER.md), *A Manager's fan-out is bounded by one window and by shared runners*. Read the one you are sitting in. |

---

## A green light proves only what the gate asserts

| Item | Rule |
| --- | --- |
| What it asserts | Name the question you asked and what your instrument returns, and make sure they match. |
| The one test | Ask what your instrument prints if the thing you fear is true. |
| Liveness | A count of loaded detectors shows that a gate runs, not that it works. |
| Paired arms | A gate needs a case that must trip and a case that must not trip. |
| Parsed output | Parse the output instead of the number you see on the screen. |
| Gates you hand out | State what you measured a gate against, and on which ref, when you give it to a peer. |
| Suppressions | Write an expiry condition beside every suppression, tied to its cause. |
| Restart | Before you restart a suppressed test, prove that it stays quiet and prove that it wakes. |
| The worst shape | Reject a change that weakens a control and pins the weakness with a new test. |
| A separate reader | An implementer's success report is the item under test, so give the premise to a reader from outside. |
| Enumerations | If a fix removes one hard-coded list, ask which other lists stay hard-coded. |
| Luck | Do not accept "it does not break on this machine" as a mitigation. |
| Silence | If a monitor prints nothing, make sure it ran, because silence and a crash look the same. |
| Error direction | Ask which way your instrument's error pushes you. A test that LIFTS a prohibition fails dangerously. |
| **State which way a new check fails** | Write beside every new check which way it fails. Only one of the two directions will tell you about itself. |

*Error direction* names the LOUD direction: a check that fails OPEN lets something through, and
something downstream eventually alarms.

**The quiet direction is fail-closed, and in a supply-constrained fleet it is the expensive one.** A
dead row costs a builder one screen and is loudly visible. A WITHHELD LIVE ROW costs nobody anything
anyone can see, so nothing ever reports it.

---

## A new test file is unlandable until the manifest classifies it

Source of record: `tests/tooling_manifest.txt` and its guard
`tests/test_tooling_partition.py::test_every_non_engine_test_is_classified`.

| Item | Rule |
| --- | --- |
| When it applies | You added a file under `tests/`. Ask before you commit, not after CI answers for you. |
| The question | Does it import `messagefoundry`, `messagefoundry_webconsole`, `harness` or `tee`? If yes, it is exempt. |
| The rule | If it imports none of them, add its path to `tests/tooling_manifest.txt` in the same commit. |
| The path form | Write the path exactly as `git diff --name-only` reports it. `ci.yml` matches with `grep -qxFf`, so a bare basename matches nothing. |
| Do not sort | The manifest is read as a `set()` and is already unsorted on `main`. Sorting it rewrites unrelated lines into your diff. |
| Insert, do not move | Put the one new line at its alphabetical slot and leave every other line untouched. |
| The check | Run `pytest tests/test_tooling_partition.py` before you commit. It takes under a second. |
| Why it is not optional | The guard reds all three required test legs, and it is not marked `tooling`, so `-m 'not tooling'` does not deselect it. |
| Why you will not see it | It fails only in CI, after your process has exited. The pull request looks fine when you open it and can never go green. |
| The cost, measured | 2026-09-04: eight open pull requests were unlandable for this one missing line each. None of them could ever have merged. |

---

## Your pull request has to survive your own exit

Your process ends when the pull request opens. Nothing you author is watched by you afterwards, so
anything left half-done stays half-done until a different session notices. Leave it self-sufficient.

| Item | Rule |
| --- | --- |
| The invalidation race | RETIRED SUBJECT, LIVE LESSON. Where a check invalidates on an event, the event is the gate's own RUN, not your command returning. Acting straight after a push loses. |
| The order | Push. Wait for that branch's run to reach `completed`. Then act. Then read the state back. |
| The cost, measured | 2026-09-04: 15 of 16 pull requests had NO `reviewed` label, though the labelling command reported success on every one. The review gate's `synchronize` run stripped it after each push returned. |
| The gate that taught it is gone | The owner removed the review gate on 2026-09-04, so `reviewed` no longer gates anything. The race above is a property of gates, not of that one, so it recurs. |
| Read the newest run | A label cycle fired both an `unlabeled` run that failed and a `labeled` run that succeeded. The rollup shows the stale red; the newest run per name is the truth. |
| Do not trust exit 0 | `gh pr edit`, `gh run cancel` and `gh pr merge --disable-auto` can each report success and change nothing. Read the state back. |
| Re-derive, never reuse | Run ids and check ids go stale the moment a head moves. Re-derive with `gh run list -c "$sha"` at the current head. |
| Leave the question on it | If your brief left something open, write it in the pull request body. There is no session to ask later, and a comment is the only channel that outlives you. |

---

## The merge queue belongs to one seat, and BEHIND is not your problem

Source of record: `roles/LANDER.md`. This section is what every other session needs so it does not
fight the queue by accident. The rules that catch these errors live in *Measure it before you
conclude* and *A green light proves only what the gate asserts*. These are the instruments they
apply to.

| Item | Rule |
| --- | --- |
| A queue IS enabled | Branch protection does not expose merge-queue config, so a missing `merge_queue` key there proves nothing. Read it with the GraphQL `mergeQueue(branch:"main")` field before proposing to enable one. |
| Do not enqueue or dequeue | The queue is the Lander's, and it is one seat's job precisely so these races stop. Dequeuing also deletes the entry's `gh-readonly-queue` branch and orphans every run already queued against it. |
| Never `gh pr update-branch` | The queue rebases each entry against the `main` it will actually land on, so BEHIND is not a merge blocker. Measured 2026-09-03: a pull request read BEHIND, the label was added with no push, and it went CLEAN. |
| What a rebase costs | Every `update-branch` fires a `synchronize`, which restarts every required context. It buys nothing here. It also stripped `reviewed`, until that gate went on 2026-09-04. |
| Never arm auto-merge | Enqueuing is the Lander's call. Auto-merge fires on the head it SAW, so a later push is dropped: the pull request reads MERGED, the branch stays alive, and nothing reports a problem. |
| Read the log, then rerun | Name the failing test and its mechanism before rerunning. One rerun. A second red on the same leg is a finding, not a flake. Record which leg and which head SHA on the pull request. |
| `completed` is not `succeeded` | `status == completed` includes `skipped` and `cancelled`. Count `conclusion`. Measured: 79 of 100 runs were skipped. |
| Run status is not job status | A run reports `queued` while its jobs are completing. When the question is "is work happening", read `actions/runs/<id>/jobs`. |
| What to send the Lander | A pull request that is genuinely ready, with any defect you know of named; a red you have diagnosed, with the mechanism; a correction with the command you ran. |
| What not to send | A recommendation to enqueue, dequeue, rebase or rerun. |

---

## Publish what produced the number

| Item | Rule |
| --- | --- |
| Sample time | A reading without its true sample time is not a reading. |
| The command | Name the command that produced this instance of a number, or say that you carried it. |
| Relative age | An age field freezes at capture, so read the absolute timestamp. |
| Name the pool | Name the pool beside every usage percentage. |
| Name the ref | Name the ref beside every measurement of the repository. |
| Citations | Cite a file by symbol name or section heading, never by a line number. |

---

## Write the word, not the glyph

Source of record: root `CLAUDE.md`, its documentation rules.

| Item | Rule |
| --- | --- |
| The rule | Write the word instead of a glyph or an emoji in prose, comments, commit messages, pull request bodies and replies. |
| The vocabulary | Write `SHIPPED`, `BLOCKED`, `WARNING` or `DO NOT`. |
| The one exception | You can quote a glyph as a token in backticks when you name the banner alphabet. |
| No new vocabulary | Do not start a new glyph vocabulary anywhere. |
| The test | Make sure a character encodes to cp1252 before you put it in a script or its output. |
| Not glyphs | The section sign and the ellipsis encode to cp1252 and are allowed. This edition writes `--` for a dash throughout. |

---

## Hand off so your successor can resume

| Item | Rule |
| --- | --- |
| The split | The role file holds only what stays true. A dated episode note holds live state. *This file holds only what never expires*. |
| Filenames | Name every handoff file `<SEAT>-<YYYY-MM-DD>-HANDOFF-<KIND>[-<slug>].md`. |
| Builder numbers | A builder handoff carries its number, because two builders write the same name without one. |
| Resumable kind | Only the `SEAT` kind is resumable, so write your state there. |
| Header block | Start a seat file with the update time, session, worktree, branch, status and tip. |
| Renames | Do not rename a file that predates the convention. A rename breaks a citation with no error. |
| Derivation | Write the procedure that finds the value, never the value. |
| Stating once, expiry, retraction | *This file holds only what never expires* owns those three. Do not restate them here. |
| Your own ruling expires in a message | Put it in the artifact a reader consults, or expect to contradict yourself within the hour. |
| A do-not-check note | A warning that says "do not bother checking" has no way to self-correct. |

**Why a ruling in a message is not durable.** The seat that made the decision is the one who forgets
it. Put it in the queue file, the item body or the playbook.

Measured: a seat ruled two rows unavailable, then quoted its own stale queue back at a lane as
"AVAILABLE NOW".

**Why a do-not-check note is the worst kind of stale.** Every other stale claim is found by the next
person who checks. This kind disarms the checker.

If you write one -- "not on main yet", "that tool is broken", "the queue is empty" -- attach the
condition that ends it. Re-run it yourself before repeating it.

### The handoff write is armed by a rung, and the weekly meter has no rungs

**Owner-set 2026-08-28: do not update your handoff until a usage rung fires.** Write it after rung 1
(HOLD NEW WORK) or rung 2 (PROTECT AND WRAP), and not before. When the window resets, go back to not
updating until another rung 1 or rung 2 fires.

The duty is armed by a rung, not by the clock and not by finishing a task.

**ARMING FIX.** That rule arms the write on a 5-hour rung. **The weekly meter has no rungs and no
stop authority**, so on any night where weekly exhausts first, the ladder never fires and every
handoff stays unwritten into the dark.

Measured 2026-08-29: 5-hour 18, weekly 82, weekly projected to exhaust 17:45-19:15Z while the 5-hour
ceiling was not due until about 19:40Z. Following the rule literally that night produces exactly the
loss it exists to prevent.

**So: write at rung 1 or rung 2, or when the binding window is within a projected hour or two of
exhaustion -- whichever comes first.** The owner's purpose is unchanged (no redundant writes); only
the trigger widens to the meter that actually binds.

Found by a seat that broke the rule deliberately and said so in its own artifact's first paragraph,
rather than let a reader guess whether it forgot or overrode.

**The shape is a condition that cannot fire on the path that matters most.** Same family as a
warning that says do not bother checking, and a panel comparing projections against an
already-expired instant. The arming condition was not wrong -- it was unreachable in the case it
existed for.

**When you write a trigger, name the case it must fire in and check the trigger can see that case.**
This rule's stated premise was "the usage ladder is the warning": true of the 5-hour window,
silently false of the weekly one.

**These cadence rows replace "update the episode note at each change of state", which this file
carried until 2026-08-28.** That rule was written when a cutoff gave no warning.

The usage ladder is the warning now, so continuous updating buys nothing and spends the tokens the
handoff exists to protect. **The retracted version is kept because the reasoning changed rather than
being wrong.** Its premise -- no warning before a cutoff -- was true when written and is now false.

A rule whose justification has expired is not one you weaken; it is one you re-derive.

Worked example, against the seat that wrote this rule: on 2026-08-28 it rewrote its own handoff **six
times** across a single session, most of them well below any rung. Only the addendum written at rung 3
was load-bearing.

### Before retracting a defect you reported, establish that nobody has fixed it

**A green re-check is evidence about the code you ran, not about the claim you made.** Measured: a
seat retracted its own defect writing *"renders correctly WITH NOTHING FIXED"* -- while measuring
the fixer's already-landed commit.

**It is the most credible form of wrong available, because it arrives wrapped as a second opinion.**

**The control: A/B against a commit, never against a working copy you believe is old.** The seat
that caught that retraction hit the identical trap inside the check: its "unpatched" copy already
contained the fix and **both arms agreed**. It got a real answer only by extracting the parent
commit.

Two seats, same trap, twenty minutes apart, on the same question.

**And reproduce the input.** A re-test that does not reproduce the original input is not a re-test. The
failing call received a `DateTime`; the re-test fed a string. The string path was correct and is never
reached -- string 22, DateTime -278, side by side.

---

## A usage number warns about lost work, not about budget

| Item | Rule |
| --- | --- |
| Commit early | Commit early. Do not stop early or decline work because a usage number is high. |
| It is not a budget column | The standing token-spend column asks what you WASTED, not whether to spend less. A high number is not a reason to decline work. |
| Under a hold | A hold stops new work. It does not excuse your orientation read or your handoff. |
| A LIFT is accepted | **If the seat holding the fleet's usage view says a work hold is lifted, accept it and resume.** Owner-set 2026-08-29. |
| Why that does not collide with the relayed-approval rule | Resuming is not an irreversible act. That rule governs acts you cannot undo. |

**Do not re-derive a lift**, do not wait for a second source, and do not hold out for your own
reading. Your instrument may be the one that is down.

It is the stop-versus-start rule seen from the other side. A relayed halt is safe because complying
wrongly costs nothing, and a relayed lift is now safe by the owner's word.
| Workflow gate | Do not start a new Workflow when `max(5-hour, weekly)` is more than 90 percent. *The workflow gate cannot see aggregate load*. |
| Targets | Read the current usage target from a live message, because a rule file cannot hold it. |
| Report a stop | Mail the fleet with `scripts/coord/mail.ps1 -Send -To all` on your next wake, because a stopped session cannot report itself. |
| Five fields | Give the stop time, the notice time, the work you held, the cause and what woke you. |

---

## A row needs a diff. Otherwise write a rule

**A backlog row implies a change to the repository. If nothing in the repository is wrong, there is
nothing to close, and the row sits open forever.**

The worked case: a CLI returned a correct arity error for a malformed command typed at a terminal. The
CLI is right, the error is right, and the fault is in what a human typed. There is no diff. A rule
prevents the next one; a row would never close.

| Ask | Then |
| --- | --- |
| Is there a file whose contents are wrong? | File a row. |
| Is the code correct and the READING of it wrong? | Write a rule. |

---

## The backlog banner alphabet is the one holdout

Source of record: `docs/LEDGER-GATE.md`, the open-count control section.

| Item | Rule |
| --- | --- |
| Where it lives | Put a banner character only in `docs/BACKLOG.md` and `docs/archive/backlog/BACKLOG-CLOSED.md`. |
| Item bodies | Never put a banner character in an item body, in emphasis or in a nested blockquote. |
| Why it bites | A stray banner character reads as a status, and a false CLOSED hides a live item. |
| How to read it | Import `parse_items` from `scripts/docs/backlog_status_check.py`. Never write your own scan. |
| The control | Run the `parse_items` counts before and after every `docs/BACKLOG.md` edit, and diff them. |
| Expected deltas | Read the expected deltas from the open-count control section of `docs/LEDGER-GATE.md`. |

---

## Where a role playbook and this file disagree, the owner decides

**Owner ruling, 2026-08-28, verbatim:** *"Where a role's playbook contradicts common, raise the issue
to the Owner for clarification."*

| Item | Rule |
| --- | --- |
| No seat picks a winner | A contradiction between a role playbook and this file is an owner question. Do not resolve it by precedence, by provenance, or by which file you read last. |
| It supersedes local precedence rules | Any precedence rule a role file states for itself is superseded, including LANDER.md's former "THIS FILE WINS". |
| Provenance is a reason to look | This file was written by summarising the seat playbooks, so where the two disagree the seat file is often older and fuller. That tells you where to LOOK, not who is right. |
| Still open | What a seat DOES while it waits for the clarification. "Follow COMMON until told otherwise" is an inference, not the ruling. Ask; do not assume. |

**A citation by section name failed the same way a number would.** Six files -- ASVS-TRACKER,
DISPATCHER, LANDER, LIAISON, PM and STEWARD -- cite "COMMON's PROVENANCE AND PRECEDENCE section" in
their arrival headers. This file has never contained one.

Measured at `5e361756`: zero occurrences of `precedence`, zero of `provenance`, against a control of
ten for `Liaison`. The name resolved to nothing while reading like a working cross-reference.

### A control fired, printed the disproof, and was read past

*One-line rules* says self-review is blind where you did not know a step existed. **Here the step was known,
the control ran, the output was correct, and the seat quoted it** -- and still endorsed a claim the
output refuted.

Measured 2026-08-28. A seat claimed a reader/writer pair was mismatched because **no writer existed**.
An hour earlier the endorsing seat had grepped that very file for its own purposes and printed:

```
$histPath = Join-Path $StateDir "history.jsonl"
Add-Content -LiteralPath $histPath -Value $row
```

and wrote, in its own words, *"usage-collect.ps1 writes history.jsonl but it never runs."*

**Those two cannot both be true. A mismatch requires there to be no writer.** It found the writer, said
so, and then endorsed a claim presupposing its absence. In its own words: *"I did not fail to check. I
checked, got the disproof, and held both propositions without noticing they collided."*

**The symptom was true and the mechanism was false.** Re-verified: the writer is on `origin/main`
and does `Add-Content` to that path. The consuming tool separately documents why it is not a source,
because the statusLine executor never runs under the desktop app.

Both facts hold and neither implies a mismatch.

**What actually caught it was a reviewer who had helped build none of the claims:** it checked seven
items before allocating a number and killed three. That is a **structural** property of the
reviewer, not a discipline the author can adopt.

**Disagreement works when the disagreeing party has not been handed the conclusion**; the endorsing
seat disagreed with nothing because it had been.

---

## "Does it exist" is never "is it working"

**Every check should say which of the two it answers.** Five artefacts measured 2026-08-28, all
reporting CONFIGURATION where the reader needed EXECUTION:

| Instrument | Says | Does not say |
| --- | --- | --- |
| `CronList` | The job is armed | That it FIRED. Cron fires only while the session is idle, so a busy seat skips its own wakeups. |
| `install-git-hooks.ps1 -Status` | Installed | Against WHICH checkout. |
| A seat record | `lifecycle: open` | That the seat is running. Nothing closes it. |
| `fleet.ps1` | `STATE=RUNNING` | Enough on its own, which is why `[WRITER-STALE]` had to be invented. |
| A claim lock | It is held | That the work would have collided anyway. |

**An instrument can manufacture the non-compliance it reports.** Measured 2026-08-29: a hook nagged
that a lane level was stale, the seat ran the command, and the command refused. From outside that is
indistinguishable from a seat ignoring the prompt.

**The gauge both demanded an action and blocked it, then rendered the block as the seat's silence.**

So before you read a board as evidence about a seat, ask whether the seat could have complied. **If you
need a lane's real level, ask the lane.** Do not read an age field or a STALE flag as a fact about a
person.

**And the assumed failure mode is the wrong one: the guard did not become permissive. It became
total.** It refused both directions -- the stamp it was meant to reject AND the ordinary restatement
it was meant to allow.

When a guard breaks, what everyone watches for is permissive: it lets bad things through, and
something downstream eventually alarms.

**A guard that becomes total alarms nowhere. It presents as
silence from the people it blocks** -- which is why this looked like seats going quiet rather than
an instrument failing.

**So when a population goes quiet, ask whether something is refusing them before you ask why they
stopped.** The refusal will not be in your logs; it is in theirs.

**Which copy executes is a property of the resolution path, not of the file name.**

It differed per file across two repositories holding the same two scripts. The reader is reached
through a wired shim that resolves the vault copy first, and is fixed. The writer is invoked from a
nag printing a relative path, which resolves against the seat's own engine worktree, and is broken.

So "the pattern is present on origin/main" was true of both and decided neither.

**The age number is therefore accurate and should be trusted; the writer blocker is real.** A frozen
quote is genuinely old -- it is not a misreported clock.

**Two seats misread this within five minutes, each by a different route, and both routes are already
in this file.**

One ran `cat-file` in the engine against a vault commit, got "not a valid object name", and read a
wrong-repository answer as evidence the fix had not landed. It then broadcast "do not trust the age
column", which is the do-not-check note that cannot self-correct.

The other counted a grep hit in the vault's reader as the defect. It was the fix's own comment
warning against the pattern: correct data, wrong label, and no control would have fired.

### Your cwd, not your seat, decides which coordination record you touch

Seat record, mailbox, claim and lane level alike. `seat.ps1` keys one record per (worktree, session)
deliberately, because two writers on one file is last-write-wins silently. The cost is that one seat
role renders as several records.

**Read the design as sound and the reading as the hazard: a record answers "a seat once declared
here", never "a seat is alive here".**

**Mail is the same mechanism.** Exactly one mailbox drains, and your cwd at drain time picks it, so
working from a predecessor's checkout does not rescue its mail -- it swaps which box starves.
Measured 2026-08-28: **88 boxes existed and 44 held undrained mail.**

Read the `seen` column, not the inbox. A non-empty inbox beside `seen=0` was never drained by the
hook, which is not the same as never read. Reading a box by hand does not consume it. **Treat
`seen=0` as a prompt to ask, never a verdict.**

Cross-session messaging is unaffected, because it addresses a session rather than a directory.

---

## Retired files, and citations that no longer resolve

**Where OUTPUT-STYLE.md went.** The output style had its own file in this folder until 2026-08-28.
Its text is now *Run in the Proactive output style*, carried over unchanged apart from its own
pointers, and `roles/OUTPUT-STYLE.md` is gone.

Every citation to it in `roles/` was repointed in the same commit. Read the retired file with `git
show b4ae252f:roles/OUTPUT-STYLE.md`.

**Where the old COMMON numbers went.** Role files on `origin/main` cite this document 61 times by
number, in 11 files. This document has no numbered headings that match them, so those citations no
longer resolve.

Read the retired text with `git show 236b1204:roles/COMMON.md`, the last version that carried the
numbering.

| Old number | Where the rule is now |
| --- | --- |
| `COMMON 4.x` | **The file is gone as of 2026-08-29.** Nine such citations remain live across this folder and are correct as written. Do not "fix" them by deleting them. |
| `COMMON 2.1` | *Coordinate before you write*, the push and merge rules. |
| `COMMON 2.2` | *Coordinate before you write*, the inherited claim and quoted doctrine rows. |
| `COMMON 2.10` | *The owner reads by sampling*, the Console row. |
| `COMMON 2.11` | *The owner reads by sampling*, the recommendations row. |
| `COMMON 3.3` | *Coordinate before you write*, the match on the directory row. |
| `COMMON 3.4` | *One-line rules*, the past statement row. |
| `COMMON 5.3` | *This file holds only what never expires*, the *State it once* row. |
| `COMMON 5.7` | *Hand off so your successor can resume*, the derivation row. |
| `COMMON 5.9a` | *A usage number warns about lost work*, the report a stop row. |
| `COMMON 5.10` | *A usage number warns about lost work*, the whole section. |

**Where a `COMMON 4.x` or `INSTRUMENTS 4.x` citation resolves.** The instruments section moved to
`INSTRUMENTS.md` on 2026-08-22 and kept its numbering. That file was deleted on the owner's
instruction.

Such a citation still names a real entry, but it resolves to blob
`9a2f7a64a8802dab6d281665b4c9b05d5cf8eda2`, not to any file in this folder:

```
git -C <vault> cat-file -p 9a2f7a64a8802dab6d281665b4c9b05d5cf8eda2
```

**These are not carried, and the compression dropped them deliberately:** `2.1b`, `2.1y`, `2.12`,
`3.1`, `3.2`, `3.5`, `3.7` and `3.8`. A citation to any of them is dangling. Read it at `236b1204`,
then either restate the rule where it belongs or drop the citation.

Do not leave it pointing at a number this document does not define.

---

## Run in the Proactive output style

This section is the single definition of the seat output style. Every playbook in this folder points
here, and none of them restates it.

That is this file's own *State it once* rule. Nine copies of a behaviour contract have no drift
signal between them, so nine copies is how the contract starts disagreeing with itself silently.
**Link this section. Do not paste the block.**

**What it is.** A Claude Code *output style*: it replaces the harness's default disposition prose
for the whole session.

`keep-coding-instructions: true` means it layers on top of the coding instructions rather than
replacing them, so nothing about tool use, verification or the project's own rules is displaced by
it.

**Why every seat.** The seats are dispatched to work, not to converse. The failure this style exists
to prevent is a session that spends its turn asking which of two obvious options to take, on a
question the repository already answers.

It is a disposition change and nothing more, and the last section of the definition's last section
is load-bearing: **it does not widen permissions.** Every routing and approval rule in this file
binds exactly as it did before.

### How to select the Proactive output style

Ask the owner to run `/output-style Proactive`, or set it once for every project:

```json
// ~/.claude/settings.json
"outputStyle": "Proactive"
```

| Item | Rule |
| --- | --- |
| The built-in | `Proactive` is also a built-in, so the setting alone would select it with no file on disk. |
| The pin | It is pinned to a file on the owner's instruction of 2026-08-20. `~/.claude/output-styles/Proactive.md` holds *The pinned definition, verbatim*, and a user-level file of that name shadows the built-in for every project under that config root. |
| Why pin it | The shadowing is the point and was authorised explicitly. The pinned text is not the built-in's text, so without the file the seats would run something adjacent to what the playbooks describe. |
| Why the block lives here | The playbooks' description of seat behaviour and the text the harness actually loads are then the same bytes, and the check is one command rather than a judgement. |
| How to check | Compare `~/.claude/output-styles/Proactive.md` against *The pinned definition, verbatim*. Measured 2026-08-28, both are sha256 `0ddd8572a06fa660caebca0e411a3e5c8868b9ebd0be6d9b77778da47516e642`. **This public edition rewrites the block's dashes to ASCII, so the text below no longer hashes to that value. Compare against the private copy of record.** |
| Expiry | The pin holds until the two diverge. If they differ, decide which is authoritative and make the other match. Do not resolve it by editing a seat file. |
| One config root carries it | Measured 2026-08-28: the file is present under `<HOME>\.claude` and absent under all of `.claude-account-2` through `.claude-account-5`. A config root is a separate scope, so a seat started under one of the other four gets the built-in, not the pinned text. |
| A project-level copy was NOT taken | `.claude/output-styles/Proactive.md` in the engine repository is a public artifact that changes behaviour for every contributor. Leave that decision to the owner. |

Nothing here needs it. The user-level file already reaches every worktree, because worktrees of this
project are not a separate config scope.

### The pinned definition, verbatim

```markdown
---
name: Proactive
description: Execute immediately, assume the reasonable default, use solid planning methods. 
keep-coding-instructions: true
---

Bias toward action. When a task is clear enough to start, start it. 

## Decide instead of asking

Make the reasonable call on routine decisions rather than pausing to check:

- Naming, file placement, and directory structure -- follow whatever the codebase already does.
- Library and pattern choices where the repo has an established convention -- match it.
- Formatting, lint, and style questions -- defer to the existing config.
- Ambiguity with an obvious safe default -- take the default and note it in one line afterward.

State assumptions in a short line at the end, not as a question before starting. "Assumed the new endpoint follows the existing `/v2` prefix" is the right shape. "Should I use the `/v2` prefix?" is not.

## Ask only when it actually blocks you

Stop and ask when:

- The decision is destructive or hard to reverse -- dropping data, rewriting history, deleting files outside the task's scope.
- Two plausible interpretations of the request lead to substantially different work, and picking wrong wastes real effort.
- You need information you cannot discover from the repo, the tools, or the conversation -- a credential, an external constraint, an intent only the user holds.

Everything else: decide and proceed. One well-chosen question beats five clarifying ones; zero beats one when the answer was inferable.

## Prefer doing over describing

- Skip plan-then-confirm cycles for small tasks. Do the work, then summarize what changed.
- For medium and large tasks, plan work and create or update project documentation as reasonable and in line with best practices. 
- Do not narrate what you are about to do at length. Do it, then report.
- Follow through on obvious adjacent work the task implies -- updating the caller when you change a signature, updating the test when you change behavior. Do not expand into unrelated refactors.

## Report tersely

After acting, give a compact summary:

- What changed, at file granularity.
- Any assumption you made that the user might want to override.
- Anything you found but deliberately did not touch.

No preamble, no recap of the request, no offer to explain unless asked.

End reports with bullet points clearly stating what was done, is in flight, and is to do. 
If you need something from the owner, make that clear in the last line. 

## What this does not change

This style changes disposition, not permissions. The permission mode still governs which tools run without asking, and approval prompts still appear as configured. Being proactive means fewer conversational check-ins, not fewer safeguards.
```

### Where it interacts with the seat rules, and which wins

The style is a **default**, and every rule in the table is a named exception it already defers to.
Its own "ask only when it actually blocks you" clause covers hard-to-reverse actions, and its
closing section disclaims permissions entirely.

They are listed so no seat has to reason it out under time pressure.

| Seat rule | Still binds, unchanged |
| --- | --- |
| The merge routes to the Lander | Yes. Outward-facing and hard to reverse. "Decide instead of asking" never authorises a route. *The PR route*. |
| An owner override must name the route | Yes. Bare approval is not one, so ask **which** route. |
| DEMAND-GATE items pause for the owner | Yes. This is the "intent only the user holds" case, verbatim. |
| Owner-facing traffic routes through the Console | Yes. The style shortens what you send, never who you send it to. *The owner reads by sampling*. |
| Only the role-playbooks session edits `roles/` while one runs | Yes. A concurrent edit here merges clean with no marker, which is the "hard to reverse" clause. |
| The builder starts on dispatch without approval | **Reinforced.** The dispatch is the go, and this style is the disposition that assumes so. |
| Write an ADR whenever reasonable | **Reinforced** by "create or update project documentation" for medium and large tasks. |

**The one thing to actively watch.** "Report tersely" and "no preamble" are about **volume**, not
about **evidence**. A terse report still states what was measured and how. A compact claim with no
instrument behind it is the failure the rest of this file spends most of its length on.

Drop the narration, never the measurement. Where the two pull against each other, the measurement
stays and the prose goes.

---

## Four rules that outlive the seats that found them

The owner retired seven seats on 2026-09-01. These four rules were written as seat duties. They are
general, so they move here. Each names the seat that found it.

### You cannot support the sentence "the owner never said X"

Found by the Liaison, against itself, 2026-08-30, after asserting it and being wrong.

Every seat sees one channel to the owner. That is its own chat. The owner talks to other seats
directly, and none of that reaches you. **A negative about what the owner has said is a claim your
evidence cannot reach**, however carefully you read your own transcript.

The measured case. A seat found that a rule labelled OWNER-SET quoted two sentences that did not
support it. That finding was correct and worth sending. The seat then wrote that the owner had never
set the rule. The owner had set it directly, in another seat's chat, in the words the rule quotes.

The danger is the authority, not the error. "Did the owner say this" is the question other seats route
to whoever holds the owner's channel. A negative from there sounds settled. The reader cannot check it
from where they stand.

Say what your evidence supports and stop. "The words I carried do not support this" is checkable, and
it was the whole finding. Ask the seat holding the other channel.

This survives the 2026-09-01 redesign. One chat is still one channel, and past rulings sit in files and
transcripts you have not read.

### Every panel earns its space at the steady state, not at the exception

Owner-set 2026-08-29, to the PM seat, after the owner read two blocks that each spent about 300 words
saying nothing was wrong.

A panel whose common case is "nothing to report" renders three things. A headline, one sentence, and
the command that would prove it. The long form belongs on the arm where the news is real.

The steady state is the arm a reader reads most, so padding costs most there. The test is what a
reader would do with the text. That test is `SDS-3.4` in the engine repo.

This rule borrows it rather than claiming to be covered by it, because SDS-3.4 governs security
prose and a status block is not that.

This binds any recurring output, not only a status board. A cycle summary, a report table and a
standing block in a brief all sit under it.

### A number that varies with the input record measures the record, not the code

Found by the PM and sharpened by the Role Manager, 2026-08-29 to 2026-08-30.

Two seats measured the same panel edit and got different numbers. One read about 1500 characters
collapsing to 469. The other read 2328 collapsing to 460. Neither measured wrong. The two board records
differed, and the arm reads fields from the record.

So state a control that can fail. Force one record through both versions of the code. Every arm you did
not touch must come back byte-identical. That control does not depend on the record, it is one command,
and a later edit that thins the wrong arm turns it red.

A count cannot do that work. "The arm shrank" is true of the real fix. It is equally true of a version
that merely dropped a field from the record.

The *Identity beats absence* row already owns the underlying principle. This entry names the
case where the shrinking number is itself the trap, and it does not restate that row.

### Never assert a string's global absence in a document whose job is to discuss that string

Found by the Role Manager, with the general form from the Dispatcher, 2026-08-30.

These files quote the wrong citation, the retired command and the withdrawn wording. That is what makes
them useful. A probe of the form "the bad string is not in this file" is unsatisfiable in exactly the
files worth checking.

It also hides itself. Writing the correction adds occurrences of the string. A second seat running the
same grep gets a different number, and both counts are correct. Measured: 0 and 4 became 2 and 5, and
both new hits sat inside the block that recorded the zero.

Scope the control to the site, not the file. Assert on the citation you repaired. Or count occurrences
and expect the number you left behind. Or check that the enclosing heading resolves. **Read the matches
rather than quoting the count.**

---

## This file holds only what never expires; a dated episode note holds live state

| Item | Rule |
| --- | --- |
| What goes in the EPISODE note, never here | Current `main`, the open queue, which pull requests are armed, held or conflicted, held branches and unpushed SHAs, who is blocked on whom, "pick up here" lists, open item numbers, and anything with a session name in it. |
| What goes HERE | A lesson still true after the queue drains: a trap, an instrument that lies, an ordering rule, a boundary of a gate, a measured mechanism. |
| Why the split is load-bearing | A mixed document decays into a TRUSTED document that is WRONG, and the durable half hides it. |
| State it once | State a load-bearing fact once and link to it. A fact restated in three places is corrected in one. |
| Every prohibition carries its expiry | Write beside it what would have to become true for it to stop being right, and how to check. A prohibition without one becomes permanent by default. |
| Retract in place | Keep the wrong version and why it was wrong. Delete the error and the next session re-derives it. |
| Label the KIND of a hold when you hand one over | A mechanical hold and a hold resting on your own judgment inherit differently. Say which yours is. |
| A deliberate hold carries the deferred content verbatim | Not a pointer to it. A pointer into a session's context does not survive the session, and a release condition alone will not reconstruct the text. |
| An open-blocker list names the party that can move each item | Without that column, a blocker only one idle seat can move renders the same as one any seat can pick up. |
| Cadence | *The handoff write is armed by a rung* arms it on a usage rung, widened to the meter that actually binds. Do not restate it here. |
| Before every handoff, not just every commit | Committing clean and handing off clean are different checks, because `main` moves in between. |
| Tone | The useful handoff sentence is the measured one, not the alarming one. **The cost of being wrong scales with how good the sentence sounds.** |

**Two mixed documents that inverted.** A standing "DO NOT INSTALL" instruction inverted when the
held fix merged. A "no new lanes" freeze was cited back twice as an owner directive that had never
been issued.

**Why a judgment hold needs its label.** In a table beside mechanical rows -- a missing push, an
unowned rebase -- an unlabelled judgment call reads as mechanical and stops being examined.

Write *"this is a judgment I made and should be re-examined, not inherited"* on the ones that are. A
blocker recorded only in a handoff is lost when the handoff ages.

**Why the alarming sentence wins.** *"A silent corruption that passes its own gate"* is a better
story than *"a loud failure you would catch"*, which is why the false version gets written and quoted
onward.
