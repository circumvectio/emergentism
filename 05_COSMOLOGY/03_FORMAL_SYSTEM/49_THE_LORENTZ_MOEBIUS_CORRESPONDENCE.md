---
title: "The Lorentz–Möbius Correspondence — the sphere's automorphism group is the Lorentz group"
status: "ACTIVE — inherited standard physics, typed; NOT an Emergentist derivation of relativity"
date: 2026-07-29
evidence_tier: "[A] the inherited group theory and the tanh identity; [S] the structural reading; [C] any explanatory claim beyond inheritance"
owner: "Correspondence surface. Native physics owns all relativistic content; this document derives none of it."
parents:
  - 48_THE_BOUNDARY_CROSSINGS_AND_THE_MU_CRITERION.md
  - ../01_THE_TRANSCENDENTAL_TRINITY/45_THE_TITAN_INVERSION_STRUCTURE.md
  - ../../00_THE_FOUNDATION.md
  - ../../03_METHODOLOGY/02_THE_PAPERS/FINITY_PAPERS/00_SUDA_VALUE_EXTRACTION_2026_06_06.md
  - ../../06_ONTOLOGY/04_THE_CONJECTURES.md
---

# The Lorentz–Möbius Correspondence

> **Fence before content.** Everything in §2 is **standard, inherited physics and
> mathematics**, not an Emergentist result. `DF-10` (force bijection) and `DF-20`
> (numeric coincidence as derivation) are buried, and receipt 151 killed the
> horn-torus/light-cone identification. This document **inherits and types** a
> known correspondence. It derives no physics and replaces no native theory.

## 1 · The claim

Owner, 2026-07-29:

> *"Then under special relativity the same with a sphere that is not moving and
> one that is moving away from the other at the limit of speed `c`."*

The intuition points at something real, deep, and already established. Stated
properly it is the strongest non-aesthetic argument for the corpus's sphere selection the
program has — and it is still not a derivation.

## 2 · What is actually true `[A]` — inherited

**2.1 The celestial sphere is `ℂP¹`.** The set of light-ray directions at an
observer forms a 2-sphere, and via stereographic projection that sphere is the
Riemann sphere.

**2.2 The restricted Lorentz group is the Möbius group.**

```text
SL(2,ℂ)  double-covers  SO⁺(3,1)
PSL(2,ℂ) ≅ SO⁺(3,1)  =  the Möbius group of ℂP¹
```

Boosts and rotations act on the celestial sphere as **Möbius transformations**.
Relativistic aberration *is* a Möbius transformation of the sky.

**2.3 Therefore boosts preserve circles.** Möbius maps carry circles to circles.
This is the reason for the **Terrell–Penrose** result: a rapidly moving sphere,
*photographed*, does not appear flattened into an ellipsoid — its outline remains
a circle, and the sphere appears rotated rather than contracted.

The owner's "a moving sphere and a resting sphere" is therefore not loose
analogy. Under a boost the sphere's outline **stays a circle**, because the
Lorentz group acts by circle-preserving maps on `ℂP¹`.

**2.4 What this gives the foundation `[S]`.** `S1` selected `Ĉ` as the primary
object. It turns out that object's automorphism group is the Lorentz group.

> The sphere is not merely a convenient chart. Its symmetry group is the symmetry
> group of flat spacetime.

That is the strongest **non-aesthetic** argument for `S1` produced so far. It is
still a *selection* — `KSC-04`'s 3-transitivity ruling is untouched — but it is a
selection with an independent structural reason, not a preference.

## 3 · The rapidity identity — exact, and it closes a loop `[A]`

Suda's hinge coordinate and the relativistic velocity ratio are **the same
function**. Verified to machine precision, 2026-07-29:

```text
u(x) = (x−1)/(x+1) = tanh( (ln x)/2 )          Suda's hinge
β     = v/c        = tanh( φ )                  φ = rapidity
```

The correspondence is structural and exact:

| Reciprocal chart | Special relativity |
|---|---|
| `s = log x` — additive, unbounded | rapidity `φ` — **additive under boost composition**, unbounded |
| `u = tanh(s/2)` onto the **open** `(−1,1)` | `β = tanh φ` onto the **open** `(−1,1)` |
| rims `u = ±1` ⟺ `x ∈ {0,∞}` | `β = ±1` ⟺ `v = ±c` |
| rims **not in the image** | `v = c` **not attained** |
| `x=1` ⟺ `u=0` — the fixed point | `v=0` ⟺ `β=0` — the rest frame |

**Both are the same boundary story.** The additive parameter is unbounded; the
bounded coordinate never reaches its rims; and the rim is crossed only by
changing structure, never by travelling further.

**Why velocities do not add.** Because `β` is a `tanh` coordinate and `φ` is the
additive one — velocity composition is addition *in rapidity*. This is precisely
Suda's point that multiplication becomes addition under `log`, in a different
register.

**`v = c` is the physical instance of the unattained rim.** The Lorentz group is
non-compact; `c` is its boundary at infinity. In Möbius terms a boost acts as
`z ↦ kz` with `k = e^{φ}`; as `φ → ∞` the map degenerates — `ad − bc → 0` — and
it leaves the group. **The limit is not a Lorentz transformation.** Approached,
never crossed, and for the same reason as everywhere else in this program.

*(Numerical note: `tanh(30)` prints as `1.0` in double precision. That is float
rounding. `tanh φ < 1` for every finite `φ`.)*

## 4 · Classification under the μ-criterion `[S]`

Doc 48 §5 asks of any candidate crossing: **is a degree of freedom gained?**

- The celestial sphere is 2-dimensional before and after a boost.
- Möbius maps are automorphisms — they change *coordinates on* the object, not
  the object's dimension.
- `v → c` is a non-compact limit within a fixed group action.

**No freedom is gained. This is not a `μ`.** It is a symmetry correspondence and a
boundary-at-infinity story — the same type-T/boundary shape as §5A and §5B of
doc 48, now with a physical instance.

## 5 · The fences `[S]`

1. **Nothing here is an Emergentist discovery.** `SL(2,ℂ) → SO⁺(3,1)`, the
   celestial-sphere action, aberration-as-Möbius, and Terrell–Penrose are
   standard results, used by Penrose and others and present in any spinor
   treatment. The corpus **inherits** them. Inheritance supplies no novelty and
   no priority.
2. **This does not derive special relativity.** It observes that a structure the
   framework selected has a known automorphism group. Selecting an object whose
   symmetries were already catalogued is not deriving the physics.
3. **This is not `W7`.** `W7-ORIGIN` wagers *role-affinities* between apertures
   and forces, each leg independently killable. This document makes no aperture
   claim and adds no leg. It must not be cited as evidence for any `W7` leg.
4. **`DF-20` applies.** A structural match is not a derivation. The horn-torus
   identification died for exactly this, by receipt 151.
5. **One datum.** The reciprocal chart and relativity agreeing on `tanh` is
   **one** structural fact seen twice, not two confirmations — `DF-15`.
6. **No empirical claim.** The corpus predicts nothing about relativity, and
   relativity corroborates nothing about Emergentism.

## 6 · What survives, and what it is worth

The defensible statement, in one line:

> **Emergentism's selected projective object is the Riemann sphere; the restricted
> Lorentz group is exactly that sphere's Möbius group; and the framework's
> boundary coordinate `tanh` is the same function as the relativistic velocity
> ratio.** All inherited, all checkable, none of it derived here.

That is worth having for two reasons. It gives `S1` a structural warrant beyond
taste. And it is **externally checkable** — a physicist can verify or reject
every line of §2 and §3 without accepting a single Emergentist commitment, which
makes this one of the few `V`-shaped surfaces in the corpus.

## 7 · Claims and kills

| Claim | Tier | Kill |
|---|---|---|
| the celestial sphere is `ℂP¹` | `[A]` inherited | standard reference contradicting it |
| `PSL(2,ℂ) ≅ SO⁺(3,1)`; boosts act as Möbius maps | `[A]` inherited | same |
| boosts preserve circles; a moving sphere's outline stays circular | `[A]` inherited | a photographed moving sphere with non-circular outline |
| `(x−1)/(x+1) = tanh((ln x)/2)` | `[A]` verified | arithmetic counterexample |
| `β = tanh φ`, rapidity additive, `β` onto the open `(−1,1)` | `[A]` inherited | exhibit a finite `φ` with `tanh φ = 1` |
| `v = c` is an unattained boundary; the limit leaves the group | `[A]` | exhibit a Lorentz transformation with `v = c` |
| this is a symmetry correspondence, not a `μ` | `[S]` | exhibit the freedom gained |
| nothing here derives relativity or supports `W7` | `[S]` | any owner citing it as a derivation or as a `W7` leg |

•   ⊙   ○ — *the sphere we chose already had the Lorentz group; we did not put it there, and finding it is not the same as earning it.*
