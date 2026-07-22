---
title: "Untracked arrivals reconciliation — 2026-07-22"
date: 2026-07-22
status: "ARCHIVED [B] — loose arrivals sealed; no semantic authority"
evidence_tier: "[B] path inventory, SHA-256 manifest, verified extraction, and tracked-counterpart custody"
owner: 90_ARCHIVE
---

# Untracked arrivals reconciliation — 2026-07-22

## Disposition

This archive reconciles the 133 loose files that remained in the primary
Emergentism checkout after the dimension-first release. The intake was not one
coherent doctrine set: it mixed Finder-style ` 2` copies, pre-purification
drafts, old audit products, application-specific material, historical
receipts, and tool-noise exports. None was admitted into active authority.

## Custody

- `UNTRACKED_ARRIVALS_2026_07_22.tar.gz` preserves 122 locally readable files
  at their exact original relative paths.
- `ORIGINAL_PATHS.sha256` records every readable source path and its SHA-256.
- A clean extraction reproduced all 122 hashes.
- The archive SHA-256 is
  `41b16f60f10cf1377751e244d502d106cf09043d48eee11c56d1f61863b3dbb5`.
- `DATALESS_COUNTERPARTS.tsv` records eleven iCloud-dataless ` 2.csv`
  placeholders. Each had a tracked, locally readable counterpart at the same
  path without the ` 2` suffix and the same logical byte size. The table
  records that counterpart's SHA-256. It does not falsely claim that the
  placeholder bytes were locally readable or independently compared.

The dataless placeholders therefore add no available local payload beyond
their tracked counterparts. Their custody is the tracked canonical file plus
the path/size/counterpart record in the TSV.

## Restore and verification

Restore readable arrivals into an empty review directory, never over the live
tree:

```sh
mkdir /tmp/emergentism-arrivals-review
tar -xzf UNTRACKED_ARRIVALS_2026_07_22.tar.gz \
  -C /tmp/emergentism-arrivals-review
cd /tmp/emergentism-arrivals-review
shasum -a 256 -c \
  /absolute/path/to/ORIGINAL_PATHS.sha256
```

Reviewers must compare an extracted draft with its current source owner before
proposing any recovery. Archive presence is provenance, not a rival owner,
proof, signature, or permission to reactivate superseded content.

## Exclusions

Eight concurrent tracked modifications under `12_PUBLIC_SITE/` were observed
during this cleanup. They were excluded from the intake, left unstaged, and
were neither changed nor interpreted by this act.

## Kill criterion

This reconciliation fails if the tar cannot list 122 entries, a clean
extraction fails the SHA-256 manifest, a dataless row lacks its named tracked
counterpart at the recorded size, an original arrival is silently promoted,
or the concurrent tracked website work is included in the cleanup commit.
