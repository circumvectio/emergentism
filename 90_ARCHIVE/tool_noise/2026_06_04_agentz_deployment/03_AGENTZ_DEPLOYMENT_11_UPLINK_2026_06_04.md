---
rosetta:
  primary_level: L4
  primary_column: Agentz Deployment Control
  register: "[B/I]"
  canonical_phrase: "11_UPLINK Agentz Deployment Receipt"
---

# 11_UPLINK Agentz Deployment Receipt

**Date:** 2026-06-04
**Scope:** `01_EMERGENTISM/11_UPLINK/`
**Status:** Complete for source-visible folders and files in this lane.

This receipt records an Agentz L1-L7 deployment over `11_UPLINK`. It is a
routing and control receipt, not a doctrine rewrite. Existing lane front doors
remain the active route surfaces; this pass adds exact per-folder/per-file
coverage so future agents can see what has already been traversed.

## Coverage

| Surface | Count | Control |
|---|---:|---|
| Source-visible folders | 16 | Physical folders under this lane |
| Source-visible files | 360 | Git source-visible tracked/unignored files |
| Deployment manifest rows | 376 | One row per folder and source-visible file |
| Route-card/front-door files | 47 | `AGENTS.md`, `CLAUDE.md`, `README.md`, or route-card surfaces |
| Archive/provenance rows | 16 | Bounded as non-authority |
| Frozen app-source rows | 0 | Source-preserved only, where applicable |

Manifest: [`03_AGENTZ_DEPLOYMENT_11_UPLINK_2026_06_04.csv`](03_AGENTZ_DEPLOYMENT_11_UPLINK_2026_06_04.csv)

## File-Type Profile

| Suffix | Count |
|---|---:|
| `.json` | 1 |
| `.jsonl` | 4 |
| `.md` | 355 |

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

- Session packets can preserve old [T] product targets; current public or build claims still require [B] receipts or [D]/[C] labels.
- Uplink should route readers down into source-owner folders before revising doctrine.
- No broad file moves, deletions, or doctrine upgrades were performed by this receipt generator.
- Any future rename or restructure should cite this manifest and then update the owning front door.

## Verification Commands

```bash
python3 - <<'PY'
from pathlib import Path
import csv, subprocess
lane = '01_EMERGENTISM/11_UPLINK'
manifest = Path('01_EMERGENTISM/00_META/03_AGENTZ_DEPLOYMENT_11_UPLINK_2026_06_04.csv')
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
git diff --check -- 01_EMERGENTISM/00_META/03_AGENTZ_DEPLOYMENT_11_UPLINK_2026_06_04.csv 01_EMERGENTISM/00_META/03_AGENTZ_DEPLOYMENT_11_UPLINK_2026_06_04.md
```
