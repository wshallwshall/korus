# CI for leaders: What done means when the author cannot vouch for the change

<a id="tldrbluf"></a>

Continuous integration runs checks when a change arrives. For people funding this work, "done"
should mean checks passed, with evidence of what they examined.

AI-written mistakes can look plausible enough to pass review. Parallel sessions can also produce
defects that merge into the main branch, or trunk, without conflicts.

Bring [these five questions](#what-to-ask-your-team-for) to your next engineering meeting. Ask an engineer to build the pipeline; this
guide supplies no workflow file to copy.

---

## Why review stopped being enough

Slop is confident, well-formed output that is wrong enough to cause harm but plausible enough to
pass review.

An early hook reported 93% weekly usage for a session whose account was at 5%. Both the formatted
number and account were wrong ([Usage awareness](USAGE-AWARENESS.md)).

The errors are familiar, but output grew without a matching rise in reviewer hours. [The CISO summary](https://secure-development-standards.pages.dev/standards/CISO-SUMMARY.html)
describes the resulting drop in attention per change.

An external study found that AI-assisted developers wrote less secure code yet felt more confident
about its security. Perry et al. used a 2022-generation model (ACM CCS 2023).

Re-baseline that finding against [Code quality](https://secure-development-standards.pages.dev/standards/CODE-QUALITY.html) before you cite it.

Use checks that can fail to supplement review. [CI enforcement](https://secure-development-standards.pages.dev/standards/CI-ENFORCEMENT.html) explains why.

## The defect class that review cannot see

Two sessions can each choose the next free identifier in an isolated checkout. Both branches look
correct alone and merge without any conflicting lines.

Reviewing either branch alone cannot reveal the collision. It happened three separate times where
this tooling was built ([Sequence allocation](SEQUENCE-ALLOC.md)).

Three concurrent branches claimed one identifier, with the clash appearing after merge.
[CI and standards](https://secure-development-standards.pages.dev/CI-AND-STANDARDS.html) requires: *"Reserve globally unique identifiers from a shared registry, never by
scanning"*.

None of these four defenses catches that combined defect on its own:

- A separate checkout per session.
- A file lock.
- Code review.
- A green pipeline on each branch.

A central check must test the combined identifiers.

An allocator reserves each number by creating a file only if absent. Eight concurrent processes got
eight distinct numbers; rewriting one shared list silently lost four writes.

Duplicate fixes can also merge without conflicts. Two sessions fixed one defect an hour apart;
rebase reported no conflict, and the doubled fix shipped with 92 passing tests.

Elsewhere, three sessions fixed one dependency advisory with zero textual conflicts. Two of the
three pull requests closed as duplicates ([Coordination](COORDINATION.md)).

The trunk moved seven times while one pair of pull requests remained open. Individually passing
branches can still fail when combined in either order.

A branch check covers only that branch. A pull-request check covers a merge against the trunk as it
stood when the run began, excluding later trunk changes and other open branches.

## What a gate is, and what it replaces

A gate reports a deterministic pass or fail as an exit code: the same change gets the same answer.
No change may merge on the assistant's assurance alone.

[AI-assisted development](https://secure-development-standards.pages.dev/standards/AI-ASSISTED-DEVELOPMENT.html) states both the definition and the no-merge rule.

A session-start reminder asked sessions to use separate checkouts. Over 30 days where this tooling
was built, 44% of writes from sessions in the shared checkout still landed there.

This repository cannot recompute that figure, and nobody has remeasured it. Treat the
[README](https://claude-multisession.pages.dev/README.md) figure as a dated citation.

A completed change needs checks that ran, could have failed, and identified what they examined.

A prose check caught eight openings over the 30-word limit on 2026-08-10. They came from an editing
pass that added standard openings to eighteen pages.

On 2026-08-10, another check found fifteen of eighteen rendered pages lacked a summary section.
Before that test, missing summaries had no record and could not fail a run.

A gate tests stated properties of output. It does not improve the assistant or speed up the
reviewer.

## What a gate answers, and what it leaves open

| What goes wrong | What answers it |
|---|---|
| Output that is plausible and over a stated limit | A ratchet against a measured baseline |
| Two sessions allocating one shared number | Creating a file only if it does not exist |
| A convention asked for in a reminder | A deterministic check on the write itself |
| A branch that was green before the trunk moved | Revalidation against the current trunk |
| The same intent implemented twice | A claim register declared before work starts, checked at commit |

A ratchet sets a limit at today's measured value. The limit may fall but must never rise.

The write-target gate followed the 44% measurement. It checks the write's destination, not the
session's current directory ([Tips and tricks](TIPS-AND-TRICKS.md)).

The claim register sees only what sessions declare. Two sessions doing the same work under different
names can both pass.

Each change may look correct alone despite duplicating another ([Coordination](COORDINATION.md)).

## What it costs

Without a merge queue, requiring every branch to match the current trunk allows at most one merge
per full pipeline cycle.

Three costs follow from that:

- A low-urgency merge costs every other branch in flight a full cycle.
- One broken check that blocks merges stops every session, not one.
- A changed gate makes every already-green branch unverified.

[CI and standards](https://secure-development-standards.pages.dev/CI-AND-STANDARDS.html) states the sequencing rule, under *"Sequence the queue deliberately"*.

[CI enforcement](https://secure-development-standards.pages.dev/standards/CI-ENFORCEMENT.html) sets out the costs a single stream of work already carries, under *"Costs"*.

Estimate how many sessions your pipeline can handle before buying another account
([Token accounting](TOKEN-ACCOUNTING.md)).

Use your pipeline cycle time and the number of sessions in flight.

Those two numbers establish your ceiling. This repository has not measured one for you.

A verb-scanning rule once blocked a read-only status command because its prose contained a
blocklisted word. False positives can teach sessions to bypass the control.

Neither repository measures productivity gains. CI enforcement rejects unsupported benefit claims;
fund this for auditability, continuity, and reviewability.

## How to tell whether a control is real

A running control may lack a failure path, or have one nobody tested. Only a control proved to fail
supports an attestation, though all three look alike on a dashboard.

| State | What you may attest | What it is worth |
|---|---|---|
| It runs | The job executed and exited zero | Nothing about the code. A check that cannot go red produces this forever |
| It can fail | The logic has a red path somewhere in it | Nobody has driven that path with a real defect |
| It has been proved able to fail | A planted defect turned it red, on this artifact, on this date | The only state an attestation can rest on |

Scripts install the controls and hooks trigger them. A control can be:

- Missing.
- Wired to nothing.
- Wired to a dead script.
- Failing open -- waving work through when the check itself errors.

All four can exit zero and let work proceed. A fail-open control can still warn: this repository's
gate writes to stderr and the deny log when it cannot load.

The [worktree gate](WORKTREES.md) keeps sessions in separate checkouts. One shipped version crashed on the
default value used when a caller omitted an argument.

The gate fails open, so that crash allowed every prohibited write. It affected one install on every
real tool call, with no on-screen warning.

Tests passed the argument explicitly and never reached the failing default. A test now runs the gate
without arguments.

Before trusting a pass, make the same check fail deliberately. The 2026-08-04 drift audit tested
each shipped gate fix with five separate mutations that had to fail.

An adversarial review found three regressions, now covered by their own test file
([Drift audit case study](CASE-STUDY-drift-audit.md)).

## What a green pipeline does not prove

A green result describes what ran. Each limit below can survive a clean pipeline run.

- A green leak gate proves less than it appears to. Without a configured token source, CI uses
  generic detectors only. Detectors for private names remain off. [The leak gate](LEAK-GATE.md) says a pass then
  proves nothing about those names.
- A skipped job reports green having run nothing. When steps only run if code changed, a
  documentation-only pull request skips all of them, including the step that polices documentation.
- A dry run proves that nothing errored, not that the output is right. Running a change without
  letting it take effect passes valid-but-wrong output, and that is the slop a pipeline is
  structurally blind to: [CI and standards](https://secure-development-standards.pages.dev/CI-AND-STANDARDS.html).
- A scanner cannot see a policy judgment. A design note may enable an attack without containing a
  forbidden string. [The leak gate](LEAK-GATE.md) states that limit.
- The assistant's outbound queries pass no scanner. A commit-time scan cannot intercept a query as
  the assistant sends it, so that channel is human discipline alone, as [AI-assisted development](https://secure-development-standards.pages.dev/standards/AI-ASSISTED-DEVELOPMENT.html) states.
- A test can exercise the wrong copy. In the repository where this tooling was built, 85 tests
  passed while enforcement ran from an installed copy days behind source. [Drift audit case study](CASE-STUDY-drift-audit.md) records
  that count, cited rather than re-measured, so re-derive it.

## What to ask your team for

Establish which checks block a merge and whether anyone has seen them fail.

These five questions cover concurrency and AI-written code. [The CISO summary](https://secure-development-standards.pages.dev/standards/CISO-SUMMARY.html) supplies broader
questions for control owners.

| Ask | What a healthy answer sounds like |
|---|---|
| Show me one required check failing on purpose. | A planted violation, the red run, and the fix, run in front of you this week rather than described. |
| How many sessions push to this repository at once, and what is the pipeline cycle time? | Two numbers, read off a coordination surface and a recent run, rather than an estimate. |
| What allocates a number two sessions could both claim? | A registry that creates a file only if it does not exist, plus a check that fails a branch carrying an unreserved number. |
| What does a green run say it examined? | A count of units scanned printed on every run, and a non-zero exit when that count is zero. |
| When four branches are ready, who decides merge order, and what revalidates each against a moved trunk? | A named person or a written rule, plus a check that a branch is current with the trunk before it lands. |

A document alone is a weak answer. Read the current blocking list from server configuration;
settings change faster than the prose describing them.

## Related

| For | Read |
|---|---|
| The collision class git cannot report | [Sequence allocation](SEQUENCE-ALLOC.md) |
| Why a clean merge is not evidence nobody duplicated your work | [Coordination](COORDINATION.md) |
| Proving a control is live rather than installed | [Drift audit case study](CASE-STUDY-drift-audit.md) |
| Fail-open versus fail-closed -- letting work through when the check itself errors, or refusing it -- and declaring which you chose | [Hooks](HOOKS.md) |
| What a content scanner permanently cannot see | [The leak gate](LEAK-GATE.md) |
| What a pipeline buys, what it costs, and what to ask about it | [CI enforcement](https://secure-development-standards.pages.dev/standards/CI-ENFORCEMENT.html) |
| The two-page version written for a security owner | [CISO summary](https://secure-development-standards.pages.dev/standards/CISO-SUMMARY.html) |
| The practitioner record your engineers will work from | [CI and standards](https://secure-development-standards.pages.dev/CI-AND-STANDARDS.html) |
| How much AI-written code a human must actually read | [Review depth](https://secure-development-standards.pages.dev/standards/REVIEW-DEPTH.html) |
| Whether any of this reaches your team at all | [Which standards apply](https://secure-development-standards.pages.dev/standards/WHICH-STANDARDS-APPLY.html) |

The instructions below address Claude Code.

---

## For Claude Code

### Audit first, then stop

Audit all five rows below and report the results before proposing a gate.

For a repository running one session at a time, recommend scan receipts without concurrency gates.
Each run still needs to report what it examined.

Read server-side configuration directly. Branch protection changes faster than documentation, so a
remembered required-check count may be stale.

Produce commands for the human to run. Do not run installers or change branch protection.

| Establish this | How |
|---|---|
| Which checks block a merge | Read branch protection or the ruleset from the host's API for this repository |
| Whether each blocking check can fail | Plant a violation on a scratch branch and watch it go red |
| What the runner actually examines | Read the discovery configuration before trusting any total |
| How many sessions push here | Ask the human; the answer sets the cycle cost |
| What allocates shared identifiers | Read the allocator, or report that there is none |

Stop and report the audit. Do not write a gate until the human chooses one.

### Build in this order

1. Make one existing check print how many units it scanned, and where it looked. Until a run reports
   that count, no later green result is evidence about anything.
2. Refuse a pass on zero units. This repository's Tests step greps the runner output for
   `Ran [1-9][0-9]* tests` and exits `1` when that line is absent. Match the pattern to the
   runner the target repository actually uses.
3. Plant a violation of every blocking check and watch each go red. Do this before adding a new
   check, because an unarmed gate is cheaper to add than to find later.
4. Add four concurrency gates.
   - Allocation that reserves a number by creating a file only if it does not exist.
   - A check that the index row for that number lands in the same commit as the number.
   - A work-claim register, declared before work starts and checked at commit.
   - A refusal to push to protected refs.
5. Make the server-side check the authoritative one, not the local hook. A local hook is advisory
   once a session can remove it. A merge gate is harder to remove, not impossible to skip: a job
   that is skipped, or one nothing marks required, reports green.
6. Add a check that runs on the trunk after merge. A branch-level pass asserts nothing about the
   combination.

### Gate shapes, and the receipt each owes

| Gate | How it must behave | Receipt it must emit |
|---|---|---|
| Test suite | Fails the run when the runner reports no tests executed | The count of tests executed |
| Content scanner | Exits `0` when clean, `1` when a forbidden string is found, `2` on a usage error or an empty scan | What it loaded, and what it scanned |
| Control audit | Exits `0` proven, `1` red, `2` undetermined | One row per control, undetermined tagged as such |
| Identifier registry | Creates a file only if it does not exist; two-dot diff in CI mode | The allocation record for the identifier the change claims |
| Prose ratchet | Seeded at today's measured figure, never at zero | The corpus scanned, and the current figure |

Read these three shipped instances before you write a new gate:

- `.github/workflows/gates.yml` refuses a pass when the runner reports no tests executed.
- `scripts/security/scan_forbidden.py` prints what it loaded and what it scanned, and exits `2` on an empty
  scan.
- `bin/ccx-doctor.ps1` exits `0` only when every required control is installed, wired, and
  proved by refusing a planted attack. It exits `1` on any red or any required control
  wired to nothing, and `2` when a check could not be determined.

Use exit `0` for proven, `1` for red, and `2` for
undetermined. A skipped check must not claim a pass by exiting `0`.

Seed a ratchet at the measured figure. A zero limit on day one risks shipping disabled.

Read current baseline constants from `tests/test_prose_rules_hold.py` each time. Do not rely on this page or memory
for those values.

### Verify before you report success

- Drive the artifact that enforces, not the copy in the repository. A test bound to the source copy
  says nothing about an installed one.
- Mutate the shipped artifact one change at a time and require each mutation to go red. The
  2026-08-04 audit ran five mutations per fixed gate, and an adversarial review of those fixes
  surfaced three regressions. Mutate until every branch has been driven, not until you reach five.
- Run the entry point with no arguments. A default value is a code path no test that passes the
  argument will ever reach.
- Pair every positive with a negative control, so a zero is worth something. A search returning zero
  proves nothing until the same predicate returns non-zero on input that has to match.
- Run the suite from CI's working directory, with CI's path arguments. A run from the wrong
  directory can find nothing and still exit clean.
- Read what your instrument defaulted to. Latest-attempt filters, scoped discovery and page sizes
  each answer a narrower question and report no error.
- Enumerate sibling paths for every control you add. The other operating system, the counterpart
  destructive verb, the adjacent route: an assistant implements where it was prompted.
- Neutralise every caller-supplied value before it reaches a refusal message. A branch name accepts
  semicolons and pipes, and a newline in a path forges a second remediation block.

### What you must never claim

- You cannot claim a speed or productivity gain. None is measured in either repository. Report
  auditability, continuity and reviewability instead.
- You cannot claim a gate can fail unless you made it fail. Report the deny path as unproven in the
  same place you report the pass.
- You cannot claim a control is enforcing from a green test run. Name the copy you exercised.
- You cannot claim coverage from a scoped run. State the paths you scanned beside the count.
- You cannot claim a required-check count from memory. Read it out of the configuration on the day
  you write the sentence.
- You cannot claim a fix is unique. A clean merge is not evidence that no other session did the same
  work an hour earlier.
- You cannot claim a headline percentage about AI-written code. Percentages that did not reconcile
  with their own sources were dropped here after checking, so do not source a number from popular
  statistics.

### Where the detail lives

Read the linked source before acting on a row. Do not reconstruct its details from memory.

| For | Read |
|---|---|
| Every rule the handoff half above compresses, with the incident behind it | [CI and standards](https://secure-development-standards.pages.dev/CI-AND-STANDARDS.html) |
| Sorting a control set into blocking and advisory | [CI enforcement](https://secure-development-standards.pages.dev/standards/CI-ENFORCEMENT.html) |
| Controls for AI-assisted work, and what a gate is | [AI-assisted development](https://secure-development-standards.pages.dev/standards/AI-ASSISTED-DEVELOPMENT.html) |
| Adoption order, and reporting-only before blocking | [Adopting these](https://secure-development-standards.pages.dev/standards/ADOPTING-THESE.html) |
| The identifier collision and its allocator | [Sequence allocation](SEQUENCE-ALLOC.md) |
| Which hook fires when, and its failure posture | [Hooks](HOOKS.md) |
| A scanner that treats an empty scan as a refusal | [Leak gate](LEAK-GATE.md) |
| Auditing controls that only look installed | [Drift audit case study](CASE-STUDY-drift-audit.md) |
| The traps, in the order they bite | [Tips and tricks](TIPS-AND-TRICKS.md) |
