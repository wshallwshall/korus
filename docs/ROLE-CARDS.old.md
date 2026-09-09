# Role cards: giving a worktree a seat that outlives its session

## TLDR/BLUF

**What this is.** A one-word marker in a worktree, one card per seat, and a `SessionStart` hook
that injects the right card. The seat then belongs to the worktree instead of to the session that
was told it.

**Why you should care.** A session is told its seat in its first message. That instruction is an
ordinary user turn, so it competes with everything else and it does not survive a compaction. The
rules go quiet exactly when a long session needs them.

Not for you if one session ever works here at a time.

**How to use it.** Set the marker once per worktree. Everything else follows.

```powershell
Set-Content .claude\seat.local.txt 'builder'
```

---

## The four pieces

| Piece | Where | What it does |
|---|---|---|
| The marker | `.claude/seat.local.txt` | Holds one lowercase word. Git-ignored. |
| The cards | `docs/roles/<seat>.card.md` | One per live seat. Capped at 150 lines and 6 KB. |
| The roster | `docs/roles/seats.json` | Live seats, the alias map, and the retired seats with reasons. |
| The hook | `scripts/hooks/role-card-inject.ps1` | Resolves the seat, injects that card, writes a re-readable copy. |

The marker belongs to the worktree, not to a session. Sessions come and go inside a worktree. The
marker survives a crash, a compaction, an account switch and a respawn.

## Why the marker is named `seat.local.txt`

This repository's ignore rules are unusual, and they are the reason.

`.gitignore` states at the top of the file that `.claude/` is **deliberately not ignored**. Anything
tracked under it must carry `.example.` in its name. Machine-local files are ignored by `*.local.*`
instead.

Measured with `git check-ignore -v`:

| Path | Ignored? |
|---|---|
| `.claude/seat` | **No.** It would show as untracked. |
| `.claude/seat.local` | **No.** `*.local.*` needs a segment after `.local.` |
| `.claude/seat.local.txt` | Yes, by `.gitignore:18` |
| `.claude/ROLE.local.md` | Yes, by `.gitignore:18` |

The second row is the near-miss that makes the filename look arbitrary. `TheMarkerCannotRideIntoACommit`
in `tests/test_role_cards.py` pins all four.

**Check your own repository before copying any of these paths.** A sibling project ignores
`.claude/**` and tracks `CLAUDE.local.md`, which is the exact inverse, so a path lifted from it
would be untracked here and could ride into a commit on a blanket stage.

## Resolution order, and why it ends in silence

1. `.claude/seat.local.txt` in the worktree root.
2. `$env:KORUS_SEAT`.
3. Nothing. No card, and the hook prints the one command that sets a marker.

**No rung reads a branch or directory name.** That is the obvious fourth rung and it is a trap.

A worktree name is a creation-time label that nothing keeps current. This repository has one right
now whose name describes a question its session answered in the first two minutes.

A card is injected at the weight of the working agreement, so a wrong card outranks the document
the session should have been reading. Silence costs one printed line. A wrong card costs a session
that confidently follows another seat's rules.

Two tests pin the silence. One runs the hook from a directory named `claude/lander-x` and asserts
no card. The other reads the hook's source and fails if `rev-parse`, `symbolic-ref` or `git branch`
ever appears in it.

## The hook never fails a turn

Every path exits 0, as the other hooks here do. A missing roster, an unknown label, an oversized
card and an unwritable copy each produce a note and a zero.

A hook that can break a session is a worse fault than an undeclared seat, and this one runs in
every worktree.

## The roster comes from CLAUDE.md, not from `roles/README.md`

Seven seats are live: Console, Manager, Builder, Reviewer, Regulator, Steward and Lander.

`roles/README.md` came across from a private vault. It still lists Dispatcher, PM, Liaison,
Cleaner, Role manager and Process improvement as live, and it describes itself as a partial list.

CLAUDE.md's seat table governs, and it says so in the table's own note. A test fails if the two
rosters drift apart.

A retired label resolves to no card **and says it was retired**, with the reason. Silence alone
would send a reader looking for a card that was deliberately removed.

## Why the alias map exists

A sibling project counted 46 distinct role strings against a six-seat roster. Eight were spellings
of one seat, because several sessions hold the same seat at once and a number was appended to tell
them apart.

No instrument can group by seat when the seat has eight names. The map collapses them, and an
unmapped string resolves to nothing.

## What a card carries, and what it must not

Every card has the same five sections: what the seat owns, what it must not do, its authority, what
it checks on arrival, and where the full playbook is.

**A card carries nothing that expires.** Live state -- open queues, item numbers, who is blocked on
whom -- belongs in a dated note.

That rule is not theoretical. A seat folder elsewhere paid for it twice: a standing "do not
install" instruction inverted when the held fix merged, and a freeze was cited twice as authority
after it had lapsed.

The 150-line and 6 KB caps are enforced in the tests and re-checked by the hook, so a card edited
in a worktree that never ran the suite cannot quietly cost every session on the machine.

## The leak half is not decoration

These cards derive from playbooks that came out of a private vault. That transfer has already put
six user-home paths and two private artifact URLs into this public tree, past a gate that returned
zero both times.

So the suite scans every card for artifact URLs, bare UUIDs and user-home paths, and **each scan is
paired with a planted control that must fire**. A pattern that matches nothing would otherwise pass
in silence, which is how the six paths arrived.

`scripts/security/scan_forbidden.py` still has no artifact-URL pattern. That gap is filed
separately and is not closed by this change.

## What this does not do

- **It does not make a session obey.** It makes the rules present.
- **It does not replace a seat declaration.** The marker carries the role, which a machine can
  write. It does not carry the goal, which no machine can.
- **It does not compete with a nested `CLAUDE.md`.** Those scope by directory. A Builder and a
  Reviewer editing one folder need different rules, so directory scoping cannot carry a seat.
- **It changes no section of `CLAUDE.md`.**

## Rollout

The hook is wired in `.claude/settings.example.json`, which is inert by construction: the harness
loads `settings.json` and `settings.local.json` only.

So a checkout picks this up when someone copies the example into a real settings file. There is no
backfill, and an unwired worktree behaves exactly as it did before.

## The one thing still unproven

Whether a hook wired in a project's **own** `.claude/settings.json` can emit
`hookSpecificOutput.additionalContext`, or only plain stdout.

The distinction decides whether a card renders at full working-agreement weight or as hook output.

**This repository does not settle it, and a partial answer reads like a whole one.** Every hook
here that emits `additionalContext` is a `PreToolUse` hook:

| Hook | Event | Output shape |
|---|---|---|
| `scripts/hooks/collision_gate.ps1` | `PreToolUse` | `additionalContext` |
| `scripts/hooks/steer-inject.ps1` | `PreToolUse` | `additionalContext` |
| `scripts/hooks/block-blanket-git-stage.ps1` | `PreToolUse` | `additionalContext` |
| `scripts/worktree/session-context.ps1` | `SessionStart` | plain stdout, line 226 |

So `PreToolUse` is proven here and `SessionStart` is untested. This hook writes plain stdout, which is
the shape this repository has actually exercised at that event.

The probe is cheap: one hook, one distinctive token, one fresh session.

## Verification actually run

Test-driven. The tests were written first and watched fail: **23 failed, 16 passed** before any of
the code existed. The 16 that passed at red were the git-ignore assertions and the CLAUDE.md roster
checks, which correctly held already and must keep holding.

| Check | Result |
|---|---|
| `pytest tests/test_role_cards.py` | 39 passed, 12 subtests passed |
| ASCII gate, CI invocation | exit 0 |
| Hook run by hand, marker set | exit 0, card injected |

**A caution about the prose gate.** It scans `docs/`, `README*` and `INSTALL*` only. `CLAUDE.md`
and everything under `roles/` sit outside that corpus, which was measured by planting a banned
construction in `CLAUDE.md` and watching the gate stay green. This page is inside it.
