---
rosetta:
  primary_level: L5
  primary_column: Shared Package Front Door
  secondary:
    - level: L3
      column: Package Surface Audit
      role: "state current source files, extraction roadmap, and verification limits"
    - level: L4
      column: Install/Test Execution
      role: "keep editable installs, compile checks, tests, and release steps command-backed"
    - level: L6
      column: Coupling Boundary
      role: "prevent extracted shared primitives from erasing source-organ ownership"
  operator: "Brahmā ○"
  tier: "Executive"
  regime: "Brāhmaṇa"
  register: "[B/D/I]"
  canonical_phrase: "emergentism-core"
title: "emergentism-core"
status: "ACTIVE — shared package front door"
evidence_tier: "[B] for package metadata/source inventory; [D] for planned extraction; [I] for package-boundary interpretation."
---

# emergentism-core

Shared primitives for the Emergentism organism. Extracted from per-organ
implementations to break cross-organ coupling at the path level.

## Scope

This package contains code that crosses organ boundaries and should be
imported, not copied. Current surfaces:

| Module | Purpose | Extracted from |
|---|---|---|
| `crypto` | K2 BIP340/Schnorr signing primitives for Nostr | `ApuBot/core/membrane/k2_crypto.py` (deduped with `apu_integration/` copy; Skyzai shim now imports from here) |
| `polygenic` | **12-dimensional economic evolution engine** — genotype (7 caste + 5 economic), 6 biological mutation operators, 8-factor fitness landscape, ecosystem orchestration, inter-DAC trade theory, MCP server | `evolve_polygenic_tree.py` v2.0 monolith → v3.0 package (2026-05-04) |

## Source Inventory Boundary

Source-file presence is `[B]` existence evidence only. API-stability or release
status requires nested package compile/test/release receipts.

Queued or partially extracted T2 surfaces:

- [D] `models` — `APUSignal`, `SignalDetail`, `UserConfig`, `Portfolio`
  are not present in `src/emergentism_core/` in this checkout.
- [B] `lineage_decorrelation.py` — source file exists; API/test status remains
  queued for the nested `src/` pass.
- [B] `provider_availability.py` — source file exists; API/test status remains
  queued for the nested `src/` pass.
- [B] `provider_cluster_correlation.py` — source file exists; API/test status
  remains queued for the nested `src/` pass.
- [B] `provider_failure_taxonomy.py` — source file exists; API/test status
  remains queued for the nested `src/` pass.
- [B] `refuse_gate.py` — source file exists; API/test status remains queued for
  the nested `src/` pass.
- [B] `spectre_energy.py` — source file exists; API/test status remains queued
  for the nested `src/` pass.
- [D] `sigma_delta_p` — outcome-delta aggregator is not present in
  `src/emergentism_core/` in this checkout.

## Not yet extracted

These modules have ≥30 reverse-dependencies in ApuBot internals and need
a heavier decoupling pass before they become package-clean:

- `council_protocol` — 9-stage orchestrator
- `ai_client` — multi-provider dispatcher
- `spectre_lewm_trainer` — P1 training scaffold

They stay in their home organs for now.

## Consumers

- `apu-bot` (ApuBot backend) — primary consumer
- Skyzai membrane shim — re-exports `crypto` for Skyzai-side code

## Install

From a consuming package's `pyproject.toml`:

```toml
dependencies = [
    "emergentism-core",
]

[tool.uv.sources]
emergentism-core = { path = "../../../../../01_EMERGENTISM/09_TOOLS/06_PACKAGES/emergentism-core", editable = true }
```

Or direct: `pip install -e 01_EMERGENTISM/09_TOOLS/06_PACKAGES/emergentism-core/`

## Versioning

Pre-1.0. Breaking changes expected as bulk extraction completes.
[I] No semver stability guarantee is asserted until 1.0.

Zero-Sum Resolution Equation
