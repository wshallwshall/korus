---
title: KORUS
layout: default
---

# KORUS

<a id="tldrbluf"></a>

KORUS helps you run several Claude Code sessions on one project without losing track of their work.
It combines scripts that block common mistakes with a way to divide tasks, review changes, and merge them.

The name stands for Keep One Repo, Unblock Sessions. The method comes from one developer's experience
using Claude Code to build a real project.

It covers model settings, account costs, project records, and work across sessions. The `korus`
repository supplies the scripts for that last part.

**Start with [Quickstart](QUICKSTART.md)** to install the controls and try an edit they should
block. If you're deciding whether you need them, read the [FAQ](FAQ.md).

KORUS assumes Claude Code for Desktop. It is aimed at people who use Claude Code throughout a build;
an occasional session may not need this setup.

<a id="what-goes-wrong-without-it"></a>

## Separate sessions can still undo each other's work

Suppose session A is editing a file. Before it commits, session B runs this command in their shared
checkout:

<!-- no-copy -->
```powershell
git checkout -B feature/parser origin/main
```

Git may allow the switch if the branch is not checked out elsewhere. Both sessions now see files
from the new branch, and A's uncommitted work is on a different branch than A expects.

Neither session gets a warning that the other one changed its workspace.

Other conflicts are harder to spot. Sessions can edit the same file, reuse a record number, compete
for a config lock, or change shared lists and agent memory.

They can also build the same feature in different files. Both pull requests pass their checks,
Git reports no conflict, and someone later has to discard one implementation.

The upstream report, [claude-code#76590](https://github.com/anthropics/claude-code/issues/76590),
includes a [field report](https://github.com/anthropics/claude-code/issues/76590#issuecomment-5004149125)
of roughly fourteen sessions sharing one directory.

Claude Code's native worktrees now prevent many writes back into the main checkout. A worktree is a
separate checkout with its own branch and files, but shared Git history.

Those checks do not coordinate edits between isolated sessions. PowerShell also has fewer command
checks than Bash. The [FAQ](FAQ.md) explains where KORUS adds protection.

<a id="what-it-looks-like-when-it-works"></a>

## A blocked edit gives you time to coordinate

Session A edits `service.py` and leaves the change uncommitted. Session B tries to edit the same file
in its own worktree.

The collision gate blocks B's edit before it runs. Its message names the live session holding the
change and, when available, the task that session is doing.

B can coordinate with A or work on `parser.py` instead. That gives both sessions a chance to finish
without finding the overlap at merge time.

<figure role="group">
<svg viewBox="0 0 820 210" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Two session lanes on a shared timeline. Session A edits service.py and leaves the change uncommitted. Session B then reaches for the same file and the collision gate refuses the edit before it runs, naming who holds the file. Session B edits parser.py instead, and both branches land.">
  <defs>
    <marker id="ix-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="currentColor" />
    </marker>
  </defs>
  <text x="12" y="52" font-size="12" font-weight="bold" fill="currentColor">Session A</text>
  <line x1="100" y1="46" x2="780" y2="46" stroke="currentColor" stroke-width="1" marker-end="url(#ix-arrow)" />
  <rect x="120" y="26" width="200" height="40" rx="6" fill="none" stroke="currentColor" stroke-width="1.5" />
  <text x="220" y="43" font-size="11" text-anchor="middle" fill="currentColor">edits service.py</text>
  <text x="220" y="59" font-size="10" font-style="italic" text-anchor="middle" fill="currentColor">left uncommitted</text>
  <text x="12" y="158" font-size="12" font-weight="bold" fill="currentColor">Session B</text>
  <line x1="100" y1="152" x2="780" y2="152" stroke="currentColor" stroke-width="1" marker-end="url(#ix-arrow)" />
  <rect x="340" y="132" width="190" height="40" rx="6" fill="none" stroke="currentColor" stroke-width="1.5" stroke-dasharray="4 3" />
  <text x="435" y="149" font-size="11" text-anchor="middle" fill="currentColor">reaches for service.py</text>
  <text x="435" y="165" font-size="10" font-style="italic" text-anchor="middle" fill="currentColor">the tool call never runs</text>
  <line x1="435" y1="130" x2="435" y2="92" stroke="currentColor" stroke-width="1.5" marker-end="url(#ix-arrow)" />
  <rect x="330" y="74" width="210" height="30" rx="6" fill="none" stroke="currentColor" stroke-width="2" />
  <text x="435" y="94" font-size="12" font-weight="bold" text-anchor="middle" fill="currentColor">REFUSED, with the reason</text>
  <rect x="570" y="132" width="190" height="40" rx="6" fill="none" stroke="currentColor" stroke-width="1.5" />
  <text x="665" y="149" font-size="11" text-anchor="middle" fill="currentColor">edits parser.py instead</text>
  <text x="665" y="165" font-size="10" font-style="italic" text-anchor="middle" fill="currentColor">both branches land</text>
  <text x="12" y="196" font-size="10" font-style="italic" fill="currentColor">Without the gate, B's write lands and one of the two loses work at merge -- with nothing on either screen saying so.</text>
</svg>
<figcaption>The refusal happens at edit time, before the write, and names who holds the file. Without
it both writes succeed and the loss surfaces at merge, or later.</figcaption>
</figure>

<a id="what-the-tooling-enforces"></a>

## The scripts check edits, commits, and pushes

| Control | What it does | Where it stops |
|---|---|---|
| [Worktree gate](WORKTREES.md) | Blocks edit-tool writes into an allowlisted primary checkout and selected Git commands that swap its tree | It does not see every way a shell command can write a file |
| [Collision gate](COORDINATION.md) | Blocks an edit when a live peer has uncommitted changes to that file | It cannot block work it cannot see; two sessions can still build the same feature in different files |
| [Git hooks](HOOKS.md) | Reject a commit claiming work the worktree does not hold, and a direct push to a protected branch | `--no-verify` skips them without a local record; use remote branch protection too |
| [Sequence allocation](SEQUENCE-ALLOC.md) | Uses an atomic file create to give each caller a different record number | Both sessions must ask; no installer wires the commit-time sequence gate |
| [Pruning](PRUNING.md) | Removes a worktree only when it is merged, clean, and unoccupied | Some occupants are invisible, including one editing by absolute path from elsewhere |

The sequence gate ships unwired. The doctor reports it `OFF` until you wire it.

The pruning tool stops when it knows it cannot determine occupancy. Each run also lists four cases
it cannot detect. Check those limits before removing worktrees.

The [worktree guide](WORKTREES.md#what-actually-stops-the-failure) compares the three controls related
to the branch-switch example. Only the worktree gate prevents that failure.

<a id="the-rest-of-the-framework"></a>

## People still need to divide the work

Scripts do not assign jobs. You give each session a role in its opening prompt: one briefs and
checks progress, one builds a task, one reviews it, and one decides what merges.

Another role investigates failed checks. [Run a KORUS build](KORUS-BUILD.md) explains the arrangement.

More sessions can produce work faster than the project can review and merge it. The
[reported run in the FAQ](FAQ.md#more-sessions-can-fill-the-merge-queue-faster) shows that limit;
it does not establish a productivity gain.

| Decision | Guide |
|---|---|
| Which model and effort setting to use | [The KORUS framework](KORUS.md), the original account rewritten with permission |
| How to run one desktop instance per Claude account | [Desktop accounts](DESKTOP-ACCOUNTS.md) |
| How account cost compares with published API rates | [Token accounting](TOKEN-ACCOUNTING.md) |
| What to keep in the backlog, decision records, and security register | [The KORUS framework](KORUS.md) |
| When to stop before a usage limit | [Usage awareness](USAGE-AWARENESS.md), a design with no shipped hook |
| Which checks establish that work is done | [CI for leaders](CI-FOR-LEADERS.md) |

<a id="what-it-costs-you"></a>

## Install the controls, then check that they work

Setup copies `scripts/`, `bin/`, and `ccx.config.json` into your repository. You commit those files
and edit two config keys. Cloning this repository alone installs nothing.

An allowlist under your user config root applies per machine. Other controls have different scopes;
[Install](INSTALL.md) lists them and explains how to check each one.

**These controls prevent accidents; they are not a security boundary.** A shell command can write a
file without the edit-time gates seeing its target.

Run the doctor before and after installation. An edit succeeding cannot tell you whether a gate is
working or simply absent.

```powershell
pwsh -NoProfile -File <tooling>/bin/ccx-doctor.ps1 -Repo <the-repo-you-govern>
```

There is no `ccx` command on `PATH`. Use [Troubleshooting](TROUBLESHOOTING.md) for red or undetermined
rows, and [Limits and requirements](LIMITS.md) for platform support and blind spots.

<a id="start-here"></a>

<a id="where-to-go-next"></a>

## Choose your next step

| You want to | Read |
|---|---|
| Try the tooling | [Quickstart](QUICKSTART.md) |
| Understand the shared-repository model | [Concepts](CONCEPTS.md) |
| Have Claude Code assess your project | [Feed this to Claude Code](FEED-THIS-TO-CLAUDE-CODE.md) |
| Set up session communication and merging | [Running multiple sessions](RUNNING-MULTIPLE-SESSIONS.md) |
| Find a command | [Every script](SCRIPTS.md) |
| Set up a working agreement | [CLAUDE.md.template](https://claude-multisession.pages.dev/CLAUDE.md.template) |

For day-to-day work, the guides follow this order: [Worktrees](WORKTREES.md),
[Coordination](COORDINATION.md), [Steering](STEERING.md), [Sequence allocation](SEQUENCE-ALLOC.md),
[PRs and merges](PR-AND-MERGE.md), then [Pruning](PRUNING.md).

[Leak gate](LEAK-GATE.md) describes a scanner you can run and its blind spot.
[Session mail](SESSION-MAIL.md) explains how to build communication for peers that announce cannot reach.

[Tips and tricks](TIPS-AND-TRICKS.md) collects lessons from use. The case studies cover a
[drift audit](CASE-STUDY-drift-audit.md), a [correction chain](CASE-STUDY-correction-chain.md),
and [a claim three verifiers refuted](CASE-STUDY-refuted-but-true.md).

The standards live at [secure-development-standards](https://secure-development-standards.pages.dev/).
