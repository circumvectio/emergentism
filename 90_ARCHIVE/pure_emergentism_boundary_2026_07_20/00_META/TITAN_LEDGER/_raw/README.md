# TITAN_LEDGER/_raw — raw swarm output (K3 archive)

**Status:** [S] K3 archive; raw `<agent_swarm_result>` blocks retained for audit-trail integrity.
**Owner:** 2026-07-17 TITAN transcendental claim-extraction swarm (15 workers).
**Live surface:** [`../TITAN_TRANSCENDENTAL_CLAIM_LEDGER_2026_07_17.md`](../TITAN_TRANSCENDENTAL_CLAIM_LEDGER_2026_07_17.md) (the consolidated ledger; ~526 lines).

## What this folder owns

The 2 raw-swarm appendices from the 15-worker extraction:

- `TITAN_CLAIM_LEDGER_APPENDIX_A_LANES_2026_07_17.md` — 11 lane slices (raw `<agent_swarm_result>` blocks, ~208 KB)
- `TITAN_CLAIM_LEDGER_APPENDIX_B_RULINGS_2026_07_17.md` — 4 ruling slices (~60 KB)

## What this folder must not own

- The consolidated ledger. The live surface is `../TITAN_TRANSCENDENTAL_CLAIM_LEDGER_2026_07_17.md`.
- New raw swarm output. The 15-worker extraction is closed.
- Public-facing surfaces. The ledger is the published form; the appendices are internal audit trail only.

## Why archived (K3)

The consolidated ledger absorbed the appendices' content; the raw `<agent_swarm_result>` blocks are retained for K3 audit-trail integrity (so future K7/§8 work can verify the extraction's provenance). The move to `_raw/` is the K3 archive move — the files are preserved, not erased, and the live surface is the consolidated ledger per the parent README.

## Lifecycle

Cold memory. The appendices are not edited. Future extractions should be appended under a dated lane, not refactored into the consolidated ledger.
