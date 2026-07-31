---
title: "Emergentism public site"
status: "ACTIVE RELEASE BOUNDARY — deployment truth requires a dated external receipt"
date: 2026-07-22
evidence_tier: "[B] repository/build state; doctrine inherits source tiers"
---

# Emergentism public site

The site is the public front door to Emergentism: a fallibilist worldview for
finite beings, made usable through Finity. A stranger should understand the
category, try one bounded practice, inspect claims at their stated prices,
follow dated corrections, and keep an exit visible throughout.

## Primary journey

Six stable doors organize the public journey; Exit is always adjacent:

1. **Practice** — [`practice/`](practice/) carries the source-owned Finity Card,
   a local commitment/outcome receipt builder, a clearly illustrative worked
   example, and optional deeper practices.
2. **Worldview** — [`plainly/`](plainly/) introduces Emergentism in ordinary
   language. [`rosetta/`](rosetta/) leads with seven functional moves; symbolic
   and cross-tradition correspondences remain an optional, tiered appendix.
3. **Research** — [`record/`](record/) is the trust hub. It routes to
   [`discoveries/`](discoveries/), [`lab/`](lab/), [`map/`](map/), sources,
   tests, and dated corrections without turning open work into doctrine.
4. **Library** — [`book/`](book/) is the current reader. [`read/`](read/) remains
   the wider reading index and visibly distinguishes current from frozen work.
5. **Participate** — [`contribute/`](contribute/) starts with three human acts:
   share a Finity receipt, attack a claim, or contribute bounded evidence.
6. **Exit** — [`exit/`](exit/) lets a visitor put the map down without penalty.

[`about/`](about/) is the accountability surface for authorship, category,
boundaries, and missing independent review; it remains available from page
footers without competing with the six primary doors.

The detailed spine remains available at [`dimensions/`](dimensions/) and
[`0/`](0/) through [`6/`](6/). The older [`compass/`](compass/) remains a
compressed reading, not the primary research interface.

## Founder value architecture

The public front is organized as a value sequence, not a directory:

1. **Identity — Emergentism.** A type-disciplined, revisable worldview that
   keeps map and territory, possibility and actuality, choice and consequence
   distinct.
2. **Human problem — finite action.** Reality exceeds every map, yet finite
   beings still have to choose and act.
3. **First practice — Finity.** A visitor can use seven prompts to frame one
   live decision, predeclare a review point, and record an observed outcome
   without accepting the wider worldview. Comparative benefit remains `[C]`.
4. **World contact — the receipt loop.** A map proposes, action meets reality,
   consequence returns a receipt, and the map is revised.
5. **Expansion — the Rosetta.** Seven functional terms—constrain, remove,
   enable, commit, create, dissolve, preserve—lead. Mythic names and comparative
   correspondences are optional research mnemonics, not ranks or proof.
6. **Trust — consequence before adherence.** The laboratory, trial record,
   rivals, kill criteria, and exit remain available beside the practical
   offer. A worked example demonstrates format, not efficacy.
7. **Participation — Use, Attack, Evidence.** A receipt, a contradiction, or one
   bounded contribution is enough; membership and assent are never required.

The intended value loop is:

`fallible map → possible futures → Finity → actual move → observed outcome → revised map`

No step depends on membership, belief, payment, or delegated truth authority.

## Source and projection boundary

- `public_semantic_parity.json` binds pages to current source owners.
- `living-map.json` routes open work and contribution modes; it cannot create or
  promote doctrine.
- `render_dimension_site.py` deterministically renders `/dimensions/` and
  `/0/…/6/`.
- `check_public_semantic_parity.py` rejects dimensional inversions, literal
  closure, forbidden quantum inflation, physical-cone expansion language, and
  application-authority leakage on current surfaces.
- Frozen generated-library pages remain readable as historical projections,
  carry a non-authority banner, are `noindex`, and are excluded from current
  book retrieval.
- A typed set of historical exceptions may be withheld from public routing or
  redirected to an archival notice when its old copy would create an unsafe or
  materially misleading first impression. Source custody remains in the
  repository; withholding a route is neither deletion nor evidence promotion.
- `book-pwa/` is a frozen historical source snapshot excluded from deployment;
  it is not part of the Emergentism release.

## Build and verification

```text
python3 render_dimension_site.py
python3 build_book.py
python3 build_book.py --check
python3 build_rag_index.py
python3 refresh_reading_manifest.py
python3 refresh_reading_manifest.py --check
python3 apply_frozen_library_boundary.py
python3 predeploy_check.py
```

`refresh_reading_manifest.py` preserves the frozen June library document list
byte-for-byte at the data level and refreshes only its lifecycle declaration
and the current One-Sitting reader contract. It does not regenerate or promote
the frozen library pages.

The deploy boundary is `.vercelignore`; `vercel.json` supplies headers and the
root redirect. No external scripts, stylesheets, fonts, or media are required.

## How to actually deploy

Added 2026-07-31. Until then this document ended at `predeploy_check.py`, so a
newcomer could produce release-candidate bytes and had no documented way to ship
them.

```bash
cd 12_PUBLIC_SITE && vercel --prod --yes
```

- The project is already linked; `.vercel/project.json` holds the ids. **Never open,
  print, or commit `.vercel/.env.production.local`** — it is gitignored and holds
  deploy credentials.
- The live domain is `https://emergentism.org`. A deploy that reports
  `"target": "production"` and `READY` has shipped bytes; it has not verified them.

**A green local gate does not prove what the host returns.** `vercel.json` headers
are only observable against the deployed domain, and on 2026-07-31 seven routes were
found silently indexable because nothing checked. After every deploy that touches
`vercel.json` or any route's publication status, verify against the live domain:

```bash
curl -sI https://emergentism.org/titans/ | grep -i x-robots-tag
```

Expected: the four **declared-provisional** routes (`/amrita/ /egg/ /riemann/ /suda/`)
return **no** `X-Robots-Tag` and are indexable; every frozen-library route and
`/offline/` return `noindex, follow`. `09_TOOLS/01_SCRIPTS/check_q4_declarations.py`
guards the page-side half of this and says plainly that it cannot check the host.

The contribution page is a static contract in this release. It accepts no
payments, API credentials, private data, or live inference jobs. Any future
compute broker would require a separate server-side security and authorization
gate; this release does not promise or expose one.

## Current release truth

This repository can produce locally checked static bytes. Deployment, the
branded domain, external red-team review, and empirical calibration are
separate gates and must be reported separately.

The Finity evaluation program is typed as three draft gates with contact
deferred: fresh-reader comprehension, conflict-declared independent review, and
a four-arm comparison against a strongest component-matched ordinary worksheet.
Exact materials, review bundle, ethics determination, analysis assets, and
freeze remain outstanding. No reader or participant has been contacted, no
external review exists, no ethics determination or preregistration exists, and
no data or result exists. The Laboratory may expose those absences; it may not
turn the drafts themselves into evidence.
