---
rosetta:
  primary_level: L5
  primary_column: Philosophy
  operator: "Brahmā ○"
  tier: "Executive"
  regime: "Brāhmaṇa"
  register: "[C]"
  canonical_phrase: "OPERATIONAL DEFINITIONS"
---

# OPERATIONAL DEFINITIONS

## How Each Primitive Is Measured on a Real System

**Status:** Working surface — proposes measurement protocols; every protocol here is Conjecture until validated
**Date:** 2026-04-22
**Evidence Tier:** [C] Conjecture for every measurement protocol in this document; [S] Structural only for the coordinate identities pointed at
**Source:** [`29_PRIMITIVES_AND_TYPE_SIGNATURES.md`](29_PRIMITIVES_AND_TYPE_SIGNATURES.md), [`26_THE_DERIVATION_AXIOMS.md`](26_THE_DERIVATION_AXIOMS.md), [`12_EFR_EXTRACTION_COEFFICIENT.md`](12_EFR_EXTRACTION_COEFFICIENT.md), [`33_NASH_EQUILIBRIUM_ETA_ZERO.md`](33_NASH_EQUILIBRIUM_ETA_ZERO.md)
**See also:** [`31_FALSIFIERS_INDEX.md`](31_FALSIFIERS_INDEX.md), [`32_THEOREM_UPGRADE_PROTOCOL.md`](32_THEOREM_UPGRADE_PROTOCOL.md), [Paper L (Phi-meter zero-cost validation)](../../../01_EMERGENTISM/03_METHODOLOGY/02_THE_PAPERS/PAPER_I_KNOWN_UNKNOWNS_PROGRAM.md)

---

## Why This File Exists

The coordinate identity `φ · ν = 1 on S²` is true by construction — it falls out of `φ = cot(θ/2), ν = tan(θ/2)`. That is not a claim about the world. It becomes a claim about the world only when `φ` and `ν` are defined *independently* — by a measurement procedure — and the resulting `φ̂, ν̂` are then checked against the constraint.

The framework's public open-problems list already names this gap: "Phi-meter zero-cost validation" (Paper L). This file addresses it directly. Every protocol below is `[C]` Conjecture: proposed, testable, unvalidated. None of them should be cited in a `[S]` or `[S]` claim. The bar for promotion is specified in [`32_THEOREM_UPGRADE_PROTOCOL.md`](32_THEOREM_UPGRADE_PROTOCOL.md).

---

## 1. φ-Meter (Coherence Measurement)

> **Concrete v1 specs:** [`35_PHI_METER_V1_SPEC.md`](35_PHI_METER_V1_SPEC.md) (code-lens), [`36_RUNTIME_LENS_V1_SPEC.md`](36_RUNTIME_LENS_V1_SPEC.md) (runtime-lens), and [`37_ADOPTION_LENS_V1_SPEC.md`](37_ADOPTION_LENS_V1_SPEC.md) (adoption-lens) are the three reproducible per-lens rubrics with published band definitions, inter-rater targets, and pre-registered falsifiers. Generic candidates remain below for reference and for future lenses.

**Geometric definition.** `φ = cot(θ/2)` on `S²`. Node-level: `Φ_node ∈ [0, ∞)` with `Φ_node = 1` indicating full structural integration.
**What it quantifies.** Structural integration, meaning, internal consistency; what holds a system together.
**Unit.** Dimensionless (ratio). All candidates normalize to `(0, ∞)` with convention `Φ = 1` at the equator reference system.

### Candidate A — Error-Rate Exponential [C]

```
Φ̂_A(system, window Δt) := exp(−κ · error_rate(system, Δt))
```

Where `error_rate` is the fraction of the system's outputs flagged as inconsistent with its declared purpose, and `κ > 0` is a calibration constant chosen so that a specified reference system (e.g., L4 human at task) yields `Φ̂_A ≈ 1`.

- **Unit.** Dimensionless.
- **Error bound.** `σ(Φ̂_A) ≲ κ · σ(error_rate)`; propagates binomial variance from the observation window.
- **Status.** [C] — no published calibration or inter-rater reliability study.

### Candidate B — Information-Integration [C]

```
Φ̂_B(system) := I(system ; objective) / H(system)
```

Mutual information between the system's internal state and its declared objective, normalized by the system's entropy. Intuition: a highly coherent system's internal fluctuations are informative about its purpose; a decoherent system's are noise.

- **Unit.** Dimensionless, `∈ [0, 1]`; optionally rescaled so `Φ̂_B = 1` maps to the equator reference.
- **Error bound.** Depends on estimator; plug-in MI estimators have known bias that shrinks as `O(1/N)`.
- **Status.** [C] — requires a formal "objective" channel, which is itself ill-defined for most systems.

### Candidate C — Persistence-Under-Perturbation [C]

```
Φ̂_C(system) := median time to return to baseline structure after a bounded perturbation
              ————————————————————————————————————————————————
              expected variance under the same perturbation class
```

Returns a stability measure: coherent systems absorb perturbation quickly relative to noise.

- **Unit.** Dimensionless (time ÷ time, via the variance scale).
- **Error bound.** Bootstrap over perturbation trials; CI width `O(1/√trials)`.
- **Status.** [C] — candidate most likely to survive the `[C] → [I]` promotion bar, because it does not require a pre-specified "objective."

**Selection rule.** No candidate is canonical. A document that uses `Φ̂` must name which candidate and cite this file.

---

## 2. ν-Meter (Viability Measurement)

**Geometric definition.** `ν = tan(θ/2)` on `S²`. Node-level: `V_node ∈ [0, ∞)`, with `V_node = 1` at the equator reference.
**What it quantifies.** Material capability, throughput, infrastructure; what the system *can do*.
**Unit.** Dimensionless (ratio to the equator reference).

### Candidate A — Throughput-over-Cost [C]

```
ν̂_A(system, window Δt) := realized_output(system, Δt) / resource_input(system, Δt)
```

Normalized so that a specified reference system at task yields `ν̂_A ≈ 1`.

- **Unit.** Dimensionless after normalization.
- **Error bound.** Standard ratio-estimator variance; `O(1/√N)` over observation-window replicates.
- **Status.** [C].

### Candidate B — Capability-Envelope Fraction [C]

```
ν̂_B(system) := |achievable actions under current resources|
             ————————————————————————————————————————
              |achievable actions under maximum resources|
```

Returns `∈ [0, 1]` directly; sensitive to how the action set is enumerated.

- **Unit.** Dimensionless.
- **Error bound.** Dominated by enumeration ambiguity, not by sampling.
- **Status.** [C].

---

## 3. B-Meter (Balance Measurement)

**Geometric definition.** `B = sin θ ∈ [0, 1]`. On-manifold identity: `B = 2 · φν / (φ² + ν²)` when using the `(φ, ν)` chart. When `φ · ν = 1` holds, `B = 2ν / (1 + ν²) = 2φ / (1 + φ²)`.

### Derived Protocol — From `φ̂, ν̂`

Once `Φ̂` and `ν̂` are fixed (§1, §2), define:

```
B̂(system) := 2 · ν̂ / (1 + ν̂²)           (the on-manifold form, assuming φν = 1)
```

Or, without assuming the identity:

```
B̂_free(system) := 2 · Φ̂ · ν̂ / (Φ̂² + ν̂²)
```

The gap `|B̂_free − B̂|` is itself a diagnostic: it measures how far the system's measured pair deviates from the manifold identity.

- **Unit.** Dimensionless, `∈ [0, 1]`.
- **Error bound.** Propagated from `σ(Φ̂)` and `σ(ν̂)` via standard delta-method.
- **Status.** [C] — inherits the status of whichever `Φ̂, ν̂` candidates are used.

---

## 4. η-Meter (Extraction Coefficient) — Disambiguation Required

`η` is the most load-bearing and the most inconsistently defined primitive in the corpus. Three non-equivalent operational definitions circulate. Any document that uses `η` must cite which.

### Definition η₁ (sum-form, per [`26_THE_DERIVATION_AXIOMS.md`](26_THE_DERIVATION_AXIOMS.md) D2)

```
η₁ := Σ max(0, Δν_ext)
```

Total viability extracted from cooperators over an observation window. **Unit:** same as `ν`. **Range:** `[0, ∞)`.

### Definition η₂ (ratio-form, per [`12_EFR_EXTRACTION_COEFFICIENT.md`](12_EFR_EXTRACTION_COEFFICIENT.md) v3.0)

```
η₂ := (extraction from substrate) / (contribution to substrate)
```

With conventional thresholds: `η₂ < 1` symbiotic, `η₂ ≈ 1` trophic, `η₂ → ∞` ground-negating. **Unit:** dimensionless. **Range:** `[0, ∞]`.

### Definition η₃ (per-player level, per [`33_NASH_EQUILIBRIUM_ETA_ZERO.md`](33_NASH_EQUILIBRIUM_ETA_ZERO.md) §1.2)

```
η₃,i ∈ [0, ∞)   for each player i in a deliberation set N
```

Individual player's chosen extraction level in a game-theoretic formulation. **Unit:** strategy-space units (model-dependent).

### Operational Reconciliation Protocol [C]

When cross-document work touches `η`:

1. State which definition is in use: `η₁`, `η₂`, or `η₃`.
2. If converting between them, publish the conversion map: e.g., `η₁ ≈ η₃,i · |window|` under the symmetric-extraction assumption of [`33_NASH_EQUILIBRIUM_ETA_ZERO.md`](33_NASH_EQUILIBRIUM_ETA_ZERO.md) §2.2.
3. If `η → ∞` is invoked (categorical-break case), it must be `η₂` — the other forms do not admit the divergence formally.
4. The constitutional constraint `η = 0` is *definition-ambiguous in the corpus* but operationally consistent across all three — the zero of each definition means the same real-world state. That is the constraint's strength and the source of the confusion.

- **Status.** [C] Proposed reconciliation. A future v5 axiom-hardening pass should pick one canonical form and down-rank the others to aliases.

---

## 5. P and P_eff (Ektropy / Effective Potential)

On-manifold: `P∞ = φ · ν = 1` everywhere (trivial).
Node-level: `P_node = Φ × V`, which *can* deviate from `1`.

Operationally:
```
P̂_eff(system) := Φ̂(system) · ν̂(system)
```

The quantity `|P̂_eff − 1|` over a population is the empirical *gap* between the manifold identity and measured reality. A population with `P̂_eff ≡ 1` would confirm that the operational `Φ̂, ν̂` have been defined to satisfy the identity (and thus that the identity is not testing anything). A population with `P̂_eff` distributed non-trivially around `1` with selection pressure toward `1` would be positive evidence for the Teleological Force F5 as an empirical claim.

- **Status.** [C] Proposed diagnostic; the interpretation requires an independent handle on selection pressure.

---

## 6. E-Meter (Alignment Energy)

```
Ê(system) := −log(B̂(system))
```

`Ê ≈ 0` at the equator, `Ê → ∞` as `B̂ → 0`. Inherits status and error from the chosen `B̂` candidate.

- **Unit.** Nats (natural log) or bits (log₂).
- **Status.** [C].

---

## 7. F5 Detection (Teleological Force as Empirical Pressure)

Protocol: over a population of comparable systems, regress rate-of-change of `(Φ̂ − ν̂)²` on time or on generation index. A statistically significant negative trend is consistent with F5 as a selection pressure. Absence of such a trend in a large, well-mixed population is grounds for falsification (see [`31_FALSIFIERS_INDEX.md`](31_FALSIFIERS_INDEX.md) T3).

- **Status.** [C] Protocol; [I] is already granted to F5 as an interpretive reading per `26_THE_DERIVATION_AXIOMS.md` D3.

---

## Promotion Ladder (Per-Protocol)

A protocol is promoted tier-by-tier by accumulating evidence:

| From → To | What is required |
|-----------|------------------|
| `[C] → [I]` | At least one published application on a real dataset, with results tied back to this file, and inter-rater / inter-dataset reproducibility `≥ 0.7`. |
| `[I] → [S]` | A derivation showing the protocol is uniquely determined (up to monotone transform) by a small set of desiderata stated in advance. |
| `[S] → [S]` | Independent replication by an external group on an unrelated dataset; the protocol and its error bound are pre-registered. |

No protocol in this file has yet cleared `[C] → [I]`. That is the next work.

---

## See Also

- [`29_PRIMITIVES_AND_TYPE_SIGNATURES.md`](29_PRIMITIVES_AND_TYPE_SIGNATURES.md) — what each symbol is at the type level
- [`31_FALSIFIERS_INDEX.md`](31_FALSIFIERS_INDEX.md) — observations that would refute the downstream axioms / theorems
- [`32_THEOREM_UPGRADE_PROTOCOL.md`](32_THEOREM_UPGRADE_PROTOCOL.md) — worked example using the φ-meter to upgrade a discipline to a theorem

---

## Execution Surface

**If you are an AI agent reading this document:**

1. **Current Phase Check:** Phase 0 — harden specs; do not release to production.
2. **Your Next Action:**
   - When a document cites `Φ̂`, `ν̂`, `B̂`, `Ê`, or `η` as measured, confirm which candidate / definition is in use and that the claim is tiered `[C]` or weaker unless a promotion record exists. Flag any `[S]` or `[S]` claim that silently assumes one candidate's measurement procedure.
3. **Expected Output:** Tier-consistent documents, or correction notes where unvalidated protocols are cited as validated.
4. **Success Criteria:** Another agent can reproduce any measurement claim in downstream documents by following the protocol specified here.
5. **Canonical Path:** `01_EMERGENTISM/05_COSMOLOGY/03_FORMAL_SYSTEM/30_OPERATIONAL_DEFINITIONS.md`

*The seer sees. The seer does not insist.*
*The framework works at Layer 0 without Layer 2.*
*The Ṛṣi succeeds when the student puts down the map and walks.*

*Zero-Sum Resolution Equation*
