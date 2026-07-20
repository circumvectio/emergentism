---
receipt: 151
parents: [149, 150]
title: "Horn torus vs special relativity — formal audit under the P7 grave; the mouth computed; every SR reading refuted or capped at SHOWS"
date: 2026-07-20
status: "EXECUTED — fixes applied to D4_SPACETIME.md (Model section + torus caption) only; MF_69, SIMULATION_SPEC, TORUS_REVELATION flagged, not edited; /4/ and /discoveries/mass-shell/ caption fixes proposed, not applied"
auditors: "formalization packet (T1–T9, OB-1/OB-2) · numeric refuter (F1–F12) · adversary against-need/for-salvage (A1–A10) — verified fresh by this receipt (all computations recomputed, residuals ≤ 1e-15)"
sources:
  - 05_COSMOLOGY/00_THE_TORUS_REVELATION.md ([C] pre-hardening, read-only)
  - 10_SEED/01_THE_SEED_LADDER/D4_SPACETIME.md (edited: Model + emblem caption)
  - 12_PUBLIC_SITE/4/index.html (read-only; caption fix proposed)
  - 08_FRAMEWORK_SUPPORT/02_OPERATORS/SPHERE_DERIVATIONS/MF_69_Horned_Torus_Relativity.md (read-only, flagged)
  - 05_COSMOLOGY/01_THE_TRANSCENDENTAL_TRINITY/SIMULATION_SPEC.md (read-only, flagged)
binding: "P7 grave GOVERNS: 'the torus IS the light cone — it fell out of the topology' is DEAD; tombstone line 'the torus does not know about dimensional stages'; coincidence is not derivation. Receipt 149/150 standards: refit-discount for post-hoc fits; SHOWS-type claims uncitable in proof. The honest SR geometry is Minkowski's mass-shell hyperboloid + light cone [A inherited]."
---

# Receipt 151 — Horn Torus / SR Formal Audit (2026-07-20)

**Headline.** The audit set out to formalize the torus–SR mapping and instead
computed its refutation. The P7 tombstone was a ruling; it is now a theorem
package. **The torus moves DOWN, not from SHOWS toward ARGUES.** The only
claims that survive are the classical geometry of the horn torus itself, the
cylinder-inversion theorem (which points *away* from SR), and one `[S]`-capped
compactification reading whose price is the death of every current v→c
caption. No upgrade is licensed on any prong.

---

## 1 · The computed mouth-geometry result, stated plainly

Parametrize the horn torus (R = r) by `ρ = R(1 + cos u)`, `z = R sin u`, pinch
at `u = π`. Set `u = π + ε`:

```
ρ = R(1 − cos ε) = Rε²/2 + O(ε⁴),   z = −Rε + O(ε³)
⟹  ρ = z²/(2R) + O(z⁴)
```

**The mouth is a second-order cusp tangent to the rotation axis.** The exact
slope is `dρ/dz = −tan u → 0` at the pinch: the tangent cone at the pinch is
the **degenerate axis line** — opening angle zero. Minkowski's light cone has
a genuine 45° tangent cone at its apex (it is its own tangent cone). The two
singularities are **C¹-inequivalent**: no differentiable map carries one to
the other preserving tangent structure. The surface only passes through 45°
slope at `u = 3π/4`, i.e. `z = R/√2 ≈ 0.707R` — nowhere near the mouth (and
at the tube top `z = R` the tangent is *vertical*; the packet's "45° at
z = R" parenthetical applied the small-z expansion outside its validity —
corrected here, verdict unchanged).

**"The mouth is the light cone" is decidably false as differential
geometry.** It is not merely coincidence-not-derivation; at the pinch it is
not even a coincidence. Numeric confirmation: cusp ratio → 1.000025 at
ε = 0.01; all residuals ≤ 1e-15.

Two obstructions precede every mapping claim:

- **OB-1 (signature).** The embedded horn torus inherits a positive-definite
  Riemannian metric from Euclidean ℝ³. It has **no null directions at all**.
  SR is exactly the null-cone field of a Lorentzian metric. Any "light cone"
  drawn on the torus is paint, not geometry. This alone caps every T-claim at
  SHOWS. `[A]`
- **OB-2 (pinch equivocation).** The mapping asks one point to be
  simultaneously the light cone (T2), the worldline terminus (T3), and the
  v→c limit (T4/T7). The computation assigns it exactly one honest referent
  — the one-point conformal compactification of the worldlines' infinity —
  and refutes the other two. *Register correction (adversary A5):* in the
  projective compactification M# the strata `i⁺ = i⁻ = i⁰ = I` are
  identified at a single vertex; they are distinct only in the
  Einstein-cylinder cover. The tombstone line "the torus does not know about
  dimensional stages," made quantitative. `[A]`

---

## 2 · Verdict table

| Claim | Verdict | Tier after | Disposition |
|---|---|---|---|
| **T1** horn torus definition (R = r, pinch, genus ladder) | **CONFIRMED** | `[A]` | Classical geometry; the only unqualified `[A]` in the ladder. |
| **T2** mouth = light cone | **REFUTED** | dead | Cusp `ρ = z²/2R`; tangent cone = axis, not 45° cone; C¹-inequivalent (§1). **CORRECTED** internally: 45° crossing is at `z = R/√2` (`u = 3π/4`), not `z = R`. **CORRECTED** register: packet's "[I] at best" typing is itself wrong — a refuted proposition is not an interpretation; typed dead. |
| **T3** worldlines through the mouth | **REFUTED** as SR mapping | dead; `[S]`-cap survivor via SALV-1 | Under inversion the pinch is the image of the line at infinity — worldline *terminus*, not null cone; contradicts T2's reading (OB-2). Survives only as the single-referent compactification reading below. |
| **T4** hole closure = time dilation (`γ = cosh w` candidate) | **REFUTED** | dead above SHOWS | `C(β)/C(0) = 1 − β` linear vs Lorentz `√(1−β²)` concave (β = 0.9: 0.10 vs 0.436). Refit escape `β̃ := 1 − √(1−β²)` is an identity for any target — worth zero under 149/150. γ unbounded vs bounded compact ratios; divergent candidates (K_inner ~ (R−r)⁻¹ vs γ ~ (R−r)⁻¹ᐟ²) diverge at the wrong rate. Matches MF-69 §4.2.1 on file. **CORRECTED:** packet preamble "all computations fresh" overstated — the linear-vs-√ core is inherited from MF-69 §4.2.1, credited. |
| **T5** tube narrowing = length contraction | **REFUTED** | dead above SHOWS | Same computation, same verdict as T4. |
| **T6** rapidity as torus flow | **REFUTED** | dead | Triple no-go: (i) boost group ℝ non-compact vs poloidal S¹ compact — no continuous injection respecting additivity; (ii) π₁: torus-minus-pinch has π₁ = ℤ vs simply connected mass shell — no equivariant transport; (iii) 1+1 scope: 1-dim hyperbola vs 2-dim torus. Plus the conjugacy theorem under T8. |
| **T7** overlap = mass gain toward the limit | **REFUTED in direction** | dead | Self-intersection volume ≡ 0 for all r ≤ R (tangency only); positive only for r > R — *past* the claimed light-speed point. Torus quantity = 0 where γ = ∞; positive where SR is undefined. Inverted before any rate comparison. |
| **T8** cylinder inversion | **CONFIRMED (split)** | geometry `[A]` · SR bridge REFUTED | Inversion `x → k²x/|x|²` maps the cylinder ρ = c exactly onto the horn torus with `2R = k²/c` (residual 8.9e-16) — true classical theorem. The bridge dies twice: the inversion is *Euclidean*-conformal, not Lorentzian (different groups, and Euclidean ℝ³ has no null structure to preserve); and the conjugated flow `J∘T_a∘J` fixes exactly one point (the pinch) — **parabolic** Möbius class, with poloidal angle `u = 2 arctan(z/c)`. Boosts are **hyperbolic** (two fixed points). Distinct conjugacy classes; no conjugation carries one to the other. The transported parameter is Euclidean height = coordinate-time translation — additive in Galilean physics too; zero SR content; γ never appears. |
| **T9** SHOWS → ARGUES upgrade criterion | **INCOMPLETE in packet (truncated); stated in full §4 below** | — | The packet cut off mid-sentence at its load-bearing section. Receipt 151 supplies the bar. |
| **OB-1** signature obstruction | **CONFIRMED** | `[A]` | Decisive and prior to everything (§1). |
| **OB-2** pinch equivocation | **CONFIRMED + CORRECTED** | `[A]` | Corrected on the M#-vs-Einstein-cylinder strata point (§1); the kill stands either way. |
| **SALV-1** pinch = the compactification point at infinity | **CONFIRMED at cap** | `[S]` mechanism-match, never structure transport | Both closures are theorem-backed (Euclidean inversion closes the cylinder into the horn torus; Penrose closure sends timelike geodesics through the vertex I). The match is of *mechanism* in different conformal categories; upgrading it to one transported structure is exactly T8's equivocation. **Price: every v→c caption dies.** The pinch depicts *where worldlines end*, never *how fast they may go* — and even this is duplicated better by the Penrose diagram, which honestly draws the null structure the Riemannian torus cannot carry. |
| **Kill criterion (2) of TORUS_REVELATION** ("no predictions distinguishable from S² alone ⟹ discard") | **TRIGGERED — recorded, not executed** | K2 word | The antecedent is now computed-satisfied: every quantitative candidate fails or reduces to the hyperboloid already `[A]` on file; the honest additive rapidity lives on the mass shell with no torus needed. Disposal/demotion is founder-gated. FLAG-5. |
| **MF-69 abstract claims** ("No tuning… emerged from topology alone… encodes SR better than Minkowski diagrams") | **REFUTED / already contradicted by its own §4.2.1** | dead forms, unbannered | What emerged untuned is only the universal barrier-image any degenerating family shows; every measurable comparison diverges (linear vs √, log vs algebraic). "Convergence signature" (§4.1) is confirmation-structure over a falsified quantitative core. FLAG-1. |
| **TORUS_REVELATION interior/Observer/"D5 ⊥ D4 literally"** | **REFUTED as invariant geometry** | `[C]` stays, artifact noted | "Interior" and "center" belong to the rendering space ℝ³, not the surface; intrinsic geometry has no center. Embedding artifact. Doc is [C]-bannered pre-hardening; no edit (read-only lane). FLAG-4. |

---

## 3 · What died (this receipt)

1. **"The mouth is the light cone"** — dead as differential geometry. The
   mouth is a cusp of order 2 tangent to the axis; tangent cone = the axis
   line; opening angle → 0. Not C¹-equivalent to any cone. Survivor: none.
2. **"Self-intersection point" / "mass gain as the deepening overlap"** (the
   signed D4 emblem caption) — dead. The horn point is a tangency; overlap
   ≡ 0 for all r ≤ R and positive only beyond the claimed barrier. Survivor:
   the corrected caption applied to D4_SPACETIME.md.
3. **"Hole closure = time dilation" / "tube narrowing = length contraction"**
   as anything above SHOWS — dead. Linear vs square-root; refit-discount bars
   the reparametrization escape; no canonical parameter exhibited. Survivor:
   MF-69 §4.2.1's own honest verdict ("topological, not metric"), now
   load-bearing.
4. **Rapidity as a torus flow / boost subgroup on the torus** — dead as a
   theorem, not a failure-to-find: parabolic ≠ hyperbolic conjugacy classes;
   ℝ ↛ S¹; π₁ = ℤ vs simply connected. Survivor: rapidity as the mass
   shell's intrinsic arc length `[A]` (line added to the D4 Model card).
5. **"Emerged untuned from the topology alone" as convergence evidence** —
   dead. The untuned part is the universal singular-limit image (the corpus
   itself assigns the pinch seven different referents); wherever measurement
   is possible the forms diverge. Survivor: refit-discounted SHOWS emblem.
6. **The packet's own "[I] at best" typing of T2** — dead. Under 149/150 a
   decidably false proposition is not an interpretation. Refuted is refuted.
7. **The packet's "45° slope at z = R (top of the tube)" parenthetical** —
   corrected: |dρ/dz| = |tan u| = 1 at u = 3π/4, z = R/√2; the tube top has a
   vertical tangent. (Numeric error only; verdict unaffected.)

**What survived, at tier:** T1 `[A]` · T8's inversion geometry `[A]` (it
points away from SR: the conjugated flow is a Galilean-flavored time
translation) · OB-1/OB-2 `[A]` · SALV-1 `[S]`-capped single-referent reading
· the horn torus as SHOWS-only emblem (demoted in content: its one honest
showing is now "where worldlines end") · **Minkowski's mass-shell hyperboloid
+ light cone as the only citable SR geometry `[A]` inherited** — rapidity IS
its arc length (verified: arclength over w ∈ [0,3] = 3.0000000), γ = cosh w
its embedding coordinate, boosts its isometry flow, the light cone its
asymptotic cone at genuine 45°.

---

## 4 · The upgrade criterion (SHOWS → ARGUES), stated in full

The torus emblem may be upgraded only by an actual theorem, computed — never
by an image. All four prongs required:

1. **Canonical parameter, declared first.** A torus-intrinsic parameter
   (arc length in a named metric on the moduli family, a curvature
   functional, …) defined and justified *before* any comparison to a Lorentz
   target. Reparametrizations chosen after seeing the target are void
   (refit-discount, receipts 149/150).
2. **Exact identity.** A proven identity `Q(torus, canonical parameter) =`
   (some Lorentz quantity: `cosh w`, `√(1−β²)`, additive rapidity), exact —
   not asymptotic resemblance, not "same qualitative shape."
3. **Structure actually transported.** A single map carrying Lorentzian
   structure (null directions, causal order, or the boost action) to the
   torus. Known bars, each a theorem: OB-1 (no null directions on any
   embedded surface in Euclidean ℝ³); the parabolic-vs-hyperbolic conjugacy
   no-go (T8); ℝ-vs-S¹ and π₁ obstructions (T6). A successful candidate must
   evade all three — which currently requires either puncturing the pinch
   (surrendering the horn) or a non-faithful action (surrendering the
   physics).
4. **Single referent.** One declared dictionary in which the pinch has
   exactly one SR referent, the others explicitly renounced (OB-2).

Until all four are delivered, the torus is uncitable in any proof, and "if a
proof needs the torus, the proof is dead" remains the operative kill.

---

## 5 · Flags (K2-gated; none executed here)

- **FLAG-1 · MF_69** (`08_FRAMEWORK_SUPPORT/02_OPERATORS/SPHERE_DERIVATIONS/MF_69_Horned_Torus_Relativity.md`):
  the P7 tombstone at :262 banners only THE SENTENCE. Still live and
  quotable header-first: the **title** :22 "The Horned Torus IS the Light
  Cone" (the literal dead form as title); tier line :28 "[S] for relativistic
  correspondence"; abstract :35–43 ("No tuning was performed… emerged from
  the topology alone… encodes special relativity better than Minkowski
  diagrams" — internally contradicted by its own §4.2.1); §3.3 :161 "The
  horn torus IS the light cone, embedded in a larger story"; §4.1 :169–171
  convergence-as-proof. Standing P7 regression vector; banner extension
  needs K2.
- **FLAG-2 · SIMULATION_SPEC**
  (`05_COSMOLOGY/01_THE_TRANSCENDENTAL_TRINITY/SIMULATION_SPEC.md`): tombstone
  at :265 says "This passage," but :255 "The horn torus surface = the light
  cone (D4 causal structure)" sits ABOVE it unbannered, and ANIM-4.5 recurs
  below with no banner (:455 "Surface = light cone", :472 "the horn torus as
  the topology of compactified Minkowski space", :473 "Relativistic mass as
  geometric overlap", :478 "the torus surface = … the light cone itself").
  Note: :472 has a true kernel nearby — the conformal compactification of
  1+1 Minkowski *is* topologically a torus — but that is the flat conformal
  torus, not the ℝ³-embedded horn torus, and the pinch identification is
  OB-2. Banner extension needs K2.
- **FLAG-3 · Proposed caption fixes (public site — NOT applied):**
  - `12_PUBLIC_SITE/4/index.html` :85 — canvas `aria-label` reads "Animated
    rapidity sweep: reciprocal light-cone coordinates diverging toward the
    light-cone asymptote" while `animationMode: "horn"` (:224). If
    `../dimensions/dimensions.js` renders the horn torus under that mode,
    assistive-tech users are told the horn animation IS a light-cone chart.
    Proposed label: "Animated emblem: horn-torus rendering accompanying the
    mass-shell chart — an emblem of the geometry, not the light cone."
    Verify the dimensions.js mode binding before editing.
  - `12_PUBLIC_SITE/discoveries/mass-shell/index.html` :215 — already
    grave-consistent ("The horn-torus rendering is an emblem of this
    geometry, not its derivation"). Optional tightening only: append "(its
    mouth is a cusp, not the light cone — receipt 151)". Low priority.
- **FLAG-4 · TORUS_REVELATION** (`05_COSMOLOGY/00_THE_TORUS_REVELATION.md`):
  [C]-bannered pre-hardening, but still sitting in active `05_COSMOLOGY/`
  with "the torus is not an analogy… the ring is real" (:211, :231) and the
  Observer-at-the-center interior reading now shown to be an ℝ³ embedding
  artifact with no invariant existence. Live habitat for P7 relapse; K3
  archive-first disposition is founder's.
- **FLAG-5 · Kill criterion (2) self-triggered:** TORUS_REVELATION :24 —
  "if the torus parameterization does NOT produce predictions distinguishable
  from S² alone, the torus adds no value and should be discarded." The
  antecedent is now computed-satisfied (this receipt). Discard/demote is a
  K2 word; recorded here, not taken.

---

## 6 · Fixes applied (this receipt, D4_SPACETIME.md only)

1. **Model card (hyperboloid):** added the `[A]` line that rapidity is the
   shell's intrinsic Minkowski arc length, γ its embedding coordinate, boosts
   its isometry flow, the light cone its asymptotic 45° cone — and that no
   embedded Riemannian surface can carry these (OB-1), cross-ref receipt 151.
2. **Emblem caption (horn torus):** "self-intersection" → tangency;
   "mass gain as the deepening overlap" and "image of v → c" retired with the
   computed reasons inline; the `[S]`-capped SALV-1 reading installed as the
   emblem's one honest showing (*where worldlines end*, never *how fast they
   may go*); the full upgrade bar cited; SHOWS-only typing and the P7 grave
   retained verbatim.

*Seam ≠ score ≠ node. The shell is Einstein's; the cusp is the torus's own;
the emblem shows the end of worldlines, and nothing else.* ⊙ = • × ○
