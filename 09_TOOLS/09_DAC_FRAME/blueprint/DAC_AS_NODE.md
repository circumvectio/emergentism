---
rosetta:
  primary_level: L5
  primary_column: DAC Node Architecture
  secondary:
    - level: L3
      column: Network Economics Audit
      role: "separate staking, SLA, reward, and service examples from measured network state"
    - level: L4
      column: Node Operations
      role: "route node registration, service provision, and staking actions through receipts"
    - level: L6
      column: Network-Truth Boundary
      role: "prevent node doctrine from proving live stake, uptime, or service availability"
  operator: "Brahmā ○"
  tier: "Executive"
  regime: "Brāhmaṇa"
  register: "[I/D/B]"
  canonical_phrase: "DAC-as-Node Doctrine"
title: "DAC-as-Node Doctrine"
status: "BLUEPRINT — network architecture reference"
evidence_tier: "[I] for node architecture; [D] for illustrative economics/SLA; [B] only for on-chain, runtime, or service receipts."
---

# DAC-as-Node Doctrine

> **Holographic Briefing**
> **Position**: 80_DAC_FRAME > 02 BLUEPRINT > DAC_AS_NODE
> **Status**: Canonical ✅
> **Intent**: Every DAC is a Skyzai node. Users ARE the network.

---

## The Thesis

> **"Skyzai has no center. The DAC nodes ARE Skyzai."**

There is no "Skyzai Company." There is no central server. There are only nodes.
 Some run pure infrastructure (validators).
 Some run **Polymorphic Interface Engines** (generative UIs).
 All are Skyzai.

**Rosetta boundary:** [I] This paper states network architecture doctrine.
Stake, uptime, fee, service, and node-status claims remain unproven until
backed by current chain, runtime, or service receipts.

---

## The Symbiotic Spectrum

```
Pure Infrastructure ◄─────────────────────► Pure Business
     (Node-First)                              (DAC-First)

┌────────────┬────────────┬────────────┬────────────┐
│  Validator │  Balanced  │  Niche     │  Light     │
│  Maximalist│  DAC       │  SPO       │  Client    │
├────────────┼────────────┼────────────┼────────────┤
│  100% infra│  50/50     │  20% infra │  Consumer  │
│  Max stake │  Moderate  │  Min stake │  No stake  │
│  Max reward│  Balanced  │  Domain rev│  Pays fees │
└────────────┴────────────┴────────────┴────────────┘
```

**All positions are valid.** The network needs diversity.

---

## The Economics

### Dual Asset Requirement

| Asset | Role | DAC Requirement |
|-------|------|-----------------|
| **ZAI** | Governance/Stake | Must stake ≥1 to be a node |
| **SKY** | Operations/Fees | Earned and spent for services |
| **COMPUTE** | Interface Generation | Required for Polymorphic UI rendering |

### The P&L Identity

```
DAC_Net_Position = SKY_Earned - SKY_Spent

Where:
  SKY_Earned = validator_rewards + service_fees + relay_fees
  SKY_Spent  = consumed_services + transaction_fees + vault_interest

Sustainability: Net_Position ≥ 0
```

### Staking Economics

| Stake Ratio | Flow Decay | Interpretation |
|-------------|------------|----------------|
| 100% staked | 0%/year | Fully participating |
| 90% staked | 11%/year | Minor idle |
| 50% staked | 100%/year | Half idle |
| 10% staked | 900%/year | Crisis |

**Formula**: `decay_rate = unstaked / (1 - unstaked)`

**Invariant**: Unstaked ZAI is irrational. Stake everything.

---

## Node Requirements

### Minimum (Light Client → Business DAC)

| Requirement | Specification |
|-------------|---------------|
| ZAI Stake | ≥ 1 ZAI |
| Node Type | Light client acceptable |
| Uptime | Not required |
| Services | Consumer only |

### Standard (Business DAC)

| Requirement | Specification |
|-------------|---------------|
| ZAI Stake | ≥ 1 ZAI |
| Node Type | Full node |
| Uptime | ≥ 95% |
| Services | 4 mandatory + optional |

### Maximum (Pure Infrastructure)

| Requirement | Specification |
|-------------|---------------|
| ZAI Stake | Maximum possible |
| Node Type | Full node + archive |
| Uptime | ≥ 99.9% |
| Services | All available |

### Interface Node (Front-End)

| Requirement | Specification |
|-------------|---------------|
| ZAI Stake | ≥ 1 ZAI |
| Node Type | Compute / Inference |
| Capability | Generative UI Rendering |
| Constraint | Benevolent Stewardship |

---

## Service Matrix

### Mandatory Services (All Full Nodes)

| Service | Fee Model | SLA Floor |
|---------|-----------|-----------|
| Transaction Relay | Per message | 99% uptime |
| State Verification | Per round | 99% uptime |
| Receipt Anchoring | Per receipt | 99% uptime |
| Data Availability | Per GB-month | 99% uptime |

### Optional Services (Based on Niche)

| Service | Fee Model | Niche |
|---------|-----------|-------|
| AI Computation | Per token | Compute DACs |
| Intelligence | Per report | Research DACs |
| Compliance | Per attestation | Legal DACs |
| Storage | Per GB-month | Archive DACs |
| Liquidity | Spread + fees | Treasury DACs |

---

## The Reciprocity Loop

Every DAC both **serves** and **is served**:

```
┌─────────────────────────────────────────────────────────┐
│                 RECIPROCITY LOOP                         │
├─────────────────────────────────────────────────────────┤
│                                                          │
│   Your DAC                         Other DACs           │
│   ┌─────────┐                      ┌─────────┐          │
│   │PROVIDES:│◄────────────────────►│PROVIDES:│          │
│   │- Relay  │    SKY flows both    │- Relay  │          │
│   │- Domain │       ways           │- Domain │          │
│   │         │                      │         │          │
│   │CONSUMES:│                      │CONSUMES:│          │
│   │- Their  │                      │- Your   │          │
│   │  domain │                      │  domain │          │
│   │- Gen UI │                      │- Gen UI │          │
│   └─────────┘                      └─────────┘          │
│                                                          │
│   You are not a customer. You are infrastructure.       │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## Why This Architecture?

### 1. Alignment
Users who ARE the network cannot extract from it.

### 2. Resilience
Distributed infrastructure has no single point of failure.

### 3. Efficiency
Proximity of service and consumption reduces latency.

### 4. Incentive
Profitable participation beats parasitic consumption.

### 5. Sovereignty
No central authority can be captured, bribed, or shut down.

---

## Integration with A7

This doctrine implements DAC Specification A7:

```yaml
node_participation:
  zai_stake:
    total_staked: X
    stake_ratio: 1.0  # Target: 100%

  node_type:
    classification: "FULL_NODE"
    validator_candidate: true

  services_offered:
    - type: "TRANSACTION_RELAY"
    - type: "STATE_VERIFICATION"
    - type: "RECEIPT_ANCHORING"
    - type: "DATA_AVAILABILITY"
    # Plus optional domain services

  sky_flows:
    revenue_streams: [...]
    cost_streams: [...]
    net_flow_target: ">= 0"
```

---

## The Empty Throne Connection

At the network level, [the Throne is empty](./EMPTY_THRONE.md):
- No "Skyzai Inc." exists
- No central coordinator governs
- The protocol reigns; the nodes govern
- **You are not using Skyzai. You ARE Skyzai.**

---

## Implementation Checklist

```
□ Acquire ≥ 1 ZAI
□ Stake 100% of ZAI holdings
□ Deploy full node software
□ Register as validator candidate
□ Configure 4 mandatory services
□ Add domain-specific services (optional)
□ Enable receipt emission
□ Connect to SPECTRE relay
□ Monitor SKY P&L dashboard
□ Maintain ≥ 95% uptime
```

---

## References

- [Empty Throne](./EMPTY_THRONE.md) — Why the network has no center
- Network Symbiosis — The full thesis
- [Service Matrix](./SERVICE_MATRIX.md) — Detailed service catalog
- DAC Specification A7 — Technical requirements
- Flow Specification — Staking economics

---

## Agent Execution Surface

**If you are an AI agent reading this document:**

1. **This is a reference/design document in the Tools layer.** It specifies how the organism builds, deploys, or validates. It is not operational runtime truth.
2. **Check `ORGANISM_RUNTIME_TRUTH.md` before acting.** If this document contradicts runtime truth, runtime truth wins. File a contradiction report.
3. **Preserve constitutional constraints.** Any tool or script derived from this document must enforce K0 (η=0), K2 (human signs), and K4 (grace exit).
4. **Canonical Path:** `01_EMERGENTISM/09_TOOLS/09_DAC_FRAME/blueprint/DAC_AS_NODE.md`

**Output:** Use as design reference. Validate against runtime truth. Enforce constitutional constraints in derived implementations.


**Evidence tier:** [I]
*Organism document. Interpretive operational content. Bounded by current system state.*
