# CLUSTER2_LEDGER/_raw — raw extraction output (K3 archive)

**Status:** [S] K3 archive; raw worker output retained for audit-trail integrity.
**Owner:** 2026-07-17 Cluster II (CCC / dyadism / ethics / powermax) claim-extraction swarm (5 workers).
**Live surface:** [`../CLUSTER2_CCC_DYADISM_ETHICS_POWERMAX_CLAIM_LEDGER_2026_07_17.md`](../CLUSTER2_CCC_DYADISM_ETHICS_POWERMAX_CLAIM_LEDGER_2026_07_17.md) (the consolidated ledger).

## What this folder owns

The 5 raw extraction files from the 5-worker extraction swarm:

- `AXIOLOGY_CLAIM_EXTRACTION_2026_07_17.md`
- `CCC_CLAIM_EXTRACTION_2026_07_17.md`
- `ETA_ZERO_CLAIM_EXTRACTION_2026_07_17.md`
- `POWERMAX_CLAIM_EXTRACTION_2026_07_17.md`
- `SYNTROPY_CLAIM_EXTRACTION_2026_07_17.md`

## What this folder must not own

- The consolidated ledger. The live surface is `../CLUSTER2_CCC_DYADISM_ETHICS_POWERMAX_CLAIM_LEDGER_2026_07_17.md`.
- New raw extraction output. The 5-worker extraction is closed.
- Public-facing surfaces. The ledger is the published form; the extractions are internal audit trail only.

## Why archived (K3)

The consolidated ledger absorbed the extractions' content; the raw worker files are retained for K3 audit-trail integrity (so future K7/§8 work can verify the extraction's provenance). The move to `_raw/` is the K3 archive move — the files are preserved, not erased, and the live surface is the consolidated ledger per the parent README.

## Lifecycle

Cold memory. The extractions are not edited. Future extractions should be appended under a dated lane, not refactored into the consolidated ledger.
