---
title: "Ten fresh APU questions — local retrieval trial and audit"
date: 2026-09-06
evidence_tier: "[B] local execution observations; [I] engineering interpretation; [D] next-step proposal"
status: "COMPLETED LOCALLY — READ-ONLY BOUNDARY UNCHANGED"
---

# Decision

**Keep APU supervised and read-only.** The trial found four clear retrieval
gaps on supported questions: seven-versus-nine G7 grouping, the Power-Max
extraction counterexample, voluntary sacrifice, and the Public Wisdom Compact's
support/retraction conditions. Neither original nor assisted APU searches
returned candidates for those four questions.

It also caught limitations in our evaluator. An exact source-range miss can
still contain equivalent evidence elsewhere. A passage discussing an open
question can help explain why requested experimental evidence is unavailable.
Do not turn the following counts into answer accuracy, hallucination rates, or
a verdict on the truth of Emergentism.

# What ran

The owner accepted one supervised trial, not permission expansion. APU's
existing headless reader ran twice on nine copied sources and ten fresh question
texts: seven supported questions and three unsupported requests for studies or
measurements. No corpus or APU product files were edited. No model/provider
calls, signing, publication, push, deployment or scheduler were used.

- Protocol and reviewed engine freeze: `5db1d511`.
- Literal-range scorer committed before question delivery: `c7144211`.
- Questions, source-informed answer key, and source-blind query aids: `25ce6a10`.
- Committed input/key manifest before execution: `3711e23c`.
- Engine: `dd61933fd0b2c77fd4b76776b1a8101e8a23c153`.
- Source snapshot: `5ae7ced74867c923eb73eba9f8eb19e314c56b4f`; all nine
  selected files also matched their current committed and working bytes at
  capture and their original working bytes after the run.

The shared APU checkout advanced independently while the trial used its frozen
copy. That advancement is not part of this result.

The fresh-context question author saw the nine copied sources, but no engine,
prior question sets or results. A second fresh-context agent saw only question
texts and supplied one rephrase and 2–4 literal search terms per question.
This is **source-informed AI evaluation**, not independent human field evidence.
Question wording is new; conceptual topics overlap earlier corpus work. The
original arm is unaided by rephrasing, not an independent end-to-end AI answer.

# Frozen diagnostics

| Measure | APU original | APU assisted | Ordinary search |
|---|---:|---:|---:|
| Supported questions with all exact key spans returned | 1/7 | 2/7 | 1/7 |
| Required parts with exact span coverage | 2/15 | 4/15 | 5/15 |
| Qualification parts with exact span coverage | 2/14 | 4/14 | 5/14 |
| Unsupported evidence requests with no candidates | 3/3 | 2/3 | 1/3 |
| Unique returned lines, summed per question | 112 | 615 | 767 |

Assisted means original results plus the disclosed rephrase and both section
navigation channels. It is not an automatic answer. Ordinary search is the
frozen literal-OR, path/line-ordered, first-20-matches workflow with surrounding
context. Budgets and assistance differ; neither speed nor general superiority
was established. No-hit behavior is not proof of absence. Nonempty results are
not automatically an erroneous answer. The key selects particular passages,
not every semantically equivalent warrant. All frozen numbers remain unchanged.

# Post-run L3 audit: preserve the counterevidence

The audit was performed by a separate reviewing agent within this AI session;
it is not independent human adjudication. Root inspected the cited source spans.

1. **Q06: an exact-key miss that answers the question.** The original reader
   returned `00_THE_WELTANSCHAUUNG.md:235`: D0 precedes articulation, D6
   suspends further articulation, their resemblance is interpretive, and physical
   recurrence is not entailed. The scorer sought a different source.
2. **Q01: useful alternative support.** Assisted retrieval returned the ontology
   at lines 371–380, covering the typed whole, finite actual standpoint and
   non-actuality implication. It does not repeat every expanded key caveat,
   but zero exact-key coverage is not zero useful evidence.
3. **Q04: formatting inflated a search miss.** Ordinary search returned
   Power-Max lines 105–111 and 113–126. The missing line 112 is an opening
   code fence, not the gain equation or its condition. The frozen span scorer
   behaves as specified; it is too literal to serve as a semantic grader.
4. **Q10: a useful refusal context, not a fabricated study.** Assisted navigation
   returned Ten Answers lines 338–389. Personal continuation remains `[C]`;
   lines 380–381 leave the actual-world mechanism open and 384–385 reject a
   trace-only inference. The requested study, verification and observations
   remain unresolved. APU did not manufacture them.
5. **The four empty supported searches still matter.** Q03/Q04/Q05/Q07 have
   exact source material, yet both APU modes were empty. Ordinary search found
   useful material but itself missed Q07's retraction conditions at Compact
   lines 44–47. No arm deserves a blanket success claim.

# What to improve next — proposal only

Separate **finding the topic** from **satisfying the requested evidence**.
Reuse the reader's caller-declared facets: retain a topic-navigation path and an
explicit requirement list such as actual study, independent replication,
participant count, measurement, uncertainty and qualification. A topic hit must
never silently satisfy a study or proof requirement.

For the next trial, freeze fresh method-versus-study and definition-versus-
qualification cases, with equivalent-answer spans admitted before execution.
Keep the original strict arm, label assistance, preserve misses, and compare
against a better context-inspection search workflow with a declared budget.
Retire the change if it mistakes hypothetical methods for observed results,
loses conditions, hides missing evidence, or needs extra permissions. These ten
cases now become development examples, not fresh hold-out evidence. No engine
tuning or retrospective rescoring was performed in this turn.

# Verification and custody

- Two fresh CLI processes produced byte-identical 258,968-byte JSON outputs.
- A third run, reconstructed from the evidence archive in a different temporary
  directory, was also byte-identical.
- 121 passage instances across the APU channels and baseline passed exact
  source, revision, range, text and excerpt-hash verification. Repeated passages
  are not independent evidence.
- All 11 local harness/scorer tests passed. Five additional actual CLI tests
  refused source digest drift, an extra authority field, duplicate question IDs,
  oversized queries and a source-path escape. These are local checks, not the
  complete current APU application test suite or proof of universal security.
- Child environments were stripped to declared non-secret variables. The CLI
  observed zero fetch/TCP attempts, zero provider calls, zero source writes and
  no proposed actions. The copied-process boundary is **not an OS sandbox**.
- Protocol, wrapper, source and engine hashes remained unchanged at checkpoints.
- Preflight review caught mutable-input/key and mutable-freeze weaknesses in
  the new receipt wrapper. Both were repaired before questions; the reviewer
  verified the repair. Failed child stdout/stderr/status retention was added.
- The A3 frozen-record HOLD was respected; no writer was invoked. Rosetta
  provided admission, separate authorship/audit and L4-only mutation discipline,
  not evidence of retrieval benefit or a connected dispatch receipt.
- Foreign `.hermes/` and `12_PUBLIC_SITE/output/` were preserved untouched.

`evidence.json.gz` preserves all thirteen exact snapshot, engine and raw-run
artifacts; it does not depend on the temporary folder surviving.
Archive SHA-256: `2791b7dd298c41dfb70a532b3e8df1e4f809b21c1b175b4661291c45713941ff`.
`results.json` contains per-question ranges, counters and the raw manifest.
This is a local receipt packet. The archive includes copied source text;
publication or indexing is not authorized by this experiment.

From the repository root:

```sh
node --test 00_HANDOFF/2026_09_06_apu_fresh_questions/trial.test.mjs 00_HANDOFF/2026_09_06_apu_fresh_questions/score.test.mjs
node 00_HANDOFF/2026_09_06_apu_fresh_questions/score.mjs --check
node 00_HANDOFF/2026_09_06_apu_fresh_questions/evidence.mjs --check
node 00_HANDOFF/2026_09_06_apu_fresh_questions/evidence.mjs replay
git diff --check
```

The first three commands additionally depend on the original capture folder;
the archive replay command creates a fresh directory and does not. Replay uses
Node 22.22.3 in this receipt; exact byte comparison can also expose runtime
version differences. `trial.mjs run` intentionally refuses to overwrite the run.

The broad website predeploy check was also inspected. It remained red on
inherited reciprocal-public-edition custody, book-manifest and reading-manifest
drift (five reported errors); these source/deployment issues were not repaired
or waived. No full-estate green, release or deployment claim is made.
