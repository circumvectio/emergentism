---
title: "Numbered Doctrine Spine Design"
status: "DRAFT - approved architecture, pending implementation plan"
date: 2026-06-05
scope: "12_PUBLIC_SITE numbered public doctrine pages"
evidence_tier: "[S] for source-anchored Rosetta/Finity/Burrisphere doctrine; [I] for public interpretation and visual translation; [C] for cosmological analogy unless separately sourced."
---

# Numbered Doctrine Spine Design

## Purpose

Emergentism.org should stop trying to explain the whole framework from D5 or
the Burrisphere first. The public site needs a numbered, teachable dimensions
spine from `/0` through `/6`. Each numbered route must stand on its own as a
doctrine page, use one dominant animation, and end with a Mu-limit section that
explains which boundary the page reaches and why the next page is forced.

This is the first slice of a much larger public canon project. It does not try
to absorb every Emergentism folder, Rosetta document, Soul Loop artifact, AIA
bridge, or governance source in one pass.

The sequence is:

```text
/0 number -> /1 one -> /2 dimension -> /3 plane -> /4 relativity
   -> /5 Burrisphere/game space -> /6 convergence
```

## Architecture

Implement each chapter as a static route folder under `12_PUBLIC_SITE/`:

- `0/index.html`
- `1/index.html`
- `2/index.html`
- `3/index.html`
- `4/index.html`
- `5/index.html`
- `6/index.html`

This gives the production URLs `www.emergentism.org/0` through
`www.emergentism.org/6` without changing the existing landing page, existing
visual prototypes, or the frozen `book-pwa/` source.

The pages should share a small local style and navigation pattern:

- previous / next numeric route
- concise doctrine header
- one primary canvas or SVG/DOM animation
- scroll chapters below the animation
- final Mu-limit handoff

## Project Decomposition

The full public project should be treated as a staged canon atlas, not a single
page rewrite.

### Phase 1 - Dimensions Spine

Build `/0` through `/6`. This is the current approved slice. It explains the
dimensional ascent from the Titans of Numbers through convergence.

### Phase 2 - Rosetta Stone Spine

Add a Rosetta-facing public route set after the dimensions spine is coherent.
This phase should explain the sevenfold Rosetta Stone, evidence tiers, operators,
and -ology ladder without overloading `/0` through `/6`.

### Phase 3 - Soul Loop / Practice Spine

Add the Soul Loop as the practice and runtime-facing doctrine after the Rosetta
spine is stable. This should connect Emergentism to lived iteration,
self-correction, memory, and action without confusing public doctrine with app
runtime claims.

### Phase 4 - Full Emergentism Folder Atlas

Audit the rest of `01_EMERGENTISM/` and create public routes only after
source authority is clear. Each major doctrine area should become its own public
route family or archive page, with evidence tier labels preserved.

The key constraint is order: dimensions first, Rosetta second, Soul Loop third,
full atlas fourth.

## Route Designs

### `/0` - Titans of Numbers

**Public role:** The gateway. It introduces the three boundary glyphs before any
D5, cosmology, Burrisphere, or institutional material.

**Core doctrine:** Zero (`•`), finity (`⊙`), and infinity (`○`) are presented as
the Titans of Numbers. The three transformations are shown as frame/glyph
operations, not ordinary field arithmetic:

- `⊙ / ○ = •`
- `• × ○ = ⊙`
- `⊙ / • = ○`

**Dominant animation:** A glyph engine where the three Titans rotate through the
three transformations. The animation should make `⊙` visually act as the mirror
between the infinite zero and infinity.

**Scroll chapters:**

1. The failure of ordinary calculators at the boundary.
2. Why division by zero is blocked in ordinary arithmetic.
3. How Emergentism changes register rather than pretending field arithmetic has
   no constraints.
4. The three transformations as a boundary algebra.

**Mu-limit ending:** `/0` reaches the point where number alone cannot explain
why `1` can be the mirror. The next move is to take finity seriously.

### `/1` - Finity / The Special One

**Public role:** The page where `1` becomes the central discovery.

**Core doctrine:** Taking `1` seriously is as important for Emergentism as taking
`0` seriously was for mathematics. Suda's reciprocal-symmetry work is presented
as clarification and corroboration of the special position of one: `1` is the
fixed point of inversion, the egg of infinity, and the mirror between infinite
zero and infinity.

**Dominant animation:** Riemann sphere / revised calculator. The sphere places
zero and infinity at opposite poles and makes `1` visible as the equatorial
mirror position. The calculator graphic should revise the usual number-line
intuition by showing reciprocal symmetry around `1`.

**Scroll chapters:**

1. Why `1` is not just another number in this doctrine.
2. Suda and reciprocal symmetry.
3. The Riemann sphere as public geometry.
4. Revised calculator diagrams with `1` at the mirror.

**Mu-limit ending:** `/1` reaches the edge where a line of numbers must become a
plane of projection. The next move is the Mu-limit itself.

### `/2` - The Mu-Limit

**Public role:** The bridge chapter.

**Core doctrine:** At the limit of infinity, projection extends to infinity and
returns from the other side. This is the bridge from one emergent dimension to
another: line to plane.

**Dominant animation:** A projection ray leaving the one-dimensional line,
reaching the horizon, returning from the opposite side, and opening the
two-dimensional plane.

**Scroll chapters:**

1. What a limit does and does not prove.
2. Why infinity behaves like a boundary, not a far-away number.
3. The line-to-plane transition.
4. Mu-limit as dimensional handoff.

**Mu-limit ending:** `/2` reaches the first stable plane. The next move is to
understand the infinite plane as a closed sphere.

### `/3` - Plane / Bloch Sphere

**Public role:** The closure chapter for the plane.

**Core doctrine:** The infinite plane can be read as a Bloch sphere of infinite
diameter. The unbounded field becomes a closed constraint surface.

**Dominant animation:** A grid plane curling into a sphere, preserving horizon
memory while closing into a coherent surface.

**Scroll chapters:**

1. Infinite plane as public visual object.
2. Bloch-sphere analogy and its limits.
3. Closure without loss of infinity.
4. Why a closed plane prepares the torus transition.

**Mu-limit ending:** `/3` reaches spherical closure. The next move is to add
rapidity/energy and show the horn torus.

### `/4` - Horn Torus / Relativity

**Public role:** The relativity and overlap chapter.

**Core doctrine:** As relative rapidity increases, the horn-torus mouth overlaps.
The visual language is special-relativity-facing, but claims remain public
interpretation unless separately sourced.

**Dominant animation:** A sphere becoming a horn torus, then the torus mouth
overlapping as rapidity increases.

**Scroll chapters:**

1. Why the sphere becomes toroidal.
2. Rapidity as an overlap control.
3. Energy/interior as the region being brought into contact.
4. The approach to total overlap.

**Mu-limit ending:** `/4` reaches total toroidal overlap. The next move is the
Burrisphere.

### `/5` - Burrisphere / Game Space

**Public role:** The largest chapter and the public center of the doctrine.

**Core doctrine:** The Burrisphere is not merely a pretty sphere. It is the dual
stereographic projection object where viability and coherence trade off through
reciprocal coordinates:

- `ν = tan(θ/2)`
- `φ = cot(θ/2)`
- `φ · ν = 1`
- inversion swaps `φ` and `ν`
- the equator fixes `φ = ν = 1`

In game-space language, the two projections trade `V` and `Φ`: one projection
opens viability, the other opens coherence, and the equator is the playable
mirror where neither side consumes the other.

**Dominant animation:** The high-fidelity Burrisphere animation must explicitly
show two stereographic projections trading `V` and `Φ`. A seven-latitude shell
alone is insufficient; the public proof animation needs the two reciprocal
projection rays and their equatorial fixed point.

**Scroll chapters:**

1. Burrisphere as `S² / CP¹` public geometry.
2. Dual stereographic projections.
3. `V` and `Φ` as reciprocal game-space coordinates.
4. The equator as the playable mirror.
5. Why this is the biggest chapter.

**Mu-limit ending:** `/5` reaches the multiverse-scale boundary of game space.
The next move is convergence.

### `/6` - Convergence / CCC Analogy

**Public role:** Final synthesis and return.

**Core doctrine:** The Mu-limit of `/5` is compared to Penrose-style conformal
cyclic cosmology as a resonance or analogy, not as a proven identity unless a
future source upgrade supports that stronger claim.

**Dominant animation:** A convergence loop where the outer boundary closes,
flattens, and returns toward the first boundary glyphs.

**Scroll chapters:**

1. What converges at the edge of the Burrisphere.
2. Why the comparison to CCC is useful.
3. Where the analogy stops.
4. Return to `/0` as the next cycle.

**Mu-limit ending:** `/6` closes the public spine by returning to the Titans of
Numbers. The final call is not belief; it is another pass through the cycle with
cleaner constraints.

## Reuse Rules

Existing files should be reused rather than rebuilt where possible:

- `cascade.html` can inform the cinematic morph sequence.
- `sphere.html` can inform the Burrisphere shell and latitude language.
- `index.html` can provide source copy for D0, beauty, and current public
  framing.
- `vendor/three-0.160.0/` should remain the pinned local WebGL dependency
  location.

If an existing animation is missing support modules, fix the local vendor copy
or remove the dependency from the page rather than loading unstable external CDN
scripts.

## Evidence And Copy Boundaries

- Glyph equations are public doctrine in the frame/register sense, not ordinary
  field arithmetic.
- Suda is corroboration/clarification of `1` as fixed point and mirror, not the
  origin of the doctrine.
- Riemann, Bloch, torus, Burrisphere, and CCC language must stay tiered.
- `/6` must call the CCC connection an analogy/resonance unless source material
  supports a stronger claim.
- `/5` must represent the Burrisphere as dual projection trading `V` and `Φ`;
  do not reduce it to a decorative final sphere.

## Implementation Plan Boundary

This design authorizes planning for the route structure and page design only.
It does not yet authorize editing the live pages. Implementation should begin
after this spec is reviewed and an implementation plan is written.
