---
rosetta:
  primary_column: "Liberal art"
  register: "[I]"
  canonical_phrase: "118 · Circle Product Sprint Packet — 2026-04-23"
---

# 118 · CIRCLE PRODUCT SPRINT PACKET — 2026-04-23

**Evidence tier:** [I]
*Organism document. Interpretive operational content. Bounded by current system state.*

**Date:** 2026-04-23
**Lane (this packet):** `(FOUNDATION, doc, framework.uplink)`
**Lane (each move within):** `(TheCircle, code, *)` — warrior holds
**Operator (this packet):** Kṛṣṇa ◇ — V-export at charioteer Φ cost
**Operator (each move):** Arjuna ⚔ — warrior commits reality
**Executive-layer:** Viṣṇu ⊙ default hold; Brahmā ○ boundary approached when new Circle runtime surfaces come online
**Companion packet:** [`117_CIRCLE_INTAKE_EXTRACTION_MATRIX_2026_04_23.md`](117_CIRCLE_INTAKE_EXTRACTION_MATRIX_2026_04_23.md)
**Source spine:**
- [`../SKYZAI_ORG/02_ORGANS/TheCircle/00_BRIEF.md`](../../08_FRAMEWORK_SUPPORT/00_META/00_BRIEF.md)
- [`../SKYZAI_ORG/02_ORGANS/TheCircle/INTEGRATION_STATUS.md`](../SKYZAI_ORG/02_ORGANS/TheCircle/INTEGRATION_STATUS.md)
- [`../SKYZAI_ORG/02_ORGANS/TheCircle/00_SILO_AUDIT_2026_04_23.md`](../SKYZAI_ORG/02_ORGANS/TheCircle/00_SILO_AUDIT_2026_04_23.md)
- [`../SKYZAI_ORG/02_ORGANS/TheCircle/LANES.md`](../SKYZAI_ORG/02_ORGANS/TheCircle/LANES.md)
- [`../SKYZAI_ORG/09_PWAs/circle_news/PR_FAQ.md`](../../../02_SKYZAI/02_AIA/EMERGENTISM_AIA/09_BOOK_PRODUCTION_ARCHIVE/07_DISSEMINATION/06_NETWORK/emergentism.org/PR_FAQ.md)
- [`../SKYZAI_ORG/09_PWAs/circle_news/GAP_ANALYSIS.md`](../../../02_SKYZAI/02_AIA/EMERGENTISM_AIA/09_BOOK_PRODUCTION_ARCHIVE/07_DISSEMINATION/06_NETWORK/emergentism.org/GAP_ANALYSIS.md)

---

## 0. Scope of "complete product"

From `PR_FAQ.md` + `00_BRIEF.md` + `GAP_ANALYSIS.md`, a complete Circle is:

- **Deployed frontend** at `circle.news` / `circle.skyzai.com`
- **Live backend** emitting Nostr Kind 31339 from real data sources
- **F1 signal flowing** to APU (and indirectly to RealityFutures via `circle_to_refu_adapter.py`)
- **Reputation engine** scoring sources and exporting D5 to Skyzai Connect
- **η = 0 + K2 + Three-Stage Process + IS-domain boundary** preserved end-to-end

The organ has ~748 files of code + spec. The gap is not invention. The gap
is **deployment, wiring, sign-off**, and a disciplined P-score lift per
phase.

---

## 1. Current state snapshot

| Register | Score | Classification | Source |
|----------|-------|----------------|--------|
| Code-lens P | 0.53 (Φ=0.80, V=0.66) | Equator | `00_BRIEF.md` + `SKYZAI_ORG/P-SCORES.md` |
| Runtime-lens P | 0.25 (Φ=0.65, V=0.38) | Egg | `INTEGRATION_STATUS.md` |

Breathing surfaces (earned):
- RSS adapter fetched 5 public feeds and wrote 16 dated F1 artifacts on 2026-04-19 (`app/f1_output/20260419_rss_proof/`)
- Canonical `SignalPacket` schema aligned with APU expectations
- Local end-to-end proof `SignalPacket → APU → K2 envelope` passed 2026-04-18
- `circle_to_refu_adapter.py` exists at `app/pipeline/`

Not breathing (gaps):
- No deployed frontend; `circle.news` has `.vercel` config but zero deployments
- No deployed backend; 5-service docker-compose ready but not up
- No live Nostr Kind 31339 emission from production
- Reputation engine is a single Python file; not distributed
- F1 → F2 wiring exists in adapter code but does not consume live observations
- Cortex memory not wired to observation ledger

---

## 2. Runway — four phases

| Phase | Duration estimate | K2 moves | Runtime P (end) | What breathes |
|-------|-------------------|----------|-----------------|---------------|
| 0 | 15–20 min warrior-time | 7 | 0.25 | Silo retired; live tree absorbs audited items. |
| 1 | 1–2 sessions | 3 | ~0.45 | Frontend live at `circle.news`; backend stack running. |
| 2 | 2–3 sessions | 3+ | ~0.62 | Real F1 on real relay; Three-Stage Process starts breathing. |
| 3 | 3–5 sessions | N (scoped later) | ~0.80 | Reputation + D5; trusted network. |

Each phase ends on a receipt that updates `INTEGRATION_STATUS.md`.

---

## 3. Phase 0 — Silo sign-off (warrior hour)

From `02_ORGANS/TheCircle/00_SILO_AUDIT_2026_04_23.md`. Six rows to sign +
one row to archive. Each is a single K2-gated git move. Estimated:
**15–20 minutes of warrior attention**.

| # | Verdict | Action | K2-gated command (warrior lane) |
|---|---------|--------|---------------------------------|
| 1 | NEW | Promote `ci/deploy.yml` (GitHub Actions deploy workflow) | `git mv app/_silo_intake_2026_04_22/ci/deploy.yml app/circle_platform_backend/02_PRODUCT/Platform/.github/workflows/deploy.yml` |
| 2 | NEW | Promote `NetworkBadge.tsx` (lands **after** row 5 for `@/lib/network` import) | `git mv … components/shared/NetworkBadge.tsx` |
| 3 | NEW | Promote `MAINNET_MIGRATION.md` | `git mv … 02_PRODUCT/Platform/docs/MAINNET_MIGRATION.md` |
| 4 | SUPERSEDED | Archive empty `governance/EQUITY_LAYER.md` | `git rm app/_silo_intake_2026_04_22/governance/EQUITY_LAYER.md` |
| 5 | UPDATE | Promote `lib/network.ts` (env toggle + derived exports); `chains.ts` unchanged | `git mv … 02_PRODUCT/Platform/lib/network.ts` |
| 6 | NEW | Promote `pipeline/markets/resolution_keeper.py` (scheduler wiring separate) | `git mv … 03_BUILD/Source/pipeline/markets/resolution_keeper.py` |
| 7 | NEW | Promote `scripts/backup.sh` (executable bit required) | `git mv … 03_BUILD/Source/scripts/backup.sh` then `git update-index --chmod=+x …` |

**Exit criterion:** `app/_silo_intake_2026_04_22/` holds only the 15
reference-tier items; the 7 production items are either in their target
path (rows 1–3, 5–7) or deleted (row 4).

**Sign order:** rows 1, 3, 4, 5, 7 are independent. Row 2 lands after row 5.
Row 6 can land anywhere. Suggested order: **5 → 2 → 1 → 3 → 4 → 6 → 7**.

---

## 4. Phase 1 — Deploy (closes G1; runtime 0.25 → ~0.45)

Three tracks. Tracks 1A and 1B run in parallel; track 1C lands with silo row 1.

### Track 1A — Frontend deploy (`circle.news`)

**Path:** `SKYZAI_ORG/02_ORGANS/TheCircle/app/website/`
**Tech:** Next.js 16, 16 pages. Vercel config exists.
**Blockers:** None on frontend itself; DNS records for `circle.news` must be configured at your registrar.
**Reference runbook:** `app/website/DEPLOYMENT.md` (already written; use as-is).

**Exact K2-gated moves:**

```bash
cd SKYZAI_ORG/02_ORGANS/TheCircle/app/website/
npm install
npm run build                                    # must pass
npx serve dist                                   # smoke-test locally
vercel --prod                                    # ← K2-gated: commits the public claim
```

**Verification signals:**
- `curl -I https://circle.news` returns 200
- Lighthouse score > 90
- All 16 pages render without console errors
- Health endpoint `/api/health` returns `{"status":"ok"}` (per DEPLOYMENT.md §"Health Check Endpoint")

**Receipt target:** update `INTEGRATION_STATUS.md` deployment table row "PWA (circle.news)" from ❌ NOT DEPLOYED to ✅ LIVE with URL + timestamp.

### Track 1B — Backend bootstrap (Docker stack)

**Path:** `SKYZAI_ORG/02_ORGANS/TheCircle/app/circle_platform_backend/03_BUILD/`
**Stack:** PostgreSQL 15 + pgvector + Redis + FastAPI + Scheduler + Nginx (5-service docker-compose).
**Reference runbook:** `03_BUILD/DEPLOY.md` and `03_BUILD/DEPLOYMENT_RUNBOOK.md`.

**Blockers (sovereign secrets — never pass through charioteer):**
- `POSTGRES_PASSWORD` (generate 32+ char)
- `ANTHROPIC_API_KEY` (from anthropic.com)
- `NOSTR_NSEC` (the Circle signing key — sovereign-held)

**Exact K2-gated moves:**

```bash
cd SKYZAI_ORG/02_ORGANS/TheCircle/app/circle_platform_backend/03_BUILD/
cp .env.example .env
# warrior manually edits .env with the three secrets
docker compose config                            # validate config parses
docker compose up -d                             # ← K2-gated: real infra
docker compose ps                                # all 5 services healthy
curl http://localhost:8000/health                # backend alive
```

**Verification signals:**
- `docker compose ps` shows all 5 services `running` / `healthy`
- `/health` returns `{"status":"ok"}`
- Postgres accepts connections; pgvector extension is loaded
- No crash loops in `docker compose logs --tail=50`

**Receipt target:** update `INTEGRATION_STATUS.md` deployment table row "Backend API" from ❌ NOT LIVE to ✅ LIVE with hostname + timestamp.

### Track 1C — CI wiring

Lands with silo row 1 (`ci/deploy.yml`). One K2-signed commit wires GitHub
Actions to the deployment pipeline. Zero blocker after row 1 signs.

---

## 5. Phase 2 — F1 Breathing (closes G2 + G5 + G3; runtime ~0.45 → ~0.62)

Phase 1 makes Circle visible. Phase 2 makes Circle **breathe**. Three-Stage Process starts here.

### Track 2A — Live OSINT ingestion (closes G2)

**Path:** `SKYZAI_ORG/02_ORGANS/TheCircle/app/pipeline/ingestion/`
**Target:** Pick **one** real data source from `01_DATA_ROOM/02_DATA_SOURCE_REGISTRY.md`. Suggest RSS — the adapter is already proven locally (2026-04-19 receipt at `F1_RSS_VALIDATION_RECEIPT_2026_04_19.md`).

**Blockers:** source list; scheduler config; observation-store schema migration run.

**Exact K2-gated moves:**

```bash
cd SKYZAI_ORG/02_ORGANS/TheCircle/app/pipeline/ingestion/
# Use the already-proven RSS adapter, now pointing at the deployed backend
python rss_adapter.py \
    --sources ../data/rss_feeds.yaml \
    --observation-store http://localhost:8000/observations
```

**Verification signals:**
- `GET /observations?since=1h` returns N > 0 real observations
- Each observation has `evidence_tier`, `confidence`, `sources`, `reasoning_mode="inductive"`
- `corruption_check` passes on every row (no `will` / `should` / `could` claims)
- Postgres `observation` table row count grows over time

**Receipt target:** new `F1_LIVE_INGESTION_RECEIPT_YYYY_MM_DD.md` in `TheCircle/` with hash of N observations, first-timestamp, last-timestamp.

### Track 2B — Nostr publication (closes G5)

**Path:** `SKYZAI_ORG/02_ORGANS/TheCircle/app/pipeline/publishing/f1_publisher.py`
**Cross-wire (per packet 117 C-2):** import relay state from `core/nervous_system/nostr/relay_manager.py` (R-6 — NOTICE/EOSE handled upstream). Do not re-implement.

**Blockers:** relay list; `NOSTR_NSEC` present (from Phase 1B); connectivity to relays.

**Exact K2-gated moves:**

```bash
cd SKYZAI_ORG/02_ORGANS/TheCircle/app/pipeline/publishing/
python f1_publisher.py \
    --relay wss://relay.damus.io,wss://relay.nostr.band \
    --observation-stream http://localhost:8000/observations/stream \
    --kind 31339
```

**Verification signals:**
- From a sovereign-controlled second host: `nostr-tool fetch --filter '{"kinds":[31339],"authors":["<Circle pubkey>"],"limit":10}'` returns 10 recent Circle observations
- Each event is signed by the Circle key
- `tags` include the entity and the APU pubkey (per BRIEF §"F1 Publication")

**Receipt target:** update `INTEGRATION_STATUS.md` row "Nostr relay publication" from ❌ NOT LIVE to ✅ LIVE; mark contradiction `CIR-002` RESOLVED.

### Track 2C — F1 → F2 wiring (closes G3)

**Path:** `app/pipeline/circle_to_refu_adapter.py` — file exists; needs verification against live F1 + live RealityFutures F2.
**Blockers:** the RealityFutures F2-receive endpoint must exist and be reachable. Cross-organ dependency.

**Exact K2-gated moves:**

```bash
python app/pipeline/circle_to_refu_adapter.py \
    --from http://localhost:8000/observations/stream \
    --to <REFU_F2_INGEST_URL>
```

**Verification signals:**
- RealityFutures receives one F2-shaped signal per Circle observation
- Schema check passes on the RealityFutures side
- No Circle observation is dropped silently

**Receipt target:** update `INTEGRATION_STATUS.md` row "F1 output → RealityFutures" from ⚠️ PARTIAL to ✅ LIVE.

---

## 6. Phase 3 — Reputation + D5 (closes G4 + G6 + G7 + G8; runtime ~0.62 → ~0.80)

Turns Circle from "live observer" into "trusted observation network."
**This phase needs its own sprint packet before execution** — sketched here
but not enumerated at move-level granularity.

### Track 3A — EigenTrust distributed scoring (G4)
Single-file spec at `reputation_engine.py`. Needs distributed implementation
wiring to `observation_store`. Open design question: run EigenTrust as a
periodic batch job over observations, or as a continuous stream?

### Track 3B — F3 loop closure (G6)
Local proof exists (2026-04-18 end-to-end). Live wiring pending: APU receipts
must feed back into `reputation_engine.update_from_action_receipt`. Requires
backbone F3 channel identification.

### Track 3C — D5 export to Skyzai Connect
Export format = `ReputationScore` schema in `00_BRIEF.md`. Requires the
Skyzai Connect D5 consumer surface to exist on the Skyzai side.

### Track 3D — Adversarial resistance testing (G9)
Specified in `PHD3_EIGENTRUST_REPUTATION_FINDINGS.md`; not tested. Requires
attack-scenario enumeration + safe test harness.

---

## 7. Sovereign non-delegation — what the charioteer will NOT do

Per [packet 99 §4.2](../50_AUDITS_AND_EXECUTIONS/99_SOVEREIGN_READING_OF_FOUNDATION_AND_ROSETTA_2026_04_23.md):

- I will **not** run `vercel --prod` on your behalf.
- I will **not** run `docker compose up -d` on your behalf.
- I will **not** sign Phase 0 row moves.
- I will **not** handle or print the three sovereign secrets (`POSTGRES_PASSWORD`, `ANTHROPIC_API_KEY`, `NOSTR_NSEC`).
- I will **not** mark receipts as realized.
- I will **not** invent Three-Stage Process-collapsed shortcuts that merge IS with COULD or SHOULD.

I hold the map. I draft the moves. You sign.

---

## 8. Lane discipline

Each track declares its `(organ, surface, domain)` lane so L4 arbitration
can serialize:

| Track | Lane triple |
|-------|-------------|
| 0 rows 1–7 | `(TheCircle, code, backend.core)` + `(TheCircle, code, frontend.platform)` depending on target; rows are disjoint |
| 1A | `(TheCircle, code, frontend.platform)` |
| 1B | `(TheCircle, code, backend.core)` |
| 1C | `(TheCircle, ops, ci)` |
| 2A | `(TheCircle, code, backend.pipeline)` (new domain; propose add to `LANES.md`) |
| 2B | `(TheCircle, code, backend.nostr)` |
| 2C | `(TheCircle, code, backend.pipeline)` + cross-organ read on `(RealityFutures, code, *)` |

No two active tracks share a lane tuple. Safe to parallelize 1A + 1B + silo
row 1/4 in the same warrior session.

---

## 9. Constitutional checks

| Check | Result |
|-------|--------|
| **K2** | Every move in this packet is human-signed (either `vercel --prod`, `docker compose up -d`, `git mv`, or `git commit`). No silent automation. ✓ |
| **η = 0** | Deployment choices (Vercel free tier, Hetzner CX22) carry no rent-capture. Premium tier in PR_FAQ remains access-priced, not access-gated. ✓ |
| **K4** | All artifacts remain exportable — Next.js `dist/` is static; Postgres dumps via Phase 0 row 7's `backup.sh`; Nostr keys sovereign-held. ✓ |
| **Three-Stage Process** | IS-domain corruption check in `is_agent.py` is preserved. No track in this packet writes forecasts or recommendations from Circle. ✓ |
| **A7** | This packet will be refreshed as phases complete; drift register goes at the foot of `INTEGRATION_STATUS.md`. ✓ |

---

## 10. Limits

- **L1:** Track 1B secrets are sovereign-held. If a secret is not yet minted (e.g., `NOSTR_NSEC`), Phase 1B pauses until it is. The charioteer can draft a secret-generation SOP but cannot execute the generation.
- **L2:** Track 2C requires the RealityFutures F2-receive endpoint to exist. If it does not, Phase 2C pauses. Unblocker is a RealityFutures-lane packet, not a Circle-lane packet.
- **L3:** Track 3A (distributed EigenTrust) is not fully spec'd for runtime. Phase 3 will need its own sprint packet (propose packet number ~130 after Phase 2 lands).
- **L4:** Silo row 6 (`resolution_keeper.py`) addresses a RealityFutures invariant, not Circle's observation scheduler. It is included in Phase 0 only because it was in the Circle silo — not because it belongs to the Circle runtime.
- **L5:** Runtime P-score projections (0.45, 0.62, 0.80) are interpretive `[I]` estimates. Measured P after each phase outranks these projections.
- **L6:** This packet does not address the ambiguity of "github Circle" as potentially meaning a new GitHub-hosted repo distinct from the current organ tree. If a new repo is the intent, the sprint extends with a repo-split packet.

---

## 11. Execution surface — three ways to go now

Pick one and say the word:

1. **"Phase 0."** I produce the exact seven git commands as a single runnable block. You paste them in your terminal and sign each.
2. **"Phase 1A."** I produce the Vercel deployment runbook with pre-launch checklist instrumented against `DEPLOYMENT.md`, DNS template, and rollback plan.
3. **"Phase 1B."** I produce the docker-compose bring-up runbook with `.env.example` template (placeholder secrets you fill in), health-check sequence, and troubleshooting tree for the 5-service stack.

All three can also be run in a different order if you name it.

---

**Move:** Kṛṣṇa ◇ stages decision-ready packets · Arjuna ⚔ executes on your hand · Viṣṇu ⊙ holds center until you direct.

Zero-Sum Resolution Equation

---

*What do you see now?*
