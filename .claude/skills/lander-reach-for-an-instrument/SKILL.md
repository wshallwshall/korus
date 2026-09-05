---
name: "lander-reach-for-an-instrument"
description: "Choose and read a git, gh or shell instrument during landing work. Use before trusting a count, a scan, an exit code, or a green check."
user-invocable: true
disable-model-invocation: false
---

# lander-reach-for-an-instrument

> Task rules for the Lander seat, split out of [LANDER.md](../../../roles/LANDER.md) on 2026-09-05.
> The prohibitions that bind before this task starts stay in that file. Read it first.

### 4e. Every suppression needs an expiry condition tied to its cause, written when the suppression is written

A watcher correctly skipped a class of failure while one root cause was unfixed. One root cause
failing N PRs is one fact.

Then the fix landed and the filter did not know. From that moment an unconditional skip would have
hidden a genuinely new failure behind a note asserting it was "known". That is the most convincing
possible way to not see something.

| Item | Rule |
| --- | --- |
| Narrow, do not delete | "Known issue, not waking" is true only until the fix lands, and nothing tells the filter that day arrived. |
| Prove both arms | Before restarting a watcher, prove the suppressed state suppresses AND the un-suppressed state wakes. |
| It generalises | Any standing "do not do X" resting on a transient condition needs its expiry written beside it. |
| Where exactly this inverted | *Compare against the INSTALLED copy, not against `main`*, on a machine-global install instruction. |

## 6. The dominant failure mode: instruments that are green and blind

Source of record for the general discipline: COMMON.md, *Measure it before you conclude* and *A green
light proves only what the gate asserts*. This section carries only what is specific to landing.

| Item | Rule |
| --- | --- |
| The shape | A check runs, returns green, and never could see the thing it is trusted to report on. It is worse than no check, because it turns "I should verify" into "I already know." |
| The tell | Never a failing check. It is a check that succeeds while pointed slightly off. |
| So | When a gate, diff or probe comes back clean on something you expected to be hard, name the question out loud and confirm the tool returns that same sentence. |
| Frequency | Nine instances surfaced across four sessions and not one of them errored. **Assume it is happening to you now.** |
| A FAILED control accuses two suspects, not one | Measured 2026-08-20: a lander ran a control against its own supposedly-unpushed commit, got 0, and concluded the tool was blind. |
| What was actually wrong | The tool was fine. An automation had already rescue-tagged the commit, so the PREMISE was wrong. |
| So | List both instrument and assumption as suspects, and test the cheaper one first. A premise is usually one command; re-deriving an instrument is not. |

### 6a. The instrument-scope table -- every one of these returned CLEAN or GREEN

| Instrument | What it answered | What was asked |
| --- | --- | --- |
| `git merge-tree A B` | does the whole BRANCH merge | does THIS COMMIT apply |
| `gh pr view --json files` | what does this PR CHANGE | what CONFLICTS |
| `git status` / repo state | the repo's cwd | the resolved path handed to the hook |
| `origin/main` is ready | is the SOURCE ready | is the checkout I INSTALL FROM ready |
| grep for a token | is the token PRESENT | is it an assertion or a QUOTATION of one |
| `hasattr(item, "statuses")` | attribute absent, so vacuously true | do items declare one status |
| a job conclusion | did the JOB pass | did the STEP pass |
| `--is-ancestor` | is it an ancestor | did it land (false under squash-merge) |
| filesystem path resolution | is it ON DISK | is it IN THE REPOSITORY |
| `rev-list <ref> --not --all` | nothing, because `--all` includes the ref and subtracts it from itself | is this ref's content held anywhere ELSE |
| `rev-list <head> --not --glob=refs/heads` on a branch worktree | nothing, because its own branch contains its head | would removing this worktree lose anything |
| `merge-base --is-ancestor <lane> <train>` | is the lane's tip reachable | did the lane CONTRIBUTE anything (vacuously true for a lane with no commits) |

| Item | Rule |
| --- | --- |
| The last row needs a TIMING qualifier or it inverts | "Zero own commits plus CONTAINED" has two causes that look identical: a lane that never had anything, and a lane whose work is already on main. |
| Which reading is right | Before integration the first, after it the second. A rule ignoring the moment it is run sends you re-checking work that landed safely. |
| The fix | Count the lane's own commits against the base it branched from, at integration time: `git rev-list --count <base>..<lane>`. Never against `main` afterwards. |
| THE SELF-SUBTRACTION TRAP | Any "is this held anywhere else" question computed over a set that INCLUDES the thing under test returns a clean zero for everything, and a clean zero reads as permission. |
| Who wrote both instances | People hunting this exact error class, one of them in the brief for the assessment that caught it. |
| The tell | 0 for every member, including ones you expect to be unique. Point the control at something you know is unheld and confirm it comes back non-zero. |
| The fix | Name the namespaces explicitly and leave the candidate out: `--not --glob=refs/heads --glob=refs/remotes`, and for a worktree, exclude its own branch. |
| A vacuous zero that happens to be right is still not evidence | Removing a clean branch-checked-out worktree loses nothing because the branch ref survives the removal, not because that measurement showed anything. |
| Why that matters | Same verdict, unrelated reason. A correct conclusion resting on a vacuous instrument is what stops anyone deriving the real one. |
| The cherry-pick case, one flag | `git merge-tree --write-tree origin/main <sha>` merges the BRANCH containing `<sha>`. |
| Setting the base | `git merge-tree --write-tree --merge-base=<sha>^ origin/main <sha>`. |
| Measured | The first form returned CLEAN and the second CONFLICT for the same commit, because the file it edits does not exist on `main` yet. |
| CHANGED-IN-BOTH IS NOT CONFLICTING | A lander told a PR owner its conflict spanned three files. It spanned one; the other two auto-merged. |
| The instrument | `git merge-tree --write-tree` answers the conflict question, and a file list never does. |
| What the error cost | It made a one-file resolution look three times larger. **An overstated blocker can deter the only party entitled to clear it.** |
| On disk is not in the repository | Untracked-but-present files exist in every working tree, so a guard resolving paths against the filesystem answers a question one step wider than the repository. |
| The check | Verify link-affecting changes against an export: `git archive $(git write-tree) \| tar -x -C <tmp>`, then run the guard THERE. |

### 6a-bis. A green that is a statement about the ENVIRONMENT is worse than an untested control

A control that has never been red is a claim. A control green for an environmental reason looks like
evidence, so it closes the question instead of inviting one. Three instances in one session.

| Item | Rule |
| --- | --- |
| `bash` from `PATH` | A negative control resolved `bash` from `PATH`, so its green was a fact about PATH order, not about the gate it exercised. |
| Inherited shell encoding | A lane's tests passed only because its shell exported `PYTHONIOENCODING=utf-8`. |
| What happened without it | The child's encoding was never pinned, so an em dash returned as cp1252 `0x97`, the reader thread died on `UnicodeDecodeError`, and stdout arrived as `None`. |
| Why that is the dangerous kind | It would have passed one platform and failed another. |
| An inherited baseline | A "known pre-existing failures" baseline passed between sessions was an artifact of which interpreter each venv resolved. |
| Defence 1 | Pin the environment INSIDE the thing under test, not around it: fix the child's encoding, resolve the interpreter explicitly. |
| Defence 2 | Prove the fix is not itself environment-dependent by running it under several ambient conditions, including a hostile one. |
| Defence 3 | Never inherit a baseline. Measure your own and diff it node-id by node-id (`comm -13` and `comm -23` both empty), never by count. |

### 6a-quinquies. A control that cannot RUN where the answer would be "no"

Distinguish this from *A green that is a statement about the ENVIRONMENT*, its nearest neighbour.
There a control runs and passes for an environmental reason. Here it DOES NOT RUN AT ALL, and its
not-running is indistinguishable from passing in the leg's verdict.

This section's own remedy cannot reach it: "confirm the tool returns that same sentence" fails when
the tool returns no sentence.

| # | The control | What it could not see |
| - | --- | --- |
| 1 | 13 worktree-gate suites, green for months | ZERO carried a backslash-escaped-quote case, and two live fail-opens sat behind them. Could not see the CLASS. |
| 2 | an escaped-quote suite's verb parametrisation | Both verbs denied by the SAME rule, so it exercised its own parametrisation. Could not see the PROPERTY. |
| 3 | an installed-gate parity test | SKIPS whenever `~/.claude/hooks` is absent, always true on a hosted runner. Could not see the MACHINE. |

| Item | Rule |
| --- | --- |
| Why instance 3 has teeth | A security fix can merge GREEN while the developer box keeps running the version with both fail-opens open, and no CI leg can report it. |
| The test is not at fault | Its skip text already reads *"SKIP (nothing compared) ... nothing is enforcing"*. The author saw it and labelled it honestly. |
| Why the label does not save it | It lives in a SKIP LINE, and a skip line is not the leg's verdict. A green leg and an unrunnable check render identically to anyone reading the summary. |
| So | **You cannot word your way out of this one.** |
| The question | Not "is this control green", but "on the machine, or in the configuration, where the answer would be NO, can this control RUN AT ALL?" |
| The remedy | Enumerate where the control cannot execute before trusting a green. |
| Why enumeration is the only route | A control that fires only on a developer box is not covering CI; one that fires only in CI is not covering the box; neither will ever say so. |
| Who found them | All three were found by someone other than the control's author. Three more measurements behind the outside-vantage rule. |

### 6a-sexies. "Already up to date" is not evidence anything merged, so assert the ref MOVED

`git merge FETCH_HEAD` exits 0 and prints "Already up to date." in at least two states where it merges
nothing. Both measured.

| state | how you arrive | what it looks like |
| --- | --- | --- |
| (a) `FETCH_HEAD` empty | a FAILED `git fetch <ref>` | rc 0, "Already up to date.", HEAD unmoved |
| (b) `FETCH_HEAD` FULL, every entry `not-for-merge` | a routine, successful `git fetch origin` | rc 0, "Already up to date.", HEAD unmoved |

| Item | Rule |
| --- | --- |
| (b) is the one people miss | Measured: 4,821 bytes, 35 entries, 35 marked `not-for-merge`, 0 mergeable. |
| The mechanism | A bulk fetch writes every branch into `FETCH_HEAD` and marks them all not-for-merge, and `merge` consumes only unmarked entries. |
| Why (b) is the dangerous one | State (a) fires only after something already went wrong, so there is a failed command upstream to notice. **State (b) fires on the happy path.** |
| The obvious defence, recorded as REJECTED | "Check `FETCH_HEAD` is non-empty before merging" PASSES in state (b), at 4,821 bytes and 35 entries, and merges nothing. |
| Why it is recorded rather than omitted | So nobody re-derives it. A guard written against state (a) alone is green exactly when it should fire. |
| The only check covering both | Compare HEAD before and after. `rc=0` and the message are not facts about the world. |
| It generalises | To any command whose success message is read as a description of an effect, and to a mutation-plant that silently no-ops. |
| Two open limits | A stale properly-formatted `FETCH_HEAD` (real on-disk form `<sha>\t\t<desc>`) was NOT tested, so a genuine wrong-merge on some other path is untested rather than ruled out. |
| The second limit | "A failed fetch truncates `FETCH_HEAD` to empty" is observed, not proven, as the general cause of (a). |
| Recorded as FALSE | "One fetch anywhere poisons every worktree." `FETCH_HEAD` is per-worktree (`.git/worktrees/<name>/FETCH_HEAD`; `git-dir` differs from `git-common-dir`), so it does not propagate. |

### 6b. A green suite is evidence about the mutations it kills, and nothing else

| Item | Rule |
| --- | --- |
| The measurement | A 420-passed, 0-failed suite could not see four live fail-opens. Four independent verifiers then found at least five new fail-opens and two new false-deny classes, three proven end to end. |
| Mutation testing found why | Twelve single-mechanism mutants, each run through the entire suite: 9 killed, 3 survived a full green run, every survivor proven non-equivalent. |
| The worst survivor | A test whose own docstring names the class it cannot detect. It ends in a bare assertion and never inspects the text it is nominally about. |
| The procedure | Mutate the decision points and count survivors. |
| What an unkilled mutant means | A suite with unkilled mutants is not "mostly good". It is silent about exactly the region those mutants occupy. |
| The third category: INCAPABLE | A test whose bound cannot separate the bug from the fix is neither flaky nor correct. |
| How to find it | Run the mutation the test exists to catch and measure the gap. If the bound does not separate them, no amount of re-running will. |
| Measured 2026-08-22 | A concurrency test whose bound sat 0.13 seconds below the mutation it was written for. |
| The lander consequence, a PRIORITISATION rule | An incapable test that blocks merges has NEGATIVE value. It is pure tax. |
| So | It can be ordered ahead of a higher-scoring item that blocks more PRs, which is the reverse of how a difficulty score reads. |
| The fix direction is usually in the row | Assert the property the test is about, not the elapsed time it infers that property from. |

### 6e. A terminated process's exit code is indistinguishable from a verdict

| Item | Rule |
| --- | --- |
| The measurement | `git merge-tree ... \| Select-Object -First 2` returned exit 1, nearly reported as a merge CONFLICT. |
| What actually happened | There was no conflict. `Select-Object` closed the pipe and killed git before it could answer. The tool did not answer wrongly; it never answered. |
| The direction matters more than the mechanism | A truncated pipe manufactures a FAILURE. An empty pattern manufactures a SUCCESS. |
| Why the false failure deserves the louder warning | A false conflict is acted on immediately (rebasing, resetting, hand-resolving) while a false clean is merely believed. |
| The rule | Never truncate a pipeline whose exit code you intend to read. |

### 6f. A failed pattern expansion returns the most persuasive wrong number available

Measured on an LF-only file:

```
actual CR bytes  (tr -cd '\r' | wc -c) :    0     <- the truth
grep -c $'\r'                          : 1305     <- the probe
grep -c ''       (empty pattern)       : 1305     <- identical: the pattern expanded to NOTHING
grep -c 'zzz-cannot-occur-zzz'         :    0     <- grep is fine; only the PATTERN vanished
installed file, actual CR bytes        : 1305     <- and THIS is what 1305 would have "confirmed"
```

| Item | Rule |
| --- | --- |
| Why it is persuasive | It returned exactly the number that would have confirmed the false hypothesis, because `grep -c ''` yields the LINE COUNT. |
| The coincidence that makes it work | Any per-line quantity you are measuring also equals the line count. |
| What it nearly corroborated | A peer's independent false positive. Two instruments agreeing, looking like confirmation from different directions. |
| Defence 1 | Run the negative control. `grep -c '<string-that-cannot-occur>'` must return 0. If it returns the line count, your pattern is empty. |
| Defence 2 | Count BYTES, not lines. `tr -cd '\r' \| wc -c` cannot be fooled this way. |
| Say the discard out loud | The number was discarded because two sound instruments agreed with each other and disagreed with it. Ignoring a measurement is legitimate, but say so, or the discard looks like cherry-picking. |

## 14. Instruments that lie, in one list

Source of record for the general discipline: COMMON.md, *Measure it before you conclude* and *A green
light proves only what the gate asserts*. This section carries only what is specific to landing in
these repositories.

### 14e. Byte-parity questions need blob OIDs, not diffs

| Rule | Detail |
| --- | --- |
| `git hash-object` is config-dependent | Same file, same commit, different `core.autocrlf` gives different digests. A byte-exact parity instrument is only "strict" relative to one machine's config. |
| So | Compare **normalised content**, and never "fix" a parity test by re-installing the thing it guards. |
| For any mirror or parity question, compare blob OIDs | `git rev-parse <ref>:<path>` on each side. The OID hashes the **committed bytes**, so there is no working-tree normalisation layer to get wrong. |
| Measured cost of the alternative | A raw diff between two identical mirrored copies reported **3,794 differing lines**, every line in both files, because of the CRLF and LF fold. |
| And on Windows | A working-tree comparison shows a false difference from `autocrlf`. One command, no text layer, immune to both. |
| The installed-copy / source split | Hooks run from installed copies. Two were measured genuinely stale with **zero instruments watching them**, one of which **gates pushes**. |
| What that shape is | False green from the *absence* of a check. There is no red to dismiss. |
| Prefer a writer that refuses over a checker that reports | A fail-closed writer makes the new state unable to regress rather than merely correct on the day. Every "state a rule and hope" control is weaker. |

### 14f. PowerShell changes type and case underneath you

**A pipeline that matches once returns a scalar, and `[0]` then indexes a character.** Measured:

```
('alpha|beta'               | Where-Object {...})[0]  ->  'a'            <- a CHARACTER
('alpha|beta','alpha|gamma' | Where-Object {...})[0]  ->  'alpha|beta'   <- the line
```

The same expression changes TYPE with the match count, so code developed against two matches corrupts
silently on the day exactly one matches.

**This already destroyed content:** a row-removal script indexed `[0]`, got `"|"`, and replaced that
one character throughout the file, mangling unrelated lines. **Wrap in `@(...)` to force an array.**

It was caught only because the script echoed the size of what it was about to change, printing
*"removing the whole row (1 chars)"*. **Any mutation must assert the size of its own edit**, which is
the same rule as asserting a plant landed and asserting a ref moved.

| Rule | Detail |
| --- | --- |
| Variable names are case-insensitive | A local `$pr` and a `[int]$Pr` **parameter are the same variable**, so assigning an object to the local throws on coercion to the parameter's type. |
| Why it is invisible | It looks like two variables in every reading of the code. |

### 14i. Describing a range from memory steers a bisect away from the answer

Measured: `48f8712d..8077a033` was described as *"#325 (store/\*.py) and two ledger-only merges"*.

It was **19 non-ledger files and three feature commits**: MLLP rate pacing, a breaking TOTP cutover,
and a structured blocker record, across `api/app.py`, `auth/totp.py`, all four store backends,
`transports/mllp.py` and `uploads.py`.

A whole branch had been collapsed to the part of it under discussion all evening, then the **range**
described by that stale label instead of measured. **Nobody would look at an MLLP pacing feature while
believing the range was store plus ledger.** A wrong range does not merely under-inform a bisect, it
actively steers it. `git diff --name-only A B` and `git log --oneline A..B` cost one command each.

| Rule | Detail |
| --- | --- |
| A file list cannot settle "could this affect X" | The knob can sit in any file. Grep the added lines for the mechanism. |
| The decisive check for a suspected environment or recursion interaction | **908 added lines in range**, nonzero, proving the diff was read. |
| And the negative half | **Zero** matches for `setrecursionlimit`, `sys.setrecursion`, `threading.stack_size`, `stack_size` or `RecursionError`. |
| Plus the blob | The failing test's blob **byte-identical across the range** (`24807e73e152` both ends). That is a strong negative; "the file names look unrelated" is not. |
| A local run cannot attribute a CI failure | Different interpreter build, thread stack and image, so a local pass or fail is a fact about the local box. |
| Re-frame rather than discard | *"Is this trigger environment-sensitive at all"* IS answerable locally, and is often the premise the item actually needs. |

### 14k. Prose wraps, so an absence claim about prose needs a multiline instrument

Measured: a line-oriented search for `Never raises` in a docstring returned **False**. A multiline
`Never\s+raises` returned **True**, because the phrase spans a line break.

**A line-grep cannot distinguish "not present" from "present but wrapped", and reports the same thing
for both.** Absence is the dangerous direction: that false negative was used to "correct" a peer's
accurate citation, which would have recorded a correctly-reasoned lesson resting on a false premise.

| Rule | Detail |
| --- | --- |
| A correction is a claim, and so is a retraction | Check both as hard as the original. |
| What mutual checking caught in one session | A missing step in a shared script, a proposed fix wrong in both directions, a retracted-but-correct finding, a wrong routing decision, two ownership misattributions, a crashed probe read as a verdict, and this false absence claim. |
| The count | **Seven, across three sessions, and only one was found by the person who made it.** |
| Why the confirming challenge gets skipped | The one ending in "you were right" costs the same effort and produces no visible artifact. |

### 14r. A substring test standing in for a token test -- three instances in one session, across three authors

This is the single most productive defect shape observed, and it is invisible on every reading of the
code, because the pattern looks like what it means:

```
complete   matched inside  INCOMPLETE     <- a guard against CLOSURE claims fired on a sentence
                                             asserting the exact opposite. Reddened main.
arity      matched inside  granularity    <- one grep hit nearly produced "main already has this",
                                             which would have deleted a real control from the queue.
endswith(("-sha1","-md5"))                <- TERMINAL POSITION only, so gss-group1-sha1-<oid> and
                                             a vendor-suffixed dh-group1-sha1 name rate ABOVE the
                                             floor and connect. A cipher floor that admits what it
                                             screens.
```

A **fourth** arrived the same night, one level up: SPAN-vs-QUOTATION rather than substring-vs-token.

A lint refusing new hard-coded ASVS tallies fired on
`` `scanned 3 cells (1 pass / 0 partial / 0 fail / 0 na / 1 unverified)` `` -- inside backticks, a
quoted transcript whose entire point is that the numbers DISAGREE, sitting in the closing banner of
the item that FIXED broken tallies.

Its matcher deliberately tolerates markdown emphasis (``_EMPH = r"[\`*_\"']*"``, because *"24 `pass`,
15 `partial`"* is a real tally decorated with backticks) and therefore **cannot tell backticks that
DECORATE A WORD from backticks that ENCLOSE THE WHOLE CLAIM.** Emphasis and quotation are the same
character.

Two of the first three produce a confident **false negative about a security control**, the direction
that does not announce itself. The fourth produces a **false positive against correct evidence**, and
both tempting fixes are destructive.

| Rule | Detail |
| --- | --- |
| A backticked span is a mention, not a use | The same rule CLAUDE.md states when it permits quoting a glyph as a token. Strip whole inline code spans before scanning, then keep the emphasis tolerance for what remains. |
| When a matcher fires on a quotation, fix the matcher | Do not reword the quoted evidence, which deletes the falsification transcript that made a closure checkable. |
| Nor grandfather it | A may-only-shrink baseline permanently *asserts* the false positive is a real tolerated tally. |
| The instance fixes | Add `\b`, match a token, anchor to the whole field, or strip quoted spans. |
| **The durable defence: print what you matched, never just how many** | A count cannot be wrong in a visible way. `1` looks identical whether it matched `arity` or `granularity`. |
| The evidence | Every one of the three above was caught or missed exactly according to whether the instrument was made to show the matching line. |
| A PR body that disclaims a file sends the reviewer past exactly the file that needs review | A PR body read *"`scripts/asvs/scorecard.py` is untouched -- another stream owns it"* while that path sat in its own diff at `+209/-9`, holding the shared internals. |
| Why that one was load-bearing | A stale body is normally cosmetic. Here the sentence most likely to be trusted pointed away from the highest-risk hunk. |
| When correcting one | Keep the original text under a **"retained for the record"** line. The damage falls on the reviewer who already read it, and silently swapping the text leaves them believing something no longer on the page. |

### 14s. An empty scan is indistinguishable from a clean one

Measured live: a character scanner printed `cp1252-UNSAFE chars: 0  <- clean` while scanning **zero
lines**, because the `git diff` feeding it had failed upstream. The branch was local-only, not on
`origin`, and a loop over nothing flags nothing.

**The verdict line was exactly the one a genuinely clean branch produces.** The fix is to make the scan
state its own coverage AND prove it was sensitive: re-run printing `added lines scanned: 68` and
`non-ASCII seen: 10`. **The nonzero count of things it saw and chose not to flag is what proves it was
looking.**

A floor (`if scanned < N: fail`) turns this from a convention into a control. It bites hardest on
scanners looking for a rare thing, where zero findings is the expected result and therefore invisible.

### 14t. A crashed instrument must not exit the same code as a real failure

A PR watcher whose whole job is distinguishing red from green crashed and exited `1`, its own code for
*a required context failed*. **A bug in the instrument was indistinguishable from a red in the
subject.**

Give a watcher three outcomes, not two: `1` = the subject genuinely failed, `2` = unknown or timeout,
`3` = the watcher itself broke. Any tool that reports a verdict needs a distinct way to say *"I did not
reach one."*

### 14u. `jq` is not installed on this box, and a watcher that pipes to it fails in whichever direction its guard points

Measured 2026-08-12 across two PR watchers. `command -v jq` finds nothing, so every `... | jq -r .field`
yields an **empty string** and every `! jq -e ...` guard is **unconditionally true**.

The two failed in opposite directions from one cause. The first printed a state line with **every field
blank**, which reads as a PR state and is not one. The second reported **`WATCHER-BROKE` on every
poll**, which reads as a broken instrument and is right, but about itself rather than about anything it
was watching. **Neither ever observed the PR.**

| Rule | Detail |
| --- | --- |
| The tell that it is the shell, not the subject | A direct `gh pr view` at the same moment returns a well-formed answer. Settle an instrument disagreement that way before believing either side. |
| `gh` ships its own `--jq` and needs no binary | `gh pr view N --json a,b --jq '.a + "\|" + .b'` works where the pipe does not. |
| So | Prefer it in every watcher and parse with shell parameter expansion (`${s%%\|*}`) rather than adding a dependency. |
| The mixed case is the one that hides | In the first watcher the failure-detection line used `gh --jq` and caught a genuine `windows-2025` red, while the state lines beside it used the pipe and saw nothing. |
| What that looked like | One watcher, both halves apparently reporting, and only half of it connected to reality. |

### 14v. MSYS path conversion rewrites a `rev:path` argument, and the failure reads as a clean result

`git show origin/main:.github/workflows/ci.yml` can come back
`ambiguous argument 'origin\main;.github\workflows\ci.yml'` -- **both the slash and the colon
rewritten**, the `rev:path` parsed as a colon-separated PATH list.

It exits 128 on stderr, so **piping it into a counter prints 0**, which reads as *"nothing found"*
rather than *"nothing read"*.

**Set `MSYS_NO_PATHCONV=1` at the top of every shell**, not as a remedy after being bitten, or spell it
`origin/main:./<file>`.

A peer with this in their durable notes as a known shape still walked into it. On 2026-08-20 a lander
hit it again with this entry already in the file: the rewrite returned **0 for the target AND 0 for the
positive control**, and **the control is the only reason it was caught.** An entry you have read is not
a habit you have.

## 16j. LIVENESS is not CAPABILITY, and the purest blind gate exempts its own evidence

| Item | Rule |
| --- | --- |
| LIVENESS | Is something loaded and running? A floor like `MEFOR_MIN_DETECTORS`, asserting at least N detectors registered, answers this cheaply and is worth having. |
| The rule | **Never read a floor as a capability check.** Know which question a green is answering. |
| CAPABILITY | Does it trip on the class and NOT trip on the near-miss? Only paired arms answer it. |
| The example | `tests/test_scan_forbidden.py` carries **seven MUST-TRIP cases against five MUST-NOT-TRIP cases**. |
| The purest blind gate, by name | `test_scanner_no_longer_skips_its_own_token_bearing_tests`. |
| What it records | The secret scanner exempted its own test files, so **the files proving it worked were the files it could not see.** |
| Why the exemption was reasonable | Test fixtures carry deliberate token-shaped strings. Its effect was to put the gate's own evidence out of the gate's reach. |
| What a green there was | **Structurally incapable of being evidence**, and nothing about it looked wrong. Every other blind-instrument entry here approximates that shape. |
| A reading that agrees with the code is not a measurement | It is the same instrument twice. Reading the source predicted a counter would increment; running it is a *different* instrument. |
| Why that matters | Most compound failures are one instrument used twice and mistaken for corroboration. |
| A counter reading non-zero is not proof it discriminates | A single-arm probe cannot separate *"the tally counts the right thing"* from *"the tally counts everything it touches"*. Both print 1. |
| So | Any tally needs an arm that must NOT increment. |
| An eyeballed number is not a parsed number | A probe printed INCONCLUSIVE because it never captured stdout, while the correct answer sat on screen agreeing with it. |
| The tempting moment | Your probe saying INCONCLUSIVE while the screen agrees with you is the most tempting moment there is to overrule it. Re-run with a real capture instead. |
