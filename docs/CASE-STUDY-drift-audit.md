# Case study: Auditing a multi-session estate as one system

<a id="tldrbluf"></a>

On 2026-08-04, we audited KORUS controls on one host from source through installed behavior. A
merged, passing control could still enforce nothing.

The audit produced the six design rules below. To check your current installation, run the audit;
the recorded host's status cannot establish yours.

Use these checks when auditing your own controls. The command reports the scope it examined and the
questions it could not answer.

---

Check whether the controls on your machine enforce their rules now. The 2026-08-04 audit covers one
host only; publishing its bypass inventory would expose specific gaps.

Run from the repository root:

```powershell
pwsh -NoProfile -File bin/ccx-doctor.ps1
```

The audit prints what it scanned, unknown results, and blind spots. It marks an undetermined result
`??`, never `OK`.

---

## Why the estate is the unit of audit, not the script

Reading `scripts/hooks/worktree_gate.ps1` shows its deny rules. Reading
`scripts/hooks/collision_gate.ps1` shows how it handles errors. Neither proves which copy actually
runs.

The client runs an installed copy. Four links must hold:

- an installer places that copy outside every working tree;
- a matcher in a client config root invokes it;
- it resolves its helpers from beside itself;
- the host has an interpreter to run it.

A failure between those steps can leave each file looking correct. In this system, silent failure
can produce the same bytes as success:

> **Every failure mode in this system is byte-identical to success.**

A hook can be missing, unwired, pointed at a dead script, or failing open. Each can produce exit 0
and no output while work proceeds.

A fresh clone can therefore look healthy after one installer run, or none.

Audit the whole path from checkout to decision. Use recorded evidence for each step.

---

## The four-layer model

Check each control at four layers. A pass at one layer proves nothing about the next.

| Layer | The question it answers | Instrument | The failure that looks like success |
|---|---|---|---|
| **Source** | Does the rule exist in this checkout? | Read the file; run the test suite | The rule is merged, tested and green -- and has never been installed anywhere |
| **Installed** | Is that rule in the copy the client executes? | SHA-256 of the installed artifact vs the source | Installed copy is days behind source. Reverse drift is equally invisible: delete a rule from source and the stale installed copy keeps enforcing it forever, while every test correctly reports it gone |
| **Wired** | Does anything actually invoke that copy? | Read live matchers out of every config root; diff them against the rules the *installed* script implements | A matcher exists but names a similarly-titled script from a different project; or a rule is implemented and no matcher ever reaches it |
| **Effective** | What does it decide when fed a real input? | Pipe crafted input at the installed artifact and read the emitted decision | Rules exit on first match, so a later rule may be structurally unreachable. A helper the script dot-sources is absent, so it exits 0 and enforces nothing |

These checks exposed three costly mistakes:

Run the installer as a separate, announced step after merging a hook. Distinguish deliberate
disabling from accidental lack of wiring.

One coordination hook remained unwired for hours because another project's similarly named entry
occupied its slot.

Drive input into the installed script to test its decisions. The source, installed copy, and
settings matcher may all disagree.

A status message must distinguish resolved state from failed discovery. One hook printed status for
weeks without resolving anything, outlasting the other silent defects found that day.

See [put a signal outside the component](TIPS-AND-TRICKS.md#put-at-least-one-signal-outside-the-component-being-audited).

---

## The drift taxonomy: D1-D4

Each drift class needs a different check and fix. The last three can hide the first:

| Class | What drifts | Symptom | Instrument |
|---|---|---|---|
| **D1 -- Session drift** | Where work happens: a session builds in the shared checkout instead of an isolated one | Two sessions overwrite each other; a tree is swapped out from under a live session | Target-path gating at tool time; a `SessionStart` backstop that repairs and *says so* |
| **D2 -- Control drift** | Which artifact enforces: source, installed copy and wired matcher diverge | Nothing. This is the silent class | SHA parity per layer; matcher-vs-implemented-rule diff |
| **D3 -- Coverage drift** | What the rules can see: work moves to routes the rule set does not cover | A control is live, correct, and simply never invoked | Fire it on purpose; enumerate the routes; report every non-match you deliberately allow |
| **D4 -- Belief drift** | What everyone thinks is true: docs, memory, status and premises diverge from behavior | Confident, wrong statements -- including your own from last month | Re-measure the premise; date and attribute every figure; state status exactly |

D1 describes the worktree problem the controls aim to prevent. D2, D3, and D4 explain why an audit
can wrongly conclude it is solved.

### On D3 specifically

A list of covered tools or verbs silently excludes everything absent from it. Prefer
deny-by-default; otherwise, publish the rule inventory and make `-Status` check expected coverage.

`scripts/hooks/worktree_gate.ps1` inspects tool arguments and cannot see files written inside a
shell script. A script invocation need not contain the `git` token a command-string gate seeks.

An approved repair script can take this route too. Document string-scanning gates as accident
prevention, never as security boundaries.

Command-parsing hooks share `scripts/hooks/_command.ps1` for splitting and
`scripts/hooks/_gittarget.ps1` for resolving git targets.

Separate parsers can disagree about the same command. Keep exactly one copy of each safety check so
a second, untested copy cannot drift.

### On D3's opposite failure

On the development repository, a verb scanner denied a read-only status command because a prose line
contained a blocked word. It also denied a commit containing one in its message.

Unnecessary denials encourage sessions to disregard the refusal text. On the shell path, that text
is the only control available.

Use these parsing checks:

- scan per line, and fold continuations;
- blank out quoted spans;
- recurse into interpreter arguments;
- ship ALLOW-asserting tests for the multi-line, echoed and message-containing cases.

Repeated false alarms can cause sessions to bypass or remove the gate.

---

## Six design rules the audit produced

### 1. Gate on the write's target path, never the session's cwd

Over 30 days, 29% of writes from sessions in the shared checkout landed in separate worktrees
through absolute paths. A gate based on working directory would wrongly deny them.

Check the destination path. Sessions can write to their worktrees without changing directory or
restarting.

This also permits writes into another session's worktree. Accept that limit explicitly; the denial
text teaches this route.

Subagents inherit the parent's working directory. A target-path gate still denies writes to
forbidden destinations, regardless of where the parent started.

### 2. The gate's own enforcement surface must be governed

The installed gate and allowlist live outside governed checkouts, so branch changes cannot remove
them. That also leaves them outside an ordinary checkout-path rule.

Without a separate rule, any governed session could edit the gate itself.

Rule 1a in `scripts/hooks/worktree_gate.ps1` protects its own script and allowlist. It prevents a
session from disarming the control.

A human can still uninstall it from a terminal. The script's `.NOTES` documents the kill switch.

Any control with editable enforcement files must protect those files. Evaluate that protection
separately from the rule it protects.

### 3. An unbacked backstop is worse than an admitted gap

One gate header claimed a commit-time check covered its shell blind spot. The dispatcher existed,
but none of its checks enforced that predicate.

Only the refusal text asked sessions to obey.

Verify that a claimed backup check enforces the needed predicate. Otherwise, remove or qualify the
claim so the next reader knows the gap remains.

### 4. Evaluate prohibitions as a set, never one at a time

One rule denied dispatch from the shared checkout; another denied relocating a live session into a
worktree. Together, they left no in-session route to isolation.

A human had to restart the session elsewhere.

`scripts/worktree/install-gate.ps1` makes the relocation rule opt-in through `-EnterWorktreeGate`.
It is off by default, and the parameter comment explains the combined dead end.

Provide a supported route before banning the existing one. A prohibition that removes every route to
required behavior is defective.

Two related checks follow:

- Re-measure a deny's premise before defending it, and record its scope precisely. One rule here
  was remembered as broader than it was. Part of its rationale had expired too: the tooling gained a
  capability the rationale assumed absent. An expired premise is D4 drift in a control's uniform.
- An install option that removes a control must leave a queryable trace. A flag that drops a
  rule silently recreates the observability gap the system exists to close. Here the flag leaves
  the rule *implemented but unmatched*, the audit reports it as dead, and the installer prints a
  warning.

### 5. A control with no receipts cannot be ranked, fixed, or defended

One gate wrote decisions to stdout and exited 0 without keeping a log, counter, or audit file.
Nobody could measure prevented drift or the effect of a fix.

Log each denial's timestamp, rule, tool, working directory, target, and decision. Never log the raw
command.

A subagent process id lets its parent find denied work. These records make severity rankings
testable.

### 6. Prefer a control that acts and receipts itself; where you cannot, say so

One hook resolves peers and asks the model to send a message. The model also records delivery, so
the audited action writes its own evidence.

Every audit run names this as a permanent blind spot.

---

## Evidence discipline

The audit must also prove that its own checks can detect failure.

### Green tests that bind the repo copy prove nothing about the installed one

One gate in the development repository had 85 passing tests, all against source. The installed copy
was days behind, and no test read it or live settings.

`Get-HandledTools` in `bin/ccx-doctor.ps1` skips when no installed artifact exists. Otherwise, it
checks SHA-256 equality and compares installed rules with every config root's matchers.

It prints the scanned scope so a skip cannot look like a pass:

| State | Meaning |
|---|---|
| `UNWIRED` | The installed script implements the rule and no matcher ever invokes it -- a dead rule |
| `STRAY` | A matcher invokes the gate for a tool the installed script ignores |
| off by choice | An opt-in rule that is off because somebody chose that, reported separately so it never hides in the same bucket as an accident |

### Fire every control on purpose, and pair every attack with a negative control

`bin/ccx-doctor.ps1` sends crafted `PreToolUse` payloads to the installed gate and requires refusal
for each attack:

- a blanket stage;
- a commit claiming an unheld work item;
- a push to a protected ref.

The probes use disposable repositories, an allowlist, and a state root. They delete these fixtures
when finished.

Pair each attack with an ordinary action the same gate must allow. Otherwise, a broken script that
refuses everything can look correctly enforced.

Copying an entry point without its helpers produced that failure.

When probes test source instead of an installed copy, the audit reports `??`, never `OK`. Working
source does not prove a live control exists.

### The probe is part of the system under test

The first probe passed input under a parameter name that bound to nothing, without an error. Four
attacks sent a tool name and working directory but no tool input.

Path-based rules allowed the empty payloads, and the audit wrongly blamed the gate.

`New-PreToolUsePayload` now throws on empty tool input. The attack block catches it and records `??`
for probes that never fired.

If a known failure and the case under test produce the same output, report untested. Check the probe
against a known-good instance before trusting either result.

### Prove each fix by mutation

A passing test does not prove it can detect the defect. For each shipped fix, five mutations were
applied one at a time and required to fail.

The exercise found three regressions from adversarial review, now pinned in a separate test file.

Deliberately alter the shipped artifact and confirm each mutation fails its test. Add a regression
check for each defect review finds.

### Test the real pair, not stubs

One fix made ordinary edits to untouched files fail despite a green suite. Test stubs emitted JSON
the real helper never produced.

Run the real components together before shipping an interface change.

### Label figures you cited but did not re-measure

The 29% figure is the gate's only quantitative support for target-path checks. This repository
cannot recompute it, and nobody has checked whether it still holds.

Label figures "cited, not re-measured -- treat with care." Strike superseded claims rather than
deleting them, and build a way to recompute numbers that guide design.

The 29% measurement, 85-test count, and per-prompt coordination cost came from the development
repository. None has been remeasured since; check again before reusing them.

---

## Writing the outcome down

### Record rejected options with the specific blocking fact

These alternatives get proposed again whenever shared-checkout protection fails:

- an OS-level sandbox;
- filesystem ACLs;
- a bare-repository layout;
- a repository-level worktree lock;
- a native path-deny rule in the client's own permission system.

Each option had a specific blocker: platform support, the lock's actual scope, or nested worktrees
inside the checkout a path rule would cover.

Some options also lost the refusal text that tells a session how to recover.

Record the blocking fact beside each rejected option. That lets later sessions revisit changed facts
without repeating the entire investigation.

For an unproven mechanism, set a time limit and first test whether it can fail as expected.

One denial listed the forbidden primary first among suggested worktrees, pushing a valid option
beyond the display cap. A string-to-object comparison caused the filter to always pass.

Test that the forbidden path never appears among the suggestions.

### State status exactly

A bare Done can cause the next session to assume unfinished work is complete.

State what remains for each item: Mostly done -- X, Y; NOT done: Z. An overstated status can stop
the next session from checking a known gap.

`bin/ccx-doctor.ps1` makes its exit code reflect that distinction:

- `0` only when every required control is installed *and* wired *and* refused every attack;
- `1` on any red;
- `2` when a check could not be determined. `-SkipAttacks` forces exit 2.

The tags are `OK`, `RED`, `OFF`, `??`, and `--`. Never treat `??` as `OK`.

### Print what you scanned, and name your blind spots, on every run

Every run prints `WHAT WAS SCANNED`: config roots, session records read, unplaced records,
worktrees, and interpreter. It also prints blind spots, whether or not a check failed.

---

## What this method cannot tell you

The audit has these limits:

| Limit | Consequence |
|---|---|
| **PowerShell 7, Windows-first** | Nearly every shipped script is PowerShell. Off Windows, process-table self-marking and path case-folding degrade, and the audit says so on every run. The Python part of the set -- the git-hook checkers, the leak gate and the one substrate module they share -- is stdlib-only and portable |
| **The session-management MCP is Claude Code Desktop only** | It is **absent on a plain CLI install**. Where it is absent, the announce hook still fires, still resolves peers, and then asks the model to call tools it does not have. PowerShell cannot see whether that MCP exists, so delivery is unprovable from here -- it is printed as a permanent blind spot |
| **The client's session record schema is a vendor contract** | Every liveness answer rests on a per-session JSON record written by the client. That schema can change under you without notice, and when it does the fence degrades quietly |
| **The client-side session listing cannot see every session kind** | Editor-hosted sessions in particular. A liveness signal built on it is incomplete by construction -- which is why liveness in this repository may only **veto** a destructive action, never **permit** one |
| **No interpreter, no gate** | With no Python on PATH the git-hook shims fail open: they print to stderr and exit 0. The commit-time controls are off, and only the audit says so |
| **Documented bypasses exist and are not closed here** | A commit made with verification skipped bypasses both git hooks, and nothing local records that it happened. This is a guardrail against the accidental mistake, not a security boundary. Anything that claims otherwise is the unbacked-backstop defect in design rule 3 above |
| **Scope** | The audit examines one clone and the config roots it lists. It is not a machine-wide statement |

Two controls remain only partly provable:

- The collision gate's deny path needs a live peer worktree with an uncommitted change to the
  same file. The audit proves only that it does not go silent when it cannot resolve: the fail-open
  path emits a notice rather than output byte-identical to all-clear. The deny is a blind spot every
  run.
- The session banner makes no decision, so there is nothing to attack. It is reported by receipt
  and by live re-resolution only.

---

## The audit loop, condensed

1. Enumerate every control by receipt. Hash each installed copy against source. Read live matchers
   from every config root. Diff wired matchers against the rules the *installed* script implements.
2. Fire each control on purpose and require it to deny. Against the installed copy, against
   throwaway fixtures, each attack paired with a negative control the same control must allow.
3. Print what you scanned, always. A skip must never read as a pass; report it `??` and let the
   exit code carry it.
4. Name your blind spots on every run, whether or not anything failed.
5. Prove each fix by mutation before calling it a fix.
6. Write the outcome exactly -- including what is not done, which options were rejected and why, and
   which figures were cited rather than re-measured.

[`anthropics/claude-code#76590`](https://github.com/anthropics/claude-code/issues/76590) records the worktree failure repaired by `scripts/worktree/worktree-selfheal.ps1`. The
`SessionStart` hook announces repairs so they do not look like an uneventful start.

---

## A note on what is not in this document

The source was a dated, ranked register of probe-verified bypasses and exact commands. That register
remains permanently withheld because publishing it would expose working bypasses.

Run the audit for current findings about your own installation. A published register cannot
establish its present state.
