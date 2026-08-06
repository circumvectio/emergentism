---
title: "Standing Gate Figure — pass/fail/hang counts (P2.3)"
status: "ACTIVE — recurring snapshot, first run 2026-08-06"
date: 2026-08-06
evidence_tier: "[A] counts reproduced on disk this session by direct execution; [B] inventory derived from filesystem scan of `09_TOOLS/01_SCRIPTS/check_*.py` (the gate-set implicit in `09_TOOLS/01_SCRIPTS/gate.sh`); [I] interpretation of what the figure measures"
owner: "K2 (Yves R. Burri) — disposes per §0.6"
parents:
  - 09_TOOLS/01_SCRIPTS/gate.sh
  - 00_HANDOFF/COMPILER_GATE_TRIAGE_2026_08_05.md
  - 00_HANDOFF/INSTRUMENT_REBUILD_WAVE_RECEIPT_2026_08_06.md
---

# Standing Gate Figure

## Purpose

A **standing figure** of pass / fail / hang / error counts for the
`check_*.py` gates in `09_TOOLS/01_SCRIPTS/`. The number is diagnostic of
**instrument integrity** — what fraction of the corpus's claim-graph
properties are *actually* being mechanically verified at any given moment —
not of doctrinal health. A green pass is evidence that the instrument
fired; a fail or a hang is the *signal that an instrument exists*, not
that the corpus is wrong.

## Inventory (this run, 2026-08-06)

Scanned `09_TOOLS/01_SCRIPTS/`. The gate-set used here is the 26 files
matching `check_*.py`. The canonical `09_TOOLS/01_SCRIPTS/gate.sh` wires
22 of these (the same set minus the four listed below under "un-wired
in gate.sh but in inventory"). Total inventory: **26**. Reproducible with:

```bash
ls /Users/Yves/Documents/01_EMERGENTISM/09_TOOLS/01_SCRIPTS/check_*.py | wc -l
```

## Methodology

- **CWD:** corpus root (`/Users/Yves/Documents/01_EMERGENTISM/`)
- **Runner:** `python3 00_HANDOFF/_run_standing_gate_figure.py` (NDJSON to stdout)
- **Timeout:** 60s wall-clock per gate; timeout classified as `hang`
- **Classification:**
  - `pass` — exit 0
  - `fail` — exit 1
  - `error` — exit 2 (or Python traceback on stderr)
  - `hang` — `subprocess.TimeoutExpired` after 60s
  - `other_<rc>` — any other exit code
- **Concurrency:** serial, one gate at a time (parallelism would corrupt
  wall-clock timing and risk state contention with `build_magnum_opus_register.py`)

---

## Current snapshot — 2026-08-06

| Metric | Count |
|---|---:|
| **pass** | **9** |
| **fail** | **16** |
| **hang** | **1** |
| error | 0 |
| other | 0 |
| **TOTAL** | **26** |

**Wall-clock total (sum of per-gate times):** 116.7s
**Wall-clock total (real-time, serial):** ~120s
**Hangs dominate cost:** 1 hang (60s) is 50% of the real-time budget.

### Per-gate breakdown

| # | Classification | Wall (s) | Gate |
|--:|:--|--:|:--|
| 1 | pass | 0.10 | `09_TOOLS/01_SCRIPTS/check_coherence_profile.py` |
| 2 | pass | 0.10 | `09_TOOLS/01_SCRIPTS/check_no_secrets_staged.py` ⚠ |
| 3 | pass | 0.11 | `09_TOOLS/01_SCRIPTS/check_record_counters.py` |
| 4 | pass | 0.12 | `09_TOOLS/01_SCRIPTS/check_adjudication_custody.py` |
| 5 | pass | 0.17 | `09_TOOLS/01_SCRIPTS/check_trophic_rosetta_doctrine.py` |
| 6 | pass | 1.66 | `09_TOOLS/01_SCRIPTS/check_d6_equiv_d0.py` |
| 7 | pass | 4.89 | `09_TOOLS/01_SCRIPTS/check_established.py` |
| 8 | pass | 5.30 | `09_TOOLS/01_SCRIPTS/check_generative_base.py` |
| 9 | pass | 14.70 | `09_TOOLS/01_SCRIPTS/check_g2_normal_form.py` |
| 10 | fail | 0.06 | `09_TOOLS/01_SCRIPTS/check_q4_declarations.py` |
| 11 | fail | 0.10 | `09_TOOLS/01_SCRIPTS/check_tree_contract.py` |
| 12 | fail | 0.11 | `09_TOOLS/01_SCRIPTS/check_claim_status.py` |
| 13 | fail | 0.20 | `09_TOOLS/01_SCRIPTS/check_work_in_progress.py` |
| 14 | fail | 0.58 | `09_TOOLS/01_SCRIPTS/check_forwarding_stubs.py` |
| 15 | fail | 0.88 | `09_TOOLS/01_SCRIPTS/check_dead_citations.py` |
| 16 | fail | 0.94 | `09_TOOLS/01_SCRIPTS/check_site_build_artifacts.py` |
| 17 | fail | 1.11 | `09_TOOLS/01_SCRIPTS/check_barred_claims.py` |
| 18 | fail | 1.20 | `09_TOOLS/01_SCRIPTS/check_receipt_citations.py` |
| 19 | fail | 1.36 | `09_TOOLS/01_SCRIPTS/check_review_bundle.py` |
| 20 | fail | 1.37 | `09_TOOLS/01_SCRIPTS/check_links.py` |
| 21 | fail | 3.27 | `09_TOOLS/01_SCRIPTS/check_contact_limited.py` |
| 22 | fail | 4.53 | `09_TOOLS/01_SCRIPTS/check_contradiction_census.py` |
| 23 | fail | 7.55 | `09_TOOLS/01_SCRIPTS/check_node_product_ranking.py` |
| 24 | fail | 10.50 | `09_TOOLS/01_SCRIPTS/check_emergentism_purity.py` |
| 25 | fail | 12.09 | `09_TOOLS/01_SCRIPTS/check_active_receipt_citations.py` |
| 26 | **hang** | **60.02** | `09_TOOLS/01_SCRIPTS/check_foundation.py` |

**⚠ = `check_no_secrets_staged.py`** is *deliberately not wired* into
`gate.sh` because it inspects the staged git diff (which a tree gate
cannot see). It passed here because the runner invoked it outside a
staged context. Treat its `pass` as a **vacuous pass** — it does not
guarantee no secrets are staged. (Source: `gate.sh` lines 71-73.)

### Diagnostic snippets (first line of stderr where non-empty)

| Gate | First stderr line |
|---|---|
| `check_claim_status.py` | `Traceback (most recent call last):` |
| `check_contact_limited.py` | `Traceback (most recent call last):` |

These two are failing with **unhandled exceptions** in the checker code
itself, not with corpus violations. The other 14 fails are corpus
violations or contract mismatches (matching the `COMPILER_GATE_TRIAGE_2026_08_05.md`
diagnosis).

---

## Run history

| Timestamp (UTC) | pass | fail | hang | error | other | total | Wall (s) | Source |
|---|--:|--:|--:|--:|--:|--:|--:|---|
| 2026-08-06 (this run) | 9 | 16 | 1 | 0 | 0 | 26 | 116.7 | `_run_standing_gate_figure.py` NDJSON |

**Cadence (recommended, not committed):** daily, before any wave opens
a triage. Re-run with:

```bash
python3 00_HANDOFF/_run_standing_gate_figure.py > /tmp/gates.ndjson 2> /tmp/gates.log
```

---

## What this figure is and is not

- **It IS** a count of which `check_*.py` instruments fired today.
  A `pass` says the instrument ran and saw nothing wrong with the
  property it checks. A `fail` says it ran and found something wrong.
  A `hang` says the instrument is too slow to be useful at 60s
  timeout.
- **It IS NOT** a statement about the corpus's truth. Failures are
  diagnostic of the instrument, not necessarily of the corpus. Several
  fails are *known* (cf. `COMPILER_GATE_TRIAGE_2026_08_05.md`: four
  defects, one of which masks ~30 downstream tests).
- **The 1 hang is the operationally interesting number.** Of the
  26, only one is too slow to verify in 60s, and it is
  `check_foundation.py` — the foundation check, hung at 60s. The
  corpus's foundational property is the one whose verifier cannot
  return in time.
- **The 9 passes are the integrity floor.** 9/26 = 35% of
  instrumented properties are actually being verified today. Down from
  whatever it was before the instrument rebuild wave
  (`INSTRUMENT_REBUILD_WAVE_RECEIPT_2026_08_06.md`); up from whatever
  the floor will be after the next triage.

## Triage hooks

- Known defects blocking the count are catalogued in
  `00_HANDOFF/COMPILER_GATE_TRIAGE_2026_08_05.md`.
- The instrument rebuild that produced this inventory is in
  `00_HANDOFF/INSTRUMENT_REBUILD_WAVE_RECEIPT_2026_08_06.md`.
- A separate effort (P2.1) is independently producing the gate
  inventory; cross-check `P2.1` against the 26 in the Inventory section
  above.

## Provenance (this document)

- **First run:** 2026-08-06, this session.
- **Runner:** `00_HANDOFF/_run_standing_gate_figure.py`
  (kept on disk; re-runnable; NDJSON output).
- **Counts are not committed** (per task constraint). The runner is
  committed by the next wave if K2 disposes; the counts themselves are
  per-run data, not a deliverable artifact.
- **Tier note:** `[A]` for the counts (reproduced on disk by direct
  execution); `[B]` for the inventory (filesystem scan, reproducible);
  `[I]` for the interpretation of what the figure measures.

---

*The corpus has 26 instruments. Today 9 fire green, 16 fire red, and 1
does not return in time. That is the floor. The triage is in the
parent documents; this is the standing number.*

•   ⊙   ○
