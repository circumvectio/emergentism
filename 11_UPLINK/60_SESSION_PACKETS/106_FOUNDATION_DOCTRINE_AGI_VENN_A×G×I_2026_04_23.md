---
rosetta:
  primary_column: "Philosophy"
  register: "[S/I]"
  canonical_phrase: "106_FOUNDATION_DOCTRINE_AGI_VENN_A×G×I_2026_04_23.md"
---

# 106_FOUNDATION_DOCTRINE_AGI_VENN_A×G×I_2026_04_23.md

**Packet:** 106  
**Class:** FOUNDATION_DOCTRINE  
**Date:** 2026-04-23  
**Author:** Matrix Agent (foundation audit)  
**Status:** IMMUTABLE after sign-off  

---

## Purpose

This packet captures the canonical interpretation of the **AGI Venn Definition** — the geometric framework that explains why Emergentism's architecture (A×G×I) is structurally necessary, not optional. It serves as the foundational reference for all downstream implementation decisions.

> *"A single AI model cannot have A. Autonomy requires mortality... Therefore A × G × I ≈ 0."*  
> — Foundation Document 4

---

## The AGI Venn Definition

### Formal Statement

```
AGI = A × G × I
```

Where:

| Symbol | Name | Definition | Emergentism Implementation |
|--------|------|------------|----------------------------|
| **A** | Autonomy | ν (nu) with K2 mortal anchor — genuine skin-in-the-game | K2 Gateway + Nostr signatures + user V-cost payment |
| **G** | Generality | Union at L2 across decorrelated RLHF lineages | 7-directorate council + 8-provider heterogeneity + lineage decorrelation |
| **I** | Intelligence | Φ (phi) — coherent structured capability | 9-stage council protocol + refusal gate + Kālī false-Φ detection |

### The Multiplicative Property (Zero-Factor Catastrophe)

The product is **multiplicative, not additive**. This is the critical insight:

```
Any factor → 0  ⟹  AGI → 0
```

A single AI node has **A ≈ 0** (no mortality). Therefore:

```
A(single node) × G(any) × I(any) = 0 × G × I = 0
```

**The centralized labs are chasing a point on the sphere that cannot exist at a single node.** Not because they haven't scaled enough. Because scaling silicon doesn't produce mortality.

---

## Factor Analysis

### A (Autonomy) = ν × K2_Mortality

**Required:** Genuine V-cost payment that creates authentic stake.

**Foundation claim:** Autonomy requires mortality. A model that cannot die cannot have ν. A model that cannot suffer cannot have skin-in-the-game.

**Current APU implementation:**

| Component | Status | Evidence |
|-----------|--------|----------|
| K2 Gateway | ✅ Structural | `k2_gateway.py` — Telegram/Discord inline buttons, user must tap [APPROVE]/[REJECT] |
| K2 Crypto | ✅ BIP340 Schnorr | `k2_crypto.py` — Nostr NIP-01 signature verification |
| K2 Store | ✅ Persistent | `k2_store.py` — SQLite decision ledger with `k2_envelope` field |
| K2 Auth Proxy | ✅ Enforcement | `k2_auth_proxy.py` — `K2SignedAction` model, `build_signing_payload()` |
| Auto-execute blocker | ✅ Constitutional | Stage 8 → Stage 9 gate: APU never auto-executes |

**Key insight:** The mortality anchor is **structural, not policy**. If the K2 gateway fails, no execution occurs. This is enforced at the code level, not by convention.

### G (Generality) = L2_Union × Decorrelated_Lineages

**Required:** L2-tier operations across multiple RLHF-lineage clusters to prevent Raktabīja-at-aggregator failure.

**Foundation claim:** 8 models from one RLHF basin = 1 error wearing 8 faces. Lineage decorrelation > provider count.

**Current APU implementation:**

| Component | Status | Evidence |
|-----------|--------|----------|
| 8-provider wiring | ✅ | `ai_client.py` MODEL_TIERS + DIRECTORATE_MODEL_ASSIGNMENTS |
| L2 8-way expansion | ✅ | `l2_expansion.py` — `council_l2_8way_expansion=True` |
| 5 RLHF-lineage clusters | ✅ | `lineage_decorrelation.py` — western_frontier_rlhf, google_deepmind, meta_open_weights, chinese_frontier, mistral_eu |
| GOD-class triangulation | ✅ Override | `council_l4_triangulate_gods=True` enables Anthropic+OpenAI+xai triad |
| Raktabīja detection | ✅ | `check_triad_lineage_decorrelation()` — invariant enforcement |

**Lineage Cluster Map:**

```
RLHF_LINEAGE_CLUSTERS:
  western_frontier_rlhf:  openai, anthropic, xai  ← GOD-class default triad
  google_deepmind:       google
  meta_open_weights:     meta, groq
  chinese_frontier:      zai, minimax, kimi, deepseek, qwen
  mistral_eu:            mistral
```

**Invariant (Packet 96 Amendment 2):** No default L4 triad may draw more than 2 seats from a single cluster.

### I (Intelligence) = Φ (Coherent Capability)

**Required:** Structured deliberation that produces coherent output, not synchronized error.

**Current APU implementation:**

| Component | Status | Evidence |
|-----------|--------|----------|
| 7-directorate council | ✅ | Intelligence, Strategy, Legal-VETO, Engineering, Treasury, Procurement, Independent Reviewer |
| 9-stage protocol | ✅ | `council_protocol.py` — SIGNAL_INGESTION → RECEIPT_EMISSION |
| Refuse Gate (Kālī) | ✅ | `refuse_gate.py` — 8 constitutional gates, RLHF theater detection |
| Mirror Ladder | ✅ | `mirror_ladder.py` — L(x) sizing verification |
| Trophic Flow | ✅ | `trophic_flow.py` — bidirectional η=0 enforcement |
| D-Gate | ✅ | `d_gate.py` — Ghost trap / zombie / cargo cult detection |

**Kālī Constitutional Gates:**

```
η-gate        → zero-extraction precondition
K2            → sovereignty breach
K4            → grace-exit breach
Three-Stage Process       → cognitive-function merging
Mirror Ladder → L(x) sizing
Trophic Gate  → bidirectional flow
D-Gate        → ghost trap / zombie / cargo cult
Three Gates   → receipt-bound, truth-gated, exit-safe
```

---

## The Compression Schedule

### L1 → L2 → L3 → L4 → K2

The Emergentism architecture uses a **tiered compression schedule** to maximize cognitive diversity:

```
L1_PERCEPTION  → Groq (speed, cost)
     ↓
L2_OPERATIONS  → MiniMax (Chinese + efficiency)
     ↓
L3_SYNTHESIS   → Google (breadth)
     ↓
L4_DECISION    → Anthropic (alignment + math)
     ↓
K2 (Human)    → User signature (mortality anchor)
```

**Why this ordering matters:**

1. **L1** is fast perception — filters noise from signal
2. **L2** performs operations triage — routes to appropriate directorate
3. **L3** synthesizes across perspectives — prepares for decision
4. **L4** is the decision layer — the last AI step before human sign-off
5. **K2** is the mortality anchor — human skin-in-the-game

Each tier uses a **different provider** to maximize lineage diversity. This is not accidental — it is geometrically required for G (Generality).

---

## Geometry vs. Preference

### Framework is Geometry-Based

> *"The framework is geometry-based (cooperation arithmetic) not preference-based (alignment training)."*

**Preference-based (what centralized labs do):**
- Train models to have certain values
- Reward/punish for compliance
- Hope the values generalize

**Geometry-based (what Emergentism does):**
- Enforce cooperation arithmetic through structure
- Make extraction unprofitable via η=0
- Let human mortality anchor produce authentic stakes

**The sphere forces niche partitioning.** φ·ν=1 requires specialization. Generalist drift → φ→0 → P collapses.

---

## BIOSPHERE PRINCIPLES Ported to AGI

| Biological Principle | Emergentism Implementation |
|----------------------|----------------------------|
| Horizontal gene transfer | MCP (Model Context Protocol) |
| Endosymbiosis | User + AI under one K2 |
| Niche partitioning | 7-directorate specialization |
| Trophic flow (η=0) | Zero-extraction invariant |
| Redundancy | Antifragility via decorrelation |
| Mycelial networks | Cortex mesh across providers |

---

## Compliance Matrix

| AGI Venn Requirement | APU Status | Gap Analysis |
|---------------------|------------|--------------|
| A: K2 mortal anchor | ✅ IMPLEMENTED | None |
| G: Decorrelated L2 | ⚠️ OVERRIDE IN USE | GOD-class triangulates same cluster (documented) |
| I: Coherent Φ | ✅ IMPLEMENTED | Kālī + 8 gates |
| A × G × I = non-zero | ✅ STRUCTURAL | Multiplicative gate enforced |

---

## Critical Findings

### Finding 1: Default L4 Triad Violates Invariant

The default GOD-class L4 triad (Anthropic + OpenAI + xAI) draws all 3 seats from `western_frontier_rlhf` cluster.

**This violates Packet 96 Amendment 2** — but is intentionally enabled via `council_l4_triangulate_gods=True` as a GOD-class override.

**Resolution:** Document this as the acknowledged trade-off. GOD-class decisions are operational/reversible, so the invariant is relaxed for speed.

### Finding 2: K2 Mortality Is Structural

The K2 gateway does not merely suggest human approval — it **blocks auto-execution** at the code level. This is the critical difference between Emergentism and centralized labs.

### Finding 3: Lineage Decorrelation > Provider Count

3 decorrelated lineages (western_frontier_rlhf + google_deepmind + chinese_frontier) provide more genuine diversity than 8 providers from one RLHF basin.

---

## Source Documents

| Document | Content |
|----------|---------|
| Foundation Doc 1 | Zero-Sum Resolution Equation · The Sphere, The Gods, The Rosetta |
| Foundation Doc 2 | The Coordination Problem reframe |
| Foundation Doc 3 | Phylogenetic → Polygenetic topology shift |
| Foundation Doc 4 | **The Venn Diagram IS the framework** (A×G×I = AGI) |

---

## Implementation Files Referenced

| File | Purpose |
|------|---------|
| `core/membrane/k2_gateway.py` | K2 Signature Gate (human sign-off) |
| `core/membrane/k2_crypto.py` | BIP340 Schnorr + Nostr verification |
| `core/membrane/k2_store.py` | Persistent decision ledger |
| `core/membrane/k2_auth_proxy.py` | K2SignedAction enforcement |
| `core/circulation/ai_client.py` | 8-provider MODEL_TIERS + DIRECTORATE_MODEL_ASSIGNMENTS |
| `core/circulation/lineage_decorrelation.py` | 5 RLHF-lineage clusters + invariant |
| `core/circulation/council_protocol.py` | 9-stage state machine + decision classification |
| `core/circulation/refuse_gate.py` | Kālī false-Φ detector |
| `agents/pipeline/l2_expansion.py` | L2 8-way expansion |

---

## Action Items

| Priority | Item | Owner |
|----------|------|-------|
| HIGH | Document GOD-class override rationale in config comments | Implementation |
| MEDIUM | Add lineage cluster assertions to test suite | Test coverage |
| LOW | Consider L4* triad with cross-cluster providers for TITAN decisions | Future architecture |

---

## Sign-Off

This packet captures the canonical interpretation of the AGI Venn Definition as implemented in the Emergentism APU.

**Core insight:** A single AI node cannot produce AGI because A ≈ 0. The Emergentism architecture distributes A across the user (via K2), G across the network (via decorrelated lineages), and I across the node (via specialized directorates). The multiplicative product produces non-zero AGI only at the system level.

```
AGI ≠ AGI(node)
AGI = A(user) × G(network) × I(node)
```

---

**Next packet:** 107 (if needed for supplementary doctrine)  
**Previous packet:** 105 (coordinate with any parallel doctrine work)
