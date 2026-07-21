---
rosetta:
  primary_level: L4
  primary_column: Philosophy
  secondary:
    - level: L3
      column: Philosophy
      role: "classify drift hits by evidence tier and genre"
    - level: L6
      column: Philosophy
      role: "bound books, mirrors, audits, and archives as different authority classes"
    - level: L5
      column: Philosophy
      role: "stabilize drift scans as corpus governance architecture"
  operator: "Arjuna ⚔"
  tier: "God"
  regime: "Kṣatriya"
  register: "[S/I]"
  canonical_phrase: "Drift Scan Discipline — Genre-Aware Governance"
---

# Drift Scan Discipline

**Status:** Active governance rule
**Evidence tier:** [S] Corpus governance
**Date:** 2026-04-26
**Depends on:** `00_THREE_HATS.md`, `00_CORE_CONCEPTS.md`, `00_ANTIFRAGILITY_PROTOCOL.md`, `../../02_EPISTEMOLOGY/01_EVIDENCE_TIERS/00_THE_HONEST_POSITION.md`

## Purpose

`08_FRAMEWORK_SUPPORT/` is not one genre. It contains source canon, operator
specs, books, generated release mirrors, peer-review packets, historical audit
closeouts, and public deliverables. A flat drift scan will therefore be noisy by
design.

This document defines how to read the noise.

## Canonical Notation

Use the current formula grammar unless a document is explicitly quoting or
preserving historical language:

- `P∞ = φ · ν = 1` for the invariant sphere product
- `B = sin θ` for balance on S²
- `P_node = Φ × V` for node-level empirical or organizational flourishing
- `ΣΔB` for manifold-level balance movement
- `ΣΔP_node` for node-level empirical or organizational movement
- `η` for extraction
- `α5` for the fifth-force parameter

Avoid bare `P`, `ΣΔP`, `Delta P`, `Sigma Delta P`, `eta`, and `alpha_5`
outside quotations, old filenames, or clearly historical notes.

## Genre Buckets

| Bucket | Examples | Scan stance | Repair stance |
|---|---|---|---|
| **Source spine** | root README, `00_START_HERE`, governance, active operator specs, Rosetta READMEs | strict | edit directly; these files teach the rest of the corpus |
| **Books / synthesis** | `05_SYNTHESIS/`, `07_DISSEMINATION/01_BOOK_*`, long manuscripts | interpretive but not exempt | preserve literary voice, add boundary notes, repair overclaims that speak like public proof |
| **Release mirrors** | `07_DISSEMINATION/06_NETWORK/releases/`, `evolutionary.network/releases/` | mirror-aware | edit source owner first when known; otherwise mark inherited wording before mass rewrites |
| **Peer-review packets** | `06_TRANSLATION/PEER_REVIEW/REVIEW_PACKETS/`, `COMPLETED_REVIEWS/` | challenge-aware | sharpen abstracts, assumptions, and reviewer questions; do not treat quoted objections as live canon |
| **Audit closeouts** | `06_TRANSLATION/COUNCIL/05_DOCUMENT_AUDITS/`, dated sprint reports | historical | old paths and old names are evidence of the audit trail; mark historical if needed, do not chase every code-span as a live route |
| **Archives** | `90_ARCHIVE/` | excluded by default | only inspect when provenance is the task |

## Priority Rule

When a scan flags the same issue in many places, repair in this order:

1. The current source owner or governance rule.
2. Current public-facing abstracts, READMEs, and paper packets.
3. Current manuscript source.
4. Release mirrors and generated exports.
5. Historical audit packets.
6. Archive, only when explicitly opened.

This prevents mirror churn from disguising source-truth repair.

## Claim-Language Rule

Strong language is allowed only when the hat and tier allow it.

- Scientist hat: local theorem, established math, explicit test, kill criteria.
- Philosopher hat: symbolic convergence, interpretation, translation, wager.
- Builder hat: conditional operational consequence under receipts.

Forbidden upgrades:

- symbolic convergence becoming proof
- physics analogy becoming physics claim
- neuroscience proxy becoming evidence of core state
- AI assistance becoming K2 authority
- publication copy becoming empirical receipt
- old audit path becoming active route

## Scan Modes

Use two passes instead of one flat pass:

```bash
# Strict active surfaces: should be clean or intentionally annotated.
rg -n -g '*.md' -g '!90_ARCHIVE/**' \
  -g '!05_SYNTHESIS/**' \
  -g '!07_DISSEMINATION/06_NETWORK/**' \
  -g '!06_TRANSLATION/COUNCIL/05_DOCUMENT_AUDITS/**' \
  'geometry is the territory|cannot fail|smoking gun|only explanation|Hard Problem Solved|brain IS|measurement problem dissolves|bare P|Delta P|eta|alpha_5' .

# Mirror/book/audit surfaces: triage by owner and genre before editing.
rg -n -g '*.md' -g '!90_ARCHIVE/**' \
  'geometry is the territory|cannot fail|smoking gun|only explanation|Hard Problem Solved|brain IS|measurement problem dissolves|Delta P|Sigma Delta P|alpha_5' .
```

The second command is a discovery map, not a direct mandate to mass-edit every
match.

## Anti-Capture Floor

Every genre remains bound by the same floor:

- K2 belongs to the human signer, not AI.
- AI may draft, witness, check, and warn; it may not sign.
- `η = 0` means no extraction from cooperators.
- Grace Exit remains live: leave with everything that is yours.
- Claims must survive receipt, kill-condition, or tier downgrade.

## Execution Surface

- **Canonical Path:** 01_EMERGENTISM/08_FRAMEWORK_SUPPORT/01_GOVERNANCE/00_DRIFT_SCAN_DISCIPLINE.md
