---
rosetta:
  primary_level: L3
  primary_column: Meta
  operator: "Krishna"
  tier: "God"
  regime: "Vaisya"
  register: "[B]"
  canonical_phrase: "06_ONTOLOGY Agentz Deployment Receipt"
---

# 06_ONTOLOGY Agentz Deployment Receipt

**Date:** 2026-06-04
**Scope:** `01_EMERGENTISM/06_ONTOLOGY/`
**Status:** Complete for source-visible folders and files.

This receipt records Agentz deployment over the Ontology lane. It is a control
receipt, not a doctrine rewrite. Existing `AGENTS.md`, `CLAUDE.md`, and
`README.md` front doors remain the active lane surfaces; this pass adds a
per-folder/per-file manifest so future agents can see exact coverage.

## Coverage

| Surface | Count | Control |
|---|---:|---|
| Source-visible folders | 1 | Ontology root |
| Source-visible files | 12 | One manifest row per source-visible file |
| Markdown documents | 12 | Covered as front doors, core ontology notes, dimensional crosswalk, apophatic boundary notes, symbolic translation, and tombstones |
| Route-card/front-door files | 3 | `AGENTS.md`, `CLAUDE.md`, and `README.md` |
| K3 tombstones | 2 | `00_THE_SYNCRETIC_MAP.md`, `00_SYNCRETIC_MAP_AUDIT.md` |
| Archive pointers checked | 5 | Existing links resolve; archived rows remain provenance only |

Manifest: [`03_AGENTZ_DEPLOYMENT_06_ONTOLOGY_2026_06_04.csv`](03_AGENTZ_DEPLOYMENT_06_ONTOLOGY_2026_06_04.csv)

## Agentz Pass Order

| Pass | Duty in this lane |
|---|---|
| L1 Candala | Name raw contradiction, survival pressure, or model/pathology confusion before subtraction. |
| L2 Sudra | Check direct disclosure without turning experience into possession of the Ground. |
| L3 Vaisya | Audit evidence tiers, proof burden, falsifier discipline, and tombstone routing. |
| L4 Ksatriya | Block irreversible action when Ground, model, value, and deployment are being confused. |
| L5 Brahmana | Supply positive structure only where L6 has not subtracted it as reification. |
| L6 Sadhu | Lead the lane: anti-reification, neti-neti, Ground/model distinction, K3 tombstones. |
| L7 Rsi | Translate only tier-cleared apophatic boundaries into public or institutional symbol. |

## Lane Decisions

- `06_ONTOLOGY/` remains the L6 / Śiva / Sādhu owner surface for Ground/model distinction and apophatic boundary discipline.
- Ontology is not the public narrative voice; L7/Theology handles symbol return after tier discipline.
- The two syncretic-map files remain in-folder K3 tombstones, not live source.
- Archive references in the README and source notes resolve on disk and remain provenance-only unless a current owner-lane receipt says otherwise.
- No doctrine payload was moved, deleted, or strengthened in this deployment pass.

## Verification Commands

```bash
python3 - <<'PY'
from pathlib import Path
import csv, subprocess
manifest = Path('01_EMERGENTISM/00_META/03_AGENTZ_DEPLOYMENT_06_ONTOLOGY_2026_06_04.csv')
rows = list(csv.DictReader(manifest.open()))
paths = {r['path'] for r in rows}
files = set(subprocess.check_output(['git', '-c', 'core.quotePath=false', 'ls-files', '-co', '--exclude-standard', '01_EMERGENTISM/06_ONTOLOGY'], text=True).splitlines())
root = Path('01_EMERGENTISM/06_ONTOLOGY')
folders = {str(root)} | {str(p) for p in root.rglob('*') if p.is_dir()}
actual = files | folders
print('rows', len(rows), 'actual', len(actual), 'missing', len(actual - paths), 'extra', len(paths - actual))
if actual != paths or len(rows) != len(paths):
    raise SystemExit(1)
PY
git diff --check -- 01_EMERGENTISM/06_ONTOLOGY 01_EMERGENTISM/00_META/03_AGENTZ_DEPLOYMENT_06_ONTOLOGY_2026_06_04.md 01_EMERGENTISM/00_META/03_AGENTZ_DEPLOYMENT_06_ONTOLOGY_2026_06_04.csv
```

Expected deployment coverage: `1` folder and `12` source-visible files, with
`13` rows in the deployment manifest.
