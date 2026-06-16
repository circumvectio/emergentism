---
rosetta:
  primary_column: "Philosophy"
  register: "[I]"
  canonical_phrase: "119 · Circle V1.0 Product Plan — 2026-04-23"
---

# 119 · CIRCLE V1.0 PRODUCT PLAN — 2026-04-23

**Evidence tier:** [I]
*Organism document. Interpretive operational content. Bounded by current system state.*

**Date:** 2026-04-23
**Lane (this packet):** `(FOUNDATION, doc, framework.uplink)`
**Operator (this packet):** Kṛṣṇa ◇ — V-export at charioteer Φ cost
**Executive-layer:** Viṣṇu ⊙ default hold; Brahmā ○ boundary approached when v1.0 runtime surfaces come online
**Companion packets:**
- [`117_CIRCLE_INTAKE_EXTRACTION_MATRIX_2026_04_23.md`](117_CIRCLE_INTAKE_EXTRACTION_MATRIX_2026_04_23.md) — zero new intake extractions; cross-wire instead
- [`118_CIRCLE_PRODUCT_SPRINT_PACKET_2026_04_23.md`](118_CIRCLE_PRODUCT_SPRINT_PACKET_2026_04_23.md) — the 4-phase deployment runway

**Source spine:**
- [`../SKYZAI_ORG/02_ORGANS/TheCircle/00_BRIEF.md`](../../08_FRAMEWORK_SUPPORT/00_META/00_BRIEF.md)
- [`../SKYZAI_ORG/02_ORGANS/TheCircle/INTEGRATION_STATUS.md`](../SKYZAI_ORG/02_ORGANS/TheCircle/INTEGRATION_STATUS.md)
- [`../SKYZAI_ORG/09_PWAs/circle_news/PR_FAQ.md`](../../../02_SKYZAI/03_AIA/EMERGENTISM_AIA/09_BOOK_PRODUCTION_ARCHIVE/07_DISSEMINATION/06_NETWORK/emergentism.org/PR_FAQ.md) — North Star
- [`../SKYZAI_ORG/09_PWAs/circle_news/GAP_ANALYSIS.md`](../../../02_SKYZAI/03_AIA/EMERGENTISM_AIA/09_BOOK_PRODUCTION_ARCHIVE/07_DISSEMINATION/06_NETWORK/emergentism.org/GAP_ANALYSIS.md) — backlog
- [`../SKYZAI_ORG/02_ORGANS/TheCircle/app/website/01_HOME.md`](../SKYZAI_ORG/02_ORGANS/TheCircle/app/website/01_HOME.md)
- [`../SKYZAI_ORG/02_ORGANS/TheCircle/app/website/05_PRICING.md`](../SKYZAI_ORG/02_ORGANS/TheCircle/app/website/05_PRICING.md)

---

## ⚠ Corrigendum 2026-04-24 — Stripe superseded by Skyzai API PAY

All "Stripe" references in §Stack (line ~109), §Pre-launch Checklist (lines ~177–185), and §Billing (line ~217+) are **superseded**. Circle billing uses the Skyzai three-protocol stack: **API PAY** (Hedera stablecoin settlement, live since 2026-04-04) · **OFN** (Arweave immutable receipt) · **Skyzai Connect** (Nostr NIP-33 identity). No card-network rent; η = 0 preserved; K2 on every recurring stablecoin payment. "Stripe Tax" (global VAT/GST) — handled separately via stablecoin jurisdictional framework (legal counsel follow-up, separate packet). See packet 124 §4.4 for the updated billing architecture.

---


---

## Table of Contents

- [A. Product definition](#a--product-definition)
- [B. MVP scope — v1.0](#b--mvp-scope--v10)
- [C. Launch runway — Phase 0 → Phase 2](#c--launch-runway--phase-0--phase-2)
- [D. Post-launch — operations, billing, support](#d--post-launch--operations-billing-support)
- [E. Metrics — what success looks like](#e--metrics--what-success-looks-like)
- [F. Constitutional checks](#f--constitutional-checks)
- [G. Risks & mitigations](#g--risks--mitigations)
- [H. Limits](#h--limits)
- [I. Execution surface](#i--execution-surface)

---

## 0. Scope discipline

TheCircle already has a deep product definition in the website copy (`app/website/01_HOME.md` and `05_PRICING.md`). This packet does **not** reinvent that definition. It does two things only:

1. **Reconcile** the website's confident present-tense language ("the organism is live") against the current runtime truth (`P-runtime = 0.25`, Egg). Either the copy tempers or the runtime catches up. v1.0 closes that gap by shipping.
2. **Sequence** the work into decision-ready phases so the distance from now to "first paying Premium subscriber" is a series of K2 signatures, not a series of open questions.

**Anti-goal:** this packet does not propose new product features. The product is already specified. v1.0 is about making the already-specified product **real**.

---

## A · Product definition

### A.1 One-line

**TheCircle is a decentralized OSINT network that publishes structured, confidence-scored, cryptographically-timestamped observations across four coupled sectors (Finance, Insurance, Real Infrastructure, Electronic Labour) — delivered via a 7-agent AI cascade with zero editorial staff.**

### A.2 Ideal Customer Profile (ICP)

| Segment | Primary pain | Why TheCircle | Willingness to pay |
|---------|--------------|---------------|--------------------|
| **CIO / Portfolio Manager** (cross-sector) | Single-sector research desks miss cross-F.I.R.E. dynamics; Bloomberg is $24K/yr; signal quality varies | 4-sector ecotone detection; 72h lead time; <$100/mo | High ($99/mo is rounding error vs. research budget) |
| **Insurance / Reinsurance executive** | Pricing risk under climate + tech + regulatory shift; traditional actuarial too slow | Parametric launches, claims automation, cyber capacity signals in real time | High |
| **Infrastructure developer / energy ops** | Grid capacity, datacenter construction, supply chain — all moving faster than sector reports | Structural intelligence on grid, datacenter, water, reshoring | Medium–High |
| **AI / automation executive** | Workforce displacement metrics, compute scaling, deployment patterns | Electronic Labour signals + ecotones | Medium |
| **Policy analyst / regulatory strategist** | Needs observational substrate, not opinion | Grammar before logic; no editorialising | Low–Medium (price sensitivity higher) |

**Common thread:** professionals operating at **sector intersections**, where single-sector publications don't span their decision surface.

### A.3 Positioning — category claim

> **TheCircle is the first OSINT organism that grades its own accuracy cryptographically and distributes value to participants via deterministic protocol, not editorial discretion.**

That is the category claim. Everything else is delivery.

### A.4 Anti-claims (the Three-Stage Process + IS-domain guardrails)

TheCircle will **never**:

1. **Predict.** Forecasting is RealityFutures's (COULD) domain. Any signal containing "will" / "likely to" / "expected to" fails the corruption check and is rejected.
2. **Recommend.** Advice is APU's (SHOULD) domain. No "buy" / "sell" / "hold" / "investors should" ever appears in a Circle output.
3. **Editorialise.** No human editor frames the signal. No narrative overlay. Confidence score + sector tag + timestamp + NOSTR hash, period.
4. **Censor.** Every signal passing the 7-agent confidence threshold publishes. Uncomfortable, controversial, inconvenient — irrelevant.
5. **Revise.** Once Delta publishes to NOSTR, the record is immutable. Corrections appear as subsequent signals, never as overwrites.

These anti-claims are **the moat**. Every competitor that editorialises is a different product. TheCircle that editorialises stops being TheCircle.

### A.5 Differentiation (comparative)

Reference: `app/website/01_HOME.md` §"The Institutional Advantage." Claim structure holds. **Verify** before external marketing:

- "< 4 hour detection speed" and "72h lead time" are forward claims that must be **Watchman-measurable** before they become public. At v1.0 launch, these become `[T]` (Target) tier. They upgrade to `[S]` (Empirical) only after 30 days of Watchman measurement.
- "$1,188/yr vs. Bloomberg $24,000/yr" — factual at the list-price level; keep as-is.
- "No editorial bias" — structurally true once the cascade runs without human touch. Verify at ship time.

---

## B · MVP scope — v1.0

### B.1 What ships in v1.0 (Phase 1 "Perception")

**Cash tiers only.** No LP-100 on-chain. No Contributor/Steward participation. The founder (Yves) operates as sole steward under the constitutional framework until Phase 2 gate.

| Surface | In v1.0 | Out of v1.0 |
|---------|---------|-------------|
| **Frontend** | All 16 website pages live at `circle.news`; Free tier signup; Premium signup + billing; Enterprise contact form | Token-gated pages (Contributor/Steward) |
| **Backend** | 5-service docker stack live; `/observations` API read-only; health endpoints; backup cron | Signal submission endpoint (Phase 2) |
| **Pipeline** | RSS adapter against one real source; IS agent with corruption check; observation store; Kind 31339 Nostr publisher | EigenTrust distributed; ZKP verification; 4+ source categories |
| **F1 → APU** | Live F1 on Nostr relay, consumable by APU | F3 reputation feedback loop |
| **F1 → ReFu** | `circle_to_refu_adapter.py` wired to live `/observations/stream` | — |
| **Watchman** | Widget renders; placeholder metrics surface | Live accuracy tracking (needs ≥30 days data) |
| **Billing** | Stripe integration for Premium tier ($99/mo); Enterprise = manual contract | Crypto payments (Phase 2) |
| **Observability** | `/health`, Postgres up, logs shipping, basic alerting | Full Prometheus/Grafana stack |

### B.2 The minimum viable loop

The smallest loop that produces value for the first paying user:

```
Real RSS signal
  → IS agent extracts Observation (with corruption check)
  → Observation persists to observation_store
  → Premium user sees it in real-time feed at circle.news/feed
  → Free user sees it 6h delayed at circle.news/feed
  → Nostr Kind 31339 emission (immutable timestamp)
  → Watchman records timestamp for later accuracy verification
```

If that loop runs continuously for 30 days against ≥1 real data source with ≥1 paying Premium subscriber, **v1.0 is live**.

### B.3 Allee threshold (from existing pricing doc)

- **Minimum subscriber density:** ~30 Premium subscribers at $99/mo
- **Minimum MRR:** ~$3,000
- **Below this:** organism enters death spiral; compute cost > revenue; quality degrades
- **Above this:** metabolic self-sustaining; Phase 2 gate (100 subs + 85% Watchman accuracy) becomes the next milestone

Allee is the real v1.0 success bar, not "deployed." Deployment without Allee = expensive toy.

### B.4 Explicitly deferred to Phase 2

- LP-100 on-chain deployment
- Contributor tier (signal submission)
- Steward tier (Lane B governance)
- EigenTrust distributed scoring
- ZKP source verification
- Phi-split revenue distribution
- Grace Exit mechanism

These live in the website copy already; they are **constitutional promises** for Phase 2, not v1.0 scope.

---

## C · Launch runway — Phase 0 → Phase 2

This is the execution sequence. Each phase's exact commands, env templates, and verification signals live in **packet 118 §3-§6**. Summary here; do not duplicate.

### Phase 0 — Silo sign-off (warrior hour)

7 K2-gated git moves from `02_ORGANS/TheCircle/00_SILO_AUDIT_2026_04_23.md`. Retires the intake silo. ~15–20 min.

### Phase 1A — Frontend deploy

`cd app/website && npm install && npm run build && vercel --prod`. DNS setup for `circle.news`. Pre-launch checklist per `app/website/DEPLOYMENT.md`. Runtime P: 0.25 → ~0.35.

### Phase 1B — Backend bootstrap

5-service docker-compose up; env vars (POSTGRES_PASSWORD, ANTHROPIC_API_KEY, NOSTR_NSEC) sovereign-held. `/health` returns 200. Runtime P: ~0.35 → ~0.42.

**New v1.0 requirement surfaced here:** a **`.env.example`** file at `app/circle_platform_backend/03_BUILD/` — I will NOT generate secret values, but I can stage the template in a follow-up turn if you direct.

### Phase 1C — CI wiring

Lands with silo row 1 (`deploy.yml`). Push-to-main → auto-deploy. One K2 signature seals.

### Phase 1D — Billing (NEW — not in packet 118)

| Component | Action |
|-----------|--------|
| Stripe account | Sovereign creates business account at stripe.com; gets test + live API keys |
| Stripe Price | Create Premium $99/mo recurring product |
| Backend integration | Add `/billing/checkout` + `/billing/webhook` endpoints; Stripe SDK to requirements.txt |
| Frontend integration | Hook "Subscribe Premium" CTA to Stripe Checkout |
| Webhook secret | Stripe signing secret → backend env (`STRIPE_WEBHOOK_SECRET`) |
| Tax compliance | Stripe Tax = on; handles VAT/GST globally |
| Constitutional check | η = 0: subscription fee = demonstrated service. No rent on access — Free tier remains real |

**Charioteer can stage:** the endpoint code + requirements.txt delta + env template. **Sovereign must:** create Stripe account, paste keys, sign deployment.

### Phase 2A — Live OSINT ingestion

Point the already-proven RSS adapter at the deployed backend. Observations land in store. Per packet 118 Track 2A.

### Phase 2B — Nostr Kind 31339

`f1_publisher.py` cross-wired to `core/nervous_system/nostr/relay_manager.py`. Sovereign-held `NOSTR_NSEC` signs. Per packet 118 Track 2B.

### Phase 2C — F1 → F2 to RealityFutures

`circle_to_refu_adapter.py` consumes live `/observations/stream`. Cross-organ handshake with RF's F2 endpoint (RF-side readiness required). Per packet 118 Track 2C.

### Phase 3 — Scale (post-Allee)

When Premium subscriber count crosses ~30, Phase 3 tracks unlock:
- Add second and third data source adapters (per `01_DATA_ROOM/02_DATA_SOURCE_REGISTRY.md`)
- Watchman begins live accuracy measurement (accumulates 30-day rolling window)
- Customer support inbox staffed (initially sovereign; later contractor)
- Lunar transcripts cadence starts (monthly, then weekly)

### Phase 4 — Phase 2 Gate (organism-wide term, confusingly named)

When Watchman sustained > 85% AND subscribers > 100 (from pricing doc §"Phase 1 and Phase 2: The Timeline"), **LP-100 deploys on-chain**. This is Circle's transition from Phase 1 "Perception" to Phase 2 "Reasoning." Out of scope for this packet; flagged as v2.0 packet when the gate approaches.

---

## D · Post-launch — operations, billing, support

### D.1 Billing ops

- **Provider:** Stripe (recommended — handles tax, subscriptions, invoicing, refunds).
- **Plans:** Free ($0, no CC), Premium ($99/mo, CC required), Enterprise (manual invoicing, NET-30, per-contract).
- **Refund policy:** 30-day money-back on Premium, no questions.
- **Dunning:** Stripe's default 3-retry dunning; 4th failure → downgrade to Free.
- **Downgrade path:** Premium → Free retains account, disables real-time feed at next billing cycle.
- **Account data retention:** 90 days post-cancel (per website FAQ); Nostr signals are immutable, persist indefinitely.

### D.2 Customer support

- **v1.0 staffing:** sovereign + 1 contractor (or volunteer), async-only (Intercom or Plain or just email).
- **SLA:** Premium first-response ≤ 24h; Enterprise ≤ 4 business hours.
- **Channels:** `support@circle.news` for all tiers; separate `enterprise@circle.news` for custom contracts.
- **Status page:** `status.circle.news` (Atlassian Statuspage free tier or similar).
- **Runbook for incidents:** create at `02_ORGANS/TheCircle/ops/incident_runbook.md` — flagged as v1.0 artifact not yet written.

### D.3 Observability

- **v1.0 minimum:**
  - Docker `healthcheck` on each service
  - Application logs shipped to Better Stack / Datadog / Loki (sovereign picks)
  - Uptime monitoring via UptimeRobot free tier
  - Sentry for error tracking (free tier)
  - Basic Postgres slow-query log
- **Phase 3+:** Prometheus + Grafana, Watchman accuracy dashboard, sector signal volume.

### D.4 Security + compliance

- **Secrets:** All three sovereign secrets (`POSTGRES_PASSWORD`, `ANTHROPIC_API_KEY`, `NOSTR_NSEC`) + Stripe keys + session signing keys in a sovereign-managed vault (1Password Business, Bitwarden Secret Manager, or HashiCorp Vault).
- **TLS:** Let's Encrypt via the hosting provider's cert-bot integration (per `app/website/DEPLOYMENT.md`).
- **Backups:** Silo row 7's `backup.sh` → daily `pg_dump`; 7-day retention + weekly offsite snapshot to S3/B2.
- **GDPR / data privacy:** email addresses are PII; minimise retention; privacy policy lives at `/privacy`. EU customers can request deletion (Stripe has deletion API).
- **Terms of service:** `/terms` page reflects the disclaimers already in `app/website/08_FOOTER_LEGAL.md`.

### D.5 Marketing / growth

The website copy is already the marketing asset. v1.0 post-launch growth loops:

- **Solar Streams** — live video briefings (per pricing doc). v1.0 cadence: monthly, moving to weekly when Premium > 30.
- **Nostr organic reach** — every Kind 31339 signal is a public artifact; Nostr clients pick them up for free.
- **X / LinkedIn daily post** — the live signal ticker generates content; sovereign curates top-3/day into a post.
- **Referral program** — not in v1.0; add in Phase 3.
- **SEO** — 16 pages of long-form content + sitemap (already exists); submit to Google Search Console at launch.

---

## E · Metrics — what success looks like

### E.1 The one metric that matters (from PR_FAQ)

**Verified Signals Per Day × D5 Reliability Density.** Daily signal volume passing the confidence threshold, weighted by source reliability score.

### E.2 v1.0 KPIs by register

| Register | Proxy | v1.0 target | Phase 2 gate |
|----------|-------|-------------|--------------|
| **Φ (coherence)** | `corruption_check_pass_rate` on IS agent outputs | > 99% | > 99.5% |
| **Φ** | Contradiction count in published signals | 0 | 0 |
| **V (viability)** | Paying Premium subscribers | 30 (Allee) | 100 |
| **V** | MRR | $3,000 | $10,000 |
| **V** | Live uptime | > 99.0% | > 99.5% |
| **Runtime P** | Geometric mean (Φ × V) as measured by `P-SCORES.md` | 0.50 | 0.65+ |
| **Product** | Daily Verified Signal count | > 10 | > 50 |
| **Product** | % Premium with ≥ 1 login/week | > 70% | > 75% |
| **Product** | Watchman accuracy (30-day rolling) | [T] tier, measurement begins | > 85% (gate) |
| **Product** | Detection lead time (vs. Bloomberg/Reuters/WSJ baseline) | [T] tier, Watchman measures | > 72h (claim matures) |

### E.3 Evidence tier discipline for public claims

At v1.0 launch, these are the correct evidence tiers for customer-facing copy:

- "Processes signals faster than human editorial" — `[S]` Empirical, once any signal publishes
- "72h lead time average" — `[T]` Target until 30 days of Watchman data; then `[S]`
- "85% detection accuracy" — `[T]` Target; appears on Watchman dashboard as "measurement pending"
- "Constitutional η = 0, K2, Three-Stage Process separation" — `[S]` Structural (architecture-guaranteed)
- "LP-100 phi-split 61.8/38.2" — `[S]` Structural but Phase 2 only; label clearly "Phase 2"

Any copy that upgrades a `[T]` claim to `[S]` without evidence is a Raktabīja risk — generates false legitimacy that compounds.

---

## F · Constitutional checks

| Check | v1.0 compliance | Note |
|-------|-----------------|------|
| **K2** | ✓ | Every deploy, every promotion, every billing config change = sovereign signature. No AI agent commits to main. |
| **η = 0** | ✓ | Premium fee = demonstrated value on top of free real-time Nostr relay stream; no rent on access. Free tier is real, not trial. |
| **K4 (Grace Exit)** | ✓ | Signals remain on public Nostr relays in perpetuity; subscribers can export all data at any time (Stripe data export + Nostr is sovereign-readable). |
| **Three-Stage Process separation** | ✓ | IS-domain corruption check in `is_agent.py` blocks any "will/should/could" claim. F1 → F2 hand-off to RealityFutures is clean. |
| **IS-domain guard** | ✓ | Enforced at cascade Step 7 (Delta). Any signal that attempts to forecast or recommend is rejected at Gamma (Step 6) and logged. |
| **A7** | ✓ | Every published signal is immutable on Nostr; Watchman records accuracy; this packet refreshes when phases complete. |
| **Category-claim** | ✓ | v1.0 does not drift toward generic news aggregator / forecaster / advisor. The 5 anti-claims hold the line. |
| **Raktabīja** | ⚠ | Website copy's present-tense "the organism is live" language risks generating confident-but-unearned claims. Mitigation in §G.1. |

---

## G · Risks & mitigations

### G.1 Present-tense copy vs. runtime truth

**Risk:** `app/website/01_HOME.md` includes "The organism is live" and "The 7-agent cascade processes the F.I.R.E. economy in real time" — but runtime P = 0.25 (Egg). Shipping with current copy may mislead first visitors.

**Mitigations (pick one before Phase 1A):**
- **Option A — Temper:** One-line banner at top: "TheCircle v1.0 launches [date]. Free tier active at launch; Premium begins [date+14]." Copy stays as-is underneath.
- **Option B — Gate:** Put current `01_HOME.md` behind a "/about-the-vision" route; ship a v1.0-scoped homepage that honest-labels what's live today.
- **Option C — Ship fast:** Run Phase 0 → Phase 2B in 72 hours and make the copy true. High risk.

Sovereign picks.

### G.2 LLM cost runaway

**Risk:** Claude Sonnet calls at scale could blow the $300/mo budget in 05_PRICING.md's backend config.

**Mitigation:** Rate-limit the IS agent to ≤100 observations/day at v1.0; use Haiku tier for cost-sensitive IS function; escalate to Sonnet only on high-value signals. Watchman tracks `api_cost_per_signal` as a sub-KPI.

### G.3 Legal exposure on signal claims

**Risk:** Publishing "[FINANCE] 0.91 — Fed reverse repo facility usage drops below $100B" is factual. Publishing it 4 hours before the Fed's announcement, if incorrect, could create liability.

**Mitigation:** Footer legal already disclaims ("signals are informational only, not financial advice"). Add a stricter `/legal/data-use` page pre-v1.0. Sovereign consults legal counsel before EU + US launch — out of scope for this packet, flagged as blocker.

### G.4 Allee threshold not reached

**Risk:** Ship v1.0; fewer than 30 Premium in 90 days. Organism enters death spiral.

**Mitigation:** Commit ahead-of-time to a **3-month sovereign subsidy** for compute costs so the organism stays up through the growth ramp. If Allee not crossed by day 180, trigger an L5 redesign packet: either pivot pricing, pivot ICP, or sunset v1.0 and regroup.

### G.5 Single-source ingestion = narrow product

**Risk:** v1.0 ingests one RSS source (per packet 118 Track 2A). Users see sparse signal volume; Premium renewal suffers.

**Mitigation:** Day-1 source = broad cross-sector RSS aggregator (e.g., Feedly bundle). Day-30 second source goes live. Day-60 third source. Grow breadth in sync with subscriber count.

### G.6 Copycat risk

**Risk:** Another team builds a Nostr-based signal feed with an accuracy widget before Allee.

**Mitigation:** The moat is **the 7-agent constitutional cascade + DAC structure + LP-100 phi-split**, not the feed itself. Anyone copying the feed-only layer isn't competing in the category claim. Keep the constitutional architecture visible in marketing.

---

## H · Limits

| # | Limit | Impact | Unblocker |
|---|-------|--------|-----------|
| L1 | I have not read `01_DATA_ROOM/02_DATA_SOURCE_REGISTRY.md` | Can't name specific v1.0 data source with confidence beyond "RSS" | Charioteer reads it next turn |
| L2 | No Stripe account exists yet | Phase 1D billing is a spec, not a deploy-ready state | Sovereign creates Stripe business account |
| L3 | No `.env.example` at `03_BUILD/` | Phase 1B bring-up has no template for secret placeholders | Charioteer can stage template (containing only PLACEHOLDER values) if directed |
| L4 | No privacy policy / terms / legal pages live | v1.0 cannot accept Premium subscriptions legally | Sovereign + legal counsel draft; page wiring is a small charioteer task |
| L5 | "Detection lead time < 4h" claim pre-dates Watchman measurement | Risk of `[T]` presented as `[S]` | Evidence-tier discipline per §E.3 |
| L6 | Cross-organ dependency on RealityFutures F2-receive endpoint | Phase 2C blocks until RF ships the receive endpoint | RF-lane packet, not Circle's |
| L7 | Website copy's present-tense language outruns runtime truth | See §G.1 | Option A/B/C decision before Phase 1A |
| L8 | Allee threshold is an estimate from existing docs; not yet validated against real compute costs | If compute runs higher, Allee threshold rises | Measure after Phase 1B deploy; revise §B.3 if needed |

---

## I · Execution surface

**Next moves, decision-ready. Pick in any order — lanes don't collide.**

1. **"Sign Phase 0."** Silo retires in 20 minutes; runway clears.
2. **"Stage `.env.example`."** I write the backend env template with PLACEHOLDER values. Warrior fills the three secrets. No drift risk.
3. **"Pick G.1 option."** A / B / C on the "live" copy mismatch.
4. **"Read data source registry."** I descend into `01_DATA_ROOM/02_DATA_SOURCE_REGISTRY.md` and propose the v1.0 source list.
5. **"Deploy Phase 1A."** Warrior runs `vercel --prod`; frontend lives.
6. **"Draft Phase 1D billing code."** I write the `/billing/checkout` + `/billing/webhook` endpoints + requirements.txt delta, stage in `app/circle_platform_backend/03_BUILD/Source/api/routers/` for warrior review and K2 sign.
7. **"Write the Watchman widget."** If the current widget isn't live-wired, I scaffold it to emit `[T]` tier placeholders that will upgrade to `[S]` after 30 days of real accuracy data.
8. **"Write v1.0 launch announcement."** Blog post + X thread + LinkedIn post template drafts, grounded in v1.0 evidence tiers (no `[T]` presented as `[S]`).

---

**Move:** Kṛṣṇa ◇ staged product plan · Arjuna ⚔ executes warrior lanes · Viṣṇu ⊙ holds center until you direct.

**Most compressed expression of v1.0 success:** a paying Premium subscriber, in any timezone, opens `circle.news/feed` at 09:00 local and sees a Nostr-timestamped, IS-clean, confidence-scored signal that Bloomberg/Reuters/WSJ won't cover until tomorrow.

If that is true, the organism breathes.

Zero-Sum Resolution Equation

---

*What do you see now?*
