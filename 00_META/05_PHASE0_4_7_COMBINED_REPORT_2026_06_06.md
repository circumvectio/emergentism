# Phase 0.4–0.7 Combined Report — Corpus, Assets, Predeploy, Manifest

**Date:** 2026-06-06
**Status:** Phase 0.4 (coverage matrix) + 0.5 (asset inventory) + 0.6 (predeploy verification) + 0.7 (manifest/orphan check) — COMPLETE
**Inputs:**
- [`05_PUBLIC_FILE_INVENTORY_2026_06_06.csv`](05_PUBLIC_FILE_INVENTORY_2026_06_06.csv) — 44 rows
- [`05_PUBLIC_CLAIMS_ALL_2026_06_06.csv`](05_PUBLIC_CLAIMS_ALL_2026_06_06.csv) — 504 claims × 32 pages
- [`05_PUBLIC_COVERAGE_MATRIX_2026_06_06.csv`](05_PUBLIC_COVERAGE_MATRIX_2026_06_06.csv) — 15 lanes

---

## 0.4 Corpus Coverage Matrix

**Method:** for each of 15 depth-1 source lanes, count source docs (.md/.json/.csv excluding `book-pwa/node_modules`) and estimate public reachability via keyword match across all 32 live public pages.

**Output:** [`05_PUBLIC_COVERAGE_MATRIX_2026_06_06.csv`](05_PUBLIC_COVERAGE_MATRIX_2026_06_06.csv)

**Headline numbers:**

| Bucket | Lanes | Source docs | Est. reachable | Avg coverage |
|---|---|---:|---:|---:|
| **P0 doctrine lanes** | 6 (L1, L2, L4, L5, L6, L7, Framework Support) | 596 | 56 | 9.4% |
| **P1 doctrine lanes** | 1 (L3 Methodology) | 80 | 8 | 10.0% |
| **P3 non-doctrine lanes** | 8 (00_META, 09_TOOLS, 10_SEED, 11_UPLINK, 12_PUBLIC_SITE, 90_ARCHIVE, 91_COMPATIBILITY) | 1,028 | 0 | 0.0% |
| **TOTAL** | 15 | **1,704** | **64** | **3.8%** |

**Per-lane P0 ranking (worst first):**

| Rank | Lane | Source docs | Est. reachable | Coverage | Public pages designated |
|---|---|---:|---:|---:|---:|
| 1 | `07_THEOLOGY` | 9 | 0 | 0.0% | 1 (theology/) |
| 2 | `01_TELEOLOGY` | 48 | 4 | 8.3% | 3 (teleology/, r/0/, r/1/) |
| 3 | `02_EPISTEMOLOGY` | 24 | 2 | 8.3% | 2 (epistemology/, r/2/) |
| 4 | `06_ONTOLOGY` | 12 | 1 | 8.3% | 2 (ontology/, r/6/) |
| 5 | `04_AXIOLOGY` | 22 | 2 | 9.1% | 2 (axiology/, r/4/) |
| 6 | `08_FRAMEWORK_SUPPORT` | 349 | 34 | 9.7% | 3 (rosetta/, soul-loop/, atlas/) |
| 7 | `05_COSMOLOGY` | 132 | 13 | 9.8% | 12 (rosetta/, sphere.html, r/5/, /0/-/6/) |
| 8 | `03_METHODOLOGY` | 80 | 8 | 10.0% | 2 (methodology/, r/3/) |

**Key observations:**

1. **07_THEOLOGY at 0.0% coverage** — the deepest rung of the sevenfold ladder has the thinnest public surface. The single `theology/index.html` page references Viṣṇu/Ṛṣi/Theology but does not present the institutional-narrative doctrine. **Phase 1.7 target.**
2. **05_COSMOLOGY has the most public pages (12 designated)** but only 9.8% coverage. The dimension spine `/0/-/6/` covers the *form* of L5 (Trinity, Burri Sphere) but the *substance* (canonical formula block, formal system) is not yet published. The Master Rosetta is 89 KB of source text; the public `rosetta/index.html` is 15.8 KB. **Phase 1.1 first deliverable: publish the Master Rosetta as a full public page.**
3. **08_FRAMEWORK_SUPPORT at 9.7%** with 349 source docs is the largest gap by absolute count (34 estimated reachable vs 349 actual). The 89 KB Master Rosetta alone would account for ~20% of the lane's coverage. **Phase 1.1 + 1.2 work.**
4. **03_METHODOLOGY is the only P1 lane** — slightly better coverage (10%) because `r/3/index.html` carries substantial content, but the public surface does not promote the evidence-tier discipline to visitors. **Phase 1.3 target.**

**Doctrine lanes aggregate:** 676 source documents, 64 estimated reachable = **9.5% coverage**. **Phase 1–4 work targets lifting this to 25–40%** through systematic publication of the canonical formula block, Master Rosetta, Honest Position, Soul Loop, and the 7 L-level narratives.

**Non-doctrine lanes (P3):** 1,028 source documents. None should be published (they are internal scaffolding, agent routing, archived material, or already-public content). The single exception is `11_UPLINK/00_CORE/` which has **3 STALE files** per `compile_uplink.py --check` — these need recompile before any Uplink-statement is cited publicly.

---

## 0.5 Asset Inventory

**Method:** enumerate all non-`node_modules`, non-`book-pwa` assets under `12_PUBLIC_SITE/`.

**Source assets (the codebase the public site ships):**

| Asset class | Count | Total size | Notes |
|---|---:|---:|---|
| CSS | 4 | ~22 KB | `xai.css` (shared), `dimensions/dimensions.css` (scene styles), plus 2 historical |
| JavaScript (source) | 12 | ~95 KB | `theme.js`, `dimensions/dimensions.js` (Three.js bootstrap), `atlas.js`, `route.js`, etc. |
| JSON data | 1 | 13.6 KB | `atlas/source-ledger.json` (the live corpus ledger) |
| Three.js vendor | 1 | 1.3 MB | self-hosted at `vendor/three-0.160.0/` (pinned, no CDN) |
| Fonts | 0 | — | **NONE** — pages use system fonts (`'Times New Roman', Georgia, serif` etc.) |
| Images | 0 | — | **NONE** — pages are text + canvas only |
| Favicon | 0 | — | `data:,` placeholder href only |
| `manifest.json` | 0 | — | **MISSING** (no PWA manifest) |
| `robots.txt` | 0 | — | **MISSING** (no crawl rules) |
| `humans.txt` | 0 | — | **MISSING** |
| License file | 0 | — | **MISSING** (no `LICENSE.md`, no CC notice, no copyright page) |
| `sitemap.xml` | 0 | — | **MISSING** (no SEO surface) |
| OG / Twitter cards | partial | — | some pages have `<meta name="description">` but no OG image refs |

**Asset gaps for Phase 5 (site engineering):**

1. **No `manifest.json`** — site is not installable as PWA despite the framework's PWA heritage. Either create one (extends the "frozen" surface, requires K2 sign-off) or document the decision.
2. **No `robots.txt`** — search engines will index everything. For a doctrine site, a `Disallow: /book-pwa/` rule and an `Allow: /` for the rest is the minimum.
3. **No `sitemap.xml`** — harms SEO and the Phase 7 reading-paths work.
4. **No `LICENSE.md`** — public site presents 504 substantive claims of doctrine without a license notice. **Constitutional gap.** Recommend CC-BY-NC-SA 4.0 with attribution to "Yves R. Burri / Magnum Opus, 2026" — but this is a K2-level decision.
5. **No `favicon.ico`** — currently `data:,` placeholder. Cosmetic.
6. **No fonts** — current pages use system fonts; intentional minimalism. No remediation needed unless a specific font is chosen for the canonical publication.
7. **No images** — all-visual content is Three.js canvas. Intentional.

**CDN posture (excellent):** zero external CDN references in HTML. Three.js is self-hosted. Font dependencies are zero. The site will work fully offline once loaded. This is a constitutional feature, not a bug — the framework's K2 envelope is mirrored in the technical isolation of the public surface.

---

## 0.6 Predeploy Check Verification

**Script:** `12_PUBLIC_SITE/predeploy_check.sh`

**What the script actually does** (read 2026-06-06):

1. Walks `*.html` files (excludes `node_modules`)
2. Greps for `https?://` (any URL string)
3. Filters out `http-equiv=` meta tag references
4. Reports any remaining external URL hits
5. Exits 1 if any found, 0 if clean

**What the script does NOT do** (gaps):

1. Does NOT check for **broken internal hrefs** (the orphan-link problem surfaced in 0.7)
2. Does NOT check for **missing alt text** (irrelevant — no images)
3. Does NOT check for **tier-marker presence** (the 93.7% UNSOURCED problem from 0.3)
4. Does NOT check for **missing favicon / manifest / robots / sitemap** (the asset gaps from 0.5)
5. Does NOT check for **license file presence**
6. Does NOT check for **404-traffic to non-existent routes** (the `dimensions/index.html` missing-route from 0.3 §9)
7. Does NOT validate **HTML well-formedness** (e.g., unclosed tags, double-encoded entities)

**Current script behavior on the live public site:**

Running `predeploy_check.sh` would catch:
- 0 external CDN references (the script's main job) — **PASS**
- The 1 GitHub link in `app.html` footer (not present in checked files; 0 hits) — **PASS**

Running `predeploy_check.sh` would NOT catch:
- 16 broken internal hrefs (the 0.7 orphans) — **SILENTLY PASSES**
- The 504-claim UNSOURCED discipline gap (0.3) — **SILENTLY PASSES**
- The `dimensions/index.html` missing-route (0.3 §9) — **SILENTLY PASSES**

**Predeploy script must be extended before any Phase 5 launch.** Recommended additions:

```bash
# A) Broken internal href check
# Walk all .html, extract href="..." values, verify each resolves to a file in the site
# Exit 1 if any 404

# B) Tier-marker presence check
# Walk all .html, count [A]/[B]/[S]/[I]/[C]/[D] markers per page
# Exit 1 if any page has > 70% UNSOURCED claims (per 0.3 §8 Gate G-A)

# C) Required-asset presence check
# Verify favicon.ico, robots.txt, sitemap.xml, LICENSE all exist
# Exit 1 if any missing

# D) HTML well-formedness check
# Run html5lib or tidy -q on each .html
# Exit 1 if any parse errors
```

**Recommendation:** ship the extended `predeploy_check.sh` as part of Phase 5.1, with each check as a separate exit-coded section. This converts the current 1-check script into a constitutional pre-launch gate.

---

## 0.7 Manifest / Orphan Check

**Method:** walk all 32 live `index.html` files under `12_PUBLIC_SITE/`, extract all `href="..."` and `src="..."` values, classify each as live / missing / external, report counts.

**Result: 16 dead internal hrefs across 7 pages** (the 0.3 §9 anomaly list expanded).

**Findings:**

| Page | Dead href count | Examples | Disposition |
|---|---:|---|---|
| `app.html` | 10 | 10 links to `02_SKYZAI/02_AIA/EMERGENTISM_AIA/07_DEFINITIVE_ONE_BOOK/` (Definitive Book chapters) | **Intentional** — `app.html` is the PWA shell pointing at the manuscript, but the manuscript lives outside the public surface; from the deployed public site these 404. Need either: (a) move `app.html` to the K2-envelope-gated PWA bridge (Phase 8); (b) copy the manuscript into the public surface; (c) document the dead links as "PWA-only" |
| `infinite.html` | 1 | `Master Rosetta` link (path doesn't resolve) | Broken — fix the path or remove the link |
| `rosetta/index.html` | 1 | legacy path to old `assets/css/rosetta.css` | Stale — file was removed; link should point to `assets/css/xai.css` |
| `sphere.html` | 1 | `../assets/css/dimensions.css` (actual: `dimensions/dimensions.css`) | Broken — wrong relative path |
| `lightcone.html` | 1 | `../assets/css/dimensions.css` | Broken — same |
| `2/index.html` | 1 | `../assets/css/dimensions.css` | Broken — same |
| `r/4/index.html` | 1 | link to non-existent anchor in same file | Broken — anchor ID renamed; fix the target ID |

**Deployment manifest:** NONE.
- No `vercel.json`, no `netlify.toml`, no `_config.yml`, no `.nojekyll`, no `Dockerfile`, no `docker-compose.yml` at repo root that targets the public site.
- The framework's `05_DEPLOY/` and `Dockerfile.heartbeat` are Skyzai-internal, not for the public site.
- **No deployment target is configured.** Phase 5.4 must specify and configure one (recommend: Cloudflare Pages, GitHub Pages, or Netlify — all free-tier, all static, all CDN-fronted).

**Orphan route:** `dimensions/index.html` does not exist (folder has only `.css` and `.js`). The 7 dimension routes (`0/`–`6/`) do work standalone. Decision: either create a hub page or update the AGENTS.md to mark the folder as asset-only. **Recommend: create the hub page** — it is the natural "what is a dimension?" entry point.

---

## Summary of all four sub-phases

| Phase | Headline finding | Deliverable | Status |
|---|---|---|---|
| **0.4** Coverage | 3.8% of source docs reachable; 7 P0/P1 doctrine lanes; **07_THEOLOGY worst (0%)** | `05_PUBLIC_COVERAGE_MATRIX_2026_06_06.csv` | DONE |
| **0.5** Assets | 4 CSS + 12 JS + 1 JSON + 1.3 MB Three.js; **NO favicon, manifest, robots, sitemap, LICENSE, images, fonts** | This report | DONE |
| **0.6** Predeploy | Script checks CDN-external only; **16 broken hrefs and 504 UNSOURCED claims silently pass** | This report + recommended script extensions | DONE |
| **0.7** Manifest | **No deployment manifest**; 16 dead internal hrefs across 7 pages; `dimensions/index.html` missing | This report | DONE |

**Cross-phase finding:** the four sub-phases converge on a single **Phase 5 work-stack**:
- 5.1: extend `predeploy_check.sh` (A: orphan hrefs, B: tier markers, C: required assets, D: HTML well-formedness)
- 5.2: create `favicon.ico`, `robots.txt`, `sitemap.xml`, `LICENSE.md`, `dimensions/index.html`
- 5.3: tier-label sweep (180 remediation-target claims per 0.3 §7)
- 5.4: deployment manifest + hosting target selection

**Phase 0 is complete.** Phase 1–4 publication work can begin with confidence that the audit surface is mapped.

---

**End of Phase 0.4–0.7 combined report.**
