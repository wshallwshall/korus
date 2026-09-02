# KORUS Constitution

KORUS runs several AI coding sessions against one codebase. These are the rules a
session, a seat, a gate or a later spec may not break.

**Every article below traces to something measured.** The evidence is named inline so a
reader can check it instead of trusting it. An article with no evidence behind it does
not belong here, and adding one is an amendment rather than an edit.

## Core Principles

### I. No session is the only reader of its own work

Every piece of work has a second observer that did not produce it. Not a second pass by
the same session, and not a subagent that session briefed. A different session.

**Evidence.** On 2026-09-02, four substantive errors were made across two paired
sessions. All four were caught. **None was caught by its author.** Each was found by the
other session, and one by a worker whose report both sessions had overruled.

This is why the method has two long-lived seats rather than one. A single session with
better screens is not a substitute, because the errors it makes are the ones its screens
do not model.

### II. Publish readings, not conclusions

A session tells its peers what it ran and what came back: the command, the timestamp, the
ref, the raw output. Not what it concluded.

A peer who receives a conclusion can only agree or doubt. A peer who receives a reading
can run it.

**Evidence.** On 2026-09-02 a worker reported a refusal string verbatim, beside a
conclusion it had been handed. Two senior sessions agreed the conclusion was wrong. **The
string was right and both sessions were wrong.** It survived because its brief said "do
not paraphrase the refusal; quote it".

So quote refusals, errors and rulings **character for character**. A paraphrase changes
scope silently, and the changed version is what later work encodes.

### III. A gate records that someone looked, not that a step happened

A gate a party can satisfy without doing the work measures the wrong thing. So does one
that cannot see a careful party declining to pass something.

**Evidence.** On 2026-09-02 a pull request drew two reviews eight minutes apart. The
first found four defects and deliberately withheld its approval. The second found nothing
and applied the label, which enqueued the change. **The gate recorded the review that
found nothing**, because withholding a label is invisible to it: a reviewer that declines
to pass looks exactly like one that never ran.

Every gate needs a way to record refusal, and refusal must be as legible as approval.

### IV. Every claim names the condition it did not vary

Independence is relative to what was varied. Two observers who differ in everything they
thought to change, and match in something neither thought to change, produce corroboration
worth one observation.

**Evidence.** On 2026-09-02 two workers on different accounts, running different tasks,
each ran both arms of a controlled comparison and reported the same result. The conclusion
was wrong. Both were headless, and **a headless session cannot vary its own
headlessness**. The confound was invisible from inside, and no care by either worker could
have surfaced it. An observer in a different mode running the same command settled it in
minutes.

So a finding states what was held constant, not only what was changed. When two sessions
agree, the question is not what instrument they shared. It is **what is true of every run
either of them has ever made**.

### V. No rule may manufacture its own evidence

A rule that tells a session it cannot do something stops it trying. The absence of an
attempt then reads as confirmation.

**Evidence.** Two shipped files told every session it could not declare its own seat. It
could. Two workers on the same config root, 33 minutes apart, differed in what their brief
said, and only the one told it could, did. The other rendered undeclared, which is exactly
what the false rule predicted. **A rule that suppresses the action which would disprove it
generates its own supporting evidence.**

Before a rule forbids something, someone must have tried it and recorded what happened.

### VI. A number without its instrument is not a measurement

Report the command beside the count. Print the needle beside every zero. Run a control
that would fail if the search were broken.

**Evidence, repeatedly.** A zero from a hyphenated spelling, while the spaced spelling sat
in the same file. A count of 240 against a true 274, because two tools resolved one path
string to two different files with no error anywhere. A clean scanner result that was
really the exit code of the command it had been piped into. **A plausible result is not
evidence the instrument worked, and the plausible one gets checked least.**

### VII. Waiting is a design cost and it is measured

Seat lifetimes are chosen against measured spend, not preference.

**Evidence, this fleet.** A session actively working spends about 10,041 tokens a minute.
A three-minute heartbeat spends 2,108. A ten-minute sleep loop spends 22,275. **A session
that has ended spends nothing.**

This is why workers end rather than idle. It is also the cost a design must pay back when
it needs a worker to persist, and that trade is stated in the spec rather than assumed.

## What the record must contain

**Findings live where the work happens.** A finding filed against a published copy, in a
repository where nobody builds, is a finding nobody will act on.

**Numbers carry their date and their source.** A measurement without a date cannot be
told from one the code has since invalidated.

**Measured and asserted are marked apart.** This distinction is load-bearing, and it is
the first thing lost when a document is summarised.

**A retraction sits at the claim, not below it.** A correction posted after a wrong claim
never reaches the reader who lands on the claim.

**No glyphs or emoji anywhere.** A glyph's meaning is positional, and that is invisible to
anyone who learns it from examples rather than from a definition. Words carry their scope
in the sentence around them. Say the word.

## How a change lands

**One coherent change per commit**, with a message saying what was measured and what it
changes.

**Nothing merges on its author's own approval.** See Article III.

**A number is allocated before it is cited.** Never search for the next free identifier.
Two sessions that both search pick the same one, create differently named files, merge
cleanly, and corrupt the ledger with nothing reporting a problem.

**Never cite an identifier nobody has allocated.** While it is unissued the citation
resolves to nothing, which is honest. The day someone allocates it, that citation starts
resolving to unrelated work, and it reads as a working cross-reference forever.

**A gate is never bypassed.** If a gate is wrong, fix the gate in its own reviewed change,
and prove it still catches what it was built to catch before trusting it.

## Governance

This constitution supersedes other practice in this repository. Where a spec, a plan or a
playbook conflicts with it, the constitution wins and the other document is amended.

**Amendments require evidence.** An article is added, changed or removed by naming what
was measured and when. A principle that cannot be traced to a measurement is a preference,
and preferences belong in a style guide.

**Articles may be proven wrong.** Every article here rests on a small number of
observations, several from a single night of operation. When a later measurement
contradicts one, the article changes and the old text stays with the reason, because a
reader who remembers the old rule needs to see it named as retired rather than find it
silently absent.

**Version**: 1.0.0 | **Ratified**: 2026-09-02 | **Last Amended**: 2026-09-02
