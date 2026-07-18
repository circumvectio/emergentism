---
type: archive-tombstone
title: "Preserved Mathematical Register — pre-narrative D0–D6 surface"
date: 2026-07-18
status: "[S] K3 archive-first · preserved for inspection, not for deployment"
tier: "[S] standing rule: archive is non-canonical, non-citable, non-deployed"
supersedes: "12_PUBLIC_SITE/trinity/00-the-genesis-simulation/ through 06-the-cosmological-cycle/ (the live narrative register; deploys to the public site)"
parent: "12_PUBLIC_SITE/90_ARCHIVE/tool_noise/2026_07_14_compass_restructure/"
reason: "the 2026-07-14 compass restructure replaced the mathematical D0–D6 register (12_PUBLIC_SITE/0/..6/) with the narrative register (12_PUBLIC_SITE/trinity/00..06-...). The mathematical version was not deleted — K3 archive-first requires it be moved here with full git history. The narrative trinity/ is the live canonical surface; this archive is the math-comparison surface."
deployment: "EXCLUDED via .vercelignore (added 2026-07-18 alongside this move). The D0–D6 URLs are no longer served; the narrative /trinity/ URLs are the only live compass surface."
do_not_redeploy: true
do_not_delete: true
---

# Preserved Mathematical Register — D0–D6 (2026-07-12)

This directory holds the **mathematical D0–D6 register** of the public site
as it stood immediately before the 2026-07-14 compass restructure. It is
preserved under K3 archive-first; the live canonical surface is now the
**narrative register** at `12_PUBLIC_SITE/trinity/`.

## What was here

| Old URL | Old title (from `<title>`) | New narrative surface (`trinity/`) |
|---|---|---|
| `/0/` | Titans of Numbers | `trinity/00-the-genesis-simulation/` |
| `/1/` | The Special One | `trinity/01-the-emergence/` |
| `/2/` | The Mu-Limit | `trinity/02-the-trinity/` |
| `/3/` | Sphere / Bloch Sphere | `trinity/03-the-closure/` |
| `/4/` | Horn Torus | `trinity/04-bit-to-qubit/` |
| `/5/` | The Burrisphere | `trinity/05-division-by-zero/` |
| `/6/` | CCC Return | `trinity/06-the-cosmological-cycle/` |

The mathematical register kept the D0–D6 register glyphs and the
mathematical Dasein register; the narrative register tells the same arc
as a book-length story. The two are parallel renderings of the same
D0–D6 content, not duplicates — keep this archive for the math side.

## Why it was moved (K3 archive-first)

- The 0–6 dirs were tracked in git but were no longer linked from any
  canonical compass surface after the 2026-07-14 restructure.
- They were being deployed as live orphan pages at `/0/`, `/1/`, ..., `/6/`
  on the public site (Vercel) — a real deployment risk and a real reader
  confusion vector.
- Per the standing K3 rule: withdrawn content is tombstoned under
  `90_ARCHIVE/`, never erased. `git mv` preserves the full commit history
  (the index entries `R` in `git status` confirm the rename detection).

## Deployment

`.vercelignore` was updated (2026-07-18) to exclude this directory and
the parent `2026_07_14_compass_restructure/`. The live public site no
longer serves the D0–D6 URLs; readers reach the same content via the
narrative register at `/trinity/`.

## Do not

- **Do not redeploy** the 0–6 dirs to the public site. They are
  renumbering residue. The trinity/ surface is the live compass.
- **Do not delete** this directory. The mathematical D0–D6 register
  has a separate epistemic value (the math-side canon, the Dasein
  register, the block-sphere / horn-torus / Burrisphere treatments)
  that the narrative register does not preserve 1:1. K3 keeps it.
- **Do not move** the 0–6 dirs back to the public surface without a
  fresh K2 disposition and a new compass-restructuring receipt.

## If you need to cite a D0–D6 fact

- Use `12_PUBLIC_SITE/trinity/0N-*/index.html` for the narrative version.
- Use this directory only when the math-side register is load-bearing
  (e.g., the D3 Bloch sphere, the D5 Burrisphere, the D6 CCC return)
  and the narrative side glosses over the math.

`⊙ = • × ○`
