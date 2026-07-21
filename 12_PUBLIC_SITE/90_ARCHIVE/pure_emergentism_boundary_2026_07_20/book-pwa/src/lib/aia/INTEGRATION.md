---
rosetta:
  primary_level: L4
  primary_column: AIA Dialectical Integration Contract
  secondary:
    - level: L3
      column: Build and Test Receipt Audit
      role: "separate historical npm-test status from current runtime, UI, and backend receipts"
    - level: L5
      column: PWA Source Architecture
      role: "route contradiction, ledger, constitution, versioning, and DAG modules into the Infinite Book scaffold"
    - level: L6
      column: Source-Only Boundary
      role: "prevent integration notes from proving production deployment or live model/database behaviour"
  operator: "Arjuna ⚔"
  tier: "God"
  regime: "Kṣatriya"
  register: "[B/I/C]"
  canonical_phrase: "AIA dialectical layer — integration contract"
title: "AIA Dialectical Layer — Integration Contract"
status: "ACTIVE — source integration note"
evidence_tier: "[I]/[C] for integration claims unless paired with current build/test receipts; [B] only for explicit command receipts."
type: pwa-integration-contract
---

# AIA Dialectical Layer — Integration Contract

This module (`src/lib/aia/`) is the **contradiction-as-branch-state** engine from
the Infinite Book spec. It is intentionally **pure and decoupled** from the
Zustand store (`src/lib/store.ts`) and from Prisma so it can be unit-tested
without a DOM, a model, or a database. It is built to **slot into the existing
store**, not replace it.

Status: 5 modules, **40 passing tests** (`npm test`). No store/UI files were
modified — this is additive.

## What it provides

| File | Purpose | Key exports |
|------|---------|-------------|
| `types.ts` | View-model types | `Claim`, `BranchMode`, `ConsistencyStatus`, `ContradictionType`, `Contradiction`, `ExpansionMode`, `Friction`, `ConflictProbe`, `ClassificationContext` |
| `contradiction.ts` | Classification routing + UX friction | `classifyContradiction`, `frictionFor`, `branchModeForExpansionMode`, `contradictionPolicy` |
| `ledger.ts` | Dialectical resolution reducer | `resolveContradiction` (revise · fork · keep_as_antithesis · synthesize · dismiss) |
| `constitution.ts` | Branch Constitution + context folding | `acceptIntoConstitution`, `recordOpenTension`, `compileContext`, `compileContextString` |
| `versioning.ts` | Canon immutability (Git-for-Text) | `hashContent`, `reviseCanon`, `isBranchStale` |
| `dag.ts` | Mirror-edge cycle guard | `wouldCreateCycle`, `addMirrorEdge` |

## How it answers the original UX question

> *Does an optimistically-rendered node freeze on `canon_conflict`, or render with a badge the user can ignore?*

`frictionFor(type, branchMode)` encodes the rule: **freeze only when a
`canon_conflict` threatens the `mainline`**; every other tension (ancestor,
sibling, intentional) renders as a **badge** the reader can ignore, fork, or
synthesize. So: the mainline stays coherent; antithesis branches are free to
contradict.

## Wire-in to `store.ts` (additive, ~3 touch points)

1. **Extend `PendingAIBranch`** with dialectical fields (defaults keep current behaviour):
   ```ts
   branchMode?: BranchMode;            // default "mainline"
   consistencyStatus?: ConsistencyStatus; // default "unchecked"
   contradicts?: string[];             // contradiction ids
   boundVersionHash?: string;          // canon version this grew from (versioning.ts)
   ```
2. **After `BRANCH_GENERATION_COMPLETE`**, branch state now stores the server-returned
   `consistencyReport` beside contradiction summaries. The report is produced by a
   second structured model pass in `/api/expand`; when it parses, its relation rows
   are used as the `ConflictProbe` for contradiction classification, with the old
   deterministic stance/scope probe as fallback.
3. **Replace the binary `RESOLVE_CONFLICT`** (`keep_private | discard`) with
   `RESOLVE_CONTRADICTION { contradictionId, action }` delegating to `resolveContradiction`.
   The existing conflict badge in `Node.tsx` becomes the dialectical badge (✓ △ ⚠ ◇ ⊘ ∞)
   driven by `Contradiction.type` + `severity`.

## Backend (separate, non-colliding next step)

- A future inline classifier can emit **HTTP 409 `canon_conflict`** so the store's
  existing 409 branch in `GraphProvider.tsx` finally fires (today it's dead — nothing emits 409).
- Persist branch-level `consistencyStatus` / compact report metadata so review queues can filter coherence state without loading full branch cards.
- Persisting `branchMode` / `consistencyStatus` / `contradicts` maps to new columns on
  `AIPBranch`, and `node_versions` (content hash) realises `versioning.ts` server-side.
- `dag.ts` mirrors the PostgreSQL BEFORE-INSERT cycle trigger; the reachability proof is identical.

## Not yet wired (flagged, out of this slice)

- Store's `focusStack` only **pops** (swipe-right). Nothing **pushes** — zoom-in is dead.
- `SWIPE_LEFT_NODE` is a placeholder (thread UI).
- These live in `store.ts`/`Node.tsx` (Codex-owned) — left untouched to avoid collision.
