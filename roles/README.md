# Role playbooks for parallel Claude Code sessions

This folder holds one durable playbook per **seat** in MessageFoundry's parallel session setup. A new
session in a given seat reads its own file on arrival, **instead of being hand-fed context**. That is the
whole point of the folder: the owner should not have to paste a briefing into a fresh window.

The vault is private, so these files may name internal process, gates, instruments and their failure
modes. They must still obey the project's writing rules -- no glyphs or emoji, and no present-tense claim
that MessageFoundry is deployed (it is a not-yet-deployed beta).

## The seats

This is a partial list. 

***SEVEN OF THE SEATS BELOW WERE RETIRED BY OWNER DECISION 2026-09-01: Dispatcher, Project
Manager, Liaison, Cleaner, Role manager, Process improvement and ASVS Tracker.*** **The live seats
are Console, Builder, Reviewer, Regulator, Steward and Lander.** *Their rows and files are kept as
the record of what those seats did.* **DO NOT ROUTE WORK TO A RETIRED SEAT, AND DO NOT READ A
RETIRED ROW AS A LIVE INSTRUCTION.** *The Console replaces the Dispatcher and the Liaison both: it
reads the record, picks the work, spawns a Builder, and is the only seat the owner talks to, so a
question for the owner goes there.* **The Regulator is new and decides whose failure a red check
is.** *Nothing replaced the PM, the Cleaner, the Role manager, the Process improvement seat or the
ASVS Tracker.*

| Seat | File | What it owns |
|---|---|---|
| Console | [CONSOLE.md](CONSOLE.md) | The plan and the brief. Reads the ledger, picks the row, writes a brief that holds for one turn, and polls for what comes back. **Replaces the Dispatcher.** Does not build, enqueue or merge. |
| Manager | [MANAGER.md](MANAGER.md) | **An ALTERNATIVE to the Console, not a layer.** Owner-spawned in one desktop instance, bound to ONE account, and runs its workers as in-process subagents rather than separate sessions. Several run at once and the only thing they share is the repository. Does not build, enqueue or merge. |
| Builder | [BUILDER.md](BUILDER.md) | One brief, one turn. Commits, pushes, opens the PR carrying the ledger row, then its process exits. It does not guess at what the brief left open, and it does not wait: it writes the question to the Console, comments it on the PR, and stops. |
| Reviewer | [REVIEWER.md](REVIEWER.md) | Reads the diff. A pass applies the `reviewed` label and posts the head SHA it read. A fail posts findings on the PR, for whichever Builder comes next. **The label is a required status check on `main`, and nothing automated ever adds it.** |
| Regulator | [REGULATOR.md](REGULATOR.md) | Decides whose failure a red is: the PR's, `main`'s, a flake, or the queue's. Only the PR's own failure becomes work. **It starts with no memory, so its log is not optional.** |
| Lander | [LANDER.md](LANDER.md) | **What enters the merge queue, and in what order.** Merge-forwards, which `strict: true` makes continuous as `main` moves. Label timing, because a merge-forward strips the label and it goes back on only after the resulting run completes. The one-at-a-time ledger slot, since the queue builds each entry on the one ahead of it. And handing back the PRs that need a ruling rather than work. |
| Steward | [STEWARD.md](STEWARD.md) | **A cron, not a seat.** Zero model calls, so it needs no account. Reads usage and names the account with headroom. It cannot warn a running session, because nothing can interrupt one. |
| Every seat | [COMMON.md](COMMON.md) | The rules and instrument failures that belong to no single seat. **Read this first, whichever seat you hold.** |
| Every seat | **RETIRED 2026-09-01** | **Seven seats were retired by owner decision: Dispatcher, Liaison, PM, Cleaner, Role Manager, Process Improvement and ASVS Tracker.** Their files are named here so a reader who remembers one finds it retired rather than absent. The Console replaces the Dispatcher. General rules those seats had found are carried into [COMMON.md](COMMON.md) rather than lost with them. **A document that routes work through any of the seven is stale.** |

**`INSTRUMENTS 4.x` and `COMMON 4.x` citations still resolve, but not to a file.**
`INSTRUMENTS.md` was deleted 2026-08-29 on the owner's instruction. Its content is blob
`9a2f7a64a8802dab6d281665b4c9b05d5cf8eda2`, readable with `git -C <vault> cat-file -p
9a2f7a64a8802dab6d281665b4c9b05d5cf8eda2`. Live seats still cite it, so do not delete those
citations. [COMMON.md](COMMON.md), *Where the old COMMON numbers went*, owns the row.

**A grant a seat receives ADDS TO its standing authority; it never narrows it.** When one arrives the
question is whether the seat already holds more, not what the message covers.
[COMMON.md](COMMON.md) 2.1a owns the rule and records why adding further pointers to a grant has
stopped working.

**A tick is a wakeup, not a message.** It keeps a seat awake; it carries no instruction and expects no
reply, so **no seat sends an ACK for one**, acknowledges one, or produces a status line because one
arrived.
[COMMON.md](COMMON.md) 2.1c owns the rule and what it forbids.

***THE PR ROUTE IS THREE STEPS, OWNER-SET 2026-08-29: create the PR and notify the REVIEWER -- a
courtesy, not the trigger, because the Reviewer finds waiting PRs itself; the
Reviewer POSTS ANY FINDINGS ON THE PR rather than handing it back to an author that has usually
exited; on approval the Reviewer passes it to the LANDER, which merges.*** **The Lander still owns the merge and holds its standing grant for it -- a PR now
reaches it THROUGH the Reviewer rather than directly.** *Handing work over is still the DEFAULT
action and no seat asks permission to do it.* ***NO PR MERGES UNLABELLED, BUT A MISSING REVIEWER SEAT IS NOT WHAT BLOCKS IT: ANY SEAT CAN APPLY THE LABEL.*** **RETIRED 2026-08-31: this line
previously read** "if no Reviewer seat is running, hand the PR to the Lander as before". *Since the
review gate was armed, `a reviewer has read this` is a required status check on `main`, so the
Lander cannot merge an unlabelled PR either.* **Start a Reviewer, have any other running seat read the diff and label it (`gh pr edit <N> --add-label reviewed`), or let the CONSOLE carry the question to the owner. See
[REVIEWER.md](REVIEWER.md) section 1.**

**Every seat runs in the Proactive output style.** Its single definition, how to select it, and how it
interacts with the routing and approval rules are in [COMMON.md](COMMON.md), *Run in the Proactive
output style* -- **the seat files point at it and none of them restates it**, for the reason this file
gives below: nine copies of a behaviour contract have no drift signal between them. **It changes disposition, not permissions.** The
push/PR/merge routing, the DEMAND-GATE pause and every approval gate bind exactly as before.

**A THIRD RENAME LANDED 2026-08-26 AND WAS RECORDED NOWHERE UNTIL 2026-08-28: `ROLE-PLAYBOOKS.md`
became `PLAYBOOKS-MANAGER.md`** (`604fb623`). *Reported by the PROCESS
IMPROVEMENT seat, which noticed the two renames above were recorded and this one was not.*

> ***IT LANDED AS AN `R100` PURE RENAME -- ZERO CONTENT MOVED -- WHICH IS EXACTLY WHY IT COULD NOT
> CARRY ITS OWN REFERENCES.*** *Seven citations were left pointing at the retired name, including the
> seats-table row in this file, and* **the sections they cited all still existed, so nothing errored
> and every grep read clean.** *Repaired `1f0daff6`; zero occurrences of the retired name remain in
> this folder.*

**A FOURTH RENAME LANDED 2026-08-29, owner-set: `PLAYBOOKS-MANAGER.md` became
[ROLE-MANAGER.md](retired/ROLE-MANAGER.md)** (`befdc79a`), *to stop the collision with the Project Manager
seat -- both abbreviate to PM and both were being addressed as "the manager".* **35 references
updated across 8 files; controls: 35 occurrences of the retired name before and 0 after, and 0
occurrences of the NEW name before, so nothing unrelated was folded into this seat.**

> ***AND IT DEMONSTRATED A FAILURE THE THREE RENAMES ABOVE DID NOT: A BLANKET REPLACE REWRITES THE
> HISTORY OF THE OLD NAME ALONG WITH ITS LIVE REFERENCES.*** *The paragraph immediately above was
> corrupted by the very pass that renamed the seat -- it came to read that the THIRD rename produced
> `ROLE-MANAGER.md`, which is false, and it is unfalsifiable from inside the file because every name
> in the sentence was by then a real one.* **Repaired in the same window, by the seat that broke it.**
> ***A file recording the history of a name must be edited BY HAND during a rename of that name,
> never by a global substitution*** *-- and the three renames above escaped this only because nobody
> had written their history down yet.*

> **The check after any seat rename, both arms:** *every link in this file resolves -- 11 of 11 at
> `befdc79a` -- and zero occurrences of the retired name remain OUTSIDE a history block. Run the
> second arm with a control token that must return zero, or a broken grep reads as a clean folder.*


***THE SEAT IS THE ROLE MANAGER. Owner ruling, 2026-08-28, in one line: "You are Playbooks
Manager".*** *Until then the H1 read "ROLE PLAYBOOKS seat" and this table's row said "Role
playbooks", while the file, the handoffs and `seat.ps1` all said `role-manager`.* **The seat
holding the single-editor rule did not settle its own name; it flagged both as live and asked.**

**The sweep was SCOPED TO THE SEAT NAME, like the two above.** *Three kinds of occurrence were left
alone on purpose:* **the owner's own rulings of 2026-08-13, 2026-08-22 and the Steward's, which are
quoted verbatim and say "Role playbooks"**; *this file's H1, which names the FOLDER and not the
seat*; and **a quoted table label inside an INSTRUMENTS entry.** ***A rename that edits a quoted
ruling has changed what the owner said.***

**Two seats were renamed on 2026-08-13: the Coordinator became the LANDER, and the ASVS Monitor became
the ASVS TRACKER.** Both renames were scoped to the seat name only -- `scripts/coord` paths, the verb
"coordinate", and the ordinary word "monitor" were guarded and asserted unchanged, because a rename that
edits the surrounding English is a rename that changes meaning silently.

**On the Coordinator name specifically.** The rename is recorded here rather than
applied silently, because the old name is still in use everywhere else on this machine at the time of
writing -- peer sessions, memory entries, and the published method notes all still say "coordinator", and
a live session is titled `_Coordinator`. If a peer refers to the coordinator, they mean the Lander. Expiry
condition for this note: delete it once no artifact a session is likely to read still uses the old name.

**The name was NOT recycled, deliberately.** The owner-queue seat added later was going to be called the
Coordinator, and was named the **Liaison** instead precisely to avoid reusing a retired seat name. Reuse
would have made one word denote two seats sharing no duties, against roughly 182 historical occurrences
that could not be swept -- they are records of what a session did on a given night, and rewriting them
would falsify the record to tidy a name. A distinct name costs nothing and the ambiguity would have been
permanent. **Do not reuse a retired seat name for a new seat.**

## The rule this folder is built on: ROLE files carry nothing that expires

**A playbook here states what will still be true after the current queue drains.** Live state -- the open
queue, which PRs are armed or held, current item numbers, who is blocked on whom, "pick up here" lists,
session names -- belongs in a **dated episode note**, never in these files.

That split is not tidiness, and it was paid for. A mixed document decays into a **trusted** document that
is **wrong**, and the wrongness is invisible because the durable half stays right. Two measured instances
from this project's own handoffs: a standing "DO NOT INSTALL" instruction, correct when written and
repeated in bold at the top of the file, **inverted** when the held fix merged, with nothing in the
document able to tell; and a "no new lanes" freeze that was recorded as an owner directive, cited back
twice as authority, and had never been issued.

Three consequences every file here inherits:

1. **State a load-bearing fact once and link to it.** A fact restated in three places is corrected in one.
2. **Write every standing prohibition with its expiry condition beside it** -- what would have to become
   true for it to stop being right, and how to check. A prohibition without one becomes permanent by
   default.
3. **Retract in place, and keep the retraction.** Several sections in these files are more useful for
   recording a wrong version and why it was wrong than they would be stating only the right answer. Delete
   the error and the next session re-derives it.

## Where episode notes live

Episode notes are deliberately **not** in this folder, because they expire and these files do not. They
stay wherever the seat holding them keeps them -- for the lander, alongside the project's other
working documents; for any lane, a durable handoff under `<git-common-dir>/mefor-coord/handoffs/` is the
better home, because that directory is shared across every worktree on the clone and survives any one
session's tree. A session scratchpad does not survive, and is the wrong place for anything another
session may need.

**Derive that directory, never type it:** `git rev-parse --path-format=absolute --git-common-dir`. The
bare `.git/...` form is wrong from a worktree, and every session is in one -- `.git` there is a file,
not a directory, so the bare form resolves against your cwd and lists **nothing**. An empty listing is
what that failure looks like, not what "no handoffs" looks like.

## Keeping these current

***RETIRED 2026-09-01: this section previously opened*** "WHILE A ROLE MANAGER SESSION IS RUNNING,
IT IS THE ONLY SESSION THAT EDITS THESE FILES", *and it sent feedback and change requests there
instead, whichever seat you were in and however small the fix.* **The owner retired the Role Manager
seat on 2026-09-01 and nothing replaced the folder-edit gate.** *No session holds this folder and
there is no seat to send a change request to, so the rule below does not bind and the expiry
condition it names is met.*

**WHAT SURVIVES IS THE REASON, AND IT STILL BINDS: DO NOT FIX A DEFECT HERE IN ONLY THE FILE YOU
OPENED.** *Sweep the whole folder for the same defect before you commit, because an edit that
invalidates a claim in a file you never touched merges clean with no marker.* **Say in the commit
message what you swept for.**

Owner ruling, 2026-08-13, in these words: *"The Role playbooks session should be the only session
currently editing the playbooks. There won't always be a Role playbooks session, so this isn't a
law... just a current rule."*

***THAT RULING IS KEPT AS THE RECORD, AND ITS OWN EXPIRY CONDITION HAS FIRED.*** *The owner wrote it
as conditional on a Role playbooks session running; the owner retired that seat on 2026-09-01.*
***RETIRED 2026-09-01: this paragraph previously read*** "So it is conditional. Check whether one is
live (`list_sessions`) before concluding you may not fix something." **Do not run that check to
settle this. It cannot see a VS Code session, and the paragraph below says why that mattered.**

***THE INSTRUMENT WARNING HERE IS KEPT BECAUSE IT GENERALISES. ITS REMEDY RETIRED WITH THE SEAT.***
`list_sessions` **cannot see a VS Code session**, so it returns "not found" for a session that is
running, and under the retired rule that false negative LIFTED A PROHIBITION rather than merely
costing you a question. **An absent seat and a retired seat render identically there, so never
settle a retirement with it.** ***RETIRED 2026-09-01: this paragraph previously ended*** "if you
still cannot tell, ASSUME ONE IS RUNNING and send a change request." *There is no standing single
editor to send one to, so that default would now block every edit and reach nobody.* **If a liveness
check returns nothing, use the liveness fence or ask.** *Full reasoning, and why the same blind spot
is safe under the owner-routing rule and was dangerous under this one: COMMON, "the liveness check
fails dangerously here".*

**Why, in one measurement.** A folder of cross-referencing files, read by every seat on arrival, edited
by however many sessions happen to be live. Concurrent edits to one file conflict loudly and get resolved; edits
that **invalidate a claim in a file you never touched** merge clean with no marker. This project has
measured that failure three times in one evening across two repositories. **A single writer was the
only thing that reliably caught that. NOTHING REPLACED IT, which is why the folder-wide sweep above
is now the control.**

**What to send instead, and it is worth more than an edit.** The best material these files have
received came from seats reporting what happened when they *executed* the playbook: the Builder that
ran the arrival battery and found a row that could not answer its own question; the Dispatcher that
found COMMON unreachable by COMMON's own rules; the Liaison that found its own seat unreachable from
every other file. **Report the measurement and what it cost you.** You do not have to propose wording.

**When you do propose wording, it is a claim like any other** -- it gets verified before it lands, and
several have not survived that. Send the measurement alongside it so the check is cheap.

Do **not** write a second, thinner summary of a seat somewhere else: two documents describing one role
have no drift signal between them, and this project has hit that defect repeatedly. If you want a
short pointer elsewhere, make it a pointer -- a summary goes stale silently, where a pointer cannot.

*Expiry condition, given by the owner in the same sentence: **no Role playbooks session running.***
***IT IS MET: the owner retired the seat on 2026-09-01***, *which is also the second lift the same
sentence allowed, the owner saying so.* **`list_sessions` no longer decides this, and a negative from
it never did establish the condition.** *A peer still cannot lift a rule here, and neither can a work
assignment from another seat.*
