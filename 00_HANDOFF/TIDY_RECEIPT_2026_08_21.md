---
title: "Tidy receipt — worktrees, branches and folders, 2026-08-21"
date: 2026-08-21
status: "[B] receipt — records what was executed and what was deliberately not"
evidence_tier: "[B] every count and disposition below was produced by a command run on 2026-08-21 between 16:53 and 17:30 +07 and is true OF THAT MOMENT"
owner: "Chair for Bucket 2; agent-executed for Bucket 1"
---

# Tidy receipt — 2026-08-21

Scope: the request was to tidy the Emergentism worktree and its folders. What
follows is what was done, what was found, and what was left for the chair — with
the reasoning for the boundary, since most of the untidiness here is **not**
agent-disposable.

## 1 · The state found

| | |
|---|---|
| worktrees | 5 — the primary plus 4 under `Documents/.codex-worktrees/` |
| branches | 10 local, 8 unmerged into `main` |
| dirty worktrees | 2 (`…refinement-20260821` 35 entries, `…spark-reader-20260820` 4) |
| primary tree | clean, on `theory/parasite-load-2026-08-17` |
| parent repo | clean; correctly gitignores `.codex-worktrees/` and `/01_EMERGENTISM/`; tracks nothing under either |

**Four commit tips exist on this disk and nowhere else** — verified against a
*fresh* `git fetch --all` at 17:25, not a cached ref: `981310d4`
(refinement-20260821), `8e408ce7` (great-mystery), `ec7bc5b4` (glyph-migration),
`2e335782` (parasite-load, carrying this session's work). `ae062bf6` *is* on
`origin`. The audit's first pass derived this from a `FETCH_HEAD` stamped
2026-08-20 21:32 — a 20-hour-old cache. It was re-derived before anything acted
on it, and it held.

## 2 · Executed (agent-safe: reversible, no content decision, no outward effect)

- **Rescue snapshot** of all 39 uncommitted paths across both dirty worktrees, plus
  each worktree's **index** (the 20260821 worktree holds 3 staged *renames*, and a
  rename lives in the index, not in the files — copying files alone would have lost
  that they were renames), plus the three `/private/tmp` coverage ledgers that a
  `/tmp` clear would destroy. → `/Users/Yves/emergentism_rescue_2026_08_21/` with a
  manifest. **Copy, not move; both sources re-censused unchanged immediately after.**
- **Deleted `refine-rosetta/2026-08-15`** — verified strict ancestor of `origin/main`
  with `git cherry` returning zero unique commits, deleted with `-d` (which refuses
  if the premise is false, so the command self-checks). Restore:
  `git branch refine-rosetta/2026-08-15 8ffd8881`.
- **Refreshed remote-tracking refs** with `--no-prune` (deliberate: pruning could
  delete a remote-tracking ref that is a branch's only offsite record).

## 3 · NOT done, and why — the boundary matters more than the list

- **No branch was merged into `main`.** Eight branches carry 2–25 unique commits of
  another session's doctrinal work. Merging is a content decision, not tidiness.
- **Neither dirty worktree was touched.** Codex sessions are open but idle. The
  20260821 change set is *one coherent archive-first migration* — 3 staged renames
  into dated `90_ARCHIVE/` dirs, 3 `TOMBSTONE.md` custody records, 2 forwarding
  stubs, a `.docx` sidecar tombstone, 3 regenerated registers, plus ~294 lines of
  F5 doctrinal edits and a `CONTRIBUTING.md` rewrite. **The likeliest accident here
  is not a destructive checkout — it is a `git commit -a`,** which would ship the
  renames without their untracked tombstones and stubs, yielding an archive with no
  custody record and three dead paths. It must be committed atomically with an
  explicit pathspec, and the doctrinal edits must be a *separate* commit: they are
  different claims.
- **No worktree was removed**, including the clean `…refinement-20260820`. It is
  mechanically safe, but its ref shares a tip with `spark-reader-20260820`, whose
  worktree holds the only copy of a 236+/278− public-front-door rewrite. Removing
  the harmless twin makes the pair *look* resolved and invites the next hygiene pass
  to reach for `--force` on the wrong one. Net risk of acting exceeds the tidiness.
- **`git worktree prune` was not run** — verified a no-op (`--dry-run -v` silent, all
  four gitdirs exist). Running it gains nothing and normalises a command that would
  do harm one directory over.
- **No filename was normalised.** `00_*` is a semantic flag, not an ordinal; date-format
  and suffix-case variance encode provenance. A prior corpus-wide audit called 43% of
  filenames non-conforming — *that audit was the error.*

## 4 · Two premises that failed on inspection

**The duplicate that wasn't.** `00_WELTANSCHAUUNG_KERNEL_v0.2_EMERGENTISM_ONLY.md`
exists at both root and `06_ONTOLOGY/`. Same name, different depth — and **different
bytes** (`250b57d4…` vs `600e0126…`). Two documents, not a duplication. Tidying on the
name alone would have destroyed content.

**The citation baseline is branch-dependent.** Baseline `2043` was stored at commit
`eab26dae`; the current branch differs from `main` by **35 `.md` files**, which the
gate counts. So part of the "+17 drift" in board Update 2 is not decay — it is the
checkout. Attribution must control for branch before anything is repaired. This is
the measured-findings-decay rule in a new form: **a measurement is true of a branch,
not only of a date.**

Also corrected during the audit: an agent's `/usr/bin/ps` check returned silence and
nearly became "no Codex processes are running." `ps` is at `/bin/ps` on this machine.
The instrument had not run at all — the third distinct instance this week of a check
reporting a property it never tested.

## 5 · Chair items, by leverage

1. **Dispose of the 35-entry change set in `…refinement-20260821`** — atomically, explicit
   pathspec, archive commit separate from doctrinal commit. Highest exposure on the board.
2. **Dispose of the 4-file `spark-reader` rewrite** — the only copy of a public front-door change.
3. **Decide the fate of 8 unmerged branches** — merge, archive, or push. They are one disk
   failure from gone; four have no offsite copy at all.
4. **`chore/glyph-migration-2026-08-14` has diverged** (ahead 5, behind 5) and carries the
   emission-green work and `09_THE_THREE_SCRIPTS_AND_THE_LIMIT`. It is the one branch that
   cannot be fast-forwarded.
5. Then the standing items: `C3` DNS cutover, `D1`, the disposition batch.

## 6 · The single biggest risk

Not disorder — **concentration**. Four branch tips and ~496 lines of untracked work exist
in exactly one place each. The rescue snapshot converts the untracked half from
unrecoverable to recoverable, but it is a copy on the same disk. **Nothing here is safe
until those branches reach a remote**, and that is a chair act.

**Canonical path:** `01_EMERGENTISM/00_HANDOFF/TIDY_RECEIPT_2026_08_21.md`
