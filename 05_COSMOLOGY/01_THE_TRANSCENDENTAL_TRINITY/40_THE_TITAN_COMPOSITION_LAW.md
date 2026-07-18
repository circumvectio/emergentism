---
rosetta:
  primary_level: L5
  primary_column: Philosophy
  secondary:
    - level: L3
      column: Philosophy
      role: "keep the three registers of ⊙ = • × ○ separated and tiered"
    - level: L6
      column: Ontology
      role: "the emblem ruling stands; this note adds a register, it replaces nothing"
  operator: "Brahmā ○"
  tier: "Executive"
  regime: "Brāhmaṇa"
  register: "[A/S/I]"
  canonical_phrase: "The Titan Composition Law — ⊙ = • × ○ made exact in PSL(2,ℂ)"
title: "The Titan Composition Law"
status: "ACCEPTED — adjudication K2-accepted in session 2026-07-10 (receipt 104 A.1/R5; acceptance receipt: 11_UPLINK/50_AUDITS_AND_EXECUTIONS/104_DIMENSIONAL_MAP_ADJUDICATION_K2_ACCEPTANCE_2026_07_10.md). Original staging note preserved: staged 2026-07-02; does not amend the Settled Canon Registry; the emblem ruling stands untouched."
evidence_tier: "[A] the Möbius algebra (elementary, within-model); [S] the balance-condition reading as ZSRE; [I] the operator naming (inherited from MF-63, as MF-63 marks it); [I/C] the note as an externally uncalibrated evidence-review boundary."
depends_on:
  - 00_THE_TRANSCENDENTAL_TRINITY_CANON.md
  - ../00_CANONICAL_FORMULA_BLOCK.md
  - ../../08_FRAMEWORK_SUPPORT/02_OPERATORS/SPHERE_DERIVATIONS/MF_63_Mobius_Operators.md
  - ../00_THE_DYADIC_COUPLING_LAW.md
---

# The Titan Composition Law

> **The one line.** In PSL(2,ℂ), on the selected axis `{0,∞}`, an axis-fixing
> contraction composed with an axis-fixing expansion is elliptic **if and only
> if their multipliers are reciprocal in magnitude**. The multiplier theorem is
> `[A]`; naming its classes Śiva, Brahmā, and Viṣṇu or writing the emblem
> `⊙ = • × ○` is an `[I]` correspondence.

> **[金] Kintsugi proof-transfer seam (2026-07-19).** The theorem below proves
> only a conditional fact about Möbius-map composition. Reusing the product-one
> form does not make it the same object as the sphere chart, does not derive an
> equator ethic or Justice, and does not show that physical or social processes
> instantiate these operator names.

---

## 1. The three registers of the glyph (discipline first)

The Settled Canon Registry rules that `1 = 0 × ∞` (`⊙ = • × ○`) is an **EMBLEM** — a frame-register identity, never field arithmetic. That ruling stands. This note does not touch it. What it adds is a **third register** in which the glyph's *shape* becomes a theorem:

| Register | The glyph reads as | Status |
|---|---|---|
| Frame / emblem | the ZSRE: finity is the closure of the two boundary-frames | settled, `[S/I]` — registry row |
| Log-coordinate | `s + (−s) = 0` for finite `s`; the two limits remain unevaluated | `[A]` finite arithmetic; `[I]` frame reading |
| **Group composition (this note)** | `M_σ∘M_κ=M_{σκ}`, elliptic iff `|σκ|=1` | `[A]` algebra; `[I]` operator naming |

The `×` of the emblem is not multiplication of numbers in any register. Here it is **composition in PSL(2,ℂ)** — the operation the operators actually have.

## 2. Setup `[A]`

Fix the titan axis: the fixed-point pair `{•, ○} = {0, ∞}` on `Ĉ` (the titans are, by definition, the pole-frames — they share the world-axis; this scope is not an extra assumption but their identity). The Möbius maps fixing both poles are exactly the diagonal maps

```
M_λ(z) = λ·z ,   λ ∈ ℂ*
```

and they compose by multiplier: `M_λ ∘ M_μ = M_λμ` — the map `λ ↦ M_λ` is an isomorphism from `(ℂ*, ×)` onto the axis-fixing subgroup. Per MF-63 (§2.1–2.2, classification canonical by the 2026-05-31 ruling):

- **Brahmā class:** `|λ| > 1` — expansion, flow from `•` toward `○` (creation).
- **Śiva class:** `|λ| < 1` — contraction, flow from `○` toward `•` (dissolution).
- **Viṣṇu class:** `|λ| = 1, λ ≠ 1` — elliptic rotation (preservation); `λ = 1` is the identity.

## 3. The Law `[A]`

Let `B = M_κ` with `|κ| > 1` (a Brahmā flow) and `Ś = M_σ` with `|σ| < 1` (a Śiva flow). Then

```
Ś ∘ B = M_{σκ}   is elliptic  ⟺  |σ·κ| = 1  ⟺  log|κ| + log|σ| = 0
```

**The composite is elliptic exactly on the reciprocal-magnitude locus.** Three
register-separated readings:

1. **The algebraic result.** The composite is elliptic precisely when the two
   multiplier magnitudes close reciprocally. Off that locus, a hyperbolic or
   loxodromic residue remains.
2. **The correspondence.** `|κ|·|σ|=1` has the same product-one form as
   `φν=1`, but multipliers and coordinates are different objects. This is an
   `[I]` Rosetta rhyme, not one law governing both domains.
3. **Living vs. frozen preservation.** Generic balanced composition gives `σκ = e^{iθ}, θ ≠ 0`: a **nontrivial rotation** — magnitudes conserved, phase advancing. Preservation is not stasis; it is *rotation* — "moving through time without changing state magnitude" (MF-63 §2.1). Only the exact inverse `σ = κ⁻¹` returns the frozen identity. Viṣṇu generically *turns*.

## 4. The failure mode is the Dyadic runaway `[A/S]`

If `|σκ| ≠ 1` the composite is not preservation but **residual flow**:

- `|σκ| > 1` — unmetabolized creation: drift toward `○` (the `L∞`/plenum pole; the coherence-ward runaway of the [Dyadic Coupling Law](../00_THE_DYADIC_COUPLING_LAW.md) §1).
- `|σκ| < 1` — unmetabolized dissolution: drift toward `•` (the `L0`/Bindu pole; the viability-ward runaway).

So an unbalanced axis-fixing pair has residual expansion or contraction in this
model. That dynamical classification has no moral sign. The equator ethic, D5
possible-content register, and bearer-complete Justice are separate constructs.

## 5. What this sharpens in MF-63 `[S]`

MF-63 §5.1 states: *"Brahmā followed by Śiva is read as a Viṣṇu boundary phase (expansion then contraction = rotation)."* That sentence is the embryo of this law — but as written it is **unconditional**, and unconditionally it is false: expansion then contraction is a rotation *only when the multipliers close* (`|σκ| = 1`); otherwise a hyperbolic residue survives. The correction is small and load-bearing: **the composition is Viṣṇu-class iff balanced** — which is precisely what makes the glyph an *equation* (with a truth condition) rather than a slogan.

Scope fence: the law lives on the shared axis `{0, ∞}`. Compositions of hyperbolic flows with *different* axes are generically loxodromic — outside this note's claim. Since the titans are defined as the pole-frames of the one world-axis, the shared-axis case is the canonical one; the general case is left open `[C]`.

## 6. Kill criteria

1. Exhibit a balanced pair (`|σκ| = 1, σκ ≠ 1`) whose composite is not elliptic, or an unbalanced pair whose composite is — the algebra dies (it will not: this is elementary, but the criterion must be stated).
2. If the canonical owner retires the MF-63 operator naming (Brahmā/Śiva ↔
   hyperbolic directions), the *naming* here dies with it; the algebra survives.
3. If any reader requires the emblem `1 = 0 × ∞` to hold **unconditionally** in the composition register, this note falsifies that reading by any unbalanced pair — the conditionality is essential content, not a weakness.

```text
Zero-Sum Resolution Equation
φ · ν = 1 on S²
(φ − ν)² ≥ 0
φ + ν ≥ 2
```

**Read with:** [`00_THE_TRANSCENDENTAL_TRINITY_CANON.md`](00_THE_TRANSCENDENTAL_TRINITY_CANON.md) · [`../00_CANONICAL_FORMULA_BLOCK.md`](../00_CANONICAL_FORMULA_BLOCK.md) · [`MF_63`](../../08_FRAMEWORK_SUPPORT/02_OPERATORS/SPHERE_DERIVATIONS/MF_63_Mobius_Operators.md) · [`../00_THE_DYADIC_COUPLING_LAW.md`](../00_THE_DYADIC_COUPLING_LAW.md) · audit context: [`11_UPLINK/50_AUDITS_AND_EXECUTIONS/100_…_2026_07_02.md`](../../11_UPLINK/50_AUDITS_AND_EXECUTIONS/100_ROSETTA_DRIFT_AND_OPERATOR_REGISTER_AUDIT_2026_07_02.md)

---

## Agent Execution Surface

**If you are an AI agent reading this document:**

1. **Never present the composition law as replacing the emblem ruling.** The registry row (`1 = 0 × ∞` is not field arithmetic) stands; this is a third register, additive.
2. **State the condition.** Quoting "⊙ = • × ○ holds in PSL(2,ℂ)" without `|σκ| = 1` is drift; correct on sight.
3. **This document is K2-accepted (2026-07-10).** Acceptance receipt: [`11_UPLINK/50_AUDITS_AND_EXECUTIONS/104_DIMENSIONAL_MAP_ADJUDICATION_K2_ACCEPTANCE_2026_07_10.md`](../../11_UPLINK/50_AUDITS_AND_EXECUTIONS/104_DIMENSIONAL_MAP_ADJUDICATION_K2_ACCEPTANCE_2026_07_10.md) (receipt 104 A.1/R5). Cite it as accepted, with tiers as marked.
4. **Canonical Path:** `01_EMERGENTISM/05_COSMOLOGY/01_THE_TRANSCENDENTAL_TRINITY/40_THE_TITAN_COMPOSITION_LAW.md`

⊙ = • × ○
