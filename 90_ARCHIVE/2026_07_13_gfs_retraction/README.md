---
title: "GFS study corpus retirement archive"
date_opened: 2026-07-13
retirement_receipt: 2026-07-16
status: "K3 ARCHIVE — RETIRED — NON-AUTHORITATIVE — NOT CITABLE AS ACTIVE EVIDENCE"
evidence_tier: "[D] archive disposition; preserved [B]/[I] historical claims retain only their historical meaning"
source_base: 9c1fb7ae232de6e2fa1f1cbac36391c00a1994df
dangling_source: 8cffc1a224ac7b7d21bfea3c66d31d0ceb11c41a
---

# GFS study corpus retirement archive

This directory is the cold, provenance-preserving home of the Emergentism
Global Flourishing Study (GFS) work. The entire direct study lane was retired
on 2026-07-16. Nothing here is a live result, pending experiment, validation
path, or citable support for Emergentism.

Retirement does not erase the historical record. K3 requires the files, their
contradictions, and their failed or inconclusive interpretations to remain
inspectable. Any future human-flourishing study must begin as a new study with
new instruments, preregistration, raw-data custody, and independent authority;
it may not revive this archive by reference.

## Topology

- `active_corpus/` preserves, byte-for-byte, the 11 direct GFS artifacts that
  were active at source base `9c1fb7a`: the Wave-1 owner receipt, six pipeline
  files, and the four-file 2026-07-02 pooled experiment.
- `dangling_8cffc1a/` preserves, byte-for-byte, only the five GFS blobs added by
  detached commit `8cffc1a`: the AND-class receipt, discriminator, and three
  result tables. The commit was not cherry-picked; unrelated path renames in
  that commit were not imported.
- `SHA256_MANIFEST.tsv` binds every preserved payload to its original path,
  source revision, byte count, run identity, and archive path.
- `2026-07-16_GFS_RETIREMENT_RECEIPT.md` records the disposition, study limits,
  duplicate facts, missing evidence, and owner-reference repairs.

## Non-authority boundary

The archived documents contain historical tier labels such as `[B]` and `[I]`.
Those labels describe what the authors claimed at the time; placement here
does not renew them. The archive may be cited only as provenance for what was
attempted, reported, contradicted, or retired.

## Raw-data boundary

No respondent-level GFS microdata is tracked in this repository. The historical
files refer variously to `gfs_all_countries_wave2.csv` and
`gfs_all_countries_wave2.dta`, but neither file is present here. Consequently,
the April fit, July re-pooling, and July AND-class extension cannot be rerun
from raw observations from this repository alone.

## Earlier cold material left in place

Three GFS peer-review artifacts were already under the cold archive and were
not duplicated or moved into this directory:

- `90_ARCHIVE/08_FRAMEWORK_SUPPORT/06_TRANSLATION/PEER_REVIEW/GFS_PREREGISTRATION_DRAFT.md`
- `90_ARCHIVE/08_FRAMEWORK_SUPPORT/06_TRANSLATION/PEER_REVIEW/GFS_WAVE1_SECONDARY_ANALYSIS_BRIEF.md`
- `90_ARCHIVE/08_FRAMEWORK_SUPPORT/06_TRANSLATION/PEER_REVIEW/gfs_analysis_preregistered.R`

They remain non-authoritative historical material under the root archive route
card.
