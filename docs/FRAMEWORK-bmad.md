---
title: "BMAD 6.11.0 with Ultracode: A how-to"
layout: default
---

# BMAD 6.11.0 with Ultracode: A how-to

<a id="tldrbluf"></a>

[BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD) 6.11.0 adds named roles and planning skills to Claude Code. It can supply written plans
and review steps for Ultracode.

Keep skills that write shared state out of concurrent Ultracode work. Two writers can overwrite each
other's updates; the upstream docs cover BMAD itself.

[The procedure below](#how-to-use-them-together) shows how to combine planning, parallel work, and review.

---

## What is BMAD

BMAD means Breakthrough Method for Agile AI-Driven Development. It and Ultracode offer different
ways to organize Claude Code work.

BMAD uses human-directed roles and Markdown specifications. Ultracode lets Claude Opus choose when
to run parallel subagents, using maximum (`xhigh`) reasoning effort.

BMAD's analyst, product manager, and architect help you write a product requirements document (PRD)
and an architecture document before coding.

Version-controlled files under `_bmad-output/` keep those decisions available through a long build.
The 49 installed skills also include a developer, a user experience designer, and party mode for
combining personas.

Run `/effort ultracode` to enable `xhigh` reasoning and automatic work assignment. Claude decides
when a task needs parallel subagents.

The run holds each subagent's result in a script variable until it finishes. This reduces what the
main context window must carry.

BMAD saves its PRD, architecture document, story files, and sprint status file to disk. They remain
after the session ends.

Install BMAD with:

```
npx bmad-method@6.11.0 install --yes --tools claude-code --modules bmm --directory .
```

The install adds 3.0MB across 248 files in `.claude/skills/` and `_bmad/`. Git ignores none of them
by default.

Two of the 49 skills run Python. `sprint_status.py` replaces the work-tracking file atomically, but
has no lock to prevent two writers from losing an update.

`config_utils.py` stops with an error when it cannot resolve the project root. It does not guess
when you run BMAD from the wrong directory.

The 49 skills:

<!-- no-copy -->
```
bmad-advanced-elicitation      bmad-agent-analyst           bmad-agent-architect
bmad-agent-dev                 bmad-agent-pm                bmad-agent-ux-designer
bmad-architecture              bmad-brainstorming           bmad-build
bmad-build-auto                bmad-checkpoint-preview      bmad-code-review
bmad-correct-course            bmad-create-architecture     bmad-create-epics-and-stories
bmad-create-prd                bmad-create-story            bmad-customize
bmad-deep-recon                bmad-dev-auto                bmad-dev-story
bmad-document-project          bmad-domain-research         bmad-edit-prd
bmad-editorial-review          bmad-editorial-review-prose  bmad-editorial-review-structure
bmad-forge-idea                bmad-generate-project-context bmad-help
bmad-market-research           bmad-party-mode              bmad-prd
bmad-prfaq                     bmad-product-brief           bmad-project-context
bmad-qa-generate-e2e-tests     bmad-quick-dev               bmad-retrospective
bmad-review                    bmad-review-adversarial-general
bmad-review-edge-case-hunter   bmad-review-verification-gap bmad-spec
bmad-sprint-planning           bmad-sprint-status           bmad-technical-research
bmad-ux                        bmad-validate-prd
```

---

## BMAD vs Ultracode

<figure role="group">
<svg viewBox="0 0 840 660" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="BMAD run alone writes persistent files from a set of personas with no fixed order. Ultracode run alone fans out to anonymous subagents that return data and leave nothing on disk. Combined, BMAD's planning files become the input Ultracode's fan-out executes against, except for BMAD's stateful skills, which must stay out of the fan-out.">
  <defs>
    <marker id="bmad-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="currentColor" />
    </marker>
    <marker id="bmad-arrow-accent" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="#2563eb" />
    </marker>
  </defs>

  <text x="20" y="30" font-size="15" font-weight="bold" fill="currentColor">BMAD, run alone</text>
  <rect x="30" y="45" width="290" height="115" rx="8" fill="none" stroke="currentColor" stroke-width="1.5" />
  <text x="40" y="62" font-size="11" font-style="italic" fill="currentColor">Personas, no fixed order</text>
  <rect x="42" y="72" width="72" height="26" rx="4" fill="none" stroke="currentColor" />
  <text x="78" y="89" font-size="11" text-anchor="middle" fill="currentColor">Analyst</text>
  <rect x="122" y="72" width="50" height="26" rx="4" fill="none" stroke="currentColor" />
  <text x="147" y="89" font-size="11" text-anchor="middle" fill="currentColor">PM</text>
  <rect x="180" y="72" width="76" height="26" rx="4" fill="none" stroke="currentColor" />
  <text x="218" y="89" font-size="11" text-anchor="middle" fill="currentColor">Architect</text>
  <rect x="42" y="106" width="50" height="26" rx="4" fill="none" stroke="currentColor" />
  <text x="67" y="123" font-size="11" text-anchor="middle" fill="currentColor">Dev</text>
  <rect x="100" y="106" width="90" height="26" rx="4" fill="none" stroke="currentColor" />
  <text x="145" y="123" font-size="11" text-anchor="middle" fill="currentColor">UX designer</text>
  <rect x="198" y="106" width="100" height="26" rx="4" fill="none" stroke="currentColor" />
  <text x="248" y="123" font-size="11" text-anchor="middle" fill="currentColor">Party mode</text>

  <line x1="320" y1="102" x2="365" y2="102" stroke="currentColor" stroke-width="1.5" marker-end="url(#bmad-arrow)" />

  <rect x="368" y="45" width="220" height="115" rx="8" fill="none" stroke="currentColor" stroke-width="1.5" />
  <text x="478" y="98" font-size="11" text-anchor="middle" fill="currentColor">
    <tspan x="478" dy="0">PRD, architecture,</tspan>
    <tspan x="478" dy="16">story files, sprint</tspan>
    <tspan x="478" dy="16">status</tspan>
  </text>
  <text x="478" y="180" font-size="11" font-style="italic" text-anchor="middle" fill="currentColor">Persists after the session ends</text>

  <text x="20" y="225" font-size="15" font-weight="bold" fill="currentColor">Ultracode, run alone</text>
  <rect x="30" y="255" width="95" height="42" rx="6" fill="none" stroke="currentColor" stroke-width="1.5" />
  <text x="77" y="280" font-size="11" text-anchor="middle" fill="currentColor">Request</text>
  <line x1="128" y1="276" x2="163" y2="276" stroke="currentColor" stroke-width="1.5" marker-end="url(#bmad-arrow)" />
  <rect x="166" y="255" width="130" height="42" rx="6" fill="none" stroke="currentColor" stroke-width="1.5" />
  <text x="231" y="273" font-size="11" text-anchor="middle" fill="currentColor">
    <tspan x="231" dy="0">Fans out to</tspan>
    <tspan x="231" dy="14">subagents</tspan>
  </text>

  <line x1="299" y1="266" x2="345" y2="241" stroke="currentColor" stroke-width="1.5" marker-end="url(#bmad-arrow)" />
  <line x1="299" y1="276" x2="345" y2="276" stroke="currentColor" stroke-width="1.5" marker-end="url(#bmad-arrow)" />
  <line x1="299" y1="286" x2="345" y2="311" stroke="currentColor" stroke-width="1.5" marker-end="url(#bmad-arrow)" />
  <rect x="348" y="226" width="72" height="28" rx="4" fill="none" stroke="currentColor" />
  <text x="384" y="244" font-size="11" text-anchor="middle" fill="currentColor">Task</text>
  <rect x="348" y="262" width="72" height="28" rx="4" fill="none" stroke="currentColor" />
  <text x="384" y="280" font-size="11" text-anchor="middle" fill="currentColor">Task</text>
  <rect x="348" y="298" width="72" height="28" rx="4" fill="none" stroke="currentColor" />
  <text x="384" y="316" font-size="11" text-anchor="middle" fill="currentColor">Task</text>

  <line x1="423" y1="240" x2="473" y2="266" stroke="currentColor" stroke-width="1.5" marker-end="url(#bmad-arrow)" />
  <line x1="423" y1="276" x2="473" y2="276" stroke="currentColor" stroke-width="1.5" marker-end="url(#bmad-arrow)" />
  <line x1="423" y1="312" x2="473" y2="286" stroke="currentColor" stroke-width="1.5" marker-end="url(#bmad-arrow)" />
  <rect x="476" y="255" width="150" height="42" rx="6" fill="none" stroke="currentColor" stroke-width="1.5" />
  <text x="551" y="280" font-size="11" text-anchor="middle" fill="currentColor">Session context</text>
  <text x="230" y="345" font-size="11" font-style="italic" text-anchor="middle" fill="currentColor">Ends when the run ends -- nothing written unless told to</text>

  <text x="20" y="400" font-size="15" font-weight="bold" fill="#2563eb">Combined: BMAD plans, Ultracode executes</text>
  <rect x="30" y="420" width="220" height="60" rx="8" fill="none" stroke="#2563eb" stroke-width="1.5" />
  <text x="140" y="446" font-size="11" text-anchor="middle" fill="currentColor">
    <tspan x="140" dy="0">PRD, architecture,</tspan>
    <tspan x="140" dy="16">story files</tspan>
  </text>

  <line x1="253" y1="450" x2="298" y2="450" stroke="#2563eb" stroke-width="1.5" marker-end="url(#bmad-arrow-accent)" />

  <rect x="301" y="420" width="240" height="60" rx="8" fill="none" stroke="#2563eb" stroke-width="1.5" />
  <text x="421" y="446" font-size="11" text-anchor="middle" fill="currentColor">
    <tspan x="421" dy="0">Ultracode fan-out,</tspan>
    <tspan x="421" dy="16">one subagent per story</tspan>
  </text>

  <line x1="544" y1="450" x2="589" y2="450" stroke="#2563eb" stroke-width="1.5" marker-end="url(#bmad-arrow-accent)" />

  <rect x="592" y="420" width="150" height="60" rx="8" fill="none" stroke="#2563eb" stroke-width="1.5" />
  <text x="667" y="446" font-size="11" text-anchor="middle" fill="currentColor">
    <tspan x="667" dy="0">Code</tspan>
    <tspan x="667" dy="16">and tests</tspan>
  </text>

  <rect x="30" y="510" width="712" height="60" rx="8" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3" />
  <text x="46" y="534" font-size="11" fill="currentColor">
    <tspan x="46" dy="0">Keep BMAD's stateful skills (anything writing sprint-status.yaml) out of this fan-out --</tspan>
    <tspan x="46" dy="16">no lock between the read and the write. Route only planning output and checked review skills in.</tspan>
  </text>
</svg>
<figcaption>BMAD alone writes persistent files from personas with no fixed order. Ultracode alone
fans out to anonymous subagents that return data and leave nothing on disk. Combined, BMAD's
planning files become the input Ultracode's fan-out executes against.</figcaption>
</figure>

---

## Does BMAD augment Ultracode

BMAD adds a written project spec and named review passes. Ultracode does not keep either on its own.

Run the planning skills once before starting parallel work. With one writer at a time, they cannot
race over the state file.

You can run review skills in parallel after checking that they do not write that file.

Do not run the whole persona set concurrently. The personas are designed for sequential work, and
concurrent state-file writes can lose updates.

---

## How to use them together

1. Run the planning skills, in this order: `bmad-create-prd`, `bmad-create-architecture`,
   `bmad-create-epics-and-stories`. Each writes one file under `_bmad-output/`.
2. Hand the resulting story files to Ultracode. `/effort ultracode` fans out across them, one
   subagent per story.
3. Check that a review skill -- `bmad-review`, `bmad-review-adversarial-general`,
   `bmad-review-edge-case-hunter`, `bmad-review-verification-gap` -- does not touch
   `sprint-status.yaml` before routing it into the fan-out.
4. Never run `bmad-sprint-status`, `bmad-dev-story`, `bmad-build`, or any other skill that writes
   `sprint-status.yaml`, as two or more concurrent subagents sharing one worktree. Give each its own
   worktree, or keep it sequential.
5. For unattended runs across a whole epic -- native Ultracode is session-scoped, so it will not
   advance to the next story on its own -- a third-party extension exists:
   [`bmad-module-ultracode-goal`](https://github.com/armelhbobdad/bmad-module-ultracode-goal).
   - It gates each story's advancement on a deterministic pass from BMAD's own Test Architect
     module, not the model's self-assessment.
   - It is unofficial: published by an individual, not by `bmad-code-org`. Read its source before
     trusting it with an unattended run.
