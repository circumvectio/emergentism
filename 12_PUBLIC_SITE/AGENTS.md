---
title: "12_PUBLIC_SITE - Agent Routing"
status: "ACTIVE - frozen public-site/source-preserving route"
evidence_tier: "[S] for Rosetta-linked doctrine; [I]/[C] for public interpretation and scaffold claims; [B] only for dated build/deploy/product receipts."
type: public-site-route-card
scope: Emergentism public-site prototypes and frozen Infinite Book PWA source pending AIA migration.
sources:
  - 01_EMERGENTISM/12_PUBLIC_SITE/README.md
  - 01_EMERGENTISM/12_PUBLIC_SITE/00_K2_ENVELOPE_APP_MIGRATION_2026_05_31.md
  - 01_EMERGENTISM/12_PUBLIC_SITE/book-pwa/AGENTS.md
rosetta:
  primary_level: L5
  primary_column: Cosmology
  operator: "Brahmā ○"
  tier: "Executive"
  regime: "Brāhmaṇa"
  register: "[I]"
  canonical_phrase: "Public site agent routing"
---

# 12_PUBLIC_SITE - Agent Routing

**Lane scope:** public narrative prototypes plus the K3-frozen `book-pwa/` source — **moved → `02_SKYZAI/03_AIA/app/` per K2 signoff 2026-06-11** (see `00_BOOK_PWA_MOVED.md`). The K2 envelope is now CLOSED; source tree preserved per K3, archival pending deploy-readiness verification.
**Primary lead:** L5 for public-site architecture, with L3 evidence audit and L6
boundary control.
**Evidence tier:** `[S]` only for Rosetta-linked doctrine; `[B]` only for dated
build, deployment, payment, auth, model, or runtime receipts.

## Read First

- [`README.md`](README.md)
- [`WEBSITE_NARRATIVE.md`](WEBSITE_NARRATIVE.md)
- [`00_BOOK_PWA_MOVED.md`](00_BOOK_PWA_MOVED.md) — **the K3 tombstone redirecting `book-pwa/` → `02_SKYZAI/03_AIA/app/`**
- [`00_K2_ENVELOPE_APP_MIGRATION_2026_05_31.md`](00_K2_ENVELOPE_APP_MIGRATION_2026_05_31.md) — the signed K2 envelope (now CLOSED, execution receipt 2026-06-12)
- [`book-pwa/AGENTS.md`](book-pwa/AGENTS.md) — preserved source (frozen)
- [`../00_META/03_AGENTZ_DEPLOYMENT_12_PUBLIC_SITE_2026_06_04.md`](../00_META/03_AGENTZ_DEPLOYMENT_12_PUBLIC_SITE_2026_06_04.md)
- [`../00_META/03_AGENTZ_DEPLOYMENT_12_PUBLIC_SITE_2026_06_04.csv`](../00_META/03_AGENTZ_DEPLOYMENT_12_PUBLIC_SITE_2026_06_04.csv)

## Recursive Deployment Control

- Every source-visible folder and file in this lane is covered by
  [`03_AGENTZ_DEPLOYMENT_12_PUBLIC_SITE_2026_06_04.csv`](../00_META/03_AGENTZ_DEPLOYMENT_12_PUBLIC_SITE_2026_06_04.csv).
- `12_PUBLIC_SITE/` is the current physical path. Historical `10_PUBLIC_SITE`
  strings are preserved only as signed-coordinate provenance.
- `book-pwa/` remains source-preserved and frozen for migration, tombstone, and
  public-claim repair only.

## Current Public Library State

- 2026-06-07 control receipt:
  [`../../00_START_HERE/agent_planning/2026_06_07_EMERGENTISM_ORG_PUBLIC_SITE_REORIENTATION.md`](../../00_START_HERE/agent_planning/2026_06_07_EMERGENTISM_ORG_PUBLIC_SITE_REORIENTATION.md).
- `generate_public_library.py` currently renders `docs/handoff` public bundles
  into `read/`, `papers/`, `canon/`, `foundations/`, `trinity`, `formal/`,
  `paradox/`, `memetic/`, `rosettad/`, `operators/`, `will/`, `value/`,
  `ground/`, `sacred/`, `method/`, and `meta/`.
- `reading-manifest.json` currently wires `294` rendered public corpus
  documents.
- `sitemap.xml` currently exposes `351` URLs.
- `predeploy_check.py` is the deploy gate for public-site link, tier, route,
  reading-bundle, publication-boundary, and generated-library chrome coverage.
- `audit_live_domain_against_manifest.py` is the post-deploy/live-domain audit
  gate; run with `--strict` only after the domain is expected to serve this
  static site.
- The GitHub Actions Vercel deployment workflow now performs pull, production
  build, prebuilt production deploy, and strict audit against the returned
  Vercel deployment URL before the custom-domain probe. The custom-domain
  strict gate remains manual/dispatch-only until DNS and hosting cutover are
  expected to serve this repository site.
- The linked Vercel project was refreshed on 2026-06-12
  (`dpl_ELnhnyH9EF8qRXSDV3HQWJtczXWg`), and
  `https://emergentism-org.vercel.app/` serves the repository site. A clean
  staged public preview also exists at `https://emergentism-public.vercel.app/`.
  Live `emergentism.org` / `www.emergentism.org` still requires DNS/host cutover:
  current probes route apex through Squarespace and `www` through Google Sites.

## Routing Law

- `12_PUBLIC_SITE/` is the current physical path.
- `10_PUBLIC_SITE/` references are historical after the migration to this lane.
- `book-pwa/` remains source-preserved and frozen for migration/tombstone/public
  claim repair until the `02_SKYZAI/03_AIA/app/` destination is explicitly accepted.
- Public claims must preserve the `[A/B/S/I/D/C]` evidence ladder.

## Numbered Doctrine Spine (/0–/6)

The dimensional ascent is exposed as 7 HTML route shells (`0/` through `6/`) sharing
a single design system and Three.js bootstrap:

| Path | Shared assets (relative from route dir) |
|------|----------------------------------------|
| `0/`–`6/` | `../assets/css/xai.css`, `../dimensions/dimensions.js` |
| All routes | `../vendor/three-0.160.0/` (self-hosted, pinned) |

- Each page sets `window.DIMENSION_PAGE = { animationMode: "<mode>" }` before loading
  `dimensions.js`. Live modes: `titans`, `logline`, `muLimit`, `bloch`,
  `horn`, `burrisphere`, `ccc`. The script still accepts `convergence` as a
  backward-compatible alias for `ccc`; new route shells should use `ccc`.
- Page shells must not reference external CDNs. Run `./predeploy_check.sh` before deploy.
- `assets/css/spine.css`, `partials/nav.html`, and `partials/topbar.html`
  remain tracked compatibility/shared-layout assets. Do not duplicate them or
  create alternate navigation partials without a route-card update.

## Constraints

- **MIGRATION COMPLETE 2026-06-12:** `book-pwa/` is moved → `02_SKYZAI/03_AIA/app/` per K2 signoff. Source tree preserved here per K3 (do not develop). New AIA engine work goes to `02_SKYZAI/03_AIA/`.
- Do not add new PWA product features in this folder during the frozen interval.
- Do not claim deployment, payment, auth, AI-provider, or runtime readiness
  without fresh receipts.

**Rosetta boundary:** [I] This route card governs public-site routing and source
preservation. It does not make `book-pwa/` a live production surface; the canonical
app at `02_SKYZAI/03_AIA/app/` is the live engine lane.
