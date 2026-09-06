---
type: local-experiment-receipt
date: 2026-09-06
status: "READ-ONLY COMPONENT ADDED; GENERAL-READER ACCEPTANCE NOT PASSED"
evidence_tier: "[B] local measurements; [I] next-step interpretation"
---

# APU P2 — stricter retrieval, fuller context, remaining misses

The reusable improvement now lives in the **APU product repository**, not only
in a corpus experiment: `createCorpusPassageReader(snapshot)` validates inert
copied sources and returns exact, complete bounded sections with source hashes.
It is an opt-in pure module. **The live librarian, providers and website do not
use it yet.** No permissions were increased.

Product implementation/test/documentation commit:
`7a39f33f6df839d2220f0f7c3e5edd2058d08fd8`.
[Product contract and limits](/Users/Yves/Documents/04_CODE/01_SKYZAI_LEVELS/L5_REFLECTION/APU/apu.bot/docs/pilots/2026-09-06-passage-reader.md).
This directory owns only the corpus-side evaluation and its history.

## What improved, and what did not

The new reader excludes notation-only matches, requires meaningful lexical
coverage, and refuses to clip a section beyond its context budget. It preserves
source declarations as declarations, not claim-level warrant. Neither a match
nor a complete section is presented as an answer or proof.

| Fresh challenge measurement | Frozen P1 | APU P2 |
|---|---:|---:|
| Supported questions with all required source lines included | 1/4 | 1/4 |
| Correct abstentions on the two no-support controls | 0/2 | 2/2 |
| Abstentions on supported questions (retrieval failures) | 0/4 | 3/4 |

The two controls ask for a merger quorum and Thailand passport validity. P2
returns no candidates; P1 returns lexical matches that do not supply those
answers. N4 finds the domain-specific rejection criteria and retains the
distinction between an empirical model failure and its analytic optimization
statement. N1–N3, concerning revocable sacrifice, authority and publication,
are missed by P2. These are **source/range tests, not a semantic answer score**.

On the already-revealed development set, required-range coverage rose from
1/12 to 5/12; correct no-support abstentions rose from 1/2 to 2/2. But expected
owner/range hits fell from 7/12 to 6/12, and supported-query abstentions rose
from 1/12 to 5/12. These are costs, not successes hidden inside an average.

The specific P1 problems remain visible:

- H5 now includes Power-Max lines 97–161: the selected corollary, strongest
  rivals and domain kill criteria travel together.
- H6 no longer mistakes `many` or the `C` in a temperature for topic evidence.
- H4 regresses: its valid deletion-duty passage fails the stricter lexical
  threshold. The reader's abstention does not mean that the source lacks an answer.
- Q4 hits its expected source but does not include every requested line. Even
  whole-section retrieval can miss conditions in neighbouring sections.

**Decision [I]:** retain the tested opt-in component, not a replacement for live
search and not evidence for additional autonomy. The next distinct experiment
should improve paraphrase retrieval while retaining no-support abstention,
conditions, contrary evidence and explicit uncertainty. These questions are now
revealed and cannot be reused as fresh held-out evidence.

## Custody and testing

The [runner](run.mjs) and [engine binding](engine-lock.json) were frozen in
`6c3a3773cb915d73dfd36d53aacead25f4c28060` after the product commit and before
the six [new questions](challenges.json) were revealed. L2 authored them in a
separate local context using two named sources; this is not independent external
validation. Code, thresholds and questions were not changed after reveal.

The [machine receipt](receipt.json) records every count, output manifest hash,
input revision and private output path. Two fresh processes produced identical
results **and receipts**. All 109 returned passage instances across both arms
reconstruct from the copied source text, line ranges and hashes; 25 are P2
instances. Integrity does not establish relevance or truth.

L3 independently checked those 109 slices, both manifests, aggregate counts and
the N4/H5 qualifications. Targeted review of all nine copied sources found no
support for N5/N6. L3 confirmed H4's false abstention and found no count, scope
or interpretation correction required here. This is a separate review context
in the same local environment, not external validation or user acceptance.

The generic APU module passes **18 focused tests**. A malformed non-string source
kind regression was observed failing before its fix. Review also rejected a
development attempt at plural folding and a 35% threshold: it recovered H4 but
conflated word endings and admitted weaker topic overlap. The frozen candidate
retains 45% with no stemming. Private development runs remain listed in the
receipt rather than being presented as held-out wins.

Full-app checks are not green: two changing-checkout runs reported respectively
446 and 452 passing tests with one copied-pilot custody failure. The concurrent
lane changed its packet and then its scope; neither was adopted or repaired in
this change. Typecheck, source lint and `git diff --check` passed at the recorded
checkpoints. No browser, full-app build, public-site gate or independent-user
acceptance is claimed for this unmounted module.

## Reproduce locally

Use Node 22 with type stripping and the existing pinned P0 inputs. A fresh P0
can be produced by the unchanged predecessor runner; its local dependency
closure is not fully pinned. The P2 runner reads the current generic module only
if it matches the exact engine lock; restore/review the named product revision
through normal custody if the module has since changed, never weaken the lock.

```sh
node 00_HANDOFF/2026_09_06_apu_readonly_pilot/run_pilot.mjs
node --experimental-strip-types 00_HANDOFF/2026_09_06_apu_relevance_pilot/run.mjs P0_OUTPUT_DIRECTORY 00_HANDOFF/2026_09_06_apu_relevance_pilot/challenges.json
```

The runner checks the completed P0 pathset/hashes, original source bytes and
HEAD at checkpoints, source revision/scope, engine digest, repeated query
equality and source-exact quotations. It writes only fresh private temporary
evaluation output, with completion last. Fetch/TCP guards observed zero calls;
these checks are **not an OS containment claim**. Temporary artifacts are not
durable custody; frozen code, input locks and questions make them reconstructable.

## Preserved boundaries

Foreign active APU edits (package, store, librarian, docs and preview) were left
alone. A concurrently edited Emergentism claim card and the pre-existing
`.hermes/` and `12_PUBLIC_SITE/output/` were excluded. Our work uses explicit,
separately reversible product and corpus commit groups; no broad cleanup.

Rosetta admission and local L2/L3 review occurred, with parent L4 as sole mutator.
Architecture/preservation/constitutional counsel was sequential within the
review, not seven independently recorded station outcomes. The A3 frozen-v0
drift remains HOLD; no writer retry, alternate recorder, reset or event mutation.

No model-provider call, source promotion, canonical claim change, website edit,
background loop, permission expansion, push or deployment. Earlier browser-policy
denial was not retried or worked around. This work improves a bounded component;
it does not make APU generally competent or authorized to act on its answers.
