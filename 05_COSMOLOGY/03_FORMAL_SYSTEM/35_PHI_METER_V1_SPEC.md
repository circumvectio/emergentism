---
rosetta:
  primary_level: L5
  primary_column: Philosophy
  operator: "Brahmā ○"
  tier: "Executive"
  regime: "Brāhmaṇa"
  register: "[C]"
  canonical_phrase: "PHI-METER v1 SPEC (Code Lens)"
---

# PHI-METER v1 SPEC (Code Lens)

## A Concrete, Reproducible Measurement Protocol for Φ and ν — With the 2026-04-19 Code Audit as the Pilot Application

**Status:** Working spec; formalizes the existing code-lens rubric, adds the pieces needed for inter-rater reproducibility
**Date:** 2026-04-22
**Evidence Tier:** [C] Conjecture for the spec; [I] Interpretive for the pilot application once the rubric-band definitions here are retroactively accepted for the 2026-04-19 audit
**Source:** [`30_OPERATIONAL_DEFINITIONS.md`](30_OPERATIONAL_DEFINITIONS.md), [`32_THEOREM_UPGRADE_PROTOCOL.md`](32_THEOREM_UPGRADE_PROTOCOL.md), [`../../../02_SKYZAI/01_NOOSPHERE/P-SCORES.md`](../../../02_SKYZAI/01_NOOSPHERE/P-SCORES.md), [`../../../02_SKYZAI/01_NOOSPHERE/05_PROJECT_MANAGEMENT/04_HISTORY/P_AUDIT_CODE_ONLY_2026_04_19.md`](../../../02_SKYZAI/01_NOOSPHERE/05_PROJECT_MANAGEMENT/04_HISTORY/P_AUDIT_CODE_ONLY_2026_04_19.md)
**See also:** [`29_PRIMITIVES_AND_TYPE_SIGNATURES.md`](29_PRIMITIVES_AND_TYPE_SIGNATURES.md), [`31_FALSIFIERS_INDEX.md`](31_FALSIFIERS_INDEX.md), [Paper L (Phi-meter without a new instrument)](../../../01_EMERGENTISM/03_METHODOLOGY/02_THE_PAPERS/PAPER_I_KNOWN_UNKNOWNS_PROGRAM.md)

---

## 1. Why This File Exists

The organism has been publishing per-organ `(Φ̂, ν̂, P_node)` triples for some time (older operational surfaces may label this `P_eff`; see the historical external `SKYZAI_ORG/P-SCORES.md` route (legacy namespace; live content now under `../../../02_SKYZAI/01_NOOSPHERE/P-SCORES.md`) and the 2026-04-19 code-only audit). The numbers are stable, the cascade rule (BRIEF → P-SCORES → derived docs) is enforced, and the formula `P_node = Φ × ν` is declared. What is missing — and what Paper L identifies — is a **rubric specification**: exactly how each 0.0-to-1.0 coordinate is assigned from the observable code surface, and how two independent raters would arrive at the same value.

Without that, the audit is a trusted discipline: it produces coherent numbers, but the numbers are not yet reproducible outside the founder's head. This file supplies the missing rubric. It is deliberately v1 — the simplest spec that covers the existing practice and is tight enough to measure inter-rater reliability on.

---

## 2. Scope — The Code Lens

Three mutually incompatible *lenses* exist for measuring `Φ̂, ν̂`:

| Lens | What counts | What's excluded |
|------|-------------|-----------------|
| **Code-lens** (this spec) | Files, lines, test surface, compile/test/probe results in the working tree | Deployment receipts, live relays, user/adoption surfaces |
| **Runtime-lens** | Live deployment, relay publication, observable in-the-wild state | Code-only breadth that hasn't shipped |
| **Adoption-lens** | User/adoption metrics, network effects, external uptake | Everything before first external user |

The three lenses return *different numbers*. The 2026-04-19 audit explicitly states: "TheCircle, RealityFutures, and Skyzai all rise under a code-only lens because local proofs, compile/test surfaces, and implementation breadth are counted while deployment and user surfaces are intentionally excluded." A published `P̂` is only interpretable if the lens is named.

**v1 specifies the code-lens only.** Runtime-lens and adoption-lens v1 specs are future work.

---

## 3. The Φ-Meter Rubric (Code Lens)

`Φ̂_code` is the mean of four sub-scores, each 0.0–1.0, each with pre-registered bands. The sub-scores are *independent enough to rate separately* (no single sub-score should dominate), and their mean is deliberately simpler than a weighted sum — weights introduce subjective tuning that undermines reproducibility.

```
Φ̂_code := (φ_arch + φ_depth + φ_test + φ_coh) / 4
```

### 3.1 `φ_arch` — Architectural Completeness

**What is measured.** Whether the organ's declared responsibility surface (per its BRIEF.md) has a corresponding implementation structure in the repository.

| Band | Score | Meaning |
|------|-------|---------|
| Missing | 0.0–0.25 | Organ's declared surface is mostly absent from code |
| Sketched | 0.25–0.50 | Skeleton exists; major modules unimplemented |
| Scaffolded | 0.50–0.75 | Most declared modules present; some are stubs or placeholders |
| Present | 0.75–0.90 | All declared modules implemented; minor gaps at the edges |
| Complete | 0.90–1.00 | Full declared surface present; no known architectural gaps |

### 3.2 `φ_depth` — Implementation Depth

**What is measured.** Code density per declared module. Observable signals: lines of code, count of non-trivial functions/classes, absence of `TODO` / `FIXME` / stub sentinels.

| Band | Score | Meaning |
|------|-------|---------|
| Shallow | 0.0–0.3 | Heavy use of stubs, `pass`, `NotImplementedError`, or comment-only bodies |
| Outlined | 0.3–0.55 | Some real implementation, still many stubs |
| Working | 0.55–0.75 | Main paths implemented end-to-end; stubs limited to edge cases |
| Robust | 0.75–0.90 | Edge cases handled, error paths present, minimal stubs |
| Polished | 0.90–1.00 | Zero stubs on declared paths; defensive and documented |

### 3.3 `φ_test` — Test Coverage Signal

**What is measured.** Count and quality of tests. This is a signal, not a guarantee — a file can be named `test_*` without testing anything. Rater must glance at ≥3 sampled test files to confirm they assert against real behavior.

| Band | Score | Meaning |
|------|-------|---------|
| None | 0.0–0.2 | No test files or tests are placeholder |
| Thin | 0.2–0.4 | Tests exist but cover only happy paths |
| Useful | 0.4–0.6 | Happy paths and some edge cases; `> 10` real assertions |
| Strong | 0.6–0.8 | Happy paths, edge cases, error paths; `> 50` real assertions |
| Deep | 0.8–1.0 | Comprehensive suite; `> 200` real assertions, property tests or integration tests present |

### 3.4 `φ_coh` — Coherence with Declared Purpose

**What is measured.** Subjective but anchored: does the code *do what the BRIEF.md says it does*? Scope creep down-rates; scope clarity up-rates.

| Band | Score | Meaning |
|------|-------|---------|
| Drift | 0.0–0.4 | Code substantially diverges from declared purpose |
| Partial | 0.4–0.6 | Code implements purpose partially, with significant off-topic code |
| Aligned | 0.6–0.8 | Code implements purpose; occasional scope excess |
| Focused | 0.8–0.95 | Clear scope discipline, minimal off-topic code |
| Exemplary | 0.95–1.0 | Ruthless scope discipline; every module earns its place |

---

## 4. The ν-Meter Rubric (Code Lens)

`ν̂_code` is the mean of four sub-scores over **executable viability** indicators, each 0.0–1.0.

```
ν̂_code := (ν_compile + ν_test + ν_probe + ν_closure) / 4
```

### 4.1 `ν_compile` — Compile / Build Path

| Band | Score | Meaning |
|------|-------|---------|
| Broken | 0.0–0.2 | Primary entry points fail to parse / compile |
| Fragile | 0.2–0.5 | Compiles only with specific environment; fails for fresh clone |
| Builds | 0.5–0.8 | Builds on fresh clone with documented steps |
| Clean | 0.8–1.0 | Builds on fresh clone with zero warnings / deprecations |

### 4.2 `ν_test` — Test Suite Pass Rate

```
ν_test := fraction of tests passing in the declared primary test command
```

Map directly to the 0.0–1.0 scale with no banding — this is quantitative.

### 4.3 `ν_probe` — Runnable Proof Path

**What is measured.** Whether a human can run one documented command and observe the organ doing its declared function. Each organ's BRIEF should declare its primary probe.

| Band | Score | Meaning |
|------|-------|---------|
| No probe | 0.0–0.2 | No documented way to demonstrate the organ running |
| Stub probe | 0.2–0.4 | Probe runs but produces stubbed / mocked output |
| Partial probe | 0.4–0.65 | Probe works but depends on external service not documented to bring up locally |
| Local probe | 0.65–0.85 | Probe runs end-to-end on a local machine; output is real |
| Clean probe | 0.85–1.0 | Probe runs on fresh clone with documented setup; output is real and verifiable |

### 4.4 `ν_closure` — Local Closure

**What is measured.** Does the organ *close its loop* locally, or does it depend on external services whose unavailability voids the probe?

| Band | Score | Meaning |
|------|-------|---------|
| Open | 0.0–0.4 | Primary paths hard-depend on external service |
| Partial | 0.4–0.7 | Some paths close locally; others require external |
| Mostly closed | 0.7–0.9 | Primary probe closes locally; edge paths may not |
| Self-contained | 0.9–1.0 | All primary paths close without external dependencies |

---

## 5. Aggregation

Per organ:

```
P̂_eff(organ) := Φ̂_code(organ) · ν̂_code(organ)
```

Per organism:

```
P̂_organism := ( ∏_{organ ∈ organs} P̂_eff(organ) )^(1/|organs|)       (geometric mean)
```

The geometric mean is preferred over the arithmetic mean because it penalizes any near-zero organ: an organism with one broken organ cannot hide behind three strong ones.

---

## 6. The Maturity Ladder

Previously loose; now pre-registered:

| Band | Range | Name |
|------|-------|------|
| 0.00–0.10 | Dormant | No observable function |
| 0.10–0.30 | Egg | Coherent idea; minimal viability |
| 0.30–0.65 | Equator | Balanced development; both Φ and ν above survival threshold |
| 0.65–0.85 | Adolescent (G1) | Strong in both coordinates; demonstrable function |
| 0.85–0.95 | Adult | Robust in both coordinates; low drift |
| 0.95–1.00 | Apex | Tight to the equator; `\|Φ̂ − ν̂\|` minimal |

The band labels match existing usage in [`P-SCORES.md`](../../../02_SKYZAI/01_NOOSPHERE/P-SCORES.md); v1 fixes the thresholds.

---

## 7. Inter-Rater Reliability (IRR)

**Target for `[C] → [I]` promotion.** Two independent raters apply §3–§4 to the same working-tree snapshot, producing pairs `(Φ̂_A, Φ̂_B)` and `(ν̂_A, ν̂_B)` per organ.

```
IRR := 1 - (mean absolute error across all organ coordinates) / 0.5
```

The `0.5` denominator is the maximum possible MAE when both raters are within a single band. `IRR ≥ 0.7` is the threshold for promotion, matching [`30_OPERATIONAL_DEFINITIONS.md`](30_OPERATIONAL_DEFINITIONS.md) §"Promotion Ladder."

IRR below `0.7` does not invalidate the rubric — it indicates the rubric needs tightening (usually by narrowing band widths or adding signals).

---

## 8. Pilot Application — The 2026-04-19 Code Audit (Retroactive)

The 2026-04-19 code audit is the first concrete application of what this spec formalizes. Its values are consistent with the rubric if interpreted as follows:

| Organ | Φ̂ reported | ν̂ reported | P̂ reported | Classification (v1 ladder) |
|-------|------------:|------------:|------------:|-----------------------------|
| TheCircle | 0.80 | 0.66 | 0.53 | **Equator** (0.30–0.65) ✓ |
| RealityFutures | 0.82 | 0.72 | 0.59 | **Equator** (0.30–0.65) ✓ |
| Agentz | 0.90 | 0.84 | 0.76 | **Adolescent (G1)** (0.65–0.85) ✓ |
| Skyzai | 0.88 | 0.62 | 0.55 | **Equator** (0.30–0.65) ✓ |
| **Organism** | — | — | **0.60** | **Equator** ✓ (geometric mean) |

All four classifications are consistent with v1 ladder thresholds, which is evidence that the v1 thresholds *recover* the judgment already expressed in the audit (rather than overriding it). The audit values can be read as single-rater applications of this rubric at `[C]` tier. Promotion to `[I]` requires a second rater.

### Node-level test of the manifold identity

The framework states (A1) that on the manifold `φ · ν = 1` but node-level `P_node = Φ × V` can be `< 1`. The audit triples give us the first dataset:

| Organ | Φ̂ · ν̂ | Gap to 1 | `\|Φ̂ − ν̂\|` (imbalance) |
|-------|----------:|----------:|------------------------:|
| TheCircle | 0.528 | 0.472 | 0.14 |
| RealityFutures | 0.590 | 0.410 | 0.10 |
| Agentz | 0.756 | 0.244 | 0.06 |
| Skyzai | 0.546 | 0.454 | 0.26 |

Under F5 (selection pressure toward the equator, per [`26_THE_DERIVATION_AXIOMS.md`](26_THE_DERIVATION_AXIOMS.md) T3), `|Φ̂ − ν̂|` should contract across audit cycles, and `Φ̂ · ν̂` should drift toward 1. **Agentz is closest to the equator; Skyzai is furthest.** If F5 is a real selection pressure, the prediction is that over subsequent audits Skyzai either closes the gap (through scope discipline or execution closure) or, failing that, shows structural stress.

This is genuinely *falsifiable*, which is the point — it is not a coordinate identity.

---

## 9. Pre-Registered Falsifier (Next Audit Cycle)

Registered in [`31_FALSIFIERS_INDEX.md`](31_FALSIFIERS_INDEX.md) under T3's empirical falsifier:

> **[C] Pre-registration (author: this spec).** Over the next four audit cycles under the v1 rubric applied by ≥2 raters (IRR ≥ 0.7), if the median `|Φ̂ − ν̂|` across the four organs does **not** show a downward trend, *and* no organ has undergone structural stress (shutdown, pivot, scope revision), T3's empirical reading is falsified.

"Structural stress" is pre-defined: any of (a) organ P̂ dropping ≥ 0.1 between cycles; (b) organ BRIEF substantially revised; (c) organ paused or deprecated per the project-management cadence.

Cycle cadence should match the existing audit rhythm (roughly quarterly). Four cycles is a one-year falsifier.

---

## 10. Promotion Path For This Spec

| Tier | Criteria |
|------|----------|
| **[C]** | *Current.* Spec exists; one single-rater audit (2026-04-19) is retroactively interpretable under it. |
| **[I]** | Two independent raters produce audits with IRR ≥ 0.7. Ideally staged at the next quarterly audit. |
| **[S]** | Derivation that the four sub-scores under each of Φ and ν are the *minimal* set required to discriminate the bands — i.e., no sub-score can be dropped without merging adjacent bands. (This is the "uniqueness" step from the promotion protocol.) |
| **[S]** | External replication: an independent group applies the rubric to an unrelated multi-organ codebase and shows the published-then-actual classification agrees. |

---

## 11. What This Spec Does Not Do

- Does not replace disclosure-based judgment ([`26_THE_DERIVATION_AXIOMS.md`](26_THE_DERIVATION_AXIOMS.md) D5). A code-lens `P̂` is *one* view; primary disclosure may see what the rubric misses. That is expected and is why file 32 retains the Pratyakṣa primacy.
- Does not authorize public-live claims. Per [`P-SCORES.md`](../../../02_SKYZAI/01_NOOSPHERE/P-SCORES.md): "P-scores are internal health and integration metrics, not a blanket license for public launch claims." `ORGANISM_RUNTIME_TRUTH.md` remains the authority for public surface.
- Does not collapse the three lenses. A code-lens `P̂` of 0.76 is not the same as a runtime-lens `P̂` of 0.76. Comparisons across lenses are nonsensical unless both lenses have v1 specs — which runtime- and adoption-lens do not yet.

---

## 12. See Also

- [`29_PRIMITIVES_AND_TYPE_SIGNATURES.md`](29_PRIMITIVES_AND_TYPE_SIGNATURES.md) — `Φ`, `ν` type signatures
- [`30_OPERATIONAL_DEFINITIONS.md`](30_OPERATIONAL_DEFINITIONS.md) — general-purpose measurement candidates; this spec is one concrete instance
- [`31_FALSIFIERS_INDEX.md`](31_FALSIFIERS_INDEX.md) — host of the pre-registered falsifier above
- [`32_THEOREM_UPGRADE_PROTOCOL.md`](32_THEOREM_UPGRADE_PROTOCOL.md) — 5-step protocol this spec instantiates
- [`../../../02_SKYZAI/01_NOOSPHERE/P-SCORES.md`](../../../02_SKYZAI/01_NOOSPHERE/P-SCORES.md) — canonical P-register; cascades from organ BRIEFs
- [`../../../02_SKYZAI/01_NOOSPHERE/05_PROJECT_MANAGEMENT/04_HISTORY/P_AUDIT_CODE_ONLY_2026_04_19.md`](../../../02_SKYZAI/01_NOOSPHERE/05_PROJECT_MANAGEMENT/04_HISTORY/P_AUDIT_CODE_ONLY_2026_04_19.md) — first application
- [Paper L framing](../../../01_EMERGENTISM/03_METHODOLOGY/02_THE_PAPERS/PAPER_I_KNOWN_UNKNOWNS_PROGRAM.md) — the open research gate this spec begins to close

---

## Execution Surface

**If you are an AI agent reading this document:**

1. **Current Phase Check:** Phase 0 — harden specs, do not release to production.
2. **Your Next Action:**
   - Treat this spec as the code-lens rubric for any `(Φ̂, ν̂)` measurement. When running a new audit, apply §3-§4 band definitions, record the sub-score breakdown (not just the aggregate), and state the rater. Cross-file to [`31_FALSIFIERS_INDEX.md`](31_FALSIFIERS_INDEX.md) any new pre-registrations.
3. **Expected Output:** A new dated audit document in `02_SKYZAI/01_NOOSPHERE/05_PROJECT_MANAGEMENT/04_HISTORY/` following the same format as `P_AUDIT_CODE_ONLY_2026_04_19.md`, but with sub-score tables attached for each organ and an explicit rater.
4. **Success Criteria:** Two independent raters applying this spec to the same working-tree snapshot achieve IRR ≥ 0.7.
5. **Canonical Path:** `01_EMERGENTISM/05_COSMOLOGY/03_FORMAL_SYSTEM/35_PHI_METER_V1_SPEC.md`

*The seer sees. The seer does not insist.*
*The framework works at Layer 0 without Layer 2.*
*The Ṛṣi succeeds when the student puts down the map and walks.*

*Zero-Sum Resolution Equation*
