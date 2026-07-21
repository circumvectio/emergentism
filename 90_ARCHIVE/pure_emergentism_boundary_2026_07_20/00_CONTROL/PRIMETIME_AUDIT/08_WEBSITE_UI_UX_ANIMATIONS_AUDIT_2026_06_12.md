# 08 — Website UI/UX/Animations Deep Audit

**Status:** Executed 2026-06-12 · non-destructive (read-only sweep + rendered verification; no site file modified)
**Scope:** `12_PUBLIC_SITE/` deploy surface (355 deployable pages, 9.5MB; `book-pwa/`, `docs/`, build scripts vercelignored)
**Method:** [S] three parallel scripted sweeps (link/asset integrity · animation/JS systems · UX/IA/a11y/SEO; scratch in `/tmp/site_audit*.py`, `/tmp/link_asset_audit_yb.py`) + rendered verification on localhost:4178 (Chromium: console capture, mobile 375×812 + desktop 1440 screenshots, DOM/overflow probes). Severity: P0 = breaks a core journey or errors on load · P1 = meaningful degradation (perf/battery/a11y/SEO) · P2 = polish/hygiene.

---

## Verdict

**The skeleton is ship-grade; the flagship is under-served.** Zero broken internal links across 11,623 checked on 353 pages; 349/349 sitemap URLs live; 100% image-alt, viewport, title, and description coverage; no console noise; no CDN dependencies; a single self-hosted three.js; devicePixelRatio capped everywhere. But: the **book** — the site's center of gravity — is missing from the persistent nav and the sitemap, and **side-scrolls 3.4× the viewport on phones**; one page (`five-plus-one/`) throws console errors on every load after downloading 1.27MB of three.js it cannot use; and the three WebGL lab pages ignore reduced-motion and burn GPU in background tabs.

## P0 — fix before DNS cutover

| # | Finding | Evidence | Fix |
|---|---|---|---|
| P0-1 | **`five-plus-one/` loads 1.27MB three.js and throws on every load.** `window.DIMENSION_PAGE={animationMode:"constitution"}` has no handler in `dimensions.js`; `boot()` grabs the page's `<svg class="dimension-canvas">` and hands it to `new THREE.WebGLRenderer` | Rendered-verified: repeated `THREE.WebGLRenderer: canvas.getContext is not a function` + `Dimension spine WebGL failed` from `dimensions.js:794` | Remove the `dimensions.js`+importmap includes from `five-plus-one/index.html` (the SVG is self-contained), or early-return guard for unknown `animationMode` in `boot()` |
| P0-2 | **Book absent from the persistent topbar** on ~348 corpus pages (`0–6 R S A Game Whole Read` — no Book). From any leaf page the flagship is reachable only via the ATLAS fab or going home | Rendered-verified on front door + shells (`trinity/04-bit-to-qubit/index.html:15-27` et al.) | Add `Book` to the shared topbar template; regenerate shells via `generate_public_library.py` |
| P0-3 | **`/book/` missing from `sitemap.xml`** (with `/axioms/`, `/game/`, `/synthesis/`) — sitemap (Jun 7) predates the book build (Jun 11) | 349 entries scanned; 0 ghosts, these 4 absent | Regenerate sitemap in `predeploy_check.py`; 4-line interim hand-edit |
| P0-4 | **Book side-scrolls on mobile:** 6 of 15 `<pre>` blocks force the whole document to 1265px on a 375px viewport — flagship reading is broken on phones | Rendered-verified probe: `{presOverflowing:6, pageHorizontalOverflow:true, docScrollW:1265, viewportW:375}` | Add `pre{overflow-x:auto}` to the `build_book.py` inline CSS template (book CSS styles `code` but has no `pre` rule) |

## P1 — degradations (perf · battery · a11y · SEO)

**Motion & WebGL (sphere.html / lightcone.html / cascade.html / soul-loop/ / dimensions.js):**
1. No `visibilitychange`/`document.hidden` pause on any of the 5 rAF loops (`sphere:184`, `lightcone:124`, `cascade:312`, `dimensions.js:838`, `soul-loop:298`) — bloom + autoRotate composite forever in background tabs.
2. `prefers-reduced-motion` respected only by `index.html`, `book/`, `dimensions.js`; **not** by sphere/lightcone/cascade/soul-loop (autoplay, no pause control except cascade).
3. Per-frame heap churn: `lightcone:137-138` disposes+recreates `ConeGeometry` every frame (+2 fresh `Float32Array`s); `cascade` rebuilds a ~6,200-vertex grid per frame while morphing. Animate via scale/position + preallocated buffers.
4. No mobile reduction anywhere: fixed segment counts (sphere 64×40, torus 104×30, starfields 700/340) + UnrealBloom multi-pass on phones. Gate on `matchMedia(max-width:760px)`.
5. Undebounced `resize` handlers on all WebGL pages (`setSize` + projection recompute per event).
6. Latent: `sphere.html:177` raycasts via `innerWidth/Height` instead of `getBoundingClientRect()` — breaks click-picking the moment the canvas is embedded non-fullbleed.

**Accessibility:**
7. No skip-to-content link on any of 355 pages (11–19 link topbars ahead of content).
8. Injected drawers (`atlas-drawer.js`, `book-ai.js`) are only `translateX`-ed off-screen — **focusable while closed on 348 pages**; no `aria-expanded`/`inert`.
9. Contrast: `--bone-faint #6b7280` on `#050505` = 4.22:1 (footer, tier notes, book-dark h3s); `dimensions.css --dim #6a6a6a` on `#000` = 3.88:1. Lift to ≥4.5:1.
10. `dimensions.css` (16 pages) has no `:focus-visible` style and no reduced-motion guard.
11. `infinite.html` core interactions are `span.onclick` — keyboard-dead — and its "Become an Infinite Reader" CTA is a dead button (payment never wired) while the page sits in sitemap+atlas. Mark prototype / disable CTA / noindex.

**SEO/GEO & IA:**
12. **Zero canonical, OG, Twitter, JSON-LD tags on all 355 pages**; four competing book surfaces (`/book/`, 688KB `/canon/the-reciprocal-public-edition/`, `app.html` (whose "Read the Book" goes to `/read/`), `infinite.html`) with no disambiguation → duplicate-content exposure exactly where the value is.
13. Meta descriptions are wing-level boilerplate: 61 unique across 353 pages (43× the same trinity blurb).
14. **21 pages link the private GitHub repo** (`github.com/Menexus-GmbH/magnum-opus/...`) as "Canon source" → public 404s + internal-path leakage.
15. Nav-generation drift: 6+ topbar shells; the 9-page 2026-06-06 generation brands "**Magnum Opus**" with brand-link to `/0/` (not home) and duplicates the `S` label (soul-loop vs suda-notes).
16. No 404 page (long-slug site → bare Vercel default, no way home).
17. `reading-manifest.json` (65KB) ships with zero deployed consumers — wire it or stop shipping it.
18. 108 internal `.html`-suffixed links (55 in `atlas/`, 27 in `sources/`) + `.html` sitemap entries → one 308 hop each under `cleanUrls`; www/apex unguarded by canonicals at cutover.

## P2 — polish (selected; full lists in agent receipts)

Favicon: no `favicon.ico` on disk + 33 pages with no icon link (incl. `sphere.html`) → guaranteed 404/visit; 317 pages ship the deliberate `data:,` blank. · `partials/` (12 self-broken links, no viewport) and `.DS_Store` deploy — 2 `.vercelignore` lines. · 11 duplicate-title pairs; 8 section indexes titled "… — Emergentism — Emergentism". · Orphans: `assets/css/spine.css` (superseded by inlined spine styles), `assets/css/source-note.css`, `assets/js/theme.js` (archive-first per K3). · 16 `drive.google.com` refs in `memetic/01–06` (rot/permission risk). · Tap targets 30–32px (AA-pass, 44px HIG-fail); mobile topbar scrolls with hidden scrollbar and no overflow affordance — book topbar visibly wraps/cuts off at 375px (screenshot). · Fabs overlap `ch-nav` at page bottom on mobile. · `.kvs-table`/`.rosetta-table` lack scroll wrappers. · `.library-article` measure ~95–100cpl (book's is ~65). · No font preload (FOUT). · `book-ai.js` injects the ✦ expand button *inside* each `h2` (pollutes accessible names). · Doubled `h1` on 308 generated pages; h2→h4 skips on 13. · No `webglcontextlost` handling. · `soul-loop` canvas `getContext` unguarded. · Count drift: front door "292 documents/sixteen wings" vs `read/` "276/thirteen". · "Enter the framework →" as the *exit* label on instrument pages. · `book-pwa/` (965.8MB, 98.2% of tree) still inside the deploy dir — one `.vercelignore` regression from disaster; removal is the signed AIA-migration follow-up, owner-gated.

## What is genuinely strong (keep)

0 broken links (11,623 checked) · 349/349 sitemap URLs live · 100% alt/viewport/title/description coverage · no `console.log`/debug/dead code in shipped JS · no CDN, one three.js copy, immutable cache headers on assets · DPR capped at 2 everywhere · front door is plain-HTML accessible with exemplary reduced-motion handling · the book's desktop reading UX (sticky scroll-spy TOC, themes persisted, ~65ch measure, deep-linkable headings, drop caps, `{passive:true}` scroll, reduced-motion) is the best surface on the site · `predeploy_check.py` guardrails already exist — sitemap regen, title/description lint, and topbar-consistency checks slot straight into it.

## Top 10 fixes by impact/effort

1. `pre{overflow-x:auto}` in `build_book.py` → kills the flagship's mobile side-scroll (P0-4, one line).
2. Sitemap: add `/book/ /axioms/ /game/ /synthesis/`; regenerate in predeploy (P0-3).
3. Topbar: add `Book`; regenerate the 348 shells (P0-2).
4. `five-plus-one/`: drop the dead three.js include (P0-1).
5. `visibilitychange` pause + reduced-motion branch across the 5 rAF loops (P1-1/2).
6. Drawer focus containment (`inert` + `aria-expanded`) in `atlas-drawer.js`/`book-ai.js` (P1-8).
7. Canonical+OG+JSON-LD block in the generators; canonical-banner the three non-canonical book editions (P1-12).
8. Branded `404.html` (P1-16).
9. Per-page meta descriptions + title de-dupe + skip-link in generator pass (P1-13/7, P2 titles).
10. Kill the 21 private-GitHub "Canon source" links (P1-14).

## Receipts

- Lane receipts: link/asset sweep, animation/JS audit, UX/IA/a11y/SEO audit (agent outputs, 2026-06-12; scripts `/tmp/site_audit.py`, `/tmp/link_asset_audit_yb.py` — regenerate on demand).
- Rendered: console capture of P0-1 (`THREE.WebGLRenderer: canvas.getContext is not a function` ×N at `dimensions.js:794`); mobile overflow probe (`docScrollW:1265 @ 375`); screenshots front door (desktop) + book (mobile, topbar wrap visible).
- Interactive dashboard artifact of these findings delivered to owner alongside this doc (bundle.html, web-artifacts flow).

*No site file was modified by this audit. All fixes above are recipes, not applied changes — application is a separate pass (generator edits regenerate 300+ pages; hand-patched tree discipline applies).*
