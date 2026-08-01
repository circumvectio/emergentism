---
title: "Full corpus adjudication and coherence calibration — all 229 actionable findings receive custody"
status: "PASS-WITH-DEBT — all 229 actionable findings adjudicated; independent reviews and exact staged gate replay pass; named semantic and world-contact debts remain open"
date: 2026-08-01
evidence_tier: "[B] for hashed source/ledger identities, counts, repository changes, and executed checks; [I] for coherence calibration; [S] for selected scope and debt disposition"
owner: "01_EMERGENTISM"
parents:
  - ../../09_TOOLS/08_AUDIT_ARTIFACTS/2026_08_01_FIRST_60_ADJUDICATION.jsonl
  - ../../09_TOOLS/08_AUDIT_ARTIFACTS/2026_08_01_REMAINING_169_ADJUDICATION.jsonl
  - ../../09_TOOLS/08_AUDIT_ARTIFACTS/2026_08_01_REMAINING_169_INDEPENDENT_REVIEW_SUPPLEMENT.jsonl
  - ../../00_META/00_EMERGENTISM_INTERNAL_COMPLETION_REGISTER.md
  - ../../00_WORK_IN_PROGRESS/README.md
---

# Full corpus adjudication and coherence calibration

## Outcome at this boundary

The reconstructed 21-lane audit produced **261 findings**, of which **229 were
classified actionable**. All 229 now have durable adjudication custody:

| Slice | Durable result |
|---|---|
| First 60 actionable findings | 37 real; 23 false |
| Remaining 169, source-ledger repaired or already repaired | 54 `FIXED_PREEXISTING_OR_INHERITED`; 95 `FIXED_IN_THIS_ADJUDICATION`; 1 `RESOLVED_SOURCE_OWNER_ROUTE`; 2 `RESOLVED_SYNTAX_ONLY` |
| Remaining 169, not repair records | 8 `DISMISSED_FALSE`; 4 `DEDUPLICATED` |
| Remaining 169, explicitly constrained | 1 `FENCED_ACTIVE_PENDING_K3_ARCHIVE`; 2 `QUARANTINED_MISSING_CUSTODY`; 1 `OWNER_GATE_OPEN_TOPOLOGY`; 1 `OWNER_GATE_HELD_PUBLIC_DOCS` |

The independent review did not rewrite that ledger. It adds two controlling
corrections in a supplemental artifact:

| Finding | Source-ledger disposition | Reviewed disposition |
|---|---|---|
| 66 | `FIXED_IN_THIS_ADJUDICATION` | `SUPERSEDED_FROZEN_CUSTODY` — v1 stays byte-frozen; README/v2 own current counts |
| 183 | `FIXED_IN_THIS_ADJUDICATION` | `QUARANTINED_ACTIVE_TYPE_CONFLICT` — Foundation seat glossary repaired, but Titan arithmetic conflicts with `KSC-04` |

The effective reviewed partition of the remaining 169 is therefore: **151
repaired/resolved/safely superseded**, **8 dismissed false**, **4 deduplicated**,
and **6 explicitly constrained**. The numbers still sum to 169.

“Adjudicated” means that every actionable record has a reasoned disposition.
It does not mean every reported claim was true, every debt was editable, or
external validation occurred. The 37 real findings in the first slice were
translated back into source-level repair work; their final closure is included
in the independent review and staged-gate boundary below.

## Why all 21 lanes said `coherent: false`

The audit field was a **zero-defect lane Boolean**: one surviving issue made a
lane `false`. It was not a probability, a severity score, or a claim that every
sentence in a lane was incoherent. The result therefore supports two bounded
conclusions:

1. every sampled lane contained at least one item worth adjudicating; and
2. the field is too coarse to compare lanes or measure improvement after repair.

It does **not** support saying that all lanes were equally defective. Future
audits should report a typed profile instead of compressing four distinct
questions into one Boolean:

| Profile axis | Question | State at this candidate boundary |
|---|---|---|
| Semantic | Do current source owners agree on terms, tiers, types, and selected formulae? | **PASS-WITH-DEBT**; reviewed repair set passes, with Foundation typing and the docketed `KSC-02` active-projection sweep still open |
| Routing | Do front doors, mirrors, archives, and generated registers point to the correct owners? | **PASS-WITH-DEBT**; exact registers reproduce, with named topology/public-document owner gates held |
| Operational | Can declared compilers, tests, public builds, and formal checks reproduce the claimed state? | **PASS** at this local staged boundary; full corpus gate, Lean build, and deterministic public checks pass |
| World contact | Have independent observations or external reviewers returned outcomes that discriminate claims? | **Open**; no internal gate can close this axis |

## Reproducible custody

| Artifact | SHA-256 |
|---|---|
| First-60 adjudication ledger | `sha256:7ee2f5389d4d53c3142259f54a142390af96b19e982d53e082827eb024041e92` |
| Remaining-169 adjudication ledger | `sha256:af3520a7583148bc382538aa0595be6fb3611139ff6d02004bf98541540eb19f` |
| Remaining-169 independent-review supplement | `sha256:92931867a86b49a26f8629adb772770678d92ec4ac788c892bc768033e72bb7d` |
| Reconstructed raw findings | `sha256:93f72d87e899122c18945045f259a3223f101fa9df5187c721c32cd7fb805e6c` |
| Workflow journal | `sha256:b12986fb977ce6cfec0e38bd8fc134014d2ad35d4d650df6caa1a69d5908b0ca` |
| Source session | `sha256:0666bf47f049438301b17239cae26b393a14c1c5376c40505999abceab921c13` |

The two ledgers are corpus-durable `[B]` evidence. The raw reconstruction and
orchestration journals live outside the corpus; their hashes establish the
inputs used but do not turn those external paths into canonical owners. Ledger
rows are append-only evidence and must not be rewritten to flatter a later run.

## Independent review and checks

At the final staged boundary, the focused purity, work-in-progress, link,
claim-card, claim-graph, dimension-canon, Finity-boundary, foundation,
register-negative, R2-freeze, and staged-secret checks pass. An independent
18-file core review also passes after
repairing the residual checklist, meridian, etymology, probability, and
clinical-language seams. The first-60 review found no remaining semantic
P0/P1/P2 after repair; final register regeneration reproduces **3,405 files**
and **793 folders**, and the derivation replay reports **22,571 words across 21
Markdown files**. The remaining-169 review forced the two
supplemental corrections above and repaired the Matrix, `μ₀`, Flow,
Rosetta-tier, inventory, metadata, source-owner, and owner-gate seams it found.

The exact staged tree then passes the complete corpus gate: **18 top-level
controls**, **12 compiler suites**, and Lean formal verification via `lake
build`. The staged-secret scanner passes on the real patch and its six negative
controls pass. The deterministic public replay produces 12 chapters, 3,145
words, 107 RAG passages, and 312 frozen-boundary pages; predeployment passes
15/15 and the artifact gate passes all six artifact classes. Independent core,
first-60, remaining-169, and public-site reviews report no undocketed P0/P1/P2.
These are local repository and build results, not deployment or publication.

## Debt that remains visible

- One active tooling residue is fenced for archive-first removal in the next
  K3 sprint; it is not silently declared resolved here.
- The Foundation projection is on `CONFLICTED HOLD`: its Titan arithmetic is
  non-citable until rewritten against a separate typed algebra witness. `KSC-04`
  and the named K-1/K-5 source owners remain controlling.
- Active downstream projections still select or rank with the retired product
  despite `KSC-02` selecting `min`. The exact owner-aware sweep is docketed as
  `KSC-02-ACTIVE-PROJECTION-DRIFT` for the immediately following sprint.
- Two findings name files whose claimed custody could not be found. They remain
  quarantined rather than reconstructed from inference.
- One topology decision and one frozen-public-document decision remain owner
  gates. This receipt does not consume either decision.
- Empirical calibration, independent replication, publication, deployment,
  contracts, and legal signature are separate consequences. None is implied by
  a local test or commit, and none is performed by this receipt.

## Kill criterion

This receipt fails if any durable ledger count or hash above cannot be
reproduced, if a first-60 real finding lacks an implemented or explicitly held
disposition, if the staged gate does not pass, or if later review shows that a
claimed repair merely hid the contradiction. A failure becomes a new dated
record; it is not edited out of this one.

---

*The audit is complete when every finding has custody; the project is complete
only to the exact boundary named. Internal coherence is not world contact.*
