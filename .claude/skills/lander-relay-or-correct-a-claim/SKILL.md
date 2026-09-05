---
name: "lander-relay-or-correct-a-claim"
description: "Relay, correct or broadcast a claim to peers or the owner. Use before sending a caution, a correction, or a finding about someone else's work."
user-invocable: true
disable-model-invocation: false
---

# lander-relay-or-correct-a-claim

> Task rules for the Lander seat, split out of [LANDER.md](../../../roles/LANDER.md) on 2026-09-05.
> The prohibitions that bind before this task starts stay in that file. Read it first.

### AUTHORITY questions vs SEVERITY trade-offs -- do not conflate them

Holding a PR is correct for an **authority** question and wrong for a **severity** one. The failure
mode is generalising the first habit onto the second.

| Kind | Rule |
| --- | --- |
| **AUTHORITY -- hold** | *"Is this rule ratified?"* A merge would lend a contested rule the appearance of settlement. |
| The measured pair | Two PRs were correctly held on this basis, both resting on owner rulings relayed by another session rather than witnessed here. |
| How both resolved | **The session that HAD the owner's instruction took the action itself.** *"I can verify that YOU armed it; I cannot verify what someone told you"* is the cleanest statement of the line. |
| **SEVERITY -- decide** | *"Which of these two harms is worse?"* That is lander judgment and the owner has delegated it. |
| The measured error | A PR was held on severity grounds and it was WRONG. Holding it kept a security gate that could not fire, to protect one stale sentence in a vault-only document. |
| **The tell** | If you cannot name the *decision only the owner can make*, you are not holding for authority. You are hesitating. |
| Why a bad hold costs | A caution that fires on healthy cases trains everyone to ignore it, so it is absent on the day it matters. |
| **Funding a feature is not owning its bugs** | Measured 2026-08-22: a seat framed a known-wrong label in a shipped reporting feature as an owner call because the owner had funded the feature. |
| Why that is wrong | *"Do we ship a reporting feature with a known wrong label"* is an engineering decision, whoever paid for the work. |
| **EXPIRY** | The owner withdraws a delegation this file records. Check by reading their words, never by inferring from who funded what. |

### Do not enforce a ruling that exists nowhere in the repo

The owner's content policy was relayed as a constraint to **four** sessions before anyone checked. A
session grepped every local and remote ref and found nothing, because there is nothing. It is real,
it was stated twice in chat, and it is recorded in **no file**.

That is the standing this section refuses from other sessions, applied to your own relaying. **If you
are going to constrain another session's work with a ruling, either point at the file or say plainly
that it is context rather than constraint.**

Ask the owner where it should live. An ADR is the defensible home, since ADRs are explicitly kept for
security review.

### 4a-quater. A broadcast caution has a cost, so check whether the hazard is already closed

You are the seat that messages every lane, so a caution you send is adopted by sessions with no cheap
way to check it. They spend real time on it, or discount a result that was fine. Neither shows up as
a failure anywhere.

**Measured 2026-08-13.** A build session reported that the primary checkout's venv resolved to their
worktree. The lander reproduced it and got a worse answer: it resolved to the lander's. Two sessions,
two results, one venv. That disagreement is the only reason it was tested rather than relayed.

Measured from three directories with the same interpreter:

```
cwd = C:\           -> the PRIMARY's package     correct
cwd = the primary   -> the PRIMARY's package     correct
cwd = a worktree    -> that worktree's package   ordinary shadowing
sys.path[0] = ''    <- printed BOTH times, decisive, read by NEITHER of us
```

| Item | Rule |
| --- | --- |
| The venv was never misconfigured | Python puts the working directory first on `sys.path`. Two seats measured CWD RESOLUTION and reported it as VENV CONFIGURATION. |
| What that would have cost | Someone repairs a correct venv, and every lane distrusts its own green. |
| The hazard was already closed | The narrowed caution went to four lanes. One was immune by an ENFORCED PROPERTY, not by luck. |
| The enforced property | `scripts/asvs/scorecard.py` has zero first-party imports, and `tests/test_asvs_verifier_vault_contract.py` pins that. |
| How the pin is proven able to fail | `non_stdlib()` over every mirrored tool's import roots, exercised against a deliberate mutation. |
| Why that failure would be silent | A non-stdlib import does not red the gate. It STRANDS the auto-mirror. |
| Before broadcasting a caution | Ask whether the thing is already closed by a property somebody enforced, and grep for the test that would pin it. |
| What a needless caution costs | It trains lanes to discount your warnings. That is the currency you need on the day one is real. |
| State your scope | Say which parts of the estate you verified, and say plainly which you did not check. |

### 5c. Verify a peer's MECHANISM, not just their conclusion

A session handed over two auth defects. Both conclusions were right and both mechanisms were wrong,
and filing the mechanisms as reported would have produced the wrong fix.

Read the code and test the shapes, then tell the peer. In that case they verified the corrections
independently and found a sharpening that had been missed.

### 6a-ter. The count was right and the identity was wrong

| Item | Rule |
| --- | --- |
| The measurement | A baseline was relayed as "expect ONE pre-existing failure, and it is `X`". |
| What two lanes measured | On one commit, on one day: **1 failure and 19**, an eighteen-failure spread across two venvs, and `X` passed in both. |
| What the single failure actually was | An unrelated stale editable install. |
| Why identity is the worse error | A wrong count is noticed the moment someone recounts. A wrong identity survives every recount, because the number keeps agreeing. |
| The rule | When a baseline or known-failure set is relayed, carry the NODE-IDS, not the cardinality. |
| If the identity cannot be pinned | Delete the number rather than repair it. A figure corrected three times is a figure nobody should be quoting. |

### 6h. Hedging does not reduce the cost of a claim you could have measured

Source of record: COMMON.md, rows *Hedges* and *The alarming sentence*.

| Item | Rule |
| --- | --- |
| Measured here | A draft asserted a merge strategy would interleave items and that a gate "could plausibly" pass the wreckage. |
| What the real tools said | The interleaving does not happen, and when the strategy does mangle an item the gate catches it loudly. |
| Why the false version got written | *"A silent corruption that passes its own gate"* is a better story than *"a loud failure you would catch"*, so it would have been quoted onward. |
| The rule | The cost of being wrong scales with how good the sentence sounds. Marking a claim uncertain is not a substitute for measuring it when measuring costs one command. |

### 6i. Print what you scanned, not a count

| Item | Rule |
| --- | --- |
| What the discipline caught | A markdown anchor miscounted as a citation, backslash-escaped tokens an anchored regex could not see, a blob-versus-worktree line-ending error, and a wrong "18 unmarked citations" report. |
| Why that last one mattered | It would have contradicted a correct peer. |
| State the SCOPE with the number | Item counts are scope-specific and look like disagreements. A parser over `main` gave 335 and over a branch adding one item gave 336. Neither is wrong. |
| State the CONVENTION with the number | Two sessions comparing hunk headers appeared to have drifting line numbers. One reported with default `-U3` context and the other measured with `-U0`. |
| What that nearly was | Every header started three lines earlier in one view, one step from a false alarm about a contested file. |

### 6i-bis. A verdict is a lossy projection, and what it discards is the evidence the check was misaddressed

*Print what you scanned* is written against a check aimed correctly and counting wrongly. This is the
other one: a check aimed at the WRONG OBJECT still returns a confident verdict, and the verdict is
exactly the form in which the misaddressing becomes invisible.

| Item | Rule |
| --- | --- |
| Measured 2026-08-12, and the lander got it wrong | A lane reported a worktree-removal safety argument as `45145ad0 -> b2a42d06`, meaning commit `45145ad0` has patch-id `b2a42d06`. |
| What the lander did | Read the arrow as commit to commit, computed `patch-id` of a "commit" that does not exist, got an empty second term, and printed `DIFFER or unresolvable`. |
| How close that came | One step from telling the lane its safety argument for a DESTRUCTIVE action did not verify. |
| What caught it | The raw value, and nothing else could have. The line read `pa=b2a42d060f99`, which visibly begins with the token quoted in the message. |
| What the number was saying | *"I am the patch-id you named"*, while the verdict line said *"mismatch"*. |
| Why a boolean would have been believed | It carries no trace of that, and it warns about destruction, which is the direction that gets acted on immediately. |
| The durable formulation, and it is the lane's | *"A verdict is a lossy projection of a measurement, and the loss is exactly the part that would have shown the check was misaddressed."* |
| Rule 1 | Print the OPERANDS, not just the comparison: `pa=... pb=...` beside the verdict. |
| Why | An empty operand is the signature of a check pointed at nothing, and it renders identically to a legitimate mismatch once collapsed to a boolean. |
| Rule 2, the one nobody does | LABEL THE UNIT when you report a hash to another session. Write `45145ad0 (commit) patch-id=b2a42d06`. |
| What never to write | An arrow between two hex tokens of the same length family. An arrow between like-shaped tokens reads as same-kind by default. |
| The cost of the fix | Four characters, and the class is gone. |
| Note the shape of the fix | It sits on the SENDER, and the sender was not the one who erred. When a misunderstanding needs care to avoid, put the fix where care is not required. |

## 16 / 16a. A right answer stops the checking, so grade the LABEL and the INSTRUMENT separately

Source of record for the general discipline: COMMON.md, *Measure it before you conclude* and *A green
light proves only what the gate asserts*. Two landing-specific instances anchor it.

**The label.** Six assessment cells moved between grades after a ruling. The movement was relayed under
one cause in a taxonomy; it was a different cause, and a build session caught it.

**The conclusion was correct under either label** -- no regression, zero code changed -- so no sentence
read wrong and there was no tell. **In a taxonomy whose purpose is that the label carries the meaning,
the label IS the substance.** A right-sounding conclusion is exactly what stops anyone re-checking the
label. When you relay a categorised finding, verify the category separately.

**The instrument.** Asked whether rescued ref `bb399457` was a discarded rebuild of a wide
commit-message classifier, a peer grepped its blob for three tokens, got nothing, and concluded
correctly. Re-run across three refs, that predicate and a discriminating one read:

    the ref under test        0     discriminating predicate:  8
    main                      0                                7
    the branch that HAS it    0                               12

**Zero on the positive control.** The predicate does not discriminate. It cannot separate *"the thing
is absent"* from *"those are not the words this code uses."* It agreed with the truth by coincidence.

The ref **did** carry a classifier, just the narrow one, so the stated finding *"carries no classifier
at all"* was false while the conclusion built on it was true.

| Item | Rule |
| --- | --- |
| A hand-run grep is a gate that runs once | Before believing an empty result, run the predicate against a ref that MUST match. Cost: one command. |
| What a zero on the control means | The instrument is blind and the result means nothing. It fails the same way a CI gate does, minus the review that would have caught it. |
| Prefer object identity to absence | The clean proof was one command: the ref's blob is **byte-identical to a file already on `main`** at a known commit. Not a lost artifact, a historical state. |
| The same move elsewhere | It closed `a-1212-retention`: base tree == branch tree, so the branch was spent rather than blocked. |
| For "is this the artifact I want" | Reach for the OID before reaching for a search. **The strong measurement is also the cheaper one.** |
| Why this is worth a section though it broke nothing | It landed on the RIGHT answer, so nothing would ever have contradicted it, and the brief would have carried a claim whose stated support was empty. |
| The general form | **A true conclusion resting on nothing is more durable than a false one.** It is load-bearing, unfalsified, and cited onward. |

## 16b. The unmeasured claim is the one that is CONTEXT to the sentence you are arguing

Two sessions produced this independently, one hour apart, from opposite sides.

| Item | Rule |
| --- | --- |
| The measured instance | One message made two claims about BACKLOG `#1223`: that the defect was live, and that its fix lived in `api/app.py`. |
| Which was proved | The first, by running the shipped redactor. That was the harder claim and the one under examination. |
| Which was not | The second, asserted from siblings `#1224` and `#1225`. One `git show --stat` shows it lives in `config/wiring.py`. |
| The conjunction form | *"This closes release exit criterion 12"* when criterion 12 is a two-clause conjunction and only the second clause was met. Count the clauses before you close a criterion. |
| The mechanism, and it is not irony | Attention is a resource spent on the sentence under examination. The premise, the file path, the second clause and the framing ride through as context and get none. |
| Mid-correction is worse | Correcting is exactly when attention is most concentrated on someone else's claim. The over-claim above was written in the same edit that corrected someone else's. |
| Restatement launders | A claim CARRIED FORWARD gets no scrutiny. The peer's words: *"My 'bodies included' survived three messages because it was never the sentence under discussion."* |
| Why repetition feels like corroboration | By the third message it reads as established because it has been said three times and checked zero. Each restatement carries more social weight than the last. |
| The check | In any message making a correction or a finding, list the claims that are NOT the one you are arguing, and measure those. |

## 16c. When an instruction names a MECHANISM, the mechanism can be wrong while the intent is right

**Measured instance.** A lander told a session to file a new ledger row *"in the same commit"* as an
existing one. Complying literally meant `--amend`, which would have rewritten a SHA out from under an
in-flight review, the precise harm the same lander had warned against one message earlier.

The session filed a **separate commit**, satisfying the actual intent of one PR and the normal
code-plus-ledger train, protecting the review, and saying so and why.

**The instruction specified a mechanism when it meant an outcome, and the mechanism aged badly in the
minutes between writing and executing it.** That is normal and will keep happening. Instructions are
written against a state that then moves.

| Item | Rule |
| --- | --- |
| When executing | Deviate when the mechanism defeats the intent, and SAY that you did and why. |
| Why silence is the failure | Silent literal compliance that breaks something looks like obedience in review. |
| When instructing | Name the OUTCOME and let the executor pick the mechanism. They hold the newer state. |

## 16d. An OBSERVATION order is not an EVENT order -- polling makes them diverge

A lander polled a PR, saw `OPEN`, took a peer's handover, polled again, saw `MERGED`, and told the peer
*"main moved while you were writing, you are one merge behind, I will update-branch."* All false:

    the merge landed    20:22:00
    the peer's fix      20:38:46
    the peer's merge    20:45:43   <- 23 minutes AFTER the merge called "later"

The peer's merge commit already carried the new `main` as its second parent. Measured `0 behind`. They
were never behind.

| Item | Rule |
| --- | --- |
| Read ordering from the artifact | Commit and merge timestamps, parent edges, `--is-ancestor`, run `created_at`. These are the record. |
| What your own timeline is worth | "I saw X then Y" is a fact about your polling and the weakest possible evidence about X and Y. |
| The gap has no size | Nothing is observed between two polls, so a state you DISCOVER after an event can have preceded it by any amount. |
| What was available the whole time | The commit graph carried the true ordering. |
| It propagated | The peer accepted and repeated the false claim, in the same exchange where both were agreeing that unverified claims travel. |

## 16e / 16f. Counts and subject sets cannot establish EQUIVALENCE, and a CALMING number gets less scrutiny

**Measured instance.** A branch existed as a local ref and an origin ref, `10 ahead / 10 behind`. A
session compared **commit-subject sets**, found nine of ten identical and the symmetric difference
exactly two commits, and concluded *"same work, different arrangement."*

Every number was correct. The conclusion was wrong:

    origin tree  c4af7d85...      local tree  015d02ce...
    diff between the tips: 3 files, +313 / -44
    the fix's commit:  ancestor of origin?  NO      ancestor of main?  YES
    origin's main-merge took main at a commit PREDATING the fix -- which was also the merge-base

Origin was **missing a credential-redaction fix entirely.** Not two arrangements of one body of work.

| Item | Rule |
| --- | --- |
| Equivalence is a content claim | It needs a content instrument. A subject set answers *"were the same commit MESSAGES written"*, never *"is the same CODE present"*. |
| Why nine matching subjects prove nothing | They are equally consistent with identical trees and with a 313-line difference. |
| Say the blind spot out loud | When the load-bearing word is **unchanged**, **equivalent** or **already present**, state what a difference would have to look like to SURVIVE your instrument. |
| For subject sets | "Any content change that keeps the messages", which is most of them. Once that sentence exists the blind spot is obvious. It costs one line and it is the whole control. |
| Ranked, cheapest sound first | Tree OID equality, then `git diff` between the tips, then `--is-ancestor` for the specific commit, then content probes. |
| The rule | **Counts and name sets locate things. They do not conclude about them.** |
| The same family | Judging "unchanged" by a MULTISET of gate calls, which is blind to a swap between routes, and `--is-ancestor` under squash-merge. All three read a projection and report on the object. |
| Why the search stopped | The instrument was reached for to DOWNGRADE AN ALARM, and the first benign answer was accepted. |
| The peer's own diagnosis | *"I was not reaching for subject sets to prove equivalence. I was reaching for them to DOWNGRADE AN ALARM... and accepted the first instrument that produced a benign answer."* |
| Trigger and tell | Trigger: an alarm you want gone -- a scary count, a red you believe is spurious, a divergence you hope is cosmetic. Tell: you stopped at the first calming number. |
| The asymmetry | A measurement that confirms trouble gets re-run. A measurement that dissolves it gets banked. |
| So | Re-run the REASSURING measurement, not the alarming one. When you report relief, say which instrument produced it and what it cannot see. |

## 16g. An unverified claim compiled into an AUTOMATED system has no reader left to doubt it

**Prose has readers; instructions have executors.** A false sentence in a handoff gets argued with. The
same sentence in an agent prompt gets acted on, N times, in parallel, and every downstream artifact
inherits it. A session carried a false claim verbatim into the rules block of a running seven-agent
workflow.

Their own framing, which is the durable statement:

> *"An unverified claim compiled into an automated system stops being a sentence and becomes a premise
> nothing will re-examine. A human reader might push back on it; an agent executes it. The check has to
> happen BEFORE the claim becomes instructions, because afterwards there is no reader left to doubt
> it."*

| Item | Rule |
| --- | --- |
| Order of operations | Verify a claim BEFORE it becomes instructions. Afterwards there is no reader left to doubt it. |
| Pin the SHA, never the branch name | A review workflow named its subject by branch name seven times, and the tip was amended mid-run. |
| What that produced | Agents resolved the name at the moment each ran, so different agents reviewed different trees and nothing recorded which. |
| Why the second is worse | A false FACT is wrong, fixed, inspectable and refutable by anyone who reads it. |
| A MUTABLE REFERENCE never becomes false | No line of the script stops being true; the thing it points at changes underneath. **Re-reading it returns the new answer and confirms itself.** |
| A review is a claim about a TREE | Naming a branch makes it a claim about whatever that name means later. |
| A contaminated record | If a run finished on a premise you later found false, note it in the item even when the OUTPUT was correct. Whoever mines those transcripts inherits the premise without the correction. |

## 16h. A FALSIFIED MECHANISM attached to a TRUE conclusion outlives a wrong answer

A peer's statement, which is the sharpest form of the theme running through this whole family:

> *"A doc that gives a falsified mechanism for a true conclusion is the shape we have both been chasing
> all night -- a right answer resting on a wrong reason survives longer than a wrong answer, because
> nothing contradicts it."*

**Measured instance.** A lander saw three peer sessions whose `lastActivityAt` clustered inside 3.5
seconds and proposed that the listing call stamps the field, making it a heartbeat rather than an
activity signal. A peer tested it with two reads 28 seconds apart, nothing sent between:

    two sessions advanced   +46.5s and +39.1s
    the lander's own   UNCHANGED, byte-identical

A read does not stamp the field. The cluster's real cause was one question away: **the peer had just
messaged all three sessions**, so they activated together. The lander's argument was *"three
independently-driven sessions do not land that close"*: true, with a false premise, because they were
not independently driven at that moment.

| Item | Rule |
| --- | --- |
| Say when a control was accidental | The lander's own unmoving timestamp is what made the two moving ones mean anything. |
| Why | Two numbers that change prove nothing alone. They need a third that stayed put under the same read. |
| What silence costs | Otherwise the next reader believes the experiment was built to answer the question. |
| Before explaining a coincidence | Ask who ELSE touched the system. The lander reasoned from correlation to a property of the instrument without asking what other actor was in the picture. |
| Why they did not ask | They were the only sender they were thinking about. |
| Write three states separately | Here the race explanation survived, the heartbeat mechanism died, and whether `lastActivityAt` tracks mid-turn or process-alive **remains untested**. |
| So | Neither confirmed nor refuted. Do not let a dead mechanism drag down the conclusion it was invented to support, and do not let it prop the conclusion up either. |
