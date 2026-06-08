---
rosetta:
  primary_level: L4
  primary_column: Agent-Ops Front Door
  secondary:
    - level: L3
      column: Validator Receipts
      role: "separate current audit outputs from stale generated inventories"
    - level: L5
      column: Agent-Tool Architecture
      role: "map scaffold, compaction, skill, loader, and router utilities"
    - level: L6
      column: Authority Boundary
      role: "keep generated agent surfaces downstream from owner-lane canon"
  operator: "Arjuna ⚔"
  tier: "God"
  regime: "Kṣatriya"
  register: "[B/D/I]"
  canonical_phrase: "07_AGENT_OPS"
title: "07_AGENT_OPS"
status: "ACTIVE — agent-operation front door"
evidence_tier: "[B] for current validator/generator receipts; [D] for scaffolds and dry-run plans; [I] for route-control synthesis."
---

# 07_AGENT_OPS

Agent-operation utilities for scaffolding, validation, compaction, and batch
maintenance across AI-facing repo surfaces.

## What Belongs Here

- agent-surface validators
- batch utilities that add or repair CLAUDE/working-backwards surfaces
- helper scripts for agent skill compilation or Rosetta-oriented loading
- repo-wide `AGENTS.md` generation helpers when the output remains tied to
  source-owner routing

## Current Focus

The scripts in this folder currently support:

- depth-aware `AGENTS.md` scaffold generation
- execution-surface validation
- batch PWA/tools surface creation
- agent skill compilation
- compaction and Rosetta loading helpers
- syntropic router scaffolding for lane locks, transitions, and Soma-event logs

## Current Inventory

| Surface | Tier | Role |
|---|---|---|
| `execution_surface_validator.py` | [B/D] | Validates agent-facing execution surfaces when run; stale output must not be promoted without a fresh receipt. |
| `AGENT_GAPS.json` | [B] | Generated gap inventory for its producing run; current corpus truth requires rerun or Rosetta index evidence. |
| `generate_agents_md.py` | [D/B] | Dry-run/write generator for route cards; dry-run output is a plan, written files require owner-lane review. |
| `batch_add_pwa_wiki_surfaces.py`, `batch_add_tools_surfaces.py` | [D] | Batch scaffold helpers; output remains draft until path-scoped review. |
| `compile_agent_skills.py`, `agent_framework_integration.py` | [D/I] | Skill/framework support utilities; runtime claims need explicit execution receipts. |
| `auto_compaction.py`, `rosetta_loader.py` | [D/I] | Loading and compaction helpers; preserve source-owner routing and tier boundaries. |
| `syntropic_router.py` | [D/I] | Router scaffold for session records, lane locks, and Soma-event logs; local runtime state is not doctrine. |

## Authority Rule

These scripts maintain agent-facing surfaces, but they do not become doctrine.
If generated or batch-written output conflicts with upstream source truth, fix
the owning source lane first and rerun the utility.

## AGENTS.md Generator

`generate_agents_md.py` is dry-run first:

```bash
python3 01_EMERGENTISM/09_TOOLS/07_AGENT_OPS/generate_agents_md.py --max-depth 2
python3 01_EMERGENTISM/09_TOOLS/07_AGENT_OPS/generate_agents_md.py --max-depth 2 --write
python3 01_EMERGENTISM/09_TOOLS/07_AGENT_OPS/generate_agents_md.py --max-depth 4 --only-prefix 02_SKYZAI/01_NOOSPHERE/02_INFRASTRUCTURE/Cascade
python3 01_EMERGENTISM/09_TOOLS/07_AGENT_OPS/generate_agents_md.py --max-depth 4 --only-prefix 02_SKYZAI/01_NOOSPHERE/02_INFRASTRUCTURE/Cascade --write --refresh-generated
```

Use the dry run as the subfolder navigation inventory. Use `--write` only after
reviewing the planned files and confirming they are owner-lane route surfaces,
not generated output, vendor trees, or cold archives. Use `--refresh-generated`
only to repair files that this utility previously generated; hand-authored
`AGENTS.md` files are skipped.

## Route Upstream

- tool inventory: `../README.md` and `../CLAUDE.md`
- agent grammar: `../../11_UPLINK/00_CORE/06_AGENTS.md`
- agent runtime resolutions: `../../11_UPLINK/00_CORE/06c_AGENTS_RESOLUTIONS_v3.md`
- organism routing: `../../../02_SKYZAI/01_NOOSPHERE/AGENTS.md`

## Router Surface

- `syntropic_router.py` is the first tracked router scaffold.
- It owns session records, lane locks, and Soma-event logging at runtime.
- Lane home registries live with their owning organ/entity in `LANES.md`.
- Runtime state is local, not doctrine; if state conflicts with canon, fix the canon lane first.
