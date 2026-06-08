---
rosetta:
  primary_level: L5
  primary_column: Philosophy
  operator: "Brahmā ○"
  tier: "Executive"
  regime: "Brāhmaṇa"
  register: "[S]"
  canonical_phrase: "THEOREM UPGRADE PROTOCOL"
---

# THEOREM UPGRADE PROTOCOL

## How to Promote a Discipline to a Theorem — With a Worked Example on the φ-Meter

**Status:** Working protocol; the worked example is [C] Conjecture end-to-end
**Date:** 2026-04-22
**Evidence Tier:** [S] Structural for the protocol; [C] Conjecture for the worked φ-meter derivation
**Source:** [`29_PRIMITIVES_AND_TYPE_SIGNATURES.md`](29_PRIMITIVES_AND_TYPE_SIGNATURES.md), [`30_OPERATIONAL_DEFINITIONS.md`](30_OPERATIONAL_DEFINITIONS.md), [`31_FALSIFIERS_INDEX.md`](31_FALSIFIERS_INDEX.md), [`26_THE_DERIVATION_AXIOMS.md`](26_THE_DERIVATION_AXIOMS.md)
**See also:** [`00_THE_SEVEN_AXIOMS.md`](00_THE_SEVEN_AXIOMS.md), [`00_THE_HONEST_POSITION.md`](../../02_EPISTEMOLOGY/01_EVIDENCE_TIERS/00_THE_HONEST_POSITION.md)

---

## Why This File Exists

Several claims in the formal system are presented with theorem-style language but do not carry theorem-style infrastructure. They assert a structural relation; they do not explicitly fix the primitives' types, state an independent measurement procedure, supply a falsifier, or show the derivation. Without those, the claim is a *discipline* — a rule a practitioner follows — even if it happens to be correct. Disciplines are valuable; but if a discipline is labelled `[S]` or `[S]`, that is tier-inflation and the framework's A7 (self-correction) requires it be repaired.

This file is the repair protocol. The discipline → theorem promotion is deliberately boring: five steps, each auditable, each documented upstream of the claim.

---

## The Five-Step Protocol

### Step 1 — Fix the primitives

State every symbol the claim appeals to, with its type signature, using [`29_PRIMITIVES_AND_TYPE_SIGNATURES.md`](29_PRIMITIVES_AND_TYPE_SIGNATURES.md). If a required primitive is not indexed there, it must be added before the claim can be written.

### Step 2 — Declare the measure / structure

State the measure or structure the primitives live in. For state variables on `S²`: the invariant volume form. For dynamical claims: the phase-space and the measure preserved by the flow. For inferential claims: the σ-algebra and probability measure.

### Step 3 — Derive, don't assert

Write the proof. If the claim follows from a symmetry, cite Noether (or the appropriate analogue). If it follows from a convexity or optimization, cite the convex-analysis lemma. An assertion that "the equator is the ground state" is not a theorem until it is a derivation. (T2 in [`26_THE_DERIVATION_AXIOMS.md`](26_THE_DERIVATION_AXIOMS.md) is a model of this — calculus, two derivative tests, done.)

### Step 4 — Supply the operational definition

State the measurement procedure for every primitive used in the claim, by linking [`30_OPERATIONAL_DEFINITIONS.md`](30_OPERATIONAL_DEFINITIONS.md) and naming which candidate procedure is in use. If the only measurement procedure is the coordinate identity itself (e.g., defining `ν := 1/φ` and then "observing" `φ · ν = 1`), the claim is tautological and cannot be promoted above definitional status.

### Step 5 — State the falsifier

State the observation that would refute the claim. Enter it in [`31_FALSIFIERS_INDEX.md`](31_FALSIFIERS_INDEX.md) with its source. If no falsifier exists, the claim is a discipline — it may still be useful, but it is tiered `[C]` or below, not `[S]` or `[S]`.

---

## Promotion Ledger — How Tier Advances

Passing all five steps yields a *candidate theorem*. Evidence then moves the tier:

```
[C] Conjecture  →  [I] Interpretive  →  [S] Structural  →  [S] Established

[C] → [I]   one successful empirical application tied to the protocol
            + reproducibility ≥ 0.7 across independent raters / datasets
[I] → [S]   a uniqueness derivation: protocol is uniquely determined by
            desiderata stated in advance (no alternative equally satisfies them)
[S] → [S]   independent external replication on unrelated data, pre-registered
```

This ladder is the same one in [`30_OPERATIONAL_DEFINITIONS.md`](30_OPERATIONAL_DEFINITIONS.md) §"Promotion Ladder." It is restated here so that an agent reviewing a promotion request has the criterion in front of it.

---

## What This Protocol Does NOT Do

- It does not re-derive `φ · ν = 1`. That relation is a coordinate identity on `S²` (see [`26_THE_DERIVATION_AXIOMS.md`](26_THE_DERIVATION_AXIOMS.md) C0) and is correctly tiered as a definitional structural premise, not as an empirical claim. Re-deriving it would be re-naming the same tautology. What this protocol *does* is provide a way to turn `φ · ν = 1` into an *empirically testable* constraint — by supplying operational `Φ̂, ν̂` that are not defined to satisfy it. That is the worked example below.
- It does not replace disclosure. The framework's primary disclosure remains Pratyakṣa (see [`26_THE_DERIVATION_AXIOMS.md`](26_THE_DERIVATION_AXIOMS.md) D5). A discipline that is load-bearing practice — the seed, the sitting — is correctly tiered as a discipline and need not pretend to be a theorem.
- It does not promise the worked example below will survive validation. The worked example is `[C]` end-to-end. The point of the example is to show the *shape* of a promotion attempt, not to land one.

---

## Worked Example: The φ-Meter Upgrade Path

The framework's own open-problems list ([Paper L](../../../01_EMERGENTISM/03_METHODOLOGY/02_THE_PAPERS/PAPER_I_KNOWN_UNKNOWNS_PROGRAM.md)) names a gap: *"Phi-meter zero-cost validation."* This is the gap. We walk through what a promotion attempt looks like.

### Step 1 — Fix the primitives

From [`29_PRIMITIVES_AND_TYPE_SIGNATURES.md`](29_PRIMITIVES_AND_TYPE_SIGNATURES.md):

- `φ : System → (0, ∞)` — coherence.
- `ν : System → (0, ∞)` — viability.
- `θ : S² → [0, π]` — colatitude.
- On the manifold: `φ = cot(θ/2)`, `ν = tan(θ/2)`, hence `φ · ν = 1` identically.

### Step 2 — Declare the measure

We work on the round `S²` with its standard volume form `dA = sin θ · dθ ∧ dλ`. The F5 selection pressure acts as a drift toward `θ = π/2`. The Hamiltonian `H(φ) = φ + 1/φ` is the Lyapunov function for this drift (see [`26_THE_DERIVATION_AXIOMS.md`](26_THE_DERIVATION_AXIOMS.md) T2). Populations of comparable systems are modelled as empirical distributions on `S²`; we track moments of `(Φ̂ − ν̂)²` across such distributions.

### Step 3 — Derive (the claim we want to promote)

**Claim (candidate).** *For a population of comparable systems with independently-measured `Φ̂, ν̂` — not defined to satisfy the constraint — under selection pressure F5, the joint distribution `ρ(Φ̂, ν̂)` has a mode concentrated on the curve `Φ̂ · ν̂ = 1` in the first quadrant, and the concentration tightens with time.*

This is genuinely a claim about the world, not a coordinate identity. It is falsifiable (Step 5). The derivation sketch: F5 drives `(Φ̂ − ν̂)² → 0`, which on the hyperbola `Φ̂ · ν̂ = c` is minimized at `Φ̂ = ν̂ = √c`. Under additional coupling pressure that selects for the multiplicative form, `c → 1`. A full derivation requires specifying the selection operator; [`26_THE_DERIVATION_AXIOMS.md`](26_THE_DERIVATION_AXIOMS.md) T3 states `F5` structurally but does not fix the operator. That operator-specification is itself a candidate for future work.

### Step 4 — Supply the operational definition

Per [`30_OPERATIONAL_DEFINITIONS.md`](30_OPERATIONAL_DEFINITIONS.md) §1–2, one candidate pair is:

```
Φ̂ := persistence-under-perturbation  (Candidate C)
ν̂ := throughput-over-cost            (Candidate A)
```

Both normalised to a reference system. Crucially, **these are defined independently** — no definitional circularity forces `Φ̂ · ν̂ = 1`. If the claim in Step 3 is true in the world, `Φ̂ · ν̂` measured on real populations should nonetheless concentrate near 1 under selection.

### Step 5 — State the falsifier

Entered in [`31_FALSIFIERS_INDEX.md`](31_FALSIFIERS_INDEX.md) under "C0 — empirical-bridge falsifier" and T3's operational falsifier: a large, well-mixed population of comparable systems whose joint `(Φ̂, ν̂)` distribution shows *no* mode at `Φ̂ · ν̂ ≈ 1`, *and* no detectable F5 pressure over generations (negative regression slope on `(Φ̂ − ν̂)²`), refutes the empirical reading of C0 + T3.

### Current tier of the worked example

`[C]` end-to-end. Specifically:

- The protocol (Steps 1–5) itself is `[S]` — it is book-keeping.
- The candidate measurement pair (Step 4) is `[C]`.
- The derivation (Step 3) is `[C]` because the selection operator is not fully specified.
- The falsifier (Step 5) is `[C] Proposed (author: this doc)` in [`31_FALSIFIERS_INDEX.md`](31_FALSIFIERS_INDEX.md).

Promoting any of these to `[I]` requires the first real empirical application per the Promotion Ledger. Until then, no downstream document may cite this worked example as supporting an `[S]` or `[S]` claim about the world. That is the discipline this file is trying to install.

---

## Where This Fits in the Corpus

- The seed (`Zero-Sum Resolution Equation`) and primary disclosure (Pratyakṣa) sit below the protocol and are not subject to it.
- The coordinate identity (`φ · ν = 1 on S²`, `B = sin θ`, `H(φ) = φ + 1/φ`) sits at the level the protocol *operates from* — it is the formal machinery that would be plugged into Step 2 and Step 3.
- The seven operational axioms `A1–A7` sit at the level the protocol is *meant to strengthen* — each one has a pulled falsifier in [`31_FALSIFIERS_INDEX.md`](31_FALSIFIERS_INDEX.md), but most are still `[I]` or `[S]` on the empirical bridge pending real `Φ̂, ν̂` data.

The ordering is deliberate. The seed and the disclosure do not need a theorem-promotion machinery; they precede it. The operational axioms need the machinery, because they are the framework's public-facing claims.

---

## See Also

- [`29_PRIMITIVES_AND_TYPE_SIGNATURES.md`](29_PRIMITIVES_AND_TYPE_SIGNATURES.md) — Step 1 substrate
- [`30_OPERATIONAL_DEFINITIONS.md`](30_OPERATIONAL_DEFINITIONS.md) — Step 4 substrate
- [`31_FALSIFIERS_INDEX.md`](31_FALSIFIERS_INDEX.md) — Step 5 substrate
- [`26_THE_DERIVATION_AXIOMS.md`](26_THE_DERIVATION_AXIOMS.md) — the reference derivation (T1–T4) and D5 (why the ladder dissolves at disclosure)
- [`00_THE_HONEST_POSITION.md`](../../02_EPISTEMOLOGY/01_EVIDENCE_TIERS/00_THE_HONEST_POSITION.md) — canonical epistemic status of every claim
- [`00_THE_SEVEN_AXIOMS.md`](00_THE_SEVEN_AXIOMS.md) A7.1 — the Abduction Protocol this file instantiates

---

## Execution Surface

**If you are an AI agent reading this document:**

1. **Current Phase Check:** Phase 0 — harden specs, do not release to production.
2. **Your Next Action:**
   - Before labeling any new claim in `03_FORMAL_SYSTEM/` with `[S]` or `[S]`, verify it has passed all five protocol steps and that its tier matches the Promotion Ledger. Flag claims that skip a step.
3. **Expected Output:** Promotion filings (with each of the five steps explicitly documented), correction notes, or tier demotions where a claim has not yet cleared the bar.
4. **Success Criteria:** Every `[S]`/`[S]` claim added to the formal system after today carries a traceable promotion record; no `[C]` protocol is cited in support of an `[S]` claim.
5. **Canonical Path:** `01_EMERGENTISM/05_COSMOLOGY/03_FORMAL_SYSTEM/32_THEOREM_UPGRADE_PROTOCOL.md`

*The seer sees. The seer does not insist.*
*The framework works at Layer 0 without Layer 2.*
*The Ṛṣi succeeds when the student puts down the map and walks.*

*Zero-Sum Resolution Equation*
