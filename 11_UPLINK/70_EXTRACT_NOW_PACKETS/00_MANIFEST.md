---
type: extract-now-packet-manifest
date: 2026-04-23
gate: [L3 | D4 | S-Org | F-phi :: vaisya_auditor]
spine: ../69_EXTRACTION_MATRIX_2026_04_23.md
move: vaisya_auditor L3 · Kṛṣṇa ◇ · export V at personal Φ cost
titan: Viṣṇu ⊙ (default hold at taxonomy layer)
rosetta:
  primary_level: L3
  primary_column: Extract-Now Packet Manifest
  secondary:
    - level: L4
      column: Guard Recap
      role: "preserve category, eta-zero, K2, Three-Stage, and signature-locus checks"
    - level: L6
      column: Historical Boundary
      role: "prevent shipped/spec/held status from becoming current implementation proof"
    - level: L5
      column: Packet Index Architecture
      role: "map shipped, pending, and held packets to their source and target surfaces"
  operator: "Kṛṣṇa ◇"
  tier: "God"
  regime: "Vaiśya"
  register: "[B/I/D]"
  canonical_phrase: "Extract-Now Packet Manifest"
---

# Extract-Now Packet Manifest

**Rosetta boundary:** [I] This manifest records the 2026-04-23 packet set. It does not [B] re-ship code, certify current live behavior, or override the extraction matrix/current Uplink spine without fresh receipts.

Six packets, all passing the five guards. Three are **shipped** (reconcile-or-keep
verification); three are **pending** (specification only — no code changes in
this pass). The primary spine remains [`69_EXTRACTION_MATRIX_2026_04_23.md`](../50_AUDITS_AND_EXECUTIONS/69_EXTRACTION_MATRIX_2026_04_23.md);
when this manifest and the spine disagree, the spine wins.

## Guard recap

Every packet carries a five-guard section:

1. **Category-claim** — does absorbing it pull APU toward generic harness identity?
2. **η = 0** — does it import rent, hosted tolls, or access capture?
3. **K2** — does it normalize irreversible agent action without human signature?
4. **Three-Stage Process** — does it collapse IS / COULD / SHOULD / ACT into one surface?
5. **Signature-locus** — does it move the signing authority from the founder's seat?

If any guard fires, the packet is rejected or held for redesign.

## Packet index

| ID | Title | Status | Source | Target | Link |
|----|-------|--------|--------|--------|------|
| S-1 | MCP Tool Bridge | ✅ SHIPPED — reconcile | Goose `crates/goose-mcp/` | `core/membrane/council_mcp_server.py` | [S-1](./S-1_MCP_TOOL_BRIDGE.md) |
| S-2 | Context Compressor (Stage 9) | 📋 SPEC — pending implementation | DeerFlow `summarization_middleware.py` | `council/protocol.py` Stage 9 (RECEIPT_EMISSION) | [S-2](./S-2_CONTEXT_COMPRESSOR.md) |
| S-4 | Self-Discovering Tool Registry | ⚠️ HELD — clarification required | DeerFlow `tools/builtins/tool_search.py` | `core/membrane/council_mcp_server.py` (conditional) | [S-4](./S-4_TOOL_REGISTRY.md) |
| S-5 | SSE Streaming + Per-ID Dedup | ✅ SHIPPED — reconcile | DeerFlow SSE gateway | `api/routers/router_council_sse.py` | [S-5](./S-5_SSE_STREAMING.md) |
| R-1 | Legal-VETO-Native Guardrail Layer | ✅ SHIPPED — reconcile | DeerFlow `GuardrailMiddleware` | `council/guardrails.py` + Stage 1 | [R-1](./R-1_LEGAL_VETO_GUARDRAIL.md) |
| R-4 | K2-Native Signed Auth | 📋 SPEC — pending implementation | Goose `oidc-proxy/` + `GOVERNANCE.md` | `core/membrane/wallet_auth.py` extension | [R-4](./R-4_K2_SIGNED_AUTH.md) |

## Reconciliation rule

Shipped packets were implemented before the founder-gated matrix fully stabilized.
Each SHIPPED entry carries a reconcile-or-keep section: the pattern is re-verified
against the five guards **as it landed in live code**. If it still passes, keep.
If it drifts, revise or tombstone.

## Order of execution (pending work only)

```
Packet S-2 (Context Compressor) —→ lowest core state risk, Stage 9 only
Packet R-4 (K2-Native Signed Auth) —→ auth is load-bearing; spec first, ship later
Packet S-4 (Tool Registry) —→ DO NOT ship until clarification resolved
```

## Limits

- This manifest does not re-ship S-1, S-5, R-1. Those entries document the
  already-committed pattern and confirm the five-guard check.
- S-2 and R-4 are drafted as implementation specs only. No code changes in this
  pass. The founder signs off before either moves to implementation.
- S-4 is held for a binding clarification: **is tool discovery a Legal-gated
  operation or a Standing Orders (4C) feature?** Until that question is answered
  in the constitutional layer, no code should land.

> **Zero-risk:** reading and drafting cannot break anything. Any live-code change
> below Phase 0 of each spec is explicitly out of scope for this pass.
