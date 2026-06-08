---
rosetta:
  primary_level: L4
  primary_column: Deployment Front Door
  secondary:
    - level: L3
      column: Receipt Discipline
      role: "index which deployment surfaces are instructions versus verified receipts"
    - level: L5
      column: Operations Topology
      role: "map scripts, compose assets, summaries, and quickstarts without asserting runtime truth"
    - level: L6
      column: Public Claim Boundary
      role: "route current live/safe/approved status to the organism runtime truth file"
  operator: "Arjuna ⚔"
  tier: "God"
  regime: "Kṣatriya"
  register: "[B/D/I]"
  canonical_phrase: "05_DEPLOY"
title: "05_DEPLOY"
status: "ACTIVE — deployment front door"
evidence_tier: "[B] for dated deploy/build receipts; [D] for unrun plans and commands; [I] for operational interpretation."
---

# 05_DEPLOY

Deployment scripts, Docker assets, environment setup helpers, and operational
quickstarts for running bounded parts of the stack.

## What Belongs Here

- Dockerfiles and compose definitions
- deployment shell scripts
- environment/bootstrap helpers
- deployment summaries and quickstart notes

## What Does Not

- public/runtime truth claims
- product strategy
- doctrine about what is live

## Authority Rule

This folder tells you how something can be deployed, not whether it is live,
approved, or safe to claim publicly. For present-tense runtime status, route to
`../../../02_SKYZAI/01_NOOSPHERE/ORGANISM_RUNTIME_TRUTH.md`.

## Path Freshness Gate

Some deployment assets in this folder still contain retired `SKYZAI_ORG/...`
paths. Do not run `DEPLOY_MASTER.sh`, `docker-compose.yml`, or copied commands
from summary files until the target paths have been refreshed to canonical
`02_SKYZAI/...` routes and the run has a dated health receipt.

## Current Deployment Inventory

| Surface | Status |
|---|---|
| `setup_env.sh` | [D] Local environment bootstrap helper; run only after reviewing generated secrets and paths. |
| `DEPLOY_MASTER.sh` | [D] Multi-target deployment script; blocked pending canonical path refresh. |
| `health_check.sh` | [D] Verification helper; output becomes `[B]` only when dated and captured. |
| `docker-compose.yml` / `Dockerfile.heartbeat` | [D] Local service topology assets; compose paths require canonical refresh before use. |
| `QUICKSTART.md` / `README-DEPLOYMENT.md` | [I] Operator runbooks with planned outcomes unless paired with dated checks. |
| `DEPLOYMENT_SUMMARY.md` | [I] Sprint-era deployment summary; bounded by the runtime-truth file. |

## Route Upstream

- parent tool inventory: `../README.md` and `../CLAUDE.md`
- organism runtime truth: `../../../02_SKYZAI/01_NOOSPHERE/ORGANISM_RUNTIME_TRUTH.md`
- rooted organism routing: `../../11_UPLINK/00_CORE/03_ORGANISM.md`
