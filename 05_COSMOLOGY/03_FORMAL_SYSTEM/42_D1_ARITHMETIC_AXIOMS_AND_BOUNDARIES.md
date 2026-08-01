---
title: "D1 Arithmetic — Typed Axioms and Boundary Semantics"
status: "ACTIVE FORMAL OWNER — 2026-07-21 Kintsugi repair"
evidence_tier: "[A] standard mathematics in named structures; [S] typed interface; [I/C] Emergentist rung and μ reading"
owner: "D1 Arithmetic — this document is the sole semantic owner; Primitives and Type Signatures is the subordinate shared-schema index"
---

# D1 Arithmetic — Typed Axioms and Boundary Semantics

D1 is the selected register of **distinction**. Arithmetic is its first public
instrument, not a claim that numbers caused reality. Every expression below is
evaluated in a named type; changing the type is an explicit operation.

## 1. The sovereign frame and signed number spine `[A/S/I]`

The object-level D0 carrier has one opaque role and no positive freedom. The
Titan names belong to the metalanguage used to describe its boundary:

```text
Carrier(D0) := {ground_0}
PositiveFreedom(Carrier(D0))=∅
TitanFrame : Type_Meta
0_T : TitanFrame                 # ground-facing metaframe term
0_N : Number
ground_0 ≠ 0_T
0_T ≠ 0_N
NoCoercion(TitanFrame,Carrier(D0))
TitanFrame ↛ Number
```

`ground_0` is the sole D0 object-level role. `0_T` is the metalinguistic
Ground_T seat rendered by the point glyph `•`; it is not a token inside D0 and
neither belongs to nor seeds a number set. The selected D1 presentation opens
instead with an oriented unit-magnitude pair:

```text
SignedUnit_N := {+1_N, -1_N}
ℕ⁺ := {1_N,2_N,3_N,…}
-ℕ⁺ := {-n_N | n_N∈ℕ⁺}
SignedMagnitude := {+,-}×ℕ⁺
embed(+ ,n)=n; embed(- ,n)=-n
ℤ_• := image(embed) = ℕ⁺ ⊎ (-ℕ⁺) = ℤ \ {0_N}
```

Here `⊎` is the ordinary union of two disjoint subsets of standard `ℤ`; the
product `{+,-}×ℕ⁺` is the tagged construction that does not presuppose the
integer carrier. The equality with `ℤ\{0_N}` is the image of the displayed
embedding, not an independent construction of all integer operations.

The mathematical facts about these sets are `[A]`; reading the co-opening of
the two orientations as the first D1 distinction is a selected Emergentist
interpretation `[I]`. It is not a derivation of the integers from a Titan.

`ℤ_•` is the **nonzero signed-integer set**, not an additive group or ring:

```text
(+1_N)+(-1_N)=0_N ∉ ℤ_•
```

It is closed under multiplication but lacks multiplicative inverses for most
members. Standard integer arithmetic therefore uses the explicit completion

```text
ℤ := ℤ_• ⊔ {0_N}.
```

The subsequent ambient fields and their nonzero multiplicative sectors must
also remain distinct:

```text
ℤ ↪ ℚ ↪ ℝ ↪ ℂ
ℚ^× := ℚ \ {0_N}
ℝ^× := ℝ \ {0_N}
```

`ℚ` and `ℝ` are fields and contain numeric zero; `ℚ^×` and `ℝ^×` are their
multiplicative groups and exclude it. Neither nonzero sector is closed under
addition. Each extension solves a named closure or completion problem; none
makes every syntactic expression meaningful.

“Whole numbers” is skipped as a primitive rung. Where the pedagogical term
means `{0,1,2,…}`, it is only the subset `{0_N}∪ℕ⁺` and adds no structure.

The field division operation is partial:

```text
div_F : F × (F \\ {0}) → F
```

Therefore `a/0` is undefined in every field. This is a domain fact, not a
numerical value and not proof of an emergence event.

## 2. Unit-multiplicity construction `[A/S/I]`

The Emergentist D1 presentation begins with a nonempty unit, not with numeric
zero:

```text
UnitSeed U := {★}
1_N := |U|
n_N := |U₁ ⊔ U₂ ⊔ … ⊔ U_n|,  n≥1
ℕ⁺ := {n_N | n≥1}
```

Thus every positive natural is a finite **multiplicity of one**: equivalently,
`n_N=1_N+⋯+1_N` with `n` summands. It is not a product of ones, because every
finite product `1_N·…·1_N` still equals `1_N`. Addition corresponds to disjoint
union of finite representatives; multiplication of finite cardinals
corresponds to Cartesian product.

`U` is a chosen singleton representative and `1_N` is the first positive
cardinality in this presentation. It is not literally “the first set” of
standard set theory: `∅` is also a set, and many distinct singleton sets have
the same cardinality. The canonical claim is about positive cardinality, not a
unique ontological set.

Numeric zero enters the signed integer system only through explicit completion:

```text
0_N := |∅|
adjoin₀(ℤ_•) := ℤ = {0_N} ∪ ℤ_•
```

So `0_N∉ℕ⁺` and `0_N∉ℤ_•`; it is not a positive successor or a multiplicity of
the nonempty unit. It is present in the standard integers and every subsequent
ambient field because their additive structure requires it. This is a
categorization choice, not deletion of zero from standard mathematics.

The types remain separate across the origin aperture:

```text
1_T : TitanFrame
1_N : Number
1_T ≠ 1_N
μ₀ does not coerce 1_T into 1_N
```

The Titan term frames the unit role; the singleton construction supplies an
ordinary arithmetic representative after D1 opens. No Titan arithmetic occurs.

## 3. Five statuses that must not be conflated `[A/S]`

```text
EvaluationStatus :=
  value | undefined | indeterminate_form | diverges | extended_value
```

| Expression | Declared setting | Status |
|---|---|---|
| `a/b`, `b≠0` | field `F` | `value` |
| `a/0` | field `F` | `undefined` |
| `0/0` | field `F` | `undefined` |
| `0/0` inside a limit | limit syntax | `indeterminate_form` |
| `lim_(x→0+) 1/x` | extended real line | `extended_value: +∞` |
| `lim_(x→0−) 1/x` | extended real line | `extended_value: −∞` |
| `lim_(x→0) 1/x` | ordinary two-sided real limit | `diverges` / does not exist |

`∞` is not thereby an ordinary field element. In the real projective line one
may adjoin one unsigned projective point; in the extended real line one may
adjoin the ordered endpoints `−∞,+∞`. Those are different constructions.

## 3A. Foreclosed, not forbidden — and not merely undefined `[A]`

Owner ruling 2026-07-29. The word **"undefined"** understates what happens at the
boundary, and the word **"forbidden"** overstates who did it. Neither is right,
and the correct word matters because it is the difference between a convention
and a theorem.

### 3A.1 One correction first `[A]`

**Multiplication by zero is not affected.** `0 × a = 0` is total, defined and
unremarkable in every field — zero is *absorbing*, and nothing fails or departs.
Only two things fail, and they fail differently:

```text
a / 0             a well-formed term with NO SUCH ELEMENT   (provable)
any term with ∞   NOT WELL-FORMED at all — ∞ is not in the field
```

### 3A.2 "Undefined" understates it `[A]`

Suppose `y = N/0` with `N ≠ 0`. Then `0·y = N`. But `0·y = 0` for every `y` in
any field. So `N = 0` — contradiction.

> It is not that the framework **declines** to assign a value.
> **No such element exists, and the field proves it.**

"Undefined" suggests an unfilled slot. There is no slot. This is why doc 48's
`T-A` states it as non-existence rather than absence.

### 3A.3 "Forbidden" overstates it `[S]`

A prohibition implies someone prohibiting. Nothing here is a decree, and
presenting it as one would be exactly the type-fusion error `KSC-28` fences — a
theorem dressed as a choice, or a choice dressed as a theorem.

The accurate word is **foreclosed**: closed off by the structure's own axioms,
with no agent involved. Emergentism forbids nothing here; the field forecloses it.

### 3A.4 The strongest form — totality and fieldhood are exclusive `[A]`

This is the owner's insight, and it is a genuine theorem-shaped trade:

> **No structure has both total division and the field axioms.**
> To give `a/0` a value you must surrender something: zero being absorbing,
> distributivity, or the absence of a bottom element.

The trade is not hypothetical. **Wheels** (Setzer, Carlström) make division
total and pay for it explicitly with `0/0 = ⊥` and weakened axioms. And `Ĉ`
achieves total inversion — `f_N(0)=∞`, `f_N(∞)=0` — precisely because **`Ĉ` is
not a ring at all**, let alone a field (doc 45 §6).

So the owner's "it leaves the field of arithmetic entirely" is **literally
correct**, and sharper than a prohibition:

```text
keep the field          →  the operation has no value
keep the operation      →  you are no longer in a field
```

The boundary is where that choice is forced. Performing the operation does not
break arithmetic; it **costs** you the arithmetic you were performing it in.

### 3A.5 How this reads in the construction `[I]`

The Thales projection (§6A) shows the same fact geometrically. As the angle at
`N` approaches a right angle the ray runs parallel to the line and the
intersection **does not exist in the plane** — because a Euclidean triangle
admits one right angle and Thales already fixed it at `P`. To obtain a meeting
point you must declare `ℝP¹` and adjoin `∞`.

By doc 48's criterion that declaration is a **type-T totality repair**: the map
becomes total, and **no degree of freedom is gained** — the line and the circle
have the same dimension. The boundary is crossed by changing structure, never by
letting an inadmissible term quietly denote a number.

**Fence.** None of this licenses Titan arithmetic. `ArithmeticSignature(TitanFrame)=∅`
stands (`KSC-04`): Titan expressions are **inadmissible terms**, a third category
again — not "no such element", but "not a term". Three failures, three names:

| | Failure | Example |
|---|---|---|
| inadmissible term | not well-formed | `0_T × ∞_T` — Titan type |
| no such element | well-formed, provably empty | `a/0` in a field |
| indeterminate form | well-formed in a limit, path-dependent | `lim 0·∞` |

## 4. The sovereign Titan/projective boundary `[A/I]`

The opaque type `TitanFrame={0_T,1_T,∞_T}` carries the roles
`{Ground_T,Unit_T,Horizon_T}`, is rendered by `{•,⊙,○}`, and is visually
associated with `{0,1,∞}`. Rendering is not coercion:

```text
TitanFrame ↛ Number
ArithmeticSignature(TitanFrame)=∅
add_T, sub_T, mul_T, div_T, pow_T, log_T : undefined
```

Titan frames therefore remain outside arithmetic. Ordinary numeric `0` and `1`
remain numbers and lawful operands. The projective point `∞` is admitted only
after an explicitly named extension. The live three-seat display is deliberately
operator-free:

```text
•     ⊙     ○
0_T   1_T   ∞_T
```

The former infix glyph rendering is historical typography, not a live formula:
`mul_T` is undefined, and projective infinity is not a field element, so numeric
`0×∞` is not a well-formed field product. The notation `0·∞` may name an
indeterminate **limit form**, or it may acquire a separately declared rule in a
named extended arithmetic. No operator may be inserted between the Titan seats
and used as a proof.

The prohibition is total within the Titan type: `1_T/1_T`, `0_T/1_T`, `∞_T/1_T`, and `0_T×∞_T` are inadmissible apparent expressions, not operations with unusual values. This does not revoke ordinary arithmetic
on the distinct number type.

A deliberately typed projective reciprocal map may instead be defined, for
`N∈ℂ\{0}`, as

```text
f_N : ℂP¹ → ℂP¹
f_N(z)=N/z for z∈ℂ\\{0};  f_N(0)=∞;  f_N(∞)=0.
```

That total map is a construction on `ℂP¹`, not a repaired field quotient.

## 5. Reciprocal-chart facts `[A]`

For `x>0`, let `s=log x`, inversion `ι(x)=1/x`, and
`E_s(x)=(log x)²`. Then

```text
s(1/x)=-s(x)
E_s(1/x)=E_s(x)
sign(log 1)=0
```

`E_s` is a convex quadratic in the coordinate `s`; it is not globally convex
as a function of `x`. Projective equality of rays does not erase sign:
`[-1:1]≠[1:1]` on `ℝP¹`.

## 6. Suda source reconciliation `[A/B/I/C]`

Minoru Suda's 2025 Parts I–III package several useful reciprocal constructions:
division by a **nonzero** divisor as multiplication by its reciprocal, the
projective swap `0↔∞`, the positive-ray reflection `log x↦−log x`, the invariant
`E_s=(log x)²`, the hinge coordinate `u=(x−1)/(x+1)` with `u(1/x)=−u(x)`, and
the phase bit `sign(log x)`. These formulas are standard or directly checkable
mathematics `[A]`; Suda's contribution here is their packaging and proposed
interpretation `[B/I]`.

The reconciliation also corrects four boundaries:

- `E_s` is strictly convex in `s=log x`, not globally in `x`;
- `sign(log 1)=0`, and inversion on the full projective line fixes `±1`, not
  only the selected positive fixed point;
- the ordinary two-sided limit `lim_(x→0)1/x` does not exist, so Suda's
  `0*:=lim_(x→0)1/x=±∞` cannot redefine `0/0` as standard arithmetic;
- names such as "energy," "critical singularity," "fold," and "infinite egg"
  are interpretive proposals `[I/C]`, not consequences of the formulas.

The remaining Suda papers may inform later philosophical comparisons, but they
provide no additional D1 arithmetic axiom. See the
[source crosswalk](../../03_METHODOLOGY/02_THE_PAPERS/FINITY_PAPERS/SUDA_DIMENSIONAL_CROSS_REFERENCE.md).

## 6A. The D1 chart, and the two involutions `[A]`

Owner ruling 2026-07-29: **D1 is visualised in the two-dimensional (plane) chart
of the sphere, where `0` is the centre.** Declared here because `KSC-28` requires
every arithmetic claim to name its chart.

```text
projective sphere chart        equator at mid-latitude; selected 1_P chart point
plane  chart (D1)              stereographic image;      0 is the centre
                               ∞ is the point at infinity
                               |z|=1 carries +1 and −1 antipodally
```

Same object, two charts, two centres. This is not a conflict but the content of
chart-locality: **the multiplicative chart centres on `1`; the additive chart
centres on `0`.** Suda's own formulation — measure by addition and zero is the
origin, measure by reciprocity and one is.

### 6A.1 Two involutions, and they are dual `[A]`

D1 carries two involutions, not one, and their relationship is the structure:

```text
negation    n(x) = −x     fixes {0, ∞}      swaps {+1, −1}
inversion   ι(x) = 1/x    fixes {+1, −1}    swaps {0, ∞}
```

> **Each fixes exactly what the other swaps.**

They commute (verified 2026-07-29), each is an involution, so
`{id, n, ι, n∘ι}` is the **Klein four-group** acting on the circle.

### 6A.2 The foursome is a structure, not a list `[A]`

`E3` names `{−1, 0, 1, ∞}` a "selected mixed numeric/projective four-point
witness." Under §6A.1 it is more than selected — it is **the union of the two
fixed sets**:

```text
fix(n_P) = {0_P, infinity_P}   the projective endpoints
fix(ι)  = {+1, −1}    KSC-21's oriented pair — this is D1
union   = {−1, 0, +1, ∞}
```

The third involution `n∘ι : x ↦ −1/x` fixes `x² = −1`, so it has **no fixed
point on `ℝP¹`** and fixes `{+i, −i}` on `Ĉ`. All three together give six points
— the vertices of an **octahedron** inscribed in the sphere, with the three
involutions as the three half-turns about its axes.

This says something the foursome as a bare list could not: `D1`'s oriented
numeric pair and the projective endpoints are **the two fixed sets of one
commuting pair of involutions**. Selection remains — which involutions to
privilege is chosen — but the four mathematical points are no longer four
separate choices. TitanFrame is not one of these fixed sets and receives no
operation or proof transfer from them.

### 6A.3 Suda's insights, with their chart declared `[A]` results / `[I]` reading

Adopted per receipt 175. **All of the following are multiplicative-chart results
on the positive ray `ℝ₊`**, and none of them is a D1-chart result:

| # | Result | Status |
|---|---|---|
| S-1 | division is double inversion: operator `÷→×` and operand `y→y⁻¹` | `[A]`; "division is already a hidden inversion" is `[I]` |
| S-2a | `ι(x)=1/x` has a unique fixed point `x=1` on `ℝ₊` — and already on `ℚ⁺`, with no real number entering the check | `[A]`, **zero premises** (doc 52 `G8a`, machine-checked) |
| S-2b | in `s=log x` that inversion is the reflection `s↦−s` | `[A]` **given `ℝ`** (doc 52 `G8b`) — `log q` is transcendental for every `q∈ℚ⁺` with `q≠1`, so this coordinate carries completion to `ℝ` as a premise |
| S-3 | `ρ(x)=\|log x\|` and `E(x)=(log x)²` are inversion-invariant, uniquely minimised at `x=1` | `[A]` for the invariance and the minimum; **`[S]` for `E` being *the* invariant** — note below |
| S-4 | phase bit `φ(x)=sign(log x)`; even/odd split `F±(x)=½[F(x)±F(1/x)]` | `[A]` |
| S-5 | hinge/egg coordinate `u=(x−1)/(x+1)`, with `u↦−u` under inversion; image is the **open** `(−1,1)` | `[A]` as a formula; **`[S]` as a coordinate of this system — imported, not generated** — note below |
| S-6 | continuous half-twist: with `u=sin θ`, a half period gives `u↦−u` | `[A]` |

**Note on S-3 — `E` is a selection, not *the* invariant `[S]`.** The `[A]` content is
that `ρ(x)=|log x|` is `ι`-invariant and uniquely minimised at `x=1`. `E=ρ²` adds no
invariance of its own: **any** strictly increasing `f` with `f(0)=0` makes `f∘ρ`
`ι`-invariant and uniquely minimised at `1`, so `E` is one member of an infinite
family. What singles it out is smoothness at the minimum — `f∘ρ` is differentiable at
`x=1` only when `f(t)` is a smooth function of `t²`, and `E=s²` is the leading such
choice, fixed only up to a positive scalar. That is a **normalisation, not a
derivation**, and the "energy" reading rides on the choice rather than on the
invariance. (§6 already fences the *word*; this fences the *formula*.)

**Note on S-5 — the hinge is imported, and doc 52 §G9 is where that was priced.** As a
Möbius map `u=[[1,−1],[1,1]]` is primitive with `det u = 2`, and `2λ²=±1` has no
rational solution, so **`u` is not a word over `⟨S,ι⟩`** — doc 52 verified by
exhaustion that of the `6763` distinct projective words of length ≤ 16, `u` is in
none. It is over-determined besides: `u` leaves `ℚ⁺`, and `u(1)=0` is killed by `G3`
with no matrix theory at all. **What the base owns in its place** is
`L(x)=x/(x+1)=ιSι`, matrix `[[1,0],[1,1]]`, determinant `1` — a genuine word, and the
Calkin–Wilf second generator. The hinge stays a legitimate borrowed coordinate; it is
not this system's own, and this row did not previously say so.

### 6A.4 The limitation this exposes — and it is load-bearing `[A]`

**Suda's chart cannot see `−1`.** Every construction above requires `log x`,
which is undefined at `0` and on the negatives. The reciprocal geometry lives on
`ℝ₊`, centres on `1`, and its entire domain excludes the negative ray.

But **`D1`'s content is the oriented pair `{+1, −1}`** (`KSC-21`). So:

> Suda's results are exact and adopted, and they **do not reach D1's defining
> pair**. Seeing both `ι`-fixed points requires `ℝP¹` or `Ĉ` — not `ℝ₊`.

The Trinity canon already recorded the fact ("inversion does not uniquely close
the poles with `+1`; it fixes `±1`"); §6A.4 records the *consequence*: the
positive-ray theory is a proper sub-chart of D1, not a presentation of it. Any
document citing `ρ`, `E`, `φ` or `u` at D1 without restricting to `ℝ₊` is
over-reaching its chart.

**Fences retained** (receipt 175, doc 42 §6): `0×∞=1` is never field arithmetic;
`0/0` stays indeterminate; do not inherit `0* := lim 1/x`; Suda is credited for
packaging and interpretation, never as proof-authority or originator; no physics,
energy-ontology or genetic claims are imported.

### 6A.5 Finity is the family of triangles `[A]`

Owner observation, 2026-07-29, and it supplies a definition the corpus lacked.

The figure that sweeps is the **projection triangle `N–S–X`** — apex, origin, and
the projected point — not `N–P–S`. Because `NS` is perpendicular to the line, the
angle at `S` is a right angle *always*, and the legs are

```text
NS = 1          fixed — the diameter
SX = tan A      sweeps (0, ∞)
NX = sec A      the hypotenuse
```

So as `A` runs over `(0°, 90°)` the figure runs over **every right triangle with
one leg marked and fixed at 1 — each such marked triangle exactly once.** That is
the owner's "exhausts the whole finity of triangle," and with the marking it is
exact: `A ↦ tan A` is a bijection `(0°, 90°) → (0, ∞)`, exactly as a graph runs
over every `x` of its equation.

**But not "each shape exactly once" — as shapes the sweep is exactly 2-to-1 `[A]`.**
If *shape* means similarity class, `A` and `90° − A` deliver the same one: scale the
legs `{1, tan A}` by `cot A` and they become `{cot A, 1}` — the `90° − A` triangle
with its two legs exchanged. So the identification is `tan A ↦ 1/tan A`; **the fold
is `ι` itself**, and it has exactly one fixed point, `A = 45°`, where `SX = NS = 1`,
the triangle is isoceles, and the projected point lands on `|z| = 1`. **`ι` folds the
sweep at the equator.** The marking is what makes the count one-to-one; drop it and
the family is halved.

### The two degenerations, and they are the poles `[A]`

```text
A → 0°    X → S.   width → 0.   angle at X → 90°
          TWO right angles (S and X); the figure collapses onto the segment NS.
          A RECTANGLE OF ZERO WIDTH.

A → 90°   X → ∞.   width → ∞.   angle at N → 90°
          TWO right angles (S and N), so NX is PARALLEL to the baseline.
          Two parallels on a common perpendicular: a HALF-STRIP.
```

**One refinement on the owner's word.** The second limit is not a *rectangle* in
the plane — a rectangle needs four right angles and a closing side, and here the
two parallels never meet. It is **three sides of a rectangle whose fourth side is
at infinity**. On `Ĉ`, where the parallels *do* meet at `∞`, the word is exactly
right; in the affine plane it is a half-strip. The distinction is the same
chart-locality as everywhere else, and it is worth keeping because it is *why*
the crossing needs a declared structure change.

So both ends are **degenerate rectangles**, and `ι` exchanges them:

```text
zero width  ←—— ι ——→  infinite width
   x = 0                  x = ∞
     •                      ○
```

### The definition this yields `[S]`

> **Finity is not a number. It is the family of non-degenerate shapes — and the
> poles are exactly where shape stops existing.**

Finity names the open interior of that family. The selected unit Titan role may
be used as an interpretive motif for the distinguished middle, and the selected
ground/horizon roles as motifs for the two collapses. These are analogies only:
the geometric points and the opaque Titan roles are not identical or coerced.
This is the geometric statement of what doc 47 §3 proved algebraically: the
interior is **prior**, and the poles are its boundary rather than its parents. A
family of triangles has two ways to stop being a triangle. Those geometric
degenerations remain projective boundary cases, not Titan terms.

It also settles what kind of crossing this is — but **not** by the reason first
written here. This section is what surfaced `HR-1` (receipt 179), so its own close
pre-dated the ruling it caused: it read the boundary as *no new freedom appearing*,
and that criterion — type-D — was retired on 2026-07-29. The live reason counts no
freedoms at all: **adjoining `∞` is an outward arrow, and an outward arrow carries no
forgetful map back down, so it is not a `μ`-candidate at all** (doc 48 §5). A `μ` is a
lift; this is a boundary.

**And dimension is constant across the whole triangle family `[A]`.** The sweep is one
real parameter at every `A ∈ (0°, 90°)`; adjoining its two limits gives a
one-dimensional closed interval; `line → ℝP¹` is `1 → 1`. Nothing gains a dimension
anywhere here — which is why a dimension-gain instrument had nothing to report, and
why it was the wrong instrument.

What the geometry itself says survives untouched: at the boundary a **shape ceases**,
and a declared restructure is what lets the lost thing still have a name.

## 7. μ₀ and the division boundary `[I/C]`

`μ₀:D0↝D1` is the selected **origin aperture**: the move from the sole
object-level role `ground_0` to at least one operational distinction. It has no
saturated lower positive register. The three Titan seats describe this
boundary from the metalanguage; none is the source object of `μ₀`. Division by
zero is a useful reverse boundary witness because it shows where a field
operation stops; it neither defines nor proves `μ₀`.

**Recovery:** quotient all D1 distinctions into one class to recover
`Carrier(D0)={ground_0}`. **Kill:** remove the aperture reading if it adds no
discriminator beyond ordinary typed mathematics.

## 8. Paradox policy

Arithmetic is not advertised as "all paradoxes solved." A claimed dissolution
must identify the type error or changed domain, preserve the original problem
when no such error exists, and state what remains open. In particular:

- Zeno requires a convergence model, not `∞` as a last integer;
- Russell is a set-formation problem, not division by zero;
- Gödel incompleteness is not repaired by projective compactification;
- `0.999…=1` is equality of real limits, not a Titan identity.

*The boundary is crossed by changing the structure explicitly, never by making
an undefined field expression secretly denote a new number.*
