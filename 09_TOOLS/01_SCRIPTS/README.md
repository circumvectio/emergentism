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
  The claim-status checker additionally binds the exact 48-row lifecycle and
  full contract document, validates the named external-owner registry and
  restored-result inventory, and rejects terminal/fake blockers or dependency
  cycles.
- `check_coherence_profile.py` validates the tool-owned four-axis declaration
  in `coherence_profile.json`. Its overall state is explicitly internal;
  world contact remains a separate typed axis and cannot be supplied by a
  local gate result.
- `check_contact_limited.py` recomputes the receipted completion counters from
  their machine owners. It guards the receipt-collision universe, exclusive
  public lifecycle (including zero-unclassified closure, cross-implementation
  ignore parity, aliases, and raw-overlap debts), the complete 48-row claim
  lifecycle (26 W/RQ rows plus 22 grave-parent rows), exact contact contracts,
  zero ambiguous dispositions, exact owner-held debts, and the fail-closed
  `OPEN` world axis.
  A pass is an internal inventory result, never evidence that those debts have
  closed or that world contact occurred. Its state digest is bound to a dated
  snapshot receipt; an already-committed receipt must match both the worktree
  and its first-parent bytes, so a rebaseline requires a new receipt path.
- `check_active_receipt_citations.py` ratchets target identity across a fixed
  set of active source owners and the citation-scannable current/provisional
  public text-dependency closure. It binds typed locators and exact
  receipt/packet filename tokens,
  treats all 97 physically reused prefixes as unsafe bare, and rejects new
  unregistered active owners. Generated FILE/FOLDER inventories, compiler
  fixtures, and vendored public libraries are explicit non-citation classes;
  current lane indexes, modules, manifests, workers, and service-worker
  precache dependencies remain in scope. Default mode is read-only. An
  adjudicated rebaseline is explicit:

  ```sh
  python3 09_TOOLS/01_SCRIPTS/check_active_receipt_citations.py --write
  python3 09_TOOLS/01_SCRIPTS/check_active_receipt_citations.py
  ```

  The generated `00_META/ACTIVE_RECEIPT_CITATION_REGISTRY.json` binds its
  dated custody through the registry's own `custody.receipt_ref`. A pass proves
  local target identity in the declared active scope, not receipt truth,
  evidence strength, historical renumbering, publication, or deployment.
- `claim_policy.py` — shared positive-assertion rules.
- `check_node_product_ranking.py` — KSC-02 regression gate: the active corpus
  and active Managed Agents projection may not restore the retired product as
  a selected/ranked/scored/maximized node objective. Explicit history,
  negative results, and separately cardinal candidates remain readable.
- `check_review_bundle.py` verifies the latest versioned review hash set and
  rejects a human-facing `READY TO SEND` label while the machine registry keeps
  `FPE-REVIEW-01` blocked. A pass proves local packet custody, never reviewer
  identity, contact, reply, or independent evidence.
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

## External/corporate scripts in K3 custody

The following former active files were not Emergentism evidence or worldview
gates. They were not called by `gate.sh` and conferred no claim authority:

- `verify_z_ai.py` — external model-endpoint connectivity probe; its active
  duplicate was removed after exact archived-byte verification.
- `mver_validator.py` and `test_mver_validator.py` — corporate data-room hash
  validator and synthetic tests; both were moved byte-identically.

The completed 2026-08-01 custody record, source paths, and SHA-256 identities
are at
[`../90_ARCHIVE/runtime_and_dataroom_strays_2026_08_01/README.md`](../90_ARCHIVE/runtime_and_dataroom_strays_2026_08_01/README.md).
No utility was executed and no runtime, network, data-room, publication, or
deployment effect occurred.

## Status

Active support folder. Scripts can compile, validate, and repair routing, but source owners remain upstream.

## Corpus adequacy gates

```sh
python3 09_TOOLS/01_SCRIPTS/check_barred_claims.py --scope cards
python3 09_TOOLS/01_SCRIPTS/check_barred_claims.py --scope public
python3 09_TOOLS/01_SCRIPTS/check_barred_claims.py --scope all
python3 09_TOOLS/01_SCRIPTS/check_node_product_ranking.py
```

`claim_policy.py` holds the narrow positive-assertion rules shared by the
corpus and public release checks. Lifecycle controls historical language;
denials and boundary statements are not treated as forbidden assertions.

`check_node_product_ranking.py` imports the exact active-corpus boundary from
`check_emergentism_purity.py` and additionally scans the active
`08_FRAMEWORK_SUPPORT/08_AGENTS/MANAGED_AGENTS/` deployment projection.
Archives, compatibility, handoffs, public-site output, audit/session packets,
and generated registers remain excluded. Its only file exclusion is its own
negative-control fixture.
