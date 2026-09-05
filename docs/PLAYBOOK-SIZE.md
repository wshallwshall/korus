# Playbook size and format

Rules for writing a seat playbook. The evidence for each rule is in the commit that introduced
it; `git log -p docs/PLAYBOOK-SIZE.md` carries the measurements, the sources and their limits.

**A published study varied instruction-file length and found no effect on adherence.** This page
claimed the opposite until 2026-09-05. The retraction sits here, not in a footnote, because the
false version ran for weeks and the claim was load-bearing.

The study is arXiv 2605.10039, McMillan, 11 May 2026.

- 1,650 Claude Code sessions, four manipulated file-structure variables.
- From the abstract: *"Size and conflict nulls are supported by affirmative-null Bayes factors
  (BF10 between 0.05 and 0.10)."*
- That is evidence FOR the null on size, not a failure to reject.
- Its limits are real: one trivial compliance target, models a generation old, and no line range
  stated in the abstract.

**Keep files short for CONTEXT BUDGET, not for adherence.** The budget cost is mechanical and
documented: the file loads in full and occupies the window on every request.

The adherence claim is a different kind of thing. The vendor asserts it on several of its own
pages with no experiment attached, and it now has an affirmative null standing against it. Argue
the rule on the ground that holds.

**The study's largest effect is not about files at all.** Compliance degrades as a session runs on.

- The abstract reports about 5.6 percent lower odds of compliance per generated function
  (OR = 0.944).
- The abstract calls it non-monotonic rather than a constant per-step effect, so it does not
  extrapolate. Forty functions does not mean halved.
- Exploratory: found during analysis, not pre-specified, and measured on one trivial annotation.
- Take the direction, not the dose. The lever is session length and re-anchoring, not file shape.

**"No study" and "no figure" are different sentences. Do not collapse them.** A null on adherence
does not mean no length figure binds you.

One figure is product-enforced and is the only one here that is not a judgment. Claude Code warns
when a single loaded memory file passes about 5 percent of the context window in characters, with
a floor near 40,000.

Measured 2026-09-05 on `origin/main`, the MessageFoundry engine `CLAUDE.md` is 59,648 characters,
so it trips that floor at 1.49x today.

**Count characters, not bytes, and read the shared ref, not your checkout.**

- `wc -c` returns bytes and the threshold is stated in characters. That file carries 299 multi-byte
  characters, so the two answers differ.
- A stale worktree copy differed by a further 3,640.
- Both of my errors pushed the same way, and I published 1.41x before either was caught.
- Read the threshold out of the CLI binary rather than trusting this line.

## Cut a playbook by deleting, never by rewriting

**A rewrite loses conditions. A deletion cannot.** Added 2026-09-05, after two rewrites of one
playbook flattened conditional rules into absolutes and inverted several of them.

The transform that is safe to run over a playbook has four steps, in this order.

1. Take out retraction history, subject to the keep-test below.
2. Collapse duplicate copies of a fact, keeping the one a cross-reference names.
3. Tighten table cells.
4. Leave prose alone.

**Prose is where the conditions live.** A rule with an exception, a discriminator or an expiry
states it in a paragraph. A table row carries its condition in a column and survives compression.
A paragraph does not.

**Test a retraction against the corpus before you remove it.** Grep every other tracked document
for the retracted claim. A hit means the retraction is the thing refuting it, so it stays.

Keep it too when it names a wrong claim a reader could reach on their own. That is the purpose the
rule gives it: delete the error and the next session re-derives it.

**Assert every cut against its exact text, and require exactly one match.** A cut that finds
nothing must raise. Otherwise a no-op edit and a real one produce the same clean run.

**The yield is small, and that is the finding.** Measured across the six live playbooks --
BUILDER, COMMON, LANDER, STEWARD, CONSOLE and MANAGER -- it removed 64 lines of 8,698.

```
git stash list                                  # nothing of ours in flight
git diff --numstat -- roles/                    # the removed count, per file
git show HEAD:roles/BUILDER.md | wc -l          # 950 before, against 913 after
```

STEWARD, CONSOLE and MANAGER yielded nothing. Their retractions all pass the keep-test, and
STEWARD's own rule sheet counts them, so removing one would falsify that row.

**Length and contradiction are different defects.** Contradictions survive a faithful compression,
because both halves compress equally well. Cutting length does not fix them.

## Split a playbook by when a rule fires, not by what it is about

**A rule that fires on one branch of the work does not belong in the file that loads every
session.** Added 2026-09-05, from a section-by-section audit of the longest playbook here.

Classify every section by when it fires: every cycle, on a named branch, once per seat lifetime,
or never. Then place it.

- Every-cycle and lifetime rules stay resident.
- Branch rules move to a task file, loaded at the trigger the core names.
- Never-fires and another seat's rules leave the playbook.

Measured over `roles/LANDER.md`, 2,983 lines in 144 sections:

```
grep -cE '^#{2,4} ' roles/LANDER.md      # the section count
wc -l roles/LANDER.md                    # the line count the split must sum back to
```

| Destination | Sections | Lines |
| --- | --- | --- |
| Resident core | 46 | 1,019 |
| Eight task files: red check, conflict, ledger, handover, instrument, relay, PR content, empty queue | 74 | 1,528 |
| Another seat: steward, cleanup, owner, gate builder | 24 | 436 |

**The acceptance check is arithmetic.** Every section lands in exactly one destination, and the
destinations sum back to the original line count.

A section that goes missing then shows up as a failed sum, rather than as a file that still reads
well without it.

**Run that check before you write a single file.** A destination you mapped but gave no output
file drops its sections silently, and a run that fails after writing leaves half a split on disk.

**The sum catches a loss, never a misattribution.** Moving lines between two destinations leaves
the total unchanged, so derive each destination's count from the mapping rather than typing it.
Measured here: a wrong pair of figures summed to the right total and read as correct.

**A prohibition stays resident whatever else moves.** A task file loads when the task starts, which
is after the act it forbids.

**The failure this fixes is recorded in the file itself.** LANDER.md describes a lander that read
its grant on arrival, met a later passage while already acting, and asked the owner twice for a
grant written 1,970 lines earlier.

It names the mechanism too: the later passage is emphatic, self-referential, and encountered while
already acting.

## The rules

| Item | Rule |
| --- | --- |
| Anything that has to hold | Gate it. A playbook sentence is not a control |
| What the playbook carries | What a gate cannot check, plus the reason behind each rule |
| The budget | The sum in context: playbook, shared rules, `CLAUDE.md`, the task. Not the file |
| Ordering | By consequence of failure. The front and the end hold; the middle does not |
| Cross-references | By name. Never by section number, position, or line |
| Repeating a rule across playbooks | A pointer, never a second summary |
| Every number in a playbook | The command beside it, and the condition you did not vary |
| Any length figure, here or anywhere | A judgment, except the one product-enforced threshold above. No length figure has adherence evidence behind it |
| Moving a rule out to load lazily | Fine for reference. Never for a "never do X" rule, which must stay resident |
| A rule you cannot gate and cannot explain | Delete it |
| Debt you import | Record it in the ratchet. Never hide it behind an exemption |
| Shortening a playbook | Delete whole sentences, rows and paragraphs. Never reword one |
| A rule with a condition | Never flattened to an absolute, whatever it costs in length |
| A retraction | Out, unless another document still carries the claim, or a reader could reach it alone |
| Every cut you make | Matched against its exact text, and required to match exactly once |
| A cross-referenced section | Not the copy you delete when collapsing a duplicate |
| Where a rule lives | Decided by when it fires, never by what it is about |
| A rule that fires on one branch | A task file, loaded at a trigger the resident core names |
| A prohibition | Resident, whatever else moves out |
| A rule another seat owns | That seat's playbook, not this one |

## What these cost when broken

| Break | What happens |
| --- | --- |
| A rule left ungated | It decays. Measured: the same rule held at 0 violations gated and 93 ungated |
| A rule cited by position | A stale pointer costs more than no pointer |
| A second summary instead of a pointer | Two copies with no drift signal between them |
| A number without its command | It cannot be checked, so it is believed until it is wrong |
| A per-file size target | It cannot see a duplicate. Two identical 78-line files both load on this machine today |
| A condition dropped from a rule | The absolute that remains licenses the act the rule forbids |
| A rule reworded rather than deleted | The lost clause reads as a changed line, not as a missing one |
| A cut that matched nothing | It reads as a clean run, so the edit is believed to have happened |
| A retraction removed while another document carries the claim | The wrong version stands unopposed |
| A branch rule left resident | Every session pays for it and most never reach it |
| A task file no trigger names | It loads by luck, and nothing reports the run where it did not |

## Where the durable line sits

A playbook holds what never expires. Live state -- current branches, open pull requests, queue
depth, session names, "pick up here" lists -- goes in a dated episode note.

A document that mixes the two decays into a trusted document that is wrong, and the half that
stayed right hides it.

## This page

It is a rules page on purpose. An earlier version carried the literature review, the corpus
measurements and a proposed experiment, and ran to 1,766 words: a document about documents being
too long, made mostly of background. That version is in the history, which is where the evidence
belongs.
