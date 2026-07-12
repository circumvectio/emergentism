---
title: "125 — Full content review + refinement: de-fabricated openness, exit-door reachability, tier corrections, library noindex — SHIPPED under the website delegation"
date: 2026-07-12
status: "[E] EXECUTED under the receipt-123 website delegation (operational lane). K2: 'read and review everything, is it optimal for the mission, refine and improve.' A 6-agent review (4 spine clusters + exposure + synthesis) produced a verdict + refinement plan; the high-value items are implemented, gate PASS, deployed to Vercel prod, verified live. ONE judgment call flagged for K2 override (§4)."
evidence_tier: "[S] the fixes (gate green, in-browser + live-header verified); [I] the review judgments; [A] the ground-truth checks (repo paths, generator deps)"
verdict_extends: "receipt 120 (mission/telos) · receipt 121 (honest foundation) · receipt 123 (delegation) · receipt 124 (prior stakeholder pass)"
owner: "K2 delegated the website lane; software reviewed + refined + shipped. The noindex call (§4) is flagged for K2 to countersign or override."
parents:
  - ./124_PRIME_TIME_PWA_STAKEHOLDER_AUDIT_SHIP.md
  - ./123_SITE_DELEGATION_GATE_GREEN_SHIP.md
---

# 125 · Content review → refinement → ship

## 1. Verdict

**Not optimal as-is; the bones were right but four defect classes made the site
*perform* virtues it should *embody*.** All fixed as static edits:

1. **Fabricated openness (the worst).** `/build/` and `/exit/` "run it yourself"
   blocks pointed at a repo (`yvesrb/magnum-opus`, `skyzai/emergentism-build`)
   and paths (`_generator/`, `requirements.txt`, `npm run test:k4`) that **do
   not exist** — a skeptic taking the site's central dare hit a 404 on line one.
   The `/build/` receipt was a hardcoded mock asserting "not hand-edited." This
   is the one failure the mission explicitly forbids (openness must be LIVE).
   **Fixed** against ground truth: real repo `circumvectio/emergentism`, the real
   stdlib `predeploy_check.py`, `pip install markdown` for generation; receipt
   relabeled `[C]` illustrative-not-live; footer fake-stamp neutralized; the
   fake k4 test-suite replaced with what is actually verifiable + a `[C]`-planned
   note for the rest.
2. **Exit door invisible from the deepest pages.** `/0/`–`/6/` chrome linked no
   Compass/Poisons/Exit — breaking "K4 visible from inside" and "the open loop
   stays visible" from the ladder rungs. **Fixed:** Compass/Poisons/Exit now in
   the nav on all seven.
3. **Residual cathedral framing.** journey's "the cathedral stays, the door
   changes" ratified the exact self-image the mission renounces. **Fixed** to
   packaging-discipline framing.
4. **Tier drift.** `/map/` wore its top empirical badge `[B]` on interpretive
   caste rows (tripping its own kill-criterion) while burying the proven math;
   `/exit/` inflated a policy to `[A]` "leave with everything"; the journey hub
   rendered the unwon `Φ×V` product uncaveated. **Fixed:** map caste rows
   `[B]→[I]`, `φ·ν=1→[A]`, K2-collapse `→[S]`; exit `→[S]` "leave with what is
   yours" (canon: redeemable, not everything); journey `foresight × means →`
   need-both AND-class with `[C]`/`[S]` note.

## 2. The compression decision (the deepest mission issue)

367 pages / 8.4M chars were reachable and **all 357 were search-indexed** —
a first-contact reader from Google could land inside `trinity/…` with no
compass, no tier frame, no exit. **Fix (option c): noindex the ~15 generated
wings at the edge; keep them reachable + crawlable (`noindex, follow`); trim the
sitemap 357→17 to the spine + `/read/`; add a threshold banner atop `/read/`.**
Verified live: library wings return `x-robots-tag: noindex, follow`; spine
(compass/read/5/amrita) stays indexable. Search now lands on the compass; the
cathedral is reachable but never the front face. Nothing deleted (K3), nothing
unlinked, still forkable — OPEN preserved.

*Implementation note:* the first Vercel pattern (`:wing(a|b|…)/:path*` named-
param alternation) silently failed to match trailing-slash dirs; switched to the
proven per-wing `(.*)` form.

## 3. What was left excellent, untouched

The compass hero tier-trio; "the exit is marked on the inside"; the `/test/`
two-column falsifier discipline; the halāhala coda + the `φ·ν=1 [S]` /
`(φ−ν)²≥0 [A]` box; `/6/` (CCC as analogy-not-identity) and `/1/`.

## 4. The one judgment call flagged for K2

**noindex on the generated library is a real reduction in search
*discoverability* of the corpus.** The argument that it does not reduce
*openness* rests on "not the first thing search surfaces" ≠ "not available"
(still crawlable, reachable, forkable) — defensible and consistent with "compass
not cathedral," but it is a judgment about what "open" obligates. I made the
call in-lane (it's reversible: delete the vercel.json header block); **K2 can
override.**

## 5. Git + deploy state

Deployed to Vercel prod from the working tree; all refinements + noindex
verified live. The site commits (`e47f16e`, `6a6fec1`) landed on branch
`fix/apply-seams-110-115` (a concurrent agent left the shared worktree there;
its `04ff9c5` canon-tidy commit is path-disjoint — zero `12_PUBLIC_SITE` files —
so nothing was clobbered). Pushed to `origin/fix/apply-seams-110-115` (fast-
forward). **The merge to `main` is deferred to the cross-branch coordination
running across the 9 active worktrees — not force-reconciled unilaterally.**
Follow-up work order (freeze-gated, needs the generator not a static edit):
bake `noindex` + Exit-in-nav into `generate_public_library.py` so a future
`--force` regeneration keeps both.

## 6. Disposition

`[E]` in the delegated lane. The site now embodies the mission it states: the
"run it yourself" dare is true, the exit is one click from every rung, the tiers
are right-side-up, and search meets the reader at the compass.
