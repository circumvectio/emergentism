import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import { chartPoint, chartMotion, phaseIndexForAzimuth, phaseBoundaryForAzimuth, intersectLineWithHorizontalPlane,
  clipRayToRadialWindow as clipChartRay } from "./burrisphere-math.js";

const canvas = document.querySelector("#burrisphere-canvas");
const polarSlider = document.querySelector("#polar-angle");
const bearingSlider = document.querySelector("#axial-rotation");
const polarOutput = document.querySelector("#polar-angle-output");
const bearingOutput = document.querySelector("#axial-rotation-output");
const motionToggle = document.querySelector("#motion-toggle");
const centreButton = document.querySelector("#centre-button");
const bearingButton = document.querySelector("#bearing-button");
const overlayToggle = document.querySelector("#overlay-toggle");
const fullscreenButton = document.querySelector("#fullscreen-button");
const cameraButton = document.querySelector("#camera-button");
const viewport = document.querySelector("#sphere-viewport");
const runtimeStatus = document.querySelector("#runtime-status");
const phaseReadout = document.querySelector("#phase-readout");
const motionStatus = document.querySelector("#motion-status");
const liveLegend = document.querySelector("#live-legend");
const legendMove = document.querySelector("#legend-move");
const legendSeam = document.querySelector("#legend-seam");
const legendDirection = document.querySelector("#legend-direction");
const legendStatus = document.querySelector("#legend-status");
const actionCells = [...document.querySelectorAll(".bi-action-plane__cell")];
const motionPreference = window.matchMedia("(prefers-reduced-motion: reduce)");
let reducedMotion = motionPreference.matches;

const readouts = {
  phi: document.querySelector("#phi-value"),
  nu: document.querySelector("#nu-value"),
  product: document.querySelector("#product-value"),
  balance: document.querySelector("#balance-value"),
  theta: document.querySelector("#theta-value"),
  azimuth: document.querySelector("#azimuth-value"),
};

const COLORS = {
  void: 0x07090f,
  bone: 0xefe8db,
  gold: 0xd7b65a,
  blue: 0x78a7e8,
  violet: 0xa58be2,
  mint: 0x76ceb0,
  poison: 0xd97557,
};

const R = 1.08;
const TAU = Math.PI * 2;
const ITINERARY_DURATION = 12000;
const PLANE_SIZE = 8.4;
const LIMIT = PLANE_SIZE * 0.46;
const ACTION_RADIUS = 2 * R;
const ACTION_CURSOR_RADIUS = 1.55 * R;
const SOUTH = new THREE.Vector3(0, -R, 0);
const NORTH = new THREE.Vector3(0, R, 0);
const phases = [
  { index: "M4 · 01", name: "Taking-A", color: COLORS.violet },
  { index: "M4 · 02", name: "Taking-B", color: COLORS.gold },
  { index: "M4 · 03", name: "Giving-A", color: COLORS.gold },
  { index: "M4 · 04", name: "Giving-B", color: COLORS.blue },
];
// Read identities and signatures from the source-generated rules, not a second
// handwritten catalogue. Opening a rule remains separate from moving the point.
phases.forEach((phase, index) => {
  const link = actionCells.find(cell => Number(cell.dataset.phase) === index).querySelector("a");
  phase.operator = link.getAttribute("href").slice(1);
  const rule = document.getElementById(phase.operator);
  phase.name = rule.querySelector("summary span").textContent;
  phase.alias = rule.querySelector("summary strong").textContent;
  phase.signature = rule.querySelector(".bi-equation__signature code").textContent;
});
const referenceNames = Object.fromEntries([
  ["south", "shiva_dissolve", "south"],
  ["equator", "vishnu_preserve", "balance"],
  ["north", "brahma_create", "north"],
].map(([key, id, place]) => [key, `${document.getElementById(id).querySelector("summary strong").textContent} · ${place}`]));

let renderer;
try {
  renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: false, powerPreference: "high-performance" });
} catch (_error) {
  document.body.dataset.webgl = "failed";
  canvas.hidden = true;
  document.querySelector("#webgl-fallback")?.removeAttribute("hidden");
}
if (renderer) {
document.body.dataset.webgl = "ready";
document.querySelector("#geometry-controls").disabled = false;
runtimeStatus.textContent = "Ready. Move θ or ψ independently; choose a rule below without changing the geometry.";
renderer.setClearColor(COLORS.void, 1);
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, window.innerWidth < 700 ? 1.25 : 1.6));

const scene = new THREE.Scene();
scene.fog = new THREE.FogExp2(COLORS.void, 0.055);
const camera = new THREE.PerspectiveCamera(38, 1, 0.1, 100);
const controls = new OrbitControls(camera, canvas);
// Direct manipulation: no residual orbit velocity to advance on resize or
// fullscreen. The explicit one-turn itinerary is the only automatic motion.
controls.enableDamping = false;
controls.enablePan = false;
controls.minDistance = 4.2;
controls.maxDistance = 12;
controls.target.set(0, 0, 0);

scene.add(new THREE.HemisphereLight(0xdce8ff, 0x151019, 1.05));
const key = new THREE.DirectionalLight(0xffe8ab, 1.35);
key.position.set(4, 6, 5);
scene.add(key);
const rim = new THREE.PointLight(COLORS.blue, 5.5, 18, 2);
rim.position.set(-4, 1.4, -3);
scene.add(rim);

const root = new THREE.Group();
scene.add(root);

function line(points, color, opacity = 1, dashed = false) {
  const geometry = new THREE.BufferGeometry().setFromPoints(points);
  const material = dashed
    ? new THREE.LineDashedMaterial({ color, transparent: true, opacity, dashSize: 0.09, gapSize: 0.06, depthWrite: false })
    : new THREE.LineBasicMaterial({ color, transparent: true, opacity, depthWrite: false });
  const object = new THREE.Line(geometry, material);
  if (dashed) object.computeLineDistances();
  return object;
}

function loopAtLatitude(theta, color, opacity) {
  const points = [];
  const y = -R * Math.cos(theta);
  const radius = R * Math.sin(theta);
  for (let i = 0; i <= 128; i += 1) {
    const a = (i / 128) * Math.PI * 2;
    points.push(new THREE.Vector3(radius * Math.cos(a), y, radius * Math.sin(a)));
  }
  return line(points, color, opacity);
}

const sphere = new THREE.Mesh(
  new THREE.SphereGeometry(R, 72, 48),
  new THREE.MeshPhysicalMaterial({
    color: 0xdfe5ef,
    transparent: true,
    opacity: 0.105,
    roughness: 0.12,
    metalness: 0.05,
    transmission: 0.18,
    side: THREE.DoubleSide,
    depthWrite: false,
  }),
);
root.add(sphere);
root.add(new THREE.Mesh(
  new THREE.SphereGeometry(R + 0.002, 32, 24),
  new THREE.MeshBasicMaterial({ color: COLORS.bone, wireframe: true, transparent: true, opacity: 0.045, depthWrite: false }),
));

for (const fraction of [1 / 6, 1 / 3, 1 / 2, 2 / 3, 5 / 6]) {
  root.add(loopAtLatitude(fraction * Math.PI, fraction === 1 / 2 ? COLORS.gold : COLORS.bone, fraction === 1 / 2 ? 0.72 : 0.095));
}
for (let meridian = 0; meridian < 8; meridian += 1) {
  const points = [];
  const a = (meridian / 8) * Math.PI;
  for (let i = 0; i <= 96; i += 1) {
    const theta = (i / 96) * Math.PI;
    points.push(new THREE.Vector3(R * Math.sin(theta) * Math.cos(a), -R * Math.cos(theta), R * Math.sin(theta) * Math.sin(a)));
  }
  root.add(line(points, COLORS.bone, 0.065));
}
root.add(line([new THREE.Vector3(0, -R * 1.42, 0), new THREE.Vector3(0, R * 1.42, 0)], COLORS.bone, 0.2));

function makePlane(y, color) {
  const group = new THREE.Group();
  const disk = new THREE.Mesh(
    new THREE.CircleGeometry(PLANE_SIZE / 2, 96),
    new THREE.MeshBasicMaterial({ color, transparent: true, opacity: 0.035, side: THREE.DoubleSide, depthWrite: false }),
  );
  disk.rotation.x = -Math.PI / 2;
  group.add(disk);
  const grid = new THREE.GridHelper(PLANE_SIZE, 20, color, color);
  grid.material.transparent = true;
  grid.material.opacity = 0.13;
  grid.material.depthWrite = false;
  group.add(grid);
  const ringPoints = [];
  for (let i = 0; i <= 128; i += 1) {
    const a = (i / 128) * Math.PI * 2;
    ringPoints.push(new THREE.Vector3(2 * R * Math.cos(a), 0.008, 2 * R * Math.sin(a)));
  }
  group.add(line(ringPoints, color, 0.68));
  group.position.y = y;
  root.add(group);
  return group;
}

makePlane(R, COLORS.blue);
makePlane(-R, COLORS.mint);

// [I] M4 is a separate four-sector reading overlay co-located with the lower
// ν chart. It is deliberately planar: no transfer territory touches the sphere.
const bottomActionPlane = new THREE.Group();
bottomActionPlane.name = "M4 bottom action plane [I]";
bottomActionPlane.position.y = -R + 0.024;
const sectorMeshes = [];

phases.forEach((phase, index) => {
  const azimuthStart = -Math.PI / 2 + index * Math.PI / 2;
  const geometry = new THREE.CircleGeometry(ACTION_RADIUS, 36, azimuthStart, Math.PI / 2);
  geometry.rotateX(Math.PI / 2);
  const material = new THREE.MeshBasicMaterial({
    color: phase.color,
    transparent: true,
    opacity: 0.035,
    side: THREE.DoubleSide,
    depthWrite: false,
    blending: THREE.AdditiveBlending,
  });
  const sector = new THREE.Mesh(geometry, material);
  sector.name = `${phase.index} · ${phase.name}`;
  sector.renderOrder = 4;
  sectorMeshes.push(sector);
  bottomActionPlane.add(sector);

  bottomActionPlane.add(line([
    new THREE.Vector3(0, 0.018, 0),
    new THREE.Vector3(
      ACTION_RADIUS * Math.cos(azimuthStart),
      0.018,
      ACTION_RADIUS * Math.sin(azimuthStart),
    ),
  ], COLORS.violet, 0.58, true));
});

const actionRing = [];
for (let i = 0; i <= 128; i += 1) {
  const angle = (i / 128) * Math.PI * 2;
  actionRing.push(new THREE.Vector3(
    ACTION_CURSOR_RADIUS * Math.cos(angle),
    0.026,
    ACTION_CURSOR_RADIUS * Math.sin(angle),
  ));
}
bottomActionPlane.add(line(actionRing, COLORS.violet, 0.52, true));
const phaseCursor = new THREE.Mesh(
  new THREE.OctahedronGeometry(0.064, 0),
  new THREE.MeshBasicMaterial({ color: COLORS.violet, depthWrite: false }),
);
phaseCursor.position.y = 0.075;
phaseCursor.renderOrder = 8;
bottomActionPlane.add(phaseCursor);
root.add(bottomActionPlane);

function pole(position, color, scale = 0.055) {
  const group = new THREE.Group();
  const core = new THREE.Mesh(new THREE.SphereGeometry(scale, 20, 20), new THREE.MeshBasicMaterial({ color }));
  const glow = new THREE.Mesh(
    new THREE.SphereGeometry(scale * 2.6, 20, 20),
    new THREE.MeshBasicMaterial({ color, transparent: true, opacity: 0.13, blending: THREE.AdditiveBlending, depthWrite: false }),
  );
  group.add(core, glow);
  group.position.copy(position);
  root.add(group);
  return group;
}

pole(NORTH, COLORS.blue);
pole(SOUTH, COLORS.mint);

function titanGlyph(glyph, color, position) {
  const textureCanvas = document.createElement("canvas");
  textureCanvas.width = 160;
  textureCanvas.height = 160;
  const context = textureCanvas.getContext("2d");
  context.clearRect(0, 0, 160, 160);
  context.fillStyle = `#${color.toString(16).padStart(6, "0")}`;
  context.font = '500 92px "Newsreader", Georgia, serif';
  context.textAlign = "center";
  context.textBaseline = "middle";
  context.fillText(glyph, 80, 82);
  const texture = new THREE.CanvasTexture(textureCanvas);
  texture.colorSpace = THREE.SRGBColorSpace;
  const sprite = new THREE.Sprite(new THREE.SpriteMaterial({
    map: texture,
    transparent: true,
    depthTest: false,
    depthWrite: false,
  }));
  sprite.scale.set(0.42, 0.42, 0.42);
  sprite.position.copy(position);
  sprite.renderOrder = 20;
  return sprite;
}

const titanGlyphs = new THREE.Group();
titanGlyphs.name = "F3 Titan axis [I]";
titanGlyphs.add(
  titanGlyph("•", COLORS.mint, SOUTH),
  titanGlyph("⊙", COLORS.gold, new THREE.Vector3(0, 0, 0)),
  titanGlyph("○", COLORS.blue, NORTH),
);
root.add(titanGlyphs);

const itinerary = new THREE.Group();
const spiralPoints = [];
for (let i = 0; i <= 240; i += 1) {
  const t = i / 240;
  const theta = t * Math.PI;
  const a = t * Math.PI * 2 - Math.PI / 2;
  spiralPoints.push(new THREE.Vector3(
    (R + 0.022) * Math.sin(theta) * Math.cos(a),
    -(R + 0.022) * Math.cos(theta),
    (R + 0.022) * Math.sin(theta) * Math.sin(a),
  ));
}
itinerary.add(line(spiralPoints, COLORS.violet, 0.78, true));
root.add(itinerary);

const point = pole(new THREE.Vector3(), COLORS.gold, 0.052);
const lowerMarker = pole(new THREE.Vector3(), COLORS.mint, 0.045);
const upperMarker = pole(new THREE.Vector3(), COLORS.blue, 0.045);
const lowerRay = line([NORTH, new THREE.Vector3()], COLORS.mint, 0.88);
const upperRay = line([SOUTH, new THREE.Vector3()], COLORS.blue, 0.88);
root.add(lowerRay, upperRay);

let showItinerary = true;
let manualTheta = THREE.MathUtils.degToRad(Number(polarSlider.value));
let manualAzimuth = THREE.MathUtils.degToRad(Number(bearingSlider.value));
let motionState = reducedMotion ? "reduced" : "idle";
let itineraryProgress = 0;
let itineraryStartedAt = 0;
let activePhase = -1;
let dirty = true;
let lastDomUpdate = 0;
let framePending = false;
let cameraInitialized = false;
let legendMode = "still";
let cameraActive = false;
let lastLegendTheta = manualTheta;
let lastLegendAzimuth = manualAzimuth;
let legendMovement = chartMotion(manualTheta, manualTheta, manualAzimuth, manualAzimuth);

function setText(element, value) {
  if (element.textContent !== value) element.textContent = value;
}

function refreshLegend() {
  const atPole = chartPoint(manualTheta, manualAzimuth).atPole;
  const phase = atPole ? null : phases[phaseIndexForAzimuth(manualAzimuth)];
  const seam = atPole ? null : phaseBoundaryForAzimuth(manualAzimuth);
  setText(legendMove, !showItinerary ? "G7 overlay hidden" : phase ? `${phase.alias} · ${phase.name}` : "No move · pole boundary");
  setText(legendSeam, showItinerary && seam ? "Sector seam · next sector shown" : "");
  legendSeam.title = seam ? `${phases[seam.previous].name} / ${phases[seam.next].name}; increasing-ψ convention` : "";
  const {direction, toward, atReference} = legendMovement;
  let text, target = "", state = legendMode;
  if (!showItinerary) {
    text = "Interpretive direction hidden";
    state = "hidden";
  } else if (cameraActive && motionState !== "playing") {
    text = "Camera only · point held";
    state = "camera";
  } else if (motionState === "paused") {
    text = "Paused · no approach";
    state = "paused";
  } else if (legendMode === "reset") {
    text = `Reset · ${atReference ? referenceNames[atReference] : "position held"}`;
  } else if ((motionState === "playing" || legendMode === "theta") && ["up", "down"].includes(direction)) {
    target = toward;
    text = atReference ? `At ${referenceNames[atReference]}` : `${direction === "up" ? "↑" : "↓"} toward ${referenceNames[toward]}`;
    state = atReference ? "at-reference" : "moving";
  } else if (legendMode === "bearing" && direction === "around") {
    text = "ψ only · no Titan approach";
    state = "around";
  } else {
    text = `Still · ${atReference ? referenceNames[atReference] : "no Titan approach"}`;
    state = "still";
  }
  setText(legendDirection, text);
  liveLegend.dataset.operator = showItinerary && phase ? phase.operator : "";
  liveLegend.dataset.seam = String(Boolean(showItinerary && seam));
  liveLegend.dataset.target = target;
  liveLegend.dataset.motion = state;
  // Only meaningful label transitions are announced, never per-frame numbers.
  setText(legendStatus, `${legendMove.textContent}. ${legendSeam.textContent} ${text}. Interpretive reference only.`);
}

function settleLegend() {
  if (motionState === "playing") return;
  legendMode = "still";
  refreshLegend();
}

function setLinePoints(object, points) {
  const position = object.geometry.attributes.position;
  points.forEach((value, index) => position.setXYZ(index, value.x, value.y, value.z));
  position.needsUpdate = true;
}

function clipRayToRadialWindow(source, exact) {
  return clipChartRay(source, exact, LIMIT);
}

function formatCoordinate(value) {
  if (!Number.isFinite(value)) return "∞";
  if (value === 0) return "0.000";
  if (value >= 100) return value.toExponential(2);
  if (value < 0.01) return value.toExponential(2);
  return value.toFixed(3);
}

function updatePhase(azimuth, atPole) {
  const index = atPole ? -1 : phaseIndexForAzimuth(azimuth);
  if (index === activePhase) return;
  activePhase = index;
  if (atPole) {
    phaseReadout.querySelector(".bi-phase__index").textContent = "M4 · bearing degenerates at pole [I]";
    phaseReadout.querySelector("strong").textContent = "Axis boundary";
    document.querySelector("#phase-signature").textContent = "No transfer signature at the pole.";
    phaseReadout.querySelector(".bi-action-plane__current").style.borderColor = `#${COLORS.violet.toString(16).padStart(6, "0")}`;
    actionCells.forEach((cell) => {
      cell.classList.remove("is-active");
      cell.removeAttribute("aria-current");
    });
    sectorMeshes.forEach((sector) => { sector.material.opacity = 0.035; });
    return;
  }
  const phase = phases[index];
  phaseReadout.querySelector(".bi-phase__index").textContent = `${phase.index} · bottom action plane [I]`;
  phaseReadout.querySelector("strong").textContent = `${phase.name} · ${phase.alias}`;
  document.querySelector("#phase-signature").textContent = phase.signature;
  phaseReadout.querySelector(".bi-action-plane__current").style.borderColor = `#${phase.color.toString(16).padStart(6, "0")}`;
  actionCells.forEach((cell) => {
    const isActive = Number(cell.dataset.phase) === index;
    cell.classList.toggle("is-active", isActive);
    if (isActive) cell.setAttribute("aria-current", "true");
    else cell.removeAttribute("aria-current");
  });
  sectorMeshes.forEach((sector, sectorIndex) => {
    sector.material.opacity = sectorIndex === index ? 0.16 : 0.035;
  });
}

function updateSliderAccessibleText(atPole) {
  const chartState = atPole
    ? `${readouts.theta.textContent}; open-chart boundary; phi nu product has limiting value 1`
    : `${readouts.theta.textContent}; phi ${readouts.phi.textContent}; nu ${readouts.nu.textContent}; B ${readouts.balance.textContent}`;
  polarSlider.setAttribute("aria-valuetext", chartState);
  bearingSlider.setAttribute(
    "aria-valuetext",
    atPole
      ? `${bearingOutput.textContent}; bearing is degenerate at the pole`
      : `${bearingOutput.textContent}; selected M4 reading ${phaseReadout.querySelector("strong").textContent}`,
  );
}

function updateGeometry(theta, azimuth, updateDom = true) {
  const {atPole, nu, phi, balance, point: shared} = chartPoint(theta, azimuth, R);

  const lowerExact = intersectLineWithHorizontalPlane(NORTH, shared, -R);
  const upperExact = intersectLineWithHorizontalPlane(SOUTH, shared, R);
  const lower = lowerExact ? clipRayToRadialWindow(NORTH, lowerExact) : null;
  const upper = upperExact ? clipRayToRadialWindow(SOUTH, upperExact) : null;

  phaseCursor.position.x = ACTION_CURSOR_RADIUS * Math.cos(azimuth);
  phaseCursor.position.z = ACTION_CURSOR_RADIUS * Math.sin(azimuth);
  phaseCursor.visible = !atPole;

  point.position.copy(shared);
  lowerRay.visible = Boolean(lower);
  upperRay.visible = Boolean(upper);
  lowerMarker.visible = Boolean(lower && !lower.clipped);
  upperMarker.visible = Boolean(upper && !upper.clipped);
  if (lower) {
    lowerMarker.position.copy(lowerExact);
    setLinePoints(lowerRay, [NORTH, lower.vector]);
  }
  if (upper) {
    upperMarker.position.copy(upperExact);
    setLinePoints(upperRay, [SOUTH, upper.vector]);
  }

  if (updateDom) {
    readouts.phi.textContent = formatCoordinate(phi);
    readouts.nu.textContent = formatCoordinate(nu);
    readouts.product.textContent = atPole ? "limit 1" : (phi * nu).toFixed(3);
    readouts.balance.textContent = balance.toFixed(3);
    readouts.theta.textContent = `${THREE.MathUtils.radToDeg(theta).toFixed(1)}°`;
    readouts.azimuth.textContent = atPole ? "— at pole" : `${THREE.MathUtils.radToDeg(azimuth).toFixed(1)}°`;
    polarOutput.textContent = readouts.theta.textContent;
    bearingOutput.textContent = `${THREE.MathUtils.radToDeg(azimuth).toFixed(1)}°`;
    updatePhase(azimuth, atPole);
    legendMovement = chartMotion(theta, lastLegendTheta, azimuth, lastLegendAzimuth);
    lastLegendTheta = theta;
    lastLegendAzimuth = azimuth;
    refreshLegend();
    updateSliderAccessibleText(atPole);
    canvas.dataset.thetaDegrees = THREE.MathUtils.radToDeg(theta).toFixed(3);
    canvas.dataset.azimuthDegrees = THREE.MathUtils.radToDeg(azimuth).toFixed(3);
    canvas.dataset.lowerRay = lower ? (lower.clipped ? "straight-clipped" : "straight-plane") : "undefined-at-pole";
    canvas.dataset.upperRay = upper ? (upper.clipped ? "straight-clipped" : "straight-plane") : "undefined-at-pole";
  }
  dirty = true;
  queueFrame();
}

function frameCamera(reset = false) {
  const width = viewport.clientWidth;
  const height = viewport.clientHeight;
  renderer.setSize(width, height, false);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, width < 700 ? 1.25 : 1.6));
  camera.aspect = width / height;
  camera.fov = width < 700 ? 44 : 38;
  if (reset || !cameraInitialized) {
    camera.position.set(4.65, 3.25, 7.6);
    controls.target.set(0, 0, 0);
    cameraInitialized = true;
  }
  camera.updateProjectionMatrix();
  controls.update();
  dirty = true;
  queueFrame();
}

function updateMotionButton() {
  dirty = true;
  queueFrame();
  const playing = motionState === "playing";
  if (!playing) legendMode = "still";
  refreshLegend();
  motionToggle.setAttribute("aria-pressed", String(playing));
  if (motionState === "reduced") {
    motionToggle.disabled = true;
    motionToggle.setAttribute("aria-disabled", "true");
    motionToggle.setAttribute("aria-label", "One-turn itinerary disabled by reduced-motion preference");
    motionToggle.querySelector(".bi-action-icon").textContent = "—";
    motionToggle.querySelector("span:last-child").textContent = "Motion off";
    motionStatus.textContent = "Reduced-motion preference active. Use the two coordinate sliders directly.";
    return;
  }
  motionToggle.disabled = false;
  motionToggle.removeAttribute("aria-disabled");
  if (playing) {
    motionToggle.setAttribute("aria-label", "Pause the selected one-turn itinerary");
    motionToggle.querySelector(".bi-action-icon").textContent = "Ⅱ";
    motionToggle.querySelector("span:last-child").textContent = "Pause turn";
    motionStatus.textContent = "Selected one-turn interpretive itinerary playing.";
  } else if (motionState === "paused") {
    motionToggle.setAttribute("aria-label", "Resume the selected one-turn itinerary");
    motionToggle.querySelector(".bi-action-icon").textContent = "▶";
    motionToggle.querySelector("span:last-child").textContent = "Resume turn";
    motionStatus.textContent = "Selected one-turn interpretive itinerary paused.";
  } else {
    motionToggle.setAttribute("aria-label", motionState === "complete" ? "Replay the selected one-turn itinerary" : "Play the selected one-turn itinerary");
    motionToggle.querySelector(".bi-action-icon").textContent = "▶";
    motionToggle.querySelector("span:last-child").textContent = motionState === "complete" ? "Replay turn" : "Play 1 turn";
    motionStatus.textContent = motionState === "complete" ? "Selected one-turn interpretive itinerary complete." : "Free coordinate inspection.";
  }
}

function enterFreeMode() {
  motionState = reducedMotion ? "reduced" : "idle";
  itineraryProgress = 0;
  updateMotionButton();
}

polarSlider.addEventListener("input", () => {
  enterFreeMode();
  legendMode = "theta";
  manualTheta = THREE.MathUtils.degToRad(Number(polarSlider.value));
  updateGeometry(manualTheta, manualAzimuth, true);
});

bearingSlider.addEventListener("input", () => {
  enterFreeMode();
  legendMode = "bearing";
  manualAzimuth = THREE.MathUtils.degToRad(Number(bearingSlider.value));
  updateGeometry(manualTheta, manualAzimuth, true);
});

for (const slider of [polarSlider, bearingSlider]) {
  for (const event of ["change", "blur", "pointercancel"]) slider.addEventListener(event, settleLegend);
}

motionToggle.addEventListener("click", () => {
  if (motionState === "reduced") return;
  if (motionState === "playing") {
    motionState = "paused";
    // Flush the last displayed sample before freezing; labels and point agree.
    updateGeometry(manualTheta, manualAzimuth, true);
  } else {
    if (motionState !== "paused") {
      itineraryProgress = 0;
      manualTheta = 0;
      manualAzimuth = -Math.PI / 2;
      polarSlider.value = "0";
      bearingSlider.value = "-90";
      legendMode = "reset";
      updateGeometry(manualTheta, manualAzimuth, true);
    }
    itineraryStartedAt = performance.now() - itineraryProgress * ITINERARY_DURATION;
    motionState = "playing";
    legendMode = "itinerary";
  }
  updateMotionButton();
});

centreButton.addEventListener("click", () => {
  enterFreeMode();
  legendMode = "reset";
  manualTheta = Math.PI / 2;
  polarSlider.value = "90";
  updateGeometry(manualTheta, manualAzimuth, true);
});

bearingButton.addEventListener("click", () => {
  enterFreeMode();
  legendMode = "reset";
  manualAzimuth = Math.PI / 2;
  bearingSlider.value = "90";
  updateGeometry(manualTheta, manualAzimuth, true);
});

overlayToggle.addEventListener("click", () => {
  showItinerary = !showItinerary;
  itinerary.visible = showItinerary;
  bottomActionPlane.visible = showItinerary;
  titanGlyphs.visible = showItinerary;
  phaseReadout.hidden = !showItinerary;
  refreshLegend();
  overlayToggle.setAttribute("aria-pressed", String(showItinerary));
  overlayToggle.setAttribute("aria-label", showItinerary ? "Hide the interpretive G7 action plane and path" : "Show the interpretive G7 action plane and path");
  overlayToggle.querySelector("span:last-child").textContent = showItinerary ? "Hide G7 overlay" : "Show G7 overlay";
  dirty = true;
  queueFrame();
});

cameraButton.addEventListener("click", () => {
  frameCamera(true);
  if (motionState !== "playing") {
    settleLegend();
    runtimeStatus.textContent = "Camera reset only. The selected move and chart coordinates are unchanged.";
  }
});

fullscreenButton.addEventListener("click", async () => {
  try {
    if (!document.fullscreenElement) await document.documentElement.requestFullscreen();
    else await document.exitFullscreen();
  } catch (_) {
    runtimeStatus.textContent = "Full screen was unavailable or declined. The same instrument and all rules remain available in this window.";
  }
});

document.addEventListener("fullscreenchange", () => {
  fullscreenButton.setAttribute("aria-label", document.fullscreenElement ? "Exit full screen" : "Enter full screen");
  fullscreenButton.querySelector("span:last-child").textContent = document.fullscreenElement ? "Exit full screen" : "Full screen";
  fullscreenButton.focus({preventScroll:true});
});

canvas.addEventListener("webglcontextlost", (event) => {
  event.preventDefault();
  motionState = reducedMotion ? "reduced" : "idle";
  updateMotionButton();
  document.body.dataset.webgl = "lost";
  document.querySelector("#geometry-controls").disabled = true;
  runtimeStatus.textContent = "Graphics context lost. Read the seven rules below; reload to retry graphics.";
  canvas.hidden = true;
  document.querySelector("#webgl-fallback")?.removeAttribute("hidden");
});

new ResizeObserver(() => frameCamera()).observe(viewport);
controls.addEventListener("start", () => { cameraActive = true; refreshLegend(); });
controls.addEventListener("end", () => { cameraActive = false; refreshLegend(); });
controls.addEventListener("change", () => { dirty = true; queueFrame(); });
document.addEventListener("visibilitychange", () => {
  if (document.hidden && motionState === "playing") {
    motionState = "paused";
    updateMotionButton();
  }
  if (!document.hidden) { dirty = true; queueFrame(); }
});
motionPreference.addEventListener("change", event => {
  reducedMotion = event.matches;
  enterFreeMode();
});
frameCamera();
updateMotionButton();
updateGeometry(manualTheta, manualAzimuth);

function animate(now) {
  framePending = false;
  if (document.hidden || document.body.dataset.webgl === "lost") return;
  if (document.visibilityState === "visible" && motionState === "playing") {
    itineraryProgress = THREE.MathUtils.clamp((now - itineraryStartedAt) / ITINERARY_DURATION, 0, 1);
    manualTheta = Math.PI * itineraryProgress;
    manualAzimuth = -Math.PI / 2 + TAU * itineraryProgress;
    polarSlider.value = String(THREE.MathUtils.radToDeg(manualTheta));
    bearingSlider.value = String(THREE.MathUtils.radToDeg(manualAzimuth));
    const updateDom = now - lastDomUpdate >= 80 || itineraryProgress >= 1;
    updateGeometry(manualTheta, manualAzimuth, updateDom);
    if (updateDom) lastDomUpdate = now;
    if (itineraryProgress >= 1) {
      motionState = "complete";
      updateMotionButton();
    }
  }
  if (document.visibilityState === "visible" && (motionState === "playing" || dirty)) {
    dirty = false;
    const moving = controls.update();
    renderer.render(scene, camera);
    // Read-only QA observations, not scientific or outcome evidence.
    canvas.dataset.camera = camera.position.toArray().map(x => x.toFixed(5)).join(",");
    canvas.dataset.renderCount = String(Number(canvas.dataset.renderCount || 0) + 1);
    dirty = dirty || moving;
  }
  if (motionState === "playing" || dirty) queueFrame();
}
function queueFrame() {
  if (!framePending && !document.hidden && document.body.dataset.webgl !== "lost") {
    framePending = true;
    requestAnimationFrame(animate);
  }
}
queueFrame();
}
