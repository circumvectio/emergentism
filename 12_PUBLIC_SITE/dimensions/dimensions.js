const page = window.DIMENSION_PAGE || {};
const canvas = document.querySelector(".dimension-canvas");
const visual = document.querySelector(".visual-panel");
const rootElement = document.documentElement;
const REDUCED_MOTION = !!(window.matchMedia
  && window.matchMedia("(prefers-reduced-motion: reduce)").matches);
const dimensionCommands = [
  { key: "/0", aliases: ["/0", "0", "d0", "titans"], label: "/0 · Titans", detail: "Ground / finity", href: "../0/" },
  { key: "/1", aliases: ["/1", "1", "d1", "one", "finity"], label: "/1 · The Special One", detail: "Reciprocal mirror", href: "../1/" },
  { key: "/2", aliases: ["/2", "2", "d2", "mu", "mu-limit"], label: "/2 · Mu-Limit", detail: "Line to plane", href: "../2/" },
  { key: "/3", aliases: ["/3", "3", "d3", "sphere", "bloch"], label: "/3 · Sphere", detail: "Closure surface", href: "../3/" },
  { key: "/4", aliases: ["/4", "4", "d4", "torus", "horn"], label: "/4 · Horn Torus", detail: "Energy overlap", href: "../4/" },
  { key: "/5", aliases: ["/5", "5", "d5", "burrisphere", "game"], label: "/5 · Burrisphere", detail: "Dual projection", href: "../5/" },
  { key: "/6", aliases: ["/6", "6", "d6", "convergence", "ccc"], label: "/6 · Convergence", detail: "Return to /0", href: "../6/" },
  { key: "R", aliases: ["rosetta", "r"], label: "Rosetta", detail: "Sevenfold map", href: "../rosetta/" },
  { key: "S", aliases: ["soul", "soul-loop"], label: "Soul Loop", detail: "Loop doctrine", href: "../soul-loop/" },
  { key: "A", aliases: ["atlas", "a"], label: "Atlas", detail: "Public atlas", href: "../atlas/" },
  { key: "EM", aliases: ["cascade", "emergence"], label: "Emergence", detail: "Animation", href: "../cascade.html" },
  { key: "SP", aliases: ["sphere-demo", "burri", "burri-sphere"], label: "Burri Sphere", detail: "Prototype", href: "../sphere.html" }
];

let THREE;
let OrbitControls;

function initThemeControls() {
  let stored = null;
  try {
    stored = window.localStorage.getItem("emergentism-theme");
  } catch (_) { /* storage blocked — default theme */ }
  const initial = stored || "dark";
  rootElement.dataset.theme = initial;

  const topbar = document.querySelector(".topbar");
  if (!topbar || topbar.querySelector(".theme-toggle")) return;

  const button = document.createElement("button");
  button.className = "theme-toggle";
  button.type = "button";

  function syncButton() {
    const theme = rootElement.dataset.theme === "light" ? "light" : "dark";
    button.textContent = theme === "light" ? "Dark" : "Light";
    button.setAttribute("aria-label", `Switch to ${button.textContent.toLowerCase()} theme`);
    button.setAttribute("aria-pressed", theme === "light" ? "true" : "false");
  }

  syncButton();
  button.addEventListener("click", () => {
    rootElement.dataset.theme = rootElement.dataset.theme === "light" ? "dark" : "light";
    try {
      window.localStorage.setItem("emergentism-theme", rootElement.dataset.theme);
    } catch (_) { /* storage blocked — theme stays per-page */ }
    syncButton();
  });
  topbar.append(button);
}

function initCommandPalette() {
  const topbar = document.querySelector(".topbar");
  if (!topbar || document.querySelector(".command-palette")) return;

  const trigger = document.createElement("button");
  trigger.className = "command-open";
  trigger.type = "button";
  trigger.textContent = "Command";
  trigger.setAttribute("aria-haspopup", "dialog");
  trigger.setAttribute("aria-expanded", "false");

  const palette = document.createElement("div");
  palette.className = "command-palette";
  palette.setAttribute("role", "dialog");
  palette.setAttribute("aria-label", "Route command palette");
  palette.innerHTML = `
    <div class="command-panel">
      <form>
        <label class="command-prefix" for="dimension-command-input">Command</label>
        <input class="command-input" id="dimension-command-input" type="text" autocomplete="off" spellcheck="false" placeholder="/0, /1, /5, rosetta, sphere" />
      </form>
      <div class="command-results"></div>
    </div>
  `;

  document.body.append(palette);
  topbar.append(trigger);

  const input = palette.querySelector(".command-input");
  const results = palette.querySelector(".command-results");

  function matches(command, query) {
    if (!query) return true;
    const q = query.toLowerCase();
    return command.aliases.some((alias) => alias.includes(q))
      || command.label.toLowerCase().includes(q)
      || command.detail.toLowerCase().includes(q);
  }

  function render() {
    const filtered = dimensionCommands.filter((command) => matches(command, input.value.trim())).slice(0, 8);
    results.innerHTML = filtered.length
      ? filtered.map((command, index) => `
        <a class="command-result${index === 0 ? " is-active" : ""}" href="${command.href}">
          <span>${command.key}</span>
          <div>
            <strong>${command.label}</strong>
            <small>${command.detail}</small>
          </div>
        </a>
      `).join("")
      : `<div class="command-empty">No command found.</div>`;
  }

  function openPalette(seed = "") {
    palette.classList.add("is-open");
    trigger.setAttribute("aria-expanded", "true");
    input.value = seed;
    render();
    requestAnimationFrame(() => {
      input.focus();
      input.select();
    });
  }

  function closePalette() {
    palette.classList.remove("is-open");
    trigger.setAttribute("aria-expanded", "false");
    input.value = "";
  }

  trigger.addEventListener("click", () => openPalette());
  input.addEventListener("input", render);
  palette.querySelector("form").addEventListener("submit", (event) => {
    event.preventDefault();
    const first = results.querySelector(".command-result");
    if (first) window.location.href = first.href;
  });
  palette.addEventListener("click", (event) => {
    if (event.target === palette) closePalette();
  });

  document.addEventListener("keydown", (event) => {
    const tagName = event.target && event.target.tagName;
    const isTyping = tagName === "INPUT" || tagName === "TEXTAREA";
    if (event.key === "/" && !isTyping) {
      event.preventDefault();
      openPalette("/");
    } else if (event.key === "Escape" && palette.classList.contains("is-open")) {
      closePalette();
      trigger.focus();
    }
  });
}

function fail(error) {
  console.error("Dimension spine WebGL failed", error);
  document.body.classList.add("webgl-failed");
}

function makeMaterial(color, opacity = 1, wireframe = false) {
  return new THREE.MeshBasicMaterial({
    color,
    transparent: opacity < 1,
    opacity,
    wireframe
  });
}

function setupCanvas2D() {
  const ctx = canvas.getContext("2d");
  if (!ctx) {
    throw new Error("2D canvas unavailable");
  }

  function resize() {
    const bounds = visual.getBoundingClientRect();
    const ratio = Math.min(window.devicePixelRatio || 1, 2);
    canvas.width = Math.max(1, Math.floor(bounds.width * ratio));
    canvas.height = Math.max(1, Math.floor(bounds.height * ratio));
    canvas.style.width = `${bounds.width}px`;
    canvas.style.height = `${bounds.height}px`;
    ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
    return bounds;
  }

  return { ctx, resize };
}

function drawTitanCalculator(time = 0) {
  const { ctx, resize } = setupCanvas2D();
  const tickValues = [-6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6];
  let bounds = resize();
  window.addEventListener("resize", () => {
    bounds = resize();
    if (REDUCED_MOTION) draw(0);
  });

  function draw(now) {
    const ink = "#fff";
    const muted = "#8f8f8f";
    const dim = "#5f5f5f";
    const width = bounds.width;
    const height = bounds.height;
    const t = now * 0.001;
    const cx = width / 2;
    const cy = height / 2;
    const pad = Math.max(28, Math.min(width, height) * 0.08);
    const left = pad;
    const right = width - pad;
    const axis = cy + Math.sin(t * 0.35) * 4;
    const span = right - left;
    const unit = span / 12;

    ctx.clearRect(0, 0, width, height);
    ctx.fillStyle = "#000";
    ctx.fillRect(0, 0, width, height);

    ctx.strokeStyle = "rgba(255,255,255,0.08)";
    ctx.lineWidth = 1;
    for (let x = left; x <= right + 1; x += unit) {
      ctx.beginPath();
      ctx.moveTo(x, pad);
      ctx.lineTo(x, height - pad);
      ctx.stroke();
    }
    for (let y = pad; y <= height - pad + 1; y += unit) {
      ctx.beginPath();
      ctx.moveTo(left, y);
      ctx.lineTo(right, y);
      ctx.stroke();
    }

    ctx.strokeStyle = "#fff";
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(left, axis);
    ctx.lineTo(right, axis);
    ctx.stroke();

    tickValues.forEach((s) => {
      const x = cx + s * unit;
      const major = s === 0 || Math.abs(s) === 3 || Math.abs(s) === 6;
      ctx.strokeStyle = s === 0 ? "#fff" : "rgba(255,255,255,0.42)";
      ctx.lineWidth = s === 0 ? 2 : 1;
      ctx.beginPath();
      ctx.moveTo(x, axis - (major ? 20 : 11));
      ctx.lineTo(x, axis + (major ? 20 : 11));
      ctx.stroke();

      if (major) {
        ctx.fillStyle = s === 0 ? ink : muted;
        ctx.font = "12px ui-monospace, SFMono-Regular, Menlo, monospace";
        ctx.textAlign = "center";
        ctx.fillText(s === 0 ? "1" : `e${s > 0 ? "+" : ""}${s}`, x, axis + 40);
      }
    });

    const pulse = 0.5 + Math.sin(t * 1.6) * 0.5;
    const reciprocalS = 3.1 + Math.sin(t * 0.6) * 1.25;
    const lx = cx - reciprocalS * unit;
    const rx = cx + reciprocalS * unit;

    ctx.setLineDash([8, 8]);
    ctx.strokeStyle = `rgba(245,245,245,${0.36 + pulse * 0.28})`;
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.moveTo(lx, axis - 72);
    ctx.bezierCurveTo(cx - unit * 1.7, axis - 132, cx + unit * 1.7, axis - 132, rx, axis - 72);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(lx, axis + 72);
    ctx.bezierCurveTo(cx - unit * 1.7, axis + 132, cx + unit * 1.7, axis + 132, rx, axis + 72);
    ctx.stroke();
    ctx.setLineDash([]);

    function marker(x, y, radius, color, label, sublabel) {
      ctx.fillStyle = color;
      ctx.beginPath();
      ctx.arc(x, y, radius, 0, Math.PI * 2);
      ctx.fill();
      ctx.strokeStyle = "#000";
      ctx.lineWidth = 2;
      ctx.stroke();
      ctx.fillStyle = "#f4f4f1";
      ctx.font = "700 18px ui-monospace, SFMono-Regular, Menlo, monospace";
      ctx.textAlign = "center";
      ctx.fillText(label, x, y - radius - 12);
      ctx.fillStyle = "#8f8f88";
      ctx.font = "12px ui-monospace, SFMono-Regular, Menlo, monospace";
      ctx.fillText(sublabel, x, y + radius + 22);
    }

    marker(lx, axis, 8, dim, "•", "s -> -∞");
    marker(cx, axis, 13, "#fff", "⊙", "s = log(1) = 0");
    marker(rx, axis, 8, muted, "○", "s -> +∞");

    // titles sit below the top HTML chip and above the bottom one — no overlap
    ctx.fillStyle = ink;
    ctx.font = "700 13px ui-monospace, SFMono-Regular, Menlo, monospace";
    ctx.textAlign = "left";
    ctx.fillText("Emergentism logarithmic calculator scale", left, pad + 44);
    ctx.fillStyle = muted;
    ctx.font = "12px ui-monospace, SFMono-Regular, Menlo, monospace";
    ctx.fillText("x ↦ 1/x mirrors s ↦ -s around unity", left, pad + 64);

    ctx.textAlign = "right";
    ctx.fillStyle = ink;
    ctx.fillText("⊙ = • × ○", right, height - pad - 48);
    ctx.fillStyle = muted;
    ctx.fillText("frame/register doctrine, not field arithmetic", right, height - pad - 28);

    if (!REDUCED_MOTION) requestAnimationFrame(draw);
  }

  if (REDUCED_MOTION) {
    draw(0);
  } else {
    requestAnimationFrame(draw);
  }
}

function line(points, color = 0xffffff, opacity = 1) {
  const geometry = new THREE.BufferGeometry().setFromPoints(points);
  const material = new THREE.LineBasicMaterial({
    color,
    transparent: opacity < 1,
    opacity
  });
  return new THREE.Line(geometry, material);
}

function ring(radius, color, opacity = 1) {
  const mesh = new THREE.Mesh(
    new THREE.TorusGeometry(radius, 0.01, 12, 160),
    makeMaterial(color, opacity)
  );
  mesh.rotation.x = Math.PI / 2;
  return mesh;
}

function addStars(scene) {
  const count = 340;
  const positions = new Float32Array(count * 3);
  for (let i = 0; i < count; i += 1) {
    const a = i * 2.399963;
    const r = 5.5 + (i % 37) * 0.055;
    positions[i * 3] = Math.cos(a) * r;
    positions[i * 3 + 1] = Math.sin(i * 0.77) * 2.7;
    positions[i * 3 + 2] = Math.sin(a) * r;
  }
  const geometry = new THREE.BufferGeometry();
  geometry.setAttribute("position", new THREE.BufferAttribute(positions, 3));
  scene.add(new THREE.Points(
    geometry,
    new THREE.PointsMaterial({ color: 0x606060, size: 0.018, transparent: true, opacity: 0.65 })
  ));
}

function createSphere(radius = 1.4, opacity = 0.22, wseg = 120, hseg = 64) {
  return new THREE.Mesh(
    new THREE.SphereGeometry(radius, wseg, hseg),
    makeMaterial(0xffffff, opacity, true)
  );
}

function createGridPlane(size = 3.8, lines = 13) {
  const group = new THREE.Group();
  const half = size / 2;
  for (let i = 0; i < lines; i += 1) {
    const p = -half + (size * i) / (lines - 1);
    group.add(line([
      new THREE.Vector3(-half, 0, p),
      new THREE.Vector3(half, 0, p)
    ], 0xb8b8b8, 0.45));
    group.add(line([
      new THREE.Vector3(p, 0, -half),
      new THREE.Vector3(p, 0, half)
    ], 0xb8b8b8, 0.45));
  }
  return group;
}

// A live readout overlay inside the visual panel (mono, bottom-left).
function makeReadout() {
  if (!visual) return null;
  if (getComputedStyle(visual).position === "static") visual.style.position = "relative";
  let el = visual.querySelector(".model-readout");
  if (!el) {
    el = document.createElement("div");
    el.className = "model-readout";
    el.style.cssText =
      "position:absolute;left:16px;top:16px;z-index:5;max-width:68%;" +
      "font:500 12px/1.6 'Roboto Mono',ui-monospace,Menlo,monospace;" +
      "color:var(--text,#F3F4F6);pointer-events:none;letter-spacing:.01em;white-space:pre-line;" +
      "background:color-mix(in srgb, #050505 66%, transparent);padding:9px 12px;" +
      "border:1px solid rgba(255,255,255,.09);border-radius:9px;backdrop-filter:blur(4px)";
    visual.appendChild(el);
  }
  return el;
}

// Morphing horn torus driven by RAPIDITY. Outer radius is fixed; as rapidity w
// grows, v/c = tanh(w) -> 1 and the central MOUTH (R - rt) contracts: an open
// ring torus closes to a horn (R = rt, mouth = 0) and then a spindle (R < rt)
// whose interior overlaps at the axis — the centre accumulating mass/momentum
// while the throat pinches shut. A model of how reality folds at the limit.
function makeMorphTorus(outer = 1.7, rings = 48, seg = 18, color = 0xffffff) {
  const verts = [];
  for (let i = 0; i < rings; i++) {            // meridian rings (around the tube)
    const u = (i / rings) * Math.PI * 2;
    for (let j = 0; j < seg; j++) {
      verts.push({ u, v: (j / seg) * Math.PI * 2 }, { u, v: ((j + 1) / seg) * Math.PI * 2 });
    }
  }
  for (let j = 0; j < seg; j++) {              // longitude rings (around the axis)
    const v = (j / seg) * Math.PI * 2;
    for (let i = 0; i < rings; i++) {
      verts.push({ u: (i / rings) * Math.PI * 2, v }, { u: ((i + 1) / rings) * Math.PI * 2, v });
    }
  }
  const arr = new Float32Array(verts.length * 3);
  const geom = new THREE.BufferGeometry();
  geom.setAttribute("position", new THREE.BufferAttribute(arr, 3));
  const mesh = new THREE.LineSegments(
    geom,
    new THREE.LineBasicMaterial({ color, transparent: true, opacity: 0.34 })
  );
  // f = tube fraction: 0.5 is the HORN (R = rt, mouth = 0, throat closed to a
  // point); f < 0.5 an open ring; f > 0.5 a spindle whose interior overlaps.
  function setF(f) {
    f = Math.max(0.05, Math.min(0.94, f));
    const rt = outer * f;                // tube (minor) radius
    const R = outer * (1 - f);           // axis-to-tube radius
    for (let k = 0; k < verts.length; k++) {
      const { u, v } = verts[k];
      const rad = R + rt * Math.cos(v);
      arr[k * 3] = rad * Math.cos(u);
      arr[k * 3 + 1] = rt * Math.sin(v);
      arr[k * 3 + 2] = rad * Math.sin(u);
    }
    geom.attributes.position.needsUpdate = true;
    return { rt, R, mouth: R - rt };
  }
  setF(0.5);                             // start as a HORN torus
  return { mesh, setF };
}

function makeMarker(position, color = 0xffffff, size = 0.055) {
  const marker = new THREE.Mesh(
    new THREE.SphereGeometry(size, 20, 20),
    makeMaterial(color, 1)
  );
  marker.position.copy(position);
  return marker;
}

function buildScene(mode, scene) {
  const root = new THREE.Group();
  scene.add(root);
  const dyn = []; // per-frame update fns (morphing / orbiting models)

  const axis = line([
    new THREE.Vector3(0, -1.8, 0),
    new THREE.Vector3(0, 1.8, 0)
  ], 0x8a8a8a, 0.7);
  root.add(axis);

  if (mode === "titans") {
    root.add(ring(1.18, 0xb8b8b8, 0.9));
    root.add(ring(0.62, 0xffffff, 0.65));
    root.add(makeMarker(new THREE.Vector3(-1.25, 0, 0), 0x707070, 0.09));
    root.add(makeMarker(new THREE.Vector3(0, 0, 0), 0xffffff, 0.12));
    root.add(makeMarker(new THREE.Vector3(1.25, 0, 0), 0xb8b8b8, 0.09));
    root.add(line([
      new THREE.Vector3(-1.25, 0, 0),
      new THREE.Vector3(1.25, 0, 0)
    ], 0xffffff, 0.8));
  }

  if (mode === "logline") {
    // SUDA'S NUMBER LINE, READ IN LOG COORDINATES. s = log x maps the positive
    // ray onto the whole line: 0 recedes to −∞ on the left, ∞ to +∞ on the
    // right, and the ONE sits at the exact centre — the unique fixed point of
    // inversion I(x) = 1/x, which in log coordinates is the mirror s ↦ −s.
    // A live reciprocal pair (x, 1/x) folds through the One — their product is
    // pinned to 1. The energy E = (ln x)² is the well whose unique minimum is
    // the One. Three charts, one centre: x · s = log x · u = (x−1)/(x+1).
    const SC = 0.62;                                  // scene units per log₂ step
    const EXT = 3.4 * SC;
    root.add(line([new THREE.Vector3(-EXT - 0.5, 0, 0), new THREE.Vector3(EXT + 0.5, 0, 0)], 0xffffff, 0.85));
    for (let k = -3; k <= 3; k += 1) {                // ticks at x = 2^k — log-evenly spaced
      root.add(line([new THREE.Vector3(k * SC, -0.07, 0), new THREE.Vector3(k * SC, 0.07, 0)],
        k === 0 ? 0xffeb3b : 0x777777, k === 0 ? 0.95 : 0.7));
    }
    // the Titans frame the line: • 0 and ○ ∞ are the two limits (at infinite
    // log distance), ⊙ 1 is the centre — gold, the mirror axis itself
    root.add(makeMarker(new THREE.Vector3(-EXT - 0.5, 0, 0), 0x606060, 0.055)); // • toward 0
    root.add(makeMarker(new THREE.Vector3(EXT + 0.5, 0, 0), 0xc8c8c8, 0.055)); // ○ toward ∞
    const one = ring(0.1, 0xffeb3b, 0.95);
    one.rotation.x = 0; root.add(one);                // ⊙ — the One, facing the viewer
    root.add(line([new THREE.Vector3(0, -0.55, 0), new THREE.Vector3(0, 1.95, 0)], 0xffeb3b, 0.28)); // the mirror axis
    // the energy well E = (ln x)² — drawn over the line, minimum exactly at 1
    const well = [];
    for (let s = -3.3; s <= 3.301; s += 0.1) well.push(new THREE.Vector3(s * SC, 0.17 * s * s, 0));
    root.add(line(well, 0x9a9a9a, 0.5));
    const xPt = makeMarker(new THREE.Vector3(SC, 0, 0), 0xffeb3b, 0.075);     // x
    const invPt = makeMarker(new THREE.Vector3(-SC, 0, 0), 0xffffff, 0.075);  // 1/x — the mirror
    const ePt = makeMarker(new THREE.Vector3(SC, 0.17, 0), 0xb8b8b8, 0.05);   // E(x) on the well
    const arc = line([new THREE.Vector3(0, 0, 0)], 0xffeb3b, 0.55);           // the inversion fold
    root.add(xPt); root.add(invPt); root.add(ePt); root.add(arc);

    const readout = makeReadout();
    if (readout) readout.style.whiteSpace = "pre-line";
    dyn.push(function (t) {
      const s = 2.9 * Math.sin(t * 0.45);             // sweep in log coordinates
      const x = Math.pow(2, s);
      xPt.position.set(s * SC, 0, 0);
      invPt.position.set(-s * SC, 0, 0);
      ePt.position.set(s * SC, 0.17 * s * s, 0);
      const R = Math.abs(s) * SC;                     // the fold x → 1/x, under the line
      if (R > 0.02) {
        const pts = [];
        for (let i = 0; i <= 40; i += 1) {
          const a = Math.PI * i / 40;
          pts.push(new THREE.Vector3(R * Math.cos(a), -0.5 * R * Math.sin(a), 0));
        }
        arc.geometry.setFromPoints(pts);
      } else {
        arc.geometry.setFromPoints([new THREE.Vector3(0, 0, 0), new THREE.Vector3(0, 0, 0)]);
      }
      const u = (x - 1) / (x + 1);
      const E = Math.pow(Math.log(x), 2);
      if (readout) readout.textContent =
        "SUDA'S LINE · in log coordinates the ONE is the centre\n" +
        "x = " + x.toFixed(2) + "   1/x = " + (1 / x).toFixed(2) + "   x · 1/x = 1\n" +
        "s = log₂ x = " + s.toFixed(2) + "   mirror s ↦ −s   E = (ln x)² = " + E.toFixed(2) + " (min at 1)\n" +
        "three charts · one centre:  x   ·   s = log x   ·   u = (x−1)/(x+1) = " + u.toFixed(2);
    });
  }

  if (mode === "muLimit") {
    root.add(line([
      new THREE.Vector3(-2.4, 0, 0),
      new THREE.Vector3(2.4, 0, 0)
    ], 0xffffff, 0.9));
    root.add(createGridPlane(3.2, 11));
    root.add(line([
      new THREE.Vector3(-1.8, 0, 0),
      new THREE.Vector3(0, 1.6, 0),
      new THREE.Vector3(1.8, 0, 0)
    ], 0xb8b8b8, 0.9));
  }

  if (mode === "bloch") {
    // The Bloch / Riemann sphere STANDS ON the complex plane (tangent at 0,
    // the south pole) and projects DOWNWARD: a straight ray from ∞ (north
    // pole) through the surface point P lands on the floor at 2r·cot(θ/2) —
    // the same tangent-plane stereographic projection the Burrisphere dualises.
    // The equator's shadow on the floor is the unit circle (φ = 1).
    const r = 1.0;
    const N = new THREE.Vector3(0, r, 0), Sp = new THREE.Vector3(0, -r, 0);
    const floor = createGridPlane(8.0, 23); floor.position.y = -r; root.add(floor);
    root.add(createSphere(r, 0.26));
    root.add(ring(r, 0xffffff, 0.85));                          // the equator (φ = 1 up here)
    const unitC = ring(2 * r, 0xffeb3b, 0.55);                  // its shadow: the unit circle on ℂ
    unitC.position.y = -r; root.add(unitC);
    root.add(makeMarker(N, 0xb8b8b8, 0.07));                    // ∞
    root.add(makeMarker(Sp, 0x707070, 0.07));                   // 0 — where the sphere touches ℂ
    const th = Math.PI * 80 / 180;                              // P just above the equator → φ just over 1
    const P0 = new THREE.Vector3(r * Math.sin(th), r * Math.cos(th), 0);
    const land = new THREE.Vector3(2 * r / Math.tan(th / 2), -r, 0); // 2r·cot(θ/2), on the floor
    root.add(line([N, land], 0xffeb3b, 0.9));                   // straight ray ∞ → P → ℂ
    root.add(makeMarker(P0, 0xffffff, 0.08));
    root.add(makeMarker(land, 0xffeb3b, 0.07));
  }

  if (mode === "horn") {
    // The horn torus STANDS ON the complex plane the Riemann sphere stands on.
    // At rest (rapidity w = 0) it is a HORN: the throat closes to a single point
    // = the relative centre, in motion relative to everything else (the fixed
    // plane / unit circle |z|=1, Suda's self-dual centre x=1). A LOGARITHMIC
    // rapidity slider drives it: rapidity is the log of the Doppler factor, so
    // near the ends the velocity goes to the c limit and the throat opens to a
    // spindle — β can no longer grow, so the energy becomes MASS (E = γ m c²).
    root.add(createGridPlane(6.4, 21));                          // the complex plane
    root.add(ring(1.0, 0xffeb3b, 0.7));                          // unit circle |z|=1  (x=1, Suda)
    root.add(line([new THREE.Vector3(-3.1, 0, 0), new THREE.Vector3(3.1, 0, 0)], 0x555555, 0.55));
    root.add(line([new THREE.Vector3(0, 0, -3.1), new THREE.Vector3(0, 0, 3.1)], 0x555555, 0.55));
    const torus = makeMorphTorus(1.7, 104, 30, 0xffffff);       // high-resolution mesh
    root.add(torus.mesh);
    const relCentre = ring(0.12, 0xffeb3b, 0.95);               // the relative centre on the plane (a ring, no dot)
    root.add(relCentre);

    const readout = makeReadout();
    if (readout) readout.style.whiteSpace = "normal";
    const W_MAX = 4.5;                                          // ends: v/c -> 0.9998, γ -> ~45
    const G_MAX = Math.cosh(W_MAX);
    let userActive = false, slider = null;
    if (visual) {
      const wrap = document.createElement("div");
      wrap.className = "model-slider";
      wrap.style.cssText = "position:absolute;left:16px;right:16px;bottom:16px;z-index:6;display:flex;" +
        "align-items:center;gap:10px;font:700 11px/1 'Roboto Mono',ui-monospace,monospace;color:#9CA3AF;letter-spacing:.04em";
      const lo = document.createElement("span"); lo.textContent = "←c"; lo.style.color = "#42A5F5";
      const hi = document.createElement("span"); hi.textContent = "c→"; hi.style.color = "#42A5F5";
      const mid = document.createElement("span"); mid.textContent = "rest"; mid.style.color = "#FFEB3B";
      slider = document.createElement("input");
      slider.type = "range"; slider.min = "-100"; slider.max = "100"; slider.step = "1"; slider.value = "0";
      slider.setAttribute("aria-label", "rapidity (logarithmic — rest at centre, light speed at the ends)");
      slider.style.cssText = "flex:1;accent-color:#FFEB3B;cursor:pointer;height:4px";
      slider.addEventListener("input", () => { userActive = true; });
      wrap.append(lo, slider, hi);
      visual.appendChild(wrap);
      visual.dataset.midLabel = "rest";
    }
    function bar(frac, color) {
      const w = Math.max(0, Math.min(1, frac)) * 100;
      return "<span style='display:inline-block;width:74px;height:7px;border:1px solid #3a3a3a;border-radius:4px;vertical-align:-1px;overflow:hidden'>" +
        "<span style='display:block;height:100%;width:" + w.toFixed(0) + "%;background:" + color + "'></span></span>";
    }
    dyn.push(function (t) {
      let w;
      if (userActive && slider) {
        w = (parseFloat(slider.value) / 100) * W_MAX;            // slider is LINEAR in rapidity = LOG in velocity
      } else {
        w = Math.sin(t * 0.26) * W_MAX * 0.82;                  // gentle auto-demo until the user grabs the slider
        if (slider) slider.value = String(Math.round((w / W_MAX) * 100));
      }
      const vc = Math.tanh(w);                                  // β = v/c — saturates at ±1
      const aB = Math.abs(vc);
      const gamma = Math.cosh(w);                               // γ — the relativistic-mass factor
      const k = Math.exp(w);                                    // Doppler factor = e^w (the log line: w = ln k)
      // EXACT morph law: f = γ/(γ+1), so the mouth ratio R/rt = (1−f)/f = 1/γ
      // = B = dτ/dt — the throat IS the rate of lived (proper) time. At rest
      // γ=1 → R=rt (HORN); as β→1, γ→∞ and R→0 asymptotically — the overlap
      // completes only in the limit, and the torus RESOLVES INTO A SPHERE —
      // the Burrisphere — which then projects upward.
      const f = gamma / (gamma + 1);
      const g = torus.setF(f);
      torus.mesh.material.opacity = 0.3 + 0.06 * aB;
      // the relative centre moves on the complex plane (log-compressed real axis)
      const px = 2.5 * Math.tanh(w / 2.2);
      relCentre.position.set(px, 0, 0);
      relCentre.scale.setScalar(1 + 1.4 * aB);
      root.rotation.y += 0.0024;
      const moving = aB > 0.02;
      if (readout) readout.innerHTML =
        "<div style='color:#FFEB3B;font-weight:700;letter-spacing:.07em;margin-bottom:6px'>RELATIVE MOTION ON THE COMPLEX PLANE</div>" +
        "rapidity w = " + w.toFixed(2) + " &nbsp;<span style='color:#6b7280'>= ln(Doppler)</span><br>" +
        "β = v/c &nbsp;" + bar(aB, "#42A5F5") + " " + vc.toFixed(4) + "<br>" +
        "γ = cosh w = " + gamma.toFixed(1) + " &nbsp;<span style='color:#9CA3AF'>E = γmc² · m/m₀ = γ</span> " + bar(gamma / G_MAX, "#FFEB3B") + "<br>" +
        "mouth R/r = 1/γ = " + (1 / gamma).toFixed(3) + " &nbsp;<span style='color:#9CA3AF'>= dτ/dt — the rate of lived time</span><br>" +
        (!moving
          ? "<span style='color:#FFEB3B'>at rest · HORN torus (γ=1, R=r) — E = mc², all energy is rest mass</span>"
          : gamma > 20
            ? "<span style='color:#FFEB3B'>R→0 · proper time freezes → resolves as the BURRISPHERE (projects upward)</span>"
            : "<span style='color:#9CA3AF'>SPINDLE · β saturates at c · the work of acceleration becomes <b style='color:#FFEB3B'>mass-energy</b></span>");
    });
  }

  if (mode === "burrisphere") {
    // THE DUAL TANGENT-PLANE STEREOGRAPHIC PROJECTION — the real geometry.
    // The sphere is sandwiched between two copies of the SAME complex plane:
    // the floor touches it at 0 (south pole), the top plane touches it at ∞
    // (north pole). From ∞ a straight ray through P lands DOWN on the floor at
    // radius 2r·cot(θ/2) = 2r·φ; from 0 a straight ray through P lands UP on
    // the top plane at 2r·tan(θ/2) = 2r·ν. Both rays pass through P — the two
    // projections meet ON the sphere. φ·ν = 1 throughout. The unit circles
    // (radius 2r on each plane) are the equator's two shadows: the god/demon
    // boundary. As ψ rotates while θ sweeps, both landings SPIRAL through the
    // quadrants — reciprocal radii, crossing their unit circles together.
    const r = 1.0;
    const N = new THREE.Vector3(0, r, 0);                            // ○ ∞ — Brahmā's station: the top plane touches here
    const S = new THREE.Vector3(0, -r, 0);                           // • 0 — Śiva's station: the floor touches here
    const GOD = 0xffeb3b, DEMON = 0xd23b3b;
    const U = 2 * r;                                                 // unit-circle radius on a tangent plane

    root.add(createSphere(r, 0.22));
    root.add(ring(r, GOD, 0.8));                                     // the equator — god/demon boundary on the sphere
    [0.45, 0.8].forEach((y) => {
      const lat = ring(Math.sqrt(r * r - y * y), 0x666666, 0.3);
      lat.position.y = y; root.add(lat);
      const m = lat.clone(); m.position.y = -y; root.add(m);
    });

    // the two tangent copies of the same complex plane (floor at 0, top at ∞)
    [-r, r].forEach((y) => {
      const g = createGridPlane(9.0, 25); g.position.y = y; root.add(g);
      const u = ring(U, GOD, 0.6); u.position.y = y; root.add(u);    // unit circle = the equator's shadow
      root.add(line([new THREE.Vector3(-4.5, y, 0), new THREE.Vector3(4.5, y, 0)], 0x555555, 0.5));
      root.add(line([new THREE.Vector3(0, y, -4.5), new THREE.Vector3(0, y, 4.5)], 0x555555, 0.5));
    });
    root.add(makeMarker(N, 0xc8c8c8, 0.07));
    root.add(makeMarker(S, 0x8a8a8a, 0.07));

    // the four operators, resident on the ∞-plane (the ν-chart): gods have
    // ν < 1 → INSIDE the unit circle, clustered near ∞; demons have ν > 1 →
    // OUTSIDE. One quadrant each, per the complex-plane game.
    [[0.9, 0.9, GOD], [-0.9, 0.9, GOD], [-2.2, -2.2, DEMON], [2.2, -2.2, DEMON]]
      .forEach((o) => root.add(makeMarker(new THREE.Vector3(o[0], r, o[1]), o[2], 0.06)));

    // THE TITANS ARE THE STATIONS OF THE GEOMETRY ITSELF — proto-reality,
    // the {0, 1, ∞} scaffold the game is played on: Śiva • = 0 (the floor
    // touch, S above), Brahmā ○ = ∞ (the top touch, N above), and Viṣṇu ⊙ = 1
    // — the centre, with the gold equator as the circle of his own glyph.
    root.add(makeMarker(new THREE.Vector3(0, 0, 0), 0xffeb3b, 0.055)); // ⊙ Viṣṇu — the One at the centre

    const pMark = makeMarker(new THREE.Vector3(r, 0, 0), 0xffffff, 0.085); // P — where the two rays meet
    const rayDown = line([N, new THREE.Vector3(U, -r, 0)], GOD, 0.8);  // ∞ → P → floor: lands at 2r·φ
    const rayUp = line([S, new THREE.Vector3(U, r, 0)], GOD, 0.8);     // 0 → P → top: lands at 2r·ν
    const phiPt = makeMarker(new THREE.Vector3(U, -r, 0), GOD, 0.07);  // the φ landing (floor)
    const nuPt = makeMarker(new THREE.Vector3(U, r, 0), GOD, 0.07);    // the ν landing (top)
    root.add(pMark); root.add(rayDown); root.add(rayUp); root.add(phiPt); root.add(nuPt);

    // the two spiral trails traced by the landings — reciprocal radii
    const TRAIL = 360, phiTrail = [], nuTrail = [];
    const phiLine = line([new THREE.Vector3(U, -r, 0)], 0xffeb3b, 0.38);
    const nuLine = line([new THREE.Vector3(U, r, 0)], 0xffeb3b, 0.38);
    root.add(phiLine); root.add(nuLine);

    const readout = makeReadout();
    if (readout) { readout.style.whiteSpace = "pre-line"; readout.style.top = "auto"; readout.style.bottom = "14px"; }
    const quadName = ["I", "II", "III", "IV"];
    dyn.push(function (t) {
      const psi = t * 1.6;                                           // azimuth rotates
      const theta = Math.PI / 2 + 0.70 * Math.sin(t * 0.23);         // the angle sweeps across the equator
      const phi = 1 / Math.tan(theta / 2);                           // cot(θ/2)
      const nu = Math.tan(theta / 2);                                // 1/φ
      const cps = Math.cos(psi), sps = Math.sin(psi), sT = Math.sin(theta);
      const P = new THREE.Vector3(r * sT * cps, r * Math.cos(theta), r * sT * sps);
      pMark.position.copy(P);
      // the TRUE landings: collinear with (∞,P) and (0,P) by the half-angle identities
      const Lphi = new THREE.Vector3(U * phi * cps, -r, U * phi * sps);
      const Lnu = new THREE.Vector3(U * nu * cps, r, U * nu * sps);
      phiPt.position.copy(Lphi);
      nuPt.position.copy(Lnu);
      rayDown.geometry.setFromPoints([N, Lphi]);                     // straight through P
      rayUp.geometry.setFromPoints([S, Lnu]);                        // straight through P
      const isGod = phi > 1;                                         // P above the equator
      const col = isGod ? GOD : DEMON;
      [pMark, phiPt, nuPt].forEach((m) => m.material.color.setHex(col));
      rayDown.material.color.setHex(col);
      rayUp.material.color.setHex(col);
      phiTrail.push(Lphi.clone()); if (phiTrail.length > TRAIL) phiTrail.shift();
      nuTrail.push(Lnu.clone()); if (nuTrail.length > TRAIL) nuTrail.shift();
      phiLine.geometry.setFromPoints(phiTrail);
      nuLine.geometry.setFromPoints(nuTrail);
      root.rotation.y += 0.0016;
      const q = quadName[Math.floor((((psi % (2 * Math.PI)) + 2 * Math.PI) % (2 * Math.PI)) / (Math.PI / 2)) % 4];
      const opName = isGod
        ? (cps < 0 ? "Kṛṣṇa L3 · give" : "Arjuna L4 · give")
        : (cps < 0 ? "Kali L1 · take" : "Kālī L2 · take");
      if (readout) readout.textContent =
        "DUAL STEREOGRAPHIC PROJECTION · the two rays meet at P\n" +
        "θ = " + (theta * 180 / Math.PI).toFixed(0) + "°   φ = " + phi.toFixed(2) + "   ν = " + nu.toFixed(2) + "   φ·ν = 1 (mass-shell)   E/mc² = (φ+ν)/2 = " + ((phi + nu) / 2).toFixed(2) + "\n" +
        "quadrant " + q + " · " + opName + " · " + (isGod ? "GOD-move (φ > 1)" : "DEMON-move (φ < 1)") + "\n" +
        "Titans {0, 1, ∞} — Śiva • the 0-touch · Viṣṇu ⊙ the centre · Brahmā ○ the ∞-touch";
    });
  }

  if (mode === "convergence") {
    root.add(createSphere(1.25, 0.18));
    root.add(ring(1.25, 0xffffff, 0.9));
    root.add(ring(0.86, 0xb8b8b8, 0.7));
    root.add(ring(0.48, 0x707070, 0.65));
    root.add(line([
      new THREE.Vector3(-1.7, -0.8, 0),
      new THREE.Vector3(0, 0, 0),
      new THREE.Vector3(1.7, 0.8, 0)
    ], 0xffffff, 0.9));
  }

  return { root, update: (t) => dyn.forEach((f) => f(t)) };
}

async function boot() {
  initThemeControls();
  initCommandPalette();

  if (!canvas || !visual) return;
  try {
    if (new URLSearchParams(window.location.search).has("forceWebGLFallback")) {
      throw new Error("Forced WebGL fallback");
    }

    if (page.animationMode === "titans") {
      drawTitanCalculator();
      return;
    }

    THREE = await import("three");
    ({ OrbitControls } = await import("three/addons/controls/OrbitControls.js"));

    const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(45, 1, 0.1, 100);
    camera.position.set(0, 0.35, 4.7);

    const controls = new OrbitControls(camera, canvas);
    controls.enableDamping = true;
    controls.enablePan = false;
    controls.enableZoom = false;
    // models that spin their own root don't also get camera auto-rotate
    const selfRotating = page.animationMode === "burrisphere" || page.animationMode === "horn";
    controls.autoRotate = !REDUCED_MOTION && !selfRotating;
    controls.autoRotateSpeed = page.autoRotateSpeed || 0.35;
    if (page.animationMode === "burrisphere") {
      // the sphere sits sandwiched between the two tangent planes (floor = 0,
      // top = ∞) — stand near the floor and look UP toward infinity
      camera.position.set(0, -0.7, 9.6);
      controls.target.set(0, 0.7, 0);
      controls.update();
    }
    if (page.animationMode === "bloch") {
      // resting sphere + tangent floor at -r; landing reaches 2r·cot(θ/2)
      camera.position.set(0, 0.4, 5.8);
      controls.update();
    }
    if (page.animationMode === "logline") {
      // the line spans ±2.6 with the energy well above — front view, framed wide
      camera.position.set(0, 0.55, 5.9);
      controls.target.set(0, 0.45, 0);
      controls.update();
    }

    addStars(scene);
    const { root, update } = buildScene(page.animationMode, scene);

    function resize() {
      const bounds = visual.getBoundingClientRect();
      renderer.setSize(bounds.width, bounds.height, false);
      camera.aspect = bounds.width / Math.max(bounds.height, 1);
      camera.updateProjectionMatrix();
    }

    function animate(time) {
      const t = time * 0.001;
      if (page.animationMode === "titans") {
        root.rotation.z = Math.sin(t * 0.6) * 0.08;
      } else if (page.animationMode === "muLimit") {
        root.rotation.x = Math.sin(t * 0.42) * 0.18;
      } else if (page.animationMode === "bloch") {
        root.scale.setScalar(1 + Math.sin(t * 0.6) * 0.025);
      } else if (page.animationMode === "convergence") {
        root.rotation.z = t * 0.08;
        root.scale.setScalar(1 + Math.sin(t * 0.7) * 0.04);
      }
      update(t); // morphing / orbiting models (horn, burrisphere)

      controls.update();
      renderer.render(scene, camera);
      requestAnimationFrame(animate);
    }

    if (REDUCED_MOTION) {
      // static render: one frame now, re-render only on interaction/resize
      update(1.2); // pose the morphing/orbiting models at a representative frame
      resize();
      renderer.render(scene, camera);
      controls.addEventListener("change", () => renderer.render(scene, camera));
      window.addEventListener("resize", () => {
        resize();
        renderer.render(scene, camera);
      });
      return;
    }

    resize();
    window.addEventListener("resize", resize);
    requestAnimationFrame(animate);
  } catch (error) {
    fail(error);
  }
}

boot();
