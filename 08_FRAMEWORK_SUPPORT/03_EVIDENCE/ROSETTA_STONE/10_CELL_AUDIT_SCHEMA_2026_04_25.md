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

The stable native-term reference is `pack_id@version:term_key`. Bare `Lx`
references are invalid outside a single declared pack. A v1 cell that used a
bare row remains historical input; it is not silently reinterpreted as a v2
cell.

A reference is not a snapshot lock. Every active projection binds both its
source and every target to `rs.pack_snapshot_binding.v1`: PackManifest-model
digest, owner, source version, and exact-source digest. Registry presence,
availability, health, or a matching string ID cannot substitute for the bound
model. A target drift is as disqualifying as a source drift.

---

## 1. Column Class

Every column gets a class before any cell is scored.

| Class | Examples | Evidential use | Primary risk |
|---|---|---|---|
| **Anchor** | Operator, geometry, equation, balance | Defines the selected grammar | Internal inconsistency |
| **Declared chain** | Varna, reasoning, pramana, -ology, regime | Tests a selected crosswalk; does not assert causation | Circular validation / person typing |
| **Externally sourced domain** | source-defined psychological stages, Plato, documented developmental sequences | Supplies domain facts, never confirmation by itself | Bad sourcing / overextension / proof transfer |
| **Interpretive domain** | Mythology, Yoga, neuroscience upper rows, initiatory comparisons | Hypothesis / translation | Selection bias |
| **Derived diagnostic** | institutional operations, economics, cognitive-role routing | Build grammar / design test | Mistaken as proof |
| **Speculative extension** | AGI, wave packets, thin archaeological or esoteric mappings | Research prompt | Conjecture inflation |

**Rule:** a cell inherits the column-class ceiling. A derived diagnostic cell can be useful, but it cannot become independent evidence for the Rosetta.

---

## 2. Required Fields

Audit the pack before its cells. Fields marked conditional become required when
their named feature is claimed.

At ledger root, `evidence_tier_vocabulary` enumerates the accepted warrant-kind
symbols. It is a set serialized as a unique string list; list position has no
precedence meaning. The former `tier_order` field is invalid because it
mis-types evidence kinds as a total ladder.

### 2.1 Pack-manifest fields

| Field | Meaning |
|---|---|
| `schema_version` | `rs.pack_manifest.v2` for active records; v1 string-only packs are historical/read-only. |
| `pack_id` | Stable native namespace, for example `PHIL7`; never a generic bare `L` namespace. |
| `version` | Immutable semantic version for this meaning. |
| `owner_ref` | Source owner or controlling corpus path. |
| `native_domain` | Typed native domain represented by the pack. |
| `native_terms` | Source vocabulary recorded before normalization. |
| `native_term_definitions` | Ordered `{term_key, label, description}` records; keys exactly equal `native_terms`. |
| `native_cardinality` | Count of native terms before any projection operation. |
| `source_version` | Dated or immutable source snapshot. |
| `digest_algorithm` | `sha256` for v1. |
| `source_exact_digest` | Required digest of the exact source byte stream. |
| `native_expression_digest_algorithm` / `native_expression_digest_canonicalization` / `native_expression_digest` | SHA-256 over canonical ordered key-label-description records (`rs.native_term_definitions.v1`). |
| `semantic_digest_status` | `PROVISIONAL` until a versioned canonical serialization is declared. |
| `semantic_canonicalization_id` / `semantic_canonicalization_version` | Conditional semantic-digest procedure. |
| `digest_normalization_operations` | Harmless byte canonicalization only; never mapping operations. |
| `lifecycle_status` | `DRAFT`, `ACTIVE`, `DISPUTED`, `SUPERSEDED`, `KILLED`, or `ARCHIVED`. |

### 2.2 Projection-manifest fields

| Field | Meaning |
|---|---|
| `schema_version` | Machine contract version: `rs.projection_manifest.v2` for active records; v1 is historical/read-only. |
| `projection_id` | Stable name for one directional interpretation. |
| `projection_revision` | Immutable positive revision number. |
| `parent_revision` | Previous revision in the audit graph, if any. |
| `supersedes_ref` | Exact prior projection revision replaced without erasure. |
| `source_pack_ref` / `target_pack_refs` | Versioned pack refs; direction is explicit. |
| `source_pack_binding` / `target_pack_bindings` | Typed source and target snapshot bindings: pack ref, owner, source version, exact-source digest, PackManifest-model digest algorithm, canonicalization, and digest. Bindings are required even when packs are locally available. |
| `normalization_operations` | Ordered group, split, insert, drop, reorder, translate, or choose-representative operations. |
| `proposed_invariant` | Relation claimed to survive translation. |
| `discarded_information` | Lexical, ordinal, causal, temporal, normative, geometric, or authority-bearing loss. |
| `dependency_refs` | Typed `rs.dependency_binding.v1` records. `BOUND` names owner, immutable version, SHA-256 digest and canonicalization; `PACK` reuses its pack binding values. `DEFERRED` nulls binding fields and states why. Availability strings and bare `kind + ref` pairs are invalid. |
| `strongest_rival` | Best competing map or null explanation. |
| `discriminator` | Observation that would separate the projection from its rival. |
| `kill_criterion` | Condition that kills or contracts the projection. |
| `round_trip_test` | What should and should not survive a return projection. |
| `claim_digest_algorithm` / `claim_digest_canonicalization` / `claim_semantic_digest` | Stable fingerprint of two-sided bindings and mapping semantics, excluding mutable application statuses. |
| `resolution_status` | Bounded recursive status: resolved, underdetermined, deferred, killed, cycle-blocked, budget-exhausted, authority-required, or source-unverifiable. |
| `resolution_dispositions` | Append-only `rs.resolution_disposition.v1` history. A current RESOLVED disposition binds the exact projection/claim, non-circular full audit-state digest, complete lineage, scoped limitations, decision authority/custody, discriminator and evidence results, and an independent trusted external attestation. It always sets `world_efficacy_claim: false`. |
| `predecessor_comparisons` | Typed comparison against every predecessor: ref, claim digest, accepted/rejected result, reason, external-verifier attestation. |
| `rejected_claim_digests` | Monotonic inherited set; prevents rejected claims being healed by remove/re-add or aliasing. |
| `lifecycle_status` | `DRAFT`, `ACTIVE`, `DISPUTED`, `SUPERSEDED`, `KILLED`, or `ARCHIVED`. |

### 2.3 Cell fields

| Field | Meaning |
|---|---|
| `cell_id` | Stable cell ID within a projection revision; for example `REP6_TO_GEN7@1:phenotype_to_L4`. |
| `projection_ref` | Owning `projection_id@revision`. |
| `source_ref` / `target_refs` | Fully namespaced terms. A target list permits one-to-many maps. |
| `relation_type` | `ONE_TO_ONE`, `ONE_TO_MANY`, `MANY_TO_ONE`, `ANALOGY`, `INVERSION`, `BOUNDARY`, `UNMAPPED_SOURCE`, `UNFILLED_TARGET`, or `EXTRA`. |
| `domain_expression` | Native source expression, preserved rather than renamed to its target. |
| `fit_status` | `FIT`, `PARTIAL`, `MULTIROW`, `UNMAPPED_SOURCE`, `UNFILLED_TARGET`, `EXTRA`, `DISPUTED`, `KILLED`, or `ARCHIVED`. |
| `fact_tier` | Warrant kind for the source-domain fact independently of Rosetta. |
| `mapping_tier` | Warrant kind for the cross-domain placement. |
| `authorization_status` | `NOT_REQUESTED`, `PENDING`, `AUTHORIZED`, `REFUSED`, `EXPIRED`, `REVOKED`, `INVALID`, `ABSENT`, or `NOT_REQUIRED`; separate from causal use. |
| `use_status` | `UNUSED`, `PROPOSED`, `ATTEMPTED`, or `ABORTED`; an attempt does not imply authority. |
| `outcome_status` | `NOT_OBSERVED`, `OBSERVED`, `CONTRADICTED`, `REPLICATED`, or `NON_INFORMATIVE`. |
| `source_basis` | Text, dataset, artifact, model, practice, runtime receipt, or observation. |
| `independence_status` | Independent, partially dependent, framework-derived, or unknown. |
| `fit_reason` | Why the relation preserves the proposed invariant. |
| `discarded_information` | Cell-specific loss beyond pack-level loss. |
| `dependency_status` / `dependency_refs` | Direct, inherited, circular, unresolved, or none, with digest-bound typed dependencies or an explicit deferred state. |
| `scale` / `time_horizon` | Scope over which the mapping is proposed. |
| `strongest_rival` | Most plausible competing placement or null. |
| `discriminator` | Preregistered differentiating observation. |
| `known_biases` | Selection, translation, cultural, retrospective-fit, source-thinness, or other declared bias. |
| `kill_criterion` / `downgrade_path` | Failure condition and demote, split, kill, supersede, or archive response. |
| `authorization_envelope_ref` | Conditional typed binding for an authority-bearing claim: envelope ref/digest, principal, mandate, scope, consent, custody, validity, expiry or revocation, contest path, actor, and consequence bearers. |
| `status_transitions` | Append-only transitions; every transition carries a typed external-verifier attestation over the changed subject digest. |
| `commitment_receipt_refs` / `commitment_provenance_records` | Proposal or attempt receipts plus typed issuer, evidence-authority, custody, record digest, and signature or attestation. |
| `outcome_receipt_refs` / `outcome_provenance_records` | Observation receipts plus typed issuer, evidence-authority, observation and digest, custody, method, independence basis, and signature or attestation. |
| `operator` / `geometry` | Conditional pack-specific hypotheses, never universal required fields. |
| `adjacent_check_prev` / `adjacent_check_next` | Conditional when native or projected order is claimed. |
| `mirror_check` / `center_check` | Conditional when mirror or privileged-center structure is claimed. |
| `audit_status` / `verified_by` / `verified_at` | Append-only audit state and provenance. |

---

## 3. Status Separation Rule

Each cell carries five orthogonal semantic status families in six recorded
fields. The mapping family deliberately separates `mapping_tier` from
`fit_status`; do not compress either, or any family, into one word such as
“validated.”

| Axis | Question |
|---|---|
| `fact_tier` | Is the native-domain statement warranted independently of Rosetta? |
| `mapping_tier` and `fit_status` | What is the mapping warrant, and how does this directional correspondence stand? |
| `authorization_status` | Was authority absent, pending, valid, refused, expired, revoked, invalid, or not required? |
| `use_status` | Was a downstream use unused, proposed, attempted, or aborted? |
| `outcome_status` | What did an independently produced outcome receipt show? |

The six evidence symbols `[A]`, `[B]`, `[S]`, `[I]`, `[C]`, and `[D]` are
distinct warrant kinds, not a total ladder. Their position in a serialized
vocabulary has no strength meaning. A `mapping_tier` is justified by its own
mapping basis; the checker does not rank or compare it with `fact_tier`.
Authorization never changes either kind. A favorable outcome may support a
scoped use claim, but it does not prove the mapping without a discriminator and
rival. Likewise, a false or unauthorized act remains causally observable even
though its normative status differs.

Every recorded status transition requires a complete
`rs.external_verifier_attestation.v1` with attestation ref, verifier and
evidence-authority refs, independence basis, subject ref and SHA-256 digest,
old/new status binding, verification method, issue time, custody, and
`signature_or_attestation_ref`. A self-report, receipt count, or
application-owned verifier cannot certify its own status change. In addition,
every changed `fact_tier` or `mapping_tier` requires a non-empty receipt basis;
this applies to every direction of change because the symbols have no rank.

```yaml
axis: outcome_status
from: NOT_OBSERVED
to: OBSERVED
recorded_at: immutable timestamp
reason: bounded reason
receipt_refs: []
external_verifier_attestation:
  schema_version: rs.external_verifier_attestation.v1
  attestation_ref:
  verifier_ref:
  verifier_authority_ref:
  independence_basis:
  subject_ref:
  status_axis: outcome_status
  from_status: NOT_OBSERVED
  to_status: OBSERVED
  subject_digest_algorithm: sha256
  subject_digest_canonicalization: rs.status_transition_subject.v1
  subject_digest:
  verification_method_ref:
  issued_at:
  custody_ref:
  signature_or_attestation_ref:
```

The subject digest is canonical JSON over schema version, subject ref, axis,
old state, new state, record time, reason, and ordered receipt refs. The
checker recomputes it and rejects a detached or replayed attestation.

`authorization_status: AUTHORIZED` also requires a complete
`rs.authorization_envelope_ref.v1`. It binds a stable external envelope and
digest to principal, mandate, scope, consent, custody, validity start, expiry
or revocation registry and last check, contest path, actor, and consequence
bearers. An unauthorized attempt remains representable as `ABSENT`, `INVALID`,
or `REFUSED` plus `ATTEMPTED`; its causal evidence is not erased.

Commitment and outcome provenance are separate typed record sets. Their issuer
sets and evidence-authority sets must be disjoint for the same claim.
`REPLICATED` requires at least two outcome records with distinct issuers,
evidence authorities, observation refs, and custody chains plus stated
independence bases. Two references, digests, signatures, or transports under
one effective authority do not constitute replication.

Examples:

| Cell | fact | mapping | authorization | use | outcome |
|---|---|---|---|---|---|
| `GEN7_TO_PHIL7@1:L4_to_value` | `[B]` discipline name | `[I]`, `PARTIAL` | `NOT_REQUESTED` | `UNUSED` | `NOT_OBSERVED` |
| `REP6_TO_GEN7@1:phenotype_to_L4` | source-tiered biology | `[I]`, `DISPUTED` until tested | `PENDING` | `PROPOSED` | `NOT_OBSERVED` |
| an unauthorized but observed attempt | retained at source tier | unchanged | `ABSENT` | `ATTEMPTED` | `OBSERVED` with external provenance |

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
| Drift kill | A bound source or target PackManifest-model digest, source version, or exact-source digest no longer matches. |
| Dependency kill | Apparent convergence is inherited, circular, or generated by the framework itself. |
| Adjacency kill | The previous/next rows are not source-domain neighbors or transitions. |
| Mirror kill | The mirror pair does not show functional inversion. |
| Center kill | L4 is not a domain-native center, balance node, commitment node, or demonstrable bridge. |
| Independence kill | The column was generated from the framework and then used as independent evidence. |
| Predictive kill | A pre-registered test fails. |
| Authorization kill | An authority-bearing status lacks a complete envelope or typed external-verifier attestation. |
| Receipt kill | A claimed use or outcome lacks typed provenance, or commitment and outcome issuers/evidence authorities overlap. |
| Replication kill | `REPLICATED` is based on multiple refs without independent issuers, evidence authorities, observations, custody, and independence bases. |
| Lineage kill | A resolved run skips or rejects a predecessor comparison, drops an inherited rejection, or remove/re-adds the same rejected claim digest. |

**Antifragility rule:** when a cell fails, demote or remove it before inventing a rescue. Repair only after the failed condition is recorded.

Failed revisions are append-only. A repair creates a child revision with a
supersession edge; it does not overwrite the failure. Recursive audits terminate
as `RESOLVED`, `UNDERDETERMINED`, `DEFERRED`, `KILLED`, `CYCLE_BLOCKED`,
`BUDGET_EXHAUSTED`, `AUTHORITY_REQUIRED`, or `SOURCE_UNVERIFIABLE`.

`RESOLVED` requires an `ACCEPTED` externally attested comparison against every
predecessor in the ancestral path. Rejection sets are monotonic. A rejected
claim fingerprint cannot become resolved through deletion, reordered import,
aliasing, or remove/re-add; a materially changed claim gets a new digest while
retaining the rejected predecessor and its reason.

`RESOLVED` additionally requires a separate current
`rs.resolution_disposition.v1`; the status declaration cannot certify itself.
Disposition history is append-only and predecessor-linked. The current record
binds the exact projection ref and claim digest; SHA-256 of
`rs.projection_resolution_audit_state.v1`; non-empty bounded scopes,
limitations, discriminator-result refs, and evidence-result refs; the complete
root-to-current lineage and one comparison-attestation ref per edge; accountable
disposition authority, decision ref/custody, trust boundary, timestamp and
reason; and an `rs.external_verifier_attestation.v1` over the full disposition
subject. The audit-state digest includes the manifest except the circular
resolution declaration/current history, plus all prior dispositions. The
verifier identity, evidence authority, and custody remain outside the decision
authority, decision custody, and source/target owner boundary.

Structural validation of the attestation object is not trust validation. A
consumer accepts a disposition as trusted only when an external verifier has
checked the attestation against the named trust boundary and verification
method; a caller-declared signature or attestation ref alone is insufficient.
This applies separately to every root-to-current comparison attestation: the
consumer recovers the exact ancestor comparison object, recomputes its subject
digest, and validates it through the external trust boundary. Merely listing
the ancestor attestation refs cannot qualify a resolution.

Allowed disposition scopes are `SCHEMA_CONFORMANCE`, `SOURCE_AND_CUSTODY`,
`MAPPING_DISAMBIGUATION`, `APPLICATION_EVIDENCE`, and
`REGIME_CONTROL_ANALYSIS`. A theoretical disposition must explicitly record
`world_efficacy_claim: false`; resolving one or more audit scopes is not a claim
that an applied intervention works.

Each predecessor record uses `rs.predecessor_comparison.v1` with
`predecessor_ref`, `predecessor_claim_digest`, `comparison_status`,
`comparison_reason`, and a complete external attestation. That attestation
binds `status_axis: predecessor_comparison`, `from_status: UNREVIEWED`, the
accepted/rejected result, and an
`rs.predecessor_comparison_subject.v1` digest. The subject includes the
current/predecessor pair, predecessor claim digest, result, and reason.

### 6.1 `RS.REGIME@1` control record

Regime analysis records control distributions, not deterministic political
labels. For each declared surface and observation window it requires:

| Field | Meaning |
|---|---|
| `surface_ref` / `observation_window` | Exact control surface and bounded interval. |
| `controller_refs` / `controller_plurality` | Controllers plus count and inclusion rule; nominal plurality alone is not independence. |
| `concentration_measure` | Named metric, denominator, value, and uncertainty. |
| `alias_coalitions` | Shared signer, owner, mandate, funding, custody, infrastructure, evidence authority, or failure-domain links. |
| `contestability` | Eligible challengers, path, cost, latency, and observed disposition. |
| `revocability` | Revoker, scope, latency, test evidence, and observed effectiveness. |
| `dependency_refs` | Technical, legal, financial, informational, and custodial dependencies using the same digest-bound or explicitly deferred typed records. |
| `receipt_independence` | Commitment/outcome issuer, evidence-authority, custody, and verifier separation. |
| `observed_consequences` | Receipted effects, uncertainty, and consequence bearers. |
| `longitudinal_capture_signatures` | Repeated cross-surface concentration or suppression patterns over time. |
| `political_label` | Must be `null` in this contract. A named regime is a separate historical-institutional claim. |

```yaml
schema_ref: RS.REGIME@1
surface_ref:
observation_window: {start: null, end: null, inclusion_rule: null}
controller_refs: []
controller_plurality: {count: null, inclusion_rule: null}
concentration_measure: {metric: null, denominator: null, value: null, uncertainty: null}
alias_coalitions: []
contestability: {eligible_challengers: [], path_ref: null, cost: null, latency: null, observed_disposition: null}
revocability: {revoker_refs: [], scope: null, latency: null, test_evidence_refs: [], observed_effectiveness: null}
dependency_refs: []
receipt_independence: {commitment_issuer_refs: [], outcome_issuer_refs: [], evidence_authority_refs: [], custody_refs: [], verifier_refs: []}
observed_consequences: []
longitudinal_capture_signatures: []
political_label: null
```

An alias coalition is analyzed as one effective controller for the affected
surface unless evidence discriminates its members. A capture signature is
longitudinal evidence, not a one-time score. No row, threshold, or signature in
`RS.REGIME@1` deterministically emits tyranny, democracy, oligarchy, timocracy,
aristocracy, anarchy, theocracy, or any person type.

---

## 7. Cell Template

```yaml
pack_manifest:
  schema_version: rs.pack_manifest.v2
  pack_id:
  version:
  owner_ref:
  native_domain:
  native_terms: []
  native_term_definitions:
    - term_key:
      label:
      description:
  native_cardinality:
  source_version:
  digest_algorithm: sha256
  source_exact_digest:
  native_expression_digest_algorithm: sha256
  native_expression_digest_canonicalization: rs.native_term_definitions.v1
  native_expression_digest:
  semantic_digest_status: PROVISIONAL
  semantic_canonicalization_id: null
  semantic_canonicalization_version: null
  digest_normalization_operations: []
  lifecycle_status: DRAFT

projection_manifest:
  schema_version: rs.projection_manifest.v2
  projection_id:
  projection_revision:
  parent_revision: null
  supersedes_ref: null
  source_pack_ref:
  source_pack_binding:
    binding_schema: rs.pack_snapshot_binding.v1
    pack_ref:
    owner_ref:
    source_version:
    source_exact_digest:
    pack_manifest_digest_algorithm: sha256
    pack_manifest_digest_canonicalization: rs.pack_manifest_digest.v1
    pack_manifest_digest:
  target_pack_refs: []
  target_pack_bindings: []
  normalization_operations: []
  proposed_invariant:
  discarded_information: []
  dependency_refs:
    - binding_schema: rs.dependency_binding.v1
      kind:
      ref:
      binding_status: BOUND
      owner_ref:
      version:
      digest_algorithm: sha256
      digest_canonicalization:
      digest:
      deferred_reason: null
  strongest_rival:
  discriminator:
  kill_criterion:
  round_trip_test:
  claim_digest_algorithm: sha256
  claim_digest_canonicalization: rs.projection_claim_digest.v1
  claim_semantic_digest:
  resolution_status: UNDERDETERMINED
  resolution_dispositions: []
  predecessor_comparisons: []
  rejected_claim_digests: []
  column_class:
  lifecycle_status: DRAFT
  cells:
    - cell_id:
      projection_ref:
      source_ref:
      target_refs: []
      relation_type:
      domain_expression:
      fit_status:
      fact_tier:
      mapping_tier:
      authorization_status: NOT_REQUESTED
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
      authorization_envelope_ref: null
      commitment_receipt_refs: []
      commitment_provenance_records: []
      outcome_receipt_refs: []
      outcome_provenance_records: []
      operator: null
      geometry: null
      adjacent_check_prev: null
      adjacent_check_next: null
      mirror_check: null
      center_check: null
      audit_status:
      verified_by:
      verified_at:
      status_transitions: []
```

---

## 8. Workflow

1. Freeze and digest the native source before looking for target rows; bind
   ordered native keys, labels, and descriptions as well as exact source bytes.
2. Inventory its terms, cardinality, order, scale, and time horizon.
3. Freeze **every target pack** and declare a directional projection revision.
   Record source and target PackManifest-model digests, exact-source digests,
   source versions, column class, evidential ceiling, and all normalization
   operations. Availability strings do not satisfy this step.
4. Name the proposed invariant, discarded information, dependencies, strongest
   rival, discriminator, and kill criterion.
5. Map only the cells that fit. Record partial, multirow, unmapped, and extra
   terms without forcing a native count into seven.
6. Run adjacency, mirror, center, operator, or geometry checks only when those
   structures are actually claimed.
7. Separate fact, mapping, authorization, use, and outcome status. Attach an
   external-verifier attestation to every transition and a non-empty receipt
   basis to every changed fact or mapping evidence kind; attach a complete
   envelope to authority-bearing status and typed commitment/outcome provenance
   with disjoint issuers and evidence authorities.
8. Run a round-trip test and report its loss vector.
9. Append failures next to successes. A repair creates a new revision, compares
   every predecessor, and inherits all rejected claim digests. Never heal a
   rejected intermediary by remove/re-add.
10. Update a theoretical owner only after review; a downstream mirror submits a
    change proposal and never mutates theory automatically.

---

## 9. Output Standard

Each audited column should produce:

- versioned source and target snapshots, PackManifest-model bindings, and
  native-term key-label-description inventories
- a projection table at the source's native cardinality
- a normalization and loss ledger
- adjacency or mirror tables only when those properties are claimed
- a failed/partial mapping appendix
- a dependency graph and two-sided source/target drift check
- an attestation, authorization, and commitment/outcome provenance audit
- a complete predecessor-comparison and inherited-rejection ledger
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
