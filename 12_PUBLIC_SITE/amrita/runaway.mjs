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

// --- Burrisphere-runaway scene -------------------------------------------
// Note: THREE is loaded via dynamic import *inside* mountRunaway (not a
// top-level static import) so that runaway.test.mjs, which only imports
// sphereState above, can load cleanly under Node without resolving the
// browser-only vendor module path.

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

export async function mountRunaway({ canvas, readouts, fallbackEl }) {
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

  const THREE = await import("../vendor/three-0.160.0/three.module.js");

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
