const page = window.DIMENSION_PAGE || {};
const canvas = document.querySelector(".dimension-canvas");
const visual = document.querySelector(".visual-panel");
const rootElement = document.documentElement;
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
  const stored = window.localStorage.getItem("emergentism-theme");
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
    window.localStorage.setItem("emergentism-theme", rootElement.dataset.theme);
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

  function draw(now) {
    const ink = "#fff";
    const muted = "#8f8f8f";
    const dim = "#5f5f5f";
    const bounds = resize();
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

    ctx.fillStyle = ink;
    ctx.font = "700 13px ui-monospace, SFMono-Regular, Menlo, monospace";
    ctx.textAlign = "left";
    ctx.fillText("Emergentism logarithmic calculator scale", left, pad + 8);
    ctx.fillStyle = muted;
    ctx.font = "12px ui-monospace, SFMono-Regular, Menlo, monospace";
    ctx.fillText("x ↦ 1/x mirrors s ↦ -s around unity", left, pad + 30);

    ctx.textAlign = "right";
    ctx.fillStyle = ink;
    ctx.fillText("⊙ = • × ○", right, height - pad - 28);
    ctx.fillStyle = muted;
    ctx.fillText("frame/register doctrine, not field arithmetic", right, height - pad - 8);

    requestAnimationFrame(draw);
  }

  requestAnimationFrame(draw);
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

function createHornTorus() {
  return new THREE.Mesh(
    new THREE.TorusGeometry(0.9, 0.9, 42, 160),
    makeMaterial(0xffffff, 0.35, true)
  );
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
    root.add(createSphere(1.35, 0.32));
    root.add(ring(1.35, 0xffffff, 1));
    root.add(makeMarker(new THREE.Vector3(0, -1.35, 0), 0x707070, 0.08));
    root.add(makeMarker(new THREE.Vector3(1.35, 0, 0), 0xffffff, 0.1));
    root.add(makeMarker(new THREE.Vector3(0, 1.35, 0), 0xb8b8b8, 0.08));
    root.add(line([
      new THREE.Vector3(0, 1.35, 0),
      new THREE.Vector3(1.35, 0, 0),
      new THREE.Vector3(2.7, -1.35, 0)
    ], 0xffffff, 0.95));
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
    const torus = createHornTorus();
    torus.rotation.x = Math.PI / 2;
    root.add(torus);
    root.add(ring(0.9, 0xb8b8b8, 0.75));
    root.add(line([
      new THREE.Vector3(-1.8, 0, 0),
      new THREE.Vector3(1.8, 0, 0)
    ], 0x707070, 0.85));
  }

  if (mode === "burrisphere") {
    root.add(createSphere(1.38, 0.23));
    root.add(ring(1.38, 0xffffff, 1));
    root.add(line([
      new THREE.Vector3(0, 1.38, 0),
      new THREE.Vector3(1.38, 0, 0),
      new THREE.Vector3(2.55, -1.04, 0)
    ], 0xb8b8b8, 1));
    root.add(line([
      new THREE.Vector3(0, -1.38, 0),
      new THREE.Vector3(-1.38, 0, 0),
      new THREE.Vector3(-2.55, 1.04, 0)
    ], 0x707070, 1));
    root.add(makeMarker(new THREE.Vector3(1.38, 0, 0), 0xb8b8b8, 0.08));
    root.add(makeMarker(new THREE.Vector3(-1.38, 0, 0), 0x707070, 0.08));
    root.add(makeMarker(new THREE.Vector3(0, 0, 0), 0xffffff, 0.1));
    [0.42, 0.8, 1.12].forEach((y, i) => {
      const lat = ring(Math.sqrt(1.38 * 1.38 - y * y), i === 1 ? 0xffffff : 0x777777, 0.5);
      lat.position.y = y;
      root.add(lat);
      const mirror = lat.clone();
      mirror.position.y = -y;
      root.add(mirror);
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

  return root;
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
    controls.autoRotate = true;
    controls.autoRotateSpeed = page.animationMode === "burrisphere" ? 0.55 : 0.35;

    addStars(scene);
    const root = buildScene(page.animationMode, scene);

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
      } else if (page.animationMode === "horn") {
        root.rotation.y += 0.004;
      } else if (page.animationMode === "convergence") {
        root.rotation.z = t * 0.08;
        root.scale.setScalar(1 + Math.sin(t * 0.7) * 0.04);
      }

      controls.update();
      renderer.render(scene, camera);
      requestAnimationFrame(animate);
    }

    resize();
    window.addEventListener("resize", resize);
    requestAnimationFrame(animate);
  } catch (error) {
    fail(error);
  }
}

boot();
