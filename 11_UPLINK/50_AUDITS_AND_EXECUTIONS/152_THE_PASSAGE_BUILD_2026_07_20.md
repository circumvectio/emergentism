---
receipt: 152
parents: [149, 150, 151]
title: "The Passage build — √2 spindle verified, double-cover computed, animation-truth synced, canon rumination filed, The Crossing shipped to the public funnel (no deploy)"
date: 2026-07-20
status: "EXECUTED — canon rumination written; flagship page + two gallery cards built; three discovery pages caption-synced; regression pass run and count-drift fixed; NO DEPLOY; D4_SPACETIME.md and all 15x receipts untouched"
auditors: "Phase-1 verifier (√2 spindle, exact + numeric) · degeneration-family computation (sympy exact, residuals ≤ 1e-8) · site build agent · caption-sync agent · regression verifier (this receipt)"
sources:
  - 11_UPLINK/50_AUDITS_AND_EXECUTIONS/151_HORN_TORUS_SR_FORMAL_AUDIT_2026_07_20.md (governing verdicts; read-only)
  - 06_ONTOLOGY/ruminations/00_RUMINATION_ON_THE_TORUS_SPHERE_PASSAGE_2026_07_20.md (NEW — canon rumination, Kintsugi seam)
  - 12_PUBLIC_SITE/discoveries/the-crossing/index.html (NEW — flagship page)
  - 12_PUBLIC_SITE/index.html · 12_PUBLIC_SITE/discoveries/index.html (EDITED — featured card + eleven-count)
  - 12_PUBLIC_SITE/discoveries/mass-shell/index.html · game/index.html · nonduality/index.html (EDITED — caption sync)
binding: "Receipt 151 GOVERNS: horn mouth = parabolic cusp ρ = z²/2R, tangent cone = axis line, OB-1 signature obstruction, upgrade bar §4, refit-discount per 149/150. P7 grave: the torus derives nothing; 'the torus does not know about dimensional stages.' NEVER 'D5 derived from SR' — the image shows the ladder, it does not push it. μ-at-saturation stays [C]. Beauty = L2 invitation, never verdict. Seam ≠ score ≠ node."
---

# Receipt 152 — The Passage Build (2026-07-20)

**Headline.** The spindle result is complementary to, not a repair of, the
horn refutation. Receipt 151 killed "the mouth is the light cone" (cusp,
tangent cone = axis, OB-1). This receipt records what was then computed
honestly on the same family — the √2 spindle's genuine 45° cone points, the
doubly covered sphere limit, the closing curvature ledger — and how it was
carried into canon (one rumination, at tier) and into the public funnel (one
flagship page, two gallery cards, three caption syncs), with every fence
printed on the surface it rides. Nothing here contradicts 151; nothing here
upgrades any SR reading above SHOWS; nothing was deployed.

---

## 1 · The verified math (Phase-1, CANDIDATE → confirmed)

Family `X(u,v) = ((R + r cos u) cos v, (R + r cos u) sin v, r sin u)`, tube
radius `r` fixed, ring radius `R ∈ [0, r]`. All results verified fresh
(sympy exact + numeric residuals ≤ 1e-8; the √2 slope residual 1.1e-16).

### 1a · The √2 spindle verdict `[A]` (Euclidean geometry only)

- Axis crossings exist iff `R ≤ r`, at `z* = ±√(r² − R²)`; crossing slope
  `|dρ/dz| = √(r² − R²)/R`.
- **`|dρ/dz| = 1` (exactly 45°) ⟺ `2R² = r²` ⟺ `R = r/√2`**, and there
  `z* = ±r/√2`. (`z* = R` is an algebraic restatement of the same
  condition, not an independent fact.)
- Each crossing is a **C¹-genuine cone point**: tangent cone = the exact 45°
  quadric double cone `x² + y² = (z − z*)²`, both nappes, verified
  transversal. This is precisely what receipt 151 proved the horn mouth is
  NOT — the spindle family answers T2's differential-geometry objection; it
  does not touch OB-1.
- Intrinsic invariant: apex total angle `2π sin 45° = √2·π`; deficit
  `(2 − √2)π`. That is all the surface itself carries there.
- **Fences:** the tangent cone's set-congruence with the null cone of a
  spacetime diagram is `[S]` as point-set geometry; the words "null slope"
  are `[I]` — a reading. OB-1 stands: positive-definite metric, no null
  directions, no signature (1,1), no boost, no conformal `[S]` rescue (the
  conformal class of a Riemannian metric contains no Lorentzian metric).
  "Spindle cone point = light cone" would repeat T2's category error one
  rung up and **must not be written**.
- **The √2 station is chosen-by-target, not canonical-in-family:** the slope
  `s(t) = t/√(1−t²)` is a strictly monotone bijection of `t = R/r ∈ (0,1)`
  onto `(0,∞)` — every opening angle occurs exactly once; 45° is selected by
  the SR target. As evidence it is worth zero (149/150 refit-discount);
  citable only with the discount stated. No functional of the family is
  extremized at `t = 1/√2`.

### 1b · The degeneration verdict `[A]` (fix r, shrink R → 0)

- **Stations:** `R > r` ring · `R = r` horn (one pinch, parabolic cusp
  `ρ = z²/2R + O(z⁴)`, tangent cone = axis — 151 reconfirmed independently)
  · `0 < R < r` spindle (two cone points, at **every** spindle station, not
  only √2) · `R = 0` **sphere of radius r covered exactly twice**.
- **Double cover:** deck involution `σ: (u,v) ↦ (π−u, v+π)` with
  `X(u,v) = X(σ(u,v))` identically; fixed-point-free on the parameter torus;
  fails to immerse only on the two collapse circles `u = ±π/2`, each
  collapsing to a pole `(0,0,±r)`.
- **Pinch trajectory:** the singular points trace `R² + z² = r²` — the horn's
  single pinch at the origin splits into the spindle pair, slides along the
  quarter-circle, and lands on the poles at `R = 0`, where each cone opens
  flat (θ → π/2) and **evaporates into a smooth point**. As `R → r` the cone
  closes (θ → 0) into the horn's degenerate cusp — consistent with 151 at
  both ends.
- **Curvature ledger:** smooth-part total
  `∬K dA = 8π√(r² − R²)/r`; cone-point deficit `2π(1 − √(r² − R²)/r)` each.
  Horn: smooth total 0 (immersed-torus value; all curvature hidden in the
  pinch). Sphere limit: **8π = 2 × 4π** — Gauss–Bonnet for the sphere
  counted twice, ledger closed, nothing left concentrated.
- **Tier:** all of the above `[A]` classical Euclidean geometry, verified;
  it derives nothing beyond itself (P7 grave).

### 1c · The animation-truth verdict (/4/ code, read not edited)

The `/4/` animation computes **real hyperbolic functions of one rapidity
slider first and pushes them into the torus family** — SR → torus, never
torus → SR. It renders the horn only at `w = 0`; for every `w > 0` it is
already a spindle; the sphere is a limit approached, never occupied (no rest
frame at c — and this fits μ-grammar as resonance only). No φ/ν reciprocal
coordinates and no light cone are drawn. Grave-compliant in code; one false
`aria-label` remains (FLAG-1 below).

### 1d · Standing tiers, restated

- μ-at-saturation: `[C]`, unmoved and unmovable by any of this geometry.
- The passage reading (V-model saturates → Φ-model emerges): `[I]` emblem
  riding `[A]` geometry; SHOWS-type; uncitable in proof.
- Double-cover ↔ two-charts: `[I]` resonance, one datum, refit-discounted,
  no computed structure-map.
- **NEVER "D5 derived from SR."** The image shows the ladder; it does not
  push it.

---

## 2 · The canon doc

`06_ONTOLOGY/ruminations/00_RUMINATION_ON_THE_TORUS_SPHERE_PASSAGE_2026_07_20.md`
— WRITTEN. Kintsugi seam citing 149/150/151 (the crack: "the horn torus IS
the light cone," dead and staying dead; the gold: the honestly computed
family, refit-discounted). Register `[I]`-riding-`[A]`, SHOWS-type,
K2-aware / not signed. Companion links to receipt 151, D4_SPACETIME.md
(read-only), and the /4/ animation. Verified present on disk this receipt.

## 3 · The site build (NO DEPLOY)

| File | Act |
|---|---|
| `12_PUBLIC_SITE/discoveries/the-crossing/index.html` | **NEW flagship.** Three stations (horn honestly captioned per 151 — cusp, not the light cone, graveyard-dated; √2 spindle at verified tier with the null-slope reading explicitly priced and the refit-discount printed; doubled sphere with the 4π→8π ledger and the two-charts line held as resonance). Red fence panel: **"The torus derives nothing"** / never derived-from-relativity. Links to `/4/` (with code-truth caption) and `/sphere.html`. Tier chips `[A]`/`[I]`/`[C]`; strength-line → `/record/`; CTAs to `/practice/` + `/build/` only; exit line in footer; og meta with absolute prod URLs. |
| `12_PUBLIC_SITE/discoveries/index.html` | Featured full-width card `11 · the-crossing · featured` atop the gallery; `.card.featured` CSS; ten existing cards untouched, not renumbered. Count copy updated ten → **eleven** (title, meta, og, hero, footer — this receipt's regression fix). |
| `12_PUBLIC_SITE/index.html` | Same featured card + CSS atop the home gallery. Count copy updated ten → **eleven** (meta, og, fileno, dek, gallery h2, "All eleven as one gallery" CTA, footer — this receipt's regression fix). |
| `12_PUBLIC_SITE/discoveries/mass-shell/index.html` | Caption sync: false "mass shell in reciprocal coordinates" removed; animation-truth caption installed (SR pushed in, never read out); passage paragraph linking the-crossing at `[I]`. |
| `12_PUBLIC_SITE/discoveries/game/index.html` | Arrival line: family closes toward a sphere, "a limit approached, never occupied," image-only `[I]`, links the-crossing. |
| `12_PUBLIC_SITE/discoveries/nonduality/index.html` | Double-cover one-liner: limit sphere "arrives twice-covered — two charts laid over one ground" `[I]`, resonance-not-proof, links the-crossing. |

## 4 · Regression pass (this receipt)

- **Links:** every internal target of the-crossing and the edited pages
  resolves on disk (mass-shell, burrisphere, /4/, sphere.html, record,
  axioms, practice, build, exit, fable, plainly, book, fonts, manifest,
  pwa.js, atlas-drawer.js, apple-touch-icon, og-card.png — all OK). The
  three `/discoveries/the-crossing/` links from mass-shell/game/nonduality
  now resolve (the page exists; the earlier 404 flag is closed).
- **og meta:** present on the-crossing with absolute prod URLs
  (`https://emergentism.org/discoveries/the-crossing/`, og-card.png).
- **Tier chips:** intact on the-crossing (`[A]`/`[I]`/`[C]`), both featured
  cards, and all three caption-sync insertions (`[I]`).
- **Tier discipline:** no claim exceeds Phase-1 verified tiers. The 45°
  language is bounded ("as a point-set… That much is a theorem. The words
  'null slope' are a reading"); the refit-discount is printed on the page
  ("worth zero… cited only with that discount stated"); approached-never-
  occupied appears on the-crossing, mass-shell, and game; μ-at-saturation
  held as wager (`[C]`) on the-crossing.
- **The fence:** the red fence panel with **"The torus derives nothing"**
  and "never 'the higher game derived from relativity'" is visible on
  the-crossing; no "D5 derived from SR" anywhere in the built surfaces.
- **No forbidden edits:** `git status` clean on `10_SEED/01_THE_SEED_LADDER/
  D4_SPACETIME.md` and every 15x receipt — untouched, as bound.
- **Fixed in place (this receipt):** count drift ten → eleven, 11 spots
  across `index.html` + `discoveries/index.html` (the featured card made the
  gallery 11 cards while all copy still said ten).
- **Render check (local preview :8931):** home gallery shows "Eleven
  claims…" with the featured card first-of-11 and chips rendering;
  the-crossing renders full content, station labels correct (`R = r`
  lowercase preserved), **zero console errors**. NO DEPLOY.

## 5 · Flags (carried, not executed)

- **FLAG-1 · `/4/index.html` :85 aria-label still false** — reads "Animated
  rapidity sweep: reciprocal light-cone coordinates diverging toward the
  light-cone asymptote" while the code renders the horn/spindle family
  (151's FLAG-3). The code-truth pass verified the mode binding, so 151's
  proposed replacement label is safe to apply; still unapplied because /4/
  sits outside this build's edit lane.
- **FLAG-2 · dimensions.js "Burrisphere" comment** and the **no-"horn"-
  caption-for-w>0 rule** — carried from the canon pass; unexecuted.
- **FLAG-3 · Phase-1 register:** the √2 cone points should move
  CANDIDATE → VERIFIED-`[A]`-geometry in the Phase-1 register (verifying
  algebra: `|dρ/dz| = √(r²−R²)/R = 1 ⟺ R = r/√2`).
- **FLAG-4 · 151's K2-gated flags remain open** (MF_69 banner extension,
  SIMULATION_SPEC banner extension, TORUS_REVELATION disposition, kill-
  criterion (2) execution) — founder-gated; recorded, not taken.
- **FLAG-5 · Deploy is a host act.** Everything above is local; the public
  funnel changes ship only on a K2-signed deploy.

*Seam ≠ score ≠ node. The geometry is the family's own; the crossing is an
emblem riding it; the ladder is shown, never pushed.* ⊙ = • × ○
