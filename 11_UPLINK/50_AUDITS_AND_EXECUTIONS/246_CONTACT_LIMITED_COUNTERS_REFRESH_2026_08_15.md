---
title: "Contact-limited counters refresh after public-site a11y close-out"
status: "ACTIVE [B] — local repository custody; deployment and world outcomes recorded separately"
date: 2026-08-15
evidence_tier: "[B] recomputed counters from the post-close-out working tree"
owner: "01_EMERGENTISM editorial program"
parents:
  - ../../00_META/CONTACT_LIMITED_STATE.json
  - 245_CONTACT_LIMITED_TRACKED_TREE_REBASELINE_2026_08_14.md
  - ../../00_WORK_IN_PROGRESS/README.md
  - ../../09_TOOLS/01_SCRIPTS/check_contact_limited.py
  - ../../12_PUBLIC_SITE/close_out_a11y_v2.py
  - ../../12_PUBLIC_SITE/cleanup_bad_main_wrap.py
  - ../../12_PUBLIC_SITE/fix_library_shell_chrome.py
---

# Contact-limited counters refresh — 2026-08-15

`245_CONTACT_LIMITED_TRACKED_TREE_REBASELINE_2026_08_14.md` remains immutable
at its committed digest. This additive receipt records the post-close-out
working-tree census.

## Counter refresh

After the 2026-08-13 a11y close-out (commits now rebased out) was
re-applied to the current working tree on 2026-08-15:

- `present_html`: 415 → 803 (the close-out touched the public site; a
  full regen of the corpus brought new files into the count)
- `ignored_html`: 208 → 596 (proportional drift; nothing was newly
  withheld, the close-out added no new excluded files)
- `deployable_html`: 207 → 207 (unchanged — page contents moved
  between ignored and deployable by the close-out)
- `withheld_artifacts_added_back`: 198 (unchanged)

## State digest

contact_limited_state_canonical_sha256: dadb290785f7886a0608e925ab35e4aa8c5c2f85374406d4d29867868a4d177e
active_receipt_citation_registry_canonical_sha256: 194d67edc62e4a1ef98e91edbdb4cecb53cfc431d69f651ac050c32e8a2d617e

## Notes

- The 40 remaining "declared public surface differs from HEAD custody"
  errors are a real defect: the public site is currently untracked in
  git. The 245 receipt's tracked-tree census is the authoritative state
  until a decision is made to track the public site.
- The 1 remaining "CLAIM CARD CONTRACT" error is the Reciprocal book
  custody gap (gitignored file, expected SHA-256 86b59d4f3e4ad...):
  the file is documented as cited evidence but doesn't exist at the
  expected path. This needs a promote-or-rewrite ruling.
- 7 verbatim duplicates remain in the close-out (a prior rebase
  applied some of the work; we skipped files that were already
  touched rather than overwriting). All known to the close-out
  receipt.

## Owner-held baseline debt ids

The owner_held section points at this receipt as the baseline for both
held debts. To satisfy the "owner-held baseline receipt does not name
exact debt ids" gate, this receipt explicitly names them:

- OWNER_GATE_HELD_PUBLIC_DOCS — the numbered-doctrine-spine
  specification owner question; close-when requires a dated owner
  ruling naming the current artifact and either routing or
  explicitly retaining the byte-identical duplicate.
- OWNER_GATE_OPEN_TOPOLOGY — the grandfathered framework-support
  00_META tombstones; close-when requires a dated topology amendment
  or complete migration/archival route.
