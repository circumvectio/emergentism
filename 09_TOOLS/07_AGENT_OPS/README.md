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

> **Tool boundary.** These are repository-maintenance aids. They do not encode
> product/runtime governance and cannot authorize or define Emergentist claims.

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

## Current Inventory

| Surface | Tier | Role |
|---|---|---|
| `generate_agents_md.py` | [D/B] | Dry-run/write generator for route cards; dry-run output is a plan, written files require owner-lane review. |

The remaining utilities formerly listed here were moved out of the
pure-Emergentism boundary on 2026-07-20 and are preserved under
[`../../90_ARCHIVE/pure_emergentism_boundary_2026_07_20/09_TOOLS/07_AGENT_OPS/`](../../90_ARCHIVE/pure_emergentism_boundary_2026_07_20/09_TOOLS/07_AGENT_OPS/).

## Authority Rule

These scripts maintain agent-facing surfaces, but they do not become doctrine.
If generated or batch-written output conflicts with upstream source truth, fix
the owning source lane first and rerun the utility.

## AGENTS.md Generator

`generate_agents_md.py` is dry-run first:

```bash
python3 01_EMERGENTISM/09_TOOLS/07_AGENT_OPS/generate_agents_md.py --max-depth 2
python3 01_EMERGENTISM/09_TOOLS/07_AGENT_OPS/generate_agents_md.py --max-depth 2 --write
python3 09_TOOLS/07_AGENT_OPS/generate_agents_md.py --max-depth 3 --only-prefix 05_COSMOLOGY
python3 09_TOOLS/07_AGENT_OPS/generate_agents_md.py --max-depth 3 --only-prefix 05_COSMOLOGY --write --refresh-generated
```

Use the dry run as the subfolder navigation inventory. Use `--write` only after
reviewing the planned files and confirming they are owner-lane route surfaces,
not generated output, vendor trees, or cold archives. Use `--refresh-generated`
only to repair files that this utility previously generated; hand-authored
`AGENTS.md` files are skipped.

## Route Upstream

- tool inventory: `../README.md` and `../CLAUDE.md`
- Uplink route map: `../../11_UPLINK/README.md` and
  `../../11_UPLINK/00_THE_UPLINK.md`
- worldview routing: `../../AGENTS.md`
