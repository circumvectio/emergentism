---
rosetta:
  primary_level: L6
  primary_column: Archived Organism Root Fitness Assessment v1.0
  secondary:
    - level: L5
      column: Cross-Root Fitness Architecture
      role: "preserve the scoring model and ecosystem map as a dated artifact"
    - level: L3
      column: Metric Receipt Audit
      role: "treat filesystem/git metrics as dated, tool-assisted observations"
    - level: L4
      column: Priority Boundary
      role: "prevent old recommended actions from becoming current execution"
  operator: "Sādhu △"
  tier: "Titan"
  regime: "Sādhu"
  register: "[D/I]"
  canonical_phrase: "Archived organism root fitness assessment v1.0"
title: "Organism Root Fitness Assessment"
evidence_tier: "[D] archived dated assessment; [I] interpretive operational synthesis; tool metrics are historical inputs."
type: organism-assessment
date: 2026-05-04
status: ARCHIVED — Assessment v1.0
scope: Dated cross-root fitness assessment retained for provenance; not current health proof.
sources:
  - 01_EMERGENTISM/90_ARCHIVE/08_FRAMEWORK_SUPPORT/08_AGENTS/AGENTS.md
---


# Organism Root Fitness Assessment

> Applying the 7-caste agent framework + 5-dimension economic specialisation model to evaluate the six active roots of the Magnum Opus repository. Each root is treated as a "macro-chapter" with its own genotype emphasis, economic intensity profile, and fitness score.

**Rosetta boundary:** [D] This is a 2026-05-04 snapshot. Scores, file counts, and recommended actions require fresh scans before they can govern current work.

---

## Executive Summary

| Root | Fitness | Status | Dominant Caste | Dominant Economic | Key Risk |
|---|---|---|---|---|---|
| **01_EMERGENTISM** | **0.600** | HEALTHY | L5, L6, L7 | labour, knowledge | Archive bloat |
| **02_SKYZAI/06_SPECTRE** | **0.600** | DORMANT | L5, L6, L7 | capital | No runtime |
| **02_SKYZAI_ORG** | **0.357** | STRESSED | L1, L4, L5 | capital | Dependency bloat |
| **03_SKYZAI_COM** | **0.300** | STRESSED | L4, L5 | knowledge | Incomplete sprints |
| **03_VENTURES/_PORTFOLIO** | **0.281** | STRESSED | L2, L4 | balanced | Placeholder dirs |
| **04_ENTITIES** | **0.240** | CRITICAL | L3, L4 | regulatory | Ghost paths |

**Ecosystem average fitness: 0.396** — below the 0.500 equator threshold. The organism is structurally stressed.

---

## Methodology

Each root was assessed as a 12-dimensional genotype:

- **Caste block (L1–L7)**: Emphasis weights derived from file-type distribution and functional role
- **Economic block (κ,λ,μ,ρ,ν)**: Intensity proportions derived from capital deployment, labour input, IP density, regulatory burden, and network connectivity
- **Fitness**: Computed via `FitnessLandscape.compute()` with 8 factors:
  - F_k2 (constitutional consent), F_cci (caste concentration), F_edi (economic diversity)
  - F_act (activity recency), F_excl (competitive exclusion), F_env (environment)
  - F_econ (economic efficiency), F_eta (η = 0 compliance)

Data sources: filesystem scan, git history, README/AGENTS.md coverage, empty-directory detection, build-artifact inventory.

---

## 1. EMERGENTISM_ORG — Doctrine & Framework Source

**Fitness: 0.600 | Status: HEALTHY | Caste: L5, L6, L7 | Economic: labour, knowledge**

### Current State

| Metric | Value |
|---|---|
| Directories (L2) | 62 |
| Files (non-artifact) | ~2,571 |
| READMEs | 219 |
| AGENTS.md | 2 (root + 11_UPLINK) |
| Recent commits (30d) | 5+ |
| Empty/stale dirs | 10 (mostly in 90_ARCHIVE, 91_COMPATIBILITY) |

### Caste Analysis

- **L5 Brāhmaṇa (1.8)**: Architecture, systematisation — dominant. The framework support directory is essentially a L5 caste surface.
- **L6 Sādhu (1.4)**: Compression, pruning, archive — strong. The 90_ARCHIVE dirs and synthesis compression functions are L6 work.
- **L7 Ṛṣi (1.5)**: Constitutional, transcendental — strong. Sevenfold Foundation Root, theology, ontology.
- **L4 Kṣatriya (1.0)**: Execution — baseline. Not an execution surface; this is theory.

### Economic Analysis

- **μ knowledge (0.45)**: IP-dense. Framework derivations, Rosetta Stone, formal proofs.
- **λ labour (0.30)**: Writing-intensive. 219 READMEs = massive human cognitive labour.
- **κ capital (0.05)**: Minimal. No deployed infrastructure.
- **ρ regulatory (0.05)**: Minimal. Constitutional, not compliance-facing.
- **ν network (0.15)**: Cross-references between documents create knowledge network effects.

### Strengths
- **Highest README density** in the organism (219 READMEs / 62 dirs = 3.5 per dir)
- **Active development**: 5 commits in recent period, all touching this root
- **Well-structured**: Sevenfold Foundation Root provides clear routing
- **Living documents**: Polygenic tree, coordination protocols, agent runbooks all actively maintained

### Gaps
1. **Archive bloat**: 90_ARCHIVE, 91_COMPATIBILITY, source_notes dirs are under-populated or stale
2. **AGENTS.md coverage**: Only 2 AGENTS.md files for 62 directories — subdirectories need local agent guidance
3. **L1 intake**: 01_INTAKE exists but is a queue, not an active processing pipeline
4. **L2 exploration**: 02_EPISTEMOLOGY, 03_METHODOLOGY have content but lack active research cadence

### Recommended Actions
- [ ] Prune empty archive dirs or move to 999_ARCHIVE
- [ ] Add AGENTS.md to 09_TOOLS/ and 10_SEED/
- [ ] Activate L1 intake pipeline: define clear processing SLA

---

## 2. SKYZAI_ORG — First Organism Runtime

**Fitness: 0.357 | Status: STRESSED | Caste: L1, L4, L5 | Economic: capital**

### Current State

| Metric | Value |
|---|---|
| Directories (L2) | 93 |
| Files (reported) | ~68,894 |
| Files (excl. node_modules/.venv) | ~12,000 estimated |
| READMEs | 2,799 |
| AGENTS.md | 13 |
| node_modules dirs | 64 |
| .venv | 1 |
| Recent commits (30d) | 5 |

### Caste Analysis

- **L4 Kṣatriya (1.8)**: Execution — dominant. This is the operational organism: DACs, organs, child-DACs, project management.
- **L1 Caṇḍāla (1.3)**: Intake, firewall — strong. 00_BACKBONE, 01_INTAKE, local_runtime.
- **L5 Brāhmaṇa (1.3)**: Architecture — moderate. ORGANISM_BLUEPRINT, BREATHING_PATH_CANONICAL.
- **L2 Śūdra (1.2)**: Exploration — moderate. 01_INTAKE/QUEUE processes raw sources.

### Economic Analysis

- **κ capital (0.35)**: Capital-intensive. ApuBot app, TheCircle infra, RealityFutures contracts, Skyzai runtime.
- **λ labour (0.20)**: Moderate labour. SMF time for K2 signing, organ operation.
- **μ knowledge (0.20)**: Moderate IP. Protocol specs, API standards.
- **ρ regulatory (0.10)**: Low-moderate. K2 signing, constitutional checks.
- **ν network (0.15)**: Network effects from settlement rails, member nodes.

### Strengths
- **Most complex organ**: ApuBot (7,116 files) — the cognitive core
- **Four organs measured**: TheCircle, RealityFutures, Agentz, Skyzai all have P-scores
- **Child-DAC infrastructure**: AGENTZ_CLOUD, yieldfront, tokenization centres
- **Agent deployment**: 10_AGENTS/ has operationalized specs

### Critical Issues
1. **Dependency bloat — EXTINCTION RISK**: 64 node_modules directories inflate file count 5×. This is a **pathology** — L4 Violence (unchecked expansion without L6 pruning).
2. **Evolutionary.Network nearly extinct**: 17 files total. The organism's immune system is undeveloped.
3. **Duplicate project management**: Both `04_PROJECT_MANAGEMENT` and `05_PROJECT_MANAGEMENT` exist — competitive exclusion violation.
4. **.venv in 00_BACKBONE**: Python environment committed to repo — should be gitignored.

### Recommended Actions
- [ ] **URGENT**: Add `node_modules/` to .gitignore and purge from history
- [ ] **URGENT**: Remove `.venv` from 00_BACKBONE — add to .gitignore
- [ ] Merge or delete duplicate PROJECT_MANAGEMENT dirs
- [ ] Bootstrap Evolutionary.Network: minimum viable immune system (slashing, recovery receipts)
- [ ] L6 compression pass on 02_ORGANS: prune empty spec dirs

---

## 3. SKYZAI_COM — Public Product Surface

**Fitness: 0.300 | Status: STRESSED | Caste: L4, L5 | Economic: knowledge**

### Current State

| Metric | Value |
|---|---|
| Directories (L2) | 24 |
| Files | 245 |
| READMEs | 24 |
| AGENTS.md | 1 |
| Recent commits (30d) | 5 |
| Completed sprints | 9 |
| Incomplete folders | 7 (DEX, POS, AGENTS, LAUNCH, FRONTEND, SDK, API) |

### Caste Analysis

- **L4 Kṣatriya (1.5)**: Execution — dominant. Product sprints, factory, wallet, operational specs.
- **L5 Brāhmaṇa (1.6)**: Architecture — dominant. Product architecture, SDK design, API specs.
- **L3 Vaiśya (1.0)**: Audit — baseline. Covenant, compliance, invariants.

### Economic Analysis

- **μ knowledge (0.40)**: Knowledge-intensive. Product specs, SDK design, architecture.
- **λ labour (0.25)**: Moderate labour. Sprint execution.
- **κ capital (0.15)**: Low capital. Mostly documentation, not deployed infra.
- **ρ regulatory (0.10)**: Low regulatory. Covenant specs, not compliance-facing.
- **ν network (0.10)**: Low network. Not yet connected to live settlement rails.

### Strengths
- **Sprint discipline**: 9 completed sprints with clear deliverables
- **Well-documented**: 24 READMEs for 24 dirs = 100% coverage
- **GAP_ANALYSIS exists**: Self-aware about gaps
- **Factory pattern**: 01_FACTORY has DAC template, genesis event, kit inheritance

### Critical Issues
1. **Incomplete product surface**: 7 of 17 folders are < 30% complete
2. **No runtime connection**: Specs exist but no live connection to SKYZAI_ORG runtime
3. **AGENTS.md singleton**: Only 1 AGENTS.md for 24 directories
4. **DEX/POS dormant**: Critical financial infrastructure has minimal specs

### Recommended Actions
- [ ] Complete DEX, POS, AGENTS sprints (highest commercial priority)
- [ ] Connect 01_FACTORY to 02_SKYZAI/01_NOOSPHERE/04_CHILD_DACS for live genesis
- [ ] Add AGENTS.md per major folder
- [ ] LAUNCH/FRONTEND/SDK need minimum viable specs before sprint 10

---

## 4. ENTITIES — Organism-Native Entity Lanes

**Fitness: 0.240 | Status: CRITICAL | Caste: L3, L4 | Economic: regulatory**

### Current State

| Metric | Value |
|---|---|
| Directories (L2) | 31 |
| Files | 2,466 |
| READMEs | 296 |
| AGENTS.md | 1 |
| Recent commits (30d) | 5 |
| Ghost-path fixes | 15+ files in recent commits |
| Legacy stubs | AUREUS legacy_product_stub (Flutter app, cloud_functions — empty) |

### Caste Analysis

- **L3 Vaiśya (1.6)**: Audit, compliance — dominant. Entity structuring, regulatory navigation.
- **L4 Kṣatriya (1.3)**: Execution — strong. Entity operation, stakeholder management.
- **L7 Ṛṣi (1.2)**: Constitutional — moderate. Foundation constitutional work.

### Economic Analysis

- **ρ regulatory (0.35)**: Regulatory-intensive. Entity formation, jurisdiction navigation, compliance.
- **λ labour (0.20)**: Moderate labour. Counsel, SMF time.
- **μ knowledge (0.20)**: Moderate IP. Entity templates, governance frameworks.
- **κ capital (0.15)**: Low-moderate capital. Brand assets, websites.
- **ν network (0.10)**: Low network. Not yet connected to live settlement.

### Strengths
- **High README count**: 296 READMEs = well-documented
- **Foundation constitutional work**: Canonical source entity
- **Shared DAC template**: 00_SHARED/DAC_TEMPLATE for replication
- **Dual federation spec**: Cross-entity coordination protocol exists

### Critical Issues
1. **Lowest K2 approval rate (0.80)**: 8 signatures, 2 refusals. L2 Terror pathology signal.
2. **Ghost paths**: Recent commits fixed 15+ ghost paths — structural rot.
3. **AUREUS legacy stub**: Empty Flutter app and cloud_functions dirs — dead weight.
4. **HELIOS minimal**: Virtual sales front has minimal content.
5. **MENEXUS unclear**: Operating company docs exist but operational status unclear.

### Recommended Actions
- [ ] **URGENT**: Investigate K2 refusals in ENTITIES — why 20% rejection rate?
- [ ] Prune AUREUS legacy_product_stub or revive with committed plan
- [ ] Ghost-path audit: run automated link checker across all 296 READMEs
- [ ] HELIOS needs minimum viable sales surface
- [ ] MENEXUS operational runbook: what does the operating company do?

---

## 5. PORTFOLIO_ORGS — Portfolio Sidecars

**Fitness: 0.281 | Status: STRESSED | Caste: L2, L4 | Economic: balanced**

### Current State

| Metric | Value |
|---|---|
| Directories (L2) | 18 |
| Files | 2,923 |
| READMEs | 923 |
| AGENTS.md | 1 |
| Recent commits (30d) | 5 |
| QNTM data room | 14 sections, well-structured |
| Tokenization centres | KSA (active), UAE (placeholder), General (comprehensive) |

### Caste Analysis

- **L2 Śūdra (1.5)**: Exploration, research — dominant. QNTM intelligence, Saudi research cohort.
- **L4 Kṣatriya (1.4)**: Execution — strong. Deal execution, mandate pipeline, capital raise.
- **L1 Caṇḍāla (1.2)**: Intake — moderate. Investor packet, counterparty map.

### Economic Analysis

- **Balanced profile**: No single dimension dominates — appropriate for portfolio work.
- **ρ regulatory (0.25)**: Moderate. UK FCA, SAMA, CMA regulatory navigation.
- **μ knowledge (0.25)**: Moderate. Market research, intelligence reports.
- **κ capital (0.15)**: Low-moderate. Data room infrastructure, PDF generation.
- **λ labour (0.20)**: Moderate. Deal negotiation, counsel.
- **ν network (0.15)**: Moderate. KSA/UAE network building.

### Strengths
- **QNTM data room**: Excellent structure — 14 sections covering executive, corporate, financial, regulatory, technology, team, legal, commercial, strategy
- **Saudi strategy**: Full synthesis + distilled brief exist
- **Tokenization centre structure**: 26 sub-folders covering full asset lifecycle
- **Pitch deck v4.3**: Professional PDF output with landscape format

### Critical Issues
1. **Placeholder directories**: UAE tokenization centre (1 file), Agentz series A (1 file), country replication playbook (1 file)
2. **QNTM intelligence sparse**: 03_SUPPORT has 1 file
3. **Agentz underdeveloped**: AGENTZ_CLOUD has minimal content vs. its strategic importance
4. **Stakeholder thesis scattered**: Hubert_Knapp folder exists but content unclear

### Recommended Actions
- [ ] Populate UAE tokenization centre or mark as Phase 2
- [ ] AGENTZ_CLOUD needs minimum viable operating system spec
- [ ] QNTM: connect data room to live UK PRA/FCA application tracking
- [ ] SKYZAI_BRIDGE: define what this sidecar actually bridges

---

## 6. SPECTRE — Distributed Physical Mesh

**Fitness: 0.600 | Status: DORMANT | Caste: L5, L6, L7 | Economic: capital**

### Current State

| Metric | Value |
|---|---|
| Directories (L2) | 13 |
| Files | 35 |
| READMEs | 10 |
| AGENTS.md | 1 |
| Recent commits (30d) | 5 |
| Code files | 1 (register_node.py) |
| Spec files | ~15 |

### Caste Analysis

- **L5 Brāhmaṇa (1.7)**: Architecture — dominant. Mycelial mesh doctrine, holarchy, PLANCK unit.
- **L6 Sādhu (1.3)**: Compression — strong. Holobiont principle, holonic attractor.
- **L7 Ṛṣi (1.5)**: Constitutional — strong. Vision-level distributed network concept.
- **L4 Kṣatriya (1.1)**: Execution — minimal. One Python script (register_node.py).

### Economic Analysis

- **κ capital (0.40)**: Capital-intensive by design. Physical nodes, energy metering, hardware.
- **μ knowledge (0.25)**: Moderate IP. Network topology, privacy primitives.
- **λ labour (0.15)**: Low labour. Not yet operational.
- **ρ regulatory (0.10)**: Low regulatory. Energy market regulations pending.
- **ν network (0.10)**: Low network. No live nodes yet.

### Strengths
- **Clear architecture**: MYCELIAL_MESH_DOCTRINE, 4 primitive specs (SPECTRE, RELAY, AXIOM, FLOW)
- **Energy market theory**: PLANCK unit of account, metrology candidate
- **Node registry**: register_node.py exists as seed
- **Holobiont principle**: Well-articulated theoretical foundation

### Critical Issues
1. **DORMANT status**: No activity since mid-April. 17 days inactive.
2. **35 files for a physical network**: This is a spec skeleton, not an operational system.
3. **No live nodes**: Node registry exists but no registered nodes.
4. **No energy market pilots**: PLANCK is theoretical; no metrology or metering exists.
5. **Competitive exclusion with SKYZAI_ORG**: Both claim "network" functions. Boundary unclear.

### Recommended Actions
- [ ] **URGENT**: Define SPECTRE↔Skyzai boundary — MSA-style interface
- [ ] Revive from DORMANT: commit to Node 0 deployment plan
- [ ] Energy market: minimum viable pilot (1 node, 1 meter, 1 transaction)
- [ ] Register first edge node using register_node.py
- [ ] Connect to 02_SKYZAI/06_SPECTRE/30_DEPLOYMENT/README.md with actual deployment steps

---

## Cross-Cutting Analysis

### Competitive Exclusion Warnings

| Pair | Distance | Issue |
|---|---|---|
| EMERGENTISM_ORG ↔ SPECTRE | 0.129 | Both L5/L6/L7 dominant, architecture-heavy. Boundary: theory vs. physical |
| EMERGENTISM_ORG ↔ SKYZAI_COM | 0.129 | Both L4/L5, knowledge-intensive. Boundary: framework vs. product |
| SKYZAI_ORG ↔ PORTFOLIO_ORGS | 0.156 | Both L4 execution. Boundary: organism core vs. sidecars |
| PORTFOLIO_ORGS ↔ ENTITIES | 0.119 | Both L4 execution, deal-making. Boundary: portfolio vs. native entities |
| ENTITIES ↔ SKYZAI_COM | 0.119 | Both L3/L4 regulatory/execution. Boundary: legal entity vs. product |

**Resolution**: All pairs need explicit interface contracts. The `00_DUAL_FEDERATION_SPEC.md` in ENTITIES is a start but needs expansion.

### Build Artifacts at Repo Root

```
cache/           solidity-files-cache.json  → move to .gitignore
out/             EventCellSettlement.sol/ + build-info/  → move to .gitignore  
output/          playwright/  → move to .gitignore
tmp/             pdfs/  → move to .gitignore
```

These are production build outputs that should not be tracked.

### AGENTS.md Coverage Gap

| Root | Dirs (L2) | AGENTS.md | Coverage |
|---|---|---|---|
| 01_EMERGENTISM | 62 | 2 | 3.2% |
| 02_SKYZAI_ORG | 93 | 13 | 14.0% |
| 03_SKYZAI_COM | 24 | 1 | 4.2% |
| 04_ENTITIES | 31 | 1 | 3.2% |
| 03_VENTURES/_PORTFOLIO | 18 | 1 | 5.6% |
| 02_SKYZAI/06_SPECTRE | 13 | 1 | 7.7% |

**Organism average: 6.3%** — far below healthy threshold. Every directory that receives agent traffic needs an AGENTS.md.

---

## Prioritised Action List

### P0 — Lethal (extinction risk)
1. **Purge node_modules from SKYZAI_ORG** — 64 dirs of dependency bloat
2. **Purge .venv from SKYZAI_ORG/00_BACKBONE** — committed Python environment
3. **Investigate K2 refusals in ENTITIES** — 20% rejection rate is L2 Terror signal

### P1 — Critical (fitness < 0.300)
4. **Bootstrap Evolutionary.Network** — 17 files is immune-system failure
5. **Revive SPECTRE from DORMANT** — Define Node 0 deployment plan
6. **Complete SKYZAI_COM DEX/POS/AGENTS** — Incomplete financial infrastructure
7. **Merge duplicate PROJECT_MANAGEMENT dirs** in SKYZAI_ORG

### P2 — Stressed (fitness 0.300–0.500)
8. **Add root-level .gitignore** for cache/, out/, output/, tmp/
9. **Ghost-path audit across ENTITIES** — 296 READMEs need link checking
10. **AGENTS.md coverage pass** — target 50% of L2 directories
11. **Prune empty placeholder dirs** across all roots
12. **AUREUS legacy stub** — revive or tombstone

### P3 — Healthy (fitness > 0.500)
13. **L6 compression pass on EMERGENTISM_ORG archives**
14. **Activate L1 intake pipeline** with processing SLA
15. **Connect SKYZAI_COM factory to SKYZAI_ORG child-DAC runtime**

---

## Fitness Tracking Dashboard

| Root | Current | Target | Δ |
|---|---|---|---|
| 01_EMERGENTISM | 0.600 | 0.700 | +0.100 (prune archives, activate intake) |
| 02_SKYZAI_ORG | 0.357 | 0.550 | +0.193 (purge deps, boot EvNet) |
| 03_SKYZAI_COM | 0.300 | 0.500 | +0.200 (complete sprints, connect runtime) |
| 04_ENTITIES | 0.240 | 0.450 | +0.210 (fix K2 rate, prune ghosts, revive AUREUS) |
| 03_VENTURES/_PORTFOLIO | 0.281 | 0.450 | +0.169 (fill placeholders, connect QNTM tracking) |
| 02_SKYZAI/06_SPECTRE | 0.600 | 0.600 | Maintain (currently DORMANT by design; revive = +0.200) |
| **Ecosystem Avg** | **0.396** | **0.525** | **+0.129** |

---

*Generated by organism root fitness assessment protocol*
*φ · ν = 1 on S²*
*⊙ = • × ○*

## Execution Surface

- **Canonical Path:** 01_EMERGENTISM/08_FRAMEWORK_SUPPORT/08_AGENTS/ORGANISM_ROOT_FITNESS_ASSESSMENT.md
