---
rosetta:
  primary_level: L5
  primary_column: Tooling Architecture
  secondary:
    - level: L4
      column: Tool Execution
      role: "route scripts, deploy helpers, and mutable tooling through bounded execution"
    - level: L3
      column: Tool Audit
      role: "validate generated outputs, receipts, dependency graphs, and link/path checks"
    - level: L6
      column: Core State
      role: "prevent tool output from becoming source doctrine authority"
  operator: "Brahmā ○"
  tier: "Executive"
  regime: "Brāhmaṇa"
  register: "[B/S/I]"
  canonical_phrase: "09_TOOLS — Agent Routing"
title: "AGENTS.md — 09_TOOLS"
status: "ACTIVE — tools route card"
evidence_tier: "[B] for local route references and runnable tool paths; [S] for tooling authority boundaries; [I] for subtool caste mapping."
---

# AGENTS.md — 09_TOOLS

## What This Directory Contains

The tool layer of the Emergentism organism. Scripts, compilers, simulations, packages, and data pipelines that operationalise framework theory into executable code.

## Agentz Cloud / Rosetta Dispatch

| Agentz | Deployment in this lane |
|---|---|
| L1 Caṇḍāla | Names raw tool failures, missing files, broken paths, and contradiction surfaces. |
| L2 Śūdra | Explores available data, commands, environments, and evidence-producing surfaces. |
| L3 Vaiśya | Verifies outputs, dependency graphs, manifests, links, and command receipts. |
| L4 Kṣatriya | Owns bounded execution: scripts, deploy helpers, sprint gates, and K2-reviewed writes. |
| L5 Brāhmaṇa | Owns tooling architecture, compilers, simulations, packages, and reusable structure. |
| L6 Sādhu | Cuts generated-output authority drift and preserves archive/provenance boundaries. |
| L7 Ṛṣi | Translates tool evidence into constitutional or public-symbol narrative only after receipt checks. |

| Subdirectory | Function | Primary Caste |
|---|---|---|
| `01_SCRIPTS/` | Operational scripts (evolution engine, agent sync, coordination) | L4 Kṣatriya |
| `02_COMPILERS/` | Corpus map builders, uplink compilers | L5 Brāhmaṇa |
| `03_SIMULATIONS/` | Formal proofs: spectrum, r-star, MIDUS | L5 Brāhmaṇa with L3/L6 checks |
| `04_DATA_PIPELINES/` | General data-pipeline intake; the former GFS lane is retired under `90_ARCHIVE/2026_07_13_gfs_retraction/` | L2 Śūdra |
| `05_DEPLOY/` | Docker and deployment configs (docker-compose.yml, Dockerfile.heartbeat) | L4 Kṣatriya |
| `06_PACKAGES/emergentism-core/` | **Shared primitives package** — polygenic evolution, K2 crypto, provider taxonomy | L5 Brāhmaṇa |
| `07_AGENT_OPS/` | Agent framework integration, Rosetta loader, syntropic router | L4 Kṣatriya |
| `08_AUDIT_ARTIFACTS/` | Dependency graph auditing | L3 Vaiśya |
| `09_DAC_FRAME/` | DAC Framework operational tools (scripts/, tools/) | L5 Brāhmaṇa |
| `10_SPRINT_GATES/` | Sprint-gate packaging and digest utilities | L4 Kṣatriya |

## Recursive Deployment Control

- Every source-visible folder and file in this lane is covered by
  [`03_AGENTZ_DEPLOYMENT_09_TOOLS_2026_06_04.csv`](../00_META/03_AGENTZ_DEPLOYMENT_09_TOOLS_2026_06_04.csv).
- The paired receipt is
  [`03_AGENTZ_DEPLOYMENT_09_TOOLS_2026_06_04.md`](../00_META/03_AGENTZ_DEPLOYMENT_09_TOOLS_2026_06_04.md).
- Tools may produce receipts or generated summaries; those outputs do not
  become doctrine authority without owner-lane confirmation.

## Critical Runtime

### Polygenic Economic Evolution Engine (v3.0)
- **Location**: `06_PACKAGES/emergentism-core/src/emergentism_core/polygenic/`
- **CLI**: `01_SCRIPTS/evolve_polygenic_tree.py`
- **Registry**: `02_SKYZAI/01_NOOSPHERE/02_INFRASTRUCTURE/Cascade/08_AGENTZ_CLOUD_PWA/01_POLYGENETIC_TREE/09_POLYGENETIC_ECOSYSTEM.json`
- **MCP Server**: `06_PACKAGES/emergentism-core/src/emergentism_core/mcp_polygenic_economics.py`

### Agent Sync
- **[B] Live entry point**: `01_SCRIPTS/agent_goose_sync.py` (supersedes the pre-2026-05-30 reference to `sync_agents.py`)
- Synchronizes agent definitions / Goose agent surfaces across the tool layer


## K2 Boundaries

- `evolve_polygenic_tree.py --all` runs mutation/selection without K2 review — constitutional constants are K2-governed but auto-applied
- `agent_goose_sync.py` mutates agent-definition surfaces — review its diff before applying broadly
- Simulation scripts are read-only — safe to run without K2

## Entry Points for Agents

1. **First time here**: Read `01_SCRIPTS/evolve_polygenic_tree.py --help`
2. **Modifying evolution constants**: Edit `06_PACKAGES/emergentism-core/src/emergentism_core/polygenic/mutation.py` biological constants section
3. **Adding a tool**: Follow `07_AGENT_OPS/` patterns; update this AGENTS.md

Zero-Sum Resolution Equation
