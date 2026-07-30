---
title: "Boundary Crossings and the Open μ Discriminator — proofs at the division boundary"
status: "ACTIVE — boundary typology retained; former type-D μ criterion withdrawn pending owner adjudication"
date: 2026-07-29
evidence_tier: "[A] §2 theorems and §4 typology; [S] §5 withdrawal/open protocol; [I] §3 template"
owner: "Boundary-crossing typology. Subordinate to 42_D1_ARITHMETIC_AXIOMS_AND_BOUNDARIES.md on all D1 claims."
parents:
  - 42_D1_ARITHMETIC_AXIOMS_AND_BOUNDARIES.md
  - 10_EFR_MU_LIMIT_FORMULA.md
  - ../01_THE_TRANSCENDENTAL_TRINITY/00_THE_TRANSCENDENTAL_TRINITY_CANON.md
  - ../01_THE_TRANSCENDENTAL_TRINITY/45_THE_TITAN_INVERSION_STRUCTURE.md
  - ../../00_THE_FOUNDATION.md
---

# The Boundary Crossings and the μ-criterion

> **Terminology hazard, first.** The phrase *"μ-limit"* carries a killed lemma:
> receipt 109 retracted a μ-limit formula that "conflated a pointwise coordinate
> identity with a normalization integral." This document says **boundary
> crossing** and reserves `μ` for what §5 licenses. Cite `10_EFR_MU_LIMIT_FORMULA.md`
> only for its own scoped content.

## 1 · The claim

Owner, 2026-07-29:

> *"Division by zero is undefined, but we can play the game of `lim x→0` so we
> never divide by zero — only by 0.1, 0.01, 0.001. We stay within finity and
> don't cross to divide by the infinite zero."*

This is exactly right, it is provable, and the proofs below establish something
the claim does not yet say: **what kind of crossing this is, and why this example
does not by itself establish a `μ`.**

## 2 · Five theorems at the division boundary `[A]`

**T-A · No zero-denominator quotient satisfies the field quotient law.**
In a field `F`, suppose `y` were a quotient of `N` by `0`, for `N ≠ 0`, in the
sense required by division: `0·y=N`. But `0·y=0` for every `y∈F`, contradiction.
The ordinary field-division operation is therefore partial:

```text
div : F × (F \ {0}) → F
```

An underlying field can be expanded with an arbitrary total binary symbol `/`
by stipulating a value at denominator zero. Such a branch cannot satisfy the
quotient law and is not field division. The theorem concerns the operation, not
the bare possibility of adding a total symbol to the signature.

**T-B · The limit game is legal at every step, and never reaches the boundary.**
For `x_n = 10^{-n}`, each `1/x_n = 10^n` is a finite field element obtained by a
defined reciprocal on its declared nonzero domain. The sequence is unbounded;
no term is `∞`; no step divides by zero. **The owner's formulation is exact:**
one stays inside finity throughout, and the boundary is never an operand.

**T-C · On the real affine line, the two-sided real limit fails.**
For `N > 0`: `lim_{x→0⁺} N/x = +∞` and `lim_{x→0⁻} N/x = −∞` in the two-point
extended reals. Left and right disagree, so `lim_{x→0} N/x` **does not exist** in
`ℝ`. This is a genuine defect of the line, not a notational inconvenience.

**T-D · On the sphere, the limit exists and the map becomes total.**
`ℂP¹` has a **single** point at infinity, unsigned. Hence `lim_{z→0} N/z = ∞`
irrespective of direction, and

```text
f_N : ℂP¹ → ℂP¹ ,   f_N(z)=N/z ,   f_N(0)=∞ ,   f_N(∞)=0
```

is a **total** meromorphic map. The missing endpoint of the reciprocal map is
repaired in this declared complex-projective extension. This is a concrete
payoff of choosing `ℂP¹`: the affine chart omits an endpoint that the projective
space supplies. It does not follow that every feature lost on the real line is
restored, or that `ℂP¹` is forced as the unique completion.

**T-E · But no degree of freedom is gained.**

```text
dim_ℂ(ℂ) = dim_ℂ(ℂP¹) = 1        dim_ℝ(ℂ) = dim_ℝ(ℂP¹) = 2
```

Compactification adds a **point**, not a **freedom**. The Trinity canon already
states this; T-E records it as the load-bearing fact it turns out to be.

## 3 · The template `[I]`

Canon calls the division example a "mathematical parable" of a boundary
interface. Made systematic, it has five stages, and the fifth is the one usually
skipped:

```text
1  APPROACH     the operation runs toward its domain boundary      N/z, z→0 in ℂ
2  STOP         field division is undefined there                  N/0  (T-A)
3  RESTRUCTURE  a different structure is explicitly declared      ℂ ⟶ ℂP¹
4  TOTALITY     the reciprocal map becomes total there             f_N(0)=∞ (T-D)
5  RECOVERY     restrict back to recover the old behaviour exactly ℂP¹ ⊃ ℂ\{0}
```

Stage 5 is what distinguishes a legitimate restructure from a redefinition. Any
crossing that cannot recover its lower description has not crossed a boundary —
it has replaced the subject.

## 4 · Three separable descriptors of the examples `[A/I]`

The examples show that boundary crossings differ in **what they change**, and
that totalization, order loss, and dimension gain need not coincide:

| Crossing | Totality repaired? | Order lost? | Freedom gained? |
|---|---|---|---|
| `ℝ → ℝP¹` | **yes** — `1/x` becomes total | **yes** — no global linear order both extends the affine order and is compatible with the circle topology | no — `dim_ℝ` stays 1 |
| `ℂ → ℂP¹` | **yes** — `f_N` becomes total | n/a — `ℂ` is unordered | no — `dim_ℝ` stays 2 |
| `ℝP¹ → Ĉ` | already total | already lost | **yes** — `dim_ℝ` 1 → 2 |

So there are three separable phenomena:

```text
type-T   TOTALITY    a partial operation becomes total
type-O   ORDER       an order structure is lost
type-D   DIMENSION   a degree of freedom is gained
```

`ℝ → ℝP¹` is simultaneously type-T and type-O while gaining no real dimension;
`ℝP¹ → Ĉ` is type-D in that dimension count. These witnesses establish
non-equivalence of the descriptors. Full logical independence would require
examples for all admissible combinations and is not claimed.

## 5 · No settled μ-criterion `[S]`

> **WITHDRAWN AS A SETTLED CRITERION; HR-1 REMAINS OPEN.** Two findings the same day: the
> reclassification workflow found §4's `dim_ℝ` witness and §5.2's "genuinely
> larger" witness **disagree over finite carriers**; and an owner observation
> showed §4's three rows are all **outward** arrows (compactification,
> complexification) while every `μ` is a **lift with a forgetful map** — a
> different arrow. Checked: `dim_ℝ` kills 4 of 5 μ's, the fibre test kills 0 of 5.
> **Neither discriminates.** In both actual failures (μ₂, μ₃) the load-bearing
> step was **reducibility**, which the GP-MU packets already publish as their kill.
> Receipt 179 recommends retiring type-D as the μ-criterion and testing
> reducibility, with §4 surviving intact as what it is — a correct taxonomy of
> **boundary** phenomena. **Do not propagate this section into the ~112 boilerplate
> copies until HR-1 is ruled.** The μ₂/μ₃ verdicts are unaffected either way.

`E1` defines the ladder in terms of freedoms, while `E5` calls `μ` an aperture
at which a new effective freedom becomes available. That language motivates a
candidate witness but does not yet supply a discriminator:

> A defensible `μ` claim must name the lower and higher types, the forgetful or
> recovery map, the alleged new effective freedom, and a reducibility test. No
> single scalar criterion is currently canonical.

Three consequences survive the withdrawal:

**5.1 The division boundary does not establish `μ₀`.** It is type-T in §4 and
adds no demonstrated effective freedom. This preserves the D1 owner's fence
without pretending that the open μ question has been solved by definition.

**5.2 `KSC-22` remains a selected scaffold boundary.** Adjoining `∞_P` repairs a
domain but does not by itself establish D2. A relational configuration space may
be a D2 neighbour; dimension gain alone does not prove emergence or irreducibility.

A precision that reconciles two earlier results: for a **continuous** map
`f:X→Y`, its graph `Γ_f={(x,f(x))}` with the subspace topology is homeomorphic
to `X`; for an arbitrary function, the projection is only a set-theoretic
bijection unless more regularity is supplied. In neither case does one graph by
itself prove strong emergence. The collection of all relations on a carrier `X`
is `𝒫(X×X)` and is strictly larger than `X×X` by Cantor's theorem. Calling a
particular structured configuration space the D2 neighbour remains `[S]`; its
topology and effective degrees of freedom must be declared rather than inferred
from the word *space*.

**5.3 The contract is the live test.** Any future `μ` claim must supply boundary,
saturation statistic, threshold, novelty test, recovery, gained-freedom witness,
reducibility analysis, prediction, and kill. Until a discriminator separates
known positive and negative cases, `μ_n` is an interface label plus an open
causal conjecture—not a result licensed by dimensional language.

## 5A · Test case — "a straight line is a circle of infinite diameter" `[A]`

Owner, 2026-07-29, offered as a proof of the μ-limit. It is a **real theorem**,
and the §4 typology describes it exactly. It neither proves sphere primacy nor
supplies a general μ discriminator.

### 5A.1 What is true, and it is more than the claim says

**The generalized-circle theorem.** Under stereographic projection, a circle on the sphere
maps to a **circle** in the plane if it misses the north pole, and to a
**straight line** if it passes through it. Verified 2026-07-29: the sphere-circle
cut by the plane `z = 1−y` (which contains `N`) projects to the exact line
`v = 1`.

So on `ℂP¹` there is no distinction to draw:

> **A line is a generalized circle (circline)—the member containing `∞`.**
> Möbius maps preserve the combined class of circles and lines.

**The curvature reading is also correct.** A circle of radius `R` has curvature
`κ = 1/R → 0`. A sector of huge radius is *locally* indistinguishable from a
segment. The owner's phrasing captures this exactly.

**And it subsumes a result already in canon.** Receipt 175 established that
`ℝ ∪ {∞}` is a great circle on `Ĉ`. That is the circline theorem's special
case — the meridian is simply the line-through-`∞` that is additionally
`ι`-invariant. The geometry and the algebra were describing the same object.

### 5A.2 One precision — "a circle of infinite diameter" is not a circle

In `ℝ²` there is **no** circle of infinite radius. Under a coefficient
normalization, some sequences of Euclidean circles with radius tending to
infinity converge to lines; adjoining `∞` represents those lines as circlines.
That closes this particular missing-line boundary. It does **not** make the
family of nondegenerate spherical circles closed under every natural topology:
circles can shrink to a point. A global closure theorem would have to declare
its parameter topology and include the relevant degenerate point-circles.

This is the session's recurring shape once more: the object fails on the line and
succeeds on the sphere.

### 5A.3 The typology classifies the construction; μ remains unpaid `[A/S]`

```text
circles in the plane         (cx, cy, r)             dim 3
lines in the plane           (angle, offset)         dim 2 missing-line stratum
nondegenerate circlines      sphere-plane sections   dim 3, with further
                                                       point degenerations possible
```

For the radius-to-infinity degeneration under discussion, compactification adds
the missing-line stratum without increasing the ambient three-parameter count.
This is a scoped closure statement, not a claim that every circline parameter
space is globally closed.

> **Therefore this is a type-T closure. Nothing here establishes a `μ`.**

It is analogous to `T-D`: adjoining `∞` totalizes the reciprocal map there and
incorporates the line stratum into the generalized-circle description here.
The analogy is `[I]`; the two constructions do not become one theorem.

**What it proves:** Möbius geometry treats Euclidean circles and lines as one
generalized-circle class after the point at infinity is included. Selecting that
geometry as primary remains a preference informed by this utility, not a theorem
of uniqueness.

**What it does not prove:** any emergence, any new freedom, or `μ₀`. Local
indistinguishability under `κ → 0` is an approximation statement; global
identity holds only after the point at infinity is adjoined — and that adjoining
is `S1`, a declared selection, not a discovery.

## 5B · The same one dimension up — plane and sphere `[A]`

Owner, same sitting: *"and the same with a flat plane and an infinity sphere."*

Correct, and it is the exact analogue:

```text
Gaussian curvature of a sphere of radius R :  K = 1/R²  →  0
S²  is the one-point compactification of the plane:  ℝ² ∪ {∞} ≅ S²
```

Locally a huge sphere is flat; globally the plane **plus one point** *is* the
sphere. This is the circline theorem raised by one dimension — and it is
literally `ℂP¹`, the object already adopted under `S1`. The owner has arrived at
the Riemann sphere from the geometry side.

**One precision, the same as before:** `S²` is embedded in `ℝ³` but is
**intrinsically 2-dimensional**. The move is 2D ↔ 2D, not 3D → 2D; the ambient
space is 3-dimensional, the object is not.

**Classification:** `dim 2 → dim 2`. One-point compactification closes the
underlying plane by one point and adds no demonstrated freedom. **Type-T; the μ
claim remains unpaid.**

## 6 · What is *not* proved `[S]`

Upheld verbatim from the D1 owner and the Trinity canon, because this document
must not be read as licensing more than it earns:

- **Division by zero does not prove `μ₀`.** Division, fields, limits and
  meromorphic maps all presuppose D1 distinctions already. The example runs from
  D1 semantics *toward* the D0 horizon; it cannot establish the aperture it
  illustrates.
- **No ontological emergence follows.** Every theorem in §2 is about structures
  and maps. None is about the world.
- **`μ₀` remains `[I/C]`** and still owes a reproducible distinction
  discriminator and a lower-description recovery test.
- **No descriptor in §4 is a μ criterion.** A demonstrated reduction defeats a
  claimed novelty; absence of a reduction proof does not establish irreducibility.
  The full `KSC-05` contract and the per-interface GP packet remain binding.

## 7 · Claims and kills

| Claim | Tier | Kill |
|---|---|---|
| no quotient `y` satisfies `0·y=N≠0`; field division therefore excludes denominator zero | `[A]` | exhibit such a field element `y` |
| every step of `1/10^n` is a legal total operation | `[A]` | exhibit a step that divides by zero |
| the two-sided limit fails on `ℝ` | `[A]` | show left and right limits agree |
| `f_N` is total on `ℂP¹` | `[A]` | exhibit a point of `ℂP¹` where it is undefined |
| compactification gains no dimension | `[A]` | show `dim ℂP¹ ≠ dim ℂ` |
| totality, order and dimension are non-equivalent descriptors in the displayed examples | `[A]` | show the examples do not separate the named descriptors |
| the division boundary is type-T and does not establish `μ₀` | `[S]` | exhibit and test the claimed new effective freedom under KSC-05 |
| a continuous graph is homeomorphic to its domain; all relations form `𝒫(X×X)` | `[A]` | violate the stated continuity/homeomorphism or Cantor result |
| a sphere-circle through `N` projects to a straight line | `[A]` | exhibit one that projects to a bounded curve |
| adjoining `∞` incorporates the missing-line stratum into the circline class; no global closure without declared degenerates is claimed | `[A]` | show the generalized-circle correspondence or stated degeneration is wrong |
| line-as-circline is a scoped type-T description; no μ follows from it | `[A/S]` | supply a KSC-05 packet that independently establishes the claimed novelty |

**Recovery test for this document.** Delete §4–§5 and the D1 owner's fence still
stands on its own authority. The typology explains the fence; it does not carry
it.

•   ⊙   ○ — *the operation stops, the structure is declared, and only sometimes is a freedom born.*
