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
