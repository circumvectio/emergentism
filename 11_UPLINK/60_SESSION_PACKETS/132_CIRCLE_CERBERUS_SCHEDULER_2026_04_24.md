---
rosetta:
  primary_column: "Liberal art"
  register: "[I]"
  canonical_phrase: "132 · Circle Cerberus Scheduler — The Autonomic Nervous System · 2026-04-24"
---

# 132 · CIRCLE CERBERUS SCHEDULER — THE AUTONOMIC NERVOUS SYSTEM · 2026-04-24

> *Originally staged as packet 126; renumbered to 132 after slot collisions (126 = QNTM (the institutional MPC/ZK-Identity rail) rename audit; 129 = Triadic Engine; 130 = Boundary Audit; 131 = D4 Body Opens D5).*
>
> **Walks the Triadic Cascade** (packet 129): ingest (Beauty / Grammar / Induction / in time) → route (Truth / Logic / Deduction / above time) → serve (Justice / Rhetoric / Abduction / against time) → cascade receipt closes back to ingest at higher resolution. Cerberus is the autonomic surface at which the recursion runs in Circle's runtime. η = 0 read grammatically per packet 129 §6: the turn is structurally lossless, not merely free of commercial rent.

**Evidence tier:** [I]
*Organism document. Interpretive operational content. Bounded by current system state.*

**Date:** 2026-04-24
**Lane (this packet):** `(FOUNDATION, doc, framework.uplink)` for staging; `(TheCircle, architecture, backend.cerberus)` for the builds this authorises
**Operator:** Kṛṣṇa ◇ — V-export at charioteer Φ cost
**Executive-layer:** Brahmā ○ boundary approached (new surface: Cerberus scheduler organ beneath the Three-Stage Process). New surface justified by explicit sovereign Vision evolution 2026-04-24.
**Companion packets (load-bearing):**
- [`121_CIRCLE_POLYGENETIC_OBSERVATION_MESH_2026_04_23.md`](121_CIRCLE_POLYGENETIC_OBSERVATION_MESH_2026_04_23.md) — mesh doctrine (extended by §3.3 of this packet)
- [`122_CIRCLE_V1_UNIFIED_SPRINT_PLAN_2026_04_23.md`](122_CIRCLE_V1_UNIFIED_SPRINT_PLAN_2026_04_23.md) — Sprints 7–10 enlarged per §15 of this packet
- [`123_CIRCLE_PRODUCT_SYNTHESIS_2026_04_24.md`](123_CIRCLE_PRODUCT_SYNTHESIS_2026_04_24.md) — 7-door product synthesis (Vision update here extends Doors 2 + 5 + 6)
- [`124_CIRCLE_V1_COMPLETE_WORK_PLAN_2026_04_24.md`](124_CIRCLE_V1_COMPLETE_WORK_PLAN_2026_04_24.md) — runway (extended per §15)
- [`125_CIRCLE_BRAND_COMPLIANCE_AUDIT_2026_04_24.md`](125_CIRCLE_BRAND_COMPLIANCE_AUDIT_2026_04_24.md) — brand audit
- **Session brainstorm 2026-04-24** — Vision evolution (OSINT · Human AI Cerberus · executive brief) + sovereign doctrine extensions on resource allocation and event-driven ingestion

---

## 0. The shift

This packet crystallises the 2026-04-24 session doctrine. Three load-bearing additions to the Circle architecture:

1. **Vision evolution.** Circle is being built as *"the most powerful OSINT network with human AI Cerberus in the world."* Product unit = executive brief (PDB-style) with timeline establishment + interpretation. ICP extends up-market from cross-sector analyst (packet 123) to C-suite / flag rank / head-of-state brief consumers.

2. **N=1 viability.** Circle must work with one sovereign + one API key + Nexus identity + API PAY. Network effects compound — every new user contributes keys + objectives, raising G-score + brief quality for every existing user. The mesh is **user-scale**, not just provider-scale (extends packet 121).

3. **Cerberus scheduler organ.** Beneath the Three-Stage Process, a new autonomic layer that ingests events, triggers cascades, and allocates resources across provider pool × user pool × time. Event-driven (not cron) → efficient at N=1, still effective at N=1000.

---

## 1. Vision integration

### 1.1 Vision

> **Circle: the most powerful OSINT network, governed by Human AI Cerberus.**

### 1.2 Mission

> **Useful for 1 user with 1 API key. Compounding for every user as the network grows.**

### 1.3 Product form (extends packet 123 Door 1)

Morning brief. PDB-style. Not a feed of cards. Structure:

- **Bottom Line Up Front** — 2–4 sentences, decision-grade
- **Timelines** — one per tracked objective, with dated events, evidence tier inline, provider basin footnote
- **Facts not yet connected** — cooling signals that may become timelines
- **Failures disclosed** — this week's verified-wrong signals (link to `/trust`)

Every brief carries basin metadata: *"This brief cost $0.47 across 3 providers · G=0.58 · 12 triggers fired · 0 wasted polls."*

### 1.4 ICP (extends packet 123 §1)

Primary: cross-sector analyst at $99/mo (packet 123 stays valid). Add an upper tier:

- **Executive tier** — C-suite, fund CIO, strategic advisor to state-scale principal. $499–$2,500/mo. Delivers morning brief formatted for decision-makers. White-glove objective curation with sovereign-supervised tuning.

Secondary and tertiary ICPs unchanged.

---

## 2. Cerberus — brand + architecture

### 2.1 Mythic reading (ratified)

Cerberus is the three-headed guardian at the threshold. Reading E of packet 125 §brainstorm is ratified:

**Cerberus is the scheduler-organ.** Three heads, one function:

| Head | Watches | Decides |
|---|---|---|
| **Ingest-head** | subscriptions + trigger rules | *is there something new worth seeing?* |
| **Route-head** | provider pool + rate limits + budgets | *who processes it, how expensively?* |
| **Serve-head** | user portfolio + objective priorities + fairness | *whose brief does this signal enter?* |

Human sits above all three heads — K2 can audit any dispatch, pause rules, rotate keys, revoke keys. "Human AI Cerberus" = AI schedules, human audits.

### 2.2 Brand surface

Cerberus is **not a product name** and **not a rebrand of the Trinity**. The Trinity (TheCircle · RealityFutures · Skyzai.BOT) stays. Cerberus is the **trust + sovereignty** overlay:

- `/trust` page carries the Cerberus name as the audit surface brand
- Every brief footer includes "Cerberus · [dispatch count] this session"
- The scheduler organ in code is named `cerberus/` in the backend tree
- No Cerberus logo yet — brand guide v2.1 seal (the inner lattice) remains canonical

### 2.3 Constitutional fit

Cerberus **does not violate** the IS-only Three-Stage Process boundary. It decides *when* and *how* to observe. It does not decide *what to conclude*. The corruption_check fires downstream in the cascade per `is_agent.py` — unchanged by this packet.

K2 authority is extended: every Cerberus dispatch decision is audit-logged with a K2-compatible signature (service-account for automated dispatch; sovereign-signed for manual override).

---

## 3. Three-layer autonomic mesh

### 3.1 Layer 1 — Subscription Workers (`cerberus-subs`)

**Responsibility:** maintain durable connections to the outside world; normalise incoming events into `RawEvent`; dedupe.

**Process model:** one supervisor process + N async worker coroutines (one per active subscription). Stateful — subscriptions persisted in Postgres. Watchdog restarts dead workers.

**Per-source worker contracts:**

| Source | Library | Mechanism |
|---|---|---|
| RSS / Atom | `feedparser` + `aiohttp` | ETag + Last-Modified; WebSub subscription if advertised |
| WebSub push | `aiohttp` receiver at `/webhook/websub/:feed_id` | HMAC-verify → normalise → Redis Stream |
| Nostr | `websockets` + `nostr-sdk` | Persistent subscription; auto-reconnect; dedupe by event id |
| On-chain | `web3.py` async subscribe OR indexer webhook | Filter by contract + topic + value |
| Adaptive poll | `aiohttp` + DOM-diff | Polling interval auto-tunes to velocity |
| Webhook in | FastAPI subrouter on `circle-api` | Signature-verified; enqueues RawEvent |

**Adaptive polling algorithm:**

```
next_poll_at = now + clamp(30s, base_interval / velocity_score, 1h)
velocity_score = exp_moving_avg(events_per_poll, α=0.3)
```

Hot source (high velocity) → polls every 30s. Quiet source → every hour. Self-tunes. Bounded both ends.

**State:** `subscriptions` + `subscription_heartbeats` tables. Subscription survives restarts.

**Scale:** one process handles ~500 active subscriptions on CX22. Horizontal split by `hash(subscription_id) mod N` at scale.

### 3.2 Layer 2 — Trigger Engine (`cerberus-trigger`)

**Responsibility:** evaluate trigger rules against RawEvents; emit DispatchRequests when rules fire; enforce cooldowns + fairness.

**Process model:** stateless consumer of `circle.raw_events` Redis stream. Horizontally scalable.

**Rule schema:**

```python
@dataclass
class TriggerRule:
    id: str
    objective_id: str
    source_type: Literal["rss","nostr","imageboard","onchain","scraped","webhook"]
    source_id: str
    threshold_kind: Literal["keyword","velocity","value","always"]
    threshold_params: dict
    dispatch_priority: Literal[0,1,2,3]
    cooldown_sec: int
    active: bool
```

**Cooldown lock (atomic, Redis):**

```python
async def try_fire(rule_id: str, entity: str, ttl: int) -> bool:
    key = f"cooldown:{rule_id}:{entity}"
    return await redis.set(key, "1", nx=True, ex=ttl)
```

**Priority bands:**

| Priority | Source |
|---|---|
| 0 — immediate | cross-organ receipts (APU, RF), sovereign-flagged, exec-tier objectives |
| 1 — high | Premium objectives, velocity bursts, breaking events |
| 2 — normal | standard triggers (RSS updates, slow Nostr) |
| 3 — background | house-cascade, backfill, sovereign-seeded baseline |

Each band = its own Redis stream. Scheduler consumes 0 before 1 before 2 before 3.

**Fairness filter:** no single user monopolises priority 1. Round-robin within band + weighted by tier (Executive 3× Premium 2× Contributor 1×).

### 3.3 Layer 3 — Cerberus Scheduler (`cerberus-scheduler`)

**Responsibility:** per DispatchRequest → allocate provider + key + user + timing + quality → emit `CascadeJob`.

**Core algorithm:**

```python
async def schedule(request: DispatchRequest) -> CascadeJob | None:
    obj = await objectives.get(request.objective_id)
    user = await users.get(obj.owner_pubkey)
    policy = await routing_policies.get(obj.id)

    for provider in weighted_shuffle(policy.provider_weights):
        key = await select_key(provider, user, obj, policy.isolation_level)
        if key is None or key.health_grade in ("D","F"):
            continue
        if not await rate_limiter.try_acquire(key.id, windows=["minute","hour"]):
            continue
        estimated = cost_estimate(provider, obj)
        reservation = await budget.try_reserve(key.id, user.id, obj.id, estimated)
        if reservation is None:
            continue
        model = resolve_model(provider, obj.quality_dial)
        audit_id = await audit.record(
            actor="cerberus-scheduler",
            action="dispatch",
            target=obj.id,
            k2_svc_sig=True,
        )
        return CascadeJob(
            dispatch_id=uuid4(),
            request=request,
            provider=provider,
            key_id=key.id,
            model=model,
            user_id=user.id,
            reserved_budget_cents=reservation.cents,
            k2_audit_id=audit_id,
        )

    await defer_queue.put(request, delay=backoff(request.attempt_count))
    return None
```

**Rate limiter** (sliding window, Redis sorted sets, atomic Lua):

```lua
ZREMRANGEBYSCORE key 0 (now - window_sec)
local current = redis.call('ZCARD', key)
if current < limit then
    redis.call('ZADD', key, now, uuid)
    return 1
end
return 0
```

**Key selection isolation modes** (extends packet 121 §3.2):

| Mode | Logic | Applies to |
|---|---|---|
| `strict` | dedicated (user, objective) key slot; never shared | Premium+, Exec-tier |
| `pooled` | shared among Free-tier house-cascade; per-user budget enforced | Free tier |
| `byok` | user's own key; skip house pool; rate-limit isolated | Premium+ BYOK |

**State:**
- Redis: rate counters (hot path), routing-policy cache (60s TTL), defer queue
- Postgres: budget ledger, audit trail

---

## 4. Data model (v1.0 minimal — 13 tables)

```sql
users              (id, pubkey, tier, created_at, grace_exit_at)
subscriptions      (id, source_type, source_id, config_json, active, heartbeat_at)
trigger_rules      (id, objective_id, source_id, kind, params_json, cooldown_sec, priority, active)
objectives         (id, owner_pubkey, title, question, sectors[], threshold,
                    budget_cents, provider_prefs[], cadence, quality_dial, active, scoring_json)
provider_keys      (id, provider, owner_pubkey, scope, encrypted_key,
                    monthly_budget_cents, rate_limit_per_min, health_grade, last_used_at)
routing_policies   (objective_id, provider_weights_json, fallback_chain[],
                    isolation_level, updated_at)
observations       (id, entity, sector, facts_json, confidence, evidence_tier,
                    sources[], provider_basin_json, nostr_event_id, created_at)
receipts           (id, signal_id, objective_id, kind, verdict,
                    lead_time_hours, emitted_by, at)
budget_ledger      (id, user_id, key_id, objective_id, amount_cents, kind, tx_id, at)
audit              (id, actor, action, target_id, k2_sig, at)
briefs             (id, user_id, date, payload_json, cost_cents, basin_summary_json)
watchlists         (user_id, entity, created_at)
user_keys_contrib  (user_id, key_id, contributed_at, discount_share, attribution_badge)
```

Postgres 16 with pgvector extension for future embedding work.

---

## 5. Message layer

### 5.1 v1.0 — Redis Streams

**Streams:**

| Stream | Producer → Consumer |
|---|---|
| `circle.raw_events` | subs → trigger |
| `circle.dispatch_requests.{0,1,2,3}` | trigger → scheduler (one per priority) |
| `circle.cascade_jobs` | scheduler → cascade runners |
| `circle.observations_written` | writer → SSE + Cortex + Watchman fan-out |

**Semantics:** at-least-once delivery. Idempotency via job uuid. Consumer groups per service. Acks on successful processing.

### 5.2 v2.0 upgrade path

Swap to NATS JetStream at N>100 users. Publish/consume abstraction in a shared library ensures interface stability — no producer or consumer code changes, only backing swap.

---

## 6. Key encryption + runtime flow

**Layered envelope:**

```
Master (sovereign-held)        NOSTR_NSEC
Derived (per-user)             ARGON2(NSEC || user_salt) → KEK
DEK (per-user)                 random 256-bit, wrapped with KEK
Key ciphertext                 AES-256-GCM(provider_key_bytes, DEK)
```

**Runtime decrypt flow:**

1. Scheduler emits CascadeJob with `key_id`
2. Cascade worker calls `key_vault.decrypt(key_id, requesting_service="cascade-worker")`
3. Vault verifies call is internal (mutual TLS or shared secret); unwraps DEK → key plaintext
4. Plaintext held in worker RAM for 60s max; never logged, never in prompt, never to disk
5. Worker calls provider using plaintext; clears on completion or timeout
6. Audit log: `action="key_decrypt", target=key_id, by=worker_id, at=...`

**Never:** plaintext in logs · prompts · env vars · disk · HTTP bodies.

**Upgrade path:** move KEK to Hetzner cloud HSM or AWS KMS at scale.

---

## 7. Effective-vs-efficient quality dial

Per-objective setting (Premium+). Default: **Efficient** (protects N=1 economics).

| Mode | Behaviour | Cost per signal | Use case |
|---|---|---|---|
| **Efficient** | Cheapest route that passes corruption_check. Haiku / Flash / small models for initial pass; escalate only on ambiguity | ~$0.01-0.05 | Background monitoring, Free + Premium baseline |
| **Balanced** | Mixed routing; premium models on interpretation step only | ~$0.10-0.30 | Most Premium objectives |
| **Effective** | Premium models (Opus / GPT-5 / Gemini Ultra) on every step | ~$0.50-1.50 | Executive-tier objectives, high-stakes signals |

Budget cap is the backstop regardless of dial position. Scheduler enforces reservation before dispatch.

Per-objective override: Premium user sets dial per objective. Sovereign-seeded objectives default Balanced; exec-tier brief cover stories default Effective.

---

## 8. N=1 → N=1000 capacity mechanics

### 8.1 Cost + cadence scaling

| Scale | Key pool | Cadence (typical) | Monthly cost | G-score target |
|---|---|---|---|---|
| **N=1** — sovereign alone | 1 Claude key | 3-6 observations/day | ~$15-30 | G=0 (single provider — honestly disclosed on /trust) |
| **N=10** — first cohort | 10 keys, 3-4 providers | ~50 observations/day distributed | ~$200-400 | G ≈ 0.40-0.55 |
| **N=100** — post-Allee | ~100 keys, 6+ providers | ~500 observations/day | ~$2,000-4,000 | G ≥ 0.60 |
| **N=1000** — Phase 2+ | ~1000 keys, 15+ providers | continuous across all objectives | ~$20,000-40,000 | G ≥ 0.75 |

Event-driven ingestion holds ~10× cost advantage at every scale vs. cron polling.

### 8.2 Capacity transparency

`/trust` page gains a **Capacity** section (new metrics per §11):

- Event firing rate last 24h
- Dispatch count last 24h
- Trigger-silence periods
- Cadence per active objective
- Current utilization % (dispatches ÷ theoretical max given key pool + rate limits)

Target utilization: **60–80% steady-state.** Below = waste. Above = bottleneck, prompt to add keys.

---

## 9. User-as-sensor economics

**The compounding mechanic.** Every new user with a provider key raises *every existing user's* brief quality. No user pays for their own observation capacity — they pay for access to the emergent pool.

### 9.1 Key contribution incentives (Phase 2+)

| Action | Economic reward |
|---|---|
| Contribute 1 Claude / OpenAI / Gemini key (BYOK into pool) | 10% Premium discount per month the key remains healthy |
| Contribute 1 rare / niche provider key (CoinGecko, Scrapy-seat, NewsAPI) | 15% discount + attribution badge |
| Contribute ≥ 3 distinct-provider keys | 25% discount + Contributor-tier preview |
| Key health drops to F / D for > 7 days | discount pauses until restored or replaced |

Keys contributed remain **user-owned** — can be rotated or revoked at any time. K4 Grace Exit: user revokes all contributions with one click; pool absorbs the capacity loss gracefully.

### 9.2 Phase-2 LP-100 share

Contributors who contribute keys AND produce public objectives with verified receipts earn LP-100 φ-split on their objective's signal-citation revenue. Mechanism details in packet 119 §Economics (superseded by future Phase-2 packet).

---

## 10. Deployment topology

### 10.1 v1.0 — single host, Hetzner CX22 (~€7/mo, 2 vCPU, 8 GB RAM)

```
docker-compose services              RAM budget
────────────────────                 ──────────
postgres                             1.5 GB     (pgvector extension)
redis                                0.5 GB     (streams + counters + cache)
cerberus-subs                        0.5 GB     (supervisor + asyncio workers)
cerberus-trigger                     0.3 GB
cerberus-scheduler                   0.5 GB
circle-cascade       × 1-2 instances 1.5 GB     (LLM I/O; hot path)
circle-writer                        0.3 GB
circle-api                           0.5 GB     (FastAPI + uvicorn)
circle-billing                       0.3 GB     (API PAY + OFN + Connect)
nginx + tls (certbot)                0.1 GB
                                     ─────
                                     ~6.0 GB used · 2.0 GB headroom
```

Single `docker-compose.yml`. `systemd` keeps it up. Hot restart per service.

### 10.2 v2.0 — scale-out (post-Allee, N>100)

| Tier | Migration |
|---|---|
| Compute | Cascade workers → separate node pool (heaviest load) |
| Database | Postgres → managed Hetzner DB or PlanetScale |
| Cache + streams | Redis → Redis Cloud / Upstash (durable) · NATS JetStream (streams) |
| Orchestration | Hetzner k3s or managed Kubernetes when N>500 |

**No v1.0 choice prevents v2.0.** Service boundaries survive the migration.

---

## 11. Observability

### 11.1 Stack

| Layer | Tool |
|---|---|
| Structured logs | Python `structlog` → stdout → JSON files + logrotate (v1.0) · Loki (v2.0) |
| Metrics | `prometheus-client` per service → single Prometheus scraper → Grafana |
| Traces | OpenTelemetry → Jaeger (optional v1.0; mandatory v2.0) |
| Audit | `audit` Postgres table, append-only, K2-signed |
| Alerts | Grafana Alertmanager → Slack / Telegram / Email |

### 11.2 Five critical Grafana dashboards

1. **Mesh health** — `circle_g_score`, providers active, lineage_decorrelation_failures, corruption_check pass rate
2. **Capacity** — events/min by source, dispatches/min by priority, cascade queue depth, utilization %
3. **Budget** — spend/day by user / provider / objective, headroom per key, tier-cap proximity
4. **Subscription health** — up/down by source, heartbeat latency, restart counts, adaptive-poll cadence distribution
5. **User experience** — brief generation latency p50/p95/p99, SSE connection counts, first-signal-time

### 11.3 Nine mesh metrics on `/trust` (public, extends packet 121 §5)

Packet 121 §5 listed 8 metrics; this packet adds one:

9. `capacity_utilization_7d` — target 60–80% steady-state · published as rounded band (low / moderate / high) to avoid capacity reverse-engineering

---

## 12. Testing strategy

| Layer | Pattern | Tool |
|---|---|---|
| Unit | rule matcher · rate limiter math · budget accountant · cost estimator · quality dial | pytest |
| Contract | Observation schema · Nostr Kind 31339 · API PAY webhook shape · OFN receipt | pytest + jsonschema |
| Integration | trigger → schedule → cascade → emit with mock provider | pytest + testcontainers (postgres, redis) |
| E2E | real RSS → real emitted signal · golden-path only | nightly CI |
| Chaos | kill random service mid-flight · verify recovery + no lost dispatches | `toxiproxy` + pytest |
| Load | N=100 users × 100 events/min · measure budget + latency | `locust` |
| Security | audit key never in logs · corruption_check cannot be bypassed | pytest + grep-in-logs |

---

## 13. Constitutional boundaries

All eight organism guards preserved:

| Guard | Enforcement in Cerberus |
|---|---|
| **K2** | Every dispatch records service-signed K2 audit entry. Key decrypt logged per call. Sovereign can inspect + revoke any key, pause any rule. |
| **η = 0** | Free tier remains real (pooled house-cascade). No user pays for observation capacity — all tiers pay for directed sensing. |
| **K4** | User revokes contributed keys with one click (`/account/keys/revoke`). Pool absorbs loss. Data export includes all dispatch audit entries. |
| **Three-Stage Process** | Scheduler decides *when*, not *what*. `corruption_check` unchanged on cascade emit. Rules themselves corruption-checked on creation (reject "predict/recommend"). |
| **A7** | Failed dispatches + wasted polls published on `/trust`. Accuracy / calibration tracked per quality-dial mode. |
| **Category** | Constitutional composition: Cerberus is the *scheduling organ* with publicly auditable fairness + diversity metrics, not a generic LLM router. No competitor ships this surface. |
| **Raktabīja** | Rule replication prevented: each rule has single canonical `trigger_rules` entry; no shadow copies. |
| **G** | `circle_g_score ≥ 0.60` steady-state; per-signal basin disclosed; lineage_decorrelation_failures monitored. |

---

## 14. Six design decisions — ratified 2026-04-24

| # | Decision | Ratified choice | Rationale |
|---|---|---|---|
| 1 | Service layout | **7 separate containers** | Clean fault isolation; scales independently; docker-compose trivial; v2.0 k8s migration preserves boundaries |
| 2 | Message backing | **Redis Streams v1.0 → NATS v2.0** | Lowest infra at v1.0; interface abstraction in shared lib preserves swap path |
| 3 | Key encryption | **NOSTR_NSEC-derived KEK** | Sovereign already holds NSEC; no new secret surface; HSM migration clean when scale demands |
| 4 | WebSub public endpoint | **Direct on `api.circle.news/webhook/websub/:id`** | Simplest v1.0; Skyzai Connect proxy available if sovereignty concerns grow |
| 5 | Billing integration | **Full API PAY SDK wrapper** | Required architectural dependency. Sovereign provides SDK surface doc pre-Sprint-4B |
| 6 | Quality dial default | **Efficient** with per-objective override | Protects N=1 economics; Premium+ user can override per-objective to Balanced or Effective |

---

## 15. Sprint integration — packet 122 extensions

Packet 122 Sprints 7, 8, 9 expand to absorb Cerberus scope:

| Sprint | Original scope | Cerberus addition |
|---|---|---|
| **Sprint 7** (mesh schema) | `objectives`, `provider_keys`, `key_routing_policies`, `observation_receipts` tables | **Plus:** `subscriptions`, `trigger_rules`, `audit`, `budget_ledger`, `user_keys_contrib` tables |
| **Sprint 8** (routing) | `core/pipeline/provider_router.py`, key encryption, cascade refactor | **Plus:** `cerberus-scheduler` service, `cerberus-trigger` service, rate-limit Redis module, budget accountant |
| **Sprint 8B (NEW)** — Ingestion | — | **New sprint:** `cerberus-subs` service, RSS/Nostr/on-chain workers, WebSub endpoint, adaptive poller |
| **Sprint 9** (objectives + API) | 8 CRUD endpoints, ObjectiveCreateModal, ObjectiveDetailPage | **Plus:** TriggerRule CRUD endpoints, trigger-rule builder UI, quality-dial setting on objective |
| **Sprint 10** (receipts + dashboard) | Watchman extended dashboard, cron scoring | **Plus:** Capacity section on `/trust`, capacity_utilization metric, cost-transparency footer on brief |

**Net addition: 1 new sprint (8B).** Total Sprints 1–10 → 1–11. Runway estimate grows by ~1 warrior session.

---

## 16. Cross-organ alignment

| Organ | Cerberus touchpoint |
|---|---|
| **APU** | APU council deliberation consumes Cerberus dispatch audit for provenance. APU `apu_decision_tied` receipts flow back to Cerberus scoring. |
| **RealityFutures** | RF market-resolution receipts close the scoring loop for predictable-event objectives. Market-creation uses Cerberus to select provider for RF's own signal consumption. |
| **Cortex** | Every Observation persisted via `circle-writer` also writes Cortex memory; Cerberus audit entries are part of the memory trace (for witness-mesh queries per packet 107). |
| **Skyzai Connect** | Auth middleware on `circle-api` verifies Nostr NIP-33 JWTs from Connect. User's Connect npub = user identity throughout Cerberus. |
| **API PAY** | `circle-billing` drives subscription + key-contribution discount via API PAY settlement; OFN receipts confirm every billing event. |

---

## 17. Risk register (Cerberus-specific, extends packet 124 §12)

| R | Risk | Sev | Mitigation |
|---|---|---|---|
| R-21 | Event storm overwhelms trigger engine | Med | Bounded priority streams; drop counter on low bands; sovereign-alert on overflow |
| R-22 | Provider key leaked via cascade prompt injection | Critical | Key plaintext never in prompt; runtime decrypt only; audit on every access |
| R-23 | Reply-velocity metric gamed by bot farms | Med | Cross-source corroboration required before emission; outlier detection; suspicious-source flagging on /trust |
| R-24 | User-contributed key malicious (bait-and-switch) | Med | Health grading; cluster-correlated failure detection (packet 113 pattern); auto-quarantine on anomaly |
| R-25 | Scheduler bottleneck at mid-scale | Med | Horizontal shard by `hash(objective_id) mod N`; staged migration plan in §10.2 |
| R-26 | N=1 signal-drought → brief becomes thin | Low | Sovereign-seeded baseline objectives fill. User can add more triggers. Brief honestly discloses thinness. |
| R-27 | WebSub hub rejection / unreachable | Low | ETag-efficient poll fallback per-feed; health metric per source |
| R-28 | API PAY congestion during subscription renewal peaks | Low | Exponential backoff; grace-period before downgrade; renewal-K2 prompts batch-schedulable |
| R-29 | K2 audit log grows unbounded | Low | Monthly archive to cold storage; hot query window 90 days; OFN hash-anchor of archive |
| R-30 | Cerberus name collision with unrelated products | Low | Internal service + audit surface only; not exposed as user-facing product name |

---

## 18. Execution surface — decision-ready moves

Sovereign can name any of these:

1. **"Approve packet 126"** — ratifies the architecture + six design decisions + sprint-scope additions. Unlocks Sprint 7 + 8 + 8B design work.
2. **"Stage Alembic migrations for 126 schema"** — I draft the 5 new tables for Sprint 7 per §4.
3. **"Stage `cerberus-scheduler/` skeleton"** — I write the Python module tree (routes, scheduler, rate-limiter, budget-accountant stubs) for Sprint 8.
4. **"Stage `cerberus-trigger/` skeleton"** — similar, for Sprint 8B.
5. **"Stage `cerberus-subs/` skeleton"** — RSS + Nostr + on-chain worker stubs.
6. **"Update packet 124"** — inline edit to add Sprint 8B, update §14 work-estimate table, add R-21-R-30 to §12.
7. **"Draft Trigger-Rule Builder UI"** — frontend component for Sprint 9 (Premium user creates rules).
8. **"Brand the `/trust` Cerberus surface"** — update `TrustSurfacePage.tsx` to display Cerberus audit metrics.
9. **"Draft API PAY integration spec"** — waits on sovereign SDK surface doc.

---

## 19. Limits

- **[I] Packet 126 is L5 Brāhmaṇa redesign.** The "no new design until Sprint-10 ships" rule from packet 124 §18 L1 yields here — the sovereign Vision update + explicit doctrine extension authorises a new packet. No further design packets accepted after this one until Sprint 10.
- **[S] API PAY SDK surface doc** remains the single external blocker for `circle-billing` scaffolding. Sovereign supplies or points to `02_ORGANS/Skyzai/execution/api_pay/` or equivalent.
- **[I] Cerberus brand rollout** (logo / mythic illustration in brand guide) is v1.1+ work, not v1.0. v1.0 uses the word "Cerberus" in the code, audit logs, and `/trust` surface only.
- **[S] "OSINT network" public claim** carries legal surface (intelligence-tradecraft norms, source protection, compartmentalisation). Legal counsel pre-check before public copy uses the phrase.
- **[I] Habitat ratification still pending.** If Habitat = A ∪ D (packet 123 §7.3), Cerberus identity surfaces route through Habitat. If Habitat ≠ A ∪ D, Cerberus owns identity natively. Post-packet-126 decision.
- **[I] Executive-tier pricing ($499-$2,500/mo) is my proposal.** Sovereign ratifies actual numbers; pricing is ☀️ lane.
- **[S] N=1000 economics** depend on provider-pricing evolution (2026-2027). Current estimates use 2026-04 rates; may shift materially.

---

## 20. Compression

> **Three heads. One organ. Human audits every dispatch.**
>
> Ingest · Route · Serve — the autonomic nervous system of the OSINT network.

Circle observes. Cerberus schedules. The human signs.

---

Zero-Sum Resolution Equation

*What do you see now? Which execution-surface number?*
