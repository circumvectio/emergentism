#!/usr/bin/env node
// Local evaluation custody wrapper, not APU product logic or worldview authority.
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

export const here = path.dirname(fileURLToPath(import.meta.url));
const repo = path.resolve(here, '../..');
const hash = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
const json = p => JSON.parse(fs.readFileSync(p, 'utf8'));
const git = (cwd, ...args) => execFileSync('git', args, { cwd, maxBuffer: 16 * 1024 * 1024 });
const write = (p, value) => { fs.mkdirSync(path.dirname(p), { recursive: true, mode: 0o700 });
  fs.writeFileSync(p, typeof value === 'string' || Buffer.isBuffer(value) ? value : JSON.stringify(value, null, 2) + '\n', { flag: 'wx', mode: 0o600 }); };
const enginePaths = ['apu.bot/scripts/inspect_library.mjs', 'apu.bot/src/lib/libraryFacets.ts',
  'apu.bot/src/lib/libraryInvestigation.ts', 'apu.bot/src/lib/corpusPassages.ts'];
const checkFile = (p, sha256) => { assert.equal(fs.realpathSync(p), p); assert(fs.lstatSync(p).isFile()); assert.equal(hash(fs.readFileSync(p)), sha256); };

export function prepare() {
  const lock = json(path.join(here, '../2026_09_06_apu_readonly_pilot/source-lock.json'));
  const engineRevision = git(lock.engineRepo, 'rev-parse', 'dd61933^{commit}').toString().trim();
  const root = fs.realpathSync(fs.mkdtempSync(path.join(os.tmpdir(), 'apu-fresh-questions-')));
  const capturedAt = new Date().toISOString();
  const sources = lock.sources.map(s => {
    checkFile(path.join(repo, s.path), s.sha256);
    assert.equal(git(repo, 'status', '--porcelain', '--', s.path).toString().trim(), '');
    const bytes = git(repo, 'show', `${lock.sourceRevision}:${s.path}`);
    assert.equal(bytes.length, s.bytes); assert.equal(hash(bytes), s.sha256);
    assert.equal(hash(git(repo, 'show', `HEAD:${s.path}`)), s.sha256);
    const content = new TextDecoder('utf-8', { fatal: true, ignoreBOM: true }).decode(bytes);
    assert(Buffer.from(content).equals(bytes));
    write(path.join(root, 'sources', s.path), bytes);
    return { path: s.path, kind: s.kind, content, sha256: s.sha256 };
  });
  const engine = enginePaths.map(p => {
    const bytes = git(lock.engineRepo, 'show', `${engineRevision}:${p}`);
    write(path.join(root, 'engine', p), bytes);
    return { path: p, sha256: hash(bytes) };
  });
  const snapshot = { kind: 'aia.copied_corpus', version: 1, scopeId: 'emergentism-fresh-questions-2026-09-06',
    revision: lock.sourceRevision, capturedAt, sources };
  write(path.join(root, 'snapshot.json'), snapshot);
  const freeze = { version: 1, root, capturedAt, sourceRevision: lock.sourceRevision,
    sourceHeadAtCapture: git(repo, 'rev-parse', 'HEAD').toString().trim(), sourceRepo: repo,
    sourceLockSha256: hash(fs.readFileSync(path.join(here, '../2026_09_06_apu_readonly_pilot/source-lock.json'))),
    engineRepo: lock.engineRepo, engineRevision,
    engineHeadAtCapture: git(lock.engineRepo, 'rev-parse', 'HEAD').toString().trim(), engine,
    sources: lock.sources, snapshotSha256: hash(fs.readFileSync(path.join(root, 'snapshot.json'))),
    protocolSha256: hash(fs.readFileSync(path.join(here, 'PROTOCOL.md'))),
    wrapperSha256: hash(fs.readFileSync(fileURLToPath(import.meta.url))), node: process.version,
    constraints: { providerCalls: 0, sourceWrites: 0, permissionsChanged: false, a3: 'HOLD_NOT_ATTEMPTED' } };
  write(path.join(here, 'freeze.json'), freeze);
  console.log(JSON.stringify({ root, engineRevision, sourceCount: sources.length }));
}

export function baseline(snapshot, terms) {
  assert(terms.length >= 2 && terms.length <= 4 && terms.every(t => typeof t === 'string' && t.trim()));
  const matches = [];
  for (const s of [...snapshot.sources].sort((a, b) => a.path < b.path ? -1 : a.path > b.path ? 1 : 0)) {
    const lines = s.content.split('\n');
    for (let n = 0; n < lines.length && matches.length < 20; n++) {
      if (terms.some(t => lines[n].toLowerCase().includes(t.toLowerCase())))
        matches.push({ path: s.path, startLine: Math.max(1, n - 2), endLine: Math.min(lines.length, n + 4) });
    }
  }
  const merged = [];
  for (const m of matches) { const last = merged.at(-1);
    if (last && last.path === m.path && m.startLine <= last.endLine + 1) last.endLine = Math.max(last.endLine, m.endLine);
    else merged.push({ ...m });
  }
  return merged.map(m => { const s = snapshot.sources.find(s => s.path === m.path);
    const text = s.content.split('\n').slice(m.startLine - 1, m.endLine).join('\n');
    return { ...m, text, sourceSha256: s.sha256, excerptSha256: hash(text), revision: snapshot.revision }; });
}

export function verifyFreeze(f) {
  assert.deepEqual(f.engine.map(e => e.path), enginePaths);
  const lockBytes = fs.readFileSync(path.join(here, '../2026_09_06_apu_readonly_pilot/source-lock.json'));
  assert.equal(hash(lockBytes), f.sourceLockSha256);
  assert.deepEqual(f.sources, JSON.parse(lockBytes).sources);
  checkFile(path.join(here, 'PROTOCOL.md'), f.protocolSha256);
  checkFile(fileURLToPath(import.meta.url), f.wrapperSha256);
  checkFile(path.join(f.root, 'snapshot.json'), f.snapshotSha256);
  for (const s of f.sources) { checkFile(path.join(f.sourceRepo, s.path), s.sha256); checkFile(path.join(f.root, 'sources', s.path), s.sha256); }
  for (const e of f.engine) checkFile(path.join(f.root, 'engine', e.path), e.sha256);
}

export function freezeCases() {
  const files = ['questions.json', 'query-aids.json'].map(p => {
    const bytes = fs.readFileSync(path.join(here, p));
    assert(bytes.equals(git(repo, 'show', `HEAD:${path.relative(repo, here)}/${p}`)), 'case input not committed');
    return { path: p, sha256: hash(bytes) };
  });
  write(path.join(here, 'case-freeze.json'), { version: 1, keyLocation: 'questions.json requiredParts and expected',
    protocolCommit: git(repo, 'log', '-1', '--format=%H', '--', path.relative(repo, path.join(here, 'freeze.json'))).toString().trim(),
    inputsCommit: git(repo, 'rev-parse', 'HEAD').toString().trim(),
    freezeSha256: hash(fs.readFileSync(path.join(here, 'freeze.json'))), files });
}

export function run() {
  const f = json(path.join(here, 'freeze.json')); verifyFreeze(f);
  const manifestBytes = fs.readFileSync(path.join(here, 'case-freeze.json'));
  assert(manifestBytes.equals(git(repo, 'show', `HEAD:${path.relative(repo, here)}/case-freeze.json`)), 'case manifest not committed');
  const manifest = JSON.parse(manifestBytes);
  assert.equal(hash(fs.readFileSync(path.join(here, 'freeze.json'))), manifest.freezeSha256);
  assert.equal(hash(git(repo, 'show', `${manifest.protocolCommit}:${path.relative(repo, here)}/freeze.json`)), manifest.freezeSha256);
  const captured = manifest.files.map(item => { const bytes = fs.readFileSync(path.join(here, item.path));
    assert.equal(hash(bytes), item.sha256); return { ...item, bytes }; });
  assert.deepEqual(captured.map(c => c.path), ['questions.json', 'query-aids.json']);
  const questions = JSON.parse(captured[0].bytes);
  const aids = JSON.parse(captured[1].bytes);
  assert.equal(questions.questions.length, 10); assert.equal(aids.length, 10);
  const request = { version: 1, questions: questions.questions.map((q, n) => {
    assert.equal(q.id, aids[n].id);
    return { id: q.id, question: q.question, facets: [{ id: 'rephrase', query: aids[n].rephrase,
      proposedBy: 'question-only-agent', basis: 'question-only', rationale: aids[n].rationale }] };
  }), inspectPaths: [] };
  const out = path.join(f.root, 'run'); fs.mkdirSync(out, { mode: 0o700 }); // refuse overwrite
  write(path.join(out, 'request.json'), request);
  write(path.join(out, 'case-freeze.json'), manifestBytes);
  for (const c of captured) write(path.join(out, c.path), c.bytes);
  const cli = path.join(f.root, 'engine/apu.bot/scripts/inspect_library.mjs');
  const argv = ['--experimental-strip-types', cli, path.join(f.root, 'snapshot.json'), path.join(out, 'request.json'), '--browse'];
  for (const name of ['first.json', 'repeat.json']) {
    try {
      const bytes = execFileSync(process.execPath, argv, { cwd: out,
        env: { PATH: path.dirname(process.execPath), LANG: 'C.UTF-8', NODE_ENV: 'test' },
        timeout: 60000, maxBuffer: 16 * 1024 * 1024, stdio: ['ignore', 'pipe', 'pipe'] });
      write(path.join(out, name), bytes);
    } catch (error) {
      write(path.join(out, `${name}.failed.stdout`), error.stdout ?? Buffer.alloc(0));
      write(path.join(out, `${name}.failed.stderr`), error.stderr ?? Buffer.alloc(0));
      write(path.join(out, 'FAILED.json'), { phase: name, status: error.status ?? null, signal: error.signal ?? null,
        files: fs.readdirSync(out).sort().map(p => ({ path: p, sha256: hash(fs.readFileSync(path.join(out, p))) })),
        meaning: 'Execution failed; no completion or result-quality claim.' });
      throw Error('child_failed_output_preserved');
    }
  }
  assert(fs.readFileSync(path.join(out, 'first.json')).equals(fs.readFileSync(path.join(out, 'repeat.json'))));
  const snapshot = json(path.join(f.root, 'snapshot.json'));
  write(path.join(out, 'baseline.json'), aids.map(a => ({ id: a.id, terms: a.searchTerms, passages: baseline(snapshot, a.searchTerms) })));
  verifyFreeze(f);
  assert(fs.readFileSync(path.join(here, 'case-freeze.json')).equals(manifestBytes));
  assert.equal(hash(fs.readFileSync(path.join(here, 'freeze.json'))), manifest.freezeSha256);
  for (const c of captured) checkFile(path.join(here, c.path), c.sha256);
  const files = fs.readdirSync(out).sort().map(p => ({ path: p, bytes: fs.statSync(path.join(out, p)).size, sha256: hash(fs.readFileSync(path.join(out, p))) }));
  write(path.join(out, 'COMPLETE.json'), { deterministic: true, sourceHashesUnchanged: true, engineHashesUnchanged: true, files,
    caseManifestSha256: hash(manifestBytes), inputsUnchangedAtCheckpoints: true,
    networkBoundary: 'APU CLI fetch/TCP refusal; sanitized child environment; not OS sandbox',
    providerCalls: 0, caveat: 'Completion is execution only, not retrieval adequacy or permission.' });
  console.log(JSON.stringify({ out, files }));
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  if (process.argv[2] === 'prepare') prepare();
  else if (process.argv[2] === 'freeze-cases') freezeCases();
  else if (process.argv[2] === 'run') run();
  else throw Error('usage: trial.mjs prepare|freeze-cases|run');
}
