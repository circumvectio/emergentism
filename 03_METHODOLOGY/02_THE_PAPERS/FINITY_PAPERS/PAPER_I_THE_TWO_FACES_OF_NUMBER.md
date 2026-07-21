---
rosetta:
  primary_level: L3
  primary_column: Philosophy
  operator: "Kṛṣṇa ◇"
  tier: "God"
  regime: "Vaiśya"
  secondary: {level: L5, column: Cosmology, role: "Finity geometry"}
  register: "[A] positive-real reciprocal-chart identities; [I] finity and balance readings; no Titan arithmetic."
  canonical_phrase: "The Two Faces of Number"
title: "The Two Faces of Number — Corrected Reciprocal-Chart Study"
status: "ACTIVE RESEARCH NOTE — subordinate to the D1 arithmetic and Titan owners"
evidence_tier: "[A] stated identities on their domains; [I] naming and crosswalks."
supersedes_blob: "0c1b1252e82ea5cb7f8b7c741a7820a626cfdf17"
---

**Corpus:** Emergentism

# The Two Faces of Number

## Finity as the Self-Dual Centre, and the Conjugacy of the Additive and Multiplicative Charts on the Riemann Sphere

*Emergentism / the Burrisphere programme (Yves R. Burri). Ideas set out 2024; this rigorous statement 2026.*

> **Tiering.** Every claim carries an evidence tier — `[A]` elementary mathematics, `[S]` framework-internal structure, `[I]` interpretive reading, `[C]` conjecture — and is never silently upgraded. The mathematics here is old and elementary; the framework's contribution is the *naming* and the *coupling*, not the theorems.

> **[金] Boundary.** The predecessor treated numeric `0`, `1`, and projective
> infinity as if they were the Titan roles, printed a Titan operation, and said
> that division by zero was well-defined on the sphere. Those statements are
> withdrawn. This paper now studies only the positive-real reciprocal chart.
> The D1 arithmetic owner and Titan canon supersede every stronger reading.

---

## Abstract

We formalize the claim that the number system carries two complementary charts: an **additive** chart centred on `0` (the additive identity, with order and translation) and a **multiplicative** chart centred on `1`, the unique positive fixed point of the reciprocal `I(x) = 1/x` with `I'(1) = −1`. On the Riemann sphere `S²` with half-angle coordinates `φ = cot(θ/2)`, `ν = tan(θ/2)` (so `φ · ν = 1`), we show that under the identification `x = ν` the reciprocal `x ↦ 1/x` is **exactly** the colatitude reflection `θ ↦ π − θ` across the equatorial plane (longitude fixed) — which swaps the two poles and fixes the equatorial circle `θ = π/2`, where `φ = ν = 1`. Adopting the reciprocal-invariant energy `E(x) = (log x)²` (Suda, 2025), we prove the exact bridge to the sphere's balance functional `B = sin θ` (here `[I]` *balance* is the interpretive reading of the coordinate `sin θ`),

> `B = sin θ = 2x/(1 + x²) = sech(log x) = sech √E`   (per hemisphere, `s = log x` of fixed sign),

so the multiplicative centre `x = 1` coincides with the equatorial maximum `B = 1`, with `E ≈ 2(1 − B)` near the equator. The two charts are conjugate by the group isomorphism `log : (ℝ₊, ·) ≅ (ℝ, +)`. Each claim is marked by evidence tier: the identities are `[A]`; the reading of `E` as *imbalance*, of `B` as *balance*, and of `1` as **finity** is `[I]`. The selected Titan seats are a separate metaframe and perform no arithmetic. The construction extends Suda's reciprocal-symmetry programme (Parts I–III) by coupling the multiplicative chart to the additive chart and to a selected coordinate on `S²`.

**Keywords:** Riemann sphere; reciprocal symmetry; multiplicative identity; logarithmic coordinate; hyperbolic secant; Cayley transform; evidence tiers.

---

## 1. Introduction

The number line is taught with `0` at the centre: a seesaw on which `+a` and `−a` balance about the origin. This is the **additive** picture, and it is correct — for addition, order, and the metric. But a great deal of nature is not additive. Growth, scale, frequency, perception, ratio — these compose by *multiplication*, and under multiplication the "do-nothing" centre is not `0` (which annihilates) but `1` (the identity). This paper makes precise a simple consequence: **number wears two faces, an additive face centred on `0` and a multiplicative face centred on `1`, and they are conjugate by the logarithm.** `[S]`

The multiplicative face has a natural home — the Riemann sphere — and a natural symmetry — the reciprocal `I(x) = 1/x`, which exchanges the small and the large while fixing the unit. We make the centrality of `1` rigorous in three equivalent charts, and then prove that this multiplicative centre is *the same locus* as the equatorial maximum of the sphere's balance functional. The reciprocal-symmetry apparatus we use was given independently and rigorously by Suda (2025, Parts I–III) on the positive reals; we adopt it for the coordinate-level rigour and add two things: the coupling to the **additive** chart, and the bridge to a **balance functional** on `S²`.

A note on provenance, marked at its honest tier. The framework's use of three selected boundary roles and the coinage *finity* were set out by the author in 2024. We do not here supply a third-party-dated, externally verifiable artifact (DOI or archived timestamp) for that 2024 statement; accordingly we do **not** advance it as a settled precedence claim, and the reader should treat the priority assertion as `[I]` until such a receipt is supplied. Independent later similarity can motivate comparison, but is not evidence that the shared interpretation is true. Suda's 2025 work is cited for the positive-real reciprocal formalism. `[I]`

We claim nothing about the consistency or unification of mathematics, and nothing about physics. This is a paper about *one structure*, stated at its honest tier.

---

## 2. Two charts, one isomorphism `[A]`

Let `ℝ₊ = (0, ∞)`. The exponential and logarithm furnish a group isomorphism

> `log : (ℝ₊, ·) → (ℝ, +)`, `log(xy) = log x + log y`, with inverse `exp`, and `log 1 = 0`.

Thus the **multiplicative** group `(ℝ₊, ·)` — centred on its identity `1` — is carried isomorphically onto the **additive** group `(ℝ, +)` — centred on its identity `0`. The two faces are not rivals; they are the *same* group in two dresses, and the bridge's keystone is `log 1 = 0`: the multiplicative centre maps to the additive centre.

The faces differ in what they make visible. The ordinary real line is ordered
and has no infinite elements; its two-ended compactification may adjoin
`−∞` and `+∞`. Division by zero remains undefined in the field. The positive
ray embeds as a one-dimensional arc in the Riemann sphere
`S²≅ℂP¹`; adjoining the projective point changes the structure but does not
make field division at zero valid. The extended inversion map may exchange
numeric `0` and projective `∞_P`. That map is not an evaluation of `N/0` in a
field. This paper works on `x∈ℝ₊=(0,∞)`.

---

## 3. The reciprocal is a reflection `[A]`

On `ℝ₊` consider `I(x) = 1/x`. Its fixed points satisfy `x = 1/x`, i.e. `x² = 1`; on the full real line these are `±1`, and on `ℝ₊` the **unique** fixed point is `x = 1`. Its derivative `I'(x) = −1/x²` gives `I'(1) = −1`: an orientation-reversing fixed point — a mirror, not an attractor or repeller.

Conjugating by `h(x) = log x` (so `h⁻¹(s) = eˢ`) yields, for `g = h ∘ I ∘ h⁻¹`,

> `g(s) = log(1/eˢ) = −s`.

So **inversion is exactly the reflection `s ↦ −s`** through `s = 0`, an involution (`g ∘ g = id`) with `g'(s) ≡ −1`, whose unique fixed point `s = 0` is `x = 1`. This is the rigorous content of "the reciprocal pivots about the unit."

---

## 4. The invariant energy: a strictly convex well at the unit `[A]`

Define the reciprocal-invariant radius `ρ(x) = |log x|` and the **energy** `E(x) = ρ(x)² = (log x)²` (Suda, 2025, Part II). Invariance under inversion is immediate:

> `E(1/x) = (−log x)² = (log x)² = E(x)`,  i.e. `E ∘ I = E`.

In the coordinate `s = log x`, `E = s²` is even and strictly convex (`E'' = 2 > 0`), with a **unique** global minimum at `s = 0` — that is `x = 1`, where `E(1) = 0` — and `E(x) → +∞` as `x → 0⁺` or `x → ∞`. The twist index `τ(x) = sign(log x)` (Suda, 2025, Part III; there written `ϕ(s) = sign(s)`) flips under inversion (`τ(1/x) = −τ(x)`) and vanishes only at the fixed point. The unit is therefore the unique zero of a faithful, inversion-symmetric energy: `1` is *the* balanced scale, and `0`, `∞` are its symmetric extremes — equidistant from `1` in the `|log x|` metric, infinitely far in it.

---

## 5. The projective egg `[A]`

The Cayley transform `u = (x − 1)/(x + 1)` is a strictly increasing bijection `ℝ₊ → (−1, 1)` (`du/dx = 2/(x+1)² > 0`), with inverse `x = (1 + u)/(1 − u)`, sending

> `0⁺ ↦ −1`,  `1 ↦ 0`,  `∞ ↦ +1`.

It compresses the entire positive ray onto a bounded interval with the unit at the centre — what Suda (2025, Part II) names the *egg of infinity*, the bounded image that holds both poles on its rim. Under inversion,

> `u(1/x) = (1 − x)/(1 + x) = −u(x)`,

so `I` becomes the **half-twist** `u ↦ −u` about `u = 0`. This is the *same* order-2 reflection as §§3–4 in a third chart: since `u = tanh((log x)/2) = tanh(s/2)` and `tanh` is odd, `s ↦ −s ⟺ u ↦ −u`. Three charts — multiplicative `x`, additive `s = log x`, bounded `u` (Suda's egg) — one involution fixing `x = 1`.

---

## 6. The bridge to `S²`: the unit is the equator `[A]`

This is the paper's centre. On `S²` with colatitude `θ ∈ (0, π)` and longitude `λ` the framework sets `φ = cot(θ/2)`, `ν = tan(θ/2)`, so `φ · ν = 1` identically (a coordinate definition; tiered `[S]`/definition). The bare trigonometric identities below are `[A]`. Take the identification

> `x = ν = tan(θ/2)`  ⟹  `φ = 1/x = cot(θ/2)`  (forced, since `φ · ν = 1`).

Then each clause of the multiplicative chart becomes a clause about the sphere:

- **Inversion = the `φ ↔ ν` swap = reflection across the equatorial plane.** Since `ν(π − θ) = tan(π/2 − θ/2) = cot(θ/2) = 1/ν(θ)`, the map `x ↦ 1/x` *is* the colatitude map `θ ↦ π − θ` (longitude `λ` fixed): it swaps `φ ↔ ν` and exchanges the two poles (`θ = 0 ↔ θ = π`). **Caution on "antipodal."** This map is the *reflection across the equatorial plane*, not the antipodal map of `S²`: the true antipodal map is `(θ, λ) ↦ (π − θ, λ + π)`. They agree only up to the longitudinal half-turn `λ ↦ λ + π`. Because the present claim is `[A]`, we name the map exactly: it is the **equatorial reflection** `θ ↦ π − θ`.
- **The unit = the equator.** `x = ν = 1 ⟺ θ = π/2 ⟺ φ = ν = 1`. On the one-parameter colatitude reduction `θ ∈ (0, π)` (equivalently the reduced reciprocal dynamics on `ℝ₊`, parametrized by `ν` alone) the equator `θ = π/2` is the **unique** fixed point of `θ ↦ π − θ`. On the *full* sphere the fixed-point set of the equatorial reflection is the **entire equatorial circle** `θ = π/2` (all longitudes); the single-point statement holds only after the colatitude reduction, and we state it only there.
- **The poles = the poles.** `x → 0` and `x → ∞` are the two poles of `S²` (`θ = 0`: `ν = 0, φ = ∞`; `θ = π`: `ν = ∞, φ = 0`) — exactly the points where `φ` or `ν` is undefined.

Now the balance functional. With `B = sin θ` and the half-angle identity `sin θ = 2 tan(θ/2)/(1 + tan²(θ/2)) = 2x/(1 + x²)`, write `x = eˢ` (so `s = log x`):

> `B = 2eˢ/(1 + e²ˢ) = 2/(eˢ + e⁻ˢ) = 1/cosh s = sech(log x)`.

Since `E = s² = (log x)²`, we obtain the exact identity

> **`B = sech(log x) = sech √E`**   **(per hemisphere only**, where `s = log x` has fixed sign).

The hemisphere restriction is essential and recurs wherever `B = sech √E` appears: `B` is *even* in `s` (it depends only on `cosh s`), whereas the substitution `s = +√E` takes the positive root, so over the full sphere the bridge `B = sech √E` is two-to-one — the two hemispheres `s > 0` (`x > 1`) and `s < 0` (`x < 1`) carry the same `B` and the same `E`. The signed datum that distinguishes them is exactly Suda's twist index `τ = sign(s)` of §4. Within one hemisphere the bridge is a bijection.

**Theorem (the bridge).** Under `x = ν = tan(θ/2)`: (i) Suda's reciprocal `I` is the equatorial reflection `θ ↦ π − θ` (longitude fixed; *not* the antipodal map); (ii) on the colatitude reduction its unique fixed point `x = 1` is the equator `φ = ν = 1`, and on the full sphere its fixed locus is the equatorial circle; (iii) Suda's energy and the framework's balance satisfy `B = sech √E` per hemisphere, so `E = 0 ⟺ B = 1` at the equator, `E → +∞ ⟺ B → 0` at either pole, and near the equator `1 − B = ½E + O(E²)` (next term `−5E²/24`), i.e. `E ≈ 2(1 − B)` — Suda's energy is, to leading order, *twice the balance deficit*. `[A]`

*Proof.* (i)–(ii) are the displayed half-angle identities; the fixed-locus distinction (single point on the reduction vs. circle on `S²`) is immediate from the definition of the colatitude map. (iii): the chain above gives `B = sech s`; substituting `s² = E` with `s` of fixed sign gives `B = sech √E` per hemisphere; the Taylor expansion `sech s = 1 − s²/2 + 5s⁴/24 − O(s⁶)` gives `1 − B = ½s² − 5s⁴/24 + O(s⁶) = ½E − 5E²/24 + O(E³)`, whence `1 − B = ½E + O(E²)`. ∎

**Numerical check.** The script below verifies `φ·ν = 1` and `B = sech(log ν)` to the precision printed, and exhibits `B(90°) = 1`, `E(90°) = 0`. (Reproduced by the referee; we include it so the check does not rely on a reader's re-derivation.)

```python
# Python 3, standard library only. No seed (deterministic).
import math
print(f"{'theta_deg':>9} {'phi*nu':>12} {'B=sin':>10} {'sech(ln nu)':>12} {'E=(ln nu)^2':>12}")
for deg in (16, 60, 90, 120, 164):
    th = math.radians(deg)
    phi = 1.0 / math.tan(th / 2.0)     # cot(theta/2)
    nu  = math.tan(th / 2.0)           # tan(theta/2)
    B   = math.sin(th)
    s   = math.log(nu)
    sech = 1.0 / math.cosh(s)
    E   = s * s
    print(f"{deg:9d} {phi*nu:12.5f} {B:10.5f} {sech:12.5f} {E:12.5f}")
```

Expected output (five places):

```
theta_deg       phi*nu      B=sin  sech(ln nu)  E=(ln nu)^2
       16      1.00000    0.27564      0.27564      3.85045
       60      1.00000    0.86603      0.86603      0.30174
       90      1.00000    1.00000      1.00000      0.00000
      120      1.00000    0.86603      0.86603      0.30174
      164      1.00000    0.27564      0.27564      3.85045
```

So the multiplicative centre, the energy well, and the equatorial maximum of `B` are **one locus**, and the reciprocal half-twist *is* the reflection across the equatorial plane. The map that takes the macroscopic to the microscopic is the map that takes the northern hemisphere to the southern, fixing only the circle of perfect balance.

---

## 7. Finity and the sovereign frame boundary `[I]`

The mathematics of §§2–6 is elementary and old. The framework calls the
positive reciprocal fixed point `x=1` **finity**. The name highlights the
self-dual centre of this particular chart; it does not make numeric `1` a new
kind of number, a metaphysical substance, or a product of boundary values.

The selected Titan roles are shown without an operator:

```text
•     ⊙     ○
0_T   1_T   ∞_T
```

`0_T`, `1_T`, and `∞_T` are opaque labels, not numeric operands. Ordinary
`0_N` and `1_N` remain numbers. `∞_P` is a projective point only in a named
extension. `ArithmeticSignature(TitanFrame)=∅`; no multiplication or division
licenses a transition among the seats. Alternative algebras may totalize
division only by explicitly leaving the field and declaring their new laws;
they do not change the field result or the Titan type boundary.

---

## 8. Tiers, kill criteria, and relation to prior work

**Tiers.** §§2–6 (the isomorphism, the reflection, the defined function `E`, the Cayley chart, and the bridge `B = sech √E`) are `[A]` on their stated domains. Calling `E` energy, `B` balance, and `1` finity is `[I]`. The provenance/convergence language of §1 is `[I]`. The operator-free Titan display is selected symbolic vocabulary and contributes no theorem.

**Kill criteria.** (a) Exhibit `θ ∈ (0, π)` with `cot(θ/2) tan(θ/2) ≠ 1`, or `B ≠ sech(log ν)` — impossible, would break elementary trigonometry, but the claim is stated so it *could* fail. (b) Produce a pre-2024 source that *names* `1` the self-dual midpoint/third reification and builds on it — this would move the *naming* from novel to prior. (We hold ourselves to the same dated-receipt standard we apply to others: absent an externally dated 2024 artifact for the framework's own statement, the priority claim is `[I]`, not settled.) (c) Show the `[S/I]` reading produces a false operational prediction where the geometry is used.

**Relation to prior work.** The Riemann sphere, the reciprocal's fixed point at `1`, and the log/exp isomorphism are classical (Riemann 1851; Ahlfors 1979). On `ℝ₊`, §4 proves that `1` is the unique fixed point of the reciprocal and the minimizer of the defined function `E=(log x)²`. It is not the geometric mean of numeric zero and projective infinity. The reciprocal-invariant function, log-conjugacy, bounded Cayley chart, and twist index are attributed here to **Suda (2025)** under the source record. Emergentism adds an interpretive naming and balance crosswalk. Similarity between the two programmes is an `[I]` comparison, not evidence that either ontology is true.

---

## 9. Conclusion

The unit is not "just another number." On the multiplicative face it is the fixed mirror of the reciprocal, the floor of an inversion-invariant energy, the centre of the projective egg, and — on the sphere — the equator of perfect balance, the one circle of latitude the small-large exchange leaves fixed. Three charts, one involution, one centre; and that centre is the same locus at which the framework's balance functional is maximal. The locus of maximal equilibrium is the locus about which scale turns inside out. We have stated this at its honest tier, fenced the one emblem that cannot be field arithmetic, named the equatorial map exactly (an equatorial reflection, not the antipode), kept the provenance language at the tier its receipts support, and left the consistency of mathematics, and the rest of the world, untouched. That is the only kind of result worth publishing: a true one, that knows exactly how large it is.

---

## References

- Ahlfors, L. V. (1979). *Complex Analysis: An Introduction to the Theory of Analytic Functions of One Complex Variable* (3rd ed.). McGraw-Hill, New York. ISBN 0-07-000657-1. [The point at infinity and the Riemann sphere, §1.2; linear fractional (Möbius) transformations, ch. 3, §3.]
- Carlström, J. (2004). Wheels — on division by zero. *Mathematical Structures in Computer Science*, **14**(1), 143–184. Cambridge University Press. DOI: 10.1017/S0960129503004110. (Preprint: Stockholm University Research Reports in Mathematics, No. 11, 2001, ISSN 1401-5617.) [Algebraic structure totalizing division, including `1/0`, at the cost of leaving the field; precedent cited in §7 and developed in Paper II.]
- Riemann, B. (1851). *Grundlagen für eine allgemeine Theorie der Functionen einer veränderlichen complexen Grösse* (Inauguraldissertation). Göttingen. Reprinted in *Bernhard Riemann's Gesammelte Mathematische Werke*, ed. H. Weber, 2nd ed., Teubner, Leipzig (1892), pp. 3–48. [Origin of the sphere representation of the extended complex plane.]
- Suda, M. (2025). *Fractional Structure and Möbius Transformation — Part I: Double Inversion in Division and the Phase of Twist.* PhilArchive: https://philarchive.org/rec/SUDFSA (archived 16 August 2025).
- Suda, M. (2025). *Fractional Structure and Möbius Transformation — Part II: The Critical-One Hypothesis and the Egg of Infinity.* PhilArchive: https://philarchive.org/rec/SUDFSA-2. [Source of `E(x) = (log x)²`, the `s = log x` reflection, the projective half-twist normal form, and the term *egg of infinity*.]
- Suda, M. (2025). *Fractional Structure and Möbius Transformation — Part III: Operational Invariants, Fractional Flows, and Measurement Protocols.* PhilArchive: https://philarchive.org/rec/SUDFSA-3. [Cited for the twist index `ϕ(s) = sign(s)` (our `τ`), the operational invariant pair `(E, ϕ)`, and the measurement protocols (Protocol A, B, C) reused in §§4, 6; local PDF acquired 2026-06-06, see `_SOURCES/README.md`.]
- Suda, M. (2025). *A New Ontology of Energy: Zero, Infinity, and the Infinite Egg* (part Ⅰ). [Japanese; no public URL confirmed as of 2026-06-06. Cited for the independent statement 「1 は無限のたまごである」 ("1 is the infinite egg") as corroboration of the finity thesis. See `_SOURCES/README.md`.]
- (Companion) Burri, Y. R. *Paper II — Division by Zero as Category-Correction* (Finity Papers, in preparation); *Paper III — A Product Constraint as a Structural Ethic* (Finity Papers, in preparation). [Paper III cites McGilchrist, I. (2009), *The Master and His Emissary: The Divided Brain and the Making of the Western World*, Yale University Press, New Haven. ISBN 978-0-300-14878-7.]

---

## Figure Spec (for the submission illustrator)

**Figure 1. The two faces of number on the Riemann sphere: one involution, three charts, one centre.**

*Intent.* A single composite figure showing that the reciprocal `x ↦ 1/x` is the equatorial reflection `θ ↦ π − θ`, that the unit `1` is the equator, and that the balance functional `B = sin θ = sech √E` peaks there. The figure must visually distinguish **equatorial reflection** (the correct map) from the antipodal map (which it is *not*).

*Main panel — the sphere (drumhead view).*
- Draw `S²` as a lightly shaded sphere, viewed slightly above the equator so the equatorial circle reads as a horizontal ellipse across the middle (a taut "drumhead").
- **North pole** (top, `θ = 0`): label `0` — annotate `ν = 0, φ = ∞`. **South pole** (bottom, `θ = π`): label `∞` — annotate `ν = ∞, φ = 0`.
- **Equatorial circle** (`θ = π/2`): draw it as a bold ring and label it `1` (finity). Annotate `φ = ν = 1`. Mark it as the **fixed locus** of the reflection — a thin caption: "fixed circle of `θ ↦ π − θ` (all longitudes)."
- Place a representative meridian (fixed longitude `λ`) as a bold arc from north pole to south pole. On it mark a sample point `P` at colatitude `θ` (northern hemisphere, `x = ν < 1`) and its image `P′` at colatitude `π − θ` on the **same meridian** (southern hemisphere, `x > 1`). Connect `P ↔ P′` with a curved double-headed arrow labelled `I : x ↦ 1/x = θ ↦ π−θ`. Crucially, `P` and `P′` share the same longitude — the arrow stays in one meridian plane and reflects across the equator. **Do not** send `P` to the geometric antipode.
- Inset caption near that arrow (small, boxed): "Equatorial reflection — longitude fixed. NOT the antipodal map `(θ,λ)↦(π−θ, λ+π)`." Optionally show the true antipode `P″` as a faint hollow dot a half-turn around in longitude, with a light "×" through the `P→P″` connection to mark it as the map we are *not* using.

*Coordinate ribbon (left margin, vertical).*
- A vertical bracket spanning pole-to-pole labelled with the additive coordinate `s = log x`, running from `−∞` (north pole, `x→0`) through `0` (equator, `x=1`) to `+∞` (south pole, `x→∞`). This shows the log chart of §3 in register with the sphere: the equator is `s = 0`.

*Lower-left inset — the projective egg (Suda's egg of infinity).*
- The Cayley image: a horizontal capsule/egg shape; left rim labelled `−1` (`0⁺`), centre dot labelled `0` (`x = 1`), right rim labelled `+1` (`∞`). A small curved arrow `u ↦ −u` showing the half-twist about the centre. Caption: "bounded chart `u = tanh(s/2)`; same involution."

*Lower-right inset — the bridge curve.*
- A 2-D plot: horizontal axis `s = log x` from `−3` to `+3`; vertical axis from `0` to `1`. Plot `B = sech s` as a bell curve peaking at `(0, 1)`. Mark the peak `(s=0, B=1)` with a dot labelled "equator, `E=0`." Shade the two tails toward `B→0` and label them "poles, `E→∞`." Overlay, as a light dashed parabola near the peak, `B ≈ 1 − s²/2`, with a caption "`1 − B = ½E + O(E²)` (per hemisphere)." A small two-headed left/right arrow under the axis labelled `τ = sign(s)` indicates the two hemispheres that share each `B`.

*Style notes.* Monochrome or two-tone (one accent colour for the reflection arrow and the equator). Keep all annotations in the same math font as the paper. Numeric coordinate labels and Titan glyphs must remain visually and typographically distinct; the figure may show the operator-free seats `•   ⊙   ○`, but no operation between them.

---

*Canonical Path:* `01_EMERGENTISM/03_METHODOLOGY/02_THE_PAPERS/FINITY_PAPERS/PAPER_I_THE_TWO_FACES_OF_NUMBER.md`

•   ⊙   ○
