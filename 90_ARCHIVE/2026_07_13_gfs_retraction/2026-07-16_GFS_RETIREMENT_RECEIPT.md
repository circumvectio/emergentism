---
title: "GFS study corpus retirement receipt"
date: 2026-07-16
status: "COMPLETE — SOURCE/ARCHIVE HALF"
disposition: "RETIRED TO K3 ARCHIVE; NOT LIVE, NOT PENDING, NOT CITABLE AS ACTIVE EVIDENCE"
evidence_tier: "[B] file/hash receipt; [D] retirement decision; [I] historical interpretation only"
source_base: 9c1fb7ae232de6e2fa1f1cbac36391c00a1994df
dangling_source: 8cffc1a224ac7b7d21bfea3c66d31d0ceb11c41a
---

# GFS study corpus retirement receipt

## Decision

The owner directed that all GFS study material be archived. This receipt
executes that decision on the Emergentism source/archive half. The direct GFS
study corpus is no longer an active methodology owner, pipeline, experiment,
pending program, public-validation lane, or evidence source.

This is an archive-first retirement, not deletion. Historical files remain
byte-preserved and hash-bound. Their old language is evidence of the study's
history only.

## Preserved payload

| Source class | Count | Source revision | Disposition |
|---|---:|---|---|
| Active direct artifacts | 11 | `9c1fb7ae232de6e2fa1f1cbac36391c00a1994df` | Moved byte-for-byte under `active_corpus/` with original path topology preserved. |
| Detached AND-class artifacts | 5 | `8cffc1a224ac7b7d21bfea3c66d31d0ceb11c41a` | Extracted blob-for-blob under `dangling_8cffc1a/`; the commit itself was not cherry-picked. |
| Earlier peer-review archive artifacts | 3 | Already cold | Left at their prior archive paths; pointers are recorded in `README.md`. |

The deterministic file-level record is `SHA256_MANIFEST.tsv`. It lists 16
payloads, their original paths, source revisions, byte counts, run identities,
and SHA-256 digests.

## Run identities and what they actually were

| Run identity | Date | Inputs available here | Honest scope |
|---|---|---|---|
| `GFS-W1-2026-04-09` | 2026-04-09/10 | Per-country results CSV and meta-analysis text; three closely related Python pipeline variants | Historical country-level fit. Raw respondent microdata is absent, so this repository cannot reproduce the fit end to end. |
| `GFS-POOL-2026-07-02` | 2026-07-02 | `gfs_results_20260409.csv` plus pooled script/output/verdict | A re-analysis of the April per-country table, not a new sample, raw-data refit, or independent replication. |
| `GFS-AND-2026-07-12` | 2026-07-12 | Detached receipt, discriminator, and three result tables from `8cffc1a` | An extension on the same GFS study and proxy construction. It was never part of the current branch and is preserved only as detached provenance. |

## Missing raw evidence

- Neither `gfs_all_countries_wave2.csv` nor
  `gfs_all_countries_wave2.dta` is tracked in this repository.
- The detached discriminator embeds an absolute external-drive default path to
  the DTA file. That path is provenance, not repository custody.
- The historical Wave-1 owner headlines `n = 207,920`; the pooled experiment
  sums the preserved complete-case country table to `n = 128,868`; the detached
  AND-class receipt says `207,919` rows loaded and `128,868` complete cases.
  Without the raw microdata and a custody receipt, the one-row discrepancy and
  the approximately 79,000-row analysis attrition cannot be independently
  reconciled here.
- The scripts say “22-country” while preserved outputs and receipts report 23
  country codes. The archive preserves that mismatch; it does not repair it.

## Duplicate and dependence facts

1. The April analysis, July pooled verdict, and July AND-class extension are
   not three independent studies. They are successive analyses of the same GFS
   sample/proxy lineage.
2. The 2026-07-02 pooled run consumes the April aggregate result table rather
   than respondent microdata. Its claims are dependent on the April pipeline.
3. The three tracked country-analysis scripts are near-duplicate variants of
   one pipeline, not independent implementations. They are all preserved
   because their variable construction differs in places and no raw rerun
   adjudicates which variant generated every output.
4. The detached AND-class run explicitly uses the April construction and
   validates against the April result table. It extends the model family; it
   does not supply independent evidence.
5. No two of the 16 archived payload files are byte-identical. “Duplicate” here
   means shared data, proxy, and analytical lineage, not duplicate bytes.

## Interpretation boundary

The archived lineage mixed several claims: additive versus interaction fit,
balance, AND-class shape, a mu-limit story, and the zero-factor boundary. The
study's survey proxies and observed interior range did not directly test a
literal zero-factor boundary. Conversely, that mismatch cannot be used to
claim the boundary law is true. The correct disposition is retirement: no
positive or negative GFS conclusion is load-bearing in active Emergentism.

## Source-owner repairs in this change

- The live Methodology front door, claim matrix, empirical board, science-stack
  status, and test-design owner now name GFS as retired archive provenance.
- `00_THE_AMRITA.md` no longer carries GFS as live empirical support or a live
  result in its present-tense distillation; it records the study only as a
  retired example of self-correction.
- Tool route cards no longer identify GFS as the active data-pipeline focus.
- The old `91_COMPATIBILITY` path now points only to this archive root and
  explicitly forbids revival.
- Dated audits, papers, preregistrations, and session history were not rewritten.
  Their GFS statements remain historical and may contain links to the old path;
  those links no longer confer current authority.
- `12_PUBLIC_SITE/**` was outside this source/archive implementation and was not
  edited by it.

## Verification contract

The retirement is acceptable only if:

1. all 16 manifest hashes match the preserved payloads;
2. the five detached payloads match the corresponding blobs in `8cffc1a`;
3. the 11 active payloads remain byte-identical to source base `9c1fb7a`;
4. no direct GFS artifact remains at its former active path;
5. active source-owner and tool-route documents contain no live/pending/citable
   GFS program claim;
6. `git diff --check` passes; and
7. no source/archive commit includes `12_PUBLIC_SITE/**`.
