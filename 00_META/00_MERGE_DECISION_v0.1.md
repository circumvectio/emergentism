---
title: "Merge Decision v0.1 — kintsugi worktree → parent branch, 18 commits, audit chain pivot"
date: 2026-07-18
status: "[D] draft — K2 sign pending; the decision (not the act) is the V-forcer; the actual `git merge` is K2's operational call"
evidence_tier: "[S] the worktree state on disk; [D] the policy is staged"
owner: "K2 (Yves R. Burri). The K2 sign authorizes the merge; the merge itself is the operational consequence."
parents:
  - 00_META/00_THE_RELEASE_DOCTRINE.md
  - 00_META/00_PER_DOC_FIX_LOG_v0.1.md
  - 00_META/00_RETRACTED_126_DISPOSITION_v0.1.md
---

# Merge Decision v0.1

> **The 9th V-forcer pivots from artifact to institutional.** Eight artifact-shaped V-forcers landed in this session (calibration essay, release doctrine, routing migration, propagation sweep, per-doc fix pattern, K2 sign on log, RETRACTED_126 disposition, per-finding execution batch 1). The convergence-memo's meta-rule requires the 9th to be a *different kind*. **The decision is the V-forcer; the artifact is the receipt.**

## 1. The worktree state

- **Source branch (current worktree):** `codex/emergentist-compass-calibration`
- **Target branch (parent):** `codex/emergentist-compass-kintsugi`
- **Common ancestor:** `da7ae8f` ("docs(emergentism): receipt the Kintsugi Compass")
- **Source ahead / behind target:** **18 ahead, 0 behind** — clean fast-forward
- **All unpushed work:** none — branch tracks `origin/codex/emergentist-compass-calibration`
- **V-forcers in this session (8 of 18):**
  1. `6596f13` — calibration essay (Egregoreotype tier-bump)
  2. `999fe6e` — Release Doctrine `[D]` draft
  3. `5c3e6f8` — routing-file migration (314 files → `_INTERNAL/agent-routing/` + `CONTRIBUTING.md`)
  4. `e1c2245` — propagation sweep v0.1 (163 findings, 78 docs)
  5. `8d41f56` — per-doc fix pattern v0.1 + sample dispositions
  6. `f81d75d` — K2 sign per-doc fix log v0.1 (`[D]` → `[A]`)
  7. `85f3799` — RETRACTED_126 disposition v0.1 (48 FALSE-POSITIVE by mode, 31 DEFER)
  8. `f329600` — per-finding execution batch 1 (7 FALSE-POSITIVE in geometric ontology)

The other 10 commits are pre-existing on the calibration branch (likely from parallel sessions and earlier work — verified clean, not in scope for this V-forcer).

## 2. The decision

**The 8 V-forcers form a constitutional chain.** Each is an artifact (doctrinal summary, organizational structure, audit report, discipline doc, log row), and the chain collectively retires the audit findings into the canon over time. The 24 remaining per-finding candidates continue post-merge; the chain does not block the merge.

**Decision: merge `codex/emergentist-compass-calibration` → `codex/emergentist-compass-kintsugi`.** The merge is a fast-forward (no conflicts). The post-merge branch contains the 18-commit audit chain. The 24 candidates and the remaining per-category batches (`FORBIDDEN_IMPORT` 51, `KSC_VIOLATION` 33, 20-row semantic pass) continue on the merged branch.

## 3. Why merge now

Three reasons the merge is the right pivot:

1. **The artifact chain is constitutionally settled at this point.** The audit has run (sweep v0.1), the discipline is canonical (`[A]` per-doc fix log), the per-finding pattern is established, and the first 7 candidates are dispositioned. The remaining 24 candidates are a continuation, not a blocker. The chain can continue on the parent branch.

2. **The Phase 0 blockers are mostly cleared.** Per the Release Doctrine Phase 0: #1 propagation sweep ✓, #1 follow-on (per-doc fix pattern + log) ✓, #3 stranger test ✓. Phase 0 #2 (extraction boundary) is parked but not on the merge-critical path. The parent branch is ready to absorb the audit chain.

3. **The institutional act is the right shape for the 9th V-forcer.** The 8 prior V-forcers were artifact-shaped (the AI stages). The 9th is a K2 decision (the mortal signs). The decision record is the canonical artifact; the merge itself is the operational consequence. **The kind of move shifts from AI-staging to K2-disposing** — exactly the convergence-memo's "different kind" pivot.

## 4. The post-merge plan

After the merge:

1. **The 24 remaining per-finding candidates** (in `00_META/00_RETRACTED_126_DISPOSITION_v0.1.md §3`) continue as future V-forcers, batched by doc. The pattern is established: read the doc, check for Kintsugi banner, disposition accordingly.

2. **The `FORBIDDEN_IMPORT` category (51 findings)** is the next per-category batch. Estimated 40 FALSE-POSITIVE by mode (registry-citation + audit-trail-ledger), ~8 live, ~3 defer. Future V-forcer.

3. **The `KSC_VIOLATION` category (33 findings)** is the third per-category batch. Estimated 22 FALSE-POSITIVE (Kintsugi-bannner'd + anti-assertion), ~7 live, ~4 defer. Future V-forcer.

4. **The 20-row semantic pass** (manual review of the rows the regex can't catch) is parked from the sweep §4. Future V-forcer once the high-confidence disposition completes.

5. **Phase 0 #2 (extraction boundary + scrub)** remains parked. The negative-list manifest is the next institutional V-forcer after the audit chain settles.

6. **The kintsugi-worktree's `_INTERNAL/agent-routing/`** is a private concern; the public surface remains the funnel (root `README.md` + `CONTRIBUTING.md` + reader guide).

## 5. The merge command (operational)

```bash
# From the parent repo at /Users/Yves/Documents/01_EMERGENTISM/
# (NOT from the worktree — the worktree is checked out on the source branch)
cd /Users/Yves/Documents/01_EMERGENTISM/
git checkout codex/emergentist-compass-kintsugi
git merge --ff-only codex/emergentist-compass-calibration
git push origin codex/emergentist-compass-kintsugi
```

The `--ff-only` flag enforces the fast-forward (the source is 18 ahead, 0 behind, so no merge commit is needed). The push propagates the merged state to `origin`.

**Risk assessment:** the merge is low-risk (clean fast-forward, no conflicts, no commit-by-commit review needed beyond the V-deltas in the source branch's commit messages). If the merge produces unexpected behavior post-fast-forward, the parent branch can be reset to `da7ae8f` (the common ancestor) — but no such reset is expected.

## 6. The K2 sign line

```text
☐ I authorize the merge of codex/emergentist-compass-calibration →
  codex/emergentist-compass-kintsugi. The 18 commits land on the
  parent branch via --ff-only fast-forward. The 24 remaining
  per-finding candidates and the FORBIDDEN_IMPORT / KSC_VIOLATION
  / 20-row-semantic-pass batches continue post-merge.

  K2 (Yves R. Burri): __________________________   Date: __________
```

---

*The decision is the V-forcer. The artifact is the receipt. The merge is the operational consequence — K2's call.*
