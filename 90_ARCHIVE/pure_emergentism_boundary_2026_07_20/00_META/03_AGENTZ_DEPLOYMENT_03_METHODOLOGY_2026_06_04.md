---
rosetta:
  primary_level: L3
  primary_column: Meta
  operator: "Krishna"
  tier: "God"
  regime: "Vaisya"
  register: "[B]"
  canonical_phrase: "03_METHODOLOGY Agentz Deployment Receipt"
---

# 03_METHODOLOGY Agentz Deployment Receipt

**Date:** 2026-06-04
**Scope:** `01_EMERGENTISM/03_METHODOLOGY/`
**Status:** Complete for source-visible folders and files.

This receipt records Agentz deployment over the Methodology lane. It is a
control receipt, not a doctrine rewrite. Existing `AGENTS.md`, `CLAUDE.md`,
and `README.md` front doors remain the active lane surfaces; this pass adds a
per-folder/per-file manifest so future agents can see exact coverage.

## Coverage

| Surface | Count | Control |
|---|---:|---|
| Source-visible folders | 7 | Root, derivation, papers, finity papers, paper sources, preregistrations, archive |
| Source-visible files | 72 | One manifest row per source-visible file |
| Markdown documents | 71 | Covered as route cards, front doors, papers, preregistrations, archive, or active method surfaces |
| Tooling scripts | 1 | Covered as tooling review-before-edit |
| Route-card/front-door files | 21 | `AGENTS.md`, `CLAUDE.md`, and `README.md` surfaces across the lane |
| Archive rows | 9 | Preserved as non-authoritative historical material |

Manifest: [`03_AGENTZ_DEPLOYMENT_03_METHODOLOGY_2026_06_04.csv`](03_AGENTZ_DEPLOYMENT_03_METHODOLOGY_2026_06_04.csv)

## Agentz Pass Order

| Pass | Duty in this lane |
|---|---|
| L1 Caṇḍāla | Name the raw claim pressure, contradiction, or objective function that method must test. |
| L2 Śūdra | Keep disclosed patterns from becoming proof before method earns them. |
| L3 Vaiśya | Lead the lane: inference, ranking, falsification, proof burden, receipts, and tier movement. |
| L5 Brāhmaṇa | Align derivations, paper architecture, and formal-system routes. |
| L6 Sādhu | Bound method overreach, archive non-authority, and stale or bureaucratic claims. |
| L7 Ṛṣi | Translate only tier-cleared method into compressed public or institutional narrative. |

## Lane Decisions

- `03_METHODOLOGY/` remains the L3 / Kṛṣṇa owner surface for tests, claim discipline, derivation, papers, and preregistration evidence.
- `01_THE_DERIVATION/` remains the derivation spine.
- `02_THE_PAPERS/` remains a tiered paper surface; proof, model, translation, and conjecture must stay separated.
- `03_PREREGISTRATIONS/` remains frozen evidence-design/result material; negative or mixed results stay visible.
- `90_ARCHIVE/` remains provenance only, not current authority.
- No doctrine payload was moved, deleted, or strengthened in this deployment pass.

## Verification Commands

```bash
python3 - <<'PY'
from pathlib import Path
import csv, subprocess
manifest = Path('01_EMERGENTISM/00_META/03_AGENTZ_DEPLOYMENT_03_METHODOLOGY_2026_06_04.csv')
rows = list(csv.DictReader(manifest.open()))
paths = {r['path'] for r in rows}
files = set(subprocess.check_output(['git', 'ls-files', '-co', '--exclude-standard', '01_EMERGENTISM/03_METHODOLOGY'], text=True).splitlines())
root = Path('01_EMERGENTISM/03_METHODOLOGY')
folders = {str(root)} | {str(p) for p in root.rglob('*') if p.is_dir()}
actual = files | folders
print('rows', len(rows), 'actual', len(actual), 'missing', len(actual - paths), 'extra', len(paths - actual))
if actual != paths or len(rows) != len(paths):
    raise SystemExit(1)
PY
git diff --check -- 01_EMERGENTISM/03_METHODOLOGY 01_EMERGENTISM/00_META/03_AGENTZ_DEPLOYMENT_03_METHODOLOGY_2026_06_04.md 01_EMERGENTISM/00_META/03_AGENTZ_DEPLOYMENT_03_METHODOLOGY_2026_06_04.csv
```

Expected deployment coverage: `7` folders and `72` source-visible files, with
`79` rows in the deployment manifest.
