# Playbook size and format

Keep playbooks within the shared context budget and preserve every rule's conditions. `git log -p
docs/PLAYBOOK-SIZE.md` records the measurements, sources, and limits behind these rules.

A published study found no effect of instruction-file length on adherence. This page claimed the
opposite until 2026-09-05.

The retraction stays prominent because the false claim supported these rules for weeks.

The study is arXiv 2605.10039 by McMillan, published 11 May 2026.

- 1,650 Claude Code sessions, four manipulated file-structure variables.
- From the abstract: *"Size and conflict nulls are supported by affirmative-null Bayes factors
  (BF10 between 0.05 and 0.10)."*
- That is evidence FOR the null on size, not a failure to reject.
- Its limits are real: one trivial compliance target, models a generation old, and no line range
  stated in the abstract.

Short files use less context. An instruction file loads in full and occupies the context window on
every request.

The vendor claims shorter files improve adherence, but attaches no experiment. The study's
affirmative null challenges that claim; context cost remains the supported reason to shorten files.

The study's largest effect concerned session length: compliance declined as the session continued.

- The abstract reports about 5.6 percent lower odds of compliance per generated function
  (OR = 0.944).
- The abstract calls it non-monotonic rather than a constant per-step effect, so it does not
  extrapolate. Forty functions does not mean halved.
- Exploratory: found during analysis, not pre-specified, and measured on one trivial annotation.
- Take the direction, not the dose. The lever is session length and re-anchoring, not file shape.

Keep the claims separate. Evidence against a length effect on adherence does not remove a product
limit on file size.

Claude Code warns when one loaded memory file exceeds about 5 percent of the context window in
characters. The threshold has a floor near 40,000.

On 2026-09-05, the MessageFoundry engine `CLAUDE.md` on `origin/main` had 59,648 characters. That
was 1.49x the floor.

Measure characters from the shared ref. Byte counts and stale checkouts give different answers.

- `wc -c` returns bytes and the threshold is stated in characters. That file carries 299 multi-byte
  characters, so the two answers differ.
- A stale worktree copy differed by a further 3,640.
- Both of my errors pushed the same way, and I published 1.41x before either was caught.
- Read the threshold out of the CLI binary rather than trusting this line.

## Cut a playbook by deleting, never by rewriting

Added 2026-09-05 after two rewrites lost conditions and inverted several playbook rules. Both turned
conditional requirements into absolutes.

Use this order when cutting a playbook:

1. Take out retraction history, subject to the keep-test below.
2. Collapse duplicate copies of a fact, keeping the one a cross-reference names.
3. Tighten table cells.
4. Leave prose alone.

Paragraphs hold exceptions, conditions, and expiry terms. Table conditions have their own cells,
which makes compression easier to check.

Before removing a retraction, search every other tracked document for the rejected claim. Keep the
retraction if another document still repeats it.

Also keep a retraction when a reader could independently reach the same wrong claim. It prevents the
next session from restoring the error.

Match every cut against its exact text and require exactly one match. Raise an error when nothing
matches; otherwise an unchanged file can look successfully edited.

Across the six live playbooks, the pass removed 64 of 8,698 lines. Those files were BUILDER, COMMON,
LANDER, STEWARD, CONSOLE, and MANAGER.

```
git stash list                                  # nothing of ours in flight
git diff --numstat -- roles/                    # the removed count, per file
git show HEAD:roles/BUILDER.md | wc -l          # 950 before, against 913 after
```

STEWARD, CONSOLE, and MANAGER had no removable material. Their retractions passed the keep-test, and
STEWARD's rule sheet counted them.

Check contradictions separately from length. Faithful compression preserves both sides of a
conflict.

## Split a playbook by when a rule fires, not by what it is about

Move branch-specific instructions out of the file loaded by every session. This rule was added
2026-09-05 after auditing the longest playbook section by section.

Classify each section by when it applies: every cycle, on a named branch, once per seat lifetime, or
never.

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

Assign every section to exactly one destination. The destination line counts must add up to the
original count.

A missing section then fails the sum, even if the shortened file reads well.

Check the mapping before writing files. Every destination needs an output file, or the split can
drop sections and leave partial results on disk.

A correct total can hide lines assigned to the wrong destination. Derive each destination's count
from the mapping; a wrong pair here once summed to the right total.

Keep prohibitions in the resident core. A task file may load only after the act it forbids.

LANDER.md records a session that read its grant on arrival, then asked the Owner twice for that same
grant. The grant was 1,970 lines earlier.

The session met a later, emphatic passage while already acting. That passage referred to itself and
displaced the earlier grant.

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

Keep durable rules in the playbook. Put current branches, pull requests, queue depth, session names,
and "pick up here" lists in dated episode notes.

When rules and live state mix, stale facts can remain trusted because the surrounding rules still
hold.

## This page

An earlier version ran to 1,766 words, including a literature review, corpus measurements, and a
proposed experiment. Git history preserves that background.
