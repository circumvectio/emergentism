---
rosetta:
  primary_level: L5
  primary_column: Philosophy
  secondary:
    - level: L3
      column: Philosophy
      role: "audit surface for formula tracking across corpus"
  operator: "Brahmā ○"
  tier: "Executive"
  regime: "Brāhmaṇa"
  register: "[A/S/C] — per statement"
  canonical_phrase: "Canonical Formula Block — chart facts and node models kept distinct"
  vmosk_a_ref: "01_EMERGENTISM/VMOSK_A.md — Perennial Doctrine Root"
---

# The Canonical Formula Block

**Status:** Active — Kintsugi repair, 2026-07-19
**Evidence:** `[A]` analytic chart facts · `[S]` declared model interfaces ·
`[I]` interpretations · `[C]` empirical or ontological wagers
**Purpose:** Keep exact mathematics, selected models, and philosophical readings
in different types.

> **[金] Kintsugi seam.** This owner supersedes the semantic inflation preserved
> in Git blob `6c977be4a4b342c3a60f83664800a04a6da045e9`. The old formulas remain
> provenance, but no longer license “world-building grammar,” empirical
> conservation, ontology, or ethics. The crack was not the algebra. It was the
> inference from a chosen chart to the world.

## 1. The chart block `[A]`

For colatitude `θ ∈ (0,π)`, define the positive dual coordinates

```text
φ = cot(θ/2)
ν = tan(θ/2)
```

Then, by elementary trigonometry,

```text
φν = 1
(φ − ν)² ≥ 0
φ + ν ≥ 2
B := 2/(φ + ν) = sin θ ≤ 1
```

Equality in the last two inequalities holds exactly at
`φ = ν = 1`, equivalently `θ = π/2`. In log coordinates
`s = log ν = −log φ`, the same facts are

```text
log φ + log ν = 0
φ + ν = 2 cosh(s)
B = sech(s)
```

These are analytic consequences of the coordinate definitions. They do **not**
establish an empirical conservation law, a necessary ontology, a moral rule, or
the finite-node product model. At the poles, `0` and `∞` are extended-coordinate
limits; the ordinary product `0·∞` is not defined.

### Polar through-point chord construction `[A]`

Let `N` and `S` be the north and south poles of a sphere of radius `R`, and let
`P` have colatitude `θ`. The two polar chords sharing `P` have lengths

```text
|SP| = 2R cos(θ/2)
|NP| = 2R sin(θ/2).
```

For the unit sphere, their diameter-normalized reaches are

```text
u := |SP|/2 = cos(θ/2)
d := |NP|/2 = sin(θ/2).
```

Their product therefore gives a second exact construction of the balance
function:

```text
B_chord := 2ud = sin θ = B ≤ 1,
```

with equality exactly at `θ=π/2`. For arbitrary radius, the same normalization
is

```text
B_chord = |SP||NP|/(2R²) = sin θ.
```

Equivalently, normalize each polar chord by its equatorial length `√2 R`; the
product of those two normalized lengths is `B` directly.

The axial projection gives the squared form. With `z=cos θ`, the two segments
of the polar diameter cut by the axial projection of `P` have lengths
`R(1+z)` and `R(1−z)`. Hence

```text
[R(1+cos θ)][R(1−cos θ)] = R² sin² θ,
```

or, on the unit sphere,

```text
(1+cos θ)(1−cos θ) = sin² θ = B².
```

The chord reaches and chart shadows are related but not identical:

```text
φ = u/d = cot(θ/2)
ν = d/u = tan(θ/2)
φν = 1
B = 2ud = 2/(φ+ν).
```

Thus `φν=1` is the constant product of reciprocal **ratios**, while
`2ud=B` is the varying product of normalized **chord reaches**. The chord
theorem is a real analytic result and a useful alternative construction of
`B`; it does not prove the uppercase node product, an ontology, or a moral law.

### Inversion precision `[A/S]`

For `J_inv(z)=1/z` on the projective line,

```text
Fix(J_inv) = {−1,+1}
J_inv(0)=∞
J_inv(∞)=0
```

On the positive ray, `+1` is the only fixed point. The set
`{−1,0,+1,∞}` is a **selected `J_inv`-invariant union** of the fixed set and the
two-point orbit `{0,∞}`; it is not the orbit or topological closure of
`{0,∞}`.

The glyph `⊙ = • × ○` is an Emergentist emblem `[I]`, never the arithmetic
assertion `1 = 0 × ∞`. Its apophatic companion is

```text
• = ⊙ / ○
```

read as **“not this, not this”**: the positive whole is divided away toward the
unasserted ground. It is likewise an emblem, not a field proof that bare
`1/∞=0` supplies an ontology. Where a projective limit or extended-number
convention assigns such a value, that mathematical convention remains
separate from the symbolic reading.

## 2. The normalized node block `[S/C]`

The uppercase symbols belong to a different type:

```text
Φ,V ∈ [0,1]
```

`Φ` denotes normalized modeled-foresight/coherence and `V` normalized usable
embodied means/viability for the stated boundary and time horizon. Their values
require an explicit operationalization; they are not lowercase sphere
coordinates.

A normalized **conjunctive aggregator** is any declared

```text
C : [0,1]² → [0,1]
```

such that it is monotone in each argument,
`C(0,V)=C(Φ,0)=0`, and `C(1,1)=1`. These conditions express the AND-class
claim that both factors are necessary. They do not choose a unique interior
ranking.

Emergentism selects the product member

```text
P_node := C×(Φ,V) := ΦV
```

as its normalized working model. This equality is structural by declaration
`[S]`; its adequacy as a universal fit is `[C]`. The bound
`0 ≤ P_node ≤ 1` follows from the normalization domain, not from the Burri
sphere. Under the additional fixed-budget condition `Φ+V=c`, the product is
maximized at balance and satisfies `ΦV≤c²/4`; that is a product-specific AM–GM
result, not a general law of all conjunctive aggregators.

`min(Φ,V)` is a useful bottleneck statistic but is not forced as the native
score. It can rank cases differently from the product: `(0.2,1)` exceeds
`(0.4,0.4)` under the product (`0.20>0.16`) while the minimum ranks them in the
opposite order (`0.20<0.40`). Product, minimum, harmonic, and Cobb–Douglas
members are therefore not interchangeable without evidence.

## 3. The future-action compression `[I/S]`

The public phrase

```text
F = M × A
```

is retained as mnemonic only. Its typed form is

```text
F_modelled := M ⋆ A
```

where `M` is a fallible model of possible futures, `A` is an agent's available
means and commitments, and `⋆` is a domain-specified coupling—not ordinary
multiplication. A represented future may reweight present selection. The
realized outcome still depends on the environment, constraints, other agents,
and chance. This is model-mediated future influence, not a physical signal from
the future.

## 4. Canonical quotation and anti-drift rule

When the framework is compressed, quote the chart, chord, and node blocks as
separate constructions:

```text
Chart [A]: φ=cot(θ/2), ν=tan(θ/2) ⇒ φν=1 and B≤1.
Chord [A]: u=cos(θ/2), d=sin(θ/2) ⇒ 2ud=B≤1.
Node [S/C]: Φ,V∈[0,1]; P_node:=ΦV is the selected conjunctive model.
```

Correct these failures on sight:

- calling `φν=1` a discovered empirical conservation law;
- deriving `P_node=ΦV`, ethics, Being, or a D-ladder from the chart identity;
- deriving `P_node=ΦV`, morality, or ontology from the chord product `2ud=B`;
- using lowercase `φ,ν` for measured node factors;
- saying the sphere uniquely chooses the product or the minimum;
- using the product ceiling without declaring normalization;
- treating `0×∞=1` as field arithmetic;
- claiming `{−1,0,1,∞}` is generated by the orbit of `{0,∞}`;
- interpreting `F_modelled=M⋆A` as physical retrocausality.

## 5. Kill and upgrade criteria

- An algebraic counterexample repairs the `[A]` line immediately.
- A valid measurement protocol may promote a node factor from stipulated to
  empirical, but never promotes the chart's philosophical readings with it.
- Comparative data that reliably favors another conjunctive aggregator replaces
  the selected product for that domain.
- A reproducible physical discriminator is required before any future-to-past
  mechanism can be claimed; altered present choice after altering a represented
  future supports only model-mediated influence.

---

## Agent Execution Surface

1. Name the register: chart, node, action, or interpretation.
2. Preserve lowercase/uppercase typing.
3. Do not transfer proof across registers through analogy.
4. Use this file as the formula owner; later documents may interpret it but may
   not merge its types.

**Canonical path:**
`01_EMERGENTISM/05_COSMOLOGY/00_CANONICAL_FORMULA_BLOCK.md`

⊙ = • × ○

• = ⊙ / ○ — *not this, not this; emblem, not arithmetic.*
