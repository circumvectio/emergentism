---
title: "RETRACTED_126 Disposition v0.1 — category-level analysis of 79 findings"
date: 2026-07-18
status: "[D] draft — category-level analysis; per-finding review of the 31 LIVE candidates is parked for follow-up V-forcers"
evidence_tier: "[S] the disposition evidence (each line is `[S]`-seen-on-disk); [D] the policy is staged"
owner: "K2 (Yves R. Burri). K2 signs the category-level disposition; per-finding K2 disposition is downstream."
parents:
  - 00_META/00_PER_DOC_FIX_PATTERN_v0.1.md
  - 00_META/00_PER_DOC_FIX_LOG_v0.1.md
  - 00_META/00_PROPAGATION_SWEEP_REPORT_v0.1.md
  - 00_META/00_SETTLED_CANON_REGISTRY.md
---

# RETRACTED_126 Disposition v0.1

> Category-level analysis of the **79 RETRACTED_126 findings** from `00_META/00_PROPAGATION_SWEEP_REPORT_v0.1.md`. The findings are dominated by the **audit-trail-ledger mode** (the audit *is* the over-claim record); the per-finding review class is smaller than the prior estimate of "~5 live" suggested — this analysis corrects that to **31 candidates**.

## 1. The 79 findings by mode

| Mode | Count | Disposition (default) | Why |
|---|---|---|---|
| **audit-trail-ledger** | 33 | FALSE-POSITIVE | The doc *is* the audit of the over-claim; the term is cited as the over-claim that was retracted. The audit ledger is the K3 durable record. |
| **pending-K2** | 4 | FALSE-POSITIVE | Filename `*PENDING_K2*` — the doc explicitly awaits K2 disposition; the term is cited as the over-claim under review. |
| **session-packet** | 3 | FALSE-POSITIVE | Historical session record (`60_SESSION_PACKETS/*`); the term is cited as a position that was later retracted. |
| **registry-citation** | 8 | FALSE-POSITIVE | The registry / covenant *must* mention the term to specify what's dead; the citation is the spec. |
| **per-finding review (LIVE candidates)** | 31 | **DEFER** | Formal-system, root-canon, papers, or root-level summaries. The doc may or may not have a Kintsugi banner; the over-claim may or may not be in a tombstoned section. Per-finding review required. |
| **TOTAL** | **79** | 48 FALSE-POSITIVE / 31 DEFER | |

**Correction to the prior estimate:** `00_META/00_PER_DOC_FIX_LOG_v0.1.md §1` estimated ~5 live for RETRACTED_126. The category-level analysis here raises that to **~31 candidates that need per-finding review**. The audit-trail class is large (33) but the candidate class is also substantial. **The rate analysis is updated accordingly: ~48/79 = 61% false-positive (vs. the prior 89% estimate); ~31/79 = 39% candidates for per-finding review (vs. ~6%).**

## 2. The 48 FALSE-POSITIVE (audit-trail + pending-K2 + session-packet + registry-citation)

**Audit-trail ledgers (33):** the audit *is* the over-claim record.

| Doc | Count |
|---|---|
| `11_UPLINK/50_AUDITS_AND_EXECUTIONS/110_FORMAL_LOGIC_AUDIT_APPLY_THREE_GOLDEN_SEAMS_PENDING_K2.md` | 8 |
| `11_UPLINK/50_AUDITS_AND_EXECUTIONS/107_THE_OPEN_LOOP_D6_D0_CLOSURE_PENDING_K2.md` | 8 |
| `11_UPLINK/50_AUDITS_AND_EXECUTIONS/73_BRAHMANA_STRUCTURAL_AUDIT_2026_05_04.md` | 3 |
| `11_UPLINK/50_AUDITS_AND_EXECUTIONS/72_VAISYA_TIER_AUDIT_2026_05_04.md` | 2 |
| `11_UPLINK/50_AUDITS_AND_EXECUTIONS/126_WELTANSCHAUUNG_FORMAL_AUDIT_2026_07_13.md` | 2 |
| `08_FRAMEWORK_SUPPORT/01_GOVERNANCE/02_REPORTS/FOUNDATION_LOGIC_AUDIT_2026_04_19.md` | 6 |
| `11_UPLINK/50_AUDITS_AND_EXECUTIONS/63_RUMINATION_UPLINK_2026_04_23.md` | 1 |
| `11_UPLINK/50_AUDITS_AND_EXECUTIONS/128_EMERGENTIST_COMPASS_EXTERNAL_CALIBRATION_2026_07_18.md` | 1 |
| `11_UPLINK/50_AUDITS_AND_EXECUTIONS/112_AMRITA_REFINEMENT_SPEC_FIVE_MOVES_PENDING_K2.md` | 1 |
| `11_UPLINK/50_AUDITS_AND_EXECUTIONS/104_DIMENSIONAL_MAP_ADJUDICATION_K2_ACCEPTANCE_2026_07_10.md` | 1 |
| **Subtotal** | **33** |

**Pending K2 (4):** the doc explicitly awaits K2 disposition.

| Doc | Count |
|---|---|
| `08_FRAMEWORK_SUPPORT/03_EVIDENCE/PARADOX_DISSOLUTIONS/00_THE_LENS_AS_COMPASS_PENDING_K2.md` | 4 |

**Session packets (3):** historical session record.

| Doc | Count |
|---|---|
| `11_UPLINK/60_SESSION_PACKETS/159_TIER_A_ROSETTA_DRAFT_PACK_2026_04_24.md` | 1 |
| `11_UPLINK/60_SESSION_PACKETS/143_SEVENFOLD_FOUNDATION_ROOT_REORGANIZATION_2026_04_24.md` | 1 |
| `11_UPLINK/60_SESSION_PACKETS/137_F5_EKTROPY_THE_FIFTH_FORCE_STRONG_FORM_DRAFT_2026_04_24.md` | 1 |
| **Subtotal** | **3** |

**Registry citation (8):** the spec must mention the term to forbid.

| Doc | Count |
|---|---|
| `00_META/00_SETTLED_CANON_REGISTRY.md` | 5 |
| `00_META/00_THE_OPEN_CANON_COVENANT.md` | 3 |
| **Subtotal** | **8** |

**Action for the 48 FALSE-POSITIVE:** **no in-doc edit.** The audit-trail-ledger mode is the durable K3 record of the over-claim's retirement; the pending-K2 files are explicit dispositions; the session-packets are historical; the registry-citations are the spec. Documented in this disposition; the per-doc fix log row for these findings is "FALSE-POSITIVE by mode — no in-doc edit."

## 3. The 31 candidates for per-finding review

These findings are in **formal-system docs, root-canon summaries, papers, and root-level overviews**. The doc may or may not have a Kintsugi banner; the over-claim may or may not be in a tombstoned section. **Per-finding review is the disposition path.**

| Doc | Count | Notes (likely-class, not verdict) |
|---|---|---|
| `05_COSMOLOGY/00_THE_GEOMETRIC_ONTOLOGY_OF_REALITY.md` | 7 | High count — likely a tombstoned section; needs review |
| `05_COSMOLOGY/00_THE_COMPLETE_ONTOLOGY_OF_REALITY.md` | 4 | Same — needs review |
| `05_COSMOLOGY/03_FORMAL_SYSTEM/41_UNIFIED_DIMENSIONAL_DERIVATION.md` | 2 | Includes 4-force bijection; KSC-04 / KSC-05 territory |
| `05_COSMOLOGY/03_FORMAL_SYSTEM/23_DIMENSIONAL_CLOSURE_PROOF.md` | 1 | KSC-03 source doc; likely tombstoned, needs review |
| `05_COSMOLOGY/03_FORMAL_SYSTEM/27_DIMENSIONAL_ARCHITECTURE_CLARIFICATION.md` | 1 | KSC-03 source doc; same |
| `05_COSMOLOGY/03_FORMAL_SYSTEM/00_THE_SEVEN_AXIOMS.md` | 1 | High-importance doc; needs review |
| `05_COSMOLOGY/00_EMERGENTISM.md` | 2 | Root-level cosm doc; needs review |
| `05_COSMOLOGY/00_THE_ARGUMENT_EMERGENCE_AS_LENS_ON_DASEIN.md` | 1 | Same |
| `08_FRAMEWORK_SUPPORT/02_OPERATORS/SPHERE_DERIVATIONS/MF_65_Curvature_Transition.md` | 2 | Sphere-derivation paper; needs review |
| `08_FRAMEWORK_SUPPORT/02_OPERATORS/MF_ADVANCED/MF_283_The_Orthogonality_Theorem_v2.md` | 1 | Same |
| `08_FRAMEWORK_SUPPORT/00_META/00_MAGNUM_OPUS/00_MAGNUM_OPUS_REVIEW.md` | 1 | Magnum Opus review; needs review |
| `03_METHODOLOGY/02_THE_PAPERS/PEER_REVIEW_PROGRAM/00_COSMOLOGY_AND_CONSTITUTION_AUDIT.md` | 1 | Paper; needs review |
| `03_METHODOLOGY/02_THE_PAPERS/PEER_REVIEW_PROGRAM/00_AXIOMS_AND_STATUS.md` | 1 | Paper; needs review |
| `03_METHODOLOGY/02_THE_PAPERS/FINITY_PAPERS/SUDA_DIMENSIONAL_CROSS_REFERENCE.md` | 1 | Paper; needs review |
| `03_METHODOLOGY/01_THE_DERIVATION/01_BURRI_RULES_DERIVATION_LEDGER.md` | 1 | Derivation ledger; needs review |
| `01_TELEOLOGY/01_F5_FORCE_MAP_AND_EKTROPY.md` | 1 | F5 territory; KSC-05 / F5 ruling intersection |
| `01_TELEOLOGY/00_THE_GENERATIVE_LAGRANGIAN.md` | 1 | Same |
| `00_THE_AMRITA.md` | 1 | High-importance root doc; needs review |
| `00_CONTROL/PRIMETIME_AUDIT/02_SPRINT_1_VERDICT.md` | 1 | Primetime audit; needs review |
| **Subtotal** | **31** | |

**Action for the 31 candidates:** **per-finding review, parked.** Each candidate is a future V-forcer. The disposition for each is one of LIVE / FALSE-POSITIVE / DEFER per the per-doc fix pattern. The estimated live rate among these 31 is ~30–50% (vs. the original ~6% estimate) — higher because these are the docs that *don't* self-flag as audit-trail.

## 4. The 3 4-force bijection findings

The 4-force bijection is a separate retracted item (3 findings total), distinct from D6≡D0. Distribution:

| Doc | Disposition (default) |
|---|---|
| `00_META/00_SETTLED_CANON_REGISTRY.md:56` | FALSE-POSITIVE — registry citation |
| `11_UPLINK/50_AUDITS_AND_EXECUTIONS/126_WELTANSCHAUUNG_FORMAL_AUDIT_2026_07_13.md:40` | FALSE-POSITIVE — audit-trail |
| `05_COSMOLOGY/03_FORMAL_SYSTEM/41_UNIFIED_DIMENSIONAL_DERIVATION.md:38` | DEFER — per-finding review |

**Action for the 4-force bijection:** 2 FALSE-POSITIVE by mode (registry, audit-trail); 1 DEFER for per-finding review. Same pattern as D6≡D0.

## 5. Disposition summary

| Disposition | Count | % of 79 |
|---|---|---|
| **FALSE-POSITIVE** (audit-trail + pending-K2 + session-packet + registry-citation) | 48 | 61% |
| **DEFER** (per-finding review of 31 candidates) | 31 | 39% |
| **LIVE** (in-doc edits applied in this V-forcer) | 0 | 0% |

**The 0-LIVE outcome for this V-forcer is the right discipline.** Per the per-doc fix pattern, per-finding review is required for the 31 candidates; doing it in one V-forcer would either skip the review (violating the pattern) or expand scope beyond the convergence-memo's "one V-forcer, one commit, stop" rule. The category-level disposition is the deliverable; the per-finding reviews are downstream.

## 6. Parking lot (per-finding review of 31 candidates)

Per the convergence-memo, the per-finding review of the 31 candidates is a sequence of follow-up V-forcers, not a single sprint. Each V-forcer can take one of these shapes:

- **Per-doc V-forcer:** for a high-finding-count doc (e.g., `05_COSMOLOGY/00_THE_GEOMETRIC_ONTOLOGY_OF_REALITY.md` with 7 findings), one V-forcer dispositions all 7 with a single in-doc edit (or a doc-level Kintsugi banner if applicable).
- **Per-topic V-forcer:** group candidates by topic (e.g., all KSC-03 closure-related findings in formal-system docs as one V-forcer with a unified Kintsugi banner addition).
- **Batched per-finding V-forcer:** if the candidates are independent and small, batch 3-5 dispositions per V-forcer with their per-finding log rows.

**Recommendation:** start with the per-doc V-forcer for `05_COSMOLOGY/00_THE_GEOMETRIC_ONTOLOGY_OF_REALITY.md` (highest count, 7 findings). Spot-check whether the doc has a Kintsugi banner; if so, the doc-level disposition is FALSE-POSITIVE (banner is the fix) and the V-forcer is a single log entry. If not, the V-forcer is the banner addition + log row.

## 7. The K2 sign line

```text
☐ I sign this disposition — the category-level analysis of the 79 RETRACTED_126
  findings is approved: 48 FALSE-POSITIVE by mode, 31 DEFER for per-finding
  review, 0 LIVE in this V-forcer. The per-finding review of the 31 candidates
  is parked for follow-up V-forcers per §6.

  K2 (Yves R. Burri): __________________________   Date: __________
```

---

*This disposition is the category-level audit. Per-finding reviews are downstream. K2 signs the category-level analysis; per-finding K2 disposition follows.*
