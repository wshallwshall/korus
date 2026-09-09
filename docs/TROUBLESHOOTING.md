# Troubleshooting

## TLDR/BLUF

Run `bin/ccx-doctor.ps1` to check the installed controls, then match its result or your symptom
below.

Broken and working controls often produce identical output: both can allow an edit silently. If you
have not installed anything, start with [Quickstart](QUICKSTART.md).

From a plain terminal, run the doctor with the repository you want to check:

```powershell
pwsh -NoProfile -File <tooling>/bin/ccx-doctor.ps1 -Repo <the-repo-you-govern>
```

The doctor leaves your repository untouched. Its attack tests use temporary, disposable fixtures.

---

## Symptoms

| Symptom | What it actually is | What to do |
|---|---|---|
| The doctor says `STALE` | The installed copy's SHA-256 differs from this checkout's source. The code that runs is not the code you are reading. Reported `RED`. | Re-run that control's installer, from a plain terminal. Install from the same checkout the doctor hashes against, which it prints as `tooling checkout`. |
| The report is about the wrong clone | `-Repo` defaults to the directory you ran it from. Sources are hashed from the doctor's own checkout whatever `-Repo` says. | Pass `-Repo <target>`. Then read `repo examined` and `tooling checkout` under `WHAT WAS SCANNED`; both are printed for this reason. |
| The doctor exits 2 | At least one check could not be determined, and nothing was proven broken. A skip is never a pass. | Read the `undetermined` lines in the verdict. `-SkipAttacks` produces this on its own, because nothing was fired. |
| A control shows `OFF` | It is implemented and nothing invokes it. Zero enforcement, which from inside a session looks like a healthy control with nothing to say. | Install or wire it. A required `OFF` drives exit 1; an opt-in one is counted separately as `OFF (opt-in)` and does not. |
| The collision gate did not refuse an edit | Most often it is one of its documented blind spots rather than a fault. It cannot see a peer in **your own** worktree, and its map is cached for 60 seconds. | Check the list below before assuming a break. [Limits](LIMITS.md#what-the-collision-gate-does-not-see) has every case. |
| The collision gate says nothing at all, repeatedly | It could not check, and said so once. The notice is throttled per worktree and per reason, 30 minutes by default. | The notice is emitted by the gate itself, not by `overlap.ps1`. Look in your session, not in a terminal. |
| The worktree gate never refuses anything | Most likely its allowlist has no entries. With none it exits 0 having written nothing, which reads exactly like a healthy gate with nothing to refuse. | Count the entries in `~/.claude/hooks/ccx-gate.repos.txt`. Re-run `install-gate.ps1 -Repo <primary>`, naming every governed primary in one run. |
| Announce never delivers | On a plain CLI install there is no MCP server to deliver through. On Desktop, check the `OFF` file and the receipts the hook writes. | Create or remove `<git-common-dir>/<prefix>-coord/announce/OFF`. The doctor cannot see whether the MCP server is connected. |
| Presence lists nobody | Either nobody is live, or the roster could not be completed. Under `-Json` both are the two bytes `[]` on stdout, and the reason goes to stderr. | Read the exit code rather than the rows. `0` is a complete roster, including one that lists nobody. `2` is a roster that could not be completed. |
| Presence exits 2 | The roster could not be completed: not inside a git repository, or `Available` is false. One unplaceable record makes it false. | Treat the output as incomplete even when rows are listed. An unplaceable record could name any worktree, so it clears none of them. |
| The reaper refuses a worktree | `prune-merged.ps1` acts only on merged AND clean AND not occupied. Any check that cannot reach a confident answer skips. Untracked files block it. | Read the printed SKIP reason. Exit 2 means it refused and removed nothing: a `-Name` matching no prunable sibling, a wrong cwd, an unresolvable trunk, or an unavailable fence. |
| Self-heal declines to repair the primary | The primary's tree is dirty. The backstop repairs a drifted primary only when it is clean, and it reports the decline rather than acting. | Commit or stash the work sitting in the primary. A detached HEAD is deliberately not treated as drift, and is a silent no-op. |
| A commit is refused naming a number | The claim gate. The subject declares `<KIND> #N`, the staged diff touches code, and this worktree does not hold the claim on N. | Take the claim first, substituting the real number: `pwsh -NoProfile -File scripts/coord/claim.ps1 -Take 12`. |
| Every commit and every push is refused | `_ccxconfig.py` is absent from the git hooks directory, or will not import. Both Python checkers import it at startup, then exit 1. | Re-run the git-hook installer from a plain terminal: `pwsh -NoProfile -File <tooling>/scripts/coord/install-git-hooks.ps1 -RepoRoot <target>`. |
| No commit or push is ever refused | The opposite failure, and the quiet one. With no `python` on `PATH` the two `/bin/sh` shims print one line to stderr and **exit 0**, so both git gates are off with every file still installed. | Check that `python --version` actually prints. On Windows it is often an execution-alias stub that resolves and runs nothing. |
| A push is refused | The push guard. The ref is in `protectedRefs`, which defaults to `main` and `master`. Deleting a protected ref is refused as well. | Push a branch and open a pull request. An explicitly empty `protectedRefs` disables the guard and announces that on stderr. |
| Sequences are configured and nothing enforces them | No `pre-commit` hook invokes `seq_check.py`. The doctor prints `OFF` on that row and marks it not required, so it does not raise the exit code. | [Sequence allocation](SEQUENCE-ALLOC.md#wiring-the-pre-commit-hook) has the snippet. That row, and the `OFF (opt-in)` line, are where it shows. |

### Why the collision gate stays quiet

A missing refusal can follow from the gate's design. Check these cases, detailed in
[Limits](LIMITS.md#what-the-collision-gate-does-not-see):

- A second session in your own worktree. `overlap.ps1` skips your own worktree before comparing any
  path, so two sessions on one checkout collide in silence.
- A peer who started within the last minute. The overlap map is cached for 60 seconds, and the gate
  never asks for a refresh.
- A peer whose change git cannot report as a path. A new file in a new directory, a rename, or
  anything git-ignored.
- A write by absolute path into another worktree, or through a symlink.
- A peer that committed and went clean. Reported, not refused, on purpose.

### The green run and the real hole

Four optional controls can remain off in a green run: the sequence gate, ASCII gate, blanket-stage
guard, and steering injector. An unwired sequence gate leaves number collisions unchecked.

No shipped installer writes `pre-commit`, since another tool may own it. Requiring that hook would
fail every fresh install.

The doctor therefore reports the sequence gate as `OFF (opt-in)`, without raising the exit code.

With sequences configured but unchecked at commit time, two sessions can use the same number and
merge without conflict. Check the `OFF` row; the exit code does not report this gap.

`scripts/quality/check-ascii.ps1` ships in every checkout, but nothing invokes it by default. Add it
to your `pre-commit` and continuous integration (CI) checks to reject non-ASCII characters.

## Reading the doctor

Each check has a row and a tag:

| Tag | What it licenses |
|---|---|
| `OK` | Installed, wired, and where it could be attacked it refused the case it exists to refuse. |
| `RED` | Proven broken: wired but stale or unloadable, or it allowed what it must deny, or it denied what it must allow. |
| `OFF` | Implemented, and nothing invokes it. Zero enforcement. |
| `??` | Could not be determined. Never read one of these as a pass. |
| `--` | Not applicable here, such as no sequences configured, or an opt-in rule left off on purpose. |

The exit code follows the most severe result:

| Exit | Meaning |
|---|---|
| 0 | Every required control is installed and wired, and every attack it **could** fire was refused. |
| 1 | At least one `RED`, or at least one required control `OFF`. |
| 2 | At least one check could not be determined, and nothing above it fired. |

Exit 0 leaves three controls untested, and the doctor names them each run. It cannot stage the live
peer needed for a collision refusal.

PowerShell cannot prove announce delivery, and the steering injector has no attack test.

Read both the verdict and its blind spots.

### Why a skip is exit 2 rather than a pass

A skipped check cannot distinguish broken controls from working ones. Both can emit identical
output, so the doctor gives an untested control exit 2.

The doctor can also exit 2 before testing, with `CANNOT DETERMINE ANYTHING`. It stops if its
`scripts/coord/_common.ps1` fails to load or the path is outside git.

It also stops if `ccx.config.json` is absent at or above that path, or cannot load. These are the
four early-stop cases.

### `-SkipAttacks` cannot prove enforcement

`-SkipAttacks` replaces the attack set with one `??` row and prevents exit 0. The result is 2, or 1
if receipt checks find something broken or missing.

Receipts show which files exist and which controls the settings invoke. An attack test checks
whether the control refuses a prohibited action.

For an uninstalled control, the doctor tests its source copy and lowers the verdict. That test can
prove the code refuses an action, but no installed hook enforces it.

## When the answer is "cannot tell"

These three results mean the tools could not finish checking:

Presence exit 2 means the roster is incomplete, even when it lists rows. Finding two peers says
nothing about a third the scan could not place.

When overlap cannot resolve, the collision gate allows the edit and reports `could NOT check`: it
consulted no peer worktree. During the cooldown, later edits proceed without another notice.

Liveness checks depend on the client's per-session JSON record format. The client can change that
format independently of this project.

Record changes produce two different symptoms:

| What changed | What you see |
|---|---|
| The directory moved, or records were removed | The census counts go to zero |
| A field was renamed, or `startedAt`'s unit changed | **The counts do not move.** Those records still parse and still place; every verdict simply becomes `UNVERIFIED` |

`UNVERIFIED` vetoes work, so gates keep refusing. An unchanged census alone does not prove that the
record format still matches.

The census and roster-unavailable notice appear only under `WHAT WAS SCANNED`. An unreadable roster
adds no verdict row and changes no exit code; read that block too.

> The rule. Absence of a refusal is not evidence of absence of a peer.

Do not treat silence as proof that no peer exists.

## Related

| For | Read |
|---|---|
| What this needs to run, and where each control stops | [Limits and requirements](LIMITS.md) |
| Every control's event, matcher and fail-open or fail-closed posture | [Hooks](HOOKS.md) |
| Wiring the sequence gate, and why no installer writes `pre-commit` | [Sequence allocation](SEQUENCE-ALLOC.md) |
| The worktree commands, and what removal destroys | [Worktrees](WORKTREES.md) |
| Why a removal is skipped, and how to recover a half-removed worktree | [Pruning worktrees](PRUNING.md) |
| Who is live, what they are touching, and the collision gate's full rule | [Coordination](COORDINATION.md) |
| Installing the controls, and watching one refuse | [Quickstart](QUICKSTART.md) |
| Every installer flag, and how to prove each control is live | [Install](INSTALL.md) |
