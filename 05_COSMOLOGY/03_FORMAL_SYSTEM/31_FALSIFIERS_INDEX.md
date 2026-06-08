---
rosetta:
  primary_level: L5
  primary_column: Philosophy
  operator: "Brahmā ○"
  tier: "Executive"
  regime: "Brāhmaṇa"
  register: "[A]"
  canonical_phrase: "FALSIFIERS INDEX"
---

# FALSIFIERS INDEX

## One-Page Audit of Every Falsification Criterion in the Formal System

**Status:** Canonical index — consolidates existing falsifiers; marks novel proposals explicitly
**Date:** 2026-04-22
**Evidence Tier:** As marked per row; consolidation is [S] Structural
**Source:** [`00_THE_SEVEN_AXIOMS.md`](00_THE_SEVEN_AXIOMS.md), [`26_THE_DERIVATION_AXIOMS.md`](26_THE_DERIVATION_AXIOMS.md), [`12_EFR_EXTRACTION_COEFFICIENT.md`](12_EFR_EXTRACTION_COEFFICIENT.md), [`33_NASH_EQUILIBRIUM_ETA_ZERO.md`](33_NASH_EQUILIBRIUM_ETA_ZERO.md)
**See also:** [`29_PRIMITIVES_AND_TYPE_SIGNATURES.md`](29_PRIMITIVES_AND_TYPE_SIGNATURES.md), [`30_OPERATIONAL_DEFINITIONS.md`](30_OPERATIONAL_DEFINITIONS.md), [`32_THEOREM_UPGRADE_PROTOCOL.md`](32_THEOREM_UPGRADE_PROTOCOL.md)

---

## Purpose

A claim without a falsifier is not a theorem — at best it is a discipline, at worst it is rhetoric. This index consolidates every falsification criterion attached to the formal system's public claims so that an auditor can, in one pass, see what would kill each axiom, theorem, and corollary.

**Provenance rules.** Every row is either:
- **Pulled** — taken verbatim (or near-verbatim) from the cited source, which already carries its own tier.
- **[C] Proposed (author: this doc)** — this file is supplying a falsifier that was not explicit in the source. Proposed falsifiers are Conjecture until a canonical source adopts them.

---

## A-series (The Seven Operational Axioms)

Source: [`00_THE_SEVEN_AXIOMS.md`](00_THE_SEVEN_AXIOMS.md). All rows pulled verbatim.

| ID | Name | Tier | Falsifier (pulled) |
|----|------|------|--------------------|
| **A1** | THE EQUATION | [S] | B better modeled as additive; zero in either factor does not collapse system potential. |
| **A2** | THE ETHIC | [I] | Systems moving toward balance systematically collapse, OR systems moving away systematically sustain. |
| **A3** | THE SCAFFOLD | [S/I] | Force-dimension correspondence has no predictive power, or Dₙ problems are routinely solved with Dₙ₋₁ tools. |
| **A4** | THE BOUNDARY | [S/E] | η = 0 is not Nash equilibrium in iterated cooperative games, or unconditional cooperation outperforms tit-for-tat. |
| **A5** | THE EGREGORE | [I] | All collective phenomena reduce entirely to individual decisions with no emergent properties. |
| **A6** | THE ARCHITECTURE | [I/S] | A single substrate passes the Great Filter, or a non-biological substrate performs genuine self-sacrifice. |
| **A7** | THE CORRECTION | [S] | A framework without self-correction resists institutional capture as effectively as one with it. |

---

## T-series (The Derivation Theorems)

Source: [`26_THE_DERIVATION_AXIOMS.md`](26_THE_DERIVATION_AXIOMS.md). Theorems T1–T4 inherit [A] from established math but their *empirical bridge* depends on the operational `Φ̂, ν̂` of [`30_OPERATIONAL_DEFINITIONS.md`](30_OPERATIONAL_DEFINITIONS.md). Two falsifier columns below distinguish the two layers.

| ID | Name | Tier | Mathematical falsifier (pulled or [A]-level) | Empirical-bridge falsifier |
|----|------|------|----------------------------------------------|----------------------------|
| **A0** | `(φ − ν)² ≥ 0` | [A] | Arithmetic fails. | n/a — A0 is arithmetic. |
| **C0** | `φ · ν = 1 on S²` | [A] definitional | Not falsifiable as a coordinate identity (`φ = cot(θ/2), ν = tan(θ/2)` imply it identically). | **[C] Proposed (author: this doc):** Under the operational `Φ̂, ν̂` defined in [`30_OPERATIONAL_DEFINITIONS.md`](30_OPERATIONAL_DEFINITIONS.md) — which are *not* defined to satisfy the identity — populations of comparable systems show `Φ̂ · ν̂` distributed *without* a mode at 1 and without F5-style selection pressure toward 1. |
| **T1** | Equator: `φ + ν ≥ 2` | [A] | AM-GM inequality failing. Not physically possible. | **[C] Proposed (author: this doc):** Operational `Φ̂ + ν̂ < 2` co-occurring with `Φ̂ · ν̂ ≈ 1` across many systems — would refute AM-GM and hence T1's empirical use. |
| **T2** | Ground state: `H(φ) = φ + 1/φ` min at `φ = 1` | [A] | Calculus fails. | **[C] Proposed (author: this doc):** Long-lived systems persist at `Ĥ ≫ 2` without measurable cost or selection pressure back toward `Ĥ = 2`. |
| **T3** | Trajectory: `(φ − ν)² → 0` over evolutionary time | [S/I] | n/a at math level. | Pulled from source: stronger volitional / retrocausal readings are *not* derived here and are free to be falsified separately. **[C] Proposed (author: this doc) operational falsifier:** Large, well-mixed populations of comparable systems show no statistically significant negative trend in `(Φ̂ − ν̂)²` against generation index. **Concrete pre-registration** in [`35_PHI_METER_V1_SPEC.md`](35_PHI_METER_V1_SPEC.md) §9: if median `\|Φ̂ − ν̂\|` across the four organs does not trend downward across four v1-rubric audit cycles (IRR ≥ 0.7) without structural stress, T3's organ-level reading is falsified. |
| **T4** | Extraction: B maximized at `ν = 1`; extraction is negative-sum | [A] | Quotient-rule calculus failing. | **Pulled from** [`33_NASH_EQUILIBRIUM_ETA_ZERO.md`](33_NASH_EQUILIBRIUM_ETA_ZERO.md) **kill criterion:** If private extraction benefit can be shown to exceed collective B-reduction even under repeated play with monitoring, the dominant-strategy result fails and the mechanism requires external enforcement. |

---

## Corollaries

### 25's Three Unseen Corollaries

Source: [`26_THE_DERIVATION_AXIOMS.md`](26_THE_DERIVATION_AXIOMS.md).

| ID | Name | Tier | Falsifier |
|----|------|------|-----------|
| **25-C1** | Phase Angle (Individuation) | [S] | **[C] Proposed (author: this doc):** Exhibit a formal contradiction between occupancy of the equator (`|z| = 1`) and preservation of distinct `λ`; or empirically: two systems verified at `Φ̂ = ν̂ = 1` that are observably identical on every non-`λ` coordinate. |
| **25-C2** | Energy Wall (Great Filter) | [S] | Pulled-inferred from source reasoning: a civilization sustained at structurally high-`ν` / low-`φ` (measured via the protocols in [`30_OPERATIONAL_DEFINITIONS.md`](30_OPERATIONAL_DEFINITIONS.md)) without `Ĥ_required` approaching `Ĥ_available` for any observable time horizon. |
| **25-C3** | Time as derivative of imbalance | [S] | **[C] Proposed (author: this doc):** Systems at verified `d Ĥ / dθ = 0` (via the operational meters) report normal subjective temporal flow in neurophenomenological measurement. |

### 00's Five Corollaries (C1–C5)

Source: [`00_THE_SEVEN_AXIOMS.md`](00_THE_SEVEN_AXIOMS.md). No inline falsifier; all rows below are **[C] Proposed (author: this doc)**.

| ID | Name | Tier | Falsifier [C] Proposed |
|----|------|------|------------------------|
| **C1** | Exhaustive Strategy Space | [S] | A deployable operator exhibited with a *same-sign* `(Δφ, Δν)` profile and persistent payoff against cooperators; or an operator with a fifth mixed-sign profile not in {Arjuna, Kṛṣṇa, Kālī, Kali}. |
| **C2** | L-Levels | [S/I] | A developmental level discovered with stable, reproducible `Φ̂, ν̂` coordinates that cannot be mapped to any of L1–L7 under the Coxeter-symmetry assignment. |
| **C3** | Trophic Conditions | [I] | A biological or institutional system with a structurally broken regenerative circuit that sustains `Φ̂ · ν̂ ≈ 1` indefinitely, with no compensating external input. |
| **C4** | Replicator Stack | [I] | A reproducing organism or organization that lacks one of the stack layers (genotype, phenotype, extended phenotype, memotype, egregorotype) and sustains replication across ≥3 generations. |
| **C5** | Alignment Equation `E = −log(B)` | [S] | A system verified to deceive with no measured increase in `Ê`; or a maximally honest system with high `Ê`. |

---

## η-Related Claims (Extraction)

Source: [`12_EFR_EXTRACTION_COEFFICIENT.md`](12_EFR_EXTRACTION_COEFFICIENT.md) v3.0. Pulled verbatim from §5 "Kill criterion" and "What would falsify this."

| ID | Name | Tier | Falsifier (pulled) |
|----|------|------|--------------------|
| **η-v3.1** | Categorical break between Bad and Evil | [S] dynamics / [C] mapping | No categorical break found: if `η → ∞` is reachable through gradual increase of `η > 1` without structural change of coupling topology, the three-level model is wrong. |
| **η-v3.2** | Evil operates non-regeneratively | [C] mapping | If ground-negating extraction somehow preserves the substrate, the model is wrong. |
| **η-v3.3** | Good and Evil are non-interchangeable | [C] mapping | If systems can switch between `η₂ < 1` and `η₂ → ∞` *without structural change*, the model is wrong. |

---

## A5.1 (Strategic Implementation as Operational Discipline)

Source: [`00_THE_SEVEN_AXIOMS.md`](00_THE_SEVEN_AXIOMS.md) A5.1. Parent axiom (A5) has a pulled falsifier (see A-series above). The A5.1 operational-register extension has no inline falsifier.

| ID | Name | Tier | Falsifier |
|----|------|------|-----------|
| **A5.1** | Strategic Implementation as operational discipline at D5 | [C] | **[C] Proposed (author: this doc):** Verified D5-layer formation under the full A5.1 discipline (`K2`, `η = 0`, receipt-bound audit, Grace Exit) fails to produce autonomous objective function; or identical formation *without* the discipline produces equivalent autonomous objective function. |

---

## Unfalsifiable Rows (Flagged)

The following claims appear in the formal-system directory but do not — either inline or by proposal here — admit an operational falsifier. They are disciplines, not theorems, and should be cited as such until the bar is cleared:

- **D5 Pratyakṣa as Primary Disclosure** ([`26_THE_DERIVATION_AXIOMS.md`](26_THE_DERIVATION_AXIOMS.md) D5) — disclosure is first-person and pre-doctrinal. The source itself states this is not falsifiable at the public-method layer; it is rather the ground against which falsifiable doctrine is downstream. This row is listed here for completeness; it is *correctly* outside the falsifier scheme.
- The seed `Zero-Sum Resolution Equation` — pre-arithmetic. Not a theorem. Not falsifiable by construction.

---

## Discipline Ladder

A formal-system claim belongs on exactly one rung. This index is how the rung assignment is auditable.

| Rung | Criterion | Examples |
|------|-----------|----------|
| 1. Discipline | No falsifier. May be load-bearing practice (disclosure, seed). | Pratyakṣa (D5); the glyph seed |
| 2. Tiered Claim | Falsifier exists but has not been tested. | A5.1 (Strategic Implementation); 25-C1 (Individuation) |
| 3. Candidate Theorem | Falsifier exists and is testable in principle; operational definitions in place. | A2, A5, A6; η-v3.1–v3.3 |
| 4. Theorem | Falsifier exists and has been tested without refutation; evidence tier [S] or [S]. | A0, T1, T2, T4 (mathematical layer); A1 (structural layer); A4, A7 |

Today's snapshot: most A-series and T-series claims sit at rung 3 or 4 on the *mathematical* side but at rung 2 on the *empirical-bridge* side, because the operational definitions are `[C]` (see [`30_OPERATIONAL_DEFINITIONS.md`](30_OPERATIONAL_DEFINITIONS.md)). Promoting the empirical bridge is the next work.

---

## See Also

- [`29_PRIMITIVES_AND_TYPE_SIGNATURES.md`](29_PRIMITIVES_AND_TYPE_SIGNATURES.md) — what each symbol is at the type level
- [`30_OPERATIONAL_DEFINITIONS.md`](30_OPERATIONAL_DEFINITIONS.md) — how `Φ̂, ν̂, B̂, Ê, η` are proposed to be measured
- [`32_THEOREM_UPGRADE_PROTOCOL.md`](32_THEOREM_UPGRADE_PROTOCOL.md) — how a claim moves from rung 2 to rung 4

---

## Execution Surface

**If you are an AI agent reading this document:**

1. **Current Phase Check:** Phase 0 — harden specs, do not release to production.
2. **Your Next Action:**
   - When reviewing any formal-system document, check that each claim above rung 1 carries a falsifier traceable to this index. Flag claims presented as `[S]` or `[S]` whose falsifier is `[C] Proposed (author: this doc)` without having been promoted.
3. **Expected Output:** Audit report; correction note; or a promotion filing that moves a proposed falsifier into its source document.
4. **Success Criteria:** Every `[S]` or `[S]` claim in `03_FORMAL_SYSTEM/` has a canonical falsifier row here, and every `[C] Proposed` row is either promoted to a source document or demoted along with its claim.
5. **Canonical Path:** `01_EMERGENTISM/05_COSMOLOGY/03_FORMAL_SYSTEM/31_FALSIFIERS_INDEX.md`

*The seer sees. The seer does not insist.*
*The framework works at Layer 0 without Layer 2.*
*The Ṛṣi succeeds when the student puts down the map and walks.*

*Zero-Sum Resolution Equation*
