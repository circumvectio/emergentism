import test from 'node:test';
import assert from 'node:assert/strict';
import { baseline, verifyFreeze, here } from './trial.mjs';
import fs from 'node:fs';
import path from 'node:path';
const source = (p, text) => ({ path: p, content: text, sha256: 'fixture-only' });
const snap = sources => ({ revision: 'fixture', sources });
test('search is literal OR, case insensitive, not regex', () => {
  const result = baseline(snap([source('x.md', 'ALPHA\nbeta\na.b\naxb')]), ['alpha', 'a.b']);
  assert.equal(result.length, 1); assert.equal(result[0].startLine, 1);
  assert.equal(result[0].endLine, 4);
  assert.deepEqual(baseline(snap([source('x.md', 'axb')]), ['a.b', 'absent']), []);
});
test('no terms found produces no candidate, not an answer', () => {
  assert.deepEqual(baseline(snap([source('x.md', 'ordinary text')]), ['alpha', 'beta']), []);
});
test('search sorts paths and caps at twenty matching lines', () => {
  const result = baseline(snap([source('z.md', 'alpha'), source('a.md', Array(30).fill('alpha').join('\n'))]), ['alpha', 'beta']);
  assert.equal(result.length, 1); assert.equal(result[0].path, 'a.md'); assert.equal(result[0].endLine, 23);
});
test('returned ranges preserve exact original bytes', () => {
  const text = '•\nα\nALPHA\n\n⊙\n○';
  assert.equal(baseline(snap([source('x.md', text)]), ['alpha', 'missing'])[0].text, text);
});
test('search term count enforced', () => {
  assert.throws(() => baseline(snap([]), ['one']));
  assert.throws(() => baseline(snap([]), ['a', 'b', 'c', 'd', 'e']));
});
test('pinned protocol, wrapper, engine and all original/copy source hashes agree', () => {
  verifyFreeze(JSON.parse(fs.readFileSync(path.join(here, 'freeze.json'))));
});
