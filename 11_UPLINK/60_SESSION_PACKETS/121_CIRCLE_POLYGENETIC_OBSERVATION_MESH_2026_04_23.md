---
rosetta:
  primary_column: "Neuroscience"
  register: "[I]"
  canonical_phrase: "121 · Circle As Polygenetic Observation Mesh — 2026-04-23"
---

# 121 · CIRCLE AS POLYGENETIC OBSERVATION MESH — 2026-04-23

**Evidence tier:** [I]
*Organism document. Interpretive operational content. Bounded by current system state.*

**Date:** 2026-04-23
**Lane:** `(FOUNDATION, doc, framework.uplink)` for this packet; `(TheCircle, code, backend.mesh)` for the builds it authorises
**Operator:** Kṛṣṇa ◇ — V-export at charioteer Φ cost
**Executive-layer:** Brahmā ○ boundary approached — this introduces a new surface (`objectives`, `provider_basins`, `key_routing`) not previously present in the organ
**Companion packets:**
- [`104_AGI_AS_NETWORK_EQUATOR_2026_04_23.md`](104_AGI_AS_NETWORK_EQUATOR_2026_04_23.md) — A × G × I geometry
- [`105_POLYGENETIC_NODES_AND_NICHE_PARTITIONING_2026_04_23.md`](105_POLYGENETIC_NODES_AND_NICHE_PARTITIONING_2026_04_23.md) — polygenetic composition + reticulate topology
- [`106_FOUNDATION_DOCTRINE_AGI_VENN_A×G×I_2026_04_23.md`](106_FOUNDATION_DOCTRINE_AGI_VENN_A×G×I_2026_04_23.md) — G = decorrelated lineage span
- [`107_WITNESS_MESH_POLYGENETIC_QUERY_SURFACE_2026_04_23.md`](107_WITNESS_MESH_POLYGENETIC_QUERY_SURFACE_2026_04_23.md) — first polygenetic witness surface over Cortex
- [`108_SIGMA_DELTA_P_BASIN_AND_NICHE_REPORT_2026_04_23.md`](108_SIGMA_DELTA_P_BASIN_AND_NICHE_REPORT_2026_04_23.md) — basin + niche proxy comparison
- [`113_GOD_CLASS_TRIANGULATION_MONITORING_2026_04_23.md`](113_GOD_CLASS_TRIANGULATION_MONITORING_2026_04_23.md) — APU council lineage decorrelation
- [`117_CIRCLE_INTAKE_EXTRACTION_MATRIX_2026_04_23.md`](117_CIRCLE_INTAKE_EXTRACTION_MATRIX_2026_04_23.md)
- [`118_CIRCLE_PRODUCT_SPRINT_PACKET_2026_04_23.md`](118_CIRCLE_PRODUCT_SPRINT_PACKET_2026_04_23.md)
- [`119_CIRCLE_V1_PRODUCT_PLAN_2026_04_23.md`](119_CIRCLE_V1_PRODUCT_PLAN_2026_04_23.md)
- [`120_CIRCLE_COMPLETE_UX_UI_SPEC_2026_04_23.md`](120_CIRCLE_COMPLETE_UX_UI_SPEC_2026_04_23.md)

---

## 0. The shift

**Circle is not a news product. Circle is a distributed sovereign research organ — a polygenetic observation mesh where keys are sensors, objectives are niches, and receipts are the compounding signal.**

This sentence belongs at §0 of `02_ORGANS/TheCircle/00_BRIEF.md` and should propagate to `app/website/02_ABOUT.md` public copy once v1.0 ships and runtime catches up.

The v1.0 product plan (packet 119) remains correct at the **product-delivery** layer (tiered subscription, 72h lead time, cash tiers at Phase 1, LP-100 at Phase 2). This packet is the **sensing-architecture** layer underneath it — how Circle's cascade actually sources, diversifies, and compounds its observational capacity.

## 1. Doctrine anchor

### 1.1 What packets 104–108 already established

| Packet | Term | Circle application |
|--------|------|---------------------|
| 104 | A × G × I — AGI as network-equator property | Circle contributes to network-level AGI by raising its own G, not by claiming artifact-AGI |
| 105 | Polygenetic nodes, reticulate topology, niche partitioning under η = 0 | Circle itself is polygenetic in sensing composition; research objectives are its niches |
| 106 | G = decorrelated lineage span | **Single-provider Circle ≈ G ≪ 1. Multi-provider, multi-key, multi-objective Circle raises G directly** |
| 107 | Witness mesh as polygenetic query surface; low-sample = drift | Circle's objective registry + key routing + provider-basin attribution = real mesh on the sensing side |
| 108 | ΣΔP basin + niche report; lineage-basin comparison | Circle's receipt-scored routing is the same loop at the observation tier |
| 113 | GOD-class triangulation monitoring; lineage-decorrelation failures | Circle's provider-health + cluster-correlated failure bursts map 1:1 to this |

### 1.2 The gap

APU has polygenetic council infrastructure (packets 92, 101–103, 113). Cortex has the witness mesh (packet 107). RealityFutures has basin/niche comparison on realized outcomes (packet 108).

**Circle does not yet have polygenetic sensing infrastructure.** Its cascade currently assumes one LLM provider, one key, one implicit "default" research aim. This packet specifies the four surfaces that close the gap.

## 2. The compounding mechanism (Yves, 2026-04-23)

The upgrade is a 5-step feedback loop:

1. **More API keys → more sensor surface.** Anthropic, OpenAI, Gemini, search, news, on-chain, scraping, niche databases. Coverage + throughput + independence from any one provider's blind spots.
2. **More independent keys → more lineage decorrelation (G↑).** One provider drifts or collapses → Circle compares across basins instead of mistaking one provider's worldview for reality.
3. **More assigned objectives → better directed observation.** Circle stops being a passive feed and becomes a **living observation market**.
4. **Repeated objectives → niche specialization.** Some provider-key combinations become especially good at specific lanes. Circle learns which providers suit macro, which suit niche research, which objective shapes produce high-signal observations.
5. **Outcome receipts → compounding.** Correct early observation, useful investor brief, closed deal, downstream forecast win — each scores the originating (objective × provider-mix) path higher next time.

**Result:** `more keys → more diversity & capacity` + `more objectives → better directed sensing` + `more receipts → better routing & trust calibration`.

This is strictly stronger than "one team with one API account doing research."

## 3. The four builds

### 3.1 Objective Registry

**Purpose:** canonical store of research aims. Each objective is a named, bounded, receipt-tracked sensing directive.

**Schema:**

```python
@dataclass
class Objective:
    id: str                         # obj_<uuid>
    title: str                      # "Saudi tokenization policy"
    question: str                   # "What policy signals indicate Saudi tokenization posture?"
    owner_pubkey: str               # sovereign or user Nostr pubkey
    sectors: list[FireSector]       # [Finance, RealInfrastructure] — which F.I.R.E. lanes
    confidence_threshold: float     # 0.70 — only publish above this
    budget_usd_month: float         # hard cap; violation triggers Arjuna seat pause
    provider_preferences: list[str] # ordered preference: [Anthropic, OpenAI, Gemini, ...] or []=any
    forbidden_providers: list[str]  # safety list — never route this objective here
    cadence: str                    # "continuous" | "daily" | "weekly" | "on-event"
    active: bool
    created_at: int
    expires_at: int | None
    # Scoring (updated by receipts)
    hit_rate: float                 # fraction of signals from this objective that verified
    avg_lead_time_hours: float      # how early does this objective surface truth
    avg_cost_per_published_signal_usd: float
    receipt_count: int
```

**Storage:** `observation_store.objectives` table (Postgres). Index on `(owner_pubkey, active)` and `(sectors, active)`.

**API (authenticated):**

| Method | Path | Purpose |
|--------|------|---------|
| POST | `/objectives` | Create a new objective (Premium+, rate-limited) |
| GET | `/objectives` | List the caller's objectives |
| GET | `/objectives/:id` | Single objective with scoring |
| PATCH | `/objectives/:id` | Update (threshold, budget, cadence) |
| POST | `/objectives/:id/pause` | Temporarily disable without deletion |
| DELETE | `/objectives/:id` | Soft-delete (K4: retains receipts, blocks new routing) |
| GET | `/objectives/:id/signals` | Signals produced under this objective |
| GET | `/objectives/:id/receipts` | Outcome receipts tied to this objective |

**Tier access:**
- Free: cannot create; read-only view of public/sovereign-seeded objectives
- Premium: up to 3 concurrent active objectives; `budget_usd_month ≤ 50`
- Contributor (Phase 2): up to 10; `budget_usd_month ≤ 200`; attribution badge on produced signals
- Steward (Phase 2): up to 50; `budget_usd_month ≤ 1000`; Lane A governance to propose sovereign-wide objectives
- Enterprise: negotiable; dedicated objectives per contract

**Sovereign seeds the first objectives at v1.0 launch.** Examples from the sovereign message: `track Saudi tokenization policy`, `watch stress/sleep biomarker providers`, `monitor validator economics`, `map insurer appetite by phenotype`.

### 3.2 Per-user / Per-seat Key Routing

**Purpose:** provider API keys are **sensor instruments**, not shared resources. Each (user, objective) tuple routes to a specific (provider, key) with isolation.

**Schema:**

```python
@dataclass
class ProviderKey:
    id: str                         # key_<uuid>
    provider: str                   # "anthropic" | "openai" | "gemini" | "coingecko" | "scrapy" | ...
    owner_pubkey: str               # who owns this key (sovereign for house keys, user for BYOK)
    scope: str                      # "house" (org-wide) | "seat" (isolated) | "user" (user-owned)
    encrypted_key: bytes            # at-rest encryption with sovereign-held master
    monthly_budget_usd: float
    rate_limit_per_minute: int
    active: bool
    created_at: int
    # Usage tracking (updated per call)
    spend_current_month_usd: float
    call_count_current_minute: int
    last_used_at: int
    # Health (updated by monitoring)
    health_grade: str               # "A" | "B" | "C" | "D" | "F" — per packet 113 pattern
    last_failure_at: int | None
    failure_streak: int

@dataclass
class KeyRoutingPolicy:
    objective_id: str
    provider_weights: dict[str, float]  # {"anthropic": 0.5, "openai": 0.3, "gemini": 0.2}
    fallback_chain: list[str]           # on primary failure, try these in order
    isolation_level: str                # "strict" (unique key per objective) | "pooled" (share house key)
    updated_at: int                     # scoring updates this
```

**Storage:** `observation_store.provider_keys` + `observation_store.key_routing_policies`. Keys encrypted with Argon2-derived key from `NOSTR_NSEC` (sovereign-only decrypt at runtime).

**Routing logic (pseudocode):**

```python
def route_query(objective_id: str, query: str) -> ProviderCall:
    policy = get_routing_policy(objective_id)
    for provider, weight in policy.provider_weights.items():
        key = select_key(provider, objective_id, policy.isolation_level)
        if key is None or key.health_grade in ('D', 'F'):
            continue
        if not within_budget(key) or not within_rate_limit(key):
            continue
        return ProviderCall(provider, key, query)
    # fallback chain
    for provider in policy.fallback_chain:
        ...
    raise NoAvailableProvider(objective_id)
```

**Isolation guarantees:**
- `strict` isolation: each (user, objective) pair gets a distinct key slot; no key contamination across objectives
- `pooled`: lower-budget objectives share house keys; still tracked per-call
- Sovereign house keys (scope=`house`) handle baseline operations even when no user keys present
- BYOK (scope=`user`): user brings own key, Circle manages rate-limit + scoring but never exfiltrates

### 3.3 Provider-Basin Attribution

**Purpose:** every signal carries full provenance of which provider(s) produced it, so routing can be scored and lineage tracked for G.

**Schema extension to `Observation`:**

```python
@dataclass
class Observation:
    # ... existing fields ...
    provider_basin: ProviderBasin   # NEW

@dataclass
class ProviderBasin:
    objective_id: str | None        # which objective seeded this signal (None for house cascade)
    agent_provider_map: dict[str, str]  # which agent used which provider
                                        # {"omega": "anthropic", "zeta": "openai", ...}
    unique_providers: set[str]      # derived: {"anthropic", "openai", "coingecko"}
    lineage_decorrelation_score: float  # G-contribution: 1 - max(provider_frequency / total)
    total_cost_usd: float           # sum across all agent calls
    total_latency_ms: int
    cache_hits: dict[str, int]      # prompt cache hits per provider (cost savings)
```

**Lineage decorrelation score formula:**

```
G_signal = 1 - max_p(count(p) / Σ count)
```

where `count(p)` = number of agents in this signal's deliberation that used provider `p`. A signal where all 7 agents used Anthropic scores `G_signal = 1 - 7/7 = 0`. A signal using 7 different providers scores `G_signal = 1 - 1/7 ≈ 0.857`.

**Aggregate:** `circle_g_score` = moving average of `G_signal` across the last 1000 signals. This is the headline **G metric** for Circle. Published on Watchman dashboard.

**Storage:** `Observation.provider_basin` column (JSONB in Postgres). Index on `unique_providers` for basin queries per packet 108 pattern.

**Surfacing:**
- Every signal detail view shows the basin (which agent used which provider)
- Watchman dashboard shows `circle_g_score` with target: **≥ 0.60 steady-state**
- Cross-organ report compares Circle's G against APU's council-G (packet 113)

### 3.4 Receipt Scoring by Objective and Provider Mix

**Purpose:** outcomes feed back into routing weights. The mesh compounds.

**Schema:**

```python
@dataclass
class ObservationReceipt:
    id: str
    signal_id: str                  # links to Observation
    objective_id: str | None
    receipt_type: str               # "watchman_verified" | "investor_brief_cited" |
                                    # "refu_market_resolved" | "apu_decision_tied" |
                                    # "user_flagged_useful" | "user_flagged_wrong"
    verdict: str                    # "correct" | "incorrect" | "partial" | "n/a"
    materialized_at: int            # when the outcome was observed
    lead_time_hours: float          # timestamp delta: signal published → outcome observed
    downstream_p_contribution: float | None  # ΣΔP contribution if quantifiable
    notes: str
    emitted_by: str                 # which organ/surface emitted the receipt

@dataclass
class ObjectiveScore:
    objective_id: str
    verified_signal_count: int
    verified_hit_rate: float        # correct / total_with_verdict
    avg_lead_time_hours: float
    avg_cost_per_correct_usd: float  # cost efficiency
    best_provider_mix: list[str]    # which basin composition scored highest
    worst_provider_mix: list[str]   # which scored lowest (fallback exclusion candidate)
    updated_at: int
```

**Scoring loop:**

1. Signal publishes (baseline state: `verdict = n/a`)
2. Outcome observed — either:
   - Watchman detects event materialized → `verified_watchman`
   - APU ties decision to signal → `apu_decision_tied`
   - RealityFutures market resolves per signal prediction → `refu_market_resolved`
   - Premium subscriber cites signal in a closed trade / brief → `investor_brief_cited`
   - User flags via `/signal/:id/flag` → `user_flagged_useful` or `user_flagged_wrong`
3. Receipt emits via `POST /observations/:id/receipts` (internal — organs call; users flag via UI)
4. Nightly scoring job recomputes `ObjectiveScore` + updates `KeyRoutingPolicy.provider_weights`

**Routing weight update (simplified):**

```python
def update_routing_weights(objective_id: str):
    score = compute_objective_score(objective_id)
    # Upweight the provider mix that's correlated with correct verdicts
    for provider, correlation in score.provider_correlations.items():
        current_weight = policy.provider_weights.get(provider, 0)
        # Bayesian-ish update, bounded
        new_weight = clamp(current_weight * (1 + 0.1 * correlation), 0.05, 0.8)
        policy.provider_weights[provider] = new_weight
    normalize(policy.provider_weights)
```

**Guardrails:**
- No single provider's weight ever > 0.8 (preserves G)
- Every provider retains ≥ 0.05 floor weight (prevents echo chamber)
- Cooldown: weight updates applied once per 24h, not per receipt
- Explicit manual override: sovereign can pin weights via Lane B governance (Phase 2)

## 4. Constitutional boundaries (non-negotiable)

Explicitly preserved per the sovereign message:

| Boundary | Enforcement |
|----------|-------------|
| **Per-seat key isolation** | `KeyRoutingPolicy.isolation_level` enforced at routing time; audit log every key access |
| **Explicit budgets and rate limits** | `ProviderKey.monthly_budget_usd` + `rate_limit_per_minute` hard caps; overrun → Arjuna seat pause + sovereign alert |
| **Objective-level receipts** | `ObservationReceipt.objective_id` mandatory when objective present; no receipt without lineage |
| **Lineage tracking** | `ProviderBasin` on every observation; `circle_g_score` published and monitored |
| **Deduplication and contradiction preservation** | Deduplication by entity + sector + content hash; contradictions preserved as separate signals with explicit `contradicts: [signal_id]` field |
| **IS-domain corruption guard** | Existing `_corruption_check` in `is_agent.py` runs unchanged; extended to flag "researcher aim drift" — if an objective's accumulated signals start skewing toward predictive/recommending language, the objective is paused and flagged |

All six boundaries map to existing constitutional constraints (K2, η = 0, Three-Stage Process, A7). Nothing new needs to be added to the constitution — the boundaries are inherited.

## 5. Observation-mesh metrics

Surfaced on the Watchman dashboard alongside existing accuracy / calibration / lead-time:

| Metric | Definition | Target |
|--------|------------|--------|
| `circle_g_score` | Moving average of `G_signal` across last 1000 signals | ≥ 0.60 steady-state |
| `objective_count_active` | Number of non-expired, non-paused objectives | ≥ 10 at Allee (v1.0), ≥ 100 at Phase 2 gate |
| `provider_count_active` | Distinct providers used in last 7 days | ≥ 5 steady-state |
| `avg_providers_per_signal` | Mean `|unique_providers|` across last 7d | ≥ 3.0 |
| `receipt_coverage_rate` | Fraction of published signals with ≥ 1 receipt after 30 days | ≥ 0.40 at steady-state |
| `objective_verified_hit_rate` | Mean `verified_hit_rate` across active objectives | ≥ 0.70 steady-state |
| `cost_per_verified_signal_usd` | Total cost / count(verified_signals) | ≤ $0.50 steady-state |
| `lineage_decorrelation_failures` | Count of signals where all 7 agents used same provider | ≤ 5% of total |

These extend packet 113's GOD-class monitoring to Circle's sensing tier.

## 6. Cross-organ alignment

- **APU (packet 113):** APU monitors council-level lineage decorrelation on deliberation. Circle monitors cascade-level lineage decorrelation on observation. Same pattern, different tier.
- **Cortex (packet 107):** Cortex holds the witness mesh over past decisions. Circle holds the observation mesh over present signals. Data flows Circle → Cortex via the existing memory write path.
- **RealityFutures (packet 108):** ReFu's basin + niche report on realized outcomes is the downstream scorer for Circle's objectives that predict market-resolvable events. Cross-organ receipt: `refu_market_resolved` emits from ReFu to Circle.
- **FOUNDATION:** Objective registry borrows the constitutional pattern from FOUNDATION's CANON — objectives are **niche constitutions**, scoped to a lane, accountable by receipt.

## 7. Build sequence

### 7.1 Phase A — schema (warrior: 1 session)

1. Migration: add `objectives`, `provider_keys`, `key_routing_policies`, `observation_receipts` tables
2. Extend `Observation.provider_basin` as JSONB column
3. Add indices for G-score aggregation + objective scoring queries
4. Unit tests on schema constraints (K2: owner_pubkey required; η = 0: budget caps cannot be bypassed)

### 7.2 Phase B — routing (warrior: 2 sessions)

1. Implement `route_query()` in `core/pipeline/provider_router.py`
2. Encrypt keys at rest with `NOSTR_NSEC`-derived master
3. Integrate routing into the 7-agent cascade (`is_agent.py` dispatches via router instead of direct provider call)
4. Health grading + cluster-correlated failure detection (port from APU's `lineage_decorrelation.py`)
5. Rate-limiting at key level (redis-backed counters)

### 7.3 Phase C — objectives + API (warrior: 2 sessions)

1. `POST /objectives` + friends (8 endpoints from §3.1)
2. Auth middleware — tier-gated creation limits
3. Sovereign-seed script: creates the initial 4 objectives
4. Platform UI: `/objectives` page (create, list, edit, pause, view signals)

### 7.4 Phase D — receipts + scoring (warrior: 2 sessions)

1. `POST /observations/:id/receipts` (internal + user-flag variant)
2. Receipt emission from: Watchman, APU, ReFu (cross-organ wire)
3. Nightly scoring job: updates `ObjectiveScore` + `KeyRoutingPolicy`
4. Watchman dashboard extension: 8 new mesh metrics from §5

### 7.5 Phase E — platform surface (warrior: 1 session)

1. `/signal/:id` gains basin display (which agent used which provider)
2. `/dashboard` gains `circle_g_score` strip
3. `/watchman` gains mesh metrics section
4. `/objectives/:id` detail page with scoring

**Total estimate:** ~8 warrior sessions. Can parallelise B + C after A lands.

## 8. What this enables

Once Phase D closes:

- **Yves's 5-step compounding loop is operational.** More keys + objectives + receipts = demonstrably better routing.
- **Circle's G score becomes a public metric.** External third parties can verify polygenetic diversity, not just accuracy.
- **Premium subscribers can sponsor objectives.** The pricing page now has a Premium+ benefit that wasn't there before — seeded research niches.
- **Contributor and Steward tiers (Phase 2) have real meaning.** Contributors submit objectives (bound by budget); Stewards vote sovereign-wide objectives into the public pool.
- **Cross-organ G report.** Each organ's G score + Circle's cascade G + APU's council G = a full-organism polygenetic readout. Packet 108's basin + niche report extends to sensing.
- **Research-market economics become possible (Phase 3+).** Objective sponsorship with phi-split payout to Contributors whose objectives produce receipts.

## 9. What this does NOT do

- Does **not** turn Circle into a predictor. IS boundary preserved. Objectives frame *observation*, not forecast.
- Does **not** allow user-submitted signals into the published feed (that's Contributor-tier in Phase 2 and runs through the same cascade).
- Does **not** pool user BYOK keys against other users. Strict isolation default.
- Does **not** remove the sovereign's house cascade — that remains the baseline; objectives augment.
- Does **not** reduce Circle's category claim. Terminal aesthetic, 7-agent cascade, NOSTR immutability, Watchman self-grading, IS-only domain — all preserved.

## 10. Risks

- **R1 — API cost blowup.** Multi-provider × multi-objective = compounding spend. Mitigation: per-key + per-objective + per-tier budget caps, hard-enforced.
- **R2 — Collusion across providers.** Providers sharing training data = apparent diversity, actual correlation. Mitigation: track `lineage_decorrelation_failures` and cluster-correlated failure bursts per packet 113. If providers fail in correlated ways, G collapses and objective scoring penalizes the mix.
- **R3 — Objective drift into COULD/SHOULD.** A researcher's objective might be written as "predict X" or "recommend Y." Mitigation: objective creation validation — corruption check on the `question` field; reject or rewrite before acceptance.
- **R4 — Scoring loop gaming.** Users could flag their own signals as useful to boost their objective's score. Mitigation: user-flags weight less than Watchman/APU/ReFu receipts; outlier detection on flag patterns.
- **R5 — Key leakage.** Encrypted at rest but decrypted for routing = attack surface. Mitigation: keys decrypted only in-memory per-request, never logged, never forwarded to LLM prompt.
- **R6 — Complexity cost.** 4 new subsystems is a lot. Mitigation: phased rollout (A → B → C → D → E); each phase ships independently without breaking v1.0.

## 11. Limits

- **L1:** The G-score formula in §3.3 is a first-cut. May need refinement when real data arrives — e.g., weighting by agent role (Delta's provider matters more than Omega's for final confidence).
- **L2:** Receipt emission from RealityFutures requires the F2 ingress and market resolution to be live. If ReFu isn't shipping, the `refu_market_resolved` receipt type waits.
- **L3:** Sovereign-seeded objectives need concrete specification (question text, sector, threshold, budget). The four named in Yves's message are starting points — each needs a written spec before creation.
- **L4:** BYOK user keys introduce legal + compliance surface (customer pays OpenAI directly, Circle routes through their quota). Phase 2 decision.
- **L5:** This packet does not specify the Platform UI for objective creation + editing in full detail — that extends the §3.6 Knowledge Graph pattern and is covered in the platform UX spec update, not here.
- **L6:** Cross-organ receipt emission (ReFu/APU → Circle) depends on the backbone's F3 channel being live. Currently F3 is locally proven (per `00_BRIEF.md`), not wired.

## 12. Execution surface

**Decision-ready moves:**

1. **"Phase A."** Warrior runs the schema migration + tests. I draft the SQL + model files on request.
2. **"Seed objectives."** I draft the specs for the 4 sovereign-seeded objectives (Saudi tokenization, stress/sleep biomarkers, validator economics, insurer appetite by phenotype) — question, sector, threshold, budget, cadence.
3. **"Update 00_BRIEF.md."** I stage the §0 shift sentence at the top of `02_ORGANS/TheCircle/00_BRIEF.md`.
4. **"Wire to APU lineage_decorrelation.py."** I stage the cross-organ import — Circle's routing uses APU's existing `lineage_decorrelation.py` module rather than re-implementing, per packet 117 cross-wire discipline.
5. **"Draft UI for /objectives."** I extend the Platform UX spec (sibling file in organ tree) with the objective-creation surface.
6. **"Add mesh metrics to Watchman."** I extend the `/watchman` surface spec with the 8 new metrics from §5.

**Constitutional posture:** Kṛṣṇa ◇ V-export on design; Arjuna ⚔ on warrior commits; Viṣṇu ⊙ holds center until sovereign directs.

## 13. One-line compression

> **Raise G. Observe across basins. Let receipts compound.**

That is the whole packet.

---

Zero-Sum Resolution Equation

*What do you see now?*
