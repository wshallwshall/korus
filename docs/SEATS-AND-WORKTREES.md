# Seats and worktrees

## TLDR/BLUF

**What this is.** How a worktree and a role card combine. One isolates the files, the other carries
the rules. Neither alone gives a session a working seat.

**Why you should care.** A new worktree arrives holding every card and no seat. The marker that
picks one is git-ignored, so it never travels. A fresh worktree is silent until you set it.

**How to use it.** Two commands, once per worktree.

```powershell
pwsh -NoProfile -File scripts/worktree/new.ps1 -Name <short-name>
Set-Content .claude\seat.local.txt 'builder'
```

Not for you if one session ever works in this repository at a time.

---

## The two halves solve different failures

| Half | Failure it removes | Where it is documented |
|---|---|---|
| The worktree | Two sessions editing one checkout, each overwriting the other. | [Worktrees](WORKTREES.md) |
| The role card | A session told its seat in a first message that a compaction then drops. | [Role cards](ROLE-CARDS.md) |

Run one without the other and you keep the failure it does not cover. Two worktrees with no markers
give you clean file isolation and two sessions guessing at their rules.

---

## A new worktree has every card and no seat

This is the part that surprises people, and it follows from what git tracks.

| Piece | Tracked? | Reaches a new worktree |
|---|---|---|
| The cards, `docs/roles/*.card.md` | Tracked | Yes |
| The roster, `docs/roles/seats.json` | Tracked | Yes |
| The marker, `.claude/seat.local.txt` | Ignored by `.gitignore:18` | No |
| Live hook wiring, `.claude/settings.json` | Untracked | No |
| Example wiring, `.claude/settings.example.json` | Tracked, and inert | Yes, and does nothing |

Measured with `git check-ignore -v .claude/seat.local.txt`, which names `.gitignore:18` as the rule.

So every worktree can render any card, and none of them picks one. **That is the design, not a
gap.** A marker that travelled would clone one seat into every checkout of the repository.

The example wiring is inert by construction. The harness loads `settings.json` and
`settings.local.json` only, so a tracked example can never become a control that looks installed.

---

## Why the seat belongs to the worktree

A session learns its seat in its first message. That is an ordinary user turn, so it competes with
everything else in the window, and it does not survive a compaction.

The rules go quiet exactly when a long session needs them.

A worktree outlives all of it: a crash, a compaction, an account switch, a respawn. Put the seat
there and the next session in that directory starts where the last one left off.

---

## Resolution never reads a branch or directory name

1. `.claude/seat.local.txt` in the worktree root.
2. `$env:KORUS_SEAT`.
3. Nothing. No card, and one printed line naming the command that sets a marker.

The fourth rung looks obvious and is a trap. A worktree name is a creation-time label that nothing
keeps current. This repository holds one right now whose name describes a question its session
answered in the first two minutes.

A card arrives at the weight of the working agreement, so a wrong card outranks the document the
session should be reading. Silence costs one printed line. A wrong card costs a whole session.

Two tests pin the silence. One runs the hook from a directory named `claude/lander-x` and asserts no
card. The other reads the hook's source and fails if `rev-parse`, `symbolic-ref` or `git branch`
appears in it.

---

## Where the two halves disagree

| State | What happens | The tell |
|---|---|---|
| Worktree, no marker | The session runs on whatever it was told. Correct until the first compaction, then silently not. | The hook prints one line at session start. |
| Marker, but two sessions in one checkout | Both get the right rules and overwrite each other's files. | Nothing reports it. The card cannot see a second session. |
| A copied worktree directory | It carries the source's marker, so two directories claim one seat. | Two sessions answer to the same seat name. |
| A renamed worktree | Nothing changes, because no rung reads the name. | None needed. This one is safe by design. |

The second row is the expensive one. A card makes a session confident about its rules and says
nothing about who else is editing the same files.

---

## What neither half isolates

A worktree gives separate files, a separate branch and a separate index. A card gives separate
rules. Five things stay shared across every worktree of a clone, and
[Worktrees](WORKTREES.md) owns the full table.

The one that bites hardest here: **the assistant's project memory is per machine, not per
worktree.** Last write wins. Reads are fine, and writes need one owner.

Coordination state is shared on purpose, and it outlives the worktree that took a claim. Release on
evidence that the directory is gone and deregistered, never on a timer.

---

## Setting it up

1. Create the worktree.

   ```powershell
   pwsh -NoProfile -File scripts/worktree/new.ps1 -Name <short-name>
   ```

2. Set the marker to one lowercase seat name from
   [`docs/roles/seats.json`](roles/seats.json).

   ```powershell
   Set-Content .claude\seat.local.txt 'builder'
   ```

3. Wire the hook once per checkout, by copying `.claude/settings.example.json` into a real settings
   file. Nothing backfills, and an unwired worktree behaves as it did before.

Check the filename before inventing your own. `*.local.*` needs a segment after `.local.`, so
`.claude/seat.local` would be **tracked** and could ride into a commit on a blanket stage.

---

## What this does not do

- **It does not make a session obey.** It makes the rules present.
- **It does not carry the goal.** The marker holds the role, which a machine can write. What the
  session is for is not something a machine can supply.
- **It does not detect a second session in your checkout.** That is the worktree's job, and only if
  you made one.

---

## Related

[Worktrees](WORKTREES.md) has the commands and the isolation boundary.
[Role cards](ROLE-CARDS.md) has the card format, the alias map and the design record.
[The playbooks](PLAYBOOKS.md) has the seven live seats and the file each one reads.
[Running multiple sessions](RUNNING-MULTIPLE-SESSIONS.md) covers the surfaces and the channels.
