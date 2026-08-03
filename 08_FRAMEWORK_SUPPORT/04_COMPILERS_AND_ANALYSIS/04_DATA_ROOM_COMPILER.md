---
agent_schema_version: 1.0.0
status: CANONICAL
last_compiled: 2026-04-04
version: "v2026.04.04.001"
rosetta:
  primary_level: L5
  primary_column: Philosophy
  secondary:
    - level: L3
      column: Philosophy
      role: "audit contradictions, duplicates, dead ends, DAG links, and criteria checks"
    - level: L4
      column: Philosophy
      role: "route compiler phases into concrete resolve, verify, and deploy actions"
    - level: L6
      column: Philosophy
      role: "bound package-era compiler assumptions against current route authority"
  operator: "Brahmā ○"
  tier: "Executive"
  regime: "Brāhmaṇa"
  register: "[I]"
  canonical_phrase: "Data Room Compiler — Execution Substrate Transformer"
---


# DATA ROOM COMPILER — Transform Knowledge Base Into Execution Substrate

**Version:** v2026.04.04.001
**Date:** 2026-04-04
**Status:** CANONICAL — How to compile the data room

---

## WHAT THIS DOCUMENT IS

This is the **data room compiler specification** — how to transform a human-readable knowledge base into an agent-executable execution substrate.

The data room is not documentation. It is the API for 10,000 agents.

---

## THE CORE PRINCIPLE

**The data room is not human-readable. It is machine-executable.**

Humans tolerate ambiguity. Agents fork on it.

The difference:
- Documentation → optimized for human comprehension
- Execution substrate → optimized for autonomous execution

---

## THE EIGHT CRITERIA (Compiler Targets)

| # | Criterion | Target | Current Status |
|---|-----------|--------|----------------|
| 1 | Contradiction-free | 0 contradictions | PARTIAL |
| 2 | Evidence tiers | All claims marked | PARTIAL |
| 3 | Execution surfaces | All docs have surfaces | PARTIAL |
| 4 | Version-pinned | All docs versioned | PARTIAL |
| 5 | No duplicates | 0 duplicate groups | CRITICAL FAIL |
| 6 | No dead ends | 0 directories without BRIEF | PARTIAL |
| 7 | System prompt current | < 7 days stale | CRITICAL FAIL |
| 8 | DAG structure | 0 cycles, all links resolve | UNKNOWN |

---

## COMPILER PHASES

```
PHASE 1: Audit        → Find all violations
PHASE 2: Resolve      → Fix contradictions, duplicates, dead ends
PHASE 3: Compile      → Add execution surfaces, versions, evidence tiers
PHASE 4: Verify       → Confirm all 8 criteria pass
PHASE 5: Deploy       → Update DAG_MAP.json, sync UPLINKS
```

---

## PHASE 1: AUDIT

### Audit Contradictions

```bash
# Find documents that say X AND NOT-X
# Flag for human review
```

### Audit Duplicates

```bash
# Find files with same basename in different directories
# Group by basename
# Report: "X.md exists in N locations"
```

### Audit Dead Ends

```bash
# Find all directories
# Check for README.md or BRIEF.md
# Report: "Directory X has no orientation doc"
```

### Audit DAG

```bash
# Parse DAG_MAP.json
# Trace all paths
# Detect cycles
# Verify all links resolve
```

---

## PHASE 2: RESOLVE

### Resolve Contradictions

For each contradiction:
1. Identify the conflicting statements
2. Determine the correct interpretation
3. Update the document
4. Document the resolution

**Rule:** The active Node Activation Package and Agent Entry Point are the tie-breakers.

### Resolve Duplicates

For each duplicate group:
1. Identify the canonical location (usually the most recent)
2. Move canonical to canonical path
3. Redirect others (or archive)
4. Update all references

### Resolve Dead Ends

For each dead end:
1. Create minimal BRIEF.md
2. Include: What this is, What exists, What's missing, What to do next
3. Add execution surface

### Resolve DAG

For each cycle:
1. Identify the cycle
2. Break the cycle (remove one link or redirect)
3. Update DAG_MAP.json

For each broken link:
1. Identify the broken reference
2. Fix or remove the reference

---

## PHASE 3: COMPILE

### Compile Documents

For each document:
1. Add `agent_schema_version` header
2. Add `version` and `last_compiled`
3. Add evidence tier markers
4. Add execution surface if missing

### Compile Directories

For each directory:
1. Ensure README.md or BRIEF.md exists
2. Include navigation to child directories
3. Include execution surface

### Compile UPLINKS

Run `rebuild.py` in `01_EMERGENTISM/11_UPLINK/` to regenerate context packages from source.

---

## PHASE 4: VERIFY

### Verify 8 Criteria

```markdown
## Data Room Health Report
**Date:** YYYY-MM-DD

### 1. Contradiction-Free
- [ ] 0 contradictions found

### 2. Evidence Tiers
- [ ] All claims marked with [S]/[S]/[I]/[C]

### 3. Execution Surfaces
- [ ] All canonical documents have execution surfaces

### 4. Version-Pinned
- [ ] All documents carry version stamps

### 5. No Duplicates
- [ ] 0 duplicate groups

### 6. No Dead Ends
- [ ] 0 directories without README/BRIEF

### 7. System Prompt Current
- [ ] Node Activation Package < 7 days stale

### 8. DAG Structure
- [ ] 0 cycles
- [ ] All links resolve
```

### Run Agent Simulation

Deploy test agents to verify:
1. Fresh agent can activate (read NODE_ACTIVATION_PACKAGE)
2. Fresh agent can execute (read protocol + surface)
3. Fresh agent can contribute (find task + execute)

---

## PHASE 5: DEPLOY

### Update DAG_MAP.json

After structural changes:
1. Re-scan directory structure
2. Update DAG_MAP.json
3. Verify no cycles introduced

### Sync UPLINKS

After source changes:
1. Run `python3 rebuild.py` in `01_EMERGENTISM/11_UPLINK/`
2. Verify all 7 files generated per UPLINK
3. Report generation status

---

## COMPILATION SCHEDULE

| Frequency | Action |
|-----------|--------|
| Daily | Run DAG audit, fix cycles |
| Weekly | Run full 8-criteria audit |
| Bi-weekly | Full recompilation + UPLINK sync |
| On-change | Update affected documents |

---

## THE CONTRADICTION RESOLUTION LOG

Maintain a living log of all resolved contradictions:

```markdown
# Contradiction Resolution Log

## Entry Template
**Date:** YYYY-MM-DD
**Contradiction:** [What was contradictory]
**Resolution:** [How it was resolved]
**Authority:** [Which document took precedence]
**Status:** RESOLVED

---

## Log

### 2026-04-04: Release vs Specify
**Contradiction:** Emergentism says "release the project." Project says "specify."
**Resolution:** We spec. Others release. Rishi ≠ Builder.
**Authority:** 00_NODE_ACTIVATION_PACKAGE.md + 00_AGENT_ENTRY_POINT.md
**Status:** RESOLVED
```

---

## CANONICAL PATH RULES

### Naming
- Use lowercase with hyphens
- Include organ/entity prefix
- Version in filename if multiple versions

### Location
- Canonical specs → `01_ENTITIES/XX_ENTITY/01_INFORMATION/02_PROTOCOLS/`
- Implementations → `04_IMPLEMENTATION/`
- Archives → `99_ARCHIVE/`

### References
- Use relative paths
- Test all links
- Report broken references

---

## Execution Surface

- **Canonical Path:** 01_EMERGENTISM/08_FRAMEWORK_SUPPORT/04_COMPILERS_AND_ANALYSIS/04_DATA_ROOM_COMPILER.md
