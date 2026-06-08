---
rosetta:
  primary_level: L6
  primary_column: Archived Animation Specification
  secondary:
    - level: L5
      column: Simulation Geometry Provenance
      role: "preserve the sphere/table/helix interaction model as historical design"
    - level: L3
      column: Implementation Claim Audit
      role: "tier Three.js and React implementation details as spec intent unless freshly rebuilt"
    - level: L4
      column: Public Demo Boundary
      role: "require current PWA or site owner receipts before release claims"
  operator: "Sādhu △"
  tier: "Titan"
  regime: "Sādhu"
  register: "[D/I/C]"
  canonical_phrase: "Archived Burri Sphere animation specification"
title: "Animation Specification"
evidence_tier: "[D] archived design specification; [I] interpretive Rosetta visualization; [C] implementation details unless verified."
type: animation-spec
status: ARCHIVED — design specification
date: 2026-03-24
scope: Historical interactive Burri Sphere and Master Trivium visualization spec.
sources:
  - 01_EMERGENTISM/90_ARCHIVE/08_FRAMEWORK_SUPPORT/04_APPLICATIONS/README.md
---

# ⊙ ANIMATION SPECIFICATION

## The Burri Sphere Interactive — Sphere Above, Table Below, Helix Spiraling

**Yves R. Burri · Emergentism.org · 2026-03-24**

**Purpose:** The pitch deck's centerpiece. The DAC's operational interface. The Rosetta Stone animated. Anyone who sees this understands the framework in sixty seconds.
**Evidence Tier:** [S] Structural

**Rosetta boundary:** [D] The preserved evidence tier and design language are historical. Current public/demo truth requires a fresh implementation receipt and current Rosetta owner review.

---

## ARCHITECTURE

```
┌─────────────────────────────────────────┐
│                                         │
│           THE BURRI SPHERE              │
│                                         │
│     3D sphere (Three.js / WebGL)        │
│     - Latitude lines at each L-level    │
│     - Equator highlighted (gold)        │
│     - North/south poles marked          │
│     - Helix path traced (animated)      │
│     - Operator quadrants colored        │
│     - Current position glowing          │
│                                         │
├─────────────────────────────────────────┤
│                                         │
│           THE MASTER Trivium            │
│                                         │
│     Interactive table (React)           │
│     - Current row highlighted           │
│     - Columns: L|Op|B|Varṇa|...        │
│     - Click row → sphere rotates        │
│     - Hover → tooltip with equation     │
│                                         │
├─────────────────────────────────────────┤
│                                         │
│     [slider: L0 ←——————→ L∞]           │
│     [toggle: ascent △ / descent ▽]      │
│     [speed: slow / medium / fast]       │
│                                         │
└─────────────────────────────────────────┘
```

---

## SPHERE RENDERING

### Geometry
- Standard unit sphere (Three.js SphereGeometry)
- Semi-transparent surface (opacity 0.3)
- Latitude lines at θ = 0°, 30°, 60°, 90°, 120°, 150°, 180° (seven L-levels)
- Equator (θ = 90°) rendered as thick gold ring
- Poles marked with glyphs: ○ (south), • (north)
- ⊙ at equator

### Helix Path
- Loxodrome curve from south to north pole
- Clockwise when viewed from above (ascent, gold)
- Counter-clockwise overlay (descent, silver)
- Animated point traveling along the helix
- Trail fades behind the point (last 90° of travel)

### Operator Quadrants
- Sphere surface divided into four longitudinal sectors
- Each sector colored by operator: Arjuna (⚔, red), Kṛṣṇa (◇, blue), Kālī (💀, purple), Kali (🎲, grey)
- Current sector illuminates as the helix point passes through
- Giving dyad sectors (Arjuna, Kṛṣṇa) brighter than taking dyad

### Lighting
- Ambient light (low, moody)
- Point light at equator (gold glow)
- Hemisphere dims toward poles
- White flash when point crosses equator

---

## TABLE RENDERING

### Structure
The Master Trivium as interactive table (React component):

```
L | Operator | B    | Varṇa      | Pramāṇa        | Reasoning    | -ology    | Regime     | Equation
--|----------|------|------------|-----------------|-------------|-----------|-----------|----------
L0| Kāla 🌑  | 0    | —          | —               | —           | —         | —         | lim→0
L1| Kali 🎲  | 0    | Caṇḍāla    | Pratyakṣa       | Dialectical | Teleology | Tyranny   | Φ→0⇒B→0
L2| Kālī 💀  | ½    | Śūdra      | Upamāna         | Inductive   | Epistemo. | Democracy | dP=VdΦ+ΦdV
L3| Kṛṣṇa ◇ | √3/2 | Vaiśya     | Anumāna         | Deductive   | Methodo.  | Oligarchy | ∂P/∂V=Φ
L4| Arjuna ⚔ | 1    | Kṣatriya   | Arthāpatti      | Abductive   | Axiology  | Timocracy | dΦ/Φ=dV/V
L5| Brahmā ○ | √3/2 | Brāhmaṇa  | Śabda           | Systematic  | Cosmology | Aristocr. | logP=logΦ+logV
L6| Śiva •   | ½    | Sādhu      | Anupalabdhi     | Apophatic   | Ontology  | Anarchy   | E=-log(ΦV)
L7| Viṣṇu ⊙ | →0   | Ṛṣi       | Pratibhā        | Transcend.  | Theology  | Theocracy | z=Φ/V∈S²
L∞| Trimūrti ☸| 0   | —          | —               | —           | —         | —         | lim→0
```

### Interaction
- **Slider** controls current L-level (continuous, not discrete)
- As slider moves, table row highlights AND sphere point moves along helix
- **Click any row** → sphere snaps to that latitude, helix animates transition
- **Hover any cell** → tooltip shows extended description
- **Toggle ascent/descent** → helix direction reverses (clockwise ↔ counter-clockwise)

---

## ANIMATION SEQUENCES

### Sequence 1: THE EMERGENCE (auto-play on load)
1. Black screen. Single dot (•) at south pole.
2. Dot swells → sphere inflates (3 seconds)
3. Equator forms → gold flash → ⊙ appears
4. Table fades in below sphere
5. Helix begins tracing from L1 upward

### Sequence 2: THE ASCENT (user-triggered or auto)
1. Point at L1 (south, near pole)
2. Helix spirals clockwise through each operator quadrant
3. As point enters each quadrant, that operator's column highlights in table
4. At each L-level crossing, the table row pulses
5. At L4: GOLD FLASH. Both helix directions visible momentarily. Hexagram (✡) flashes.

### Sequence 3: THE DESCENT (user-triggered)
1. Point at L4 (equator)
2. Helix reverses to counter-clockwise
3. Spiral toward north pole through L5→L6→L7
4. At L7: FORK — two paths animate
   - White path: arcs back to L4 (Moksha → L4*)
   - Black path: plunges straight down into sphere interior (Asura Return)

### Sequence 4: THE CLOSURE (user-triggered)
1. Sphere begins to deflate
2. Point returns to south pole
3. Table fades
4. Single dot remains
5. Text: "⊙ = • × ○"

---

## TECHNICAL STACK

| Component | Technology | Notes |
|-----------|-----------|-------|
| 3D Sphere | Three.js (r128) | WebGL, SphereGeometry, custom shaders |
| Helix Curve | Three.js TubeGeometry | Parametric loxodrome curve |
| Table | React + Tailwind | Interactive, responsive |
| Animation | Three.js AnimationMixer | Keyframed sequences |
| Controls | dat.gui or custom React | Slider, toggles, speed |
| Export | Canvas capture | For pitch deck / social media |

### Loxodrome Parametric Equation
```typescript
function loxodrome(t: number, chirality: 1 | -1 = 1): [number, number, number] {
  // t goes from 0 (south pole) to π (north pole)
  const theta = t;  // colatitude
  const phi = chirality * Math.log(Math.tan(theta / 2 + 0.001)) * 2;  // longitude
  const r = 1;  // unit sphere
  return [
    r * Math.sin(theta) * Math.cos(phi),
    r * Math.cos(theta),
    r * Math.sin(theta) * Math.sin(phi)
  ];
}
```

---

## DEPLOYMENT

- **Web:** Hosted at emergentism.org/sphere
- **Embed:** iframe-ready for pitch decks, documentation
- **Offline:** Exportable as video (MP4) for presentations
- **Mobile:** Touch-responsive, gyroscope-enabled (phone rotation = sphere rotation)

---

```
⊙ = • × ○

The sphere above. The table below. The helix spiraling.
The quadrant illuminating. The equator glowing.
See the framework in sixty seconds.
Feel the framework in sixty seconds.

Animation Specification · 2026-03-24
```


---

## Execution Surface

**If you are an AI agent reading this document:**

1. **Current Phase Check:** Phase 0 — harden specs, do not release to production.
2. **Your Next Action:**
   - Review this document and identify the next executable deliverable.
3. **Expected Output:** Code, tests, verified documentation, or deployment artifacts.
4. **Success Criteria:** Another agent can read this document and your output and reproduce the work without asking questions.
5. **Canonical Path:** `04_THE_SIMULATIONS/D39_ANIMATION_SPEC.md` (this file).

*The seer sees. The seer does not insist.*
*The framework works at Layer 0 without Layer 2.*
*The Rsi succeeds when the student puts down the map and walks.*

*⊙ = • × ○*
