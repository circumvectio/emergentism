# CLUSTER2_LEDGER — Cluster II claim ledger, 2026-07-17

**Status:** [S] claim-extraction swarm-output (consolidated); [B] verifier-backed; non-canonical until K2 counter-sign.
**Owner:** 2026-07-17 Cluster II (CCC / dyadism / ethics / powermax) claim-extraction swarm (5 workers → consolidated ledger).
**Source of truth:** the 6 files in this folder; the parent `00_META/` retains a flat index for routing only.

## What this folder owns

The Cluster II claim ledger: 1 consolidated ledger (`CLUSTER2_CCC_DYADISM_ETHICS_POWERMAX_CLAIM_LEDGER_2026_07_17.md`) + 5 raw extraction files (AXIOLOGY / CCC / ETA_ZERO / POWERMAX / SYNTROPY claim extractions, one per worker). The consolidated ledger is the live surface; the extraction files are raw worker output retained for K3 audit-trail integrity.

## What this folder must not own

- Source canon under `04_AXIOLOGY/`. The Cluster II ledger verifies or claims against source; it does not own source.
- Receipts under `11_UPLINK/50_AUDITS_AND_EXECUTIONS/`. The audit trail lives in the Uplink.
- New raw extraction. The 5-worker extraction is closed; the ledger is the durable record.

## Where to read first

1. `CLUSTER2_CCC_DYADISM_ETHICS_POWERMAX_CLAIM_LEDGER_2026_07_17.md` — the consolidated ledger (the live surface).
2. `CCC_CLAIM_EXTRACTION_2026_07_17.md` — the CCC lane.
3. `AXIOLOGY_CLAIM_EXTRACTION_2026_07_17.md` — the axiology lane.
4. `ETA_ZERO_CLAIM_EXTRACTION_2026_07_17.md` / `POWERMAX_CLAIM_EXTRACTION_2026_07_17.md` / `SYNTROPY_CLAIM_EXTRACTION_2026_07_17.md` — the secondary lanes.

## Lifecycle

Consolidated swarm-output. The extraction files are intentionally retained for K3 audit; future extractions should be appended under a dated lane, not refactored into the consolidated ledger.
