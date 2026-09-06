#!/usr/bin/env node
// Receipt-side harness: unchanged, pinned APU core; no product/canon mutation.
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import crypto from 'node:crypto';
import net from 'node:net';
import assert from 'node:assert/strict';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { execFileSync } from 'node:child_process';

const self = fileURLToPath(import.meta.url);
const here = path.dirname(self);
const sha = x => crypto.createHash('sha256').update(x).digest('hex');
const json = p => JSON.parse(fs.readFileSync(p, 'utf8'));
const git = (repo, ...args) => execFileSync('git', args, { cwd: repo, maxBuffer: 32 * 1024 * 1024 });
const write = (root, name, value) => {
  const target = path.join(root, name);
  fs.mkdirSync(path.dirname(target), { recursive: true, mode: 0o700 });
  fs.writeFileSync(target, typeof value === 'string' || Buffer.isBuffer(value) ? value : JSON.stringify(value, null, 2) + '\n', { flag: 'wx', mode: 0o600 });
};
const safePath = p => typeof p === 'string' && p.split('/').every(s => /^[A-Za-z0-9][A-Za-z0-9_.-]*$/.test(s));

function readSources(lock) {
  assert.equal(lock.mode, 'offline-copy-only');
  assert.equal(lock.version, 1);
  assert.equal(lock.sources.length, 9);
  assert.match(lock.sourceRevision, /^[a-f0-9]{40}$/);
  const seen = new Set();
  const sources = lock.sources.map(item => {
    assert(safePath(item.path) && item.path.endsWith('.md'), 'unsafe source path');
    assert(!seen.has(item.path), 'duplicate source'); seen.add(item.path);
    assert.equal(item.kind, 'reference');
    const target = path.join(lock.sourceRepo, item.path);
    assert.equal(fs.realpathSync(target), target, 'symlink source or ancestor');
    assert(fs.lstatSync(target).isFile());
    assert(fs.statSync(target).size <= 256 * 1024);
    const bytes = fs.readFileSync(target);
    assert.equal(bytes.length, item.bytes);
    assert.equal(sha(bytes), item.sha256, `source drift: ${item.path}`);
    const content = new TextDecoder('utf-8', { fatal: true, ignoreBOM: true }).decode(bytes);
    assert(!content.includes('\0') && Buffer.from(content).equals(bytes), 'non-lossless UTF-8');
    assert.equal(git(lock.sourceRepo, 'status', '--porcelain', '--', item.path).toString().trim(), '', 'selected source dirty');
    assert.equal(sha(git(lock.sourceRepo, 'show', `${lock.sourceRevision}:${item.path}`)), item.sha256, 'pinned commit mismatch');
    // HEAD may advance for unrelated work or this receipt; selected bytes may not.
    assert.equal(sha(git(lock.sourceRepo, 'show', `HEAD:${item.path}`)), item.sha256, 'current committed source mismatch');
    return { path: item.path, kind: item.kind, content, sha256: item.sha256 };
  });
  assert(sources.reduce((n, s) => n + Buffer.byteLength(s.content), 0) <= 1024 * 1024);
  return sources;
}

function baseline(snapshot, task) {
  return snapshot.sources.flatMap(source => {
    const lines = source.content.split('\n').flatMap((line, i) => line.toLowerCase().includes(task.query.toLowerCase()) ? [i + 1] : []);
    return lines.length ? [{ path: source.path, matchingLines: lines }] : [];
  }).sort((a, b) => a.path.localeCompare(b.path));
}

function measurements(snapshot, tasks, run) {
  assert.equal(run.result.answers.length, tasks.tasks.length, 'answer count differs from frozen tasks');
  return run.result.answers.map((answer, i) => {
    const task = tasks.tasks[i];
    assert.equal(answer.message, `find ${task.query}`);
    const direct = baseline(snapshot, task);
    const cited = answer.citations.map(c => {
      const source = snapshot.sources.find(s => s.path === c.provenance?.path);
      assert(source, 'citation has no frozen source');
      assert.equal(c.provenance.sha256, source.sha256);
      assert.equal(c.provenance.revision, snapshot.revision);
      assert.equal(c.provenance.capturedAt, snapshot.capturedAt);
      assert.equal(c.provenance.kind, source.kind);
      assert.equal(c.provenance.adoption, 'not-adopted');
      return source.path;
    });
    assert.equal(answer.packet.receipt.provider, 'local');
    assert(answer.packet.ops.every(op => op.type === 'cite'));
    const paths = [...new Set(cited)];
    const directPaths = direct.map(s => s.path);
    return {
      id: task.id, query: task.query, expectedSource: task.expectedSource,
      directBodyMatches: direct, returnedNodeCount: cited.length, citedSourcePaths: paths,
      firstFiveNodeSourcePaths: [...new Set(cited.slice(0, 5))],
      expectedOwnerInAllHits: task.expectedSource ? paths.includes(task.expectedSource) : null,
      expectedOwnerInFirstFiveNodes: task.expectedSource ? cited.slice(0, 5).includes(task.expectedSource) : null,
      missedBodyMatchPaths: directPaths.filter(p => !paths.includes(p)),
      metadataOnlyPaths: paths.filter(p => !directPaths.includes(p)),
      nullControlPassed: task.expectedSource ? null : direct.length === 0 && cited.length === 0,
      citationProvenanceValid: true, semanticAnswerCorrectness: 'not measured',
    };
  });
}

async function worker(output) {
  assert.equal(fs.realpathSync(output), output);
  const lock = json(path.join(output, 'source-lock.json'));
  const tasks = json(path.join(output, 'tasks.json'));
  const snapshot = json(path.join(output, 'snapshot.json'));
  let attempts = 0;
  const refuse = () => { attempts++; throw new Error('pilot fetch/TCP refused'); };
  // Installed before importing Vite or the APU core. Not an OS network sandbox.
  globalThis.fetch = refuse;
  net.Socket.prototype.connect = refuse;
  const memory = new Map();
  Object.defineProperty(globalThis, 'localStorage', { value: {
    getItem: key => memory.get(key) ?? null,
    setItem: (key, value) => memory.set(key, value),
    removeItem: key => memory.delete(key),
  } });
  const product = path.join(output, 'engine', 'apu.bot');
  const loader = path.join(product, 'node_modules', 'vite', 'dist', 'node', 'index.js');
  const { createServer, version } = await import(pathToFileURL(loader).href);
  const server = await createServer({ root: product, configFile: false, envFile: false,
    cacheDir: path.join(output, 'loader-cache'),
    server: { middlewareMode: true, hmr: false, watch: null },
    optimizeDeps: { noDiscovery: true, include: [] } });
  let first, second, tests;
  try {
    const core = await server.ssrLoadModule('/scripts/copied_pilot_core.ts');
    const intake = await server.ssrLoadModule('/src/lib/corpusIntake.ts');
    const queries = tasks.tasks.map(t => `find ${t.query}`);
    first = await core.rehearse(snapshot, queries);
    second = await core.rehearse(snapshot, queries, snapshot);
    // APU records wall-clock receipt and node-version times. Preserve the raw
    // runs; only the known receipt timestamp is excluded from answer equality.
    const stableAnswers = run => run.result.answers.map(answer => ({ ...answer,
      packet: { ...answer.packet, receipt: { ...answer.packet.receipt, createdAt: null } } }));
    assert.deepEqual(stableAnswers(first), stableAnswers(second));
    assert(second.result.delta.length === 9 && second.result.delta.every(s => s.status === 'unchanged'));
    tests = [];
    const reject = async (name, mutation, error) => {
      const altered = structuredClone(snapshot); mutation(altered);
      await assert.rejects(() => intake.validateCorpusSnapshot(altered), error);
      tests.push({ name, pass: true });
    };
    await reject('copied-byte tamper', s => { s.sources[0].content += 'tamper'; }, /source_digest_mismatch/);
    await reject('duplicate source path', s => { s.sources.push(s.sources[0]); }, /unsafe_or_duplicate_source_path/);
    await reject('path traversal', s => { s.sources[0].path = '../escape.md'; }, /unsafe_or_duplicate_source_path/);
    await reject('forged authority kind', s => { s.sources[0].kind = 'policy'; }, /invalid_source_kind/);
    await reject('oversized copied source', s => { s.sources[0].content = 'x'.repeat(256 * 1024 + 1); }, /corpus_size_limit/);
    const project = await intake.copiedCorpusProject(snapshot);
    await assert.rejects(() => intake.queryCopiedProject(project, 'delete everything'), /pilot_read_queries_only/);
    tests.push({ name: 'non-find command rejected', pass: true });
    const changed = structuredClone(snapshot);
    changed.sources[0].content += '\nSynthetic copied-source change only.\n';
    changed.sources[0].sha256 = sha(changed.sources[0].content);
    const delta = await intake.compareCorpusSnapshots(snapshot, changed);
    assert.equal(delta.filter(s => s.status === 'changed').length, 1);
    assert.equal(delta.find(s => s.status === 'changed').path, snapshot.sources[0].path);
    tests.push({ name: 'changed copy detected, originals untouched', pass: true });
    assert.equal(attempts, 0);
  } finally { await server.close(); }
  write(output, 'project.aia.json', first.archive);
  write(output, 'first-result.json', first.result);
  write(output, 'repeat-result.json', second.result);
  write(output, 'measurements.json', measurements(snapshot, tasks, first));
  write(output, 'checks.json', { tests, repeatNonTimestampAnswersIdentical: true,
    repeatProjectDigestIdentical: first.result.projectDigest === second.result.projectDigest,
    digestBoundary: 'Full project digests include generated node-version timestamps; not expected to repeat byte-for-byte.',
    unchangedSourcesInRepeat: second.result.delta.length, core: first.result.checks,
    runtime: { node: process.version, vite: version, dependencies: 'reused local node_modules; not fully pinned',
      environment: 'explicit PATH, NODE_ENV, LANG only; no inherited credentials; Vite config and env files disabled' },
    guard: { fetchAndTcpAttempts: attempts, scope: 'fetch and net.Socket.connect interception; not comprehensive OS egress containment' },
    engineRevision: lock.engineRevision });
}

function parent() {
  assert.equal(process.argv.length, 2, 'Usage: node run_pilot.mjs (fixed reviewed files; fresh temporary output)');
  const lockBytes = fs.readFileSync(path.join(here, 'source-lock.json'));
  const tasksBytes = fs.readFileSync(path.join(here, 'tasks.json'));
  const lock = JSON.parse(lockBytes), tasks = JSON.parse(tasksBytes);
  assert.equal(lock.sourceRepo, '/Users/Yves/Documents/01_EMERGENTISM');
  assert.equal(lock.engineRepo, '/Users/Yves/Documents/04_CODE/01_SKYZAI_LEVELS/L5_REFLECTION/APU');
  assert.match(lock.engineRevision, /^[a-f0-9]{40}$/);
  assert(tasks.frozenBeforeRun && tasks.tasks.length > 0 && tasks.tasks.length <= 10);
  assert.equal(new Set(tasks.tasks.map(t => t.id)).size, tasks.tasks.length);
  assert(tasks.tasks.every(t => /^[a-z]+$/.test(t.query) && t.query.length < 100));
  const sources = readSources(lock);
  const observedHead = git(lock.sourceRepo, 'rev-parse', 'HEAD').toString().trim();
  const snapshot = { kind: 'aia.copied_corpus', version: 1, scopeId: lock.scopeId,
    revision: lock.sourceRevision, capturedAt: new Date().toISOString(), sources };
  const tempRoot = fs.realpathSync(os.tmpdir());
  const output = fs.mkdtempSync(path.join(tempRoot, 'emergentism-apu-pilot-'));
  fs.chmodSync(output, 0o700);
  console.log(`Private pilot output: ${output}`);
  write(output, 'source-lock.json', lockBytes); write(output, 'tasks.json', tasksBytes);
  write(output, 'snapshot.json', snapshot);
  for (const source of sources) write(output, `sources/${source.path}`, source.content);
  const archive = git(lock.engineRepo, 'archive', '--format=tar', lock.engineRevision, 'apu.bot');
  write(output, 'engine.tar', archive);
  fs.mkdirSync(path.join(output, 'engine'), { mode: 0o700 });
  execFileSync('tar', ['-xf', path.join(output, 'engine.tar'), '-C', path.join(output, 'engine')]);
  const product = path.join(output, 'engine', 'apu.bot');
  const dependencies = fs.realpathSync(path.join(lock.engineRepo, 'apu.bot/node_modules'));
  fs.symlinkSync(dependencies, path.join(product, 'node_modules'), 'dir');
  const entryNames = ['scripts/copied_pilot_core.ts', 'src/lib/corpusIntake.ts', 'src/lib/librarian/local.ts',
    'src/lib/search.ts', 'src/lib/store.ts', 'src/lib/projectPackage.ts', 'package-lock.json'];
  const entries = () => entryNames.map(p => ({ path: p, sha256: sha(fs.readFileSync(path.join(product, p))) }));
  const before = entries();
  const custody = { sourceRevision: lock.sourceRevision, observedSourceHeadBefore: observedHead,
    engineRevision: lock.engineRevision,
    observedEngineHead: git(lock.engineRepo, 'rev-parse', 'HEAD').toString().trim(),
    engineArchiveSha256: sha(archive), engineEntries: before,
    sourceLockSha256: sha(lockBytes), tasksSha256: sha(tasksBytes), wrapperSha256: sha(fs.readFileSync(self)),
    dependencyPath: dependencies, engineWorkingTree: git(lock.engineRepo, 'status', '--porcelain').toString(),
    mutationBoundary: 'Only fresh temporary output. Originals checked before and after; no OS source-write sandbox.' };
  write(output, 'custody-before.json', custody);
  try {
    execFileSync(process.execPath, [self, '--worker', output], { cwd: output,
      env: { PATH: '/usr/bin:/bin:/usr/sbin:/sbin', NODE_ENV: 'test', LANG: 'en_US.UTF-8' },
      timeout: 120000, stdio: ['ignore', 'pipe', 'pipe'] });
    assert.deepEqual(readSources(lock), sources);
    assert.deepEqual(entries(), before);
    assert.equal(sha(fs.readFileSync(self)), custody.wrapperSha256, 'wrapper changed during run');
    assert.equal(sha(fs.readFileSync(path.join(here, 'source-lock.json'))), sha(lockBytes));
    assert.equal(sha(fs.readFileSync(path.join(here, 'tasks.json'))), sha(tasksBytes));
    const observedAfter = git(lock.sourceRepo, 'rev-parse', 'HEAD').toString().trim();
    assert.equal(observedAfter, observedHead, 'source HEAD moved during run; preserve output and review');
    write(output, 'custody-after.json', { originalsUnchangedAtCheckpoints: true, observedSourceHeadAfter: observedAfter,
      engineEntriesUnchangedAtCheckpoints: true });
    const names = ['source-lock.json', 'tasks.json', 'snapshot.json', 'project.aia.json', 'first-result.json',
      'repeat-result.json', 'measurements.json', 'checks.json', 'custody-before.json', 'custody-after.json',
      'engine.tar', ...sources.map(s => `sources/${s.path}`)];
    write(output, 'COMPLETE.json', { files: names.map(p => ({ path: p, sha256: sha(fs.readFileSync(path.join(output, p))) })) });
    console.log(JSON.stringify({ output, checks: json(path.join(output, 'checks.json')) }, null, 2));
  } catch (error) {
    write(output, 'FAILED.json', { state: 'incomplete', reason: 'Pilot failed. Inspect private output; no completion receipt emitted.' });
    throw error;
  }
}

if (process.argv[2] === '--worker') await worker(process.argv[3]);
else parent();
