---
rosetta:
  primary_level: L5
  primary_column: Philosophy
  operator: "Brahmā ○"
  tier: "Executive"
  regime: "Brāhmaṇa"
  register: "[A] the named projective, Cayley, and class-theory facts; [S] their type separations; [I] every Titan, glyph, and Sanātana reading"
title: "The Titan Inversion Structure — exact orbit facts after retiring seat arithmetic"
status: "ACTIVE — corrected after cross-owner audit; the old infix equations remain retired"
date: 2026-07-29
owner: "Formal owner for the Titan inversion facts; subordinate to K-1 for chart facts"
evidence_tier: "[A] the named orbit, chart, topology, and class-theory facts; [S] their separation; [I] every selected representation"
parents:
  - 00_THE_TRANSCENDENTAL_TRINITY_CANON.md
  - ../00_CANONICAL_FORMULA_BLOCK.md
  - ../03_FORMAL_SYSTEM/42_D1_ARITHMETIC_AXIOMS_AND_BOUNDARIES.md
  - ../../00_META/00_SETTLED_CANON_REGISTRY.md
---

# The Titan Inversion Structure

> The old three infix equations were **ill-typed**. Changing from the line to the
> sphere does not repair an operation the sphere does not possess. What survives
> is exact but narrower: two inversion-orbit facts on `Ĉ`, plus one reciprocal
> coordinate identity on the punctured affine chart.

## 1 · The three typed survivors

```text
ι(0) = ∞_P
ι(∞_P) = 0
φ(θ) · ν(θ) = 1       for θ∈(0,π), with φ=cot(θ/2), ν=tan(θ/2)
```

The first two are point equations for the named involution. The third is an
identity between finite, nonzero chart coordinates. None multiplies or divides
Titan seats. The former glyph equations remain visible in history, not live here.

## 2 · A selected representation on the Riemann sphere `[A/I]`

The exact object in this section is the Riemann sphere. The Titan seats remain
opaque labels. They enter the picture only through a declared interpretive map;
changing the object does not silently coerce a seat into a point or set.

```text
Ĉ := ℂP¹ = ℂ ∪ {∞_P}          the Riemann sphere
ι(z) := 1/z                    inversion, extended by ι(0)=∞_P, ι(∞_P)=0
```

Let `Feature(Ĉ) := Point(Ĉ) ⊎ Subset(Ĉ)` be a tagged feature type, let
`E:={z∈Ĉ:|z|=1}`, and select the representation `[I]`

```text
r_T : TitanFrame → Feature(Ĉ)
r_T(•)=Point(0)       r_T(⊙)=Subset(E)       r_T(○)=Point(∞_P)

ι_* : Feature(Ĉ) → Feature(Ĉ)
ι_*(Point(p))  := Point(ι(p))
ι_*(Subset(A)) := Subset(ι[A])
```

Under that selected representation:

| Seat | Location on `Ĉ` | Character |
|---|---|---|
| `•` | south pole, `z = 0` | a **point** of `Ĉ` |
| `○` | north pole, `z = ∞` | a **point** of `Ĉ` |
| `⊙` | the equator, `\|z\| = 1` | the circle equidistant from both poles |

`ι` is an involution on `Ĉ`. It **swaps the poles** and maps the equator to
itself: `|z|=1 ⟹ |ι(z)|=1`. The induced map `ι_*` therefore swaps `r_T(•)`
with `r_T(○)` and preserves `r_T(⊙)` setwise. The projective orbit facts are
exact independently of `r_T`; only their association with Titan seats is
conditional on the selected representation. No operation acts on `TitanFrame`
itself, and many other representations are possible.

The glyph shapes are mnemonic only. In particular, the drawn outline of `○` is
not its image under `r_T`, which is the tagged point `Point(∞_P)`.

## 3 · Compactification and the "crossed limit" reading `[A/I]`

On the real line, `∞_P` is **not an element**. The ordinary two-sided real limit
`lim_{x→0}1/x` does not exist: its one-sided extended-real behaviours have
opposite signs. This is divergence in the original real codomain, not a real
number waiting at the endpoint.

A named compactification changes the codomain and its topology. The real
projective line `ℝP¹=ℝ∪{∞_P}` compactifies the real line, while
`Ĉ=ℂP¹=ℂ∪{∞_P}` compactifies the complex plane and contains `ℝP¹` as its real
meridian. In either projective topology, inversion extends continuously through
`0` and `lim_{x→0}ι(x)=∞_P`. Thus `∞_P` is not a value of the original undefined
field expression, but it is both a point and the value and limit of the
explicitly extended map. Calling this **crossing the limit rather than
approaching it** is the corpus's `[I]` reading of those `[A]` constructions:

```text
in ℝ       lim_(x→0) 1/x fails      — ∞_P is not an element
in ℝP¹     lim_(x→0) ι(x)=∞_P       — ∞_P is a projective point
in Ĉ       lim_(z→0) ι(z)=∞_P       — the same extension on the complex sphere
```

Canon already carries the relevant type distinction: `0_T ≠ 0_N`, while
`∞_P` is a projective point only in a named extension. The map `r_T` relates a
Titan label to a geometric feature for interpretation; it does not identify the
label with that feature. `ArithmeticSignature(TitanFrame)=∅` is a constitutive
typing rule, not something proved by a picture. Ordinary arithmetic remains
lawful on its ordinary domains, and chart-local complex arithmetic remains
lawful on the affine chart.

## 4 · The typed survivors are theorems `[A]`

**The orbit equations.** The poles are mutual images under `ι`:
`ι(∞_P)=0` and `ι(0)=∞_P`. On `Ĉ` these are point equations of the extended
map; they also agree with its projective limit statements. They are not
endpoint multiplication. They are already current canon — the Trinity canon states
`f_1(0) = ∞`, `f_1(∞) = 0`, and calls the statement exact. Division glyphs are
not aliases for these equations.

**The reciprocal-coordinate identity.** Take canon's own chart. For
`θ∈(0,π)`,

```text
ν = tan(θ/2)      φ = cot(θ/2)      φ · ν = 1
θ → 0      ν → 0,    φ → ∞_P
θ = π/2    ν = φ = 1                the equator ⊙
θ → π      ν → ∞_P,  φ → 0
```

`θ` is colatitude on the sphere: the poles are excluded endpoints
`θ∈{0,π}`, and the equator is `θ=π/2`. The two finite coordinates are coupled
by inversion at every interior latitude, and their product is identically `1`.
Along the specified reciprocal path its limit is also `1`; there is no product
of the endpoint values themselves.

> `φ(θ)ν(θ)=1` is an interior coordinate identity. At `θ=π/2`, both coordinates
> equal the distinguished scalar `1`. The entire equator is not that scalar, and
> the Titan seats are not operands.

## 5 · Why the named path has a determinate product limit `[A]`

The form `0 · ∞` is undefined as endpoint arithmetic. A constrained family of
finite pairs can nevertheless have a determinate product limit. Here the named
family satisfies `ν(θ)φ(θ)=1` before either endpoint is reached.

**Constraint determines this path; it does not define endpoint multiplication.**
Other coupled approaches can yield other finite limits, zero, or divergence.
The result belongs to the specified reciprocal path only.

## 6 · The associativity falsifier does not reach the sphere `[A]`

The Trinity canon retires the infix form by assuming (i) `0×∞=1`,
(ii) `a×∞=∞` for finite nonzero `a`, (iii) associativity, then deriving
`(0×∞)×2 = 2` against `0×(∞×2) = 1`.

That argument is valid, and its conclusion stands for what it addresses: **no
ring or field extension admits those three premises together.**

It does not reach §2, because the standard Riemann-sphere structure supplies no
total associative ring multiplication extending ordinary complex
multiplication and realizing all three premises. Standard extended
multiplication does use `a·∞_P=∞_P` for finite `a≠0` where it is defined, but
`0·∞_P` is undefined. Premise (i), and therefore the three-premise package, is
absent. Abstractly transporting an unrelated ring structure onto a set of the
same cardinality would not extend the standard chart operations and would prove
nothing about the Titan reading.

**KSC-04 governs.** `ArithmeticSignature(TitanFrame) = ∅` remains literally
true. The sphere supplies an involution and chart-local coordinates, not a
second arithmetic in which the retired expressions become legal.

## 7 · What this identifies, and the fence it inherits `[S]`

```text
φ(θ) · ν(θ) = 1       exact on the interior reciprocal chart
Titan triple            selected interpretation of its orbit geometry
```

These are related but not identical statements. `φ,ν` name coupled interior
coordinates; `•,○` name the limiting pole seats; `⊙` names the selected
equatorial emblem. The excluded poles `θ∈{0,π}` are not substituted into the
coordinate product.

The consequence runs **both ways**, and the second direction is binding:

- the coordinate identity is `[A]`, analytic and exact on its domain;
- the Titan seating is `[I]`, selected and empty of world.

Neither licenses ontology, ethics, a conservation law, or a node-power result.
`DF-21`/CC-CORE-1 applies verbatim. A typed analogy is not a transferred warrant.

### 7.1 The three-step ladder this exposes `[A]`

| Object | dim over `ℝ` | Order | `∞` |
|---|---|---|---|
| `ℝ` | 1 | totally ordered, formally real | not an element |
| `ℝP¹` | 1 | no global linear order that both extends the usual real order and retains the circle topology | a point |
| `Ĉ = ℂP¹` | 2 | no compatible ordered-field structure extending `ℝ` | a point |

Two independent crossings, not one: **compatibility of the usual linear order
with the circle topology is lost at `ℝ→ℝP¹`** while dimension is still 1, and
**dimension is gained at `ℝP¹→Ĉ`**. The two pole features become projective
points at the first crossing. The selected `r_T(⊙)=Subset(E)` is not a point and
belongs to the sphere representation at the second crossing. A different map
placing all three seats at `0,1,∞_P` on `ℝP¹` would be a second `[I]`
representation, not a consequence of `r_T`. This is the live tension with
`KSC-22` flagged on 2026-07-29, sharpened rather than resolved here.

The ordinary real line is not rejected: `ℝ∪{∞_P}` is an `ι`-invariant meridian of
`Ĉ`. Its order and field operations remain chart-local data; the meridian does
not make the whole sphere an ordered field.

## 7A · The centre and the boundary — `⊙` decomposed `[A/I]`

Owner reading `[I]`, 2026-07-29: `⊙` is not one thing. The glyph is a **dot inside
a circle**, and both parts carry weight — *"the point at the centre is 1 … and
the circle around it is the boundary, the limit constantly approached but never
crossed."*

The analytic part of Suda's hinge coordinate is exact. On the positive ray,

```text
u = (x−1)/(x+1)          x = (1+u)/(1−u)
x = 1   ↦  u = 0         x → 0  ↦  u → −1        x → ∞  ↦  u → +1
inversion  x ↦ 1/x   becomes   u ↦ −u
```

The image of the ordered multiplicative group `ℝ_{>0}` is the **open** interval
`(−1,+1)`. The values `u=±1` are ordinary real points, but neither is attained
by any `x>0`. That is the precise content of "approached but never crossed" in
this parameterization: the endpoints are absent from the image.

The radial picture has a complex extension, but it is a **second projective
coordinate**, not the equator `|z|=1` of §2. Define the Cayley automorphism

```text
C : Ĉ → Ĉ
C(z) := (z−1)/(z+1),   C(−1):=∞_P,   C(∞_P):=1
ι_C := C ∘ ι ∘ C⁻¹,    so ι_C(u)=−u
```

Then

```text
1 ↦ 0          the centre — the dot
0 ↦ −1         •  on the boundary circle
∞_P ↦ +1       ○  on the boundary circle |u|=1, antipodal to •
```

Thus the positive ray becomes the open diameter `(-1,1)`, with its two omitted
endpoints made visible. Reading the glyph's dot as the unit and its circle as a
container for this diameter is `[I]`; the interval endpoints are not the whole
circle, and this picture must not be identified with the original equator.

### The two limits are not in conflict `[A]`

| | Register | The boundary is |
|---|---|---|
| from **inside** finity (`ℝ_{>0}`) | ordered multiplicative group / open positive ray | **approached, never attained** — the endpoints are outside the image |
| by **declared domain closure** in `Ĉ` | closure `[−1,+1]` | **included** — `u=−1` corresponds to the existing affine point `x=0`; `u=+1` corresponds to `∞_P` |

Both statements hold, and canon already carries the rule joining them. Doc 42
closes with it:

> *"The boundary is crossed by changing the structure explicitly, never by
> making an undefined field expression secretly denote a new number."*

No undefined field expression has been repaired. Passing from the open domain
to its declared closure changes which boundary points belong to the model;
relative to the affine real line, only `∞_P` is newly adjoined. §3's "crossed,
not approached" is the `[I]` reading of this explicit structural change.

### Why centre and boundary are kin `[A/I]`

Under the involution in the selected real-diameter picture, two selected
features are invariant in different senses:

```text
ι fixes the unit in the z-coordinate       ι(1)=1
ι_C fixes the u-centre pointwise             ι_C(0)=0
ι_C fixes the endpoint pair setwise          {−1,+1}↦{−1,+1}   (• ↔ ○)
```

These are not the only invariant features: original inversion fixes numeric
`±1`, while the Cayley-conjugate map `ι_C:u↦−u` preserves every circle centred at
`0` setwise. The selected centre and endpoint pair nevertheless share an
invariance, which motivates the owner's ātman/brahman reading `[I]`. That is an
analogy, not an identity or evidence about either tradition (§8, `KSC-12`).

### `1` is centre in a precise and limited sense `[A/I]`

Suda's own formulation, adopted: *"If you measure by addition, zero looks like
the origin. If you measure by reciprocity, one is the origin."* Sharpened:

```text
1 is the additive GENERATOR of ℕ⁺       n_N = 1_N + … + 1_N
1 is the log-coordinate ORIGIN          log 1 = 0; positive fixed point of ι
0 is the additive origin
```

Both roles at once — generator on one line, origin on the other — motivate the
`[I]` picture of `1` as the point "from which the rest emerges."

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

### 8.1 A collision inside the naming `[A/I]`

`⊙` is glossed as *"the set of all sets that does not include itself"* and `○`
as *"the set that includes the fact that it doesn't include itself."* If both
phrases are formalized as Russell's condition `R={x:x∉x}`, the two seats collapse
onto the same class. `KSC-22` records the exact boundary: no such **set** exists
in ZF-style theory. The definable class does exist in a declared class theory.

### 8.2 A typed class-theory representation `[A/I]`

NBG and MK provide the standard set/proper-class distinction `[A]`. To avoid
mixing an object, a sort, and a metasort, define a tagged metalinguistic feature
type and a selected representation `[I]`:

```text
SetClassFeature := EmptySetObject | SetSort | ProperClassObject
s_T : TitanFrame → SetClassFeature
s_T(•) := EmptySetObject(∅)
s_T(⊙) := SetSort(Set)
s_T(○) := ProperClassObject(V)
```

`SetSort(Set)` is a metalinguistic tag, not a class whose members are all sets;
`ProperClassObject(V)` names the universal class specifically, not a collection
of proper classes.

| Seat | Rigorous object | Why it fits |
|---|---|---|
| `•` | the set object `∅` | the standard pure cumulative hierarchy starts at `∅`; *absence containing all potential* remains `[I]` |
| `⊙` | the metalinguistic sort **Set** | sets are exactly the classes eligible to be members in NBG/MK; they include both finite and infinite sets, so *collectible finity* remains `[I]` |
| `○` | the proper-class object `V` | `V` contains every set and, as a proper class, is not eligible to be a member |

And the barber lands precisely. Under Foundation no set is a member of itself,
so every set satisfies `x ∉ x`, and therefore

```text
R = {x : x ∉ x} = V
```

**Under Foundation, Russell's class is the universal class.** Russell's argument
shows that `R=V` is a proper class rather than a set. Selecting the tagged object
`ProperClassObject(V)` as the image of `○` is `[I]`; no theorem proves anything
about the Titan seat. The interpretation may align with the theorem, but it is
not itself a theorem.

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
| `ι(0)=∞_P`, `ι(∞_P)=0` as point equations on `Ĉ` | `[A]` | same |
| `φ(θ)ν(θ)=1` on the declared interior chart | `[A]` | arithmetic error in the stated functions |
| projective compactification adjoins `∞_P`; the extended map has a projective limit; "crossed limit" is the reading | `[A]` construction and limit / `[I]` reading | show the named extension, topology, or interpretation is misstated |
| the associativity falsifier does not reach the named sphere structure | `[A]` | exhibit a total associative ring multiplication extending `ℂ` and satisfying premises (i)–(iii) |
| the Titan triple is an interpretation of the inversion geometry | `[I]` | a clearer interpretation displaces it |
| loss of a compatible global linear order and dimension-gain are two crossings | `[A]` | exhibit the denied compatible order or show the dimension claim is wrong |
| `s_T` tags `•,⊙,○` as `∅`, the Set sort, and `V` | `[A]` class-theory facts / `[I]` selected metalinguistic representation | the tags collapse levels, a set is called finite merely because it is a set, or the mapping is used as proof |
| Titans remain non-operands (`KSC-04`) | `[S]` | any use of `•` or `○` as a free argument to an arithmetic operation |

**What this document does not do.** It derives no ontology, ethics, cosmology,
or D-ladder. It does not make `•` or `○` numbers or operands on any object. It
does not upgrade `φ·ν=1` beyond analytic, and it does not restore the retired
infix forms.

•   ⊙   ○ — *three opaque seats; one selected picture of a swapped pair and a preserved circle.*
