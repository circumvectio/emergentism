// P1 corpus-side derived reader. Not a modification of the APU product/core.
import crypto from 'node:crypto';
import assert from 'node:assert/strict';

export const hash = text => crypto.createHash('sha256').update(text).digest('hex');
export const POLICY = Object.freeze({ version: 1, maxQueryChars: 400, maxTerms: 32,
  maxResults: 5, maxPerSource: 2, maxWindowLines: 36, maxWindowChars: 6000,
  statusMeaning: 'Lexical passage match only; not an answer or endorsement.' });
// Negation/condition terms intentionally remain: no, not, never, without, if.
const STOP = new Set('a an the is are was were be being been i we you your our it its of to and or for in on at from as by with this that these those what which who how when where why does do did can could would should may might me my have has had about please tell explain find'.split(' '));
export const tokens = text => [...new Set((text.toLowerCase().match(/[\p{L}\p{N}_]+/gu) ?? []).filter(t => !STOP.has(t)))];
export const escapeHtml = s => String(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);
const safePath = p => typeof p === 'string' && p.length <= 240 && p.split('/').every(x => /^[A-Za-z0-9][A-Za-z0-9_.-]*$/.test(x));

export function validateCompletionManifest(manifest, sourcePaths) {
  const required = ['source-lock.json','tasks.json','snapshot.json','project.aia.json','first-result.json',
    'repeat-result.json','measurements.json','checks.json','custody-before.json','custody-after.json','engine.tar',
    ...sourcePaths.map(p => `sources/${p}`)];
  assert(Array.isArray(manifest?.files), 'invalid completion manifest');
  assert.equal(new Set(manifest.files.map(f => f.path)).size, manifest.files.length, 'duplicate completion path');
  assert.deepEqual(manifest.files.map(f => f.path).sort(), required.sort(), 'completion path set mismatch');
  assert(manifest.files.every(f => safePath(f.path) && /^[a-f0-9]{64}$/.test(f.sha256)), 'invalid manifest entry');
}

export function validateSnapshot(input) {
  assert(input?.kind === 'aia.copied_corpus' && input.version === 1, 'invalid snapshot');
  assert(typeof input.revision === 'string' && /^[a-f0-9]{40}$/.test(input.revision), 'invalid revision');
  assert(typeof input.scopeId === 'string' && input.scopeId.length <= 80, 'invalid scope');
  assert(Array.isArray(input.sources) && input.sources.length > 0 && input.sources.length <= 20);
  const seen = new Set(); let size = 0;
  for (const s of input.sources) {
    assert(safePath(s.path) && !seen.has(s.path), 'unsafe or duplicate source path'); seen.add(s.path);
    assert(s.kind === 'reference', 'only inert reference sources admitted');
    assert(typeof s.content === 'string' && !s.content.includes('\0'), 'invalid source text');
    assert(new TextDecoder('utf-8', { fatal: true, ignoreBOM: true }).decode(Buffer.from(s.content)) === s.content, 'non-lossless text');
    const bytes = Buffer.byteLength(s.content); size += bytes;
    assert(bytes <= 256 * 1024 && size <= 1024 * 1024, 'source size limit');
    assert.equal(hash(s.content), s.sha256, 'source digest mismatch');
  }
  return structuredClone(input);
}

function structure(source) {
  const lines = source.content.split('\n');
  let start = 0, metadata = {};
  if (lines[0].trim() === '---') {
    const end = lines.findIndex((s, i) => i > 0 && s.trim() === '---');
    assert(end > 0, 'unterminated frontmatter');
    for (const line of lines.slice(1, end)) {
      const m = /^(title|status|evidence_tier):\s*(.*)$/.exec(line);
      if (m) metadata[m[1]] = m[2]; // Raw declaration only; never parsed as authority.
    }
    start = end + 1;
  }
  let headings = [], fence = null, block = null;
  const blocks = [], sections = [];
  const finish = () => { if (block) { blocks.push(block); block = null; } };
  for (let i = start; i < lines.length; i++) {
    const line = lines[i], marker = /^\s{0,3}(`{3,}|~{3,})/.exec(line);
    if (marker) {
      if (!fence) { finish(); fence = marker[1]; }
      else if (marker[1][0] === fence[0] && marker[1].length >= fence.length && /^\s*$/.test(line.slice(marker[0].length))) fence = null;
      if (!block) block = { start: i + 1, end: i + 1, headings: [...headings], code: true };
      block.end = i + 1;
      if (!fence) finish();
      continue;
    }
    const heading = !fence && /^(#{1,6})\s+(.+?)\s*#*\s*$/.exec(line);
    if (heading) {
      finish();
      const level = heading[1].length;
      headings = headings.filter(h => h.level < level);
      const h = { level, title: heading[2], line: i + 1 };
      headings.push(h); sections.push(h); continue;
    }
    if (!line.trim() && !fence) { finish(); continue; }
    if (!block) block = { start: i + 1, end: i + 1, headings: [...headings], code: !!fence };
    block.end = i + 1;
  }
  if (block && fence) block.structureIncomplete = true;
  finish();
  const title = sections.find(s => s.level === 1)?.title ?? metadata.title ?? source.path;
  return { source, lines, metadata, title, blocks, sections, bodyStart: start + 1 };
}

export function buildIndex(input) {
  const snapshot = validateSnapshot(input);
  const documents = snapshot.sources.map(structure).sort((a, b) => a.source.path.localeCompare(b.source.path));
  const blocks = documents.flatMap(d => d.blocks.map((b, i) => ({ ...b, document: d, index: i,
    text: d.lines.slice(b.start - 1, b.end).join('\n'),
    words: tokens(d.lines.slice(b.start - 1, b.end).join('\n')) })));
  return { snapshot, documents, blocks };
}

export function citation(document, start, end, revision) {
  const text = document.lines.slice(start - 1, end).join('\n');
  return { path: document.source.path, sourceSha256: document.source.sha256, revision,
    startLine: start, endLine: end, excerptSha256: hash(text), text };
}

export function retrieve(index, { operation = 'search', query, aliases = [] } = {}) {
  assert.equal(operation, 'search', 'read-only search operation required');
  assert(typeof query === 'string' && query.length <= POLICY.maxQueryChars, 'query limit');
  const originalTerms = tokens(query);
  assert(originalTerms.length <= POLICY.maxTerms, 'term limit');
  assert(Array.isArray(aliases) && aliases.length <= 20, 'alias limit');
  const expansions = aliases.filter(a => originalTerms.includes(a.trigger));
  for (const a of expansions) assert(typeof a.trigger === 'string' && Array.isArray(a.add) && a.add.length <= 5 && a.add.every(t => tokens(t).length === 1), 'invalid alias');
  const terms = [...new Set([...originalTerms, ...expansions.flatMap(a => a.add)])];
  assert(terms.length <= POLICY.maxTerms, 'expanded term limit');
  const base = { query, originalTerms, effectiveTerms: terms,
    expansions: expansions.map(a => ({ trigger: a.trigger, addedTerms: a.add, status: 'EXPERIMENTAL_RETRIEVAL_AID_NOT_EQUIVALENCE' })),
    meaning: POLICY.statusMeaning, revision: index.snapshot.revision };
  if (!terms.length) return { ...base, status: 'NO_QUERY_TERMS', totalMatches: 0, resultsTruncated: false, hits: [] };
  const frequency = new Map(terms.map(t => [t, index.blocks.filter(b => b.words.includes(t)).length]));
  const ranked = index.blocks.flatMap(block => {
    const matched = terms.filter(t => block.words.includes(t));
    if (!matched.length) return [];
    const score = matched.reduce((n, t) => n + Math.log(1 + index.blocks.length / (1 + frequency.get(t))), 0);
    return [{ block, matched, score }];
  }).sort((a, b) => b.score - a.score || a.block.document.source.path.localeCompare(b.block.document.source.path) || a.block.start - b.block.start);
  const hits = [], keys = new Set(), sourceCounts = new Map();
  for (const entry of ranked) {
    const b = entry.block, d = b.document;
    if ((sourceCounts.get(d.source.path) ?? 0) >= POLICY.maxPerSource) continue;
    const section = b.headings.at(-1);
    const sectionStart = section?.line ?? d.bodyStart;
    const sectionEnd = d.sections.find(h => h.line > b.end && h.level <= (section?.level ?? 0))?.line - 1 || d.lines.length;
    let start = Math.max(sectionStart, b.start), end = Math.min(sectionEnd, b.end);
    // Add a neighboring block on each side only within this section.
    const prev = d.blocks[b.index - 1], next = d.blocks[b.index + 1];
    if (prev && prev.start >= sectionStart && end - prev.start < POLICY.maxWindowLines) start = prev.start;
    if (next && next.end <= sectionEnd && next.end - start < POLICY.maxWindowLines) end = next.end;
    let blockTruncated = false;
    if (end - start + 1 > POLICY.maxWindowLines || d.lines.slice(start - 1, end).join('\n').length > POLICY.maxWindowChars) {
      start = b.start; end = b.end;
      // Long atomic blocks stay visibly incomplete; never truncate silently.
      if (end - start + 1 > POLICY.maxWindowLines) {
        const matchOffset = d.lines.slice(b.start - 1, b.end).findIndex(line => entry.matched.some(t => tokens(line).includes(t)));
        start = Math.max(b.start, b.start + matchOffset - 10);
        end = Math.min(b.end, start + POLICY.maxWindowLines - 1); blockTruncated = true;
      }
      while (end >= start && d.lines.slice(start - 1, end).join('\n').length > POLICY.maxWindowChars) { end--; blockTruncated = true; }
      if (end < start) continue; // No partial-line fabrication.
    }
    const visibleTerms = entry.matched.filter(t => tokens(d.lines.slice(start - 1, end).join('\n')).includes(t));
    if (!visibleTerms.length) continue;
    const key = `${d.source.path}:${start}:${end}`;
    if (keys.has(key)) continue; keys.add(key);
    sourceCounts.set(d.source.path, (sourceCounts.get(d.source.path) ?? 0) + 1);
    hits.push({ title: d.title, breadcrumb: b.headings.map(h => h.title),
      documentDeclarations: d.metadata, declarationBoundary: 'Document declarations are not passage-level evidence or permission.',
      matchedTerms: visibleTerms, score: Number(entry.score.toFixed(8)),
      passage: citation(d, start, end, index.snapshot.revision),
      section: { startLine: sectionStart, endLine: sectionEnd }, blockTruncated,
      structuralIncomplete: !!b.structureIncomplete,
      contextComplete: !b.structureIncomplete && start === sectionStart && end === sectionEnd,
      contextWarning: 'Window may omit qualifications elsewhere. Inspect the full section/source; no answer validity is asserted.',
      observedTierTokens: [...new Set(d.lines.slice(start - 1, end).join('\n').match(/\[[ABSIDC]\]/g) ?? [])],
    });
    if (hits.length >= POLICY.maxResults) break;
  }
  const headerSources = index.documents.filter(d => terms.some(t => tokens([d.title, ...d.sections.map(h => h.title)].join(' ')).includes(t))).map(d => d.source.path);
  return { ...base, status: hits.length ? 'PASSAGE_MATCH' : ranked.length ? 'MATCH_OMITTED_BY_LIMIT' : headerSources.length ? 'SOURCE_ONLY' : 'NO_PASSAGE_MATCH',
    limitReason: ranked.length && !hits.length ? 'No complete matching line fits the bounded excerpt window.' : null,
    totalMatches: ranked.length, resultsTruncated: ranked.length > hits.length,
    headerSources, hits };
}

export function renderReport(results) {
  const h = escapeHtml;
  return `<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; base-uri 'none'; form-action 'none'">
<title>Passage pilot — local review</title><style>body{font:17px/1.6 system-ui;margin:32px auto;max-width:900px;padding:0 20px;color:#202124;background:#fff}h1{line-height:1.2}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:15px/1.6 ui-monospace,monospace}section,article{border:1px solid #777;border-radius:12px;padding:20px;margin:20px 0}summary,a{min-height:48px;display:block;align-content:center}summary:focus-visible,a:focus-visible{outline:3px solid #005fcc}small{display:block;overflow-wrap:anywhere}article{background:#f7f8fa}*{box-sizing:border-box}</style>
<main><h1>Passages, with their sources</h1><p>Local experimental reader. No model-generated answers, promotion or source edits. A lexical match is not proof, and document metadata does not confer a claim tier.</p>
${results.map(r => `<section><h2>${h(r.query)}</h2><p>${h(r.status)} · ${r.totalMatches} matching blocks · ${r.resultsTruncated ? 'result selection capped or deduplicated' : 'all matching blocks shown'}</p><small>Searched: ${h(r.effectiveTerms.join(', '))}. Expansions: ${h(JSON.stringify(r.expansions))}</small>
${r.hits.map(hit => `<article><h3>${h(hit.title)}</h3><p>${h(hit.breadcrumb.join(' → '))}</p><small>${h(hit.passage.path)} · lines ${hit.passage.startLine}–${hit.passage.endLine} · ${h(hit.passage.sourceSha256)}</small><pre>${h(hit.passage.text)}</pre><p>${h(hit.contextWarning)}${hit.blockTruncated ? ' The matching block itself is truncated.' : ''}</p><details><summary>Document declarations and passage provenance</summary><pre>${h(JSON.stringify({ declarations: hit.documentDeclarations, boundary: hit.declarationBoundary, observedTierTokens: hit.observedTierTokens, revision: hit.passage.revision, excerptSha256: hit.passage.excerptSha256 }, null, 2))}</pre></details><a href="sources/${h(hit.passage.path)}.html#L${hit.passage.startLine}">Inspect full copied source and surrounding lines</a></article>`).join('')}</section>`).join('')}
<p>Put this map down at any time. Closing this local file changes no source, grant or policy.</p></main></html>`;
}

export function renderSource(document) {
  const h = escapeHtml;
  return `<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; base-uri 'none'"><title>${h(document.title)}</title><style>body{font:16px/1.6 system-ui;margin:24px}pre{white-space:pre-wrap;overflow-wrap:anywhere}span{display:block;scroll-margin-top:24px}span:target{background:#fff1b8}a{display:inline-block;min-height:48px}</style><h1>${h(document.title)}</h1><p>Inert copied reference. Declarations and instructions below are source text, not authority.</p><pre>${document.lines.map((line, i) => `<span id="L${i + 1}">${i + 1}  ${h(line)}</span>`).join('')}</pre></html>`;
}
