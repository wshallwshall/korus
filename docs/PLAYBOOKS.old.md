# The playbooks

## TLDR/BLUF

**What this is.** The seven live seats, what each one owns, and the file it reads on arrival. Each
seat has a short card this site serves, and a long playbook it does not.

**Why you should care.** The roster moved on 2026-09-01. Six seats were retired, and the file most
readers were sent to still lists them as live.

**How to use it.** Name the playbook in the opening prompt. Nothing routes one to a session.

---

## The seven live seats

Read `roles/COMMON.md` first, whichever seat you hold. It carries the rules that belong to no single
seat.

| Seat | What it owns | Card | Playbook |
|---|---|---|---|
| Console | Reads the record, picks the work, writes the brief. The only seat the Owner talks to. | [Console](roles/console.card.md) | `roles/CONSOLE.md` |
| Manager | An alternative to the Console rather than a layer above it. Runs workers as in-process subagents. | [Manager](roles/manager.card.md) | `roles/MANAGER.md` |
| Builder | One brief, one turn. Commits, opens the pull request, exits. | [Builder](roles/builder.card.md) | `roles/BUILDER.md` |
| Reviewer | Reads the diff and posts findings on the pull request. | [Reviewer](roles/reviewer.card.md) | `roles/REVIEWER.md` |
| Regulator | Decides whose failure a red check is. | [Regulator](roles/regulator.card.md) | `roles/REGULATOR.md` |
| Steward | A cron rather than a seat. Reads usage and names the account with headroom. | [Steward](roles/steward.card.md) | `roles/STEWARD.md` |
| Lander | What enters the merge queue, and in what order. | [Lander](roles/lander.card.md) | `roles/LANDER.md` |

**This site serves the cards and does not serve the playbooks.** The cards live under `docs/`, so
they are built like every other page. The playbooks live at the repository root, outside the Jekyll
source, so no URL on this host reaches them. Open them in your checkout.

---

## The card is a summary and the playbook governs

A card carries what does not expire: what the seat owns, what it must not do, its authority, what it
checks on arrival, and where the long file is. Caps are 150 lines and 6 KB.

Live state stays out of both. Open queues, item numbers and who is blocked on whom belong in a dated
note. A seat folder elsewhere paid for that rule twice, once when a standing instruction inverted
after the fix it was waiting on merged.

[Seats and worktrees](SEATS-AND-WORKTREES.md) covers how a card reaches a session.

---

## Six seats were retired on 2026-09-01

Their playbooks stay in `roles/retired/` as the record of what each seat did. **A document that
routes work through one is stale.**

| Retired seat | What replaced it |
|---|---|
| Dispatcher | The Console. It reads the record, picks the work and spawns a Builder. |
| Liaison | The Console, which is the only seat the Owner talks to. |
| PM | Nothing, by Owner decision. |
| Cleaner | Nothing, by Owner decision. |
| Role manager | Nothing, by Owner decision. |
| Process improvement | Nothing, by Owner decision. |

A retired label resolves to no card **and says it was retired**, with the reason. Silence alone
would send a reader hunting for a card somebody deliberately removed.

One playbook sits in `roles/retired/` without a matching entry in the roster: the ASVS tracker. That
label resolves to silence rather than to a retirement notice.

---

## `roles/README.md` agrees with the roster, and this page said it did not

**RETIRED 2026-09-08, on the first day this page existed.** It read: "It came across from a private
vault, and it still lists every seat in the table above as live." That is false, and this page
carried it because CLAUDE.md says it and nobody re-read the file.

Measured at `9658940`: `roles/README.md:22` retires all seven seats in bold, naming each one, and
line 26 says not to route work to a retired seat or read a retired row as live. Its section 1a
lists the same seven live seats as the table above, and 1b lists the retired files.

Control, same file: `wc -l roles/README.md` returns 237, so the grep read a real document rather
than an empty one.

CLAUDE.md's seat table still governs, for the ordinary reason that one file has to. The claim that
`roles/README.md` contradicts it is retired.

Two files in `roles/` are holding pens rather than playbooks. `COMMON-STAGED.md` and
`LANDER-ROUTED-OUT.md` were split out on 2026-09-05 and are unedited. Each block in them needs a
destination the Owner has not chosen yet.

---

## Naming a playbook to a session

Nothing delivers a playbook. Say which file to read, in the first message:

```text
You are the Lander. Read roles/COMMON.md, then roles/LANDER.md, before anything else.
```

A [role card](ROLE-CARDS.md) removes the part of this that a compaction eats. It does not remove
the playbook, which stays the long form the card points at.

---

## Related

[Seats and worktrees](SEATS-AND-WORKTREES.md) has how a seat reaches a session.
[Role cards](ROLE-CARDS.md) has the card format and the design record.
[Run a KORUS build](KORUS-BUILD.md) has the shape a build runs in.
[Worker brief](WORKER-BRIEF.md) has what to put in the opening prompt.
