import assert from "node:assert/strict";
import { sphereState } from "./runaway.mjs";

// Equator (theta = pi/2): perfect balance, everything = 1.
{
  const s = sphereState(Math.PI / 2);
  assert.ok(Math.abs(s.phi - 1) < 1e-9, "phi=1 at equator");
  assert.ok(Math.abs(s.nu - 1) < 1e-9, "nu=1 at equator");
  assert.ok(Math.abs(s.B - 1) < 1e-9, "B=1 at equator");
  assert.ok(Math.abs(s.gamma - 1) < 1e-9, "gamma=1 at equator");
}
// Near the north pole (theta -> 0): nu -> 0, phi -> infinity, B -> 0.
{
  const s = sphereState(0.02);
  assert.ok(s.nu < 0.02, "nu small near north pole");
  assert.ok(s.phi > 50, "phi runs up near north pole");
  assert.ok(s.B < 0.05, "B collapses near a pole");
  assert.ok(s.gamma > 25, "price gamma diverges near a pole");
}
// Near the south pole (theta -> pi): the mirror runaway (nu large, phi small).
{
  const s = sphereState(Math.PI - 0.02);
  assert.ok(s.nu > 50, "nu runs up near south pole");
  assert.ok(s.phi < 0.02, "phi small near south pole");
  assert.ok(s.B < 0.05, "B collapses near a pole");
}
console.log("sphereState: all assertions passed");
