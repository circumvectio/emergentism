import {
  createStripChart as createSharedStripChart,
  clearStripChart as clearSharedStripChart,
  updateStripChart as updateSharedStripChart
} from "../assets/js/instrument-charts.js?v=2026-06-14-instrument-10";

const page = window.DIMENSION_PAGE || {};
const canvas = document.querySelector(".dimension-canvas");
const visual = document.querySelector(".visual-panel");
const rootElement = document.documentElement;
if (canvas && visual) document.body.classList.add("dimension-page");
const REDUCED_MOTION = !!(window.matchMedia
  && window.matchMedia("(prefers-reduced-motion: reduce)").matches);
const TAU = Math.PI * 2;
const SAMPLE_HZ = 30;
const SAMPLE_DT = 1 / SAMPLE_HZ;
const MAX_FRAME_DT = 0.12;
const INSTRUMENT_CPS = {
  slow: 0.008,
  medium: 0.014,
  fast: 0.02
};
function nowMs() {
  return (typeof window.performance !== "undefined" && typeof window.performance.now === "function")
    ? window.performance.now()
    : Date.now();
}

function scheduleFrame(callback) {
  let settled = false;
  const timer = window.setTimeout(() => {
    if (settled) return;
    settled = true;
    callback(nowMs());
  }, 1000 / 60);
  if (typeof window.requestAnimationFrame !== "function") return timer;
  return window.requestAnimationFrame((time) => {
    if (settled) return;
    settled = true;
    window.clearTimeout(timer);
    callback(typeof time === "number" ? time : nowMs());
  });
}
const COLORS = {
  bg: "#050505",
  surface: "#0A0A0A",
  text: "#F3F4F6",
  muted: "#9CA3AF",
  dim: "#555555",
  gold: "#FFEB3B",
  goldSoft: "#FFF176",
  blue: "#2196F3",
  blueSoft: "#42A5F5",
  red: "#F44336",
  green: "#4CAF50"
};
const modeLabels = {
  titans: "D0 frame",
  logline: "D1 reciprocal line",
  muLimit: "D2 mu-limit",
  bloch: "D3 Riemann/Bloch",
  horn: "D4 rapidity torus",
  burrisphere: "D5 dual projection",
  constitution: "5+1 constitution",
  ccc: "/6 CCC return",
  convergence: "/6 CCC return"
};
const modeInvariants = {
  titans: "s_left + s_right = 0",
  logline: "x·1/x = 1",
  muLimit: "rank +1 at μ",
  bloch: "φ·ν = 1",
  horn: "R/r = 1/γ",
  burrisphere: "φ·ν = 1 · B=sinθ",
  constitution: "5 refusals + Ω",
  ccc: "/6 ≡ /0",
  convergence: "/6 ≡ /0"
};
const modeInstrumentIds = {
  titans: "E0-FRM",
  logline: "E1-REC",
  muLimit: "E2-LFT",
  bloch: "E3-STP",
  horn: "E4-RPD",
  burrisphere: "E5-DLP",
  constitution: "E5+1-GOV",
  ccc: "E6-CCC",
  convergence: "E6-CCC"
};
const modeScales = {
  titans: { x: "log coordinate s", y: "reciprocal mirror offset" },
  logline: { x: "log₂(x) axis", y: "E=(ln x)² well" },
  muLimit: { x: "λ along source line", y: "μ orthogonal lift" },
  bloch: { x: "complex-plane radius", y: "sphere latitude θ" },
  horn: { x: "rapidity w", y: "means ratio dτ/dt" },
  burrisphere: { x: "ν means radius", y: "Φ worldline sight θ" },
  constitution: { x: "fence index", y: "closure residual" },
  ccc: { x: "aeon phase q", y: "conformal radius Ω" },
  convergence: { x: "aeon phase q", y: "conformal radius Ω" }
};
const animationMode = page.animationMode === "convergence"
  ? "ccc"
  : (page.animationMode || "model");

function smooth01(x) {
  return x * x * (3 - 2 * x);
}

function sweep01(t, cyclesPerSecond = 0.045) {
  const p = ((t * cyclesPerSecond) % 1 + 1) % 1;
  return p < 0.5 ? p * 2 : (1 - p) * 2;
}

function phase01(t, cyclesPerSecond = 0.045, offset = 0) {
  return ((t * cyclesPerSecond + offset) % 1 + 1) % 1;
}

function clamp01(x) {
  return Math.max(0, Math.min(1, x));
}

function finiteNumber(value, fallback = 0) {
  const n = Number(value);
  return Number.isFinite(n) ? n : fallback;
}

function createSampleClock() {
  return {
    accumulator: 0,
    index: 0,
    lastStepCount: 0,
    advance(frameSeconds, rate = 1, forcedSeconds = 0, paused = false) {
      if (!paused) this.accumulator += Math.min(Math.max(frameSeconds, 0), MAX_FRAME_DT) * rate;
      if (forcedSeconds > 0) this.accumulator += forcedSeconds;
      const steps = Math.min(12, Math.floor(this.accumulator / SAMPLE_DT));
      if (steps > 0) {
        this.accumulator -= steps * SAMPLE_DT;
        this.index += steps;
      }
      this.lastStepCount = steps;
      return steps * SAMPLE_DT;
    },
    label() {
      return SAMPLE_HZ + " Hz · n " + String(this.index).padStart(5, "0");
    }
  };
}
const dimensionCommands = [
  { key: "/0", aliases: ["/0", "0", "d0", "titans"], label: "/0 · Titans", detail: "Ground / finity", href: "/0/" },
  { key: "/1", aliases: ["/1", "1", "d1", "one", "finity"], label: "/1 · The Special One", detail: "Reciprocal mirror", href: "/1/" },
  { key: "/2", aliases: ["/2", "2", "d2", "mu", "mu-limit"], label: "/2 · Mu-Limit", detail: "Line to plane", href: "/2/" },
  { key: "/3", aliases: ["/3", "3", "d3", "sphere", "bloch"], label: "/3 · Sphere", detail: "Closure surface", href: "/3/" },
  { key: "/4", aliases: ["/4", "4", "d4", "torus", "horn"], label: "/4 · Horn Torus", detail: "Energy overlap", href: "/4/" },
  { key: "/5", aliases: ["/5", "5", "d5", "burrisphere", "game"], label: "/5 · Burrisphere", detail: "Dual projection", href: "/5/" },
  { key: "/6", aliases: ["/6", "6", "d6", "convergence", "ccc"], label: "/6 · CCC Return", detail: "Endstate = start", href: "/6/" },
  { key: "R", aliases: ["rosetta", "r"], label: "Rosetta", detail: "Sevenfold map", href: "/rosetta/" },
  { key: "S", aliases: ["soul", "soul-loop"], label: "Soul Loop", detail: "Loop doctrine", href: "/soul-loop/" },
  { key: "A", aliases: ["atlas", "a"], label: "Atlas", detail: "Public atlas", href: "/atlas/" },
  { key: "EM", aliases: ["cascade", "emergence"], label: "Emergence", detail: "Animation", href: "/cascade.html" },
  { key: "SP", aliases: ["sphere-instrument", "burri", "burri-sphere"], label: "Burri Sphere", detail: "Instrument", href: "/sphere.html" }
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
    scheduleFrame(() => {
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

function ensureInstrumentOverlay(mode = animationMode) {
  if (!visual) return null;
  visual.classList.add("instrument-visual", `instrument-mode-${mode}`);
  const existing = visual.querySelector(".instrument-overlay");
  if (existing) return existing;

  const scale = modeScales[mode] || { x: "x instrument axis", y: "y instrument axis" };
  const overlay = document.createElement("div");
  overlay.className = "instrument-overlay";
  overlay.setAttribute("aria-hidden", "true");
  overlay.innerHTML = `
    <div class="instrument-graticule"></div>
    <div class="instrument-corners">
      <span></span><span></span><span></span><span></span>
    </div>
    <div class="instrument-reticle"></div>
    <div class="instrument-scale x" data-axis-label="${scale.x}"></div>
    <div class="instrument-scale y" data-axis-label="${scale.y}"></div>
    <div class="instrument-id">
      <span>${modeInstrumentIds[mode] || "E-MOD"}</span>
      <span>calibrated model</span>
    </div>
    <div class="instrument-calibration">
      <span>CAL</span>
      <span>30 Hz</span>
      <span>Δt 0.0333 s</span>
      <span>screen-space assay</span>
    </div>
    <div class="instrument-measurements">
      <div class="instrument-meter" data-signal="primary">
        <span data-label="primary">primary</span>
        <i><b></b></i>
        <em data-value="primary">--</em>
      </div>
      <div class="instrument-meter" data-signal="secondary">
        <span data-label="secondary">secondary</span>
        <i><b></b></i>
        <em data-value="secondary">--</em>
      </div>
      <div class="instrument-meter error" data-signal="error">
        <span data-label="error">residual</span>
        <i><b></b></i>
        <em data-value="error">--</em>
      </div>
    </div>
    <div class="instrument-telemetry">
      <span data-field="mode">${modeLabels[mode] || mode}</span>
      <span data-field="invariant">${modeInvariants[mode] || "calibrated"}</span>
      <span data-field="fps">-- fps</span>
      <span data-field="sample">sample --</span>
      <span data-field="time">t+0.00s</span>
      <span data-field="phase">phase --</span>
      <span data-field="metric">sample --</span>
      <span data-field="uncertainty">σ --</span>
      <span data-field="state">locked frame</span>
    </div>
  `;
  visual.appendChild(overlay);
  return overlay;
}

function setInstrumentMetric(metric = "", state = "", phase = "", uncertainty = "", signals = null) {
  if (!visual) return;
  if (metric) visual.dataset.instrumentMetric = metric;
  if (state) visual.dataset.instrumentState = state;
  if (phase) visual.dataset.instrumentPhase = phase;
  if (uncertainty) visual.dataset.instrumentUncertainty = uncertainty;
  if (signals) setInstrumentSignals(signals);
}

function setInstrumentSignals(signals = {}) {
  if (!visual) return;
  [
    ["primary", "Primary"],
    ["secondary", "Secondary"],
    ["error", "Residual"]
  ].forEach(([key, fallbackLabel]) => {
    const raw = finiteNumber(signals[key], Number.NaN);
    if (Number.isFinite(raw)) visual.dataset[`signal${key}`] = String(clamp01(raw));
    if (signals[`${key}Label`]) visual.dataset[`signal${key}Label`] = String(signals[`${key}Label`]);
    else if (!visual.dataset[`signal${key}Label`]) visual.dataset[`signal${key}Label`] = fallbackLabel;
    if (signals[`${key}Text`]) visual.dataset[`signal${key}Text`] = String(signals[`${key}Text`]);
    else if (Number.isFinite(raw)) visual.dataset[`signal${key}Text`] = clamp01(raw).toFixed(3);
  });
}

function updateSignalMeter(overlay, key) {
  const meter = overlay.querySelector(`[data-signal="${key}"]`);
  if (!meter) return;
  const value = clamp01(finiteNumber(visual.dataset[`signal${key}`], 0));
  const label = visual.dataset[`signal${key}Label`] || key;
  const text = visual.dataset[`signal${key}Text`] || value.toFixed(3);
  const labelEl = meter.querySelector(`[data-label="${key}"]`);
  const valueEl = meter.querySelector(`[data-value="${key}"]`);
  const barEl = meter.querySelector("b");
  if (labelEl) labelEl.textContent = label;
  if (valueEl) valueEl.textContent = text;
  if (barEl) barEl.style.transform = `scaleX(${value.toFixed(4)})`;
}

function updateInstrumentOverlay(overlay, t, fps) {
  if (!overlay) return;
  const timeField = overlay.querySelector('[data-field="time"]');
  const fpsField = overlay.querySelector('[data-field="fps"]');
  const sampleField = overlay.querySelector('[data-field="sample"]');
  const phaseField = overlay.querySelector('[data-field="phase"]');
  const metricField = overlay.querySelector('[data-field="metric"]');
  const uncertaintyField = overlay.querySelector('[data-field="uncertainty"]');
  const stateField = overlay.querySelector('[data-field="state"]');
  if (timeField) timeField.textContent = "t+" + t.toFixed(2) + "s";
  if (fpsField) fpsField.textContent = REDUCED_MOTION ? "static" : fps.toFixed(0) + " fps";
  if (sampleField) sampleField.textContent = visual.dataset.instrumentSample || "sample --";
  if (phaseField) phaseField.textContent = visual.dataset.instrumentPhase || "phase --";
  if (metricField) metricField.textContent = visual.dataset.instrumentMetric || "sample --";
  if (uncertaintyField) uncertaintyField.textContent = visual.dataset.instrumentUncertainty || "σ --";
  if (stateField) stateField.textContent = visual.dataset.instrumentState || "locked frame";
  updateSignalMeter(overlay, "primary");
  updateSignalMeter(overlay, "secondary");
  updateSignalMeter(overlay, "error");
}

function ensureInstrumentControls() {
  if (!visual) return null;
  let controls = visual.querySelector(".instrument-controls");
  if (!controls) {
    controls = document.createElement("div");
    controls.className = "instrument-controls";
    controls.innerHTML = `
      <button type="button" data-action="hold" aria-pressed="false">HOLD</button>
      <button type="button" data-action="step">STEP</button>
      <button type="button" data-action="zero">ZERO</button>
      <label>
        <span>rate</span>
        <input type="range" min="25" max="150" step="5" value="100" aria-label="simulation rate" />
      </label>
    `;
    visual.appendChild(controls);
  }
  return {
    root: controls,
    hold: controls.querySelector('[data-action="hold"]'),
    step: controls.querySelector('[data-action="step"]'),
    zero: controls.querySelector('[data-action="zero"]'),
    rate: controls.querySelector('input[type="range"]')
  };
}

function syncInstrumentControls(playback, paused) {
  if (!playback || !playback.hold) return;
  playback.hold.textContent = paused ? "RUN" : "HOLD";
  playback.hold.setAttribute("aria-pressed", paused ? "true" : "false");
}

function createModelSlider({
  className = "",
  leftLabel = "min",
  rightLabel = "max",
  ariaLabel = "instrument slider",
  value = "0",
  min = "0",
  max = "100",
  step = "1"
} = {}) {
  if (!visual) return null;
  const wrap = document.createElement("div");
  wrap.className = `model-slider ${className}`.trim();
  wrap.setAttribute("role", "group");
  wrap.setAttribute("aria-label", ariaLabel);

  const lo = document.createElement("span");
  lo.className = "slider-end slider-lo";
  lo.textContent = leftLabel;

  const input = document.createElement("input");
  input.type = "range";
  input.min = String(min);
  input.max = String(max);
  input.step = String(step);
  input.value = String(value);
  input.setAttribute("aria-label", ariaLabel);

  const hi = document.createElement("span");
  hi.className = "slider-end slider-hi";
  hi.textContent = rightLabel;

  const output = document.createElement("output");
  output.className = "slider-output";
  output.textContent = value;
  output.setAttribute("aria-live", "polite");

  wrap.append(lo, input, hi, output);
  visual.appendChild(wrap);

  return {
    root: wrap,
    input,
    output,
    setOutput(text) {
      output.textContent = text;
    }
  };
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
  const overlay = ensureInstrumentOverlay("titans");
  const readout = makeReadout();
  if (readout) {
    readout.style.left = "auto";
    readout.style.right = "16px";
    readout.style.maxWidth = "min(420px, 46%)";
    readout.classList.add("instrument-readout", "titans-readout");
  }
  let bounds = resize();
  window.addEventListener("resize", () => {
    bounds = resize();
    if (REDUCED_MOTION) draw(0);
  });
  const playback = ensureInstrumentControls();
  let paused = false;
  let simTime = 0;
  let stepSeconds = 0;
  const sampleClock = createSampleClock();
  let lastFrame = time;
  let fps = 0;
  if (playback) {
    playback.hold.addEventListener("click", () => {
      paused = !paused;
      syncInstrumentControls(playback, paused);
    });
    playback.step.addEventListener("click", () => {
      paused = true;
      stepSeconds += 1 / 12;
      syncInstrumentControls(playback, paused);
    });
    playback.zero.addEventListener("click", () => {
      paused = true;
      simTime = 0;
      stepSeconds = 0;
      sampleClock.accumulator = 0;
      sampleClock.index = 0;
      visual.dispatchEvent(new CustomEvent("instrument:zero"));
      setInstrumentMetric(visual.dataset.instrumentMetric || "", "zeroed", "phase 0.00");
      syncInstrumentControls(playback, paused);
    });
    playback.rate.addEventListener("input", () => {
      setInstrumentMetric(visual.dataset.instrumentMetric || "", "rate " + (parseFloat(playback.rate.value) / 100).toFixed(2) + "x", visual.dataset.instrumentPhase || "");
    });
    syncInstrumentControls(playback, paused);
  }

  function draw(now) {
    const ink = "#fff";
    const muted = "#8f8f8f";
    const dim = "#5f5f5f";
    const width = bounds.width;
    const height = bounds.height;
    const dt = lastFrame ? Math.max(1, now - lastFrame) : 16.7;
    fps = fps ? fps * 0.9 + (1000 / dt) * 0.1 : 1000 / dt;
    lastFrame = now;
    const rate = playback && playback.rate ? parseFloat(playback.rate.value) / 100 : 1;
    const sampleAdvance = sampleClock.advance(dt * 0.001, rate, stepSeconds, paused);
    stepSeconds = 0;
    simTime += sampleAdvance;
    visual.dataset.instrumentSample = REDUCED_MOTION ? "sample static" : sampleClock.label();
    const t = simTime;
    updateInstrumentOverlay(overlay, t, fps);
    const cx = width / 2;
    const cy = height / 2;
    const pad = Math.max(28, Math.min(width, height) * 0.08);
    const left = pad;
    const right = width - pad;
    const axis = cy;
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

    const reciprocalPhase = phase01(t, INSTRUMENT_CPS.medium);
    const reciprocalS = 1.85 + smooth01(sweep01(t, INSTRUMENT_CPS.medium)) * 2.5;
    const lx = cx - reciprocalS * unit;
    const rx = cx + reciprocalS * unit;
    const mirrorResidual = Math.abs((lx + rx) - (2 * cx)) / Math.max(unit, 1e-6);
    setInstrumentMetric(
      "s ±" + reciprocalS.toFixed(2),
      (paused ? "held frame" : "unity fixed"),
      "phase " + reciprocalPhase.toFixed(2),
      "σ mirror " + mirrorResidual.toExponential(1),
      {
        primary: reciprocalS / 4.5,
        primaryLabel: "|s|",
        primaryText: reciprocalS.toFixed(2),
        secondary: 1 - clamp01(mirrorResidual),
        secondaryLabel: "mirror",
        secondaryText: "1.000",
        error: clamp01(mirrorResidual * 24),
        errorText: mirrorResidual.toExponential(1)
      }
    );

    ctx.setLineDash([8, 8]);
    ctx.strokeStyle = "rgba(245,245,245,0.48)";
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

    if (readout) readout.textContent =
      "D0 FRAME REGISTER · reciprocal calibration\n" +
      "left s = " + (-reciprocalS).toFixed(2) + " · right s = " + reciprocalS.toFixed(2) + " · centre s = 0\n" +
      "mirror operation: s ↦ −s · product register: • × ○ → ⊙\n" +
      "measured variable: displacement only; the frame remains fixed";

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

    if (!REDUCED_MOTION) scheduleFrame(draw);
  }

  draw(0);
}

function drawConstitutionInstrument(time = 0) {
  if (visual) visual.classList.add("constitution-visual");
  const { ctx, resize } = setupCanvas2D();
  const overlay = ensureInstrumentOverlay("constitution");
  const readout = makeReadout();
  if (readout) {
    readout.style.left = "auto";
    readout.style.right = "16px";
    readout.style.maxWidth = "min(330px, 38%)";
    readout.classList.add("instrument-readout");
  }
  const playback = ensureInstrumentControls();
  const sampleClock = createSampleClock();
  const fences = [
    { key: "η=0", title: "no extraction", tier: "[S]", color: "#FFEB3B" },
    { key: "K2", title: "human signature", tier: "[B/S]", color: "#42A5F5" },
    { key: "K3", title: "archive first", tier: "[S]", color: "#F3F4F6" },
    { key: "K4", title: "grace exit", tier: "[S]", color: "#8B5CF6" },
    { key: "A7", title: "self-correction", tier: "[S]", color: "#4CAF50" }
  ];
  let bounds = resize();
  let paused = false;
  let simTime = 0;
  let stepSeconds = 0;
  let lastFrame = time;
  let fps = 0;

  function sync() {
    syncInstrumentControls(playback, paused);
  }

  if (playback) {
    playback.hold.addEventListener("click", () => {
      paused = !paused;
      sync();
    });
    playback.step.addEventListener("click", () => {
      paused = true;
      stepSeconds += 1 / 12;
      sync();
    });
    playback.zero.addEventListener("click", () => {
      paused = true;
      simTime = 0;
      stepSeconds = 0;
      sampleClock.accumulator = 0;
      sampleClock.index = 0;
      setInstrumentMetric("closure 0.000", "zeroed", "phase 0.00");
      sync();
      draw(0);
    });
    playback.rate.addEventListener("input", () => {
      setInstrumentMetric(visual.dataset.instrumentMetric || "", "rate " + (parseFloat(playback.rate.value) / 100).toFixed(2) + "x", visual.dataset.instrumentPhase || "");
    });
    sync();
  }

  function regularPoint(cx, cy, r, index, offset = -Math.PI / 2) {
    const angle = offset + (index / fences.length) * TAU;
    return { x: cx + Math.cos(angle) * r, y: cy + Math.sin(angle) * r, angle };
  }

  function drawArrow(x0, y0, x1, y1, color) {
    const angle = Math.atan2(y1 - y0, x1 - x0);
    const head = 9;
    ctx.strokeStyle = color;
    ctx.lineWidth = 1.4;
    ctx.beginPath();
    ctx.moveTo(x0, y0);
    ctx.lineTo(x1, y1);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(x1, y1);
    ctx.lineTo(x1 - Math.cos(angle - 0.48) * head, y1 - Math.sin(angle - 0.48) * head);
    ctx.moveTo(x1, y1);
    ctx.lineTo(x1 - Math.cos(angle + 0.48) * head, y1 - Math.sin(angle + 0.48) * head);
    ctx.stroke();
  }

  function draw(now = 0) {
    const dt = lastFrame ? Math.max(1, now - lastFrame) : 16.7;
    fps = fps ? fps * 0.9 + (1000 / dt) * 0.1 : 1000 / dt;
    lastFrame = now;
    const rate = playback && playback.rate ? parseFloat(playback.rate.value) / 100 : 1;
    const sampleAdvance = sampleClock.advance(dt * 0.001, rate, stepSeconds, paused);
    stepSeconds = 0;
    simTime += sampleAdvance;
    visual.dataset.instrumentSample = REDUCED_MOTION ? "sample static" : sampleClock.label();

    const width = bounds.width;
    const height = bounds.height;
    const wide = width >= 780;
    const cx = width * (wide ? 0.36 : 0.5);
    const cy = height * 0.52;
    const radius = Math.min(width, height) * (wide ? 0.25 : 0.31);
    const t = simTime;
    const phase = phase01(t, INSTRUMENT_CPS.fast);
    const scan = phase * fences.length;
    const active = Math.floor(scan) % fences.length;
    const local = scan - Math.floor(scan);
    const activeFence = fences[active];
    const nextIndex = (active + 1) % fences.length;
    const p0 = regularPoint(cx, cy, radius, active);
    const p1 = regularPoint(cx, cy, radius, nextIndex);
    const cursor = {
      x: p0.x + (p1.x - p0.x) * local,
      y: p0.y + (p1.y - p0.y) * local
    };
    const points = fences.map((_, i) => regularPoint(cx, cy, radius, i));
    let closureX = 0;
    let closureY = 0;
    for (let i = 0; i < points.length; i += 1) {
      const a = points[i];
      const b = points[(i + 1) % points.length];
      closureX += b.x - a.x;
      closureY += b.y - a.y;
    }
    const closureResidual = Math.hypot(closureX, closureY) / Math.max(radius, 1);
    const centroid = points.reduce((acc, point) => ({ x: acc.x + point.x, y: acc.y + point.y }), { x: 0, y: 0 });
    centroid.x /= points.length;
    centroid.y /= points.length;
    const centerResidual = Math.hypot(centroid.x - cx, centroid.y - cy) / Math.max(radius, 1);

    ctx.clearRect(0, 0, width, height);
    ctx.fillStyle = "#050505";
    ctx.fillRect(0, 0, width, height);

    ctx.strokeStyle = "rgba(243,244,246,0.08)";
    ctx.lineWidth = 1;
    for (let x = 0; x <= width; x += 32) {
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x, height);
      ctx.stroke();
    }
    for (let y = 0; y <= height; y += 32) {
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(width, y);
      ctx.stroke();
    }

    ctx.strokeStyle = "rgba(243,244,246,0.2)";
    ctx.beginPath();
    points.forEach((point, index) => {
      if (index === 0) ctx.moveTo(point.x, point.y);
      else ctx.lineTo(point.x, point.y);
    });
    ctx.closePath();
    ctx.stroke();

    ctx.strokeStyle = "rgba(255,235,59,0.22)";
    ctx.beginPath();
    ctx.arc(cx, cy, radius * 0.54, 0, TAU);
    ctx.stroke();

    points.forEach((point, index) => {
      const fence = fences[index];
      drawArrow(point.x, point.y, cx + (point.x - cx) * 0.24, cy + (point.y - cy) * 0.24, "rgba(243,244,246,0.18)");
      ctx.beginPath();
      ctx.arc(point.x, point.y, index === active ? 24 : 20, 0, TAU);
      ctx.fillStyle = index === active ? fence.color : "#10100f";
      ctx.strokeStyle = fence.color;
      ctx.lineWidth = index === active ? 2 : 1;
      ctx.fill();
      ctx.stroke();
      ctx.fillStyle = index === active ? "#050505" : fence.color;
      ctx.font = "800 13px ui-monospace, SFMono-Regular, Menlo, monospace";
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      ctx.fillText(fence.key, point.x, point.y - 3);
      ctx.fillStyle = "rgba(243,244,246,0.58)";
      ctx.font = "700 10px ui-monospace, SFMono-Regular, Menlo, monospace";
      ctx.fillText(fence.title, point.x, point.y + 33);
    });

    ctx.beginPath();
    ctx.arc(cx, cy, 34, 0, TAU);
    ctx.fillStyle = "#0A0A0A";
    ctx.strokeStyle = "#FFEB3B";
    ctx.lineWidth = 2;
    ctx.fill();
    ctx.stroke();
    ctx.fillStyle = "#FFEB3B";
    ctx.font = "800 26px ui-monospace, SFMono-Regular, Menlo, monospace";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillText("Ω", cx, cy - 2);
    ctx.fillStyle = "rgba(243,244,246,0.58)";
    ctx.font = "700 10px ui-monospace, SFMono-Regular, Menlo, monospace";
    ctx.fillText("+1 direction", cx, cy + 48);

    drawArrow(cx, cy, cursor.x, cursor.y, activeFence.color);
    ctx.beginPath();
    ctx.arc(cursor.x, cursor.y, 7, 0, TAU);
    ctx.fillStyle = activeFence.color;
    ctx.fill();
    ctx.strokeStyle = "#050505";
    ctx.lineWidth = 2;
    ctx.stroke();

    if (wide) {
      const graphX = width * 0.62;
      const graphY = Math.min(height - 72, cy + radius * 0.72);
      const graphW = Math.min(210, width * 0.23);
      const graphH = 44;
      ctx.strokeStyle = "rgba(243,244,246,0.16)";
      ctx.lineWidth = 1;
      ctx.strokeRect(graphX, graphY, graphW, graphH);
      ctx.strokeStyle = "rgba(66,165,245,0.55)";
      ctx.beginPath();
      for (let i = 0; i <= 24; i += 1) {
        const q = i / 24;
        const y = graphY + graphH * (0.78 - 0.3 * Math.sin((q + phase) * TAU));
        const x = graphX + q * graphW;
        if (i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      }
      ctx.stroke();
      ctx.fillStyle = "rgba(243,244,246,0.58)";
      ctx.font = "700 10px ui-monospace, SFMono-Regular, Menlo, monospace";
      ctx.textAlign = "left";
      ctx.fillText("route pressure scan", graphX + 8, graphY + graphH - 8);
    }

    setInstrumentMetric(
      "closure " + closureResidual.toExponential(1) + " · center " + centerResidual.toExponential(1),
      (paused ? "held frame" : "perimeter scan"),
      "phase " + phase.toFixed(2),
      "σ closure " + Math.max(closureResidual, centerResidual).toExponential(1),
      {
        primary: (active + local) / fences.length,
        primaryLabel: "scan",
        primaryText: (active + 1) + "/5",
        secondary: 1 - clamp01(centerResidual * 18),
        secondaryLabel: "centroid",
        secondaryText: centerResidual.toExponential(1),
        error: clamp01(Math.max(closureResidual, centerResidual) * 24),
        errorText: Math.max(closureResidual, centerResidual).toExponential(1)
      }
    );
    updateInstrumentOverlay(overlay, t, fps);
    if (readout) {
      readout.style.display = "block";
      readout.textContent = width < 620
        ? "5+1 CONSTITUTION · perimeter assay\n" +
          "fence " + (active + 1) + "/5 · " + activeFence.key + " · " + activeFence.tier + "\n" +
          "closure " + closureResidual.toExponential(1) + " · center " + centerResidual.toExponential(1) + "\n" +
          (REDUCED_MOTION ? "sample static" : sampleClock.label())
        : "5+1 CONSTITUTION · perimeter assay\n" +
          "active fence " + (active + 1) + "/5 · " + activeFence.key + " · " + activeFence.title + " · " + activeFence.tier + "\n" +
          "Ω is the directional +1, not a sixth refusal\n" +
          "closure residual |Σedges|/r = " + closureResidual.toExponential(1) + "\n" +
          "centroid offset = " + centerResidual.toExponential(1) + " · sample clock " + (REDUCED_MOTION ? "static" : sampleClock.label());
    }

    if (!REDUCED_MOTION) scheduleFrame(draw);
  }

  window.addEventListener("resize", () => {
    bounds = resize();
    if (REDUCED_MOTION) draw(0);
  });
  draw(0);
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

function setLinePoints(lineObject, points) {
  const safePoints = points.length > 1
    ? points
    : [points[0] || new THREE.Vector3(), points[0] || new THREE.Vector3()];
  lineObject.geometry.setFromPoints(safePoints);
}

function appendTrace(points, point, max = 120) {
  points.push(point.clone());
  if (points.length > max) points.shift();
}

function createPointTrace(max = 120, color = 0xffffff, opacity = 0.42, size = 0.026) {
  const geometry = new THREE.BufferGeometry();
  const positions = new Float32Array(max * 3);
  geometry.setAttribute("position", new THREE.BufferAttribute(positions, 3));
  geometry.setDrawRange(0, 0);
  const mesh = new THREE.Points(
    geometry,
    new THREE.PointsMaterial({
      color,
      size,
      transparent: true,
      opacity,
      sizeAttenuation: true,
      depthWrite: false
    })
  );
  return { max, mesh, positions };
}

function updatePointTrace(trace, samples) {
  if (!trace) return;
  const count = Math.min(samples.length, trace.max);
  const start = Math.max(0, samples.length - count);
  for (let i = 0; i < count; i += 1) {
    const p = samples[start + i];
    trace.positions[i * 3] = p.x;
    trace.positions[i * 3 + 1] = p.y;
    trace.positions[i * 3 + 2] = p.z;
  }
  trace.mesh.geometry.setDrawRange(0, count);
  trace.mesh.geometry.attributes.position.needsUpdate = true;
}

function createTickedRing(radius, color = 0xffffff, opacity = 0.38, tickCount = 40, tickLength = 0.045) {
  const group = new THREE.Group();
  group.add(ring(radius, color, opacity));
  for (let i = 0; i < tickCount; i += 1) {
    const a = (i / tickCount) * TAU;
    const major = i % 4 === 0;
    const len = tickLength * (major ? 1.8 : 1);
    const inner = radius - len;
    const outer = radius + len;
    group.add(line([
      new THREE.Vector3(inner * Math.cos(a), 0, inner * Math.sin(a)),
      new THREE.Vector3(outer * Math.cos(a), 0, outer * Math.sin(a))
    ], color, opacity * (major ? 0.72 : 0.45)));
  }
  return group;
}

function createXYTickedRing(radius, color = 0xffffff, opacity = 0.32, tickCount = 48, tickLength = 0.04) {
  const group = new THREE.Group();
  group.add(new THREE.Mesh(
    new THREE.TorusGeometry(radius, 0.009, 10, 192),
    makeMaterial(color, opacity)
  ));
  for (let i = 0; i < tickCount; i += 1) {
    const a = (i / tickCount) * TAU;
    const major = i % 6 === 0;
    const len = tickLength * (major ? 1.9 : 1);
    const inner = radius - len;
    const outer = radius + len;
    group.add(line([
      new THREE.Vector3(inner * Math.cos(a), inner * Math.sin(a), 0),
      new THREE.Vector3(outer * Math.cos(a), outer * Math.sin(a), 0)
    ], color, opacity * (major ? 0.78 : 0.44)));
  }
  return group;
}

function createStripChart(origin, width = 2.2, height = 0.52, color = 0x42a5f5, max = 96, label = "", labelColor = color, chartOptions = {}) {
  return createSharedStripChart(THREE, {
    origin,
    width,
    height,
    color,
    max,
    label,
    labelColor,
    frameOpacity: 0.28,
    traceOpacity: 0.64,
    cursorOpacity: 0.3,
    ...chartOptions
  });
}

function clearStripChart(chart) {
  if (!chart) return;
  clearSharedStripChart(THREE, chart);
}

function updateStripChart(chart, value, min = 0, max = 1, sampled = false) {
  if (!chart) return;
  updateSharedStripChart(THREE, chart, value, min, max, sampled);
}

function addReferenceFrame(scene) {
  const frame = new THREE.Group();
  const base = 0x7a7a7a;
  const axisMat = new THREE.LineBasicMaterial({ color: base, transparent: true, opacity: 0.28 });
  const tickMat = new THREE.LineBasicMaterial({ color: base, transparent: true, opacity: 0.18 });
  const extent = 3.2;
  const tick = 0.035;

  [
    [new THREE.Vector3(-extent, 0, 0), new THREE.Vector3(extent, 0, 0)],
    [new THREE.Vector3(0, -extent, 0), new THREE.Vector3(0, extent, 0)],
    [new THREE.Vector3(0, 0, -extent), new THREE.Vector3(0, 0, extent)]
  ].forEach((pts) => frame.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints(pts), axisMat)));

  for (let i = -3; i <= 3; i += 1) {
    if (i === 0) continue;
    const k = i;
    [
      [new THREE.Vector3(k, -tick, 0), new THREE.Vector3(k, tick, 0)],
      [new THREE.Vector3(-tick, k, 0), new THREE.Vector3(tick, k, 0)],
      [new THREE.Vector3(0, -tick, k), new THREE.Vector3(0, tick, k)]
    ].forEach((pts) => frame.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints(pts), tickMat)));
  }

  [1, 2, 3].forEach((radius) => {
    const xy = ring(radius, base, radius === 1 ? 0.18 : 0.1);
    xy.rotation.x = 0;
    const xz = ring(radius, base, radius === 1 ? 0.16 : 0.08);
    const yz = ring(radius, base, radius === 1 ? 0.14 : 0.07);
    yz.rotation.y = Math.PI / 2;
    frame.add(xy, xz, yz);
  });

  scene.add(frame);
}

function createSphere(radius = 1.4, opacity = 0.22, wseg = 88, hseg = 44) {
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
    const major = i === 0 || i === lines - 1 || i === Math.floor(lines / 2);
    const opacity = major ? 0.38 : 0.22;
    group.add(line([
      new THREE.Vector3(-half, 0, p),
      new THREE.Vector3(half, 0, p)
    ], 0xb8b8b8, opacity));
    group.add(line([
      new THREE.Vector3(p, 0, -half),
      new THREE.Vector3(p, 0, half)
    ], 0xb8b8b8, opacity));
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
      "position:absolute;left:16px;right:auto;top:auto;bottom:16px;z-index:5;max-width:68%;max-height:min(34vh,280px);" +
      "font:600 11px/1.55 'Roboto Mono',ui-monospace,Menlo,monospace;font-variant-numeric:tabular-nums;" +
      "color:var(--ink,#F3F4F6);pointer-events:none;letter-spacing:0;white-space:pre-line;text-align:left;" +
      "background:rgba(5,5,5,.9);padding:9px 12px;" +
      "border:1px solid rgba(255,255,255,.14);border-left:2px solid #FFEB3B;border-radius:2px;backdrop-filter:blur(4px);" +
      "box-shadow:none";
    visual.appendChild(el);
  }
  return el;
}

function isCompactInstrument(width = 0) {
  const measured = width || (visual ? visual.getBoundingClientRect().width : window.innerWidth);
  return measured < 700;
}

// Morphing horn torus driven by one-sided RAPIDITY. At w = 0 it is the horn
// touch (R = rt). As w grows, v/c = tanh(w) -> 1 and the major radius R tends
// to 0: the torus converges asymptotically toward the sphere/light boundary.
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
    f = Math.max(0.05, Math.min(0.985, f));
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
    const balanceChart = createStripChart(new THREE.Vector3(-1.42, -1.12, 0.04), 2.84, 0.46, 0x42a5f5, 120, "B=sech(ln x)", 0x42a5f5, {
      targetValue: 1,
      targetBand: [0.94, 1],
      targetColor: 0xffeb3b
    });
    root.add(xPt); root.add(invPt); root.add(ePt); root.add(arc, balanceChart.group);
    if (visual) {
      visual.addEventListener("instrument:zero", () => clearStripChart(balanceChart));
    }

    const readout = makeReadout();
    if (readout) {
      readout.style.whiteSpace = "pre-line";
      readout.style.left = "auto";
      readout.style.right = "16px";
      readout.style.top = "92px";
      readout.style.bottom = "auto";
      readout.style.maxWidth = "min(390px, 44%)";
      readout.classList.add("instrument-readout", "logline-readout");
    }
    dyn.push(function (t, sampled) {
      const logPhase = phase01(t, INSTRUMENT_CPS.medium);
      const s = -2.9 + smooth01(sweep01(t, INSTRUMENT_CPS.medium)) * 5.8; // sweep in log coordinates
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
      const balance = 1 / Math.cosh(Math.log(x));
      const reciprocalResidual = Math.abs(x * (1 / x) - 1);
      updateStripChart(balanceChart, balance, 0, 1, sampled);
      setInstrumentMetric(
        "s " + s.toFixed(2) + " · B " + balance.toFixed(3),
        "x·1/x=1",
        "phase " + logPhase.toFixed(2),
        "σ x·1/x " + reciprocalResidual.toExponential(1),
        {
          primary: balance,
          primaryLabel: "B",
          primaryText: balance.toFixed(3),
          secondary: Math.abs(u),
          secondaryLabel: "|u|",
          secondaryText: Math.abs(u).toFixed(3),
          error: clamp01(reciprocalResidual * 1e6),
          errorText: reciprocalResidual.toExponential(1)
        }
      );
      if (readout) readout.textContent = isCompactInstrument()
        ? "D1 RECIPROCAL LINE · " + (sampled ? "SAMPLE" : "HOLD") + "\n" +
          "s=" + s.toFixed(2) + " · x=" + x.toFixed(2) + " · 1/x=" + (1 / x).toFixed(2) + "\n" +
          "B=" + balance.toFixed(3) + " · E=" + E.toFixed(2) + " · u=" + u.toFixed(2) + "\n" +
          "σ(x·1/x−1)=" + reciprocalResidual.toExponential(1)
        : "D1 RECIPROCAL LINE · LOG-COORDINATE ASSAY\n" +
          "s=log₂x " + s.toFixed(2) + " · x " + x.toFixed(2) + " · 1/x " + (1 / x).toFixed(2) + " · x·1/x 1\n" +
          "B=sech(lnx) " + balance.toFixed(3) + " · E=(lnx)² " + E.toFixed(2) + " · u=(x−1)/(x+1) " + u.toFixed(2) + "\n" +
          "residual σ(x·1/x−1)=" + reciprocalResidual.toExponential(1) + " · chart: sampled B history";
    });
  }

  if (mode === "muLimit") {
    root.add(line([
      new THREE.Vector3(-2.4, 0, 0),
      new THREE.Vector3(2.4, 0, 0)
    ], 0xffffff, 0.9));
    const grid = createGridPlane(3.2, 11);
    root.add(grid);
    const liftTrace = line([new THREE.Vector3(-1.8, 0, 0)], 0xffeb3b, 0.34);
    const projectionTrace = line([new THREE.Vector3(-1.8, 0, 0)], 0x42a5f5, 0.22);
    const liftSamples = [];
    const projectionSamples = [];
    const liftDots = createPointTrace(160, 0xffeb3b, 0.5, 0.032);
    const projectionDots = createPointTrace(160, 0x42a5f5, 0.42, 0.025);
    const liftChart = createStripChart(new THREE.Vector3(-1.48, -1.28, 0.06), 2.96, 0.46, 0x42a5f5, 120, "μ lift");
    if (visual) {
      visual.addEventListener("instrument:zero", () => {
        liftSamples.length = 0;
        projectionSamples.length = 0;
        clearStripChart(liftChart);
      });
    }
    root.add(line([
      new THREE.Vector3(-1.8, 0, 0),
      new THREE.Vector3(0, 1.6, 0),
      new THREE.Vector3(1.8, 0, 0)
    ], 0xb8b8b8, 0.9));
    const sample = makeMarker(new THREE.Vector3(-1.8, 0, 0), 0xffeb3b, 0.075);
    const projection = makeMarker(new THREE.Vector3(-1.8, 0, 0), 0xffffff, 0.045);
    const liftLine = line([
      new THREE.Vector3(-1.8, 0, 0),
      new THREE.Vector3(-1.8, 0, 0)
    ], 0xffeb3b, 0.65);
    root.add(liftTrace, projectionTrace, liftDots.mesh, projectionDots.mesh, sample, projection, liftLine, liftChart.group);
    const readout = makeReadout();
    if (readout) {
      readout.style.left = "auto";
      readout.style.right = "16px";
      readout.style.top = "auto";
      readout.style.bottom = "70px";
      readout.style.maxWidth = "min(430px, 46%)";
      readout.classList.add("instrument-readout", "mu-readout");
    }
    dyn.push((t, sampled) => {
      const muPhase = phase01(t, INSTRUMENT_CPS.medium);
      const p = smooth01(sweep01(t, INSTRUMENT_CPS.medium));
      const x = -1.8 + 3.6 * p;
      const lift = 1.6 * Math.max(0, 1 - Math.abs(2 * p - 1));
      const onLine = new THREE.Vector3(x, 0, 0);
      const onPlane = new THREE.Vector3(x, lift, 0);
      sample.position.copy(onPlane);
      projection.position.copy(onLine);
      liftLine.geometry.setFromPoints([onLine, onPlane]);
      if (sampled) {
        appendTrace(liftSamples, onPlane, 160);
        appendTrace(projectionSamples, onLine, 160);
      }
      setLinePoints(liftTrace, liftSamples);
      setLinePoints(projectionTrace, projectionSamples);
      updatePointTrace(liftDots, liftSamples);
      updatePointTrace(projectionDots, projectionSamples);
      updateStripChart(liftChart, lift, 0, 1.6, sampled);
      const projectionResidual = Math.abs(onPlane.x - onLine.x);
      setInstrumentMetric(
        "λ " + p.toFixed(2) + " · μ " + lift.toFixed(2),
        "orthogonal lift",
        "phase " + muPhase.toFixed(2),
        "σ projection " + projectionResidual.toExponential(1),
        {
          primary: lift / 1.6,
          primaryLabel: "μ",
          primaryText: lift.toFixed(2),
          secondary: p,
          secondaryLabel: "λ",
          secondaryText: p.toFixed(2),
          error: clamp01(projectionResidual * 20),
          errorText: projectionResidual.toExponential(1)
        }
      );
      if (readout) readout.textContent = isCompactInstrument()
        ? "D2 μ-LIMIT · LIFT ASSAY\n" +
          "λ=" + p.toFixed(2) + " · μ=" + lift.toFixed(2) + "\n" +
          "σ projection=" + projectionResidual.toExponential(1) + "\n" +
          "state: off-axis coordinate sampled"
        : "D2 μ-LIMIT · LINE-TO-PLANE ASSAY\n" +
          "λ=" + p.toFixed(2) + " · μ=" + lift.toFixed(2) + " · projection σ=" + projectionResidual.toExponential(1) + "\n" +
          "state: local coordinate gains one off-axis degree of freedom\n" +
          "chart: sampled μ lift history";
    });
  }

  if (mode === "bloch") {
    // The Bloch / Riemann sphere STANDS ON the complex plane (tangent at 0,
    // the south pole) and projects DOWNWARD: a straight ray from ∞ (north
    // pole) through the surface point P lands on the floor at 2r·cot(θ/2) —
    // the same tangent-plane stereographic projection the Burrisphere dualises.
    // The equator's shadow on the floor is the unit circle (φ = 1).
    const r = 1.0;
    const N = new THREE.Vector3(0, r, 0), Sp = new THREE.Vector3(0, -r, 0);
    const floor = createGridPlane(8.0, 21); floor.position.y = -r; root.add(floor);
    root.add(createSphere(r, 0.26));
    root.add(ring(r, 0xffffff, 0.85));                          // the equator (φ = 1 up here)
    const unitC = createTickedRing(2 * r, 0xffeb3b, 0.48, 48);   // its shadow: the unit circle on ℂ
    unitC.position.y = -r; root.add(unitC);
    root.add(makeMarker(N, 0xb8b8b8, 0.07));                    // ∞
    root.add(makeMarker(Sp, 0x707070, 0.07));                   // 0 — where the sphere touches ℂ
    const projectionRay = line([N, new THREE.Vector3(2 * r, -r, 0)], 0xffeb3b, 0.9);
    const pMarker = makeMarker(new THREE.Vector3(r, 0, 0), 0xffffff, 0.08);
    const landMarker = makeMarker(new THREE.Vector3(2 * r, -r, 0), 0xffeb3b, 0.07);
    const surfaceTrace = line([new THREE.Vector3(r, 0, 0)], 0xffffff, 0.28);
    const landingTrace = line([new THREE.Vector3(2 * r, -r, 0)], 0x42a5f5, 0.28);
    const surfaceSamples = [];
    const landingSamples = [];
    const surfaceDots = createPointTrace(150, 0xffffff, 0.42, 0.024);
    const landingDots = createPointTrace(150, 0x42a5f5, 0.48, 0.026);
    const balanceChart = createStripChart(new THREE.Vector3(-1.52, -1.54, 0.06), 3.04, 0.48, 0x42a5f5, 120, "B=sin theta", 0x42a5f5, {
      targetValue: 1,
      targetBand: [0.94, 1],
      targetColor: 0xffeb3b
    });
    if (visual) {
      visual.addEventListener("instrument:zero", () => {
        surfaceSamples.length = 0;
        landingSamples.length = 0;
        clearStripChart(balanceChart);
      });
    }
    root.add(surfaceTrace, landingTrace, surfaceDots.mesh, landingDots.mesh, projectionRay, pMarker, landMarker, balanceChart.group);
    const readout = makeReadout();
    if (readout) {
      readout.style.left = "auto";
      readout.style.right = "16px";
      readout.style.top = "92px";
      readout.style.bottom = "auto";
      readout.style.maxWidth = "min(430px, 46%)";
      readout.classList.add("instrument-readout", "bloch-readout");
    }
    dyn.push((t, sampled) => {
      const projectionPhase = phase01(t, INSTRUMENT_CPS.medium);
      const p = smooth01(sweep01(t, INSTRUMENT_CPS.medium));
      const th = (55 + 70 * p) * Math.PI / 180;
      const P = new THREE.Vector3(r * Math.sin(th), r * Math.cos(th), 0);
      const land = new THREE.Vector3(2 * r / Math.tan(th / 2), -r, 0);
      pMarker.position.copy(P);
      landMarker.position.copy(land);
      projectionRay.geometry.setFromPoints([N, land]);
      if (sampled) {
        appendTrace(surfaceSamples, P, 150);
        appendTrace(landingSamples, land, 150);
      }
      setLinePoints(surfaceTrace, surfaceSamples);
      setLinePoints(landingTrace, landingSamples);
      updatePointTrace(surfaceDots, surfaceSamples);
      updatePointTrace(landingDots, landingSamples);
      const phi = 1 / Math.tan(th / 2);
      const nu = Math.tan(th / 2);
      const balance = Math.sin(th);
      const landingRadius = Math.abs(land.x);
      const expectedLandingRadius = 2 * r * phi;
      const reciprocalResidual = Math.abs(phi * nu - 1);
      const landingResidual = Math.abs(landingRadius - expectedLandingRadius);
      updateStripChart(balanceChart, balance, 0, 1, sampled);
      setInstrumentMetric(
        "θ " + (th * 180 / Math.PI).toFixed(1) + "° · B " + balance.toFixed(3),
        "tangent projection",
        "phase " + projectionPhase.toFixed(2),
        "σ φν " + reciprocalResidual.toExponential(1) + " · ρ " + landingResidual.toExponential(1),
        {
          primary: balance,
          primaryLabel: "B",
          primaryText: balance.toFixed(3),
          secondary: clamp01(landingRadius / (4 * r)),
          secondaryLabel: "ρ",
          secondaryText: landingRadius.toFixed(2),
          error: clamp01((reciprocalResidual * 1e6) + landingResidual),
          errorText: Math.max(reciprocalResidual, landingResidual).toExponential(1)
        }
      );
      if (readout) readout.textContent = isCompactInstrument()
        ? "D3 TANGENT PROJECTION\n" +
          "θ=" + (th * 180 / Math.PI).toFixed(1) + "° · φ=" + phi.toFixed(2) + " · ν=" + nu.toFixed(2) + "\n" +
          "B=" + balance.toFixed(3) + " · ρ=" + landingRadius.toFixed(2) + " · σρ=" + landingResidual.toExponential(1)
        : "D3 RIEMANN/BLOCH · TANGENT PROJECTION\n" +
          "θ=" + (th * 180 / Math.PI).toFixed(1) + "° · φ=cot(θ/2) " + phi.toFixed(2) + " · ν=tan(θ/2) " + nu.toFixed(2) + " · φν=1\n" +
          "B=sinθ " + balance.toFixed(3) + " · landing ρ " + landingRadius.toFixed(2) + " · expected 2rφ " + expectedLandingRadius.toFixed(2) + "\n" +
          "residuals: σφν " + reciprocalResidual.toExponential(1) + " · σρ " + landingResidual.toExponential(1);
    });
  }

  if (mode === "horn") {
    if (visual) visual.classList.add("horn-visual");
    // The horn torus STANDS ON the complex plane the Riemann sphere stands on.
    // At rest (rapidity w = 0) it is a HORN: the throat touches at a single
    // relative centre on the fixed plane / unit circle |z|=1. A one-way rapidity
    // slider sends w toward infinity: β tends to c, R/r tends to 0, and the
    // finite drawing approaches the sphere limit without pretending to reach it.
    root.add(createGridPlane(6.4, 21));                          // the complex plane
    root.add(createTickedRing(1.0, 0xffeb3b, 0.52, 40));          // unit circle |z|=1  (x=1, Suda)
    root.add(line([new THREE.Vector3(-3.1, 0, 0), new THREE.Vector3(3.1, 0, 0)], 0x555555, 0.55));
    root.add(line([new THREE.Vector3(0, 0, -3.1), new THREE.Vector3(0, 0, 3.1)], 0x555555, 0.55));
    const torus = makeMorphTorus(1.7, 84, 24, 0xffffff);        // calibrated wire density; high enough to read, light enough to run
    root.add(torus.mesh);
    const limitShell = createSphere(1.7, 0.045, 88, 44);
    limitShell.material.color.setHex(0x42a5f5);
    const limitGauge = createXYTickedRing(1.7, 0x42a5f5, 0.12, 72, 0.035);
    root.add(limitShell, limitGauge);
    const relCentre = ring(0.12, 0xffeb3b, 0.95);               // the relative centre on the plane (a ring, no dot)
    const properTimeGauge = createTickedRing(1.0, 0x42a5f5, 0.36, 40);
    properTimeGauge.position.y = 0.014;
    const rapidityTrace = line([new THREE.Vector3(0, 0.018, 0), new THREE.Vector3(0, 0.018, 0)], 0x42a5f5, 0.58);
    const properTimeChart = createStripChart(new THREE.Vector3(-1.55, -1.58, 0.08), 3.1, 0.42, 0x42a5f5, 120, "dτ/dt = 1/γ", 0x42a5f5, {
      targetValue: 1,
      targetBand: [0.94, 1],
      targetColor: 0xffeb3b
    });
    root.add(properTimeGauge, rapidityTrace, relCentre, properTimeChart.group);

    const readout = makeReadout();
    if (readout) {
      readout.style.whiteSpace = "pre-line";
      readout.style.maxWidth = "min(440px, 46%)";
      readout.style.top = "auto";
      readout.style.bottom = "70px";
      readout.classList.add("instrument-readout", "horn-readout");
    }
    const W_MAX = 4.5;                                          // ends: v/c -> 0.9998, γ -> ~45
    const G_MAX = Math.cosh(W_MAX);
    let userActive = false, slider = null, sliderControl = null;
    if (visual) {
      sliderControl = createModelSlider({
        className: "rapidity-slider",
        leftLabel: "w=0 · horn",
        rightLabel: "w→∞ · sphere limit",
        value: "0",
        ariaLabel: "rapidity from horn touch toward the infinite light-speed sphere limit"
      });
      slider = sliderControl ? sliderControl.input : null;
      if (slider) slider.addEventListener("input", () => { userActive = true; });
      if (sliderControl) sliderControl.setOutput("w = 0.00");
      visual.dataset.midLabel = "rest";
      visual.addEventListener("instrument:zero", () => {
        userActive = false;
        if (slider) slider.value = "0";
        if (sliderControl) sliderControl.setOutput("w = 0.00");
        clearStripChart(properTimeChart);
      });
    }
    dyn.push(function (t, sampled) {
      let w;
      if (userActive && slider) {
        w = (parseFloat(slider.value) / 100) * W_MAX;            // slider is LINEAR in rapidity = LOG in velocity
      } else {
        w = smooth01(sweep01(t, INSTRUMENT_CPS.slow)) * W_MAX * 0.92; // measured rapidity sweep until the user grabs the slider
        if (slider) slider.value = String(Math.round((w / W_MAX) * 100));
      }
      if (sliderControl) sliderControl.setOutput("w = " + w.toFixed(2));
      const vc = Math.tanh(w);                                  // β = v/c — tends to 1
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
      limitShell.material.opacity = 0.035 + 0.12 * clamp01(gamma / G_MAX);
      limitGauge.scale.setScalar(0.98 + 0.02 * clamp01(gamma / G_MAX));
      limitGauge.traverse((o) => { if (o.material) o.material.opacity = 0.08 + 0.15 * clamp01(gamma / G_MAX); });
      // the relative centre moves on the complex plane (log-compressed real axis)
      const px = 2.5 * Math.tanh(w / 2.2);
      relCentre.position.set(px, 0, 0);
      relCentre.scale.setScalar(1 + 0.45 * aB);
      properTimeGauge.scale.setScalar(Math.max(0.04, 1 / gamma));
      rapidityTrace.geometry.setFromPoints([
        new THREE.Vector3(0, 0.018, 0),
        new THREE.Vector3(px, 0.018, 0)
      ]);
      updateStripChart(properTimeChart, 1 / gamma, 0, 1, sampled);
      root.rotation.y = 0;
      const moving = w > 0.02;
      const morphResidual = Math.abs((g.R / Math.max(g.rt, 1e-9)) - (1 / gamma));
      setInstrumentMetric(
        "w " + w.toFixed(2) + " · γ " + gamma.toFixed(1),
        "dτ/dt " + (1 / gamma).toFixed(3),
        "phase " + clamp01(w / W_MAX).toFixed(2),
        "σ R/r " + morphResidual.toExponential(1),
        {
          primary: 1 / gamma,
          primaryLabel: "dτ/dt",
          primaryText: (1 / gamma).toFixed(3),
          secondary: vc,
          secondaryLabel: "β",
          secondaryText: vc.toFixed(4),
          error: clamp01(morphResidual * 40),
          errorText: morphResidual.toExponential(1)
        }
      );
      if (readout) {
        const limitState = !moving
          ? "rest: E=mc² · R=r"
          : gamma > 20
            ? "asymptote: γmc² diverges"
            : "approach: β tends to c";
        readout.textContent = isCompactInstrument()
          ? "D4 HORN · RAPIDITY 0→∞\n" +
            "w=" + w.toFixed(2) + " · β=" + vc.toFixed(4) + " · γ=" + gamma.toFixed(1) + "\n" +
            "R/r=" + (1 / gamma).toFixed(3) + " · dτ/dt=" + (1 / gamma).toFixed(3) + "\n" +
            "σ(R/r)=" + morphResidual.toExponential(1) + " · " + limitState
          : "D4 HORN · RAPIDITY ASSAY\n" +
            "w=" + w.toFixed(2) + " · β=" + vc.toFixed(4) + " · γ=" + gamma.toFixed(1) + " · E/mc²=γ\n" +
            "R/r=dτ/dt=" + (1 / gamma).toFixed(3) + " · k=e^w=" + k.toFixed(2) + " · σ(R/r)=" + morphResidual.toExponential(1) + "\n" +
            "chart: sampled proper-time ratio · " +
            "limit: " + limitState;
      }
    });
  }

  if (mode === "burrisphere") {
    if (visual) visual.classList.add("burrisphere-visual");
    // THE DUAL TANGENT-PLANE STEREOGRAPHIC PROJECTION — the real geometry.
    // The sphere is sandwiched between two copies of the SAME complex plane:
    // the floor touches it at 0 (south pole), the top plane touches it at ∞
    // (north pole). From ∞ a straight ray through P lands DOWN on the floor at
    // radius 2r·cot(θ/2) = 2r·φ; from 0 a straight ray through P lands UP on
    // the top plane at 2r·tan(θ/2) = 2r·ν. Both rays pass through P — the two
    // projections meet ON the sphere. φ·ν = 1 throughout. The unit circles
    // (radius 2r on each plane) are the equator's two shadows: the φ/ν
    // balance boundary. As ψ rotates while θ sweeps, both landings SPIRAL through the
    // quadrants — reciprocal radii, crossing their unit circles together.
    const r = 1.0;
    const N = new THREE.Vector3(0, r, 0);                            // ○ ∞ — the top plane touches here (Brahmā's sign)
    const S = new THREE.Vector3(0, -r, 0);                           // • 0 — the floor touches here (Śiva's sign)
    const FORESIGHT = 0xffeb3b, MEANS = 0x42a5f5, BALANCED = 0xf3f4f6;
    const U = 2 * r;                                                 // unit-circle radius on a tangent plane

    root.add(createSphere(r, 0.22));
    root.add(ring(r, FORESIGHT, 0.8));                                // the equator — Φ/V balance boundary on the sphere
    [0.45, 0.8].forEach((y) => {
      const lat = ring(Math.sqrt(r * r - y * y), 0x666666, 0.3);
      lat.position.y = y; root.add(lat);
      const m = lat.clone(); m.position.y = -y; root.add(m);
    });

    // the two tangent copies of the same complex plane (floor at 0, top at ∞)
    [-r, r].forEach((y) => {
      const g = createGridPlane(9.0, 21); g.position.y = y; root.add(g);
      const u = createTickedRing(U, FORESIGHT, 0.46, 56); u.position.y = y; root.add(u); // unit circle = the equator's shadow
      root.add(line([new THREE.Vector3(-4.5, y, 0), new THREE.Vector3(4.5, y, 0)], 0x555555, 0.5));
      root.add(line([new THREE.Vector3(0, y, -4.5), new THREE.Vector3(0, y, 4.5)], 0x555555, 0.5));
    });
    root.add(makeMarker(N, 0xc8c8c8, 0.07));
    root.add(makeMarker(S, 0x8a8a8a, 0.07));

    // four quadrant probes on the ∞-plane (the ν-chart): balanced/foresight
    // samples stay inside the unit circle; means-heavy samples fall outside.
    [[0.9, 0.9, FORESIGHT], [-0.9, 0.9, FORESIGHT], [-2.2, -2.2, MEANS], [2.2, -2.2, MEANS]]
      .forEach((o) => root.add(makeMarker(new THREE.Vector3(o[0], r, o[1]), o[2], 0.06)));

    // Map the instrument into quadrants without moralizing the geometry. The
    // ∞-plane splits by two axes: Im(z) = foresight-heavy / means-heavy,
    // Re(x) = outward / inward move orientation.
    // The OVERLAP is the unit-circle disc (the equator's shadow): the region
    // where the φ-chart and ν-chart coincide and all four moves meet at balance
    // — ⊙1, L4. It is a calibrated target band, not an automatic moral verdict.
    const quadTint = (sx, sz, color) => {
      const m = new THREE.Mesh(
        new THREE.PlaneGeometry(U, U),
        new THREE.MeshBasicMaterial({ color, transparent: true, opacity: 0.08, side: THREE.DoubleSide, depthWrite: false }));
      m.rotation.x = -Math.PI / 2;
      m.position.set(sx * U / 2, r + 0.004, sz * U / 2);
      root.add(m);
    };
    quadTint(1, 1, FORESIGHT); quadTint(-1, 1, FORESIGHT); // Im>0 — Φ-heavy
    quadTint(-1, -1, MEANS); quadTint(1, -1, MEANS);       // Im<0 — V-heavy
    const overlap = new THREE.Mesh(
      new THREE.CircleGeometry(U, 48),
      new THREE.MeshBasicMaterial({ color: FORESIGHT, transparent: true, opacity: 0.11, side: THREE.DoubleSide, depthWrite: false }));
    overlap.rotation.x = -Math.PI / 2; overlap.position.y = r + 0.006; root.add(overlap); // the balance overlap (⊙1 / L4)

    // THE TRANSCENDENTALS ARE THE STATIONS OF THE GEOMETRY ITSELF — the
    // {0, 1, ∞} scaffold the game is played on: • 0 at the floor touch,
    // ○ ∞ at the top touch, ⊙ 1 at the centre (the gold equator is the
    // circle of the ⊙ glyph). The Titans READ these signs from latitudes —
    // Śiva reads •, Brahmā reads ○, Viṣṇu reads ⊙ — they are not seated at
    // the poles (the pole ROWS are L0 Kāla / L∞ Trimūrti per the nine-row).
    root.add(makeMarker(new THREE.Vector3(0, 0, 0), 0xffeb3b, 0.055)); // ⊙ — the One at the centre (Viṣṇu's sign)

    const pMark = makeMarker(new THREE.Vector3(r, 0, 0), 0xffffff, 0.085); // P — where the two rays meet
    const rayDown = line([N, new THREE.Vector3(U, -r, 0)], FORESIGHT, 0.8);  // ∞ → P → floor: lands at 2r·φ
    const rayUp = line([S, new THREE.Vector3(U, r, 0)], FORESIGHT, 0.8);     // 0 → P → top: lands at 2r·ν
    const phiPt = makeMarker(new THREE.Vector3(U, -r, 0), FORESIGHT, 0.07);  // the φ landing (floor)
    const nuPt = makeMarker(new THREE.Vector3(U, r, 0), FORESIGHT, 0.07);    // the ν landing (top)
    root.add(pMark); root.add(rayDown); root.add(rayUp); root.add(phiPt); root.add(nuPt);

    // the two spiral trails traced by the landings — reciprocal radii
    const TRAIL = 150, phiTrail = [], nuTrail = [], pointTrail = [];
    const phiDots = createPointTrace(TRAIL, FORESIGHT, 0.48, 0.026);
    const nuDots = createPointTrace(TRAIL, MEANS, 0.46, 0.026);
    const pointDots = createPointTrace(TRAIL, 0xffffff, 0.4, 0.021);
    if (visual) {
      visual.addEventListener("instrument:zero", () => {
        phiTrail.length = 0;
        nuTrail.length = 0;
        pointTrail.length = 0;
      });
    }
    const phiLine = line([new THREE.Vector3(U, -r, 0)], 0xffeb3b, 0.24);
    const nuLine = line([new THREE.Vector3(U, r, 0)], 0x42a5f5, 0.24);
    const pointLine = line([new THREE.Vector3(r, 0, 0)], 0xffffff, 0.18);
    const phiRange = createTickedRing(U, FORESIGHT, 0.2, 56);
    const nuRange = createTickedRing(U, MEANS, 0.2, 56);
    phiRange.position.y = -r + 0.01;
    nuRange.position.y = r + 0.01;
    const balanceChart = createStripChart(new THREE.Vector3(-1.7, -1.36, 0.08), 3.4, 0.42, 0x42a5f5, 120, "U_B bridge", 0x42a5f5, {
      targetValue: 1,
      targetBand: [0.94, 1],
      targetColor: 0xffeb3b
    });
    root.add(phiRange, nuRange, phiLine, nuLine, pointLine, phiDots.mesh, nuDots.mesh, pointDots.mesh, balanceChart.group);

    const readout = makeReadout();
    if (readout) {
      readout.style.whiteSpace = "pre-line";
      readout.style.top = "auto";
      readout.style.bottom = "70px";
      readout.style.maxWidth = "min(520px, 52%)";
      readout.classList.add("instrument-readout", "burrisphere-readout");
    }
    const THETA_MIN = 0.12;
    const THETA_MAX = Math.PI - 0.12;
    let thetaUserActive = false;
    let thetaSlider = null;
    let thetaSliderControl = null;
    if (visual) {
      thetaSliderControl = createModelSlider({
        className: "theta-slider",
        leftLabel: "Φ sight",
        rightLabel: "V means",
        value: "50",
        ariaLabel: "theta latitude from D5 worldline foresight through balance to D4 means-to-act"
      });
      thetaSlider = thetaSliderControl ? thetaSliderControl.input : null;
      if (thetaSlider) thetaSlider.addEventListener("input", () => { thetaUserActive = true; });
      if (thetaSliderControl) thetaSliderControl.setOutput("θ = 90°");
      visual.addEventListener("instrument:zero", () => {
        thetaUserActive = false;
        if (thetaSlider) thetaSlider.value = "50";
        if (thetaSliderControl) thetaSliderControl.setOutput("θ = 90°");
        clearStripChart(balanceChart);
      });
    }
    const thetaFromSlider = () => {
      const p = thetaSlider ? parseFloat(thetaSlider.value) / 100 : 0.5;
      return THETA_MIN + Math.max(0, Math.min(1, p)) * (THETA_MAX - THETA_MIN);
    };
    const sliderFromTheta = (theta) =>
      Math.round(((theta - THETA_MIN) / (THETA_MAX - THETA_MIN)) * 100);
    const quadName = ["I", "II", "III", "IV"];
    const D5_SWEEP_CPS = INSTRUMENT_CPS.slow;
    const D5_BALANCE_OFFSET = 0.25 / D5_SWEEP_CPS;
    function pointLineResidual(a, p, b) {
      const ab = b.clone().sub(a);
      const ap = p.clone().sub(a);
      return ap.cross(ab).length() / Math.max(ab.length(), 1e-9);
    }
    dyn.push(function (t, sampled) {
      const psi = t * 0.12;                                          // measured azimuth trace
      const theta = thetaUserActive
        ? thetaFromSlider()
        : THETA_MIN + smooth01(sweep01(t + D5_BALANCE_OFFSET, D5_SWEEP_CPS)) * (THETA_MAX - THETA_MIN); // auto-sweep from the calibrated balance latitude
      if (!thetaUserActive && thetaSlider) thetaSlider.value = String(sliderFromTheta(theta));
      if (thetaSliderControl) thetaSliderControl.setOutput("θ = " + Math.round(theta * 180 / Math.PI) + "°");
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
      phiRange.scale.setScalar(Math.min(phi, 4.5 / U));
      nuRange.scale.setScalar(Math.min(nu, 4.5 / U));
      phiRange.visible = Number.isFinite(phi);
      nuRange.visible = Number.isFinite(nu);
      const BALANCE_EPSILON = 0.015;
      const isBalance = Math.abs(phi - 1) <= BALANCE_EPSILON;        // the equator: φ = ν = 1
      const isForesightDominant = phi > 1 + BALANCE_EPSILON;         // P above the equator
      const col = isBalance ? BALANCED : isForesightDominant ? FORESIGHT : MEANS;
      [pMark, phiPt, nuPt].forEach((m) => m.material.color.setHex(col));
      rayDown.material.color.setHex(col);
      rayUp.material.color.setHex(col);
      if (sampled) {
        appendTrace(phiTrail, Lphi, TRAIL);
        appendTrace(nuTrail, Lnu, TRAIL);
        appendTrace(pointTrail, P, TRAIL);
      }
      setLinePoints(phiLine, phiTrail);
      setLinePoints(nuLine, nuTrail);
      setLinePoints(pointLine, pointTrail);
      updatePointTrace(phiDots, phiTrail);
      updatePointTrace(nuDots, nuTrail);
      updatePointTrace(pointDots, pointTrail);
      root.rotation.y = 0;
      const q = quadName[Math.floor((((psi % (2 * Math.PI)) + 2 * Math.PI) % (2 * Math.PI)) / (Math.PI / 2)) % 4];
      const opName = isBalance
        ? "equator calibration"
        : isForesightDominant
          ? "φ-dominant sector"
          : "ν-dominant sector";
      const moveName = isBalance
        ? "BALANCED (φ≈ν≈1)"
        : isForesightDominant
          ? "D5 sight proxy > D4 means proxy"
          : "D4 means proxy > D5 sight proxy";
      const balance = Math.sin(theta);
      const imbalance = Math.abs(Math.log(Math.max(phi, 1e-6)));
      const energyCost = 1 / Math.max(balance, 1e-6);
      const reciprocalResidual = Math.abs(phi * nu - 1);
      const rayResidual = Math.max(pointLineResidual(N, P, Lphi), pointLineResidual(S, P, Lnu));
      const finiteCouplingProxy = balance;
      updateStripChart(balanceChart, finiteCouplingProxy, 0, 1, sampled);
      setInstrumentMetric(
        "B " + balance.toFixed(3) + " · U " + finiteCouplingProxy.toFixed(3),
        thetaUserActive ? "manual latitude" : "reciprocal sweep",
        "phase " + (((psi % TAU) + TAU) % TAU / TAU).toFixed(2),
        "σ φν " + reciprocalResidual.toExponential(1) + " · ray " + rayResidual.toExponential(1),
        {
          primary: balance,
          primaryLabel: "B",
          primaryText: balance.toFixed(3),
          secondary: 1 / (1 + imbalance),
          secondaryLabel: "1/(1+|lnφ|)",
          secondaryText: (1 / (1 + imbalance)).toFixed(3),
          error: clamp01((reciprocalResidual * 1e6) + rayResidual * 18),
          errorText: Math.max(reciprocalResidual, rayResidual).toExponential(1)
        }
      );
      if (readout) readout.textContent = isCompactInstrument()
        ? "D5 BURRISPHERE · DUAL PROJECTION\n" +
          "θ=" + (theta * 180 / Math.PI).toFixed(0) + "° " + (thetaUserActive ? "hold" : "sweep") + " · φ=" + phi.toFixed(2) + " · ν=" + nu.toFixed(2) + "\n" +
          "B=" + balance.toFixed(3) + " · U_B=" + finiteCouplingProxy.toFixed(3) + " · γ≈" + energyCost.toFixed(2) + "\n" +
          "σφν=" + reciprocalResidual.toExponential(1) + " · σray=" + rayResidual.toExponential(1) + "\n" +
          "quadrant " + q + " · " + opName
        : "D5 BURRISPHERE · DUAL-PROJECTION ASSAY\n" +
          "θ=" + (theta * 180 / Math.PI).toFixed(0) + "° " + (thetaUserActive ? "hold" : "sweep") + " · φ=" + phi.toFixed(2) + " · ν=" + nu.toFixed(2) + " · φν=1\n" +
          "B=" + balance.toFixed(3) + " · U_B=" + finiteCouplingProxy.toFixed(3) + " · γ≈" + energyCost.toFixed(2) + " · |lnφ|=" + imbalance.toFixed(2) + "\n" +
          "σφν=" + reciprocalResidual.toExponential(1) + " · σray=" + rayResidual.toExponential(1) + " · chart: sampled bridge viability\n" +
          "state: quadrant " + q + " · " + opName + " · " + moveName;
    });
  }

  if (mode === "ccc") {
    if (visual) visual.classList.add("ccc-visual");
    const readout = makeReadout();
    if (readout) {
      readout.style.maxWidth = "min(430px, 46%)";
      readout.style.whiteSpace = "pre-line";
      readout.style.top = "auto";
      readout.style.bottom = "70px";
      readout.style.left = "16px";
      readout.style.right = "auto";
      readout.classList.add("instrument-readout", "ccc-readout");
    }
    const cccRing = (color, opacity = 1, tube = 0.012) => new THREE.Mesh(
      new THREE.TorusGeometry(1, tube, 12, 192),
      makeMaterial(color, opacity)
    );
    const boundaryRadius = 1.82;
    const boundary = cccRing(0xffffff, 0.24, 0.009);
    boundary.scale.setScalar(boundaryRadius);
    root.add(boundary);
    const boundaryGauge = createXYTickedRing(boundaryRadius, 0xffffff, 0.22, 72, 0.035);
    root.add(boundaryGauge);

    const aeonShell = cccRing(0xffffff, 0.74, 0.011);
    const conformalShell = cccRing(0x42a5f5, 0.42, 0.009);
    root.add(aeonShell, conformalShell);

    const originDot = new THREE.Mesh(
      new THREE.SphereGeometry(0.065, 32, 16),
      makeMaterial(0xffffff, 0.96)
    );
    const boundaryDot = new THREE.Mesh(
      new THREE.SphereGeometry(0.045, 24, 12),
      makeMaterial(0xffeb3b, 0.9)
    );
    root.add(originDot, boundaryDot);

    const graphX0 = 0.28;
    const graphW = 2.95;
    const graphY = -1.48;
    root.add(line([
      new THREE.Vector3(graphX0, graphY, 0.02),
      new THREE.Vector3(graphX0 + graphW, graphY, 0.02)
    ], 0xffffff, 0.2));
    root.add(line([
      new THREE.Vector3(graphX0, graphY, 0.02),
      new THREE.Vector3(graphX0, graphY + 0.54, 0.02)
    ], 0xffffff, 0.16));
    const expansionCurve = [];
    const inverseCurve = [];
    for (let i = 0; i <= 96; i += 1) {
      const q = i / 96;
      const x = graphX0 + q * graphW;
      expansionCurve.push(new THREE.Vector3(x, graphY + 0.08 + 0.42 * smooth01(q), 0.02));
      inverseCurve.push(new THREE.Vector3(x, graphY + 0.08 + 0.42 * (1 - smooth01(q)), 0.02));
    }
    root.add(line(expansionCurve, 0xffeb3b, 0.48));
    root.add(line(inverseCurve, 0x42a5f5, 0.48));
    const graphCursor = line([
      new THREE.Vector3(graphX0, graphY + 0.02, 0.03),
      new THREE.Vector3(graphX0, graphY + 0.56, 0.03)
    ], 0xffffff, 0.3);
    const expansionDot = makeMarker(new THREE.Vector3(graphX0, graphY + 0.08, 0.04), 0xffeb3b, 0.035);
    const inverseDot = makeMarker(new THREE.Vector3(graphX0, graphY + 0.5, 0.04), 0x42a5f5, 0.035);
    root.add(graphCursor, expansionDot, inverseDot);
    const closureChart = createStripChart(new THREE.Vector3(graphX0, graphY - 0.62, 0.04), graphW, 0.4, 0xffeb3b, 120, "q closure", 0xffeb3b);
    const boundarySamples = [];
    const boundaryTrace = createPointTrace(140, 0xffeb3b, 0.38, 0.018);
    root.add(closureChart.group, boundaryTrace.mesh);
    if (visual) {
      visual.addEventListener("instrument:zero", () => {
        clearStripChart(closureChart);
        boundarySamples.length = 0;
        updatePointTrace(boundaryTrace, boundarySamples);
      });
    }

    const phaseNeedle = line([
      new THREE.Vector3(0, 0, 0.02),
      new THREE.Vector3(boundaryRadius, 0, 0.02)
    ], 0xffeb3b, 0.45);
    root.add(phaseNeedle);

    dyn.push((t, sampled) => {
      const leadPhase = phase01(t, INSTRUMENT_CPS.medium);
      const q = smooth01(leadPhase);
      const aeonRadius = 0.12 + q * (boundaryRadius - 0.12);
      const conformalRadius = 0.12 + (1 - q) * (boundaryRadius - 0.12);
      aeonShell.scale.setScalar(aeonRadius);
      conformalShell.scale.setScalar(conformalRadius);
      aeonShell.material.opacity = 0.18 + 0.58 * (1 - 0.35 * q);
      conformalShell.material.opacity = 0.18 + 0.34 * q;
      const a = leadPhase * TAU;
      phaseNeedle.geometry.setFromPoints([
        new THREE.Vector3(0, 0, 0.02),
        new THREE.Vector3(boundaryRadius * Math.cos(a), boundaryRadius * Math.sin(a), 0.02)
      ]);
      boundaryDot.position.set(boundaryRadius * Math.cos(a), boundaryRadius * Math.sin(a), 0.03);
      originDot.material.color.setHex(q > 0.92 ? 0xffeb3b : 0xffffff);
      originDot.scale.setScalar(1 + 0.35 * q);
      if (sampled) appendTrace(boundarySamples, boundaryDot.position, 140);
      updatePointTrace(boundaryTrace, boundarySamples);
      const graphX = graphX0 + q * graphW;
      const expansionY = graphY + 0.08 + 0.42 * q;
      const inverseY = graphY + 0.08 + 0.42 * (1 - q);
      graphCursor.geometry.setFromPoints([
        new THREE.Vector3(graphX, graphY + 0.02, 0.03),
        new THREE.Vector3(graphX, graphY + 0.56, 0.03)
      ]);
      expansionDot.position.set(graphX, expansionY, 0.04);
      inverseDot.position.set(graphX, inverseY, 0.04);
      boundary.rotation.z = 0;
      boundaryGauge.rotation.z = 0;
      boundary.material.opacity = 0.22;
      const mapResidual = Math.abs(q + (1 - q) - 1);
      const closureResidual = Math.abs((aeonRadius + conformalRadius) - (boundaryRadius + 0.12));
      updateStripChart(closureChart, q, 0, 1, sampled);
      setInstrumentMetric(
        "a " + (aeonRadius / boundaryRadius).toFixed(2) + " · Ω " + (conformalRadius / boundaryRadius).toFixed(2),
        "CCC rescale analogy",
        "phase " + leadPhase.toFixed(2),
        "σ q-map " + mapResidual.toExponential(1) + " · close " + closureResidual.toExponential(1),
        {
          primary: q,
          primaryLabel: "aeon q",
          primaryText: q.toFixed(2),
          secondary: 1 - q,
          secondaryLabel: "rescale",
          secondaryText: (1 - q).toFixed(2),
          error: clamp01(Math.max(mapResidual, closureResidual) * 40),
          errorText: Math.max(mapResidual, closureResidual).toExponential(1)
        }
      );
      if (readout) readout.textContent =
        "CCC RETURN · CONFORMAL RESCALE\n" +
        "/6 ≡ /0 · route closure, not a new object\n" +
        "a=" + (aeonRadius / boundaryRadius).toFixed(2) + " · Ω=" + (conformalRadius / boundaryRadius).toFixed(2) + " · q+(1−q)=1 · σ=" + mapResidual.toExponential(1) + "\n" +
        "boundary trace sampled · end boundary → origin\n" +
        "Penrose CCC = analogy, not asserted identity";
    });
  }

  return { root, update: (t, sampled = true) => dyn.forEach((f) => f(t, sampled)) };
}

async function boot() {
  initThemeControls();
  initCommandPalette();

  if (!canvas || !visual) return;
  try {
    if (new URLSearchParams(window.location.search).has("forceWebGLFallback")) {
      throw new Error("Forced WebGL fallback");
    }

    if (animationMode === "titans") {
      drawTitanCalculator();
      return;
    }
    if (animationMode === "constitution") {
      drawConstitutionInstrument();
      return;
    }

    THREE = await import("three");
    ({ OrbitControls } = await import("three/addons/controls/OrbitControls.js"));

    const renderer = new THREE.WebGLRenderer({
      canvas,
      antialias: true,
      alpha: true,
      preserveDrawingBuffer: true
    });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.setClearColor(0x050505, 1);

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(45, 1, 0.1, 100);
    camera.position.set(0, 0.35, 4.7);

    const controls = new OrbitControls(camera, canvas);
    controls.enableDamping = true;
    controls.enablePan = false;
    controls.enableZoom = false;
    controls.autoRotate = false;
    controls.autoRotateSpeed = 0;
    if (animationMode === "burrisphere") {
      // the sphere sits sandwiched between the two tangent planes (floor = 0,
      // top = ∞) — stand near the floor and look UP toward infinity
      camera.position.set(0, -0.7, 9.6);
      controls.target.set(0, 0.7, 0);
      controls.update();
    }
    if (animationMode === "bloch") {
      // resting sphere + tangent floor at -r; landing reaches 2r·cot(θ/2)
      camera.position.set(0, 0.4, 5.8);
      controls.update();
    }
    if (animationMode === "logline") {
      // the line spans ±2.6 with the energy well above — front view, framed wide
      camera.position.set(0, 0.55, 5.9);
      controls.target.set(0, 0.45, 0);
      controls.update();
    }
    if (animationMode === "horn") {
      // keep the full torus readable beneath the compact HUD and slider
      camera.position.set(0, 0.32, 6.15);
      controls.target.set(0, 0.05, 0);
      controls.update();
    }

    const overlay = ensureInstrumentOverlay(animationMode);
    const playback = ensureInstrumentControls();
    let paused = false;
    let simTime = 0;
    let stepSeconds = 0;
    const sampleClock = createSampleClock();
    if (playback) {
      playback.hold.addEventListener("click", () => {
        paused = !paused;
        syncInstrumentControls(playback, paused);
      });
      playback.step.addEventListener("click", () => {
        paused = true;
        stepSeconds += 1 / 12;
        syncInstrumentControls(playback, paused);
      });
      playback.zero.addEventListener("click", () => {
        paused = true;
        simTime = 0;
        stepSeconds = 0;
        sampleClock.accumulator = 0;
        sampleClock.index = 0;
        visual.dispatchEvent(new CustomEvent("instrument:zero"));
        setInstrumentMetric(visual.dataset.instrumentMetric || "", "zeroed", "phase 0.00");
        syncInstrumentControls(playback, paused);
      });
      playback.rate.addEventListener("input", () => {
        setInstrumentMetric(visual.dataset.instrumentMetric || "", "rate " + (parseFloat(playback.rate.value) / 100).toFixed(2) + "x", visual.dataset.instrumentPhase || "");
      });
      syncInstrumentControls(playback, paused);
    }
    addReferenceFrame(scene);
    const { root, update } = buildScene(animationMode, scene);

    function resize() {
      const bounds = visual.getBoundingClientRect();
      renderer.setSize(bounds.width, bounds.height, false);
      camera.aspect = bounds.width / Math.max(bounds.height, 1);
      camera.updateProjectionMatrix();
    }

    let lastFrame = 0;
    let fps = 0;
    function animate(time) {
      const dt = lastFrame ? Math.max(1, time - lastFrame) : 16.7;
      fps = fps ? fps * 0.9 + (1000 / dt) * 0.1 : 1000 / dt;
      lastFrame = time;
      const rate = playback && playback.rate ? parseFloat(playback.rate.value) / 100 : 1;
      const sampleAdvance = sampleClock.advance(dt * 0.001, rate, stepSeconds, paused);
      stepSeconds = 0;
      simTime += sampleAdvance;
      visual.dataset.instrumentSample = REDUCED_MOTION ? "sample static" : sampleClock.label();
      const t = simTime;
      if (animationMode === "titans") {
        root.rotation.z = 0;
      } else if (animationMode === "muLimit") {
        root.rotation.x = 0;
      } else if (animationMode === "bloch") {
        root.scale.setScalar(1);
      } else if (animationMode === "ccc") {
        root.rotation.z = 0;
      }
      update(t, sampleAdvance > 0); // morph state every frame; advance histories only on sample ticks
      if (paused) {
        setInstrumentMetric(visual.dataset.instrumentMetric || "", "held frame", visual.dataset.instrumentPhase || "");
      }
      updateInstrumentOverlay(overlay, t, fps);

      controls.update();
      renderer.render(scene, camera);
      scheduleFrame(animate);
    }

    function renderInstrumentFrame(t, fpsValue, sampled = true) {
      update(t, sampled);
      controls.update();
      renderer.render(scene, camera);
      updateInstrumentOverlay(overlay, t, fpsValue);
    }

    resize();
    window.addEventListener("resize", resize);
    visual.dataset.instrumentSample = REDUCED_MOTION ? "sample static" : sampleClock.label();
    renderInstrumentFrame(REDUCED_MOTION ? 1.2 : 0, 0, true);

    if (REDUCED_MOTION) {
      // static render: one calibrated frame now, re-render only on interaction/resize
      controls.addEventListener("change", () => renderInstrumentFrame(1.2, 0, true));
      window.addEventListener("resize", () => {
        resize();
        renderInstrumentFrame(1.2, 0, true);
      });
      return;
    }

    scheduleFrame(animate);
  } catch (error) {
    fail(error);
  }
}

boot();
