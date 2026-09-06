#!/usr/bin/env node
// Read-only comparison: frozen P1 versus the opt-in generic APU passage module.
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import net from 'node:net';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { execFileSync } from 'node:child_process';
import { buildIndex, retrieve, validateCompletionManifest } from '../2026_09_06_apu_passage_pilot/passages.mjs';

const hash = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
const here = path.dirname(fileURLToPath(import.meta.url));
const json = file => JSON.parse(fs.readFileSync(file, 'utf8'));
const [inputArg, challengeArg] = process.argv.slice(2);
assert(inputArg && process.argv.length <= 4, 'Usage: node --experimental-strip-types run.mjs COMPLETED_P0_DIRECTORY [FRESH_CHALLENGES_JSON]');
const prior = path.resolve(here, '../2026_09_06_apu_readonly_pilot');
const lock = json(path.join(prior, 'source-lock.json'));
const engineLock = json(path.join(here, 'engine-lock.json'));
const moduleFile = path.join(engineLock.repo, engineLock.module);
const moduleBytes = fs.readFileSync(moduleFile);
assert.equal(hash(moduleBytes), engineLock.sha256, 'APU module drift');
const input = fs.realpathSync(path.resolve(inputArg));
assert.equal(input, path.resolve(inputArg), 'P0 input symlink refused');
const complete = json(path.join(input, 'COMPLETE.json'));
validateCompletionManifest(complete, lock.sources.map(s => s.path));
const inputFiles = [moduleFile, path.join(here, 'run.mjs'), path.join(here, 'engine-lock.json'),
  path.join(prior, 'source-lock.json'), path.join(prior, 'tasks.json'),
  path.resolve(here, '../2026_09_06_apu_passage_pilot/passages.mjs'),
  path.resolve(here, '../2026_09_06_apu_passage_pilot/challenges.json'),
  path.join(input, 'COMPLETE.json'), ...complete.files.map(e => path.join(input, e.path)),
  ...(challengeArg ? [path.resolve(challengeArg)] : [])];
const before = inputFiles.map(file => {
  assert.equal(fs.realpathSync(file), file, 'symlink refused');
  assert(fs.lstatSync(file).isFile());
  return { file, sha256: hash(fs.readFileSync(file)) };
});
for (const f of complete.files) assert.equal(hash(fs.readFileSync(path.join(input, f.path))), f.sha256, 'P0 artifact drift');
assert.deepEqual(json(path.join(input, 'source-lock.json')), lock);
const snapshot = json(path.join(input, 'snapshot.json'));
assert.equal(snapshot.revision, lock.sourceRevision);
assert.equal(snapshot.scopeId, lock.scopeId);
assert.deepEqual(snapshot.sources.map(s => [s.path, s.sha256]).sort(), lock.sources.map(s => [s.path, s.sha256]).sort());
const checkOriginals = () => {
  for (const s of lock.sources) {
    const file = path.join(lock.sourceRepo, s.path);
    assert.equal(fs.realpathSync(file), file);
    assert.equal(hash(fs.readFileSync(file)), s.sha256, 'original source drift');
    assert.equal(hash(execFileSync('git', ['show', `HEAD:${s.path}`], { cwd: lock.sourceRepo })), s.sha256, 'source HEAD drift');
  }
};
checkOriginals();
const known = [...json(path.join(prior, 'tasks.json')).tasks,
  ...json(path.resolve(here, '../2026_09_06_apu_passage_pilot/challenges.json'))];
const fresh = challengeArg ? json(path.resolve(challengeArg)) : [];
assert(Array.isArray(fresh) && fresh.length <= 10);
const tasks = [...known.map(t => ({ ...t, group: 'revealed-development' })), ...fresh.map(t => ({ ...t, group: 'withheld-until-code-freeze' }))];
assert.equal(new Set(tasks.map(t => t.id)).size, tasks.length);
for (const t of tasks) {
  assert(typeof t.id === 'string' && typeof t.query === 'string');
  if (t.expectedSource) {
    const source = snapshot.sources.find(s => s.path === t.expectedSource); assert(source, 'unknown expected source');
    for (const [start, end] of t.requiredRanges ?? [t.expectedLines]) assert(Number.isInteger(start) && Number.isInteger(end) && start > 0 && end >= start && end <= source.content.split('\n').length, 'invalid expected range');
  }
}
let attempts = 0;
const refuse = () => { attempts++; throw Error('P2 network refused'); };
globalThis.fetch = refuse; net.Socket.prototype.connect = refuse;
const { createCorpusPassageReader, PASSAGE_POLICY } = await import(pathToFileURL(moduleFile));
const original = hash(JSON.stringify(snapshot));
const reader = await createCorpusPassageReader(snapshot), idx = buildIndex(snapshot);
const results = [];
for (const task of tasks) {
  const p1 = retrieve(idx, { query: task.query }), p2 = await reader.search(task.query);
  assert.deepEqual(p2, await reader.search(task.query));
  const measure = result => {
    const ranges = task.requiredRanges ?? (task.expectedLines ? [task.expectedLines] : []);
    const hits = result.hits.filter(h => h.passage.path === task.expectedSource);
    return { expectedOwnerFound: task.expectedSource ? hits.length > 0 : null,
      expectedRangeOverlap: ranges.length ? hits.some(h => ranges.some(([a,b]) => h.passage.endLine >= a && h.passage.startLine <= b)) : null,
      allRequiredRangesIncluded: ranges.length ? ranges.every(([a,b]) => hits.some(h => h.passage.startLine <= a && h.passage.endLine >= b)) : null,
      abstained: result.hits.length === 0, semanticCorrectness: 'UNSCORED; exact ranges are not semantic support' };
  };
  for (const r of [p1,p2]) for (const h of r.hits) {
    const source = snapshot.sources.find(s => s.path === h.passage.path); assert(source);
    const text = source.content.split('\n').slice(h.passage.startLine - 1, h.passage.endLine).join('\n');
    assert.equal(text, h.passage.text); assert.equal(hash(text), h.passage.excerptSha256);
    assert.equal(source.sha256, h.passage.sourceSha256);
  }
  results.push({ task, p1, p2, measurements: { p1: measure(p1), p2: measure(p2) } });
}
assert.equal(hash(JSON.stringify(snapshot)), original, 'snapshot mutation');
assert.equal(attempts, 0); checkOriginals();
for (const f of before) assert.equal(hash(fs.readFileSync(f.file)), f.sha256, 'input/implementation changed during run');
const output = fs.mkdtempSync(path.join(fs.realpathSync(os.tmpdir()), 'emergentism-apu-relevance-'));
fs.chmodSync(output, 0o700);
const written = [];
const write = (name, value) => {
  fs.writeFileSync(path.join(output, name), JSON.stringify(value, null, 2) + '\n', { flag: 'wx', mode: 0o600 });
  written.push({ path: name, sha256: hash(fs.readFileSync(path.join(output, name))) });
};
write('results.json', results);
write('receipt.json', { version: 1, status: 'LOCAL_READ_ONLY_CANDIDATE_NOT_LIVE_APU', policy: PASSAGE_POLICY,
  p0Input: input, inputHashes: before, sourceRevision: snapshot.revision,
  networkAttemptsObserved: attempts, inputUnchangedAtCheckpoints: true, deterministicRepeatedQueries: true,
  limitations: ['No OS sandbox claim', 'No browser or provider integration', 'Lexical/section inclusion, not semantic correctness',
    'English heuristic; short symbols and paraphrases may be missed', 'No source, policy or permission change', 'No push or deploy', 'A3 recorder remains HOLD'] });
write('COMPLETE.json', { files: [...written] });
console.log(JSON.stringify({ output, measurements: results.map(r => ({ id: r.task.id, group: r.task.group, ...r.measurements })) }, null, 2));
