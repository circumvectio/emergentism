---
rosetta:
  primary_level: L3
  primary_column: Meta
  operator: "Krishna"
  tier: "God"
  regime: "Vaisya"
  register: "[B]"
  canonical_phrase: "04_AXIOLOGY Agentz Deployment Receipt"
---

# 04_AXIOLOGY Agentz Deployment Receipt

**Date:** 2026-06-04
**Scope:** `01_EMERGENTISM/04_AXIOLOGY/`
**Status:** Complete for source-visible folders and Markdown documents.

This receipt records Agentz deployment over the Axiology lane. It is a control
receipt, not a doctrine rewrite. Existing `AGENTS.md`, `CLAUDE.md`, and
`README.md` front doors remain the active lane surfaces; this pass adds a
per-folder/per-document manifest so future agents can see exact coverage.

## Coverage

| Surface | Count | Control |
|---|---:|---|
| Source-visible folders | 4 | Root, Theurgy, Value Theory, archive |
| Source-visible Markdown documents | 22 | One manifest row per document |
| Route-card/front-door files | 12 | `AGENTS.md`, `CLAUDE.md`, and `README.md` surfaces across the lane |
| Theurgy / K2 rows | 6 | K2 participation and signed-action discipline |
| Value Theory rows | 7 | Rights, duties, due process, moral/ethical dyad |
| Archive rows | 4 | Preserved as non-authoritative historical material |

Manifest: [`03_AGENTZ_DEPLOYMENT_04_AXIOLOGY_2026_06_04.csv`](03_AGENTZ_DEPLOYMENT_04_AXIOLOGY_2026_06_04.csv)

## Agentz Pass Order

| Pass | Duty in this lane |
|---|---|
| L1 Caṇḍāla | Name the objective pressure, harm pressure, or branch under consideration. |
| L2 Śūdra | Surface candidate values without treating them as commitments. |
| L3 Vaiśya | Supply risk, receipt, rollback, and falsifier status before action. |
| L4 Kṣatriya | Lead the lane: value, justice, K2, refusal, and the smallest defensible commit. |
| L5 Brāhmaṇa | Align value claims with operator grammar and constitutional architecture. |
| L6 Sādhu | Cut extraction, moral performance, delegated responsibility, and archive overreach. |
| L7 Ṛṣi | Translate only tier-cleared value and K2 boundaries into compressed narrative. |

## Lane Decisions

- `04_AXIOLOGY/` remains the L4 / Arjuna owner surface for value, justice, K2, and signed action.
- `01_THEURGY/` remains the K2 participation and signed-action discipline sublane.
- `02_VALUE_THEORY/` remains the value-theory, rights, duties, and due-process sublane.
- `90_ARCHIVE/` remains provenance only, not current authority.
- No doctrine payload was moved, deleted, or strengthened in this deployment pass.
- AI may route, draft, warn, lint, and witness; it may not replace the natural-person K2 signature.

## Verification Commands

```bash
python3 - <<'PY'
from pathlib import Path
import csv, subprocess
manifest = Path('01_EMERGENTISM/00_META/03_AGENTZ_DEPLOYMENT_04_AXIOLOGY_2026_06_04.csv')
rows = list(csv.DictReader(manifest.open()))
paths = {r['path'] for r in rows}
files = set(subprocess.check_output(['git', '-c', 'core.quotePath=false', 'ls-files', '-co', '--exclude-standard', '01_EMERGENTISM/04_AXIOLOGY'], text=True).splitlines())
root = Path('01_EMERGENTISM/04_AXIOLOGY')
folders = {str(root)} | {str(p) for p in root.rglob('*') if p.is_dir()}
actual = files | folders
print('rows', len(rows), 'actual', len(actual), 'missing', len(actual - paths), 'extra', len(paths - actual))
if actual != paths or len(rows) != len(paths):
    raise SystemExit(1)
PY
git diff --check -- 01_EMERGENTISM/04_AXIOLOGY 01_EMERGENTISM/00_META/03_AGENTZ_DEPLOYMENT_04_AXIOLOGY_2026_06_04.md 01_EMERGENTISM/00_META/03_AGENTZ_DEPLOYMENT_04_AXIOLOGY_2026_06_04.csv
```

Expected deployment coverage: `4` folders and `22` source-visible Markdown
documents, with `26` rows in the deployment manifest.
