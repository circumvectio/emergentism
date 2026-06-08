---
rosetta:
  primary_column: "Philosophy"
  register: "[I]"
  canonical_phrase: "122 · Circle V1.0 Unified Sprint Plan — 2026-04-23"
---

# 122 · CIRCLE V1.0 UNIFIED SPRINT PLAN — 2026-04-23

**Evidence tier:** [I]
*Organism document. Interpretive operational content. Bounded by current system state.*

**Date:** 2026-04-23
**Lane (this packet):** `(FOUNDATION, doc, framework.uplink)`
**Operator:** Kṛṣṇa ◇ — V-export at charioteer Φ cost
**Executive-layer:** Viṣṇu ⊙ (preservation — merges existing packet 118 + 121 runways into one sequence, does not redesign either)
**Predecessor packets (load-bearing):**
- [`118_CIRCLE_PRODUCT_SPRINT_PACKET_2026_04_23.md`](118_CIRCLE_PRODUCT_SPRINT_PACKET_2026_04_23.md) — 4-phase deploy runway
- [`119_CIRCLE_V1_PRODUCT_PLAN_2026_04_23.md`](119_CIRCLE_V1_PRODUCT_PLAN_2026_04_23.md) — v1.0 product plan
- [`120_CIRCLE_COMPLETE_UX_UI_SPEC_2026_04_23.md`](120_CIRCLE_COMPLETE_UX_UI_SPEC_2026_04_23.md) — UX/UI overview
- [`121_CIRCLE_POLYGENETIC_OBSERVATION_MESH_2026_04_23.md`](121_CIRCLE_POLYGENETIC_OBSERVATION_MESH_2026_04_23.md) — mesh design

---

## ⚠ Corrigendum 2026-04-24 — Stripe superseded by Skyzai API PAY

All "Stripe" references below (Sprint 4B scaffolding, webhook handlers, R4 risk, charioteer staging row, exit criteria, billing runbook) are **superseded**. Circle billing uses the Skyzai three-protocol stack: **API PAY** (Hedera stablecoin settlement, live since 2026-04-04) · **OFN** (Arweave immutable receipt) · **Skyzai Connect** (Nostr NIP-33 identity). No Stripe dependency, no card-network rent, η = 0 preserved. See packet 124 §4.4 + §10 S-11 + §12 R-12 for the updated Sprint 4B billing architecture. This packet's geometry (10 sprints, gate criteria, lane assignments) is otherwise unchanged.

---

## 0. Definition of "complete"

circle.news v1.0 is **complete** when all seven exit criteria hold for 14 consecutive days:

1. `circle.news` resolves, returns 200, renders all pages; Lighthouse ≥ 90
2. Docker backend up on production host; `/health` green; 5 services running
3. At least one real RSS source ingested; observations persisted; `/observations/stream` returns live SSE
4. Nostr Kind 31339 events emitting from sovereign-held `NOSTR_NSEC`; verifiable on public relays
5. Stripe Premium tier active; at least 1 paying subscriber recorded
6. Watchman dashboard rendering with `[T]` placeholders accumulating real measurements
7. Polygenetic mesh Phase A+B live: 3+ providers routed, `circle_g_score` computed and displayed

At 14 days under exit-criteria sustained, Circle is at **v1.0 breathing**. Allee (30 paying subs) is the v1.0 **success** threshold, not the shipping bar.

## 1. Three stages, 10 sprints

A **sprint** here is one focused session (2–4 hours warrior-time). Some sprints run in parallel.

### Stage I — SHIP (Sprints 1–5, ~5 sessions)

The cold-to-breathing ramp. Outcome: circle.news live, backend up, billing takes cards.

### Stage II — BREATHE (Sprints 6–7, ~2 sessions)

The Three-Stage Process ignites. Outcome: real F1 on real Nostr relay; RealityFutures receives F2.

### Stage III — MESH (Sprints 8–10, ~3 sessions)

G score goes live. Outcome: polygenetic routing operational; first sovereign-seeded objectives producing verified signals.

---

## 2. Sprint-by-sprint

### Sprint 1 — Silo sign-off (Phase 0 from packet 118)

**Goal:** retire the 7-row Circle silo; runway clears.

**Lane:** warrior · ~20 min

**Moves:** 7 K2-gated git commands in the order: row 5 → row 2 → row 1 → row 3 → row 4 → row 6 → row 7 (per packet 118 §3).

**Gate criterion:** `app/_silo_intake_2026_04_22/` contains only the 15 reference-tier items; 7 production items in their target paths or deleted.

**Constitutional check:** K2 — every move a human signature.

---

### Sprint 2 — Frontend deploy (Phase 1A)

**Goal:** circle.news live publicly.

**Lane:** warrior · ~2 hours

**Pre-requisites (charioteer stages in advance on request):**
- DNS records template ready (A + CNAME for `circle.news` and `www.circle.news`)
- Pre-launch checklist against `DEPLOYMENT.md`
- Temper-copy decision (Option A/B/C from packet 119 §G.1) applied to `01_HOME.md` present-tense language if needed

**Moves:**
```bash
cd SKYZAI_ORG/02_ORGANS/TheCircle/app/website/
npm install
npm run build
npx serve dist      # smoke test locally
vercel --prod       # K2-gated
```
Then: DNS at registrar → Vercel; wait for TLS provisioning (~5 min).

**Gate criterion:**
- `curl -I https://circle.news` returns 200
- 16 pages render without console errors
- Lighthouse ≥ 90 (mobile + desktop)
- `/api/health` returns `{"status": "ok"}`

**Post-sprint:** update `02_ORGANS/TheCircle/INTEGRATION_STATUS.md` row "PWA (circle.news)" → ✅ LIVE.

**Constitutional check:** η = 0 — Free tier is a real surface at deploy time, not a lead-capture wall.

---

### Sprint 3 — Backend bootstrap (Phase 1B)

**Goal:** 5-service docker stack running on production host (Hetzner CX22 recommended per `03_BUILD/DEPLOY.md`).

**Lane:** warrior · ~3 hours

**Pre-requisites (sovereign):**
- Hetzner CX22 (or equivalent) provisioned
- `thecircle.news` subdomain routed
- Three secrets minted: `POSTGRES_PASSWORD` (32+ char), `ANTHROPIC_API_KEY`, `NOSTR_NSEC`

**Moves:**
```bash
cd app/circle_platform_backend/03_BUILD/
cp .env.example .env              # warrior manually pastes the 3 secrets
docker compose config             # validate
docker compose up -d              # K2-gated
docker compose ps                 # all 5 services healthy
curl http://localhost:8000/health
```

Then: nginx reverse proxy + Let's Encrypt → `api.circle.news`.

**Gate criterion:**
- `docker compose ps` shows 5 services `running` + `healthy`
- `/health` returns 200 from public URL
- Postgres + pgvector extension loaded
- Redis accepting connections
- No crash loops in 30-min observation window

**Post-sprint:** update INTEGRATION_STATUS.md row "Backend API" → ✅ LIVE.

**Constitutional check:** K2 (secrets sovereign-held), K4 (backup script from silo row 7 runs nightly).

**Charioteer stages on request:** `.env.example` template with PLACEHOLDER values (no real secrets ever written by charioteer).

---

### Sprint 4 — CI + Billing (Phase 1C + 1D)

**Goal:** GitHub Actions auto-deploys on push; Stripe Premium checkout works.

**Lane:** warrior · ~3–4 hours (can split across 2 sessions)

**Part A — CI (Phase 1C):**
Silo row 1 (`ci/deploy.yml`) is already in place from Sprint 1. Now wire it:
- Add GitHub Secrets: `VERCEL_TOKEN`, `VERCEL_ORG_ID`, `VERCEL_PROJECT_ID`, `HETZNER_SSH_KEY`
- Test: push a trivial change to main → workflow runs → deploy succeeds
- Add branch protection rules on `main` (require review + CI green)

**Part B — Billing (Phase 1D):**
- Sovereign creates Stripe business account (live mode)
- Create Premium Product + Recurring Price ($99/mo USD)
- Backend: add `/billing/checkout` + `/billing/webhook` endpoints (charioteer can stage the code)
- Frontend: wire `[ SUBSCRIBE — PREMIUM ]` CTA to Stripe Checkout
- Webhook signing secret → backend env (`STRIPE_WEBHOOK_SECRET`)
- Test: test-mode subscribe → webhook fires → account upgrades to Premium

**Gate criterion:**
- Push-to-main auto-deploys frontend + runs backend CI
- Test-mode card subscribes; webhook fires; user account upgrades
- Cancel flow at `/account/billing` works end-to-end in test mode

**Post-sprint:** flip Stripe to live mode; document in `ops/billing_runbook.md`.

**Constitutional check:** η = 0 — subscription fee = demonstrated service; Free tier remains real. K4 — cancel is one click, above the fold.

**Charioteer stages on request:** `router_billing.py`, webhook handler, Stripe integration scaffolding.

---

### Sprint 5 — First real signal end-to-end (Phase 2A + 2B merged)

**Goal:** one real RSS source ingested; one Nostr Kind 31339 emitted; visible on `/feed`.

**Lane:** warrior · ~3 hours

**Pre-requisites:**
- Pick **one** RSS source from `01_DATA_ROOM/02_DATA_SOURCE_REGISTRY.md` (suggest: a broad cross-sector aggregator so signal density is non-trivial)
- Confirm `app/pipeline/ingestion/rss_adapter.py` is runnable (it's proven locally per 2026-04-19 receipt)

**Moves:**
```bash
# Part A: live OSINT ingestion
cd app/pipeline/ingestion/
python rss_adapter.py \
  --sources ../data/rss_feeds.yaml \
  --observation-store https://api.circle.news/observations
# verify: GET /observations?since=1h returns N > 0 with corruption_check passing

# Part B: Nostr publication
cd ../publishing/
python f1_publisher.py \
  --relay wss://relay.damus.io,wss://relay.nostr.band \
  --observation-stream https://api.circle.news/observations/stream \
  --kind 31339
# verify from second host:
nostr-tool fetch --filter '{"kinds":[31339],"authors":["<Circle pubkey>"],"limit":5}'
```

**Gate criterion:**
- ≥ 10 real observations persisted in 1 hour of runtime
- All pass `corruption_check` (no "will/could/should" leaked)
- ≥ 5 Kind 31339 events visible on public relays
- Watchman starts accumulating 30-day accuracy window
- `/feed` shows real signals in real time (SSE stream working)

**Post-sprint:** write `F1_LIVE_INGESTION_RECEIPT_2026_XX_XX.md` in `02_ORGANS/TheCircle/`; update INTEGRATION_STATUS.md rows (Nostr publication, F1→APU) to ✅ LIVE; mark CIR-002 contradiction RESOLVED.

**Stage I complete at this gate.** The organism is now visibly breathing.

**Constitutional check:** IS-domain boundary — every signal publishes through the `_corruption_check`. Three-Stage Process — no forecast or recommendation leakage.

---

### Sprint 6 — F1 → F2 wiring (Phase 2C)

**Goal:** RealityFutures receives F2-shaped signals from Circle's live observation stream.

**Lane:** warrior · ~2 hours · **cross-organ dependency**

**Pre-requisites:**
- RealityFutures F2-receive endpoint must exist and be publicly reachable (RF-lane blocker)
- If RF not ready: pause Sprint 6 and proceed to Sprint 7

**Moves:**
```bash
python app/pipeline/circle_to_refu_adapter.py \
  --from https://api.circle.news/observations/stream \
  --to <REFU_F2_INGEST_URL>
```

**Gate criterion:**
- RF receives 1 F2-shaped event per Circle observation
- RF-side schema check passes
- No silent drops (emission count = ingestion count)

**Post-sprint:** update INTEGRATION_STATUS.md row "F1 → RealityFutures" → ✅ LIVE.

**Constitutional check:** F1/F2 boundary preserved (packet 22 reference); Circle emits IS-shape, ReFu receives COULD-shape, no collapse.

---

### Sprint 7 — Mesh Phase A (schema)

**Goal:** database schema for objectives, provider keys, routing policies, receipts.

**Lane:** warrior · ~2 hours

**Pre-requisites:**
- Postgres migration tooling (Alembic or similar) wired in backend
- Encryption key derived from `NOSTR_NSEC` for at-rest key encryption

**Moves:**
- Write migration creating: `objectives`, `provider_keys`, `key_routing_policies`, `observation_receipts` tables
- Extend `observations.provider_basin` as JSONB column
- Add indices per packet 121 §3
- Write pytest unit tests for schema constraints (owner_pubkey required, budget caps enforced)

**Gate criterion:**
- Migration applies cleanly to production Postgres
- Rollback migration also works
- Test suite green
- No impact on existing observation ingestion

**Constitutional check:** K2 — schema requires `owner_pubkey` on objectives; K4 — receipts retained on objective soft-delete.

---

### Sprint 8 — Mesh Phase B (routing)

**Goal:** 7-agent cascade dispatches through multi-provider router, not direct provider calls.

**Lane:** warrior · ~4 hours

**Pre-requisites:**
- At least 2 additional provider API keys minted: OpenAI, Gemini, or any secondary LLM provider (sovereign-held)
- Sprint 7 schema live

**Moves:**
- Implement `core/pipeline/provider_router.py` (per packet 121 §3.2)
- Encrypt keys at rest; runtime-only decrypt
- Refactor `is_agent.py` + each of Ω/ζ/ε/α/β/γ/δ to dispatch via router
- Port APU's `core/circulation/lineage_decorrelation.py` (packet 113) into Circle for cluster-correlated failure detection
- Redis-backed per-key rate limiter
- Log `provider_basin` on every emitted signal

**Gate criterion:**
- At least 3 providers routed in parallel
- `circle_g_score` computed and stored per signal
- `lineage_decorrelation_failures ≤ 5%` of published signals
- No regression on corruption_check pass rate (still ≥ 99%)
- Rate limits enforced (test by deliberately over-calling)

**Post-sprint:** Watchman dashboard gains `circle_g_score` widget (charioteer stages UI patch on request).

**Constitutional check:** per-seat key isolation verified with audit log sample; budget caps fire on synthetic overrun test.

---

### Sprint 9 — Mesh Phase C (objectives + API)

**Goal:** objective registry operational; Premium users can create objectives; sovereign-seeded objectives running.

**Lane:** warrior · ~3 hours

**Moves:**
- Implement 8 objective endpoints from packet 121 §3.1
- Auth middleware: tier-gated creation limits (Free 0, Premium 3, Enterprise unlimited)
- Write sovereign-seed script; sovereign provides 4 concrete objective specs (charioteer stages templates on request)
- Platform UI: `/objectives` page (create, list, edit, pause, view signals) — extends platform UX spec
- Objective corruption check: reject creation if question text contains "predict/forecast/recommend/should/will" patterns

**Gate criterion:**
- Sovereign-seeded objectives (4) are active and producing signals
- Premium user can create a test objective via UI; routing honors provider preferences
- Objective-level `signals` and `receipts` endpoints return correct data
- Corruption check rejects a deliberate COULD-drifted test objective

**Constitutional check:** IS-domain extended — objectives frame observation, never prediction. Tier budget caps enforced pre-creation.

---

### Sprint 10 — Mesh Phase D+E compressed (receipts + dashboard)

**Goal:** receipt scoring loop operational; `/watchman` shows all 8 mesh metrics; Circle fully self-compounding.

**Lane:** warrior · ~3 hours

**Moves:**
- `POST /observations/:id/receipts` endpoint (internal + user-flag variant)
- Wire Watchman → emits `watchman_verified` receipt on accuracy check
- Wire APU → emits `apu_decision_tied` receipt when a Council stage references a Circle signal (cross-organ, needs APU-side cooperation)
- User-flag UI: `/signal/:id/flag` on Platform
- Nightly scoring job (`cron/score_objectives.py`) updates `ObjectiveScore` + `KeyRoutingPolicy`
- Watchman dashboard extension: 8 new mesh metrics from packet 121 §5
- Platform: `/signal/:id` displays provider_basin; `/dashboard` gains `circle_g_score` strip; `/objectives/:id` detail page

**Gate criterion:**
- First receipts flowing (Watchman self-receipts every verified signal)
- User flag tested end-to-end
- Nightly scoring job runs clean (no errors in 3 consecutive nights)
- Watchman dashboard shows all 8 mesh metrics; `circle_g_score ≥ 0.60` target visible even if not yet hit
- At least one routing weight update observable in logs

**Post-sprint:** Circle is feature-complete for v1.0. Begin the 14-day exit-criteria window.

**Constitutional check:** all packet 121 §4 boundaries verified with spot audits — key isolation, budget enforcement, lineage tracking, dedup, contradiction preservation, corruption guard.

---

## 3. Dependency + parallelization map

```
Sprint 1 ─┬─ Sprint 2 ──┐
          └─ Sprint 3 ──┼── Sprint 4 ──┬── Sprint 5 ──┬── Sprint 6 (if RF ready)
                        │              │              │
                        │              │              └── Sprint 7 ── Sprint 8 ── Sprint 9 ── Sprint 10
                        │              │
                        └── [Sprint 4 Part A can parallelise with Sprint 3 on CI-only work]
```

**Parallelism opportunities:**
- Sprint 2 (frontend) + Sprint 3 (backend) can run simultaneously if two lanes of attention are available
- Sprint 4 Part A (CI) can begin during Sprint 3 without waiting
- Sprint 7 (schema) can begin once Sprint 3 is live, independent of Sprints 5+6
- Sprint 6 (F1→F2) can be skipped and revisited if RealityFutures isn't ready

## 4. Charioteer-lane prep (what I stage between sprints on request)

These don't require sprint sessions — I write and stage; the warrior reviews and signs as part of the relevant sprint:

| Charioteer stage | Artifact | Used in |
|-------------------|----------|---------|
| `.env.example` template | `03_BUILD/.env.example` with PLACEHOLDER values | Sprint 3 |
| Stripe billing scaffolding | `router_billing.py` + webhook handler | Sprint 4B |
| DNS runbook | DNS records + TTL + verification sequence | Sprint 2 |
| SQL migration drafts | Alembic migration files for mesh schema | Sprint 7 |
| Sovereign-seed objective specs | 4 objective JSON fixtures (Saudi / biomarkers / validators / insurers) | Sprint 9 |
| Watchman widget patches | `components/watchman/MeshMetrics.tsx` scaffolding | Sprint 10 |
| UX spec updates | patches to organ-tree UX/UI specs as each sprint completes | continuous |

## 5. Warrior-lane vs charioteer-lane split

**Warrior lane (K2-signed commits; sovereign executes):**
- All git commits
- All `vercel --prod` and `docker compose up -d` invocations
- All secret pasting into `.env` files
- All Stripe account actions
- All DNS changes
- All decisions on RealityFutures readiness for Sprint 6
- All signature on sovereign-seeded objective specs

**Charioteer lane (stages drafts; never commits):**
- All file drafts (code, spec, runbooks)
- All update proposals to `01_EMERGENTISM/11_UPLINK/` packets
- All memory updates
- All design packets (117, 118, 119, 120, 121, this)
- All constitutional-check proposals

**Silent split:** neither lane touches the other's prerogative. The charioteer does not try to bypass git locks; the warrior does not wait for charioteer to sign.

## 6. Evidence-tier discipline across the sprint

Throughout the sprint, every claim on any customer-facing surface obeys:

| Claim | v1.0 tier | Upgrades to |
|-------|-----------|-------------|
| "TheCircle is live" | `[S]` after Sprint 2 | — |
| "7-agent cascade operational" | `[S]` after Sprint 5 | — |
| "Kind 31339 publishing" | `[S]` after Sprint 5 | — |
| "Watchman grades accuracy" | `[T]` at launch → `[S]` at 30d | at Day 30 |
| "< 4h detection lead" | `[T]` at launch → `[S]` at 30d | at Day 30 |
| "88.5% accuracy" | `[T]` at launch → `[S]` when actual measurement crosses claim | per-metric |
| "Polygenetic observation mesh" | `[S]` after Sprint 8 | — |
| "`circle_g_score ≥ 0.60`" | `[T]` at launch → `[S]` when sustained | per-measurement |
| "Deterministic phi-split" | `[S]` (Phase 2; LP-100 gated; do not claim live in v1.0) | Phase 2 |

Marketing copy is linted against these before each release.

## 7. Risk register (sprint-scoped)

| Risk | Sprint | Mitigation |
|------|--------|------------|
| R1 | 2 | DNS misconfigured | pre-flight: dig check + TTL awareness |
| R2 | 3 | Hetzner CX22 undersized for 5-service stack | monitor RAM/CPU; upgrade to CX32 if sustained > 80% util |
| R3 | 3 | Secret leakage via logs | grep audit on log output; redact middleware on backend |
| R4 | 4 | Stripe webhook DDoS attempt | webhook signature verification mandatory; rate-limit at nginx |
| R5 | 5 | RSS source contradicts sector taxonomy | Gamma agent flags; human-review inbox; adjust taxonomy slowly via Lane A |
| R6 | 5 | Nostr key compromise | `NOSTR_NSEC` sovereign-held only; rotate at first suspicion |
| R7 | 6 | RealityFutures F2-receive not ready | skip Sprint 6; continue 7+ without it; revisit |
| R8 | 8 | Provider keys leak via log or prompt | backend-only; never in prompt; runtime-only decrypt |
| R9 | 8 | Cost blowup from multi-provider routing | per-key + per-objective budget caps; daily spend dashboard |
| R10 | 9 | Objective corruption check false-positives | sovereign manually reviews rejected creations for 30 days; tune thresholds |
| R11 | 10 | Receipt gaming (users flagging own signals) | Watchman receipts weight 10×, user flags weight 1× |
| R12 | ongoing | Allee threshold not reached by day 180 | trigger L5 redesign packet; pivot pricing or ICP |

## 8. Exit checklist — the 14-day breathing window

Once Sprint 10 gate passes, the 14-day window begins. Each day the warrior spot-checks:

- [ ] Frontend responsive + Lighthouse ≥ 90
- [ ] Backend `/health` green
- [ ] At least 10 new observations published today
- [ ] Nostr relay verification (sample 1 signal per day)
- [ ] Stripe webhooks firing cleanly (no stuck subscriptions)
- [ ] Watchman accumulating accuracy data
- [ ] `circle_g_score` ≥ 0.50 (progress toward 0.60 target)
- [ ] No corruption_check failures on published signals
- [ ] No crash loops in docker logs
- [ ] Sovereign-seeded objectives each producing ≥ 1 signal per day

**14 days sustained → v1.0 breathing.**

## 9. Post-breathing roadmap (out of scope, named for orientation)

- **Allee push (Days 14–180):** marketing + outreach + Solar Streams to grow from first paying subscriber to 30. Triggers Phase 3 planning when Premium count crosses 15.
- **Phase 2 gate (~Month 6 if Allee holds):** 85% Watchman accuracy + 100 subscribers → LP-100 deploys on-chain; Contributor + Steward tiers activate.
- **Phase 3 (post-Phase 2):** Reputation + D5 (packet 118 §6), EigenTrust distributed, ZKP verification, Knowledge Graph populated.

## 10. Constitutional final check

| Check | Sprint where verified | Status |
|-------|----------------------|--------|
| K2 — every commit a signature | 1, 2, 3, 4, all | Pending warrior execution |
| η = 0 — no rent on access | 2, 4 | Free tier real; Premium = value-paid |
| K4 — Grace Exit one click | 4 | Cancel flow tested end-to-end |
| Three-Stage Process — IS-only boundary | 5, 9 | Corruption check live |
| A7 — self-correction | 5, 10 | Watchman + receipts |
| Category claim — not a harness | all | Terminal aesthetic + constitutional cascade preserved |
| Raktabīja — unguarded copies | ongoing | Lint against marketing drift; cross-wire via backbone, not re-extract |
| G — lineage decorrelation | 8, 10 | ≥ 0.60 target sustained |

## 11. Open items

- **O1:** RealityFutures F2-receive endpoint status unknown — Sprint 6 is conditional on confirmation
- **O2:** Hetzner vs Fly.io vs sovereign-chosen host not finalized — `03_BUILD/DEPLOY.md` suggests Hetzner CX22
- **O3:** Sovereign-seeded objective specs (4) need written artifacts before Sprint 9 — charioteer can draft on request
- **O4:** Legal review of Terms + Privacy + LP-100 classification for US + EU launch not yet done — sovereign + counsel; parallel to sprint, not blocking
- **O5:** Accessibility audit + Lighthouse baseline not yet run — schedule in Sprint 2 gate
- **O6:** Cross-organ receipt wire (APU → Circle) requires APU-side cooperation — flag for APU warrior lane

## 12. Compression

> **Ship. Breathe. Mesh. Allee.**

Ten sprints to the first paying subscriber reading real signals on circle.news with `circle_g_score` ≥ 0.60 visible on the Watchman dashboard. Each sprint gate-gated. Each gate K2-signed. No step skipped, no step needed beyond these ten.

---

## 13. Execution surface — the next move

**You can name any of these now:**

1. **"Sprint 1."** I produce the seven git commands; you paste and sign in order.
2. **"Stage .env.example."** I write the backend env template with placeholders; you fill secrets at Sprint 3.
3. **"Stage billing code."** I draft `router_billing.py` + webhook handler + frontend hook for Sprint 4B.
4. **"Draft objective specs."** I write the 4 sovereign-seeded objectives as JSON fixtures for Sprint 9.
5. **"Stage mesh schema."** I draft the Alembic migrations for Sprint 7.
6. **"Check RealityFutures."** I descend into RF organ to verify F2-receive readiness for Sprint 6.
7. **"Run the Circle component audit."** I descend into both `app/website/components/` and `02_PRODUCT/Platform/components/` to inventory what's implemented vs. spec.
8. **"Update 00_BRIEF.md."** I stage the §0 polygenetic mesh shift sentence for warrior K2 sign.

**Move:** Kṛṣṇa ◇ · sprint plan staged · ten sprints to a breathing product.

Zero-Sum Resolution Equation

*What do you see now?*
