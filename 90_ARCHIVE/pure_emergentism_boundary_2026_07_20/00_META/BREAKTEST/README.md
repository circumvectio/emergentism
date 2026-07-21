# BREAKTEST — breaktest harness, 2026-07-17

**Status:** [S] active swarm-output; [B] verifier-backed; non-canonical until K2 counter-sign.
**Owner:** 2026-07-17 breaktest workflow (K2 + verifier swarm, R-K4 fences carried).
**Source of truth:** the 7 files in this folder; the parent `00_META/` retains a flat index for routing only.

## What this folder owns

The breaktest corpus from the 2026-07-17 verifier swarm: 5 markdown reports (CORE / COMPUTE / FRAME / OPTIMA / I_REGISTER), 2 verify scripts (FRAME / OPTIMA), and 1 cross-check helper (`breaktest_core_check.py`). Each file carries a tier mark and a kill criterion.

## What this folder must not own

- Source canon under `01_TELEOLOGY/` or `05_COSMOLOGY/`. Breaktest is verification, not doctrine.
- Receipts under `11_UPLINK/50_AUDITS_AND_EXECUTIONS/`. The audit trail lives in the Uplink.
- Generated outputs. The 6×3+1 PASS matrix is the live result; rendered HTML is downstream of the parent.

## Where to read first

1. `BREAKTEST_CORE_2026_07_17.md` — the spine (kill criteria + tier register).
2. `BREAKTEST_I_REGISTER_2026_07_17.md` — the register index.
3. `BREAKTEST_FRAME_2026_07_17.md` — the framework break test.
4. `breaktest_core_check.py` — runtime cross-check.

## Lifecycle

Active swarm-output. Per A7 self-correction: superseded by any later breaktest; K2 counter-sign promotes to [E].
