---
rosetta:
  primary_level: L3
  primary_column: Meta
  operator: "Krishna"
  tier: "God"
  regime: "Vaisya"
  register: "[B]"
  canonical_phrase: "02_EPISTEMOLOGY Agentz Deployment Receipt"
---

# 02_EPISTEMOLOGY Agentz Deployment Receipt

**Date:** 2026-06-04
**Scope:** `01_EMERGENTISM/02_EPISTEMOLOGY/`
**Status:** Complete for source-visible folders and Markdown documents.

This receipt records Agentz deployment over the Epistemology lane. It is a
control receipt, not a doctrine rewrite. Existing `AGENTS.md` and `CLAUDE.md`
front doors were already present; this pass adds per-folder and per-document
control rows so future agents can see exactly what is covered.

## Coverage

| Surface | Count | Control |
|---|---:|---|
| Source-visible folders | 3 | Local route cards at root and both subfolders |
| Source-visible Markdown documents | 24 | One manifest row per document |
| Active route-card surfaces | 6 | `AGENTS.md` and `CLAUDE.md` at root, evidence tiers, and memetics |
| Front doors | 3 | `README.md` at root and both subfolders |
| Ignored OS metadata | 1 | `.DS_Store` is ignored by `.gitignore` and not treated as doctrine or a document |

Manifest: [`03_AGENTZ_DEPLOYMENT_02_EPISTEMOLOGY_2026_06_04.csv`](03_AGENTZ_DEPLOYMENT_02_EPISTEMOLOGY_2026_06_04.csv)

## Agentz Pass Order

| Pass | Duty in this lane |
|---|---|
| L1 Caṇḍāla | Surface raw disclosure pressure, contradiction, and memetic-capture risk. |
| L2 Śūdra | Lead the lane: candidate surfacing, direct perception, evidence reception, and disclosure-vs-proof boundaries. |
| L3 Vaiśya | Audit tier status, receipts, and the L2 to L3 candidate-claim gate. |
| L5 Brāhmaṇa | Check Rosetta topology, evidence-ladder architecture, and owner-route coherence. |
| L6 Sādhu | Cut projection, reification, pattern intoxication, and unsupported egregore claims. |
| L7 Ṛṣi | Translate only tier-cleared epistemology into compressed public/institutional narrative. |

## Lane Decisions

- `02_EPISTEMOLOGY/` remains the L2 / Kālī owner surface for how pattern is known.
- `01_EVIDENCE_TIERS/` remains the evidence-ladder and claim-admission sublane.
- `03_MEMETICS/` remains L2-owned, with L6/L7 secondary boundaries for anti-reification and public-symbol translation.
- No doctrine payload was moved, deleted, or strengthened in this deployment pass.
- Public/action claims still require explicit evidence tier and owner-lane routing before use.

## Verification Commands

```bash
git ls-files -co --exclude-standard 01_EMERGENTISM/02_EPISTEMOLOGY | wc -l
find 01_EMERGENTISM/02_EPISTEMOLOGY -type d | wc -l
python3 01_EMERGENTISM/09_TOOLS/01_SCRIPTS/emergentism_audit_manifest.py
git diff --check -- 01_EMERGENTISM/02_EPISTEMOLOGY 01_EMERGENTISM/00_META/03_AGENTZ_DEPLOYMENT_02_EPISTEMOLOGY_2026_06_04.md 01_EMERGENTISM/00_META/03_AGENTZ_DEPLOYMENT_02_EPISTEMOLOGY_2026_06_04.csv
```

Expected deployment coverage: `3` folders and `24` source-visible Markdown
documents, with `27` rows in the deployment manifest.
