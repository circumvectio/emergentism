---
date: 2026-07-04
status: "[D] audit report — verified findings (81 total, every one re-checked; refuted claims dropped). Fixes NOT applied; deploy remains gated."
method: "10 first-principles lenses (purpose/honesty/IA/interactive/math/a11y/perf/security/SEO/code) + adversarial verify pass on all material findings."
companion: "../../11_UPLINK/50_AUDITS_AND_EXECUTIONS/103_FORMAL_LOGIC_AUDIT_K2_PACKET_2026_07_04.md — the corpus-side formal-logic audit of the same day."
---

# Emergentism Public Site — First-Principles Audit Report

**Target:** `/Users/Yves/Documents/01_EMERGENTISM/12_PUBLIC_SITE` · static HTML5 · ~356 real routes (+5 standalones; the oft-quoted 710 double-counts an untracked `.vercel/output/static` build mirror) · production entry: `/` 307→ `/amrita/`
**Method:** every finding below was independently re-verified against the tree; refuted claims dropped, adjusted claims re-scoped. All paths relative to the site root.

---

## 1. Verdict

The site exists to convert a skeptic through demonstrated honesty: one [A]-proven result (φ·ν=1 as conjugacy on S²), made felt, wrapped in a tier ladder that shows its own cuts. The bespoke core — `/amrita/`, the runaway scene, the math, the network-level η=0 — genuinely delivers this, at times exceptionally. But the site as deployed fails its own test in one repeating way: **the verification affordances are theater.** Every "source →" on the honest ladder is a decoy link; all 78 "Canon source" receipts in the library 404; the frozen ~308-page library still asserts, as Theorem/QED/"conservation law", the exact claims the front door publicly cut. The skeptic the site is designed for is precisely the reader who clicks the receipt — and every receipt breaks. The single biggest first-principles issue is that the site's honesty is *asserted at the front door and unenforced everywhere behind it*, with no pipeline (the generator is dead, the predeploy gate is blind and optional) capable of keeping the two in agreement.

## 2. The site by its own standard

The standard is the site's own: tier-honesty, "every claim above [I] links home", cuts stay visibly cut. Scored against it:

- **The bespoke spine passes, impressively.** The amrita caption demotes its own hero equation's strongest reading ("It does not by itself prove the equator is anyone's optimum; that is [S] and conditional"). The cut squid claim exists only struck-through with its refutation; a site-wide grep finds no live assertion of it. "TOE" is disclaimed everywhere it appears. Failed predictions are left standing and scored (`axioms/index.html:241`). The runaway math is correct to machine precision and ships its own falsifier (`sphere.html` renders live |φν−1|).
- **The receipts fail, universally.** Not one "source →" or "Canon source" link on the entire site actually reaches its cited source. The claim "every claim links home" is currently false at 100% of the places it can be tested by click.
- **The frozen library contradicts the cuts.** h11 cuts "N=3 uniquely stable" to "conjecture at best"; the library renders the same source doc as "[S] … Formal proof … QED." h01 names "φ·ν=1 as a conserved invariant" the poison found "in every single lane"; at least 8 shipped routes commit exactly that framing, unfenced — one (`formal/20`) even calls the tautology *violable*.
- **The meta-claim overclaims.** `index.html:418`: "Every claim on this site wears an evidence tier." Checkably false (`trinity/02:76`, `operators/mf-69:241` — untiered categorical assertions). By the site's own rule, this universal is itself an overclaim above evidence.

**Conclusion:** the ethos is real and lived where hands touched the page recently; it is contradicted where the dead generator's output ships unreviewed. The site is honest at its core and dishonest at its edges — and the edges are ~87% of the surface.

## 3. Findings, ranked

### CRITICAL — the site contradicts its own honesty thesis at load-bearing points

**C1. The honest ladder's "source →" links are decoys — all 32 drops link to a generic index**
`amrita/index.html:98` · Every drop renders `<a class="src" href="../read/" title="${d.source}">source &rarr;</a>` — the citation lives only in a hover tooltip; the click lands on the generic `/read/` index, which surfaces **zero** of the 25 cited documents. Verified scope: 17/32 drops cite docs that DO have rendered site routes (e.g. `foundations/the-honest-position/`, `will/00-the-core-conjecture/`) — direct links existed and were not used; the other 15/32 — including **both flagship [A] conjugacy drops (n01, n04)**, the balance-conditional keystone (n12), and 7 of 11 halāhala cuts — cite docs with no rendered route anywhere.
*Why:* this is the exact click where the conversion thesis is tested. The skeptic checks the receipt on the one proven thing and finds it goes nowhere — which teaches them the tier badges may also be decorative. Worse than a missing page: it's a verification affordance that pretends.
*Fix:* emit real hrefs for the 17 with routes today; for the 15 without, render visible text "source in the corpus — not yet published" instead of a link. Make `validate_amrita_json.py` require a `route` field or an explicit `unpublished: true`.

**C2. All 78 "Canon source" receipts across 24 library pages 404 — and leak private 02_SKYZAI paths**
`complete-ontology/index.html:382` · Links to `github.com/Menexus-GmbH/magnum-opus/blob/main/...` — verified live: the GitHub repo returns 404, so 100% of the library's tier-honesty receipts (`[A/S/I/C] · K2-ratified · Canon source: →`) are dead for every visitor. `trinity/13:309`, `trinity/28:145`, plus `formal/35/36/37` (~15 more hrefs) expose full internal `02_SKYZAI/...` paths — the confidential lane, including P-SCORES and sprint-history filenames.
*Why:* the library's provenance chain is broken wholesale, and the broken links double as free intelligence about the private corpus tree. If the repo were ever pushed to "fix" the links, it would expose the confidential lane itself.
*Fix:* rewrite to on-site `/sources/` entries or visible non-link path text; strip every `02_SKYZAI/*` reference from public HTML. Patch `generate_public_library.py`'s `GITHUB_ROOT` (line 370) too, or regeneration reintroduces them.

**C3. The library ships "N=3 is uniquely stable" as [S] proof/QED — the claim the front door cuts to "conjecture at best"**
`formal/11-efr-triadic-stability/index.html:60-62,194` · "Status: Formal proof … Evidence Tier: [S] Structural — mathematical proof" ending "N = 3 is the unique stable configuration. QED." — a render of the *same canonical source* that `amrita/amrita.json` h11 marks halāhala ("Stated as flat proof with no tier … Conjecture at best"). `trinity/02:76` and `trinity/09:237` assert the untiered "Triadic Stability Theorem (MF-511)" that "proves" uniqueness. Compounding: the page glosses [S] as "mathematical proof", abusing the tier definition itself.
*Why:* the front door confesses the poison; one click deeper, the site serves it. This is the seam the whole /amrita/ design exists to eliminate, failing on its most-scrutinized example.
*Fix:* hand-patch (generator is dead): demote formal/11 to [C] with the kill-criterion framing, tier and caveat the two trinity assertions, and banner all three to the h11 cut so the contradiction is visible, not silent.

**C4. φ·ν=1 laundered as a "conservation law" on ≥8 shipped routes — h01's named poison, verbatim**
`formal/16-efr-transcendentals/index.html:125` · "P∞ = φ·ν = 1 is conserved everywhere … the framework's formal analogue of truth"; `formal/20` §4.2 treats the tautology as *violable* ("would violate φ·ν = 1" — nothing can violate ν:=1/φ); `formal/15:291` and `formal/18:234` derive it from zero as "the simplest conservation law"; `formal/17`, `formal/29`, `trinity/32` repeat the framing; `formal/29` even contradicts `formal/16` on the domain (poles excluded vs "everywhere"). Zero fencing language on any of these pages — while `formal/26:88`, `will/00`, and the book carry the correct fence, proving the corpus knows better.
*Why:* h01 says this framing "appeared as poison in every single lane." Shipped canon commits it unfenced. `formal/20` is the worst case — it gives a coordinate identity dynamical content, which is precisely the tautology-laundering the seven-operator audit identified as the framework's genuine rot.
*Fix:* import `formal/26:88`'s fence sentence onto each offending page; rewrite formal/20 §4.2's "violation" as a statement about the η=0 game rule, not the identity.

**C5. The metrology page asserts false math: B = 2φν/(φ²+ν²) ≠ sin θ, and a diagnostic that measures the wrong thing**
`formal/30-operational-definitions/index.html:134,142` · The "on-manifold identity" contradicts itself on its own line: with (φ,ν)=(2,0.5) — exactly on-manifold — the formula gives 0.471 vs sin θ = 0.8. Algebraically it equals sin θ only at the equator. The line-142 "manifold deviation" diagnostic |B̂_free−B̂| therefore reports large deviation (≈0.33) for perfectly reciprocal but imbalanced systems — it tracks distance from the *equator*, not the manifold.
*Why:* this is the page defining the meters the doctrine cites, in the identity family of the site's one proven thing, and the error is checkable with a calculator in five minutes by exactly the hostile reader the site courts.
*Fix:* correct form is B = 2/(φ+ν) (or GM/AM: 2√(Φ̂ν̂)/(Φ̂+ν̂) for free meters); a real manifold-deviation diagnostic is |Φ̂·ν̂ − 1| — which `sphere.html:394` already computes live.

### HIGH

**H1. The '/'→'/amrita/' redirect severs the designed journey; the hub is unreachable and amrita's brand link self-loops**
`vercel.json:10` + `amrita/index.html:15` · With `cleanUrls:true`, `/index.html` 308s→`/` 307s→`/amrita/`: the 42KB landing hub — sole carrier of the tier legend, the five refusals, the honesty band, the library map, the book CTA, and the only curated bridge *into* amrita — is served to no one at any URL. amrita's brand link (`href="../"`) bounces straight back to the page you're on. BFS confirms exactly `index.html`, `ontology/`, `theology/` become unreachable (all three still in the sitemap as ghosts). Nuance: amrita's number-nav does reach the 0–6 spine, so it is not a total dead end — but the journey's designed second act is gone.
*Fix:* give the hub a stable route (`/home/` or fold its orientation content into amrita screen 4); point the brand link somewhere real; re-root `predeploy_check.py`'s orphan logic at `/amrita/` and make bespoke-page orphaning an error (line 147 currently: `return True  # Orphans are warnings, not errors`).

**H2. Homepage inversion for crawlers: the indexed homepage is a 152-word JS shell**
`vercel.json` + `amrita/index.html:90` · The entire Screen-3 honesty ladder — the site's core honesty artifact, including the struck-through squid cut — is client-rendered from `fetch("amrita.json")` with zero `<noscript>`. Non-JS crawlers (GPTBot, ClaudeBot, link-preview bots) index a near-empty page; `sitemap.xml:93` still lists the redirecting `/`. (Googlebot itself likely renders eventually — the harm is concentrated in AI/preview crawlers, which for this site matter more.)
*Fix:* render the 32 drop titles + tiers as static HTML and let JS enhance; drop `/` from the sitemap.

**H3. ~87% of the surface is a frozen, un-regeneratable projection with a live re-inflation hazard**
`generate_public_library.py:26-30,874` · The generator's own docstring: source bundle absent, "CANNOT regenerate", ~308 wing pages are "FROZEN ARTIFACTS" maintained by ~15 documented hand-patches to generated HTML. If anyone restores the bundle and re-runs it, `main()` regenerates unconditionally and silently overwrites every tier-honesty correction — re-inflating the exact overclaims the framework cut. Meanwhile the [A]-proven core lives in ~4KB of `amrita.json` plus one caption.
*Fix:* decide the library's status: (a) restore bundle + back-port all patches + make regeneration the only write path, or (b) declare it a frozen archive — banner it, neuter the generator, de-emphasize in nav. Either, explicitly.

**H4. No Content-Security-Policy on a site that solicits and stores reader LLM API keys in localStorage**
`vercel.json:12-33` + `assets/js/book-ai.js:15,125,137,143,212` · Headers lack CSP and HSTS; `buildCommand: null` means the predeploy gate never runs at deploy. Reader API keys ("sk-…") sit in origin-readable localStorage on 6 pages; 18 pages carry inline `<script>`; the gate's external-ref check is blind to JS-level fetch. Not an active XSS (no URL-derived input reaches a sink) — but a single bad edit to any of ~355 frozen hand-patched pages could exfiltrate keys, and nothing in the headers would stop it.
*Fix:* add CSP with a `connect-src` allowlist (preserves BYOK) + explicit HSTS; wire `predeploy_check.py` into the deploy. Bonus: CSP makes the site's "we phone no one" claim *browser-enforced* — machine-checkable honesty, exactly the site's brand.

**H5. The flagship interaction is pointer-only — keyboard/AT users are locked out of the one proven thing, and the aria-label promises what they cannot do**
`amrita/runaway.mjs:102-104` + `amrita/index.html:36,38-43` · Only pointerdown/move/up; no tabindex, no keydown, no aria-live anywhere in `amrita/`. The canvas's accessible name instructs "drag vertically" — unexecutable for its AT audience. WCAG 2.1.1 Level A failure on the production entry's primary content. The sting: `dimensions/dimensions.js:568,577` already does this right.
*Fix:* `tabindex="0"` + role=slider + arrow-key handler into the existing θ setter; debounced `aria-live="polite"` on the readouts; rewrite the label.

**H6. 1-year `immutable` cache on unversioned, still-mutating assets**
`vercel.json:35-51` · `max-age=31536000, immutable` on `/assets/` and `/vendor/`, while 348 pages reference `xai.css` and `atlas-drawer.js` bare (no fingerprint). Git history: the immutable header shipped 2026-06-08; `xai.css` was then edited in ~14 further commits through 06-15 — it mutated repeatedly under a never-revalidate policy. The `?v=` technique exists in-tree (`sphere.html:112`) but not on the two highest-fanout assets. (HTML itself is outside the rule, so content corrections do reach visitors; what pins for a year is the design system and drawer/book-ai code.)
*Fix:* add `?v=` to xai.css/atlas-drawer.js/book-ai.js references, or relax `/assets/` to `max-age=3600, stale-while-revalidate` and reserve `immutable` for `/vendor/` + fonts.

**H7. The front door eagerly downloads the unminified 1.27 MB three.module.js for a below-the-fold scene, over a serial 3-hop waterfall**
`amrita/index.html:78-87` + `amrita/runaway.mjs:52` · `mountRunaway()` runs unconditionally at load; the dynamic import (1,272,972 B raw / 257,967 B gz — the *dev* build, 53k lines) is gated only on WebGL, never visibility; no modulepreload, so HTML→runaway.mjs→three.js is serial. Three.js is ~91% of front-door transfer; everything else totals ~25 KB gz. The fallback proves the page works without it.
*Fix:* three one-liners — vendor the minified build; mount via IntersectionObserver on `#feel`; add `<link rel="modulepreload">` if eager load is kept.

**H8. Zero social/share metadata on all 359 pages**
`amrita/index.html:6-10` · No og:*, no twitter:*, no og:image anywhere. A niche worldview site acquires skeptics almost exclusively via shared links on X/HN/Discord; every share currently unfurls image-less and low-salience (X renders no card at all).
*Fix:* add OG/Twitter tags to the bespoke surfaces first; script-inject derived tags across the frozen pages (consistent with the hand-patch maintenance mode).

**H9. 306 generated pages share just 16 meta descriptions**
`generate_public_library.py:377-461,774` · Each wing's hardcoded blurb is passed verbatim to every leaf (trinity blurb on exactly 42 pages, formal 38, operators 30, papers 25); all submitted in the sitemap, no noindex. 85% of indexable inventory is one of 16 blurbs — search engines read it as machine-spun near-duplicate inventory, which (per the generator's frozen state) it is.
*Fix:* one-off script deriving each leaf's description from its own lede; wing blurb stays on the wing index only.

### MEDIUM

- **No rel=canonical anywhere; twin routes both in sitemap** — `foundations/the-ring-that-is-the-ground/` vs `ground/00-.../` (0.93 body similarity, distinct md5s, both in sitemap). *Adjusted down from High:* only 2 of the 11 twin-title pairs are genuine near-dupes (the ring pair + `canon/the-logarithmic-realignment` vs `formal/40` at 0.936); the rest share only a `<title>`. Fix: pick canonicals for the 2 real dupes; add self-referential canonicals sitewide; de-dupe titles.
- **The WebGL fallback asserts a falsehood: "the numbers still move"** — `amrita/index.html:37` + `runaway.mjs:45-50`: in fallback mode `paint()` runs once and *no input is wired*; the numbers can never move. A literal false statement about the page's own behavior, on the honesty flagship, in the degraded mode privacy-hardened skeptics are most likely to hit. Fix: wire a `<input type="range">` in fallback (also solves half of H5), or change the copy to the true statement.
- **Three.js import/renderer failure → dead blank canvas** — `runaway.mjs:52` runs after the WebGL probe; `index.html:87` only `console.error`s. A 404/parse failure leaves a visible inert canvas captioned "Drag toward a pole", fallback never activates. Fix: extract a `degrade()` helper, call from both probe branch and catch.
- **Landing's universal meta-claim is false** — `index.html:418` "Every claim on this site wears an evidence tier" vs untiered assertions at `trinity/02:76`, `mf-69:241`. Scope it honestly ("where you find one that doesn't, that's a bug — report it") or make it true.
- **mf-69 reasserts the CUT torus claim in title and closing** — `operators/mf-69-horned-torus-relativity/index.html:34,241`: "The Horned Torus IS the Light Cone … It fell out of the topology" — directly contradicting its own body ("topological but not metric", line 193's [I] disclaimer) and h07's cut. Skimmers read the title and THE SENTENCE, not the hedged middle. Retitle + tier or delete the flourish.
- **formal/13's false equivalence feeds the moral classifier** — line 186 claims GM/AM ≡ min/max; they differ 2.6× at θ=60° (0.866 vs 0.333), and min/max reproduces C5's wrong formula — the same chart conflation twice. This meter drives the ΣΔB sacrifice-classification test. Delete or restate as a distinct proxy.
- **formal/14 asserts unity-product as an empirical stability condition** — line 274 "Φ_knowledge × ν_knowledge = 1", untiered, breaking the uppercase/lowercase fence `formal/00:83` calls load-bearing, and asserting the "unwon wager" h02 confesses. Downgrade to [C]/[I] or switch to the lowercase chart with the fence.
- **r/5 headline caption is sign-garbled** — `r/5/index.html:62`: "φ·ν = 1 on S² — the equator is the unique global minimum": a constant has no extremum, and the site's own Theorem 2.2 proves the equator is B's *maximum*. First math a visitor reads on that instrument. One-line fix.
- **sitemap.xml is frozen and drifted; the flagship book is invisible** — 7 live routes missing (`/book/` — the 639KB whole-book reader — plus `/axioms/`, `/game/`, `/synthesis/`, 3 post-freeze docs); 6 redirecting URLs listed; 0 lastmod; and `/amrita/` has no link to `/book/` anywhere. The highest-conversion artifact after the [A] result is unreachable from the front door and undiscoverable by search, while the paywall stub *is* indexed. Fix: standalone sitemap script (mirror `build_atlas_index.py`); add /book/ to amrita's Go-deeper cards.
- **A "payment not wired" paywall prototype ships and is sitemap-indexed** — `infinite.html:132-133` + `sitemap.xml:94`: a dead "Become an Infinite Reader" button on a zero-extraction-ethos site, one search result away. Its inline `onclick=` handlers also obstruct a strict CSP. Remove from deploy/sitemap until real.
- **app.html is a third competing ladder, self-described as "accretion", still indexed** — `app.html:6,153`. Five overlapping "read the framework" entries split the skeptic's first hour. Archive it (K3) or 301 to /amrita/.
- **Atlas drawer omits 84 of ~355 routes** — `atlas/site_index.json` (stale, 2026-06-15): the ENTIRE trinity/ (43) and foundations/ (13) wings, the /r/ spine, and `/amrita/` itself are invisible to the site's only global search. Rerun `build_atlas_index.py`; add a coverage assertion to the gate.
- **Navigation chrome is forked** — 13 routes carry an older topbar where "R" goes to `/r/0/` instead of `/rosetta/` (`dasein/index.html:110`); `suda-notes/index.html` leaks the internal brand in its title: "— Magnum Opus". Converge on one topbar contract; fix the title.
- **Title-doubling bug live on 13–15 wing hub pages** — `papers/index.html`: `<title>The Papers — Emergentism — Emergentism</title>` — on the most-linked, most-crawled hub pages; the generator's docstring predicts this exact bug. Hand-patch + add a zero-hits regex check to the gate.
- **~14 personal Google Drive links published as citations** — `memetic/05-.../index.html:238,244-245`: either de-facto-public private drafts (plus owner-account disclosure) or dead receipts — both branches fail. Audit sharing, replace with `/sources/` copies.
- **Internal build partials ship to production** — `partials/topbar.html` (with developer commentary) confirmed in the real Vercel output; also an orphaned template whose root-relative links are the site's only 11 unresolvable hrefs — a trap for whoever "fixes" the topbar fork with it. Add `partials/` to `.vercelignore`; fix or delete the partial.
- **Publication boundary holds by extension-glob coincidence** — `.vercelignore` has no `_PLANS/`, `partials/`, `.vercel/` entries; `_PLANS/` (internal strategy docs) stays private only because everything in it happens to be `.md`. One non-.md export and strategy ships with a green gate. Invert to a top-level allowlist in `check_publication_boundary()`.
- **The runaway scene ignores prefers-reduced-motion, spins forever, and renders at a looser pixel cap than its own siblings** — `runaway.mjs:107` unconditional rAF loop, no pause, no media query (WCAG 2.2.2), pixel cap 2 vs the house 1.2/1.45; `cascade.html:116`, `sphere.html:121`, `lightcone.html:92`, `dimensions.js:14` and the landing all honor it — the newest, most-trafficked surface shipped below the house standard. Also add the missing `@media (prefers-reduced-motion)` block to `xai.css` (its unconditional `scroll-behavior:smooth` affects all ~340 pages).
- **No skip-to-content link on any route** — every page fronts 11–13 topbar links + the injected Atlas button; keyboard users pay the full toll on every hop of a multi-page reading journey (WCAG 2.4.1). One CSS class + scriptable injection.
- **Every generated page has two identical h1s** — `papers/index.html:34,58` pattern across ~313 pages: doubled page title in every screen-reader outline. Scriptable demotion of the hero heading; back-port to the generator template.
- **Cache policy inverted + version-stamp drift** — the one consistently version-stamped asset (`dimensions/dimensions.js`, 101KB, loaded on the whole number spine) sits *outside* every cache rule, and its `?v=` stamps disagree across live pages (instrument-19 vs instrument-21). Add a `/dimensions/` header block; have the gate assert one stamp per asset.
- **The scene's test guards the wrong invariant, and nothing runs it** — `runaway.test.mjs` asserts limits but never φ·ν=1, B=2/(φ+ν), γ·B=1, or B≤1 (all verified true to 2.2e-16 — the code is right, the armor is thin); `predeploy_check.py` never invokes it. ~10 test lines + one gate check.

### LOW

- **[I]-tier drop invisible to the tier UI** — `amrita/index.html:53-56` offers only All/[A]/[S]/halāhala; n15 ([I]) belongs to no filter, and filtering gives AT users no feedback (no live region). On the tier-transparency showcase, the displayed taxonomy silently under-represents the data. Add an [I] button + an aria-live count.
- **Temporary 307 for a settled front door** — `vercel.json:10` `"permanent": false` tells crawlers to keep `/` canonical, contradicting the entry decision. Flip to 308 once settled; drop `/` from the sitemap either way.
- **No JSON-LD anywhere** — the book, 26 papers, and breadcrumb hierarchy are all schema-eligible; structured data is the machine-readable analogue of the tier ethos.
- **Blank favicon on the actual homepage** — `amrita/index.html`: `href="data:,"`; the branded circle-dot SVG exists only on the unreachable landing. Copy it over.
- **Shipped manifests disclose private-repo structure** — `amrita/amrita.json` tooltips + `atlas/source-ledger.json` publish internal lane names (`11_UPLINK/50_AUDITS...`). Decide per path: publish the target or replace the path with a public identifier.
- **The predeploy gate's asset model has drifted** — `predeploy_check.py:149` requires `theme.js` (referenced by zero pages) while never existence-checking `src=` scripts or the two runtime fetch endpoints; a renamed `atlas-drawer.js` ships green and breaks 348 pages. Also: `check_external_refs()` is blind to CSS `@import`/`url()` and JS fetch literals, and never runs at deploy (`buildCommand: null`).
- **~48 KB of vendored three.js addons referenced by zero pages** — `vendor/three-0.160.0/postprocessing/` + `shaders/` ship behind a 1-year immutable header. Delete or ignore.
- **runaway.mjs robustness nits** — no `pointercancel` (interrupted touches can stick `dragging=true`); `dispose()` leaks the resize/pointer listeners and geometries; `sphereState` has no domain guard and its two poles disagree (θ=0 → ∞, θ=π → 1.6e16) — masked only by the UI clamp on a function exported as the canonical [A] artifact.
- **Bare-glyph number nav has no accessible names** — `<a href="../0/">0</a>` … "R","S","A": private iconography that costs exactly the newcomer; add aria-labels (byte-identical chrome, scriptable).
- **Atlas drawer dialog semantics half-finished** — `assets/js/atlas-drawer.js`: no aria-expanded, focus stranded in a hidden panel on close; the correct pattern exists 30 lines away in `dimensions.js`. ~10 lines fixes all ~341 pages.
- **639 KB book monolith lays out ~99k words up front** — `book/index.html` has zero `content-visibility`; add `content-visibility:auto` on chapter wrappers in `build_book.py`.

## 4. What is genuinely good

- **The amrita front door lives the ethos at maximum temptation.** It demotes its own hero equation's strongest reading in the caption, publishes retractions in a dedicated poison column, and keeps the cut squid claim struck-through with its refutation. The squid is genuinely dead site-wide; "TOE" is disclaimed everywhere; failed predictions are left standing and scored. This *is* the product, and where hands touched it recently, it works.
- **The [A]-core mathematics is exactly right and machine-verified.** `runaway.mjs` implements the conjugacy correctly (independently swept: |φν−1|, |B−2/(φ+ν)|, |γB−1| all ≤2.2e-16); the light-cone mapping is exact with γ literally coinciding with Lorentz γ; `sphere.html` renders the live falsifier |φν−1| with its tier stamped into the instrument.
- **η=0 is real at the packet level.** Zero external requests of any kind across all routes — no fonts, no CDNs, no trackers, no cookies; the BYOK AI design keeps keys off the site's infrastructure and says so plainly. This survives adversarial inspection in DevTools, which per the site's own theory of conversion *is* the argument.
- **Zero broken internal links across 359 pages**, and the one proven thing is 0 clicks from the production entry with its mathematical grounding ≤2 clicks away.
- **Ascetic performance fundamentals**: no images at all, self-hosted subset fonts with preload, big payloads fetched only on user intent, three.js quarantined to 13 instrument surfaces; a median doctrine page costs ~25 KB gz cold.
- **The a11y failures are regression, not ignorance**: `dimensions.js` ships pause buttons, aria-live, labeled sliders; `xai.css` has global focus-visible and contrast/transparency queries. Every defect above has a correct in-house implementation to copy.
- **The engineering is clean**: genuine unmodified three.js r160, well-formed HTML even at 639 KB monolith scale, a Node-testable pure-function extraction of the core identity, and a real (if buggy) degradation path.

## 5. Prioritised recommendations

**Fix first (in order — all are hand-patches or single-file edits consistent with the current maintenance mode):**
1. **Make the receipts real** (C1, C2): wire the 17 available deep links in the amrita ladder; label the 15 unpublished sources honestly; replace/strip all 78 dead GitHub links and every `02_SKYZAI` path. This is the single highest-leverage fix — it repairs the exact click where the thesis fails.
2. **Back-port the cuts into the frozen HTML** (C3, C4, mf-69, formal/13/14, r/5): demote formal/11, fence the 8 conservation-law pages with formal/26's sentence, retitle mf-69, fix the four math slips. The same hand that cut the squid should finish the job.
3. **Fix the false identity on formal/30** (C5) — five minutes of algebra is currently refutable by a hostile reader.
4. **Repair the entry architecture** (H1, H2): give the hub a route, fix the brand self-loop, static-render the ladder, link `/book/` from amrita, flip 307→308, regenerate the sitemap via a standalone script.
5. **Harden the machine layer** (H4, H6, H5): CSP + HSTS, version the shared assets, keyboard path + aria-live on the runaway scene (fixes the fallback falsehood too).
6. **Arm the gate**: run `predeploy_check.py` at deploy (`buildCommand`), promote orphans to errors rooted at `/amrita/`, add checks for sitemap-vs-tree, `src=` existence, doubled titles, version-stamp consistency, and `node amrita/runaway.test.mjs` (with the identity sweep added).
7. **Decide the library's fate explicitly** (H3): restore-and-backport, or banner-as-frozen-and-neuter. The current state — dead pipeline, armed generator, hand-patched output — is a standing self-contradiction machine.

**Cut (archive-first, per K3):**
- `infinite.html` from deploy and sitemap until payment is real; `app.html` (301 → /amrita/); `partials/` from the deploy; the unused three.js `postprocessing/`+`shaders/`; the ~14 Drive citation links (replace with `/sources/` copies); `theme.js` from the gate's required list.

**Leave alone (and protect through any refactor):**
- The amrita copy discipline, the runaway math and its touch engineering (touch-action/pointer-capture/clamp/dynamic-import), the zero-external-request posture, the self-hosted font pipeline, the on-intent data loading, the tier-hedged meta descriptions on the instruments, and the visible failure records on `/axioms/`. These are the site's actual product. Every fix above should treat them as the standard the rest of the site is brought up to — not the other way around.

---

*Bottom line: the core is honest and the periphery isn't, and the site currently routes every skeptic through the periphery's broken receipts. Fix the receipts and back-port the cuts, and the site becomes what it claims to be; leave them, and the honesty pitch is refutable by a single click on "source →".*
