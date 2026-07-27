---
title: "Emergentism public site"
status: "ACTIVE RELEASE BOUNDARY — deployment truth requires a dated external receipt"
date: 2026-07-22
evidence_tier: "[B] repository/build state; doctrine inherits source tiers"
---

# Emergentism public site

The site is an operable compass and public research surface for a stranger: the
reality scaffold in order, open sockets visible in place, the method usable
without assent, the claims priced, the deaths dated, and the exit visible.

## Primary journey

The founder-facing sequence is deliberately narrower than the library:

1. [`index.html`](index.html) — remember Finity, distinguish possible from
   actual power, and frame one decision.
2. [`practice/`](practice/) — use the Finity Card and continue into the deeper
   practices without required assent.
3. [`plainly/`](plainly/) and [`book/`](book/) — understand the worldview in
   ordinary language, then enter the short living book.
4. [`5/`](5/) and [`rosetta/`](rosetta/) — inspect D5 possible power, D4 actual
   power, and the four-move/three-frame transformation grammar.
5. [`discoveries/`](discoveries/) and [`map/`](map/) — explore the wider claims
   and the dimension-first scaffold at their stated tiers.
6. [`lab/`](lab/) and [`record/`](record/) — test open claims and inspect dated
   corrections after the useful idea has been demonstrated.
7. [`contribute/`](contribute/) — contribute bounded evidence, expertise,
   contradiction reports, or locally custodied compute.
8. [`exit/`](exit/) — put the map down.

The detailed spine remains available at [`dimensions/`](dimensions/) and
[`0/`](0/) through [`6/`](6/). The older [`compass/`](compass/) remains a
compressed reading, not the primary research interface.

## Founder value architecture

The public front is organized as a value sequence, not a directory:

1. **Memetic unit — Finity.** One ownable word and one useful distinction: a
   finite, observable boundary an open process can approach.
2. **Mechanism — the power seam.** D5 possible power is evaluated by a present
   D4 model and meets D4 actual power; possibility alone does not act.
3. **First value — the Finity Card.** A visitor can turn one live decision into
   a bounded next move before accepting the wider worldview.
4. **Expansion — the Rosetta.** Four moves and three frames translate how power
   is taken, given, created, dissolved, and preserved across domains.
5. **Trust — consequence before adherence.** The laboratory, trial record,
   rivals, kill criteria, and exit remain available after the useful idea has
   been demonstrated.
6. **Participation — Apply, Learn, Test, Build.** These four doors are the main
   routes; the full corpus remains reachable without competing with the first
   action.

The intended value loop is:

`clear idea → useful decision → consequence receipt → better evidence → stronger map → wider use`

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
- `book-pwa/` is a frozen historical source snapshot excluded from deployment;
  it is not part of the Emergentism release.

## Build and verification

```text
python3 render_dimension_site.py
python3 build_book.py
python3 build_rag_index.py
python3 apply_frozen_library_boundary.py
python3 predeploy_check.py
```

The deploy boundary is `.vercelignore`; `vercel.json` supplies headers and the
root redirect. No external scripts, stylesheets, fonts, or media are required.

The contribution page is a static contract in this release. It accepts no
payments, API credentials, private data, or live inference jobs. A future
compute broker requires a separate server-side security and authorization gate.

## Current release truth

This repository can produce locally checked static bytes. Deployment, the
branded domain, external red-team review, and empirical calibration are
separate gates and must be reported separately.
