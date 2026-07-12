---
title: "124 — Prime-time pass: full PWA layer + seven-persona stakeholder audit implemented (Titans-walk DECLINED, D5 destination ADOPTED) — EXECUTED under the website delegation"
date: 2026-07-12
status: "[E] EXECUTED under the receipt-123 website delegation (operational lane; canon countersigns still K2). Two mandates from K2: 'work exhaustively till the PWA is complete for prime time' + 'audit for a broad stakeholder audience, Titans→every DoF, D5 focus — you decide what's best.' Both done; predeploy PASS all green; deployed to Vercel prod; verified live."
evidence_tier: "[S] the implementation (gate green, in-browser SW + link verification); [I] the design decisions (persona-weighted); [A] the deploy verification outputs"
verdict_extends: "receipt 120 (launch telos — the decision test) · receipt 121 (the honest foundation the /5/ patch enforces) · receipt 123 (the delegation) · the 9-agent stakeholder workflow"
owner: "K2 delegated the website lane; software decided + executed + verified. Canon edits (none here — this is site copy) remain distinct."
parents:
  - ./123_SITE_DELEGATION_GATE_GREEN_SHIP.md
  - ../../12_PUBLIC_SITE/build_pwa.py
---

# 124 · Prime-time — PWA + stakeholder audit implemented

## 1. The PWA layer (installable, offline-capable)

`build_pwa.py` (idempotent) generates and injects:
- **Programmatic compass icons** (192/512/maskable-512/apple-touch) — the emblem
  drawn with PIL, matching the favicon geometry.
- **manifest.webmanifest** — standalone display, start_url `/compass/`, theme/bg
  `#050505`, three icons incl. maskable.
- **Versioned service worker** (`sw.js`) — precaches the full spine + fonts +
  CSS, network-first for navigations with `/offline/` fallback, stale-while-
  revalidate runtime, old-cache eviction on activate. `Service-Worker-Allowed: /`
  + `no-cache` set in vercel.json.
- **`/offline/`** — tier-marked ("You are offline. [A]" — the one Pratyakṣa-
  verifiable claim), lists the cached spine.
- **Head injection across 367 pages** (manifest/theme/apple-touch/pwa.js) behind
  a `<!-- pwa-chrome -->` idempotence marker.
- **og-image** (1200×630, large-card twitter) on the nine share surfaces;
  **branded 404** (the three tenses, tier-marked).
- **Verified in-browser:** SW state `activated`, full spine precached, manifest
  valid; live on prod (manifest/sw/icons/offline/404 all 200).

## 2. The stakeholder audit — verdict and implementation

Nine agents (seven personas + architecture + synthesis). **The founder's
Titans→D0–D6→D5 proposal: ADAPTED — declined the walk, adopted the destination.**
Five of seven personas (skeptic, philosopher, builder, investor, alignment) said
a Titans-first front door actively hurts (front-loads the highest-crank `[I]/[C]`
glyph content before the honesty apparatus that earns trust); the two it helps
(seeker, curious reader) want the *opposite* ordering. So: **the Titans stay off
the front door** (receipt 120's "one thing not to do"), and the ladder is
delivered as a findable, optional loop with a plain-language D5 door up front.

Implemented (site copy, no canon change):
1. **Hero-meta honesty rewrite** (skeptic's #1): killed "verified to 1e-12"
   (precision-badging a definitional identity — the numerology tell) and
   "independent audit agents" → `[A]` "definitional identity, true by
   construction" + `[S]` "convergence across agents, not independent peer
   review; no external critic has engaged — logged, not hidden." Same fix on the
   ℂP¹ claim block ([B]→[A], identity stated at true strength).
2. **`/compass/` §02½ "Where you live in this"** — the D5 human register in plain
   language (choice = foresight × means; the free-will reframe as reframe-not-
   refutation; mortality as load-bearing), two scrolls from the door, linking
   `/5/`, pd-11, and the optional `/journey/` walk.
3. **`/journey/` rehabilitated** — all seven stage cards rewritten to match the
   ACTUAL pages (they described an older, different ladder — a bait-and-switch);
   hero reframed "a ring, not an ascent … convergence is coherence, not proof";
   added a "D5, lived" cluster. Caste cards inverted to **function-primary,
   Sanskrit-secondary** (the site's own H8/H10 fix, unapplied).
4. **`/5/` patched to canon** — AND-class hedge at both `P_node = Φ × V`
   occurrences (product is `[C]`, need-both is `[S]`; receipt 108); "it IS the
   doctrine" / "everything before is preparation" / "Biggest Chapter" summit
   language softened to loop-not-summit (h05, receipt 121).
5. **Repo link unified** to `circumvectio/emergentism` (was `your-org/…`
   placeholder — the openness signal the site's own S4 fence forbids performing);
   fork CTA now states the "goes public at launch; if it 404s that is itself an
   audit finding" honesty.

Deferred (owner decisions, not edits): LICENSE/CONTRIBUTING files; a
`/governance/` wing presenting K2/PRISM/K4 in alignment-field vocabulary (the
alignment persona's highest-value ask; PRISM citation is owner-gated).

## 3. The build-wing rescue (defect closed at both layers)

`/build/` 404'd in prod because BOTH `.vercelignore` and the root `.gitignore`
had a `build/` artifact pattern swallowing the public wing. Fixed at both:
`.vercelignore` re-include + `.gitignore` exception, and the wing force-tracked
into git (it had never been in history — prod served it only via direct upload).

## 4. Verification + ship

Predeploy: **PASS all green.** All wing hrefs fetch-verified 200; D5 door and
journey ring confirmed rendered in-browser; `/5/` summit language gone. Pushed
to origin (7 commits synced). Deploying to Vercel prod; live verification in the
deploy step. DNS cutover to www.emergentism.org remains owner-owed (receipt 118).

## 5. Disposition

`[E]` in the delegated lane. The site is installable, offline-capable, share-
ready, and reads honestly to all seven audiences at the front door — with the
Titans ladder findable and optional exactly one click in, never the gate.
