---
rosetta:
  primary_level: L4
  primary_column: Script Operations
  secondary:
    - level: L3
      column: Validation Receipts
      role: "own manifest, link, Rosetta, and path repair helpers as audit-support tools"
    - level: L5
      column: Tooling Architecture
      role: "route reusable libraries and scenario harnesses to their owner folders"
    - level: L6
      column: Authority Boundary
      role: "prevent active scripts from overriding upstream source owners"
  operator: "Arjuna ⚔"
  tier: "God"
  regime: "Kṣatriya"
  register: "[B/I]"
  canonical_phrase: "01_SCRIPTS — Script Front Door"
title: "01_SCRIPTS"
status: "ACTIVE — script front door"
evidence_tier: "[B] for local script inventory; [I] for folder-boundary guidance."
---

# 01_SCRIPTS

## What This Folder Is

Current repository validators and narrowly scoped support scripts.

## What It Owns

- Corpus, claim, receipt, link, and public-artifact validation.
- Rosetta annotation and bounded path-repair helpers.
- One-file support scripts that are not large enough to become packages.

## What It Must Not Own

- Long-lived shared libraries. Route those to `../06_PACKAGES/`.
- Scenario-based simulations. Route those to `../03_SIMULATIONS/`.
- Historical one-off scripts. Route those to `../90_ARCHIVE/`.

## Read First

- `gate.sh` — the corpus gate; run from the repository root with
  `bash 09_TOOLS/01_SCRIPTS/gate.sh`.
- `check_foundation.py`, `check_claim_status.py`, and
  `check_emergentism_purity.py` — broad owner, tier, and boundary checks.
- `claim_policy.py` — shared positive-assertion rules.
- `check_no_secrets_staged.py` — deliberately not a tree gate: it inspects the
  staged diff and therefore belongs in the pre-commit hook.

## Gate custody

`gate.sh` runs `build_magnum_opus_register.py --check` and fails closed when
the derived FILE/FOLDER registers drift or the builder is absent. Regenerate
the two register artifacts with:

```sh
python3 09_TOOLS/01_SCRIPTS/build_magnum_opus_register.py --write
python3 09_TOOLS/01_SCRIPTS/test_build_magnum_opus_register.py
```

The builder refuses both `--write` and `--check` when an index-tracked source
path is missing from the working tree; an authorized staged deletion removes
that path from the next register. Its three declared outputs must remain in the
index. `--write` may reconstruct a missing output only while that index custody
still exists, and restores `00_META/registers/README.md` exactly.

The gate also runs `lake build` in `../05_FORMAL_VERIFICATION/`. This Lean gate
is not suppressed by `EMERGENTISM_SKIP_SLOW=1`; only
`EMERGENTISM_SKIP_LEAN=1` produces an explicit `SKIP`. If the formal lane or
`lake` is missing without that acknowledgement, the gate fails.

## External/corporate scripts awaiting K3 custody

The following tracked files are not Emergentism evidence or worldview gates.
They are not called by `gate.sh`, confer no claim authority, and remain in place
until archive custody is ruled:

- `verify_z_ai.py` — an external model-endpoint connectivity probe that reads
  local environment configuration.
- `mver_validator.py` and `test_mver_validator.py` — a corporate data-room hash
  validator and its synthetic test suite.

The proposed K3 destination is
`../90_ARCHIVE/runtime_and_dataroom_strays_2026_08_01/`. This records a
disposition proposal, not a completed move.

## Status

Active support folder. Scripts can compile, validate, and repair routing, but source owners remain upstream.

## Corpus adequacy gates

```sh
python3 09_TOOLS/01_SCRIPTS/check_barred_claims.py --scope cards
python3 09_TOOLS/01_SCRIPTS/check_barred_claims.py --scope public
python3 09_TOOLS/01_SCRIPTS/check_barred_claims.py --scope all
```

`claim_policy.py` holds the narrow positive-assertion rules shared by the
corpus and public release checks. Lifecycle controls historical language;
denials and boundary statements are not treated as forbidden assertions.
