# Role playbooks for parallel Claude Code sessions

This folder holds one durable playbook per **seat** in MessageFoundry's parallel session setup. A
session in a given seat reads its own file on arrival, **instead of being hand-fed context**. That is
the whole point of the folder: the owner should not have to paste a briefing into a fresh window.

These files name internal process, gates, instruments and their failure modes, because the vault they
were written in is private. They still obey the project's writing rules. No glyphs or emoji, and no
present-tense claim that MessageFoundry is deployed, because it is a not-yet-deployed beta.

**List the `roles/` folder rather than typing a filename from memory.** The seat set changes, and the
table in section 1 is a snapshot of a moving set.

**This file carries no live state on purpose.** The open queue, current item numbers, which PRs are
armed or held, who is blocked on whom and session names belong in a dated episode note. Section 8
states the split. Section 7 says where the notes live.

## 1. The seat set changed on 2026-09-01, and the Console replaced two seats at once

**Seven seats retired by owner decision on 2026-09-01: Dispatcher, Project Manager, Liaison, Cleaner,
Role manager, Process improvement and ASVS Tracker.** The Console replaces the Dispatcher and the
Liaison both. Nothing replaced the other five.

**Do not route work to a retired seat, and do not read a retired row as a live instruction.**

### 1a. The live seats

| Seat | File | What it owns |
|---|---|---|
| Console | [CONSOLE.md](CONSOLE.md) | The plan and the brief. Reads the ledger, picks the row, writes a brief that holds for one turn, and polls for what comes back. **Replaces the Dispatcher.** Does not build, enqueue or merge. |
| Manager | [MANAGER.md](MANAGER.md) | **An ALTERNATIVE to the Console, not a layer.** Added 2026-09-04. Owner-spawned in one desktop instance, bound to ONE account, and runs its workers as in-process subagents rather than separate sessions. Several run at once and the only thing they share is the repository. Does not build, enqueue or merge. |
| Builder | [BUILDER.md](BUILDER.md) | One brief, one turn. Commits, pushes, opens the PR carrying the ledger row, then its process exits. It does not guess at what the brief left open, and it does not wait. It writes the question to the Console, comments it on the PR, and stops. |
| Reviewer | [REVIEWER.md](REVIEWER.md) | Reads the diff. A pass applies the `reviewed` label and posts the head SHA it read. A fail posts findings on the PR, for whichever Builder comes next. **The label is a required status check on `main`, and nothing automated ever adds it.** |
| Regulator | [REGULATOR.md](REGULATOR.md) | Decides whose failure a red is: the PR's, `main`'s, a flake, or the queue's. Only the PR's own failure becomes work. **It starts with no memory, so its log is not optional.** |
| Lander | [LANDER.md](LANDER.md) | **What enters the merge queue, and in what order.** Merge-forwards, which `strict: true` makes continuous as `main` moves. Label timing, because a merge-forward strips the label and it goes back on only after the resulting run completes. The one-at-a-time ledger slot, since the queue builds each entry on the one ahead of it. And handing back the PRs that need a ruling rather than work. |
| Steward | [STEWARD.md](STEWARD.md) | **A cron, not a seat.** Zero model calls, so it needs no account. Reads usage and names the account with headroom. It cannot warn a running session, because nothing can interrupt one. |
| Every seat | [COMMON.md](COMMON.md) | The rules and instrument failures that belong to no single seat. **Read this first, whichever seat you hold.** |

### 1b. The retired seats keep their files so a reader finds them retired, not absent

| Item | Rule |
| --- | --- |
| Where they live | [retired/DISPATCHER.md](retired/DISPATCHER.md), [retired/PM.md](retired/PM.md), [retired/LIAISON.md](retired/LIAISON.md), [retired/CLEANER.md](retired/CLEANER.md), [retired/ROLE-MANAGER.md](retired/ROLE-MANAGER.md), [retired/PROCESS IMPROVEMENT.md](<retired/PROCESS IMPROVEMENT.md>). |
| ASVS Tracker is the exception | `ASVS-TRACKER.md` is **absent from this edition**, not filed under `retired/`. Measured 2026-09-04: zero files matching `*asvs*` anywhere in this repository. A reader who remembers that seat finds nothing here. |
| Why the rows survive | They record what those seats did. A document that routes work through any of the seven is stale. |
| Where their general rules went | Into [COMMON.md](COMMON.md), rather than lost with the seats. |
| Who answers an owner question now | The Console. It is the only seat the owner talks to. |

### 1c. `INSTRUMENTS 4.x` and `COMMON 4.x` citations resolve to a blob, not a file

`INSTRUMENTS.md` was deleted 2026-08-29 on the owner's instruction. It held COMMON section 4,
"instruments that lie", **4,408 lines**. The content is blob
`9a2f7a64a8802dab6d281665b4c9b05d5cf8eda2`, readable with `git -C <vault> cat-file -p
9a2f7a64a8802dab6d281665b4c9b05d5cf8eda2`.

Live seats still cite it, so **do not delete those citations**. [COMMON.md](COMMON.md), *Where the old
COMMON numbers went*, owns the row.

## 2. COMMON owns the rules that bind every seat, and these files point rather than restate

| Item | Rule |
| --- | --- |
| A grant ADDS, it never narrows | When one arrives, ask whether you already hold more, not what the message covers. [COMMON.md](COMMON.md) 2.1a owns the rule and records why adding further pointers to a grant stopped working. |
| A tick is a wakeup, not a message | It carries no instruction and expects no reply. **No seat sends an ACK for one**, acknowledges one, or produces a status line because one arrived. [COMMON.md](COMMON.md) 2.1c owns the rule and what it forbids. |
| Every seat runs in the Proactive output style | [COMMON.md](COMMON.md), *Run in the Proactive output style*, is its single definition. **It changes disposition, not permissions.** The push, PR and merge routing, the DEMAND-GATE pause and every approval gate bind exactly as before. |
| A playbook that contradicts COMMON is an owner question | [COMMON.md](COMMON.md), *Where a role playbook and this file disagree*, owns it. No seat resolves the contradiction by picking a winner. |
| Why the seat files point rather than restate | Nine copies of a behaviour contract have no drift signal between them. This project has hit that defect repeatedly. Make a pointer, never a second summary. |

## 3. The label blocks the merge, not the Reviewer seat

**Owner-set 2026-08-29.** Create the PR and notify the Reviewer. The Reviewer posts findings on the
PR, or passes it to the Lander, which merges.

| Item | Rule |
| --- | --- |
| The notification is a courtesy, not the trigger | The Reviewer finds waiting PRs itself. |
| Findings go on the PR | Not back to an author. A Builder's process has usually exited by then, so the findings are for whichever Builder comes next. |
| The Lander still owns the merge | It holds its standing grant for it. A PR now reaches it THROUGH the Reviewer rather than directly. |
| Handing work over needs no permission | It is the default action, and no seat asks. |
| What the gate actually is | `a reviewer has read this` is a **required status check on `main`** since 2026-08-31. `required_approving_review_count` is still 0, so the gate is the label, not a GitHub review. |
| Nothing automated adds the label | Only a person does, and a push strips it. |
| A missing Reviewer seat is not what blocks a PR | **Any seat can apply the label:** `gh pr edit <N> --add-label reviewed`. Start a Reviewer, have another running seat read the diff and label it, or let the Console carry the question to the owner. See [REVIEWER.md](REVIEWER.md) section 1. |
| **RETIRED 2026-08-31** | This section previously read *"if no Reviewer seat is running, hand the PR to the Lander as before"*. Once the gate was armed, the Lander could not merge an unlabelled PR either, so the fallback stopped existing. |

## 4. A rename is scoped to the seat name, and a blanket replace rewrites that name's history

### 4a. The four recorded renames

| Date | Rename | Commit | What it cost |
|---|---|---|---|
| 2026-08-13 | Coordinator becomes **Lander** | -- | Scoped to the seat name. `scripts/coord` paths and the verb "coordinate" were guarded and asserted unchanged. |
| 2026-08-13 | ASVS Monitor becomes **ASVS Tracker** | -- | Same scoping. The ordinary word "monitor" was guarded, because a rename that edits the surrounding English changes meaning silently. |
| 2026-08-26 | `ROLE-PLAYBOOKS.md` becomes `PLAYBOOKS-MANAGER.md` | `604fb623` | **Recorded nowhere until 2026-08-28.** The Process improvement seat noticed the two renames above were recorded and this one was not. |
| 2026-08-29 | `PLAYBOOKS-MANAGER.md` becomes [ROLE-MANAGER.md](retired/ROLE-MANAGER.md) | `befdc79a` | Owner-set, to stop the collision with the Project Manager seat. Both abbreviated to PM and both were being addressed as "the manager". |

### 4b. An `R100` pure rename carries none of its own references

The 2026-08-26 rename moved **zero content**, which is exactly why it could not carry its references.
**Seven citations were left pointing at the retired name**, including the seats-table row in this
file. The sections they cited all still existed, so nothing errored and **every grep read clean**.
Repaired at `1f0daff6`, with zero occurrences of the retired name left in this folder.

### 4c. A blanket replace corrupted the history of the name it was renaming

The 2026-08-29 rename updated **35 references across 8 files**. Controls: 35 occurrences of the
retired name before and 0 after, and 0 occurrences of the new name before, so nothing unrelated was
folded into this seat.

It then demonstrated a failure the three earlier renames did not. The paragraph recording the 2026-08-26
rename was corrupted by the very pass that renamed the seat. It came to say the third rename produced
`ROLE-MANAGER.md`, which is false, and it was **unfalsifiable from inside the file** because every
name in the sentence was by then a real one. The seat that broke it repaired it in the same window.

**A file recording the history of a name must be edited BY HAND during a rename of that name, never
by a global substitution.** The three earlier renames escaped this only because nobody had written
their history down yet.

### 4d. Three kinds of occurrence stay unswept, on purpose

The 2026-08-29 sweep left alone the owner's own rulings of 2026-08-13 and 2026-08-22 and the
Steward's, which are quoted verbatim and say "Role playbooks"; this file's H1, which names the
**folder** and not the seat; and a quoted table label inside an INSTRUMENTS entry.

**A rename that edits a quoted ruling has changed what the owner said.**

The seat's own name was settled by an owner ruling, 2026-08-28, in one line: *"You are Playbooks
Manager"*. Until then the H1 read "ROLE PLAYBOOKS seat" while the file, the handoffs and `seat.ps1`
all said `role-manager`. The seat holding the single-editor rule did not settle its own name. It
flagged both as live and asked.

### 4e. The check after any seat rename has two arms

Run both. Arm one: every link in this file resolves, **11 of 11 at `befdc79a`**. Arm two: zero
occurrences of the retired name remain outside a history block.

**Run the second arm with a control token that must return zero**, or a broken grep reads as a clean
folder.

### 4f. Do not reuse a retired seat name for a new seat

The owner-queue seat added later was going to be called the Coordinator. It was named the **Liaison**
instead, precisely to avoid reusing a retired name.

Reuse would have made one word denote two seats sharing no duties, against roughly **182 historical
occurrences** that could not be swept. Those are records of what a session did on a given night, and
rewriting them would falsify the record to tidy a name. A distinct name costs nothing, and the
ambiguity would have been permanent.

**Expiry for the Coordinator note specifically:** delete it once no artifact a session is likely to
read still uses the old name. Until then, if a peer refers to the coordinator, they mean the Lander.

## 5. The single-editor rule retired with its seat, and a folder-wide sweep replaced it

**RETIRED 2026-09-01: this section previously opened** *"WHILE A ROLE MANAGER SESSION IS RUNNING, IT
IS THE ONLY SESSION THAT EDITS THESE FILES"*, and it sent feedback and change requests there instead,
whichever seat you were in and however small the fix. The owner retired the Role Manager seat on
2026-09-01 and **nothing replaced the folder-edit gate**. No session holds this folder and there is no
seat to send a change request to.

Owner ruling, 2026-08-13, in these words: *"The Role playbooks session should be the only session
currently editing the playbooks. There won't always be a Role playbooks session, so this isn't a
law... just a current rule."*

**That ruling is kept as the record, and its own expiry condition has fired.** The owner wrote it as
conditional on a Role playbooks session running, then retired that seat on 2026-09-01. The owner
saying so was also the second lift the same sentence allowed. A peer still cannot lift a rule here,
and neither can a work assignment from another seat.

| Item | Rule |
| --- | --- |
| **What survives, and it still binds** | **Do not fix a defect here in only the file you opened.** Sweep the whole folder for the same defect before you commit. **Say in the commit message what you swept for.** |
| Why the sweep is the control now | Concurrent edits to one file conflict loudly and get resolved. An edit that **invalidates a claim in a file you never touched** merges clean with no marker. This project measured that failure **three times in one evening across two repositories**. A single writer was the only thing that reliably caught it, and nothing replaced it. |
| **RETIRED 2026-09-01** | This section previously said *"So it is conditional. Check whether one is live (`list_sessions`) before concluding you may not fix something."* Do not run that check to settle this. |
| The instrument warning is kept because it generalises | `list_sessions` **cannot see a VS Code session**, so it returns "not found" for a session that is running. Under the retired rule that false negative **lifted a prohibition** rather than merely costing you a question. **An absent seat and a retired seat render identically there, so never settle a retirement with it.** |
| **RETIRED 2026-09-01** | This section previously ended *"if you still cannot tell, ASSUME ONE IS RUNNING and send a change request."* There is no standing single editor to send one to, so that default would block every edit and reach nobody. If a liveness check returns nothing, use the liveness fence or ask. |
| A dangling pointer, named rather than repeated | The retired text cited COMMON, *"the liveness check fails dangerously here"*. Measured 2026-09-04: that heading is **not in this edition's COMMON.md**. The finding above stands on its own; the pointer does not resolve. |

## 6. Send the measurement; wording is optional and gets verified anyway

The best material these files have received came from seats reporting what happened when they
*executed* the playbook. The Builder that ran the arrival battery and found a row that could not
answer its own question. The Dispatcher that found COMMON unreachable by COMMON's own rules. The
Liaison that found its own seat unreachable from every other file.

**Report the measurement and what it cost you.** You do not have to propose wording.

When you do propose wording, it is a claim like any other. It gets verified before it lands, and
several have not survived that. Send the measurement alongside it so the check is cheap.

Do **not** write a second, thinner summary of a seat somewhere else. Two documents describing one role
have no drift signal between them. If you want a short pointer elsewhere, make it a pointer. A summary
goes stale silently, where a pointer cannot.

## 7. Episode notes live outside this folder, in a directory you derive

Episode notes are deliberately **not** in this folder, because they expire and these files do not.

| Item | Rule |
| --- | --- |
| Where they belong | Wherever the seat holding them keeps them. For any lane, a durable handoff under `<git-common-dir>/mefor-coord/handoffs/` is the better home. That directory is shared across every worktree on the clone and survives any one session's tree. |
| A scratchpad is the wrong place | A session scratchpad does not survive. Never put there anything another session may need. |
| **Derive the directory, never type it** | `git rev-parse --path-format=absolute --git-common-dir`. |
| Why the bare form fails silently | The bare `.git/...` form is wrong from a worktree, and every session is in one. `.git` there is a **file**, not a directory, so the bare form resolves against your cwd and lists **nothing**. An empty listing is what that failure looks like, not what "no handoffs" looks like. |

## 8. These files carry nothing that expires; a dated episode note carries live state

**A playbook here states what will still be true after the current queue drains.**

| Item | Rule |
| --- | --- |
| What goes in the EPISODE note, never here | The open queue, current item numbers, which PRs are armed or held, unpushed SHAs, who is blocked on whom, "pick up here" lists, and anything with a session name in it. |
| What goes HERE | A lesson still true after the queue drains: a trap, an instrument that lies, an ordering rule, a boundary of a gate, a measured mechanism. |
| Why the split is load-bearing | A mixed document decays into a **trusted** document that is **wrong**, and the durable half hides it. Two measured instances from this project's own handoffs: a standing "DO NOT INSTALL" instruction, correct when written and repeated in bold at the top of the file, **inverted** when the held fix merged, with nothing in the document able to tell; and a "no new lanes" freeze recorded as an owner directive and cited back twice as authority, which had never been issued. |
| State it once | State a load-bearing fact once and link to it. A fact restated in three places is corrected in one. |
| Every prohibition carries its expiry | Write beside it what would have to become true for it to stop being right, and how to check. A prohibition without one becomes permanent by default. |
| Retract in place | Keep the wrong version and why it was wrong. Several sections here are more useful for recording an error than they would be stating only the right answer. Delete the error and the next session re-derives it. |
