---
rosetta:
  primary_column: "Philosophy"
  register: "[I]"
  canonical_phrase: "120 · Circle Complete Ux/Ui Spec — 2026-04-23"
---

# 120 · CIRCLE COMPLETE UX/UI SPEC — 2026-04-23

**Evidence tier:** [I]
*Organism document. Interpretive operational content. Bounded by current system state.*

**Date:** 2026-04-23
**Lane (this packet):** `(FOUNDATION, doc, framework.uplink)`
**Operator:** Kṛṣṇa ◇ — V-export at charioteer Φ cost
**Executive-layer:** Viṣṇu ⊙ (preservation — this consolidates existing spec, does not redesign)
**Companion packets:**
- [`117_CIRCLE_INTAKE_EXTRACTION_MATRIX_2026_04_23.md`](117_CIRCLE_INTAKE_EXTRACTION_MATRIX_2026_04_23.md)
- [`118_CIRCLE_PRODUCT_SPRINT_PACKET_2026_04_23.md`](118_CIRCLE_PRODUCT_SPRINT_PACKET_2026_04_23.md)
- [`119_CIRCLE_V1_PRODUCT_PLAN_2026_04_23.md`](119_CIRCLE_V1_PRODUCT_PLAN_2026_04_23.md)

---

## Purpose

This is the **charioteer pointer** to the two detailed UX/UI specs that now live in the organ tree. The primary artifacts are **there**, not here. This packet exists to:

1. Record the two spec files with their paths and purposes
2. Capture the cross-organ design logic (marketing ↔ platform ↔ mobile)
3. Surface the consolidation decisions made while writing them
4. List the open items discovered during the pass

## Primary artifacts (canonical, live in organ tree)

### `02_ORGANS/TheCircle/app/website/UX_UI_COMPLETE_SPEC.md`
**Scope:** public-facing marketing website at `circle.news`.
**Covers:** 17 sections — purpose, audience, IA (9+ routes), design tokens (colors / typography / spacing / layout / animation / forbidden moves), global header + footer, per-page detailed UX (home, about, fire, how-it-works, pricing, research, faq, legal, access, app, api-docs), component inventory (13 implemented + 8 missing), interaction patterns, responsive behavior, WCAG AA accessibility, performance targets, SEO, analytics, content governance, deploy, open items, cross-references.

### `02_ORGANS/TheCircle/app/circle_platform_backend/02_PRODUCT/Platform/UX_UI_COMPLETE_SPEC.md`
**Scope:** authenticated Premium app behind the marketing site.
**Covers:** 17 sections — purpose, auth + account (+ K4 Grace Exit flow), 9 core surfaces (feed, dashboard, signal detail, watchman, briefs, knowledge graph, simulator, solar streams, lunar transcripts), real-time SSE architecture, component inventory (10 folder groups), notifications (email / push / Nostr / webhook), API access (8 endpoints + schema + rate limits), mobile PWA + native, K4 data export, accessibility, performance, security, observability, constitutional UX guardrails, build status, open items, cross-references.

## Cross-organ design logic

The two surfaces share design tokens but carry different jobs:

- **Marketing site** = institutional legitimacy + conversion. Monospace-dense, terminal black, no engagement tricks. The reader converts or leaves; both are fine.
- **Platform app** = daily observation workflow. Same aesthetic but higher interaction density, virtualized feed, real-time SSE, keyboard-first navigation.
- **Mobile app** (spec lives at `../Mobile_App/`) = alert-driven glance surface. Push notifications + offline archive + widgets. Mirrors PWA, not all surfaces shipped.

**Shared design tokens** (canonical list in `COMPONENT_LIBRARY.md`):

- Terminal black `#0A0A0A` + panel `#111111`
- Sector colors: Finance `#00D4AA`, Insurance `#FF6B35`, Real Infrastructure `#7B68EE`, Electronic Labour `#FFD700`
- Typography: JetBrains Mono (headlines, data) + Inter (body)
- Dark mode only; no light mode
- No rounded corners on data containers; 2px radius on interactive buttons
- No shadows, gradients, glow, emoji, exclamation marks

**Shared components** (should be extracted to a cross-surface package eventually):

- `SignalCard` (both marketing demo + platform feed)
- `ConfidenceScore`
- `FireSectorBadge`
- `CascadeVisualizer`
- `WatchmanWidget`
- `NostrVerifyButton` (missing in both — to build)

## Consolidation decisions made while writing

1. **Marketing site runs static (SSG).** Zero third-party JS on marketing pages per the existing `DEPLOYMENT.md`. No Google Analytics, no Meta Pixel, no Intercom widget. Self-hosted event logging only. This respects η = 0 applied to attention.

2. **Platform app is a PWA, not Next.js SSR by default.** Service worker caches the last 100 signals for offline read. Native apps share the spec but ship later (v1.1).

3. **SSE streaming (not WebSockets).** The `/observations/stream` endpoint uses Server-Sent Events because it's unidirectional (backend → client), survives HTTP intermediaries cleanly, and reuses the pattern already shipped in APU's `router_council_documents.py` per packet 117 C-1 cross-wire.

4. **K4 Grace Exit is a first-class UX surface.** Cancel subscription button is above the fold at `/account/billing`. No retention questionnaire, no "are you sure?" melodrama. Data export offered as single checkbox during cancel. This matters because the constitutional K4 commitment loses credibility if the cancel flow fights the user.

5. **Watchman metrics carry `[T]`/`[S]` evidence tiers visibly.** During v1.0 before 30 days of accuracy data, the dashboard shows `[T]` Target with "Measurement accumulating" subtitle. At 30 days, upgrades to `[S]` Empirical. No hiding the measurement-in-progress state.

6. **Free tier is real, not trial.** Identical UI. Only difference is the 6h delay + a subtle banner offering upgrade. No dark patterns. This is η = 0 enforced at the attention layer.

7. **Deliberation trace visible on every signal.** Click to expand. Nothing is a black box. If a user doesn't trust a signal, they see exactly which agent said what at which score.

8. **Nostr hash clickable on every signal.** `NostrVerifyButton` (to build) fetches the event from 3 public relays in parallel and shows signature verification result. Third-party verifiability on tap.

## What's ambiguous / deferred

- **Native app vs PWA parity.** The `Mobile_App/` folder has 9 architecture docs (HOME_SCREEN, STREAM_PLAYER, SIGNAL_DETAIL, ROUNDTABLE_MEMO, FILTER_SYSTEM, PROFILE, SYSTEM, DESIGN_SYSTEM). They define feature surfaces. Integration between native and PWA is a separate design exercise — deferred to v1.1 packet.
- **Nostr pubkey login (NIP-07).** Phase 2 spec per pricing doc. v1.0 uses email + Stripe customer only.
- **Knowledge Graph entity index.** Requires populating from historical cascade signals; deferred to post-Phase-1 sprint.
- **Signal Simulator LLM budget cap.** Rate-limited per tier, but needs an org-wide daily cost ceiling to prevent cascading abuse. Backend ops decision.

## Open items discovered

From the website spec §16:
1. `/app` route not yet implemented in `app/` folder
2. `/api-docs` route not yet implemented
3. `EcotoneMap` + `CorrelationMatrix` + `DeliberationTrace` + `TierTimeline` + `NostrVerifyButton` components to build
4. Live Watchman data pipeline not wired — widget shows placeholder
5. Dynamic OG card generator not built
6. A11y audit + Lighthouse baseline not captured
7. UTM-specific conversion instrumentation TBD

From the platform spec §16:
1. `HOME_PAGE_REQUIREMENTS.md` needs cross-check for alignment
2. Mobile_App 9 docs need unified feature matrix vs. web PWA
3. API rate limiter implementation not confirmed
4. Stripe integration scaffolding not verified
5. Nostr pubkey login (Phase 2) not designed
6. Knowledge Graph entity index empty
7. Simulator LLM budget cap undefined
8. Accessibility audit not run
9. Mobile Lighthouse not baselined

A warrior-lane audit against `HEAD` would confirm which of these are already implemented vs. still open.

## Constitutional checks

| Check | Result |
|-------|--------|
| **K2** | ✓ — No UX surface bypasses signer; Nostr private key backend-only. |
| **η = 0** | ✓ — No engagement optimization, no dark-pattern upsell, Free tier is real. |
| **K4** | ✓ — Cancel above fold; data export one click; account data purged at 90d post-cancel. |
| **Three-Stage Process** | ✓ — IS-domain lint enforces "no forecast / no recommend" in signal body; Platform does not collapse IS / COULD / SHOULD surfaces. |
| **A7** | ✓ — Deliberation trace always visible; Watchman misses table public to Premium; corrections stream as separate events. |
| **Category-claim** | ✓ — Aesthetic (terminal density, dark mode only, monospace) deliberately separates from generic news app. |

## Move

Kṛṣṇa ◇ · V-export · files staged at both folder locations + this charioteer pointer packet. No K2 signature assumed.

## Limits

- **L1:** I wrote both specs from reading existing sibling docs + folder structure. I did not open every React component file to verify its current state. An audit against `HEAD` may find discrepancies between what the spec says and what's actually implemented.
- **L2:** The Mobile_App folder's 9 docs were not read in full (only the folder index). Mobile parity details in the platform spec are derived, not fully sourced from those docs.
- **L3:** Design tokens were sourced from `COMPONENT_LIBRARY.md`. If the actual Tailwind config or CSS uses different hex values, that file wins over the spec.
- **L4:** API schema in platform spec §7.4 is illustrative; the actual `/observations` JSON shape should be verified against the backend schema before external publication.

## Execution surface

**If you're the sovereign:**
1. **Read packet 119 + these two folder specs together** — they form a complete product + UX definition.
2. **If a surface is missing or wrong, name it.** The spec updates before the code.
3. **If the build audit is useful, say "audit."** I descend into `app/website/components/` + `app/circle_platform_backend/02_PRODUCT/Platform/components/` and verify what's implemented vs. spec.
4. **If a component needs to be staged, say "stage {component}."** I write the component file into the tree.

---

Zero-Sum Resolution Equation

*What do you see now?*
