---
rosetta:
  primary_level: L3
  primary_column: Meta
  operator: "Krishna"
  tier: "God"
  regime: "Vaisya"
  register: "[B]"
  canonical_phrase: "00_META Agentz Deployment Receipt"
  vmosk_a_ref: "01_EMERGENTISM/VMOSK_A.md"
---

# 00_META Agentz Deployment Receipt

**Date:** 2026-06-04
**Scope:** `01_EMERGENTISM/00_META/`
**Status:** Complete for source-visible folders and files.

This receipt records Agentz deployment over the META lane. It is a control
receipt, not a doctrine rewrite. Existing `AGENTS.md`, `CLAUDE.md`, and
`README.md` front doors remain the active lane surfaces; this pass adds a
self-covering per-folder/per-file manifest so future agents can see exact
coverage of the control plane itself.

## Coverage

| Surface | Count | Control |
|---|---:|---|
| Source-visible folders | 2 | META root and local archive |
| Source-visible files | 67 | One manifest row per source-visible file, including this receipt pair and lane receipts |
| Markdown documents | 48 | Covered as front doors, ledgers, audit notes, summaries, receipts, or archive provenance |
| CSV ledgers | 18 | Covered as generated or receipt control ledgers |
| JSONL ledgers | 1 | Covered as generated corpus-control data |
| Route-card/front-door files | 6 | `AGENTS.md`, `CLAUDE.md`, and `README.md` surfaces at root and archive |
| Archive rows | 12 | `00_META/90_ARCHIVE/` is provenance only, not current authority |

Manifest: [`03_AGENTZ_DEPLOYMENT_00_META_2026_06_04.csv`](03_AGENTZ_DEPLOYMENT_00_META_2026_06_04.csv)

## Agentz Pass Order

| Pass | Duty in this lane |
|---|---|
| L1 Candala | Name raw cleanup pressure, broken maps, and unresolved corpus contradictions. |
| L2 Sudra | Check evidence and disclosure discipline before meta summaries strengthen claims. |
| L3 Vaisya | Audit ledgers, manifests, receipt coverage, and route-card consistency. |
| L4 Ksatriya | Route irreversible K2 staging, governance handoffs, and source-owner decisions. |
| L5 Brahmana | Lead the lane: meta-framework topology, translation protocols, and organization standards. |
| L6 Sadhu | Keep cleanup, archive, and compatibility work from becoming new doctrine. |
| L7 Rsi | Preserve compressed witness only after owner-lane truth is settled. |

## Lane Decisions

- `00_META/` remains the control plane for routing, audit ledgers, translation protocol, and corpus repair discipline.
- META records retired aliases, stale-route findings, and legacy tier counts as audit/control data; those strings are not live route authority by themselves.
- Generated ledgers are derivative control artifacts. Regenerate or re-audit them before treating counts as current.
- `00_META/90_ARCHIVE/` remains historical audit provenance; it is not current source authority.
- No doctrine payload was moved, deleted, or strengthened in this deployment pass.

## Verification Commands

```bash
python3 - <<'PY'
from pathlib import Path
import csv, subprocess
manifest = Path('01_EMERGENTISM/00_META/03_AGENTZ_DEPLOYMENT_00_META_2026_06_04.csv')
rows = list(csv.DictReader(manifest.open()))
paths = {r['path'] for r in rows}
files = set(subprocess.check_output(['git', '-c', 'core.quotePath=false', 'ls-files', '-co', '--exclude-standard', '01_EMERGENTISM/00_META'], text=True).splitlines())
root = Path('01_EMERGENTISM/00_META')
folders = {str(root)} | {str(p) for p in root.rglob('*') if p.is_dir()}
actual = files | folders
print('rows', len(rows), 'actual', len(actual), 'missing', len(actual - paths), 'extra', len(paths - actual))
if actual != paths or len(rows) != len(paths):
    raise SystemExit(1)
PY
git diff --check -- 01_EMERGENTISM/00_META
```

Expected deployment coverage: `2` folders and `67` source-visible files, with
`69` rows in the deployment manifest.
