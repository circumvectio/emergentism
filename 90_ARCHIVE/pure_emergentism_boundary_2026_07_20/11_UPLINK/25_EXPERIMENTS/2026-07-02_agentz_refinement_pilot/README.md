---
title: "Agentz Refinement Pilot"
date: 2026-07-02
status: "PILOT PACKET"
evidence_tier: "[D] workflow design; [B] local run receipts"
owner: "K2-staged; not signed"
---

# Agentz Refinement Pilot

This packet turns the seven Rosetta operators onto a bounded slice of the Emergentism corpus without writing canon.

The workflow may only:

- extract claims,
- try to cut or refute them,
- specify tests,
- flag archive candidates,
- stage a K2 packet.

It may not amend canon, self-ratify, edit the Settled Canon Registry, or silently archive unread material.

## Scope

Pilot inputs are fixed in `scope.json`:

- `04_AXIOLOGY/00_THE_EXTRACTION_LAW.md`
- `05_COSMOLOGY/00_D5_THE_MUTUALISM_LIMIT.md`
- `05_COSMOLOGY/01_THE_TRANSCENDENTAL_TRINITY/40_THE_TITAN_COMPOSITION_LAW.md`
- `11_UPLINK/25_EXPERIMENTS/2026-07-02_extraction_law_empirical_test/VERDICT.md`
- `11_UPLINK/25_EXPERIMENTS/2026-07-02_extraction_law_empirical_test/results.json`

## Operators

| Operator | Pilot role | Output |
|---|---|---|
| Kali L1 | mechanical claim extractor | `outputs/claims.json`, `outputs/claims.md` |
| Kālī L2 | adversarial skeptic | `reports/L2_*` |
| Kṛṣṇa L3 | operationalizer | `reports/L3_*` |
| Arjuna L4 | K2 packet assembler | `outputs/k2_packet.md` |
| Brahmā L5 | grounding check | `reports/L5_*` |
| Śiva L6 | archive-candidate check | `reports/L6_*` |
| Viṣṇu L7 | registry/canon guard | `reports/L7_*` |

## Run

```bash
cd /Users/Yves/Documents/01_EMERGENTISM/11_UPLINK/25_EXPERIMENTS/2026-07-02_agentz_refinement_pilot
python3 run_agentz_refinement_pilot.py
```

The script is deterministic. AI role reports are stored as Markdown under `reports/` and collated into the K2 packet when present.

## Outputs

- `outputs/claims.json`
- `outputs/claims.md`
- `outputs/k2_packet.md`
- `outputs/run_receipt.json`
- `RUN_RECEIPT.md`

All outputs are staged evidence or decision surfaces. None is canon until K2 signs or rejects the staged recommendations.

