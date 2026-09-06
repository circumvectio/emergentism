---
type: local-experiment-receipt
title: "APU copied-source reader pilot — preparation"
date: 2026-09-06
status: "PREPARED — results recorded separately after execution"
evidence_tier: "[S] selected scope; [I] evaluation design; no world validation"
---

# APU reader pilot

Execution is complete; see [the result and its limits](RESULTS.md). The frozen
preparation below is retained, not rewritten to fit the observations.

The owner asked to use APU on Emergentism and incrementally expand its scope.
This packet tests one prerequisite: can its existing local librarian retrieve
source-bound material without adopting it or changing the original project?
It is an Emergentism handoff receipt, not a product specification or canon.

## Frozen scope

- Nine committed source files, 155,165 bytes; all declared `reference`.
- Separate source and engine revisions in [source-lock.json](source-lock.json).
- Eight frozen questions in [tasks.json](tasks.json), authored by an independent
  L2 lane that read the sources. Not blinded or externally preregistered.
- `formula`, `product`, `sacrifice`, `approved`, `empty`: literal boundary probes.
- `cheating`, `tested`: vocabulary-mismatch probes; misses remain reported.
- `sourdough`: absence control only if absent from the actual copied bundle.

The corpus-side [runner](run_pilot.mjs) archives the pinned APU product commit,
loads its **unchanged** import/rehearsal/search core, and imports exact copies.
The existing product CLI accepts only sources inside its own product root;
this wrapper does not expand that CLI or edit the shared product.

Run with `node 00_HANDOFF/2026_09_06_apu_readonly_pilot/run_pilot.mjs` from the
Emergentism checkout. No install is required. Existing APU `node_modules` is
reused and its path and Vite version are recorded; the complete dependency
closure is **not** pinned or independently audited. Node 22 is the tested
host candidate. Output goes only to a new private temporary directory.
Failures remain there. `COMPLETE.json` is emitted last and hashes retained
inputs, copied sources, native APU package, raw results and check receipts.

## What is measured

The independent baseline is a literal, case-insensitive substring scan over
copied file text, returning source paths and matching line numbers. APU also
searches generated node labels and provenance notes; metadata-only matches are
reported separately. Its 12-node cap may include both label and full-file quote
nodes. The first-five-node window is applied **before** source deduplication.

Owner-path presence is a routing metric, not a correct answer. Expected sections
are a separate answer key, not query input. No semantic answer score is inferred
from a hit; no human speed or comprehension advantage is measured. A null for
an ordinary paraphrase is not evidence that the corpus has no answer.

Two rehearsals use the same frozen snapshot. Compare citations and answers
excluding only the generated receipt timestamp; preserve both raw receipts.
APU node-version timestamps mean full project digests need not be identical.
Each run must independently pass codec, restore, non-mutation and recovery
checks. Tamper, duplicate path, traversal, invalid kind, oversize, non-find
command and changed-copy cases use disposable data, never canonical edits.

## Boundaries

No model calls, source edits, adoption, product edits, browser-profile reads,
public writes, push, deploy, credential use or recurring process. The worker
receives only explicit PATH/NODE_ENV/LANG and process-local storage. Vite config
and env files are disabled. Fetch/TCP guards are installed before its loader.
These guards are **not comprehensive OS network containment**. Byte checks prove
unchanged originals at checkpoints, not filesystem write prevention.

Source HEAD may advance before a later rerun, but every selected committed and
working-tree byte must still match the frozen revision. Any HEAD movement
during a run or selected-byte drift refuses completion.

## Review and custody

L1 reviewed the old runner's direct boundary. Its final worker hit a usage limit;
the partial source-anchored report was retained, not retried around that limit.
L2 supplied mixed-vocabulary questions; L3 ranked the unchanged-core wrapper
and reviewed its limits. L4 alone writes this new directory. Full A3 dispatch
recording remains on the existing frozen-record **HOLD**; these review reports
do not claim a connected or fully recorded Soul Loop.

Shared APU visual work, Emergentism `.hermes/` and site `output/`, and the
Documents root's unrelated staged work remain outside this commit.

## Incremental capability path — proposal, not a grant

| Stage | Work allowed after its explicit grant | Evidence needed before proposing the next stage |
|---|---|---|
| P0 — this pilot | Copied references; local retrieval; receipts | Provenance, abstention, no mutation, honest comparison |
| P1 — next candidate | Better passage retrieval and reviewed Explore-view suggestions | Separate UI acceptance; held-out wording; visible source/claim tiers; no false authority |
| P2 — reversible build | Named files in an isolated working copy; reviewable patches | Enforced path/verb budgets; adversarial tests; rollback and stop tests; independent diff review |
| P3 — bounded autonomous work | Repeated tasks inside an owner-defined charter, time/cost/scope limits | Reliability over multiple independent tasks; revocation; observability; automatic stop on drift |

No automatic promotion from a passing score. Public release, canonical claim
adoption, private-data access, spending and expanded tool/network permissions
retain distinct owner-approved scope. APU cannot sign or expand its own grant.
“Let it loose” is the desired reduction in supervision **inside an agreed
boundary**, not permission to remove that boundary. The present run creates
neither a daemon nor future unattended work.
