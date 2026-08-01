---
title: "Review bundle v3 — acyclic current frozen packet for FPE-REVIEW-01"
status: "ACYCLIC HASH-VERIFIED INTERNAL PACKET — CONTACT BLOCKED; not sent; no reviewer contacted"
date: 2026-08-02
evidence_tier: "[B] hashes, version lineage, and static custody graph; [S] invitation framing; no external result"
owner: "Subordinate to 02_INDEPENDENT_REVIEW.md; this version replaces v2 for future review without rewriting prior custody."
parents:
  - 02_INDEPENDENT_REVIEW.md
  - REVIEW_BUNDLE_v2.md
  - REVIEW_BUNDLE_v3.json
  - REVIEW_REGISTRY_SNAPSHOT_v3.json
  - REVIEW_BUNDLE_BINDING_CONTRACT_v1.md
---

# Review bundle v3

> **Nothing here is a result.** This is the current hash-verified packet for
> `FPE-REVIEW-01`. It is **not contact-ready** and has **not been sent**. No
> reviewer has been identified, contacted, or engaged; any reviewer who could
> satisfy this gate must be someone who **does not work here**. No review has
> been received.

## Why version 3 exists

Versions 1 and 2 remain frozen historical custody. Version 2 correctly froze
the then-current material, but its manifest also hashed `GATE_REGISTRY.json`.
That registry must record the manifest in `bundle_manifest`; updating it would
change a file that v2 itself hashes. The binding could therefore never become
true without invalidating the manifest it was meant to bind.

Version 3 replaces the mutable registry inside the frozen file set with the
deterministic `REVIEW_REGISTRY_SNAPSHOT_v3.json`. The snapshot carries only the
static review contract. The live registry binds this manifest plus a local
binding receipt outside the frozen set. The v3 checker rejects raw-registry,
self-manifest, and binding-receipt inclusion, so the graph remains acyclic.

This human-readable cover packet is itself one of the manifest's twelve
hash-bound files. Its invitation and status language therefore cannot drift
without invalidating the current frozen packet.

This is a custody repair, not a readiness promotion. It satisfies only the
mechanical `bundle_manifest` prerequisite. The six nontechnical/material
prerequisites remain missing, execution remains `blocked`, and no invitation
may be sent.

## What a reviewer will eventually be asked to do

Attack the claim and the evaluation design: prior art, comparator fairness,
identification, measurement, harm, custody, and public language. Review is
criticism, not endorsement, validation, efficacy evidence, replication, or a
vote on Emergentism. Findings retain the reviewer's declared severity and any
permitted dissent; a project response is filed separately.

The structural weakness travels with the packet: the authors designed the
practice, comparator, outcome rubric, and initial public language. A qualified
outsider is being asked to find what those authors and internal agents missed.
AI or project-agent review is useful internal search but does not satisfy this
external gate.

## Invitation draft

> **Subject:** Paid critical review of a small decision-practice claim — looking
> for the strongest case against it
>
> I have a selected seven-question decision worksheet and an unrun design for
> comparing it with strong ordinary rivals. I would like a qualified outsider to
> attack the design before any study is frozen. Compensation, if offered, is
> fixed and independent of tone or outcome. The packet includes its own
> limitations, recorded hashes, kill criteria, and permission to return a
> fatal-to-claim verdict. This is not a request for endorsement.

This text is a draft only. It names no recipient, fee, permission, ethics route,
or contact authority and cannot be sent while the registry remains blocked.

## Status

| State | Evidence |
|---|---|
| v3 static snapshot and acyclic manifest binding | **yes**, internally hash-verified on 2026-08-02 |
| verifier wired into the corpus gate | **yes** |
| complete review materials bundle; conflict form; reviewer-scope form; compensation terms; publication permission; applicability determination | **no** — all six remain missing |
| reviewer identified | **no** |
| reviewer contacted | **no** |
| review received | **no** |
| result, endorsement, validation, or replication | **none** |

**Kill for this document:** if the current manifest fails, if version lineage is
incomplete, if the snapshot no longer equals the static registry projection, or
if source bytes change without a version bump, this packet is void and no review
may be attributed to it.

•   ⊙   ○ — *the packet is internal; the verdict cannot be.*
