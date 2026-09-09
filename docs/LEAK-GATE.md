# The leak gate

<a id="tldrbluf"></a>

`scripts/security/scan_forbidden.py` checks tracked text for home paths, real IP addresses,
credentials, and private names. It exits non-zero when it finds a forbidden string.

A repository can expose an account name, host, or client without leaking a secret. These strings
need checks beyond a conventional secret scanner.

Copy the script into your repository and put `python` on `PATH`. No installer copies or wires it.

[Scripts](SCRIPTS.md) gives its path; [Limits and requirements](LIMITS.md) covers the interpreter.

[What it catches](#what-it-catches) separates built-in patterns from the private-name list you supply. Their limits differ.

---

When private work becomes public, ordinary text can disclose its origin:

- the absolute path some traceback printed;
- the address of a box someone pasted out of a terminal;
- a token prefix in a config example;
- the name of the client the work was actually for.

These strings can pass syntax checks, tests, and secret scans. Without a separate check, a reader
may find them only after publication.

The scanner uses Python's standard library with no project import. Its exit codes let it run in a
git hook without a virtual environment, or in continuous integration (CI).

A bare clone has no working tree. The no-argument scan therefore reads zero files and exits `2`;
supply filenames or use `--path` with a directory.

---

## What it catches

Built-in detectors recognize string shapes. They need no private-name list, so they work in fresh
forks, contributor clones, and CI without secrets.

The IP detector skips lockfiles, where dotted numbers usually name versions. Other detectors still
scan those files.

| Class | What it is |
|---|---|
| Absolute user-home path | `<drive>:\Users\<account>\...` in **any case** (Windows compares paths that way), `/home/` and `/Users/` case-sensitively. Carries an OS login, usually a real person's name, often the internal project name below it. Exempt: placeholders (`<name>`, `$HOME`, `%USERPROFILE%`, `{home}`) and conventional stand-ins. |
| Routable IPv4 | A free-standing quad that is not RFC1918, loopback, link-local, broadcast, `0.`-prefixed, multicast, or an RFC5737 documentation address. Naming a real host is a network disclosure, even a jump box. Look-arounds keep dotted OIDs, version strings and spec-section citations out. |
| Credential shapes | Private-key block headers, and prefix-anchored token formats. It prints `private key block`, `cloud access key id`, `forge access token`, `chat platform token` and `model API key`. Prefix-anchored because an entropy heuristic over source produces a false-positive storm, and a muted gate is worth nothing. Run a real secret scanner too: this catches only copy-paste leaks riding with identifying content. |
| Private artifact URL | All three addresses one artifact has: `claude.ai/artifact/<uuid>` and `claude.ai/code/artifact/<uuid>`; the same with `frame` in place of `artifact`; an optional readable slug before the UUID, as in `claude.ai/code/artifact/q4-plan-<uuid>`; and the content host `<uuid>.frame.claudeusercontent.com`, plus its `.staging.` variant, where `claude.ai` never appears. The UUID is a *capability*, not a name: whoever holds the URL can fetch the artifact. The UUID shape is required, so the placeholder forms this row prints do not trip the detector that documents them, and a deliberately shared `/public/artifacts/` link does not either -- that segment is plural. Also caught when prose reflow breaks the URL across two lines, reported at the first line. Prints bare, like a credential hit. |

Supply private project, client, vendor, host, and person names in your own token file. Never commit
that file to the public repository.

Home-path matching requires an account name that starts with an ASCII letter. Names beginning with a
digit, `_`, or a non-ASCII character silently escape every detector.

The detector deliberately misses lowercase `/users/<name>/Library`, which resembles a more common
REST route. Windows drive paths ignore case; `/home/` and `/Users/` do not.

This behavior was measured 2026-09-05.

On 2026-09-05, the detector caught a one-line artifact URL but missed its wrapped form. These pages
wrap near 100 characters, shorter than the URL.

The artifact detector now also checks URLs split across two lines.

It joins adjacent lines and removes whitespace at the join. The report names the first line and adds
`wrapped`, since that line alone contains no full URL.

Tests pin two remaining limits:

- A wrap across three lines is still missed. Only adjacent pairs are joined.
- A prefixed continuation line is still missed -- `# `, `> `, `* `. The join strips whitespace
  and nothing else. Stripping comment markers would fabricate adjacency a reader does not see.

Joining can also create a false match: a path-ending line followed by an unrelated UUID. On
2026-09-05, table rows, lists, quoted code, and blockquotes stayed quiet because punctuation
survived the join.

The false match has the same shape as a real wrap. Review allowlist responses closely: one allowlist
line suppresses every detector on that line.

Other detectors still check one line at a time. Wrapped home paths and credentials remain silent
misses.

The change covered only artifact URLs because the broader pattern matched zero tree lines. Home-path
matching already fires in real use.

Commit `a3df144` published two private artifact URLs at `roles/LANDER.md:4027` and
`roles/retired/PM.md:200`. The gate scanned both and exited `0` because it had no matching pattern.

A reader found them, and PR #48 removed them.

The detector now covers that gap. `tests/test_the_leak_gate_can_see_every_class_it_claims.py` plants
a violation for every detector to prove it is active.

The first pattern matched only one of the artifact's three addresses. The vendor client confirmed
the other forms, including the address bar's slug form and a content host without `claude.ai`.

The pattern also controls whether `--show-context` can print a line. An overly broad pattern can
silently suppress useful context.

After widening, the measured pattern matched zero lines in the tree.

The removed URLs remain reachable through `a3df144`, beyond any working-file scan. See [the ref store](#what-this-gate-never-looks-at-the-ref-store).

Rotating the artifact revokes access. Rewriting history costs more and does not revoke the
capability.

The gate deliberately has no bare-UUID detector. A UUID alone names no host, account, or project;
the surrounding URL makes it an address that can disclose content.

A bare-UUID detector would have matched zero times in CI's scan scope on 2026-09-05. That says
nothing about UUIDs as a class.

This project uses them for session ids. A false-positive allowlist entry would silence every
detector on the same line.

The scanner skips ten directory names even when git tracks their contents: `.git`, `.venv`, `venv`,
`node_modules`, `__pycache__`, `.mypy_cache`, `.ruff_cache`, `.pytest_cache`, `build`, and `dist`.

Tracked build output under those directories goes unscanned. The whole-tree report does not name
that exclusion.

Home-path matches are the class observed in practice in a repository like this one.

---

## Running it

```bash
python scripts/security/scan_forbidden.py                 # every git-tracked file
python scripts/security/scan_forbidden.py FILE [FILE ...] # named files (how a hook invokes it)
python scripts/security/scan_forbidden.py --path DIR      # everything under DIR; repeatable
python scripts/security/scan_forbidden.py --show-context   # also print the matched value
```

Run from the repository root. No-argument mode uses `git ls-files`; from a subdirectory, it scans
only that subtree and can exit `0`.

Use the exit code to determine the result:

- `0` -- clean.
- `1` -- forbidden content found.
- `2` -- usage error, nothing scanned, or a **fail-closed refusal**: the scanner declining to
  certify a run it could not trust.

Use `--show-context` only for local investigation. Printing a tracked disclosure into a CI log
publishes another copy; default output shows only location and category.

Home paths, credentials, and artifact URLs never print their matched values, regardless of flags.
Those values disclose the account, credential, or artifact itself.

Context suppression applies to the whole line. Until 2026-09-05, an IP match could print a home
path, artifact URL, or credential found by another detector on that line.

`AHomePathHitNeverEchoesTheAccountName` and `NoHitEchoesALineThatCarriesADisclosure` test that
behavior. The second catches leaks through neighboring hits that the first test cannot see.

Never use `--show-context` in CI. It still prints matched IP addresses and configured tokens in
full.

### Three behaviors worth knowing, because each one is a way a scanner lies

1. A run that examines zero files exits `2`. This covers non-repositories, empty checkouts, and paths entirely excluded by skip rules.

A subdirectory within a repository is different: git lists a real subset there. The scanner checks
that subset and may exit `0`.

2. Each `--path` accepts a file or directory and can be repeated. An argument yielding zero files is named with its reason and forces exit `2`, even if other arguments scan successfully.

The earlier version silently dropped file arguments unless it dropped everything.

3. Every run that reaches scanning prints its loaded detectors and scanned scope to stderr, on pass or failure:

<!-- no-copy -->
```
ccx leak gate: loaded structural=9, names=0, literals=0, allowlist=1  [STRUCTURAL-ONLY: ...]
ccx leak gate: scanned 412 file(s)  [STRUCTURAL-ONLY: ...]
```

Check the counts. `STRUCTURAL-ONLY` means no token file loaded, leaving only shape detectors active.

The marker appears on both lines so either line shows the limited scope.

A token refusal prints `loaded` and the refusal, with no `scanned` line. A usage error prints
neither; the missing line tells you scanning did not start.

4. `scanned` counts files attempted, not files fully read. A NUL byte in the first 4KB marks a file as binary, and an operating-system open failure also skips it.

Both still count, without a notice.

UTF-16 contains NUL bytes, so PowerShell 5.1 redirection can create text the scanner silently skips.
The same leak returns `1` in UTF-8 and `0` in UTF-16.

Convert captured output to UTF-8 before committing it.

---

## Wiring it as a pre-commit hook

A pre-commit hook can catch forbidden text before a commit leaves your machine.

Installers never write `.git/hooks/pre-commit`. [Hooks](HOOKS.md) owns this rule, and
`tests/test_installers_never_write_pre_commit.py` checks it.

One framework renamed a foreign hook and inserted a shim. That blocked every commit in a Windows
repository until the shim was removed.

Complete [Supplying a token file](#supplying-a-token-file) first. The recipe uses `--require-tokens`, so absent tokens cause exit `2` and
refuse every commit.

Wire the hook yourself. The `pre-commit` framework passes staged filenames as arguments:

```yaml
- repo: local
  hooks:
    - id: leak-gate
      name: leak gate
      entry: python scripts/security/scan_forbidden.py --require-tokens
      language: system
      pass_filenames: true
```

For a hand-installed hook, pass staged names as arguments too. Preserve these two limits:

- `--require-tokens`. The framework passes *args* to a hook but usually cannot set *env*, so
  only the flag makes the commit gate fail closed. Without it, a fresh clone or worktree has no
  token file -- it is gitignored -- so every commit runs with zero token detectors and reports
  success.
- It is a guardrail against accident, not a security boundary. `git commit --no-verify` bypasses
  it. Back it with a CI run over the whole tracked tree if you need the stronger claim. That run is
  also the one that catches what was committed before the hook existed.

The hook refuses forbidden strings and reports their file and category. A clean commit prints
`loaded` and `scanned`, then proceeds.

If every commit reports `no token source is configured`, supply the token file. Keep
`--require-tokens` enabled.

---

## Supplying a token file

Load private names without adding the list to git.

Choose a token source. The first takes precedence:

1. `CCX_FORBIDDEN_TOKENS` -- either a path to a token file *or* the file's content inline,
   newline-separated. This is how CI supplies it, from a secret.
2. `scripts/security/scan-tokens.local.txt` -- a local file beside the script. The repo's
   `*.local.*` ignore rule already covers it, so it cannot be committed by accident. Check that rule
   before you create the file, not after.

Use the sectioned format below. Blank lines and lines starting with `#` are ignored.

Trailing `#` comments become part of an entry. They count toward the detector floor but may never
match, so put comments on separate lines above entries.

```
[names]
REGEX | REASON | CASE
[literals]
one-substring-per-line
```

In `[names]`, REASON defaults to "private token". CASE is `i` by default or `s`; space-pipe-space
separates fields, leaving regex alternation such as `a|b` usable.

`[literals]` matches case-insensitively at non-letter boundaries. It catches `sync_token_export`,
where a `\b` boundary would fail because `_` counts as a word character.

After loading tokens, `loaded=` drops `STRUCTURAL-ONLY` and `names=` and `literals=` become
non-zero. Compare these counts with your file.

A partly loaded token source can pass a presence check and suppress `STRUCTURAL-ONLY`. Check
completeness as well as presence.

`--require-tokens` requires every section to contain entries. Set a floor with `--require-tokens=N`,
`CCX_MIN_DETECTORS=N`, or `names=7,literals=13` to catch entries lost within sections.

Per-section floors catch more loss than a total `N`. Growth in one section cannot conceal a
shrinking second section.

Set expected counts outside the token file. Damage to that file could also damage any count stored
within it.

For the same reason, the parser:

- refuses an entry containing an invisible codepoint (a zero-width space pasted through a rendering
  surface parses fine, counts toward the floor, and never matches);
- strips a BOM ahead of the first section header;
- names an unknown header instead of dropping its entries in silence;
- never echoes a token in a warning, because the warning lands in a public log.

### The allowlist

`scripts/security/scan-allowlist.txt` holds one line regex per false positive. It vetoes a line
before any detector runs, so an overly broad entry can disable scanning while counts look healthy.

The loader tests entries against five fixed canary strings. It rejects a bare `.*`, causing the
`allowlist=` count to drop.

A pattern can pass the canaries and still suppress a whole class. Matching `Users` does this
silently without changing the count.

Never allowlist a real path, host, or name.

---

## The caveat that matters most

Without a token source, the scanner reports `STRUCTURAL-ONLY`. Shape detectors run, but private-name
detectors have no entries.

This still catches home paths, the class observed in practice. It gives narrower evidence than a run
with private-name detectors, which is why `--require-tokens` exists.

Use a planted violation to establish each detector's coverage:

> **A green gate is evidence only if you have proved it can SEE that class.**

Prove the scanner fails on a known violation before trusting a clean run.

After changing detectors, allowlists, or invocation, put a known forbidden string in an external
scratch file. Scan it, then delete the scratch file.

Read `scripts/security/scan-allowlist.txt` before choosing the string. Pick an account name it does
not cover, or the allowlist can make a working detector appear broken.

Require exit `1` and the filename. A disabled detector, skipped directory, or uncompiled regex can
otherwise make a broken scan look clean.

[Tips and tricks](TIPS-AND-TRICKS.md) explains two fixture-checking traps:

- Capture the exit code without a pipe. `$?` after a pipeline reports the *last* command, not
  the scanner. In PowerShell, `$?` and `$LASTEXITCODE` answer different questions, and
  `$LASTEXITCODE` is only set by native commands. Redirect to a file and check the code separately.
- Read the planted fixture back before trusting it. `printf` interprets `\U`, `\n` and `\t`, so
  a Windows path written that way is not the string you meant. The violation the scanner then
  "failed to find" never existed. Use a quoted heredoc, then `cat` the file and look at it.

---

## What this gate never looks at: The ref store

The gate scans working files. Private history can remain elsewhere in a clone beyond its reach.

`git fetch <url> <refspec>` fetches directly from a URL. It stores objects without creating a named
remote.

A destination refspec also writes remote-tracking-style refs. A bare branch name writes only
`FETCH_HEAD`, outside `refs/`.

Common checks can therefore miss fetched private history:

- `git remote -v` lists nothing unexpected. There is no remote to list.
- `git remote remove <name>` fails with `No such remote`, so the obvious cleanup does not apply --
  and reads as "there was nothing to clean".
- `git for-each-ref` lists nothing either, after a bare-refspec fetch. There is no ref to list, and
  the objects are still there and still readable.
- The refs, and every object they make reachable, stay in the clone indefinitely.

A local clone of a public repository can hold private history without an unexpected named remote.

Check `git for-each-ref`, `git fsck --dangling`, and `.git/FETCH_HEAD`. Remote listings and ref
listings alone miss objects fetched with a bare refspec.

### If you find refs that should not be there

Keep local recovery and remote exposure separate:

| Question | Scope | What answers it |
|---|---|---|
| **Recoverability** -- can the local refs be restored? | Local | The reflog, dangling objects, a backup of the clone |
| **Exposure** -- did any of it ever reach a remote? | Remote | An audit against the remote, before or after any local cleanup |

Only the exposure question establishes disclosure. Deleting local refs does not change whether
content reached a remote.

Walk ancestry from every remote head, tag, and pull-request ref. Checking tips misses commits
retained as ancestors.

Look for forbidden paths or content as well as commit hashes.

Report coverage precisely: *at least N of M refs are clean, the remaining K are unaudited, not
proven clean*.

Missing objects can leave refs unaudited. Fetching them would write into the object store being
investigated.

---

## The permanent blind spot

A scanner cannot decide whether a disclosure is appropriate. [Tips and tricks](TIPS-AND-TRICKS.md) describes the human review
this needs.

Ordinary prose can expose private information without matching a forbidden string. All these
examples can pass the gate:

- a design note that describes an internal system in enough detail to attack it;
- a case study whose specifics identify the organization it happened at;
- a benchmark number that fingerprints a host;
- a lesson that cannot be told without shipping the recipe for bypassing a control.

Have someone who knows the disclosure limits read the whole diff. The scanner removes mechanical
work from that review; a clean run cannot authorize publication.
