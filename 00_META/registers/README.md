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
title: "00_META/registers — FILE_REGISTER + FOLDER_REGISTER + CLAIM_CARD_REGISTER + CLAIM_GRAPH + CLAIM_LIFECYCLE_INVENTORY"
status: "ACTIVE 2026-07-19 — additive-only remediation wave (receipt 141A gate)"
owner: 01_EMERGENTISM
---
# Canonical Registers — FILE_REGISTER, FOLDER_REGISTER, CLAIM_CARD_REGISTER, CLAIM_GRAPH, CLAIM_LIFECYCLE_INVENTORY

All five JSON files are deterministic derived artifacts. They are navigation,
audit, and routing views; they do not become source authority or evidence by
being present here. Never hand-edit generated entries.

## File and folder inventory

`FILE_REGISTER.json` and `FOLDER_REGISTER.json` are generated from
`git ls-files`, working-tree bytes, and the tracked-directory closure:

```sh
python3 09_TOOLS/01_SCRIPTS/build_magnum_opus_register.py --write
python3 09_TOOLS/01_SCRIPTS/build_magnum_opus_register.py --check
```

FILE_REGISTER and FOLDER_REGISTER carry stable `sha256: "SELF"` markers
because they are cyclic generated outputs; README.md and every other static
register-family file carry their real byte hashes. Fail-closed custody: if any
tracked non-output path is absent from the working tree, both modes return
nonzero and `--write` changes nothing. A staged deletion of a non-output path
lawfully removes that path from the next generated register.

## Claim, graph, and lifecycle registers

`CLAIM_CARD_REGISTER.json`, `CLAIM_GRAPH.json`, and
`CLAIM_LIFECYCLE_INVENTORY.json` are generated together from the claim-card,
adequacy-docket, schema, book-manifest, and declared source contracts owned by
`compile_claim_cards.py`:

```sh
python3 09_TOOLS/02_COMPILERS/compile_claim_cards.py --write
python3 09_TOOLS/02_COMPILERS/compile_claim_cards.py --check
```

Repair an upstream contract first, then regenerate these three downstream
artifacts. Their graph membership, counts, and lifecycle labels confer no
claim authority and do not establish the claims they inventory.

## Custody boundary

Exact generated custody: `--write` restores this README byte-for-byte from the builder; `--check` fails when it is absent or modified.
Additive-only gate (receipt 141A): these files are inventory/navigation only; they authorize no move, tombstone, promotion, or commit.
