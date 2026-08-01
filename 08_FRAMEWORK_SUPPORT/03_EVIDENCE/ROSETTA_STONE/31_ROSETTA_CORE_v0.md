---
rosetta:
  primary_level: L3
  primary_column: Methodology
  operator: "Kṛṣṇa ◇"
  tier: "Auditor"
  regime: "Vaiśya"
  register: "[S] architecture; [I] any particular pack"
  canonical_phrase: "Core + Packs + Ledger — Rosetta as a translation system, not a law of the cosmos"
title: "Rosetta Core v0 — Core + Packs + Ledger"
status: "ACTIVE v0 — the architecture; supersedes §2 of 30_ROSETTA_VNEXT_REFINEMENT_2026_07_31 which now records the kill-criterion read"
date: 2026-07-31
supersedes: "30_ROSETTA_VNEXT_REFINEMENT_2026_07_31 §2 (refinement proposal, now landed)"
depends:
  - "00_THE_MASTER_ROSETTA.md (translation laws)"
  - "00_THE_SEVEN_PHILOSOPHICAL_DISCIPLINES.md (PHIL7@1 — one namespaced pack)"
  - "00_D5_THE_SEVEN_GENERATIVE_ACTIONS.md (G7@1 — D5 game vocabulary)"
  - "D_SERIES_ROWS/00_GENERATIVE_TABLE.md (GEN7@1 — generative/regime projection)"
  - "10_CELL_AUDIT_SCHEMA_2026_04_25.md (cell schema v2)"
  - "FAILED_MAPPINGS_AND_TESTING_QUEUE.md (the negative corpus)"
---

# Rosetta Core v0 — Core + Packs + Ledger

> The Rosetta is a translation system. It is not a sevenfold law of the cosmos.
> It is a disciplined way of asking whether two domains share a useful relational
> pattern, and of saying what survives the comparison, what is lost, and what would
> kill the comparison.

This document specifies the architecture. It does not add rows, mappings, or
disciplines. The packs and cells live in the ledger; this document is the
metarules.

---

## 1. The architecture

```text
ROSETTA_CORE         the metarules (this document)
  ├── namespaced packs     independent, versioned, comparable only through explicit ρ
  │     ├── PHIL7@1         the seven reversible philosophical questions
  │     ├── GEN7@1         the generative/regime projection
  │     ├── G7@1            the D5 game vocabulary (M4 + F3)
  │     ├── REP7@1         the replicator projection
  │     ├── PSYCH7@1       psychology projection
  │     ├── CULTURE7@1     cultural/symbolic projection
  │     ├── SOUL4@0        Soul-Loop Mission Engine projection
  │     └── …              domain packs
  └── ledger               machine-readable cells, audit fields, kill criteria
```

A bare `L1` is local shorthand after a pack is declared. Cross-pack claims
require `projection_id@version:row_key`. Equal-looking seats in `G7@1` and
`PHIL7@1` are not identical objects. *This namespace discipline is not stylistic
— it is the single load-bearing anti-confusion move.*

## 2. Translation laws (Core → packs)

Every pack, every cell, and every cross-pack claim must declare:

1. **Source and target** — typed domains, neither treated as the other.
2. **The relation claimed invariant** — a single named invariant, not "a vibe."
3. **Source provenance and independence** — inheritance, diffusion, common
   ancestry, framework-derived extensions. *Ten correspondences descending from
   one Indo-European lineage are not ten independent observations.*
4. **Information discarded** — what is lost in the translation. Lexical, ordinal,
   causal, temporal, normative, geometric, or authority-bearing loss.
5. **Native cardinality** — the count before grouping, insertion, omission, or
   row-fitting. The **anti-Procrustean rule**: a five-, eight-, ten-, or
   twelve-part native system **must remain five, eight, ten, or twelve** before
   any optional normalisation.
6. **Target prediction or practical use** — what the translation is *for*.
7. **Evidence tier and kill criterion** — how the translation is killed, not
   just how it is supported.

## 3. Three evidential questions, separated

Every cell must answer three independent questions:

| Field | Question | Failure mode |
|---|---|---|
| `fact_tier` | Is the source-domain fact established? | A speculative cell can rest on a true fact and still be speculative. |
| `mapping_tier` | Is this placement within Rosetta warranted? | A fact placed on weak grounds remains a weak cell. |
| `outcome_status` | Did the translated use actually work? | A beautiful translation that produces no external benefit is still an interpretation. |

An established neuroscience fact placed speculatively at L6 is a *speculative
cell*. A mathematical identity placed in the wrong row is *a wrong cell*. A
cell that passes internal audit and produces external benefit is `[A]`; a cell
that passes internal audit and has produced no benefit is `[I]`; a cell that
fails audit is `[D]`.

## 4. First-class non-fit states

Every source term may resolve as one of:

```text
FIT       — the cell holds across the named invariant
PARTIAL   — the cell holds partially; name the missing dimensions
MULTIROW  — the source term occupies more than one row; name them
UNMAPPED  — the source term is a genuine non-fit; record why
EXTRA     — the source has a row that Rosetta does not natively have
DEPENDENT — the cell requires a pre-existing cell in the same or another pack
DISPUTED  — the cell is contested by named rivals; record the rivals
KILLED    — the cell has been killed by its own kill criterion; retain the record
```

`UNMAPPED` is **not a failure**. It is a successful negative result. The
negative corpus is part of Rosetta's claim, not a stain on it.

## 5. The namespace collision — a live defect

| | `PHIL7@1` | `GEN7@1` |
|---|---|---|
| Teleology | `purpose` (L1) | L7 |
| Ontology | `being` (L6) | L5 |

The two placements are *not* the same claim. `PHIL7@1:purpose` asks "what end is
proposed?"; `GEN7@1:L7` carries the closing horizon of the generative cycle.
A statement like "L7 is teleology" is *ambiguous across packs and has been
treated as agreement*. **Bare `L_n` references are invalid outside a single
declared pack.**

A v2 cell that used a bare row remains historical input; it is not silently
reinterpreted as a v2 cell.

## 6. Mirrors as hypotheses, not identities

The four mirror pairs (`L1↔L7`, `L2↔L6`, `L3↔L5`, `L4` self) **default to
`unknown`**, not `true`. Each pack that claims a mirror must name:

- what relation is inverted;
- what information survives the inversion;
- what observation would break the mirror.

A "broken mirror" is not a failure of Rosetta. It is a clarification of what
the mirror was claiming.

## 7. Regimes as dynamic capture signatures, not row outcomes

The regime column (tyranny, democracy, oligarchy, timocracy, aristocracy,
anarchy, theocracy) was historical analogy. v0 reframes regimes as **dynamic
capture signatures** — *what happens when one function monopolises evidence,
alternatives, authorisation, means, receipts, and correction?*

A healthy organism rotates through functions. A captured organism freezes one
function into sovereignty. The question is no longer "which regime is L_n?" but
"which function is currently monopolising which substrate?"

## 8. Authority, ownership, and the kill chain

Rosetta translates. **It does not own, evidence, or define.** The kill chain
runs through the owner pack (KSC for the canon; the source-domain for any
mappable claim). A Rosetta cell that contradicts its owner is **wrong**; a
Rosetta cell whose owner has moved on is **stale**; a Rosetta cell that has
been killed by its own criterion is **recorded**, not removed.

A semantic change to a pack creates a new `version` and a supersession edge.
Existing references are not silently rewritten.

## 9. The deepest invariant

The Rosetta is not "everything has seven levels." Its deepest claim, if it has
one, is this:

> Different domains repeatedly confront boundary, knowledge, inference, value,
> world-model, being, and ultimate-horizon problems; a disciplined translation
> can reveal their relational similarities without erasing their native
> differences.

This is less grandiose than a universal sevenfold ontology — and much more
durable, testable, and useful.

## 10. The expansion rule

Rosetta expands **inward** (refinement, namespacing, non-fit states, kill
criteria) before it expands **outward** (new packs, new domains). The kill
criterion for any outward expansion is: *does the new pack add a translation
that was previously UNMAPPED or KILLED, and does it carry its own kill
criterion?*

`Co-Authored-By: <the agent that drafted the cell>`
