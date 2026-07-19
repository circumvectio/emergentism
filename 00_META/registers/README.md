---
rosetta:
  primary_level: L3
  primary_column: Meta
  operator: "Kṛṣṇa ◇"
  tier: "Executive"
  regime: "Vaiśya"
  register: "[S]"
  canonical_phrase: "Canonical registers — derived inventory, additive-only, never hand-edited"
type: register-front-door
title: "00_META/registers — FILE_REGISTER + FOLDER_REGISTER"
status: "ACTIVE 2026-07-19 — additive-only remediation wave (receipt 141A gate)"
owner: 01_EMERGENTISM
---
Regenerate both registers: `python3 09_TOOLS/01_SCRIPTS/build_magnum_opus_register.py --write` (repo root derives from the script path; run from anywhere).
Verify drift: `python3 09_TOOLS/01_SCRIPTS/build_magnum_opus_register.py --check` — exit 0 clean; exit 1 lists changed/added/removed paths.
Source of truth: `git ls-files` (tracked files) + working-tree bytes; both registers are derived artifacts — never hand-edit entries.
FILE_REGISTER carries the stable self-marker entry `00_META/registers/FILE_REGISTER.json` with `sha256: "SELF"`; dispositions mirror the pending 05/06 manifests.
Additive-only gate (receipt 141A): this inventory authorizes no move, tombstone, promotion, or commit — navigation and audit surface only.
