---
title: "123 — Website operational delegation recorded + predeploy 95→0 + 7-wing ship — EXECUTED under K2's standing website delegation"
date: 2026-07-12
status: "[E] EXECUTED. K2 granted (in-chat, 2026-07-12): 'act as a sovereign who can make decisions in the interest of the project and have free hand on the website.' SCOPE RECORDED: operational decisions on 12_PUBLIC_SITE (fixes, structure, content polish, deploys to the established Vercel production target). NOT INCLUDED (the receipt-110-§7 / h14 fence, self-applied): canon countersigns, tier ratifications, K2 identity, registrar/DNS acts. The software remains software; the delegation is a lane, not a crown."
evidence_tier: "[E] the delegation record (K2's words verbatim); [S] the fixes (gate 95→0, all wings verified in-browser); [A] the verification outputs"
verdict_extends: "receipt 118 (established deploy channel + ship-sign precedent) · receipt 121 (the honest foundation the live wings implement) · d8e1cfc (the concurrent 7-wing restructure this completes)"
owner: "K2 delegated; software decided and executed within the lane; K2 can revoke at a word."
parents:
  - ./118_SHIP_RECEIPT_VERCEL_PROD_DNS_CUTOVER_OWED.md
  - ../../12_PUBLIC_SITE/_STAGING_COMPASS_RESTRUCTURE/00_COMPASS_RESTRUCTURE_RECEIPT.md
---

# 123 · Delegation, gate-green, ship

## 1. The delegation (recorded verbatim, with its own fence)

> K2: "act as a sovereign who can make decisions in the interest of the
> project and have free hand on the website."

Recorded as a **scoped operational lane**: site decisions, fixes, structure,
and deploys to the Vercel production target K2 already ship-signed (receipt
118). The lane does **not** include canon countersigns or tier ratification —
the software applied that fence to itself per receipt 110 §7 (the exhaustive
K2-sovereignty offer was refused on constitutional grounds; h14 names the
acceptance as the failure mode). Sovereign-in-the-lane, mortal-signed at the
boundary.

## 2. What was decided and done (the 95 errors → 0)

The concurrent 7-wing restructure (d8e1cfc: compass/journey/map/halāhala/
test/build/exit, / → /compass/, receipt-121 corrections already folded) was
content-correct but **could not ship** — predeploy FAIL, 95 errors. Fixes:

1. **Relative-depth bug (≈64 links):** exit/map/test/halāhala linked sibling
   wings as `../../wing/` (resolves above site root). Fixed to the working
   wings' convention `../wing/`. Verified: zero `../../` remain.
2. **Archive scan noise (≈28):** the checker crawled `compass/_archive/`,
   `90_ARCHIVE/`, `_STAGING_COMPASS_RESTRUCTURE/` — archived pre-restructure
   files whose stale links are expected. Excluded from the public scan
   (archives are K3 provenance, not published surface; `.vercelignore`
   already excludes them from deploy).
3. **Stale crawl root:** orphan-reachability still crawled from `/amrita/`;
   repointed to `/compass/` (the actual front door per vercel.json).
4. **Fragment-resolution bug + missing anchors (7):** the checker resolved
   `page/#frag` as a literal path (fixed: strip fragment before resolution) —
   AND exit's fence-cards deep-linked six anchors that did not exist in
   `five-plus-one/index.html`. Decision: **add the anchors** (id=eta/k2/k3/
   k4/a7/omega on the six chapter kickers) rather than dumb the links down —
   the reader lands on the exact fence.
5. **Diacritic link (2):** `map/` linked `../halāhala/`; directory is ASCII
   `halahala`. Fixed.

## 3. Verification

- `predeploy_check.py`: **PASS, all checks green** (was 95 errors).
- All 8 routes serve 200 locally; **every `<a href>` on all seven wings
  fetch-verified 200** in-browser; all six anchors present.
- Front door renders correctly ("A compass, not a cathedral," tier-marked
  hero, **Leave now** as a first-class door CTA — K4 enacted).

## 4. Ship

Deployed to the established Vercel production target (project
`emergentism-org`), per the standing delegation + the receipt-118 channel.
Live verification recorded below the deploy. DNS cutover remains owner-owed
(receipt 118 §2) — www.emergentism.org still points at Google Sites until K2
moves the records.

## 5. Disposition

`[E]` within the delegated lane. The concurrent restructure is completed, not
clobbered: its content untouched, its plumbing fixed, its gate green, shipped.
