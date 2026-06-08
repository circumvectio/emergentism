---
rosetta:
  primary_column: "Philosophy"
  register: "[S/I]"
  canonical_phrase: "Sprint-A Lock Document"
---

# Sprint-A Lock Document
## APU — Wedge A: Multi-Model BYOK + Cloud Document Deliberation

**Locked:** 2026-04-23T00:00:00Z  
**Sprint Window:** 2026-04-27 → 2026-05-15 (3 weeks)  
**Schema Version:** v0 (frozen)  
**Tests:** 66/66 passing  
**Branch:** main (clean working tree, commit `e56e1d938`)

---

## 1. Wedge A Scope (4 Actions)

| # | Action | Status | Blocker |
|---|--------|--------|---------|
| 0 | **First Human + Document** | 🔴 WAITING | Need 1 person + 1 doc + expected contradiction |
| 1 | **Action 0.1 — Document Ingestion** | 🟡 READY | Needs Action 0 |
| 2 | **Action 0.2 — Council Execution** | 🟡 READY | Needs Action 0.1 + live LLM keys |
| 3 | **Action 1+ — Feedback Loop** | 🔴 DEFERRED | Needs Action 0.2 result |

---

## 2. Architecture Delivered

### 2.1 Council Protocol (9-Stage State Machine)
- **File:** `council/protocol.py`
- **Lines:** 595
- **Stages:** SIGNAL_INGESTION → CONTEXT_ENRICHMENT → DIRECTORATE_DISPATCH → PARALLEL_DELIBERATION → CONFLICT_DETECTION → SYNTHESIS_PREPARATION → CHIEF_OF_STAFF_SYNTHESIS → K2_ENVELOPE_GENERATION → RECEIPT_EMISSION
- **Gates:** 8 machine-checkable stage gates
- **Fail-safe:** HALT on any failure; L5 deadlock escalation path
- **Tests:** 24/24 passing

### 2.2 Directorate Processors (7 Seats)
- **File:** `council/processors.py`
- **Seats:** Intelligence, Strategy, Legal, Engineering, Treasury, Procurement, Independent Reviewer
- **Pattern:** ABC with `validate_input` / `process` / `validate_output`
- **Tests:** 24/24 passing

### 2.3 Multi-Model BYOK Config API
- **File:** `api/routers/router_config.py`
- **Endpoints:**
  - `POST /config/{wallet}` — merge/create config with model assignments
  - `GET /config/{wallet}/model-assignments` — metadata only
  - `POST /config/{wallet}/model-assignments` — direct replacement
  - `POST /ai/verify` — provider credential verification
- **Encryption:** AES-256-GCM via wallet signature derivation
- **Progressive Policy:** 1 min → 2 rec → 7 full (after 3+ runs)
- **Tests:** 8/8 passing

### 2.4 Cloud Document Ingestion
- **File:** `core/membrane/doc_ingestion.py`
- **Sources:** Raw text, Notion (recursive blocks), Google Docs (structural elements)
- **Tests:** (covered in deliberation tests)

### 2.5 Document Deliberation Endpoint
- **File:** `api/routers/router_council_documents.py`
- **Endpoint:** `POST /council/document-deliberation`
- **Flow:** Ingest → APUSignal → 9-Stage Council → Structured Verdict
- **K2:** Verdict-only in Sprint-A (no write-back)
- **Tests:** 9/9 passing

---

## 3. Schema v0 Lock

**File:** `spec/council_output_schema_v0.json`

### Required Fields (10)
These fields MUST be present in every `DocumentDeliberationResponse`:

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | `completed`, `hold`, or `error` |
| `wallet_address` | string | Requesting wallet |
| `signal_id` | string | UUID of the signal |
| `decision` | string | Council decision: `PROCEED`, `HOLD`, `ESCALATE` |
| `action` | string | Recommended action or null |
| `rationale` | string | Human-readable synthesis |
| `confidence_used` | number | Confidence threshold applied |
| `rule_applied` | string | Name of governing rule |
| `receipt_id` | string | UUID for audit trail |
| `generated_at` | string | ISO 8601 timestamp |

### Optional Fields
All other fields (`opinions`, `reviews`, `conflicts`, `k2_envelope`, `source`, `title`, etc.) are optional and may be null/empty.

### Revision Policy
Schema v0 is **frozen** for the duration of Sprint-A (2026-04-27 → 2026-05-15). Any changes require:
1. Explicit sprint revision
2. Updated tests
3. Updated consumer code
4. New schema file (v1)

---

## 4. Pre-Sprint Checklist

| Item | Status |
|------|--------|
| Schema v0 locked | ✅ |
| Response model aligned | ✅ |
| Progressive BYOK policy defined | ✅ |
| Verdict-only K2 for Sprint-A | ✅ |
| Embedding provider decided | ✅ |
| First deliberation fixture encoded | ✅ |
| **71 tests passing** | ✅ |
| Git commit clean | ✅ |

---

## 5. Human Decisions Required Before Sprint Start

| # | Decision | Status | Value |
|---|----------|--------|-------|
| 1 | **Embedding provider** | ✅ DECIDED | OpenAI `text-embedding-3-small` |
| 2 | **First human + document** | ✅ DECIDED | Yves + `AGENTS_FRAMEWORK_INTRO.md` K2 section |
| 3 | **Go/no-go** | ✅ DECIDED | **GO** — Sprint-A starts 2026-04-27 |

### Decision 2 Details: First Deliberation Fixture

**Human:** Yves (founder/operator)  
**Document:** `AGENTS_FRAMEWORK_INTRO.md` — Constitutional Constraints section (K2)  
**Expected Contradiction:**
- **Legal seat:** HOLD — "structured verdict with confidence score + K2 envelope is functionally a decision; violates K2 'APU suggests, never decides'"
- **Engineering seat:** PROCEED — "human still signs via K2 envelope; Council merely structures recommendation, does not decide"

**Fixture test:** `tests/test_first_deliberation_fixture.py` (5 tests, 100% pass)  
**Wedge A success criterion:** Prove Yves sees a contradiction his single-model tool missed.

---

## 6. Known Stubs (Not Blockers)

| Stub | Location | Sprint-A Impact |
|------|----------|-----------------|
| `call_llm_provider` | `council_protocol.py` | Requires env keys for live runs |
| Provider catalog | `_experimental/` | Unmounted, not in critical path |
| Conviction crypto | `core/circulation/` | Deferred to Sprint-B |
| Execution auth | `api/routers/` | Deferred to Sprint-B |
| K2 live signing | Stage 8 | Verdict-only in Sprint-A |
| NOSTR event bus | `core/nervous_system/` | Production patch needed for Stage 9 |

---

## 7. Competitive Positioning Reminder

> APU competes with **institutional drift cost**, not with Claude Code/Cursor execution velocity. The correct relationship is layering: agents execute fast, the Council governs coherence.
>
> The Council moat is **structural** (7-model parallel deliberation with anonymized peer review), but it is **not yet felt**. Wedge A must prove a human sees a contradiction their single-model tool missed.

---

## 8. Next Actions (Post-Lock / Pre-Sprint)

1. ✅ ~~Identify first human + document~~ → Yves + K2 section
2. ✅ ~~Decide embedding provider~~ → OpenAI text-embedding-3-small
3. ✅ ~~Go/no-go~~ → GO
4. **Wire live LLM keys** → enable `call_llm_provider` with real credentials
5. **Run Action 0.1** → First live deliberation with the K2 fixture
6. **Iterate** → Human reads verdict, validates contradiction visibility

---

## 9. Anti-Drift Lock

Sprint-A is locked against category drift as well as scope drift.

### Explicitly allowed

- live-branch hardening of the current council runtime
- live-branch event-bus hardening
- typed F2 intake work on top of the current adapter path
- streaming and observability improvements that serve deliberation objects

### Explicitly disallowed

- whole-drop merges from intake forks
- adopting generic harness architecture
- introducing a second canonical APU surface
- reframing APU as a general-purpose execution agent
- bypassing K2 or Legal-VETO for demo velocity

### Fork rule

The latest `apu_bot-deployment` intake does **not** revise Sprint-A scope.

Its useful residue is bounded to:

- event-bus hardening ideas
- typed F2 intake ideas

Both must be implemented against the live branch. The fork itself remains reference-only.

---

*Document generated by APU Council Protocol v0. Locked until 2026-05-15 or explicit revision.*
