---
title: "AGENTS.md — 13_BOOKS projection route"
status: "ACTIVE — projection-only book reconstruction boundary"
date: 2026-07-28
evidence_tier: "[S] routing and custody contract"
owner: "00_META control plane; semantic owners remain K-1 through K-7"
---

# 13_BOOKS — Projection-Only Critical Editions

This directory rebuilds reader books from reviewed claim cards. It is not K-8,
does not own doctrine, and may never override K-1 through K-7. Repair a claim at
its current semantic owner before changing a current edition here.

## Boundaries

- Historical external AIA manuscripts are read-only provenance. Never edit,
  move, silently modernize, or copy them into authority here.
- `book-manifest.json` is the route and build contract. It is not evidence for
  any claim listed in it.
- A chapter may enter a current edition only at 100% claim-card coverage.
- `legacy`, `frozen`, `archive`, and `withheld` material cannot become current
  by quotation, generation, or publication.
- Reader wording must be weaker than or equal to its owners. L7 may compress;
  it may not strengthen.
- Rosetta names work functions, never human ranks.

## Review sequence

L5 maps owners and dependencies; L1 and L2 test harm and rivals; L3 audits;
L4 applies bounded source changes; L6 preserves superseded material; L7 writes
reader language; L3 checks projection parity. Public release remains a separate
gate under `../00_CONTROL/PUBLIC_SITE_BOUNDARY.md`.
