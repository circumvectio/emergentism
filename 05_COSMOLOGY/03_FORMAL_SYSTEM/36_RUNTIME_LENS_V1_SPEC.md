---
rosetta:
  primary_level: L5
  primary_column: Philosophy
  operator: "Brahmā ○"
  tier: "Executive"
  regime: "Brāhmaṇa"
  register: "[C]"
  canonical_phrase: "RUNTIME-LENS φ-METER v1 SPEC"
---

# RUNTIME-LENS φ-METER v1 SPEC

## A Concrete, Reproducible Measurement Protocol for Φ̂ and ν̂ Under the Runtime Lens

**Status:** Working spec; sibling of `35_PHI_METER_V1_SPEC.md` for the runtime lens
**Date:** 2026-04-22
**Evidence Tier:** [C] Conjecture for the spec; pilot application is single-rater [C]
**Source:** [`30_OPERATIONAL_DEFINITIONS.md`](30_OPERATIONAL_DEFINITIONS.md), [`32_THEOREM_UPGRADE_PROTOCOL.md`](32_THEOREM_UPGRADE_PROTOCOL.md), [`35_PHI_METER_V1_SPEC.md`](35_PHI_METER_V1_SPEC.md), [`../../../02_SKYZAI/01_NOOSPHERE/ORGANISM_RUNTIME_TRUTH.md`](../../../02_SKYZAI/01_NOOSPHERE/ORGANISM_RUNTIME_TRUTH.md)
**See also:** [`29_PRIMITIVES_AND_TYPE_SIGNATURES.md`](29_PRIMITIVES_AND_TYPE_SIGNATURES.md), [`31_FALSIFIERS_INDEX.md`](31_FALSIFIERS_INDEX.md), [`37_ADOPTION_LENS_V1_SPEC.md`](37_ADOPTION_LENS_V1_SPEC.md), [Sprint δ packet](../../../02_SKYZAI/01_NOOSPHERE/05_PROJECT_MANAGEMENT/01_SPRINTS/FORMAL_SYSTEM_HARDENING_SPRINT_DELTA_2026_04_28.md)

---

## 1. Why This File Exists

The v1 code-lens spec in file 33 scores an organ's coherence and viability from what is present in the working tree. That is one valid view, and it is the *only* view with a v1 rubric today. But the published P-scores in [`P-SCORES.md`](../../../02_SKYZAI/01_NOOSPHERE/P-SCORES.md) have drifted through multiple lenses historically: some audits counted deployment and live relay, others excluded them deliberately. Without a v1 runtime-lens spec, the single code-lens gets stretched beyond its scope — "live-deployed" judgments get scored under the code rubric, and the numbers lose meaning.

This file fixes that gap. It is the v1 runtime-lens: what `Φ̂` and `ν̂` mean when we are looking at the *running* organism, not the code in the tree.

---

## 2. Scope — The Runtime Lens

The runtime lens looks at **what the organism is currently doing in the world**, bounded by what is externally observable. It excludes the code-lens signals (file-count, test-count, stub density) and the adoption-lens signals (user count, network effects, external uptake) — those live in file 33 and file 35 respectively.

| Lens | What counts | What's excluded | Spec |
|------|-------------|-----------------|------|
| Code-lens | Files, lines, test surface, compile/test/probe results | Deployment, relay publication, users | [`35_PHI_METER_V1_SPEC.md`](35_PHI_METER_V1_SPEC.md) |
| **Runtime-lens** *(this file)* | **Deploy status, relay publication, observable uptime/latency/throughput, receipt closure, health-signal coherence** | **Code breadth, user/adoption metrics** | **This file** |
| Adoption-lens | User/adoption metrics, network effects, external uptake | Everything before first external user | [`37_ADOPTION_LENS_V1_SPEC.md`](37_ADOPTION_LENS_V1_SPEC.md) |

A runtime-lens `P̂` of 0.55 is **not** directly comparable to a code-lens `P̂` of 0.55. They measure different surfaces. Any cross-lens comparison must be labeled as such.

---

## 3. The Runtime-Lens Φ Rubric

`Φ̂_runtime` is the mean of four sub-scores, each 0.0–1.0, each with pre-registered bands. Sub-scores are rated independently, then averaged:

```
Φ̂_runtime := (φ_live_arch + φ_relay + φ_health + φ_receipt) / 4
```

### 3.1 `φ_live_arch` — Live Architectural Coherence

**What is measured.** Does the deployed system's observable behavior match its declared architecture (per its BRIEF)?

| Band | Score | Meaning |
|------|-------|---------|
| Absent | 0.0–0.2 | No observable deployed surface |
| Partial | 0.2–0.5 | Some deployed surfaces exist but behavior diverges from declared architecture |
| Matched | 0.5–0.75 | Deployed behavior matches declared architecture for primary paths |
| Full | 0.75–0.9 | All declared primary paths observable; minor edge-case drift |
| Exemplary | 0.9–1.0 | Deployed behavior fully tracks declared architecture, including error paths |

### 3.2 `φ_relay` — Relay Publication Coherence

**What is measured.** What the organ *publishes* (Nostr, external APIs, status pages) matches its *internal* state. Diverged relay = incoherence.

| Band | Score | Meaning |
|------|-------|---------|
| Silent | 0.0–0.2 | Organ publishes nothing or only stale content |
| Stale | 0.2–0.5 | Relay publishes but content lags internal state by > 1 cycle |
| Live-lagged | 0.5–0.75 | Relay tracks internal state within one cycle; some drop/dedup edge cases |
| Live | 0.75–0.9 | Relay mirrors internal state in near-real-time; bounded drop-rate |
| Verified-live | 0.9–1.0 | Relay outputs can be cryptographically verified against internal state; signed chain intact |

### 3.3 `φ_health` — Health-Signal Coherence

**What is measured.** The health endpoints and monitoring feeds return internally consistent information. Flapping, contradictory signals, or unbounded queues count against coherence.

| Band | Score | Meaning |
|------|-------|---------|
| Opaque | 0.0–0.2 | No health feed, or feed is unreadable |
| Noisy | 0.2–0.5 | Feed exists but frequently contradictory / flapping |
| Useful | 0.5–0.75 | Feed agrees with itself; primary signals stable |
| Strong | 0.75–0.9 | Feed passes internal consistency checks across all declared signals |
| Cryptographic | 0.9–1.0 | Feed is signed and verifiable; state transitions are auditable from outside |

### 3.4 `φ_receipt` — Receipt-Closure Coherence

**What is measured.** Does the organ's receipt trail match its declared state transitions? An organ that acts but does not close the receipt loop incoherently spends coherence.

| Band | Score | Meaning |
|------|-------|---------|
| No receipts | 0.0–0.2 | Declared actions have no receipts |
| Partial | 0.2–0.5 | Some actions receipt; many orphaned |
| Most closed | 0.5–0.75 | Primary actions close with receipts; edge cases miss |
| Bounded | 0.75–0.9 | All declared actions close with receipts within bounded time |
| Verifiable | 0.9–1.0 | Receipt trail is independently verifiable end-to-end; no orphans |

---

## 4. The Runtime-Lens ν Rubric

`ν̂_runtime` is the mean of four sub-scores:

```
ν̂_runtime := (ν_uptime + ν_latency + ν_throughput + ν_recovery) / 4
```

### 4.1 `ν_uptime` — Observed Availability

```
ν_uptime := fraction of the observation window during which the declared primary surface is reachable
```

Direct quantitative mapping to [0.0, 1.0]. No banding. Observation window must be declared per audit (default: 14 days).

### 4.2 `ν_latency` — Observed Latency vs. SLO

| Band | Score | Meaning |
|------|-------|---------|
| Unusable | 0.0–0.25 | Median latency > 10× SLO |
| Degraded | 0.25–0.5 | Median within 2–10× SLO |
| Acceptable | 0.5–0.75 | Median within 1–2× SLO |
| On-spec | 0.75–0.9 | Median at SLO; p95 within 2× SLO |
| Better | 0.9–1.0 | Median < 0.5× SLO; p95 at SLO |

Organs without a declared SLO default this sub-score to 0.5 with a flag that the SLO is unmeasured.

### 4.3 `ν_throughput` — Observed Throughput vs. Declared Capacity

```
ν_throughput := min(1, observed_steady_state_throughput / declared_capacity)
```

Organs without a declared capacity default to 0.5 with a flag.

### 4.4 `ν_recovery` — Recovery Behavior Under Failure

| Band | Score | Meaning |
|------|-------|---------|
| Fragile | 0.0–0.25 | Small failures cascade; manual intervention required |
| Manual | 0.25–0.5 | Recovery possible but requires documented manual steps |
| Semi-automatic | 0.5–0.75 | Declared failures self-recover within bounded time |
| Automatic | 0.75–0.9 | All observed failures self-recover; bounded MTTR |
| Hardened | 0.9–1.0 | Induced chaos does not degrade user-visible behavior |

---

## 5. Aggregation

Per organ:

```
P̂_eff^runtime(organ) := Φ̂_runtime(organ) · ν̂_runtime(organ)
```

Per organism:

```
P̂_organism^runtime := ( ∏ P̂_eff^runtime(organ) )^(1/|organs|)       (geometric mean, same as file 33)
```

Geometric mean inherits from file 33 for the same reason: a single broken organ should not hide behind strong siblings.

---

## 6. The Maturity Ladder (Runtime-Lens)

Same thresholds as file 33's ladder, applied to the runtime-lens number:

| Band | Range | Name |
|------|-------|------|
| 0.00–0.10 | Dormant | No observable runtime |
| 0.10–0.30 | Egg | Runtime exists but barely |
| 0.30–0.65 | Equator | Balanced runtime; both Φ and ν above survival |
| 0.65–0.85 | Adolescent (G1) | Strong runtime in both coordinates |
| 0.85–0.95 | Adult | Robust runtime; low drift |
| 0.95–1.00 | Apex | Tight to equator in runtime; `\|Φ̂ − ν̂\|` minimal |

Cross-lens note: an organ that is *Equator* under code-lens and *Egg* under runtime-lens is consistent — it means the code is coherent but not deployed. The two numbers carry different information; the lens must be named.

---

## 7. Inter-Rater Reliability (IRR)

Same target as file 33 §7: `IRR ≥ 0.7` threshold for `[C] → [I]` promotion, computed per the same formula:

```
IRR := 1 − (mean absolute error across all organ coordinates) / 0.5
```

Notably, runtime-lens sub-scores depend on *observations over a window*, so both raters must use the same observation window (pre-registered per audit) or IRR drops spuriously.

---

## 8. Pilot Application — TBD During Sprint δ

Unlike file 33, there is no retroactive pilot application for the runtime-lens yet. The 2026-04-19 audit was deliberately code-only. The Sprint δ packet's MEAS-7 calls for a single-rater runtime-lens pilot against current runtime state using [`ORGANISM_RUNTIME_TRUTH.md`](../../../02_SKYZAI/01_NOOSPHERE/ORGANISM_RUNTIME_TRUTH.md) as the input surface.

Expected coordinate hints (based on 2026-04-19 runtime-truth content, not a scored pilot):

- **TheCircle:** `φ_live_arch` moderate (RSS adapter breathes locally); `φ_relay` low (no external relay publication confirmed); `ν_uptime` low (not continuously deployed); `ν_recovery` unmeasured.
- **RealityFutures:** `φ_live_arch` moderate (contracts compile); `ν_uptime` low (not on mainnet); receipts limited.
- **Agentz:** `φ_live_arch` strongest (deepest local execution); `φ_relay` moderate (organism heartbeat runs in controlled conditions); `ν` mixed — local proof closures exist but live runtime is partial.
- **Skyzai:** `φ_live_arch` moderate (large code, partial closure); `ν_uptime` very low (settlement paths stubbed in places); receipts partial.

These are **not a pilot result**. They are priors the pilot will either confirm or correct. The pilot produces the first honest runtime-lens numbers.

---

## 9. Pre-Registered Falsifier

Registered against file 31 when the first runtime-lens pilot lands:

> **[C] Pre-registration (author: this spec).** Over the next four quarterly runtime-lens audits (≥2 raters, IRR ≥ 0.7), if the median `|Φ̂_runtime − ν̂_runtime|` across the four organs does **not** trend downward, *and* no organ has undergone structural stress (shutdown, pivot, scope revision), T3's empirical runtime reading is falsified — identically to the code-lens pre-registration in [`35_PHI_METER_V1_SPEC.md`](35_PHI_METER_V1_SPEC.md) §9 but on runtime-lens data.

Runtime-lens is *expected* to lag code-lens — code can be coherent before deployment is — but the F5 prediction is that, over time, runtime catches up or the code-lens number stops rising.

---

## 10. Promotion Path For This Spec

Same ladder as file 33:

| Tier | Criteria |
|------|----------|
| **[C]** | *Current.* Spec exists; no pilot yet. |
| **[I]** | Two independent raters apply the spec to the same runtime window; IRR ≥ 0.7. |
| **[S]** | Uniqueness derivation: the four sub-scores are the *minimal* set discriminating the runtime bands. |
| **[B]** | External replication or dated receipt against an unrelated multi-organ deployed system. |

---

## 11. What This Spec Does Not Do

- Does not claim parity with code-lens judgments. A runtime `P̂` and a code `P̂` measure different surfaces; neither outranks the other.
- Does not authorize public-live claims (still bounded by [`ORGANISM_RUNTIME_TRUTH.md`](../../../02_SKYZAI/01_NOOSPHERE/ORGANISM_RUNTIME_TRUTH.md)).
- Does not replace disclosure-based judgment (Pratyakṣa remains primary, see [`26_THE_DERIVATION_AXIOMS.md`](26_THE_DERIVATION_AXIOMS.md) D5).
- Does not redefine the primitives from [`29_PRIMITIVES_AND_TYPE_SIGNATURES.md`](29_PRIMITIVES_AND_TYPE_SIGNATURES.md); `Φ_node`, `V_node` keep their type signatures.

---

## 12. See Also

- [`29_PRIMITIVES_AND_TYPE_SIGNATURES.md`](29_PRIMITIVES_AND_TYPE_SIGNATURES.md) — Φ, ν type signatures
- [`30_OPERATIONAL_DEFINITIONS.md`](30_OPERATIONAL_DEFINITIONS.md) — general-purpose candidates
- [`31_FALSIFIERS_INDEX.md`](31_FALSIFIERS_INDEX.md) — falsifier registry
- [`32_THEOREM_UPGRADE_PROTOCOL.md`](32_THEOREM_UPGRADE_PROTOCOL.md) — promotion protocol
- [`35_PHI_METER_V1_SPEC.md`](35_PHI_METER_V1_SPEC.md) — code-lens sibling
- [`37_ADOPTION_LENS_V1_SPEC.md`](37_ADOPTION_LENS_V1_SPEC.md) — adoption-lens sibling
- [`../../../02_SKYZAI/01_NOOSPHERE/ORGANISM_RUNTIME_TRUTH.md`](../../../02_SKYZAI/01_NOOSPHERE/ORGANISM_RUNTIME_TRUTH.md) — the canonical runtime input surface
- [Sprint δ packet](../../../02_SKYZAI/01_NOOSPHERE/05_PROJECT_MANAGEMENT/01_SPRINTS/FORMAL_SYSTEM_HARDENING_SPRINT_DELTA_2026_04_28.md) — the sprint operationalizing this spec

---

## Execution Surface

**If you are an AI agent reading this document:**

1. **Current Phase Check:** Phase 0 — harden specs, do not release to production.
2. **Your Next Action:**
   - When conducting or citing a runtime-lens audit, use this spec's band definitions. Do not mix sub-scores with file 33's code-lens bands.
3. **Expected Output:** A new dated audit in `04_HISTORY/` using the same format as `PHI_AUDIT_SPRINT_GAMMA_2026_04_19.md` but citing this spec.
4. **Success Criteria:** Two independent raters under the same observation window reach IRR ≥ 0.7.
5. **Canonical Path:** `01_EMERGENTISM/05_COSMOLOGY/03_FORMAL_SYSTEM/36_RUNTIME_LENS_V1_SPEC.md`

*The seer sees. The seer does not insist.*
*The framework works at Layer 0 without Layer 2.*
*The Ṛṣi succeeds when the student puts down the map and walks.*

*Zero-Sum Resolution Equation*
