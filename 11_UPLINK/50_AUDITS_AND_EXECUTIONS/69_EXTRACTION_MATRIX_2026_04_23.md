---
rosetta:
  primary_column: "Liberal art"
  register: "[S/I]"
  canonical_phrase: "Founder-Gated Extraction Matrix"
---

# Founder-Gated Extraction Matrix
## Intake: DeerFlow · Goose · Hermes → APU

**Date:** 2026-04-23
**Gating cell:** `[L3 | D4 | S-Org | F-phi :: vaisya_auditor]`
**Rule:** `borrow the pipe, not the direction of flow`
**Sprint-A compatibility:** All `extract-now` items fit Wedge A scope



---

## Four Guards

Every candidate passed four guards before earning a route:

1. **Category-claim guard** — does absorbing it pull APU toward generic harness identity?
2. **`η = 0` guard** — does it import rent, hosted tolls, or access capture?
3. **K2 guard** — does it normalize irreversible agent action without human signature?
4. **Three-Stage Process guard** — does it collapse `IS / COULD / SHOULD / ACT` into one surface?

If any guard fires, the pattern is rejected or held for redesign.

---

## Reconciliation Rule

Some patterns were identified in intake before the founder-gated matrix fully stabilized.

Use this rule:

- if the target does **not** yet exist in live code, it is a normal packet candidate
- if the target **does** already exist in live code, it becomes a **reconcile-or-keep** check: verify it still passes the four guards, then keep or revise it

This prevents "already landed" from being mistaken for "already constitutionally settled."

---

## First Wave — `extract-now`

### `S-1` MCP Tool Bridge
**Source:** Goose MCP subsystem (`crates/goose-mcp/`)
**Status:** ✅ SHIPPED
**File:** `core/membrane/council_mcp_server.py`
**What was taken:** The pattern of exposing each capability as an MCP server over stdio, not the capability core state itself.
**What was refused:** Goose's general-purpose agent tools (file edit, bash, browser). APU exposes only governance primitives: `council_deliberate`, `council_deliberate_light`, `council_receipt`, `council_status`.
**Core State risk:** LOW — MCP is pure plumbing. The tool schemas are APU-native.
**Commit template:** `feat(integration): expose Council deliberation as MCP tools`

---

### `S-3` Anthropic Prompt Caching
**Source:** Goose provider layer (`crates/goose/src/providers/anthropic.rs`)
**Status:** ✅ SHIPPED
**File:** `core/circulation/prompt_cache.py`
**What to take:** `anthropic-beta: prompt-caching-2024-07-31` header injection for system prompts > 1024 tokens that repeat across directorate calls.
**What to refuse:** Generic provider-agnostic caching — Anthropic's caching API is provider-specific and should not be abstracted into a false universal.
**Core State risk:** LOW — cost optimization, no category drift.
**Sprint-A fit:** Reduces Wedge A demo cost when running 7-seat Council repeatedly on the same constitutional prompt.
**Commit template:** `feat(cost): Anthropic prompt caching for repeated constitutional prompts`

---

### `S-5` SSE Streaming + Per-ID Deduplication
**Source:** DeerFlow SSE gateway (`backend/packages/harness/deerflow/gateway/sse.py`)
**Status:** ✅ SHIPPED
**Target:** `api/routers/router_council_documents.py` + Skyzai deliberation surfaces
**What to take:** Server-Sent Events for live stage progression; deduplication by `deliberation_id` to prevent duplicate streams on reconnect.
**What to refuse:** DeerFlow's full gateway abstraction — APU streams only Council stage events, not generic tool-call events.
**Core State risk:** LOW — UX plumbing, not decision logic.
**Sprint-A fit:** Lets Yves watch both the 9-stage machine and the Light Council K2 fixture progress in real time.
**Commit template:** `feat(ux): SSE streaming for Council stage progression with per-id dedup`

---

### `R-1` Legal-VETO-Native Guardrail Layer
**Source:** DeerFlow `GuardrailMiddleware` → reframed for constitutional council
**Status:** ✅ SHIPPED
**File:** `council/guardrails.py` + `council/protocol.py` Stage 1 integration
**What to take:** The pattern of pre-execution pluggable policy evaluation.
**What to reframe:** DeerFlow's guardrail is single-policy over a single agent. APU's guardrail is **seat-scoped constitutional pre-check**: before any API calls are made, the Legal seat's constitutional rules are evaluated against the signal. If `η = 0` or `K2` would be violated, the Council halts immediately with a `CONSTITUTIONAL_VETO` — no tokens wasted on the other six seats.
**Core State risk:** LOW — strengthens the category claim. This is not generic middleware; it is the Legal seat's authority expressed as a hard gate.
**Sprint-A fit:** Prevents wasted API calls on signals that violate K2. Makes the first deliberation demo cheaper and faster.
**Commit template:** `feat(constitution): Legal-VETO guardrail middleware — pre-Council constitutional check`

## Second Wave — `extract-later` (post-Sprint-A)

### `S-2` Context Compressor for Stage 9
**Source:** DeerFlow `SummarizationMiddleware`
**Target:** `council/protocol.py` Stage 9 (RECEIPT_EMISSION)
**Why later:** Context compression is valuable but not the sharpest wedge. Easy to add after the council path is stable.
**Commit template:** `feat(memory): context compression for long deliberation transcripts`

### `R-2` Seat-Aware Retry / Error Classification
**Source:** DeerFlow `ToolErrorHandlingMiddleware` + `LLMErrorHandlingMiddleware`
**Target:** `council/processors.py`
**Why later:** Important, but should come after seat authority (R-1) and streaming (S-5) are stable.
**Commit template:** `feat(resilience): seat-aware retry with error classification`

### `R-4` K2-Native Signed Auth
**Source:** Goose `GOVERNANCE.md` consensus process + OIDC proxy pattern
**Status:** ✅ SHIPPED (2026-04-23 under founder D2=accept on packet 74)
**Files:**
- `core/membrane/k2_auth_proxy.py` (sha256 62445d34…828e28, 183 LOC)
- `core/membrane/approval_queue.py` (sha256 461d22a0…51a18, 368 LOC — async queue shipped alongside under same D2 authorization)
- `core/membrane/approval_models.py` (sha256 5ead8815…b0202, 83 LOC)
- `core/membrane/k2_gateway.py` (sha256 d14be71c…9da6d, 570 LOC — integration surface)
- Wired into Council Stage 9 at `api/routers/router_council_sse.py:204-205`
**Reconciliation:** `01_EMERGENTISM/11_UPLINK/75_R4_QUEUE_RECONCILIATION_2026_04_23.md`
**Remaining work:** adversarial test close (task #36); K2_STRICT_MODE=False advisory by default until tests fire.
**Commit template:** `feat(auth): K2-native signed authentication layer`

---

## Hold for Clarification — `more-info`

### `S-4` Self-Discovering Tool Registry
**Source:** DeerFlow dynamic tool loading
**Risk:** High risk of sliding toward generic harness behavior unless discovery is seat-scoped and constitutionally bounded.
**Clarification needed:** Should tool discovery be a Legal-gated operation? Or a Standing Orders (4C) feature?

### `R-3` `SKILL.md` Frontmatter Registry
**Source:** Hermes skill format
**Risk:** Good format idea, but only if mapped into Cortex/AIA core state first.
**Clarification needed:** Is this for Standing Orders (4C), agent caste prompts, or user-authored directives? Each has different canonical paths.

---

## Rejected — `skip`

| Item | Source | Why skipped |
|------|--------|-------------|
| `X-1` DeerFlow 18-middleware pipeline | DeerFlow | Replaces the organism. APU's 9-stage state machine is the constitutional primitive, not a middleware chain. |
| `X-2` Goose Recipe DSL | Goose | Wrong frame. APU uses deliberation templates, not recipes. |
| `X-3` Goose Recipe Security Scanner | Goose | Depends on a rejected frame (X-2). |
| `X-4` DeerFlow IM channel integrations | DeerFlow | Trips `η = 0`. Signal ingestion belongs to TheCircle (IS), not Agentz (SHOULD). |
| `X-5` Hermes self-improving framing | Hermes | Trips constitutional drift. APU does not self-improve; it is improved by human mandate. |
| `R-5` Hermes `mixture_of_agents` | Hermes | Too close to the category seam. Light Council (S-1 variant) is the correct absorption — consensus burst as utility, not product. |

---

## Vaibhav Fork Intake

Latest APU fork intake result:

- **whole drop:** Path 1 refused
- **new operational packets opened:** 0

Three deferred Path 3 design primitives survived scoped review and are currently parked only as non-wired design scaffolds:

1. a central event-kind taxonomy
2. a typed F2 domain taxonomy
3. a domain → seat-routing sketch

**Update 2026-04-23:** All three primitives were implemented as extraction packets R-6, S-7, S-8 and shipped:

| Packet | Primitive | File | Tests |
|--------|-----------|------|-------|
| R-6 | Nostr NOTICE/EOSE handling | `core/nervous_system/nostr/relay_manager.py` | 5 passed |
| S-7 | F2 confidence tier + provenance hash | `adapters/refu_to_apu_adapter.py` | 8 passed |
| S-8 | F2 urgency assessment | `adapters/refu_to_apu_adapter.py` | 8 passed |

---

## Packet Order for Sprint-A

```
Packet 1:  S-1 (MCP bridge)              ✅ DONE
Packet 2:  S-3 (Prompt caching)          ✅ DONE
Packet 3:  R-1 (Legal guardrail)         ✅ DONE
Packet 4:  S-5 (SSE streaming)           ✅ DONE
Packet 5:  R-6 (NOTICE/EOSE)             ✅ DONE
Packet 6:  S-7 (F2 confidence tier)      ✅ DONE
Packet 7:  S-8 (F2 urgency)              ✅ DONE
Packet 8:  Action 0.1 (call_llm_provider) ✅ DONE — first live deliberation 2026-04-23
Packet 9:  Sprint-A closeout             ✅ DONE — explicit sovereign runtime + progressive events + signed K2 proof
```

---

> **The membrane holds.** Nothing extracted changes what APU is. Everything extracted changes what APU can do without becoming something else.
