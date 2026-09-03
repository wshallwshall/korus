# Feature Specification: The Worker Brief

**Feature**: 001-worker-brief
**Status**: Draft
**Created**: 2026-09-03

## What this is

A **brief** is the complete, single-turn instruction set a Console hands a worker that cannot ask a
question. It guarantees the worker can finish one turn without guessing, without waiting, and
without discovering anything load-bearing the brief did not already state and date.

This specification is written against **eight briefs that have actually been used**: five Builder,
three Reviewer, 869 lines, 49,366 bytes. Every count below is over that same explicit eight-file
list. Where a count is stated as "N of 8" it was measured, not estimated.

**Why this feature first.** On 2026-09-02 four distinct failures traced to brief defects, while the
next candidate feature blocked nothing all night. The brief is where every constitutional article
reaches the thing doing the work. Get it wrong and all eleven articles are decoration, which is
what happened, four times, to articles that already existed.

## User Scenarios and Testing *(mandatory)*

### User Story 1 - A Console dispatches work it cannot supervise (Priority: P1)

A Console has an item to build. It writes a brief and spawns a worker on whichever account has
headroom. The worker gets one turn. The Console cannot answer a question, cannot correct a
misunderstanding, and will not see the work until a pull request appears.

**Why this priority**: this is the whole feature. Every other story is a special case of it.

**Acceptance**: given a brief conforming to this spec, a worker completes the turn, or stops and
writes a question, and does neither of the two failure modes: guessing at an unstated fact, or
waiting for a reply that cannot come.

### User Story 2 - A worker meets a fact the brief got wrong (Priority: P1)

The brief asserts something the worker discovers is false: a command that works where the brief
said it would be refused, a refusal whose text names a different cause than the brief predicted.

**Why this priority**: equal to story 1, because it is the failure that actually occurred. Seven of
eight briefs assert an incapability that is false, and none names an attempt behind it.

**Acceptance**: the worker reports the refusal or result **verbatim** and does not adopt the
brief's explanation for it. A conclusion the Console handed down is marked as a reading with an
owner, and the brief states what the worker does when that reading does not hold.

### User Story 3 - Two workers share a resource (Priority: P2)

A second worker is running. It may hold the same worktree, or touch the same files, or nothing at
all.

**Why this priority**: it caused one of the four failures and is the cheapest to fix, but a single
worker is still the common case.

**Acceptance**: the brief states who else is running, what they are touching, and **whether they
share this worktree**, including when the answer is "nobody". A worker that finds an unexpected
file can tell a peer's output from an intruder.

### Edge Cases

- **The worker must ask before a pull request exists.** Three of three live ask-and-stop blocks
  address the question to a pull request. At turn zero there is none. The brief must give an
  address that exists then.
- **The worker cannot finish.** No Builder brief has a branch for this. A Builder that stops
  without one produces a silence indistinguishable from a worker that never ran.
- **The worker finishes early.** Not addressed in any brief.
- **A tool refuses every command.** The worker cannot tell a broken grant from a permission it
  lacks, because no brief records the grants it was launched with.

## Requirements *(mandatory)*

### Functional Requirements

Each is mechanically testable against a brief file. Counts are over the eight.

#### Structure

- **FR-001**: The brief MUST open by naming the role and the one-turn condition. *(8 of 8 carry
  "ONE TURN")*
- **FR-002**: `## Scope` MUST be the first heading, and MUST name the branch, the worktree, and the
  artifact set. *(8 of 8)*
- **FR-003**: `## Done looks like` MUST exist and MUST be an ordered numbered list. *(8 of 8, and
  zero bulleted items in any)*
- **FR-004**: An out-of-scope section MUST exist and MUST be a bulleted list. *(8 of 8)*
- **FR-005**: The final Done item MUST name what the worker reports back. *(8 of 8)*

The numbered-versus-bulleted split is not cosmetic. Done is a sequence the worker walks;
out-of-scope is a set it tests membership against.

#### Provenance

- **FR-006**: Every fact the brief hands the worker MUST carry the word measured, an **ISO date**,
  and where one exists the command that produced it. *(8 of 8 say "measured"; 7 of 8 carry an ISO
  date; only 2 of 8 name an instrument)*
- **FR-007**: A freshness word MUST NOT stand in for a date. *(4 of 8 head a section "today" or
  "tonight" with no date)*
- **FR-008**: The brief MUST require the worker to sweep for the same defect elsewhere and to
  report zeros **with the needle printed**. *(3 of 8 ask for zeros; 1 of 8 asks for the needle)*
- **FR-009**: A conclusion the Console reached MUST be marked as a reading with an owner, and MUST
  come with the escape the worker takes if it does not hold.

#### Prohibitions carried to the worker

Stated separately because this fleet has measured that prohibitions hold and obligations decay.
They are the load-bearing half.

- **FR-010**: The brief MUST carry a fixed, unmodified ask-and-stop prohibition. Its text is fixed
  by this spec; only the ask address is a fill-in field. *(present in 3 of 8, and **all three
  differ from each other and from the published template**, despite that template saying it goes
  in unchanged. Paste-unchanged is not self-enforcing.)*
- **FR-011**: The brief MUST forbid polling, sleeping, or waiting for a reply, in general terms.
  *(4 of 8 carry a CI-specific instance; 4 of 8 say nothing)*
- **FR-012**: The brief MUST instruct the worker to quote refusals, errors and rulings **verbatim**
  and never to paraphrase them. *(**0 of 8**. Needles printed: `Do not paraphrase` 0, `quote it`
  0. This is the instruction that saved the evidence in failure 3, and it is in none of the eight.)*
- **FR-013**: A brief MUST NOT assert an incapability without naming the attempt behind it and its
  date. *(7 of 8 assert one; 0 of 8 name an attempt)*

#### Concurrency

- **FR-014**: The brief MUST carry a concurrency slot with three fields, always present, including
  when the answer is nobody: who else is running, what they are touching, and **whether they share
  this worktree**. *(3 of 8 disclose anything, in two different slots. Needles printed: `same
  worktree` 0, `sole occupant` 0, `another worker` 0. Field three is the whole of failure 4.)*

#### Launch

- **FR-015**: The launcher MUST grant tools by bare name. A command-scoped grant such as
  `PowerShell(pwsh:*)` silently disables the tool.
- **FR-016**: The brief MUST record the grant list it was launched with, so a refusal the worker
  hits can be checked against it. *(Needle `allowedTools` **0 of 8**)*

#### Reporting

- **FR-017**: A Builder brief MUST carry a refusal branch: what the worker does and writes when it
  cannot complete. *(0 of 5 Builder briefs; 3 of 3 Reviewer briefs have a FAIL branch)*
- **FR-018**: The brief MUST ask the worker to state what it held constant, not only what it
  changed. *(0 of 8)*

#### Form

- **FR-019**: The brief file MUST be ASCII and LF-only. *(already true 8 of 8; specified so the
  property survives the first brief written by someone who did not learn it from the corpus)*

#### Reviewer-specific

- **FR-020**: A Reviewer brief MUST carry the seven-row pass criterion table. *(3 of 3)*
- **FR-021**: It MUST close with "An absence of findings is never a pass on its own. Affirmative
  evidence of a completed run is." *(character-identical 3 of 3)*
- **FR-022**: It MUST state that no verdict has been prescribed. *(3 of 3, inside Scope)*
- **FR-023**: It MUST disclose how much of the diff the briefing seat wrote, as a **field** rather
  than a fixed sentence. *(2 of 3, with different values)*

### Removals

Instructions carried by real briefs that are now known false or harmful.

- **RM-001**: Delete the seat-declaration falsehood. *(7 of 8, in four spellings)* It should say
  the seat name, the goal, and the command that declares them, run through the Bash tool with the
  path quoted. The worst spelling converts a false claim into a prohibition, which is the half that
  holds.
- **RM-002**: An account-capability section MUST NOT assert what is refused without a date and the
  refusal string quoted. Keep the route-around sentence, which is the good half.
- **RM-003**: A verdict MUST NOT be handed down as settled. Both offending briefs already contain
  the correct alternative and it should be generalised.
- **RM-004**: A concurrency disclosure MUST NOT live inside a Done item. It gets its own slot per
  FR-014.

### Key Entities

- **Brief**: a Markdown file, ASCII, LF-only, handed to exactly one worker for exactly one turn.
- **Worker**: a session that receives one brief, executes one turn, and exits. Builder or Reviewer.
- **Console**: the seat that writes briefs and spawns workers. The brief is its artefact, which is
  what makes it a seat under Article XI.
- **Ask address**: where a blocked worker writes its question. Must exist at turn zero.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A conformance checker can grade any brief against FR-001 to FR-023 mechanically, and
  reports which requirement each failure violates.
- **SC-002**: Zero briefs assert an incapability without an attempt and a date.
- **SC-003**: Every brief carries the fixed prohibition block byte-identical, with only the ask
  address varying. Current state: 0 of 3 instances are identical.
- **SC-004**: Every brief carries the concurrency slot with all three fields. Current: 0 of 8 carry
  field three in any form.
- **SC-005**: Every brief instructs the worker to quote refusals verbatim. Current: 0 of 8.
- **SC-006**: A worker that cannot finish leaves a written refusal rather than a silence.

## Assumptions

- The two-role split (Builder, Reviewer) is the real axis. The constitution names six seats; only
  two have briefs in the corpus. A Regulator, Steward or Lander brief would test this.
- The corpus is documentation-only work. All eight Scope sections name Markdown files and nothing
  else. A code brief may need slots this spec does not have.
- The eight files are what the workers actually received. None can be shown to be unedited since
  its run.

## Open Questions

The evidence cannot settle these and this spec does not.

| # | Question |
|---|---|
| Q1 | Does the declare command through the Bash tool work on every root and both surfaces? Article IX says a capability measured on one surface does not transfer, and RM-001 acts on a fact this extraction did not measure. |
| Q2 | Pass table row 1: "method used" or "tool used"? Corpus splits 2 to 1. |
| Q3 | Where does a worker with no pull request send its question? Mail crosses accounts and dies on delivery; a comment persists and needs a pull request. Neither covers the other. |
| Q4 | Should a Reviewer PASS require a posted receipt as well as the label, and should FAIL write a machine-readable refusal mark? This is a gate-design decision, not a brief-design one. |
| Q5 | Does this spec constrain the launcher, or only the brief text? FR-015 lives in the launch flags. If the spec may not reach them, that requirement has no owner. |
| Q6 | Ledger rule: cite nothing, or cite nothing unallocated? Corpus splits 4 to 2 on wordings with different scopes. |
| Q7 | Should a Builder be told the peer's identity, or only the contended resource? |

## What would falsify this specification

A spec that cannot be wrong is decoration.

1. A brief satisfying every requirement whose worker still guesses, waits, or collides. That is the
   contract itself under test.
2. A conforming Reviewer brief that cannot apply the label.
3. The declare command failing on a measured root. Then RM-001 is wrong, and the fix is to restate
   the rule with its attempt and date, not to delete it. **This is the one item where the spec acts
   on a fact nobody in this extraction measured.**
4. A code brief needing a slot this spec does not have. That falsifies the section census, not the
   shape.
5. The prohibition-versus-obligation asymmetry failing to reproduce. The split between requirements
   and prohibitions rests on it entirely.
6. A worker given the full concurrency disclosure still misreading a peer's output. Then the fix
   for failure 4 is isolation, not disclosure.
7. A conforming brief too long to read before starting work. The corpus runs 56 to 180 lines. If
   conformance pushes past what a worker reads, the spec has traded one failure for another and
   needs a length ceiling with a measurement behind it.
