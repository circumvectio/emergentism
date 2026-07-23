---
rosetta:
  primary_level: L6
  primary_column: Meta
  operator: "Śiva • (compress / remove false necessity)"
  regime: "Sādhu"
  register: "[D] hygiene receipt — no doctrine touched"
  canonical_phrase: "Worktree tidy — stale checkouts removed, every branch preserved"
title: "Receipt 171 — Worktree Tidy (git worktrees)"
status: "DONE — 10 stale worktrees removed, branches preserved; 8 active/locked left intact"
date: 2026-07-23
evidence_tier: "[D] git receipt; repository-state fact, not a doctrine claim"
---

# Receipt 171 — Worktree Tidy

## Result

The `01_EMERGENTISM` repo had **18 non-main git worktrees** registered (14 Codex under `Documents/.codex-worktrees/`, 1 Codex under `~/.codex/worktrees/`, and 1 Claude worktree nested **inside** the repo at `.claude/worktrees/`). Host-requested tidy (2026-07-23):

- **10 removed** via `git worktree remove` (non-force) + `git worktree prune`.
- **8 refused and left fully intact** — non-force `remove` declined them as **locked/dirty**, i.e. almost certainly **active Codex sessions**. The safety net was intentional; they were not touched.
- **No branch deleted.** Every removed worktree's branch (and all its commits) is preserved and re-checkoutable with `git worktree add`. This tidy removed *checkouts*, not *work*.
- **Disk:** the nested `01_EMERGENTISM/.claude/worktrees/` (61 MB, inside the canonical repo) is cleared to 0 B; `.codex-worktrees/` partially freed (the 8 active worktrees remain).

No tracked file changed by the removals; this receipt is the only committed artifact.

## Removed (10) — branch preserved in each case

| Worktree | Branch (kept) |
|---|---|
| `~/.codex/worktrees/01_EMERGENTISM-delegated-transaction-mandate` | `codex/emergentism-plain-authority-2026-07-22` |
| `.codex-worktrees/emergentism-dimension-canon-purification` | `codex/emergentism-dimension-canon-purification` |
| `.codex-worktrees/emergentism-magnum-opus-stabilize` | `codex/emergentism-magnum-opus-stabilize-2026-07-19` |
| `.codex-worktrees/emergentism-post-claude-reconciliation` | `codex/emergentism-post-claude-reconciliation` |
| `.codex-worktrees/emergentism-release-audit-2026-07-21` | `codex/emergentism-release-audit-2026-07-21` |
| `.codex-worktrees/emergentism-release-integration-2026-07-22` | `codex/emergentism-release-integration-2026-07-22` |
| `.codex-worktrees/emergentism-strike-gfs-tyson-ko` | `codex/archive-all-gfs-2026-07-16` |
| `.codex-worktrees/emergentist-release-doctrine-kintsugi` | `codex/emergentist-release-doctrine-kintsugi` |
| `.codex-worktrees/final-emergentist-weltanschauung` | `codex/final-emergentist-weltanschauung` |
| `01_EMERGENTISM/.claude/worktrees/fervent-sutherland-a32c79` | `claude/fervent-sutherland-a32c79` |

## Left intact (8) — locked/dirty, treated as active Codex sessions

`codex/charter-tidy-2026-07-19` · `codex/emergentism-complete-open-tasks-2026-07-20` · `codex/kintsugi-a0b-machine-kernel` · `codex/open-canon-v01-consolidation-2026-07-19` · `codex/emergentism-release-doctrine` · `codex/site-tidy-compass-residue-2026-07-18` · `codex/v-forcer-10-tidy-closure-2026-07-19` · `codex/emergentist-compass-calibration`

Re-run the tidy for these once their sessions are done. To restore any removed checkout: `git worktree add <path> <branch>`.

•   ⊙   ○
