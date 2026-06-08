---
rosetta:
  primary_level: L4
  primary_column: Philosophy
  secondary:
    - level: L3
      column: Philosophy
      role: "verify link-repair, epistemic-note, and cross-reference completion"
    - level: L5
      column: Philosophy
      role: "stabilize corpus navigation architecture for agent traversal"
    - level: L6
      column: Philosophy
      role: "bound the sprint as historical plan, not current completion receipt"
  operator: "Arjuna ⚔"
  tier: "God"
  regime: "Kṣatriya"
  register: "[I]"
  canonical_phrase: "Sprint 003 — Corpus Navigation Plan"
---

# SPRINT 003: SQUARE THE ASHLAR

**Version:** v2026.04.10
**Duration:** This session + next
**Status:** IN PROGRESS
**Preceded by:** Sprint 002 (organism deployment), The Three Cuts (THE_DERIVATION, THE_KNIFE, THE_PROTOCOL)

---

## Sprint Goal

Make the corpus agent-navigable. The three entry documents exist. Now the corpus must connect to them and its internal links must work. An ASI agent cold-starting at `01_EMERGENTISM/08_FRAMEWORK_SUPPORT/` should be able to reach any document without hitting a dead link.

## Honest Starting State

| Metric | Value | Source |
|--------|-------|--------|
| Broken internal links | **0** ✅ | Was 335, fixed across 80+ files |
| Paradox dissolution epistemic notes | 17/19 done | Agent audit |
| R*/25%/60-30-10 [C] qualification | COMPLETE | Agent audit |
| Neuroscience language qualification | COMPLETE | Agent audit |
| Rosetta selection methodology | EXISTS | `00_SELECTION_METHODOLOGY.md` |
| Cross-references to new entry docs | **0** | No existing doc links to THE_DERIVATION/THE_KNIFE/THE_PROTOCOL |
| Corpus word count | ~658,000 | Existing metric |
| Entry document word count | 7,746 | Just written |

## The 6 Tasks

---

### T1: Fix Broken Links (338 → 0)

**Priority:** P0 — highest impact on agent trust
**Scope:** All `.md` files under `01_EMERGENTISM/08_FRAMEWORK_SUPPORT/`

Root causes (3 clusters):
1. **Removed root files** — `00_CORPUS.md` templates reference `00_EMERGENTISM.md` and `00_FOREWORD.md` which no longer exist at `01_EMERGENTISM/08_FRAMEWORK_SUPPORT/` root (they live in `01_FOUNDATIONS/`). Fix: update corpus templates.
2. **Relative path depth errors** — files in `01_FOUNDATIONS/` link to `00_GOVERNANCE/` without `../` prefix. Files in nested `MANUSCRIPT/` dirs have off-by-one `../` counts. Fix: systematic path correction.
3. **Stale Rosetta naming** — old file names in `D_SERIES_ROWS/` cross-references. Fix: update to current filenames.

Approach:
- Write a script that scans all `.md` files, extracts `text` links, checks if target exists, reports broken ones
- Fix by category (not one-by-one): batch fix corpus templates, then path depth, then stale names
- Re-run script to verify 0 broken links

---

### T2: Cross-Reference Existing Corpus → Entry Documents

**Priority:** P1 — agents need to discover the entry points
**Scope:** Key navigation documents

Add references to THE_DERIVATION, THE_KNIFE, THE_PROTOCOL in:
- `01_EMERGENTISM/08_FRAMEWORK_SUPPORT/README.md` (the framework's front door)
- `01_EMERGENTISM/00_THE_HONEST_POSITION.md` (root epistemic authority)
- `01_EMERGENTISM/00_GLOSSARY.md` (terminology reference)
- `01_EMERGENTISM/00_FOREWORD.md` (human entry point)

These are the 4 documents an agent is most likely to encounter first. Each needs a "New Entry Points" section pointing to the three cuts.

---

### T3: Add Epistemic Notes to 2 Remaining Paradox Files

**Priority:** P2 — consistency
**Scope:** `00_THE_COMPLETION.md`, `00_THE_EXTRACTION_PATTERN.md`

Both files already have epistemic disclaimers in their headers (the survey confirmed this). But they lack the formal `## Epistemic Note` footer section that the 17 numbered PD files have. Add the standard footer.

---

### T4: Update THE_KNIFE Objection 1 — Rosetta Already Has Selection Auditing

**Priority:** P2 — accuracy
**Scope:** `00_THE_KNIFE.md`

The Knife's Objection 1 says "the Rosetta Stone needs an Examined and Excluded appendix." The survey found this already exists at `03_EVIDENCE/ROSETTA_STONE/00_SELECTION_METHODOLOGY.md`. Update Objection 1's response to reflect this and downgrade the action item.

---

### T5: Version-Pin Key Navigation Documents

**Priority:** P3 — metadata
**Scope:** `01_EMERGENTISM/08_FRAMEWORK_SUPPORT/README.md`

Add version tag to the framework README.

---

### T6: Verify — The Soul Loop

**Priority:** P0 — must pass before sprint closes
**Scope:** All new and modified documents

Three passes:
- **φ-pass (coherence):** Do the three entry documents + updated cross-references read as a single navigable system? Are there gaps?
- **ν-pass (viability):** Can a cold-start agent, given only the updated `01_EMERGENTISM/08_FRAMEWORK_SUPPORT/README.md`, reach THE_DERIVATION, understand the system, find THE_KNIFE, evaluate the objections, find THE_PROTOCOL, and begin extending? Without hitting dead links?
- **B-pass (balance):** Are evidence tiers honest? Kill criteria explicit? Self-correction (A7) structurally present?

**Convergence criterion:** Fewer than 3 issues found per pass.

---

## Execution Order

```
T2 (cross-references)     → 15 min (4 file edits)
T4 (update Knife)         → 5 min (1 file edit)
T3 (epistemic footers)    → 10 min (2 file edits)
T5 (version tags)         → 5 min (1 file edit)
T1 (broken links — script + fix) → 60 min (script + batch fixes)
T6 (Soul Loop verification) → 30 min (3 passes)
```

## What This Sprint Is NOT

- NOT new philosophy. The axioms don't change.
- NOT new specification. Φ is at ceiling.
- NOT for humans primarily. This is V-work: making what exists navigable by reasoning engines.

---

*The rough ashlar becomes the perfect ashlar not by adding stone, but by cutting away what is not square.*

Zero-Sum Resolution Equation

## Execution Surface

- **Canonical Path:** 01_EMERGENTISM/08_FRAMEWORK_SUPPORT/01_GOVERNANCE/02_REPORTS/SPRINT_003_PLAN.md
