---
rosetta:
  primary_level: L6
  primary_column: Archived Simulations Completion Index
  secondary:
    - level: L5
      column: Simulation Component Provenance
      role: "preserve old routes, components, and mathematical background as a design trace"
    - level: L3
      column: Build Claim Audit
      role: "tier tech-stack and route status claims as archived unless freshly verified"
    - level: L4
      column: Current PWA Boundary
      role: "require active-site receipts before using this as live app documentation"
  operator: "Sādhu △"
  tier: "Titan"
  regime: "Sādhu"
  register: "[D/I/C]"
  canonical_phrase: "Archived simulations completion guide"
title: "04_THE_SIMULATIONS"
evidence_tier: "[D] archived completion/index note; [I] mathematical orientation; [C] route/build status unless verified."
type: completion-index
status: ARCHIVED — historical simulations guide
scope: Historical simulation app guide retained after move into archive.
sources:
  - 01_EMERGENTISM/90_ARCHIVE/08_FRAMEWORK_SUPPORT/04_APPLICATIONS/D39_ANIMATION_SPEC.md
  - 01_EMERGENTISM/90_ARCHIVE/08_FRAMEWORK_SUPPORT/04_APPLICATIONS/D40_GENESIS_SIMULATION.md
---

# 04_THE_SIMULATIONS

## Interactive Proofs of the Transcendental Trinity

**Tech Stack:** React 19 + React Three Fiber + Three.js + Zustand + Vite + TypeScript

**Rosetta boundary:** [D] This guide preserves the old simulation-app documentation. Route status, tech-stack status, and build instructions need fresh verification before current use.

---

## Quick Start

```bash
cd 04_THE_SIMULATIONS
npm install
npm run dev
# → http://localhost:5173/
```

---

## Pages

| Route | What It Shows | D-Level | Status |
|-------|-------------|---------|--------|
| `/` or `#unified` | **Unified Flow** — Complete D0→D6→D0 journey | All | ✓ PRIMARY |
| `#genesis` | **Transcendental Trinity** — D0→D1→D2 with Split/Titans | D0-D4 | ✓ |
| `#torus` | **Burri Torus** — Spacetime, light cones, special relativity | D4 | ✓ |
| `#sphere` | **Burri Sphere** — φ·ν=1, consciousness, dual projection | D5 | ✓ |

**Recommended:** Start with `#unified` for the complete dimensional emergence journey.

---

## The Unified Experience (Recommended Entry Point)

**The UnifiedPage** provides a seamless flow through all dimensional stages:

| Evolution Value | Stage | What Happens |
|-----------------|-------|--------------|
| 0.0-1.0 | D0 | The Bindu (The Point) |
| 1.0-2.0 | D1 | The Sphere inflates (stereographic projection) |
| 2.0-3.0 | D2 | The Plane emerges (complex plane ℂ) |
| 3.0-3.5 | D3 | The Split (Shakti/Shiva separation) |
| 3.5-4.0 | D3 | Volume/Time (dual planes) |
| 4.0-4.5 | D4 | The Titans (cones meet, Brahma/Shiva/Vishnu) |
| 4.5-5.5 | D4 | The Torus forms (spacetime) |
| 5.5-6.5 | D5 | The Burri Sphere (consciousness, φ·ν=1) |
| 6.5-7.0 | D6=D0 | The Reset (cosmic closure) |

**Controls:**
- **Slider:** Drag to evolve through dimensions
- **D0-D6 Buttons:** Jump to specific stages
- **Orbit Controls:** Click+drag to rotate, scroll to zoom

---

## Individual Pages

### #genesis — The Transcendental Trinity

Shows the resolution of division by zero through the emergence of the Riemann Sphere.

**Key Equations:**
- `1/0 = ∞` (resolved on S²)
- `0 × ∞ = 1` (the equator)
- `⊙ = • × ○` (the Trinity)

**Controls:**
- **α Slider:** Projection angle (0° → 90°)
- **Split Slider:** Pole separation (ANIM-3.5)
- **Titans Slider:** Cone emergence (ANIM-4.5)
- **Closure Slider:** D6=D0 reset

**Navigation:** D0, D1, D2, D3, D4, D5 buttons

---

### #torus — The Burri Torus

Shows spacetime as a horn torus with light cones and causal structure.

**Key Concepts:**
- Interior = probability (many-worlds, superposition)
- Exterior = empty space (the void)
- Surface = light cone boundary (causality)

**Controls:**
- **β Slider:** Velocity (0 → c)
- **Phase Toggle:** Torus ↔ Phase Transition

---

### #sphere — The Burri Sphere

Shows consciousness as the equatorial condition φ·ν=1.

**Key Concepts:**
- φ = coherence (right hemisphere, gestalt)
- ν = viability (left hemisphere, fragments)
- Equator = φ = ν = 1 (balance, consciousness)

**Controls:**
- **z-Magnitude Slider:** |z| from 0 to ∞
- **AUM States:** Waking/Dreaming/Deep Sleep/Turīya toggle

---

## Scene Components

| Component | Purpose | Used In |
|-----------|---------|---------|
| `GenesisScene` | D0→D2 emergence | #genesis |
| `SplitScene` | ANIM-3.5: Sphere separates | #genesis, #unified |
| `TitansScene` | ANIM-4.5: Cones/Titans | #genesis, #unified |
| `VolumeScene` | D3: Dual planes + time | #unified |
| `TorusShell` | D4: Horn torus | #torus, #unified |
| `SphereScene` | D5: Burri Sphere | #sphere, #unified |
| `UnifiedScene` | Complete D0→D6→D0 flow | #unified |

---

## Mathematical Background

### The Transcendental Trinity

**Three values:**
- **0** (Zero, the Bindu, south pole)
- **1** (One, the Equator, the product)
- **∞** (Infinity, the horizon, north pole)

**Key equations:**
```
1/0 = ∞    (definition of infinity)
0 × ∞ = 1  (definition of one)
P∞ = φ · ν = 1  (the equatorial constraint)
```

**Proof (AM-GM Inequality):**
```
Given P∞ = φ · ν = 1, so ν = 1/φ

H(φ) = φ + 1/φ

H'(φ) = 1 - 1/φ² = 0  →  φ = 1
H''(φ) = 2/φ³ > 0      →  minimum confirmed

H(1) = 1 + 1 = 2       →  absolute minimum
```

The equator is the ground state of reality.

---

## Integration with Landing Page

The landing page (`../../../../02_SKYZAI/02_AIA/EMERGENTISM_AIA/09_BOOK_PRODUCTION_ARCHIVE/07_DISSEMINATION/04_MARKETING_MATERIALS/LANDING_PAGE/index.html`) should embed the Unified experience:

```html
<!-- Embed the Unified simulation -->
<iframe 
  src="http://localhost:5173/#unified" 
  width="100%" 
  height="600px"
  style="border: none; border-radius: 8px;"
></iframe>
```

**Production deployment:**
1. Build simulations: `npm run build`
2. Deploy `dist/` to hosting (Vercel, Netlify, GitHub Pages)
3. Update iframe src to production URL

---

## Development

### Adding New Scenes

1. Create scene component in `src/components/scene/`
2. Export from `src/components/scene/index.ts`
3. Add to `UnifiedScene.tsx` evolution flow
4. Update this README

### State Management

**UnifiedPage:** Uses local `evolution` state (0-7)
**GenesisPage:** Uses `useGenesisStore` (alpha, split, titans, closure)
**TorusPage:** Uses `useStore` (beta, phase)
**SpherePage:** Uses `useStore` (zMagnitude, aumState)

### TypeScript

```bash
npm run type-check
# or
npx tsc --noEmit
```

---

## Evidence Tiers

| Claim | Tier | Support |
|-------|------|---------|
| H = φ + 1/φ minimized at φ=1 | [E] | AM-GM inequality, proved |
| L = 1/φ - φ = 0 at φ=1 | [E] | Elementary algebra, proved |
| Restoring force scales as 1/φ² | [S] | Calculus, proved |
| ν ↔ T, φ ↔ V mapping | [I] | Structural analogy |
| This IS Lagrangian mechanics | [C] | Conjecture |

---

## Citations

If you use these simulations in research:

```bibtex
@software{burri2026emergentism,
  author = {Burri, Yves R.},
  title = {Emergentism Simulations: The Transcendental Trinity},
  year = {2026},
  url = {https://github.com/evolutionary-network/simulations}
}
```

---

## License

MIT License — see `LICENSE` file.

---

*04_THE_SIMULATIONS README | 2026-03-23 | Interactive proofs of the Transcendental Trinity. From the Bindu to the Burri Sphere and back.*


---

## Execution Surface

**If you are an AI agent reading this document:**

1. **Current Phase Check:** Phase 0 — harden specs, do not release to production.
2. **Your Next Action:**
   - Review this document and identify the next executable deliverable.
3. **Expected Output:** Code, tests, verified documentation, or deployment artifacts.
4. **Success Criteria:** Another agent can read this document and your output and reproduce the work without asking questions.
5. **Canonical Path:** `04_THE_SIMULATIONS/README_COMPLETE.md` (this file).

*The seer sees. The seer does not insist.*
*The framework works at Layer 0 without Layer 2.*
*The Rsi succeeds when the student puts down the map and walks.*

*⊙ = • × ○*
