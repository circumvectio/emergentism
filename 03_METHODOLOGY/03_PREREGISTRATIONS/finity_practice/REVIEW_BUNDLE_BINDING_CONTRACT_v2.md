---
title: "FPE-REVIEW-01 provenance-binding contract v2"
type: review-bundle-custody-contract
status: "ACTIVE TECHNICAL PROVENANCE FIREWALL — no owner, external, or ethics prerequisite satisfied"
date: 2026-08-02
evidence_tier: "[S] local schema, hash, and fail-closed rule; no review, contact, authorization, or result"
semantic_authority: none
owner: "03_METHODOLOGY/03_PREREGISTRATIONS/finity_practice"
parents:
  - REVIEW_BUNDLE_BINDING_CONTRACT_v1.md
  - 02_INDEPENDENT_REVIEW.md
  - GATE_REGISTRY.json
  - REVIEW_BUNDLE_v4.json
---

# FPE-REVIEW-01 provenance-binding contract v2

## Purpose

Version 3 repaired an impossible manifest/registry self-hash. Version 4 closes
a separate local gap: a generic contained file plus a matching digest and
receipt could otherwise look like any satisfied prerequisite. This contract
types every `FPE-REVIEW-01` prerequisite before any form, person, permission,
ethics determination, payment, contact, or verdict exists.

The `requires_owner_authority` field is a JSON boolean, and
`requires_external_state` is exactly a string or JSON `null`; numeric lookalikes
are rejected. The v4 manifest also has a fixed 21-file inventory: twelve current
packet files and nine retained historical artifacts. It may not silently drop,
substitute, add, or traverse a symlinked artifact path under the same version.
The retained historical bytes are always verified locally; their frozen Git
content commits are an additional reconstruction check when the checkout still
has those objects, not a claim that an export has lost packet custody.

## Frozen v4 contract

```text
static provenance contract + owner state-at-freeze
                 -> REVIEW_REGISTRY_SNAPSHOT_v4.json
                 -> REVIEW_BUNDLE_v4.json

REVIEW_BUNDLE_v4.json + local binding receipt
                 -> GATE_REGISTRY.json.execution.prerequisites.bundle_manifest
```

The snapshot carries the rule, not mutable prerequisite evidence, external
state, a reviewer identity, contact event, or result. The raw registry,
manifest self-reference, and binding receipt remain excluded from the manifest.

| Prerequisite | Required provenance kind | Extra boundary |
|---|---|---|
| `bundle_manifest` | `technical_binding` | v4 manifest plus its local binding receipt only |
| `complete_review_materials_bundle` | `technical_materials_bundle` | v4 accepts no local materials assertion or template |
| `compensation_terms` | `owner_attestation` | v4 accepts no local owner-attestation record |
| `conflict_form` | `external_declaration` | v4 accepts no local reviewer declaration |
| `reviewer_scope_form` | `external_declaration` | v4 accepts no local reviewer declaration |
| `publication_permission` | `external_declaration` | v4 accepts no local reviewer declaration |
| `applicability_determination_recorded` | `applicability_determination` | v4 accepts no local ethics/applicability assertion |

## Owner-authority boundary

The v4 contract freezes `D-OWNER-03` as **`unset`**. Therefore all six
non-bundle prerequisite records remain `missing` with no artifact, digest, or
receipt. The packet remains `typed` / `deferred` / `blocked`, and
`reviewers_engaged` remains absent.

A later selection is material context, not a mutable implementation detail. It
must be a new frozen packet version and a separately reviewed schema with an
independent verification boundary. That successor must bind the actual
`D-OWNER-03` decision and its named principal, actor, terms/cap, scope,
redaction, ethics/jurisdiction, custody/retention, expiry/revocation, contest
path, and consequence bearers. This contract supplies none of them and accepts
no locally authored substitute.

## Future evidence rule

Version 4 intentionally defines **no accepted local future-evidence format**.
Even a contained, hash-bound JSON file stays insufficient: it cannot
authenticate a principal, prove consent or independence, establish an ethics
determination, or turn a self-authored receipt into an external event. The v4
registry therefore rejects every non-bundle `satisfied` state and every present
external-state record.

Before a successor can accept a complete materials bundle, it must require a
schema-checked manifest that enumerates and hash-binds the four arms, consent
draft, rubric, analysis plan, safety plan, data dictionary, retention schedule,
and preregistration target. Before it can accept owner or external evidence, it
must also define and independently review the relevant verification boundary.

## Negative controls

The gate fails if:

1. an assignment is omitted, renamed, or retyped without a new frozen packet;
2. `D-OWNER-03` is changed from `unset`, or any non-bundle review prerequisite
   carries evidence;
3. a Markdown file, blank template, generic receipt, or locally authored JSON
   is used to claim owner, material, external, or ethics completion;
4. any external-state record is marked present in the custody-only v4 registry;
   or
5. a v4 manifest downgrades to the v1 binding profile, drops or adds any fixed
   packet artifact, changes its frozen historical-artifact custody, rebinds to
   any contract other than this v2 contract, or traverses a symlinked path.

## Reproduce

```bash
python3 09_TOOLS/01_SCRIPTS/check_review_bundle.py
python3 -m unittest 09_TOOLS/02_COMPILERS/test_review_bundle.py
python3 -m unittest 09_TOOLS/02_COMPILERS/test_finity_practice_gates.py
```

*A typed receipt can reject a false local promotion. It cannot turn local text
into a person, a permission, or a world event.*
