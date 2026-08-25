import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";

const canvas = document.querySelector("#burrisphere-canvas");
const slider = document.querySelector("#chart-position");
const motionToggle = document.querySelector("#motion-toggle");
const centreButton = document.querySelector("#centre-button");
const overlayToggle = document.querySelector("#overlay-toggle");
const fullscreenButton = document.querySelector("#fullscreen-button");
const phaseReadout = document.querySelector("#phase-readout");
const actionCells = [...document.querySelectorAll(".bi-action-plane__cell")];
const reducedMotion = window.matchMedia?.("(prefers-reduced-motion: reduce)").matches ?? false;

const readouts = {
  phi: document.querySelector("#phi-value"),
  nu: document.querySelector("#nu-value"),
  product: document.querySelector("#product-value"),
  balance: document.querySelector("#balance-value"),
  theta: document.querySelector("#theta-value"),
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

let renderer;
try {
  renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: false, powerPreference: "high-performance" });
} catch (_error) {
  document.body.dataset.webgl = "failed";
  canvas.hidden = true;
  document.querySelector("#webgl-fallback")?.removeAttribute("hidden");
}
if (renderer) {
renderer.setClearColor(COLORS.void, 1);
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, window.innerWidth < 700 ? 1.25 : 1.6));

const scene = new THREE.Scene();
scene.fog = new THREE.FogExp2(COLORS.void, 0.055);
const camera = new THREE.PerspectiveCamera(38, 1, 0.1, 100);
const controls = new OrbitControls(camera, canvas);
controls.enableDamping = true;
controls.dampingFactor = 0.055;
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
const lowerRay = line([NORTH, new THREE.Vector3(), new THREE.Vector3()], COLORS.mint, 0.88);
const upperRay = line([SOUTH, new THREE.Vector3(), new THREE.Vector3()], COLORS.blue, 0.88);
root.add(lowerRay, upperRay);

let autoMotion = !reducedMotion;
let showItinerary = true;
let manualS = Number(slider.value) / 100;
let start = performance.now();
let activePhase = -1;
let dirty = true;
let lastDomUpdate = 0;

function setLinePoints(object, points) {
  const position = object.geometry.attributes.position;
  points.forEach((value, index) => position.setXYZ(index, value.x, value.y, value.z));
  position.needsUpdate = true;
}

function clipRadial(vector) {
  const radial = Math.hypot(vector.x, vector.z);
  if (radial <= LIMIT) return { vector, clipped: false };
  const scale = LIMIT / radial;
  return { vector: new THREE.Vector3(vector.x * scale, vector.y, vector.z * scale), clipped: true };
}

function formatCoordinate(value) {
  if (value >= 100) return value.toExponential(2);
  if (value < 0.01) return value.toExponential(2);
  return value.toFixed(3);
}

function updatePhase(theta) {
  const normalized = THREE.MathUtils.clamp(theta / Math.PI, 0, 0.999999);
  const index = Math.min(3, Math.floor(normalized * 4));
  if (index === activePhase) return;
  activePhase = index;
  const phase = phases[index];
  phaseReadout.querySelector(".bi-phase__index").textContent = `${phase.index} · bottom action plane [I]`;
  phaseReadout.querySelector("strong").textContent = phase.name;
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

function updateSliderAccessibleText() {
  slider.setAttribute("aria-valuetext", `${readouts.theta.textContent}; ${phaseReadout.querySelector("strong").textContent}`);
}

function updateGeometry(s, updateDom = true) {
  const nu = Math.exp(s);
  const phi = Math.exp(-s);
  const theta = 2 * Math.atan(nu);
  const balance = Math.sin(theta);
  const azimuth = 2 * theta - Math.PI / 2;
  const shared = new THREE.Vector3(
    R * Math.sin(theta) * Math.cos(azimuth),
    -R * Math.cos(theta),
    R * Math.sin(theta) * Math.sin(azimuth),
  );

  const lowerExact = new THREE.Vector3(2 * R * nu * Math.cos(azimuth), -R, 2 * R * nu * Math.sin(azimuth));
  const upperExact = new THREE.Vector3(2 * R * phi * Math.cos(azimuth), R, 2 * R * phi * Math.sin(azimuth));
  const lower = clipRadial(lowerExact);
  const upper = clipRadial(upperExact);

  phaseCursor.position.x = ACTION_CURSOR_RADIUS * Math.cos(azimuth);
  phaseCursor.position.z = ACTION_CURSOR_RADIUS * Math.sin(azimuth);

  point.position.copy(shared);
  lowerMarker.position.copy(lower.vector);
  upperMarker.position.copy(upper.vector);
  lowerMarker.visible = !lower.clipped;
  upperMarker.visible = !upper.clipped;
  setLinePoints(lowerRay, [NORTH, shared, lower.vector]);
  setLinePoints(upperRay, [SOUTH, shared, upper.vector]);

  if (updateDom) {
    readouts.phi.textContent = formatCoordinate(phi);
    readouts.nu.textContent = formatCoordinate(nu);
    readouts.product.textContent = (phi * nu).toFixed(3);
    readouts.balance.textContent = balance.toFixed(3);
    readouts.theta.textContent = `${THREE.MathUtils.radToDeg(theta).toFixed(1)}°`;
    updatePhase(theta);
    updateSliderAccessibleText();
  }
  dirty = true;
}

function frameCamera() {
  const width = window.innerWidth;
  const height = window.innerHeight;
  renderer.setSize(width, height, false);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, width < 700 ? 1.25 : 1.6));
  camera.aspect = width / height;
  camera.fov = width < 700 ? 44 : 38;
  camera.position.set(width < 700 ? 3.2 : 4.65, width < 700 ? 2.75 : 3.25, width < 700 ? 6.9 : 7.6);
  camera.updateProjectionMatrix();
  controls.update();
  dirty = true;
}

function updateMotionButton() {
  motionToggle.setAttribute("aria-pressed", String(autoMotion));
  motionToggle.setAttribute("aria-label", autoMotion ? "Pause automatic scan" : "Resume automatic scan");
  motionToggle.querySelector(".bi-action-icon").textContent = autoMotion ? "Ⅱ" : "▶";
  motionToggle.querySelector("span:last-child").textContent = autoMotion ? "Pause scan" : "Resume scan";
}

slider.addEventListener("input", () => {
  autoMotion = false;
  manualS = Number(slider.value) / 100;
  updateMotionButton();
  updateGeometry(manualS, true);
});

motionToggle.addEventListener("click", () => {
  autoMotion = !autoMotion;
  if (autoMotion) start = performance.now() - Math.asin(THREE.MathUtils.clamp(manualS / 2.55, -1, 1)) / 0.00022;
  updateMotionButton();
});

centreButton.addEventListener("click", () => {
  autoMotion = false;
  manualS = 0;
  slider.value = "0";
  updateMotionButton();
  updateGeometry(0, true);
});

overlayToggle.addEventListener("click", () => {
  showItinerary = !showItinerary;
  itinerary.visible = showItinerary;
  bottomActionPlane.visible = showItinerary;
  titanGlyphs.visible = showItinerary;
  phaseReadout.hidden = !showItinerary;
  overlayToggle.setAttribute("aria-pressed", String(showItinerary));
  overlayToggle.setAttribute("aria-label", showItinerary ? "Hide the interpretive G7 action plane and path" : "Show the interpretive G7 action plane and path");
  overlayToggle.querySelector("span:last-child").textContent = showItinerary ? "Hide G7 overlay" : "Show G7 overlay";
  dirty = true;
});

fullscreenButton.addEventListener("click", async () => {
  try {
    if (!document.fullscreenElement) await document.documentElement.requestFullscreen();
    else await document.exitFullscreen();
  } catch (_) {
    fullscreenButton.querySelector("span:last-child").textContent = "Unavailable";
  }
});

document.addEventListener("fullscreenchange", () => {
  fullscreenButton.setAttribute("aria-label", document.fullscreenElement ? "Exit full screen" : "Enter full screen");
  fullscreenButton.querySelector("span:last-child").textContent = document.fullscreenElement ? "Exit full screen" : "Full screen";
});

canvas.addEventListener("webglcontextlost", (event) => {
  event.preventDefault();
  autoMotion = false;
  updateMotionButton();
  document.body.dataset.webgl = "lost";
  canvas.hidden = true;
  document.querySelector("#webgl-fallback")?.removeAttribute("hidden");
});

window.addEventListener("resize", frameCamera, { passive: true });
controls.addEventListener("change", () => { dirty = true; });
frameCamera();
updateMotionButton();
updateGeometry(manualS);

function animate(now) {
  if (document.visibilityState === "visible" && autoMotion) {
    manualS = 2.55 * Math.sin((now - start) * 0.00022);
    slider.value = String(Math.round(manualS * 100));
    const updateDom = now - lastDomUpdate >= 100;
    updateGeometry(manualS, updateDom);
    if (updateDom) lastDomUpdate = now;
  }
  if (document.visibilityState === "visible" && (autoMotion || dirty)) {
    controls.update();
    renderer.render(scene, camera);
    dirty = false;
  }
  requestAnimationFrame(animate);
}
requestAnimationFrame(animate);
}
