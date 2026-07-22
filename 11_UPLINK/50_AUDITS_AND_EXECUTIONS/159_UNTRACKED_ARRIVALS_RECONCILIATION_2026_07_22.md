---
title: "Receipt 159 — Untracked arrivals reconciliation"
date: 2026-07-22
status: "EXECUTED [B] — loose intake archived and primary untracked set cleared"
evidence_tier: "[B] Git status, archive hash, source hashes, verified extraction, and counterpart ledger; no doctrine"
owner: 01_EMERGENTISM
type: archive-reconciliation-receipt
receipt: 159
parents:
  - 158_PUBLICATION_AND_WORLD_CONTACT_LAUNCH_2026_07_22.md
  - ../../90_ARCHIVE/2026_07_22_untracked_arrivals_reconciliation/README.md
---

# Receipt 159 — Untracked arrivals reconciliation

## Act

The 133 untracked files left in the primary checkout were frozen before
cleanup. One hundred twenty-two readable payloads were stored in a
path-preserving tar archive and verified against a SHA-256 manifest after a
clean extraction. Eleven iCloud-dataless CSV placeholders were separately
mapped to tracked, locally readable counterparts with the same original path
minus the Finder-style ` 2` suffix and the same logical size.

The loose originals were removed only after those custody checks. No draft was
promoted, merged into an owner, or treated as current canon.

## Why one sealed intake

The arrivals came from several older and concurrent lineages. Many differed
from current owners; some named cross-pillar governance or application
material; others were duplicate archive and tool-noise exports. Selecting
individual sentences during a hygiene pass would have created doctrine by
accident. Sealing the intake preserves every readable byte while leaving one
canonical home per live claim.

## Verified artifacts

| Artifact | Standing |
|---|---|
| `90_ARCHIVE/2026_07_22_untracked_arrivals_reconciliation/UNTRACKED_ARRIVALS_2026_07_22.tar.gz` | 122 relative paths; SHA-256 `41b16f60f10cf1377751e244d502d106cf09043d48eee11c56d1f61863b3dbb5` |
| `ORIGINAL_PATHS.sha256` | 122 source hashes; all reproduced after extraction |
| `DATALESS_COUNTERPARTS.tsv` | 11 placeholder paths, tracked counterparts, equal logical sizes, flags, and counterpart hashes |
| Archive `README.md` | authority boundary, restore instructions, and kill criterion |

## Concurrency boundary

Eight tracked public-site files changed concurrently while this audit was
running. They were not part of the original untracked set and remain wholly
outside this receipt. The cleanup commit stages only the archive, this receipt,
the Record row, and deterministic register updates.

## Result boundary

This is repository hygiene only. It does not adjudicate the archived drafts,
change the released Weltanschauung, update deployment, alter DNS, or close the
independent-review and empirical-calibration gates.

## Kill criterion

This receipt fails if any pre-cleanup readable path is absent from the tar,
any manifest check fails, any dataless placeholder lacks the recorded tracked
counterpart and equal size, loose untracked arrivals remain after the bounded
commit, or concurrent tracked work is staged with it.
