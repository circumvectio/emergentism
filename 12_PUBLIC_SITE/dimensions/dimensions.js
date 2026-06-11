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
    // The Bloch / Riemann sphere stands on the complex plane and projects
    // DOWNWARD: from ∞ (north pole) through the surface onto the plane below —
    // the dual of the Burrisphere, which projects upward. Equator → unit circle.
    const r = 1.35;
    const N = new THREE.Vector3(0, r, 0), Sp = new THREE.Vector3(0, -r, 0);
    root.add(createGridPlane(4.8, 17));
    root.add(createSphere(r, 0.26));
    root.add(ring(r, 0xffffff, 0.85));                          // equator = unit circle |z|=1
    root.add(ring(1.0, 0xffeb3b, 0.55));                        // the unit point x=1 on the plane
    root.add(makeMarker(N, 0xb8b8b8, 0.07));                    // ∞
    root.add(makeMarker(Sp, 0x707070, 0.07));                   // 0
    const P0 = new THREE.Vector3(r * Math.sin(Math.PI / 3), r * Math.cos(Math.PI / 3), 0);
    const land = new THREE.Vector3(r / Math.tan(Math.PI / 6), 0, 0);  // cot(θ/2)·r, on the plane
    root.add(line([N, P0, land], 0xffeb3b, 0.9));               // the downward projection ray
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
      // HORN at rest (f=0.5); as β→1 the overlap completes and R→0, so the torus
      // RESOLVES INTO A SPHERE — the Burrisphere — which then projects upward.
      const f = 0.5 + 0.47 * aB;                                // 0.5 horn -> ~0.97 (R→0 = sphere)
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
        "γ = cosh w = " + gamma.toFixed(1) + " &nbsp;<span style='color:#9CA3AF'>time ×" + gamma.toFixed(1) + "</span><br>" +
        "m / m₀ = γ &nbsp;" + bar(gamma / G_MAX, "#FFEB3B") + " " + gamma.toFixed(1) + "<br>" +
        "<span style='color:#F3F4F6'>E = γ m c²</span> &nbsp;<span style='color:#9CA3AF'>(c² = velocity²)</span><br>" +
        (!moving
          ? "<span style='color:#FFEB3B'>at rest · HORN torus — throat = the relative centre</span>"
          : aB > 0.985
            ? "<span style='color:#FFEB3B'>overlap complete · R→0 → resolves as the BURRISPHERE (projects upward)</span>"
            : "<span style='color:#9CA3AF'>SPINDLE · overlap grows · β→1 · energy → <b style='color:#FFEB3B'>mass</b></span>");
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
    const cplane = createGridPlane(6.0, 21); cplane.position.y = -r; root.add(cplane); // the complex plane = the FLOOR the sphere rests on
    root.add(ring(r, GOD, 0.85));                                   // sphere equator = the god/demon boundary (φ = ν = 1)
    root.add(line([new THREE.Vector3(-2.9, -r, 0), new THREE.Vector3(2.9, -r, 0)], 0x555555, 0.6)); // real axis, on the plane
    root.add(line([new THREE.Vector3(0, -r, -2.9), new THREE.Vector3(0, -r, 2.9)], 0x555555, 0.6)); // imaginary axis
    root.add(makeMarker(N, 0xc8c8c8, 0.07));                        // north pole → up toward ∞
    root.add(makeMarker(S, 0x808080, 0.085));                       // south pole = 0, resting on the complex plane
    [0.5, 1.0].forEach((y) => {
      const lat = ring(Math.sqrt(r * r - y * y), 0x666666, 0.32);
      lat.position.y = y; root.add(lat);
      const m = lat.clone(); m.position.y = -y; root.add(m);
    });
    const TITAN = 0x6f9bcc;
    const CY = 2.2;                                  // the projection plane, above the sphere
    const UNIT = 0.5;                                // chart radius where cot(θ/2)=1 (the god/demon boundary)
    // the projection plane: frame + the four quadrants + the unit circle
    root.add(line([
      new THREE.Vector3(-1.3, CY, -1.3), new THREE.Vector3(1.3, CY, -1.3),
      new THREE.Vector3(1.3, CY, 1.3), new THREE.Vector3(-1.3, CY, 1.3),
      new THREE.Vector3(-1.3, CY, -1.3)], 0x3a3a3a, 0.8));
    root.add(line([new THREE.Vector3(-1.3, CY, 0), new THREE.Vector3(1.3, CY, 0)], 0x5a5a5a, 0.8));
    root.add(line([new THREE.Vector3(0, CY, -1.3), new THREE.Vector3(0, CY, 1.3)], 0x5a5a5a, 0.8));
    const unitChart = ring(UNIT, GOD, 0.7); unitChart.position.y = CY; root.add(unitChart);
    // the four operators: 2 Gods (give) OUTSIDE the unit circle, 2 Demons (take) INSIDE
    [[0.62, 0.62, GOD], [-0.62, 0.62, GOD], [0.22, -0.22, DEMON], [-0.22, -0.22, DEMON]]
      .forEach((o) => root.add(makeMarker(new THREE.Vector3(o[0], CY, o[1]), o[2], 0.055)));

    const start = new THREE.Vector3(r, 0, 0);
    const pMark = makeMarker(start.clone(), 0xffffff, 0.1);          // P on the sphere
    const rayUp = line([S, start.clone()], GOD, 0.9);               // 0 → P → up to the projection
    const projPt = makeMarker(new THREE.Vector3(UNIT, CY, 0), GOD, 0.08);  // the live projection
    root.add(pMark); root.add(rayUp); root.add(projPt);
    // the SPIRAL trail traced by the projected point
    const TRAIL = 320, trailPts = [];
    const trail = line([new THREE.Vector3(UNIT, CY, 0)], 0xffeb3b, 0.5);
    root.add(trail);

    // the 3 Titans on the lower hemisphere + the centre (L4 Arjuna, the equator)
    [[2.30, 0.0], [2.55, 2.1], [2.85, 4.2]].forEach((T) => {
      root.add(makeMarker(new THREE.Vector3(
        r * Math.sin(T[0]) * Math.cos(T[1]), r * Math.cos(T[0]), r * Math.sin(T[0]) * Math.sin(T[1])
      ), TITAN, 0.07));
    });
    root.add(makeMarker(new THREE.Vector3(0, 0, 0), 0xffffff, 0.05)); // the centre

    const readout = makeReadout();
    if (readout) { readout.style.whiteSpace = "pre-line"; readout.style.top = "auto"; readout.style.bottom = "14px"; }
    const quadName = ["I", "II", "III", "IV"];
    dyn.push(function (t) {
      const psi = t * 2.3;                                          // azimuth rotates fast
      const theta = Math.PI / 2 + 1.3 * Math.sin(t * 0.2);          // the ANGLE sweeps, near pole to near pole
      const phi = 1 / Math.tan(theta / 2);                          // cot(θ/2) — the SAME stereographic radius as the Riemann sphere
      const nu = Math.tan(theta / 2);
      const cps = Math.cos(psi), sps = Math.sin(psi);
      const sT = Math.sin(theta);
      const P = new THREE.Vector3(r * sT * cps, r * Math.cos(theta), r * sT * sps);
      pMark.position.copy(P);
      const rad = Math.min(phi * UNIT, 1.3);                        // radius grows/shrinks with the angle → it SPIRALS
      const Lp = new THREE.Vector3(rad * cps, CY, rad * sps);
      projPt.position.copy(Lp);
      const isGod = phi > 1;                                         // outside the unit circle = GOD
      const col = isGod ? GOD : DEMON;
      projPt.material.color.setHex(col);
      pMark.material.color.setHex(col);
      rayUp.geometry.setFromPoints([S, P, Lp]);                      // 0 → P → up to the projection
      rayUp.material.color.setHex(col);
      trailPts.push(Lp.clone());
      if (trailPts.length > TRAIL) trailPts.shift();
      trail.geometry.setFromPoints(trailPts);
      root.rotation.y += 0.0022;
      const q = quadName[Math.floor((((psi % (2 * Math.PI)) + 2 * Math.PI) % (2 * Math.PI)) / (Math.PI / 2)) % 4];
      const opName = isGod
        ? (cps < 0 ? "Kṛṣṇa L3 · give" : "Arjuna L4 · give")
        : (cps < 0 ? "Kali L1 · take" : "Kālī L2 · take");
      if (readout) readout.textContent =
        "stereographic projection · SPIRALING (up from 0)\n" +
        "angle θ = " + (theta * 180 / Math.PI).toFixed(0) + "°   φ = cot θ⁄2 = " + phi.toFixed(2) + "   ν = " + nu.toFixed(2) + "\n" +
        "quadrant " + q + " · " + opName + " · " + (isGod ? "GOD (outside unit circle)" : "DEMON (inside)") + "\n" +
        "below: Titans Brahmā ++ · Śiva −− · Viṣṇu ≈≈ · centre L4";
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
      // the complex plane is the floor (0 at the south pole), ∞ is up top —
      // stand near the plane and look UP toward infinity / the operator chart
      camera.position.set(0, -0.8, 7.7);
      controls.target.set(0, 1.35, 0);
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
