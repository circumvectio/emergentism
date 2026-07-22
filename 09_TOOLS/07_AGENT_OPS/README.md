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

This folder holds one script. It supports:

- depth-aware `AGENTS.md` scaffold generation

Execution-surface validation, batch PWA/tools surface creation, agent skill
compilation, compaction and Rosetta loading helpers, and syntropic router
scaffolding are **no longer capabilities of this lane**; those scripts were moved
on 2026-07-20 and are retained in the
[pure-boundary archive](../../90_ARCHIVE/pure_emergentism_boundary_2026_07_20/09_TOOLS/07_AGENT_OPS/).

## Current Inventory

| Surface | Tier | Role |
|---|---|---|
| `generate_agents_md.py` | [D/B] | Dry-run/write generator for route cards; dry-run output is a plan, written files require owner-lane review. |

**Corrected 2026-07-22.** This table previously named ten surfaces as present.
Nine of them — `execution_surface_validator.py`, `AGENT_GAPS.json`,
`batch_add_pwa_wiki_surfaces.py`, `batch_add_tools_surfaces.py`,
`compile_agent_skills.py`, `agent_framework_integration.py`,
`auto_compaction.py`, `rosetta_loader.py`, `syntropic_router.py` — were moved to
the pure-boundary archive on 2026-07-20 and are preserved byte-intact at
[`../../90_ARCHIVE/pure_emergentism_boundary_2026_07_20/09_TOOLS/07_AGENT_OPS/`](../../90_ARCHIVE/pure_emergentism_boundary_2026_07_20/09_TOOLS/07_AGENT_OPS/).
Counted by testing each of the ten backticked names against this folder:
1 present, 9 absent. The parent lane README already reports the corrected state.

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
- agent grammar: **archived provenance, not live routing authority** — `06_AGENTS.md`
  left `11_UPLINK/00_CORE/` on 2026-07-20; it now lives at
  [`../../90_ARCHIVE/pure_emergentism_boundary_2026_07_20/11_UPLINK/00_CORE/06_AGENTS.md`](../../90_ARCHIVE/pure_emergentism_boundary_2026_07_20/11_UPLINK/00_CORE/06_AGENTS.md)
- agent runtime resolutions: **archived provenance** — same pass, same date;
  [`../../90_ARCHIVE/pure_emergentism_boundary_2026_07_20/11_UPLINK/00_CORE/06c_AGENTS_RESOLUTIONS_v3.md`](../../90_ARCHIVE/pure_emergentism_boundary_2026_07_20/11_UPLINK/00_CORE/06c_AGENTS_RESOLUTIONS_v3.md)
- forwarding stub for both: [`../../11_UPLINK/00_CORE/README.md`](../../11_UPLINK/00_CORE/README.md)
  (that directory now contains only that stub)
- worldview routing: `../../AGENTS.md`

> **Corrected 2026-07-22.** The two `11_UPLINK/00_CORE/` bullets above previously
> named live upstream authorities. Counted by path test: 3 targets under that
> directory were cited across this lane's route cards (`06_AGENTS.md`,
> `06c_AGENTS_RESOLUTIONS_v3.md`, and `00_INDEX.md` in `../02_COMPILERS/README.md`);
> 0 are present. They were bare backticked paths, so the mechanical dead-citation
> and forwarding-stub gates did not see them.

## Router Surface

- `syntropic_router.py` was the first tracked router scaffold. **Archived
  2026-07-20** to
  [`../../90_ARCHIVE/pure_emergentism_boundary_2026_07_20/09_TOOLS/07_AGENT_OPS/syntropic_router.py`](../../90_ARCHIVE/pure_emergentism_boundary_2026_07_20/09_TOOLS/07_AGENT_OPS/syntropic_router.py);
  this lane currently has no router surface (corrected 2026-07-22).
- When it ran, it owned session records, lane locks, and Soma-event logging at runtime.
- Lane home registries live with their owning organ/entity in `LANES.md`.
- Runtime state is local, not doctrine; if state conflicts with canon, fix the canon lane first.
