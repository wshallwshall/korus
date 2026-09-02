# KORUS

**Keep One Repo, Unblock Sessions.** A working method for running several AI coding
sessions against one codebase without them colliding, losing work, or quietly agreeing
with each other.

## Status: early, and the spec is being written now

KORUS grew out of tooling for a single project and has been revised repeatedly under
real use. Its properties were **discovered, not designed** -- most of what is known
about it came from running it and measuring what broke.

This repository exists to change that. It uses
[Spec Kit](https://github.com/github/spec-kit) for spec-driven development: the
constitution first, then the spec, then the plan.

**Nothing here is stable yet.** Findings are still being consolidated from three days of
measured operation, and some published guidance has already been shown wrong.

## Start here: the constitution

**[The KORUS Constitution](.specify/memory/constitution.md)** is the only substantive
document so far. It holds the rules a session, a seat, a gate or a later spec may not
break, and **every article names the evidence behind it** so a reader can check rather than
trust.

Ten articles, in short:

| | |
|---|---|
| I | No session is the only reader of its own work |
| II | Publish readings, not conclusions |
| III | A gate records that someone looked, not that a step happened |
| IV | Every claim names the condition it did not vary |
| V | No rule may manufacture its own evidence |
| VI | A number without its instrument is not a measurement |
| VII | Waiting is a design cost and it is measured |
| VIII | The account roster is assigned by the Owner, and no design may infer it |
| IX | Built for Claude Code, and no design may require a particular surface |
| X | A seat that cannot be measured cannot be steered |

It is at **v1.4.0** and it expects to be wrong in places. Most articles rest on a small
number of observations, several from a single night of operation, and the document says so.
Amendments require evidence, and retired text stays with the reason it was retired.

## What problem it solves

Run more than one AI session on one repository and four things go wrong:

1. **They collide.** Two sessions in one checkout overwrite each other's work.
2. **They lose work.** A session ends and its context, findings and half-finished
   branches go with it.
3. **They agree wrongly.** Two sessions that share a hidden condition reach the same
   wrong answer and their agreement reads as confirmation.
4. **They cannot be told apart.** A stalled session and a working one look identical
   from outside.

KORUS is the set of roles, gates and instruments that address these.

## The shape

Work is divided among **seats**, each a session with one job:

| Seat | What it does | Lifetime |
|---|---|---|
| Console | Plans, spawns workers, holds the owner's attention | long-lived |
| Builder | Takes one brief, does the work, opens a pull request | one turn |
| Reviewer | Reads one pull request | per pull request |
| Regulator | Attributes a failing build | woken on a red |
| Steward | Writes files other seats read | cron, no model calls |
| Lander | Decides merge order | long-lived |

Seven further seats were tried and retired. Why each went is part of the record this
repository is being built to hold.

## Repository layout

```
.specify/memory/constitution.md   the rules nothing may break
.specify/                         Spec Kit scaffold: templates and scripts
specs/                            one directory per feature: spec.md, plan.md, tasks.md
```

## Related

- [claude-multisession](https://github.com/wshallwshall/claude-multisession) -- the
  earlier public home for KORUS documentation and scripts, and where the open findings
  currently live.

## Licence

See [LICENSE](LICENSE).
