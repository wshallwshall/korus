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

### VIII. The account roster is assigned by the Owner, and no design may infer it

KORUS runs across several accounts. **Which accounts are in play is the Owner's
assignment**, not a fact about the machine. The number changes as accounts are added or
retired. Nothing may hard-code it, and nothing may infer it by looking at what happens to
be on disk.

This is the same rule that stops a hook inventing a session's goal. **A roster is intent.**
A machine that derives one from the filesystem produces something that looks authoritative
and says nothing about what the Owner wants used: it will happily enlist a config root that
exists but is not meant to be spent, or one that shares an account with another.

Reading the roots is still worth doing, as an **instrument that checks the roster rather
than replacing it**. It answers whether an assigned account can start a session, and
whether two roots resolve to one account. When a reading and the assignment disagree, the
assignment is what the fleet is for and the reading is what the machine currently is. Both
matter, and neither is the other.

A seat's account decides its quota, which tools it may run, and **which other seats it can
reach**. So no design may treat seats as interchangeable processes on one machine.

**This is the article that forecloses the most.** The realtime session-to-session channel
is **account-local**: two seats on different accounts cannot use it at all. Published
descriptions of similar multi-agent setups have their agents communicate directly through
that channel, which works only because every agent shares one account. **That topology is
not available here.** A design copied from it will appear to work in testing on one account
and fail silently across several.

What is available is a shared file store, which is account-agnostic because it is a
filesystem. It is asynchronous. **So any design requiring synchronous coordination between
seats on different accounts is invalid**, and one needing low latency must state its
polling cost against Article VII.

Three structural facts, each of which outlives whatever the current count is:

- **Config roots do not map one-to-one to accounts.** More than one root can resolve to the
  same account, including the default root, so a session that sets nothing may draw on
  another root's quota. **A fleet that routes by root believing it routes by account will
  overload an account and never see it.** The map must be read at run time.
- **The right to spawn is per-root and is read on the parent**, not the child. One granted
  root can launch workers onto any account. It also means a fleet with a single granted
  root **cannot have two leads restart each other**, which any mutual-accountability design
  under Article I must solve rather than assume.
- **Remaining quota is not readable on every root.** Work cannot be routed by headroom
  until it is, and a design that assumes headroom is visible is assuming an instrument that
  may not exist.

### IX. Built for Claude Code, and no design may require a particular surface

KORUS is built for **Claude Code**. It is not agent-agnostic and does not need to be. A
design may depend on Claude Code's own mechanics: its hooks, its skills, its settings
files, its permission model, its tools.

Claude Code runs on more than one surface. **The desktop application is the preferred seat
for the Owner**, because that is where a person can watch work and interrupt it. That is a
preference, not a requirement. **The command line is legitimate wherever it is the better
tool, including as the Owner's own front end.** No design, seat definition or gate may
require a particular surface, and none may assume the Owner is on one.

**But the surfaces are not equivalent, and a capability measured on one does not transfer
to another.** This is Article IV applied to a standing condition rather than to a single
finding, and it has already cost real work.

**Evidence.** Three differences, each of a different kind:

- **What a session can see.** The desktop application's session tooling enumerates an
  in-memory map of sessions **the desktop app itself spawned**, so a session started any
  other way "is never entered into it -- not filtered, never registered -- and cannot be
  listed or messaged by it". A design that reaches peers through that channel silently
  loses every peer it did not spawn.
- **What a session can do.** A desktop session cannot directly start another session.
  A command-line session can. So the seat that spawns workers is constrained by its
  surface, not only by its permissions.
- **How a tool behaves.** On 2026-09-02 an identical command, on one account, in one
  session, succeeded through a tool interactively and was refused headlessly. **The
  refusal named a cause that was not the real one**, and two sessions built a wrong
  mechanism on it before an observer on the other surface settled it in one command.

So a finding states the surface it was measured on, and a claim measured on one surface is
not carried to another without re-measuring. Article IV already requires this; it is stated
again here because the surface is the condition observers are least likely to think of
varying, for the same reason Article IV gives: it is usually the only one they have.

## The execution environment

These are conditions, not principles, and **every number here is a reading with a date**.
They bound every spec, and a spec written without them will be wrong in ways that appear
only at scale.

**Read on 2026-09-02, and expected to change.** Six config roots resolved to five distinct
accounts, with two roots sharing one, and one of those two was the default root. All six
started a session. Cross-account messaging is a shared file store: reading a box directly
took about 46 milliseconds, against about 17.5 seconds through the documented listing
command, which also returns every box on the machine.

**That is a reading of the machine, and it is not the roster.** The Owner assigns which
accounts are in play. The reading is useful only as a check against that assignment, and
the two disagreeing is a finding rather than an error. Re-read it; do not cite it.

**Not established.** Whether the account boundary affects anything beyond messaging, quota
and grants. Whether the shared file store sustains a correction loop at the pace Article I
needs: the result in Article I was measured on the **account-local realtime channel**, and
that channel does not exist between accounts. **Carrying that result across the channel
change would be exactly the substitution Article IV forbids.** Testing it is the first
thing any multi-account design must do.

**One project, not many.** Every seat works on one codebase, so seats converge on one merge
point. Adding accounts adds capacity that this convergence may not let the system spend.
That is a hypothesis from a single evening, not a measurement, and it is written here so a
later spec tests it rather than inherits it.

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

**Version**: 1.3.0 | **Ratified**: 2026-09-02 | **Last Amended**: 2026-09-02

<!--
Amendment log. Kept because Governance requires retired text to stay with its reason.

1.3.0  2026-09-02  Added Article IX: built for Claude Code, no design may require a
       particular surface, and a capability measured on one surface does not transfer.
       The desktop app is the preferred Owner seat; the CLI is legitimate anywhere,
       including as the Owner's front end. NOTE: the adversarial review commissioned on
       this document was launched against 1.2.0, so Article IX may be unreviewed.

1.2.0  2026-09-02  Article VIII: the roster is ASSIGNED BY THE OWNER, not discovered.
       The 1.1.0 text said the topology is "read, never assumed", which made the
       filesystem the source of truth. It is not. Which accounts are in play is intent,
       and a machine that derives intent from disk will enlist a root that exists but is
       not meant to be spent. Reading roots is retained as an instrument that CHECKS the
       roster rather than replacing it. Same rule that stops a hook inventing a goal.

1.1.0  2026-09-02  Added Article VIII and the execution-environment section.
       An earlier draft of VIII stated the account and root counts as properties of the
       fleet. They are readings that change as accounts are added or retired, and writing
       a reading as a property is the error Article VI exists to prevent. Rewritten so the
       article carries the structural facts, which outlive any count, and the numbers sit
       in the environment section with their date and an instruction to re-read them.
-->

