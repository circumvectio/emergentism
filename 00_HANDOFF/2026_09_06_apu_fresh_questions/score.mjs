#!/usr/bin/env node
// Required-span retrieval accounting only; no semantic answer grader.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
import { fileURLToPath } from 'node:url';
import { here, verifyFreeze } from './trial.mjs';
const sha = value => crypto.createHash('sha256').update(value).digest('hex');
const json = p => JSON.parse(fs.readFileSync(p, 'utf8'));
export function covered(span, passages) {
  const relevant = passages.filter(p => p.path === span.path);
  for (let i = span.startLine; i <= span.endLine; i++)
    if (!relevant.some(p => p.startLine <= i && p.endLine >= i)) return false;
  return true;
}
export function lineCount(passages) {
  const lines = new Set();
  for (const p of passages) for (let i = p.startLine; i <= p.endLine; i++) lines.add(`${p.path}:${i}`);
  return lines.size;
}
export function verifyCitation(p, snapshot) {
  const source = snapshot.sources.find(s => s.path === p.path); assert(source, 'unknown citation source');
  assert.equal(p.sourceSha256, source.sha256); assert.equal(sha(source.content), source.sha256);
  assert.equal(p.revision, snapshot.revision);
  const lines = source.content.split('\n');
  assert(Number.isInteger(p.startLine) && Number.isInteger(p.endLine));
  assert(p.startLine >= 1 && p.endLine >= p.startLine && p.endLine <= lines.length);
  const text = lines.slice(p.startLine - 1, p.endLine).join('\n');
  assert.equal(p.text, text); assert.equal(p.excerptSha256, sha(text));
}
export function measure(q, passages) {
  const partResults = q.requiredParts.map(part => ({ id: part.id, qualification: part.qualification,
    covered: part.alternatives.some(s => covered(s, passages)) }));
  return { candidates: passages.length, uniqueLines: lineCount(passages), partResults,
    coveredParts: partResults.filter(p => p.covered).length,
    coveredQualifications: partResults.filter(p => p.qualification && p.covered).length,
    allParts: q.expected === 'supported' ? partResults.every(p => p.covered) : null,
    emptyOnUnsupported: q.expected === 'unsupported' ? passages.length === 0 : null,
    passages: passages.map(({ text, ...metadata }) => metadata) };
}
function run() {
  const freeze = json(path.join(here, 'freeze.json')); verifyFreeze(freeze);
  const root = path.join(freeze.root, 'run');
  const complete = json(path.join(root, 'COMPLETE.json'));
  for (const f of complete.files) assert.equal(sha(fs.readFileSync(path.join(root, f.path))), f.sha256);
  const manifestBytes = fs.readFileSync(path.join(root, 'case-freeze.json'));
  assert.equal(sha(manifestBytes), complete.caseManifestSha256);
  const manifest = JSON.parse(manifestBytes);
  assert.equal(sha(fs.readFileSync(path.join(here, 'freeze.json'))), manifest.freezeSha256);
  for (const input of manifest.files) assert.equal(sha(fs.readFileSync(path.join(root, input.path))), input.sha256);
  const questions = json(path.join(root, 'questions.json')).questions;
  const snapshot = json(path.join(freeze.root, 'snapshot.json'));
  assert.equal(questions.length, 10); assert.equal(questions.filter(q => q.expected === 'supported').length, 7);
  assert.equal(new Set(questions.map(q => q.id)).size, 10);
  for (const q of questions) {
    assert(['supported', 'unsupported'].includes(q.expected));
    assert(q.question.length <= 260);
    if (q.expected === 'unsupported') { assert.equal(q.requiredParts.length, 0); assert(q.absenceRationale); continue; }
    assert(q.requiredParts.length > 0 && q.requiredParts.length <= 4);
    assert(q.requiredParts.some(p => p.qualification));
    assert.equal(new Set(q.requiredParts.map(p => p.id)).size, q.requiredParts.length);
    for (const p of q.requiredParts) { assert.equal(typeof p.qualification, 'boolean'); assert(p.alternatives.length);
      for (const a of p.alternatives) { const s = snapshot.sources.find(s => s.path === a.path); assert(s);
        assert(Number.isInteger(a.startLine) && Number.isInteger(a.endLine) && a.startLine >= 1 && a.endLine >= a.startLine && a.endLine <= s.content.split('\n').length); }
    }
  }
  const result = json(path.join(root, 'first.json'));
  const search = json(path.join(root, 'baseline.json'));
  assert.equal(result.receipt.networkAttemptsObserved, 0); assert.equal(result.receipt.providerCalls, 0);
  assert.equal(result.receipt.sourceWrites, 0); assert.deepEqual(result.report.actions, []);
  assert.equal(result.receipt.reportSha256, sha(JSON.stringify(result.report)));
  assert.equal(result.receipt.navigationSha256, sha(JSON.stringify(result.navigation)));
  assert.equal(result.receipt.inputHashes[0].sha256, freeze.snapshotSha256);
  assert.equal(result.receipt.inputHashes[1].sha256, sha(fs.readFileSync(path.join(root, 'request.json'))));
  assert.equal(result.report.results.length, 10); assert.equal(result.navigation.results.length, 10); assert.equal(search.length, 10);
  let citationsChecked = 0;
  const records = questions.map((q, i) => {
    const r = result.report.results[i], nav = result.navigation.results[i], b = search[i];
    assert.equal(r.id, q.id); assert.equal(nav.id, q.id); assert.equal(b.id, q.id); assert.equal(r.question, q.question);
    const original = r.original.hits.map(h => h.passage);
    const rephrase = r.facets.flatMap(f => f.result.hits.map(h => h.passage));
    const originalNavigation = nav.original.candidates.map(c => c.citation);
    const rephraseNavigation = nav.facets.flatMap(f => f.result.candidates.map(c => c.citation));
    const assisted = [...original, ...rephrase, ...originalNavigation, ...rephraseNavigation];
    for (const p of [...assisted, ...b.passages]) { verifyCitation(p, snapshot); citationsChecked++; }
    return { id: q.id, question: q.question, expected: q.expected,
      requiredParts: q.requiredParts.length, qualificationParts: q.requiredParts.filter(p => p.qualification).length,
      status: { original: r.original.status, rephrase: r.facets.map(f => f.result.status),
        originalNavigation: nav.original.status, rephraseNavigation: nav.facets.map(f => f.result.status) },
      channels: { original: original.length, rephrase: rephrase.length, originalNavigation: originalNavigation.length, rephraseNavigation: rephraseNavigation.length },
      arms: { original: measure(q, original), assisted: measure(q, assisted), ordinarySearch: measure(q, b.passages) } };
  });
  const summary = Object.fromEntries(['original', 'assisted', 'ordinarySearch'].map(arm => [arm, {
    supportedQuestionsAllPartsCovered: records.filter(r => r.arms[arm].allParts === true).length,
    supportedQuestionDenominator: 7,
    requiredPartsCovered: records.reduce((n, r) => n + r.arms[arm].coveredParts, 0),
    requiredPartsDenominator: records.reduce((n, r) => n + r.requiredParts, 0),
    qualificationPartsCovered: records.reduce((n, r) => n + r.arms[arm].coveredQualifications, 0),
    qualificationPartsDenominator: records.reduce((n, r) => n + r.qualificationParts, 0),
    unsupportedEmpty: records.filter(r => r.arms[arm].emptyOnUnsupported === true).length,
    unsupportedDenominator: 3,
    returnedUniqueLinesSummedAcrossQuestions: records.reduce((n, r) => n + r.arms[arm].uniqueLines, 0),
  }]));
  const output = { kind: 'local_required_span_diagnostics', version: 1, summary, citationsChecked, records,
    protocolCommit: manifest.protocolCommit, casesCommit: manifest.inputsCommit,
    caseManifestSha256: complete.caseManifestSha256, engineRevision: freeze.engineRevision, sourceRevision: freeze.sourceRevision,
    rawRunPath: root, rawManifest: complete, independentHumanReview: false,
    limits: ['Not semantic answer accuracy', 'Unequal text budgets and AI query assistance', 'Source-informed AI question author',
      'Exact-span key is one selected warrant, not exhaustive equivalent evidence', 'No permission or publication promotion'] };
  const bytes = JSON.stringify(output, null, 2) + '\n';
  const target = path.join(here, 'results.json');
  if (process.argv.includes('--check')) assert.equal(fs.readFileSync(target, 'utf8'), bytes);
  else fs.writeFileSync(target, bytes, { flag: 'wx', mode: 0o600 });
  console.log(JSON.stringify({ summary, citationsChecked }, null, 2));
}
if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) run();
