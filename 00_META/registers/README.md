---
rosetta:
  primary_level: L3
  primary_column: Meta
  operator: "Kṛṣṇa ◇"
  tier: "Executive"
  regime: "Vaiśya"
  register: "[S]"
  canonical_phrase: "Canonical registers — deterministic Git-index inventory"
type: register-front-door
title: "00_META/registers — FILE_REGISTER + FOLDER_REGISTER"
status: "ACTIVE 2026-07-20 — Git-index deterministic; inventory only"
owner: 01_EMERGENTISM
---
Regenerate both registers: `python3 09_TOOLS/01_SCRIPTS/build_magnum_opus_register.py --write` (repo root derives from the script path; run from anywhere).
Verify drift: `python3 09_TOOLS/01_SCRIPTS/build_magnum_opus_register.py --check` — exit 0 clean; exit 1 lists changed/added/removed paths.
Source of truth: the staged Git index (`git ls-files -s` plus indexed blob
bytes); unstaged working-tree bytes never enter the derived snapshot. Both
registers are generated artifacts — never hand-edit entries.
FILE_REGISTER carries the stable self-marker entry `00_META/registers/FILE_REGISTER.json` with `sha256: "SELF"`; dispositions mirror the pending 05/06 manifests.
Inventory boundary: these files authorize no move, tombstone, promotion, or
commit. They provide navigation and audit evidence only.
