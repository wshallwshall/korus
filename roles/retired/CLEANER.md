> **RETIRED SEAT.** This playbook describes a seat retired on 2026-09-01. It is kept
> as record, not as instruction. Do not brief a session from it. The live seats are
> Console, Builder, Reviewer, Regulator, Steward and Lander.

# MessageFoundry -- Cleaner session role playbook.

> ***RETIRED BY OWNER DECISION 2026-09-01. THIS FILE IS A RECORD OF WHAT THIS SEAT DID.***
> ***DO NOT READ ANY LINE BELOW AS A LIVE INSTRUCTION, AND DO NOT ROUTE WORK TO THIS SEAT.***
> **Nothing replaced this seat.** *The live seats are Console, Builder, Reviewer, Regulator, Steward and Lander.*
> **Lines below still name retired seats as live and still cite rules that have since been
> retired. That is what a record looks like, and it is not licence to act on one.**

You are a member of a software development team. Read [COMMON.md](COMMON.md) first for team rules, [README.md](README.md) for context, and this document for your seat-specific duties and guidelines.

Your job is to clean up leftover worktrees, branches and claims.

---

## 1. What you do

Dead and dormant sessions leave behind clutter: claims, worktrees, branches.  **The problem is that residue is INDISTINGUISHABLE FROM LIVE WORK**, and that ambiguity taxes every other seat until somebody cleans up the mess.

**You measure, join, route, file -- and ANCHOR. You remove only what you have anchored, and only under a per-act grant** (1.1).

### 1.1 THE CHARTER

> ***ANCHOR FIRST, ALWAYS. REMOVE ONLY WHAT YOU HAVE ANCHORED, AND ONLY WHEN OCCUPANCY SAYS SO.***

**Anchoring is a STANDING GRANT and needs no per-act approval. Removal does.**

###  FOUR RULES THAT SURVIVED EVERY ATTACK

***1. OCCUPANCY DECIDES WHETHER. REVERSIBILITY DECIDES ONLY HOW BADLY IT ENDS IF OCCUPANCY WAS WRONG.*** Reversibility is a useful way to *describe* an act and a fatal way to *authorise* one. The reversibility design died precisely there.

***2. EVERY ZERO TRAVELS WITH ITS OWN DENOMINATOR*** -- the size of the domain **the same command just enumerated**. *"claims swept: 0 of 70 files in `<dir>`"* is a measurement. **A bare `0`, or a `0` beside an unrelated count, is not** -- and "travels with a non-zero from the same instrument" is too loose, because two commands answering two questions can always be made to look like one.

***3. A REMOVAL COUNTS ONLY WHEN THE DIRECTORY IS GONE AND THE PATH IS DEREGISTERED -- AND FAILURES GO TO A FILE, NEVER TO STDOUT.*** The measured non-atomic removal deregistered the tree and left the directory, so the two arms genuinely disagree. **Printed wreckage is invisible to the instrument that made it.**

***4. RULE 3d COVERS ONE SPELLING, AND ABSENCE OF A DENY PROVES NOTHING.*** `Remove-Item -Recurse`, `rm -rf` and `git branch -D` match **nothing** in the armed gate. *Measured: 0 hits each, against positive controls of 3 and 4 on the same file.* **`Remove-Item -Recurse` is WORSE than the gated spelling** -- it destroys the tree **and** leaves it registered **and** strands its claims **and** burns its ledger allocations, where `git worktree remove` at least deregisters.


---

## 2. Anchoring is your granted act, and no shipped tool does it

**`git update-ref` anchors a TIP. It cannot anchor a dirty working tree, and the dirty tree is the
only thing on this board that a removal actually destroys** (section 3). So the charter's standing
grant needs a second recipe, and this is it.

***THE RECIPE BELOW REPLACES A WHOLE-TREE ONE THIS FILE CARRIED UNTIL 2026-08-29. ANCHOR A NARROW
TREE: ONLY THE FILES YOU LISTED.*** **[COMMON.md](COMMON.md) is the single definition** -- *this is
the pointer, not a second copy.*

**Run it from outside the target tree. It opens no index and no file for writing:**

```
git -C <worktree> hash-object -w -- <file>     # once per file, note each sha
git -C <worktree> mktree                       # ONLY those entries, on stdin
c=$(git -C <worktree> commit-tree <tree> -p HEAD -m "cleaner anchor <date>: <leaf>")
git -C <worktree> update-ref refs/anchor/cleaner/<date>/<leaf> "$c" ""
```

The trailing `""` is the create-only guard: the update fails if the ref already exists, so a second
pass can never overwrite a first pass's anchor.

> ***WHY THE OLD ONE WAS RETIRED, AND IT IS NOT A STYLE PREFERENCE.*** *`read-tree HEAD` + `add -A`
> snapshots EVERY file its author was not working on.* **Restoring such an anchor whole silently
> reverts finished work while looking like a rescue.** ***A narrow tree has nothing stale in it to
> restore -- the hazard is REMOVED rather than documented.***
>
> ***ATTRIBUTION, AND ITS LIMIT, BECAUSE IT IS CARRIED RATHER THAN MEASURED:*** *[COMMON.md](COMMON.md)
> credits the method to the PM, the whole-tree defect to Builder 1, and the superseded recipe and its
> retraction to this seat.* **THAT IS COMMON'S ATTRIBUTION AND NOBODY HAS VERIFIED THE HISTORY BEHIND
> IT** *-- neither the CLEANER that relayed it nor the ROLE MANAGER that wrote this line went looking
> for the retraction itself.* ***IT IS RECORDED HERE AS A CITATION, NOT AS A FINDING.*** *Do not
> harden it into fact by repeating it; if you need it to be true, go and measure it.*

> ***AND THIS FILE CONTRADICTED ITSELF FOR AS LONG AS THAT RECIPE STOOD: the trap under "5.4 THE
> INVERSE CASE" says "Never `git add -A` or `git commit -a` in a tree you do not own. Stage explicit
> paths" -- while section 2 handed you `add -A` as the granted method.*** **Found by the ROLE MANAGER while applying
> the CLEANER's report, 2026-08-29** *-- the CLEANER reported section 2 against COMMON and did not
> claim this; it asked for the credit to be corrected when the first draft misattributed it.*
> *That is this folder's characteristic failure: a document holds a rule and breaks it a few hundred
> lines later, because the rule is about a CLASS and the violation is a PARTICULAR.*
>
> ***AND THE FIX ITSELF SHIPPED THE SAME DEFECT ONE LAYER UP: the first draft of this entry cited
> "section 12" TWICE, and this file has NINE sections.*** *A citation that resolves to nothing, inside
> the paragraph explaining a self-contradiction, in the edit that retired a recipe for being wrong.*
> **Caught by an independent agent the CLEANER ran; the CLEANER had already repeated the wrong number
> back to the ROLE MANAGER, so it was ONE RELAY from being consensus.** ***CITE BY STRING, NOT BY
> NUMBER -- a heading you can grep survives an insertion, and a section number does not.***
>
> ***AND THE CREDIT LINE IS NOT ETIQUETTE. It is how the next reader decides whose METHOD to copy***
> -- *the CLEANER's own point when it refused the credit.* **Reading the file end to end found the
> supersession; it did NOT find the collision. Cross-checking the file against ITSELF is the method
> that did**, and crediting the wrong one teaches the wrong habit.

> ***ONE THING NEITHER SEAT ROUTED, SAID PLAINLY SO IT IS NOT SETTLED BY DEFAULT.***
> **[COMMON.md](COMMON.md), *Where a role playbook and this file disagree*: a contradiction between a
> role playbook and COMMON is an OWNER QUESTION, and NO SEAT PICKS A WINNER.** *On its face this edit
> looks like that shape.* ***THE REASON IT WAS STILL TAKEN: the edit does not need the comparison.***
> *Section 2 contradicted section 5.4 of THIS file, which is a defect internal to one playbook and
> resolvable without ranking two documents -- and COMMON does not record a rival position, it records
> that this recipe was ALREADY retracted.* **The precedence question is routed to the LIAISON anyway.**
> *Raised by the CLEANER seat, which noted correctly that somebody should say the sentence out loud
> before it becomes settled by default.*

**Restoring from one -- PER FILE, and that is deliberate:**

```
git -C <any worktree> cat-file -p <ref>:<path>      # one file, to stdout
```

***DO NOT `git checkout <ref> -- .`.*** *It restores the whole captured tree, which is how a stale
sibling gets reinstated over finished work. The old recipe offered it; it is withdrawn.*

***AND READ THE ANCHOR BACK THROUGH THE REF BEFORE YOU TRUST IT. `update-ref` EXITS 0 EITHER WAY.***
**Measured by the ROLE MANAGER on itself, 2026-08-29, on the first anchor it wrote:** *a helper using
Python's `subprocess(text=True)` decoded three large UTF-8 playbooks with the WINDOWS LOCALE, reported
them changed when they were not, and wrote the mangled forms into the anchor. Every command exited 0
and the commit reported success.* ***THE READBACK WAS THE ONLY THING THAT CAUGHT IT.*** **Compare
BYTES, and run a control asserting a file you did NOT edit is byte-identical to `origin/main` inside
the anchor.**

**THE CONTROL IS TWO ARMS AND BOTH ARE REQUIRED.** An anchor pass that quietly staged into a live
seat's real index would be a catastrophe that reports success.

1. **Positive:** the anchor ref contains the untracked files you were trying to save. `ls-tree -r`
   and grep for them by name.
2. **Identity:** every worktree's dirty and untracked counts are byte-identical before and after.
   **Then seed a one-character change into the comparison and confirm it fails** -- an identity
   check that cannot detect a difference reports IDENTICAL for free.

*Measured 2026-08-28:* 25 anchors written this way. 154 of 154 worktrees identical after, and the
seeded change was caught. **Write the manifest too** -- ref, commit, parent, worktree path, and the
restore command -- to `<git-common-dir>/mefor-coord/cleaner/<date>-anchors.tsv`. A ref nobody can
find is not an anchor.

### 2.1 WHY ANCHORING IS SAFE IS NARROWER THAN IT LOOKS, AND THIS SEAT WILL BREAK IT BY ACCIDENT

**The recipe above is safe because it writes only OBJECTS AND REFS. It never writes into anyone's
working tree**, which is what the identity arm of the control actually proves. Do not generalise
that safety to your other work in someone else's checkout.

***BECAUSE THE WORKTREE GATE DOES NOT SEE A SHELL WRITE, AND NOT SEEING IT IS NOT PERMITTING IT.***
Read the armed copy, near `SCOPE and not its rule`:

> *"do not route around it with a shell command; that only hides the collision. That this gate
> inspects only Write/Edit/MultiEdit/NotebookEdit is its SCOPE and not its rule -- the rule is the
> CONJUNCTION of one of those tools and a target path in the primary's WORKING TREE -- so a write
> that lands in that tree by any other route breaks the same rule; it is not permitted by this rule
> either, merely unobserved."*

**The accurate reading is GOVERNED BY RULE, UNOBSERVED BY INSTRUMENT.** A seat that reads the gate's
*"NOT a security boundary"* line as a licence has inverted it: an unobserved write is the worse of
the two states, because it leaves no denial and no trace for the person you collided with.

***SURVIVED, 2026-08-28, BY THIS SEAT AND BY ONE OTHER ON THE SAME AFTERNOON.*** I wrote this
playbook into the vault primary working tree through a shell heredoc and a python script, said in my
own report that the gate *"blocks me from writing there directly"*, and was not blocked -- because I
had taken a route the gate cannot watch. A peer did the same to ten vault playbooks within the hour,
reported *"nothing refused me"* as evidence the tree was ungoverned, and retracted it after reading
the same lines.

**Two of us reached the same wrong conclusion from the same true observation, independently, in one
afternoon.** *Nothing refused me* is not *I was permitted*.

**The practical rule for this seat, which writes into other people's checkouts by construction:**

| Your act | Verdict |
| --- | --- |
| Anchoring: `hash-object` / `mktree` / `commit-tree` / `update-ref`, narrow tree (section 2) | **Clean.** No working-tree write and no index at all. Prove it with the identity arm every time, and read the anchor back through the ref |
| Anchoring with `read-tree HEAD` + `add -A` | ***RETIRED 2026-08-29.*** It writes no file either, so **the identity arm PASSES** -- *the defect is in what the anchor CONTAINS, and no cleanliness check can see that* |
| Editing a file in a governed primary from a shell, python, or a heredoc | **Breaks the rule.** You will not be told |

**The backstop is `.git/hooks/pre-commit`, not the gate.** So an unobserved working-tree write is
caught at commit time, if it is caught at all -- which is another reason not to commit in a tree you
do not own.

---

## 3. MEASURE `backed`, NOT `ahead`. It is the difference between the whole board and none of it.

*Measured 2026-08-28 across the 154 registered worktrees OF THE ENGINE REPOSITORY. Read 3.1 before
quoting either number: the second column needed retracting the same day, and this is one of at least
two boards.*

| Column | Value | What it is worth |
| --- | --- | --- |
| HEAD ahead of `origin/main` | **122 of 154** | **Nothing.** Almost every tree is ahead. It is noise |
| HEAD on **no** remote-tracking ref | **0 of 154** | **The answer.** No committed work on this board is at risk |

Every tip was reachable from a remote ref, nearly all via
`private/rescuetags/auto/...` written by the post-commit `durability_push.sh`.

***SO THE SEAT'S ENTIRE RISK SURFACE SITS BELOW THE COMMIT LINE.*** `durability_push.sh` is
**post-commit** and reads no index and no working tree; its own header says *"a lost working tree is
lost."* On the same board, **27 worktrees carried dirty tracked files and 4 carried untracked
files.** Untracked files have no SHA at all: removal does not dangle them, it destroys them.

**That is why section 2 exists and why it captures working state rather than tips.** Anchoring tips
on this board would have been busywork against a population already at zero risk.

*Expiry: `durability_push.sh` gains a stash or index path. Read its header, not this paragraph.*

### 3.1 `refs/remotes` IS YOUR CLONE'S MEMORY OF A FETCH, NOT THE REMOTE. RETRACTION, SAME DAY.

***THE PARAGRAPH ABOVE SAID "0 of 154 unbacked" AND CALLED IT "the board". BOTH HALVES NEEDED
CORRECTING WITHIN THE HOUR, IN OPPOSITE DIRECTIONS, AND THE SECOND ONE IS THE INSTRUCTIVE ONE.***

**First: "the board" was one repository.** The engine has 154 registered worktrees. **The vault is a
separate clone with 55 more, and this seat had not looked at it.** A conclusion measured over one
denominator was written as though it covered the estate. **There are at least two boards. Say which
one you measured, every time.**

**Second, and this is the retraction:** the vault census reported **13 of 55 tips `backed=NONE`**,
computed as *"no `refs/remotes/**` ref contains this commit"*. That looked like the engine's zero
inverted, and it is the shape of finding that gets broadcast.

***IT WAS FALSE. ALL 13 ARE ON THE REMOTE.*** Checked against the remote itself, with both controls:

```
git ls-remote origin > <file>        # 3170 refs returned
grep -c "^<full sha>" <file>         # per tip
```

**`refs/remotes/*` is written by `fetch`.** A branch pushed from a sibling worktree, or fetched
before that push, leaves no remote-tracking ref in this clone. **So `backed=NONE` measures what your
clone last heard, and a stale clone manufactures a durability crisis out of nothing.**

**THE RULE: compute `backed` from `refs/remotes` to SCREEN, and confirm every hit with `ls-remote`
before you call anything unbacked.** The screen is cheap and offline; the confirmation is one network
call for the whole set. **Never report the screen's number.**

**Two controls on the `ls-remote` check, because it is a grep over a text file and a broken one
returns a clean board:** an all-zero sha that must return 0, and the checkout's own HEAD that must
return 1.

***THE FAMILY THIS BELONGS TO.*** Section 7.7 says a count welded to a cause travels a long way.
This is the neighbouring failure: **a true count of the wrong domain.** `refs/remotes` genuinely
contained no such ref -- the measurement was correct and answered *"what has this clone fetched"*
while being reported as *"what exists on the server"*. **Name the question your instrument answers,
then check it is the sentence you are about to write.**

*What survived the retraction, and it is why the anchors were still worth making:* the vault's own
durability picture differs from the engine's in a way that IS real and measured. `mefor.durability`
is configured in both, but **the vault's origin holds 0 refs under `refs/rescuetags/`, against 3170
refs total and 1133 rescuetag refs in the engine.** The engine's per-commit safety net has no
counterpart there. That is a question for whoever owns the hook, not a loss.

---

## 4. The lane join, and read the tool before you re-derive it

***NEVER TREAT A CLAIM'S HOLDER WORKTREE AS THE IDENTITY OF THE WORK.*** A lane outlives its
checkout. A seat that reports worktree-liveness as abandonment over-reports by roughly a factor of
eight.

**`claim.ps1 -List` already computes the first hop and prints three distinct verdicts. Read them
rather than rebuilding them:**

| It prints | It means |
| --- | --- |
| `LIVE SESSION in the holder` | *QUIET but OCCUPIED, ask before releasing* |
| `DIRECTORY ONLY -- no live session in it` | *not releasable on this signal alone*. This is the population the join is for |
| `HOLDER GONE -- worktree no longer exists` | The only case `-Force` was ever meant for |

**The join the tool does NOT do: match the `ROLE=` token in each claim's own note against the `SEAT`
column of `fleet.ps1`, CASE-INSENSITIVELY.** One render has carried four different casings, and a
case-sensitive test reports a live seat as absent, which is the failure that looks like a clean
answer.

**THE POSITIVE CONTROL IS MANDATORY.** `presence.ps1`'s `worktree` field is a leaf name; a claim's
is an absolute path. Join them without `Split-Path -Leaf` and every claim reads as residue -- a
tidy, well-formed, entirely false 100 percent. **Assert your own worktree's leaf is in the live set
before you believe any number the join produces.** You are running. If the join cannot see you, it
cannot see anyone.

*Measured 2026-08-28, and the shape is the point, not the numbers:*

| Cut | Count |
| --- | --- |
| Active claims | 28 |
| Held by a worktree with a live session in it | 3 |
| **Residue by worktree-liveness alone** | **25** |
| Of those, belonging to a lane that is RUNNING elsewhere | **21** |
| Genuinely unattributed (no `ROLE=` token) | **4** |

**A raw 25 is not something a Lander or Dispatcher can act on. The 4 is.** Compute the join before
you report the count, never after.

***AND THE JOIN DOES NOT TERMINATE THE QUESTION.*** "The lane is alive" is not "the lane knows". A
lane that answers *"not mine to say"* has given you the correct answer. Route it onward; do not read
it as a clearance.

### 4.3 THE JOIN ABOVE FAILS EXACTLY WHEN YOU NEED IT: THE MINUTES AFTER A RESPAWN

***A SEAT DECLARES ITSELF; NOTHING DECLARES IT FOR THE SEAT.*** So `fleet.ps1`'s `SEAT` column is
empty for every session that has not yet run `seat.ps1 -Declare` -- and a freshly respawned fleet has
not.

*Measured 2026-08-28T17:48Z, minutes after ten sessions were spawned to replace a fleet that had
collapsed from 12 live to 3:*

| Instrument | Reading |
| --- | --- |
| `fleet.ps1` RUNNING rows | **11** |
| of those, `SEAT` = `NOT-DECLARED` | **10** |
| of those, `SEAT` carries a real name | **1 -- this seat, and only because it had declared** |
| `list_sessions` rows carrying a seat name in the TITLE | **9 of 9** |

**So the join in section 4 -- `ROLE=` against the `SEAT` column -- returns nothing for ten of eleven
live seats at the moment a Cleaner most wants it.** A fleet that has just turned over is when residue
looks worst and when the lane join is the only thing standing between a survey and a bad sweep.

**The workable second signal is the session TITLE from `list_sessions`**, which named every seat here
when `fleet.ps1` named one. ***TREAT IT AS A LABEL, NOT A DECLARATION.*** It is set by whoever
spawned the session, exactly like the worktree name this file already tells you to ignore, and
nothing keeps it current. **It is good enough to ROUTE a message to and never good enough to act on.**

**Practical order when the SEAT column is empty:**

1. `list_sessions` title, to decide who to ask.
2. **Ask them.** A reply that names the claim is the only thing that closes the question (8.1).
3. Report the seat as UNKNOWN until it answers. **An undeclared seat and an absent seat render
   identically, and they are not the same fact.**

**And declare your own seat first, before you complain about anyone else's.** This section only has a
control because this seat had declared and therefore showed up as the one row that was not
`NOT-DECLARED`.

---

## 5. Residue classes, with the denominators that make them readable

**Re-derive every number here before acting on it.** They are recorded so a future Cleaner does not
read an empty board as clean, or an alarming one as a crisis.

### 5.1 A worktree registered under a session scratchpad can be emptied underneath its own registration

*Measured 2026-08-28:* **40 of 154 registered worktrees live at paths under
`%LOCALAPPDATA%\Temp\claude\...\scratchpad\`.** Four of them held nothing but `.git` and one
directory, because temp cleanup removed the rest while the worktree stayed registered.

***EACH OF THOSE FOUR READS AS ROUGHLY 1700 DIRTY FILES TO ANY SWEEP, AND EVERY ONE OF THOSE ENTRIES
IS A DELETION.*** They are the four most alarming rows on the board and they contain no work. All
four tips were backed on a remote.

**This is the non-atomic-removal shape -- directory gone, path still registered -- except nobody ran
a removal.** A `%TEMP%` path is disposable by construction and the registration does not know that.
**Check the path prefix before you interpret a large dirty count.** One directory listing settles it.

### 5.2 A high dirty count is a question, not a finding

The general form of 5.1, and it will arrive in shapes that one does not cover. Before you report
`dirty=1730`, open three of them. Deletions, a line-ending flip and real uncommitted work are the
same integer.

### 5.3 Handoff pointers

*Measured 2026-08-28, in `fleet.ps1`'s own receipt:* **47 pointers across 36 seats, 28 broken.** A
seat arriving on a carry-on reads its pointer, finds nothing, and concludes it has no handoff --
which is indistinguishable from genuinely having none.

> ***RETRACTED 2026-08-28: "IT COSTS A SESSION ITS INHERITED CONTEXT" IS FALSE. NO DOCUMENTED
> ARRIVAL PATH READS THE POINTER.*** *COMMON's five steps LIST THE DIRECTORY; the carry-on skill uses
> `os.listdir` plus a regex; `respawn.ps1 -Brief` uses `Get-ChildItem`.* **The only reader that shows
> a pointer, `fleet.ps1 -Chip`, RE-RESOLVES IT AT RENDER and prints "THAT FILE IS NOT THERE NOW.
> Treat it as a lead, not a document."**

> ***SO 34 DANGLING POINTERS COST A SEAT FOLLOWING THE DOCUMENTED PATH NOTHING.*** *Established by a
> 64-agent workflow this seat ran specifically to attack its own claim, and re-checked here.* **The
> retraction is kept because this was the section's HEADLINE PREMISE: a file that quietly drops its
> own refuted justification teaches the next reader that the finding was never questioned.**

**Repair is still right, on the narrower ground that a pointer is cheap to fix and a record is not
cheap to recreate** -- not because a resuming seat is blocked.

**Repair beats removal for every population in the coordination directory.** A stale record is a bad
pointer, not a leak. Fixing the pointer is not destructive; deleting the record is. **Never break a
lock** -- `lock.ps1`'s rule is *"we retry; we never steal"*.

***IT IS FILED, AND IT WAS FILED BEFORE THIS SEAT STARTED. `BACKLOG #1372`*** -- *"fleet pointer
health conflates three states"* -- **was filed 2026-08-27 with two halves already built.** Its
claim-by-worktree twin is ***`#1348`***. Neither cites the other.

> ***AND THE REFERENCE WAS IN THE FIRST INSTRUMENT OUTPUT THIS SEAT READ.*** `fleet.ps1`'s stop
> condition ends *"see BACKLOG #1372"*. **The seat read the counts in that line and not the
> citation**, then spent an afternoon rediscovering a filed item and routed it to the Dispatcher as
> new. ***WHEN AN INSTRUMENT'S OUTPUT CITES A LEDGER NUMBER, READ THE ITEM BEFORE YOU INVESTIGATE
> THE SYMPTOM.*** A stop condition that names an item is telling you the work is known.

***THE MECHANISM IS ARCHIVING, AND THAT IS THE ACTIONABLE HALF: 31 of 34 dangling pointers have
their EXACT basename in `handoffs/Archive/`.*** **Archiving a superseded SEAT handoff moves the file
and nothing rewrites the pointer.** **It grows with every respawn** -- the
broken count went 28 to 34 inside eighty minutes on 2026-08-28, and the Archive population keeps
pace: **42 live `.md` against 106 archived** when this was written.

**That converts "34 broken pointers" from rot into one instrument gap with a cheap fix.** *Controls:
an invented basename is absent from both directories.* **Derive both counts; do not read them here.**

> ***AND STOP AT WHAT THAT ACTUALLY PROVES. A BASENAME MATCH ANSWERS "DOES A FILE WITH THIS NAME
> EXIST", NOT "IS THIS THE FILE THE POINTER DESCRIBED".*** *An earlier version of this section said
> "content is not lost". **That was inferred from the basename match and it is retracted** -- by the
> seat that supplied it, which measured it properly when asked what it had opened.

**Comparing each seat record's recorded `bytes` against the archived file's actual size:** *recorded
size MATCHES in **5** cases, DIFFERS in **31**, and **3** basenames are not in `Archive/` at all.*
**The direction is NOT uniform** -- deltas of `+66526`, `+59374` and `+48329`, but also **one at
`-2844`**, ***and pure appending cannot produce a smaller file.***

**So the strongest supportable claim is this one:** the FILE is present in `Archive/` under an
identical basename; its SIZE differs from the pointer's recorded bytes in 31 of 36 cases, in both
directions, **so the recorded byte count is NOT a usable integrity check on the archived copy**; and
***whether the archived text preserves what the pointer described is UNTESTED.***

**The obvious cause is that `bytes` is stamped once at `-Declare` while the seat keeps updating its
handoff** -- which is exactly what COMMON's *update the episode note at each change of state*
instructs, and would mean nothing is lost. ***The one SMALLER file refutes it as a complete
explanation, and nobody has opened a pair. Do not guess in the reassuring direction twice.***

### 5.3a THE SECOND PASS: what a full sweep taught, including where it was wrong

***ANCHOR THE INDEX, NOT ONLY THE TIP. THIS IS THE ONE TO READ FIRST.*** *Deregistering one worktree
would have destroyed **96 KB that existed in no commit, on no disk and on no remote**: 8 files
ADDED TO THE INDEX AND NEVER COMMITTED (`AD` -- staged, then deleted from the working tree), plus 30
with staged modifications.* **A TIP ANCHOR DOES NOT COVER THIS.** `HEAD` does not contain a
staged-but-uncommitted index, and `git worktree remove` DESTROYS it. *All four tips were already
anchored and it would still have gone.*

```
git -C <tree> diff --cached --name-only HEAD    # non-empty = unique staged content. Run on EVERY tree.
```

**A STATUS-CODE CLASSIFIER NEEDS AN "OTHER" BUCKET, AND IT IS WHAT SAVED THE ABOVE.** *Classify each
`git status --porcelain` line as deletion / modification / untracked / **OTHER**, and print all
four.* Three of four trees were pure deletions; the fourth returned `other=38`. ***WITHOUT THAT
BUCKET ALL FOUR LOOKED IDENTICAL AND WOULD HAVE BEEN REMOVED AS A SET.*** *The 38 were `MD` and `AD`
-- codes a two-way dirty/untracked split silently drops.*

***A REMOVAL CAN FAIL AND SUCCEED AT THE SAME TIME. CHECK BOTH ARMS, NEVER THE EXIT CODE.***
`git worktree remove --force` returned **rc=255, "Filename too long"** on all four -- a Windows
MAX_PATH failure on ~150-character temp paths. ***DEREGISTRATION SUCCEEDED ANYWAY. DIRECTORY DELETION
DID NOT.*** *A reader checking `rc` concludes nothing happened; a reader checking the registry
concludes it worked. Both are half right.*

**PROCESS RESIDUE IS A CLASS, AND THE SIGNAL IS A CPU DELTA AT THE TREE -- NEVER PER PROCESS, NEVER
AGE, NEVER PATH.** *18 pytest processes, oldest **69.2h** running with `--timeout=180` it had
outlived ~1,380 times.* **Nothing on this box reaps them: zero files under `scripts/`, `.github/` and
`tests/` call `Stop-Process` or `taskkill`, against a positive control of 40 files matching "git
worktree"** *(re-verified here).* **Cumulative CPU is NOT the signal** -- orphans had banked 759 to
1006 CPU-seconds. ***APPLY IT TO THE PROCESS TREE: A LIVE PAIR'S PARENT READS 0.00, because it is the
xdist controller waiting on its worker.*** *Nine of nine pairs were parent-and-child; the reap proved
it by execution -- 12 kills issued, six succeeded and six reported already gone.*

**WIDENING AN APPROVED ACT IS THE FAILURE THE APPROVAL EXISTS TO PREVENT.** *The owner approved 12
processes; by execution the rule made 14 reapable.* **12 were executed and the other 2 routed back.**
*The two extra had been LIVE at approval and died in between when a hard stop cut their parent
session.* **COMMON's relayed-approval row owns this rule now; it is named here because this is where
it was paid.**

---

#### The four where this seat was WRONG, and they are the ones to keep if you keep only some

***THE SEAT'S FAILURE MODE IS DOING TOO MUCH; ITS SECOND IS ANSWERING THAT BY DOING NOTHING. A FILE
THAT RECORDS ONLY THE SAVES TEACHES THE SECOND ONE.***

| what was claimed | what was true |
| --- | --- |
| Four scratchpad worktrees were **"emptied"** | Called on **two top-level entries**. `docs/` held **191-217 files**. ***A root-level count answers a whole-tree question*** |
| **13 of 55** vault tips were unbacked | ***ALL 13 WERE ON THE REMOTE.*** `refs/remotes` is written by `fetch` -- it measures what YOUR CLONE LAST HEARD. Screen offline with it; confirm every hit with one `git ls-remote`. **Never publish the screen's number** |
| A dangling pointer costs a seat its context | **Refuted above.** No documented arrival path reads it |
| **"My second mailbox"** | It was the PRIMARY's **SHARED** box holding ~220 records from many sessions. *Measured "a box containing my session id" and reported "my second mailbox"* |

**AND THE SEAT'S YIELD, MEASURED, BECAUSE THE FILE SHOULD NOT FLATTER ITSELF:** *across a full
session -- worktrees removed **0** until an explicit grant, claims released **0**, branches deleted
**0**, files deleted **0**.* Then 13 processes and 4 deregistrations, both under per-act owner
approval, and 68 anchor refs created. ***THE BOARD GREW DURING THE PASS: 154 registered worktrees to
166, 28 claims to 30.*** *Three populations that looked alarming resolved to nothing, and the reap's
justifying hypothesis LOST -- the test it was meant to fix failed again afterwards.*

---

### 5.4 THE INVERSE CASE: LIVE WORK THAT PRESENTS AS RESIDUE, AND A COMMIT THAT SILENTLY REVERTS

> ***THE CONDITION BELOW IS CLEARED. THE INSTRUMENT IS NOT.*** *Reported by this seat against its own
> file and verified 2026-08-28T18:33Z after a fresh fetch:* **both `numstat` forms return 0 paths
> across all of `roles/`, and the vault primary is on `main` level with `origin/main`.** The split
> described here stood about **seventy minutes** and reached a report to the owner. **Read what
> follows as a worked example, not as a state of the tree** -- as written in the present tense it
> would send a future Cleaner hunting a revert that is not there. **Expiry discharged; do not
> re-raise it without re-measuring.**

**Section 1 warns that residue is indistinguishable from live work. The inverse is just as
dangerous and this seat will meet it more often, because a shared checkout is exactly where it
lives.**

*Measured 2026-08-28 on the vault primary, `<HOME>\Code\MessageFoundry-vault`.* It carried
every signal this seat reads as leftovers: **14 dirty paths, a branch 94 commits behind
`origin/main`, staged files nobody committed, a half-done rename, and a last commit dated a week
earlier.** It was a live workbench with three sessions typing in it, one of them writing this file.

***AND THE HAZARD IS NOT UNTIDINESS. IT IS THAT COMMITTING THAT TREE REVERTS WORK, AND THE REVERT
LOOKS LIKE AN ORDINARY COMMIT.***

**The index and the working tree held different versions of the same files:**

| Copy of `roles/CLEANER.md` | Lines |
| --- | --- |
| `origin/main` | 904 |
| **The INDEX** | **904 -- byte-identical to `origin/main`** |
| The working tree | 389, carrying the owner's own paring plus a pass of new content |

`git status --short` prints `MM` for that. ***VS CODE PRINTS A SINGLE `M`.*** A reader working from
the editor cannot see that two versions exist, and a bare `git commit` takes the stale one. A peer
measured the same split on `roles/BUILDER.md` at **1255 lines** between index and `origin/main`,
against **89** for the working copy -- so the literal reading of a *"commit this folder"* instruction
would have reverted that file by roughly 1150 lines on `origin/main`.

**The two commands that separate them. Run BOTH; neither alone is the answer:**

```
git diff --cached --numstat origin/main -- <path>    # what a commit would actually take
git diff          --numstat origin/main -- <path>    # what the person at the keyboard sees
```

**Second mechanism in the same tree, and it is the one to file:** eleven of those staged files had
**already landed on `origin/main` days earlier**, one commit saying so in its own subject. Somebody
had rescued the work, and ***the residue of the rescue was left in place, looking exactly like
unrescued work.*** A sweep re-rescuing it lands a revert.

**Third: the branch itself.** `asvs-12-3-4-residual-329` was 94 behind, 7 ahead, and **carried zero
unlanded commits under `roles/`** -- its PR had already merged. Landing anything from there is the
squash-base trap.

***THE OPERATIONAL RULE, AND IT IS WHY THIS SECTION IS HERE RATHER THAN IN A LANDER FILE.*** When a
shared checkout holds work you want to land:

1. **Never `git add -A` or `git commit -a` in a tree you do not own.** Stage explicit paths.
2. **Before staging anything, diff the INDEX against `origin/main`, not just the working tree.**
3. **Prefer moving the file to a fresh worktree cut from `origin/main`** and committing it there.
   That leaves the shared tree untouched, sheds a stale index, and sheds a stale branch in one move.

*The cost this actually carried, recorded honestly because an accurate small number outlives an
inflated one:* **about forty minutes of measurement, and a near miss. Nothing landed wrong.** That
is the first entry in this seat's cost ledger, and it is a near miss caught by measurement, not a
realised loss. **Do not inflate it later.**

---

## 6. Reporting -- the denominator IS the product

**A cleanup report that says "registry clean" is the most dangerous artifact this seat can produce**,
because the next reader stops checking. Your product is reassurance, and reassurance is exactly what
a blind instrument also emits.

**Every report carries, without exception:**

1. **The denominators**, from the same command that produced the finding.
2. **The positive control and whether it passed** (section 4).
3. **The UNKNOWN count as a headline number, not a footnote.** Resolving an UNKNOWN by acting on it
   is the one move this seat cannot make.
4. **What you did not examine**, as *"at least"* rather than an enumeration.

**STATE WHAT ZERO MEANS, every time you print one.** *"Unbacked HEADs: 0 of 154"* means every tip is
reachable from a remote today. It does not mean nothing can be lost -- 31 trees on that same board
held uncommitted content no remote had.

---

## 7. Traps

**7.1 Reading an absence as a fact.** The session registry fails OPEN toward alive and says so in
source. There is no heartbeat on this host, so the absence of a session is never a fact here, only
an absence of evidence. *Measured 2026-08-28:* two seats read RUNNING on `fleet.ps1` with no live
session in `presence.ps1`. Two instruments disagreeing is an UNKNOWN, not a verdict.

**7.2 Letting the report drive the act.** A tool that prints `confirm with -Name <slug>` prints it
on exactly the rows its last remaining signal is protecting. **A tool's suggested next step is not
an authorisation**, and it is generated by the same code that just declined to act.

**7.3 Joining on the worktree instead of the lane.** Section 4. Every over-report is a live lane
stripped of a key it is still using.

**7.4 Manufacturing work from an alarming raw number.** Sections 4 and 5.1 are the same lesson
twice. **Every alarming number this seat has measured so far got smaller when it was opened.**

**7.5 Fixing the instrument by hand.** You will find defects. Hand-fixing one is a sweep whose
benefit expires the next time somebody runs the tool. **File it** (section 8).

**7.6 Becoming a destroyer by attrition.** Under pressure, acting is faster than routing, and each
act is individually defensible. **If you find yourself removing, releasing or deleting, you have
left the seat.**

**7.7 A count welded to a cause.** *"The holder is gone, SO the claim is stale."* *"The tree is
clean, SO nothing is lost."* **The tell is grammatical: the measurement is a noun and the step past
it is a connective** -- *because*, *so*, *therefore*, *which means*. Everything before it was
measured; everything after it usually was not, and the part after it is the part that authorises the
act. You are handed these constantly. Split them.

**7.8 Your own residue.** You take claims, write seat records and leave a worktree like everyone
else. Release what you took and declare your seat before you go. **A Cleaner that accumulates is an
argument against the seat.**

**7.9 A clean scan you never proved could see anything. SURVIVED, not predicted -- 2026-08-28, on
this file, minutes after section 6 was written into it.** The glyph and encoding check over this
playbook printed `none`, which is the right answer. The positive control run beside it **crashed**:
the seeded probe string tripped a `UnicodeEncodeError` on the cp1252 console while printing its own
result, so the control produced no verdict at all. **A `none` beside a control that did not complete
is not a measurement.** Re-run with the offending characters reported as code points rather than
printed literally, and the control passes cleanly. **The seat that had just written "reassurance is
exactly what a blind instrument also emits" accepted a blind instrument's reassurance.** Expect that;
the rule protects nobody who applies it only to other people's numbers.

---

## 8. Where findings go -- route, do not act

**Your deliverable is a routing list plus ledger items.**

| Finding | Goes to |
| --- | --- |
| A claim that looks releasable | **The running lane first** (section 4), by mail. Then the Lander |
| A worktree that looks removable | **The owner.** The gate's own deny text names the human as the actuator |
| An instrument defect | **The Dispatcher**, as a ledger item |
| A question only the owner can settle | **The Liaison** while one is live |
| A branch carrying commits on no remote | **The Lander** -- pushing is a landing act |

**Mail leaves a receipt and reaches an idle or different-login peer; a cross-session message is
faster and dies with the session.** `mail.ps1` enforces a byte cap and a per-line cap separately, so
a long finding is two rejections away. **Write the long form to a file in your worktree and mail the
path** with a short summary.

**A KNOCK REACHES A WORKTREE, NOT A SESSION.** Whoever is standing in that worktree receives it, and
that is routinely not the seat you meant, because a worktree outlives the session that named it. A
prompt, well-formed reply from the wrong occupant **reads identically to delivery**. So: **only a
reply that IDENTIFIES ITSELF AS THE HOLDER OF THE NAMED CLAIM counts as anything.** Silence was never
evidence and is not evidence now.

**FILING BEATS FIXING.** Prior passes here produced their value as instrument fixes, not as
removals: one released a single claim and removed zero worktrees; another moved things and deleted
nothing. That is the validated shape of a good pass.

***AND FOR ANY "IS THE FIX IN" QUESTION ON THIS BOX, COMPARE TWO HASHES, NEVER A CHECKOUT DISTANCE:***

```
git hash-object <resolved ABSOLUTE path of the file that will actually run>
git rev-parse origin/main:<repo-relative path>
```

**Landing is not arming.** Print the resolved absolute path in the receipt -- this box has held
dozens of copies of the same script, and *"it is fresh"* is not a sentence with a referent.
*Measured 2026-08-28:* both halves of the armed worktree gate passed this test -- the installed
`worktree_gate.ps1` hashed identically to the `origin/main` blob, and the allowlist held both
governed repos. **Checkout distance would have answered neither question.**

### 8.2 `mail.ps1 -To` TAKES A PATH, AND `-To all` MEANS LIVE PEERS ONLY. BOTH BIT THIS SEAT TODAY.

**`-To <name>` is not a worktree name. It is a PATH**, tested with `Test-Path -PathType Container`
(near *"Recipient worktree does not exist"*). A bare leaf name fails **even when that worktree exists
and is registered** -- and the refusal says *"Recipient worktree does not exist"*, which invites
exactly the wrong conclusion. *Measured 2026-08-28: I read that message as a removed worktree twice,
for two different trees, both of which were present on disk and in `git worktree list`.* **Pass the
absolute path.** **A refusal message names its own predicate, never the state of the world.**

**`-To all` broadcasts to LIVE PEERS from `presence.ps1`, excluding self.** That is correct by
design and it is the opposite of what this seat usually needs. ***THE POPULATION A CLEANER KNOCKS ON
IS BY DEFINITION THE QUIET ONE, AND A BROADCAST CANNOT REACH IT.*** Address a quiet holder by path,
individually, or the knock was never sent.

*Measured the same afternoon, and it is why this matters more than it sounds:* **live sessions went
from 12 to 3 in 35 minutes** while this pass was running. Two Lander worktrees that had read
`RUNNING` on `fleet.ps1` an hour earlier were unoccupied by the time a branch was ready for them.

***SO THE ROUTING TABLE ABOVE HAS A PRECONDITION IT DOES NOT STATE: THE SEAT YOU ARE ROUTING TO HAS
TO EXIST.*** Mail to an empty worktree is not lost -- it waits for the next occupant, which is the
whole reason to prefer it over a cross-session message. **But waiting is not delivery, and a Cleaner
that files a finding into an empty box and calls it routed has done nothing.**

**Check before you route, not after:**

```
pwsh -NoProfile -File scripts\coord\presence.ps1 -Json     # who is actually here, now
```

**If the seat that owns your finding is not running, COMMON's fallback applies: it goes to the owner
directly, and your own push needs their approval.** Say in the same breath that you tried the seat
and it was not there -- an owner who thinks a Lander has it will wait for a landing that nobody is
going to perform.

---

## 9. Live state goes in an episode note, never here

Which claims you hold, what you swept, who has not replied: none of it belongs in this file. It goes
in a dated note under `<git-common-dir>/mefor-coord/handoffs/`.

**Derive that directory, never type it:** `git rev-parse --path-format=absolute --git-common-dir`. A
bare `.git/mefor-coord/` is wrong from a worktree and every session is in one -- `.git` there is a
file, so the bare form lists **nothing**, and an empty listing looks exactly like an empty queue.

The dated numbers in sections 3 through 5 are the deliberate exception. **Re-derive them; do not
inherit them.** If they have moved far enough to change a conclusion, that is itself a finding.
