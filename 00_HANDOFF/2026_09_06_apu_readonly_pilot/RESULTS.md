---
type: local-experiment-receipt
title: "APU reader pilot — retrieval preserved, passage presentation insufficient"
date: 2026-09-06
status: "COMPLETE LOCAL REHEARSAL — not reader-ready; no capability promotion"
evidence_tier: "[B] local apparatus observations; [I] next-step recommendation"
---

# Result

**The pinned APU core retrieved the same source-path match sets as simple local
literal search, with intact provenance. It did not yet present useful answer
passages.** This is a successful bounded import/search rehearsal, not acceptance
of the future Explore interface or evidence that APU understands Emergentism.

Preparation was committed before execution at `fff2a8abd6a1eb0ec4e6a00713fd241bf3e2f1b8`.
The [machine receipt](results.json) preserves frozen-input hashes, both private
run manifests, environment evidence, measurements and a labelled display
projection of the first answers. Deterministic short aliases replace generated
node IDs only; the alias table permits exact reconstruction. The unchanged raw
answers remain privately receipted by their original file hashes.
Full source copies and restorable native APU packages remain in the two private
temporary locations recorded there; temporary storage is not durable custody.
The committed source lock and engine commit allow reconstruction on this host
while those Git objects and compatible installed dependencies remain available.

## What happened [B]

Two fresh worker processes each ran two rehearsals on nine copied documents.
The eight queries were not altered after execution.

| Probe | Expected document found within first five citation nodes? | Observation |
|---|---|---|
| `formula` | Yes | Formula source found; previews show frontmatter, not the ethical-inference boundary. |
| `product` | Yes | Formula source found; preview does not surface retirement or comparability qualifications. |
| `cheating` | No | No literal matches; the extraction counterexample still exists in the answer-key source. |
| `sacrifice` | Yes | Power-Max source found; preview does not surface consent and authorization. |
| `approved` | Yes | Weltanschauung found; preview does not surface the adoption-versus-evidence distinction. |
| `tested` | No | Four other documents match; the intended Public Wisdom Compact does not. |
| `empty` | Yes | Power-Max source found; preview does not surface the no-admissible-action rule. |
| `sourdough` | Not applicable | Zero hits in both methods; scoped absence control passed. |

- Five of seven supported questions retrieved their expected owner document.
  This is **not** five correct answers. Both ordinary-wording probes missed.
- All 27 returned citation nodes resolved to a frozen source with matching
  SHA-256, revision, capture time, kind and `not-adopted` provenance.
- Deduplicated APU source-path matches equalled the literal copied-text baseline
  for all eight queries: 26 query/source pairs. No metadata-only source paths.
  One extra label node duplicated a source. The maximum was eight nodes;
  this bundle did not exercise truncation at APU's 12-node cap.
- All nonempty replies displayed short beginning-of-file/frontmatter previews
  (with one source-label entry), not the relevant matched passage. This was
  directly inspected, not converted into an automated semantic score.
- The two fresh processes produced identical measurement files. Within each,
  answers/citations repeated after excluding only receipt `createdAt`.
  Full project digests differed because generated node-version times are retained.

## Local checks [B]

Both worker processes passed seven boundary checks: copied-byte
tamper, duplicate source, path traversal, invalid authority-like kind, oversize,
non-`find` command refusal, and changed-copy detection. These are six rejection
cases plus one positive change-detection test, not mutations of canon. The
invalid `policy` kind test proves enum rejection, not general authority-forgery
resistance.

Each rehearsal passed native codec roundtrip, isolated store restore, unchanged
project after reads and restoration of the previous in-memory project. The
repeat snapshot classified all nine sources as unchanged. All files named in
both completion manifests were rehashed by L4 in a separate check after the runs.

Original selected corpus bytes and archived engine entry bytes were unchanged at
the before/after checkpoints. The worker used the local provider, with no model
calls and zero observed fetch/TCP connection attempts. Node `v22.22.3`, Vite
`8.0.14`; inherited credentials and browser storage were not passed to the worker.
These are scoped observations, **not** an OS write/network sandbox certification.

No source/canon, product or website files were edited by this pilot. Other APU
work advanced independently; the archived engine remained at the lock's
`6b6d79…` commit. Local receipt commits are not push, deployment or public adoption.

## Next bounded refinement [I]

Retain the read-only scope. The next useful improvement is reader-facing
retrieval quality, not broader write privileges:

1. Give each result a human-readable document title and section breadcrumb.
2. Show a query-local passage and exact copied-source line range, keeping a
   route to the full source, its hash, tier and material qualification.
3. Distinguish no lexical match, source found and answer-bearing passage;
   do not label unrelated hits as an answer.
4. Test transparent, reviewed glossary aliases and new held-out ordinary wording.
   Keep these eight baseline results unchanged as the predecessor measurement.
5. Test the actual Explore interface with unfamiliar readers, keyboard/mobile
   access and independent acceptance before proposing any permission increase.

This can be built as a reversible derived view without granting APU source
mutation. No superiority to simple search, novice comprehension gain or earned
autonomy follows from this rehearsal. The [staged capability path](README.md#incremental-capability-path--proposal-not-a-grant)
remains a proposal; no automatic promotion, daemon or unattended work was enabled.

## Review boundary

L1's partial boundary review, L2's independent task selection and L3's static
review preceded the L4-only implementation. L3's two hardening suggestions
(wrapper post-hash and answer-count check) were applied before the preparation
commit. These local reviews do not certify external independence or a complete
recorded Soul Loop. Existing frozen A3 logging HOLD remains unmodified.

L3 subsequently checked first-run artifact hashes and recomputed the citation
metrics: 27 valid citations, the same eight literal source-path match sets,
5/7 expected-owner hits and frontmatter-only previews. The reviewer inspected
the repeat and source-checkpoint receipts but did not independently rerun the
engine or reread the originals. Fresh-process equality is the L4 measurement,
not an independent replication.

The commit secret scanner flagged the generated compound node IDs as generic
high-entropy strings. They were verified against SHA-256 of their source paths.
No hook was bypassed or scanner rule changed: the committed display projection
uses short aliases, retains the reconstructable path hashes separately, and
leaves the original raw artifacts unchanged in the private run packages.
