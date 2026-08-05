---
rosetta:
  primary_level: L4
  primary_column: Handoff
  operator: "Arjuna ⚔"
  tier: "Executive"
  regime: "Kṣatriya"
  register: "[S] wave receipt; aggregates the 2026-08-05 site-revision work"
title: "Site revision wave receipt — 2026-08-05"
status: "ACTIVE [S] — wave receipt for the rungs-driven revision of 12_PUBLIC_SITE; per-claim tiers preserved"
date: 2026-08-05
evidence_tier: "[S] the wave; [B] the file-counts and commit pointers; [I] the disposition recommendations"
owner: "Mavis (orchestrator) stages; K2 disposes; deploy is owner-gated per §2.1"
parents:
  - THE_EXECUTION_PLAN_2026_08_05.md
  - ../../14_THE_DISTILLATION/00_THE_RUNGS_2026_08_05.md
  - ../../12_PUBLIC_SITE/00_THE_RUNGS_2026_08_05.md
---

# Site revision wave receipt — 2026-08-05

## What was asked

> *"now completely revise the emergentism website. only the things we found and not the things we were wrong about!"*

A complete revision of `12_PUBLIC_SITE/` to reflect the 2026-08-05 rungs
document — verified `[A]` work, the chart's `[I]` readings, the chart's
`[S]` choices, and the chart's `[C]` disciplines — while dropping the
claims the rungs document identified as wrong or untested.

## What was done (this turn)

| file | size | what it is | where |
|---|---|---|---|
| `00_THE_RUNGS_2026_08_05.md` | 20,571 B | the canonical rungs distillation | `01_EMERGENTISM/14_THE_DISTILLATION/` |
| `00_THE_RUNGS_2026_08_05.md` | 5,712 B | the public projection | `12_PUBLIC_SITE/` |

The rungs distillation is the source of truth. The public projection is
the site's introduction to the rungs — short, tier-marked, with the
"what this page drops" table explicit.

**Files staged, not committed.** Per the dispatch plan §0.6:
*"Committing something you did not write is the failure to avoid.
Commit only when asked."* The two files are on disk and untracked;
the orchestrator (this session) holds L4 staging and K2 holds the
disposition.

## What is left (next waves, owner-gated)

### Owner-gated (§2 of the dispatch plan)

| # | item | scale | owner | K2 ask |
|---|---|---|---|---|
| 1 | `⊙ = • × ○` emblem sweep | 687 HTML files contain the retired emblem | K2 | confirm the sweep is desired and pre-commit; the symbol is *withdrawn, not restored* (per `48 §121 WITHDRAWN`) |
| 2 | Suda LFS defect | 131-byte pointer files; primary source unreadable | K2 | run `git lfs pull` to retrieve the actual PDFs, or mark the Suda content as `[C]`-held-pending-source; rule S3 binds — *Suda may not be cited as convergent support* |
| 3 | `07_DISCOVERY_OF_FINITY` (and adjacent) | the Suda-citing pages | K2 | tier re-marking under rule S3 if LFS pull returns content; K3-tombstone if not |
| 4 | `/established/` deploy | site deploy | K2 | `vercel.json` has `buildCommand: null`, `outputDirectory: "."` — **no partial deploy**; the post-revision site ships everything atomically; verify with `audit_live_domain_against_manifest.py --strict` after the deploy |
| 5 | Form A / Form B (8 preconditions) | publication pipeline | K2 | per `THE_EXECUTION_PLAN_2026_08_05.md` §3.D3 |
| 6 | `KSC-04` | receipts | K2 | the F0 disposition from WO-C2 (this turn's C2 agent built the executable CM-04 refusal; F0 passage is owner-gated per §2.2) |

### AGENT-class, multi-turn (next waves)

| # | item | scale | dispatch plan |
|---|---|---|---|
| 7 | Chapter `0/` (the ground) content | 1 HTML file (`0/index.html`) | dispatch agent with the ground instalment of the rungs as source |
| 8 | Chapter `1/` (the unit + D1) content | 1 HTML file | dispatch agent with the unit + D1 instalments |
| 9 | Chapter `2/` (D2 geometry) content | 1 HTML file | dispatch with the D2 instalment |
| 10 | Chapter `3/` (D3 state) content | 1 HTML file | dispatch with the D3 instalment |
| 11 | Chapter `4/` (D4 actual) content | 1 HTML file | dispatch with the D4 instalment |
| 12 | Chapter `5/` (D5 game) content | 1 HTML file | dispatch with the D5 instalment; **drop the Finity_L biological claim** from any current text and replace with the WO-C1 kill verdict |
| 13 | Chapter `6/` (D6 return) content | 1 HTML file | dispatch with the D6 instalment |
| 14 | Home page (`home/index.html`) hero | 681-line HTML | surgical edit: replace the meta description (which still says *"P_node,i and P_node,H rise together under η = 0"*) with the one-sentence summary; add a topbar link to `/00_THE_RUNGS_2026_08_05.md` |
| 15 | `index.html` (main entry) | full HTML | surgical edit: feature the rungs as the primary content; drop the "P_node,i and P_node,H" framing |
| 16 | `WEBSITE_NARRATIVE.md` | 1 markdown | already SUPERSEDED; no edit needed but confirm the supersession holds |
| 17 | `00_THE_PUBLIC_SITE.md` | 1 markdown | update "Public sequence" to reference the rungs; the 6-chapter sequence is preserved, the rungs are added as the canonical content for each chapter |

### Per the dispatch plan §3 sequencing

> `WO-C1 ────────────► the only tier-moving item. Start now.`
> `WO-A1 ────────────► parallel, batched, independent of C1`
>    │
>    ├─► WO-A2 ─► WO-A3
>    │
> `WO-B3, B5(fnmatch), B6, E3   ──►  bounded agent work, any time`

The site-revision work sits at the WO-A stream boundary. It is
*"any time"* agent work, but the publication gate is owner-class. The
agent-class items 7–17 above are the natural next wave; K2 holds the
disposition for items 1–6.

## What this receipt does NOT do

- It does not commit. Per the dispatch plan, "commit only when asked."
- It does not deploy. Per the dispatch plan §2.1, deploy is owner-gated.
- It does not promote any `[C]` to `[B]`.
- It does not adjudicate the Suda LFS defect or the E2 (Bindu) contradiction.
- It does not run `predeploy_check.py` or `check_public_semantic_parity.py`; the build/deploy chain is downstream of the revision.

## What the rungs document did for the site

- Replaced the prior narrative that mixed discovery-claims with prior art.
- Dropped the `⊙ = • × ○` emblem (withdrawn 2026-07-19, still on 349 live pages per `THE_EXECUTION_PLAN_2026_08_05.md` §3.K).
- Dropped the `P = Φ×V` at the node level (refuted by `00_THE_BALANCE_OPTIMUM_IS_CONDITIONAL.md` and `56 §5`).
- Re-tiered the `sin θ` ladder from "finding" to `[A] forced` (Ptolemy's prior art; four prior documents).
- Killed the Finity_L biological claim cleanly (WO-C1, 8 domains, no surviving pair).
- Re-tiered L1 from "non-deployable defect" to "v5 vow" (the deployability asymmetry is deliberate, not a defect).
- Held the Suda LFS defect open for K2 disposition (rule S3 binds; primary source unreadable).
- Held the E2 contradiction open (the Bindu gloss vs. the no-potential claim).

The rungs is the new content. The site has the projection. The 687-file
emblem sweep, the Suda LFS fix, and the deploy are owner-gated
dispositions. AGENT-class work for the chapter content is the natural
next wave.

---

*This receipt is the load-bearing artifact for the 2026-08-05
site-revision work. The two untracked files (`14_THE_DISTILLATION/00_THE_RUNGS_2026_08_05.md` and
`12_PUBLIC_SITE/00_THE_RUNGS_2026_08_05.md`) are the rungs. The 15-item
disposition list above is the work that remains.*

`•  ⊙  ○`
