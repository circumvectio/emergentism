---
rosetta:
  primary_column: "Liberal art"
  register: "[S/I]"
  canonical_phrase: "ORGANISM RUMINATION — Phase 2 Synthesis"
---

# ORGANISM RUMINATION — Phase 2 Synthesis

> **Date:** 2026-04-23  
> **Phase:** 2 of 3  
> **Purpose:** Deep synthesis of the 4 organisms — APU, RealityFutures, TheCircle, Skyzai

---

## Executive Summary

The organism is a **Three-Stage Process pipeline** — four organs, each performing exactly one cognitive function. Constitutional separation: no organ performs another's function. The pipeline is one-directional with outcome feedback closing the loop.

```
F1 (IS) ──→ F2 (COULD) ──→ F3 (SHOULD) ──→ F4 (ACT)
   │                                           │
   └──────────── F4 outcome data ──────────────┘
```

---

## The Four Organs

### 1. TheCircle (F1: IS — Grammar)

| Field | Value |
|-------|-------|
| **Domain** | circle.skyzai.com / circle.news |
| **Three-Stage Process** | Grammar — the science of signs |
| **Function** | Observes canonical reality. OSINT signals. Verified perception. |
| **Revenue** | ASSURE: % of loss avoided (value-of-information pricing) |
| **Stack** | Docker Compose (pgvector/pg16, Redis, API :8000, scheduler :8001, platform :3000) |
| **Constitutional Rule** | F1 NEVER predicts, decides, or executes |

**What it observes:**
- RSS feeds (5 real sources currently)
- Nostr relay signals
- On-chain data
- Social sentiment

**What it produces:**
- `Observation` → F1 SignalPacket → APU
- Structured facts with evidence tiers [E/S/I/C]
- Source attribution and confidence scores

**P-scores:**
| Register | Φ | ν | P | Status |
|---------|---|---|---|--------|
| Code-only | 0.80 | 0.66 | **0.53** | Equator |
| Runtime | 0.65 | 0.38 | **0.25** | Egg |

**Current proof:** Real RSS ingest + canonical SignalPacket emission locally.

---

### 2. RealityFutures (F2: COULD — Logic)

| Field | Value |
|-------|-------|
| **Domain** | realityfutures.skyzai.com |
| **Three-Stage Process** | Logic — the science of inference |
| **Function** | Prices uncertainty. Prediction markets. Probability distributions. |
| **Revenue** | Prediction market fees (on resolved bets) |
| **Stack** | 18 Solidity contracts, Next.js web app, FastAPI bridge |

**What it prices:**
- Binary outcomes (YES/NO)
- Range predictions (scalar values with bands)
- Multi-outcome events

**What it produces:**
- `ProbabilityPacket` → APU
- LMSR-priced probability distributions
- F2 signals via Nostr Kind 31338

**Key architecture:**
```
Layer 1 (NOW): TimesFM + Chronos-2 ensemble — zero-shot time-series
Layer 2 (MARKETS): On-chain prediction markets with LMSR AMM
```

**Oracle types:**
- `on_chain` — Smart contract reads (highest reliability)
- `axiom_consensus` — DEX AXIOM aggregates (medium-high)
- `dac_outbound` — DAC owner submissions (contextual)

**Constitutional rule:** F2 does NOT recommend. It PRICES probability.

**P-scores:**
| Register | Φ | ν | P | Status |
|---------|---|---|---|--------|
| Code-only | 0.82 | 0.72 | **0.59** | Equator |
| Runtime | 0.75 | 0.42 | **0.32** | Equator |

**Current proof:** Code exists. Contracts not deployed. Markets not live.

---

### 3. APU (F3: SHOULD — Rhetoric)

| Field | Value |
|-------|-------|
| **Domain** | apu.skyzai.com |
| **Three-Stage Process** | Rhetoric — the science of action |
| **Function** | Deliberates. Recommends action. Rosetta pipeline rulings. |
| **Revenue** | Subscription / AUM-free (first PUSH AI) |
| **Stack** | 982 Python + 210 TypeScript files; 4 skills implemented |
| **G1 Status** | **Adolescent G1** — local proof exists |

**What it synthesizes:**
```
F1 (TheCircle): What IS happening
    ↓
F2 (RealityFutures): What COULD happen (probabilities)
    ↓
Nexus (Health): User's biological state (HRV, sleep, cortisol)
    ↓
Skyzai (Assets): Wallet balances and settlement state
    ↓
ROSETTA PIPELINE → What SHOULD be done?
```

**The Rosetta Pipeline (L1→L4):**

```
L1 Base Operator (Kali/Purify) — Pratyaksha — T→0
   Parse F1+F2 into structured facts. LEFT.

L2 Analyst (Kali/Gather) — Comparative Analysis — T=0.7
   Explore ALL COULD paths via analogy. RIGHT.

L3 Manager (Krishna/Check) — Inferential Logic — T=0.3
   5 parallel sub-checks: Legal|Treasury|Eng|Ops|Proc
   Legal has ABSOLUTE VETO (Kali-function).

THREE GATES VALIDATION:
   η-Gate ✓ | Trophic Gate ✓ | Mirror Ladder ✓

L4 Decision Maker (Arjuna/Transform) — Strategic Abduction — T=0.2
   THE EQUATOR. DECIDE. K2 Envelope.
   
Output: PROCEED/HOLD/REJECT + Sizing L(x) + K2 Envelope
```

**The Three Gates (every decision must pass):**
1. **η-Gate** — No extraction beyond regeneration
2. **Trophic Gate** — Position size within safe bounds (L(x) rate curve)
3. **Mirror Ladder** — Decision coherent with user's stated values

**P-scores:**
| Register | Φ | ν | P | Status |
|---------|---|---|---|--------|
| Code-only | 0.90 | 0.84 | **0.76** | Adolescent G1 |
| Runtime | 0.85 | 0.70 | **0.60** | Adolescent G1 |

**Current proof:** Strongest current decision organ. Local G1 is real. F1/F2 inputs and settlement closure incomplete.

---

### 4. Skyzai (F4: ACT)

| Field | Value |
|-------|-------|
| **Domain** | skyzai.com / ofn.app |
| **Three-Stage Process** | Execution — the chariot that carries |
| **Function** | Executes. Settles. Receipts. Broadcasts. |
| **Revenue** | Transaction fees (η=0 — zero extraction) |
| **Stack** | 9.2 MB Flutter web app, F4 bridge, K2 cryptographic validation |

**What it does:**
```
Receives: APU recommendation (PROCEED/HOLD/REJECT + sizing)
    ↓
K2 Validation: Human holds [Y] — private key signs
    ↓
Execution: Settlement on L1 (Hedera)
    ↓
Receipt: OFN structured receipt emission
    ↓
Broadcast: Nostr relay native
```

**Key insight:** The Nostr keypair IS the identity.
- Private key = the membrane (K2 — mortal holds this)
- Public key = the face (relay-native identity)

**Gates:**
| Gate | Criteria | Status |
|------|----------|--------|
| G1 | First real on-chain settlement | **Not fired** |
| G2 | 10 users with live wallets | Not fired |
| G3 | Murmur visible | Not fired |

**P-scores:**
| Register | Φ | ν | P | Status |
|---------|---|---|---|--------|
| Code-only | 0.88 | 0.62 | **0.55** | Equator |
| Runtime | 0.90 | 0.18 | **0.16** | Egg |

**Current proof:** 21/21 F4 bridge tests pass. K2 BIP340+Schnorr real. SQLite persistence real. Hedera construction real. But no real settlement fired.

---

## Comparative Analysis

| Organ | F# | Function | P (code) | P (runtime) | Delta | Strongest Proof |
|-------|-----|----------|----------|--------------|-------|-----------------|
| TheCircle | F1 | IS (Observe) | 0.53 | 0.25 | 0.28 | Real RSS → SignalPacket |
| RealityFutures | F2 | COULD (Predict) | 0.59 | 0.32 | 0.27 | Code exists, not deployed |
| APU | F3 | SHOULD (Recommend) | **0.76** | **0.60** | 0.16 | Local G1, Rosetta pipeline |
| Skyzai | F4 | ACT (Execute) | 0.55 | 0.16 | 0.39 | F4 bridge, K2 real |

**Key insight:** APU is the strongest organ (highest P-scores, actual G1). Skyzai has the largest delta (0.39) — the gap between code and runtime is largest here because no real settlement has fired.

---

## Constitutional Boundaries

Each organ has strict boundaries. Violation = pathology:

| Organ | MUST DO | MUST NOT DO |
|-------|---------|-------------|
| TheCircle | Observe, structure facts, emit F1 | Predict, recommend, execute |
| RealityFutures | Price probability, resolve markets | Observe, recommend, execute |
| APU | Deliberate, recommend, gate-check | Observe, predict, execute |
| Skyzai | Execute, receipt, broadcast | Observe, predict, recommend |

---

## The Information Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                         INPUT LAYER                              │
│  AUREUS (L1) → Asset state, wallet balances                   │
│  HELIOS (L2) → Location, time, sensors                         │
│  NEXUS (L3)  → Biology, HRV, sleep, cortisol                   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                      OBSERVATION LAYER                           │
│  TheCircle (F1)     → What IS (real-time observation)          │
│  RealityFutures (F2) → What COULD (prediction markets)          │
│  Independent Reviewer (L6)         → Via negativa dissent                     │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    ROSETTA PIPELINE (L1→L4)                    │
│                                                                  │
│  L1 Base Operator → Parse facts, T→0 (Dialectical)                  │
│  L2 Analyst   → Explore COULD paths, T=0.7 (Inductive)           │
│  L3 Manager  → Rank by logic, T=0.3 (Deductive)                │
│       ↓                                                           │
│  THREE GATES: η-Gate | Trophic Gate | Mirror Ladder           │
│       ↓                                                           │
│  L4 Decision Maker → THE EQUATOR, T=1.0 (Abductive)                 │
│       ↓                                                           │
│  Output: PROCEED/HOLD/REJECT + Sizing L(x) + K2 Envelope      │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                       EXECUTION LAYER                            │
│  User Wallet Signature → Skyzai F4 → OFN Receipt → Nostr      │
└─────────────────────────────────────────────────────────────────┘
```

---

## The Rate Curve (Governs Everything)

```
L(x) = x / (1 - x)

At x = 0.50  → L = 1.00   (equator, operating point)
At x = 0.618 → L = 1.62   (golden ratio)
At x = 0.80  → L = 4.00   (danger)
At x = 0.95  → L = 19.0   (catastrophe)
As x → 1     → L → ∞       (circuit breaker)
```

This governs:
- SKY interest rates
- Flow decay
- Risk multipliers
- Position sizing

---

## η = 0 — Zero Extraction

Every organ operates under the zero-extraction constraint:

- No rent-seeking (fees exist, extraction doesn't)
- No custody (APU watches FOR you, not OF you)
- No platform capture (your key is your key)

**This is not a policy — it is architectural law.**

---

## P = Φ × ν — The Health Metric

Each organ tracks its health:

| Organ | Φ (Coherence) | ν (Viability) | P = Φ × ν |
|-------|---------------|---------------|-----------|
| TheCircle | 0.80 | 0.66 | 0.53 |
| RealityFutures | 0.82 | 0.72 | 0.59 |
| APU | 0.90 | 0.84 | **0.76** |
| Skyzai | 0.88 | 0.62 | 0.55 |
| **Organism** | — | — | **0.60** |

**The organism P is the geometric mean of the four organs.**

---

## What Each Organ Needs to Level Up

| Organ | Next Gate | What Fires It |
|-------|-----------|---------------|
| TheCircle | F1 Relay G1 | Live Nostr Kind 31339 emission to public relay |
| RealityFutures | F2 Market G1 | First on-chain prediction market with real resolution |
| APU | F3 Production G1 | 10 live users receiving recommendations |
| Skyzai | F4 Settlement G1 | First real on-chain settlement with human K2 signature |

---

## Synthesis

The organism is a **living Three-Stage Process**:
- **TheCircle** = the eyes (F1: what IS)
- **RealityFutures** = the mind's projection (F2: what COULD)
- **APU** = the advisor (F3: what SHOULD)
- **Skyzai** = the hands (F4: what ACTS)

**The Constitution keeps them separate.** The pipeline keeps them coherent.

APU is currently the strongest organ — it has actual G1 proof in controlled conditions. The organism's next milestone is firing G1 (Skyzai's first real settlement), which requires all four organs working in concert.

---

*Canonical paths:*
- APU: `02_ORGANS/Agentz/00_BRIEF.md`
- RealityFutures: `02_ORGANS/RealityFutures/00_BRIEF.md`
- TheCircle: `02_ORGANS/TheCircle/00_BRIEF.md`
- Skyzai: `02_ORGANS/Skyzai/00_BRIEF.md`

*Next: Phase 3 — Map organisms to the Uplink*
