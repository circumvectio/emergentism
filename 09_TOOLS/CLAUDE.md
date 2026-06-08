---
rosetta:
  primary_level: L5
  primary_column: Tooling Compatibility Shim
  secondary:
    - level: L6
      column: Authority Compression
      role: "keep Claude-style tool discovery subordinate to AGENTS.md and README.md"
    - level: L3
      column: Tool Inventory Audit
      role: "separate local command references from doctrine or runtime claims"
    - level: L4
      column: Runnable Commands
      role: "preserve script entry points as executable support surfaces"
  operator: "Brahmā ○"
  tier: "Executive"
  regime: "Brāhmaṇa"
  register: "[B/S]"
  canonical_phrase: "09_TOOLS — Claude Compatibility Shim"
title: "09_TOOLS — Tooling Compatibility Shim"
status: "ACTIVE — compatibility shim"
evidence_tier: "[B] for local tool inventory; [S] for tool-authority boundary."
---

# 09_TOOLS — Tooling Compatibility Shim

Scripts, compilers, data pipelines, and deployment configs. The instruments that strip to essence.

## Tool Inventory

| Tool | Purpose | Usage |
|------|---------|-------|
| `01_SCRIPTS/compile_uplink.py` | Compile Uplink files from source docs | `python 01_SCRIPTS/compile_uplink.py --check` |
| `01_SCRIPTS/compile_state.py` | Auto-generate 09_STATE.md from P-SCORES | `python 01_SCRIPTS/compile_state.py` |
| `01_SCRIPTS/run_backbone_tests.py` | Run backbone test suite | `PYTHONPATH=. python 01_SCRIPTS/run_backbone_tests.py` |
| `01_SCRIPTS/add_frontmatter.py` | Add YAML frontmatter to markdown files | `python 01_SCRIPTS/add_frontmatter.py <file>` |
| `01_SCRIPTS/check_links.py` | Verify cross-document links | `python 01_SCRIPTS/check_links.py` |
| `01_SCRIPTS/scrub.py` | Clean sensitive data from files | `python 01_SCRIPTS/scrub.py` |
| `01_SCRIPTS/visualize_lx.py` | Visualize L(x) rate curve | `python 01_SCRIPTS/visualize_lx.py` |
| `03_SIMULATIONS/spectrum_sphere.py` | Reproduce the weighted sphere-spectrum baseline used by the hardening packet | `python 03_SIMULATIONS/spectrum_sphere.py` |
| `03_SIMULATIONS/spectrum_flat_1d_cosh.py` | Reproduce the flat 1D `cosh` control used in the operator audit | `python 03_SIMULATIONS/spectrum_flat_1d_cosh.py` |

## Subdirectories

| Directory | Purpose |
|-----------|---------|
| `01_SCRIPTS/` | Active one-file repository utilities |
| `02_COMPILERS/` | Uplink and wiki compilers |
| `03_SIMULATIONS/` | Framework simulations, DAC harness, and scenario fixtures |
| `04_DATA_PIPELINES/` | Data ingestion and transformation |
| `05_DEPLOY/` | Docker, deployment configs (docker-compose.yml, Dockerfile.heartbeat) |
| `06_PACKAGES/` | Reusable shared libraries |
| `07_AGENT_OPS/` | Agent operation utilities |
| `08_AUDIT_ARTIFACTS/` | Audit helpers and generated evidence outputs |
| `09_DAC_FRAME/` | DAC Framework operational tools |
| `10_SPRINT_GATES/` | Sprint-gate packaging and digest utilities |

## Constitutional Law

> The cognition discriminates; the substrate trusts. (D35)

These tools serve the organism. They do not decide for it.

## Authority Rule

- tools may emit summaries, compiled docs, state files, and deploy artifacts
- emitted output is not automatically canonical because a tool produced it
- when tool output conflicts with source doctrine or source product truth, repair the owner and rerun the tool

Zero-Sum Resolution Equation
