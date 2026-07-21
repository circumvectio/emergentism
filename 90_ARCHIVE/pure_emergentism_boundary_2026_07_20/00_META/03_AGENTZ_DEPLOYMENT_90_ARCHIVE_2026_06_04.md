---
rosetta:
  primary_level: L6
  primary_column: Agentz Deployment Control
  register: "[B/I]"
  canonical_phrase: "90_ARCHIVE Agentz Deployment Receipt"
---

# 90_ARCHIVE Agentz Deployment Receipt

**Date:** 2026-06-04
**Scope:** `01_EMERGENTISM/90_ARCHIVE/`
**Status:** Complete for source-visible folders and files in this lane.

This receipt records an Agentz L1-L7 deployment over `90_ARCHIVE`. It is a
routing and control receipt, not a doctrine rewrite. Existing lane front doors
remain the active route surfaces; this pass adds exact per-folder/per-file
coverage so future agents can see what has already been traversed.

## Coverage

| Surface | Count | Control |
|---|---:|---|
| Source-visible folders | 55 | Physical folders under this lane |
| Source-visible files | 243 | Git source-visible tracked/unignored files |
| Deployment manifest rows | 298 | One row per folder and source-visible file |
| Route-card/front-door files | 63 | `AGENTS.md`, `CLAUDE.md`, `README.md`, or route-card surfaces |
| Archive/provenance rows | 298 | Bounded as non-authority |
| Frozen app-source rows | 0 | Source-preserved only, where applicable |

Manifest: [`03_AGENTZ_DEPLOYMENT_90_ARCHIVE_2026_06_04.csv`](03_AGENTZ_DEPLOYMENT_90_ARCHIVE_2026_06_04.csv)

## File-Type Profile

| Suffix | Count |
|---|---:|
| `.R` | 2 |
| `.css` | 5 |
| `.html` | 8 |
| `.js` | 6 |
| `.md` | 217 |
| `.pdf` | 1 |
| `.py` | 1 |
| `.txt` | 1 |
| `.xlsx` | 1 |
| `.xml` | 1 |

## Agentz Pass Order

| Pass | Duty in this lane |
|---|---|
| L1 Candala | Detect contradictions, path drift, broken maps, and objective pressure. |
| L2 Sudra | Check disclosure, public-safety, and candidate interpretations before strengthening claims. |
| L3 Vaisya | Audit receipts, evidence tiers, route cards, links, and generated ledgers. |
| L4 Ksatriya | Execute only bounded repairs and block irreversible moves without K2/owner route. |
| L5 Brahmana | Preserve topology, owner boundaries, and source architecture. |
| L6 Sadhu | Bound archives, compatibility shims, generated output, and overgrown summaries. |
| L7 Rsi | Compress only source-confirmed truth into narrative or witness form. |

## Lane Decisions

- Former 999_ARCHIVE references are bounded by the 90_ARCHIVE front door and should not recreate the old folder.
- Archive files are preserved for provenance; repair only indexing, tombstones, or misleading route cards.
- No broad file moves, deletions, or doctrine upgrades were performed by this receipt generator.
- Any future rename or restructure should cite this manifest and then update the owning front door.

## Verification Commands

```bash
python3 - <<'PY'
from pathlib import Path
import csv, subprocess
lane = '01_EMERGENTISM/90_ARCHIVE'
manifest = Path('01_EMERGENTISM/00_META/03_AGENTZ_DEPLOYMENT_90_ARCHIVE_2026_06_04.csv')
rows = list(csv.DictReader(manifest.open()))
paths = {r['path'] for r in rows}
files = set(subprocess.check_output(['git', '-c', 'core.quotePath=false', 'ls-files', '-co', '--exclude-standard', lane], text=True).splitlines())
root = Path(lane)
folders = {str(root)} | {str(p) for p in root.rglob('*') if p.is_dir()}
actual = files | folders
print('rows', len(rows), 'actual', len(actual), 'missing', len(actual - paths), 'extra', len(paths - actual))
if actual != paths or len(rows) != len(paths):
    raise SystemExit(1)
PY
git diff --check -- 01_EMERGENTISM/00_META/03_AGENTZ_DEPLOYMENT_90_ARCHIVE_2026_06_04.csv 01_EMERGENTISM/00_META/03_AGENTZ_DEPLOYMENT_90_ARCHIVE_2026_06_04.md
```
