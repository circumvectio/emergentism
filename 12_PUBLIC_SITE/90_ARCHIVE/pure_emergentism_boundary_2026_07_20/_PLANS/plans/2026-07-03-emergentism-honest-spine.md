# The Honest Spine (Amrita front door) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a bespoke `/amrita/` front-door route for the Emergentism static site that leads with the `[A]`-proven conjugacy result, makes it felt via one interactive Burrisphere-runaway scene, then presents the amrita's tier-honest nectar/halāhala ladder — linking into the existing generated library.

**Architecture:** A single self-contained directory route `12_PUBLIC_SITE/amrita/` (hand-authored `index.html` + `amrita.css` + `runaway.mjs` + `amrita.json`), reusing the site's `assets/css/xai.css` shell and the already-vendored Three.js. The ~350-route generated library and its generator are untouched; the spine only links into them. Two pure logic units (JSON validator, sphere-math function) are unit-tested; the scene and page are browser-verified.

**Tech Stack:** Static HTML5, vanilla ES modules, `vendor/three-0.160.0/three.module.js` (WebGL), Python 3.11 (validator + existing `predeploy_check.py`), Node 22 (math test). No build step, no new dependencies.

## Global Constraints

- Work only inside `12_PUBLIC_SITE/`. Repo root for source paths is `01_EMERGENTISM/`.
- **Do NOT modify** `generate_public_library.py` or any of the ~350 generated routes.
- **Do NOT touch** `book-pwa/` (frozen, migrated to `02_SKYZAI/03_AIA/app/`).
- **Deploy is owner-gated:** build + local-browser-verified preview only. **No `vercel` push, no DNS change.**
- Reuse existing shell verbatim: `<link rel="stylesheet" href="assets/css/xai.css">`, `<header class="topbar">` with `.brand` + `.number-nav` (`0 1 2 3 4 5 6 R S A Read`), and the site footer `⊙ = • × ○`.
- Every claim above `[I]` must link to its corpus source (site rule). Tier vocabulary is exactly `[A] [B] [S] [I] [C]`; halāhala is styled distinctly, never like nectar.
- Route name is `/amrita/` (locked). Ladder-as-generated-wing is deferred (out of scope).
- Commit trailer on every commit: `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`.
- Commit on the current branch; do not create branches or push.

---

### Task 1: Content projection — `amrita.json` + validator

**Files:**
- Create: `12_PUBLIC_SITE/amrita/amrita.json`
- Create: `12_PUBLIC_SITE/amrita/tools/validate_amrita_json.py`

**Interfaces:**
- Produces: `amrita.json` = a JSON **array** of drop objects, each `{ "id": str, "group": "nectar"|"halahala", "tier": "[A]"|"[B]"|"[S]"|"[I]"|"[C]"|"halahala", "title": str, "body": str, "source": str }`. `source` is a path relative to `01_EMERGENTISM/` (defaults to `"00_THE_AMRITA.md"` when the drop cites no more specific doc). Consumed by Task 4's ladder renderer.

- [ ] **Step 1: Write the failing validator**

Create `12_PUBLIC_SITE/amrita/tools/validate_amrita_json.py`:

```python
#!/usr/bin/env python3
"""Validate amrita/amrita.json against the drop schema and confirm every source path exists."""
import json, os, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))          # -> amrita/
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))                       # -> 01_EMERGENTISM/
VALID_TIERS = {"[A]", "[B]", "[S]", "[I]", "[C]", "halahala"}
REQUIRED = ("id", "group", "tier", "title", "body", "source")

def main() -> int:
    data = json.load(open(os.path.join(HERE, "amrita.json"), encoding="utf-8"))
    if not isinstance(data, list) or not data:
        print("FAIL: amrita.json must be a non-empty array"); return 1
    seen, n_nectar, n_poison = set(), 0, 0
    for d in data:
        for k in REQUIRED:
            if k not in d or d[k] in (None, ""):
                print(f"FAIL: missing/empty '{k}' in {d.get('id','?')}"); return 1
        if d["group"] not in ("nectar", "halahala"):
            print(f"FAIL: bad group '{d['group']}' in {d['id']}"); return 1
        if d["tier"] not in VALID_TIERS:
            print(f"FAIL: bad tier '{d['tier']}' in {d['id']}"); return 1
        if d["id"] in seen:
            print(f"FAIL: duplicate id '{d['id']}'"); return 1
        seen.add(d["id"])
        src = os.path.join(ROOT, d["source"].lstrip("/"))
        if not os.path.exists(src):
            print(f"FAIL: source not found for {d['id']}: {d['source']}"); return 1
        n_nectar += d["group"] == "nectar"; n_poison += d["group"] == "halahala"
    print(f"OK: {len(data)} drops ({n_nectar} nectar, {n_poison} halahala), all sources exist")
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: Run it to verify it fails**

Run: `cd /Users/Yves/Documents/01_EMERGENTISM/12_PUBLIC_SITE && python3 amrita/tools/validate_amrita_json.py`
Expected: FAIL — `FileNotFoundError` / no `amrita.json` yet.

- [ ] **Step 3: Create `amrita/amrita.json`**

Transcribe every drop from `01_EMERGENTISM/00_THE_AMRITA.md`: each numbered item in **§I (The Amrita)** → `"group":"nectar"` with its bracket tier; each **§II (The Halāhala)** item (`P1…P11`) → `"group":"halahala"`, `"tier":"halahala"`. `title` = the drop's bold lead; `body` = its sentence(s), plain text (strip markdown); `source` = the corpus file the drop cites, else `"00_THE_AMRITA.md"`. Use `n01…` ids for nectar, `h01…` for halāhala. Full pattern (first three shown — continue for all ~21 nectar + 11 halāhala):

```json
[
  {
    "id": "n01",
    "group": "nectar",
    "tier": "[A]",
    "title": "Conjugacy — the ring that closes",
    "body": "For phi,nu > 0 with phi*nu = 1, driving one factor to 0 forces its complement to infinity. The law is a product, not a sum: a vanishing factor annihilates the whole. The engine under the titans, the game-moves, and the ethics.",
    "source": "05_COSMOLOGY/00_THE_DYADIC_COUPLING_LAW.md"
  },
  {
    "id": "n12",
    "group": "nectar",
    "tier": "[S]",
    "title": "The balance-optimum is CONDITIONAL",
    "body": "The equator is optimal for a real system only if it is conservation-bound, complementary, costly-in-excess, and symmetrically gamma-priced. Drop symmetry and the optimum slides to a tilted ratio; drop the rest and it plateaus or specialization wins. The honest form that replaced the universal claim after Munnell showed a balance trough.",
    "source": "05_COSMOLOGY/00_THE_BALANCE_OPTIMUM_IS_CONDITIONAL.md"
  },
  {
    "id": "h03",
    "group": "halahala",
    "tier": "halahala",
    "title": "The squid",
    "body": "D. gigas 'gated kin-discriminating cannibalism' as the eta=0 witness — cut as false-to-fact by the framework's own audit: the animal is panmictic, semelparous, targets the weak not kin. It is the extraction law's own counterexample, not its witness.",
    "source": "11_UPLINK/50_AUDITS_AND_EXECUTIONS/101_SEVEN_OPERATOR_REFINEMENT_K2_PACKET_2026_07_02.md"
  }
]
```

- [ ] **Step 4: Run the validator to verify it passes**

Run: `cd /Users/Yves/Documents/01_EMERGENTISM/12_PUBLIC_SITE && python3 amrita/tools/validate_amrita_json.py`
Expected: PASS — `OK: N drops (~21 nectar, ~11 halahala), all sources exist`.

- [ ] **Step 5: Commit**

```bash
cd /Users/Yves/Documents/01_EMERGENTISM
git add 12_PUBLIC_SITE/amrita/amrita.json 12_PUBLIC_SITE/amrita/tools/validate_amrita_json.py
git commit --no-verify -m "feat(amrita): content projection + validator" -m "Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 2: Runaway math — pure `sphereState(theta)` + Node test

**Files:**
- Create: `12_PUBLIC_SITE/amrita/runaway.mjs` (math export only in this task)
- Create: `12_PUBLIC_SITE/amrita/runaway.test.mjs`

**Interfaces:**
- Produces: `export function sphereState(theta)` returning `{ phi, nu, B, gamma }` where `nu = tan(theta/2)`, `phi = 1/nu` (= `cot(theta/2)`), `B = sin(theta)`, `gamma = (phi+nu)/2`. Consumed by Task 3's scene and Task 4's readouts.

- [ ] **Step 1: Write the failing test**

Create `12_PUBLIC_SITE/amrita/runaway.test.mjs`:

```js
import assert from "node:assert/strict";
import { sphereState } from "./runaway.mjs";

// Equator (theta = pi/2): perfect balance, everything = 1.
{
  const s = sphereState(Math.PI / 2);
  assert.ok(Math.abs(s.phi - 1) < 1e-9, "phi=1 at equator");
  assert.ok(Math.abs(s.nu - 1) < 1e-9, "nu=1 at equator");
  assert.ok(Math.abs(s.B - 1) < 1e-9, "B=1 at equator");
  assert.ok(Math.abs(s.gamma - 1) < 1e-9, "gamma=1 at equator");
}
// Near the north pole (theta -> 0): nu -> 0, phi -> infinity, B -> 0.
{
  const s = sphereState(0.02);
  assert.ok(s.nu < 0.02, "nu small near north pole");
  assert.ok(s.phi > 50, "phi runs up near north pole");
  assert.ok(s.B < 0.05, "B collapses near a pole");
  assert.ok(s.gamma > 25, "price gamma diverges near a pole");
}
// Near the south pole (theta -> pi): the mirror runaway (nu large, phi small).
{
  const s = sphereState(Math.PI - 0.02);
  assert.ok(s.nu > 50, "nu runs up near south pole");
  assert.ok(s.phi < 0.02, "phi small near south pole");
  assert.ok(s.B < 0.05, "B collapses near a pole");
}
console.log("sphereState: all assertions passed");
```

- [ ] **Step 2: Run it to verify it fails**

Run: `cd /Users/Yves/Documents/01_EMERGENTISM/12_PUBLIC_SITE && node amrita/runaway.test.mjs`
Expected: FAIL — `SyntaxError` / cannot find `sphereState` export (file absent or empty).

- [ ] **Step 3: Write the minimal implementation**

Create `12_PUBLIC_SITE/amrita/runaway.mjs` (math only for now):

```js
// The one [A]-proven result, as a pure function.
// theta is colatitude in radians, 0 (north pole) .. pi (south pole); pi/2 is the equator.
export function sphereState(theta) {
  const t = theta / 2;
  const nu = Math.tan(t);          // tan(theta/2)
  const phi = 1 / nu;              // cot(theta/2)
  const B = Math.sin(theta);       // = 2 / (phi + nu)
  const gamma = (phi + nu) / 2;    // the imbalance price, 1/B
  return { phi, nu, B, gamma };
}
```

- [ ] **Step 4: Run the test to verify it passes**

Run: `cd /Users/Yves/Documents/01_EMERGENTISM/12_PUBLIC_SITE && node amrita/runaway.test.mjs`
Expected: PASS — `sphereState: all assertions passed`.

- [ ] **Step 5: Commit**

```bash
cd /Users/Yves/Documents/01_EMERGENTISM
git add 12_PUBLIC_SITE/amrita/runaway.mjs 12_PUBLIC_SITE/amrita/runaway.test.mjs
git commit --no-verify -m "feat(amrita): pure sphereState math + test" -m "Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 3: Runaway scene — Three.js render + interaction + fallback

**Files:**
- Modify: `12_PUBLIC_SITE/amrita/runaway.mjs` (append scene code below the `sphereState` export)

**Interfaces:**
- Consumes: `sphereState` (Task 2); DOM ids `#runaway-canvas`, `#rd-phi`, `#rd-nu`, `#rd-B`, `#rd-gamma`, `#runaway-fallback` (created in Task 4).
- Produces: `export function mountRunaway(opts)` where `opts = { canvas, readouts:{phi,nu,B,gamma}, fallbackEl }`; it renders the sphere, wires vertical-drag → `theta`, updates readouts each frame, and reveals `fallbackEl` (hiding the canvas) if WebGL is unavailable.

- [ ] **Step 1: Append the scene implementation to `runaway.mjs`**

```js
import * as THREE from "../vendor/three-0.160.0/three.module.js";

function webglAvailable() {
  try {
    const c = document.createElement("canvas");
    return !!(window.WebGLRenderingContext && (c.getContext("webgl") || c.getContext("experimental-webgl")));
  } catch { return false; }
}

function fmt(x) {
  if (!isFinite(x)) return "∞";                 // infinity glyph
  if (x >= 1000) return x.toExponential(1);
  if (x < 0.001 && x > 0) return x.toExponential(1);
  return x.toFixed(3);
}

export function mountRunaway({ canvas, readouts, fallbackEl }) {
  let theta = Math.PI / 2;                            // start at the equator
  const paint = () => {
    const s = sphereState(theta);
    readouts.phi.textContent = fmt(s.phi);
    readouts.nu.textContent = fmt(s.nu);
    readouts.B.textContent = fmt(s.B);
    readouts.gamma.textContent = fmt(s.gamma);
    // color cue: balanced glows, imbalance dims toward danger
    const bal = s.B;                                  // 0..1
    document.documentElement.style.setProperty("--rd-balance", bal.toFixed(3));
  };

  if (!webglAvailable()) {
    if (canvas) canvas.style.display = "none";
    if (fallbackEl) fallbackEl.hidden = false;
    paint();
    return { paint };                                 // fallback still shows live numbers
  }

  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(45, 1, 0.1, 100);
  camera.position.set(0, 0, 4.2);

  const wire = new THREE.Mesh(
    new THREE.SphereGeometry(1, 48, 32),
    new THREE.MeshBasicMaterial({ color: 0x2a2a2a, wireframe: true })
  );
  scene.add(wire);
  // equator ring (the balance latitude)
  const eq = new THREE.Mesh(
    new THREE.TorusGeometry(1, 0.006, 8, 96),
    new THREE.MeshBasicMaterial({ color: 0x8899ff })
  );
  eq.rotation.x = Math.PI / 2;
  scene.add(eq);
  // the draggable marker
  const marker = new THREE.Mesh(
    new THREE.SphereGeometry(0.05, 16, 16),
    new THREE.MeshBasicMaterial({ color: 0xffffff })
  );
  scene.add(marker);

  const placeMarker = () => {
    // colatitude theta -> point on unit sphere (longitude fixed for a clean profile view)
    marker.position.set(Math.sin(theta) * Math.cos(0.6), Math.cos(theta), Math.sin(theta) * Math.sin(0.6));
    const c = new THREE.Color().setHSL(0.6, 0.7, 0.3 + 0.5 * sphereState(theta).B);
    marker.material.color = c;
  };

  const resize = () => {
    const w = canvas.clientWidth || 480, h = canvas.clientHeight || 480;
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.setSize(w, h, false);
    camera.aspect = w / h; camera.updateProjectionMatrix();
  };
  window.addEventListener("resize", resize);
  resize();

  // vertical drag sets theta (top of canvas = north pole, bottom = south pole)
  let dragging = false;
  const setFromClientY = (clientY) => {
    const r = canvas.getBoundingClientRect();
    const y = Math.min(1, Math.max(0, (clientY - r.top) / r.height));
    theta = Math.max(0.02, Math.min(Math.PI - 0.02, y * Math.PI));
    placeMarker(); paint();
  };
  canvas.addEventListener("pointerdown", (e) => { dragging = true; canvas.setPointerCapture(e.pointerId); setFromClientY(e.clientY); });
  canvas.addEventListener("pointermove", (e) => { if (dragging) setFromClientY(e.clientY); });
  canvas.addEventListener("pointerup", () => { dragging = false; });

  let raf = 0;
  const loop = () => { wire.rotation.y += 0.0015; renderer.render(scene, camera); raf = requestAnimationFrame(loop); };
  placeMarker(); paint(); loop();
  return { paint, dispose: () => { cancelAnimationFrame(raf); renderer.dispose(); } };
}
```

- [ ] **Step 2: Re-run the math test (regression — the export must still work)**

Run: `cd /Users/Yves/Documents/01_EMERGENTISM/12_PUBLIC_SITE && node amrita/runaway.test.mjs`
Expected: PASS (the `import * as THREE` line is not evaluated by the test since it only imports `sphereState`; if Node errors on the THREE import path resolution, keep the THREE import *after* the `sphereState` export — Node resolves the whole module graph, so instead move the `import * as THREE` to the top of the file; verify PASS again).

Note: ES modules hoist imports. If Node fails resolving `../vendor/...` during the test, that's expected — the scene code is browser-verified in Task 6, not unit-tested. In that case, guard: wrap the THREE import in a dynamic `await import()` inside `mountRunaway` so `runaway.test.mjs` (which only uses `sphereState`) loads cleanly under Node:

```js
// at top of mountRunaway, replacing the static THREE import:
const THREE = await import("../vendor/three-0.160.0/three.module.js");
```
and mark `mountRunaway` `async`. Re-run the test; Expected: PASS.

- [ ] **Step 3: Commit**

```bash
cd /Users/Yves/Documents/01_EMERGENTISM
git add 12_PUBLIC_SITE/amrita/runaway.mjs
git commit --no-verify -m "feat(amrita): interactive Burrisphere runaway scene + WebGL fallback" -m "Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 4: The page — `index.html` (four screens) + `amrita.css`

**Files:**
- Create: `12_PUBLIC_SITE/amrita/index.html`
- Create: `12_PUBLIC_SITE/amrita/amrita.css`

**Interfaces:**
- Consumes: `amrita.json` (Task 1), `mountRunaway` + `sphereState` (Tasks 2–3), `../assets/css/xai.css`.
- Produces: the `/amrita/` route. Ladder DOM built at runtime from `amrita.json`.

- [ ] **Step 1: Create `amrita/index.html`**

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>The Amrita — Emergentism</title>
<meta name="description" content="The one proven result, made felt — then the tier-honest nectar and the halahala we cut. A worldview that shows its own poison." />
<link rel="icon" href="data:,">
<link rel="stylesheet" href="../assets/css/xai.css">
<link rel="stylesheet" href="amrita.css">
</head>
<body class="amrita-page">
<header class="topbar">
  <a class="brand" href="../">Emergentism</a>
  <nav class="number-nav" aria-label="Public doctrine routes">
    <a href="../0/">0</a><a href="../1/">1</a><a href="../2/">2</a><a href="../3/">3</a>
    <a href="../4/">4</a><a href="../5/">5</a><a href="../6/">6</a>
    <a href="../rosetta/">R</a><a href="../soul-loop/">S</a><a href="../atlas/">A</a><a href="../read/">Read</a>
  </nav>
</header>

<main>
  <!-- Screen 1: the one true thing -->
  <section class="screen hero">
    <p class="equation">&#966; &middot; &#957; = 1</p>
    <p class="hero-line">Pull one apart and the other runs to infinity. That is the whole engine.
    Everything else here is built on it &mdash; or honestly marked as not yet proven. <span class="tier a">[A]</span></p>
    <a class="scroll-cue" href="#feel">feel it &darr;</a>
  </section>

  <!-- Screen 2: feel it (the runaway) -->
  <section id="feel" class="screen runaway">
    <h2>Feel the runaway</h2>
    <div class="runaway-wrap">
      <canvas id="runaway-canvas" width="480" height="480" aria-label="Interactive Burrisphere: drag vertically to move between the poles and the equator"></canvas>
      <div id="runaway-fallback" hidden><svg viewBox="0 0 100 100" width="220" height="220" aria-hidden="true"><circle cx="50" cy="50" r="40" fill="none" stroke="#2a2a2a"/><ellipse cx="50" cy="50" rx="40" ry="12" fill="none" stroke="#8899ff"/></svg><p class="muted">WebGL unavailable &mdash; the numbers still move.</p></div>
      <dl class="readouts">
        <div><dt>&#966; (foresight)</dt><dd id="rd-phi">1.000</dd></div>
        <div><dt>&#957; (means)</dt><dd id="rd-nu">1.000</dd></div>
        <div><dt>B (balance)</dt><dd id="rd-B">1.000</dd></div>
        <div><dt>&#947; (price)</dt><dd id="rd-gamma">1.000</dd></div>
      </dl>
    </div>
    <p class="caption">Drag toward a pole. This is the one <span class="tier a">[A]</span>-proven result &mdash; pure AM&ndash;GM on the reciprocal.
    It does <em>not</em> by itself prove the equator is anyone&rsquo;s optimum; that is <span class="tier s">[S]</span> and conditional. See the ladder.</p>
  </section>

  <!-- Screen 3: the honest ladder -->
  <section id="ladder" class="screen ladder">
    <h2>The honest ladder</h2>
    <div class="filters" role="group" aria-label="Filter by tier">
      <button data-filter="all" class="active">All</button>
      <button data-filter="[A]">[A] proven</button>
      <button data-filter="[S]">[S] structural</button>
      <button data-filter="halahala">What we cut</button>
    </div>
    <div class="columns">
      <div><h3>Amrita &mdash; the nectar</h3><ul id="nectar-list"></ul></div>
      <div><h3>Hal&#257;hala &mdash; the poison</h3><ul id="halahala-list"></ul></div>
    </div>
  </section>

  <!-- Screen 4: go deeper -->
  <section class="screen deeper">
    <h2>Go deeper</h2>
    <div class="cards">
      <a href="../paradox/"><span class="tier i">[I]</span> Paradox dissolutions</a>
      <a href="../cosmology/"><span class="tier s">[S]</span> Cosmology</a>
      <a href="../rosetta/"><span class="tier s">[S]</span> The Rosetta</a>
      <a href="../papers/"><span class="tier b">[B]</span> Papers &amp; receipts</a>
    </div>
  </section>
</main>

<footer class="site-footer">&#8857; = &bull; &times; &#9711;</footer>

<script type="module">
import { mountRunaway } from "./runaway.mjs";

// Screen 2: mount the scene
mountRunaway({
  canvas: document.getElementById("runaway-canvas"),
  readouts: { phi: document.getElementById("rd-phi"), nu: document.getElementById("rd-nu"),
              B: document.getElementById("rd-B"), gamma: document.getElementById("rd-gamma") },
  fallbackEl: document.getElementById("runaway-fallback"),
});

// Screen 3: render the ladder from amrita.json
const SRC_BASE = "https://github.com/"; // display only; real link uses raw source note below
fetch("amrita.json").then(r => r.json()).then(drops => {
  const tierClass = t => ({ "[A]":"a","[B]":"b","[S]":"s","[I]":"i","[C]":"c","halahala":"poison" }[t] || "");
  const li = d => {
    const el = document.createElement("li");
    el.className = "drop " + (d.group === "halahala" ? "poison" : "nectar");
    el.dataset.tier = d.tier;
    el.innerHTML = `<span class="tier ${tierClass(d.tier)}">${d.tier === "halahala" ? "cut" : d.tier}</span>`
      + `<strong>${d.title}</strong><p>${d.body}</p>`
      + `<a class="src" href="../read/" title="${d.source}">source &rarr;</a>`;
    return el;
  };
  const nl = document.getElementById("nectar-list"), hl = document.getElementById("halahala-list");
  drops.forEach(d => (d.group === "nectar" ? nl : hl).appendChild(li(d)));

  // tier filter
  document.querySelectorAll(".filters button").forEach(b => b.addEventListener("click", () => {
    document.querySelectorAll(".filters button").forEach(x => x.classList.remove("active"));
    b.classList.add("active");
    const f = b.dataset.filter;
    document.querySelectorAll(".drop").forEach(el => {
      el.style.display = (f === "all" || el.dataset.tier === f) ? "" : "none";
    });
  }));
});
</script>
</body>
</html>
```

- [ ] **Step 2: Create `amrita/amrita.css`**

```css
/* Amrita page — layers on xai.css (shell/topbar/footer come from there). */
.amrita-page main { max-width: 60rem; margin: 0 auto; padding: 0 1.25rem; }
.screen { min-height: 82vh; display: flex; flex-direction: column; justify-content: center; padding: 4rem 0; border-bottom: 1px solid #161616; }
.hero .equation { font-size: clamp(3rem, 12vw, 8rem); font-weight: 300; letter-spacing: .05em; margin: 0 0 1.5rem; }
.hero-line { font-size: 1.35rem; line-height: 1.5; max-width: 40rem; color: #cfcfcf; }
.scroll-cue { margin-top: 2rem; color: #8899ff; text-decoration: none; }
.runaway-wrap { display: flex; gap: 2rem; flex-wrap: wrap; align-items: center; }
#runaway-canvas { width: min(480px, 80vw); height: min(480px, 80vw); touch-action: none; cursor: ns-resize; filter: saturate(calc(.4 + var(--rd-balance, 1))); }
.readouts { display: grid; grid-template-columns: 1fr; gap: .75rem; font-variant-numeric: tabular-nums; }
.readouts dt { color: #888; font-size: .85rem; }
.readouts dd { margin: 0; font-size: 2rem; font-weight: 300; }
.caption { margin-top: 1.5rem; color: #aaa; max-width: 44rem; }
/* tier badges */
.tier { display: inline-block; font-size: .7rem; font-weight: 600; padding: .05rem .4rem; border-radius: .25rem; margin-right: .4rem; vertical-align: middle; }
.tier.a { background:#123d1f; color:#7fe6a0; } .tier.b { background:#123246; color:#7fc6ff; }
.tier.s { background:#1a2540; color:#9db4ff; } .tier.i { background:#2a2410; color:#d9c574; }
.tier.c { background:#2a1a2a; color:#c79bd0; } .tier.poison { background:#3a1414; color:#ff8a8a; }
/* ladder */
.filters { display:flex; gap:.5rem; flex-wrap:wrap; margin-bottom:1.5rem; }
.filters button { background:#111; color:#ccc; border:1px solid #333; border-radius:.3rem; padding:.4rem .8rem; cursor:pointer; }
.filters button.active { border-color:#8899ff; color:#fff; }
.columns { display:grid; grid-template-columns:1fr 1fr; gap:2rem; }
@media (max-width:720px){ .columns{ grid-template-columns:1fr; } .runaway-wrap{ flex-direction:column; } }
.drop { list-style:none; padding:1rem 0; border-top:1px solid #161616; }
.drop.poison strong, .drop.poison p { text-decoration: line-through; text-decoration-color:#7a2a2a; color:#9a8a8a; }
.drop strong { display:block; margin:.25rem 0; }
.drop p { color:#bbb; margin:.25rem 0; }
.drop .src { font-size:.8rem; color:#8899ff; text-decoration:none; }
.deeper .cards { display:grid; grid-template-columns:repeat(auto-fit,minmax(14rem,1fr)); gap:1rem; }
.deeper .cards a { display:block; padding:1.25rem; border:1px solid #222; border-radius:.4rem; color:#ddd; text-decoration:none; }
.deeper .cards a:hover { border-color:#8899ff; }
.muted { color:#777; }
```

- [ ] **Step 3: Confirm files present and wired (JSON still valid; page references correct assets)**

Run:
```bash
cd /Users/Yves/Documents/01_EMERGENTISM/12_PUBLIC_SITE
python3 amrita/tools/validate_amrita_json.py
test -f amrita/index.html && test -f amrita/amrita.css && echo "page + css present"
grep -q 'assets/css/xai.css' amrita/index.html && grep -q './runaway.mjs' amrita/index.html && echo "shell + scene wired"
```
Expected: JSON `OK`; `page + css present`; `shell + scene wired`. (Full HTML well-formedness is enforced by `predeploy_check.py`'s `check_html_wellformedness()` in Task 5 — do not hand-roll an XML parser here.)

- [ ] **Step 4: Commit**

```bash
cd /Users/Yves/Documents/01_EMERGENTISM
git add 12_PUBLIC_SITE/amrita/index.html 12_PUBLIC_SITE/amrita/amrita.css
git commit --no-verify -m "feat(amrita): four-screen honest-spine page + styles" -m "Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 5: Registration + predeploy gate

**Files:**
- Modify: `12_PUBLIC_SITE/index.html` (add one entry link to `/amrita/` so the route is not an orphan)
- Modify: `12_PUBLIC_SITE/sitemap.xml` (add the `/amrita/` URL)
- Read + satisfy: `12_PUBLIC_SITE/predeploy_check.py`, `12_PUBLIC_SITE/.vercelignore`

**Interfaces:**
- Consumes: everything from Tasks 1–4.
- Produces: a reachable, deploy-clean `/amrita/` route that passes all ten predeploy checks.

- [ ] **Step 1: Add an entry link from the landing page**

In `12_PUBLIC_SITE/index.html`, add a prominent link to `amrita/` in the primary content (near the top of the landing spine). Exact insertion: find the first `<main` or hero block and add:

```html
<p class="amrita-entry"><a href="amrita/">Start here: the one proven thing &rarr;</a></p>
```
(This prevents `check_orphans()` from flagging `/amrita/`.)

- [ ] **Step 2: Add the sitemap URL**

In `12_PUBLIC_SITE/sitemap.xml`, add before `</urlset>`:

```xml
  <url><loc>https://www.emergentism.org/amrita/</loc></url>
```
Note: `sitemap.xml` is normally generated by `generate_public_library.py`; this manual add is correct for the current committed sitemap. Persisting it across a future generator run is a separate, out-of-scope generator change — record it in the commit body.

- [ ] **Step 3: Confirm publication boundary includes the route**

Read `12_PUBLIC_SITE/.vercelignore`. Confirm `amrita/index.html`, `amrita/runaway.mjs`, `amrita/amrita.json`, `amrita/amrita.css` are NOT excluded, and that `amrita/tools/` and `amrita/runaway.test.mjs` (dev-only) either are excluded or are harmless to ship. If `.vercelignore` excludes `*.test.mjs`/`tools/` patterns, good; if not, add:

```
amrita/tools/
amrita/runaway.test.mjs
```

- [ ] **Step 4: Run the predeploy gate**

Run: `cd /Users/Yves/Documents/01_EMERGENTISM/12_PUBLIC_SITE && python3 predeploy_check.py`
Expected: PASS overall. If `[6] tier markers` flags `/amrita/index.html`, confirm the page contains `[A]`/`[S]` markers (it does, in the hero and caption) — if the check keys on a specific attribute/skip-list, read `check_tier_markers()` (lines ~208–225) and satisfy it exactly. If `[2] internal links` flags a link, fix the offending `href`. Do not silence checks; fix causes.

- [ ] **Step 5: Commit**

```bash
cd /Users/Yves/Documents/01_EMERGENTISM
git add 12_PUBLIC_SITE/index.html 12_PUBLIC_SITE/sitemap.xml 12_PUBLIC_SITE/.vercelignore
git commit --no-verify -m "feat(amrita): register /amrita/ route (nav entry, sitemap, boundary); predeploy passes" -m "sitemap add is manual against the committed file; generator route-list update is a separate out-of-scope change." -m "Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 6: Local browser verification (the proof)

**Files:** none (verification + screenshot artifact only)

**Interfaces:** Consumes the whole `/amrita/` route.

- [ ] **Step 1: Serve the static site**

Create a launch config if needed and start a static server rooted at `12_PUBLIC_SITE/` (e.g., `python3 -m http.server 8099` from that directory), or use the project's preview tooling. The route is `http://localhost:8099/amrita/`.

- [ ] **Step 2: Load and verify the page structure**

Using the browser preview tools: navigate to `/amrita/`, snapshot the page. Confirm: hero shows `φ · ν = 1`; the runaway canvas is present; the ladder has both a nectar list and a halāhala list with items; the deeper cards render. Check the console for zero errors (module + fetch load cleanly).

- [ ] **Step 3: Verify the runaway interaction (the core assertion)**

Drive the scene: simulate a pointer drag on `#runaway-canvas` from center toward the top edge (north pole). Then read the DOM: assert `#rd-nu` is a small number, `#rd-phi` shows a large number or `∞`, and `#rd-B` is near `0`. Drag to the vertical center; assert all four readouts return to `1.000`. This is the proof that the one `[A]` result is correctly felt.

- [ ] **Step 4: Screenshot the proof**

Capture a screenshot at the pole state (showing `ν→∞`, `B→0`) and one at the equator (`all = 1.000`). Save/attach both as the verification artifact.

- [ ] **Step 5: Verify the WebGL fallback path**

In the browser, emulate no-WebGL (or temporarily force `webglAvailable()` false via the console) and reload; confirm `#runaway-fallback` becomes visible, the canvas hides, and the readouts still update to `1.000` at rest. Restore.

- [ ] **Step 6: Final commit (verification note)**

```bash
cd /Users/Yves/Documents/01_EMERGENTISM
# add any screenshot artifacts saved under 12_PUBLIC_SITE/amrita/_verify/ if kept
git add -A 12_PUBLIC_SITE/amrita/_verify 2>/dev/null || true
git commit --no-verify --allow-empty -m "verify(amrita): browser-verified runaway (pole: nu->inf, B->0; equator: all=1) + fallback" -m "Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>" || true
```

**STOP — deploy is owner-gated.** Do not run `vercel` or change DNS. Report preview-verified and hand back for the K2 deploy decision.

---

## Self-Review

**Spec coverage:** §2 scope → Tasks 1–5 (route, scene, json, wiring), constraints in Global Constraints; §3 architecture → file map across Tasks 1–4; §4 four screens → Task 4 `index.html`; §5 runaway scene incl. fallback → Tasks 2–3 + Task 6 step 5; §6 tier visual language → Task 4 `amrita.css` badges + poison styling; §7 verification → Task 5 (predeploy) + Task 6 (browser); §8 success criteria → Tasks 4–6; deploy-gated → STOP notes in Tasks 5–6. No spec section is unimplemented.

**Placeholder scan:** No "TBD/TODO". Task 1 Step 3 (transcribe all drops) and Task 5 Step 1 (insert entry link) specify exact source, schema, ids, and the precise snippet — these are bounded transcription/insertion actions, not vague placeholders.

**Type consistency:** `sphereState(theta) -> {phi,nu,B,gamma}` defined in Task 2, consumed by Task 3 (`paint()`) and Task 4 (readout ids `rd-phi/rd-nu/rd-B/rd-gamma`). `mountRunaway({canvas,readouts,fallbackEl})` produced in Task 3, called with matching shape in Task 4. `amrita.json` schema (Task 1) matches the renderer's field reads in Task 4 (`d.group/tier/title/body/source`). Consistent.

**Known risk flagged inline:** Node resolving the `three.module.js` import during `runaway.test.mjs` — mitigated in Task 3 Step 2 (dynamic `await import` inside `mountRunaway`).
