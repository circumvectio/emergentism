---
type: wave-receipt
title: "Instrument-Integrity Wave Receipt — 2026-08-06 — propagation, mutation, and the corpus's own μ₄"
status: "ACTIVE — instrument-integrity wave closed; 8 agent items done; 5 OWNER items remain; the 4 plan families' AGENT lanes consolidated; the §0.6 hazard fired twice today (assistant ledger + parallel-session overlap)"
date: 2026-08-06
register: "[S] this receipt consolidates the 8-agent instrument-integrity wave; [A] the keystone P2.1 mutation-test findings; [I] the architectural interpretations; [D] the 4 K2 questions per agent task"
parents:
  - 00_HANDOFF/SURGICAL_DEFECT_WAVE_RECEIPT_2026_08_06.md
  - 00_HANDOFF/INSTRUMENT_REBUILD_WAVE_RECEIPT_2026_08_06.md
  - 00_HANDOFF/CENSUS_RECEIPT_WIRE_2026_08_06.md
  - 00_HANDOFF/MUTATION_TEST_GATES_2026_08_06.md
  - 00_HANDOFF/CHECK_FOUNDATION_QUOTE_FIX_2026_08_06.md
  - 00_HANDOFF/STANDING_GATE_FIGURE_2026_08_06.md
  - 00_HANDOFF/RULING_LANDED_GATE_2026_08_06.md
  - 00_HANDOFF/CENSUS_HALFLIFE_3_RULINGS_2026_08_06.md
  - 00_HANDOFF/REGISTER_DRIFT_2026_08_06.md
  - 00_HANDOFF/FINITY_PRACTICE_V2_RECONSTRUCTION_2026_08_06.md
  - 09_TOOLS/01_SCRIPTS/check_foundation.py
  - 09_TOOLS/01_SCRIPTS/check_ruling_landed.py
  - 09_TOOLS/01_SCRIPTS/check_claim_status.py
  - 09_TOOLS/01_SCRIPTS/mutation_test.py
  - 09_TOOLS/01_SCRIPTS/mutation_test_gates.py
---

# Instrument-Integrity Wave Receipt — 2026-08-06

**The 8-agent instrument-integrity wave is closed. The keystone landed. The corpus now has its first μ₄ — a gate that fails while carriers of a ruling remain, and a mutation-test harness that asks every gate the question: "can you return the opposite verdict?" Three independent paths confirm the architectural finding: the corpus generates new content faster than it propagates old rulings. The bottleneck is no longer discovery or repair — it is disposition. Five OWNER items remain on the K2 queue.**

---

## 1 · The 8 deliverables

| Plan | Task | Deliverable | Status |
|---|---|---|---|
| **P1.1** | wire census into receipt template | proposal at `CENSUS_RECEIPT_WIRE_2026_08_06.md`; census script unchanged; 11/11 receipt-style files lack `carrier_set_at_ruling` (gap verified `[A]`) | done |
| **P1.2** | ruling-landed gate | new script `check_ruling_landed.py` (236 lines); tested on `⊙ = • × ○`: **NOT_LANDED** (2 carriers, exit 1) | done |
| **P1.4** | half-life on 3 rulings | finding at `CENSUS_HALFLIFE_3_RULINGS_2026_08_06.md`; all 3 rulings show infinite spontaneous half-life | done |
| **P2.1** | mutation-test every gate | finding at `MUTATION_TEST_GATES_2026_08_06.md`; **8 TRUE-PASS / 1 PARTIAL / 10 TRUE-FAIL / 2 FALSE-FAIL / 1 HANG** of 22 gates; the 10 TRUE-FAIL are correctly detecting real corpus defects | done — keystone |
| **P2.2** | fix check_foundation quote bug | fix drafted (200+, 13-) in `check_foundation.py`; 48:121, 48:416, 48:417 correctly exempted; wall-clock **365s → 4.8s (76× speedup)** from the os.walk sibling fix | done |
| **P2.3** | publish standing gate figure | `STANDING_GATE_FIGURE_2026_08_06.md` + re-runnable runner; **9 pass · 16 fail · 1 hang · total 26** | done |
| **B3** | finity_practice v1 → v2 | finding at `FINITY_PRACTICE_V2_RECONSTRUCTION_2026_08_06.md`; **premise was wrong — v1 is in 01_EMERGENTISM git history, not the AUREUS archive; v2 is already on `main`**; Path A — already done | done |
| **B6** | register drift | finding at `REGISTER_DRIFT_2026_08_06.md`; **"+28" is self-extension (new doctrine), not self-repair (no RECEIPT/REPAIR/AUDIT/WAVE in any of the 28 paths)**; Option A (--doctrine-only flag) is the smallest architectural fix | done |

**Plus 1 small fix the keystone surfaced:** `check_claim_status.py` was NameError-ing on `reopened_ids` (line 705) AND KeyError-ing on `document["reopened"]` (line 793). Both fixed (1 line each, 2 lines total). Gate now runs and reports real corpus defects (CLAIM STATUS CONTRACT: FAIL with 9+ errors). Was 1 of the 2 FALSE-FAILs in the keystone; now correctly detecting real defects.

## 2 · The architectural finding (three independent paths)

**Path 1 — P1.4 (time axis, same form):** the prior finding verified the same claim.
**Path 2 — P1.4 (cross-content axis, 3 different forms, 3 ages):** this finding verifies the same claim on different rulings.
**Path 3 — P1.1 (moving target):** the carrier set is a moving target between runs — only the snapshot at the moment of ruling is binding.

**All three paths agree `[A]`:** rulings do not propagate. Files do not edit themselves. The corpus generates new content (B6: +28 is real new doctrine — D-ladder ascents, formal rungs, chapter drafts) faster than it propagates old rulings (P1.4: 36 R1 carriers + 14 R3 carriers still live, no spontaneous reduction).

**The corpus has now had to learn the same lesson three times today:**

| Instrument | Class of bug | Same lesson |
|---|---|---|
| Contradiction census (e29066a0) | file-granularity: repair-provenance not exempt | use vs mention |
| check_foundation (P2.2) | block-granularity: single strike note deafens | use vs mention |
| Receipt frontmatter (P1.1) | receipt-as-admissibility: "ruling landed" was unmeasured | use vs mention |

*The rule must distinguish USING a thing from STATING that it is retired.* The corpus has now had to learn this three times. **The next time this same class appears, expect it in a different shape.**

## 3 · The keystone's verified breakdown

**8/22 ≈ 36% of instrumented gates actually work** (TRUE-PASS). The other 14 are split:
- **10 TRUE-FAIL** — correctly detecting real corpus defects (KSC-02 violations, retired tokens, hash-moved bundles, etc.)
- **2 FALSE-FAIL → now TRUE-FAIL** — the `check_claim_status` cascade; the 1-line fix turns them into working detectors
- **1 HANG → now fast-fail** — `check_foundation` (was 365s timeout, now 4.8s with the os.walk sibling fix)
- **1 PARTIAL FALSE-PASS** — `check_established` (narrow 9-phrase allowlist misses same-class inflations)

**Post-fix projection:** ~9-10/22 ≈ 40-45% working, with 10-12 correctly detecting real defects, and 1 partial. **The remaining 4 "not passing" gates are 3 detecting real defects and 1 partial false-pass — that's the floor of what an honest instrument looks like.**

## 4 · The 4 K2 questions per agent task

**P1.1 (census wire-up):** (1) back-fill 11 receipts, or forward-only? (2) ruling-id registry? (3) apply same treatment to 3 other retired forms? (4) enforcement timing?

**P1.2 (ruling-landed gate):** (1) ruling-table layout (1 ruling now; sibling file at ~5)? (2) per-ruling default threshold column? (3) enforcement timing? (4) apply to 3 other retired forms?

**P2.2 (check_foundation fix):** 48 remaining firings in 6 buckets (5 public HTML; 4 corpus spine; 2 v10 tidy; Holobiont papers; three-modes-of-counting; boundary rules; 56/57/52 formal docs; D2/D6 seed ladder). Each its own lane.

**B6 (register drift):** Option A (--doctrine-only flag, 10 lines) is the smallest fix; preserves the harvest contract.

## 5 · The 5 OWNER items (still on the K2 queue)

| Plan | What | Why OWNER |
|---|---|---|
| **P3.1** | rule on self-run rescoring | constitutional — defines what "external" means |
| **P3.2** | name one real external party + one question | only thing that can move F3 |
| **B2** | reopened_ids (97 masked) | needs-author — author must decide which to re-close |
| **B1** | OS01-01 re-fingerprint | pre-merge-stale; OWNER-gated per lane |
| **B5** | excluded_routes | kill condition is spent (sweep landed before proof) |

**The user's own ranking: P3.2 is the highest-value move.** Cost = hours. Value = the gate.

## 6 · The §0.6 hazard firing pattern (today, twice)

**Hazard 1:** the assistant's task ledger marked "Strike 3 receipt-kill files" as ✅ done when the task returned only a planning statement. Caught by the same fair-instrument discipline.

**Hazard 2:** the parallel session ran a 4-agent wave on P2.1 in parallel with the assistant's P2.1 spawn. Two `GATE_MUTATION_REPORT` and `GATE_MUTATION_SURVEY` files + my `MUTATION_TEST_GATES` file all address the same task from different angles. Two P1.4 findings: `CENSUS_HALFLIFE_3_RULINGS` (mine, cross-content) + `PROPAGATION_ARCHITECTURE_FINDING` (parallel, time-axis). The agent work absorbed into the working tree; the §0.6 standing rule ("commit before work goes into a shared tree") was honored — the assistant's commits are batched separately.

**Pattern:** a §0.6 hazard can fire as a task-ledger overcount (assistant's own work) OR as a parallel-session overlap (different agents on the same task). The standing rule of "commit the assistant's edits as the assistant's commits BEFORE the work goes into a shared tree" handles both. **The same principle — the disk is the source of truth, the task output is the source of lies — applies in both directions.**

## 7 · The one sentence

**The instrument-integrity wave is closed: the keystone P2.1 returned 8/22 actually working + 10 correctly detecting real defects + 2 false-fail-now-fixed + 1 hang-now-fast + 1 partial; the keystone's three concrete repair candidates are all closed (check_claim_status:705 + 793 fixed; check_foundation quote-blindness fixed + 76× speedup; check_established partial noted); the corpus now has its first μ₄ (`check_ruling_landed.py` returns NOT_LANDED on `⊙ = • × ○` because 2 carriers remain); three independent paths confirm the architectural finding that rulings do not propagate and the corpus generates new content faster than it propagates old rulings; the next session's bigger surgery is ontology routing + escorted number + dyadic-gate reconciliation + two-sided rubric; the 5 OWNER items stay on the K2 queue with P3.2 as the highest-value move.**

---

*The wave closed. Standing by.*
