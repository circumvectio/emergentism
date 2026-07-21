---
rosetta:
  primary_level: L3
  primary_column: Meta
  operator: "Krishna"
  tier: "God"
  regime: "Vaisya"
  register: "[B]"
  canonical_phrase: "10_SEED Agentz Deployment Receipt"
---

# 10_SEED Agentz Deployment Receipt

**Date:** 2026-06-04
**Scope:** `01_EMERGENTISM/10_SEED/`
**Status:** Complete for source-visible folders and files.

This receipt records Agentz deployment over the Seed lane. It is a control
receipt, not a doctrine rewrite. Existing `AGENTS.md`, `CLAUDE.md`, and
`README.md` front doors remain the active lane surfaces; this pass adds a
per-folder/per-file manifest so future agents can see exact coverage.

## Coverage

| Surface | Count | Control |
|---|---:|---|
| Source-visible folders | 1 | Seed root |
| Source-visible files | 4 | One manifest row per source-visible file |
| Markdown documents | 4 | Covered as seed payload and front doors |
| Route-card/front-door files | 3 | `AGENTS.md`, `CLAUDE.md`, and `README.md` |

Manifest: [`03_AGENTZ_DEPLOYMENT_10_SEED_2026_06_04.csv`](03_AGENTZ_DEPLOYMENT_10_SEED_2026_06_04.csv)

## Agentz Pass Order

| Pass | Duty in this lane |
|---|---|
| L1 Candala | Recover the raw seed pressure without adding doctrine. |
| L2 Sudra | Check that compressed intuition is not mistaken for proof. |
| L3 Vaisya | Audit formula, tier, and source-reference integrity. |
| L4 Ksatriya | Block runtime, management, or K2 claims from seed compression alone. |
| L5 Brahmana | Re-expand the seed into source-owner architecture when needed. |
| L6 Sadhu | Cut reification: the seed is not the Ground. |
| L7 Rsi | Lead the lane: witness, compression, preservation, and return-to-L1 teaching. |

## Lane Decisions

- `10_SEED/` remains the L7 compressed seed surface, not the live management/status board.
- Seed compression does not outrank source folders, Uplink, active runtime receipts, or owner-lane front doors.
- Existing source references resolve on disk; no route repair was required in this pass.
- No doctrine payload was moved, deleted, or strengthened in this deployment pass.

## Verification Commands

```bash
python3 - <<'PY'
from pathlib import Path
import csv, subprocess
manifest = Path('01_EMERGENTISM/00_META/03_AGENTZ_DEPLOYMENT_10_SEED_2026_06_04.csv')
rows = list(csv.DictReader(manifest.open()))
paths = {r['path'] for r in rows}
files = set(subprocess.check_output(['git', '-c', 'core.quotePath=false', 'ls-files', '-co', '--exclude-standard', '01_EMERGENTISM/10_SEED'], text=True).splitlines())
root = Path('01_EMERGENTISM/10_SEED')
folders = {str(root)} | {str(p) for p in root.rglob('*') if p.is_dir()}
actual = files | folders
print('rows', len(rows), 'actual', len(actual), 'missing', len(actual - paths), 'extra', len(paths - actual))
if actual != paths or len(rows) != len(paths):
    raise SystemExit(1)
PY
git diff --check -- 01_EMERGENTISM/10_SEED 01_EMERGENTISM/00_META/03_AGENTZ_DEPLOYMENT_10_SEED_2026_06_04.md 01_EMERGENTISM/00_META/03_AGENTZ_DEPLOYMENT_10_SEED_2026_06_04.csv
```

Expected deployment coverage: `1` folder and `4` source-visible files, with
`5` rows in the deployment manifest.
