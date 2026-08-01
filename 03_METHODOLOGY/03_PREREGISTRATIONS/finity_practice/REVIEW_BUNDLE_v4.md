---
title: "Review bundle v4 — provenance-firewalled packet for FPE-REVIEW-01"
status: "ACYCLIC HASH-VERIFIED INTERNAL PACKET — CONTACT BLOCKED; not sent; no reviewer contacted"
date: 2026-08-02
evidence_tier: "[B] hashes, static provenance contract, and custody graph; [S] invitation framing; no external result"
owner: "Subordinate to 02_INDEPENDENT_REVIEW.md; v4 hash-locks retained v1–v3 artifacts and changes no external state."
parents:
  - 02_INDEPENDENT_REVIEW.md
  - REVIEW_BUNDLE_v3.md
  - REVIEW_BUNDLE_v4.json
  - REVIEW_REGISTRY_SNAPSHOT_v4.json
  - REVIEW_BUNDLE_BINDING_CONTRACT_v2.md
---

# Review bundle v4

> **Nothing here is a result.** This is the current hash-verified packet for
> `FPE-REVIEW-01`. It is **not contact-ready** and has **not been sent**. No
> reviewer has been identified, contacted, or engaged; any reviewer who could
> satisfy this gate must be someone who **does not work here**. No review has
> been received.

## Why version 4 exists

Versions 1–3 are retained historical manifests, not replayable packets against
the mutable current source paths. Version 4 hash-locks their immutable artifact
files and freezes both each version's initial commit and each artifact's
content commit for reconstruction; the checker hash-verifies those Git blobs
when they are locally available. A source export or shallow checkout still
verifies the retained current bytes and reports Git-origin reconstruction as
unreplayed. It does not claim that their old source lists still match current
bytes. Version 3 repaired the manifest/registry self-hash by replacing the
mutable registry with a static snapshot. Version 4 preserves that acyclic graph and freezes a
per-prerequisite provenance contract: the manifest binding is technical, while
the other named categories remain requirements that no local record can clear.

The `D-OWNER-03` authority state in this version is **unset**. That is a
boundary, not an authority decision: every non-bundle prerequisite remains
missing, and the checker rejects a generic local file, blank template,
hash-matching receipt, locally authored owner selection, or present
external-state record as a substitute. A later owner selection changes the
frozen context and requires a new bundle version, reviewed successor schema,
and independent verification boundary.

This human-readable packet is one of twelve required current-packet files in
the manifest's twenty-one hash-bound files; the other nine are retained v1–v3
artifacts. The checker rejects any omitted, added, or symlinked inventory path.
Its invitation, status, and provenance language cannot drift without
invalidating the current frozen packet.

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
| v4 static snapshot, acyclic manifest binding, and provenance contract | **yes**, internally hash-verified on 2026-08-02 |
| owner authority | **unset** — no principal, mandate, or selection has been recorded |
| verifier wired into the corpus gate | **yes** — internal custody only; no local owner or external evidence is accepted |
| complete review materials bundle; conflict form; reviewer-scope form; compensation terms; publication permission; applicability determination | **no** — all six remain missing |
| reviewer identified | **no** |
| reviewer contacted | **no** |
| review received | **no** |
| result, endorsement, validation, or replication | **none** |

**Kill for this document:** if the current manifest fails, if its required
inventory, version lineage, retained historical-artifact hashes, or historical
content commits conflict when locally replayable, if the snapshot no longer
equals the static registry projection, if the frozen provenance contract drifts,
or if current source bytes change without a version bump, this packet is void
and no review may be attributed to it.

•   ⊙   ○ — *the packet is internal; the verdict cannot be.*
