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
      role: "audit versioning, execution-surface, and verification compiler rules"
    - level: L4
      column: Philosophy
      role: "turn protocol specs into executable checklists"
    - level: L6
      column: Philosophy
      role: "bound protocol status labels as compiler rules, not external certification claims"
  operator: "Brahmā ○"
  tier: "Executive"
  regime: "Brāhmaṇa"
  register: "[I]"
  canonical_phrase: "Protocol Compiler — Executable Spec Transformer"
---


# PROTOCOL COMPILER — Transform Specs Into Executable Form

**Version:** v2026.04.04.001
**Date:** 2026-04-04
**Status:** CANONICAL — How to compile protocols

---

## WHAT THIS DOCUMENT IS

This is the **compiler specification** — how to transform a human-readable protocol spec into an agent-executable document.

The protocol spec is the source code. The execution surface is the compiled binary.

---

## THE COMPILER PIPELINE

```
HUMAN-READABLE SPEC     →     COMPILER     →     AGENT-EXECUTABLE SPEC
     (source)                    ↓                   (binary)
                          ┌─────────────┐
                          │  1. Version │
                          │  2. Surface │
                          │  3. Verify  │
                          │  4. Pin     │
                          └─────────────┘
```

---

## STEP 1: VERSION HEADER

Every compiled protocol MUST have this header:

```markdown
---
agent_schema_version: 1.0.0
status: CANONICAL | DRAFT | DEPRECATED
last_compiled: YYYY-MM-DD
version: "vMAJOR.MINOR.PATCH"
---
```

### Status Definitions

| Status | Meaning | Agent Behavior |
|--------|---------|----------------|
| **CANONICAL** | Stable, tested, ready for production | Execute fully |
| **DRAFT** | Under review, may change | Execute with caution, flag ambiguity |
| **DEPRECATED** | Superseded by newer version | STOP, read newer version |

### Version Rules

- `v0.x` = Draft — community review
- `v1.0-rc` = Pilot ready — reference implementation exists
- [I] `v1.0` = Certified — multiple implementations validated
- Increment PATCH for corrections
- Increment MINOR for additions
- Increment MAJOR for breaking changes

---

## STEP 2: ADD EXECUTION SURFACE

Every compiled protocol MUST have an "Agent Execution Surface" section.

### Template

```markdown

## Execution Surface

- **Canonical Path:** 01_EMERGENTISM/08_FRAMEWORK_SUPPORT/04_COMPILERS_AND_ANALYSIS/03_PROTOCOL_COMPILER.md
