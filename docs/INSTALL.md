# Install

## TLDR/BLUF

Install the four sets of hooks, then check that each installed control works.

Follow the eight [Quickstart](QUICKSTART.md) steps for a first install and a live collision refusal.
Use this reference for installer flags and checks.

You need Claude Code for Desktop, `pwsh` 7.3+, `git`, and `python` on `PATH`. Vendor the scripts
into the governed repository and place `ccx.config.json` at its root.

Three installers write user settings, so their hooks load in every repository on the machine.
Installer 2 writes the governed clone's git hooks.

Each control has its own switch; `ccx.config.json` controls only some behavior. CLI-only and
editor-extension setups are unsupported.

Linux and macOS can run the scripts, but Windows receives the practical testing. See
[Limits and requirements](LIMITS.md) for platform details.

Run the doctor before installing, complete Step 0 and all four installs, then run it again. Confirm
which repository and settings it scanned.

Use [Troubleshooting](TROUBLESHOOTING.md) for `RED`, `OFF`, or `??` results. A good install can
still show two `OFF (opt-in)` rows: ASCII, and sequences when configured.

Those rows do not fail the run. You must [wire the sequence gate](#controls-no-installer-wires)
yourself to prevent duplicate numbers.

Use a plain `pwsh` terminal. All four installers refuse when `$env:CLAUDECODE` is `1`, since a
session able to install controls can also remove them.

`-Status` remains available inside sessions.

---

> Cloning or merging installs no controls. Each control needs an installer to copy its files or
> write the settings that invoke it.

An uninstalled control may cause no visible error. A session can still show a banner, per-prompt
status, and green output while its settings look correct.

In the source project, a coordination hook stayed wired for hours while resolving no script. An
unrelated project's similarly named entry occupied its slot.

Another gate had dozens of passing tests against the repository copy. Sessions still ran a stale
installed copy.

---

## Before you start

These requirements affect the installer commands. [Limits and requirements](LIMITS.md) includes the
full platform matrix.

| Requirement | Why | If missing |
|---|---|---|
| Claude Code for Desktop | The coordination layer is shaped around the desktop client | Announce cannot deliver, and the roster is incomplete |
| PowerShell 7.3+ (`pwsh`) | 26 scripts carry `#Requires -Version 7.3` | Three installers refuse. On 7.0-7.2 the backstop still installs -- see below |
| git, recent enough for `rev-parse --path-format=absolute` (2.31+) | Every shim and checker resolves its repository through it | On an older git the shims resolve nothing and stay silent: installed, wired, enforcing nothing. Nothing checks your version |
| A `python` on `PATH` (or `CCX_PYTHON`) | The git hooks installer 2 writes are `/bin/sh` shims that exec a stdlib-only Python checker; the sequence gate and leak gate are Python too | **The installed git gates are OFF** and say so on stderr |
| The scripts vendored into the target | The three coordination shims resolve inside the session's own repository | Those three rows never resolve, and the doctor cannot reach exit 0 |
| `ccx.config.json` at the target repo root | The knob file, and announce's opt-in marker | Announce stays inert there. The other three user-scope controls are unaffected |

`install-selfheal.ps1` requires only PowerShell 7 and never calls git during install. It therefore
installs on 7.0-7.2 or without git, even when the gate installers refuse.

The resulting SessionStart backstop reads an allowlist with two comment lines and no entries. Only
`install-gate.ps1`, which needs 7.3, adds entries.

The backstop stays inactive until someone copies entries from a 7.3 machine. It can then run
unattended `git checkout` commands on the shared primary.

The PowerShell 7 scripts target Windows first. The portable pieces use only Python's standard
library: `scripts/hooks/` checkers and `scripts/security/scan_forbidden.py`.

[Hooks](HOOKS.md) maps each checker to its git event.

Linux runs in CI with two known limits. Off Windows, the doctor reports reduced roster self-marking
and path comparison without case-folding.

---

## Step 0 -- opt in

User-scope hooks load in every repository on the machine. Each control has its own way to identify
repositories that enabled it.

```powershell
# from the repo you want to govern
Copy-Item <path-to-this-checkout>/ccx.config.json ./ccx.config.json
```

Set `trunk`, `worktreeLayout`, `protectedRefs`, and optional `sequences` for your repository.
`CCX_CONFIG` can move the config lookup.

Announce checks for the config file itself. Script presence would wrongly include half-installs and
exclude setups storing scripts elsewhere.

### What this file actually bounds, and what it does not

Deleting `ccx.config.json` stops announce and resets the knobs to their defaults. Four other
controls remain active, including two that act on the shared checkout.

Without config at or above the target path, the doctor prints `CANNOT DETERMINE ANYTHING`. It exits
2 before checking any control.

| Control | Bounded by | Reads `ccx.config.json`? |
|---|---|---|
| Announce (`UserPromptSubmit`) | This file, at the repository root | Yes. This is its opt-in |
| Collision gate (`PreToolUse`, denies) | Its script resolving inside your repo | No |
| Session banner (`SessionStart`) | Its script resolving inside your repo | No |
| Worktree gate (`PreToolUse`, denies) | The shared allowlist | No |
| SessionStart backstop (runs `git checkout`) | The same allowlist | Only for the `prefix` knob |

Delete the shared allowlist to disable the last two controls everywhere at once. See
[Limits and requirements](LIMITS.md#what-actually-switches-each-control-on).

Announce checks only the repository root; the backstop checks only the governed root. Checkers, the
doctor, and worktree scripts search upward from the current directory.

A config above the root satisfies the upward-searching tools but leaves the first group inactive.
Only that second group honors `CCX_CONFIG`; announce ignores it.

Installers 3 and 4 never check for config, so silence proves nothing about its presence. Installer 2
checks the governed clone and prints its `NOTE` about that target.

Installer 1 checks its own checkout, which always includes config, so the install-path NOTE never
appears. Its `-Status` checks the current directory instead.

---

## The four installers at a glance

| Installer | Scope | Writes | Governs |
|---|---|---|---|
| `scripts/coord/install-coordination.ps1` | User -- **one** settings file per run (`~/.claude/settings.json` unless `-SettingsPath` moves it) | Three hook rows, each a **shim** that re-resolves at run time, plus a receipt | Session banner, collision gate, announce -- in every worktree, for sessions that read that file |
| `scripts/coord/install-git-hooks.ps1` | Clone (`<git-common-dir>/hooks`, or `core.hooksPath`) | `commit-msg` + `pre-push` shims, **copies** of the Python checkers and their substrate, plus a receipt | Every worktree of that one clone, immediately |
| `scripts/worktree/install-gate.ps1` | User, **every** config root it finds | A **copy** of the gate outside every working tree, one shared allowlist, `PreToolUse` rows per rule | The primary checkouts named in the allowlist |
| `scripts/worktree/install-selfheal.ps1` | User, **one** config root per run | A copy of the SessionStart backstop beside the gate, plus that root's wiring | Whatever the gate's allowlist already names -- it has no target of its own |

---

## Which repository each installer governs

Installing into the wrong clone can still produce a receipt, green status, and a mostly green doctor
report. Confirm which of these two directories each command uses:

- the tooling checkout, which is where scripts are *copied from* and hashed against, and
- the target, the clone or checkout that is *governed*.

| Installer | What its target actually is | With no flag | Name it with | When it cannot tell |
|---|---|---|---|---|
| `install-coordination.ps1` | A settings **file**. It resolves no repository at all -- each shim resolves one per session, at run time, from that session's own directory | `~/.claude/settings.json` | `-SettingsPath <file>`, once per config root your client reads | Not applicable: nothing here is repository-keyed |
| `install-git-hooks.ps1` | A **clone**. Its git common directory is where `commit-msg` and `pre-push` land | The clone you are standing in | `-RepoRoot <path>`. `-HooksDir <path>` overrides the derived directory, for a layout neither `core.hooksPath` nor the common dir covers | **Refuses.** If the clone you are standing in is not the one this script ships from, it stops and prints both, with the `-RepoRoot` line to re-run |
| `install-gate.ps1` | **Primary checkouts**, written into the shared allowlist | The primary of the clone you are standing in | `-Repo <path>`. **Pass every governed primary at once**: `-Repo <path-a>,<path-b>`. `-ConfigDir` selects which config roots get wired | **Refuses**, the same way, naming both primaries |
| `install-selfheal.ps1` | A **config root** only. What it repairs is whatever the gate's allowlist names | Nothing -- `-ConfigDir` is mandatory | `-ConfigDir <path>` (required), `-HookPath <path>` for the shared script copy | It cannot: with no allowlist entries it installs and reports itself inert |
| `bin/ccx-doctor.ps1` | The repository the whole report is **about** | The current directory's repository | `-Repo <path>`, plus `-ConfigDir` and `-SettingsPath` for the wiring it reads | It cannot refuse -- it is a report. So it prints `repo examined` and `tooling checkout` on every run and says outright when they are the same clone |

Keep these scope rules in mind:

- The checkers, the gate and the backstop are always copied from the tooling checkout, never from
  the target. A governed repository is not expected to vendor any of these files, so
  `-RepoRoot <your-repo>` does not send the installer looking in `<your-repo>/scripts/hooks/` for
  sources.
- `install-git-hooks.ps1` resolves its clone before every mode. `-Status` and `-Uninstall` use
  the same `-RepoRoot` and refusal rules to avoid changing or auditing the wrong clone. `install-gate.ps1` is the opposite, deliberately: no `-Repo` at all.
- `install-gate.ps1` REPLACES the allowlist, it does not add to it. The file is rewritten from this
  run's `-Repo` values. Running it for a second repository alone removes the first. The gate and backstop immediately
  stop protecting that first repository in every session.

Use `-Command` to pass two repositories. With `pwsh -File`, `-Repo <a>,<b>` arrives as one literal
string and fails at `Resolve-Path`:

```powershell
pwsh -NoProfile -Command "& '<tooling>/scripts/worktree/install-gate.ps1' -Repo '<path-a>','<path-b>'"
```

After every install, run the doctor with an explicit `-Repo`. Confirm `repo examined` before
relying on the report.

### Shim or copy -- the trade you are making

The coordination installer writes shims that locate and run scripts from a checkout. A pull updates
those scripts for every session.

A shim that finds no script may exit silently, producing the same output as a working hook with no
peers.

Announce reports a missing script when `ccx.config.json` shows the repository opted in. The banner
and collision shims print no such notice.

The gate and git-hook installers copy scripts outside working trees so they survive branch changes.
Scripts kept inside a checkout can disappear on detached HEAD or older commits.

A missing hook script silently lets the tool call proceed.

Copies can drift: installing stale source downgrades every worktree's live gate while all files
still appear installed. Check receipts to detect both stale copies and unresolved shims.

---

## Why user scope, and not the project's `.claude/`

Project `.claude/` settings are usually git-ignored, so git cannot deliver them to worktrees.
Existing copies can stay at their creation-time version.

Tracked settings also belong to one branch until another worktree merges them.

In the source project, more than half the worktrees lacked project settings. One live editor session
had no coordination context: it could neither see peers nor be seen.

User settings load in every worktree on that machine, however it was created. The client combines
user, project, and local hook definitions, retaining each repository's guards.

---

## Installer 1 -- coordination hooks

```powershell
pwsh -NoProfile -File <tooling>/scripts/coord/install-coordination.ps1
```

The installer adds three hook rows to `~/.claude/settings.json`:

| Event | Script | What it does |
|---|---|---|
| `SessionStart` | `scripts/worktree/session-context.ps1` | Who else is live, and what they are building |
| `PreToolUse` (`Edit\|Write\|MultiEdit\|NotebookEdit`) | `scripts/hooks/collision_gate.ps1` | Refuses a file a live session is already changing |
| `UserPromptSubmit` | `scripts/hooks/announce-session.ps1` | Tells peers you exist, and what you intend |

This installer targets a settings file and never resolves a repository. Each shim finds its
repository at runtime from the session directory, so there is no `-Repo` flag.

Each run writes one settings file: `~/.claude/settings.json`, or the path given by `-SettingsPath`
. It saves a backup and receipt beside that file.

Run it once per client config root. The doctor lists discovered roots under `config roots`.

`-Uninstall` also affects one settings file. If you wired two roots, uninstall from both to disable
both.

`-Only <event>` and `-Except <event>` apply to install, uninstall, and `-Status`. Use
`-Only UserPromptSubmit -Uninstall` to remove announce while keeping the collision gate and banner.

The shim tries the primary checkout first so sessions share one coordination protocol. It uses the
calling worktree only as a fallback.

Both locations belong to the session's repository, so only vendored scripts make these three rows
`OK`. See [Quickstart](QUICKSTART.md) for the layout and missing-script behavior.

### Prove it

```powershell
pwsh -NoProfile -File <tooling>/scripts/coord/install-coordination.ps1 -Status
```

Run `-Status` from the repository you want checked. Its `resolves` result uses the current
directory; in a vendored layout, target and tooling checkout coincide.

Check all four lines for each row:

| Line | Answers | Source of truth |
|---|---|---|
| `receipt` | Did an install of this row ever happen here? | The receipt file beside the settings file |
| `wired` | Is something carrying our marker in the settings file? | `settings.json` -- a **claim** |
| `current` | Does the wired command match what this checkout would write? | SHA-256 of both command strings |
| `resolves` | Does the shim's own resolution order find a real script **right now**? | The filesystem, from your current directory |

`=> LIVE` requires wiring, a resolving script, and a matching receipt if one exists.
`resolves NOTHING` prints a red result and the locations tried.

A missing receipt satisfies `-not $rec -or $wiredSha -eq $rec.commandSha256`. Hand-wired or
restored rows can therefore print `receipt no` followed by green.

The doctor treats that missing evidence more strictly and reports `??`.

`-Status` follows the shim's actual resolution order. Run it in each repository; a better resolver
could falsely certify a hook that fails.

### The standing cost

Measured in the source project, each prompt paid roughly 0.5 s for the shim. Peer lookup added
roughly 1.0 s on prompts that passed the cheap opt-in check.

These hooks run on every prompt in every repository on the machine.

The announce row has a 15 s timeout, its only time limit.

---

## Installer 2 -- git hooks (claim gate + push guard)

```powershell
pwsh -NoProfile -File <tooling>/scripts/coord/install-git-hooks.ps1 -RepoRoot <the-clone-to-govern>
```

`-RepoRoot` identifies the governed clone. The installer uses its `core.hooksPath`, or otherwise
`<its-git-common-dir>/hooks`.

Use `-HooksDir` only when neither derived path fits your layout.

Without `-RepoRoot`, the installer targets the current clone and requires it to match the source
clone. Otherwise it names both and prints a command with `-RepoRoot`.

The old default chose the script's checkout. Running
`cd <your-repo>; pwsh -File <tooling>/scripts/coord/install-git-hooks.ps1` installed into tooling
and reported success while leaving the working repository ungoverned.

Checker sources always come from the tooling checkout. The `-RepoRoot` target need not contain
`scripts/hooks/`.

The clone's shared hooks directory reaches every linked worktree immediately. Its files survive
branch switches without a merge or copy into each worktree.

Commit-time checks inspect the tree, covering writes from edit tools, shell redirects, scripts,
editors, and subagents. `PreToolUse` sees only arguments and misses shell-written files.

| Hook | Checker | Refuses |
|---|---|---|
| `commit-msg` | `scripts/hooks/claim_check.py` | A commit whose subject claims an item this worktree does not hold |
| `pre-push` | `scripts/hooks/push_guard.py` | A direct push of a protected ref -- that work goes through a pull request |

The installer honors `core.hooksPath` so hooks land where git reads them.

The installer protects existing hooks in two ways:

1. It refuses to overwrite a hook that is not ours. A `commit-msg` or `pre-push` without our marker
   stops the install; merge by hand. Blind overwriting deletes somebody else's control. The markers
   are on-disk identity: renaming one orphans every install. Rename once, in one commit, or not at
   all.
2. It never writes `pre-commit` -- not to install, not to patch, not to migrate. Two tools cannot
   both own that file. What happens when they try, and why the sequence gate therefore ships
   unwired, is at [the git-hook contract](HOOKS.md#the-git-hook-contract).

The installed `/bin/sh` shims find Python and run the checker. Without an interpreter, they report
the problem on stderr and exit 0, disabling that gate for the operation.

A missing interpreter disables both gates across the clone while every hook file remains present.
`-Status` checks the interpreter's version to detect Windows execution-alias stubs.

`-Status` skips interpreters that fail `--version`; shims accept `python` when `command -v`
succeeds. If `python` is a stub but `python3` works, status can report green for the wrong
interpreter.

`git commit --no-verify` and `git push --no-verify` bypass these local controls. Use server-side
checks if enforcement must resist that bypass.

### Prove it

```powershell
pwsh -NoProfile -File <tooling>/scripts/coord/install-git-hooks.ps1 -RepoRoot <the-clone> -Status
```

`-Status` resolves the same target clone as install and applies the same refusal rules. Its separate
`governs`, `hooks dir`, and `sources` lines identify the report's scope.

Status compares installed checker hashes against the receipt and current source.
`checker INSTALLED COPY DIFFERS FROM SOURCE` means sessions run different code from this checkout.

The verdict hashes only checkers. For shims, it checks the marker; a receipt mismatch merely prints
yellow.

A shim with an appended `exit 0` can still show `=> INSTALLED` and exit 0. Read the yellow warnings
above that result.

`-Status` never executes either checker and names this limit. Test a real commit, or run the doctor,
to find installed checkers that cannot run.

---

## Installer 3 -- the worktree gate

```powershell
pwsh -NoProfile -File <tooling>/scripts/worktree/install-gate.ps1 -Repo <the-primary-to-govern>
```

The gate refuses three kinds of action in an allowlisted primary:

| It refuses | Outcome |
|---|---|
| An `Edit`, `Write`, `MultiEdit` or `NotebookEdit` writing into that primary | The tool call never runs |
| A `Bash` or `PowerShell` call carrying a tree-swapping git verb aimed at it | The tool call never runs |
| A `Task`, `Agent` or `Workflow` dispatch made from it, since a subagent inherits the directory | Unless `-NoDispatchGate` |

`-Repo` supplies the primary checkouts for the allowlist; use the earlier `-Command` form for
several. Even when installing from a worktree, govern its primary.

Without `-Repo`, the installer uses the current clone's primary and requires the source clone to
match. Otherwise it names both and refuses.

The old default chose the tooling clone, wrongly allowlisting it while every report agreed.

`-ConfigDir` selects client config roots to wire. `-Status` and `-Uninstall` use the shared
allowlist and settings, so neither accepts `-Repo`.

The installer copies `scripts/hooks/worktree_gate.ps1` to `~/.claude/hooks/` and wires `PreToolUse`
in each qualifying config directory. These include `~/.claude` and marked `~/.claude-account-*`
directories.

Accepted client markers are `projects/`, `sessions/`, or `.claude.json`.

`settings.json` and `hooks/` cannot qualify a directory, since these installers create them.
Otherwise an earlier mistaken install would validate itself.

The installer lists rejected directories and reasons. Explicit `-ConfigDir` values bypass that
check.

Other logins need wiring too: parallel editor chats run under them. One unwired session checked out
its branch in another session's worktree, replacing files during active work.

The gate governs only primary paths in `~/.claude/hooks/ccx-gate.repos.txt`, as resolved from
`-Repo`. That file is also its kill switch.

The allowlist name is fixed, independent of config `prefix`. Its installed reader lives outside
repositories and shares the file with the SessionStart backstop.

An earlier version derived different filenames in the two components. Uninstalling the gate then
left the backstop able to run `git checkout` on the shared primary.

### The flag that drops a rule

`-NoDispatchGate` omits the dispatch rule and prints an install warning. Until it is rewired,
`-Status` reports dispatch tools as UNWIRED -- implemented but never fires.

Keep a visible, queryable record when an option disables a rule. Otherwise sessions cannot
distinguish an inactive control from a working one.

`-EnterWorktreeGate` explicitly enables a rule that is off by default. Status labels its default
state `opt-in`, without treating it as a fault.

Enabling both that rule and dispatch blocking traps primary-seated sessions: they can neither move
nor dispatch. A human must restart them elsewhere, so choose this combination explicitly.

### Prove it

```powershell
pwsh -NoProfile -File <tooling>/scripts/worktree/install-gate.ps1 -Status
```

Status reports five separate checks:

- `installed` / `source` / `parity`. SHA-256 of the installed copy against the source, printed as
  hashes and not asserted. A hand-bumped version label can lie, and has: rules shipped without a
  bump, so both lines read the same version directly above a `* STALE *` verdict.
- `governing`. The allowlist contents. With no file it says `gate is OFF`. With a file holding no
  entries it prints the bare header and nothing -- the all-clear shape, for a gate governing
  nothing. Installer 4 seeds that file, so count entries rather than look for the word OFF.
- `wiring`, per config directory. The matchers in that file, diffed against the rules the installed
  script has. `UNWIRED` is implemented but never fires; `stray`, matched but ignored; `opt-in`,
  off by design. A count of "3" says nothing unless you know 3 is right, so it asserts an
  expectation.
- `skipped`. Rejected directories whose names matched the config-root pattern, with reasons. Silent
  exclusion would hide what was examined. `.claude-account-*` also matches a launcher's `.lock`
  artifact, a real directory; wiring it writes settings into a lock file.
- What it scanned. The number of config directories and the number of rules it compared against. A
  skip must never read as a pass.

`Get-HandledTools` reads the installed script. Source, installer definitions, and passing tests
cannot establish which rules the running copy knows.

This status command always exits 0, even for `* STALE *` or an empty allowlist. It prints findings
without a verdict line; read the output.

---

## Installer 4 -- the SessionStart backstop

```powershell
pwsh -NoProfile -File <tooling>/scripts/worktree/install-selfheal.ps1 -ConfigDir ~/.claude
```

Required `-ConfigDir` selects one client config root. The shared allowlist selects repositories, so
installing before installer 3 leaves the backstop inactive.

`-HookPath` changes where the shared script copy is refreshed.

The installer wires `scripts/worktree/worktree-selfheal.ps1` in one config root per run. Run it for
every root sessions can use; the doctor marks missing wiring required `OFF`, causing exit 1.

This installer runs on PowerShell 7.0, unlike the others' 7.3 requirement. On 7.0-7.2 it can install
the unattended primary `git checkout` backstop without the gates.

### Prove it

There is no `-Status` or `-Uninstall`; removing the allowlist disables the backstop. Use the doctor
to check wiring and test its refusal on a dirty disposable repository.

Unlike the gate installer, this command requires one `-ConfigDir` per run and discovers no
additional roots.

Neither installer gives `$HookPath` or `$SettingsPath` a parameter default. A throwing default would
run before the refusal guard and report an unrelated failure.

---

## What the installers guarantee about a control's dependencies

A checker missing an imported module refuses every commit at import time. A gate missing dot-sourced
helpers prints a stderr receipt, then exits 0 without enforcing anything.

Each failure shipped once. Both installers now list all required dependencies and refuse a partial
source set:

| Installer | Also copies | If a source is missing | Verified by |
|---|---|---|---|
| `scripts/coord/install-git-hooks.ps1` | `scripts/hooks/_ccxconfig.py`, which both checkers import | refuses before writing anything | re-reads the copy and compares SHA-256 against the source; a mismatch aborts before the receipt is written |
| `scripts/worktree/install-gate.ps1` | `_command.ps1`, `_gittarget.ps1`, `_common.ps1` -- the gate's dot-source closure | refuses before writing anything | re-reads each copy after writing it |

The git-hook installer copies dependencies before checkers. This prevents an interrupted install
from leaving a checker that refuses everything because its module is missing.

`install-gate.ps1` copies the gate before its three helpers. An interruption can leave it failing
open with a stderr receipt; rerun the installer to restore the full set.

Check the installed files:

```
pwsh -NoProfile -File <tooling>/scripts/coord/install-git-hooks.ps1 -Status
pwsh -NoProfile -File <tooling>/scripts/worktree/install-gate.ps1 -Status
pwsh -NoProfile -File <tooling>/bin/ccx-doctor.ps1
```

Git-hook `-Status` hashes checkers against current source. Differences report
`INSTALLED COPY DIFFERS FROM SOURCE`.

Neither installer's `-Status` hashes dependencies. Git-hook status checks only two checkers; gate
status returns before defining its helper list.

Both miss stale or absent helpers.

The doctor checks both dependency sets. Run it as well as installer status.

The doctor also attacks each testable control. Those tests catch dependencies that copied
successfully but cannot load.

A gate still needs its stderr load-failure receipt: cleanup or partial removal can delete helpers
after installation. Without that message, load failure looks like a successful check with no
objection.

---

## Controls no installer wires

Optional controls remain unenforced until wired. The doctor reports each with a tag based on its
configuration:

- The two `PreToolUse` guards are `--` while nothing wires them. Wire one by hand and the doctor
  reports `OK` with the locations. It then attacks the blanket-stage guard; the steering injector
  gets a receipt row and no attack, so `OK` there means wired, never proven to fire.
- The sequence gate reads your configuration. With no `sequences` key in `ccx.config.json` it is
  `[-- ] sequence gate`, off by configuration. With one, as the shipped file has and this checkout
  prints, it is `[OFF] sequence gate`: nothing at commit time defends the numbers you allocate.
- The ASCII gate is `[OFF] ASCII gate: present, not wired` in every checkout, since every checkout
  carries `scripts/quality/check-ascii.ps1`. Nothing shipped runs it, so it refuses nothing until
  you invoke it: presence is capability, not enforcement, and `OK` needs installed and wired.

These optional tags normally do not fail the run. Missing the shipped ASCII checker is different:
`[OFF] ASCII gate: not in this checkout` counts as a required failure.

The verdict lists optional `OFF` rows separately under `OFF (opt-in)`.

| Control | Why it is not installed | Wire it |
|---|---|---|
| `scripts/hooks/seq_check.py` | It needs `pre-commit`, and installer 2 never writes that file | Into whatever hook framework you already use. Until you do, two sessions can take the same number and the collision merges clean |
| `scripts/quality/check-ascii.ps1` | A repo-local checker rather than an installed hook, so there is no second copy to hash -- and no shipped installer runs it | Into your own `pre-commit` hook and into CI (this repo's own `gates` workflow is that second half). Until you do it sees a file only when someone runs it, so a character written after a run is unscanned until the next one |
| `scripts/hooks/block-blanket-git-stage.ps1` | Narrow, and a false positive is expensive | A `PreToolUse` row on the shell tools -- `.claude/settings.example.json` in this checkout is that row, with the path left as a loud placeholder you must replace with an absolute one. It costs a `pwsh` spawn on **every** shell tool call, git or not, which is the other half of why it is opt-in |
| `scripts/hooks/steer-inject.ps1` | A `PreToolUse` hook on `*` taxes every tool call in every session (measured on the machine this tooling was developed on: roughly 366 ms per call, most of it bare `pwsh` startup) | Per worktree, in that worktree's `.claude/settings.local.json`, when you actually want it -- see `docs/STEERING.md` and `bin/ccx-steer.ps1` |

When config includes `sequences`, installer 2 warns that the sequence gate remains unwired.
Otherwise its absence looks like a successful check.

---

## Why the installers refuse to run inside Claude Code

All four installers throw when `$env:CLAUDECODE` is `1`.

Sessions able to install these controls could also remove them. The controls limit primary edits,
commits, pushes, and whether peers can see a session.

The selfheal script can run unattended `git checkout` on the shared primary, and the session can
edit that script. Its safety check must refuse a dirty tree.

The doctor tests a drifted, dirty disposable repository and requires
`selfheal negative: dirty primary refused`. Repairing that repository produces `RED`.

That probe needs Python and silently disappears without it. Unlike claim and push probes, it adds no
"attack skipped" row.

`-SkipAttacks` also suppresses it. A missing row means the backstop was not tested.

Run installers from a plain `pwsh` terminal.

The three installers with `-Status` handle it before checking `CLAUDECODE`, letting sessions
inspect their controls. The backstop installer has no status mode; use the doctor.

---

## Uninstall, and the kill switches

```powershell
pwsh -NoProfile -File <tooling>/scripts/coord/install-coordination.ps1 -Uninstall
pwsh -NoProfile -File <tooling>/scripts/coord/install-git-hooks.ps1 -RepoRoot <the-clone> -Uninstall
pwsh -NoProfile -File <tooling>/scripts/worktree/install-gate.ps1 -Uninstall
```

Installer 1 removes entries from one settings file per `-Uninstall` run. Repeat for every wired
root; others keep firing.

Installer 2 applies install's clone resolution and refusal rules to `-Uninstall`, including
`-RepoRoot`. Installer 3 removes the shared allowlist and config-root wiring without a repository
selector.

Uninstall removes only owned markers. Installer 2 preserves foreign hooks and their checker copy in
case the hook calls it.

Deleting that copy could silently disable another tool's control.

Installer 3 reports that removing its shared allowlist also disables the SessionStart backstop.

File switches reach running sessions because hooks reread them. Environment switches affect
processes launched with those values:

| Switch | Effect | Reaches a running session |
|---|---|---|
| Delete `~/.claude/hooks/ccx-gate.repos.txt` | Gate and backstop both OFF everywhere | Yes -- the file is read on every invocation |
| `<state-root>/announce/OFF` | Announce stands down | Yes |
| `CCX_ANNOUNCE_DISABLE` | Announce stands down for sessions started from that environment | New sessions only |
| `CCX_ALLOW_DIRECT_PUSH=1` | Push guard allows a protected ref | No. A process keeps the environment it started with; prefix the one `git push` |

Running sessions retain their initial hook settings. Installer 3's "every session, no restart" claim
applies to the reread allowlist, not its new settings rows.

The doctor reports the last three switches as `RED` under `live disarm switches` when it finds them
set.

Deleting or emptying the allowlist produces
`[OFF] worktree gate: allowlist governs NOTHING (no entries in ...)`. A missing file cannot appear
as a set disarm switch.

---

## Now prove all of it

```powershell
pwsh -NoProfile -File <tooling>/bin/ccx-doctor.ps1 -Repo <the-repo-you-governed>
```

After each install, run the doctor and check which repository, settings, and files it scanned.

Pass `-Repo` and verify the printed target. Otherwise the doctor checks the current directory's
repository, which may be the tooling checkout.

It prints both paths on each run and marks when they share a clone:

<!-- no-copy -->
```text
  repo examined    : <the-repo-you-governed>   (-Repo)
  tooling checkout : <tooling>   (every source hash below is read from here)
```

Confirm the allowlist names your repository and the gate refuses its primary. Look for
`worktree gate: allowlist ... governed, including this primary` and
`gate: LIVE allowlist + real primary`.

The doctor reads receipts, hashes installed copies against source, and compares settings matchers
with rules in the installed script.

It attacks five controls: the installed worktree gate, blanket-stage guard, unclaimed-item commit
gate, protected-ref push guard, and drifted-primary backstop. Each must refuse its prohibited case.

Each attack has a negative control: an ordinary action the gate must allow. Without that pair, a
script that refuses everything can look correct.

The backstop must repair a clean drifted primary and decline a dirty one with a reason. Testing only
the clean case cannot prove the dirty-tree guard works.

The allocator has no refusal to test. Its paired check verifies that read-only floor inspection
spends no number and advances no ratchet.

Attack fixtures are temporary git repositories, deleted afterward. The doctor changes nothing in
your repository.

Exit 0 leaves the collision refusal untested because it needs a live peer with uncommitted changes
to the same file. The doctor checks its failure notice and reports this gap every run.

| Exit | Meaning |
|---|---|
| 0 | Every required control is installed and wired, and every attack it **could** fire was refused |
| 1 | At least one control is broken or absent -- the guardrails you appear to have are not all there |
| 2 | At least one check could not be determined. Not a pass. This command refuses to guess |

### The verdict counts every control it can see, not the ones you chose

The exit code covers the full required control set, even when you chose a partial install:

- **Any `RED`, or a *required* control `OFF`, is exit 1. Required: the worktree gate, its
  allowlist and wiring, the three coordination rows, both git hooks, the SessionStart backstop. A
  partial install cannot exit 0.** The skipped one reads `OFF`, implemented, invoked by nothing,
  not "not chosen".
- Any `??` with no `RED` is exit 2. A skip is never a pass.
- `--` never fails a run. It marks optional blanket-stage or steering controls, or a sequence gate
  disabled by an absent `sequences` key.
- **An *opt-in* control reported `OFF` never fails a run**, and is counted on its own `OFF (opt-in)`
  line, not folded into the `OFF` number. Two rows qualify: the unwired ASCII gate and the sequence
  gate when `sequences` is set. No installer closes that sequence gap.

Exit 0 also requires working `python` on `PATH`, wiring in every listed config root, and no active
kill switch. `VERDICT` names every counted `RED`, `OFF`, and `??`.

`-SkipAttacks` marks attacks `??`, preventing exit 0. It produces 2, or 1 if another check proves
something broken or missing.

`-Json` includes `scanned` details: config roots, session records read or unplaceable, worktrees,
trunk, state root, and both hook directories. It also names Python, git, platform, and whether
attacks ran.

Read the blind spots printed each run. [Limits and requirements](LIMITS.md) details them and the
local controls' limits as safeguards against accidents.

## When it does not come back green

A first run commonly finds missing or unproven controls. Follow the matching result:

| You got | Go to |
|---|---|
| `RED`, `OFF`, `??`, or exit 1 or 2 | [Troubleshooting](TROUBLESHOOTING.md), whose first table is symptom to cause |
| `*** STALE ***`, or a report about the wrong clone | [Troubleshooting](TROUBLESHOOTING.md) |
| A green report you do not trust | [Drift audit](CASE-STUDY-drift-audit.md), which is the method for exactly that |
| The sequence gate's `OFF (opt-in)` | [Sequence allocation](SEQUENCE-ALLOC.md) has the `pre-commit` hook to wire |
| The ASCII gate's `OFF (opt-in)` | Wire `scripts/quality/check-ascii.ps1` into your own `pre-commit` and into CI |
| A leak-gate question | [Leak gate](LEAK-GATE.md). No installer wires that one either |
