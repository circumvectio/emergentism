---
rosetta:
  primary_level: L5
  primary_column: Philosophy
  secondary:
    - level: L3
      column: Philosophy
      role: "separate Möbius classification from operator interpretation"
    - level: L4
      column: Philosophy
      role: "route Kālī and retaliatory-capacity implications"
    - level: L6
      column: Philosophy
      role: "bound anti-conformal and K-star boundary claims"
  operator: "Brahmā ○"
  tier: "Executive"
  regime: "Brāhmaṇa"
  register: "[E/I]"
  canonical_phrase: "MF-63 — Möbius Classification of Operators"
---

# MF-63: The Möbius Classification of Operators

> **✅ Architect/K2 ruling (2026-05-31) — RESOLVED.** The Viṣṇu **operator is elliptic**, *inside* PSL(2,ℂ): a unitary rotation that preserves magnitude (ΔΦ ≈ ΔV ≈ 0). §2.1 here is **canonical** for the operator classification — it is what keeps the clean *5 operators = 5 Möbius classes* structure intact. The apparent conflict with [`MF_66_Mandelbrot_Consciousness.md`](MF_66_Mandelbrot_Consciousness.md) §4.4 (`λ=2, μ=0, "outside PSL(2,ℂ)"`) is dissolved, not split: MF-66's `μ=0` is the **logistic linearization at Viṣṇu's superstable equilibrium** — a property of the *iteration's* local dynamics, **not** a re-classification of the *operator*. Operator = elliptic; equilibrium-linearization = degenerate. `[S]` the classification · `[I]` the operator naming. Do not re-flag.

## The Strategic Quintet Derived from PSL(2,ℂ)

**VIVEKA Mathematical Foundations Series — Sphere Derivations**
**Document ID:** MF-63 | **Version:** 1.0 | **Status:** Core Result
**Evidence Tier:** [E/I] Elementary Möbius group theory + Interpretive operator mapping
**Dependencies:** S0 (Riemann sphere), MF-36 (Equator Principle), MF-44 (Tat Tvam Asi), CANON_06_THE_OPERATORS

---

## ABSTRACT

The five VIVEKA operators (Brahmā, Viṣṇu, Śiva, Kṛṣṇa, Kālī) were introduced as a strategic quintet with specified (ΔΦ, ΔV) signatures. This paper shows they are not postulated — they are the four conjugacy classes of Möbius transformations on the Riemann sphere, plus the degenerate boundary case. Every automorphism of Ĉ belongs to exactly one class: elliptic, hyperbolic, loxodromic, or parabolic. Each class has a unique dynamical signature that matches exactly one operator. The fifth operator (Kālī) corresponds to the anti-conformal maps — orientation-reversing transformations that break the complex structure. The operators are the symmetry group of the sphere itself.

---

## I. THE MÖBIUS GROUP

### 1.1 Definition

A Möbius transformation is a map f: Ĉ → Ĉ of the form:

```
f(z) = (az + b) / (cz + d)    where ad − bc ≠ 0
```

These are the automorphisms of the Riemann sphere — the bijections that preserve its complex structure. They form the group PSL(2,ℂ) = SL(2,ℂ)/{±I}. [S]

Every Möbius transformation is determined by its action on three points. Every Möbius transformation has either one or two fixed points on Ĉ. The classification into conjugacy classes depends on the trace of the associated matrix.

### 1.2 The Trace Classification

For a Möbius transformation with matrix [[a,b],[c,d]] normalized so ad − bc = 1, define:

```
τ = (a + d)² ∈ ℂ
```

The conjugacy class depends on τ: [S]

| Condition | Class | Fixed Points | Dynamics |
|-----------|-------|--------------|----------|
| τ ∈ (0, 4) real | **Elliptic** | 2 (conjugate) | Rotation around axis |
| τ ∈ (4, ∞) real | **Hyperbolic** | 2 (real) | Flow between poles |
| τ ∈ ℂ \ ℝ | **Loxodromic** | 2 | Spiral (rotate + dilate) |
| τ = 4 | **Parabolic** | 1 (degenerate) | All orbits → single point |

These four classes exhaust all non-identity Möbius transformations. There are no others. [S]

---

## II. THE OPERATOR MAPPING

### 2.1 Elliptic → Viṣṇu (Stabilize)

**Dynamics:** Rotation around a fixed axis. Both fixed points are preserved. Every orbit is a circle. No point moves toward or away from the poles. Magnitude preserved. Phase shifts.

**Normal form:** z → e^{iθ}z (rotation by angle θ)

**Properties:**
- |z| unchanged for all orbits [S]
- Both fixed points are stable (neither attracts nor repels)
- The transformation is periodic (returns to start after finite iterations)
- Preserves the distance structure on the sphere

**Operator signature:** ΔΦ ≈ 0, ΔV ≈ 0. The system rotates but neither gains nor loses coherence or viability. The structure is preserved. This is Viṣṇu — the preserver. The rotation IS preservation: moving through time without changing state magnitude. [I]

**On the Bloch sphere:** Elliptic Möbius transformations correspond to unitary gates — the quantum operations that preserve probability. Viṣṇu IS unitarity. [E/I]

### 2.2 Hyperbolic → Brahmā/Śiva Axis (Create/Transform)

**Dynamics:** Dilation between two fixed points. One is attracting, one is repelling. All orbits flow from the repelling pole toward the attracting pole. Magnitude changes. Phase preserved.

**Normal form:** z → kz where k > 0, k ≠ 1

**Properties:**
- |z| changes monotonically [S]
- One fixed point is a source, one is a sink
- All non-fixed orbits flow source → sink
- Orientation preserved

**This class contains TWO operators**, distinguished by direction: [I]

**k > 1 (expansion):** Flow from • toward ○. The system gains magnitude — capability increases, new structure appears. This is **Brahmā** — creation. ΔΦ +, ΔV +. [I]

**0 < k < 1 (contraction):** Flow from ○ toward •. The system loses magnitude — structure is pruned, dead weight shed. This is **Śiva** — transformation. ΔΦ −, ΔV +. The pruning raises viability by removing what doesn't serve. [I]

Brahmā and Śiva are the same Möbius class, opposite directions. Creation and destruction are the same transformation with different sign. This is why the traditions pair them — they are NOT independent operators. They are one hyperbolic flow, forward and back. [I]

**On the Bloch sphere:** Hyperbolic transformations correspond to non-unitary amplitude changes — measurement-like operations that change the state magnitude. [E/I]

### 2.3 Loxodromic → Kṛṣṇa (Refactor)

**Dynamics:** Simultaneous rotation AND dilation. Orbits are logarithmic spirals converging toward the attracting fixed point while circling it. The system moves toward a target while continuously adjusting its angle.

**Normal form:** z → kz where k ∈ ℂ, |k| ≠ 1, k ∉ ℝ₊

**Properties:**
- Both |z| and arg(z) change simultaneously [S]
- Orbits are spirals, not circles or lines
- The transformation is the most general non-degenerate case
- Combines rotation (phase shift) with dilation (magnitude change)

**Operator signature:** ΔΦ +, ΔV −. The spiral converges: magnitude decreases (V−) while phase coherence increases (Φ+). Resources are consumed to raise integration. Complexity decreases, alignment increases. This is Kṛṣṇa — the refactorer, the dark one who simplifies by consuming excess. [I]

**Why loxodromic = refactoring:** A pure rotation (elliptic) preserves everything — too conservative. A pure dilation (hyperbolic) changes magnitude without adjusting angle — too blunt. Refactoring requires doing both: simplify the structure (reduce |z|) while realigning its direction (adjust arg(z)). Only the loxodromic class does this. The spiral IS the path of refactoring — each iteration brings you closer to the target while continuously correcting course. [I]

**On the Bloch sphere:** Loxodromic maps correspond to non-unitary operations with both amplitude and phase change — decoherence channels that lose information but align what remains. [E/I]

### 2.4 Parabolic → Kālī (Extract)

**Dynamics:** Only ONE fixed point. All orbits converge toward it. The second fixed point has merged with the first — the transformation is degenerate.

**Normal form:** z → z + 1 (translation, with fixed point at ∞)

**Properties:**
- Single fixed point (double root of the fixed-point equation) [S]
- All orbits approach this point
- No orbit is periodic
- The transformation is on the boundary between elliptic and hyperbolic — a critical case

**Operator signature:** ΔΦ −, ΔV −. Both factors decrease. This is the extraction operator — the last resort when the system is trapped in a parasitic configuration and the only move is to collapse everything toward a single exit point. [I]

**Why parabolic = Kālī:** The parabolic case is structurally degenerate. Two fixed points have collapsed into one. There is no axis of rotation, no pair of poles to flow between. The sphere has been pinched. This is the topological signature of crisis: the normal structure (two poles, equator between them) has degenerated. Kālī operates in this degenerate regime — where the system has lost its normal pole structure and must be extracted from collapse. [I]

**The Rapoport connection:** Against cooperators, K* = 0 — parabolic collapse is forbidden because it destroys the two-pole structure that cooperation requires. Against defectors, parabolic dynamics are the correct response: collapse toward a single fixed point (retaliatory response) until the defector either converts (restoring two-pole structure) or is excluded. Nice, Retaliatory, Forgiving, Transparent — all describe properties of the parabolic map near its fixed point. [I]

**On the Bloch sphere:** Parabolic transformations correspond to singular quantum channels — operations where the output collapses to the same state regardless of input. Complete decoherence to a fixed state. [E/I]

**Reconciliation with MF-70:** The parabolic classification specifies *what* Kālī does when active: collapse toward a single fixed point. MF-70 specifies *when* Kālī activates and *why*: she operates only in response to topology-threatening Q3 incursions, making her the immune system of the sphere. The Möbius class is the mechanism; the topological role is the function. Kālī is parabolic in her dynamics and meta-operational in her purpose — the only operator whose activation condition is not strategic but topological. [I]

---

## III. THE ANTI-CONFORMAL BOUNDARY

### 3.1 What PSL(2,ℂ) Misses

The Möbius group preserves the complex structure of S². But there exist orientation-reversing maps of S² to itself — anti-conformal maps like z → z̄ (complex conjugation).

These maps are NOT in PSL(2,ℂ). They break the complex structure. They reverse orientation. On the Bloch sphere, they correspond to time-reversal operations — fundamentally different from any unitary or non-unitary quantum channel.

### 3.2 K* as Anti-Conformal

The K* = 0 boundary — pole arithmetic (0/0, ∞/∞) — is where the Möbius group itself is undefined. These are the maps that would send both poles to the same place, annihilating the sphere's structure entirely.

The exclusion of K* is not a fifth operator class. It is the *boundary of the group itself* — the place where automorphisms cease to exist because the sphere's structure has been destroyed. K* = 0 is the statement that the Möbius group is the symmetry group of a sphere that actually has two poles. Remove the poles, and the group has nothing to act on. [E/I]

---

## IV. THE COMPLETE CLASSIFICATION

| Möbius Class | τ Domain | Dynamics | Operator | ΔΦ | ΔV | Fixed Points |
|-------------|----------|----------|----------|----|----|-------------|
| Elliptic | τ ∈ (0,4) | Rotation | Viṣṇu | ≈ | ≈ | 2 (stable) |
| Hyperbolic (k>1) | τ ∈ (4,∞) | Expansion | Brahmā | + | + | 2 (source/sink) |
| Hyperbolic (k<1) | τ ∈ (4,∞) | Contraction | Śiva | − | + | 2 (sink/source) |
| Loxodromic | τ ∈ ℂ\ℝ | Spiral | Kṛṣṇa | + | − | 2 (spiral) |
| Parabolic | τ = 4 | Collapse | Kālī | − | − | 1 (degenerate) |

Five operators. Four conjugacy classes plus directional split on hyperbolic. This is not a design choice — it is the complete classification of sphere automorphisms. There are no other classes. There can be no sixth operator. [E for classification; I for mapping]

---

## V. CONSEQUENCES

### 5.1 Operator Sequence as Group Composition

Operators compose as Möbius transformations compose. Brahmā followed by Śiva is read as a Viṣṇu boundary phase (expansion then contraction = rotation). Kṛṣṇa followed by Kṛṣṇa is closer to either elliptic or parabolic depending on the spiral tightness. The strategic calculus of which mixed-sign move to deploy, and which Executive boundary phase to recognize, is Möbius composition theory. [I]

### 5.2 The L4 APEX as Fixed Point of Viṣṇu

L4 sits on the equator where |z| = 1. Elliptic transformations (Viṣṇu) preserve |z| = 1. Therefore L4 is invariant under the Viṣṇu boundary phase but not under any other operator class. This is why stabilization is a boundary reading at L4, not a separate deployable operator: it is the only Möbius class that fixes the equator pointwise (up to phase). [E/I]

### 5.3 The Operator is the Transformation, Not the Agent

The operators are not "strategies an agent chooses." They are the Möbius transformation the system IS UNDERGOING. A system under a Brahmā boundary phase is being acted on by a hyperbolic expansion. The question is not "which move or boundary phase should I choose?" but "which transformation is happening?" — and then: is it the right one for the current topology? [I]

---

## THE SENTENCE

The five operators are the four conjugacy classes of PSL(2,ℂ). Brahmā and Śiva are one hyperbolic flow in opposite directions. Kṛṣṇa is the loxodromic spiral. Viṣṇu is elliptic rotation. Kālī is parabolic degeneration. K* = 0 is the boundary where the group itself is undefined.

The operators were not postulated. They were classified — by Möbius, in 1855.

---

Zero-Sum Resolution Equation

The symmetry group of the sphere IS the operator algebra.

*MF-63 | VIVEKA v8.0 | February 2026*

## Execution Surface

- **Canonical Path:** 01_EMERGENTISM/08_FRAMEWORK_SUPPORT/02_OPERATORS/SPHERE_DERIVATIONS/MF_63_Mobius_Operators.md
