# Playbook size and format

Rules for writing a seat playbook. The evidence for each rule is in the commit that introduced
it; `git log -p docs/PLAYBOOK-SIZE.md` carries the measurements, the sources and their limits.

**A published study varied instruction-file length and found no effect on adherence.** This page
claimed the opposite until 2026-09-05. The retraction sits here, not in a footnote, because the
false version ran for weeks and the claim was load-bearing.

arXiv 2605.10039, McMillan, 11 May 2026: 1,650 Claude Code sessions, four manipulated
file-structure variables. From the abstract: *"Size and conflict nulls are supported by
affirmative-null Bayes factors (BF10 between 0.05 and 0.10)."* Evidence FOR the null, not a failure
to reject. Its limits are real: one trivial compliance target, models a generation old, and no line
range stated in the abstract.

**So keep files short for CONTEXT BUDGET, not adherence.** The budget cost is mechanical and
documented; the file loads in full and occupies the window on every request. The adherence
justification is asserted by the vendor with no experiment attached, and now has an affirmative
null against it. Argue the rule on the ground that holds.

**The study's largest effect is not about files.** Each function an agent generates carries about
5.6 percent lower odds of compliance within that session (OR = 0.944). The abstract calls it
exploratory, found during analysis. If it holds, adherence decays with session progress, which
argues for shorter sessions, not shorter files.

**"No study" and "no figure" are different sentences. Do not collapse them.** One length figure
is product-enforced, and it is the only one here that is not a judgment: Claude Code warns when a
single loaded memory file passes about 5 percent of the context window in characters, with a floor
near 40,000. Measured 2026-09-05 on `origin/main`, the MessageFoundry engine `CLAUDE.md` is 59,648
characters, so it trips that floor at 1.49x today.

**Count characters, not bytes, and read the shared ref, not your checkout.** `wc -c` returns bytes
and the threshold is stated in characters; that file carries 299 multi-byte characters, so the two
answers differ. A stale worktree copy differed by another 3,640. Both of my errors pushed the same
way and I published 1.41x before either was caught. Read the threshold out of the CLI binary rather
than trusting this line.

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

## What these cost when broken

| Break | What happens |
| --- | --- |
| A rule left ungated | It decays. Measured: the same rule held at 0 violations gated and 93 ungated |
| A rule cited by position | A stale pointer costs more than no pointer |
| A second summary instead of a pointer | Two copies with no drift signal between them |
| A number without its command | It cannot be checked, so it is believed until it is wrong |
| A per-file size target | It cannot see a duplicate. Two identical 78-line files both load on this machine today |

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
