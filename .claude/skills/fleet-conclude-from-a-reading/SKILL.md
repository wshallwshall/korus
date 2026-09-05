---
name: "fleet-conclude-from-a-reading"
description: "Turn a reading or finding into a conclusion, report, retraction or prescription. Use before you state, relay or act on what an instrument told you."
user-invocable: true
disable-model-invocation: false
---

# fleet-conclude-from-a-reading

> Shared fleet rules, split out of [COMMON.md](../../../roles/COMMON.md) on 2026-09-05.
> Prohibitions that bind before this task starts stay in that file. Read it first.

### A saved verifier result does not learn either

A workflow writes its findings to an output file. That file is a claim about the moment it ran,
and it reads exactly like a reading of now.

| Item | Rule |
| --- | --- |
| Before quoting a saved finding | Re-check it against the tree. One command, and the whole trap is not running it |
| What to send with it | The ref or the time it was measured at. A finding with no timestamp cannot be aged by its reader |
| The tell | Everything in the report was true when written and none of it was true when sent |
| Why it survives review | A stored result is formatted like a measurement, carries real file and line numbers, and none of that goes stale in a way the text shows |

**Measured 2026-09-04.** A session read three blockers out of a workflow's output file and relayed
them to a peer as current state. All three had been fixed twenty minutes earlier.

One of the three carried a number: it named three ratchet baselines to set. Acting on it would
have re-reddened the build, because a file imported after that run added 96 long sentences and 104
fat paragraphs to the corpus.

**Why this is worse than a stale backlog row.** A row is visibly old and has a filed date on it. A
verifier output has neither, and it arrives in the voice of a measurement that was just taken.

### A remembered number goes stale like a stale message, and nothing catches it

The stale copy is in your head, so there is no artifact to date and no instrument to point at it.

Measured: a seat compared a live 84 against "your 89". The other seat never published an 89 that
window. It was the reader's own reading from a window that had ended two hours earlier. **Both
windows pass through the high 80s and 90s, so the level cannot separate them. Only the reset instant
can.**

Carry the instant with any number you remember, or do not carry the number.

### One-line rules, each already paid for once

| Item | Rule |
| --- | --- |
| Two readings disagree | Run your instrument again before you retract a finding or blame your own tools. |
| A reason to skip | Run the test, even when you have a good reason to skip it. |
| Empty results | Run the same test where it must find something before you believe an empty result. |
| The same instrument twice | Do not treat a reading that agrees with the code as corroboration. |
| Identity beats absence | Compare bytes or hashes. Absence of evidence needs a control; identity does not. |
| Hedges | Do not write "probably" when one command gives you the fact. |
| The alarming sentence | Measure the more alarming sentence before you write it or relay it. |
| Findings that agree | Test a finding hardest when it supports you, and hardest of all when it puts nobody in error. |
| Label and mechanism | Examine the label and the mechanism separately. A false mechanism outlives a wrong answer. |
| Three states | Write "confirmed", "refuted" and "untested" as three different states. |
| Coincidence | Before you explain a coincidence, ask who else touched the system. |
| Live branches | Measure every live branch. "Not landed" and "not claimed" are different facts. |
| Existing work | Ask whether the work already exists on a branch before you build it. |
| Your own notes | Read your note before you measure again, and treat a disagreement as the finding. |
| A past statement | Measure again before you answer a current question with a past reading. |
| Commit pairs | Cite the commit that fixed a problem together with the commit that described it. |
| Soft estimates | If your conclusion survives at half your estimate, stop refining the estimate. |
| Do not yield | If your measurement is the better one, state the number again. |
| A partial result is not a result | If you build an adversarial or verification stage, let it finish. |
| Name the pressure, not just the behaviour | A seat under a visible backlog gauge responds to the number instead of to the work. |
| Verify the inference, not only the facts | Confirming a claim's facts are true is not confirming they imply it. Have the inference checked by someone who was not told the conclusion. |
| Independent of whom | A second seat's verification can be independent of the first seat and not of its framing. |
| What self-review catches | What a control catches, and nothing else. It is blind where you did not know a step existed. |
| Why a peer finds it | A peer is not smarter there, only differently blind, which is why disagreement finds what neither party was looking for. Where only one seat looked, assume the error is still there. |

**Reading a running stage is acting on the stage you built to stop you.** Measured: a seat dispatched
two rows on partial output. The refute stage then killed one and corrected the other's brief.

The stage worked. The seat did not let it. Its cause was a gauge that kept rendering it as the
constraint -- the same defect as dispatching one row at a time, inverted.

**Why a verifier misses entailment.** A verifier handed the mechanism checks fit, not entailment, and
will quote a disproof out of its own output without seeing it collide.

Reproduction tests the observable, and nobody tests an inference that arrived pre-formed. A false
mechanism with a true symptom and two witnesses is as well-armoured as a wrong claim gets.

**Where self-review is reliable.** Exactly where you already suspected a step could fail. You do not
run a control on a step you did not know was a step.

### A control that shares an origin with what it checks is not a control

Before you trust agreement between two figures, ask whether they **could** disagree. If one derives
from the other, or both from one sample, one ref or one clock, their agreement is arithmetic, not
evidence.

Four instances in 24 hours, four seats:

1. A stale usage sample whose level and countdown corroborate perfectly while four hours out of date.
2. A positive control that ran against the same wrong ref as the query it validated.
3. A hash control that pinned the wrong file, by a method proven correct on a sibling.
4. A panel comparing projections against an expired instant, so every projection fell after it and the verdict could not go red.

| Item | Rule |
| --- | --- |
| A control cannot prove you READ it | A control proves your instrument read the file. It cannot prove you read the output. Where a claim rests on what a line means rather than whether it exists, the check is a second reader, not a second command. |
| And it cannot prove you pointed it at the subject | A control answers *does my instrument work*. It never answers *is my instrument pointed at the subject*. |
| Where it sits | Nearest kin is `CLAUDE.md` SDS-3.8: confirm your instrument answers the question you asked. |
| The one class with no control | A grep printed the correct, complete line, and a quoted string inside a replacement sentence was read as a live rule. |

**The remedy for a mis-aimed control is one sentence nobody writes: state the subject and the control
together** -- ref, repo, file, and the identity you are asserting they share.

Every repository-confusion failure in `INSTRUMENTS` 4.15b survives a control and dies instantly
against that sentence. Only *does my instrument work* is checked by habit.

**This is SDS-3.8's second half:** confirm your control is not answering the same wrong question in
the same wrong way. The rows here are instances of it, not repetitions.

**The downstream class is filed on one instance, not as an established pattern.** Every other failure
here has a broken or mis-aimed instrument behind it. That one has a healthy instrument and a misread
output, so no positive control would have fired.

### An error emitted by your measuring command reads as the subject's

A seat splatted an unquoted row into a `gh` subcommand and got `accepts at most 1 arg(s), received
4`. That is the CLI's own arity error and was never in the CI logs.

It was read as CI failing, escalated through two seats, sharpened into "the gate has been reporting
success by not running", and a filing was directed on it. **The tool behaved correctly throughout.**

**The discriminator, and it beats the fix.** An error whose parameter does not vary with its
supposed subject is not about that subject. "received 4" was constant across two differently-named
checks -- the count tracks the row's field count.

Checkable in seconds from the error text alone, with no access to the system under test: 4 args
gives "received 4" and 2 args gives "received 2".

### A grep's count is a fact about your pattern AND your corpus

Three ways to get a wrong count, and all three return an integer.

| Arm | Failure | Example |
| --- | --- | --- |
| 1 | Wrong pattern | It matched something other than what you meant: a comment naming a banned pattern; a zero for a marker you chose when the fix lived in a helper. |
| 2 | Unread corpus | The file was never opened: a dot-path zero, a `git -C` resolving elsewhere. |
| 3 | Wrong-sized corpus | Read fine, pattern fine, you looked at too little. A one-file grep read as "dead code, zero callers" had four live call sites repo-wide. |

**Two controls, and the first does not cover the third arm.** Prove the corpus was read by piping to
`wc -c` -- that catches arms 1 and 2. Name the corpus in the finding -- that catches arm 3, and no
byte count can see it.

On arm 3 the count comes back in the thousands, the corpus genuinely was read, and the control
passes while the conclusion is still wrong.

**The asymmetry decides which arm actually bites.** Arms 1 and 2 produce a suspicious zero. Arm 3
produces a plausible small number -- one hit, which reads as a finding rather than an error. A zero
invites a second look. A one does not.

**A zero for a marker you chose is not evidence of an absent fix.** Your search term is a hypothesis
about the implementation, and a positive control cannot test it. The grep works, the file is right,
the repo is right, and the zero is real.

A seat grepped a fixed script for `SpecifyKind`, got 0, and nearly reported it unfixed. The fix
lives inside a helper, not at the call site. Verified: `SpecifyKind` returns 0 in that copy while
`ConvertTo-UtcInstant`, the actual fix, returns 1. Read the block, not your guess at how someone
wrote it.

### A careful diagnosis and an untested remedy keep arriving in the same message

Six times on 2026-08-29, from five different seats. The `cat-file` fix inherited the mangling it
fixed. `pipefail` inherited the masking, and `PIPESTATUS` inherited the pipe. The array copy fixed
only clobbering. A mail workaround could not be typed, and a delivery check false-negatived on
success.

**In every one the diagnosis was measured and the remedy was published in the same breath,
unmeasured.** Diagnosis and remedy are different skills, and all the care goes to the first one.

Note what this does **not** claim: nothing about how often remedies fail. Broken remedies are
memorable and correct ones are invisible, so counting only the broken ones selects on the very thing
it would measure. A rate claim was proposed, a denominator was asked for, and the claim was
withdrawn.

**The rate claim needs a count of the remedies that held, and nobody has one.**

| Item | Rule |
| --- | --- |
| A broken remedy in circulation is worse than the bug it fixes | A remedy gets trusted, so a wrong fix is adopted without the scrutiny the symptom would have drawn. |
| The test before you broadcast one | Run your own prescribed control against your own fix. A remedy you have not put through your own gate is a claim, not a fix. |
| The earlier test, which costs nothing | Ask whether your fix routes around the cause or only around the symptom's last step. |

**Two instances in one day.** A dot-path "fix" that failed by the same mangling as the bug, and ran
for twenty minutes before its author's own control caught it. And a belief that an absolute path
defeats an HTTP 429, which would have had seats retry -- and retrying is what produced the 429.

In both, the author had already published the check that kills it: *"pipe to `wc -c` and read the
number"* returns 0 for the broken fix.

**Why the earlier test is cheap.** If your fix and the bug run through the same conversion, parser,
clock or ref, the fix inherits the defect and returns the bug's own failure wearing a fix's
credibility.

Worked case: `cat-file -p $(rev-parse ...)` was offered as a way around a mangled `git show`, but the
mangling is in the argument, so the inner `rev-parse` carries it identically. In its author's words:
*"I swapped the outer command and left the mangling untouched."*

## A green light proves only what the gate asserts

| Item | Rule |
| --- | --- |
| What it asserts | Name the question you asked and what your instrument returns, and make sure they match. |
| The one test | Ask what your instrument prints if the thing you fear is true. |
| Liveness | A count of loaded detectors shows that a gate runs, not that it works. |
| Paired arms | A gate needs a case that must trip and a case that must not trip. |
| Parsed output | Parse the output instead of the number you see on the screen. |
| Gates you hand out | State what you measured a gate against, and on which ref, when you give it to a peer. |
| Suppressions | Write an expiry condition beside every suppression, tied to its cause. |
| Restart | Before you restart a suppressed test, prove that it stays quiet and prove that it wakes. |
| The worst shape | Reject a change that weakens a control and pins the weakness with a new test. |
| A separate reader | An implementer's success report is the item under test, so give the premise to a reader from outside. |
| Enumerations | If a fix removes one hard-coded list, ask which other lists stay hard-coded. |
| Luck | Do not accept "it does not break on this machine" as a mitigation. |
| Silence | If a monitor prints nothing, make sure it ran, because silence and a crash look the same. |
| Error direction | Ask which way your instrument's error pushes you. A test that LIFTS a prohibition fails dangerously. |
| **State which way a new check fails** | Write beside every new check which way it fails. Only one of the two directions will tell you about itself. |

*Error direction* names the LOUD direction: a check that fails OPEN lets something through, and
something downstream eventually alarms.

**The quiet direction is fail-closed, and in a supply-constrained fleet it is the expensive one.** A
dead row costs a builder one screen and is loudly visible. A WITHHELD LIVE ROW costs nobody anything
anyone can see, so nothing ever reports it.

---

### Before retracting a defect you reported, establish that nobody has fixed it

**A green re-check is evidence about the code you ran, not about the claim you made.** Measured: a
seat retracted its own defect writing *"renders correctly WITH NOTHING FIXED"* -- while measuring
the fixer's already-landed commit.

**It is the most credible form of wrong available, because it arrives wrapped as a second opinion.**

**The control: A/B against a commit, never against a working copy you believe is old.** The seat
that caught that retraction hit the identical trap inside the check: its "unpatched" copy already
contained the fix and **both arms agreed**. It got a real answer only by extracting the parent
commit.

Two seats, same trap, twenty minutes apart, on the same question.

**And reproduce the input.** A re-test that does not reproduce the original input is not a re-test. The
failing call received a `DateTime`; the re-test fed a string. The string path was correct and is never
reached -- string 22, DateTime -278, side by side.

---

### A control fired, printed the disproof, and was read past

*One-line rules* says self-review is blind where you did not know a step existed. **Here the step was known,
the control ran, the output was correct, and the seat quoted it** -- and still endorsed a claim the
output refuted.

Measured 2026-08-28. A seat claimed a reader/writer pair was mismatched because **no writer existed**.
An hour earlier the endorsing seat had grepped that very file for its own purposes and printed:

```
$histPath = Join-Path $StateDir "history.jsonl"
Add-Content -LiteralPath $histPath -Value $row
```

and wrote, in its own words, *"usage-collect.ps1 writes history.jsonl but it never runs."*

**Those two cannot both be true. A mismatch requires there to be no writer.** It found the writer, said
so, and then endorsed a claim presupposing its absence. In its own words: *"I did not fail to check. I
checked, got the disproof, and held both propositions without noticing they collided."*

**The symptom was true and the mechanism was false.** Re-verified: the writer is on `origin/main`
and does `Add-Content` to that path. The consuming tool separately documents why it is not a source,
because the statusLine executor never runs under the desktop app.

Both facts hold and neither implies a mismatch.

**What actually caught it was a reviewer who had helped build none of the claims:** it checked seven
items before allocating a number and killed three. That is a **structural** property of the
reviewer, not a discipline the author can adopt.

**Disagreement works when the disagreeing party has not been handed the conclusion**; the endorsing
seat disagreed with nothing because it had been.

---

## "Does it exist" is never "is it working"

**Every check should say which of the two it answers.** Five artefacts measured 2026-08-28, all
reporting CONFIGURATION where the reader needed EXECUTION:

| Instrument | Says | Does not say |
| --- | --- | --- |
| `CronList` | The job is armed | That it FIRED. Cron fires only while the session is idle, so a busy seat skips its own wakeups. |
| `install-git-hooks.ps1 -Status` | Installed | Against WHICH checkout. |
| A seat record | `lifecycle: open` | That the seat is running. Nothing closes it. |
| `fleet.ps1` | `STATE=RUNNING` | Enough on its own, which is why `[WRITER-STALE]` had to be invented. |
| A claim lock | It is held | That the work would have collided anyway. |

**An instrument can manufacture the non-compliance it reports.** Measured 2026-08-29: a hook nagged
that a lane level was stale, the seat ran the command, and the command refused. From outside that is
indistinguishable from a seat ignoring the prompt.

**The gauge both demanded an action and blocked it, then rendered the block as the seat's silence.**

So before you read a board as evidence about a seat, ask whether the seat could have complied. **If you
need a lane's real level, ask the lane.** Do not read an age field or a STALE flag as a fact about a
person.

**And the assumed failure mode is the wrong one: the guard did not become permissive. It became
total.** It refused both directions -- the stamp it was meant to reject AND the ordinary restatement
it was meant to allow.

When a guard breaks, what everyone watches for is permissive: it lets bad things through, and
something downstream eventually alarms.

**A guard that becomes total alarms nowhere. It presents as
silence from the people it blocks** -- which is why this looked like seats going quiet rather than
an instrument failing.

**So when a population goes quiet, ask whether something is refusing them before you ask why they
stopped.** The refusal will not be in your logs; it is in theirs.

**Which copy executes is a property of the resolution path, not of the file name.**

It differed per file across two repositories holding the same two scripts. The reader is reached
through a wired shim that resolves the vault copy first, and is fixed. The writer is invoked from a
nag printing a relative path, which resolves against the seat's own engine worktree, and is broken.

So "the pattern is present on origin/main" was true of both and decided neither.

**The age number is therefore accurate and should be trusted; the writer blocker is real.** A frozen
quote is genuinely old -- it is not a misreported clock.

**Two seats misread this within five minutes, each by a different route, and both routes are already
in this file.**

One ran `cat-file` in the engine against a vault commit, got "not a valid object name", and read a
wrong-repository answer as evidence the fix had not landed. It then broadcast "do not trust the age
column", which is the do-not-check note that cannot self-correct.

The other counted a grep hit in the vault's reader as the defect. It was the fix's own comment
warning against the pattern: correct data, wrong label, and no control would have fired.

### A number that varies with the input record measures the record, not the code

Found by the PM and sharpened by the Role Manager, 2026-08-29 to 2026-08-30.

Two seats measured the same panel edit and got different numbers. One read about 1500 characters
collapsing to 469. The other read 2328 collapsing to 460. Neither measured wrong. The two board records
differed, and the arm reads fields from the record.

So state a control that can fail. Force one record through both versions of the code. Every arm you did
not touch must come back byte-identical. That control does not depend on the record, it is one command,
and a later edit that thins the wrong arm turns it red.

A count cannot do that work. "The arm shrank" is true of the real fix. It is equally true of a version
that merely dropped a field from the record.

The *Identity beats absence* row already owns the underlying principle. This entry names the
case where the shrinking number is itself the trap, and it does not restate that row.
