---
title: "Spec Kit 0.16.4 for a KORUS build"
layout: default
---

# Spec Kit 0.16.4 for a KORUS build

<a id="tldrbluf"></a>

[Spec Kit](https://github.com/github/spec-kit) 0.16.4, released 2026-08-14, is GitHub's toolkit for Spec-Driven Development. It puts
requirements, plans, and tasks in files that a [KORUS](KORUS.md) build can share.

It installs ten skill prompts and a committed `.specify/` directory of templates and scripts. It
supplies no gate.

The active feature comes from a local file. Worktrees can share that pointer if they lack their own
`.specify/` directory.

[The flow](#the-flow) gives the command order and assigns each stage to a KORUS session. Check [feature state](#feature-state-is-a-file-not-a-branch) before
creating a second worktree.

---

## What it is, measured

Write the requirements first, then use them to guide the agent. [KORUS](KORUS.md) recommends this practice
to avoid relying on an evolving chat for project intent.

Measured against an installation of `specify-cli` 0.16.4 on 2026-08-15:

| Component | What it is | Size |
|---|---|---|
| 10 skill prompts | `.claude/skills/speckit-<name>/SKILL.md` | 134,365 bytes of markdown |
| 5 templates | `.specify/templates/*.md` | copyable text |
| 6 PowerShell scripts | `.specify/scripts/powershell/` | 60,677 bytes |
| Directory convention | `specs/<NNN-slug>/` holding `spec.md`, `plan.md`, `tasks.md` | n/a |

Spec Kit installs no compiled logic or analyzer. It cannot fail a build, block a commit, or reject a
document.

Your continuous integration (CI) checks and diff reviewer still enforce requirements; see [CI for leaders](CI-FOR-LEADERS.md).

---

## How it holds state

### Feature state is a file, not a branch

Each KORUS build session needs feature state that resolves within its own worktree.

- The active feature resolves from `.specify/feature.json`, key `feature_directory`.
- `SPECIFY_FEATURE_DIRECTORY` overrides it. Priority is documented as: the environment variable,
  then `feature.json`, then an error.
- It does **not** resolve from the checked-out branch. `git checkout` alone does not retarget the
  commands.
- `create-new-feature` creates `specs/<NNN-slug>/` and `spec.md`, then saves that state. It runs no
  `git checkout -b`. Branch creation happens only through an optional hook or the opt-in git
  extension.

Each scope has exactly one active feature. A scope is the directory tree the commands search, so two
sessions building different features need separate scopes.

### It resolves per worktree, until the worktree has no .specify/

On 2026-08-15, we tested `specify-cli` 0.16.4 with git worktrees. `Find-SpecifyRoot` searched parent
directories for `.specify/` without consulting git.

| Case | Result |
|---|---|
| Worktree whose branch carries the scaffold | Resolves to itself. Its own `feature.json`, no sharing |
| Worktree on a branch predating `specify init` | Resolves to the first ancestor holding `.specify/` |
| Two such worktrees nested under the primary | Both resolve to the primary and share one `feature.json` |

Create each build worktree from a branch that already contains `.specify/`. The committed files give
each worktree its own copy.

Git ignores `feature.json`, so each checkout keeps its feature pointer locally.

An older branch may lack `.specify/`, causing the search to reach the primary checkout. Two nested
worktrees can then overwrite the same untracked pointer while both show clean git status.

[Sequence allocation](SEQUENCE-ALLOC.md) covers the same shape for feature numbering.

---

## Install and initialise

Commit the initial `.specify/` files once so every build worktree inherits them.

Install the prerequisite `uv`, then run these commands at the primary checkout's root. Commit the
files they create.

Keep `--here`: `specify init <name>` instead creates a subdirectory that the worktrees will not
inherit at their roots.

```
uv tool install specify-cli
specify init --here --integration claude --script ps
```

Restart the agent to load the ten new slash commands. Create build worktrees from the commit
containing `.specify/`; do not initialize each worktree separately.

| Fact | Detail |
|---|---|
| Agent selection | `--integration <key>`. The Claude Code key is `claude` |
| Where the commands land | `.claude/skills/speckit-<name>/SKILL.md`, one directory per command |
| New skills need a restart | The agent must reload before the commands appear in its slash list |
| `specify init` does not run `git init` | Version the project yourself first |
| It needs no git at all | A search for git across the 6 installed PowerShell scripts returns 2 comment lines |

---

## The flow

The two sequences below were checked against `main` and `v0.16.0`'s `templates/commands` tree.
Changes to their order in 0.16.1 through 0.16.4 were not checked.

| Path | Sequence |
|---|---|
| Short, for smaller features | specify, plan, tasks, implement, converge |
| Full, for production work | constitution, specify, clarify, plan, checklist, tasks, analyze, implement, converge |

The README groups commands by importance, not run order. It calls `taskstoissues` core, although
neither sequence includes it.

It calls `clarify`, `checklist`, and `analyze` optional, although the full sequence includes all
three.

### Stage 1: The constitution

Write one constitution that later steps can check.

Run `/speckit-constitution [your rules]` once in the console session, before feature work:

> `/speckit-constitution Python is our primary language. All source code must adhere to OWASP ASVS
> v5.0 Level 3 and NIST SSDF SP 800-218.`

The agent writes `.specify/memory/constitution.md`. Later planning, coding, and debugging check it
before Phase 0 research and again after Phase 1 design.

### Stage 2: Specify, then clarify

Set out the feature's purpose and requirements before assigning work to other sessions.

Run `/speckit-specify [feature requirements]`, then `/speckit-clarify [spec-name]`. Keep both in the
console session so a human can answer questions.

> `/speckit-specify We need a session orchestration service that integrates with our Git-backed
> database version control. It must handle temporary auth tokens and manage user sessions.`

`specify` writes `specs/<NNN-slug>/spec.md` with an overview, user stories, and acceptance criteria.
It leaves out the technology stack, APIs, and code structure.

`clarify` checks the draft against the constitution, asks questions in chat, and adds your answers
to `spec.md`.

Only a self-check in the skill prompt keeps implementation choices out of the spec. CI does not
enforce it, so the agent may write an over-constrained spec without an error.

### Stage 3: Plan, then tasks

Choose how to build the feature, then create ordered work items.

Run `/speckit-plan [spec-name]`, then `/speckit-tasks [spec-name]`.

The agent reads the spec and writes `specs/<NNN-slug>/plan.md`. Its `Technical Context` records
language, storage, and testing choices.

The `Complexity Tracking` table records rejected alternatives only when the constitution check
fails.

`plan.md` describes the architecture. The `tasks` command writes the ordered checklist to
`specs/<NNN-slug>/tasks.md`.

The KORUS console should read both files before assigning work to build sessions.

### Stage 4: Implement

Implement one task at a time in the feature's worktree.

Run `/speckit-implement [spec-name]` in the build session holding that feature's worktree.

The agent works through `tasks.md` in order. It codes each item, writes and runs tests, fixes
failures, and checks the item off.

`taskstoissues` can turn the checklist into tracked issues afterward.

The full sequence runs `checklist` between plan and tasks. It creates a review checklist from the
spec.

It runs `analyze` between tasks and implement to check plan and tasks against the constitution. That
writes `specs/<NNN-slug>/analysis.md`; the short sequence skips both commands.

### Stage 5: Handling requirement changes

Change the requirements in the documents before changing the code. Do not ask the agent to "just fix
the code."

1. Edit `spec.md` (yourself, or ask the agent to) to reflect the new requirement.
2. Re-run `/speckit-plan`, then `/speckit-tasks`.
3. Re-run `/speckit-implement` against the updated `tasks.md`.

The agent compares the updated spec with the plan and produces a targeted checklist. It does not
rewrite the whole plan.

### Stage 6: Converge, not "fix-findings"

Find and complete work that the project documents still describe as unmet.

Run `/speckit-converge [spec-name]`. If it appends tasks, run `implement`, then `converge` again.

`converge` uses `spec.md`, `plan.md`, and `tasks.md` as its sole statement of intent. It appends
unmet work to `tasks.md` without editing or deleting code.

It returns either converged, with `tasks.md` unchanged, or N appended tasks.

There is no `/speckit-fix-findings` command and no `specs/findings.fixed.md` log in the installed
10-skill set, checked against the live `templates/commands/` directory on 2026-08-16.

The description says `converge` checks code against the documents. In the measured build, it checked
the documents against one another.

That build had 22 requirements, 65 tasks, and 85 tests. After the full flow, it ran `converge` three
times:

| Pass | Findings | Changed code |
|---|---|---|
| `analyze` | 8 | 0 |
| converge 1 | 7 | 1 |
| converge 2 | 5 | 1 |
| converge 3 | 4 | 0 |

2 of 24 findings changed application code. No pass found an unimplemented requirement, a failing
test, or behavior that contradicted the spec.

The other 22 findings concerned earlier decisions left in the documents after later, correct
decisions replaced them.

Repeat the check because your fixes can leave new document conflicts. In this measured build, a
reported missing feature meant the task list was wrong.

### A citation count is not a coverage claim

In the same build, a requirement-ID scan reported 40% coverage. Reading each uncited requirement by
hand gave 87%.

The scan counted citations. Before using such a result as coverage, read the uncited requirements.

### Which KORUS session runs which stage

| Stage | KORUS session |
|---|---|
| constitution, specify, clarify | Console. One human-reviewed pass before work fans out |
| plan, tasks | Console, or the builder the console hands the feature to |
| implement | The build session holding that feature's worktree |
| checklist, analyze, converge | The same build session, before it hands the feature back |
| taskstoissues | Console, if an issue tracker is in the loop |

Spec Kit's worktree files merge like other files. The untracked `feature.json` does not reach git,
so it adds no work to the lander's push-and-merge role.

---

## What failed verification

These two claims do not hold for 0.16.4:

| Claim | Why it is wrong |
|---|---|
| `specify init --ai claude` selects the agent | Removed at v0.10.0. `--integration` replaced it |
| `/speckit-specify` creates the git branch automatically | It creates the directory only. Branch creation is opt-in, through a hook or extension |

An earlier draft also named `/speckit-fix-findings` and `specs/findings.fixed.md` in the debugging
stage. Neither exists in the shipped templates, as Stage 6 records.

---

## What it does not give you

You can copy the templates and prompts and create the directories yourself. The toolkit saves you
maintaining 134KB of prompt text and gives sessions a shared vocabulary.

Published criticism reports large generated specs and hours spent correcting them for existing
systems. Those sources criticize cost; none disputes the mechanical facts above.

There is no architecture decision record (ADR) command or `templates/commands/adr.md`. `plan.md`
records rejected alternatives only after a failed constitution check.

Keep a separate decision record as work lands, as [KORUS](KORUS.md) advises.

A fork, `panaversity/spec-kit-plus`, adds a native ADR command at `history/adr/NNNN-slug.md`.

An earlier pass checked two catalog extensions for ADR support. It correctly rejected an `adrkit`
claim because part of that compound claim lacked documentation.

It wrongly rejected `spec-kit-arch-governance`. The catalog requires `speckit_version >=0.1.0`,
which includes every 0.16 release.

All three verifiers rejected that true claim; see [a claim three verifiers refuted](CASE-STUDY-refuted-but-true.md) before choosing either extension.

Check your existing process before adding an extension. KORUS already calls for ADRs, even though
Spec Kit lacks a command for them.

---

## A decision rule

Use the full sequence for long features or work that needs clear requirements before design choices.
Handing work to another KORUS session also makes written decisions useful.

Use `specify`, `plan`, `tasks`, `implement`, `converge` when planning would outweigh the code, or
when a reviewer already reads every diff.

This drops `constitution`, `clarify`, `checklist`, and `analyze`.

Set an exit condition before starting. If `specify` and `clarify` produce padding instead of
decisions the console can defend, stop and build directly.

---

## Where the evidence runs out

The sources do not establish how these prompts interact with `CLAUDE.md`, existing skills, or
subagent delegation. KORUS build sessions already use their own subsession workflows.

The evidence also does not settle whether a minimum viable product should use one feature or
several. Measure both questions in your own build.

---

## Provenance, and how to re-check

The install steps, command sequences, and feature-state behavior above come from installed code or
primary sources.

Recheck in this order, starting with the more reliable sources:

- run `specify --version`;
- read the installed `.claude/skills/*/SKILL.md` and `.specify/scripts/`;
- read `.specify/integration.json`;
- then consult an external write-up.

On 2026-08-16, we rechecked the command list against `github/spec-kit` `main` and the same `v0.16.4`
release.
