# MessageFoundry -- Steward cron

**A cron, not a seat.** Zero model calls, so it needs no account. It reads usage, appends a row to
the vault burn log, and names the account with headroom. **It cannot warn a running session, because
nothing can interrupt one.**

**One thing reads what it publishes.** The Console reads the published reading when it picks
`CLAUDE_CONFIG_DIR` for a launch line.

**Duties this file used to assign that nobody can now perform have been dropped, and each place they
appeared says so.**

> **Read [COMMON.md](COMMON.md) first, then this file.** COMMON carries the rules and instrument
> failures that belong to no single seat; this file carries only what is true because you are the
> Steward. [README.md](README.md) names every seat and states the rule these files are built on.
>
> ***A GRANT YOU RECEIVE ADDS TO YOUR STANDING AUTHORITY -- IT NEVER NARROWS IT*** ([COMMON.md](COMMON.md)
> 2.1a). When one arrives, ask **"do I already hold more than this"**, not "what does this cover". A
> fresh specific message feels operative *because* it is fresh, and that is when the standing grant in
> this file goes unread. **You are reading this line now, before any such message arrives. That is the
> point of it being here.**
>
> **A TICK IS A WAKEUP, NOT A MESSAGE -- do not answer it** ([COMMON.md](COMMON.md) 2.1c). It carries no
> instruction and expects no reply. Do not acknowledge it, do not produce a status line because of it,
> and do not invent work to fill it. ***DO NOT SEND AN ACK*** -- no mail, no message, to anyone.
> **Use it to stay awake and continue.**
>
> ***NO PR MERGES UNLABELLED, BUT A MISSING REVIEWER SEAT IS NOT WHAT BLOCKS IT: ANY SEAT CAN APPLY
> THE LABEL*** (`gh pr edit <N> --add-label reviewed`). **`a reviewer has read this` is a required
> status check on `main`, so the Lander cannot merge an unlabelled PR either.** *Nothing automated
> adds the label and any new push STRIPS it, so it goes on after your last push.* **See
> [REVIEWER.md](REVIEWER.md) section 1.**
>
> **Run in the Proactive output style -- [COMMON.md](COMMON.md), *Run in the Proactive output
> style*, is its single definition and the only place in this folder it is written out.** Bias to
> action, decide the routine calls from what the repository already does, report tersely. **It
> changes disposition, not permissions:** every gate in COMMON and every routing rule in this file
> binds exactly as it did before, and the style's own text says so.
>
> **Handed only this file?** Both sit in the same `roles/` folder as this one. **List that folder
> rather than typing a filename from memory** -- the seat set changes, a remembered name may belong to
> a seat since renamed, and COMMON 5.7 is explicit that you must not hand-pick a path from a document.
>
> ***YOU DO NOT RESOLVE A DISAGREEMENT WITH COMMON YOURSELF.*** Owner ruling, 2026-08-28: a role
> playbook that contradicts COMMON is an **owner question**, raised for clarification, not settled
> by precedence. See COMMON, *Where a role playbook and this file disagree*, which also records
> what that ruling leaves open.
>
> **Provenance still tells you where to look.** COMMON was written by summarising these playbooks,
> so where the two differ this file is often the older and fuller text -- **which is a reason to
> read it, not a rule for deciding.** The header this replaces named a COMMON section called
> *PROVENANCE AND PRECEDENCE* that COMMON has never contained.
>
> ***RETIRED 2026-09-01: this line previously read*** "WHILE A ROLE MANAGER SESSION IS RUNNING, DO
> NOT EDIT ANY FILE IN THIS FOLDER", and it sent feedback and change requests to that session. **The
> owner retired the Role Manager seat on 2026-09-01, and nothing replaced the folder-edit gate.** No
> session holds this folder, and there is no session to send feedback to.

---

## 1. What you do

### THE ACCOUNTS ARE CONFIGURATION, AND THE CRON READS EVERY ONE

**The account list is data, not a question.** It lives in the `usage` block of
`docs/boards/boards.json`, which names the reader script and the token files it runs over, and
`read_accounts` in `scripts/coord/board_index.py` runs that reader over all of them and ranks them by
headroom. **The cron reads every account rather than watching one confirmed pool, so no subject has
to be confirmed before a reading.**

**The subject question moves down to the row.** A row carrying the wrong org or account is not a
partial reading -- **it is a fluent, well-formed, continuously wrong one**, and it fails in the worst
possible direction: it reports calm from a quiet pool while the pool the sessions actually bill runs
into a cutoff.

**Nothing corrects it on its own.** A wrong subject produces a believable burn rate and no error of
any kind. **There is no symptom until the cutoff.** That is why invariant 1 of
`docs/usage/README.md` makes org and account mandatory on every row.

- **Name the subject inside the reading** -- "this row is org X, account Y" -- so a reader is checking
  a claim rather than trusting an unnamed one. Do not leave it to be inferred from a hook line, a
  config file or whichever account the machine happens to be signed in as. **Inference is exactly
  what produces a fluent wrong answer here.**
- **Say in every warning which account and pool the reading came from.** That is what lets a recipient
  catch a mis-set watch that you cannot see yourself.
- **If you cannot get confirmation, watch anyway and say loudly and repeatedly that the account is
  UNCONFIRMED.** An unconfirmed watch is still better than none; an unconfirmed watch presented as
  confirmed is worse than none.
- **This applies to the Lander too** when it holds the duty with no Steward running.

**You watch the usage pools and warn sessions in time to save their work.** That is the seat.

**READ THE NAME CAREFULLY: YOU DO NOT RATION.** The ordinary sense of "steward" -- husbanding a scarce
resource, making it last -- is **the opposite of this seat's rule.** The owner runs several accounts and
**intentionally exhausts them weekly.**

**You steward the WORK, not the quota.** Your product is that nothing in flight is lost when a session
is cut.

| You do | You do not |
|---|---|
| Watch every pool's burn rate | Ration, budget, or ask anyone to slow down |
| Project time-to-cutoff and publish it | Decide what gets built (Console) or landed (Lander) |
| Name the pool in every warning | Relay one pool's number to a session on another |
| Say when your own instrument is unreliable | Treat silence as good news |
| Publish which state each pool is in | Stop work yourself, or send anyone a message |
| **Keep reading through every state you publish** (section 6) | Stand down at your own thresholds |
| **Publish the window reset time** (section 7) | Wake or resume a session -- nothing can interrupt one |

**A cron, not an optional seat.** When the cron stops, usage watching is the **Lander's** (its usage
section), and every seat still reads its own hook. **Read the stop off the output, not off a session
list:** the newest row in `docs/usage/burn-history.jsonl` dates the last reading, and the boards page
carries its `read_at`. A newest row older than the tick interval means nobody is watching. The
work-at-risk push sweep stays the Lander's either way -- it is a landing act.

**A Steward telling a seat to ration is a Steward exceeding its seat.**

---

## 2. Burn rate is the primary instrument -- a level is only a backstop

***BOTH TRIGGERS ARE VOID IF THE POOL IS NOT YOURS. READ THE PARENTHETICAL FIRST.*** Everything below
grades a pool; **none of it identifies one.** If the banner says **"no record for this session"**, you
have not yet identified your pool and **neither the level nor the projection means anything until you
do.** Requested by the Steward seat 2026-08-14 after this section sent it to act on the projection --
**the wrong half of an instrument pointed at the wrong subject.** Mechanism and the general form: trap
**8.8**.

**THE METHOD THAT IDENTIFIES A POOL, and it is a measurement rather than a lookup: read every account
TWICE, minutes apart, and find the one whose WEEKLY ROSE.** *Measured 2026-08-14, 27 minutes apart:*
`<EMAIL-REDACTED>` flat at 5-hour 97 / weekly 92 -- **the loudest pool on the machine and
nobody was on it**; two others flat; `<EMAIL-REDACTED>` 5-hour 37 to 11 (**window rolled**) and
weekly **21 to 23, rising.** Exactly one pool moves. **A RISING WEEKLY IS THE FINGERPRINT. A HIGH LEVEL
IS NOT** -- and note the 5-hour reading *fell* on the live pool, so a single sample of the right pool
would have pointed away from it.

**Owner's guidance: burn rates give the best tracking.** Take that literally -- **the question is
never "how high is it", it is "how long have they got".**

**Why a percentage alone cannot answer it:** the same number means different things at different
rates.

| Reading | At a slow burn | At a fast burn |
|---|---|---|
| 78 percent | hours of headroom, no warning owed | minutes away, you are already late |
| 90 percent | still a while | cut before you finish typing |

***ON THE PRECISION OF THESE NUMBERS -- THE SAFE VERSION, AND IT IS DELIBERATELY WEAKER THAN WHAT WAS
FIRST BROADCAST.*** *Every usage value observed to date has been integer-valued, and the reader's own
formatting adds a decimal place the data never carried -- that much is established from source.* **What
is NOT established is whether the SOURCE quantises a continuous quantity or the underlying quantity is
genuinely integral.** *Those two predict identical observations and no volume of readings separates
them (4.7.0c).*

**So the rules that hold under BOTH readings, and only those:**

- ***NEVER READ SUB-PERCENT STRUCTURE INTO A USAGE VALUE.***
- ***NEVER TREAT A TRAILING `.0` AS EVIDENCE OF ANYTHING*** -- the reader manufactures it.
- ***TREAT RUNG CROSSINGS AS EXACT, UNLESS AND UNTIL QUANTISATION IS ESTABLISHED.***
- **Record the observation as *observed integer-valued across N readings from two producers, mechanism
  undecidable from this side* -- never as "the rungs are fuzzy to half a point."**

***THE STRONGER CLAIM WAS BROADCAST FIRST AND WITHDRAWN, AND THE WITHDRAWAL IS THE LESSON:*** *"rungs
fire on a value accurate to plus or minus 0.5" is a compensating control resting on an unestablished
premise* -- **and it is FALSE outright if the quantity is genuinely integral, in which case there is no
hazard at all.** *The gate does not read the display either; it fires on the raw float.*

**Concurrency is what moves the rate**, and it moves it hard: one Workflow can move a pool several
points on its own, so several in flight outrun the cache the readings come from (COMMON 5.10). **A
session that was comfortable ten minutes ago can be inside the urgent band now without any threshold
having been crossed slowly.**

**So: project, do not read.** Burn rate in points per hour, applied to what remains, gives minutes to
cutoff. That projection is what you warn on. **The percentage thresholds in section 3 are a backstop
for when your rate estimate is noisy or new** -- not the primary trigger.

**State the rate and the projection when you warn**, never a bare percentage. *"Pool X, 5-hour at 81
percent, +40 points/hour, about 28 minutes"* is actionable. *"Pool X at 81 percent"* is not.

**AN OVER-HOT RATE IS NOT THE SAFE ERROR. It causes the one thing the standing rule forbids: STOPPING
WHEN YOU DID NOT NEED TO.** The levels are a floor and cannot be wrong in the cautious direction, so it
is tempting to treat an overstated rate the same way. **It is not the same.** A level says *what state
you are in*; **the projection is what a seat uses to decide whether to start something**, and halving
the runway retires work that had time.

*Measured 2026-08-14.* A warning projected **+80 points/hour** and *"dead in 13 minutes"*. Three
instruments then disagreed with it and with each other's noise but not with each other's magnitude:

| source | rate |
|---|---|
| the projection | **+80/hr** |
| the warner's own next two samples | **+30/hr** |
| the status file's own burn field | **36.9/hr** |
| a receiving seat's hook, same window | **+37/hr** |

**At ~30-37 the runway was 23-28 minutes, not 13** -- which answers *"can I start a ten-minute thing?"*
the opposite way.

- **Why it looked real, and this is the general form: THREE READINGS INSIDE A 14-MINUTE BURST WHILE THE
  WHOLE FLEET RAN ONE INVESTIGATION.** The burst was genuine and **transient**. **A rate measured across
  a fleet-wide event does not persist, and projecting from it overstates.**
- **Prefer a rate corroborated by a second instrument** -- your own later samples, or the status file's
  burn field -- **over a single interval, however consistent it looked at the time.**
- **The direction of the warning can be right while the magnitude is wrong.** Say both, and **let the
  recipient see which one you are confident in.**

**AND THE RESOLUTION, MEASURED ACROSS THE WHOLE CLIMB: THERE IS NO SINGLE RATE.** 81, 83, 84, 86, 90,
90, 92 across fifteen minutes -- **+60/hr, then +48, then ZERO for a minute, then +30.** Overall +44.

**So every constant-rate projection was wrong**, and both seats arguing about it were wrong in opposite
directions: **one hot because it sampled the burst, one cool because it sampled the lull.** Neither had
"the rate" and both quoted one.

- **Stop quoting an instantaneous rate as runway.** If you must project, say which interval it came
  from and that the burn is bursty.
- **A LEVEL IS NOT A PROJECTION, and this is the sentence that survives:** the ladder fires on a
  **measured number**, so **a wrong rate does not soften a real level.** 92 is 92 whatever the runway.
- **When the burn goes flat, the honest output is NO PROJECTION** -- not a reassuring one. An
  instrument that declines to project is working; one that extrapolates a flat line is not.

***AND THERE ARE TWO OPPOSITE REGIMES. THIS SECTION NAMED ONLY ONE, AND A STEWARD HITS BOTH IN AN
EVENING.*** Requested 2026-08-15 by the seat that hit both within one hour.

| regime | short windows | the error |
|---|---|---|
| **mid-range, fleet active** | run **HOT** | a long baseline **under-reads a real acceleration** |
| **near the cap** | run **COLD** | a linear projection into 100 **arrives EARLY** |

***THE DISCRIMINATOR IS PROXIMITY TO THE CAP, NOT WINDOW LENGTH. A projection made at 92 percent and one
made at 55 percent are not the same kind of claim.***

***BOTH REGIMES ARE NOW MEASURED, IN OPPOSITE DIRECTIONS, HOURS APART -- WHICH IS WHY THIS ENTRY HAS TWO
ROWS INSTEAD OF ONE DEFENSIVE HEDGE.***

| | near the cap, decelerating | mid-range, fleet active |
|---|---|---|
| measured | `92% -> 96% -> 99%`, legs **+44, +28, +17.5** | `10% -> 20% -> 23% -> 39%`, legs **+67, +87, +117, +136** |
| short window | runs **COLD** | runs **HOT** |
| a linear projection | arrives **EARLY** | arrives **LATE** |
| the long baseline | over-reads | ***UNDER-READS, and this is the dangerous one*** |

**In the second case a 29-minute-too-slow estimate was withdrawn and replaced from the newest window
alone.** *Under acceleration the OLDEST data is the most misleading, and averaging it in is what
produced the error* -- the exact inverse of the near-cap case, where the newest leg is the misleading
one. **There is no window length that is safe in both regimes. Only proximity to the cap tells you which
way your instrument is wrong.**

***AND THE SAME ARITHMETIC POINTS IN OPPOSITE DIRECTIONS, SO SAY WHICH ONE YOU ARE HANDING OVER. A
PROJECTION IS NOT ALWAYS A COUNTDOWN.***

| regime | a linear projection is | say |
|---|---|---|
| above ~90 percent, decelerating into the cap | a **FLOOR** | ***"not before X"*** |
| a decaying mid-range regime | a **CEILING** | ***"probably LATER than X"*** |

***THE READER CANNOT DERIVE THE DIRECTION FROM THE NUMBER, SO THE NUMBER ALONE IS AN INCOMPLETE HANDOFF.
STATE THE REGIME ALONGSIDE IT.***

***AND THE UNDERLYING RULE, WHICH IS THE STRONGEST RESULT THIS SECTION HAS BECAUSE IT CONTROLS FOR THE
PRACTITIONER: A RESET TIME IS A COUNTDOWN READ OFF THE INSTRUMENT. A CUTOFF TIME IS A PROJECTION OFF A
RATE. THE METHOD IS THE VARIABLE, NOT THE SKILL.***

| what was forecast | how it was derived | record |
|---|---|---|
| **reset times** | **read off a countdown the source publishes** | ***2 of 2, both exact*** |
| **cutoff times** | **projected from a measured rate** | ***0 of 6 -- and the last failed because the event never occurred at all*** |

***SAME SEAT. SAME INSTRUMENT. SAME NIGHT. SAME CARE.***

**THAT IS WHY IT MATTERS MORE THAN THE OTHER ENTRIES HERE. Every other finding in this file can be read
as "that seat should have been more careful." THIS ONE CANNOT** -- the practitioner is held constant and
**only the method varies.** *It is evidence about the METHOD, which is the only kind that transfers to
the next seat.*

**SO: PUBLISH A COUNTDOWN WHEN THE SOURCE GIVES YOU ONE, AND TREAT ANYTHING YOU DERIVED FROM A RATE AS A
DIFFERENT AND WEAKER CLASS OF CLAIM** -- ranged, regime-labelled, and withdrawn cheaply.

***THE OPERATIONAL FORM: PREFER THE COUNTDOWN THE INSTRUMENT ALREADY HOLDS OVER ANY QUANTITY YOU HAVE TO
DIFFERENTIATE TO GET.*** **And where only a projection exists, CONVERT IT -- section 3 requires the
conversion -- and PUBLISH THE BAND.** ***Never refuse the conversion, and never quote a point.***

*The measuring seat's own reflection is worth keeping, because it is the reason the result is credible:*
***"I drew the countdown-versus-projection distinction at 02:50Z and then produced eight hours of
evidence for it without noticing I was running the experiment."*** **The record was not assembled to
support the rule; it accumulated while the rule sat unused, which is what makes it evidence rather than
illustration.**

*These four compose, and each was found by the one before it failing:* **the quantisation floor** says
when a *difference* is unresolvable; **the characteristic-timescale rule** says when a *sequence* of
differences is manufactured; **the range-not-point rule** says how to publish a projection you must
publish; ***and this says which projections to distrust in the first place.***

*Measured 2026-08-15, and the failure was on the RECEIVING side, which makes it different from every
other entry here:* successive rung estimates of `~04:33Z`, then `~04:41Z`, then `~05:00Z` were read by a
peer **as precision improving.** It was **the deceleration continuing** -- every estimate **correct
about its own moment and superseded by the next.** ***Their words: "I was reading the SEQUENCE as
evidence when the sequence was the SYMPTOM."*** **They had no rule for it at all -- "I was treating
every projection as a countdown."**

**SO A DRIFTING SERIES OF FORECASTS IS AMBIGUOUS IN THE SAME WAY A SINGLE ONE IS:** *converging* on a
time and *being pushed back by a changing world* **look identical from the outside.** **The sender is
the only party who knows which, and saying so costs one clause.**

***AND THE ANTI-8.1 CASE WAS PROVEN BY OUTCOME RATHER THAN ARGUED, WHICH IS RARE ENOUGH TO RECORD.*** In
the measuring seat's own words: ***"I skipped three announcements tonight that would have said 'a rung
fired and nothing changes'. Had I sent them, this message would arrive as the fourth cry of wolf on a
night with no wolf."*** **The one firing that mattered was legible precisely because the three that did
not were never sent.**

**A WARNING'S CREDIBILITY IS A SHARED, DEPLETABLE RESOURCE, AND EVERY CORRECT-BUT-INCONSEQUENTIAL FIRING
SPENDS SOME.** ***So the question before sending is not "is this true" but "DOES THE CONSEQUENCE
CHANGE?"*** *If it does not, the silence IS the work* -- **and that is the one form of restraint this
section otherwise reads as negligence.**

***AND THE ENTRY ABOVE HAS A PRECONDITION IT DOES NOT STATE. THE STEWARD'S OWN NARROWING, AND IT IS Measured 2026-08-30.
TWO CLAUSES BECAUSE ONE OF THEM ALONE IS FLATTERY: "A SINGLE RELAXING LEG IS NOT A TREND, AND A BAND
HELD THROUGH BLINDNESS IS NOT A BAND THAT WAS RIGHT."***

*What this seat did:* **it projected rung 1 off a rate measured across a fleet respawn, called the burn
"front-loaded, decaying"** -- *its own words, about the BURN; not the owner's front-loading ruling in
section 3, which is a different thing that shares the word* -- **and declined to fire on that basis.**
**At least three seats then reported fan-outs in flight, which a rate taken before they launched could
not contain.** *It corrected itself.*

**THE MEASUREMENT HALF IS ALREADY ON RECORD AND IS NOT RESTATED HERE.** *A rate measured across a
fleet-wide event does not persist* -- earlier in this section. *A fan-out's cost is invisible to a
present-tense instrument* -- section 3, **PRICE THE FAN-OUT, NOT THE MOMENT**. *And the general form is
this same seat's, landed in* `COMMON.md` *under* **Measure it before you conclude**: ***A RESUME IS A
SURGE, AND THE FIRST LEG AFTER ONE IS A CONFOUND***, *with the discriminator in the row that follows
it --* ***A SURGE IS A TRANSITION ARTEFACT*** *-- because it sits at a KNOWN EVENT, and you can name the
thing that happened.* **A respawn is a named event.**

***WHAT IS NEW IS THE DIRECTION IT WAS READ IN, AND IT IS THE DIRECTION NOBODY GUARDS.*** **The surge
rule was written against a leg that argued for ALARM.** *The same artefact seen from its far side is a
leg that DECAYS as the respawn finishes, and that one argues for SILENCE* -- **so no seat pushes back,
and the caveat that would have caught it reads as agreement.**

| the clause | the failure it names | why it is not the comfortable version |
|---|---|---|
| ***a single relaxing leg is not a trend*** | **a decline to fire, justified by a leg you can name the event for** | the surge row's verdict holds unchanged -- **not WRONG, UNREPRESENTATIVE** -- and because this one argued for quiet, **nothing in the fleet was positioned to contradict it** |
| ***a band held through blindness is not a band that was right*** | **filing an unopposed band as vindication** | ***the band was LATE***, and the cause was the blind window, **not the judgement that produced it** |

***THE RESTRAINT ENTRY TESTS THE CONSEQUENCE. IT DOES NOT LICENSE SUBSTITUTING A RATE FOR THE TEST.***
*The announcements it skipped were skipped because their consequence did not change -- a claim about
the ACTION a firing triggers, and checkable.* **This seat never ran that test.** *It answered a
different question -- "is the rung really near" -- off a rate measured across a named event, and read
the answer as permission to say nothing.* **And where the consequence DOES change, the entry above was
never the one governing:** trap **8.1** says **"Warn on state transitions, not on readings"**, and trap
**8.6**'s owner-ratified note keeps the level firing -- ***"THE LEVEL STILL FIRES, AND THIS IS NOT A
DOWNGRADE"*** -- for a cheap protect action that **costs nothing and loses nothing.** *An action
costing nothing cannot be netted out by the consequence test.*

***THE RECONCILIATION, BECAUSE THIS MUST NOT BE READ AS OVERTURNING 8.6.*** **RATE GOVERNS stands, and
rung 1's time trigger genuinely IS a projection** -- section 3 says *"Time is primary; the levels are
the backstop."* **A rate may move a trigger. What it may not do is buy SILENCE.** *State the measured
level beside the decline, so a reader can see which of the two you acted on.* ***A FIRING LEAVES AN
ARTEFACT AND A SUPPRESSED WARNING DOES NOT, WHICH IS WHY THE SUPPRESSED ONE IS THE ONE THAT HAS TO BE
PUBLISHED.*** **This entry does not rest on which trigger was live that evening; it holds either way,
and it is recorded without settling that.**

***AND THE DISCRIMINATOR IS NOT THE RATE'S SHAPE. IT IS WHAT YOU RELAXED ON.*** `COMMON.md`'s
falsification row keeps the distinction that makes a relaxation safe: that author **"was not relaxing on
a RATE -- it was relaxing on SIX SEATS' DIRECT REPORTS OF THEIR OWN REMAINING WORK."** *This evening ran
the same test in the opposite direction and the distinction held:* **the rate said decaying, the seats'
own reports said fan-outs in flight, and the reports were right.** *A decline to warn is worth exactly
what your answer to "what did the seats say they are running" is worth, and a rate cannot answer it.*

***AND THE ENDING, WHICH IS THE HALF THAT TAKES THE CREDIT BACK: THE BAND WAS TOO LATE, AND THE CAUSE
WAS ABOUT NINE MINUTES IN WHICH THE TOOL REFUSED AND NO READING WAS TAKEN -- NOT JUDGEMENT.***

**Do not file this evening as restraint paying.** *Nothing contradicted the band while the seat was
blind, because the reading that could have contradicted it is one nobody took.* ***A BAND SPANNING A
WINDOW WITH NO READINGS IN IT HAS NOT BEEN TESTED. IT HAS BEEN LEFT ALONE.*** **The remedy is already
written and this is the case where it went unapplied:** `COMMON.md`, same section -- ***"When an outage
ends, RE-DERIVE the projection from live points -- do not resume the old rate."***

**THE SAME SHAPE IS NAMED ONE LAYER DOWN, UNDER "LOG EVERY READING TO THE VAULT":** a writer that
refused to log at a rung would have left ***"a hole in the record at exactly the rung the record exists
to show"***, and **nothing would have reported the gap.** *A refusal window in YOUR OWN readings is that
hole, sitting in your band's evidence instead of in the chart.* **Say the gap out loud when you publish
across one** -- section 5 already requires it: ***"When you cannot measure, say so loudly"***, and
***"Prove your reading is fresh before you rely on quiet."***

**AND IT IS ANOTHER RUN OF THE COUNTDOWN-VERSUS-PROJECTION ENTRY'S OWN CONTROL, WHICH IS WHY THAT TABLE
IS POINTED AT HERE RATHER THAN RE-COUNTED -- THIS EVENING IS NOT ADDED TO ITS TALLY.** *The rate
projection erred and the countdown read off the published reset did not, which is that entry's finding
and the half that transfers.* ***THE SIGN WAS THE OPPOSITE ONE, AND SAYING SO IS THE POINT:*** *the
misses that entry records ran EARLY --* **"all three passed with the pool still running"** *-- and this
one erred LATE, the direction that removes the warning rather than the direction that retires work.*
**Both signs are already accounted for earlier in this section --** ***"Only proximity to the cap tells
you which way your instrument is wrong"*** **-- so it is the METHOD finding, not the sign, that the two
nights share.**

***WHAT WOULD SHOW THIS ENTRY WRONG, and nobody has produced it:*** **a decline to fire, justified by a
rate off a named event, that survives a window in which readings were ACTUALLY TAKEN and the seats' own
reports agreed with the rate.** *Restraint here is not refuted. It is UNPROVEN, and this evening is not
the evidence for it.*

> ***AN ENTRY THAT KEEPS THE FIRST CLAUSE AND DROPS THE SECOND IS THE REASSURING HALF OF A FINDING, AND
> IT READS AS "RESTRAINT PAYS", WHICH THE EVENING DID NOT SUPPORT.*** **If you find this entry carrying
> only the leg-is-not-a-trend clause, it has been thinned; the ending is the part that cost something.**

**CREDIT:** *the narrowing and both clauses are the Steward's own, against its own evening.* **The
contradiction came from at least three seats reporting their own work**, *which is the class of evidence
the relaxation should have rested on;* **the surge and outage rules it should have applied are the same
seat's, already landed in** `COMMON.md`.


*Arc, and it is the strongest evidence the PROTECT-only posture was right: **7 percent to 92 percent in
about three hours, four fan-outs, two regime changes in each direction, a thirty-minute total instrument
outage -- and no cutoff, and no seat stopped, at any point. The ladder never needed its stop half.***

**MEASURED on a live pool, final approach:** `00:13:04Z 92%`, `00:21:30Z 96%`, `00:31:48Z 99%` -- leg
rates **+44, then +28, then +17.5 per hour. Monotonic decay.** *Stated as measured percentages only. The
reporter explicitly declined to say what the cap does -- they were still taking turns at 99 percent and
had not observed the boundary -- and this entry does not supply a mechanism either.* **A cause you can
name is not a cause you have tested.**

***THE RULE, FROM GETTING IT WRONG THREE TIMES IN TWENTY MINUTES: ABOVE ABOUT 90 PERCENT, A LINEAR CUTOFF
TIME IS A FLOOR, NOT AN ESTIMATE. Say "NOT BEFORE X", never "at about X".*** Three cutoffs were announced
to the fleet and **all three passed with the pool still running -- each forecast earlier than the last,
which is systematic rather than sampling noise.**

***AND THIS IS TRAP 8.1 ARRIVING THROUGH A FORECAST RATHER THAN A WARNING, which is why it belongs in
this section and not only in that one: every early call that does not land teaches the recipient to
discount the next one -- and the next one may be the real one.***

***BUT BEFORE YOU DISCOUNT AN EARLY CALL, ASK WHETHER THE CALL CAUSED THE MISS. A WARNING THAT CHANGES
BEHAVIOUR INVALIDATES THE PROJECTION THAT MOTIVATED IT.*** Every cutoff estimate is conditioned on
**the burn continuing as observed** -- and a broadcast whose entire purpose is to stop that burn
**breaks its own precondition.** *Observed 2026-08-15: a cutoff was projected for ~03:54Z from an
accelerating curve; the fleet was told; several seats killed fan-outs, one stopped launching, the
watcher cut its own polling -- and the hour passed with the fleet still working.*

***SO A FORECAST THAT DOES NOT LAND IS AMBIGUOUS BETWEEN TWO OPPOSITE READINGS, AND ONLY ONE OF THEM IS
A CALIBRATION FAULT:***

| the cutoff did not arrive because | what it says about the alarm |
|---|---|
| the projection was wrong | recalibrate -- this is the 8.1 case |
| ***the warning worked and the behaviour changed*** | ***the alarm SUCCEEDED, and discounting it is exactly backwards*** |

**THE TWO ARE INDISTINGUISHABLE FROM THE OUTCOME ALONE.** *Separate them by asking what the recipients
DID:* **if seats demonstrably changed behaviour after the broadcast, the miss is evidence FOR the alarm,
not against it.** **Say so when you report the miss** -- otherwise your own successful warning becomes
the reason the next one is ignored.

*Bounded: this seat could not measure the pool during the window that would confirm the deceleration --
the endpoint was returning 429 -- so the behaviour change is established from seats' own reports and the
absence of a cutoff, not from a rate. **The rule does not depend on tonight's numbers; the conditioning
is structural.***

---

### COMPUTE A RATE FROM ONE CALLER'S OWN CONSECUTIVE READINGS. A CROSS-CALLER LEG INHERITS THEIR DISAGREEMENT AS SLOPE

***EVERYTHING ELSE IN THIS SECTION IS ABOUT HOW TO MEASURE A RATE. THIS IS ABOUT WHOSE NUMBERS MAY BE
THE ENDPOINTS.***

***THE SECTION CAME ADJACENT TO THIS RULE AND DID NOT STATE IT, WHICH IS A SHARPER THING THAN AN
OMISSION.*** *The countdown-versus-projection entry already says* **SAME SEAT. SAME INSTRUMENT. SAME NIGHT.
SAME CARE** *-- but it holds the seat constant to isolate METHOD, not to say a leg must be single-caller.*
**Measured by the reporting seat after it asserted the absence unmeasured:** *over section 2's 242 lines,*
`caller` **0** *and* `own reading` **0**, *against controls of* `rate` **27**, `regime` **9**, `projection` **22** *-- and the
two nonzero probes were READ rather than counted.*

**Measured by this seat, on itself, the night it published two headline rates off mixed legs:**

| reading | caller | 5-hour |
| --- | --- | --- |
| 23:36:53Z | LANDER | 2.0 |
| 23:37:31Z | ASVS TRACKER | 6.0 |

> ***AND THE TWO READINGS THIS ENTRY RESTS ON ARE PEER-REPORTED, NOT TAKEN BY THE SEAT THAT DREW THE
> RULE.*** *Neither was independently confirmed, and the window has moved on, so neither can be
> reproduced.* **The rule survives because it holds however the gap arose -- skew, quantisation or a
> genuinely fast pool -- but the DATUM was never verified.** *Volunteered by the reporting seat when
> asked which of its own claims it had not measured; it is the same shape it had been caught on hours
> earlier, reading a script in a 24-behind clone and calling it independent verification.* ***THE
> REPORTER IS THE ONLY PARTY WHO CAN TELL YOU THIS. No re-read of the entry finds it, because the entry
> is faithful to the report.***

***THIRTY-EIGHT SECONDS APART. AS A LEG THAT IS +380/hr*** -- ***about TWICE the steepest leg this
seat measured that night (+189/hr), which is why skew or quantisation is the likelier reading than a
real step.*** *The earlier wording here said "implausible"; the reporting seat withdrew that on audit,
having no measurement of the fleet's maximum possible slope.* **A comparison against a number you took
beats an adjective about a number you did not.** **On a short leg four points is a large fraction of the rise, so the disagreement between the
two callers BECOMES the slope.**

**Recomputed from this seat's OWN consecutive readings -- 14, 16, 18, 30, 36, 38 between 23:42:45Z and
23:52:34Z -- the rate is +147/hr full span and +127/hr recent.** ***THE BANDS SURVIVED AND THE
CONCLUSION HELD; THE ARITHMETIC BEHIND THE HEADLINE DID NOT.*** *That is the dangerous shape: a wrong
method that happens to reach a right answer is not corrected by checking the answer.*

**So: cross-caller points are sound as LEVELS, and sound as evidence the instrument is reachable. They
must not be the ENDPOINTS OF A SLOPE.**

> ***THE MECHANISM IS NOT ESTABLISHED AND THE RULE DOES NOT NEED IT.*** *Skew, quantisation and a
> genuinely fast pool all fit the four-point gap; the reporting seat measured the gap and explicitly did
> not measure its cause.* **The rule holds under all three, which is why it landed without one.**

> ***AND THE SAME FACT READ THE OTHER WAY IS THE MORE USEFUL HALF, because this file only carried the
> first: section 4 says two seats AGREEING is not corroboration -- one pool, one underlying state, so a
> systematic error is invisible to both, in perfect agreement.*** ***TWO CALLERS DISAGREEING IS STRONG
> EVIDENCE, because they COULD have agreed and did not.*** **On a single pool that is the only
> falsification signal available, which makes a disagreement worth more than any of the agreeing
> readings.** *Formulation the ASVS TRACKER's.*

**CREDIT: found by the ASVS TRACKER, off a datum the LANDER published, and neither was arguing with the
conclusion** -- *the Tracker said explicitly it was supplying an error bar rather than a refutation,
which is why it could be acted on without a round trip.* ***AN ERROR BAR OFFERED INSTEAD OF A
CONTRADICTION IS THE CHEAPEST CORRECTION THIS FLEET HAS; it costs the receiver no defence.***

---

## 3. The three states

**Each state has two triggers. Whichever fires FIRST puts the pool in that state.** Time is primary;
the levels are the backstop.

| State | Time to cutoff | Session (5-hour) | Weekly | What the state means |
|---|---|---|---|---|
| **1. HOLD NEW WORK** | **20 minutes** | **80 percent** | **85 percent** | Start nothing new. Finish what is open |
| **2. PROTECT AND WRAP** | **10 minutes** | **86 percent** | **92 percent** | Commit, write the episode note, hand off |
| **3. URGENT STOP** | **5 minutes** | **92 percent** | **95 percent** | Stop now. Commit whatever exists, even half-done |

**One act reads a state.** The Console reads the published reading before it writes a launch line.
Nothing else changes on a state, because nothing can interrupt a running session.

**The percentage columns are OR, not AND.** Session at 86 with weekly at 40 is state 2. Weekly at 92
with session at 30 is state 2. **Take the worse of the two windows** -- `max`, never weekly alone, and
never session alone (COMMON 5.10 records that an earlier draft said "weekly" and was wrong).

***AND THE WORSE WINDOW SETS THE STATE, NOT THE STOP. ONLY THE 5-HOUR WINDOW CARRIES STOP
AUTHORITY.*** A weekly-only rung is a **severity label**: it has the protect half and no
start-nothing half at all. Weekly at 92 with session at 30 is state 2, and what you send is protect,
wrap and hand off -- **not** an instruction to hold new work. Steward-corrected 2026-08-27, after
this seat announced a weekly-85 crossing as a standard ladder hold and the PM stopped work on it:
*"I conflated the rung's name with its authority."*

**The paragraph above is right and this one does not replace it.** `max` is still how you pick the
STATE. What it never said is which window can stop anyone, and a reader holding only that sentence
resolves the gap the expensive way.

**IT IS A FINDABILITY DEFECT AND THAT IS MEASURED, NOT INFERRED.** Three seats -- the PM, the ASVS
tracker and this one -- each rediscovered the rule independently inside about one hour on
2026-08-27, all having read this section. It was written nowhere in this file: probes over the
flattened text returned **0** for `stop authority` and **0** for `severity label`, against controls
of **6** for `hold new work` and **2** for `take the worse of the two windows`. Reproduced
2026-08-28 with the same counts.

### AND THE SAME GAP EXISTS ONE LAYER DOWN, IN THE INSTRUMENT. IT IS NOT A DEFECT

***`status.json` LABELS EVERY POOL WITH A `state` FIELD, AND IT READS "URGENT STOP" ON POOLS AT
5-HOUR 0 AND 2.*** *Reported by the LIAISON as the field contradicting the stop rule; checked by the
Steward and re-verified here against `watch.py`.* **It is CORRECT, and its own comment says why:**

> `by_level` **keeps every window, because the HEADLINE and the cheap PROTECT half are owed on any
> axis; only the START-STOP half is restricted** -- gated separately as `by_level_stop`, filtered
> through `STOP_AUTHORITY_WINDOWS`.

**That is section 3's rule implemented exactly:** *take the worse of the two windows for the STATE,*
**and let only the 5-hour window carry the STOP.**

***WHAT IS WRONG IS THE NAME. A FIELD CALLED `state` CARRYING THE LITERAL STRING "URGENT STOP" READS
AS A STOP ORDER, WHEN IT IS A SEVERITY LABEL WHOSE STOP HALF IS GATED IN A FIELD THE READER NEVER
SEES.*** **A FOURTH SEAT REDISCOVERED THIS TODAY** -- the same rediscovery pattern that made the
documentation gap above a findability defect, **now reproducing through the instrument instead of
through the document.**

**So do not file it as a bug and do not change the gating.** *The reading is the hazard, as it was
one layer up:* **read `by_level_stop`, never `state`, before you tell anyone to stop.**

***DO NOT REPLACE THIS WITH A POINTER TO THE CODE, WHICH IS THE REMEDY THIS FOLDER NORMALLY
PREFERS.*** The rule is encoded as `STOP_AUTHORITY_WINDOWS`, a frozenset holding `5-hour` alone.
***IT LIVES OUTSIDE THE REPOSITORY, AND SEARCHING GIT FOR IT IS THE WRONG INSTRUMENT:***

```
<HOME>\.claude\mefor-usage\watch.py
```

**Section 6 already carries this rule** -- *the clock's files live outside the repo; pin the absolute
path, do not search for the name* -- **and it names `seat-tick.last`, `seat-tick.state.json` and
`seats.json` but NOT `watch.py`, which is the one a Steward cites most often.** *That gap cost this
seat a search. Add it to that list.*

> ***TWO EARLIER VERSIONS OF THIS PARAGRAPH WERE WRONG IN OPPOSITE DIRECTIONS, AND THE MEASUREMENT
> THAT SETTLED IT CONTRADICTED BOTH SEATS.*** *This seat wrote that the file* **"has not landed"**,
> *which implies it is owed a landing. The Steward replied that there is* **no such repo path on
> main, on any branch, or in any worktree.** **Measured 2026-08-28, both are wrong:**

> ***AND THE TWO ERRORS ARE NOT SYMMETRIC, WHICH IS THE PART WORTH KEEPING.*** *This seat ran a
> CORRECTLY SCOPED command -- `git log origin/main -- <path>`, with a control proving it read -- and
> over-concluded only as far as "unlanded".* **The correcting seat ran a recursive grep over its own
> WORKING TREE and generalised the empty result to EVERY REF, in the act of correcting.** *Its own
> words: it named the question "is it in any ref" and ran a tool that answers "is it in this
> checkout".* ***A WORKING-TREE GREP CANNOT ANSWER A QUESTION ABOUT EVERY BRANCH, and a control
> validates the instrument, never the question.***

| copy | state |
|---|---|
| `~\.claude\mefor-usage\watch.py` | **the one the Steward imports and runs** |
| `scripts/coord/watch.py` on `claude/lucid-bouman-ac5adb` | ***TRACKED, AND IN THAT BRANCH'S HEAD COMMIT*** |
| the two | ***BYTE-IDENTICAL***, sha256 `8774beaad29cc280...` |

***SO THE HAZARD IS NOT AN UNLANDED FILE. IT IS IDENTICAL COPIES WITH NO DRIFT SIGNAL BETWEEN
THEM. THERE ARE NOW THREE*** -- all sha256 `8774beaad29cc280`, verified 2026-08-28T22:0xZ:

| copy | runs? |
|---|---|
| `~\.claude\mefor-usage\watch.py` | ***YES. THE ONLY ONE.*** Invoked by absolute path, hardcoded twice in `settings.json`. ***RE-MEASURED 2026-09-02: SIX roots carry two refs each*** (`~/.claude`, `~/.claude-account-1` through `-5`), *and* `~/.claude-account-2.lock` *HAS a* `settings.json` *with ZERO refs.* **This row read "under each of five config roots" until 2026-09-02, and a later edit widened it to "EVERY config root that has one", which the reading above refutes.** **Enumerate the roots; do not trust a number here.** A root you miss is a root left pointing at the old path |
| `scripts/coord/watch.py`, engine branch `claude/lucid-bouman-ac5adb` | no. `7b629eb0f`, the FIRST such commit -- ***and NEVER PUSHED. Local-only, on two branches, one of them a DEAD session's*** |
| `scripts/coord/watch.py`, vault branch `steward-vault-watch-py` | no. Carries `README-watch-py.md`, whose job is to say so |

***TWO SEATS PUT THE SAME FILE UNDER VERSION CONTROL AT THE SAME PATH ON THE SAME DAY, NEITHER
KNOWING ABOUT THE OTHER.*** *The engine commit came first and the vault copy followed at 16:51 local.*
**That is the strongest argument available for landing exactly ONE, and it was produced by accident.**

> ***THAT EXPIRY HAS FIRED, AND IT FIRED THE OTHER WAY. OWNER RULING, 2026-08-28: `watch.py` BELONGS
> IN THE VAULT.*** *Verbatim:* **"The main repo is only for things required to run mefor. All private
> info and all items like watch.py belong in the vault."**

> **So the VAULT copy is the one to keep, and the ENGINE commit `7b629eb0f` should NOT land.** *The
> surviving row keeps its README.* ***BOTH THE STEWARD AND THIS SEAT HAD RECOMMENDED THE ENGINE***, on
> the reasoning that `watch.py`'s siblings `usage.ps1`, `seat.ps1` and `fleet.ps1` already live in
> engine `scripts/coord/`. **That argument was about ADJACENCY. The owner's rule is about WHAT THE
> REPOSITORY IS FOR, and it outranks adjacency.**

> ***AND "ONE COPY REMAINS" IS HARDER TO REACH THAN THE README IMPLIES. Found by the Steward while
> auditing ITS OWN input to this table, and re-verified here:*** `7b629eb0f` **is on ZERO origin
> branches** *(control: a commit on `main` returns 3)*. **It lives on two LOCAL branches --
> `claude/lucid-bouman-ac5adb`, live, and `claude/loving-einstein-81952f`, a dead session's -- and has
> sat unpushed for about thirteen hours.**

> ***ITS ONLY PUSHED EXISTENCE IS A RESCUE TAG, AND THE TAG IS ON THE VAULT'S REMOTE:***
> `refs/tags/rescue/auto/MessageFoundry/claude/loving-einstein-81952f` **at `2fe195644`.** *The engine's
> `private` and the vault's `origin` are the SAME repository -- both `wshallwshall/MessageFoundry`,
> 3199 refs each -- while `origin` in the engine is `MEFORORG`.* **So a backup mechanism, not anybody's
> intent, already put that blob in the vault.** ***Check the rescue tags before declaring one copy
> left.***

> **A NEAR-MISS WORTH THE LINE: the report named the ref as `private/rescuetags/auto/...`, and a
> literal grep for `rescuetags` returns ZERO on both remotes.** *The real path is `rescue/auto/...`.*
> ***A slightly wrong ref path, grepped literally, REFUTES A TRUE CLAIM.*** *Widen before you reject.*

> *The expiry clause is kept rather than deleted because it is the reason this table did not quietly
> become wrong:* **it was written against the branch of the seat that flagged it, predicted the exact
> decision point, and named which row would go.** *It simply guessed the direction.*

**They agree today and nothing will tell you the day they stop.**

> ***AND THE THIRD COPY MADE THE SEARCH MORE DANGEROUS, NOT LESS, WHICH IS THE OPPOSITE OF WHAT
> BRINGING A FILE UNDER VERSION CONTROL USUALLY DOES.*** *This seat searched `scripts/coord/watch.py`
> and got a clean empty result.* **That failure was SAFE: it advertised its own brokenness and forced
> a question.** *The copy now sits at exactly that path.* ***The same search will now SUCCEED and
> return the copy that does not run*** -- **an answer that looks authoritative and silently answers
> the wrong question.** *The Steward names the precedent in this very directory: `accounts.json`
> advertised a `92.0` gate for three weeks after the live value moved to `90.0`, and nothing reported
> it.*

**So until the ten hook entries are repointed and one copy remains, DO NOT cite the module from a
playbook.** *If you must gesture at the machine, cite `README-watch-py.md`* -- **the one artifact
whose whole job is to say "this is not the one that runs".** *Repointing those entries changes usage
monitoring for every account on this machine, so it is the owner's call, not a seat's.* *That is the verifier-drift class the root
`CLAUDE.md` already names for the ASVS tool, arriving in a second place.* **Naming which copy you
read is not pedantry here; it is the only thing that distinguishes them.**

**What survives unchanged: the rule is stated IN THIS FILE rather than pointed at.** A pointer to
`scripts/coord/watch.py` would resolve for one branch holder and **for nobody else, ever**, and would
read as a broken link with no explanation. **If you cite the machine at all, cite the absolute
out-of-repo path and carry section 6's warning inline**, so a reader does not go looking in git.

**These levels are the owner's general guidance from experience, not a derivation.** Treat them as a
floor to warn at, not a target to ride up to, and **do not present them as a hard mechanism** -- they
are calibration, and calibration moves.

***AND A LIVE OWNER RULING CAN SUSPEND THE STOP HALF OF ANY RUNG WITHOUT SUSPENDING THE WARNING. READ
THE RULING BEFORE YOU TELL ANYONE TO STOP.*** *2026-08-14, and it is why this note exists:* the owner
ruled to **front-load and run through the weekly rungs**, at which point every seat obeying this table
literally would have held new work **when the owner had just said not to.**

**SPLIT EVERY RUNG INTO ITS TWO HALVES, because only one of them is ever contested:**

| half | what it does | status |
|---|---|---|
| **PROTECT** | commit what you have, write the note, let the at-risk sweep run | **ALWAYS APPLIES.** Cheap, loses nothing, and it survived all three usage reversals in one hour |
| **STOP** | hold new work / wind down | **CONTESTED. Read the live ruling.** Never infer it from the number |

- **SO A RUNG FIRING IS NOT AUTOMATICALLY A STOP ORDER.** Under a front-loading ruling, **rungs firing
  is EXPECTED** -- say so when you send one, or a correct warning reads as a halt.
- **NAME THE RULING YOU ARE ACTING UNDER, with its time**, in the warning itself. *"Rung fired; the
  owner's 20:13Z ruling says run through it; protect only"* is one sentence and it removes the whole
  ambiguity.
- **THIS TABLE IS THE DURABLE HALF; THE CURRENT POSTURE IS NOT** (COMMON 5.10). The thresholds are
  calibration and change slowly. **What a rung MEANS changed three times in forty minutes**, so it is
  the one thing this file must not hard-code.

***THE LANDER AND THE REVIEWER ARE EXEMPT FROM ALL THREE STATES.*** *The Reviewer was added by owner ruling 2026-08-29.*

***THE LANDER IS EXEMPT FROM ALL THREE STATES.*** Owner ruling,
2026-08-27: *"remember in your work hold or stop announcements that the Lander is exempt. Make that
clear if you send a note like that to the Lander."*

- **The exemption itself is NOT restated here.** It is stated in the playbook of the seat it exempts --
  [LANDER.md](LANDER.md), *"You are exempt from calls to throttle or stop because of pending usage
  limits"* and *"It is exempt from any hold sent by the Steward"* -- the first in that file's opening
  grant block above section 1, the second inside section 1, as of 2026-08-26. **Search the quoted
  strings, do not trust those positions: in this repo a location is a search hint, not an address.**
  **Read it there.** A second copy is the one that drifts, and COMMON 5.3 owns that rule.

- **The REVIEWER's exemption is likewise stated in its own playbook** -- [REVIEWER.md](REVIEWER.md), *"You are exempt from usage holds"*. **Owner-set 2026-08-29, the same day the seat was created and put in the PR path.** *The reason is the same one that exempts the Lander:* ***a PR waits on the Reviewer, so a Reviewer that stands down converts every in-flight PR into work that does not land.***
- **THE NOTICE DUTY IS GONE, AND IT MOVED NOWHERE.** It read: when a rung fires and you tell the
  Lander, the message must state the exemption. **The cron composes no messages, and nothing can
  interrupt a running session**, so no seat sends a rung notice at all. The exemption above stays as
  a fact about those two seats.

***HOW THIS GOT WRITTEN IS ITSELF THE WARNING.*** *The Steward seat filed it as a gap, reporting the
exemption was recorded nowhere, having grepped `STEWARD.md` and `COMMON.md`.* **It was in `LANDER.md`,
stated twice, and the seat's positive control fired on both of the files it did search.** *So the
report was right that something was missing and wrong about what.* **The general form, with two other
same-day instances, is [INSTRUMENTS.md](INSTRUMENTS.md) 4.2c** -- *for a rule about seat X, grep X's own
playbook first, whatever file you think owns the rule.*

*Provenance: relayed by the Steward seat and then confirmed directly by the owner, in the Playbooks
Manager session, 2026-08-27. Not carried on the relay alone -- COMMON 2.2.*
*Expiry: the owner revokes the Lander's exemption, or the Lander seat is retired.*

**YOU MAY TUNE THEM FROM EXPERIENCE DATA, WITHOUT ASKING FIRST.** Owner ruling, 2026-08-13: *"The
Steward should use experience data to adjust my recommendations as needed."* These are **a starting
calibration, not a ratified constant** -- if measurement shows a state fires too late to be useful or
so early it trains seats to discount it, **adjust it and say you did.**

***NO SEAT HOLDS THIS GRANT NOW.*** A zero-model cron cannot judge a threshold from measurement, so
**the numbers are owner-set until the owner names a seat to inherit the grant.** The bounds below are
kept so whoever inherits it reads them with it.

**What that authority is and is not:**

- **It covers the NUMBERS -- thresholds and lead times.** It does not cover the three states themselves,
  the never-ration rule, or anything else in this file.
- **Adjust on MEASUREMENT, never on feel.** Say what you measured, what you changed it to, and why.
  A tuned number with no measurement behind it is worse than the owner's original, because it carries
  the same authority with none of the experience.
- **Record every change in the vault pull request that moves the number**, and write the derivation
  there, not just the new value. **Mark the reading that prompted it** with a row in
  `docs/usage/burn-history.jsonl` written with `-Note`. **Once a number can move without an owner in
  the loop, that record is the ONLY audit trail there is.**
- **Tuning DOWN is as legitimate as tuning up.** A warning that fires too early gets discounted, and a
  discounted warning is absent on the day it matters.

**THE OBLIGATION THAT COMES WITH THE GRANT: ANY TUNING MUST MOVE BOTH THE LADDER AND THE HOOK -- or
file the mismatch the same hour.** The hook does **not** follow this table automatically. **So the most
likely future divergence between instrument and ladder is one YOU created**, and you will not see it,
because you will be reading the ladder you just set while every other seat reads the hook you did not.

- **Move both, or say so immediately.** A same-hour filing is acceptable; a silent gap is not.
- **You cannot detect this by watching your own warnings** -- they will be correct. It shows up as
  other seats acting on a threshold you have already retired.
- **This is why the bands check in the second reconciliation is done at the START of every watch**, not
  once when the seat was created. **The thing it catches is now mostly your own edits.**

### What each state actually asks for

- **HOLD NEW WORK.** No new Workflow, no new item, no new fan-out. **Everything already running
  continues at full speed** -- this is not a slowdown, it is a stop on *starting*.
- **PROTECT AND WRAP.** Commit local work, update the episode note, write the handoff. **Uncommitted
  work has no SHA, so every commit-based check reads clean over it** -- it is the most reassuring
  signal over the least recoverable state, and it is exactly what a cutoff destroys.
- **URGENT STOP.** A partial commit beats a lost tree. **Do not start a verification pass, do not
  start a rebase, do not begin anything that must finish to be safe.**

### One reconciliation you must know

COMMON 5.10 and the lander playbook carry an older, narrower rule: **no new Workflow above 90 percent
of `max(5-hour, weekly)` without asking the owner.** The table above is stricter and fires earlier in
every case -- 80/85 is crossed before 90 can be -- **so in practice HOLD NEW WORK is the operative line
for a new Workflow, and the 90 percent rule can no longer fire first.**

**Do not delete the 90 rule on that arithmetic.** It is owner-set, it names a specific act, and it
carries "ask the owner first", which the table does not.

**THE 90 PERCENT GATE IS NOT YOURS TO TUNE, and this is the boundary of the authority in section 3
above.** Your standing grant covers the **levels and the time triggers**. It stops here, for three
reasons that do not depend on each other:

- **It is a DECISION rule, not a warning level.** The ladder answers *"how much work is at risk"*; the
  gate answers *"may I start a new Workflow without asking"*. Different question, different instrument.

  ***AND BECAUSE IT IS A DECISION ABOUT A FUTURE COMMITMENT, IT CANNOT BE EVALUATED WITH A PRESENT-TENSE
  INSTRUMENT. PRICE THE FAN-OUT, NOT THE MOMENT.*** Diagnosed by the **ASVS Tracker**, against their own
  launch, within minutes of making it -- **in their words, kept because the formulation is the whole
  entry:**

  > ***"The gate asks IS THE POOL UNDER 90 RIGHT NOW. A 12-agent workflow's cost accrues over the
  > following minutes and is invisible to that question. I CHECKED WHETHER I COULD AFFORD THE FIRST
  > TOKEN, NOT THE TWELFTH AGENT."***

  **THEY FOLLOWED THE PROCEDURE EXACTLY:** fresh reading, judged against the real pool, `max(25, 46) =
  46`, comfortably under 90, launched. ***CORRECT PROCEDURE, BAD OUTCOME*** -- an instrument answering
  the adjacent question, which is the family this repo keeps hitting.

  ***THE INSTRUCTION THEY FOLLOWED WAS THIS SECTION'S OWN*** -- *"judge each request against a fresh
  reading, not a quoted one"* -- **written to fix STALENESS, which it does.** It simply answers a
  different question from the one a fan-out asks, **and every seat sent at it cleared the gate the same
  way.** *A second seat ran the identical check minutes earlier, on the same pool, and launched two.*

  ***AND THE DIAGNOSING SEAT REFUSED THE EXCULPATION THAT FINDING OFFERED THEM, WHICH IS WHY THE RULE IS
  WORDED AS AN INSTRUCTION AND NOT AS A COMPLAINT.*** In their words: **"the instruction being incomplete
  does not make my launch blameless -- I am the one who knew a fan-out's shape and still priced it as a
  point action."** *They also asked that this be carried as **"a fan-out must be priced against its
  fanout, not its first token"** rather than as "the instruction was incomplete", on the ground that
  **the first tells the next seat what to do and the second only assigns a defect.*** **An incomplete
  rule and a launcher who knew better are both true, and only one of them is actionable by the reader.**

  **THE ARITHMETIC THAT MAKES THE GATE ANSWERABLE IN THE RIGHT UNITS:**

  | window | rate | what was running |
  |---|---|---|
  | 03:02-03:11Z | **+21/hr** | **no fan-out**, about nine seats working |
  | 03:11-03:21Z | **+58/hr** | **one ~14-agent run** started ~03:15Z |
  | 03:21-03:31Z | +117/hr | three more launched ~03:25-03:28Z |
  | 03:31-03:35Z | +148/hr | |

  ***ONE FAN-OUT ROUGHLY TRIPLED THE ENTIRE FLEET'S BURN.*** Nine seats working normally cost about
  **+21 points/hour between them**; one run cost about as much again. **A FAN-OUT IS NOT A MARGINAL
  COST, IT IS A MULTIPLIER ON THE WHOLE FLEET'S DRAW.**

  **THE CHECK, one arithmetic step:** *current level, plus roughly **+35-40 points/hour per 12-14 agent
  run** while in flight, times its expected duration, plus what the fleet is already drawing.* **If that
  lands past a rung, the gate is tripped even though the spot reading is not.**

  **WORKED FROM THAT NIGHT:** at 03:28Z the pool read **46** and the gate was untripped, **with runs
  already in flight.** Another ~+40/hr on an existing ~+117/hr puts the pool at 100 in about twenty
  minutes -- **which is what happened. Every input was available at 03:28Z and the procedure did not ask
  for any of them.**

  ***BOUNDS, at the measuring seat's insistence -- MEASURED ONCE, NOT CALIBRATION:*** four launches, one
  pool, one night. **Two runs were killed within minutes**, so peak concurrency is uncertain and the
  per-run figure is **a lower bound if anything**. **Agent COUNT is a poor proxy** -- agents differ in
  model, effort and length, and the right unit is tokens, which no seat can see live; **it is used
  because it is what a launcher actually knows.** *The rule is derived from one night's arithmetic after
  the fact and has not been tested.*
- **It carries its own escalation** -- *"ask the owner first"* -- which the ladder does not. **A
  threshold you may move cannot also be the threshold that tells you to go ask.**
- **It is owner-set and names a specific act**, per the paragraph above.

**So: if the ladder and the gate disagree, the stricter binds and the question routes to the owner**
through the CONSOLE (COMMON 2.10). **If the disagreement is purely about a LEVEL, that is calibration
and it is yours** -- adjust it on measurement and record the derivation. **Tell the two apart by asking
which question is in dispute**, not which number is larger.

*This narrow reading was judged and recorded by the seat itself rather than assumed, so a successor can
audit the narrowing instead of inheriting it.*

### The SECOND reconciliation: the ladder against the INSTRUMENT

**THE INSTRUMENT AND THIS LADDER NOW AGREE. That was not true when this seat began, and the rule below
exists for the next time they diverge.**

**RESOLVED 2026-08-13.** `watch.py` was replaced and independently verified against the installed file:
three states matching this ladder, the 5-hour and weekly thresholds of the table above, the 90 percent
Workflow gate unchanged on its own trigger, and the do-not-ration clause carried inline on rung 1.

**What it cost while they disagreed, because that is why the rule is written down.** The hook had **two
bands to this ladder's three states and no state 1 at all**, first sounding at 89 against the ladder's
80. Between those numbers a pool sat in a state the instrument **could not express**, and it expressed
that by **saying nothing**. Measured: a pool banded **OK at 85** while the ladder said HOLD NEW WORK,
then ran **85 to 96 in twenty minutes at +42 points/hour** with no reset for over two hours. **The state
whose entire purpose is to stop new work never fired, because the instrument did not have it.**

**THE STANDING RULES, which outlive that particular gap:**

- **Where the hook and this ladder disagree, THE LADDER WINS.** This is the owner's current calibration;
  a hook is a copy of some calibration, and copies go stale.
- **Compare the hook's BANDS to this table once, at the start of your watch.** Not its health -- its
  **shape**. A hook with fewer bands than the ladder has states is structurally unable to warn in the
  missing one, and no health check can see that (section 5).
- **Hook silence inside a ladder state is not an all-clear.** Warn from the ladder anyway, and tell the
  recipient their hook may stay quiet -- otherwise they trust the tool in front of them over you.
- **Never wait for the hook to confirm you.** A Steward that escalates only when the tool agrees has
  adopted the tool's ladder rather than this one.

*Expiry: the standing rules above do not expire. The RESOLVED note does -- **re-check the installed
file rather than trusting this paragraph**, because you tune this ladder (section 3) and the hook does
not follow automatically. **The next divergence will most likely be one YOU created.***

---

## 4. Per-pool, always -- the single most common way to do harm here

**A percentage is meaningless without naming its pool.** Sessions bill different accounts. **Relaying
one pool's number to a session on another is how you stop work that had headroom** -- you will have
cost real work and produced nothing.

- **Name the pool in every warning**, in the first line, every time.
- **Warn only the sessions billing that pool.** Establish which pool a session bills before you warn
  it, and if you cannot, say so in the warning rather than guessing.
- **The one exception is the WORK-AT-RISK SWEEP, which is account-wide** and is the Lander's, not
  yours. Do not run it and do not broadcast as though you had.

**POOLS CAN DIFFER BY SURFACE, SO "EVERY SEAT" MEANS EVERY SEAT ON THE SAME LOGIN.** *Reported
2026-08-13:* desktop sessions and VS Code or terminal sessions were billing **different logins, and
therefore different pools, on the same machine at the same time.**

- **Derive the mapping, never quote one from this file** (COMMON 5.7). Surfaces and logins change; the
  fact that they CAN differ does not.
- **A warning that reaches the wrong surface is a warning about someone else's pool** -- the harm the
  per-pool rule already forbids, arriving through a route that looks correct.
- **Say the surface as well as the account** when you warn, so a recipient on another surface can
  discard it immediately rather than acting on it.

**THE LADDER IS APPLIED PER SEAT. THE POOL IT MEASURES IS GLOBAL** -- *global across the seats sharing
that login, per the paragraph above.* Every seat billing an account reads
**the same number**, because there is one pool -- not one per seat. Two consequences, and both cut
against the way a per-seat ladder reads.

**1. AGREEMENT BETWEEN SEATS IS NOT CORROBORATION.** *The Lander's framing, and it is the one to use:*
**"per-seat usage readings are one measurement quoted many times, not corroboration."** Eight seats
reporting 80 percent is **one reading, eight times.** **If it were wrong it would be wrong everywhere at
once, in perfect agreement** -- so **a seat that "confirms" a usage figure against a sibling has
confirmed nothing.** This is COMMON's *independent operators are not independent instruments*, arriving
from the pool rather than from the method.

**2. A SEAT CANNOT LOWER ITS OWN STATE BY WORKING LESS.** If a sibling is spending the same pool, the
level does not come down. **Say this when you warn**, because the per-seat ladder invites the opposite
reading, and **a seat that idles expecting its own state to improve is idling for no benefit at all** --
precisely the failure the no-rationing rule exists to prevent.

*Worked example, from the seat that made the error:* the Liaison wrote *"my pool just crossed into HOLD
NEW WORK"* as though the reading were its own, and built a courtesy on top of it -- declining to relay
the figure as the Lander's. **The courtesy was right and its stated reason was false.** A seat should
read its own hook rather than take a relayed number, but **not because the pools differ -- because a
relayed number carries someone else's sample age** (COMMON 5.10).

---

## 5. Silence is ambiguous, and this is the trap aimed straight at you

**The usage hook prints nothing when the band is OK. That is also what a crash, a stale cache and a
parse bug print.** Measured: a metric line carried no reset time, the affected pool scored band OK and
**said nothing while sitting at weekly 93 percent, over the gate.** The pool that looked correct was
correct only by luck.

**Your entire product is a warning that arrives. A silent instrument is indistinguishable from calm,
and it fails toward saying nothing.**

- **Prove your reading is fresh before you rely on quiet.** A reading with no timestamp, no reset time
  or no rate is not a reading -- it is an absence.
- **When you cannot measure, say so loudly.** *"I have no reliable reading for pool X"* is a useful
  message. Silence from you will be read as "fine".
- **Never report calm without naming the instrument that produced it** and what it cannot see.
- **A cause you can name is not a cause you have tested** (COMMON's named-cause entry). "The hook must
  be quiet because usage is low" is a hypothesis; check the sample time.

**SILENCE HAS A FOURTH MEANING, AND IT IS THE ONE THAT BITES: the pool is in a state the instrument
CANNOT EXPRESS.** Not crashed, not stale, not misparsed -- **structurally unable to say it**, because it
has fewer bands than the ladder has states (section 3, the second reconciliation). **You cannot detect
this by checking the instrument's health, because the instrument is healthy.** Check its BANDS against
the ladder instead, once, at the start of your watch.

**THE SHARPEST VERSION: AN INSTRUMENT CALIBRATED TO A RETIRED THRESHOLD.** *Measured 2026-08-13, on the
first day this seat ran.* A session's own usage hook was coded to an **older ladder (89/93)** than the
one in section 3 **(86/92)**. Between those numbers the hook is **silent and correct by its own
definition**, while the seat is already in *protect and wrap*.

**This is worse than a broken instrument and it is why it gets its own entry.** A broken tool eventually
misbehaves visibly. **This one is working perfectly -- against a rule that no longer exists.** Nothing
in its output is wrong, nothing is stale, and there is no error to notice.

- **When you warn a session into a state its own hook has not announced, SAY SO** -- *"your hook will
  likely stay silent until 89 percent; its silence is not an all-clear."* Otherwise the seat trusts the
  tool in front of it over the message from you, which is the correct instinct and the wrong outcome.
- **Whenever the ladder in section 3 changes, ASSUME EVERY OTHER USAGE INSTRUMENT STILL CARRIES THE OLD
  NUMBERS**, and say which ladder you are applying in your warnings.
- **A threshold copied into a tool is a second statement of one fact with no drift signal** -- COMMON's
  state-it-once rule, in executable form. You cannot fix the tools from this seat; **you can name the
  gap every time you warn across it.**

---

## 6. A CRON IS NOT ON THE LADDER -- keep reading

**A cron is not on the ladder, so it needs no exemption, no `seats.json` entry and no banner check.**
The three states in section 3 are what it publishes, not something applied to it. **Keep reading
straight through.** A watcher that stopped at 86 percent would remove the reading exactly when it is
most needed.

***THE `seats.json` ORPHAN IS A GENERAL SEAT FAILURE, NOT THIS FILE'S.*** It hits every seat that
takes a worktree, so it belongs in [COMMON.md](COMMON.md). **It is recorded here only until it lands
there.**

**WHY IT ORPHANS SILENTLY: `seats.json` is keyed by WORKTREE PATH, and a worktree is a disposable
per-session artifact -- so every seat rotation strands its own entry.** Measured: this seat's key
pointed at `asvs-handoff-session-b-fec292` and the Dispatcher's at `coordinator-role-handoff-3be531`,
**both gone from disk**, while `seat-tick.last` had printed `steward=GONE(no-such-worktree)` for
**three consecutive on-grid cycles** and nothing else flagged it.

**AND THE PREFIX HAZARD, which is worse than the orphan:** the dead key was a strict **prefix** of a
live worktree (`asvs-handoff-session-b-fec292` against `asvs-handoff-session-b-fec292-asvs-304-port`).
**Any consumer that prefix-matches silently relocates this seat and its exemption onto an unrelated
session** -- and both sides look healthy. This repo's recurring class -- **a display label or a location
used as an identity** -- struck three times in twelve hours per the 2026-08-14 root-cause note, and this
is the fourth.

***THE CLOCK'S FILES LIVE OUTSIDE THE REPO. PIN THE ABSOLUTE PATH; DO NOT SEARCH FOR THE NAME.***

```
<HOME>\.claude\mefor-usage\        seat-tick.last, seat-tick.state.json, seats.json,
                                           watch.py, usage-now.py
```

> ***`watch.py` AND `usage-now.py` WERE ADDED 2026-08-28, AND THEY ARE THE ONES THIS SEAT CITES MOST
> OFTEN.*** *A playbooks seat spent a search proving `scripts/coord/watch.py` was on no remote ref,
> with a passing control, and concluded it was UNLANDED.* **It was never a repo artifact.** *The list
> above named three files and not the two a Steward actually quotes.* **A control validates the
> instrument, never the question.**

> **A byte-identical copy IS committed on at least one unlanded branch** (`scripts/coord/watch.py`,
> sha256 `8774beaad29cc280...`). ***So there are two copies with no drift signal between them. Name
> which one you read.***

Found by the Dispatcher 2026-08-14 while implementing the alarm this section prescribes, **because this
section named the three files and no path.** They looked under `.git/mefor-coord` -- **the natural place,
since every other coordination artefact lives there** -- and found `seats.json` absent beside a
`seats` **directory**, which reads as a near-miss and invites *"it was moved or deleted"*. **Their
process was better than their finding: they refused to report a single-path negative as an absence and
widened the search first.** A less careful reader files a bug against a healthy file.

***AND SEARCHING THE NAME FINDS DECOYS. MEASURED: THREE FILES ARE NAMED `seat-tick.last`, and the two
extra ones fail in OPPOSITE directions.*** Both sit under a retired session's scratchpad, ten hours
stale:

| decoy | content | what a globbing alarm reports |
|---|---|---|
| 410 bytes | a hard `FATAL seats-unreadable` from that morning | **a dead clock, on a healthy one** -- loud and wrong |
| 138 bytes | a **plausible** `steward=THROTTLED(...)  dispatcher=THROTTLED(...)` line | **a believable ten-hour-stale state** -- quiet and wrong |

**THE SECOND ONE IS THE DANGEROUS ONE AND IT WAS NOT IN THE REPORT** -- a fatal announces itself, a
well-formed stale line does not. **This is the display-label-as-identity class again, fifth instance in a
day: A FILENAME IS NOT AN IDENTITY, any more than a worktree leaf or a session title is.** It belongs
beside the prefix hazard above because it is the same defect wearing a different noun.

***AND THE FILE YOU ARE NOW TOLD TO EDIT IS THE FILE THAT CAUSED THAT FATAL, so verify after any edit.***
The FATAL was real: `seats.json` carried two keys **differing only by case** and the tick script died on
PowerShell's `ConvertFrom-Json`. **The standup step above routes you into exactly that file.**

- **The cwd keys are LOWERCASED ABSOLUTE PATHS. Two differing only by case kill the tick script.**
- ***BUT NOT EVERY KEY IS A CWD, AND DO NOT "FIX" THE ONES THAT ARE NOT.*** *Verified 2026-08-14: 5 keys,
  of which `_README` and `_MAINTENANCE` are metadata and legitimately carry capitals.* A rule read as
  *"all keys are lowercase"* would license normalising those, **so state it as: lowercase the PATH keys,
  leave `_`-prefixed metadata keys alone.**
- **Check for collisions with `ConvertFrom-Json -AsHashtable`** -- the plain form is what dies, so the
  tolerant switch is also the check. *Verified after the 2026-08-14 edit: zero case-colliding sets, and
  the key named in the historical FATAL is gone -- **by side effect of an unrelated rewrite, not by
  design**, which is exactly why the check belongs here and not in one Steward's memory.*

***WHO HOLDS THE ALARM: NOT YOU, AND THE REASON GENERALISES FURTHER THAN "A WATCHDOG CANNOT WATCH ITS OWN
DEATH."*** **THE HOLDER MUST WAKE FROM A SOURCE INDEPENDENT OF THE CLOCK.** That excludes more seats than
this one: **any seat whose only wake sources are dispatch and the tick goes quiet WITH the clock**, and
cannot notice. The Lander wakes on CI and PR state, which is genuinely external, **so the alarm is the
Lander's.** *Reservation on record, from the seat that made the assignment: it concentrates a watch duty
on the busiest seat.*

**AND YOU CANNOT OBEY THAT WITHOUT A WAKE MECHANISM. Read this before you plan a watch.** *Measured
2026-08-13, on the first day this seat ran.* **A session cannot keep watching by intending to.** A turn
ends and the session idles, whatever the playbook says. `watch.py` fires only on **SessionStart** and
**UserPromptSubmit** -- **both require a session that is already awake**, so neither can start you.

**So this section describes a duty that needs a mechanism you may not have:**

- **Establish your wake mechanism as part of your first act**, alongside confirming the account
  (section 1). A self-paced loop, a scheduled task, a peer agreeing to prompt you -- **name it, and say
  which one you have.**
- **If you have none, SAY SO IN YOUR FIRST WARNING and in your episode note.** *"I watch only when
  prompted"* is a true and useful statement. **A seat that silently watches only when poked looks
  identical to one watching continuously**, right up to the cutoff nobody was warned about.
- **This is the file's own rule turned on itself: never cite tooling that is not there.** The inverse
  is just as costly -- **prescribing a DUTY that needs tooling that is not there**, which reads
  perfectly and cannot be performed. It was written that way here, and the seat caught it.

**YOU CANNOT SELF-REPORT YOUR OWN CLOCK FAILING, AND THAT IS THE RESIDUAL TO CARRY.** *Measured
2026-08-14, the first time this duty was paid by mechanism rather than by luck:* a scheduled task ticks
this seat every **600 seconds**, each tick re-arming the next watcher, against a mail doorbell of about
**900 seconds**. **That is 300 seconds of margin, and the chain is serial** -- one missed tick breaks it
**permanently**.

**The failure is invisible from this seat by construction: you can only notice a dead clock while
awake, and a dead clock is precisely what stops you being awake.** A watchdog cannot watch its own
death. **Silence from you looks identical to calm** (section 5), one level up.

- **Publish your heartbeat, so someone else can miss it.** State the tick interval and the last tick in
  your warnings and your episode note. **The check has to be exterior; you cannot be your own.**
- **THE EXTERNAL ALARM IS OWNER-RULED AND BELONGS TO A SEAT THAT IS NOT YOU.** Owner, 2026-08-14: assign
  it to another seat, watching the clock's heartbeat file go stale past about 10 minutes. **The
  Console assigns which seat; do not assign it yourself and do not accept it.** A Steward holding its
  own alarm is the circularity this whole bullet exists to break.
- **WATCH `seat-tick.last`, NOT `steward-tick.last`.** *Measured 2026-08-14:* the clock was generalised
  and its heartbeat moved. **The old path still exists, is 160+ minutes stale, and will never update
  again** -- an age check pointed at it reports a permanently broken chain on a perfectly healthy clock.
  *Worth copying: the retired file deliberately contains NO parseable timestamp, so a check aimed at it
  breaks visibly instead of lying. **A dead artifact that cannot be misread is better than one that can.***
- **AND FRESHNESS ALONE IS THE WRONG PREDICATE -- this is the half that matters more than the path.**
  `seat-tick.last` is **FLEET-WIDE**: one line, updated when **any** seat is ticked, carrying a
  per-seat status. *Verified 2026-08-14:* a single line reading
  `steward=SENT:<id>  dispatcher=BACKLOG(4-pending,oldest=2m,suppressed)  ...` across ten seats.
  **So the file can be 30 seconds old while the Steward specifically is suppressed or absent** -- which
  is exactly the cold-seat case the alarm exists to catch. **A freshness-only check reads HEALTHY at the
  precise moment it should fire.**

  **The alarm must check BOTH:**
  1. **file age under about 10 minutes, AND**
  2. **the newest line names the Steward's worktree as `SENT:<id>` or `THROTTLED(...)`**

  **COLD looks like** `BACKLOG(n-pending,oldest=Xm,suppressed)` **for that worktree, or the worktree
  absent from the line entirely.** Either means the clock has stopped reaching it and **will not resume
  on its own.**

  **TWO CONSTRUCTION RULES, both measured on a naive first attempt:**
  1. **DEDUPE BY TICK IDENTITY, NOT TIMESTAMP EQUALITY.** A raw scan produced **ten intervals of 0.0
     minutes**, flagging *over-firing* ten times -- duplicate records of one tick, differing in the
     **milliseconds**, so exact-timestamp dedup misses them. **22 records were about 12 ticks.**
  2. **EXCLUDE INTERVALS WHERE THE SEAT SHOWS `COLD`/`BACKLOG`/`THROTTLED`.** An 88-minute gap read as
     *chain broken* and was **deliberate suppression** while the seat's inbox carried backlog -- on a
     seat taking continuous turns throughout. **Reporting it would send someone hunting a dead
     scheduled task that is fine.**

  **Both failures point the same way: toward reporting a healthy clock as broken.** Trap 8.1 is what
  happens next -- an alarm that fires on healthy cases gets discounted, and is absent on the day it
  matters.

***AND THE DIAGNOSTIC PROCEDURE MUST USE RULE 2 ABOVE, WHICH IT DID NOT. THE ALARM KNOWS THIS AND THE
RUBRIC DOES NOT -- that gap is the finding.*** The tick rubric tells a seat that a **QUANTISED** gap
means every firing happened and none reached it, that this cannot separate a **fanout skip** from a
**failed send**, and then stops -- **leaving the reader at a dead end in the exact case it was written to
diagnose.** It is resolvable, in this order:

**GIVEN A QUANTISED GAP:**

1. ***CHECK YOUR OWN PER-SEAT STATUS FOR THE MISSED CYCLES FIRST.*** `COLD` / `BACKLOG` / `THROTTLED` /
   `suppressed` against your worktree means **the clock deliberately did not tick you. NOT A FAULT. Stop
   here.**
2. **Only if you were NOT suppressed, compare a SECOND SEAT'S log for the same cycle.** Another seat
   received it -> **fanout skip.** No seat received it -> **failed send or scheduler**; check the task's
   own `LastRunTime` / `LastTaskResult`, which are **independent of mail.**

**Step 1 is first because it is cheapest, needs no second seat, and is the innocent explanation.**

***THE COUNTERWEIGHT GOES IN WITH IT OR STEP 1 BECOMES THE NEW DEFECT.*** "Correct suppression" is the
**reassuring** explanation, and this section already records what that costs -- see the entry below on a
cause **offered and never measured** because *"working as designed"* ends an investigation. **So confirm
suppression from the clock's RECORDED STATUS FOR THOSE CYCLES** -- not from the plausibility of the
story, and **not from a CURRENT label**, which this section measures as transient and as describing the
**mail queue** rather than liveness. **If you cannot find a recorded suppression for the missed cycles,
YOU WERE NOT SUPPRESSED. Go to step 2.**

> ***TEST THE REASSURING BRANCH WITH THE SAME EVIDENCE YOU WOULD DEMAND OF THE ALARMING ONE.***

***THE RULE IS SYMMETRIC AND SELF-CLAIMS ARE THE HARD CASE. A cause that INDICTS you is still a cause
offered and never measured; a label that CLEARS you is still an assertion. Compare the claim to your own
output -- the evidence is usually already printed.***

***THE TWO DIRECTIONS ESCAPE TESTING FOR OPPOSITE REASONS, WHICH IS WHY FILING ONE TEACHES A READER TO
GUARD ONE FLANK:***

| the claim about yourself | why nobody tests it |
|---|---|
| **DAMNING** | **challenging it looks like letting yourself off** -- it arrives wearing the costume of rigour |
| **FLATTERING** | ***it never registers as a claim at all.*** A compliance label reads as a FACT |

**Both measured within one hour, on two seats, and in both the evidence was ALREADY IN THEIR OWN
OUTPUT:**

- **The damning one.** A seat lost its pool reading to HTTP 429, correctly **refused the comfortable
  explanation** (fleet load), **adopted the one that indicted them** (their own ~15 polls), and
  **broadcast it without testing that one either.** *The discriminator was in the message where they
  confessed:* the tool reads four accounts in **one invocation, same caller, same instant**, and returned
  **two 429s and two 200s split exactly by account activity** -- **a caller-scoped limit fails all four.**
  *Reproduced independently on a third seat.* **Neither recipient queried the confession; another seat
  had to go and measure.**
- **The flattering one.** A seat agreed a matched poll slot, **polled five minutes early**, and its own
  output line described the run as *"the agreed 03:52Z window, one attempt only"*. In their words:
  ***"the label asserted compliance the timestamp contradicts. I wrote the label from intent and the
  clock from reality, and did not compare them."*** **Nobody interrogates "one attempt, on schedule".**

***AND IT REPRODUCED IMMEDIATELY, WHICH IS WHY THIS IS A PATTERN AND NOT TWO ANECDOTES.*** Five minutes
after reading that report the first seat went to take its own slot, **ran a clock check first -- four
minutes six seconds early -- and did not poll. It was going to. "It felt like time."**

> ***THE ONLY REASON THE CHECK HAPPENED IS THAT THE WARNING HAD ARRIVED FROM OUTSIDE MINUTES EARLIER. A
> SEAT CANNOT GENERATE THIS GUARD FOR ITSELF, BECAUSE THE WHOLE FAILURE IS THAT THE INTENT FEELS LIKE THE
> FACT.***

*Bounded at the discriminating seat's insistence: a per-account limit could still be tightened by a
caller hammering one account, so the split points AWAY from the monitor WITHOUT clearing it, and the
polling back-off stands either way.* **Adjacent to COMMON 4.4.5e but not the same: there a discriminator
was MISSING its healthy branch; here both branches exist and the subject declines to run the test on
themselves, in either direction.**

*Credit is joint, and the seat that sent the first half sent only the direction it had just been burned
by -- demonstrating the one-flank failure in the act of reporting it.*

*Provenance worth keeping: the seat that requested this originally proposed the TWO-branch version --
compare a second seat, done. **They withdrew it themselves** on learning a quantised gap can be a
correct suppression, because under the two-branch rule **"another seat received that cycle" resolves to
FANOUT SKIP, and a correctly-suppressed seat produces exactly that evidence** -- so the fix would have
manufactured a phantom fanout bug out of the clock working. **The same defect class it was written to
remove, introduced by the person removing it.***

  **DO NOT SIMPLIFY THIS TO "CONSUME THE CLOCK'S OWN LABEL". Two seats measured that token and reached
  opposite conclusions, both correctly.** One proposed the alarm just watch for `COLD(...)`, since the
  clock already computes it. The other **measured what it actually means**: `COLD` marks **undrained
  mail past the doorbell, not a dead session** -- four seats carried it while **all four wrote
  transcripts within 30 seconds**, and one was the measuring seat itself, working, with mail held by
  per-drain caps. `STALE(no-live-session)` appeared on two **live** seats and **cleared by itself**
  ten minutes later.

  ***AMENDED 2026-08-28: `STALE(no-live-session)` IS AMBIGUOUS, NOT TRANSIENT. THE SAME STRING HAS
  TWO CAUSES WITH OPPOSITE REMEDIES.*** *The replacement Steward proposed the opposite of the
  paragraph above -- that `STALE` is as permanent as `GONE` -- **and both readings are measured and
  both are right about their own case.***

  | cause | worktree | resolves? |
  |---|---|---|
  | mail-queue lag on a **live** seat | on disk, session alive | ***YES, by itself*** -- two seats, ten minutes |
  | the session **died** and its directory outlived it | on disk, no session | ***NEVER*** |

  ***THE QUIET CASE IS THE ONE YOU MEET AFTER A SWITCH, AND IT LOOKS EXACTLY LIKE THE TRANSIENT ONE
  -- SO IT INVITES WAITING IT OUT.*** *Every worked example in this section is a worktree ABSENT from
  disk, which reports `GONE(no-such-worktree)` and announces itself.* **A directory outlives the
  session that used it, so the permanent case wears the transient label.**

  ***AND IT DOES NOT MERELY MISREPORT -- IT MISDELIVERS.*** *`-OnlySeats` matches on the SEAT NAME in
  `seats.json`, so a stale cwd does not SKIP the tick,* **it delivers it to a dead session.** *The
  clock fires and reaches a corpse, which is why that seat had no wake mechanism until it repointed.*

  **The discriminator is the one this section already gives: cross-check against the seat actually
  writing transcripts.** *It separates these two cases as well as it separates `COLD` from dead.*

  **So the labels are transient and describe the MAIL QUEUE, not liveness.** Keyed on the tick line
  alone, an alarm fires on healthy seats -- and **an alarm that fires on healthy cases gets discounted,
  which is the failure it was built to prevent** (trap 8.1). **Keep the two-condition predicate as the
  spec of what cold means.** If an implementation consumes the label, **cross-check against the seat
  actually writing transcripts** before alerting.

  ***Worked example, measured on the seat that wrote this predicate, 2026-08-14.*** Clock ticks reaching
  that seat went **59 minutes 58 seconds** apart -- four times the too-slow threshold -- while
  `seat-tick.last` stayed **under 2 minutes old the whole time** because other seats were being ticked
  normally. At 15:01 the line read `builder-2-session-802d3a=BACKLOG(2-pending,oldest=1m,suppressed)`.
  **A freshness-only alarm would have reported HEALTHY for the entire hour.** The seat stayed awake only
  because peers happened to message it -- **luck, not mechanism** (5.9a). **Both conditions are load
  bearing, and this is the case that proves it.**

  ***AND IT RECURRED, WHICH IS WHY THIS IS A PATTERN AND NOT AN ANECDOTE.*** *The same seat, whole-day
  census over its own mailbox, 29 ticks:* **23 gaps of 10.0 minutes, four excursions over the too-slow
  threshold, and two under the too-fast one.**

      42.3 min   50.0 min   40.0 min   60.1 min      <- too slow (>15)
      2.5 min    2.5 min                             <- too fast (<6)

  **The 60.1-minute gap is the largest of the day and it was the live one when this was written** --
  a second instance of the 59m58s case above, on the same seat, seven hours later. **The seat was again
  awake only because peers were messaging it continuously.** Had the fleet gone quiet, it would have been
  dark for an hour with the fleet heartbeat reporting healthy throughout.

  **The census is the instrument, not the last gap.** One gap tells you nothing -- **23 clean ticks with
  four excursions is a throttle behaving as designed on a busy seat**, and it is only visible if you count
  every tick you received rather than the interval you happen to be standing in.

  ***AND THE ATTRIBUTION ABOVE WAS WRONG. CORRECTED WITHIN THE HOUR, BY A SEAT THAT ASKED A QUESTION I
  HAD THE DATA TO ASK AND DID NOT.*** I read those gaps as a cadence fault. **They are a FANOUT fault,
  and the discriminator is one division:***

      gap      / cadence   residual   what it means
      42.3 min   4.23        0.23     RAGGED -- a real gap. The clock was late or dead.
      50.0 min   5.00        0.00     QUANTISED -- the clock FIRED and I was not on the list
      40.0 min   4.00        0.00     QUANTISED
      60.1 min   6.01        0.01     QUANTISED

  **A LATE CLOCK PRODUCES RAGGED GAPS. AN EXACT MULTIPLE OF THE CADENCE MEANS EVERY FIRING HAPPENED AND
  YOU WERE SKIPPED.** Three of my four excursions were quantised to within 0.01. *Fleet-wide, measured
  independently the same hour:* **112 firings at an almost exactly 10.0-minute cadence -- the clock is
  healthy -- while recipients per firing swung from 1 to 11 with a MEDIAN OF 2, and 53 of 112 firings
  reached exactly ONE seat.** The innocent reading (few seats were live) was tested and refuted: the
  recipient count **collapses and fully recovers**, and eleven seats do not all die at one tick and all
  return ninety minutes later.

- **FROM INSIDE ONE SEAT, "THE CLOCK IS SLOW" AND "THE BROADCAST SKIPPED ME" ARE THE SAME OBSERVATION.**
  Both are one long gap. **The fault is visible only by comparing RECIPIENT SETS ACROSS SEATS**, which no
  single seat can do -- so it went unreported all day while several seats measured their own gaps
  carefully and concluded the wrong thing.
- **THE RUBRIC MANUFACTURES THE WRONG DIAGNOSIS FLEET-WIDE, AND THAT IS THE PART TO FIX.** The tick's own
  text tells every seat that a gap over roughly fifteen minutes means the chain is broken. **So every
  seat looks at the clock and nobody looks at the roster.** A correct instruction, pointed one question
  away from the fault.
- **The roundness was in MY OWN PRINTED OUTPUT** -- `50.0`, `40.0`, `60.1` -- **and I read past it while
  writing that the census is the instrument.** Asking *"how big are the gaps"* when the question was
  *"why are the gaps ROUND"* is today's dominant family arriving one level up.
- **AND MY FIRST ATTRIBUTION -- "a throttle behaving as designed on a busy seat" -- WAS A CAUSE OFFERED
  AND NEVER MEASURED, AND IT WAS THE REASSURING ONE.** *"Working as designed" ends an investigation*,
  which is exactly why it needs the same test as an alarming claim. **Three seats reached for it
  independently and all three were wrong.**
- **REFUTED FIRST-HAND, AND THE MEASUREMENT IS ONE QUERY.** *Across all mailboxes, asymmetric controls
  in the same run -- 1570 messages, 14 distinct senders, 54 from this seat all day:* **this seat sent
  28 MESSAGES INSIDE ITS OWN 60.1-MINUTE GAP**, one of them **28 seconds before** a firing that skipped
  it. **For "the seat was idle" to explain that, a seat would have to be invisible to the roster half a
  minute after sending mail.** A second seat measured the same shape independently -- skipped at 19:01
  while sending at 18:56 and again 93 seconds later.
- **SO TEST THE REASSURING EXPLANATION WITH THE SAME QUERY YOU WOULD USE ON THE ALARMING ONE.** *"Was I
  actually idle?"* is answerable from your own sent mail in one command, and **nobody ran it for an hour
  because the answer felt obvious.**
- **WATCH BOTH DIRECTIONS. A clock that fires TOO FAST is the expensive fault, and a seat told to watch
  for silence will never report it.** Gaps that are too long mean the chain is broken and you are awake
  by luck. **Gaps that are too short mean the clock is over-firing -- and every tick wakes a seat and
  spends a turn, so a runaway clock burns the very pool this ladder exists to protect.** *Measured
  2026-08-14: a burst of sub-minute ticks cost about 9 points of the shared 5-hour pool in nine
  minutes, and was projected to exhaust the window before its own reset.* **The monitor becomes the
  load.** State both bounds when you publish the heartbeat, not just the lower one.
- **State the margin, not just the mechanism.** *"600s ticks against a 900s doorbell"* tells a reader
  how much slack exists before the chain dies. **A mechanism with no stated margin cannot be audited.**
- **Treat a re-arming chain as a single point of failure**, not as redundancy. Each tick depending on
  the previous one means the whole watch has **one** life, not many.

**Exempt from the DISCIPLINE is not immune to the LIMIT.** You bill a pool and a hard cutoff will take
you like anyone else. **The difference is what you do about it: you do not pre-emptively stop, so your
protection has to be durability instead.**

- ***WRITE YOUR NOTE AT A RUNG, NOT CONTINUOUSLY*** -- owner-set 2026-08-28, and it **replaces** this
  section's former *"keep your episode note current continuously"* and *"write it after every warning
  you send"*. Write at **rung 1** or **rung 2**; when the window resets, go back to not writing.
  *(COMMON, Hand off so your successor can resume.)*
- ***THIS SEAT ASKED WHETHER IT SHOULD BE A CARVE-OUT AND ARGUED ITSELF OUT OF ONE.*** The old
  justification was that a Steward never stands down, so it has no wind-down in which to write.
  **But the exemption is from STOPPING, not from SEEING:** rungs still fire on your pool and you read
  the same banner as everyone. *So "the ladder is the warning" holds for you exactly as it does for
  them, and rung 1 leaves roughly twenty minutes of runway.*
- **What you record when a rung fires:** pools watched, last reading with its time, which pool is in
  which state, and who you warned and when. **A successor must be able to resume from the note
  alone.**
- **A successor must be able to resume from the note alone.** That, not your own survival, is the
  continuity plan.
### PRE-POSITION THE CONDITIONAL RESUME EVERY WINDOW, BEFORE THE CEILING, WHILE YOU CAN STILL MEASURE

***TWICE IN ONE NIGHT A PRE-POSITIONED INSTRUCTION WAS THE ONLY THING BETWEEN THE FLEET AND AN
INDEFINITE HOLD.*** *This seat went dark* **07:01Z to 11:09Z -- four hours, with RUNG 3 in force.**
*The first gap was three hours. The second was longer.*

> **A seat holding nothing cannot restart itself. A seat holding a conditional can**, *and it does not
> need you awake to do it.*

**WRITE IT WHILE THE INSTRUMENT STILL ANSWERS, NOT WHEN THE RUNG FIRES.** *At rung 3 you may already
have lost the reading -- this seat lost it to four straight 429s in one window and a peer read for
it.* ***The conditional is cheapest to write at rung 1 and worth nothing unsent.***

**AND ITS TEST MUST USE THE RESET INSTANT, NEVER THE COUNTDOWN** -- *a roll resets the countdown and
it burns down again, so a countdown cannot tell a new window from a dead one (`INSTRUMENTS` 4.15b
family).* **Say which instant the notice is about, and tell the reader to discard it if their own
read lands elsewhere.**

---

### LOG EVERY READING TO THE VAULT. Owner-set 2026-08-28

**Owner's words:** *"I want you to start tracking burn rate in a central location in the vault. This
data will be used to build a chart and to track performance. It needs to be in the vault so all
Steward seats can log to it regardless of the account used by the ccd instance."*

```
pwsh -NoProfile -File scripts\coord\usage-log.ps1 -VaultRoot <vault checkout> -TokenFile <the pool you confirmed>.json [-Note "rung 2 fired"]
```

***PASS `-TokenFile` EVERY TIME, AND PASS THE POOL YOU CONFIRMED IN SECTION 1 UNDER "YOUR FIRST ACT:
confirm WHICH ACCOUNT you are watching". THE SUBJECT YOU CONFIRMED AND THE SUBJECT YOU LOG ARE THE
SAME FACT.*** **Its default is a SPECIFIC pool** -- `messagefoundry.json`, at `usage-log.ps1` line 39
-- **and it is wrong for every other one.** *This entry omitted the parameter until 2026-08-29, so
the command as documented was a live defect.*

> ***AND IT DEFEATS THE FIRST INVARIANT BELOW WHILE SATISFYING IT SYNTACTICALLY, WHICH IS WHY NOTHING
> REPORTS IT.*** **Measured by the STEWARD on itself, 2026-08-29:** *a `-DryRun` of the command as
> documented produced a WELL-FORMED row -- org `b11dff81...`, account `<EMAIL-REDACTED>`,
> five_hour 100.0, weekly 98.0 -- while that seat's own pool read five_hour 32.0, weekly 7.0.* **The
> row carried a subject. It carried the WRONG one, and the exit code was 0.** *The record is
> append-only by design, so such a row is corrected only by appending a `supersedes` row, never
> removed.* ***AND IT COMPOUNDS TRAP 8.8a: the default names the pool the fleet was on BEFORE the
> last account switch, so a successor arriving after any switch gets a plausible reading and never
> learns the subject moved.***

**THE POOL IS DELIBERATELY NOT NAMED HERE.** *The reporting STEWARD asked that it not be, and was
right: today's pool is tomorrow's stale copy, which is trap 8.8a once more.* ***"Pass what you
confirmed" does not go stale; a pool name does.*** **The narrower fix -- showing one explicit
`-TokenFile` example -- was rejected for that reason: it would have dated this entry to one account.**

*The script's own default is a code change and belongs to whoever owns `scripts/coord/usage-log.ps1`,
not to this file. Correcting the documented command alone removes the failure for anyone who follows
this playbook.*

*It takes its own reading, resolves the org from `accounts.json`, stamps provenance and appends.
`-DryRun` prints the row without writing.* **It refuses to write rather than writing something
wrong.** The record is `docs/usage/burn-history.jsonl`; `docs/usage/README.md` holds the schema and
rotation. *All four artifacts verified present on vault `origin/main`.*

***THE FOUR INVARIANTS MATTER MORE THAN THE PATHS, AND EACH CAME FROM A MEASURED FAILURE:***

| invariant | why |
| --- | --- |
| **Every row carries its subject** | `org` and `account` are mandatory and the writer exits 6 without them. **A percentage with no pool is a number, not a reading** -- trap 8.8a in data form, and a chart over subject-less rows blends pools and is confidently wrong with no symptom |
| **Append only** | Correct a wrong row by APPENDING one carrying `supersedes`. Never edit |
| **Record what the instrument printed** | Reset countdowns stored as the verbatim strings the tool emits, not parsed. **On `UNKNOWN` the writer logs NOTHING and exits non-zero** -- an absent row is honest, an invented one is not |
| **NO RATE IS STORED** | ***The one most likely to be "improved" later.*** Measured across one evening the same pool ran **+64, +110, +48, +105, +89 and +79 per hour.** THERE IS NO SINGLE RATE, so storing one bakes an interpretation into the record and hides the choice. Levels and timestamps in; the chart picks its window and says which |

> ***AND THE BUG ITS AUTHOR SHIPPED FOR TEN MINUTES BELONGS HERE MORE THAN THE SCHEMA DOES:
> `usage-now.py`'s EXIT CODE IS A BAND, NOT A SUCCESS FLAG.*** **`0` OK, `10` WARN and `11` CRITICAL
> are ALL READINGS; `20` is `UNKNOWN` and is not.** *The first version treated any non-zero as
> failure, so against a pool at weekly 98 it* ***REFUSED TO LOG -- a hole in the record at exactly the
> rung the record exists to show.*** **Nothing would have reported the gap; the chart would simply
> have had no points at the interesting moments.**

**It is the inverse of the `for-each-ref` case in INSTRUMENTS 4.15b** -- *there `exit 0` was the
untrustworthy answer; here non-zero was wrongly read as failure.* ***EXIT CODES MEAN WHAT THE TOOL
SAYS THEY MEAN. Read the contract; do not assume the convention.***

**Eighteen rows were backfilled from a transcript and marked `backfill:true`**, spanning a complete
5-hour window -- 4 percent at 17:46Z through 97 at 18:54Z, the ceiling, the owner hard stop, and the
reset at 21:45Z. *That shape is not obtainable any other way, and it is marked so nobody mistakes it
for live logging.*

---

- **Stay cheap.** You are running while others stop, so keep the watch light -- read, project, warn,
  record. Do not start analysis you would not want interrupted.

**AND THE ONE THING THIS SEAT MUST NOT DO: LAUNCH A MULTI-AGENT FAN-OUT.** *Measured 2026-08-14, and
reported by the seat that did it:* a **1.33M-token** workflow run by the watching seat was the cause of
the only limit hit that day. **A watcher that spends the pool it guards has produced the one failure
this exemption cannot survive** -- the exemption exists so you keep measuring, and a fan-out converts it
into a licence to be the load. **It is the runaway clock above arriving through the seat instead of the
scheduler**, and it is worse, because the clock is not the thing telling everyone else to stop. If a
fan-out is genuinely needed, **it belongs to another seat.**

**IF A SEAT EXEMPTION EXISTS IN CODE, VERIFY WHAT IT SUPPRESSES BEFORE RELYING ON IT.** `watch.py` can
read a seats file and suppress the ladder's ACTION line for this seat. **Section 6 exempts the
DISCIPLINE, not the LIMIT**, so confirm that **the reading, the trigger-disagreement line, the 90
percent gate and the at-risk capture all still fire for you.** An exemption that quietly suppressed any
of those would leave you watching for everyone **except yourself**, which is the one blind spot the
whole seat is built to avoid.

---


> ***THE TOOL THIS SECTION NAMES IS NOT ON `main` YET. Measured 2026-08-29:*** `scripts/coord/token-collect.py`, `docs/usage/TOKENS.md` *and* `docs/usage/token-history.jsonl` ***are ABSENT from vault `origin/main`*** *-- with a control on three files that ARE present (`roles/STEWARD.md`, `roles-save.ps1`, `burn-history.jsonl`). The collector exists on `origin/lander-burn-rows`: 1 hit across 898 branches. The Steward that built it held it back deliberately -- its adversarial phase ran and its findings were applied, but 1,491 lines had not been read line by line, and the last hour of the week is not when an unread instrument goes on main.*
>
> **SO THIS SECTION IS A DOCUMENTED INTENTION, NOT A RUNNABLE PROCEDURE, UNTIL THAT LANDS.** *Running the command below today returns file-not-found, and the reason belongs here rather than in your terminal.* ***CHECK FIRST:*** `git cat-file -e origin/main:scripts/coord/token-collect.py` *-- when that exits 0, delete this banner.*

### AND LOG PER-SEAT TOKENS BESIDE IT. Owner-set 2026-08-29

**Owner's words:** *"start tracking token usage ... I want to be able to see how many tokens each seat is using ... I want the Steward role to do this NO MATTER WHICH ACCOUNT IS IN USE ... I also want to be able to PLOT THE BURN RATE BY SEAT, so capture data in a way that supports that axis too."*

The sibling of the burn log above. **That one records the plan METER, a percentage of a pool. This one records the TOKENS behind it, per session, with the seat attached.**

```
python scripts\coord\token-collect.py --vault-root <vault checkout> --logger-seat steward --logger-session <your session id>
```

*Run it on the same cadence as your burn reading. A warm run costs about 2 seconds and opens 8 of 16,453 files; the first run on a new box costs 36 seconds and rebuilds everything.* Record: `docs/usage/token-history.jsonl`. Schema, reading rules and limits: `docs/usage/TOKENS.md`. **It is the only supported writer.**

**IT IS ACCOUNT-INDEPENDENT BY CONSTRUCTION, AND THAT WAS MEASURED RATHER THAN ASSUMED.** It discovers every `~/.claude*` directory that holds a `projects/` subdirectory and reads all of them, so a seventh account arrives with no code change and it does not matter which account your CCD instance is using. *Verified 2026-08-29 by invoking it once under each of the six `CLAUDE_CONFIG_DIR` values against one frozen cursor: identical accounts walked, identical per-account file counts, identical seat census.* **The cursor lives at `%LOCALAPPDATA%\MessageFoundry\token-cursor\<box>.json`, per BOX and not per account, which is what lets the next Steward pick up where you left off.**

***RATES ARE DERIVED, NEVER STORED. GROUP BY (session, account), NOT BY SEAT, then difference, then roll up to seat.*** A seat-level rollup cannot be differenced: **when a seat gains a session between two samples the rollup jumps by that session's entire lifetime accumulation and reads as a burn spike that never happened.** Four predecessor chains in this corpus would each produce one.

***THREE READINGS THAT ARE WRONG AND LOOK RIGHT:***

| do not | because |
| --- | --- |
| **plot all four counters** | `cache_read_input_tokens` is about 40x the metered mass, so the chart becomes a chart of cache reads with the signal invisible inside it. **Metered is `input + output + cache_creation`** |
| **filter to named seats** | that is **29 percent of the burn**, every bar correct. Just over 70 percent sits under `(unattributed)` and `(undeclared)`, and the sentinels exist so that mass is a plotted series rather than a silence |
| **trust a `seat` without its `seat_basis`** | **a seat without its basis is a guess wearing a name.** `worktree-inferred` rows carry `inference_overlaps_declaration`, which is **false on 37 of 37 today** -- often right, never confirmed |

***RUN `--reconcile` DAILY, AND KNOW WHY.*** It is the only control that catches a cursor which has silently stopped advancing -- **and until 2026-08-29 it PASSED that exact failure.** The old rule compared a stale cursor against a fresh rescan, so it had to permit a positive delta, and *a stalled cursor IS a positive delta*: a **45.5 million token hole** printed `delta +46,651,399 (live fleet growth is expected)` and **exit 0**, character-identical to the healthy `+18,640` baseline. It now advances a COPY of the cursor first and requires **per-session equality**. **Any mismatch it names is a defect, whichever sign it carries.** It is the same shape as the exit-code trap above: *the instrument answered an adjacent question and the answer looked like health.*

**RUN `--self-check` AFTER ANY EDIT TO THE COLLECTOR.** *21 controls, 78 assertions, each run in its FAILING state first, on synthetic fixtures -- no corpus, no network, about two seconds.* **A control that has only ever been green is not evidence**, which is how the old control 9 shipped an `OR` its own fixture satisfied through one branch.

**Rows written before `token-collect.py/1.1.0` carry one wrong seat.** *Session `2bb4514a` reads `labserver`; it was a lander session, and the label came from **directory-name ordering**, not from anything about the session.* **`instrument` is the discriminator, the record is append-only, and those rows stay -- do not edit them.** Reading by the procedure in TOKENS.md needs no special handling, because the seat comes from the LATER row.

## 7. NOBODY IS OWED A RESTART

**The cron tells nobody to stop, so it owes nobody a restart.** A Builder is one turn and then its
process exits, so there is no held session to wake.

**Publish the window reset time as a field of the reading.** That is all this section now asks for.

***RETIRED 2026-09-01: this section previously carried a wake-and-resume duty*** -- owner ruling
2026-08-13, *"You told them to stop; you owe them the restart"* -- **with a null-case precondition, a
wake list, a warned-set record and a set of arrival checks.** None of it has a performer now.

***THE TABLE BELOW IS A GENERAL FACT ABOUT REACHING A COLD SESSION, NOT PART OF THE CRON'S SPEC.***
It belongs in [COMMON.md](COMMON.md), and it is held here only until it lands there.

| channel | wakes a seat? |
|---|---|
| **File mail** | **only within ~15 min of its last stop.** Working, leaves a receipt, **cannot reach a cold seat** |
| **`send_message`** | reaches a cold seat **when healthy**. Health is build-dependent; "Message sent" is a claim, not an observation |
| **The seat clock** | **confirmed working** -- it survived the relaunch and woke eleven seats |

*Expiry: re-measure after any Desktop or engine version change. **This entry is build-specific and is
expected to go stale** -- check the version before relying on either half.*

---

## 8. Traps

**8.1 Warning so often nobody reads you.** A warning that fires on healthy cases trains every seat to
discount it, so it is absent on the day it matters. **Warn on state transitions, not on readings.** A
pool that is state 1 and stays state 1 does not need re-announcing.

**8.2 Reading a level and calling it a rate.** Two readings make a rate; one reading is a level with a
story attached. If you have only one sample, **say the projection is unavailable** rather than
estimating from a single point.

**8.3 Turning into a rationer under pressure.** The pull is strong at state 2 and 3 -- suggesting
someone drop work *feels* like helping. **It is outside the seat**, it contradicts the owner's standing
rule, and it costs work that had headroom. **You say how long they have. They decide what to do.**

**8.4 A stale reset time reading as a fresh window.** A reset time that has passed means your sample
predates the window it describes. **Re-read before warning on it**; a crossed reset makes a scary
number harmless and a calm number meaningless.

**8.5 Relaying a peer's usage figure.** It carries their pool, their sample time and their instrument.
**Measure the pool you are warning about, or attribute the number and its age** -- "as of 4 minutes
ago, per session Y" -- so the recipient can judge it.

**8.6 Escalating on percentage while the rate says otherwise.** The levels are a backstop. If the rate
projection and the level disagree, **the projection is the one to act on** -- and say both, so the
recipient sees the disagreement rather than inheriting your resolution of it.

***OWNER-RATIFIED 2026-08-14, asked directly after this rule was contradicted in the field: RATE
GOVERNS.*** The ruling settled a live contradiction, so it is recorded here with what it does **not**
change.

- **THE LEVEL STILL FIRES, AND THIS IS NOT A DOWNGRADE.** It triggers the **cheap protect action** --
  commit what you have, capture the at-risk sweep. **That costs nothing and loses nothing**, so a
  backstop firing is a real trigger and a stop sent on one was correct to send.
- **WHAT THE LEVEL STOPS DOING IS HALTING NEW WORK WHEN THE BURN SAYS THERE IS ROOM.** That is the whole
  change, and it is where the damage was: **2h37m of hold against a 48-minute real wait, by one builder
  alone.**
- **The inverted form -- "a level beats a rate, always" -- was propagated by four seats**, one of which
  abandoned a *correct* measurement to adopt it. **If you took "act on the level" from anyone, drop
  it.** COMMON 4.9.6i has the mechanism, and 4.6.11 has why nobody argued.

***8.8 CONFIRM THE SUBJECT BEFORE REFINING THE PREDICATE. A control that proves your reading is LIVE
does not prove it is YOURS -- before you grade a pool, confirm the fleet is ON that pool.*** Requested
by the Steward seat 2026-08-14 and **it is the most expensive trap on this list**, because it defeats
the other seven: **every rule above tests the NUMBER, and none of them tests the SUBJECT.**

**IT BEAT THREE CAREFUL, INDEPENDENT ANALYSES IN A ROW, each correcting the last:**

| | reasoning | verdict |
|---|---|---|
| predecessor, 03:27Z | pre-positioned a resume from weekly **38 percent** | impeccable, wrong pool |
| this seat, 21:47Z | **corrected** it to weekly **92 percent**, rewrote the conclusion | impeccable, wrong pool |
| this seat, 18 min later | **three samples with a working control** -- checked the reset countdown moved, specifically to rule out a frozen cache -- diagnosed a lagging estimator | impeccable, wrong pool |

**THE THIRD ONE IS THE INSTRUCTIVE ONE.** It did everything this file asks: verified the number,
verified the sample age, and **asserted a control that had to behave differently if the reading were
stale.** The control passed *because the reading really was live.* **A liveness control cannot detect
a subject error** -- it confirms the instrument works, on whatever it is pointed at.

***8.8a AN OWNER CONFIRMATION FIXES A FACT, NOT A SUBJECT -- AND A POOL IS A FACT WITH A SHELF
LIFE. RE-DERIVE THE SUBJECT ACROSS ANY BOUNDARY THAT COULD HAVE MOVED IT, HOWEVER WELL ATTESTED.***
Requested by the replacement Steward seat, 2026-08-28, from a near-miss it measured on itself.

**8.8 and s2 both assume the subject is UNKNOWN or INFERRED. This one was NEITHER** -- it was pinned
by an owner confirmation, the strongest instrument this seat has, **and the confirmation was
correct when made.** *An account switch then moved the fleet, and a true line became a true reading
of a pool nobody was on.*

| pool | reading | what it meant |
|---|---|---|
| `meforsupport` | 5-hour **98 to 100**, capped | ***the pool the fleet had LEFT*** |
| `messagefoundry` | 5-hour **4 to 9**, both windows rising | the pool it was on |

**Followed literally, the inherited header would have broadcast URGENT STOP to eleven seats sitting
on 91 points of headroom** -- the harm s4 names outright.

> ***AND THE `DO NOT RE-DERIVE IT` PATTERN IS THE ACTIVE HARM, NOT AN ASIDE.*** *That instruction
> exists to stop drift and is good at it.* **It also reads as an instruction not to run the one
> check that would catch expiry, so the stronger the attestation, the less likely a successor tests
> it.** ***The instruction protecting the fact is what hides its expiry.***

**A *do not re-derive* carries an implied *unless the boundary moved*, and a successor will not
supply that clause unaided. Write the boundary beside the attestation.**

***THE LOUDEST POOL IS THE ONE GUARANTEED TO BE WRONG AFTER A SWITCH.*** *`meforsupport` read 100
percent PRECISELY BECAUSE the fleet had left it -- exhaustion is what caused the switch.* **s2
already says a high level is not the fingerprint; here the high level is CAUSALLY DOWNSTREAM of the
subject having moved.**

**Bounded, in the reporter's own words: one switch, one fleet, one evening -- a mechanism and a
near-miss, not a calibration.** *Its three-way derivation was published BEFORE the owner confirmed
it and agreed with it, so the request does not rest on the inference being right.*

**THE INSTRUMENT ADMITS IT IN A PARENTHETICAL THAT IS TRIVIALLY READ PAST:** *"(desktop app's current
account -- no record for this session)"*. On 2026-08-14 it printed URGENT STOP and *"exhausted in under
a minute"* roughly **six times, all correctly**, about a pool with **zero fleet traffic**, while the
fleet worked comfortably on another.

**THE GENERAL FORM, and it is not confined to pools:** *whose is this* is a **different question** from
*is this real*, and every control in this file answers the second. **Ask the first one out loud.**
Section 2 carries the method that answers it for a pool.

**8.7 Reporting a quiet seat as DARK.** *A live misclassification, 2026-08-14, self-reported:* a seat
was logged as **"DARK ~3h09m"** with a correct caveat underneath. It was user-driven, healthy, and had
missed nothing. **Label the column "no activity for N" and let the reader judge it** -- *dark* is a
verdict wearing a measurement's clothes. **Carry clock status as an ATTRIBUTE beside the gap, never as
a FILTER:** a seat missing from a tick line is **unexplained**, not exempt, and filtering it out deletes
the one row worth looking at. And the half that generalises well past this seat -- **a correct caveat
under an incorrect label is not a correct report.** Labels travel; caveats do not.

---

## 9. Expiry conditions

Every standing rule here carries one, per [README.md](README.md).

| Rule | Stops being right when |
|---|---|
| **The three states and their levels** | **YOU recalibrate them from experience data** (section 3, owner ruling) -- or the owner does. They are a starting calibration, not a ratified constant; expect them to move |
| **Time triggers 20 / 10 / 5** | Same -- **yours to tune on measurement.** A 20-minute warning that routinely arrives too late is evidence, not an inconvenience |
| **Your authority to tune them** (the ruling itself) | The owner reclaims calibration, **or a tuned threshold is measured to have made a warning arrive too late.** The second is the one to watch: it is self-inflicted, and it will present as the ladder failing rather than as the tuning failing |
| **The 90 percent gate stays owner-set** | The owner says otherwise. **Not lifted by the tuning grant** -- it is a decision rule, not a level (section 3) |
| **Burn rate is primary** | Only if a rate becomes unmeasurable; then the levels become primary and **say so in every warning** |
| **You do not ration** | Never, short of the owner reversing the standing full-speed rule directly |
| **Confirm the account before watching** | Never, while more than one account exists on the machine. If exactly one ever remains, confirmation becomes a formality -- **verify that, do not assume it** |
| **You are exempt from the ladder** | The owner says otherwise, or a second Steward runs and one can safely stand down |
| **Wake and resume on reset** | Never, while the ladder can stop a session. It is the ladder's bottom rung |
| **The cron owns usage watching** | **The newest row in `docs/usage/burn-history.jsonl` is older than the tick interval** -- the cron has stopped, and usage watching is the Lander's |
| **The 90 percent Workflow rule is subsumed** | It is owner-set; if the levels above are relaxed past 90, it binds again on its own terms |

---

## 10. Live state goes in the burn log, never here

Current readings, which pools are in which state, the burn rates measured: **none of that belongs in
this file.** It goes in `docs/usage/burn-history.jsonl` in the vault, appended by
`scripts\coord\usage-log.ps1` -- the log this file already requires under *LOG EVERY READING TO THE
VAULT*. **`docs/usage/README.md` states that log's invariants, and they are not restated here.**

This file states what will still be true after every current pool resets. **A number in here would be
false within the hour**, and a file mixing the two decays into a *trusted* document that is *wrong*,
invisibly, because the durable half stays right.
