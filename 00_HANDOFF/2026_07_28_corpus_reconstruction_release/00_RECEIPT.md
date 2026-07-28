---
type: release-receipt
title: "Emergentism Corpus Reconstruction and Adequacy Program — Release Receipt"
status: "DEPLOYED AND VERIFIED — public projection only; research gates remain open"
date: 2026-07-28T16:34:43+07:00
evidence_tier: "[B] repository, generator, Vercel, DNS, HTTP, and served-byte observations"
authority: "Receipt only; creates no doctrine, formal result, empirical support, or independent replication"
---

# Corpus Reconstruction Release Receipt

## Release identity

| Field | Observed value |
|---|---|
| source commit | `89b6262690c4af338a952a4cb7fdff7d625472c8` |
| source branch | `codex/emergentism-corpus-reconstruction-20260728` |
| remote custody | `origin/codex/emergentism-corpus-reconstruction-20260728` |
| deploy root | `12_PUBLIC_SITE/` |
| Vercel project | `emergentism-org` (`prj_RyoMG78ylqIWRSnz7URjkeniOKLH`) |
| final deployment | `dpl_EbbQkE5wgGmfmMpfQuTi1a3hSBhu` |
| immutable URL | `https://emergentism-dumd90cob-yves-projects-c163dce1.vercel.app` |
| target and state | production target; `READY`; promoted after immutable audit |
| commit metadata | `gitCommitSha` and `corpusCommit` both equal the source commit above |

The earlier artifact `dpl_3URpLjyCdwApfLuSXgXnesCCTTLc` served the same
audited bytes but carried a mistyped optional `corpusCommit` metadata value. It
was superseded by the final deployment above. This was a provenance defect,
not a served-content difference; the correction was audited before promotion.

## Local gates

- 120 compiler tests passed.
- Purity passed across 804 active files.
- Link, file-register, folder-register, trophic-Rosetta, staged-diff, semantic
  parity, and living-map gates passed.
- The 15-part public predeploy gate passed.
- Deterministic generation matched across repeated book, RAG, atlas, and
  reading-manifest runs.
- The claim contract compiled 69 cards over eight works with 372 graph edges.
- All ten registered historical artifacts remained withheld with exact local
  hashes and exclusion contracts.

## Immutable and branded audits

Both the final immutable URL and `https://www.emergentism.org/` passed the
strict live-domain audit:

- 348/348 probed routes returned HTTP 200 after declared redirects;
- 292/292 reading-manifest documents returned HTTP 200;
- every withheld route resolved to the historical boundary with no risky body;
- the historical boundary served `X-Robots-Tag: noindex, noarchive, nosnippet,
  nofollow` and `Cache-Control: no-store, max-age=0`;
- `/home/` returned HTTP 308 to `/`;
- CSP, HSTS, frame, content-type, referrer, and permissions headers were present;
- the static deployment produced no Vercel error-log entries in the sampled
  post-promotion interval. Absence of logs is not outcome or uptime proof.

Sampled local and branded served SHA-256 values matched:

| Route | SHA-256 |
|---|---|
| `/` | `0450ef8bea4b09c5daa49568724ea45d064db6d63621f68c0baa54e32596aaf5` |
| `/book/` | `e868185e9a3932c1f9df27bf5183d7a6323b63d1a4c1cd97fc03a0caf200a4a7` |
| `/reading-manifest.json` | `c3d7047f11dc14262db20d1733f29bedaa597b2970f5205a6125f1c2fc6cb09a` |
| `/public_semantic_parity.json` | `fa0e0eede39c0706ef1c6c97cba594f94ab798c1e073d7185c1ab26e62749b61` |
| `/assets/js/living-map.js` | `7275840bfe16f4ec96ebb35b456b6d35d5c2dc9ecffc9823a2590e5d790ea278` |

## Alias and DNS observations

Vercel reported both `emergentism.org` and `www.emergentism.org` assigned to
the final immutable deployment. Observed DNS answers were:

- apex A: `64.29.17.1`, `216.198.79.1`;
- `www` CNAME: `a4dd0143bb653011.vercel-dns-017.com`;
- `www` A: `64.29.17.65`, `216.198.79.65`.

The registrar uses Google-managed authoritative nameservers rather than Vercel
nameservers. That is an observed third-party-DNS configuration, not a failure:
both branded hosts resolved to the Vercel edge, returned Vercel request IDs,
served the final hashes, and passed the strict audit.

## Publication and research boundary

Only the repaired One-Sitting reader is current public output. The seven new
historical/research critical editions remain staged and non-public. A0, A1,
A3, A4, A5, A6, and A7 have packets; A2 remains typed. Packet completion is
not truth, proof, evidence contact, or replication.

Still open are formal implementation and prior-art review, conservative
recovery, paradox-by-paradox adjudication, moral-realist bridge testing,
institutional comparison, GP-03 through GP-11 world contact, adverse results,
and independent replication. Publication, popularity, products, agents, and
this receipt do not close any of those gates.
