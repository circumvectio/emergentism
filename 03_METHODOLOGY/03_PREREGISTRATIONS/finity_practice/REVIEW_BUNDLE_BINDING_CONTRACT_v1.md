---
title: "FPE-REVIEW-01 bundle-binding contract v1"
type: review-bundle-custody-contract
status: "ACTIVE TECHNICAL CUSTODY CONTRACT — no human prerequisite satisfied"
date: 2026-08-02
evidence_tier: "[S] hash-topology and custody rule; no review, contact, or result"
semantic_authority: none
owner: "03_METHODOLOGY/03_PREREGISTRATIONS/finity_practice"
parents:
  - 02_INDEPENDENT_REVIEW.md
  - GATE_REGISTRY.json
  - REVIEW_BUNDLE_v3.json
---

# FPE-REVIEW-01 bundle-binding contract v1

## Purpose

This is a technical custody contract for the independent-review packet. It
repairs the impossible v2 graph in which a frozen manifest hashed the mutable
registry that needed to bind that same manifest. It does not choose a reviewer,
complete a form, authorize compensation, decide ethics, permit publication,
make contact, or report external review.

## The v3 graph

```text
static allow-list projection of GATE_REGISTRY
                 -> REVIEW_REGISTRY_SNAPSHOT_v3.json
                 -> REVIEW_BUNDLE_v3.json

REVIEW_BUNDLE_v3.json + local binding receipt
                 -> GATE_REGISTRY.json.execution.prerequisites.bundle_manifest
```

The first arrow carries only a static description of `FPE-REVIEW-01`. The
second binds the immutable review materials. The last records that this exact
manifest was internally assembled and checked. No arrow points back into a file
that the manifest hashes.

## Static projection allow-list

The snapshot may contain only:

- registry schema and program identity;
- definition source, semantic-owner IDs, claim-card and docket bindings;
- packet/contact vocabularies and program boundary;
- the static external-custody rule, never an external-state record;
- the review gate's ID, title, packet path and hash, claim/docket bindings,
  dependency IDs, possible move, forbidden move, kill/revise language,
  prerequisite *names*, and readiness condition.

It must exclude every execution state, prerequisite record, artifact digest,
receipt, external-state record, reviewer identity, contact event, result, and
the `bundle_manifest` back-reference. A changed static projection requires a
new snapshot and a new bundle version; a changed runtime record does not alter
an already frozen bundle.

## Frozen-bundle exclusions

`REVIEW_BUNDLE_v3.json` must not list:

1. the raw `GATE_REGISTRY.json`;
2. its own manifest path; or
3. its binding receipt.

It must list the matching versioned registry snapshot and this contract. The
checker recomputes the projection, verifies the snapshot, checks the manifest
and receipt hashes recorded by the live registry, and rejects all three
forbidden entries.

## State boundary

The v3 binding may satisfy only the technical `bundle_manifest` prerequisite.
The following six remain missing until real, appropriate custody exists:

- `complete_review_materials_bundle`;
- `conflict_form`;
- `reviewer_scope_form`;
- `compensation_terms`;
- `publication_permission`; and
- `applicability_determination_recorded`.

Therefore `FPE-REVIEW-01` remains `typed` / `deferred` / `blocked`. A blank
template is not a completed declaration, an owner decision, an ethics
determination, a reviewer, a contact event, or a verdict.

## Reproduce

```bash
python3 09_TOOLS/01_SCRIPTS/check_review_bundle.py
python3 -m unittest 09_TOOLS/02_COMPILERS/test_review_bundle.py
python3 -m unittest 09_TOOLS/02_COMPILERS/test_finity_practice_gates.py
```

## Kill condition

This contract fails if a mutable registry is reintroduced into a frozen bundle,
if the snapshot does not equal the allow-list projection, if the registry binds
the wrong manifest or receipt, if a human prerequisite is silently marked
satisfied, or if any internal artifact is presented as external review.

*The graph can close a self-reference without closing the world.*
