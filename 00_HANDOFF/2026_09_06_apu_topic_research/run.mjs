#!/usr/bin/env node
// Bounded successor experiment. Source copies and engine are data in a local archive.
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import crypto from 'node:crypto';
import zlib from 'node:zlib';
import assert from 'node:assert/strict';
import { execFileSync, spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
const here=path.dirname(fileURLToPath(import.meta.url)), repo=path.resolve(here,'../..');
const apu='/Users/Yves/Documents/04_CODE/01_SKYZAI_LEVELS/L5_REFLECTION/APU';
const prior=path.join(here,'../2026_09_06_apu_fresh_questions');
const paths=['scripts/inspect_library.mjs','src/lib/libraryFacets.ts','src/lib/libraryInvestigation.ts','src/lib/corpusPassages.ts','src/lib/libraryResearch.ts'];
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const read=p=>fs.readFileSync(p);
const json=p=>JSON.parse(read(p));
const git=(cwd,...args)=>execFileSync('git',['-C',cwd,...args],{maxBuffer:4*1024*1024});
const write=(p,b)=>fs.writeFileSync(p,b,{flag:'wx',mode:0o600});
const encode=entries=>zlib.gzipSync(JSON.stringify({version:1,entries:[...entries].map(([path,b])=>({path,sha256:sha(b),base64:b.toString('base64')}))}),{level:9});
function decode(bytes) {
  const payload=JSON.parse(zlib.gunzipSync(bytes,{maxOutputLength:12*1024*1024}));
  assert.equal(payload.version,1); const entries=new Map();
  for(const e of payload.entries){assert(!path.isAbsolute(e.path)&&!e.path.split('/').includes('..')&&!entries.has(e.path));const b=Buffer.from(e.base64,'base64');assert.equal(sha(b),e.sha256);entries.set(e.path,b);}
  return entries;
}
function priorEntries(){const b=read(path.join(prior,'evidence.json.gz'));assert.equal(sha(b),'2791b7dd298c41dfb70a532b3e8df1e4f809b21c1b175b4661291c45713941ff');return decode(b);} // Archive SHA-256, not a secret. # pragma: allow-secret
function frozenInput(freeze){
  assert.deepEqual(freeze.engine.map(e=>e.path),paths);
  const captured=new Map();
  for(const {path:p,sha256:digest} of freeze.files){const bytes=read(path.join(here,p));assert.equal(sha(bytes),digest,`changed ${p}`);captured.set(p,bytes);}
  const questionBytes=read(path.join(prior,'questions.json'));
  assert.equal(sha(questionBytes),freeze.predecessorQuestionsSha256);
  const entries=new Map();
  for(const e of freeze.engine){const bytes=git(apu,'show',`${freeze.engineCommit}:apu.bot/${e.path}`);assert.equal(sha(bytes),e.sha256);entries.set(`engine/apu.bot/${e.path}`,bytes);}
  const old=priorEntries();
  assert(questionBytes.equals(old.get('run/questions.json')),'predecessor key differs from pinned evidence');
  entries.set('development-snapshot.json',old.get('snapshot.json'));
  entries.set('legacy-request.json',old.get('run/request.json'));
  entries.set('legacy-first.json',old.get('run/first.json'));
  const cases=JSON.parse(captured.get('cases.json')), oldQuestions=JSON.parse(questionBytes).questions;
  const topic=(query)=>({id:'topic',query,proposedBy:'reviewer',basis:'source-informed',rationale:'Explicit source-informed topic selection, not an automatic rewrite or evidence claim.'});
  const freshSnapshot={kind:'aia.copied_corpus',version:1,scopeId:'fresh-synthetic-research',revision:'synthetic-v1',capturedAt:'2026-09-06T00:00:00Z',sources:cases.fresh.map(c=>({path:c.path,kind:'reference',content:c.content,sha256:sha(c.content)}))};
  const freshRequest={version:1,questions:cases.fresh.map(c=>({id:c.id,question:c.question,topicQueries:[topic(c.topic)],evidenceRequirements:c.requirements.map((text,i)=>({id:`R${i+1}`,text}))}))};
  const development={version:1,questions:cases.development.map(c=>{const q=oldQuestions.find(q=>q.id===c.id);assert(q);return{id:q.id,question:q.question,topicQueries:[topic(c.topic)],evidenceRequirements:q.requiredParts.map(p=>({id:p.id,text:p.description}))};})};
  entries.set('fresh-snapshot.json',Buffer.from(JSON.stringify(freshSnapshot)));
  entries.set('fresh-request.json',Buffer.from(JSON.stringify(freshRequest)));
  entries.set('development-request.json',Buffer.from(JSON.stringify(development)));
  entries.set('cases.json',captured.get('cases.json'));
  entries.set('questions.json',questionBytes);
  return entries;
}
function execute(entries){
  const dir=fs.realpathSync(fs.mkdtempSync(path.join(os.tmpdir(),'apu-topic-research-')));
  for(const [p,b] of entries){const target=path.join(dir,p);fs.mkdirSync(path.dirname(target),{recursive:true,mode:0o700});write(target,b);}
  const calls=[['fresh','fresh-snapshot.json','fresh-request.json','--research'],['development','development-snapshot.json','development-request.json','--research'],['legacy','development-snapshot.json','legacy-request.json'],['legacy-browse','development-snapshot.json','legacy-request.json','--browse']];
  const outputs=new Map();
  try {
  for(const [name,s,q,flag] of calls){
    const args=['--experimental-strip-types',path.join(dir,'engine/apu.bot/scripts/inspect_library.mjs'),path.join(dir,s),path.join(dir,q),...(flag?[flag]:[])];
    const opts={cwd:dir,env:{PATH:path.dirname(process.execPath),LANG:'C.UTF-8',NODE_ENV:'test'},timeout:60000,maxBuffer:4*1024*1024};
    const a=spawnSync(process.execPath,args,opts), b=spawnSync(process.execPath,args,opts);
    outputs.set(`${name}.json`,a.stdout); outputs.set(`${name}.stderr`,a.stderr);
    outputs.set(`${name}-repeat.json`,b.stdout); outputs.set(`${name}-repeat.stderr`,b.stderr);
    outputs.set(`${name}-process.json`,Buffer.from(JSON.stringify({firstStatus:a.status,repeatStatus:b.status,firstSignal:a.signal,repeatSignal:b.signal})));
    assert.equal(a.status,0,`${name}: ${a.stderr}`);assert.equal(b.status,0,`${name} repeat: ${b.stderr}`);assert(a.stdout.equals(b.stdout));
    const r=JSON.parse(a.stdout).receipt;
    assert.equal(r.providerCalls,0);assert.equal(r.sourceWrites,0);assert.equal(r.networkAttemptsObserved,0);
    assert.equal(r.reportSha256,sha(JSON.stringify(JSON.parse(a.stdout).report)));
  }
  for(const [p,b] of entries)assert.equal(sha(read(path.join(dir,p))),sha(b),`changed ${p}`);
  return outputs;
  } catch(error) {error.outputs=outputs;throw error;}
}
function summarize(entries,outputs){
  const parse=p=>JSON.parse(entries.get(p)), output=p=>JSON.parse(outputs.get(p));
  const old= parse('legacy-first.json');
  assert.deepEqual(output('legacy.json').report,old.report);
  assert.deepEqual(output('legacy-browse.json').report,old.report);
  assert.deepEqual(output('legacy-browse.json').navigation,old.navigation);
  let verified=0, requirements=0;
  const metrics=(name, key)=>{
    const snapshot=parse(`${name}-snapshot.json`), request=parse(`${name}-request.json`), report=output(`${name}.json`).report;
    return report.results.map((r,i)=>{
      assert.equal(r.id,request.questions[i].id);
      assert.deepEqual(r.evidenceRequirements,request.questions[i].evidenceRequirements.map(e=>({...e,status:'NOT_ASSESSED'})));requirements+=r.evidenceRequirements.length;
      const original=r.original.hits.map(h=>h.passage);
      const topics=r.topics.flatMap(t=>[...t.result.hits.map(h=>h.passage),...t.navigation.candidates.map(c=>c.citation)]);
      for(const c of [...original,...topics]){const s=snapshot.sources.find(s=>s.path===c.path);assert(s);assert.equal(c.sourceSha256,s.sha256);assert.equal(c.revision,snapshot.revision);assert.equal(c.text,s.content.split('\n').slice(c.startLine-1,c.endLine).join('\n'));assert.equal(c.excerptSha256,sha(c.text));verified++;}
      const arm=passages=>{const lines=new Set(passages.flatMap(p=>Array.from({length:p.endLine-p.startLine+1},(_,j)=>`${p.path}:${p.startLine+j}`)));const k=key(r.id);return{neededParts:k.length,partsReturned:k.filter(alts=>alts.some(span=>Array.from({length:span.endLine-span.startLine+1},(_,j)=>`${span.path}:${span.startLine+j}`).every(l=>lines.has(l)))).length,uniqueLines:lines.size,passages:passages.map(p=>({path:p.path,startLine:p.startLine,endLine:p.endLine}))};};
      if(name==='development')assert.deepEqual(r.original,old.report.results.find(q=>q.id===r.id).original);
      const control=name==='fresh'&&parse('cases.json').fresh.find(c=>c.id===r.id)?.expectedMiss
        ? {expected:'NO_CANDIDATES',originalPass:original.length===0,assistedPass:original.length+topics.length===0} : null;
      return{id:r.id,originalStatus:r.original.status,original:arm(original),assisted:arm([...original,...topics]),control,requirements:r.evidenceRequirements};
    });
  };
  const cases=parse('cases.json'), priorQuestions=parse('questions.json').questions;
  const fresh=metrics('fresh',id=>{const c=cases.fresh.find(c=>c.id===id);return c.neededLines.map(line=>[{path:c.path,startLine:line,endLine:line}]);});
  const development=metrics('development',id=>priorQuestions.find(q=>q.id===id).requiredParts.map(p=>p.alternatives));
  return{kind:'apu_topic_research_local_diagnostics',version:1,fresh,development,legacyReportAndNavigationUnchanged:true,requirementsPreservedNotAssessed:requirements,verifiedPassageInstances:verified,repeatByteIdentical:true,providerCalls:0,sourceWrites:0,limits:cases.scoring,authorship:cases.authorship};
}
const mode=process.argv[2];
if(mode==='freeze'){
  const ref=process.argv[3];assert(/^[0-9a-f]{40}$/.test(ref||''));
  for(const p of ['cases.json','run.mjs'])assert(git(repo,'show',`HEAD:${path.relative(repo,path.join(here,p))}`).equals(read(path.join(here,p))),`commit ${p} first`);
  const freeze={version:1,engineCommit:ref,inputCommit:String(git(repo,'rev-parse','HEAD')).trim(),nodeVersion:process.version,files:['cases.json','run.mjs'].map(p=>({path:p,sha256:sha(read(path.join(here,p)))})),predecessorQuestionsSha256:sha(read(path.join(prior,'questions.json'))),engine:paths.map(p=>({path:p,sha256:sha(git(apu,'show',`${ref}:apu.bot/${p}`))}))};
  write(path.join(here,'freeze.json'),JSON.stringify(freeze,null,2)+'\n');console.log('Frozen; commit freeze.json before run.');
}else if(mode==='run'){
  const freezeBytes=read(path.join(here,'freeze.json')),freeze=JSON.parse(freezeBytes);assert.equal(process.version,freeze.nodeVersion);
  assert(git(repo,'show',`HEAD:${path.relative(repo,path.join(here,'freeze.json'))}`).equals(freezeBytes),'commit freeze first');
  const entries=frozenInput(freeze);
  write(path.join(here,'attempt.json'),JSON.stringify({engineCommit:freeze.engineCommit,freezeSha256:sha(freezeBytes),nodeVersion:process.version})+'\n');
  let outputs,summary;
  try { outputs=execute(entries);summary=summarize(entries,outputs);
    assert(freezeBytes.equals(read(path.join(here,'freeze.json'))),'freeze changed');
    for(const {path:p,sha256:digest} of freeze.files)assert.equal(sha(read(path.join(here,p))),digest,`changed ${p}`);
    assert.equal(sha(read(path.join(prior,'questions.json'))),freeze.predecessorQuestionsSha256);
  }
  catch(error){write(path.join(here,'failed-evidence.json.gz'),encode(new Map([...entries,...[...(error.outputs||outputs||new Map())].map(([p,b])=>[`output/${p}`,b])])));throw error;}
  const archive=encode(new Map([...entries,...[...outputs].map(([p,b])=>[`output/${p}`,b])]));
  write(path.join(here,'evidence.json.gz'),archive);
  write(path.join(here,'results.json'),JSON.stringify({...summary,engineCommit:freeze.engineCommit,freezeCommit:String(git(repo,'rev-parse','HEAD')).trim(),archiveSha256:sha(archive)},null,2)+'\n');
  console.log(JSON.stringify(summary,null,2));
}else if(mode==='--check'){
  const recorded=json(path.join(here,'results.json')),bytes=read(path.join(here,'evidence.json.gz'));assert.equal(sha(bytes),recorded.archiveSha256);
  const all=decode(bytes),entries=new Map([...all].filter(([p])=>!p.startsWith('output/'))),outputs=execute(entries);
  for(const [p,b] of outputs)assert(b.equals(all.get(`output/${p}`)),`replay differs ${p}`);
  const {engineCommit,freezeCommit,archiveSha256,...summary}=recorded;
  assert.deepEqual(summarize(entries,outputs),summary);console.log(JSON.stringify({replayByteIdentical:true,engineCommit,freezeCommit,archiveSha256}));
}else throw Error('usage: run.mjs freeze ENGINE_COMMIT | run | --check');
