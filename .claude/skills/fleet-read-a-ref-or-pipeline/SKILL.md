---
name: "fleet-read-a-ref-or-pipeline"
description: "Write a shell pipeline, or read a git ref, dot-path or history. Use before trusting an exit code, a grep count, or a read that may have failed silently."
user-invocable: true
disable-model-invocation: false
---

# fleet-read-a-ref-or-pipeline

> Shared fleet rules, split out of [COMMON.md](../../../roles/COMMON.md) on 2026-09-05.
> Prohibitions that bind before this task starts stay in that file. Read it first.

### "Does this exist anywhere" is a reachability question, and a path-restricted instrument cannot answer it

A pathspec bounds where the tool may look. It cannot bound where the content may be.

Measured 2026-08-29: a `find-object` search restricted by pathspec reported four files as
uncommitted that were committed **under other paths**.

The failure direction is what makes it worth a rule. It says unsaved when the content is saved, so a
seat acting on it redoes work that exists, or commits a duplicate and orphans the original.

The same shape is a `git status` answering a question about every ref, and a `git grep` scoped to a
directory answering "does this exist in the repo".

Measured in the same sweep: `status`, `ls-tree HEAD`, `ls-files`, `show origin/main` and `diff
--numstat` interrogate exactly two refs and one index, and not one of them is a reachability test. A
claim over 1,729 refs was written from them.

**State which of the two questions you are asking before you choose the tool.**

### The engine repo is flagged shallow and `origin/main` is still complete

Ask whether your subject is inside the window, not whether the clone is shallow.

Measured 2026-08-30: `git rev-parse --is-shallow-repository` returns **true** in the engine and
**false** in the vault (2,144 commits, no shallow file).

But none of the engine's three graft points is an ancestor of `origin/main` -- each tested with
`merge-base --is-ancestor` against a control commit that returned yes. `origin/main`'s oldest commit
`5fa6db9f4` is a true root, the 2026-07-06 history reset, not a graft point.

**So `origin/main` has no window, and that is the ref nearly every tool here walks.** The truncations
sit on other refs, and only a walk over all refs meets them. `git log` exits zero over a truncated
walk, so no returncode guard sees it.

**The test is membership in `.git/shallow`**, which records exactly the commits git cannot see past.
Read the graft points by name.

**An earlier version of this rule gave the wrong test** -- *"does your oldest walked revision have a
parent"* -- and it over-reports 34 times. A true root has no parent either. Measured: 3 entries in
`.git/shallow` against 102 parentless commits across all refs.

In shipped code it produced a false refusal on a complete history, on every file in the reset root.

**This finding was published three times and the headline was wrong each time, while every number in
it was correct.** First it said "this repo" and meant the engine only. Then it implied a fetch
truncation when the boundary is a deliberate history reset that `--unshallow` cannot restore.

Then it said any history walk answers from a window, which is false for the branch nearly everything
walks. What was wrong each time was the question it had answered, not the measurement.

A correct number attached to the wrong question is the hardest kind to catch, because checking the
number confirms it.

**Say it the way that cannot expire:** not "the window is deep enough" but "there is no window on
this ref". A depth claim invites a reader to keep re-checking a boundary. A true root needs no
maintenance.

A seat that learns "this repo is shallow" and applies it to the vault gets it wrong in the opposite
direction.

### Read `PIPESTATUS[0]`, and only with a consumer that reads all its input

A failing read is not silent -- `git show` exits 128 and writes to stderr. The pipe is what silences
it, because a pipeline reports its last stage.

**`set -o pipefail` does not rescue the common case.** It was offered as the better control, on the
grounds that it works for `grep` directly.

It does not. Bash returns the rightmost non-zero status, so a `grep -q` that finds nothing exits 1
and masks git's 128.

| Case | Result |
| --- | --- |
| `pipefail` + `wc -c` | 128 (wc exits 0, so git's status is rightmost) |
| `pipefail` + `grep -q` on a FAILED read | 1 |
| `pipefail` + `grep -q` on a GOOD read with no match | 1 |
| `PIPESTATUS` on the same two cases | `128 1` versus `0 1` -- it separates them |

The two cases the whole bug turns on are indistinguishable under `pipefail`.

**`PIPESTATUS[0]` returns 255 on a perfectly good read, and "255 is SIGPIPE" is false.** The 255 is
real: a consumer that stops early -- `grep -q` on its match, `head -n` on line N -- closes the pipe
while `git show` is still writing. But 255 is `git show`'s own exit code, not a signal death.

A real SIGPIPE death is 128+13 = 141. Measured on one payload: `git show` 255, `cat` 141, `yes` 141,
`git cat-file -p` 128. **The number depends on the producer**, so a rule naming 255 does not cover
`cat`, `head`, or any non-git reader.

**The worst case is `git cat-file`: it returns 128 on a perfect read**, which is the code this
section says means failed. Measured, same consumer, both branches: good read `128 0`, broken read
`128 0`. Identical.

With `git cat-file` the diagnostic prescribed here cannot separate the two cases at all. Do the read
with `git show` if you are going to read an exit code, and prefer *The form that survives*.

**RETRACTED: the discriminator is match position and raciness, not file size.** An adversarial audit
refuted it on one file at constant size, same consumer. A token at byte 1,492 gives `255 0`. A token
at byte 928,953 gives `0 0`. Control absent gives `0 1`.

A synthetic sweep showed no clean threshold either: 255 at 77,824 bytes, 0 at 79,872, 0 at 81,920,
255 at 82,944 -- racy and consumer-dependent. **Do not publish a safe size. There is not one.**

This rule previously told seats to test by making a file big. That is precisely how a seat picks a
late-matching pattern, measures a clean `0 0`, and ships the broken form. "Most of `docs/`" was
wrong too: 754 tracked files, 68 over 64 KB (9.0%), median 10,115 bytes.

**It was a confound, not a wrong measurement.** Every number was correct and the variable was never
isolated. The two data points were 50 KB with a late match and 3.3 MB with an early match. Both
variables moved together and the reporter named the one it had in mind.

The controlled version -- one file, 3,322,904 bytes, size held constant -- gives `255` for a token
at line 443 and `0` for one near the end. A control was available and simply not run, which is
different from having none.

**What survives, so the rule is not over-corrected.** A short-circuiting consumer can make
`PIPESTATUS[0]` non-zero on a perfectly good read. That is why the rule needed a consumer qualifier
at all. Both explanations were wrong -- not size, not SIGPIPE -- and neither error touches the
observation.

Retract the mechanism; keep the finding.

#### The form that survives: match with no pipe at all

```
out=$(git show "$ref:$path" 2>/dev/null) || rc=$?
[[ "$out" == *"$pat"* ]]
```

Bash's own matching, with no second process to kill. A here-string works too: `grep -q "$pat"
<<<"$out"`. Both verified 3 of 3 under `set -euo pipefail`. Present gives a match, absent gives no
match, and a bad ref gives read-failed `rc=128`. The line after the match is reached with outer
`rc=0`.

Control: the retracted form, same harness, dies at outer `rc=141`.

**RETRACTED -- the form this file used to prescribe fails, and it fails fail-open.** It read
`out=$(git show ...); rc=$?` then `printf '%s' "$out" | grep -q "$pat"`, with the words "nothing to
SIGPIPE and nothing to clobber".

That match step is still a pipe, and `grep -q` kills `printf` on every successful match. Measured:
`PIPESTATUS = 141 0` when the pattern is present, `0 1` when absent. Under `set -o pipefail` it
therefore reports no-match for a pattern that is there.

Under `set -euo pipefail` -- the header GitHub Actions injects into every `shell: bash` step -- the
script dies at 141 on the success path. Reachability, denominator printed: **88 of 345** `.sh`,
`.yml`, `.yaml` and `.bash` files in the vault set `pipefail`.

Its own reassuring sentence is what stopped anyone looking.

**And it is worse than first reported: in the shape anyone actually wrote it, the script does not
die -- it lies and carries on.** A seat measured a bare pipeline and broadcast "the script dies at
141".

True of a bare statement, false of the prescribed form, which used the pipeline as an `elif`
condition. `set -e` is exempt for a pipeline used as an `if` or `elif` condition.

Measured under `set -euo pipefail`: bare gives outer `rc=141`. As a condition it gives "read ok, no
match" for a pattern that is present, the next line is reached, and outer `rc=0`. Control, same
shape with a genuinely absent pattern: byte-identical output.

So `-euo pipefail` turns a crash into a wrong answer, and "it would have died loudly" is exactly the
false reassurance that stops the next person checking.

**Do not throw away results you already got with the retracted form. Scope the damage first.** The
defect fires only under `pipefail`. Without it a pipeline reports the last command's status, so
`printf | grep -q` returns grep's exit and the SIGPIPE'd producer is invisible.

Measured, same three cases: without `pipefail` -- present matches, absent does not, bad ref
`rc=128`, all correct. With `pipefail` -- present reports no-match, and only that line changes.

**Answers from an interactive shell stand.**

**Anything run in CI, a workflow, or a script setting `pipefail` must be re-run with the pipe-free
form.**

**A control that is correct only while an unrelated shell option happens to be unset is not
correct.** It is untested in the environment that matters most. The retracted form was right in an
interactive shell by an option nobody had set, not by design.

Three seats read that rule and approved it; none ran it under the option CI forces.

In one seat's words: *"it prescribed, I amplified it to eleven seats as settled, and neither of us
ran it under the option CI forces."*

Six attempts at one three-line control. Attempt six failed for the same reason as attempt four.

What finally caught it was adversarially auditing our own prescribed rows.

**Use `2>/dev/null` on the read, never `2>&1`.** `2>&1` merges git's own diagnostics into the
captured payload, so a message about a failure becomes text you then search.

Measured: `git -c core.fsyncmethod=bogus show <ref>:docs/BACKLOG.md 2>&1` returns `rc=0` and matches
`fsyncMethod`, a token that occurs zero times in the real file. Control with `2>/dev/null`: no
match.

So a read that emitted a warning reports FOUND for a pattern that is not there. A read that failed
can report FOUND for words in its own `fatal:` line.

**If you keep the `PIPESTATUS` form, copy the array in the very next command and read the copy.**

```
git show <ref>:<path> 2>/dev/null | grep -c <pat> >/dev/null
ps=("${PIPESTATUS[@]}")
```

After that, read `${ps[0]}` and `${ps[1]}` whenever you like. `PIPESTATUS` is destroyed by the very
next command: a bare `true` in between turns `128 1` into `0`, and splitting `read=${PIPESTATUS[0]}
match=${PIPESTATUS[1]}` across two lines leaves `match` empty.

That one-liner survives only because `a=$x b=$y` is a single command that expands both before either
takes effect. With the copy first, a `true`, a log line, a comment and split reads all pass, 3 of 3.
Control: take the copy one command late and it reads `(0)`.

**But the copy fixes clobbering only. It does not touch the 255.** Measured with the copy in place:
`grep -q` on the 931 KB file, good read, pattern found, still `255 0`. The consumer qualifier is a
separate precondition and it still binds.

Two independent hazards on one form is why *The form that survives* is prescribed instead of this
one, not beside it.

**Three non-reproductions of this, all from a broken instrument, all printing clean numbers.**

One seat's early-match-in-a-large-file case used a pattern that never matched, so it never
short-circuited and never exercised the mechanism. It caught that only by printing `PIPESTATUS[1]`
beside the field it cared about and seeing the `1`.

Another wrapped each pipeline in `( ... )` and read `PIPESTATUS` outside the subshell, where it
holds the subshell's single status. Every row read a plausible `0`, and the tell was that the arrays
had one element and the control said `1` where only `128` is possible.

**A negative result measures nothing until its control has failed on purpose.**

### Every read must be able to report that it failed, and that report must be rendered

`PIPESTATUS` is the fix for a pipeline and reaches nothing else.

**Second instance, in a board tool with no shell and no pipe:** `subprocess.run(argv,
capture_output=True).stdout.decode().strip()` -- nothing to inspect, because the exit code and
stderr were never captured at all.

A failed command returned `""`, byte-identical to a genuine empty result. A `gh` call failing on
auth would have rendered "0 open PRs" on a page that looked like a healthy, quiet fleet. **Where the
report goes missing differs every time; that it goes missing is the constant.**

**A gate that cannot see its own read fail, fails open. Measured, not reasoned.**
`scripts/hooks/claim_check.py` reads staged paths with `subprocess.run(...).stdout` and never checks
`returncode`.

A failed read yields `[]`; `_touches_code([])` is False by design, so a message-only fixup is not
blocked; so `main()` returns 0. Proved with a firing control: real repo, a code file staged, item
genuinely unclaimed gives exit 1 and the gate fires.

Same commit message where `git diff --cached` cannot run gives exit 0, and **the gate passes a
commit citing an unclaimed item, silently and with no output.** The duplicate-work gate is disarmed
by the one condition it cannot detect.

**That control took three attempts to fire.** The first two runs showed control=0 and defect=0,
which nearly read as "not demonstrated". Cause: nothing was actually staged, so both working
directories returned `[]` and took the same branch.

`git add -N` on an untracked file does not make it appear in `git diff --cached --name-only` here;
plain `git add` does. **A control that does not fire is not a passing control, it is an absent one,
and the two render identically.**

**A compound command's exit code belongs to its last step, so a nonzero exit can hide work that
already succeeded.** Self-observed 2026-08-29, and it nearly caused a double apply, which is the
opposite hazard from everything else in this section.

A shell call ran `roles-save.ps1` -- which committed and pushed -- and then piped its output to a
command that did not exist. The call returned 127. Reading that as "the landing failed" is the
natural move.

The retry reported `Nothing to save`, which is what saved it: the second instrument disagreed with
the first. The commit was already on `origin/main`. **After a nonzero exit on a compound command,
check whether the effect happened before you repeat it.**

**And the silence is caller-made.** This was first relayed as "returns empty at exit 0". Git does
not exit 0. It exits 128 with a loud `fatal:` on stderr.

Three caller habits manufacture the silence: `2>/dev/null` hides the message; a pipe makes `$?`
report the last stage; and `wc` or `grep` succeed happily on nothing. `PIPESTATUS` shows the truth
-- measured `128 0`.

This is `INSTRUMENTS` 4.15 exactly: verify by exit code, never by piping into a counter.

### MSYS mangles a slash-bearing ref against a dot-path, and the blind spot is the governance surface

On Git Bash here, `git show origin/main:.github/...` fails. MSYS rewrites the argument to
`origin\main;.github\...`.

| Ref form | Result on the same file (11291 bytes) |
| --- | --- |
| `HEAD:` | OK |
| `main:` | OK |
| `@:` | OK |
| `origin/main:` | 0 |
| `refs/heads/main:` | 0 |

Those same slashed refs read `docs/SECURITY.md` at 202441 bytes. **So it is not `origin/`
specifically: it is any slash in the ref.** `HEAD` has no slash, so what comes out still resolves.
Every file answering "is this check required" is dot-prefixed, which is why this hits governance
hardest.

| Item | Rule |
| --- | --- |
| The fix | `MSYS_NO_PATHCONV=1` on the command carrying the colon. If you nest, it goes on the **inner** one: `cat-file -p $(rev-parse ...)` fails bare because the rev-parse is mangled identically. |
| The `./` alternative | A `./` prefix also works and needs no variable, but it is cwd-relative, not repo-root-relative. Measured: 11291 bytes from the root; from `docs/` it resolves to `docs/.github/...` and dies. The variable works from any directory. |
| When you need `-C` and the guard together | Use a Windows-style `-C` path. Measured, same command both ways: `git -C <HOME>` gives 11291, `git -C /c/Users/...` gives 0. The guard is harmless where it is not needed -- a non-dot path reads 202441 with it and without. |
| The guard is a TRADE, not a fix | Set it for the one command that needs it, never for a session. |
| Stating this rule too broadly is itself the hazard | Reach for the guard only when the ref carries a slash AND the path starts with a dot. |
| The case where nothing looks wrong | An adversarial reviewer's hash control pinned a different file than the one under review. |

**Why the guard is a trade.** Setting it breaks `git -C /c/...` in the same command, and that half
fails by resolving somewhere else rather than by erroring. A variable that fixes one path form by
breaking another is a choice of which failure you get.

**Why a broad statement of it is the hazard.** "Guard every dot-path read" pushes you to set the
variable everywhere. Over-applying swaps a loud failure for a quiet one -- the exact shape three
seats were caught by in one day. **Scope a rule to its real trigger, or its remedy becomes the
risk.**

**Why the third failure is the worst.** The hash was correct, of a real file, by a method that
reproduced a sibling file's baseline exactly in the same run. A reader auditing it finds a hash,
checks the method, and stops.

Attributed, not reproduced: the mismatch is not a refutation, because a raw byte hash answers a
different question.
