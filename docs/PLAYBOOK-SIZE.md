# Playbook size and format

Rules for writing a seat playbook. The evidence for each rule is in the commit that introduced
it; `git log -p docs/PLAYBOOK-SIZE.md` carries the measurements, the sources and their limits.

**No published study varies instruction-document length as an independent variable.** So the
length figures below are judgments, not measurements, and they are not the load-bearing part.
The rules that are measured are about gates and order.

**"No study" and "no figure" are different sentences. Do not collapse them.** One length figure
is product-enforced, and it is the only one here that is not a judgment: Claude Code warns when a
single loaded memory file passes about 5 percent of the context window in characters, with a floor
near 40,000. Measured 2026-09-05, the MessageFoundry engine `CLAUDE.md` is 56,307 characters, so it
trips that floor at 1.41x today. Verify it yourself with `wc -c`, and read the threshold out of the
CLI binary rather than trusting this line.

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
| Any length figure, here or anywhere | A judgment, except the one product-enforced threshold above |
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
