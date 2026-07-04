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
// The load-bearing identities the [A] result IS — swept across the open domain.
// These, not the limit cases above, are the thing the amrita front door proves.
for (let i = 1; i < 40; i++) {
  const theta = (i / 40) * Math.PI;                       // in (0, pi)
  const s = sphereState(theta);
  assert.ok(Math.abs(s.phi * s.nu - 1) < 1e-9, `phi*nu=1 at theta=${theta}`);
  assert.ok(Math.abs(s.B - 2 / (s.phi + s.nu)) < 1e-9, `B=2/(phi+nu) at theta=${theta}`);
  assert.ok(Math.abs(s.gamma * s.B - 1) < 1e-9, `gamma*B=1 at theta=${theta}`);
  assert.ok(s.B <= 1 + 1e-12, `B<=1 (equator is the max) at theta=${theta}`);
}

console.log("sphereState: all assertions passed");
