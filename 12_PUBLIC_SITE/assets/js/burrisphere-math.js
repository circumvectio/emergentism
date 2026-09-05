// Numeric chart geometry only. No G7, GEN7, ethical or capability inference.
export const POLE_EPSILON = 1e-9;
const SEAM_EPSILON = 1e-10; // quarter-turn units, independent of label rounding
const TAU = 2 * Math.PI;

export function chartPoint(theta, azimuth, radius = 1) {
  if (!Number.isFinite(theta) || theta < 0 || theta > Math.PI ||
      !Number.isFinite(azimuth) || !Number.isFinite(radius) || radius <= 0) {
    throw new RangeError("Finite angles, theta in [0, pi], and positive radius required");
  }
  const atSouth = theta <= POLE_EPSILON;
  const atNorth = Math.PI - theta <= POLE_EPSILON;
  const atPole = atSouth || atNorth;
  const nu = atNorth ? Infinity : atSouth ? 0 : Math.tan(theta / 2);
  const phi = atSouth ? Infinity : atNorth ? 0 : 1 / nu;
  return {
    atPole, atSouth, atNorth, phi, nu,
    product: atPole ? null : phi * nu,
    balance: atPole ? 0 : Math.sin(theta),
    point: {
      x: atPole ? 0 : radius * Math.sin(theta) * Math.cos(azimuth),
      y: atSouth ? -radius : atNorth ? radius : -radius * Math.cos(theta),
      z: atPole ? 0 : radius * Math.sin(theta) * Math.sin(azimuth),
    },
  };
}

export function intersectLineWithHorizontalPlane(source, through, planeY) {
  const dy = through.y - source.y;
  if (dy === 0) return null; // parallel or undefined pole ray, not a finite endpoint
  const t = (planeY - source.y) / dy;
  return {
    x: source.x + t * (through.x - source.x),
    y: planeY,
    z: source.z + t * (through.z - source.z),
  };
}

export function clipRayToRadialWindow(source, exact, limit) {
  // This viewport is a cylinder around the pole axis. Both ray sources are on it.
  if (source.x !== 0 || source.z !== 0 || !Number.isFinite(limit) || limit <= 0) {
    throw new RangeError("Axis-origin ray and positive finite window required");
  }
  const radial = Math.hypot(exact.x, exact.z);
  if (radial <= limit) return { vector: exact, clipped: false };
  const scale = limit / radial;
  return {
    vector: {
      x: source.x + (exact.x - source.x) * scale,
      y: source.y + (exact.y - source.y) * scale,
      z: source.z + (exact.z - source.z) * scale,
    },
    clipped: true,
  };
}

export function phaseIndexForAzimuth(azimuth) {
  if (!Number.isFinite(azimuth)) throw new RangeError("Finite bearing required");
  const seam = phaseBoundaryForAzimuth(azimuth);
  if (seam) return seam.next;
  const normalized = ((azimuth + Math.PI / 2) % TAU + TAU) % TAU;
  return Math.min(3, Math.floor(normalized / (Math.PI / 2)));
}

// Display convention only: sectors include their starting bearing. At a seam,
// retain the selected sector but expose its neighbour instead of hiding the cut.
export function phaseBoundaryForAzimuth(azimuth) {
  if (!Number.isFinite(azimuth)) throw new RangeError("Finite bearing required");
  const quarter = (azimuth + Math.PI / 2) / (Math.PI / 2);
  if (Math.abs(quarter - Math.round(quarter)) > SEAM_EPSILON) return null;
  const next = ((Math.round(quarter) % 4) + 4) % 4;
  return { previous: (next + 3) % 4, next };
}

// Change of chart coordinates, not a force, strategy, intention or camera orbit.
export function chartMotion(theta, previousTheta, azimuth, previousAzimuth) {
  const point = chartPoint(theta, azimuth);
  chartPoint(previousTheta, previousAzimuth); // same finite-domain contract
  const atReference = point.atSouth ? "south" : point.atNorth ? "north"
    : Math.abs(theta - Math.PI / 2) <= POLE_EPSILON ? "equator" : null;
  const delta = theta - previousTheta;
  if (Math.abs(delta) > POLE_EPSILON) {
    return {
      direction: delta > 0 ? "up" : "down", atReference,
      toward: atReference || (delta > 0
        ? theta < Math.PI / 2 ? "equator" : "north"
        : theta > Math.PI / 2 ? "equator" : "south"),
    };
  }
  // A full bearing turn returns to the same point; it is not an observed step.
  const bearingStep = Math.atan2(Math.sin(azimuth - previousAzimuth), Math.cos(azimuth - previousAzimuth));
  return {direction: !point.atPole && Math.abs(bearingStep) > POLE_EPSILON ? "around" : "still", atReference, toward: null};
}
