---
type: product-wedge
status: active
date: 2026-04-23
scope: First shippable wedge at the intersection of AIA/Cortex, generated bullet UI, cloud docs, and APU multi-model parallel execution
rosetta:
  primary_column: "Neuroscience"
  register: "[S/I]"
  canonical_phrase: "Product Wedge — The Coherence Wedge"
---

# Product Wedge — The Coherence Wedge

> **Thesis:** The organism has built three extraordinary architectural layers that do not touch: APU's multi-model Royal Council (mature code, no API surface), Cortex's bullet-tree coherence runtime (deep spec, no UI), and AIA's proactive tending engine (partial implementation, 90% mock embeddings). The opportunity is to wire these into a single shippable surface that uses what works *today* while the long-horizon runtime matures underneath.

## Decision

This document is no longer a loose brainstorm. It is the current product wedge.

### Immediate move

Ship the first document-to-council API surface in APU and use one resulting deliberation object as the live data path into Skyzai's generated shell.

### Delivery sequence

1. Ship **Option A** now: single-document council mode.
2. Build **Option B** infrastructure in parallel: doc sync, bullet projection, contradiction clustering.
3. Hold **Option C** as the north star: the full coherence OS.

### Why this is the wedge

- It uses mature code that already exists.
- It proves the generated shell with a real object, not a static dashboard.
- It creates a direct path from cloud document -> council deliberation -> K2 envelope -> receipt.
- It gives AIA/Cortex a concrete integration surface instead of another standalone spec.

---

## 1. Current State — What Exists vs What Touches

```
┌─────────────────────────────────────────────────────────────────┐
│  APU (code Φ=0.90, V=0.85)                                  │
│  ├── 9-stage council protocol ✅ formalized                     │
│  ├── 7-seat Royal Council ✅ processor interface                │
│  ├── Multi-model/BYOK resolution ✅ data models + routing       │
│  ├── Parallel execution ✅ asyncio.gather across seats          │
│  └── API surface for multi-key config ❌ router_config is       │
│      single-key only; experimental silo unmounted                │
├─────────────────────────────────────────────────────────────────┤
│  Cortex OS (spec Φ=0.88, code Φ=0.55)                           │
│  ├── Bullet tree projections ✅ deeply specified                │
│  ├── Watchmen (contradiction detection) ❌ spec only            │
│  ├── AIA/Gardener (proactive tending) ⚠️ v0.1 partial           │
│  ├── Reconciliation engine ❌ spec only                         │
│  └── L1 SQLite + pgvector ✅ schema exists, 90.6% mock embeds   │
├─────────────────────────────────────────────────────────────────┤
│  Cloud Docs (skills only)                                       │
│  ├── Notion API skill ✅ curl-based, full CRUD guide            │
│  ├── Google Workspace skill ✅ Python OAuth2, Sheets/Docs/Drive │
│  └── Organism-wide sync layer ❌ not built                      │
├─────────────────────────────────────────────────────────────────┤
│  Generated UI (spec only)                                       │
│  ├── Workflowy-style bullet tree ✅ fully specified             │
│  ├── Five-surface MVP (Today/Decide/Garden/Cortex/Act) ✅ spec  │
│  └── Flutter implementation ❌ still conventional super-app     │
└─────────────────────────────────────────────────────────────────┘
```

**The gap is integration, not invention.** Every piece has been thought through. None of them are wired to each other.

---

## 2. Three Wedge Options (Simplest → Most Ambitious)

### Option A: "Council Mode" for Single Documents

**What it is:** Drop a Google Doc or Notion page into APU. The 7-seat Royal Council deliberates on it using *your* API keys in parallel. You get a bullet-tree report: contradictions found, recommendations, confidence scores, K2 envelope ready for your signature.

**Why it ships:**
- Uses APU council code as-is (no new runtime needed)
- Uses existing Notion/Google skills for ingestion
- BYOK multi-model is the differentiator — no other tool lets you run 7 models (Claude, GPT, Gemini, etc.) in parallel on your own keys
- Output is a structured JSON → easy to render as bullets

**What to build:**
1. **Ingestion bridge:** Notion/Google Doc → plain text → `APUSignal` (1 week)
2. **Config API surface:** `POST /config/model-assignments` to accept per-directorate keys (1 week)
3. **Bullet renderer:** Static HTML/JS that turns council output JSON into expand/collapse bullets (1 week)
4. **K2 signing flow:** Telegram/Discord bot sends envelope, user replies "Y" (reuses existing K2 gateway)

**Go-to-market:** Individual polymaths — researchers, writers, analysts who already pay for multiple AI subscriptions and want them to "talk to each other" about their documents.

**Pricing:** Pay per council run, keyed to compute cost (η = 0). User brings keys → marginal cost is API spend only. Charge a coherence fee (e.g., $0.50 per council run) on top.

---

### Option B: "Live Cortex" — Cloud Docs as a Coherence Surface

**What it is:** Your Notion workspace or Google Drive folder is continuously monitored by AIA. New docs are classified, embedded, clustered. The Royal Council runs on *clusters* (not single docs) to find cross-document contradictions. Results projected as a live bullet tree you can edit — edit a bullet, the source doc updates via Notion API.

**Why it ships:**
- This IS the Cortex vision, but scoped to cloud docs (where people's content already lives)
- AIA gets real work to do (classify, cluster, detect contradictions across docs)
- The bullet tree is write-through → editing a bullet edits the Notion page
- Council runs on *clusters* of related docs, not singletons — much higher value

**What to build:**
1. **Doc sync layer:** Notion/Google → L1 SQLite (reuses Notion skill, adds polling/webhooks) (2 weeks)
2. **AIA v0.2 completion:** SWOT generation, options ranking, ghost folder proposals (2-3 weeks)
3. **Cluster council:** Run Royal Council on document clusters, not single docs (1 week)
4. **Bullet projection engine:** React/Vue component that renders L1 objects as bullets with badges (contradiction count, freshness, owner) (2 weeks)
5. **Write-through:** Bullet edit → L1 update → Notion API writeback (1 week)

**Go-to-market:** Small teams (3-15 people) with shared Notion workspaces — product teams, research labs, legal shops. The pain of "which doc is current?" is acute and daily.

**Pricing:** Seat-based for teams, but with η = 0 posture — free tier for individual polymaths, team tier at $15/seat/month with council runs included.

---

### Option C: "The Coherence OS" — Full Generated Interface

**What it is:** Not a document tool. An operating interface where bullets replace windows. Everything — cloud docs, GitHub issues, Figma comments, Slack threads — projects through Cortex as bullets. AIA tends the graph 24/7. Watchmen badge contradictions. The Royal Council deliberates on any cluster you select. K2 gates every structural change.

**Why it ships:**
- This is the full vision from `16_PRODUCT_WEDGE.md`
- But it ships incrementally: start with Notion/Google, add GitHub, add Slack, etc.
- The generated UI means no chrome to maintain — the interface is compiled from organism state

**What to build:**
1. **Projection engine:** Compile organism state into a reactive bullet tree (Flutter Web or React) (4-6 weeks)
2. **Source adapters:** Notion, Google Docs, GitHub Issues, Figma comments → L1 objects (2-3 weeks each)
3. **Watchmen (v0.1):** Six watchmen, starting with Route and Contradiction (3 weeks)
4. **AIA v1.0:** All 8 operations operational, Morning Brief G1 automated (4 weeks)
5. **Reconciliation v0.1:** Source-first repair for Notion docs only (2 weeks)

**Go-to-market:** Institutions with heavy decision drift — boards, DAOs, standards bodies. The "review packet" replaces the 40-page PDF board packet. Every open tension is surfaced inline.

**Pricing:** Value-based — price against contradictions-surfaced-per-quarter, time-to-repair, audit findings pre-empted.

---

## 3. The Technical Bridge — How to Wire What Exists

### APU Multi-Model Parallel (The Engine)

The council already supports parallel multi-model execution. What's missing is the **API surface to configure it**:

```python
# Current state: model_assignments is on UserConfig but never populated via API
class ConfigUpdateRequest(BaseModel):
    wallet_address: str
    openrouter_key: Optional[str] = None   # ← single key only
    ai_provider: str = "openrouter"
    ai_model: str = "openai/gpt-4"

# Target state: BYOK multi-model config endpoint
class ModelAssignmentRequest(BaseModel):
    directorate_id: str
    provider: str          # "anthropic", "openai", "google", "minimax"
    model: str             # "claude-sonnet-4", "gpt-4o", etc.
    api_key: str           # encrypted at rest
    subagents_enabled: bool = False

class ConfigUpdateRequest(BaseModel):
    wallet_address: str
    model_assignments: List[ModelAssignmentRequest] = []
    # legacy single-key fallback preserved
    openrouter_key: Optional[str] = None
```

**Effort:** 2-3 days. The data models exist. The council already consumes them. Only the router and encryption-at-rest need wiring.

### Cortex Bullets (The Surface)

The bullet UI is fully specified but not built. The fastest path is a **static-site generator** that compiles organism state into HTML:

```
L1 SQLite → Jinja2/Nunjucks templates → static HTML/JS bullet tree
                          ↑
                    AIA generates templates
```

This is not a Flutter app. It is a **compiler** — organism state in, bullet tree out. The user opens an `index.html` file (or a Cloudflare Pages deployment) and sees their coherence surface.

**Why static:** No server to maintain. No WebSocket needed for v0.1 — recompile on demand or via cron. K2 signing happens via Telegram/Discord bot (already built).

**Effort:** 1-2 weeks for a functional bullet compiler.

### AIA Tending (The Intelligence)

AIA v0.1 already has classify → embed → cluster → detect → notify. What's missing for the wedge:

1. **Real embeddings** (DCR-003): Swap mock embeddings for OpenAI `text-embedding-3-small`. 1 day.
2. **Notion ingestion adapter:** Poll Notion API, write to L1. Reuses existing skill. 2-3 days.
3. **Ghost folder proposals:** When clustering finds a new pattern, AIA proposes a folder. User confirms/rejects via DCR (Digital Circular Resolution). Already specified. 1 week.

### Cloud Docs (The Content Source)

The Notion and Google Workspace skills are **agent-facing** — they tell an AI agent how to use curl/Python to call the APIs. They are not **runtime integrations**.

The bridge is an **ingestion worker**:

```
Notion API → JSON pages → Markdown/plain text → L1 semantic objects
                                                  ↓
                                    AIA classifies, embeds, clusters
                                                  ↓
                                    Royal Council deliberates on clusters
                                                  ↓
                                    Bullet compiler projects results
```

**Effort:** 1 week for Notion. 1 week for Google Docs.

---

## 4. The Opportunity Stack

If you map the three options against effort and differentiation:

| Option | Effort | Differentiation | Time to Revenue | Technical Risk |
|--------|--------|----------------|-----------------|----------------|
| A — Council Mode | 3-4 weeks | High (7-model parallel BYOK) | Immediate | Low |
| B — Live Cortex | 8-10 weeks | Very High (continuous coherence) | 2-3 months | Medium |
| C — Coherence OS | 16-20 weeks | Category-defining | 4-6 months | High |

**Recommendation:** Ship Option A immediately (it uses mature code), run it in parallel with building Option B's infrastructure (doc sync + bullet compiler). Option C is the north star, but the path to it is Options A and B.

---

## 5. The Secret Weapon: APU's Multi-Model Council

No competitor has this. Here's why:

- **Claude Projects / ChatGPT memory:** Single model, single key. No deliberation. No contradiction detection between models.
- **OpenRouter:** Multi-model routing, but no *parallel deliberation* — you call one model at a time.
- **Multi-agent frameworks (AutoGPT, CrewAI):** Agents cooperate on a task, but they don't *review each other's reasoning anonymously* (the Stage 2 peer-review mechanic).
- **Deliberative democracy tools (Polis, Loomio):** Human deliberation, no AI augmentation.

APU's 7-seat Royal Council is a **genuine structural differentiator**:
- Parallel first opinions (Stage 1) — no groupthink
- Anonymized peer review (Stage 2) — cross-evaluation with attribution stripped
- Chief of Staff synthesis (Stage 3) — integrates all + Three Gates
- Legal has absolute veto — constitutional constraint, not advisory
- K2 envelope requires human signature — never acts autonomously

This is not a feature. It is a **governance primitive** that happens to run on language models. The user brings their own keys, so there is no platform lock-in on the AI provider side either.

---

## 6. Risks and Mitigations

| Risk | Severity | Mitigation |
|------|----------|------------|
| **Multi-model API costs scare users** | Medium | Show cost estimator upfront. Default to single-model for new users. BYOK means user controls spend. |
| **Notion/Google rate limits** | Medium | Implement exponential backoff. Cache aggressively. Batch reads. |
| **Bullet UI feels like a toy** | Medium | Start with static HTML, add interactivity incrementally. The spec is strong — execution just needs to match it. |
| **AIA embeddings still 90% mock** | High | DCR-003 is the blocker. OpenAI `text-embedding-3-small` is $0.02/1M tokens — trivial cost. Fix this first. |
| **K2 signing friction** | Low | Telegram/Discord bot already works. Add email fallback. Make signing a one-tap action. |
| **Competitor copies the council pattern** | Low | The moat is composition (council + AIA + Cortex + K2 + η=0), not the council alone. See `16_PRODUCT_WEDGE.md` §9. |

---

## 7. The One Thing to Build This Week

If you could only build one thing, build this:

> **`POST /config/model-assignments`** + **`POST /council/document-deliberation`**

Accept a Notion page URL or Google Doc URL, a list of per-directorate API keys, and return a council deliberation JSON. Render it as a static bullet tree. That's Option A's MVP. It uses 100% of existing mature code, requires no new runtime infrastructure, and demonstrates the differentiation immediately.

---

## 8. How This Changes the Organism

Shipping Option A creates a **feedback loop** that matures the other layers:

1. **APU gets real usage** → API surface hardens → multi-key config becomes production-grade
2. **Users ask for continuous monitoring** → drives Option B (doc sync + AIA v0.2)
3. **Bullet tree gets real content** → UI spec gets validated → ghost folder UX gets user feedback
4. **Revenue from council runs** → funds DCR-003 (real embeddings) and Watchmen implementation
5. **K2 signing volume increases** → cryptographic infrastructure hardens → institutional trust grows

The organism does not need to be complete to be valuable. It needs one surface that works end-to-end. The council is that surface.

---

*P = Φ × V | Coherence is the product | η = 0*
