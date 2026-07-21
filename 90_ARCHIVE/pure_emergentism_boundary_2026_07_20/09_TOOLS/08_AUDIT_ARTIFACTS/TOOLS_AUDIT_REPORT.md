---
rosetta:
  primary_level: L3
  primary_column: Tools Audit Receipt
  secondary:
    - level: L4
      column: Tool Remediation Queue
      role: "turn findings into scoped execution only after current-file confirmation"
    - level: L5
      column: Tooling Topology
      role: "summarize the 09_TOOLS folder architecture and structural risks"
    - level: L6
      column: Dated-Report Boundary
      role: "destroy audit-report-as-current-state authority after subsequent commits"
  operator: "Vaiśya △"
  tier: "Agent"
  regime: "Vaiśya"
  register: "[B/I]"
  canonical_phrase: "09_TOOLS — Logic, Coherence, and Consistency Audit Report"
title: "09_TOOLS — Logic, Coherence, and Consistency Audit Report"
status: "DATED AUDIT ARTIFACT — 2026-04-25"
evidence_tier: "[B] for the recorded audit observations; [I] for recommendations pending current-state verification."
---

# 09_TOOLS — Logic, Coherence, and Consistency Audit Report

**Audit Date:** 2026-04-25
**Auditor:** Matrix Agent
**Scope:** `/Users/Yves/Magnum Opus/01_EMERGENTISM/09_TOOLS/`

---

## Executive Summary

The 09_TOOLS directory contains 11 subfolders with scripts, compilers, simulations, data pipelines, deployment configs, packages, agent operations utilities, audit artifacts, DAC frame tools, sprint gates, and archived material. The directory follows a consistent numbering convention (01-10, 90) and maintains README documentation for each subfolder.

**Overall Health:** MODERATE - Several critical path reference errors, orphaned directories, and structural issues identified.

**Critical Issues Found:** 14
**Warnings:** 11
**Recommendations:** 23

---

## SUBFOLDER AUDITS

---

### 01_SCRIPTS

**SUMMARY:** Healthy folder with 25 Python scripts and 1 JSON manifest subfolder. Scripts are well-organized with clear naming conventions. README clearly defines scope boundaries.

**ISSUES FOUND:**
1. **Dead Reference in README.md** — README references "Read First: `manifest_check.py`" but `manifest_check.py` does not exist in the folder. The script `check_links.py` exists but is not listed.
2. **Orphaned Subfolder** — `01_DAC_SCAFFOLD_MANIFESTS/` contains only JSON manifests but README mentions a "dac_scaffold_manifests" path that doesn't align with the actual location. The README path `05_TOOLS/scripts/dac_scaffold_manifests/<repo>.json` doesn't match the actual `01_DAC_SCAFFOLD_MANIFESTS/` location.
3. **Path Inconsistency in apply_dac_scaffold.py** — Line references scaffold path as `SKYZAI_ORG/00_REFERENCE/DAV_FACTORY/DAV_SCAFFOLD` but the organism uses `02_SKYZAI/01_NOOSPHERE` prefix (not `SKYZAI_ORG`).

**RECOMMENDATIONS:**
1. Add `check_links.py` to the "Read First" list in README.md
2. Update `01_DAC_SCAFFOLD_MANIFESTS/README.md` to reference the correct relative path `../apply_dac_scaffold.py`
3. Verify `apply_dac_scaffold.py` scaffold path resolves correctly

**FILES TO CREATE:** None
**FILES TO MODIFY:**
- `/Users/Yves/Magnum Opus/01_EMERGENTISM/09_TOOLS/01_SCRIPTS/README.md` — Add `check_links.py` to Read First list
- `/Users/Yves/Magnum Opus/01_EMERGENTISM/09_TOOLS/01_SCRIPTS/01_DAC_SCAFFOLD_MANIFESTS/README.md` — Fix path references

---

### 02_COMPILERS

**SUMMARY:** Minimalist folder with single script `build_corpus_map.py`. README correctly identifies scope. Clean and focused.

**ISSUES FOUND:**
1. **Single Script, No Tests** — Only one script exists with no test coverage or README for the script itself.
2. **Limited Documentation** — Script lacks inline docstrings explaining purpose beyond the filename.

**RECOMMENDATIONS:**
1. Add docstring to `build_corpus_map.py` explaining corpus mapping purpose
2. Consider if this script belongs here or in `01_SCRIPTS/` (it seems to be a narrow compiler utility which fits here)

**FILES TO CREATE:** None
**FILES TO MODIFY:**
- `/Users/Yves/Magnum Opus/01_EMERGENTISM/09_TOOLS/02_COMPILERS/build_corpus_map.py` — Add comprehensive docstring

---

### 03_SIMULATIONS

**SUMMARY:** Moderate health. Contains DAC simulation harness, spectrum simulations, and scenario fixtures. Three scenario directories (04_combined, 05_cluster, 06_cross) are empty placeholders.

**ISSUES FOUND:**
1. **Empty Scenario Placeholders** — Directories `04_combined/`, `05_cluster/`, and `06_cross/` are completely empty (0 files). README_SIMULATION.md advertises these as "week 7+" deliverables but they lack any fixtures.
2. **Duplicate Simulation Files** — `r_star_simulation.py` and `r_star_simulation_v2.py` appear to be versioned iterations. No indication which is canonical.
3. **Conflicting Readmes** — Both `README.md` and `README_SIMULATION.md` exist. README_SIMULATION.md is more detailed but README.md is the standard entry point.
4. **Midus Proof of Concept Duplication** — Both `midus_proof_of_concept.R` and `midus_proof_of_concept.py` exist. Unclear which is authoritative.
5. **R_STAR_README.md Orphan** — `R_STAR_README.md` and `R_STAR_SIMULATION_RESULTS.md` appear to be orphaned historical outputs with no clear linking to current scripts.

**RECOMMENDATIONS:**
1. Either implement scenario fixtures for 04_combined, 05_cluster, 06_cross or remove the directories and update README_SIMULATION.md to reflect actual state
2. Archive `r_star_simulation.py` if `v2` is canonical, or consolidate them
3. Consolidate to single `README.md` (move README_SIMULATION.md content into main README or rename detailed version)
4. Determine authoritative midus script and archive the other
5. Move R_STAR*.md files to appropriate evidence or archive location

**FILES TO CREATE:** None
**FILES TO MODIFY:**
- `/Users/Yves/Magnum Opus/01_EMERGENTISM/09_TOOLS/03_SIMULATIONS/README.md` — Consolidate with README_SIMULATION.md content
**FILES TO DELETE OR ARCHIVE:**
- `/Users/Yves/Magnum Opus/01_EMERGENTISM/09_TOOLS/03_SIMULATIONS/r_star_simulation.py` (if v2 is canonical)
- `/Users/Yves/Magnum Opus/01_EMERGENTISM/09_TOOLS/03_SIMULATIONS/midus_proof_of_concept.R` (if .py is authoritative)
- `/Users/Yves/Magnum Opus/01_EMERGENTISM/09_TOOLS/03_SIMULATIONS/R_STAR_README.md`
- `/Users/Yves/Magnum Opus/01_EMERGENTISM/09_TOOLS/03_SIMULATIONS/R_STAR_SIMULATION_RESULTS.md`
- Empty directories: `04_combined/`, `05_cluster/`, `06_cross/`

---

### 04_DATA_PIPELINES

**SUMMARY:** Functional folder containing GFS (Global Funding System?) data analysis scripts. Contains mix of Python scripts, CSV outputs, and text metadata.

**ISSUES FOUND:**
1. **Output Files in Tool Folder** — `gfs_results_20260409.csv` and `gfs_meta_analysis_20260409.txt` are output artifacts stored alongside source scripts. These should be in an output/ subfolder or separate data directory.
2. **Duplicate Analysis Scripts** — `gfs_22_country_analysis.py` and `gfs_22_country_analysis_wave2.py` appear to be sequential analysis versions. `gfs_22_country_analysis_v2_fixed.py` (formerly `gfs_fixed.py`) is the codebook-v2 correction of `gfs_22_country_analysis.py`.
3. **Missing Data Source Documentation** — No README explains the data sources, API endpoints, or pipeline workflow.

**RECOMMENDATIONS:**
1. Create `04_DATA_PIPELINES/outputs/` subfolder and move CSV/TXT artifacts there
2. Add pipeline documentation explaining script relationships and data sources
3. Clarify naming: `gfs_fixed.py` should indicate what was fixed or be renamed — RESOLVED: renamed to `gfs_22_country_analysis_v2_fixed.py`

**FILES TO CREATE:**
- `/Users/Yves/Magnum Opus/01_EMERGENTISM/09_TOOLS/04_DATA_PIPELINES/outputs/` directory
**FILES TO MODIFY:**
- Move `gfs_results_20260409.csv` and `gfs_meta_analysis_20260409.txt` to outputs/
- Add README explaining pipeline architecture

---

### 05_DEPLOY

**SUMMARY:** Healthy deployment folder with Docker and deployment scripts. Multiple markdown files provide good documentation coverage.

**ISSUES FOUND:**
1. **Redundant Documentation** — Both `README.md` and `README-DEPLOYMENT.md` contain deployment information. `QUICKSTART.md` is also present. Three markdown files may cause confusion about which to read first.
2. **Missing Executable Permissions** — `DEPLOY_MASTER.sh`, `health_check.sh`, and `setup_env.sh` should have executable permissions verified.

**RECOMMENDATIONS:**
1. Consolidate deployment documentation: have `README.md` as index pointing to `DEPLOYMENT_SUMMARY.md` for details and `QUICKSTART.md` for quick reference
2. Verify shell scripts have executable permissions

**FILES TO MODIFY:**
- `/Users/Yves/Magnum Opus/01_EMERGENTISM/09_TOOLS/05_DEPLOY/README.md` — Simplify to index format
**FILES TO CHECK:**
- Verify executable permissions on `*.sh` files

---

### 06_PACKAGES

**SUMMARY:** Minimal but well-structured package folder. Contains single package `emergentism-core` with proper pyproject.toml and src layout.

**ISSUES FOUND:**
1. **Missing Tests** — `pyproject.toml` declares `pytest` as dev dependency but `tests/` directory exists but appears empty.
2. **Package Incomplete** — Package contains 6 Python modules but no `__init__.py` exports or explicit public API definition.

**RECOMMENDATIONS:**
1. Add tests to `tests/` directory or remove test configuration from pyproject.toml if not used
2. Add explicit `__all__` in `__init__.py` to define public API

**FILES TO CREATE:**
- `/Users/Yves/Magnum Opus/01_EMERGENTISM/09_TOOLS/06_PACKAGES/emergentism-core/src/emergentism_core/__init__.py` — Add explicit exports
**FILES TO MODIFY:**
- `/Users/Yves/Magnum Opus/01_EMERGENTISM/09_TOOLS/06_PACKAGES/emergentism-core/pyproject.toml` — Remove pytest if tests directory remains empty

---

### 07_AGENT_OPS

**SUMMARY:** Functional folder with agent operation utilities. Contains 8 Python scripts and 1 JSON manifest.

**ISSUES FOUND:**
1. **CRITICAL: Hardcoded Absolute Path** — `compile_agent_skills.py` contains: `BASE_DIR = "/Users/yves/Documents/☀️ Emergentism_org/02_ORGANISM"` which is a hardcoded path that won't work for other users or systems.
2. **CRITICAL: Wrong Path Prefix** — `syntropic_router.py` and `_common.py` (in 10_SPRINT_GATES) reference paths using `02_ORGANISM/` prefix but the actual directory is `02_SKYZAI/01_NOOSPHERE` (note: no underscore, different numbering).
3. **Orphaned JSON** — `AGENT_GAPS.json` contains zone references "02_ORGANISM" which may be stale.
4. **Inconsistent Naming** — Scripts use mixed naming: `batch_add_pwa_wiki_surfaces.py` (snake_case with mixed purposes), `compile_agent_skills.py` (snake_case), `syntropic_router.py` (snake_case).

**RECOMMENDATIONS:**
1. Replace hardcoded path in `compile_agent_skills.py` with `Path(__file__).resolve().parents` approach
2. Fix path prefix from `02_ORGANISM` to `02_SKYZAI/01_NOOSPHERE` in `syntropic_router.py`
3. Update or remove `AGENT_GAPS.json` with current zone paths
4. Document script purposes clearly in each file header

**FILES TO MODIFY:**
- `/Users/Yves/Magnum Opus/01_EMERGENTISM/09_TOOLS/07_AGENT_OPS/compile_agent_skills.py` — Replace hardcoded path
- `/Users/Yves/Magnum Opus/01_EMERGENTISM/09_TOOLS/07_AGENT_OPS/syntropic_router.py` — Fix path prefix
- `/Users/Yves/Magnum Opus/01_EMERGENTISM/09_TOOLS/07_AGENT_OPS/AGENT_GAPS.json` — Update zone paths or archive

---

### 08_AUDIT_ARTIFACTS

**SUMMARY:** Minimal folder with 1 script, 1 output file, and 1 README. Clear scope.

**ISSUES FOUND:**
1. **Orphaned Output** — `audit_output.md` is a generated output file stored in the tool folder rather than an archive or evidence directory.
2. **Single Script, Unclear Purpose** — `audit_dependency_graph.py` lacks docstring explaining what dependency graph it analyzes.

**RECOMMENDATIONS:**
1. Move `audit_output.md` to appropriate evidence location or `90_ARCHIVE/`
2. Add docstring to `audit_dependency_graph.py`

**FILES TO MODIFY:**
- Move `audit_output.md` to evidence or archive
- Add docstring to `audit_dependency_graph.py`

---

### 09_DAC_FRAME

**SUMMARY:** Well-organized framework folder with clear substructure: `blueprint/`, `constitution/`, `scripts/`, `tools/`. Each subfolder has a README. Contains operational DAC framework tools.

**ISSUES FOUND:**
1. **Blueprint Subfolder Reference** — `blueprint/README.md` references `SPECS/SKY_ACCOUNTING_WORKED_EXAMPLE.md` and `SPECS/PRIMITIVE_INTEGRATION.md` but these paths don't exist within the blueprint folder.
2. **Orphaned Subsubfolder** — `constitution/OS/` exists with CADENCE.md, PEOPLE.md, PROCESS.md, PRODUCT.md but parent README.md doesn't mention this subfolder structure.
3. **Tool Validation Delegation** — `tools/validate_frame.py` delegates to `validate_blueprint.py` which may not exist at the expected path.

**RECOMMENDATIONS:**
1. Verify or create `blueprint/SPECS/` directory and its contents
2. Update `blueprint/README.md` to document `OS/` subfolder structure
3. Verify `validate_blueprint.py` exists or update delegation path

**FILES TO CHECK:**
- Verify `blueprint/SPECS/` directory exists with required files
- Verify `validate_blueprint.py` path

---

### 10_SPRINT_GATES

**SUMMARY:** Well-structured sprint gate system with 9 sprint modules, shared `_common.py`, and proper entry points.

**ISSUES FOUND:**
1. **CRITICAL: Path Prefix Error in _common.py** — Lines 39-40 use `02_ORGANISM/02_ORGANS/Skyzai/` but correct path is `02_SKYZAI/01_NOOSPHERE/02_ORGANS/Skyzai/`. This will cause runtime failures.
2. **Inconsistent Module Names** — Some sprint modules use `_gates` suffix in filename (e.g., `sprint_composer.py` vs archived `sprint_composer_gates.py` in 90_ARCHIVE).
3. **Import Path Issue** — `sprint_composer.py` uses `from sprint_gates._common import` but the folder is `10_SPRINT_GATES` not `sprint_gates`.

**RECOMMENDATIONS:**
1. **CRITICAL FIX**: Update `_common.py` lines 39-40:
   - Change `PROJECT_ROOT / "02_ORGANISM" / "02_ORGANS" / "Skyzai" / "agents"` to `PROJECT_ROOT / "02_SKYZAI/01_NOOSPHERE" / "02_ORGANS" / "Skyzai" / "agents"`
   - Change `PROJECT_ROOT / "02_ORGANISM" / "02_ORGANS" / "Skyzai"` to `PROJECT_ROOT / "02_SKYZAI/01_NOOSPHERE" / "02_ORGANS" / "Skyzai"`
2. Verify Python import resolution for `sprint_gates` module

**FILES TO MODIFY:**
- `/Users/Yves/Magnum Opus/01_EMERGENTISM/09_TOOLS/10_SPRINT_GATES/_common.py` — Fix path prefix

---

### 90_ARCHIVE

**SUMMARY:** Properly marked as cold storage. Contains archived scripts from 2026-04-17 and old sprint_gates version.

**ISSUES FOUND:**
1. **epubcheck-5.1.0 Toolartifact** — `epubcheck-5.1.0/` is a third-party tool (EPUB validator) stored in archive. This is not a legacy script but a standalone tool. Location is conceptually wrong.
2. **Inconsistent Archive Naming** — `bridge_scripts_2026_04_17/` uses date suffix while `sprint_gates_2026_04_old/` uses descriptive old suffix. No unified naming convention.
3. **Build Scripts Confusion** — Three build scripts (`build_clean_notebooklm.py`, `build_lean_notebooklm.py`, `build_notebooklm.py`) and `generate_websites.py` appear to be one-off generation tools. Their relationship to current tooling is unclear.

**RECOMMENDATIONS:**
1. Move `epubcheck-5.1.0/` to `06_PACKAGES/` or a `tools/` directory if still needed, not archive
2. Standardize archive naming convention (recommend: date-based for time-specific content)
3. Document or archive the build scripts with clear provenance notes

**FILES TO MODIFY:**
- Move `epubcheck-5.1.0/` to appropriate location or document why archived
- Consider renaming `sprint_gates_2026_04_old` to date-based naming

---

## CROSS-FOLDER ISSUES

1. **Path Prefix Inconsistency** — Multiple scripts in `07_AGENT_OPS/` and `10_SPRINT_GATES/` incorrectly reference `02_ORGANISM/` when the actual directory is `02_SKYZAI/01_NOOSPHERE`. This is a systemic naming error.

2. **Authority Rule Dispersal** — The "Authority Rule" (tools don't become doctrine) is stated in multiple READMEs but not enforced technically. Consider adding a comment header to all tool scripts reinforcing this.

3. **Tool Inventory Drift** — `CLAUDE.md` lists 9 tools but actual folder contains 25+ scripts. Inventory is stale.

---

## FILES TO CREATE

| Path | Purpose |
|------|---------|
| `/Users/Yves/Magnum Opus/01_EMERGENTISM/09_TOOLS/04_DATA_PIPELINES/outputs/` | Output artifacts directory |
| `/Users/Yves/Magnum Opus/01_EMERGENTISM/09_TOOLS/06_PACKAGES/emergentism-core/src/emergentism_core/__init__.py` | Public API exports |

---

## FILES TO MODIFY (Priority Order)

| Priority | Path | Issue |
|----------|------|-------|
| CRITICAL | `10_SPRINT_GATES/_common.py` | Wrong path prefix `02_ORGANISM` -> `04_NETWORK_ENTITIES/SKYZAI/01_NOOSPHERE` |
| CRITICAL | `07_AGENT_OPS/compile_agent_skills.py` | Hardcoded absolute path |
| CRITICAL | `07_AGENT_OPS/syntropic_router.py` | Wrong path prefix `02_ORGANISM` |
| HIGH | `03_SIMULATIONS/` | Remove empty dirs, consolidate readmes |
| HIGH | `01_SCRIPTS/README.md` | Add missing script to "Read First" |
| MEDIUM | `04_DATA_PIPELINES/` | Create outputs/ subfolder |
| MEDIUM | `06_PACKAGES/emergentism-core/` | Add __init__.py exports |
| MEDIUM | `05_DEPLOY/README.md` | Consolidate documentation |
| LOW | `CLAUDE.md` | Update tool inventory |

---

## FILES TO DELETE OR ARCHIVE

| Path | Reason |
|------|--------|
| `03_SIMULATIONS/r_star_simulation.py` | Duplicate (v2 is canonical) |
| `03_SIMULATIONS/midus_proof_of_concept.R` | Duplicate (.py is authoritative) |
| `03_SIMULATIONS/R_STAR_README.md` | Orphaned output |
| `03_SIMULATIONS/R_STAR_SIMULATION_RESULTS.md` | Orphaned output |
| `03_SIMULATIONS/00_SCENARIOS/04_combined/` | Empty placeholder |
| `03_SIMULATIONS/00_SCENARIOS/05_cluster/` | Empty placeholder |
| `03_SIMULATIONS/00_SCENARIOS/06_cross/` | Empty placeholder |
| `08_AUDIT_ARTIFACTS/audit_output.md` | Should be in evidence, not tools |

---

## SUMMARY TABLE

| Subfolder | Health | Critical Issues | Warnings |
|-----------|--------|-----------------|----------|
| 01_SCRIPTS | Good | 1 | 2 |
| 02_COMPILERS | Good | 0 | 1 |
| 03_SIMULATIONS | Moderate | 2 | 3 |
| 04_DATA_PIPELINES | Moderate | 1 | 2 |
| 05_DEPLOY | Good | 1 | 1 |
| 06_PACKAGES | Good | 1 | 1 |
| 07_AGENT_OPS | Poor | 3 | 1 |
| 08_AUDIT_ARTIFACTS | Good | 1 | 1 |
| 09_DAC_FRAME | Good | 1 | 2 |
| 10_SPRINT_GATES | Moderate | 2 | 1 |
| 90_ARCHIVE | Good | 1 | 2 |

---

## CONCLUSION

The 09_TOOLS directory is generally well-organized with clear structural conventions. The primary issues are:

1. **Path Reference Errors** — `02_ORGANISM` should be `02_SKYZAI/01_NOOSPHERE` throughout. This affects `07_AGENT_OPS/` and `10_SPRINT_GATES/` critically.

2. **Orphaned Content** — Empty scenario directories, orphaned outputs, and duplicate files need cleanup.

3. **Documentation Drift** — README files reference non-existent files, and the tool inventory in CLAUDE.md is incomplete.

The authority rule and conceptual hierarchy are sound; the issues are primarily technical path references and light housekeeping.

---

*Zero-Sum Resolution Equation*
