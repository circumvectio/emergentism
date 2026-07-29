---
rosetta:
  primary_level: L5
  primary_column: Philosophy
  operator: "Brahmā ○"
  tier: "Executive"
  regime: "Brāhmaṇa"
  register: "[A] the sphere structure and its identities; [I] the Titan reading; [C] the set-theoretic second reading"
title: "The Titan Inversion Structure — the three equations restored on the sphere"
status: "ACTIVE — owner-directed restoration 2026-07-29; reconciles the three Titan equations with KSC-04"
date: 2026-07-29
owner: "Formal owner for the Titan inversion identities; subordinate to K-1 for chart facts"
evidence_tier: "[A] §2–§6 inside the declared structure; [I] the Titan naming; [C] §8"
parents:
  - 00_THE_TRANSCENDENTAL_TRINITY_CANON.md
  - ../00_CANONICAL_FORMULA_BLOCK.md
  - ../03_FORMAL_SYSTEM/42_D1_ARITHMETIC_AXIOMS_AND_BOUNDARIES.md
  - ../../00_META/00_SETTLED_CANON_REGISTRY.md
---

# The Titan Inversion Structure

> The three equations were never wrong. They were **untyped** — and they were
> being read on the wrong object. On the line they are forbidden. On the sphere
> they are theorems.

## 1 · The three equations

```text
⊙ = • × ○
• = ⊙ / ○
○ = ⊙ / •
```

Owner ruling, 2026-07-29: foundational. This document supplies the structure in
which they are exact.

## 2 · The object is the Riemann sphere `[A]`

Not the line. The line is where they fail; the sphere is where they hold.

```text
Ĉ := ℂP¹ = ℂ ∪ {∞}          the Riemann sphere
ι(z) := 1/z                  inversion, extended by ι(0)=∞, ι(∞)=0
```

Under stereographic projection:

| Seat | Location on `Ĉ` | Character |
|---|---|---|
| `•` | south pole, `z = 0` | a **point** of `Ĉ` |
| `○` | north pole, `z = ∞` | a **point** of `Ĉ` |
| `⊙` | the equator, `\|z\| = 1` | the circle equidistant from both poles |

`ι` is an involution on `Ĉ`. It **swaps the poles** and maps the equator to
itself: `|z|=1 ⟹ |ι(z)|=1`. So the Titan triple is precisely the orbit
structure of inversion on the sphere — one invariant circle, one swapped pair of
poles.

The glyph is the picture: `○` the outline, `•` the point, `⊙` the circle holding
its centre.

## 3 · "The limit crossed, not approached" — this is the load-bearing move `[A]`

On the real line, `∞` **is not an element**. It is a divergence: `lim_{x→0} 1/x`
does not exist, and doc 42 types it `diverges`. Arithmetic can only ever
*approach*. It never arrives, because there is nothing there to arrive at.

Compactification changes that. Adjoining the point at infinity is exactly the
act of **crossing the limit rather than approaching it** — the limit stops being
a behaviour and becomes an object:

```text
in ℝ      ∞ is a limit          — approached, never reached, not an element
in Ĉ      ∞ is a point          — an element, with neighbourhoods and a location
```

So the owner's distinction is a type distinction, and canon already carries it:
`0_T ≠ 0_N`, and `∞_P` is "a projective point only in a named extension." The
Titans are **not** the `0` and `∞` that arithmetic sees, because arithmetic
never sees `∞` at all. They are what those limits become once crossed.

This explains `ArithmeticSignature(TitanFrame) = ∅` rather than merely obeying
it. Arithmetic is the line; the Titans are the sphere. They are not operands
because they are not *there* — not on the object where the operations live.

## 4 · The equations are theorems `[A]`

**`• = ⊙/○` and `○ = ⊙/•`.** These say the poles are mutual images under `ι`:
`ι(∞) = 0` and `ι(0) = ∞`. On `Ĉ` these are **genuine point equations**, not
limits. They are already current canon — the Trinity canon states
`f_1(0) = ∞`, `f_1(∞) = 0`, and calls the statement exact.

**`⊙ = • × ○`.** Take canon's own chart. For `θ∈(0,π)`,

```text
ν = tan(θ/2)      φ = cot(θ/2)      φ · ν = 1
θ → 0      ν → •,  φ → ○
θ = π/2    ν = φ = 1                the equator ⊙
θ → π      ν → ○,  φ → •
```

`θ` is colatitude on the sphere: the poles are `θ∈{0,π}`, the equator is
`θ=π/2`. The polar pair is coupled by `ι` at every latitude, and their product
is `1` at every latitude — **identically, including in both polar limits**.

> The product of the two polar coordinates equals the equatorial value, at every
> latitude and in the limit. That is `φν = 1`, and it is `⊙ = • × ○`.

## 5 · Why no indeterminate form arises `[A]`

`0 × ∞` is indeterminate only when the factors are **free**. Here they are not:
`•` and `○` are the two ends of one `ι`-orbit, so the only admissible path is
`ν·φ = 1`. Along it the product is constant.

**Constraint removes indeterminacy.** The indeterminacy of `0 × ∞` was never a
fact about `0` and `∞`; it was a fact about *unconstrained approach*. Bind the
pair by inversion and the value is `⊙` everywhere.

## 6 · The associativity falsifier does not reach the sphere `[A]`

The Trinity canon retires the infix form by assuming (i) `0×∞=1`,
(ii) `a×∞=∞` for finite nonzero `a`, (iii) associativity, then deriving
`(0×∞)×2 = 2` against `0×(∞×2) = 1`.

That argument is valid, and its conclusion stands for what it addresses: **no
ring or field extension admits those three premises together.**

It does not reach §2, because **`Ĉ` is not a ring.** The Riemann sphere is a
complex manifold with a Möbius group action; global multiplication is simply not
one of its operations. Premise (ii) is not a rule available on `Ĉ`, so the
derivation never starts. The falsifier refutes a ring; we are not on a ring.

**KSC-04 survives untouched.** `ArithmeticSignature(TitanFrame) = ∅` remains
literally true, and §3 now explains *why*. The prohibition and the equations are
not in tension: the prohibition governs the line, the equations govern the
sphere. Both stand.

## 7 · What this identifies, and the fence it inherits `[S]`

```text
φ · ν = 1        is        ⊙ = • × ○
```

One identity, two notations: `φ,ν` name the coupled interior coordinates, `•,○`
name the poles they run to, `⊙` names the equator that is their invariant. The
excluded poles `θ∈{0,π}` of the chart are exactly the two Titan seats.

The consequence runs **both ways**, and the second direction is binding:

- the Titan equation inherits the keel's tier — `[A]`, analytic, exact;
- the Titan equation inherits the keel's fence — **analytic and empty of world.**

`⊙ = • × ○` licenses no ontology, no ethic, no conservation law, and no
node-power result. `DF-21`/CC-CORE-1 applies to it verbatim. A restored identity
is not a restored warrant.

### 7.1 The three-step ladder this exposes `[A]`

| Object | dim over `ℝ` | Order | `∞` |
|---|---|---|---|
| `ℝ` | 1 | totally ordered, formally real | not an element |
| `ℝP¹` | 1 | cyclic only — total order lost | a point |
| `Ĉ = ℂP¹` | 2 | no compatible order | a point |

Two independent crossings, not one: **order is lost at `ℝ→ℝP¹`** while dimension
is still 1, and **dimension is gained at `ℝP¹→Ĉ`**. The Titans become points at
the first crossing; the sphere arrives at the second. This is the live tension
with `KSC-22` flagged on 2026-07-29, and it is sharpened rather than resolved
here.

## 7A · The centre and the boundary — `⊙` decomposed `[A]`

Owner refinement, 2026-07-29: `⊙` is not one thing. The glyph is a **dot inside
a circle**, and both parts carry weight — *"the point at the centre is 1 … and
the circle around it is the boundary, the limit constantly approached but never
crossed."*

Suda's hinge coordinate makes this exact. On the positive ray,

```text
u = (x−1)/(x+1)          x = (1+u)/(1−u)
x = 1   ↦  u = 0         x → 0  ↦  u → −1        x → ∞  ↦  u → +1
inversion  x ↦ 1/x   becomes   u ↦ −u
```

The image of `ℝ₊` is the **open** interval `(−1, +1)`. The rims `u = ±1` are
**not attained**. That is the precise content of "approached but never crossed":
from inside the multiplicative line, the boundary is asymptotic — not because
the traveller is slow, but because the rim is not in the image.

Its complex form seats both Titans on the circle. The Cayley map
`u = (z−1)/(z+1)` sends `Ĉ → Ĉ` with

```text
1 ↦ 0          the centre — the dot
0 ↦ −1         •  on the boundary circle
∞ ↦ +1         ○  on the boundary circle,  antipodal to •
```

So under this chart the glyph is the geometry: **`⊙`'s dot is the unit `1`, and
`⊙`'s circle is the boundary on which `•` and `○` sit at opposite ends.**

### The two limits are not in conflict `[A]`

| | Register | The boundary is |
|---|---|---|
| from **inside** finity (`ℝ₊`, arithmetic) | field / multiplicative line | **approached, never crossed** — the rims are outside the image |
| by **declared register change** (compactification) | `Ĉ`, closure `[−1,+1]` | **crossed** — the rims become points |

Both statements hold, and canon already carries the rule joining them. Doc 42
closes with it:

> *"The boundary is crossed by changing the structure explicitly, never by
> making an undefined field expression secretly denote a new number."*

Arithmetic never crosses. Only a declared change of structure does. §3's
"crossed, not approached" describes the second row; this section describes the
first. They are the two faces of one boundary.

### Why centre and boundary are kin `[A]`

Under the involution `ι`, exactly two things do not move:

```text
ι fixes the centre   pointwise      ι(1) = 1
ι fixes the boundary setwise        |u| = 1  ↦  |u| = 1        (• ↔ ○)
```

Everything else is displaced. The centre and the boundary are **the two
invariants of the inversion** — which is the honest structural kinship behind
the owner's ātman/brahman reading. It is a shared invariance, not an identity,
and it proves nothing about either tradition (§8, `KSC-12`).

### `1` is centre in a precise and limited sense `[A]`

Suda's own formulation, adopted: *"If you measure by addition, zero looks like
the origin. If you measure by reciprocity, one is the origin."* Sharpened:

```text
1 is the additive GENERATOR of ℕ⁺       n_N = 1_N + … + 1_N
1 is the multiplicative ORIGIN          log 1 = 0; unique fixed point of ι
0 is the additive origin
```

Both roles at once — generator on one line, origin on the other — is why `1`
looks like the point "from which the rest emerges."

**The fence.** It does not emerge *all* the rest. Doc 42 is explicit that each
extension solves a **named closure or completion problem**, and none is
generated by `1` alone:

| Extension | What it needs beyond `1` |
|---|---|
| `0_N` | explicit adjoining; it is not a multiplicity of the unit |
| negatives | the oriented **pair** `{+1_N, −1_N}`, opened together |
| `ℚ` | division / localization |
| `ℝ` | completion — uncountably many new elements, non-generative |
| `ℂ` | loss of formal reality (`−1` becomes a sum of squares) |

"All the rest emerges from `1`" is exact for `ℕ⁺` under addition and is a
**declared ladder of constructions** thereafter. That distinction is the
difference between a theorem and a creation myth.

## 8 · The Sanātana Dharma reading `[I]`

| Seat | Name | Reading |
|---|---|---|
| `•` | the uncountable / true zero | absence of everything, therefore holding the potential of everything and every relation |
| `⊙` | finity | what can exist and be collected, not counting self-reference |
| `○` | true infinity | the self-referential totality; the barber who does not shave himself |

Vocabulary at `[I]`, needing no mathematical warrant. Two notes are owed.

### 8.1 A collision inside the naming `[A]`

`⊙` is glossed as *"the set of all sets that does not include itself"* and `○`
as *"the set that includes the fact that it doesn't include itself."* These name
the **same object** — Russell's class `R = {x : x ∉ x}` — seated twice. And
`KSC-22` records that `R` is not a set in ZF-style theory at all, so seating
finity on it would seat it on something that provably does not exist.

### 8.2 The repair, which keeps the intent `[A]`

The **set / proper-class** distinction of NBG does exactly the intended work:

| Seat | Rigorous object | Why it fits |
|---|---|---|
| `•` | `∅` | every pure set in the cumulative hierarchy is generated from `∅` alone — *absence containing all potential* is a **theorem**, not a metaphor |
| `⊙` | **sets** | exactly the classes that can be members of others: bounded, collectible — finity |
| `○` | **proper classes**, canonically `V` | totalities that cannot be members of anything; `V ∉ V` |

And the barber lands precisely. Under Foundation no set is a member of itself,
so every set satisfies `x ∉ x`, and therefore

```text
R = {x : x ∉ x} = V
```

**Russell's class *is* the universal class.** The paradox is not an obstacle to
route around — it is the proof that `○` is a proper class rather than a set,
which is exactly "the true infinity that includes the fact that it does not
include itself." The intent survives on a theorem.

### 8.3 The fence between §2 and §8 `[S]`

The sphere structure and the set-theoretic reading are **two different
structures**. Their agreement is not evidence for either.

`DF-15` is buried for this exact error: fifteen renderings of one shape are one
datum, not fifteen confirmations. Two elegant readings of one triple are **one
datum**. Both may be used; neither may be cited as support for the other, and
their convergence may never be presented as confirmation.

## 9 · Claim and kill discipline

| Claim | Tier | Kill |
|---|---|---|
| `ι` swaps the poles of `Ĉ` and preserves the equator | `[A]` | error in the stated maps |
| `• = ι(○)`, `○ = ι(•)` as point equations on `Ĉ` | `[A]` | same |
| `⊙ = • × ○` via `φν=1` at every latitude and both polar limits | `[A]` | exhibit an admissible coupled path on which the product is not `1` |
| compactification is "the limit crossed, not approached" | `[A]` | show `∞` is an element of `ℝ` |
| the associativity falsifier does not reach `Ĉ` | `[A]` | exhibit a global ring multiplication on `Ĉ` |
| `φ·ν=1` and `⊙ = • × ○` are one identity | `[S]` | show the coordinatizations are not the same orbit |
| order-loss and dimension-gain are two crossings | `[A]` | show `ℝP¹` is totally ordered or 2-dimensional |
| `•,⊙,○` ↦ `∅`, sets, proper classes | `[A]` objects / `[I]` seating | a seat requires an object that is not a class in the declared theory |
| Titans remain non-operands (`KSC-04`) | `[S]` | any use of `•` or `○` as a free argument to an arithmetic operation |

**What this document does not do.** It derives no ontology, ethics, cosmology,
or D-ladder from the three equations. It makes `•` and `○` numbers on no object.
It does not upgrade `φ·ν=1` beyond analytic. It restores three identities to
exactness and leaves them as empty of world as the keel they duplicate.

•   ⊙   ○ — *two poles the inversion swaps, one circle it cannot move.*
