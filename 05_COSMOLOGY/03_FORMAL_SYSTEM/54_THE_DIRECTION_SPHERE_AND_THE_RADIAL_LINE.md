---
title: "The Direction Sphere and the Radial Line — 2 + 1 = 3, and the radius is not on the sphere"
status: "ACTIVE — item 6. Standard vector geometry, inherited under KSC-12; the reading is the corpus's."
date: 2026-07-30
evidence_tier: "[A] §1, inherited standard geometry; [S] the reading; [I] any Titan gloss"
owner: "Subordinate to 52_THE_GENERATIVE_BASE.md and 48_THE_BOUNDARY_CROSSINGS.md on all dimension claims."
parents:
  - 52_THE_GENERATIVE_BASE.md
  - 49_THE_LORENTZ_MOEBIUS_CORRESPONDENCE.md
---

# The Direction Sphere and the Radial Line
*(new doc, slot `05_COSMOLOGY/03_FORMAL_SYSTEM/54_…md` — verified free)*

> **Fence first.** All of §1 is standard vector geometry, **inherited**. `KSC-12`: none of it
> transfers proof to §3. This page does **not** claim the sphere explains or generates 3-space.

## 1 · What is true `[A]` — inherited

**1.1 The factorization is exact.** With `S² = {u ∈ ℝ³ : |u| = 1}`:

```
ℝ³ \ {0}  ≅  S² × ℝ₊       v ↦ (v/|v|, |v|)      inverse (u,r) ↦ ru
```

A diffeomorphism, one representation per `v`. **`S²` is the space of directions in `ℝ³`;
`ℝ₊` is the space of magnitudes.** Count: `2 + 1 = 3`.

**1.2 "Spinning", made exact.** `SO(3)` acts on `ℝ³` with orbits

```
ℝ³  =  {0}  ⊔  ⨆_{r>0} S²_r     one sphere per radius, plus a fixed point
```

transitive on each sphere with stabilizer `SO(2)`, so `S² ≅ SO(3)/SO(2)`, `dim = 3 − 1 = 2`.
So spinning **does** exhaust every vector — *one sphere at a time*. Rotation is an isometry:
it never changes `|v|`. Spinning exhausts **directions**; only the radial family exhausts **lengths**.

## 2 · Two corrections the phrasing needs `[A]`

**2.1 Stereographic projection is the wrong operator.** It is a chart `S²\{N} → ℝ²` — a 2↔2 map
carrying **no radial information**; `r` is not recoverable from a stereographic image. What
exhausts `ℝ³\{0}` is the **polar map** `v ↦ (v/|v|, |v|)`. Stereographic projection then acts
*inside the first factor*, as a chart on directions — exactly its role in doc 49 §2.1, where the
celestial sphere is a sphere of directions carrying no radius at all.

**2.2 "Every vector" excludes one.** `0` has no direction. The factorization is of `ℝ³\{0}`; the
origin is the unique `SO(3)`-fixed point and the one place the direction map is undefined.

## 3 · The reading — this part is the corpus's `[S]`

> Three-space factors into *the object the corpus already selected* and *the chart it already uses*.
> Direction factor: `S²` — adopted under `S1`, the celestial sphere of doc 49. Magnitude factor:
> `(ℝ₊, ×)` with `ι(r)=1/r` — the reciprocal line of doc 52: `s = log r` additive and unbounded,
> `u = (r−1)/(r+1)` bounded on the open `(−1,1)`, both rims `r→0`, `r→∞` unattained.

On that reading the **unit sphere is not a normalization convention**: `r = 1` is `ι`'s fixed point
on the radial factor and its exact midpoint in the hinge coordinate (`u(1)=0`, rims at `±1`). The
sphere the corpus draws is the one the radial line already singles out.

## 4 · What this is not `[S]`

1. **Not a dimension claim.** `S²` stays intrinsically 2-dimensional (doc 48 §5B; `/riemann/`:
   "the sphere is D2, not D3"). Three-space is `sphere × radius`, never `sphere` alone.
2. **Not a `μ`.** The factorization is a homeomorphism — exactly reducible, invertible, no freedom
   gained. Under `HR-1` a `μ` is a *failure* of reducibility; this is its opposite. Not even type-T:
   nothing is closed or completed.
3. **Not a derivation of 3-space.** A bijection is not an explanation, and `ℝ³` is presupposed
   before `S²` can be defined as a subset of it. This re-describes three-space; it does not produce
   it. The circularity is conceded, not answered.
4. **One datum, third notation.** `DF-15` binds: doc 45's chart identity, doc 52's reachability, and
   this radial reading are one structure in three notations. Agreement is **not** evidence.
5. **`DF-20`** — structural match ≠ derivation. No `W7` leg, no aperture claim, no physics.

## 5 · Claims and kills

| Claim | Tier | Kill |
|---|---|---|
| `ℝ³\{0} ≅ S² × ℝ₊`, uniquely | `[A]` | exhibit `v ≠ 0` with no such `(u,r)`, or with two |
| `SO(3)`-orbits are `{0}` and the spheres; `S² ≅ SO(3)/SO(2)`, `dim 2` | `[A]` | exhibit an orbit that is neither, or a third direction parameter |
| rotation preserves `|v|`; spinning never yields the radius | `[A]` | exhibit a rotation changing a length |
| stereographic projection is radius-blind | `[A]` | recover `r` from a stereographic image alone |
| the radial factor **is** the corpus's reciprocal chart | `[S]` | show `(ℝ₊,×,ι)` is not the doc-52 line |
| this derives nothing about three-space | `[S]` | any citation of this page as an explanation of dimension |

**Own kill.** If ever cited to make `S²` three-dimensional, or to claim the sphere *explains*
3-space, this page has committed the corpus's characteristic error — withdraw it, do not defend it.

•  ⊙  ○ — *the sphere is every direction, the radius every length, and neither is why there are three.*