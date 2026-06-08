---
rosetta:
  primary_level: L5
  primary_column: Tooling Architecture
  secondary:
    - level: L6
      column: Compression Layer
      role: "strip generated output to evidence-bearing summaries without letting it become source authority"
    - level: L4
      column: Runtime Execution
      role: "hold scripts, deploy configs, and one-file utilities as operational surfaces"
    - level: L3
      column: Validation
      role: "route manifest, link, environment, and audit helpers through receipt discipline"
  operator: "Brahmā ○"
  tier: "Executive"
  regime: "Brāhmaṇa"
  register: "[B/S/I]"
  canonical_phrase: "09_TOOLS — Tooling Front Door"
title: "09_TOOLS — Tooling Architecture"
status: "ACTIVE — tooling front door"
evidence_tier: "[B] for local tool inventory; [S] for source-authority boundary; [I] for organization notes."
---

# 09_TOOLS — Tooling Architecture

> Scripts, compilers, data pipelines, deployment configs. The instruments that strip to essence.

See `CLAUDE.md` in this directory for the full tool inventory and usage.

## Authority Rule

- tools compile, lint, summarize, and deploy
- tools do not become the doctrine authority just because they can emit a file
- when generated output and source docs disagree, repair the owning source and rerun the tool
- use tooling to compress the rows, not to silently redefine what a row owns

## Agentz Deployment Control

The 2026-06-04 Agentz deployment receipt for this lane is
[`../00_META/03_AGENTZ_DEPLOYMENT_09_TOOLS_2026_06_04.md`](../00_META/03_AGENTZ_DEPLOYMENT_09_TOOLS_2026_06_04.md);
the exact folder/file manifest is
[`../00_META/03_AGENTZ_DEPLOYMENT_09_TOOLS_2026_06_04.csv`](../00_META/03_AGENTZ_DEPLOYMENT_09_TOOLS_2026_06_04.csv).
It includes active scripts, compilers, simulations, deploy helpers, packages,
agent ops, sprint gates, and cold tooling memory. Tool output remains evidence
or generated summary, not doctrine authority.

Key tools:
- `01_SCRIPTS/compile_uplink.py` — compile Uplink from source docs
- `01_SCRIPTS/compile_state.py` — auto-generate 09_STATE.md
- `01_SCRIPTS/rosetta_propose.py` — propose reviewed Rosetta frontmatter manifests without writing target docs
- `01_SCRIPTS/rosetta_annotate.py` — audit/apply reviewed Rosetta frontmatter manifests
- `01_SCRIPTS/rosetta_index.py` — generate Rosetta navigation indexes from existing frontmatter
- `01_SCRIPTS/check_phase1_env.py` — validate `.env.phase1`, gitignore coverage, and Stage 0 decision-log presence
- `01_SCRIPTS/run_backbone_tests.py` — backbone test suite
- `03_SIMULATIONS/spectrum_sphere.py` — weighted sphere-spectrum baseline for the hardening packet
- `03_SIMULATIONS/spectrum_flat_1d_cosh.py` — flat 1D `cosh` control for operator comparison
- `05_DEPLOY/` — Docker and deployment configs

## Local Organization

- `01_SCRIPTS/` holds active one-file repository utilities.
- `02_COMPILERS/` holds corpus and Uplink compiler utilities.
- `03_SIMULATIONS/` holds the DAC harness, scenario fixtures, and standalone research/spectrum simulations.
- `04_DATA_PIPELINES/` holds data ingestion and transformation scripts.
- `05_DEPLOY/` holds Docker and deployment configs.
- `06_PACKAGES/` holds reusable shared libraries.
- `07_AGENT_OPS/` holds agent operation utilities.
- `08_AUDIT_ARTIFACTS/` stores audit outputs and helpers; outputs are evidence, not authority.
- `09_DAC_FRAME/scripts/` and `09_DAC_FRAME/tools/` are scoped to DAC-frame work only.
- `10_SPRINT_GATES/` holds sprint-gate packaging and digest utilities.
- `90_ARCHIVE/` is cold tooling memory and should not be used as the active command surface.

Zero-Sum Resolution Equation
