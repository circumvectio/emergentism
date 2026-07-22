---
title: "Emergentism public site"
status: "RELEASE CANDIDATE — local, not deployed by this work"
date: 2026-07-22
evidence_tier: "[B] repository/build state; doctrine inherits source tiers"
---

# Emergentism public site

The site is an operable compass and public research surface for a stranger: the
reality scaffold in order, open sockets visible in place, the method usable
without assent, the claims priced, the deaths dated, and the exit visible.

## Primary journey

1. [`map/`](map/) — the dimension-first scaffold and its open sockets.
2. [`discoveries/`](discoveries/) — the strongest public insights, at tier.
3. [`lab/`](lab/) — packet-complete, evidence-open research questions.
4. [`contribute/`](contribute/) — bounded compute, local runs, review, and evidence.
5. [`practice/`](practice/) — use the discipline without required assent.
6. [`record/`](record/) — corrections, nulls, and dated deaths.
7. [`exit/`](exit/) — put the map down.

The detailed spine remains available at [`dimensions/`](dimensions/) and
[`0/`](0/) through [`6/`](6/). The older [`compass/`](compass/) remains a
compressed reading, not the primary research interface.

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
