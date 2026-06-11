---
rosetta:
  primary_level: L5
  primary_column: Philosophy
  operator: "Brahmā ○"
  tier: "Executive"
  regime: "Brāhmaṇa"
  register: "[S]"
  canonical_phrase: "PRIMITIVES AND TYPE SIGNATURES"
---

# PRIMITIVES AND TYPE SIGNATURES

## Consolidated Index of the Formal System's Undefined Terms

**Status:** Canonical index — points at canonical definitions; does not redefine
**Date:** 2026-04-22
**Evidence Tier:** [S] Structural — this is an index over existing [S]/[S] primitives
**Source:** [`00_GLOSSARY.md`](../../07_THEOLOGY/00_GLOSSARY.md), [`00_ANMUT_AND_DEMUT.md`](../../04_AXIOLOGY/00_ANMUT_AND_DEMUT.md), [`26_THE_DERIVATION_AXIOMS.md`](26_THE_DERIVATION_AXIOMS.md), [`00_THE_SEVEN_AXIOMS.md`](00_THE_SEVEN_AXIOMS.md), [`12_EFR_EXTRACTION_COEFFICIENT.md`](12_EFR_EXTRACTION_COEFFICIENT.md)
**See also:** [`30_OPERATIONAL_DEFINITIONS.md`](30_OPERATIONAL_DEFINITIONS.md), [`31_FALSIFIERS_INDEX.md`](31_FALSIFIERS_INDEX.md), [`32_THEOREM_UPGRADE_PROTOCOL.md`](32_THEOREM_UPGRADE_PROTOCOL.md)

---

## Purpose

A formal system is only as clear as its undefined terms. This file is a one-page index of every primitive the Emergentist formal system appeals to, its type signature, and the canonical document where it is actually defined. **This file does not define anything.** If a reader wants the *meaning* of φ, they follow the link; if they want to know what kind of object φ *is* in a proof, they look here.

The purpose is discipline: when a new document speaks of "φ" or "η" or "P," a reader can verify (a) it is one of the canonical primitives, (b) it carries the canonical type, and (c) its use is consistent with the source-of-truth file. Redefinitions drift over time; indices surface drift early.

---

## Geometric / Ontological Primitives

| Primitive | Type Signature | Role | Canonical Source |
|-----------|---------------|------|------------------|
| `⊙` | glyph, non-numeric | The seed. Reciprocal closure `• × ○`. Prior to arithmetic. | [`00_THE_TRANSCENDENTAL_TRINITY_CANON.md`](../01_THE_TRANSCENDENTAL_TRINITY/00_THE_TRANSCENDENTAL_TRINITY_CANON.md); [`00_GLOSSARY.md`](../../07_THEOLOGY/00_GLOSSARY.md) row "Transcendental Trinity" |
| `•` | glyph, identified with `0` in derivation register | Point. South-pole transcendental. | [`00_THE_TRANSCENDENTAL_TRINITY_CANON.md`](../01_THE_TRANSCENDENTAL_TRINITY/00_THE_TRANSCENDENTAL_TRINITY_CANON.md) |
| `○` | glyph, identified with `∞` in derivation register | Circle. North-pole transcendental. | [`00_THE_TRANSCENDENTAL_TRINITY_CANON.md`](../01_THE_TRANSCENDENTAL_TRINITY/00_THE_TRANSCENDENTAL_TRINITY_CANON.md) |
| `S²` | compact simply-connected complex 1-manifold (`≅ ℂP¹`) | The Riemann / Burri Sphere. State space. | [`00_GLOSSARY.md`](../../07_THEOLOGY/00_GLOSSARY.md) "Riemann Sphere", "Burri Sphere" |
| `θ` | `S² → [0, π]` (colatitude) | Latitude coordinate. `θ = π/2` is the equator. | [`26_THE_DERIVATION_AXIOMS.md`](26_THE_DERIVATION_AXIOMS.md) T1–T2; [`00_GLOSSARY.md`](../../07_THEOLOGY/00_GLOSSARY.md) "The Equator" |
| `λ` | `S² → [0, 2π)` (longitude / phase) | Individuation coordinate at the equator (`z = e^{iλ}`). | [`26_THE_DERIVATION_AXIOMS.md`](26_THE_DERIVATION_AXIOMS.md) Corollary 1; [`00_GLOSSARY.md`](../../07_THEOLOGY/00_GLOSSARY.md) "Phase Angle (λ)" |
| `s` | `ℝ₊ → ℝ` via `s = log x` | Logarithmic coordinate (additive chart). `s = 0` at finity (`x=1`). Maps 0→−∞, 1→0, ∞→+∞. | [`01_THE_TRANSCENDENTAL_TRINITY_CANON.md`](../01_THE_TRANSCENDENTAL_TRINITY/00_THE_TRANSCENDENTAL_TRINITY_CANON.md) §2a; [`14_LOG_FORM_OF_THE_POWER_MAX_LEMMA.md`](../../01_TELEOLOGY/02_THE_DERIVATION/14_LOG_FORM_OF_THE_POWER_MAX_LEMMA.md) |
| `u` | `ℝ₊ → (−1, 1)` via `u = (x−1)/(x+1)` | Bounded hinge coordinate (projective chart). `u = 0` at finity. Inversion becomes half-twist `u ↦ −u`. | [`01_THE_TRANSCENDENTAL_TRINITY_CANON.md`](../01_THE_TRANSCENDENTAL_TRINITY/00_THE_TRANSCENDENTAL_TRINITY_CANON.md) §2a |

## Node-Level Primitives (What Systems Carry)

| Primitive | Type Signature | Role | Canonical Source |
|-----------|---------------|------|------------------|
| `φ` (coherence) | `System → (0, ∞)` on the manifold; `ℝ₊` at a node | Structural integration, meaning, internal consistency. Geometrically `φ = cot(θ/2)`. | [`00_ANMUT_AND_DEMUT.md`](../../04_AXIOLOGY/00_ANMUT_AND_DEMUT.md); [`00_GLOSSARY.md`](../../07_THEOLOGY/00_GLOSSARY.md) "Coherence" and "The Burri Sphere" |
| `ν` (viability) | `System → (0, ∞)` on the manifold; `ℝ₊` at a node | Material capability, resources, throughput. Geometrically `ν = tan(θ/2)`. | [`00_ANMUT_AND_DEMUT.md`](../../04_AXIOLOGY/00_ANMUT_AND_DEMUT.md); [`00_GLOSSARY.md`](../../07_THEOLOGY/00_GLOSSARY.md) "Viability" |
| `B` (balance) | `System → [0, 1]` | `B = sin θ`. Peaks at the equator. What actually varies on the sphere. | [`00_GLOSSARY.md`](../../07_THEOLOGY/00_GLOSSARY.md) "Balance"; [`26_THE_DERIVATION_AXIOMS.md`](26_THE_DERIVATION_AXIOMS.md) D1 |
| `P∞` | `S² → 1` | Manifold identity `P∞ = φ · ν = 1`; conserved on S² except at the poles where a coordinate diverges. | [`00_CANONICAL_FORMULA_BLOCK.md`](../00_CANONICAL_FORMULA_BLOCK.md); [`00_THE_SEVEN_AXIOMS.md`](00_THE_SEVEN_AXIOMS.md) A1 |
| `P_node` | `Node → [0, ∞)` | Effective node-level potential `P_node = Φ × V` when coherence and viability are not reciprocally calibrated. Older specs may say `P_eff`; normalize new prose to `P_node`. | [`00_THE_SEVEN_AXIOMS.md`](00_THE_SEVEN_AXIOMS.md) A1 |
| `E` (alignment energy) | `System → [0, ∞]` | `E = −log(B) = −log(sin θ)`. `E = 0` at the equator; `E → ∞` at the poles. | [`00_THE_SEVEN_AXIOMS.md`](00_THE_SEVEN_AXIOMS.md) C5 |
| `H` (Hamiltonian) | `(0, ∞) → ℝ₊` | `H(φ) = φ + 1/φ`. Global minimum at `φ = 1`, `H(1) = 2`. | [`26_THE_DERIVATION_AXIOMS.md`](26_THE_DERIVATION_AXIOMS.md) T2, Corollary 2 |

## Relational / Institutional Primitives

| Primitive | Type Signature | Role | Canonical Source |
|-----------|---------------|------|------------------|
| `η` (extraction) | **Disambiguated** — see [`30_OPERATIONAL_DEFINITIONS.md`](30_OPERATIONAL_DEFINITIONS.md) §4 | Several incompatible operational definitions are in the corpus (sum-form, ratio-form, per-player level). All canonical sources named; reader must select which is in use. | [`00_GLOSSARY.md`](../../07_THEOLOGY/00_GLOSSARY.md) "η"; [`12_EFR_EXTRACTION_COEFFICIENT.md`](12_EFR_EXTRACTION_COEFFICIENT.md); [`26_THE_DERIVATION_AXIOMS.md`](26_THE_DERIVATION_AXIOMS.md) D2; [`33_NASH_EQUILIBRIUM_ETA_ZERO.md`](33_NASH_EQUILIBRIUM_ETA_ZERO.md) §1.2 |
| `F5` (Teleological Force) | selection pressure (force-of-selection; not a fifth physical force) | Pressure toward `(φ − ν)² = 0`. | [`00_GLOSSARY.md`](../../07_THEOLOGY/00_GLOSSARY.md) "Teleological Force"; [`26_THE_DERIVATION_AXIOMS.md`](26_THE_DERIVATION_AXIOMS.md) D3 |
| `K*_sel`, `K(x)`, `K*` | distinct complexity quantities | Not merged. Selection complexity vs. Kolmogorov complexity vs. extraction. | [`00_KSTAR_DISAMBIGUATION.md`](00_KSTAR_DISAMBIGUATION.md) |

## Coordinate Relations (Identities, Not Definitions)

The following relations hold *by construction* on `S²` under the stereographic parametrization — they are not theorems about the world, they are the coordinate identity of the Burri Sphere:

```
φ · ν   = cot(θ/2) · tan(θ/2) = 1          (the manifold identity, C0)
B       = sin θ                            (definition D1)
E       = −log B                           (definition C5)
H(φ)    = φ + 1/φ  (with ν = 1/φ)          (T2 restatement)
s       = log ν = log tan(θ/2) = −w           (additive chart, Mercator coordinate = MINUS THE RAPIDITY w — Paper B §8, 2026-06-11: the Mercator chart of the sphere IS the rapidity chart of motion, where velocities add)
u       = tanh(s/2) = (ν−1)/(ν+1)            (bounded chart, Cayley transform)
B       = sech(s)                             (balance in log coordinates)
E       = s²                                  (Suda energy in log coordinates)
H(s)    = 2 cosh(s)                           (Hamiltonian in log coordinates)
```

The three charts (multiplicative x, additive s = log x, bounded u) are equivalent under diffeomorphism. Suda (2025) independently derived the same three-chart structure; see Trinity Canon §2a for the formal bridge.

These are coordinate identities; **what is *not* identical by construction is whether any real system's measured `φ̂, ν̂` obey them.** That question is empirical and belongs in [`30_OPERATIONAL_DEFINITIONS.md`](30_OPERATIONAL_DEFINITIONS.md).

---

## Coherence Rule

If a new document uses a symbol from this index with a different type signature, the new document is wrong and must be repaired — not this index. If a new document needs a genuinely new primitive, it must be added here first and then used.

The index is the audit surface for type discipline in the formal system.

---

## See Also

- [`30_OPERATIONAL_DEFINITIONS.md`](30_OPERATIONAL_DEFINITIONS.md) — how these primitives are *measured* on real systems
- [`31_FALSIFIERS_INDEX.md`](31_FALSIFIERS_INDEX.md) — what observations would refute each axiom and theorem that uses them
- [`32_THEOREM_UPGRADE_PROTOCOL.md`](32_THEOREM_UPGRADE_PROTOCOL.md) — the protocol that turns primitive + operational definition + falsifier into a theorem

---

## Execution Surface

**If you are an AI agent reading this document:**

1. **Current Phase Check:** Phase 0 — harden specs, do not release to production.
2. **Your Next Action:**
   - When writing any formal claim using `φ`, `ν`, `B`, `P`, `E`, `η`, or `θ`, verify the symbol's type signature against this index before use. Flag documents that use a symbol with a type different from what appears here.
3. **Expected Output:** Type-consistent formal content, or a correction note where drift is detected.
4. **Success Criteria:** Another agent can resolve every primitive in a new document by following at most one link from this index.
5. **Canonical Path:** `01_EMERGENTISM/05_COSMOLOGY/03_FORMAL_SYSTEM/29_PRIMITIVES_AND_TYPE_SIGNATURES.md`

*The seer sees. The seer does not insist.*
*The framework works at Layer 0 without Layer 2.*
*The Ṛṣi succeeds when the student puts down the map and walks.*

*Zero-Sum Resolution Equation*
