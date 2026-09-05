---
name: "lander-pr-content-hazards"
description: "Check a pull request whose own content carries a hazard. Use when the diff touches an ADR, redacts a secret, is docs-only, or contains a glyph."
user-invocable: true
disable-model-invocation: false
---

# lander-pr-content-hazards

> Task rules for the Lander seat, split out of [LANDER.md](../../../roles/LANDER.md) on 2026-09-05.
> The prohibitions that bind before this task starts stay in that file. Read it first.

### 9a. A redaction commit republishes the token in its own diff

`git show <redaction commit>` contains the removed line verbatim. On a public repo, redacting a
not-yet-public token in an ordinary commit publishes the very thing it removes. **The fix and the
disclosure are the same object.**

| Item | Rule |
| --- | --- |
| Classify first, and record the classification | Not just the verdict. |
| The measured case | One redacted token was classified without echoing it. Shape, part count and length identified it as an auto-generated session name, not a customer or site token. |
| What that bought | It made publishing routine rather than an owner-level decision. |
| If the shape reads as a customer token | Push the redaction alone and hold the disclosure. |
| Do not widen the regex to close a leak-guard gap | A guard that fires on ordinary commit text gets allowlisted into uselessness, which is worse than the leak. |
| Instead | Measure the hit rate over the corpus and prefer narrowing by context. |

### 14c. A docs-only PR is the blind mode, not the cheap one

Doc-drift guards live in pytest gated on `code == 'true'`, and `.md` is in the noncode allowlist. So on
a docs-only PR the prose ratchet, banner hygiene and link checks are **skipped pre-merge and fire only
on the push to `main` afterwards**, misattributed to whoever opens the next code PR.

**The remedy is a list problem, not a habit problem.**

When this recurred 2026-08-11 on `test_dast_claims`, an ungated pre-merge doc-guard step **already
existed** in `ci.yml` with its own minimal `[dev]` install. It simply did not name the module.

The proof is an asymmetry that looks like luck until you see it. `test_link_resolution` **is** in that
list, so its failure was caught pre-merge on a PR. The DAST guard was not, so it reached `main`. **Same
blind mode, two outcomes, decided purely by list membership.** Fixing the lander's habit would have
left the hole open for the next person who lacked it.

| Rule | Detail |
| --- | --- |
| A curated allowlist silently omits | Nothing in a green run says *"a doc guard exists that I did not run."* Absence of a name produces no output at all. |
| So | State the rule at the list: a new doc-scanning module is added there in the same commit. |
| A defence implemented by duplication defeats itself | That step's list was written twice, once for the `printf` and once for `pytest`, so its own print-what-you-scanned defence could drift. |
| What drift would look like | Printing a module it did not run, or running one it did not print. One variable now feeds both. |
| A name that does not resolve must hard-fail | A path typo otherwise errors on an unknown file, or under a future `-k` or `--ignore` form silently scans nothing and reads as a pass. |

### 14g. Enforce the no-glyph rule with the cp1252 test, and the test narrows the rule

Three characters were flagged in a peer's diff as violations of CLAUDE.md's *no glyphs or emoji* rule. The peer fixed one
and refused two, applying the encodability test the flagger had themselves cited. Re-measured:

```
U+21D2 double arrow   RAISES UnicodeEncodeError   <- a real defect
U+2192 arrow          RAISES UnicodeEncodeError   <- a real defect
U+2014 em dash        encodes to 0x97             <- safe
U+00A7 section sign   encodes to 0xA7             <- safe
U+2026 ellipsis       encodes to 0x85             <- safe
```

**The test condemned exactly one of the three.** That rule's subject is glyphs and emoji. An em dash
is punctuation, and the rule's own text uses section markers throughout.

Stripping the two safe ones from a diff's added lines would also have left **127 em dashes elsewhere
in the same file** untouched: a change no terminal can observe, bought with internal inconsistency.

The same scan then found **three pre-existing U+2192 already on `main`** in that file, invisible to a
rule enforced by reading. **Three independent instances in one week across three authors** says the
character is reachable by habit, and that the fix is a check rather than more care. **A test gives the
same answer to everyone who runs it; "does this look like a glyph" does not.**
