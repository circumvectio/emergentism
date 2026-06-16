---
rosetta:
  primary_column: "Liberal art"
  register: "[I]"
  canonical_phrase: "117 · Circle Intake Extraction Matrix — 2026-04-23"
---

# 117 · CIRCLE INTAKE EXTRACTION MATRIX — 2026-04-23

**Evidence tier:** [I]
*Organism document. Interpretive operational content. Bounded by current system state.*

**Date:** 2026-04-23
**Lane:** `(FOUNDATION, doc, framework.uplink)`
**Operator (this packet):** Kṛṣṇa ◇ — V-export for TheCircle at charioteer Φ cost
**Executive-layer hold:** Viṣṇu ⊙ — preservation at the taxonomy layer; no rewrite
**Companion packet:** [`118_CIRCLE_PRODUCT_SPRINT_PACKET_2026_04_23.md`](118_CIRCLE_PRODUCT_SPRINT_PACKET_2026_04_23.md)
**Source spine:**
- [`69_EXTRACTION_MATRIX_2026_04_23.md`](../50_AUDITS_AND_EXECUTIONS/69_EXTRACTION_MATRIX_2026_04_23.md) — APU extraction matrix (same lens applied here)
- [`../02_SKYZAI/01_NOOSPHERE/00_INTAKE/PROCESSED/2026_04_23_intake_audit_deerflow_goose_hermes.md`](../02_SKYZAI/01_NOOSPHERE/00_INTAKE/PROCESSED/2026_04_23_intake_audit_deerflow_goose_hermes.md) — SWOT/TOWS audit
- [`../02_SKYZAI/01_NOOSPHERE/02_ORGANS/TheCircle/00_BRIEF.md`](../../08_FRAMEWORK_SUPPORT/00_META/00_BRIEF.md) — IS organ spec
- [`../02_SKYZAI/01_NOOSPHERE/09_PWAs/circle_news/PR_FAQ.md`](../../../02_SKYZAI/03_AIA/EMERGENTISM_AIA/09_BOOK_PRODUCTION_ARCHIVE/07_DISSEMINATION/06_NETWORK/emergentism.org/PR_FAQ.md) — North Star

---

## 1. Scope

Read the four `02_SKYZAI/01_NOOSPHERE/00_INTAKE/QUEUE/` items through a **Circle-relevance lens**:

- `deer-flow-main`
- `goose-main`
- `hermes-agent-main`
- `vaibhav_send_pack_2026_04_23`

Question: does TheCircle need to absorb any pattern from these intake items to become a complete product?

---

## 2. Guards

Same four guards from packet 69, **plus one Circle-specific guard**:

1. **Category-claim guard** — does absorbing pull Circle toward generic harness identity?
2. **η = 0 guard** — does it import rent, hosted tolls, or access capture?
3. **K2 guard** — does it normalize irreversible action without human signature?
4. **Three-Stage Process guard** — does it collapse `IS / COULD / SHOULD / ACT` into one surface?
5. **IS-domain guard** (Circle-specific) — does the pattern preserve the IS boundary? Any pattern that would let Circle emit `will` / `should` / `could` fails this guard automatically.

---

## 3. Cross-wire preference

When a pattern already lives in another organ's lane (typically APU's shipped
packets), Circle should **consume it via the backbone**, not re-implement it.
This preserves Three-Stage Process separation and avoids Raktabīja — the trap of
multiplying unguarded copies of the same primitive across organs.

---

## 4. Per-item verdicts

| # | Source | Pattern | Circle need? | Already shipped? | Verdict |
|---|--------|---------|--------------|------------------|---------|
| C-1 | DeerFlow SSE gateway | SSE streaming for live event progression | YES — observation broadcast surface | ✅ S-5 shipped in APU (`api/routers/router_council_documents.py`) | **CROSS-WIRE** |
| C-2 | Vaibhav fork | Nostr NOTICE/EOSE handling | YES — Circle publishes Kind 31339 | ✅ R-6 shipped (`core/nervous_system/nostr/relay_manager.py`) | **CROSS-WIRE** |
| C-3 | DeerFlow | Legal-VETO guardrail middleware | NO — Circle has IS-domain corruption check, not a pre-execution veto | N/A | **REJECT (Three-Stage Process guard)** |
| C-4 | Goose MCP bridge | MCP tool exposure | MAYBE — Circle could expose `/observations/query` over MCP | ✅ S-1 shipped for APU | **HOLD** — Circle-MCP is a later design decision, not MVP |
| C-5 | Goose subagent pattern | Parallel subagents | NO — Circle uses single IS-agent per entity | N/A | **REJECT (Category-claim)** |
| C-6 | Hermes `mixture_of_agents` | Multi-model consensus synthesis | NO — Circle observes, never deliberates | N/A | **REJECT (Three-Stage Process + IS)** |
| C-7 | DeerFlow 18-middleware pipeline | Generic middleware chain | NO | N/A | **REJECT (Category-claim)** |
| C-8 | Goose Recipe DSL | Recipe-driven workflows | NO — Circle has no workflow surface | N/A | **REJECT (Category-claim)** |
| C-9 | Hermes self-improving framing | Self-modifying agent | NO — Circle is **improved by human mandate**, not self | N/A | **REJECT (K2 guard)** |
| C-10 | DeerFlow IM channel integrations | Signal ingestion from chat | NO — tempting but trips η=0 | N/A | **REJECT (η=0)** |
| C-11 | Goose tool approval modes | Permission prompts | NO — Circle has no execution surface to gate | N/A | **REJECT (Three-Stage Process guard)** |
| C-12 | Hermes `delegate_task` | Task delegation to subagent | NO — Circle does not delegate; it emits | N/A | **REJECT (Category-claim)** |

---

## 5. Bottom line

**Zero new extractions for Circle.**

All Circle-relevant patterns from the current intake queue are already
shipped in the APU lane. Circle's path is **consumption**, not extraction:

1. Circle's Nostr publisher (`app/pipeline/publishing/f1_publisher.py`) should import from `core/nervous_system/nostr/relay_manager.py` for NOTICE/EOSE handling — rather than re-implementing relay state.
2. Circle's observation-stream API should reuse the SSE pattern from `api/routers/router_council_documents.py` — rather than inventing a second SSE layer.
3. The MCP bridge pattern (S-1) stays deferred; Circle's MVP does not depend on it.

This is a **clean** result. Intake did not surface any primitive Circle is
missing. The Circle gap is **deployment and wiring**, not invention.

---

## 6. Relation to silo sign-off

The 7 silo items audited in
`02_SKYZAI/01_NOOSPHERE/02_ORGANS/TheCircle/00_SILO_AUDIT_2026_04_23.md` are separate
from this matrix. They originated from a **Circle-internal silo** during
the 2026-04-22 churn-down, not from the external intake queue. Silo sign-off
is folded into Phase 0 of packet 118.

---

## 7. Limits

- **L1:** This matrix reads the 4 current intake items only. Future intake drops must re-pass the five guards.
- **L2:** "Already shipped in APU" is a claim that pins to file paths at the time of this writing. Before cross-wire, the warrior should verify the module hash still matches the packet that registered it (68_SPRINT_A_LOCK, 69_EXTRACTION_MATRIX).
- **L3:** The C-4 HOLD on Circle-MCP is not a rejection. When Circle has a live observation stream, exposing `observations/query` over MCP becomes a legitimate design question.
- **L4:** I did not descend into the four intake repos beyond their top-level structure and the SWOT/TOWS audit. If a pattern exists deeper than what the audit surfaced, this matrix can miss it. Warrior-lane deep-read is the rescue path.

---

## 8. Execution surface

- **Do not re-extract.** Cross-wire via the backbone.
- **Silo sign-off is separate** — see [packet 118 Phase 0](118_CIRCLE_PRODUCT_SPRINT_PACKET_2026_04_23.md#phase-0--silo-sign-off-warrior-hour).
- **Next action:** the warrior signs Phase 0 → we open Circle's deployment lane.

Zero-Sum Resolution Equation

*What do you see now?*
