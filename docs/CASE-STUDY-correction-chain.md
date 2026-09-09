# Case study: A finding that took four passes and two sessions

<a id="tldrbluf"></a>

On 2026-08-12, two sessions revised one finding four times. Two statements were wrong, and each
session corrected the other.

Both sessions gave confident answers that a command could disprove. This example applies when you
already run more than one session; a solo session has no second reader.

Treat the first finding as a hypothesis. Ask another session to run the check before you file it;
see [what to do with this](#what-to-do-with-this).

---

The sessions were checking whether any automated test read the repository's always-loaded
conventions file.

## The four statements

| Pass | Session | The claim | Verdict |
|---|---|---|---|
| 1 | A | A docs-only pull request skips the suite, so any gate protecting the file would not run | Wrong |
| 2 | B | Nothing reads the file at all: 76 test files mention it, zero read it | Wrong |
| 3 | A | Two guards read it, both are allowlisted, both run, and neither checks content | Correct |
| 4 | Joint | The defect is that the allowlist is an enumeration, so a check landed outside it goes green by absence | Correct, narrower |

Passes 2 and 3 each contradicted the previous claim. Pass 4 made the correct claim more precise.

Both sessions were ready to file a wrong finding. Session A would have filed "unguarded"; Session B
would have filed "no reader exists".

A reviewer could refute B by opening one test file. Reading one workflow path filter would refute A.

## What moved each pass

Commands changed the claims in passes 1 to 3. Neither session corrected itself by reasoning or
rereading; pass 4 narrowed pass 3 without another measurement.

Pass 2 used a grep that required the filename and a read verb on the same line. The matching code
built the path first, then read it later through a variable.

The filter could not detect that code pattern. The session treated its empty result as proof that no
reader existed.

## What the sequence does not establish

| Not established | Why |
|---|---|
| A rate | One finding is one finding. Nothing here says how often a first statement is wrong |
| That two sessions are better than one reader | The comparison was never run. A single session that re-measured might have reached pass 3 |
| That the channel caused it | How the corrections travelled between sessions was not measured |
| That the correct statement is final | Passes 3 and 4 are verdicts as of the date above, and nothing here re-establishes them |

## The errors were all one shape

Recorded the same day, across the same two sessions:

- Two false zeros, from commands that failed rather than scanned.
- A three-rule precedence chain reported from one regex. One rule was tested, and the result
  was written up as the chain's behaviour.
- A breakdown whose eight figures summed to 1202, from a tool whose own output read
  `found 646 section citations`. Written up under
  [reconcile the parts against the total](TIPS-AND-TRICKS.md#reconcile-the-parts-against-the-total-the-tool-already-printed).

Each result came from a tool nobody had checked. Every case had an available positive control that
would have cost nothing to run.

## What to do with this

Do not file a confident first reading before someone checks it.

Keep a single session's finding provisional until a second session runs the command. If both
sessions already exist, send one message.

The second run gives you an independent measurement. In passes 2 and 3, conflicting results exposed
the defect.

Limit: this is not a claim that peer review finds everything, and it does not replace the mechanical
checks in [when you write a guardrail](TIPS-AND-TRICKS.md).

Start with the code doing the reading: enumerate from the callee. Opening a guard shows which files
it reads.

Finding every possible reader requires a filter over all callers. That broader filter failed here.
