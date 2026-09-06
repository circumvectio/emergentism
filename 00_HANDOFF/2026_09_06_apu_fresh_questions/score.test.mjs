import test from 'node:test';
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import { covered, lineCount, measure, verifyCitation } from './score.mjs';
const r = (a, b, p = 'a.md') => ({ path: p, startLine: a, endLine: b });
test('union coverage permits adjacent ranges, not gaps or another source', () => {
  assert(covered(r(2, 6), [r(1, 3), r(4, 9)]));
  assert(!covered(r(2, 6), [r(1, 3), r(5, 9)]));
  assert(!covered(r(2, 6), [r(1, 9, 'b.md')]));
});
test('overlapping passages count once per source and line', () => {
  assert.equal(lineCount([r(1, 3), r(2, 4), r(1, 2, 'b.md')]), 6);
});
test('qualification miss prevents all-parts coverage', () => {
  const q = { expected: 'supported', requiredParts: [
    { id: 'definition', qualification: false, alternatives: [r(1, 2)] },
    { id: 'fence', qualification: true, alternatives: [r(8, 9), r(10, 11)] },
  ] };
  assert.equal(measure(q, [r(1, 7)]).allParts, false);
  assert.equal(measure(q, [r(1, 2), r(10, 11)]).allParts, true);
});
test('unsupported empty is not a vacuous supported answer', () => {
  const q = { expected: 'unsupported', requiredParts: [] };
  assert.equal(measure(q, []).allParts, null);
  assert.equal(measure(q, []).emptyOnUnsupported, true);
  assert.equal(measure(q, [r(1, 2)]).emptyOnUnsupported, false);
});
test('source, revision, excerpt and range drift fail closed', () => {
  const sha = s => crypto.createHash('sha256').update(s).digest('hex');
  const content = 'α\n⊙\n○', hash = sha(content);
  const snapshot = { revision: 'pin', sources: [{ path: 'a.md', content, sha256: hash }] };
  const p = { ...r(2, 3), revision: 'pin', sourceSha256: hash, text: '⊙\n○', excerptSha256: sha('⊙\n○') };
  verifyCitation(p, snapshot);
  for (const change of [{ path: 'b.md' }, { revision: 'wrong' }, { text: 'edited' }, { sourceSha256: 'wrong' }, { startLine: 0 }, { endLine: 5 }])
    assert.throws(() => verifyCitation({ ...p, ...change }, snapshot));
});
