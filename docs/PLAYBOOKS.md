# The playbooks

<a id="tldrbluf"></a>

KORUS keeps short cards and full playbooks for its roles. Name the current playbook in the
session's opening prompt.

The roster changed on 2026-09-01, when six seats retired. Older instructions may still route work to
them.

The site serves the cards. Open the full playbooks in your checkout; nothing delivers them to a
session automatically.

---

## Use the Manager for new builds

Read `roles/COMMON.md` before your seat's playbook. It holds the rules shared by all seats.

| Seat | What it owns | Card | Playbook |
|---|---|---|---|
| Console (former design) | Broad oversight did not work. The Manager replaced it; this card remains for reference. | [Console](roles/console.card.md) | `roles/CONSOLE.md` |
| Manager | Runs one or more Builders as subagents or separate sessions. Writes their briefs and reads their results. | [Manager](roles/manager.card.md) | `roles/MANAGER.md` |
| Builder | One brief, one turn. Commits, opens the pull request, exits. | [Builder](roles/builder.card.md) | `roles/BUILDER.md` |
| Reviewer | Reads the diff and posts findings on the pull request. | [Reviewer](roles/reviewer.card.md) | `roles/REVIEWER.md` |
| Regulator | Decides whose failure a red check is. | [Regulator](roles/regulator.card.md) | `roles/REGULATOR.md` |
| Steward | A cron rather than a seat. Reads usage and names the account with headroom. | [Steward](roles/steward.card.md) | `roles/STEWARD.md` |
| Lander | What enters the merge queue, and in what order. | [Lander](roles/lander.card.md) | `roles/LANDER.md` |

Cards live under `docs/`, which Jekyll builds into this site. Playbooks live at the repository root,
outside Jekyll's source directory, so this host has no page for them.

---

## The card is a summary and the playbook governs

A card holds the seat's scope, prohibitions, authority, arrival checks, and playbook path. Each card
has a 150-line and 6 KB cap.

Put open queues, item numbers, and blockers in dated notes. Keep them out of both cards and
playbooks.

A seat folder elsewhere failed this twice. In one case, a standing instruction became wrong after
the fix it awaited merged.

[Seats and worktrees](SEATS-AND-WORKTREES.md) covers how a card reaches a session.

---

## Six seats were retired on 2026-09-01

Retired playbooks remain in `roles/retired/` as a record. Instructions that route work through those
seats are stale.

| Retired seat | What replaced it |
|---|---|
| Dispatcher | The Console first replaced this seat. Use the Manager now. |
| Liaison | The Console first replaced this seat. The Owner now talks to the Manager. |
| PM | Nothing, by Owner decision. |
| Cleaner | Nothing, by Owner decision. |
| Role manager | Nothing, by Owner decision. |
| Process improvement | Nothing, by Owner decision. |

A retired label returns no card and prints its retirement reason. This tells readers the missing
card was removed on purpose.

The ASVS tracker has a playbook in `roles/retired/` but no roster entry. Its label returns nothing,
including no retirement notice.

---

## `roles/README.md` agrees with the roster, and this page said it did not

RETIRED 2026-09-08, the day this page first appeared: "It came across from a private vault, and it
still lists every seat in the table above as live."

That claim was false. This page copied it from CLAUDE.md without checking the file.

At `9658940`, `roles/README.md:22` names all seven retired seats in bold. Line 26 says not to route
work to them or read retired rows as live.

Section 1a lists the same seven live seats as this page. Section 1b lists the retired files.

As a control, `wc -l roles/README.md` returned 237. The search read a real document, not an empty
file.

CLAUDE.md's seat table remains the governing roster. We retire the claim that `roles/README.md`
contradicts it.

`COMMON-STAGED.md` and `LANDER-ROUTED-OUT.md` hold material awaiting a destination. They were split
out on 2026-09-05 and remain unedited.

The Owner has not yet chosen where each block belongs.

---

## Naming a playbook to a session

Name the full playbook in the first message:

```text
You are the Lander. Read roles/COMMON.md, then roles/LANDER.md, before anything else.
```

A [role card](ROLE-CARDS.md) keeps the seat's core rules available after compaction. The session still needs the full
playbook it points to.

---

## Related

[Seats and worktrees](SEATS-AND-WORKTREES.md) has how a seat reaches a session. [Role cards](ROLE-CARDS.md) has the card format and the design record.
[Run a KORUS build](KORUS-BUILD.md) has the shape a build runs in. [Worker brief](WORKER-BRIEF.md) has what to put in the opening prompt.

The [handoff diagram](KORUS-BUILD.md#g04) shows how work moves between the build roles.
