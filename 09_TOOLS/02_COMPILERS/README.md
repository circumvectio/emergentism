---
rosetta:
  primary_level: L5
  primary_column: Compiler Front Door
  secondary:
    - level: L3
      column: Reproducibility Audit
      role: "state which compiler outputs are source-backed and which are dormant"
    - level: L4
      column: Compiler Execution
      role: "keep compiler commands explicit and diff-reviewed before generated output is accepted"
    - level: L6
      column: Source Boundary
      role: "make compiler output downstream from source-owned doctrine and route cards"
  operator: "Brahmā ○"
  tier: "Executive"
  regime: "Brāhmaṇa"
  register: "[B/S/I]"
  canonical_phrase: "02_COMPILERS"
title: "02_COMPILERS"
status: "ACTIVE — compiler front door"
evidence_tier: "[B] for local compiler inventory and source-input status; [S] for downstream-output rule; [I] for folder-boundary guidance."
---

# 02_COMPILERS

Focused compiler utilities for building derived maps and compressed working
surfaces from source-owned material.

## What Belongs Here

- narrow compilers that emit indexes, maps, or other derived views
- helper builders that support source-first navigation

## What Does Not

- source doctrine
- hand-authored authority files that should live in the owning row
- deployment scripts

## Authority Rule

Compiler output is downstream. If a compiled artifact disagrees with the owning
source lane, repair the source and recompile.

## Current Compiler Inventory

| Compiler | Output | Status |
|---|---|---|
| `build_corpus_map.py` | `00_CORPUS.md` folder-perspective maps | [B] Dormant in this checkout: requires `../_corpus_source.yaml`, which is not present. |

## Route Upstream

- main tool inventory: `../README.md` and `../CLAUDE.md`
- UPLINK compile entry point: `../01_SCRIPTS/compile_uplink.py`
- full routing layer: `../../11_UPLINK/00_CORE/00_INDEX.md`

## Kintsugi audit foundation

The A0 baseline validator freezes the known repository test state without treating existing failures as new truth:

```bash
set -euo pipefail
python3 -B 09_TOOLS/02_COMPILERS/validate_kintsugi.py \
  --check-baseline \
  --canonical-root /Users/Yves/Documents/01_EMERGENTISM
```

`kintsugi_baseline_failures.json` records 19 baseline node IDs and five exact failure signatures at `main@26e616e651e2a87e8c85bf37db515d7fcd007b7b`. A previously failing node may turn green; a removed node, new failure, exception drift, or signature drift fails. The validator itself introduces no direct writes and disables pytest cache and Python bytecode writes; arbitrary repository test bodies are not sandboxed. The baseline gate has no K2 approval gate.

## Kintsugi A0B machine kernel

> **Boundary:** A0B validates grammar and transaction machinery. It does not
> validate Emergentism, repair canon, or create a live Kintsugi vessel.

The dated [A0B machine handoff](../../docs/superpowers/specs/2026-07-12-kintsugi-a0b-machine-kernel-handoff.md)
records the reproducible local evidence and the limits on the first live A1
vessel.

| Package boundary | Responsibility |
|---|---|
| `diagnostics.py` / `codec.py` | Typed issues, canonical JSON, hashes, and safe repository paths |
| `baseline.py` / `schema.py` | Frozen A0 baseline and restricted schema evaluation |
| `records.py` / `semantics.py` | Typed record graph, evidence/Justice rules, antibodies, and the downstream Compass mutation projection |
| `markdown.py` | Machine-fence synchronization and framed narrative hashes |
| `gitstate.py` / `manifest.py` | Git scope, protected-tree, manifest, attempt, and compare-and-swap laws |
| `review.py` | Review target, attestations, history, transitions, and validation bundle |
| `orchestration.py` | Read-only dependency-ordered validation |
| `rendering.py` | One operation-aware atomic transaction writer |
| `validate_kintsugi.py` / `render_kintsugi.py` | Stable validator and renderer command-line facades |

The schema exposes exactly three selectable root roles: `coreData`,
`publicQueue`, and `baselineAllowlist`.

### Read-only checks

Frozen baseline:

```bash
python3 -B 09_TOOLS/02_COMPILERS/validate_kintsugi.py \
  --check-baseline \
  --canonical-root /Users/Yves/Documents/01_EMERGENTISM
```

Default live check:

```bash
python3 -B 09_TOOLS/02_COMPILERS/validate_kintsugi.py --check
```

The default check currently exits `2` with controlled `KIN-E-IO` because
`02_KINTSUGI_SEAMS.json` does not yet exist. That is an honest missing-input
state, not a validation failure.

Explicit phase-check template:

```bash
python3 -B 09_TOOLS/02_COMPILERS/validate_kintsugi.py \
  --check --phase A --bootstrap --base-ref <tracked-base> \
  --canonical-root <canonical-root>
```

Stable output is `KIN-OK validation` for a successful full check and
`KIN-OK baseline collected=19 failures=5` for the frozen baseline. Failures use
`KIN-ERROR <path> <code>: <message>`.

Validator exits are `0` pass, `1` semantic validation failure, and `2` CLI or
I/O failure. Renderer exits are `0` pass, `1` transaction rejection, and `2`
parser or request error.

### Renderer contract, not a live invocation

| Operation | Role |
|---|---|
| `freeze-manifest` | Finalize the manifest, allocate the smallest unused attempt ID, and freeze the subject |
| `review-target` | Materialize the already-bound review target |
| `transition-core` | Apply one legal review-state transition with external review intake |
| `bundle` | Preflight the immutable bundle against a `COMPLETE` receipt without writing it; `transition-core --stage VERIFIED` materializes it |

The six lifecycle stages are: (1) final freeze/allocation, (2) `TARGET_READY`,
(3) `ATTESTED`, (4) `FAILED` or `ABANDONED`, (5) `COMPLETE`, and (6)
`VERIFIED`. A retry uses the canonical smallest-unused attempt ID and preserves
append-only `reviewAttempts`, `reviewAttemptArtifacts`, `reviewAttestations`,
`reviewFindings`, and `reviewFindingDispositions`. `PASSED` is terminal;
`FAILED` or `ABANDONED` requires an exact predecessor disposition before retry.

External candidates enter through `--logic-review-input`,
`--btj-review-input`, and `--finding-dispositions-input`. They remain outside
both repositories until atomic intake. Every transaction holds the shared Git
common-directory lock, checks expected HEAD and core hash before and inside the
lock, freezes the read set, and rolls back on a partial replacement. Final
`freeze-manifest` additionally persists its attempt reservation, so a failed
post-reservation freeze leaves that attempt ID burned.

Typed-control prose is filtered outside machine fences. Ledger and receipt
narratives use framed hashes so fence-side movement changes the digest.
`safeRegexSearch` is bounded to a 256-code-point pattern and a 1,024-state
Thompson NFA; it does not invoke Python's backtracking regular-expression
engine.
