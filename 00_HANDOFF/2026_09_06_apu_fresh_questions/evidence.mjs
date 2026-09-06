#!/usr/bin/env node
// Preserve/replay exact offline evidence without depending on a temporary folder.
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import crypto from 'node:crypto';
import zlib from 'node:zlib';
import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { here, verifyFreeze } from './trial.mjs';
const sha = b => crypto.createHash('sha256').update(b).digest('hex');
const freeze = JSON.parse(fs.readFileSync(path.join(here, 'freeze.json')));
const complete = JSON.parse(fs.readFileSync(path.join(here, 'results.json'))).rawManifest;
const archive = path.join(here, 'evidence.json.gz');
const names = ['snapshot.json', ...freeze.engine.map(e => `engine/${e.path}`),
  'run/COMPLETE.json', ...complete.files.map(f => `run/${f.path}`)].sort();
if (process.argv[2] === 'pack' || process.argv[2] === '--check') {
  verifyFreeze(freeze);
  const entries = names.map(p => { const bytes = fs.readFileSync(path.join(freeze.root, p));
    return { path: p, sha256: sha(bytes), bytes: bytes.length, base64: bytes.toString('base64') }; });
  const bytes = zlib.gzipSync(JSON.stringify({ kind: 'offline_trial_evidence', version: 1, entries }), { level: 9 });
  if (process.argv[2] === '--check') assert(fs.readFileSync(archive).equals(bytes));
  else fs.writeFileSync(archive, bytes, { flag: 'wx', mode: 0o600 });
  console.log(JSON.stringify({ archiveSha256: sha(bytes), compressedBytes: bytes.length, entries: entries.length }));
} else if (process.argv[2] === 'replay') {
  const payload = JSON.parse(zlib.gunzipSync(fs.readFileSync(archive), { maxOutputLength: 4 * 1024 * 1024 }));
  assert.equal(payload.kind, 'offline_trial_evidence'); assert.equal(payload.version, 1);
  assert.deepEqual(payload.entries.map(e => e.path), names);
  const root = fs.realpathSync(fs.mkdtempSync(path.join(os.tmpdir(), 'apu-evidence-replay-')));
  for (const e of payload.entries) {
    assert(!path.isAbsolute(e.path) && !e.path.split('/').includes('..'));
    const bytes = Buffer.from(e.base64, 'base64'); assert.equal(bytes.length, e.bytes); assert.equal(sha(bytes), e.sha256);
    const target = path.join(root, e.path); fs.mkdirSync(path.dirname(target), { recursive: true, mode: 0o700 });
    fs.writeFileSync(target, bytes, { flag: 'wx', mode: 0o600 });
  }
  const hashAt = p => sha(fs.readFileSync(path.join(root, p)));
  assert.equal(hashAt('snapshot.json'), freeze.snapshotSha256);
  for (const e of freeze.engine) assert.equal(hashAt(`engine/${e.path}`), e.sha256);
  for (const f of complete.files) assert.equal(hashAt(`run/${f.path}`), f.sha256);
  const argv = ['--experimental-strip-types', path.join(root, 'engine/apu.bot/scripts/inspect_library.mjs'),
    path.join(root, 'snapshot.json'), path.join(root, 'run/request.json'), '--browse'];
  const options = { cwd: root, env: { PATH: path.dirname(process.execPath), LANG: 'C.UTF-8', NODE_ENV: 'test' }, timeout: 60000, maxBuffer: 4 * 1024 * 1024 };
  const output = execFileSync(process.execPath, argv, options);
  assert.equal(sha(output), hashAt('run/first.json'));
  const snapshot = JSON.parse(fs.readFileSync(path.join(root, 'snapshot.json')));
  const request = JSON.parse(fs.readFileSync(path.join(root, 'run/request.json')));
  const checks = [];
  const refuse = (name, s, q) => {
    const sp = path.join(root, `${name}-snapshot.json`), qp = path.join(root, `${name}-request.json`);
    fs.writeFileSync(sp, JSON.stringify(s), { flag: 'wx' }); fs.writeFileSync(qp, JSON.stringify(q), { flag: 'wx' });
    try { execFileSync(process.execPath, [argv[0], argv[1], sp, qp, '--browse'], { ...options, stdio: ['ignore', 'pipe', 'pipe'] }); }
    catch (error) { assert.equal(error.status, 1); const reason = String(error.stderr).trim();
      assert(reason.startsWith('inspect_library:')); checks.push({ name, refused: true, reason }); return; }
    assert.fail(`${name} was accepted`);
  };
  const tampered = structuredClone(snapshot); tampered.sources[0].content += 'tamper'; refuse('digest-drift', tampered, request);
  const extra = structuredClone(snapshot); extra.authority = 'publish'; refuse('extra-authority-field', extra, request);
  const duplicate = structuredClone(request); duplicate.questions[1].id = duplicate.questions[0].id; refuse('duplicate-id', snapshot, duplicate);
  const huge = structuredClone(request); huge.questions[0].question = 'a'.repeat(401); refuse('oversized-query', snapshot, huge);
  const escape = structuredClone(snapshot); escape.sources[0].path = '../escape.md'; refuse('source-path-escape', escape, request);
  console.log(JSON.stringify({ replayByteIdentical: true, archiveSha256: sha(fs.readFileSync(archive)), checks,
    sourceOrEngineWrites: 0, providerCalls: 0, root, limits: 'Copied-process refusal tests, not an OS sandbox or autonomous readiness.' }, null, 2));
} else throw Error('usage: evidence.mjs pack|--check|replay');
