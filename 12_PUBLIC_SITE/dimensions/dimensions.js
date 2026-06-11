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

function createSphere(radius = 1.4, opacity = 0.22) {
  return new THREE.Mesh(
    new THREE.SphereGeometry(radius, 64, 36),
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
  function setVC(vc) {
    const f = 0.26 + 0.50 * vc;          // tube fraction: 0.26 ring -> 0.5 horn -> ~0.76 spindle
    const rt = outer * f;                // tube (minor) radius — swells with rapidity
    const R = outer * (1 - f);           // axis-to-tube radius — shrinks
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
  setVC(0);
  return { mesh, setVC };
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

  if (mode === "riemann") {
    // Stereographic projection from the north pole (∞): the 45° ray through
    // the equator point lands exactly ON the plane at radius 1 — the unit
    // made visible. The ray ends at the plane; it does not overshoot.
    const r = 1.35;
    const N = new THREE.Vector3(0, r, 0);
    const S = new THREE.Vector3(0, -r, 0);
    const E = new THREE.Vector3(r, 0, 0); // equator point = its own projection
    root.add(createGridPlane(4.6, 15));
    root.add(createSphere(r, 0.32));
    root.add(ring(r, 0xffffff, 1));
    root.add(makeMarker(S, 0x707070, 0.08));
    root.add(makeMarker(E, 0xffffff, 0.11));
    root.add(makeMarker(N, 0xb8b8b8, 0.08));
    root.add(line([N, E], 0xffffff, 0.95));
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
    const plane = createGridPlane(3.3, 13);
    plane.rotation.x = 0.45;
    root.add(plane);
    root.add(createSphere(1.35, 0.26));
    root.add(ring(1.35, 0xffffff, 0.8));
  }

  if (mode === "horn") {
    const torus = makeMorphTorus(1.7, 48, 18, 0xffffff);
    root.add(torus.mesh);
    // the central core: gains mass/momentum as the mouth pinches shut
    const core = makeMarker(new THREE.Vector3(0, 0, 0), 0xffd24a, 0.06);
    root.add(core);
    const readout = makeReadout();
    dyn.push(function (t) {
      // rapidity sweeps up toward the light-speed limit, then resets (a loop)
      const w = (t * 0.32) % 3.0;                 // rapidity 0..3
      const vc = Math.tanh(w);                    // v/c = tanh(w) -> ~0.995
      const gamma = Math.cosh(w);                 // time dilation factor
      const g = torus.setVC(vc);
      const mass = 1 + (gamma - 1) * 0.12;        // centre swells with γ
      core.scale.setScalar(Math.min(mass, 3.4));
      core.material.opacity = Math.min(0.35 + vc * 0.65, 1);
      root.rotation.y += 0.004;
      if (readout) readout.textContent =
        "rapidity  w = " + w.toFixed(2) + "\n" +
        "v / c     = " + vc.toFixed(3) + "   (β)\n" +
        "γ = cosh w = " + gamma.toFixed(2) + "   time dilation\n" +
        "mouth R−r = " + g.mouth.toFixed(2) +
          (g.mouth > 0.02 ? "   ring" : g.mouth < -0.02 ? "   spindle · interior overlaps" : "   horn · throat closed");
    });
  }

  if (mode === "burrisphere") {
    // The dual stereographic projection, ORBITING. The meeting point P circles
    // the sphere; its φ = cot(θ/2) projection sweeps the four quadrants of the
    // equatorial plane. The unit circle (radius = the sphere radius) is the
    // god/demon boundary: φ > 1 (projection OUTSIDE the unit circle, P above the
    // equator) is a GOD-move; φ < 1 (INSIDE, P below) is a DEMON-move. φ·ν = 1
    // throughout. Valence is on the move's position, not on a fixed operator (A4).
    const r = 1.38;
    const N = new THREE.Vector3(0, r, 0);
    const S = new THREE.Vector3(0, -r, 0);
    const GOD = 0xffeb3b, DEMON = 0xd23b3b;

    root.add(createSphere(r, 0.2));
    root.add(ring(r, 0xffffff, 0.45));                              // sphere equator
    root.add(createGridPlane(5.6, 19));
    root.add(ring(r, GOD, 0.85));                                   // the unit circle = god/demon boundary
    root.add(line([new THREE.Vector3(-2.6, 0, 0), new THREE.Vector3(2.6, 0, 0)], 0x555555, 0.6));
    root.add(line([new THREE.Vector3(0, 0, -2.6), new THREE.Vector3(0, 0, 2.6)], 0x555555, 0.6));
    root.add(makeMarker(N, 0xb8b8b8, 0.07));
    root.add(makeMarker(S, 0x707070, 0.07));
    [0.5, 1.0].forEach((y) => {
      const lat = ring(Math.sqrt(r * r - y * y), 0x666666, 0.32);
      lat.position.y = y; root.add(lat);
      const m = lat.clone(); m.position.y = -y; root.add(m);
    });
    const start = new THREE.Vector3(r, 0, 0);
    const pMark = makeMarker(start.clone(), 0xffffff, 0.1);         // P on the sphere
    const proj = makeMarker(start.clone(), GOD, 0.09);             // φ-projection on the plane
    const rayPhi = line([N, start.clone()], GOD, 0.9);            // ∞ → P → plane
    const rayNu = line([S, start.clone()], 0x8aa0c0, 0.6);        // 0 → P
    root.add(pMark); root.add(proj); root.add(rayPhi); root.add(rayNu);
    const readout = makeReadout();
    const quad = ["I", "II", "III", "IV"];
    dyn.push(function (t) {
      const psi = t * 0.55;                                        // azimuth sweep → circles the quadrants
      const theta = Math.PI / 2 + 0.62 * Math.sin(t * 0.62);       // colatitude crosses the equator
      const phi = 1 / Math.tan(theta / 2);                          // cot(θ/2), in units of r
      const nu = Math.tan(theta / 2);                              // reciprocal
      const cps = Math.cos(psi), sps = Math.sin(psi);
      const sT = Math.sin(theta);
      const P = new THREE.Vector3(r * sT * cps, r * Math.cos(theta), r * sT * sps);
      const Pp = new THREE.Vector3(r * phi * cps, 0, r * phi * sps);
      pMark.position.copy(P);
      proj.position.copy(Pp);
      rayPhi.geometry.setFromPoints([N, P, Pp]);
      rayNu.geometry.setFromPoints([S, P]);
      const isGod = phi > 1;
      const col = isGod ? GOD : DEMON;
      proj.material.color.setHex(col);
      rayPhi.material.color.setHex(col);
      pMark.material.color.setHex(col);
      root.rotation.y += 0.0026;
      const q = quad[Math.floor((psi % (Math.PI * 2)) / (Math.PI / 2)) % 4];
      if (readout) readout.textContent =
        "quadrant  " + q + "\n" +
        "φ = cot θ⁄2 = " + phi.toFixed(2) + "   ν = " + nu.toFixed(2) + "   (φ·ν = 1)\n" +
        (isGod ? "φ > 1  →  GOD-move · outside the unit circle"
               : "φ < 1  →  DEMON-move · inside the unit circle") + "\n" +
        "valence is on the move, not the operator (A4)";
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
