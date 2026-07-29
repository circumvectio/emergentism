---
title: "The Boundary Crossings and the μ-criterion — proofs at the division boundary"
status: "ACTIVE — formal owner for the boundary-crossing typology; upholds the D1 owner's fence on division-as-μ₀"
date: 2026-07-29
evidence_tier: "[A] §2 theorems and §4 typology; [S] §5 the μ-criterion; [I] §3 the template reading"
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
the claim does not yet say: **what kind of crossing this is, and why it is not a
`μ`.**

## 2 · Five theorems at the division boundary `[A]`

**T-A · `a/0` is not unknown; it is provably non-existent.**
In a field `F`, suppose `y = N/0` for `N ≠ 0`. Then `0·y = N`. But `0·y = 0` for
every `y ∈ F`. So `N = 0`, contradiction. Division is therefore partial by
theorem, not by convention:

```text
div : F × (F \ {0}) → F
```

**T-B · The limit game is legal at every step, and never reaches the boundary.**
For `x_n = 10^{-n}`, each `1/x_n = 10^n` is a finite field element obtained by a
totally defined operation. The sequence is unbounded; no term is `∞`; no step
divides by zero. **The owner's formulation is exact:** one stays inside finity
throughout, and the boundary is never an operand.

**T-C · On the line, the two-sided limit fails.**
For `N > 0`: `lim_{x→0⁺} N/x = +∞` and `lim_{x→0⁻} N/x = −∞` in the two-point
extended reals. Left and right disagree, so `lim_{x→0} N/x` **does not exist** in
`ℝ`. This is a genuine defect of the line, not a notational inconvenience.

**T-D · On the sphere, the limit exists and the map becomes total.**
`ℂP¹` has a **single** point at infinity, unsigned. Hence `lim_{z→0} N/z = ∞`
irrespective of direction, and

```text
f_N : ℂP¹ → ℂP¹ ,   f_N(z)=N/z ,   f_N(0)=∞ ,   f_N(∞)=0
```

is a **total** meromorphic map. **The defect of T-C is repaired exactly by the
register change.** This is a concrete payoff of sphere primacy (`S1`): the line
has a hole at the boundary; the sphere does not.

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
1  APPROACH     the operation runs toward its domain boundary      1/x, x→0
2  STOP         the operation is undefined there                   a/0  (T-A)
3  RESTRUCTURE  a different structure is explicitly declared        ℝ ⟶ ℂP¹
4  TOTALITY     the operation becomes total in the new structure    f_N(0)=∞ (T-D)
5  RECOVERY     restrict back and recover the old behaviour exactly ℂP¹ ⊃ ℂ\{0}
```

Stage 5 is what distinguishes a legitimate restructure from a redefinition. Any
crossing that cannot recover its lower description has not crossed a boundary —
it has replaced the subject.

## 4 · Three kinds of boundary crossing — and they are independent `[A]`

The central result. Boundary crossings differ in **what they change**, and the
differences come apart:

| Crossing | Totality repaired? | Order lost? | Freedom gained? |
|---|---|---|---|
| `ℝ → ℝP¹` | **yes** — `1/x` becomes total | **yes** — total order → cyclic | no — `dim_ℝ` stays 1 |
| `ℂ → ℂP¹` | **yes** — `f_N` becomes total | n/a — `ℂ` is unordered | no — `dim_ℝ` stays 2 |
| `ℝP¹ → Ĉ` | already total | already lost | **yes** — `dim_ℝ` 1 → 2 |

So there are three separable phenomena:

```text
type-T   TOTALITY    a partial operation becomes total
type-O   ORDER       an order structure is lost
type-D   DIMENSION   a degree of freedom is gained
```

`ℝ → ℝP¹` is simultaneously type-T and type-O while gaining nothing. `ℝP¹ → Ĉ`
is purely type-D. **Totality, order and dimension are independent axes of
boundary change**, and conflating them is the error behind more than one buried
form.

## 5 · The μ-criterion `[S]`

`E1` defines the ladder in terms of **freedoms** — "axes of allowed variation."
`E5` defines a `μ` as an aperture "at which a **new effective freedom** becomes
available." Read together with §4, that yields a criterion:

> **Only type-D crossings are candidate `μ`-crossings.**
> A crossing that repairs totality or dissolves an order, without gaining a
> degree of freedom, is a genuine boundary crossing and **not** a `μ`.

Three consequences, all of which *confirm* existing canon rather than overturn
it:

**5.1 The division boundary is not `μ₀`.** It is type-T. This is exactly the D1
owner's fence — *"division by zero… neither defines nor proves `μ₀`"* — now
holding as a **theorem** rather than a caution. The fence was right; §4 says why.

**5.2 `KSC-22` is vindicated and explained.** It rules that adjoining `∞_P` does
not create D2 — correct, because `ℝ → ℝP¹` is type-T/O, not type-D. And it
selects the *relational lift* as the D2 neighbour — correct, because the space of
configurations over a carrier is a genuine dimension gain.

A precision that reconciles two earlier results: a **single** graph
`Γ_f = {(x,f(x))}` is a curve homeomorphic to its domain and adds nothing —
which is why "a graph proves strong emergence" fails. The **space of all such
relations** over the carrier is the D2 object, and it is genuinely larger. One
graph is not a lift; the configuration space is.

**5.3 The criterion is a live test.** Any future `μ` claim must now exhibit the
gained freedom, not merely a repaired operation or a dissolved order. This is
narrower than the `KSC-05` contract and does not replace it — a candidate must
still supply boundary, saturation statistic, threshold, novelty test, recovery,
prediction and kill.

## 5A · Test case — "a straight line is a circle of infinite diameter" `[A]`

Owner, 2026-07-29, offered as a proof of the μ-limit. It is a **real theorem**,
it is strong support for sphere primacy, and the §5 criterion classifies it
immediately — which is exactly what a criterion is for.

### 5A.1 What is true, and it is more than the claim says

**The circline theorem.** Under stereographic projection, a circle on the sphere
maps to a **circle** in the plane if it misses the north pole, and to a
**straight line** if it passes through it. Verified 2026-07-29: the sphere-circle
cut by the plane `z = 1−y` (which contains `N`) projects to the exact line
`v = 1`.

So on `ℂP¹` there is no distinction to draw:

> **A line is a circle — the one that contains `∞`.**
> Möbius maps preserve the whole class; "circles and lines" is one family, not two.

**The curvature reading is also correct.** A circle of radius `R` has curvature
`κ = 1/R → 0`. A sector of huge radius is *locally* indistinguishable from a
segment. The owner's phrasing captures this exactly.

**And it subsumes a result already in canon.** Receipt 175 established that
`ℝ ∪ {∞}` is a great circle on `Ĉ`. That is the circline theorem's special
case — the meridian is simply the line-through-`∞` that is additionally
`ι`-invariant. The geometry and the algebra were describing the same object.

### 5A.2 One precision — "a circle of infinite diameter" is not a circle

In `ℝ²` there is **no** circle of infinite radius. The family of circles is
parametrised by `(center, radius)` and is **not closed**: lines are its limit
points and are not members. The statement is therefore *false in the plane* and
*true on the sphere*, where the family is closed and lines are members.

This is the session's recurring shape once more: the object fails on the line and
succeeds on the sphere.

### 5A.3 The criterion classifies it — type-T, not a `μ` `[A]`

```text
circles in the plane   (cx, cy, r)                dim 3   NOT closed
lines in the plane     (angle, offset)            dim 2   the missing boundary stratum
circlines on ℂP¹       planes in ℝ³ cutting S²    dim 3   CLOSED
```

Compactification adds the **boundary stratum** — closure — **not a dimension**.
`dim 3 → dim 3`.

> **Therefore this is a type-T crossing, and by §5 it is not a `μ`.**

It is the *same* repair as `T-D`: adjoining `∞` makes a partial thing total —
there, a partial operation; here, a non-closed family. One move, two
totality-repairs. That unification is the real result, and it is worth more than
the μ-claim would have been.

**What it does prove:** that line and circle are one kind on the sphere, that the
plane's distinction between them is an artefact of the missing point, and that
sphere primacy is doing genuine mathematical work rather than being a preference.

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

**Classification:** `dim 2 → dim 2`. Compactification closes the family and adds
no freedom. **Type-T. Not a `μ`.** Third instance of one repair.

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
- **Type-D is necessary, not sufficient.** A dimension gain makes a crossing a
  *candidate* `μ`; it does not make it an emergence event. Formal reducibility
  can still account for it — `GP-MU2`'s kill stands.

## 7 · Claims and kills

| Claim | Tier | Kill |
|---|---|---|
| `a/0` is provably non-existent in a field | `[A]` | exhibit a field with `0·y = N ≠ 0` |
| every step of `1/10^n` is a legal total operation | `[A]` | exhibit a step that divides by zero |
| the two-sided limit fails on `ℝ` | `[A]` | show left and right limits agree |
| `f_N` is total on `ℂP¹` | `[A]` | exhibit a point of `ℂP¹` where it is undefined |
| compactification gains no dimension | `[A]` | show `dim ℂP¹ ≠ dim ℂ` |
| totality, order and dimension are independent axes | `[A]` | show one always accompanies another |
| only type-D crossings are candidate `μ`s | `[S]` | show `E1`/`E5` define freedom without dimension |
| the division boundary is type-T, hence not `μ₀` | `[S]` | exhibit the freedom it gains |
| a single graph adds nothing; the configuration space does | `[A]` | show `Γ_f` is not homeomorphic to its domain |
| a sphere-circle through `N` projects to a straight line | `[A]` | exhibit one that projects to a bounded curve |
| the circline family is closed on `ℂP¹`, not closed in `ℝ²` | `[A]` | exhibit a circle of infinite radius in `ℝ²` |
| line-as-circle is type-T (dim 3 → 3), hence not a `μ` | `[A]` | exhibit the dimension it gains |

**Recovery test for this document.** Delete §4–§5 and the D1 owner's fence still
stands on its own authority. The typology explains the fence; it does not carry
it.

•   ⊙   ○ — *the operation stops, the structure is declared, and only sometimes is a freedom born.*
