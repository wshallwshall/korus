# Quickstart

## TLDR/BLUF

**What this is.** The install, start to finish, and then two sessions that refuse to overwrite each
other. Eight steps, run from a plain terminal, against a repository you already have.

**Why you should care.** Step 8 is the point: you make two sessions edit one file, and watch the
second one get refused. Until you have seen that refusal, nothing here is proven to be running. Not
for you if you have no repository to govern yet.

**How to use it.** Work the steps in order. KORUS assumes Claude Code for Desktop throughout, so
check [Limits and requirements](LIMITS.md) before you start if you are not on it.

---

## What you need

Claude Code for Desktop, `pwsh` 7.3 or newer, `git`, and a `python` on `PATH`. The full table, and
what breaks when each is missing, is on [Limits and requirements](LIMITS.md).

Every command below runs in a **plain terminal**, not inside a Claude Code session. All four
installers refuse when `$env:CLAUDECODE` is `1`, because a session that can install these controls
can remove them.

## 1. Get the tooling

```powershell
git clone https://github.com/wshallwshall/claude-multisession.git
```

**Pin it rather than tracking `main`.** This repository runs concurrent sessions against itself, so
`main` moves. Check out a commit you have read, and upgrade deliberately.

**If you cannot reach GitHub**, you are the reader this site was moved for, and there is no clone.

Every file is served here at its own path, so the fallback is to fetch the paths listed on
[Every script](SCRIPTS.md) into a directory of your own. One example:
[/scripts/coord/claim.ps1](https://claude-multisession.pages.dev/scripts/coord/claim.ps1)

## 2. Name the two directories

Every command says which directory it means, because the installers refuse to guess.

| | |
|---|---|
| **tooling** | This checkout. Nothing you install governs it. Scripts are copied from here and hashed against it. |
| **target** | The repository you want governed. It gets the config file, the git hooks, and its primary checkout in the gate's allowlist. |

```powershell
$tooling = "<path-to-this-checkout>"
$target  = "<path-to-the-repo-you-want-governed>"
Set-Location $target      # the doctor reports what it resolves FROM HERE, so stand in the target
```

## 3. Vendor the tooling into the target

Copy the scripts into the target and commit them, so tooling *is* target. That is the only layout in
which the doctor can reach exit 0.

```powershell
Copy-Item "$tooling/ccx.config.json" "$target/ccx.config.json"
Copy-Item "$tooling/scripts" $target -Recurse -Force
Copy-Item "$tooling/bin" $target -Recurse -Force
```

`-Force` is not optional. Without it, a target that already has a `scripts/` or `bin/` prints one
red error per existing directory, ten of them on a re-run, while still copying the files.

These two lines merge into what is there rather than replacing it. Re-running them is how you
upgrade.

Then commit them, so every worktree of the target gets them.

**Now edit `ccx.config.json`, because two keys in the shipped file will bite you.**

- `setupHook` points at `.ccx/worktree-setup.ps1`. No such file ships. Leave it and every spawn warns
  that the worktree has NOT been set up. Delete the key, or write the hook
  (`examples/worktree-setup.ps1.example` is the model, and [Worktrees](WORKTREES.md) has the
  contract).
- `sequences` declares an `adr` sequence. Leave it on a repository that numbers nothing and the
  doctor prints an `OFF (opt-in)` row for a gate no installer wires.

**Trap.** After vendoring there are two copies on disk. Install and audit from **one** of them.
Installing from one and hashing against the other is exactly the drift the doctor calls `STALE`.

The separate-checkouts layout works for the worktree gate, both git hooks and the backstop. It fails
for the three coordination hooks: they resolve their script inside whatever repository the session
runs in, so a target without those files gets three wired hooks that resolve nothing.

## 4. Baseline the doctor before installing anything

```powershell
pwsh -NoProfile -File "$tooling/bin/ccx-doctor.ps1" -Repo $target
```

Expect a wall of `OFF` and exit 1. **That is the correct result.** It is the only way to tell an
installed guardrail from a decorative one afterwards.

## 5. Install the four controls

They are four rather than one because they write to genuinely different places.

```powershell
# Coordination hooks: session banner, collision gate, announce. Takes NO repository -- it writes
# ONE settings file whose hooks resolve their repo per session at run time.
pwsh -NoProfile -File "$tooling/scripts/coord/install-coordination.ps1"

# The commit-msg claim gate and pre-push guard, into the TARGET clone's shared .git/hooks, where
# one copy governs every worktree of that clone at once.
pwsh -NoProfile -File "$tooling/scripts/coord/install-git-hooks.ps1" -RepoRoot $target

# The worktree gate. -Repo names the PRIMARY checkout to allowlist. It REPLACES the allowlist,
# so name every governed primary in one run -- and that needs -Command, not -File. See INSTALL.md.
pwsh -NoProfile -File "$tooling/scripts/worktree/install-gate.ps1" -Repo $target

# The SessionStart backstop. ONE config root per run -- run it again for each root the doctor
# lists under "config roots". An unwired root is OFF, and OFF is exit 1.
pwsh -NoProfile -File "$tooling/scripts/worktree/install-selfheal.ps1" -ConfigDir ~/.claude
```

## 6. Prove the install landed on the right repository

```powershell
pwsh -NoProfile -File "$tooling/bin/ccx-doctor.ps1" -Repo $target
```

The doctor's default target is the current directory, so a run started in the wrong place produces a
long, plausible, mostly-green report about the wrong clone. These two lines say which clone it read:

```powershell
pwsh -NoProfile -File "$tooling/bin/ccx-doctor.ps1" -Repo $target |
    Select-String 'repo examined|tooling checkout'
```

**Expect two `OFF (opt-in)` rows even on a good install.** The ASCII gate, which no installer wires,
and the sequence gate if you left `sequences` in the config. Neither raises the exit code, which is
the one place `OFF` is not exit 1.

The sequence one is a real hole rather than a formality: nothing at commit time defends the numbers
you allocate. [Sequence allocation](SEQUENCE-ALLOC.md) has the hook to wire.

## 7. Spawn two sessions

```powershell
pwsh -NoProfile -File "$tooling/scripts/worktree/spawn.ps1" -Name alerts
pwsh -NoProfile -File "$tooling/scripts/worktree/spawn.ps1" -Name parser
```

Each call creates an isolated worktree on its own branch, named after `-Name`.

It then opens an editor window **if** one is found: `-Editor`, else `$CCX_EDITOR`, else `$EDITOR`,
else `code`. With none of them on `PATH` it warns and prints the worktree path for you to open
yourself. `new.ps1` skips the editor entirely.

Neither takes a target flag: both act on the primary you are standing in, so stay in the target.

You may also see a warning that `setupHook` was not found. That is the config key from step 3, and
it does not affect the drill below.

Start a session in each worktree, then confirm they can see each other:

```powershell
pwsh -NoProfile -File "$tooling/scripts/coord/presence.ps1"
pwsh -NoProfile -File "$tooling/scripts/coord/overlap.ps1"
$LASTEXITCODE
```

**Read the exit code, not the rows.** `0` is a complete roster, including one that lists nobody. `2`
is a roster that could not be completed -- and it fires even when rows *are* listed, because two
named peers say nothing about a third.

## 8. Watch a collision get refused

**The goal.** Prove the collision gate is live rather than merely installed.

**What to do.** In session `parser`, ask it to edit a file and leave the change uncommitted. Then in
session `alerts`, ask it to edit the same file.

**What happens next.** The second edit never runs. The tool call is refused, and Claude is handed
this:

<!-- no-copy -->
```text
service.py has UNCOMMITTED changes in another LIVE session's worktree -- editing it now means one of you loses work at merge.

  4f2a1c9b (desktop) in myrepo-parser [parser]
      building: the CSV column parser

Before overriding: that session may already be doing what you are about to do.
  see everything in flight :  pwsh -NoProfile -File scripts/coord/overlap.ps1
  who is live              :  pwsh -NoProfile -File scripts/coord/presence.ps1
If you genuinely need this file, coordinate first -- or edit a different one.
```

Read the peer line by its shape: an 8-character session id, the surface, the worktree's directory
name, and its branch. The branch is `parser` because `spawn.ps1 -Name parser` names both. The
`building:` line appears only when that peer has a task list to report.

That refusal is the whole product. Everything else on this site exists to widen it or to prove it is
still there.

**What it will not do.** The gate refuses on an *uncommitted* edit in a *live* worktree. A peer that
committed its change and went clean is reported and allowed, because that work may overlap yours and
is not worth refusing over. [Coordination](COORDINATION.md) owns the full rule.

## What you have now

Four controls, and each one covers a failure the others do not:

| Control | Refuses |
|---|---|
| Worktree gate | A write into the shared primary checkout, and the git verbs that swap its tree |
| Collision gate | An edit to a file a live session has uncommitted changes in |
| `commit-msg` claim gate | A commit whose subject claims work this worktree does not hold |
| `pre-push` guard | A direct push to a protected ref |

## A seat's standing rules live in `roles/`, and nothing delivers them

Each seat named on [Run a KORUS build](KORUS-BUILD.md) has a **playbook**: a durable file it reads
on arrival. Those files sit at the repository root, not under `docs/`, and this site serves them.

**Start at [roles/README.md](https://claude-multisession.pages.dev/roles/README.md).** It defines
what a playbook is, and its section 1a is the seat-to-file table.

**This page carries no copy of that table on purpose.** A moving set gets one snapshot, and that
is the one.

Nothing routes a playbook to the session that needs it, for the reason
[Run a KORUS build](KORUS-BUILD.md) gives. So name the file yourself, in the opening prompt:

```text
You are the Builder. Read roles/COMMON.md, then roles/BUILDER.md, before anything else.
```

### The playbook corpus drifts, and nothing here fixes that

A pointer is worth less when what it points at disagrees with itself. **This is a known unsolved
problem.** No script reconciles the copies, and no check reports the drift.

| Measured 2026-09-04 | Reading |
|---|---|
| Editions of `roles/` on the machine this was written on | At least 2 -- this repository, and a separate private vault |
| Filenames the two editions share | 13, and **all 13 differ in content** |
| Filenames in only one edition | 2 here, 1 in the vault |
| Vault worktrees carrying a `roles/` copy | 62, excluding the primary |
| Copies among those differing from the vault's own working tree | 607, against 35 that matched |
| Registered vault worktrees safe to remove | 10 of 79 |

**The last two rows count different populations, so do not read them as one fraction.** The 607
copies sit in the 62 worktrees that carry `roles/`. The 10 are counted over all 79 registered
worktrees, most of which carry no playbook at all.

The two instruments, both run to produce the rows above:

```powershell
# Two editions, compared by filename and by content hash.
$k = Get-ChildItem <this-checkout>/roles -Recurse -Filter *.md -File
$v = Get-ChildItem <vault>/roles -Recurse -Filter *.md -File
($k | Where-Object { $n = $_.Name
    ($h = $v | Where-Object Name -eq $n) -and
    (Get-FileHash $_.FullName).Hash -ne (Get-FileHash $h[0].FullName).Hash }).Count
```

```powershell
# Worktree copies, hashed against the vault's own working tree.
Set-Location <vault>
$primary = (git worktree list --porcelain | Select-String '^worktree ' |
    Select-Object -First 1) -replace '^worktree ',''
$dirs = (git worktree list --porcelain | Select-String '^worktree ') -replace '^worktree ','' |
    Where-Object { $_ -ne $primary -and (Test-Path "$_/roles") }
$stale = 0
foreach ($d in $dirs) {
  foreach ($f in Get-ChildItem "$d/roles" -Filter *.md -File) {
    $p = Join-Path "$primary/roles" $f.Name
    if ((Test-Path $p) -and (Get-FileHash $f.FullName).Hash -ne (Get-FileHash $p).Hash) { $stale++ }
  }
}
"$($dirs.Count) worktrees, $stale stale copies"
```

Removal safety was classified separately: a worktree is safe only when `git merge-base
--is-ancestor <tip> origin/main` succeeds **and** `git diff origin/main...<tip> --name-only` returns
nothing.

**What none of it varied.** Every comparison read **working trees**, never either repository's
`origin/main`. So a worktree sitting on a legitimately newer branch is counted as stale here. Line
endings were varied and changed nothing: the 13 shared files still differ with `\r` stripped.

**These rows are what the rule in `roles/README.md` costs when nobody holds it.** The measurement
expires the day a check reports two copies disagreeing.

## Next

**Give the sessions a working agreement.** Copy
[CLAUDE.md.template](https://claude-multisession.pages.dev/CLAUDE.md.template)
into the target as `CLAUDE.md` and cut it to what is true there. It is where you write down what the
gates cannot see. Keep it short: a stale one still gets acted on.

**Then scale up.** [Run a KORUS build](KORUS-BUILD.md) is the session shape this all exists to
support: a console, a builder per task, a reviewer per pull request, and a lander.

[INSTALL.md](INSTALL.md) is the record of record for the
installers: the annotated version of these steps, and how to prove each one is live rather than
merely merged.
