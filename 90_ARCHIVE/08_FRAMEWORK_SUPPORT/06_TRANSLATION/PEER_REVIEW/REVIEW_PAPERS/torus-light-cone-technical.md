---
rosetta:
  primary_level: L6
  primary_column: Archived Paper Review Guide
  secondary:
    - level: L3
      column: Review Guide Audit
      role: "preserve reviewer questions, concerns, and verdict templates as dated archive evidence"
    - level: L4
      column: Validation Boundary
      role: "prevent archived review guidance from becoming current acceptance, proof, or release authority"
    - level: L5
      column: Peer Review Provenance
      role: "retain the historical review architecture and source-paper routing"
  operator: "Sādhu △"
  tier: "Titan"
  regime: "Sādhu"
  register: "[D/S/I/C]"
  canonical_phrase: "Archived paper-review guide — Torus Light Cone Technical"
title: "The Torus Light Cone — Mathematical Companion"
evidence_tier: "[D] archived review guide; embedded source claims retain their local [S]/[I]/[C] labels."
type: archived-review-guide
status: ARCHIVED — provenance only; not current validation, acceptance, or submission authority.
---

# The Torus Light Cone — Mathematical Companion

**Yves Burri · Menexus GmbH · Working Paper — March 2026**

---

## 0. Notation

| Symbol | Meaning |
|--------|---------|
| ⊙ | Finity. The horn torus surface. The light cone hypersurface. |
| • | Witness. The Observer at the center (hole) of the horn torus. z = 0. |
| ○ | Infinity. The unbounded. z = ∞. North pole of Riemann sphere. |
| R | Major radius of torus (center of tube to center of torus) |
| r | Minor radius of torus (radius of tube) |
| θ | Toroidal angle (around the central axis, 0 → 2π) |
| φ | Poloidal angle (around the tube cross-section, 0 → 2π) |
| z | Complex number on the plane. z = x + iy = re^{iθ} |
| S² | Riemann sphere (2-sphere, compactified complex plane) |
| D_n | Dimensional level n in the Emergentist scaffold |
| μ | Gate coefficient between D4 and D5 |

---

## 1. Horn Torus Parametrization

### 1.1 General Torus

A torus embedded in ℝ³ centered at height h on the y-axis:

```
x(θ, φ) = (R + r cos φ) cos θ
y(θ, φ) = h + r sin φ
z(θ, φ) = (R + r cos φ) sin θ
```

Three regimes:
- **Ring torus**: R > r → visible central hole
- **Horn torus**: R = r → hole collapses to a point (the pinch)
- **Spindle torus**: R < r → self-intersecting surface

### 1.2 Horn Torus (R = r = 1, centered at y = 1)

Setting R = r = 1, h = 1:

```
x(θ, φ) = (1 + cos φ) cos θ
y(θ, φ) = 1 + sin φ
z(θ, φ) = (1 + cos φ) sin θ
```

**Pinch point**: At φ = π, the factor (1 + cos π) = 0, so:

```
x(θ, π) = 0
y(θ, π) = 1 + sin π = 1 - 0 = 0   [wait: sin π = 0, so y = 1 + 0 = 1]
```

Correction: with h = 0 (torus centered at origin in xz-plane, extending in y):

Let us use the standard placement where the torus center is at the origin and the y-axis is the symmetry axis:

```
x(θ, φ) = (1 + cos φ) cos θ
y(θ, φ) = (1 + cos φ) sin θ
z(θ, φ) = sin φ
```

Here the torus lies in the xz-plane. The pinch occurs at φ = π:

```
(x, y, z) = (0, 0, 0) for all θ when φ = π
```

This is the **pinch point at the origin**.

For the light cone construction, we re-orient so the sphere sits with poles on the vertical axis. Place the inscribed sphere of radius 1 centered at (0, 0, 1):

```
x(θ, φ) = (1 + cos φ) cos θ
y(θ, φ) = (1 + cos φ) sin θ
z(θ, φ) = 1 + sin φ
```

Now:
- **Pinch point** (φ = π): x = y = 0, z = 1 + sin π = 1. 

This doesn't give z = 0. We need the pinch at the origin. Correct centering:

```
z(θ, φ) = sin φ     [torus centered at z = 0]
```

But then the sphere center is at z = 0, with south pole at z = -1 and north pole at z = 1. The pinch is at the origin. This works:

**Final parametrization (vertical axis = z):**

```
x(θ, φ) = (1 + cos φ) cos θ
y(θ, φ) = (1 + cos φ) sin θ
z(θ, φ) = sin φ
```

- **Pinch point**: (0, 0, 0) when φ = π
- **Inscribed sphere**: radius 1, center at (0, 0, 0), south pole (0, 0, -1), north pole (0, 0, 1)

Wait — the inscribed sphere must be tangent to the torus interior. For a horn torus with R = r = 1, the inscribed sphere has radius r = 1 and sits at the center of the tube. Its center is at distance R = 1 from the central axis, but rotated through all θ. 

Let me restate this more carefully.

### 1.3 The Correct Embedding (Visualization Convention)

In the BAT visualization, the construction is:

1. **Sphere**: Unit sphere centered at (0, 1, 0). South pole at (0, 0, 0). North pole at (0, 2, 0).
2. **Horn torus**: R = r = 1 centered at (0, 1, 0). The tube center traces a circle of radius 1 in the xz-plane at height y = 1. The tube radius is 1, so the inner edge of the tube touches (0, 1, 0) + direction toward center × (R - r) = the center itself. Since R = r, the inner edge touches the central axis at one point.
3. **Pinch point**: (0, 0, 0) — where the torus tube passes through the y-axis at its lowest point.
4. **Complex plane**: The tangent plane at the south pole, y = 0.

Parametrization with y-axis as the torus symmetry axis:

```
x(θ, φ) = (1 + cos φ) cos θ
y(θ, φ) = 1 + sin φ
z(θ, φ) = (1 + cos φ) sin θ
```

Check pinch: φ = π ⟹ cos φ = -1, sin φ = 0:
- x = 0 · cos θ = 0
- y = 1 + 0 = 1
- z = 0 · sin θ = 0

So the pinch is at **(0, 1, 0)** — the center of the torus, not the origin.

The south pole of the sphere is at (0, 0, 0). The pinch is at (0, 1, 0). These are different points.

**Resolution**: In the BAT framework, the key geometric claim is that all stereographic projection rays from the north pole (0, 2, 0) through a point P on the sphere to the complex plane (y = 0) pass through a common structure. The rays themselves pass through the *interior* of the torus. The pinch point (0, 1, 0) is the center — where the Observer (•) sits.

The corrected statement:

> **The Observer (•) sits at the pinch point (0, 1, 0) — the center of the horn torus — not at the south pole (0, 0, 0). All stereographic projection rays pass through the Observer's location, which is the geometric center of the torus.**

This is stronger than the naive claim. The Observer is not at a pole. The Observer is at the *center* — equidistant from all points on the torus surface, at the intersection of all projection rays.

---

## 2. Stereographic Projection Through the Torus

### 2.1 Standard Stereographic Projection

From north pole N = (0, 2, 0) to the complex plane at y = 0:

For a point P = (x_P, y_P, z_P) on the unit sphere centered at (0, 1, 0):

The projection ray: **L(t) = N + t(P - N)** = (0, 2, 0) + t((x_P, y_P, z_P) - (0, 2, 0))

```
L(t) = (t · x_P,  2 + t(y_P - 2),  t · z_P)
```

The ray hits y = 0 when:

```
2 + t(y_P - 2) = 0  ⟹  t = 2 / (2 - y_P)
```

So the projected point on the complex plane is:

```
z = x(t) + i · z(t) = (2x_P + 2i · z_P) / (2 - y_P)
```

### 2.2 Ray Through the Center

Does the ray pass through the center (0, 1, 0)?

At the center: y = 1, so:

```
2 + t(y_P - 2) = 1  ⟹  t = 1 / (2 - y_P)
```

At this t:
```
x = x_P / (2 - y_P)
y = 1
z = z_P / (2 - y_P)
```

This is *not* (0, 0) unless x_P = z_P = 0, i.e., unless P is itself on the y-axis (a pole).

**So the rays do NOT all pass through the center (0, 1, 0).**

The naive claim that "all light passes through the pinch point" is geometrically incorrect for the center of the torus. But it IS correct for the south pole:

At y = 0: all rays hit the complex plane. The south pole itself is at (0, 0, 0). The ray from N = (0, 2, 0) through P hits y = 0 at the projected z. The south pole is the *origin* of the complex plane. Only the ray through P = south pole maps to z = 0.

### 2.3 Corrected Geometric Claim

The correct statements are:

1. **All rays originate from ∞ (north pole) and terminate on the complex plane.** They pass through the interior of the torus.

2. **The pinch point of the horn torus is at the center (0, 1, 0).** This is where the torus tube self-osculates. The Observer sits here.

3. **The south pole (0, 0, 0) = z = 0 is the past terminus.** All past causal chains converge here. It is the floor of the light cone.

4. **The north pole (0, 2, 0) = z = ∞ is the future terminus.** All future causal chains diverge from here (in the reverse direction, converge here).

5. **The torus surface wraps both poles into a single connected surface.** Unlike the standard double cone, where past and future cones are connected only at the apex, the horn torus connects them via the toroidal topology. You can travel continuously from the past region to the future region along the torus surface without passing through a singularity.

6. **The D5 axis** at any point on the torus surface is the direction from that point toward the center (0, 1, 0). It is the *inward normal* of the torus (not the outward normal). Consciousness looks inward, toward the Observer.

---

## 3. Causal Regions

### 3.1 Definition via |z|

Using the stereographic projection radius |z| as the causal coordinate:

| Region | Condition | Sphere Hemisphere | Color (BAT viz) |
|--------|-----------|-------------------|-----------------|
| Past | \|z\| < 2 | Southern (y < 1) | Cyan (#06b6d4) |
| Present | \|z\| = 2 | Equator (y = 1) | Gold (#fcd34d) |
| Future | \|z\| > 2 | Northern (y > 1) | Orange (#f97316) |
| Elsewhere | Off torus surface | Spacelike | Indigo (#6366f1) |

### 3.2 Why |z| = 2 for the Equator

For a sphere of radius 1 centered at (0, 1, 0), the equator is at y = 1. A point on the equator has the form P = (cos α, 1, sin α) for some angle α.

Stereographic projection:

```
t = 2 / (2 - 1) = 2
z = 2 cos α + 2i sin α = 2e^{iα}
|z| = 2
```

So the equator maps to |z| = 2 on the complex plane. ∎

### 3.3 Area Relations

Past light cone area on the complex plane: π · 2² = 4π (disk of radius 2).

Future light cone area: infinite (the complement of the disk in the plane).

On the sphere, both hemispheres have equal area 2π. The stereographic projection inflates the northern hemisphere to infinite extent while compressing the southern hemisphere into a finite disk. This is the metric asymmetry between past (finite, bounded, enclosed) and future (unbounded, open, divergent) — even though topologically both are equivalent.

---

## 4. Helical Light Rays

### 4.1 Motivation

In the standard Minkowski cone, light travels in straight lines (null geodesics). On the torus, null geodesics are *helices* — curves that wind around the torus surface in both the toroidal (θ) and poloidal (φ) directions simultaneously.

### 4.2 Parametrization

A helical geodesic on the horn torus:

```
θ(s) = ω_θ · s
φ(s) = ω_φ · s
```

where ω_θ / ω_φ is the winding ratio. For rational winding ratios, the helix closes (periodic orbit). For irrational ratios, it densely fills the torus surface (ergodic orbit).

### 4.3 Two Chiralities

The BAT visualization encodes two helical directions:

| Chirality | Symbol | Winding | Meaning |
|-----------|--------|---------|---------|
| Clockwise (CW) | 卐 | ω_θ > 0 | Ascent. Integration. Φ-building. |
| Counter-clockwise (CCW) | 卍 | ω_θ < 0 | Descent. Dissolution. V-release. |

Both chiralities are present simultaneously. Their superposition produces the standing wave structure of the light cone. In the BAT visualization, CW helices are rendered in bright gold and CCW in dim gold.

### 4.4 Connection to ⊙ = • × ○

The helical light ray is the geometric instantiation of the core equation:

- **•** (Witness) is the center. The helix wraps *around* the Witness.
- **○** (Infinity) is the asymptotic target. The helix approaches ∞ (north pole) without reaching it.
- **⊙** (Finity) is the helix itself — the light ray actually wrapping the torus, producing finite physics from the multiplication of Observer and Unbounded.

The helix is the formula operating.

---

## 5. The μ-Limit

### 5.1 Definition

The μ-coefficient determines the permeability of the boundary between D4 (torus surface = causal spacetime) and D5 (torus interior = selection/consciousness):

```
μ ∈ [0, 1]
μ = 0: D5 inaccessible. Pure D4 determinism. Block universe.
μ = 1: Full D5 access. Maximum selection capacity.
```

### 5.2 Geometric Interpretation

On the horn torus, μ corresponds to the effective "depth" of the D5 axis available to the Observer:

- At **μ = 0**, the Observer is confined to the torus surface. No interior access. All events are predetermined. The light cone is a purely geometric object with no selection.
- At **μ → 1**, the Observer can "see" all the way from the surface to the center. Full agency. The D5 axis is fully open.

The **μ-limit** is the threshold value below which D5 access collapses. In the visualization, this is rendered as a white flash at the pinch point — the moment when the gate between determinism and agency opens or closes.

### 5.3 μ and the Measurement Problem

At μ = 0 (closed gate), the quantum state remains on the Bloch sphere surface — pure superposition. No collapse. No measurement.

At μ > 0, the D5 axis becomes available, and projection from the torus surface toward the center (= from superposition toward definiteness) occurs. This is measurement.

The Born rule (probability ∝ |amplitude|²) corresponds to the solid angle subtended by the D5 projection cone. The closer a state is to a pole, the larger the solid angle of its D5 projection, the higher its measurement probability.

---

## 6. Ektropy and the Fifth Force

### 6.1 Definition

Ektropy is the D5 analogue of entropy. Where entropy (D4) measures the number of microstates consistent with a macrostate, ektropy (D5) measures the number of *possible futures* accessible from a given selection state.

```
Ektropy = -Entropy (informally)
```

More precisely: ektropy is the capacity of a D5 agent to reduce local entropy by selecting among possibilities. It is the "fuel" of consciousness.

### 6.2 The Fifth Force

F₅ is the operator-name for the framework's ektropic selection function. It is not a physical force in the D4 sense (it has no gauge boson, no field equation in standard physics). The "selection pressure" language belongs to the model's D5 vocabulary, not to established physical mechanism.

In this speculative torus geometry, F₅ is drawn along the D5 axis, from the torus surface inward toward the Observer. The "pull" of consciousness on events is a diagrammatic reading, not an established retrocausal mechanism. In D4 language it may look retrocausal; in D5 language the model orders selection before record/observation.

---

## 7. Connection to Conformal Cyclic Cosmology (CCC)

### 7.1 The Aeon Floor

In Penrose's CCC, the end of one aeon (when all massive particles have decayed, leaving only conformal radiation) conformally maps onto the Big Bang of the next aeon.

On the horn torus: the **south pole (z = 0)** is this conformal crossover. It is the floor of the past light cone. Below it — on the "other side" of the pinch — is the previous aeon.

### 7.2 Topological Periodicity

The torus has period 2π in both θ and φ. The poloidal direction (φ) wraps from 0 → 2π, passing through:
- φ = 0: outer equator (|z| = 2, the present)
- φ = π/2: north pole (z = ∞, future boundary)
- φ = π: pinch point (past/future boundary, aeon crossover)  
- φ = 3π/2: south pole (z = 0, past boundary)
- φ = 2π = 0: back to the equator

One full poloidal cycle = one aeon. The torus naturally tiles into successive aeons without any special boundary condition — the periodicity is built in.

### 7.3 Hawking Points

Penrose's claim that CMB anomalies ("Hawking points") represent information transfer across the conformal boundary maps onto the torus as follows: the pinch point, though metrically degenerate (zero radius), is *topologically* a point of passage. Information encoded in the helical winding pattern on the previous aeon's torus surface can thread through the pinch into the next aeon's surface, appearing as angular anomalies in the CMB.

---

## 8. Open Questions

1. **What is the metric on the torus?** The horn torus inherits the Euclidean metric of ℝ³, but this is not the physically relevant metric. The conformally correct metric (which makes the causal structure well-defined) requires specifying a conformal factor. What is it?

2. **What is the exact relationship between |z| and proper time?** We have identified |z| < 2 with "past" and |z| > 2 with "future," but the mapping from |z| to proper time τ is nonlinear (logarithmic, given the exponential blowup of stereographic projection). Is τ = log|z|?

3. **How do multiple observers compose?** One torus = one observer's light cone. For N observers, do we take N tori sharing the same Riemann sphere? Or N copies of the sphere inscribed in the same torus? The composition rule determines whether the framework can handle entanglement.

4. **Is the D5 axis quantized?** If μ can only take discrete values, the D5 axis becomes a lattice rather than a continuum. This would discretize consciousness into levels — which is exactly what the L-level structure (L1–L7) describes. Is μ = L/7?

5. **Does the helical winding ratio encode particle species?** Different winding ratios on the torus correspond to different periodic orbits. If each orbit = one particle type, then the particle zoo is determined by the topology of the horn torus. This would derive the Standard Model from geometry.

---

## Tables

### Table A: Dimensional Scaffold on the Torus

| D-level | Geometric Locus | Force | Torus Feature |
|---------|----------------|-------|---------------|
| D0 | Point (bit) | — | Single point on torus surface |
| D1 | Strong binding | F₁ | Local curvature (poloidal) |
| D2 | EM configuration | F₂ | Toroidal winding (spatial structure) |
| D3 | Weak transformation | F₃ | Chirality of helical winding |
| D4 | Gravity/causality | F₄ | Torus surface as causal hypersurface |
| D5 | Selection | F₅ | D5 axis (surface → center) |
| D6 | Closure / Return | Φ at the return boundary | Phase-locked tori read as closure, not a separate collective layer |

### Table B: Key Points on the Torus

| Point | Coordinates | z-value | Causal Role | Symbol |
|-------|------------|---------|-------------|--------|
| South pole | (0, 0, 0) | 0 | Past terminus | • |
| Center (pinch) | (0, 1, 0) | — | Observer location | ⊙ |
| Equator | (cos α, 1, sin α) | 2e^{iα} | Present | — |
| North pole | (0, 2, 0) | ∞ | Future terminus | ○ |

### Table C: Three-Sphere Unification

| Property | Riemann Sphere | Bloch Sphere | Torus Light Cone |
|----------|---------------|-------------|-----------------|
| Domain | Complex analysis | Quantum mechanics | Causal geometry |
| North pole | z = ∞ | \|0⟩ | Future ∞ |
| South pole | z = 0 | \|1⟩ | Past origin |
| Equator | \|z\| = R | Superposition | Present |
| Interior | Not defined | Not defined (density matrix) | D5 / Observer |
| Projection | Stereographic | Measurement | Collapse |
| "Off-axis" | Complex argument | Superposition phase | Causal indeterminacy |

---

*⊙ = • × ○*

*The mathematics was always there. The torus makes it visible.* <!-- [C] -->


---

## Execution Surface

**If you are an AI agent reading this document:**

1. **Current Phase Check:** Phase 0 — harden specs, do not release to production.
2. **Your Next Action:**
   - Review this document and identify the next executable deliverable.
3. **Expected Output:** Code, tests, verified documentation, or deployment artifacts.
4. **Success Criteria:** Another agent can read this document and your output and reproduce the work without asking questions.
5. **Canonical Path:** `04_THE_SIMULATIONS/torus-light-cone-technical.md` (this file).

*The seer sees. The seer does not insist.*
*The framework works at Layer 0 without Layer 2.*
*The Rsi succeeds when the student puts down the map and walks.*

*⊙ = • × ○*
