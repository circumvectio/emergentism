#!/usr/bin/env node
// Receipt checker only: no writes, app imports, provider calls, or source adoption.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const read = name => JSON.parse(fs.readFileSync(path.join(here, name), 'utf8'));
const sha = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
const lock = read('../2026_09_06_apu_readonly_pilot/source-lock.json');
assert.match(lock.sourceRevision, /^[0-9a-f]{40}$/);
const sources = lock.sources.map(s => {
  assert(s.path.split('/').every(p => /^[A-Za-z0-9][A-Za-z0-9_.-]*$/.test(p)));
  const bytes = execFileSync('git', ['show', lock.sourceRevision + ':' + s.path],
    { cwd: lock.sourceRepo, maxBuffer: 1024 * 1024 });
  assert.equal(sha(bytes), s.sha256);
  assert.equal(bytes.length, s.bytes);
  return { path: s.path, kind: s.kind, content: bytes.toString('utf8'), sha256: s.sha256 };
});
// Original P0 metadata, not a new source capture or a repaired source lock.
const workingSnapshot = { kind: 'aia.copied_corpus', version: 1,
  scopeId: lock.scopeId, revision: lock.sourceRevision,
  capturedAt: '2026-09-06T04:42:38.093Z', sources };
const externalSnapshot = read('external-snapshot.json');
const working = read('working-citations.json');
const external = read('external-citations.json');
const inspection = read('external-inspections.json');
const inputHash = (receipt, role) => receipt.inputHashes.find(x => x.role === role).sha256;
assert.equal(sha(JSON.stringify(workingSnapshot, null, 2) + '\n'), inputHash(working.receipt, 'snapshot'));
for (const [index, request, snapshotFile] of [
  [working, 'working-questions.json', null],
  [external, 'external-questions.json', 'external-snapshot.json'],
  [inspection, 'external-inspection-questions.json', 'external-snapshot.json'],
]) {
  assert.equal(sha(fs.readFileSync(path.join(here, request))), inputHash(index.receipt, 'request'));
  if (snapshotFile) assert.equal(sha(fs.readFileSync(path.join(here, snapshotFile))), inputHash(index.receipt, 'snapshot'));
  for (const engine of index.receipt.engineFiles) {
    assert.equal(sha(fs.readFileSync(path.join(lock.engineRepo, 'apu.bot', engine.path))), engine.sha256,
      'Current owned engine drift: ' + engine.path);
  }
}
let citations = 0;
function checkResults(results, snapshot, requestFile) {
  for (const s of snapshot.sources) assert.equal(sha(s.content), s.sha256);
  const requests = read(requestFile).questions;
  assert.equal(results.length, requests.length);
  for (const [i, r] of results.entries()) {
    assert.equal(r.id, requests[i].id);
    assert.equal(r.question, requests[i].question);
    assert.equal(r.original.query, requests[i].question);
    assert.deepEqual(r.reformulated.map(({query, proposedBy, basis, rationale}) =>
      ({query, proposedBy, basis, rationale})), requests[i].reformulations);
    for (const attempt of [r.original, ...r.reformulated.map(q => q.result)]) {
      assert.equal(attempt.revision, snapshot.revision);
      for (const hit of attempt.hits) {
        const p = hit.passage, s = snapshot.sources.find(s => s.path === p.path);
        assert(s);
        assert.equal(p.sourceSha256, s.sha256);
        assert.equal(p.revision, snapshot.revision);
        assert(Number.isInteger(p.startLine) && p.startLine >= 1);
        assert(Number.isInteger(p.endLine) && p.endLine >= p.startLine && p.endLine <= s.content.split('\n').length);
        assert.equal(sha(s.content.split('\n').slice(p.startLine - 1, p.endLine).join('\n')), p.excerptSha256);
        assert.equal(hit.qualificationCoverage, 'NOT_ASSESSED');
        citations++;
      }
    }
  }
}
checkResults(working.results, workingSnapshot, 'working-questions.json');
checkResults(external.report.results, externalSnapshot, 'external-questions.json');
for (const [items, snapshot] of [[working.inspections, workingSnapshot], [inspection.inspections, externalSnapshot]]) {
  for (const i of items) {
    const s = snapshot.sources.find(s => s.path === i.path);
    assert(s);
    assert.equal(i.kind, 'SOURCE_INSPECTION');
    assert.equal(i.sha256, s.sha256);
    assert.equal(i.startLine, 1);
    assert.equal(i.endLine, s.content.split('\n').length);
    assert.equal(i.qualificationCoverage, 'NOT_ASSESSED');
  }
}
const key = read('external-key.json');
function covers(hits, range) {
  // Union of contiguous returned lines, never count gaps as coverage.
  let next = range.startLine;
  for (const p of hits.map(h => h.passage).filter(p => p.path === range.path)
    .sort((a,b) => a.startLine - b.startLine)) {
    if (p.startLine <= next && p.endLine >= next) next = p.endLine + 1;
  }
  return next > range.endLine;
}
const scores = key.keys.map(k => {
  const r = external.report.results.find(r => r.id === k.id);
  assert(r);
  const assisted = r.reformulated.flatMap(q => q.result.hits);
  return { id: k.id, class: k.class,
    originalHits: r.original.hits.length, assistedHits: assisted.length,
    originalComplete: k.class === 'supported' ? k.requiredRanges.every(q => covers(r.original.hits, q)) : null,
    assistedComplete: k.class === 'supported' ? k.requiredRanges.every(q => covers([...r.original.hits, ...assisted], q)) : null };
});
assert.equal(scores.filter(s => s.originalComplete).length, 0);
assert.equal(scores.filter(s => s.assistedComplete).length, 2);
assert(scores.filter(s => s.class === 'unsupported').every(s => s.originalHits === 0 && s.assistedHits === 0));
console.log(JSON.stringify({ status: 'LOCAL_RECEIPT_CHECK_PASS', citationsChecked: citations, scores,
  limits: ['Exact citation and numeric coverage check, not semantic adjudication',
    'Key pre-reveal immutability is agent-reported, not hash-proven',
    'No CLI replay or runtime isolation proof from this checker',
    'Working snapshot reconstructed from original Git revision without a new source pin'] }, null, 2));
