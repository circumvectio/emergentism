# TOMBSTONE — Corpus-Audit raw manifests (2026-06-04)

**Archived 2026-07-18** by the Agentz caste-dispatch tidy of `00_META/` (host-authorized; K3 archive-first). Moved with `git mv` from `00_META/` top level to here — **not deleted; history preserved.**

## What is here

| File | Was at | Bytes | What it is |
|---|---|---|---|
| `01_CORPUS_AUDIT_MANIFEST_2026_06_04.csv` | `00_META/` | 1,179,861 | Full generated corpus-audit manifest (raw rows). |
| `01_CORPUS_AUDIT_MANIFEST_2026_06_04.jsonl` | `00_META/` | 37,166 | Line-delimited twin of the same manifest. |
| `02_FULL_READ_SOUL_LOOP_LEDGER_2026_06_04.csv` | `00_META/` | 738,322 | Per-file ledger of the full-read soul-loop sweep (raw rows). |

## Why archived

These are large, **regenerable** raw outputs of the one-time 2026-06-04 corpus-audit / soul-loop pipeline. They cluttered the top of `00_META` (a 100-file folder) without being live routing surfaces.

## What stayed in place (NOT archived)

The **readable summaries** of the same run remain at `00_META/` top level:
`01_CORPUS_AUDIT_SUMMARY_2026_06_04.md`, `02_FULL_READ_SOUL_LOOP_FRONT_DOOR_SUMMARY_2026_06_04.md`, `02_FULL_READ_SOUL_LOOP_FINAL_CLOSE_2026_06_04.md`, `02_FULL_READ_SOUL_LOOP_SUMMARY_2026_06_04.md` — those are the durable record; these raw manifests are the regenerable data behind them.

*K3: provenance, not current authority. Regenerate from the audit pipeline if fresh counts are needed.*
