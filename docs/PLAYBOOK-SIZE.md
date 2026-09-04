# Playbook size: Nobody has measured where an instruction document stops being followed

## TLDR/BLUF

**What this is.** Guidance on how long a role playbook should be, and what shape it should take.
Every length figure below is a judgment, not a reading.

**Why you should care.** A 107-agent literature sweep on 2026-09-04 found no compliance study that
treats document length as an independent variable. No correlation, no regression, no length
bucketing, no truncation arm.

**What is measured instead.** Compliance ceilings at fixed length, position effects on retrieval,
and order effects at fixed length. Those three carry every recommendation here.

**How to use it.** Take [the rules](#the-rules-this-page-gives) as defaults you overrule with a
reason. Anything that has to hold needs a gate, not a sentence.

---

## No study varies length, so every length rule here is a judgment

The sweep read compliance work, long-context work and instruction-following work. Length shows up as
a corpus property that gets reported, never as a condition anyone varied.

So there is no published number for "a playbook over N words stops being followed". Any page that
hands you one, this page included, is handing you taste with citations attached.

**No vendor guidance on system-prompt or `CLAUDE.md` length survived the sweep.** Two verifiers
exhausted their search budget at 200 of 200 calls. That is an absence in one sweep, not proof that
none exists.

## A playbook is not a control

HANDBOOK.md (Panavas et al., Surge AI) grades 65 agentic tasks against expert-written procedures of
20 to 124 pages. It was accepted to the Workshop on Agent Behavior at COLM 2026
([arxiv.org/abs/2607.25398](https://arxiv.org/abs/2607.25398)).

Grading is deterministic. Each of the 824 criteria is a Python function over final environment
state: no LLM judge, and no partial credit.

Its headline: "Under strict grading, where a trial passes only if every criterion is satisfied, the
best of thirty evaluated model configurations passes 36.2% of trials."

Most frontier configurations sat below 25 percent. The governing procedures ran 8K to 79K tokens,
median 14.9K, mean 22.3K.

**Grade it as a vendor benchmark with open code and deterministic scoring.** Stronger than a
marketing post, weaker than a replication.

| Limit that travels with the 36.2 percent | What it means |
|---|---|
| All authors are Surge AI, and the vendor markets the benchmark | No independent party set the bar |
| No limitations section, no independent replication | The number has been produced once |
| Trials average about 17 reasoning steps and 30 tool calls | Agentic competence is confounded with rule compliance |

A failed trial can be a failed task rather than an ignored rule, and the score cannot separate the
two.

**What follows for a playbook.** At that ceiling under ideal grading, anything that has to hold
needs a gate. The playbook then carries what a gate cannot check, and the reason behind each rule.

[CI for leaders](CI-FOR-LEADERS.md) is this repository's reading of the same split.

## Budget the sum in context, not the file

Positional bias tracks share of the context window rather than absolute token count. "Positional
Biases Shift as Inputs Approach Context Window Limits" (Veseli, Chibane, Toneva, Koller; COLM 2025,
code released) measured that shift.

The lost-in-the-middle effect "is strongest when inputs occupy up to 50% of a model context window.
Beyond that, the primacy bias weakens, while recency bias remains relatively stable".

A distance-from-the-end gradient replaces the U-curve. **Limit: the dependent variable is retrieval,
not compliance.** Finding a fact and obeying a rule are different tasks, and nothing bridges them.

**So the unit to budget is the sum.** What competes for the window is the playbook plus the shared
rules plus `CLAUDE.md` plus the task plus whatever the repository pulls in.

A 33K-token file at 17 percent fill of a 200K window sits where primacy still helps. The same file
beside three others may not.

## Advertised context is not effective context

RULER (Hsieh et al., NVIDIA, COLM 2024) tested 17 models all claiming 32K or more. Only about half
held performance at 32K.

NoLiMa tested 13 models claiming 128K or more. Eleven fell below half their own short-context
baseline.

**Limit: both measure retrieval.** Use them to justify caution about total context, never as
compliance numbers.

## Order by consequence, because order moves compliance at fixed length

"Order Matters: Investigate the Position Bias in Multi-constraint Instruction Following" (Zeng et
al., Findings of ACL 2025, code released) reordered the same constraints and measured the swing.

With 7 constraints, best against worst ordering moved compliance about 7 points for
LLaMA3-8B-Instruct and about 5 for Qwen2.5-7B-Instruct.

In multi-round delivery the same manipulation moved LLaMA3-8B and LLaMA3-70B by about 25 percent.
**Limit: small-to-mid open models, not frontier models.**

**So put what has to survive where position favours it.** The middle is where rules go to die. Order
by consequence of failure, not by topic.

## Name a rule, never its position

"Attention Instruction: Amplifying Attention in the Middle via Prompting" (Zhang, Meng, Collier,
2024) tested pointing a model at an absolute index in its input.

Referencing an index raised accuracy about 4 to 10 points for Llama-2-chat when the referenced
segment matched the answer location. The mismatch penalty was about 25 points.

The penalty is far larger than the gain, and the authors concede the correct location is unknown in
practice. **Limit: small open models, 2024 vintage.**

**So cite a rule by its name.** "The no-glyph rule" survives an edit that moves it. "The rule in
section 4" does not, and a stale positional pointer costs more than no pointer at all.

## What this repository measured

### A gate holds the rule that prose alone does not

The same no-glyph rule, over the same lineage of text: 0 violations where a CI gate refuses, 93
where the rule is prose alone. 68 of the 93 sit in the single file that anchors the house format.

The gate side, run over this whole tree on 2026-09-04:

```powershell
& ./scripts/quality/check-ascii.ps1 -MaxReport 0 -ExcludeDir skills,.specify
```

It returned exit 0 over the 174 files the tree held that day. The count moves as the tree grows, so
the exit code is the reading. The 93 are in a private vault's `roles/`, which no reader here can run
the command against.

**What was not varied:** one tree, one day, two repositories sharing an author. The contrast is a
gate against no gate, and the two corpora are not otherwise matched.

### 61 percent of the prose was the half no test read

Measured at commit `1b6b7fc`:

| Corpus | Files | Words |
|---|---|---|
| `roles/` | 15 | 180,043 |
| `docs/` plus `README.md` | 36 | 115,357 |

```powershell
$f = (git ls-tree -r --name-only 1b6b7fc -- roles) | Where-Object { $_ -like '*.md' }
$f.Count; ($f | ForEach-Object { git show "1b6b7fc:$_" } | Measure-Object -Word).Words
```

The prose ratchets reached `roles/` on 2026-09-04, and `roles/` is the larger half of the corpus.

### The playbooks carry the debt the docs paid off

| Measure | `docs/` | `roles/` |
|---|---|---|
| Paragraphs over 300 characters | 0 | 986 |
| Sentences over 30 words | 49 | 708 |
| Table cells over 40 words | 10 | 138 |

```powershell
python -m pytest tests/test_prose_rules_hold.py -q
```

**What was not varied: `docs/` was swept twice and `roles/` never.** The comparison measures sweeps,
not authors. [House style](HOUSE-STYLE.md) carries the rules both corpora are graded against.

### Readership is a floor, not a compliance rate

Across 401 local Claude Code session transcripts on 2026-09-04, 22 sessions issued a Read against
any role playbook. Reads of the largest playbook were 78 ranged against 6 whole-file.

**The 401 counts sessions, not agents.** It is the top-level `projects/*/*.jsonl` across two config
roots.

A recursive glob over the same roots returns 13,574. That form also collects subagent and workflow
transcripts, which are not sessions and never read a playbook on arrival. Use the top-level form, or
the denominator inflates by a factor of thirty.

**Limit: the 401 include many non-seat sessions.** That makes 22 a floor over a mixed population,
and not a compliance rate among seats.

A transcript records every Read `tool_use` with its `file_path`, `offset` and `limit`, which is what
makes read depth recoverable:

```powershell
$root = "$HOME\.claude\projects"
(Get-ChildItem $root -Recurse -Filter *.jsonl -File |
  Where-Object { Select-String -Path $_.FullName -Pattern '"file_path":"[^"]*roles[/\\]' -Quiet }).Count
```

A different transcript root gives a different population, so print the root beside the count.

## The rules this page gives

| Item | Rule |
|---|---|
| Anything that has to hold | Gate it. A playbook sentence is not a control |
| What the playbook carries | What a gate cannot check, plus the reason behind each rule |
| The budget | The sum in context: playbook plus shared rules plus `CLAUDE.md` plus task |
| Ordering | By consequence of failure. Front and end hold; the middle does not |
| Cross-references | By name. Never by section number, position, or line |
| Repeating a rule across playbooks | A pointer, never a second summary. [roles/README.md](https://claude-multisession.pages.dev/roles/README.md) sets it |
| Every number in a playbook | The command beside it, and the condition you did not vary |
| Any length figure, here or anywhere | A judgment. No study varies length |

## What would settle it

An experiment, not another sweep. None of the below has been run.

**The probe set.** 40 to 60 rules, each deterministically checkable, and each something a model
would not do absent the rule.

**Position assignment.** Latin square, so every rule visits every depth bucket. That decorrelates
rule difficulty from position. Report depth deciles.

**Triggers.** Tasks that create the opportunity to break a rule without naming the rule.

**Length ablation.** 5k, 10k and 25k words, run twice: once holding relative position constant, once
holding absolute token index constant.

That pair is what separates "decays as N grows" from "decays as total length grows". Run a
relative-fill arm at 10, 25, 50 and 75 percent alongside it.

| Control | What it proves |
|---|---|
| Positive: state the rule in the user turn | If compliance is not near ceiling, the rule is unmeasurable |
| Negative: remove the rule | The baseline must be near zero, or the rule is not counter-default |
| Ingestion: log what entered context | Separates "never entered" from "entered and was ignored" |

The ingestion arm is the one a length study cannot skip. Never entered and entered-then-ignored have
opposite fixes, and they produce the same failed criterion.
