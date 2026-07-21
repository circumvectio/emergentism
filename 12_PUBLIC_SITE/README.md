---
title: "Emergentism public site — pure release boundary"
status: "ACTIVE — 36-route discovery-led release"
evidence_tier: "[I] public translation; [B] only for dated build and deployment receipts"
---

# Emergentism public site

This is a compact public projection of Emergentism: discoveries, plain-language
explanations, the Soul Loop practice, the Compass and Stone, falsifiers,
corrections, and Grace Exit. It is not a second canon and contains no product,
venture, company, runtime, or external-governance premise.

## Release architecture

[`release-manifest.json`](release-manifest.json) is the only route/file
allowlist. It declares 36 HTML routes and their exact assets.
[`build_release.py`](build_release.py) copies only those bytes into `.release/`
and embeds a deterministic tree hash. Vercel serves `.release/`, never the
source directory.

The former generated library, migrated application source, receipts, plans, and
superseded public pages are preserved under
`90_ARCHIVE/pure_emergentism_boundary_2026_07_20/`. Both `.vercelignore` and the
allowlist builder exclude that archive. Historical URLs therefore return
404/410 rather than exposing stale doctrine.

## Local release gate

```bash
python3 -B build_pwa.py --check
python3 -B build_atlas_index.py --check
python3 -B build_release.py
python3 -B predeploy_check.py --release .release
```

The gate verifies exact output-file equality, deterministic hash, zero external
system leakage, claim-boundary negatives, HTML and asset closure, route
reachability, Atlas/PWA/sitemap agreement, and the archive boundary.

## Deployment truth

`deploy.sh` runs the same gate and asks Vercel to build the same manifest-bound
tree. A passing local gate is not a deployment. A preview URL is not production
promotion. A Vercel production alias is not proof that `emergentism.org` DNS
serves it. Canonical and Open Graph URLs declare the intended public address;
their presence in source is not evidence that DNS is live. Verify each state separately with:

```bash
python3 -B audit_live_domain_against_manifest.py --strict --base-url URL
```

Private-person money movement or legal-contract signatures are outside this
editorial release lane. AI and repository work follows the user's scope,
repository permissions, provenance, reversibility, and tests.

The public promise is use without belief: see the proposals, try the practice,
inspect the record, and put down the map.
