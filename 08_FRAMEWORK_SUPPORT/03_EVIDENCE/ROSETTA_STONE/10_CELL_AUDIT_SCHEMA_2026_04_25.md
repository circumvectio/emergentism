---
rosetta:
  primary_column: "Meta"
  register: "[S/I]"
  canonical_phrase: "10 — Rosetta Cell Audit Schema"
title: "Rosetta Projection and Cell Audit Schema"
status: "ACTIVE v2 — generalized and namespaced 2026-07-31"
supersedes_blob: "3138cff20aefe02b018dd8e341ab407d68d41cc6"
---

# Rosetta Projection and Cell Audit Schema

**Date:** 2026-04-25
**Revised:** 2026-07-31
**Status:** Active v2 audit schema; the exact v1 content remains recoverable from
the `supersedes_blob` Git object.
**Depends on:** [Rosetta vNext](03_ROSETTA_VNEXT_THEORETICAL_CONTRACT.md),
[02_ROWS_COLUMNS_DEEPENING_2026_04_25.md](02_ROWS_COLUMNS_DEEPENING_2026_04_25.md),
[archived structural pressure points](../../../90_ARCHIVE/pure_emergentism_boundary_2026_07_20/08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/06_STRUCTURAL_PRESSURE_POINTS_2026_04_25.md),
[07_MIRROR_SYMMETRY_FALSIFICATION_TEST_2026_04_25.md](07_MIRROR_SYMMETRY_FALSIFICATION_TEST_2026_04_25.md)
**Purpose:** Make any namespaced projection and cell auditable without forcing
seven rows, adjacency, mirror symmetry, an operator, or geometry onto a source
that does not natively contain them.

---

## 0. Law

A Rosetta cell is not a synonym. It is a directional, versioned claim:

```text
source_ref --relation preserving named invariant--> target_ref
```

The mature form is:

```text
In projection revision R, source term S maps partially to target term T under
normalization N because source basis B supports proposed invariant I; the map
discards loss vector L, depends on D, differs from rival Q by discriminator X,
and is killed or contracted by K.
```

If the cell cannot be written in that form, it can stay in the table only as exploratory or poetic material. It must not carry evidential weight.

The stable cross-pack reference is `projection_id@version:row_key`. Bare `Lx`
references are invalid outside a single declared pack. A v1 cell that used a
bare row remains historical input; it is not silently reinterpreted as a v2
cell.

---

## 1. Column Class

Every column gets a class before any cell is scored.

| Class | Examples | Evidential use | Primary risk |
|---|---|---|---|
| **Anchor** | Operator, geometry, equation, balance | Defines the selected grammar | Internal inconsistency |
| **Declared chain** | Varna, reasoning, pramana, -ology, regime | Tests a selected crosswalk; does not assert causation | Circular validation / person typing |
| **Externally sourced domain** | Psychology L1-L4, Plato, documented developmental sequences | Supplies domain facts, never confirmation by itself | Bad sourcing / overextension / proof transfer |
| **Interpretive domain** | Mythology, Yoga, neuroscience upper rows, initiatory comparisons | Hypothesis / translation | Selection bias |
| **Derived diagnostic** | institutional operations, economics, cognitive-role routing | Build grammar / design test | Mistaken as proof |
| **Speculative extension** | AGI, wave packets, thin archaeological or esoteric mappings | Research prompt | Conjecture inflation |

**Rule:** a cell inherits the column-class ceiling. A derived diagnostic cell can be useful, but it cannot become independent evidence for the Rosetta.

---

## 2. Required Fields

Audit the pack before its cells. Fields marked conditional become required when
their named feature is claimed.

### 2.1 Projection-pack fields

| Field | Meaning |
|---|---|
| `projection_id` | Stable namespace, for example `PHIL7`; never a generic bare `L` namespace. |
| `version` | Immutable semantic version for this meaning. |
| `owner_ref` | Source owner or controlling corpus path. |
| `source_domain` / `target_domain` | Typed domains; neither is treated as the other. |
| `native_terms` | Source vocabulary recorded before normalization. |
| `native_cardinality` | Count before grouping, insertion, omission, or row fitting. |
| `source_version` | Dated or immutable source snapshot. |
| `source_exact_digest` | Optional digest for byte-for-byte drift. |
| `source_semantic_digest` | Digest after declared harmless normalization. |
| `normalization_operations` | Ordered operations such as group, split, insert external ground, drop, reorder, translate, or choose representative. |
| `proposed_invariant` | Relation claimed to survive translation. |
| `discarded_information` | Lexical, ordinal, causal, temporal, normative, geometric, or authority-bearing loss. |
| `dependency_refs` | Projection, source, and interpreter dependencies. |
| `strongest_rival` | Best competing map or null explanation. |
| `discriminator` | Observation that would separate the projection from its rival. |
| `kill_criterion` | Condition that kills or contracts the pack claim. |
| `round_trip_test` | What should and should not survive a return projection. |
| `lifecycle_status` | Draft, active, disputed, superseded, killed, or archived. |

### 2.2 Cell fields

| Field | Meaning |
|---|---|
| `cell_id` | Stable revision ID; for example `REP6G@1:phenotype__to__G7@1:L4__r1`. |
| `source_ref` / `target_refs` | Fully namespaced terms. A target list permits one-to-many maps. |
| `relation_type` | One-to-one, one-to-many, many-to-one, analogy, inversion, boundary, unmapped, or extra. |
| `domain_expression` | Native source expression, preserved rather than renamed to its target. |
| `fit_status` | Fit, partial, multirow, unmapped, extra, disputed, killed, or archived. |
| `fact_tier` | Tier for the source-domain fact independently of Rosetta. |
| `mapping_tier` | Tier for the cross-domain placement. |
| `use_status` | Unused, proposed, authorized, attempted, or refused. |
| `outcome_status` | Not observed, observed, contradicted, replicated, or non-informative. |
| `source_basis` | Text, dataset, artifact, model, practice, runtime receipt, or observation. |
| `independence_status` | Independent, partially dependent, framework-derived, or unknown. |
| `fit_reason` | Why the relation preserves the proposed invariant. |
| `discarded_information` | Cell-specific loss beyond pack-level loss. |
| `dependency_status` / `dependency_refs` | Direct, inherited, circular, unresolved, or none, with exact references. |
| `scale` / `time_horizon` | Scope over which the mapping is proposed. |
| `strongest_rival` | Most plausible competing placement or null. |
| `discriminator` | Preregistered differentiating observation. |
| `known_biases` | Selection, translation, cultural, retrospective-fit, source-thinness, or other declared bias. |
| `kill_criterion` / `downgrade_path` | Failure condition and demote, split, kill, supersede, or archive response. |
| `commitment_receipt_refs` | Conditional: records proposals, authorizations, refusals, and attempts. |
| `outcome_receipt_refs` | Conditional: independently produced observations. |
| `operator` / `geometry` | Conditional pack-specific hypotheses, never universal required fields. |
| `adjacent_check_prev` / `adjacent_check_next` | Conditional when native or projected order is claimed. |
| `mirror_check` / `center_check` | Conditional when mirror or privileged-center structure is claimed. |
| `audit_status` / `verified_by` / `verified_at` | Append-only audit state and provenance. |

---

## 3. Status Separation Rule

Each cell carries four orthogonal status axes. Do not compress them into one
word such as “validated.”

| Axis | Question |
|---|---|
| `fact_tier` | Is the native-domain statement warranted independently of Rosetta? |
| `mapping_tier` and `fit_status` | How strongly does this directional correspondence stand? |
| `use_status` | Was a downstream use merely proposed, authorized, refused, or actually attempted? |
| `outcome_status` | What did an independently produced outcome receipt show? |

The honest public mapping tier cannot exceed its weakest relevant warrant.
Authorization never raises it. A favorable outcome may support a scoped use
claim, but it does not prove the mapping without a discriminator and rival.
Likewise, a false or unauthorized act remains causally observable even though
its normative status differs.

Examples:

| Cell | fact | mapping | use | outcome |
|---|---|---|---|---|
| `GEN7@1:L4__to__PHIL7@1:value__r1` | `[B]` discipline name | `[I]`, partial | unused | not observed |
| `REP6G@1:phenotype__to__GEN7@1:L4__r1` | source-tiered biology | `[I]`, disputed until tested | proposed | not observed |
| a killed rival revision | retained at source tier | killed | refused | contradicted or non-informative |

---

## 4. Adjacent Check

Adjacency is required only when the source or projection claims an order. It
can expose cherry-picking, but it must not manufacture a sequence in an
unordered source.

For each non-boundary cell, answer:

1. Does the previous row produce the problem this row resolves?
2. Does this row produce the tension the next row resolves?
3. Would a source-domain reader accept the order?
4. Does changing the row order make the column worse?

If the answer is no, the ordering claim is downgraded. A non-ordered analogy
may remain separately tiered.

---

## 5. Mirror Check

Mirror checks apply only to packs that explicitly project S² geometry. They
test that additional hypothesis; they are not a general Rosetta requirement or
independent evidence merely because the framework supplied the mirror.

| Pair | Required inversion |
|---|---|
| `GEN7@1:L1/L7` | Same boundary pressure, inverse direction: below-social threat vs above-social closure. |
| `GEN7@1:L2/L6` | Same half-balance position, inverse refusal: first contract / immune negation vs axiomatic release. |
| `GEN7@1:L3/L5` | Same high-balance position, inverse mode: productive building vs contemplative/system holding. |
| `GEN7@1:L4` | Self-mirror: balance, commitment, or centered agency without collapsing into either side. |

Score mirror checks as:

| Score | Meaning |
|---|---|
| `strong` | Functional inversion is obvious without framework glasses. |
| `partial` | Defensible but interpretive. |
| `fail` | No functional mirror; the cell is probably linear, decorative, or forced. |

---

## 6. Kill Criteria

Every cell needs at least one kill criterion.

| Type | Form |
|---|---|
| Namespace kill | The same bare label is shown to carry incompatible pack meanings. |
| Cardinality kill | The fit requires hiding, inventing, or silently merging native terms. |
| Source kill | A domain source does not contain the claimed category, order, or function. |
| Drift kill | The tested source version or semantic digest no longer matches. |
| Dependency kill | Apparent convergence is inherited, circular, or generated by the framework itself. |
| Adjacency kill | The previous/next rows are not source-domain neighbors or transitions. |
| Mirror kill | The mirror pair does not show functional inversion. |
| Center kill | L4 is not a domain-native center, balance node, commitment node, or demonstrable bridge. |
| Independence kill | The column was generated from the framework and then used as independent evidence. |
| Predictive kill | A pre-registered test fails. |
| Receipt kill | A claimed use or outcome lacks the distinct receipt its status requires. |

**Antifragility rule:** when a cell fails, demote or remove it before inventing a rescue. Repair only after the failed condition is recorded.

Failed revisions are append-only. A repair creates a child revision with a
supersession edge; it does not overwrite the failure. Recursive audits terminate
as resolved, underdetermined, deferred, killed, cycle-blocked, budget-exhausted,
authority-required, or source-unverifiable.

---

## 7. Cell Template

```yaml
projection_id:
version:
owner_ref:
source_domain:
target_domain:
native_terms: []
native_cardinality:
source_version:
source_exact_digest:
source_semantic_digest:
normalization_operations: []
proposed_invariant:
discarded_information: []
dependency_refs: []
strongest_rival:
discriminator:
kill_criterion:
round_trip_test:
column_class:
cells:
  - cell_id:
    source_ref:
    target_refs: []
    relation_type:
    domain_expression:
    fit_status:
    fact_tier:
    mapping_tier:
    use_status:
    outcome_status:
    source_basis: []
    independence_status:
    fit_reason:
    discarded_information: []
    dependency_status:
    dependency_refs: []
    scale:
    time_horizon:
    strongest_rival:
    discriminator:
    known_biases: []
    kill_criterion:
    downgrade_path:
    commitment_receipt_refs: []
    outcome_receipt_refs: []
    operator: null
    geometry: null
    adjacent_check_prev: null
    adjacent_check_next: null
    mirror_check: null
    center_check: null
    audit_status:
    verified_by:
    verified_at:
```

---

## 8. Workflow

1. Freeze and digest one native source before looking for target rows.
2. Inventory its terms, cardinality, order, scale, and time horizon.
3. Declare the target pack, column class, evidential ceiling, and all
   normalization operations.
4. Name the proposed invariant, discarded information, dependencies, strongest
   rival, discriminator, and kill criterion.
5. Map only the cells that fit. Record partial, multirow, unmapped, and extra
   terms without forcing a native count into seven.
6. Run adjacency, mirror, center, operator, or geometry checks only when those
   structures are actually claimed.
7. Separate fact, mapping, use, and outcome status; attach distinct commitment
   and outcome receipts when applicable.
8. Run a round-trip test and report its loss vector.
9. Append failures next to successes. A repair creates a new revision.
10. Update a theoretical owner only after review; a downstream mirror submits a
    change proposal and never mutates theory automatically.

---

## 9. Output Standard

Each audited column should produce:

- a versioned source snapshot and native-term inventory
- a projection table at the source's native cardinality
- a normalization and loss ledger
- adjacency or mirror tables only when those properties are claimed
- a failed/partial mapping appendix
- a dependency graph and source-drift check
- a rival, discriminator, round-trip result, and kill record
- a one-sentence public claim ceiling

The public claim ceiling must be one of:

| Ceiling | Meaning |
|---|---|
| `externally discriminated support` | Independent sources and a preregistered discriminator survive a named rival. |
| `structural support` | Coherent with the framework, but not independent proof. |
| `interpretive translation` | Useful map, weak evidence. |
| `derived diagnostic` | Build grammar only. |
| `failed / archived` | Does not currently hold. |

---

## Working Maxim

The Rosetta is allowed to be luminous. The audit table is allowed to be boring.

That is the trade: beauty for discovery, boredom for truth.

## Execution Surface

- **Canonical Path:** 01_EMERGENTISM/08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/10_CELL_AUDIT_SCHEMA_2026_04_25.md
