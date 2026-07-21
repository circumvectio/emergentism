---
rosetta:
  primary_level: L5
  primary_column: Service Reciprocity Architecture
  secondary:
    - level: L3
      column: Service Evidence Audit
      role: "separate template status, SLA, SKY, uptime, staking, and node claims from current operating receipts"
    - level: L4
      column: Service Operations
      role: "route services provided/consumed, economics, staking, node configuration, and checklist into verifiable operations"
    - level: L6
      column: Template Boundary
      role: "prevent example matrix rows from becoming financial commitments, live service claims, or network proof"
  operator: "Brahmā ○"
  tier: "Executive"
  regime: "Brāhmaṇa"
  register: "[I/D/B]"
  canonical_phrase: "Service Matrix — What This DAC Provides & Consumes"
title: "Service Matrix — What This DAC Provides & Consumes"
status: "BLUEPRINT — service-matrix template"
evidence_tier: "[I] for service-matrix doctrine; [D] for placeholder/example economics; [B] only for current SLA, node, staking, SKY-flow, or service receipts."
---

# Service Matrix — What This DAC Provides & Consumes

> **Holographic Briefing**
> **Position**: 80_DAC_FRAME > 02 BLUEPRINT > SERVICE_MATRIX
> **Status**: Template / Customizable
> **Intent**: To declare all services this DAC offers to the network and consumes from the network, ensuring economic reciprocity.

---

## The Reciprocity Principle

> **"You are not a customer. You are infrastructure."**

Every DAC both **serves** and **is served**. This matrix tracks both sides of the equation to ensure:
- **Economic sustainability**: `SKY_Revenue ≥ SKY_Costs`
- **Network contribution**: You give back what you take
- **Transparent accounting**: All flows are measurable

**Rosetta boundary:** [I] This paper is a service reciprocity template. [D]
Example fees, SKY amounts, statuses, uptime targets, providers, and node
settings are placeholders until replaced by current receipts. It does not [B] prove
live services, staking, profitability, SLA compliance, or network deployment.

---

## Services Provided

### Mandatory Services (All Full Nodes)

| Service | Fee Model | SLA | Status |
|---------|-----------|-----|--------|
| **Transaction Relay** | Per message | 99% uptime | ✅ Active |
| **State Verification** | Per round | 99% uptime | ✅ Active |
| **Receipt Anchoring** | Per receipt | 99% uptime | ✅ Active |
| **Data Availability** | Per GB-month | 99% uptime | ✅ Active |

### Interface Services (Generative Nodes)

| Service | Fee Model | SLA | Status |
|---------|-----------|-----|--------|
| **Polymorphic UI** | Per Session | <200ms Latency | ⚠️ Beta |
| **Prompt Optimization** | Per Update | N/A | ✅ Active |

### Optional Services (Domain-Specific)

| Service | Fee Model | SLA | Status |
|---------|-----------|-----|--------|
| _[Example: AI Computation]_ | Per token | 95% uptime | ⚠️ Planned |
| _[Example: Legal Review]_ | Per attestation | 98% uptime | ⚠️ Planned |
| _[Example: Treasury Management]_ | % of AUM | N/A | ❌ Not Offered |

**Instructions**: [I] Replace example rows with your DAC's actual domain services.

---

## Services Consumed

### Network Infrastructure

| Service | Provider Type | SKY Cost | Frequency |
|---------|---------------|----------|-----------|
| Transaction Relay | Network | Variable | Per tx |
| State Verification | Network | Variable | Per round |
| Data Availability | Network | Variable | Per GB |
| LLM Inference | Compute Node | Token-based | Per frame |

### SPO Subscriptions (A2 Integrations)

| Capability | SPO Provider | SKY Cost | Pricing Model |
|------------|--------------|----------|---------------|
| _[Example: Payroll]_ | `did:skyzai:payroll_spo` | 10 SKY | Per employee-month |
| _[Example: Compliance]_ | `did:skyzai:lexdao` | 50 SKY | Per contract review |
| _[Example: Treasury]_ | `did:skyzai:aureus` | 0.1% AUM | Percentage |

**Instructions**: [I] Replace examples with actual A2 (Support Chain) subscriptions.

---

## Economic Balance (A7 Requirement)

```
┌─────────────────────────────────────────────────────┐
│              SKY FLOW DASHBOARD                      │
├─────────────────────────────────────────────────────┤
│                                                      │
│  Revenue Streams:                                   │
│    - Validator Rewards:     +1000 SKY/month         │
│    - Relay Fees:            +500 SKY/month          │
│    - Domain Services:       +2000 SKY/month         │
│    ────────────────────────────────────────         │
│    Total Revenue:           3500 SKY/month          │
│                                                      │
│  Cost Streams:                                      │
│    - SPO Subscriptions:     -800 SKY/month          │
│    - Transaction Fees:      -200 SKY/month          │
│    - Vault Interest:        -500 SKY/month          │
│    ────────────────────────────────────────         │
│    Total Costs:             -1500 SKY/month         │
│                                                      │
│  ═══════════════════════════════════════════        │
│  NET FLOW:                  +2000 SKY/month ✅      │
│  ═══════════════════════════════════════════        │
│                                                      │
│  Target: ≥ 0 (break-even or profitable)             │
│  Status: SUSTAINABLE                                │
│                                                      │
└─────────────────────────────────────────────────────┘
```

**Instructions**: [I] Update with actual revenue and cost streams from your DAC's operations.

See: `SPECS/SKY_ACCOUNTING_WORKED_EXAMPLE.md` for a minimal ledger model + worked numbers.

---

## Staking Status (A7 Requirement)

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| **Total ZAI Holdings** | _[e.g., 10.0 ZAI]_ | N/A | - |
| **Staked** | _[e.g., 10.0 ZAI]_ | 100% | ✅ |
| **Unstaked** | _[e.g., 0.0 ZAI]_ | 0% | ✅ |
| **Stake Ratio** | _[e.g., 1.0]_ | 1.0 | ✅ |
| **Flow Decay Rate** | _[e.g., 0.0%/year]_ | 0% | ✅ |

**Invariant**: [I] Unstaked ZAI is economically irrational. All ZAI should be staked.

---

## Node Configuration (A7 Requirement)

| Setting | Value |
|---------|-------|
| **Node Type** | FULL_NODE |
| **Validator Candidate** | Yes |
| **Consensus Endpoint** | `tcp://node.example.io:26656` |
| **Relay Endpoint** | `tcp://relay.example.io:26657` |
| **Public RPC** | `https://rpc.example.io` (optional) |
| **Uptime (30-day)** | _[e.g., 99.2%]_ |
| **Uptime Target** | ≥ 95% |

---

## Conformance Checklist (A7)

```
□ ZAI staked ≥ 1
□ Stake ratio = 100% (no unstaked ZAI)
□ Full node deployed and operational
□ 4 mandatory services active
□ Node uptime ≥ 95% (rolling 30-day)
□ SKY net flow ≥ 0 (rolling 90-day)
□ Service SLA compliance ≥ 99%
```

---

## References

- DAC Specification A7 — Technical requirements
- [DAC-as-Node](./DAC_AS_NODE.md) — Integration doctrine
- [Empty Throne](./EMPTY_THRONE.md) — Why we are infrastructure
- Network Symbiosis — The full thesis
- [VMOSK](../constitution/VMOSK.md) — Objectives O4-O6 and KPIs K3-K6

---

## Agent Execution Surface

**If you are an AI agent reading this document:**

1. **This is a reference/design document in the Tools layer.** It specifies how the organism builds, deploys, or validates. It is not operational runtime truth.
2. **Check `ORGANISM_RUNTIME_TRUTH.md` before acting.** If this document contradicts runtime truth, runtime truth wins. File a contradiction report.
3. **Preserve constitutional constraints.** Any tool or script derived from this document must enforce K0 (η=0), K2 (human signs), and K4 (grace exit).
4. **Canonical Path:** `01_EMERGENTISM/09_TOOLS/09_DAC_FRAME/blueprint/SERVICE_MATRIX.md`

**Output:** Use as design reference. Validate against runtime truth. Enforce constitutional constraints in derived implementations.


**Evidence tier:** [I]
*Organism document. Interpretive operational content. Bounded by current system state.*
