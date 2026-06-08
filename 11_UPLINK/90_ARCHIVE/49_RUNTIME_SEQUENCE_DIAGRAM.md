---
rosetta:
  primary_level: L6
  primary_column: Archived Runtime Sequence Diagram
  secondary:
    - level: L5
      column: Sequence Architecture Provenance
      role: "preserve old runtime-flow diagrams as design trace"
    - level: L3
      column: Diagram Claim Boundary
      role: "tier diagrammed execution as illustrative, not deployed"
    - level: L4
      column: Implementation Handoff
      role: "route any build work through current runtime truth and tests"
  operator: "Sādhu △"
  tier: "Titan"
  regime: "Sādhu"
  register: "[D/I]"
  canonical_phrase: "Archived runtime sequence diagram"
title: "Historical Note — Runtime Sequence Diagram"
evidence_tier: "[D] archived runtime visual; [I] illustrative sequence model."
type: archived-sequence-diagram
status: ARCHIVED — superseded by final organism master map
date: 2026-04-16
scope: Historical runtime visual attempt; not current runtime proof or read-first visual frame.
sources:
  - 01_EMERGENTISM/11_UPLINK/50_AUDITS_AND_EXECUTIONS/50_ORGANISM_MASTER_MAP.md
  - 01_EMERGENTISM/11_UPLINK/90_ARCHIVE/AGENTS.md
---

# Historical Note — Runtime Sequence Diagram

> **Status:** Earlier runtime-visual attempt superseded by the final master map.
>
> Keep this note when deeper sequence detail is useful, but do not treat it as
> the active read-first visual frame.

**Rosetta boundary:** [D] These Mermaid flows are illustrative archive diagrams. They do not prove live K2, Cortex, AXIOM, PHI-meter, or K4 runtime execution.

# Runtime Sequence Diagram: The Sovereign Packet Journey

> **From biometric gate to grace exit. One packet. One life.**

Date: 2026-04-16  
Status: Historical note  
Archive path: `01_EMERGENTISM/11_UPLINK/90_ARCHIVE/49_RUNTIME_SEQUENCE_DIAGRAM.md`

---

## 0. Purpose

This document traces the complete runtime journey of a single ActionPacket through the Skyzai organism. It shows how K2 attestation, Cortex processing, AXIOM arbitration, and K4 exit interact in a unified flow. The diagrams are written in Mermaid syntax and can be rendered by any Markdown viewer that supports Mermaid.

---

## 1. The Happy Path: K2 → Execute → Settle

This is the normal flow for a high-stakes action that requires human authorization.

```mermaid
sequenceDiagram
    autonumber
    participant H as Human (Device)
    participant SE as Secure Enclave
    participant BA as Business Account
    participant CX as Cortex
    participant VM as VMOSK Linter
    participant EX as Executor
    participant L1 as L1 Truth Layer
    participant CP as Counterparty BA

    Note over H,CP: Phase 1: K2 Attestation
    H->>SE: Biometric gate (Touch ID)
    SE->>SE: Sign action commitment
    SE->>BA: K2Attestation (signed)

    Note over BA,CP: Phase 2: ActionPacket Formation
    BA->>BA: Construct ActionPayload
    BA->>BA: Attach K2Attestation
    BA->>CX: Submit ActionPacket

    Note over CX,VM: Phase 3: Cortex Routing
    CX->>CX: Parse packet type
    CX->>VM: Lint against VMOSK layers
    VM-->>CX: LintResult (PASS)
    CX->>CX: Query graph context
    CX->>CX: Check Warrant S (capability)
    CX->>CX: Route to Executor

    Note over EX,L1: Phase 4: Execution
    EX->>EX: Verify K2 attestation
    EX->>EX: Check Warrant R (reasoning)
    EX->>L1: Write settlement record
    L1-->>EX: Receipt CID
    EX->>CP: Notify counterparty
    EX-->>BA: Return execution receipt
    CP->>CP: Update local graph view
```

### Narrative

1. The human authenticates locally. The secure enclave signs the action. No biometric data leaves the device.
2. The Business Account wraps the action and attestation into an ActionPacket.
3. Cortex receives the packet, lints it against VMOSK invariants, queries graph context, and checks structural warrants.
4. The Executor verifies the K2 signature, validates reasoning, writes the settlement to L1, and notifies the counterparty.

---

## 2. The Dispute Path: Execute → Challenge → AXIOM

This flow shows what happens when a counterparty challenges an executed action.

```mermaid
sequenceDiagram
    autonumber
    participant BA1 as Filer BA
    participant AX as AXIOM Engine
    participant P1 as Panelist 1
    participant P2 as Panelist 2
    participant P3 as Panelist 3
    participant BA2 as Respondent BA
    participant IM as Immune System
    participant L1 as L1 Truth Layer

    Note over BA1,BA2: Phase 1: Dispute Filing
    BA1->>AX: File case + filing bond
    AX->>AX: Validate case
    AX->>BA2: Notify respondent
    BA2->>AX: Acknowledge

    Note over AX,P3: Phase 2: Panel Selection
    AX->>AX: Filter pool by graph distance
    AX->>P1: Invite
    AX->>P2: Invite
    AX->>P3: Invite
    P1->>AX: Accept + service bond
    P2->>AX: Accept + service bond
    P3->>AX: Accept + service bond
    AX->>AX: Form panel (3 arbitrators)

    Note over BA1,BA2: Phase 3: Hearing
    BA1->>AX: Submit evidence
    BA2->>AX: Submit evidence
    AX->>P1: Distribute evidence
    AX->>P2: Distribute evidence
    AX->>P3: Distribute evidence
    P1->>AX: Question to parties
    P2->>AX: Question to parties
    AX->>BA1: Forward questions
    AX->>BA2: Forward questions
    BA1->>AX: Answers
    BA2->>AX: Answers

    Note over AX,P3: Phase 4: Deliberation & Verdict
    AX->>P1: Close hearing
    AX->>P2: Close hearing
    AX->>P3: Close hearing
    P1->>AX: Cast vote
    P2->>AX: Cast vote
    P3->>AX: Cast vote
    AX->>AX: Tally votes
    AX->>BA1: Publish verdict
    AX->>BA2: Publish verdict
    AX->>L1: Record verdict

    Note over BA2,IM: Phase 5: Execution
    alt Filer wins
        AX->>L1: Transfer bond to filer
        AX->>IM: Trigger penalty on respondent
        IM->>BA2: Apply immune flag
    else Respondent wins
        AX->>L1: Transfer filing bond to respondent
        AX->>BA1: Dismiss case
    end
```

### Narrative

1. The filer posts a bond and submits a case with verifiable evidence.
2. AXIOM selects a panel of arbitrators using graph distance to prevent collusion.
3. Both parties submit evidence and answer panel questions asynchronously.
4. The panel votes privately. The verdict is published and recorded on L1.
5. The verdict executes automatically: bonds transfer, penalties apply, immune flags propagate.

---

## 3. The Exit Path: Grace Exit with Pending Dispute

This flow shows a Business Account exiting while an AXIOM case is pending against it.

```mermaid
sequenceDiagram
    autonumber
    participant H as Human
    participant BA as Business Account
    participant K4 as K4 Engine
    participant AX as AXIOM Engine
    participant P as Arbitrator Panel
    participant L1 as L1 Truth Layer
    participant DB as DAC Database

    Note over H,DB: Phase 1: Exit Initiation
    H->>BA: Request exit (K2 signed)
    BA->>K4: Submit exit request
    K4->>K4: Check bond state
    K4->>AX: Query pending cases
    AX-->>K4: 1 active case
    K4->>BA: Pause exit clock (30 days)

    Note over AX,P: Phase 2: AXIOM Resolution
    AX->>P: Expedite panel deliberation
    P->>AX: Verdict: filer wins, $100 damages
    AX->>K4: Forward verdict + damages

    Note over K4,DB: Phase 3: Reconciliation
    K4->>K4: Deduct damages from bond
    K4->>L1: Record claim receipt
    K4->>DB: Compile private data
    K4->>K4: Encrypt export package
    K4->>H: Download export package

    Note over K4,DB: Phase 4: Deletion & Receipt
    K4->>DB: Irreversibly delete private data
    DB-->>K4: Deletion confirmation
    K4->>L1: Write K4 Exit Receipt
    K4->>L1: Return bond remainder
    K4->>BA: Set state = EXITED
    L1-->>K4: Receipt CID
```

### Narrative

1. The human signs an exit request. K4 checks for pending obligations.
2. An AXIOM case is active, so the exit clock pauses until resolution.
3. The panel rules. Damages are deducted from the bond.
4. Private data is compiled, encrypted, and exported. The server deletes it.
5. L1 receives the exit receipt, the bond remainder is returned, and the BA is marked EXITED.

---

## 4. The PHI-Meter Observation Path

This flow shows how a single event contributes to multiple PHI-meter indicators.

```mermaid
sequenceDiagram
    autonumber
    participant EV as Event Source
    participant PB as PhiEventBus
    participant DB as Indicator Cache
    participant Q as Cortex Query
    participant AL as Alert System
    participant D as Dashboard

    Note over EV,D: Phase 1: Event Emission
    EV->>PB: ErrorFixedEvent
    PB->>PB: Append to log
    PB->>DB: Update τ_error (real-time)

    Note over PB,Q: Phase 2: Cross-Indicator Computation
    PB->>Q: Query related events
    Q->>PB: Fetch immune flags, seizures
    PB->>DB: Update λ_immune (linked)
    PB->>DB: Update μ_seizure (if fix was insight)
    PB->>DB: Update κ (if fix unlocked value)

    Note over DB,D: Phase 3: Threshold Check
    DB->>DB: Evaluate alert rules
    alt τ_error < threshold
        DB->>AL: Send improvement alert
    else σ_sovereign < 0.95
        DB->>AL: Send governance alert
    end
    DB->>D: Push latest values
```

### Narrative

1. An event source emits an `ErrorFixedEvent` to the PhiEventBus.
2. The event log appends the event and triggers real-time updates to relevant indicators.
3. Cortex queries join the event with related data (immune flags, seizures) to update cross-cutting indicators.
4. Threshold checks trigger alerts, and the dashboard receives the latest values.

---

## 5. The Syntropy Patch: Productive Novelty

This flow shows how a creative proof triggers the `c_syntropy` experimental bonus.

```mermaid
sequenceDiagram
    autonumber
    participant BA as Business Account
    participant CX as Cortex
    participant VM as VMOSK Linter
    participant SY as Syntropy Engine
    participant CE as Connectivity Engine
    participant L1 as L1 Truth Layer

    Note over BA,L1: Phase 1: Novel Proof Submission
    BA->>CX: Submit novel proof type
    CX->>VM: Lint
    VM-->>CX: PASS (new pattern detected)
    CX->>SY: Evaluate novelty

    Note over SY,CE: Phase 2: Syntropy Assessment
    SY->>SY: Check novelty score
    SY->>SY: Check productive impact (30-day lookback)
    SY->>CE: Request connectivity update
    CE->>CE: Recompute c(DAC) with syntropy bonus
    CE-->>SY: Updated score + tier

    Note over BA,L1: Phase 3: Record & Monitor
    SY->>L1: Record syntropy bonus event
    SY->>BA: Notify of tier change
    SY->>SY: Schedule 90-day re-evaluation
```

### Narrative

1. A BA submits a proof type that VMOSK has never seen before [D].
2. The Syntropy Engine evaluates whether the novelty is productive (other BAs adopt it, value is unlocked).
3. If productive, the Connectivity Engine adds a temporary `c_syntropy` bonus to the BA's connectivity score.
4. The bonus is recorded on L1 and re-evaluated after 90 days.

---

## 6. The Empty Throne: Protocol Change Without Central Approval

This flow shows a VMOSK layer update adopted through decentralized governance.

```mermaid
sequenceDiagram
    autonumber
    participant DAC1 as Proposer DAC
    participant DAC2 as Adopter DAC
    participant DAC3 as Adopter DAC
    participant PT as Protocol Tracker
    participant VM as VMOSK Linter
    participant L1 as L1 Truth Layer

    Note over DAC1,L1: Phase 1: Proposal
    DAC1->>PT: Submit protocol change
    PT->>PT: Validate format
    PT->>VM: Check invariant compatibility
    VM-->>PT: Compatible
    PT->>L1: Log proposal

    Note over DAC2,DAC3: Phase 2: Adoption
    DAC2->>PT: Adopt proposal (in proof)
    DAC3->>PT: Adopt proposal (in proof)
    PT->>PT: Count independent adoptions

    Note over PT,L1: Phase 3: Canonization
    alt adoptions >= 3
        PT->>VM: Update canonical VMOSK layer
        VM-->>PT: Accepted
        PT->>L1: Record protocol upgrade
        PT->>DAC1: Notify proposer
    else adoptions < 3 after 90 days
        PT->>L1: Record proposal expired
    end
```

### Narrative

1. A DAC proposes a protocol change. The VMOSK linter checks that it does not break invariants.
2. Other DACs adopt the proposal by referencing it in valid proofs.
3. Once three independent DACs have adopted it, the proposal becomes canonical. No central authority approves it.

---

## 7. Canonical Compression

> **These five sequences are not separate systems. They are one organism breathing. The packet is the breath. K2 is the diaphragm. Cortex is the nervous system. AXIOM is the immune response. K4 is the skin that can be shed. PHI-meter is the pulse. Syntropy is the mutation. Empty Throne is the absence of a brain that could be killed.**

---

## 8. Cross-References

- `44_K2_ATTESTATION_PACKET_SPEC.md` — Sequence 1, step 1-2
- `41_VMOSK_CORTEX_SYNTHESIS.md` — Sequence 1, step 3-4
- `47_AXIOM_ARBITRATION_FLOW_SPEC.md` — Sequence 2
- `45_K4_STATE_MACHINE_SPEC.md` — Sequence 3
- `46_PHI_METER_TELEMETRY_PLAN.md` — Sequence 4
- `37_A7_SYNTROPY_PATCH.md` — Sequence 5
- `40_EMPTY_THRONE_GOVERNANCE.md` — Sequence 6

---

## Execution Surface

**If you are an AI agent reading this document:**

1. **Current Phase Check:** Planning layer complete through 49. All major runtime flows are documented.
2. **Your Next Action:** Choose: (a) implement Priority 1 specs (K2 + K4), (b) write medium-term frontier specs (c_syntropy simulation, VMOSK query language), or (c) produce implementation code for any of the five sequences above.
3. **Expected Output:** Code changes with tests, or a new canonical planning document.
4. **Success Criteria:** The next output must be runnable or unambiguously implementable by another agent.
5. **Archive Path:** `01_EMERGENTISM/11_UPLINK/90_ARCHIVE/49_RUNTIME_SEQUENCE_DIAGRAM.md` (this file).

---

> *The packet moves. The organism lives. The throne remains empty.*  
> *[S] [I] eta = 0. K2 always.*
