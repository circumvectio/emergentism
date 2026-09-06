#!/usr/bin/env node
// Feed a completed pinned P0 package to an offline derived passage layer.
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import net from 'node:net';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
import { fileURLToPath } from 'node:url';
import { execFileSync } from 'node:child_process';
const hash = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
const here = path.dirname(fileURLToPath(import.meta.url));
const prior = path.resolve(here, '../2026_09_06_apu_readonly_pilot');
const json = p => JSON.parse(fs.readFileSync(p, 'utf8'));
const lock = json(path.join(prior, 'source-lock.json'));
const [runArg, challengeArg] = process.argv.slice(2);
assert(runArg && process.argv.length <= 4, 'Usage: node run_passages.mjs COMPLETED_P0_DIRECTORY [CHALLENGES_JSON]');
const input = path.resolve(runArg);
assert.equal(fs.realpathSync(input), input, 'input must not have symlink ancestors');
const implementationNames = ['passages.mjs','run_passages.mjs','proposals.json','passages.test.mjs'];
const inputFiles = [...implementationNames.map(n => path.join(here,n)), path.join(prior,'source-lock.json'),
  path.join(prior,'tasks.json'), path.join(input,'COMPLETE.json'), ...(challengeArg ? [path.resolve(challengeArg)] : [])];
const initialHashes = inputFiles.map(file => ({ file, sha256: hash(fs.readFileSync(file)) }));
const { buildIndex, retrieve, citation, renderReport, renderSource, POLICY, validateCompletionManifest } = await import('./passages.mjs');
const complete = json(path.join(input, 'COMPLETE.json'));
validateCompletionManifest(complete, lock.sources.map(s => s.path));
for (const entry of complete.files) {
  assert(entry.path.split('/').every(p => /^[A-Za-z0-9][A-Za-z0-9_.-]*$/.test(p)), 'unsafe manifest path');
  const file = path.join(input, entry.path);
  assert.equal(fs.realpathSync(file), file); assert(fs.lstatSync(file).isFile());
  assert.equal(hash(fs.readFileSync(file)), entry.sha256, 'P0 artifact drift');
}
assert.equal(hash(fs.readFileSync(path.join(input, 'source-lock.json'))), hash(fs.readFileSync(path.join(prior, 'source-lock.json'))));
const snapshot = json(path.join(input, 'snapshot.json'));
assert.equal(snapshot.revision, lock.sourceRevision);
assert.equal(snapshot.scopeId, lock.scopeId);
assert.equal(snapshot.sources.length, lock.sources.length);
const originalCheck = () => {
  for (const s of snapshot.sources) {
    const expected = lock.sources.find(e => e.path === s.path);
    assert(expected && expected.sha256 === s.sha256);
    const file = path.join(lock.sourceRepo, s.path);
    assert.equal(fs.realpathSync(file), file);
    assert.equal(hash(fs.readFileSync(file)), expected.sha256, 'original source drift');
    assert.equal(hash(execFileSync('git', ['show', `HEAD:${s.path}`], { cwd: lock.sourceRepo })), expected.sha256);
  }
};
originalCheck();
const proposals = json(path.join(here, 'proposals.json'));
const baseline = json(path.join(prior, 'tasks.json')).tasks;
const challenges = challengeArg ? json(path.resolve(challengeArg)) : [];
assert(Array.isArray(challenges) && challenges.length <= 10);
const tasks = [...baseline.map(t => ({ ...t, group: 'known-development' })), ...challenges.map(t => ({ ...t, group: 'withheld-until-freeze' }))];
assert.equal(new Set(tasks.map(t => t.id)).size, tasks.length, 'duplicate task');
let attempts = 0;
const refuse = () => { attempts++; throw new Error('P1 network refused'); };
globalThis.fetch = refuse; net.Socket.prototype.connect = refuse;
const idx = buildIndex(snapshot);
const indexBefore = hash(JSON.stringify(idx));
const results = tasks.map(task => {
  const literal = retrieve(idx, { query: task.query });
  const expanded = retrieve(idx, { query: task.query, aliases: proposals.aliases });
  assert.deepEqual(literal, retrieve(idx, { query: task.query }));
  assert.deepEqual(expanded, retrieve(idx, { query: task.query, aliases: proposals.aliases }));
  const route = r => ({ status: r.status, expectedOwnerFound: task.expectedSource ? r.hits.some(h => h.passage.path === task.expectedSource) : null,
    expectedRangeOverlap: task.expectedLines ? r.hits.some(h => h.passage.path === task.expectedSource && h.passage.endLine >= task.expectedLines[0] && h.passage.startLine <= task.expectedLines[1]) : null,
    semanticCorrectness: 'unscored; range overlap is not qualification coverage' });
  return { task, measurements: { literal: route(literal), expanded: route(expanded) }, literal, expanded };
});
const citedProposals = structuredClone(proposals);
for (const item of [...citedProposals.aliases, ...citedProposals.outline]) {
  const d = idx.documents.find(d => d.source.path === item.path); assert(d);
  assert(item.startLine > 0 && item.endLine <= d.lines.length && item.endLine >= item.startLine);
  item.evidence = citation(d, item.startLine, item.endLine, snapshot.revision);
}
assert.equal(indexBefore, hash(JSON.stringify(idx)), 'reader mutated input');
originalCheck(); assert.equal(attempts, 0);
for (const item of initialHashes) assert.equal(hash(fs.readFileSync(item.file)), item.sha256, 'implementation or input changed during run');
const output = fs.mkdtempSync(path.join(fs.realpathSync(os.tmpdir()), 'emergentism-apu-passages-'));
fs.chmodSync(output, 0o700);
const written = [];
const write = (name, content) => {
  const file = path.join(output, name);
  fs.mkdirSync(path.dirname(file), { recursive: true, mode: 0o700 });
  fs.writeFileSync(file, typeof content === 'string' ? content : JSON.stringify(content, null, 2)+'\n', { flag: 'wx', mode: 0o600 });
  written.push(name);
};
write('results.json', results); write('proposals.json', citedProposals);
write('index.html', renderReport(results.map(r => r.literal)));
write('expanded.html', renderReport(results.map(r => r.expanded)));
for (const d of idx.documents) write(`sources/${d.source.path}.html`, renderSource(d));
write('receipt.json', { kind: 'emergentism.apu_passage_pilot', version: 1,
  status: 'OFFLINE_DERIVED_VIEW_NOT_APU_PRODUCT_RELEASE', policy: POLICY,
  sourceRevision: snapshot.revision, p0InputDirectory: input,
  p0CompleteSha256: hash(fs.readFileSync(path.join(input, 'COMPLETE.json'))),
  sourceLockSha256: hash(fs.readFileSync(path.join(prior, 'source-lock.json'))),
  implementation: implementationNames.map(name => ({ name, sha256: initialHashes.find(x => x.file === path.join(here,name)).sha256 })),
  inputsUnchangedAtCheckpoints: true, initialInputHashes: initialHashes,
  challengeSha256: challengeArg ? hash(fs.readFileSync(path.resolve(challengeArg))) : null,
  noMutationAtCheckpoints: true, deterministicQueries: true, fetchAndTcpAttempts: attempts,
  limits: ['No OS egress/write sandbox claim', 'No APU provider calls or native-core modification', 'No semantic or human-usefulness score', 'Suggestions are drafts, not grants', 'No site update, push or deployment'] });
write('COMPLETE.json', { files: written.map(name => ({ path: name, sha256: hash(fs.readFileSync(path.join(output, name))) })) });
console.log(JSON.stringify({ output, tasks: results.length, measurements: results.map(r => ({ id: r.task.id, ...r.measurements })) }, null, 2));
