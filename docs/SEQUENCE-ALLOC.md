# Sequence allocation

<a id="tldrbluf"></a>

Reserve shared sequence numbers with `scripts/coord/alloc.ps1`. Pair it with `scripts/hooks/seq_check.py` to reject
reused numbers at commit time.

Two sessions can use one number in differently named files that git merges without conflicts. The
other controls here cannot detect that collision.

Use this for numbered sequences with one worktree per session. Shared checkouts collapse ownership
to "somebody here allocated it" ([Worktrees](WORKTREES.md)).

Vendor these scripts into the governed repository and provide `pwsh` 7.3+ and
`python` on `PATH`. Even `bin/ccx-doctor.ps1` refuses below 7.3 ([Install](INSTALL.md)).

[Configure a sequence](#configuring-a-sequence) in `ccx.config.json` to activate the scripts. The gate ships unwired; run the doctor
before assuming it enforces anything.

---

Git cannot reserve a shared sequence value. Two sessions can choose the same next number for:

- Decision records named `0001-*.md`, `0002-*.md`.
- Issues written as `## 58.` headings in one file.
- Migration numbers, RFC numbers, schema versions.

Rules 1 to 3 inspect added files matching `filePattern`, covering the first and third examples.
Numbers inside a file do not change its path.

For headings inside one file, only rule 4 can run. The allocator still reserves unique numbers, but
commit-time checks cannot defend those reservations.

`examples/sequence-adr/` provides a worked example. The mechanism applies beyond decision records;
`ccx.config.json` defines each sequence.

---

## The defect

Two sessions can each see `0004` as free and create `0004-alpha.md` and `0004-beta.md`.
They can also add two `## 58.` headings sixteen hundred lines apart.

Git merges both changes without conflicts because they touched different bytes.

| Control you might expect to catch it | Why it does not |
|---|---|
| A worktree per session | The collision is *between* worktrees. Isolation is what makes it possible. |
| A file lock | Different filenames. Nothing is contended. |
| `git merge-tree` / a merge dry-run | It merges clean by construction. That is the whole problem. |
| Code review | Both diffs are individually correct. |
| A green CI on each branch | Each branch is internally consistent. The duplicate exists only after the *second* merge. |

This collision happened three times where the tooling was built. Each was recorded as "numbers
churn, recompute before merging", leaving the concurrency defect unfixed.

> **Rule.** Never compute the next free number by scanning for a maximum and adding one. Allocate it
> atomically, and enforce the allocation at commit time. When a symptom keeps recurring and the
> remedy keeps being "redo it by hand", ask whether you are looking at a race.

On 2026-08-11, a session checked an identifier, composed its entry, and wrote it. A peer took the
number between check and write; these were separate operations.

This allocator cannot share a series between clones because each has its own state root. The
identifiers in [house style](HOUSE-STYLE.md) span two repositories and have that limit.

On 2026-08-12, [spec-kit](https://github.com/github/spec-kit)'s `main` scanned spec directories for the highest
3-or-more-digit prefix and added one. The inspected scripts had no lock or atomic claim.

Opt-in `--timestamp` uses `YYYYMMDD-HHMMSS` instead. The default still scans without locking;
explicit `--number` also increments collisions without atomic protection.

On 2026-08-15, `specify-cli` 0.16.4 still used unlocked `Get-HighestNumberFromSpecs` ([Spec Kit 0.16.4 for a KORUS build](FRAMEWORK-spec-kit.md)).

Two projects independently use flat, project-scoped records. `examples/sequence-adr/` uses `docs/adr/NNNN-slug.md`;
`panaversity/spec-kit-plus` uses `history/adr/NNNN-slug.md`.

The fork adds the ADR command upstream lacks, with the same scope. Its automatic numbering still
lacks atomic allocation and an index gate.

### The index is gated, and that is the auditability half

`seq_check.py` rejects reused numbers, unallocated numbers, missing index entries, and duplicate
index rows. Index checks matter when records serve as evidence.

Reviewers use the index to assess the decision set. An unlisted record can be missed without any
visible warning.

The gate checks whether the index accounts for the records. Without it, claiming a complete decision
set requires separately enumerating the directory.

A citation count reported without its filter has the same weakness ([Spec Kit 0.16.4 for a KORUS build](FRAMEWORK-spec-kit.md)).

---

## The two halves

Allocation and commit checks are both required.

| Half | File | What it does | When it runs |
|---|---|---|---|
| **Allocator** | `scripts/coord/alloc.ps1` | Hands out a number nobody else can hold, by exclusively creating a file named after it | When you ask for a number |
| **Gate** | `scripts/hooks/seq_check.py` | Refuses a commit that adds a number which is already taken, unallocated, or missing from the index | `pre-commit`, and again in CI with `--ci` |

The allocator exclusively creates `<state-root>/alloc/<kind>/<number>.json` with `FileMode::CreateNew` and `FileShare::None`. If a
peer wins first, `IOException` makes it try the next number.

Eight concurrent PowerShell writers to a shared list silently lost four writes. Eight concurrent
allocator processes instead returned eight distinct numbers with zero collisions.

`tests/test_a_number_is_claimed_by_creating_a_file.py` runs real allocator processes against throwaway repositories.

It found eight simultaneous runs returning only SEVEN numbers. One process failed on the shared
high-water file during the floor scan, before claiming a number.

Timing alone is a weak test. Changing the claim to `Create` still returned eight distinct
numbers because the floor skipped existing claim files.

The stronger test inserts a competing claim immediately after choosing the number. That guarantees
the case where a sibling wins just before creation.

The registry is `<git-common-dir>/<prefix>-coord/alloc`, resolved by `Get-CcxStateRoot` in `scripts/coord/_common.ps1` and
`state_root()` in `scripts/hooks/_ccxconfig.py`.

Linked worktrees share the registry; other clones do not, and `git add -A` cannot reach it.
Numbers are never reclaimed, even after a branch is abandoned; gaps prevent reuse collisions.

---

## Configuring a sequence

Define the numbered files' directory and filename pattern, plus any index row.

Add `sequences` to `ccx.config.json`. This decision-record example comes from `examples/sequence-adr/`:

```json
{
  "sequences": {
    "adr": {
      "dir": "docs/adr",
      "filePattern": "^docs/adr/(\\d{4})-[^/]+\\.md$",
      "pad": 4,
      "indexFile": "docs/adr/README.md",
      "indexRowPattern": "^\\|\\s*\\[(\\d{4})\\]"
    }
  }
}
```

| Key | Required | Meaning |
|---|---|---|
| `dir` | yes | The directory swept for existing numbers, repo-relative, forward slashes |
| `filePattern` | yes | Regex over the repo-relative path. **Group 1 must capture the number.** |
| `pad` | no | Zero-padding width. `0` or absent means none |
| `indexFile` | no | An index/table file that must carry a row per number |
| `indexRowPattern` | with `indexFile` | Regex recognizing one row. **Group 1 must capture the number.** |

Both scripts validate configuration before touching the registry. Errors name the offending key.

### More than one ledger

Declare each ledger in the `sequences` map. Decision records and a backlog can each use their
own five keys:

```json
{
  "sequences": {
    "adr":     { "dir": "docs/adr",     "filePattern": "^docs/adr/(\\d{4})-[^/]+\\.md$", "pad": 4 },
    "backlog": { "dir": "docs/backlog", "filePattern": "^docs/backlog/(\\d+)-[^/]+\\.md$" }
  }
}
```

Each kind has a separate registry, floor, and claims. Adding one leaves existing entries alone; with
two kinds, `-Kind` becomes required and errors list valid names.

With two sequences, the allocator checks these rules before touching the registry:

| Rule | Why |
|---|---|
| A name must be one plain path segment | It becomes a directory under the registry. A sequence named `../escape` wrote its claims outside it and reported success |
| No two entries may share a `filePattern`, or an `indexFile` plus `indexRowPattern` | The claim excludes per kind. Two entries recognising one set of files can each issue the same number |

The check detects identical patterns only. Different regular expressions can still overlap without
detection.

Give each sequence a pattern exclusive to its files. After copying an `adr` block, change
both its name and matching strings.

Most sequence errors omit the config path. Upward discovery and `CCX_CONFIG` can select another
file; use the doctor to see which one loaded.

Without `sequences`, the allocator refuses and names the file to edit. The gate silently exits
0.

Provide both `indexFile` and `indexRowPattern`, or neither. A partial configuration silently
removes a floor term and can make the floor too low.

The allocator rejects both incomplete forms. The gate rejects `indexFile` alone, but accepts
`indexRowPattern` alone, skips rules 3 and 4, and exits 0.

Check the key pair when wiring the gate by hand. The accepted incomplete form can otherwise look
like a working check.

### `indexRowPattern` is compiled multiline, and that was once a silent hole

`alloc.ps1` uses `RegexOptions::Multiline`; `seq_check.py` uses `re.M`. Without them,
`^` matches only the start of the string, not each line.

The all-refs term supplied one line at a time, so matching worked. The working-tree term supplied a
whole file, so `^` missed every later line.

Without `Multiline`, the working-tree term found none of the index rows. Since its
introduction, it had missed numbers written but committed nowhere.

The all-refs term hid this defect by covering committed numbers. Only uncommitted numbers needed the
broken term.

> **Rule.** When two terms of the same computation feed one matcher different shapes of input, the
> stricter shape is the one to test. A term that is subsumed by a broader term in the common case
> will not announce that it has stopped working.

---

## Using it

Allocate a number or inspect the floor without spending one. The floor is the highest taken number
visible to the clone.

Run from the repository receiving the number. The allocator resolves git and configuration from the
current directory, not its script location.

Relative commands below assume vendored scripts. For a separate tooling clone, use `Set-Location`
to enter the target and call the script by absolute path.

Run `git fetch origin --prune` before allocating. The remote-tracking scan cannot see a peer's pushed number
until you fetch it.

```powershell
# take a number
pwsh -NoProfile -File scripts/coord/alloc.ps1 -Kind adr -Title "Worktree gate"

# inspect the floor without spending anything
pwsh -NoProfile -File scripts/coord/alloc.ps1 -Kind adr -ShowFloor

# what does this worktree currently hold?
pwsh -NoProfile -File scripts/coord/alloc.ps1 -List
```

A successful allocation prints the number, target directory, and required path pattern.

It suggests a filename only when the title produces a nonempty slug. It prints an index reminder
only when `indexFile` exists; fewer lines need not mean an incomplete run.

The two parameters:

- `-Kind` may be omitted when exactly one sequence is configured. With two or more it is
  required, and the error lists the configured names. The parameter is deliberately **not** a
  `ValidateSet`, so the repo does not carry two lists of kinds that have to agree.
- `-Title` is required for a real allocation. It is recorded in the claim, so a sibling
  session running `-List` can see what the number is for.

Claims contain `number`, `kind`, `title`, `branch`,
`worktree`, and `claimed`. Write UTF-8 without a BOM: the gate uses `encoding="utf-8"`,
and a BOM makes `json.loads` raise.

---

## The floor, and why it ratchets

The allocator uses the first number above the floor. It takes the maximum of four sources, then
applies the persisted high-water mark:

| Term | Source | Catches |
|---|---|---|
| 1. Filenames, per ref | `git ls-tree` over `dir` for **HEAD, trunk, every `refs/heads` and every `refs/remotes`** | A number on any branch, published or not |
| 2. Index rows, per ref | `git cat-file --batch` over `<ref>:<indexFile>` | A number recorded in the index but not yet a file |
| 3. Working tree | The directory and the index file on disk | A draft written but committed nowhere |
| 4. Registry | `<state-root>/alloc/<kind>/*.json` | A number claimed but not yet written anywhere |

Any ref can hold a taken number. A trunk-only scan misses unpublished branch numbers, allowing
duplicates in differently named files that later merge without conflicts.

On Windows, one `git show` per ref took roughly 34 seconds. Two `git cat-file` processes
took about 3 by deduplicating shared blobs among several hundred specs.

### The ratchet

The scan sees only this clone's refs. Its floor once exceeded origin and local heads because of
tracking refs for a remote absent from `git remote -v`.

Deleting those refs would lower the computed floor and allow silent reissue of numbers in use.

Persist the floor at `<state-root>/alloc/<kind>/.floor-highwater`; it may rise but never fall. If the computed value falls below
it, `alloc.ps1` prints both values and tells you to re-fetch.

| Operation | Verdict |
|---|---|
| `git fetch origin --prune` | **Safe** -- prunes only `refs/remotes/origin/*`, and is what you should run before allocating |
| `git remote prune <other>` / `git remote remove <other>` | **Dangerous** -- deletes a block of remote-tracking refs |
| Deleting remote-tracking refs by hand | **Dangerous** |
| Aggressive `gc` / `reflog expire` dropping unreachable objects | **Dangerous** |

The high-water mark prevents reissue but cannot restore history lost with deleted refs.

### Allocation is a one-way door, so it ships a read-only probe

Before `-ShowFloor`, checking the floor required spending a permanent number. An entire release
scanned two refs while its header promised all of them.

`-ShowFloor` allocates nothing and prints:

- the kind, and the resolved trunk;
- the floor, with the computed value and the high-water mark shown separately;
- the paths it swept;
- the number it would issue next, and the watermark path.

The probe has two required properties:

- It names its sources, not just the number. "Which paths did this sweep actually read" is the
  question every silent-narrowing bug turns on, and a bare integer cannot answer it. A floor looks
  identical whether it swept one path or two.
- It cannot corrupt what it reads. `Get-Floor -Peek` skips the high-water write. The first run of
  `-ShowFloor` against a deliberately planted number ratcheted that clone to a fabricated floor
  no later run could undo. An inspection that moves the thing it inspects is not an inspection.

`-ShowFloor` and allocation share one computation, differing only by `-Peek`. Put every
outcome-changing guard in `Get-Floor` or above both paths; an earlier guard bypass made their
results differ.

> **Rule.** Any irreversible allocator needs a dry run that reports its own inputs, and the dry run
> must run the same code path as the real thing.

---

## The gate

`scripts/hooks/seq_check.py` runs at `pre-commit`, and again in CI with `--ci`.

### Why a git hook, and why the shared hooks directory

`.git/hooks` belongs to the common git directory shared by linked worktrees. A hook there:

- reaches every worktree the instant it is written -- no branch, no merge, no propagation lag;
- survives a branch switch in any of them, because it sits outside every working tree;
- and sees every write route, because it inspects the staged tree rather than a tool call.

A `PreToolUse` hook sees arguments before execution and misses shell redirects,
`Set-Content`, `python -c`, heredocs, editors, and subagents. A commit hook sees their
staged bytes.

### What it checks

Per configured sequence:

1. An **added** file must not reuse a trunk number N. Exception: its index row names the new file as
   a declared companion. Only an *undeclared* reuse is a collision. The companion is matched with
   and without its extension, since an index row links the stem.
2. An **added** number not already on trunk must have been allocated to *this worktree*. The check
   sits behind rule 1, so a declared companion at an existing number is not asked for a claim. Local
   only -- see the mode asymmetry below.
3. An **added** number must have a row in the sequence's `indexFile`.
4. The index must not gain a **duplicate** row for one number.

### What it deliberately does not check

The gate ignores existing trunk debt. Rule 3 covers added files only; rule 4 subtracts duplicates
already on the base.

Renames onto taken numbers also escape, unintentionally. Both modes use `--diff-filter=A`, excluding
git's `R` entries.

`git mv docs/adr/0009-foo.md docs/adr/0004-bar.md` yields no added path. Rules 1 to 3 never examine `0004`; review
numbered-directory renames yourself.

> **Rule.** A gate that fails on pre-existing debt is a gate that gets uninstalled, and it takes the
> real protection with it when it goes.

The gate reads the staged tree through `git show :path`. Reading the working tree would let an
unrelated unfinished file block commits.

The gate uses the standard library without project imports because worktrees may lack virtualenvs.
Its shared sibling import, `_ccxconfig.py`, must load or it exits non-zero with an explicit error.

### Two rules that keep it honest

`_ccxconfig.git()` applies two rules learned from failures:

- **`encoding=` is required.** `text=True` alone decodes with the locale default, cp1252
  on stock Windows. Index files are routinely UTF-8, so the decode raised in subprocess's reader
  thread. `proc.stdout` came back `None`, the caller died on `findall(None)`, and the
  commits it guards were blocked.
- A non-zero git exit raises. A bad ref or an unfetched base must never read as an empty file,
  because an empty index parses as "no numbers taken". When the wrapper swallowed non-zero exits,
  the added-files list came back `[]` and the gate reported PASS on every run where it
  could not see.

Use `object_exists()` to test legitimate absence from a ref. A broad `except` could also hide
a broken ref.

The gate reports unchecked conditions on stderr on both pass and fail. If the trunk cannot resolve,
it says the already-taken check did not run.

---

## Wiring the pre-commit hook

`scripts/coord/install-git-hooks.ps1` owns `commit-msg` and `pre-push`, never `pre-commit`. Competing
ownership once left a foreign hook behind a broken Windows framework shim, blocking every commit.

When `sequences` exists, the installer prints a yellow warning that the gate is unwired.
`bin/ccx-doctor.ps1` reports OFF with a reason; commit-time protection waits for manual wiring.

Make commits reject reused, unallocated, or unindexed numbers.

Add this line to your existing hook framework:

```sh
# in your existing pre-commit hook, or as its own file if you own that slot
python scripts/hooks/seq_check.py || exit 1
```

Pre-commit runs from the working tree root. The relative path therefore requires vendored scripts.

If the governed repository lacks `scripts/`, Python cannot open the gate. `|| exit 1`
then refuses every commit:

<!-- no-copy -->
```text
python.exe: can't open file '<repo>\scripts\hooks\seq_check.py': [Errno 2] No such file or directory
```

This error means the hook cannot find the gate. Use an absolute gate path if the scripts live
elsewhere.

Missing Python also blocks commits. This gate has no `/bin/sh` shim, so the shell's non-zero
result reaches `exit 1`, unlike the two installed hooks.

Inspect wiring with the doctor:

```powershell
pwsh -NoProfile -File <tooling>/bin/ccx-doctor.ps1 -Repo <the-repo-you-govern>
```

The doctor searches for literal `seq_check` in the resolved `pre-commit` file. It does not
execute the gate.

It can report `OK` for comments, wrong paths, or non-executable hooks, and
`OFF` for framework indirection. Prove enforcement with a real commit.

The doctor separately runs the allocator's read-only `-ShowFloor` probe. It can detect a broken
allocator without consuming a number.

---

## Modes are not symmetric, and saying so is the point

`--ci` checks against a freshly fetched trunk to catch collisions between individually
valid branches. It repeats every rule except allocation ownership.

Rule 2 requires the local registry and worktree path. A fresh CI clone has neither, so running it
there would reject every item.

An earlier CI version computed and discarded that rule's set. The code looked like coverage but
could not fail.

> **Rule.** If a rule cannot run in a mode, name it as not running. Never leave it in place looking
> like coverage. A green CI on a numbered pull request is **not** evidence that the number was
> allocated to anybody.

After `--no-verify`, a commit can take a number from another session's unmerged branch. The
second merge exposes the collision later, visibly and recoverably.

CI requires a resolvable base and raises on failure. Local mode prints a warning instead; in CI,
missing the base defeats the job's purpose.

### If you wire the CI leg

Apply these three requirements to the CI step:

- Do not gate the step on a "code changed" path filter. A pull request that only adds a decision
  record *is* a docs-only change. A `code == 'true'` condition makes the governance step skip on
  exactly the pull requests it exists to police.
- Ride it inside an already-required job rather than adding a brand-new required context. A newly
  required check wedges every pull request opened before it existed.
- Use a two-dot diff (`base HEAD`), not three-dot. On a pull request the checkout is the merge
  commit, so HEAD contains base. Three-dot resolves a merge base, and two shallow histories fail to
  reach their common ancestor. Deepening to fix that is itself a race, and the failure was
  **silent**.

---

## Ownership is only as real as your isolation

`owns()` compares the claim's `worktree` field with the current repository root using
`fold_path()`. That makes the worktree the ownership key.

The key works only with separate worktrees. Before enforced isolation, sessions here shared the
primary checkout and rule 2 was a no-op.

> **Rule.** Check that your ownership key actually distinguishes the actors in practice, not merely
> in principle. Number allocation and worktree isolation are a pair -- the first is meaningless
> without the second making the key real.

`fold_path()` in `_ccxconfig.py` must match `ConvertTo-CcxComparablePath` in `_common.ps1` character for
character. Different folding can silently grant or refuse all ownership checks.

---

## Two lessons from a guard that had to be removed

These lessons concern a guard removed from the allocator. The shipped code deliberately excludes it.

The guard confused the overall floor with a per-band maximum in a partitioned sequence. The first
legitimate upper-band entry then blocked every allocation.

The overall floor must include every band to prevent reissue. A per-band maximum answers how many
numbers remain in that band and must exclude the others.

The guard rejected normal use of the partition instead of detecting a boundary breach.

> **Rule.** Name each measurement by the question it answers, then check which one every consumer
> reads. A guard that fires on correct input will be disabled, and it takes the real protection with
> it.

Once a number existed in the shared band, the data could not distinguish a breach from legitimate
use. The guard had to reject valid input or never fire; the needed evidence was absent.

> **Rule.** Remove a branch that cannot fire; do not leave it dormant. Replace it with something the
> data can actually support -- a warning at a threshold measured on the band where the other band's
> numbers cannot distort it -- and say in the docs what is no longer detected.

---

## Limits

These limits remain even when allocation and checks succeed:

| Limit | Consequence |
|---|---|
| `git commit --no-verify` bypasses the gate | This is a guardrail against accident, not a security boundary. The `--ci` run is the backstop. |
| Ownership is never checked in CI | A green CI is not evidence the number was allocated. |
| No installer writes `pre-commit` | Until you wire it, nothing at commit time stops two sessions using the same number. The doctor reports this as OFF, not as absent. |
| This gate fails **closed** with no python | Behind no `/bin/sh` shim, so a missing interpreter blocks every commit. The two *installed* git hooks go the other way: their shims exit 0. The doctor reports the interpreter. |
| `sequences` also arms the claim gate | `claim_check.py` takes its `<KIND>` tokens from the configured sequence names, so a commit subject naming an unclaimed item is refused too ([Coordination](COORDINATION.md)). |
| Ownership is worktree-keyed | Where every session shares one checkout, it collapses to "somebody here allocated it". |
| Two sessions can still build the same thing under two *different* numbers | Nothing structural sees duplicated work. That is what claims and announce are for -- see [coordination](COORDINATION.md). |
| The high-water ratchet cannot restore history | It stops re-issue. The commits those refs pointed at are still gone. |
| Numbers are never reclaimed | Sequences develop holes. Accepted by design. |
| A series shared across two clones cannot be allocated here | The state root is per-clone by design, so two repositories issuing from one series share no allocator. The rule identifiers in `docs/HOUSE-STYLE.md` are in that state, and the control there is a dated table rather than a gate. |

---

## Files

| Path | Role |
|---|---|
| `scripts/coord/alloc.ps1` | The allocator: floor sweep, high-water ratchet, atomic claim, `-ShowFloor`, `-List` |
| `scripts/hooks/seq_check.py` | The gate: four rules, `pre-commit` and `--ci` modes |
| `scripts/hooks/_ccxconfig.py` | Config discovery, the raising git runner, path folding -- shared by the Python hooks |
| `scripts/coord/_common.ps1` | The PowerShell counterpart: `Get-CcxConfig`, `Get-CcxStateRoot`, `Get-CcxTrunk`, `ConvertTo-CcxComparablePath` |
| `scripts/coord/install-git-hooks.ps1` | Installs the claim gate and push guard; reports that the sequence gate is *not* installed |
| `bin/ccx-doctor.ps1` | Reports the sequence gate by receipt, and probes the allocator read-only |
| `ccx.config.json` | The `sequences` key -- the only place a sequence is defined |
| `examples/sequence-adr/` | The worked configuration: a decision-record sequence, end to end |
| `examples/ledger_check.annotated.py` | The original gate this was distilled from, comments intact. **Not wired, not installed.** |
