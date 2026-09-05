import test from 'node:test';
import assert from 'node:assert/strict';
import {chartPoint, intersectLineWithHorizontalPlane, clipRayToRadialWindow,
  phaseIndexForAzimuth, phaseBoundaryForAzimuth, chartMotion} from './assets/js/burrisphere-math.js';

const near = (a, b, eps = 1e-9) => assert.ok(Math.abs(a-b) <= eps, `${a} != ${b}`);
const sub = (a, b) => [a.x-b.x, a.y-b.y, a.z-b.z];
const norm = a => Math.hypot(...a);
const cross = (a,b) => [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]];

test('actual runtime geometry: 7200 points on S², reciprocal radii, straight rays', () => {
  const R = 1.08;
  for (let i=1; i<181; i++) {
    const theta = i * Math.PI / 181;
    for (let j=0; j<40; j++) {
      const state = chartPoint(theta, j * 2 * Math.PI / 40, R);
      near(norm(Object.values(state.point)), R);
      near(state.product, 1);
      near(2/(state.phi+state.nu), state.balance);
      for (const [source, planeY, radial] of [
        [{x:0,y:R,z:0}, -R, state.nu], [{x:0,y:-R,z:0}, R, state.phi],
      ]) {
        const exact = intersectLineWithHorizontalPlane(source, state.point, planeY);
        near(exact.y, planeY);
        near(Math.hypot(exact.x, exact.z)/(2*R), radial, 1e-7);
        const visible = clipRayToRadialWindow(source, exact, 3.864);
        const a = sub(state.point, source), b = sub(visible.vector, source);
        near(norm(cross(a,b))/(norm(a)*norm(b)), 0);
        assert.ok(Math.hypot(visible.vector.x, visible.vector.z) <= 3.864 + 1e-10);
        if (visible.clipped) assert.notEqual(visible.vector.y, planeY);
      }
    }
  }
});
test('poles are excluded from product arithmetic; only one projection survives', () => {
  for (const theta of [0, Math.PI]) {
    const s = chartPoint(theta, 0);
    assert.equal(s.product, null);
    assert.equal(s.balance, 0);
    assert.equal(s.atPole, true);
    const pole = {x:0,y:theta===0 ? -1 : 1,z:0};
    assert.equal(intersectLineWithHorizontalPlane(pole, s.point, -pole.y), null);
  }
});
test('bearing is independent, wraps, and does not select a polar sector', () => {
  for (const angle of [-45,45,135,225]) {
    const psi = angle * Math.PI/180;
    assert.equal(phaseIndexForAzimuth(psi), phaseIndexForAzimuth(psi+2*Math.PI));
    near(chartPoint(0.7, psi).balance, chartPoint(0.7, psi+1).balance);
  }
  assert.equal(phaseIndexForAzimuth(-Math.PI/2), 0);
  assert.equal(phaseIndexForAzimuth(0), 1);
  assert.equal(phaseIndexForAzimuth(Math.PI/2), 2);
  assert.equal(phaseIndexForAzimuth(Math.PI), 3);
});
test('balance has meridian maximum 1; the product does not have a unique maximum', () => {
  near(chartPoint(Math.PI/2, 0).balance, 1);
  for (const theta of [0.1, 0.5, 2.5, 3.0]) {
    assert.ok(chartPoint(theta,0).balance < 1);
    near(chartPoint(theta,0).product, 1);
  }
});
test('invalid numeric inputs and non-axis clipping origins fail closed', () => {
  for (const theta of [-1, 4, NaN, Infinity]) assert.throws(()=>chartPoint(theta,0), RangeError);
  assert.throws(()=>chartPoint(1, NaN), RangeError);
  assert.throws(()=>chartPoint(1, 0, 0), RangeError);
  assert.throws(()=>clipRayToRadialWindow({x:1,y:0,z:0},{x:2,y:1,z:0},2), RangeError);
});

test('direction depends on a coordinate change, not position or presumed dynamics', () => {
  const rad = x => x * Math.PI / 180;
  for (const [before, after, direction, toward] of [
    [20,30,'up','equator'], [100,110,'up','north'],
    [160,150,'down','equator'], [80,70,'down','south'],
    [70,110,'up','north'], [110,70,'down','south'],
  ]) {
    assert.deepEqual(chartMotion(rad(after),rad(before),0,0),{direction,toward,atReference:null});
  }
  for (const theta of [0,.5,Math.PI/2,2,Math.PI]) {
    assert.equal(chartMotion(theta,theta,0,0).direction,'still');
    assert.equal(chartMotion(theta,theta,0,0).toward,null);
  }
  assert.equal(chartMotion(1,1,.2,0).direction,'around');
  assert.equal(chartMotion(0,0,.2,0).direction,'still');
  assert.equal(chartMotion(Math.PI,Math.PI,.2,0).direction,'still');
  assert.equal(chartMotion(1,1,2*Math.PI,0).direction,'still');
  assert.throws(()=>chartMotion(1,NaN,0,0),RangeError);
});

test('arrival references do not imply crossings or numerical Titan operations', () => {
  for (const [before,after,atReference] of [[.1,0,'south'],[1,Math.PI/2,'equator'],[3,Math.PI,'north']]) {
    assert.equal(chartMotion(after,before,0,0).atReference,atReference);
  }
  assert.equal(chartMotion(2,1,0,0).atReference,null,'jump must not claim observed equator arrival');
});

test('all quadrant seams, wraparound and neighbouring interiors are explicit', () => {
  for (let turn=-2; turn<=2; turn++) for (let next=0; next<4; next++) {
    const psi=-Math.PI/2+next*Math.PI/2+turn*2*Math.PI;
    assert.deepEqual(phaseBoundaryForAzimuth(psi),{previous:(next+3)%4,next});
    assert.equal(phaseIndexForAzimuth(psi),next);
    assert.equal(phaseIndexForAzimuth(psi-1e-7),(next+3)%4);
    assert.equal(phaseIndexForAzimuth(psi+1e-7),next);
    assert.equal(phaseBoundaryForAzimuth(psi-1e-7),null);
    assert.equal(phaseBoundaryForAzimuth(psi+1e-7),null);
  }
  assert.throws(()=>phaseBoundaryForAzimuth(NaN),RangeError);
});
