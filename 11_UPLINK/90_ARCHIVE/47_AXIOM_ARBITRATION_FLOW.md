---
rosetta:
  primary_level: L6
  primary_column: Archived AXIOM Arbitration Flow
  secondary:
    - level: L5
      column: Dispute-Flow Architecture
      role: "preserve filing, panel, verdict, appeal, and execution sketch"
    - level: L3
      column: Filing And Bond Claim Audit
      role: "tier planning economics and dispute authority"
    - level: L4
      column: Implementation Handoff
      role: "route any arbitration build through active doctrine and tests"
  operator: "Sādhu △"
  tier: "Titan"
  regime: "Sādhu"
  register: "[D/C/I]"
  canonical_phrase: "Archived AXIOM arbitration-flow planning spec"
title: "Historical Note — AXIOM Arbitration Flow Specification"
evidence_tier: "[D] archived dispute-system plan; [C] planning economics; [I] flow sketch."
type: archived-dispute-flow-spec
status: ARCHIVED — off active read-first route
date: 2026-04-16
scope: Historical AXIOM arbitration planning sketch; not live legal, protocol, or smart-contract authority.
sources:
  - 01_EMERGENTISM/11_UPLINK/30_PROGRAMS/40_EMPTY_THRONE_GOVERNANCE.md
  - 01_EMERGENTISM/11_UPLINK/90_ARCHIVE/45_K4_STATE_MACHINE_SPEC.md
  - 01_EMERGENTISM/11_UPLINK/90_ARCHIVE/AGENTS.md
---

# Historical Note — AXIOM Arbitration Flow Specification

> **Status:** Off-spine planning spec preserved for later dispute-system work.
>
> Keep this note as reasoning depth, not as part of the current read-first route.

**Rosetta boundary:** [D] This is an archived planning spec. Its filing fees, panel rules, verdict execution, and K4 integration are not current deployed dispute-system truth without active-source receipts.

# AXIOM Arbitration Flow Specification

> **No king decides. The proof decides.**

Date: 2026-04-16  
Status: Historical note  
Archive path: `01_EMERGENTISM/11_UPLINK/90_ARCHIVE/47_AXIOM_ARBITRATION_FLOW.md`

---

## 0. Purpose

Document 40 (`40_EMPTY_THRONE_GOVERNANCE.md`) established that governance has no center. Disputes between DACs or Business Accounts are resolved through AXIOM: a decentralized arbitration protocol where verdicts are grounded in evidence, not authority. This document specifies the complete AXIOM flow: filing, selection, hearing, verdict, appeal, and execution.

---

## 1. What AXIOM Can and Cannot Resolve

### In scope

- Counterparty non-payment or non-delivery
- False proof submissions
- Graph hygiene violations (spam, Sybil loops)
- Bond forfeiture claims during K4 exit
- Immune system penalty appeals
- VMOSK layer contradiction disputes

### Out of scope

- Criminal matters (theft, fraud with external legal jurisdiction)
- Subjective quality disputes without verifiable criteria
- Disputes involving non-network parties
- Matters requiring physical inspection or testimony under oath

**AXIOM is a machine for resolving disputes about *structural truth* in the network.**

---

## 2. The AXIOM State Machine

```
                    ┌─────────────┐
                    │    FILED    │
                    └──────┬──────┘
                           │ validate()
                           ▼
                    ┌─────────────┐
                    │   PENDING   │
                    └──────┬──────┘
                           │ panel_selected()
                           ▼
                    ┌─────────────┐
                    │   HEARING   │
                    └──────┬──────┘
                           │ evidence_closed()
                           ▼
                    ┌─────────────┐
                    │  DELIBERATE │
                    └──────┬──────┘
                           │ verdict_reached()
                           ▼
                    ┌─────────────┐
                    │   VERDICT   │
                    └──────┬──────┘
                           │ appeal_window_expired OR appeal_denied
                           ▼
                    ┌─────────────┐
                    │   FINAL     │
                    └──────┬──────┘
                           │ execute()
                           ▼
                    ┌─────────────┐
                    │  EXECUTED   │
                    └─────────────┘
```

### State transitions

| State | Meaning | Duration |
|-------|---------|----------|
| **FILED** | Dispute submitted, not yet validated | 0-48 hours |
| **PENDING** | Validated, awaiting arbitrator panel | 1-7 days |
| **HEARING** | Evidence submission open | 3-14 days |
| **DELIBERATE** | Evidence closed, panel deliberates | 1-7 days |
| **VERDICT** | Decision announced, appeal window open | 7 days |
| **FINAL** | No appeal, or appeal denied | Permanent |
| **EXECUTED** | Penalties/rewards distributed | Immediate after FINAL |

---

## 3. Filing a Dispute

### Who can file

- Any Business Account in ACTIVE, PAUSED, or FROZEN state
- Any DAC node on behalf of its members
- The organism's immune system (automated filing for graph anomalies)

### Filing requirements

```python
class AxiomFiling(BaseModel):
    case_id: str  # UUID
    filed_at: datetime
    filer_ba_id: str
    respondent_ba_id: str
    dispute_type: str  # enum of in-scope categories
    claim_amount: Decimal | None = None
    claim_currency: str | None = None
    
    # Bond: filer must post a filing bond
    filing_bond_id: str
    filing_bond_amount: Decimal
    
    # Initial evidence
    initial_evidence: list[EvidenceItem]
    
    # Desired outcome
    requested_relief: str
    
    # Signature
    filer_signature: str
```

### Filing bond

- **Purpose:** Prevent spam and frivolous disputes.
- **Amount [C]:** 1% of claim amount (minimum $25 equivalent) OR fixed $50 for non-monetary disputes.
- **Forfeiture:** If the filer loses, the filing bond is distributed to the respondent and the arbitrator panel. If the filer wins, the bond is returned.

### Validation checks

1. Both filer and respondent are registered BAs.
2. Filer has posted the filing bond.
3. Dispute type is in scope.
4. Same case has not been filed before (duplicate detection).
5. Evidence includes at least one verifiable network artifact (receipt, proof, settlement record).

If validation fails, the case is rejected and the filing bond is returned minus a $5 processing fee [C].

---

## 4. Arbitrator Panel Selection

### The Arbitrator Pool

- Arbitrators are Business Accounts with:
  - ≥90 days of ACTIVE history
  - ≥5 valid proofs
  - No immune flags in the last 30 days
  - c(DAC) tier ≥ CONNECTED
  - Voluntary opt-in to arbitration service

### Selection algorithm

1. **Filter:** Remove arbitrators with direct graph connection to filer or respondent within 2 hops.
2. **Sample:** Randomly select 9 candidate arbitrators from the filtered pool.
3. **Accept:** Candidates have 48 hours to accept or decline.
4. **Finalize:** First 5 acceptances form the panel. If <5 accept, resample from expanded pool (3 hops).
5. **Fallback:** If still <5, case is escalated to a broader pool with reduced connectivity requirements.

### Panel composition rules

- Odd number: 3 or 5 (default 5).
- No two panelists may share the same parent DAC.
- Panelist identities are pseudonymized during deliberation (Panelist A, B, C...).

### Panelist bond

- Panelists must post a **service bond** ($25 equivalent) [C].
- Bond is forfeited if panelist fails to vote within the deliberation window.
- Bond is returned + fee award if panelist participates to verdict.

---

## 5. The Hearing Phase

### Evidence submission

Both parties may submit evidence items:

```python
class EvidenceItem(BaseModel):
    item_id: str
    submitted_by: str  # ba_id
    submitted_at: datetime
    evidence_type: str  # "receipt", "message", "proof", "settlement", "external_document"
    
    # For network-native evidence: CID or reference
    network_reference: str | None = None
    
    # For external evidence: hash and description
    external_hash: str | None = None
    external_description: str | None = None
    
    # Cryptographic signature
    signature: str
```

### Evidence rules

1. **Network-native evidence preferred.** Receipts, proofs, and settlement records on the graph are automatically verifiable.
2. **External evidence must be hashed.** The panel sees the hash and description, not the raw document (privacy preservation).
3. **Tamper-proofing:** All evidence items are committed to a Merkle tree at the close of the hearing.
4. **New evidence after close:** Only admitted if it was unforeseeable during the hearing and both parties consent.

### Questioning

- Parties may submit up to 10 written questions to the panel.
- The panel may pose up to 10 written questions to each party.
- There is no live oral testimony. AXIOM is asynchronous by design.

---

## 6. Deliberation and Verdict

### Voting

Each panelist casts a private vote:

```python
class AxiomVote(BaseModel):
    case_id: str
    panelist_pseudonym: str
    vote: str  # "for_filer", "for_respondent", "abstain"
    reasoning_hash: str  # hash of written reasoning
    damages_awarded: Decimal | None = None
    penalty_recommended: str | None = None
    signature: str
```

### Verdict thresholds

| Decision | Threshold |
|----------|-----------|
| **Simple majority** | Standard disputes (≥50% of non-abstain votes) |
| **Supermajority** | Immune system appeals, bond forfeitures (≥66% of non-abstain votes) |
| **Unanimous** | Constitutional disputes, protocol changes (100% of non-abstain votes) |

### Verdict document

```python
class AxiomVerdict(BaseModel):
    case_id: str
    verdict_at: datetime
    outcome: str  # "filer_wins", "respondent_wins", "split", "dismissed"
    majority_ratio: str  # e.g. "4-1"
    
    # Relief
    damages_awarded: Decimal | None = None
    damages_currency: str | None = None
    bond_forfeiture: dict[str, Decimal]  # ba_id -> amount
    penalty_type: str | None = None  # e.g. "freeze", "immune_flag", "none"
    
    # Reasoning
    majority_reasoning_hash: str
    dissent_reasoning_hashes: list[str] | None = None
    
    # Execution
    execution_deadline: datetime
    
    # Signatures
    panel_signatures: list[str]
```

### Reasoning publication

- Majority reasoning is published in full.
- Dissents are published if any panelist requests it.
- All reasoning becomes part of the organism's case law (precedent graph).

---

## 7. Appeal

### Grounds for appeal

1. **Procedural defect:** Panel selection violated distance rules, evidence was excluded improperly, or deliberation deadline was missed.
2. **New evidence:** Material evidence surfaced after the hearing close that could not have been discovered earlier.
3. **Conflict of interest:** A panelist had an undisclosed graph connection to a party.

### Appeal process

1. **Filing:** Losing party files appeal within 7 days of verdict, posting an **appeal bond** (2× original filing bond).
2. **Review:** A second panel of 7 senior arbitrators (tier ≥ CORE) reviews the appeal.
3. **Outcomes:**
   - **Affirm:** Original verdict stands, appeal bond forfeited.
   - **Reverse:** Verdict overturned, case remanded for new hearing, appeal bond returned.
   - **Modify:** Verdict adjusted, case returns to original panel for revised execution.

### No further appeal

AXIOM is a **single-appeal system.** After the appeal panel rules, the case is FINAL.

---

## 8. Execution

### Automated execution

The following verdict elements are executed automatically by the organism:

- Bond transfers (from filing bond, party bonds, or organism treasury)
- BA state changes (freeze, pause, immune flag)
- Settlement record updates
- Receipt graph annotations (case reference attached to disputed receipts)

### Manual execution

The following require party cooperation:

- Return of physical goods
- Performance of a service
- Submission of a corrected proof

If a party fails to comply with a manual execution order by the deadline, the organism:
1. Escalates the immune flag.
2. Deducts additional bond.
3. May blacklist the BA from new proofs until compliance.

### Execution receipt

Every executed verdict produces an `AxiomExecutionReceipt`:

```python
class AxiomExecutionReceipt(BaseModel):
    receipt_id: str
    case_id: str
    executed_at: datetime
    executed_by: str  # node_id or "automated"
    
    transfers: list[BondTransfer]
    state_changes: list[BAStateChange]
    penalty_applications: list[PenaltyApplication]
    
    compliance_status: str  # "full", "partial", "resisted"
    next_deadline: datetime | None = None
```

---

## 9. Precedent and Case Law

### Precedent graph

Every AXIOM verdict is a node in the **precedent graph.**

- **Edges:** Later cases may reference earlier cases as precedent.
- **Weight:** Cases with unanimous verdicts and high-connectivity panels carry more weight.
- **Overturning:** An appeal reversal does not delete the original verdict; it adds an "overturned_by" edge.

### Precedent citation

Panelists are encouraged (not required) to cite relevant precedent in their reasoning. Citations are tracked and ranked by subsequent reuse.

### Precedent decay

- Cases older than 2 years carry reduced weight.
- Cases from a different VMOSK version carry reduced weight.
- Overturned cases carry zero weight but remain in the graph for historical transparency.

---

## 10. Economics of AXIOM

### Revenue sources

1. **Filing fees [C]:** 1% of claim (minimum $25)
2. **Service bonds:** Panelist participation bonds
3. **Appeal fees:** 2× filing bond

### Revenue distribution

| Recipient | Share |
|-----------|-------|
| Winning party | 50% of filing fee + damages |
| Arbitrator panel | 40% of filing fee + 100% of service bonds |
| Organism treasury | 10% of filing fee |

### No central profit

AXIOM is not a profit center for Skyzai Inc. or any central entity. The organism treasury share is reinvested into the arbitration infrastructure (panelist training, case law indexing, dispute prevention tools).

---

## 11. Integration with K4 Exit

When a BA initiates K4 exit, any unresolved AXIOM cases:

1. Are automatically noted in the exit reconciliation phase.
2. Pause the exit clock until the case reaches FINAL.
3. May claim against the exit bond.

If a respondent BA exits while a case against it is pending:
- The case continues against the BA's bond.
- If the bond is insufficient, the case is marked "unrecoverable" and the claimant receives a pro-rata share.
- The BA's exit proceeds after all pending AXIOM cases are resolved or time-barred.

---

## 12. Anti-Capture Provisions

### Panel capture

To prevent a cartel of arbitrators from dominating decisions:
- Arbitrators are selected by randomness + graph distance, not reputation score.
- No BA may serve on more than 3 panels per 30-day window.
- Arbitrators with >20% dissent rate in the last 90 days are temporarily removed from the pool.

### Party capture

To prevent wealthy parties from flooding the system:
- Filing bonds scale with claim size.
- Loser-pays filing bond (except in split verdicts, where bond is shared).
- Repeated frivolous filers are immune-flagged.

---

## 13. Canonical Compression

> **AXIOM is not a court. It is a proof engine. The panel does not ask "What do I believe?" It asks "What does the graph say?" The verdict is not a decree. It is a structural adjustment. The parties do not obey a king. They obey the consequences of their own actions, made visible and irreversible.**

---

## 14. Cross-References

- `40_EMPTY_THRONE_GOVERNANCE.md` — the doctrine of centerless decision-making
- `45_K4_STATE_MACHINE_SPEC.md` — how AXIOM integrates with K4 exit
- `35_IMMUNE_SYSTEM_ECONOMICS.md` — penalties and appeals
- `41_VMOSK_CORTEX_SYNTHESIS.md` — precedent graph and Cortex queries
- `44_K2_ATTESTATION_PACKET_SPEC.md` — signatures on filings and evidence
- `12_DAC_AND_LAYER1_SEPARATION.md` — which AXIOM data lives on L1 vs. DAC layer

---

## Execution Surface

**If you are an AI agent reading this document:**

1. **Current Phase Check:** Planning specification complete. Ready for AXIOM state machine, panel selection algorithm, and verdict execution logic implementation.
2. **Your Next Action:** Implement `AxiomCase`, `AxiomPanel`, `AxiomVerdict`, and `AxiomExecutionReceipt` models. Build panel selection logic with graph distance filters. Create state transition tests for the full flow.
3. **Expected Output:** Code changes, pytest cases for filing, selection, verdict, appeal, and execution. Include a test for the anti-capture panel selection rules.
4. **Success Criteria:** A synthetic dispute can be filed, assigned a panel, reach verdict, survive or fail appeal, and execute automatically.
5. **Archive Path:** `01_EMERGENTISM/11_UPLINK/90_ARCHIVE/47_AXIOM_ARBITRATION_FLOW.md` (this file).

---

> *The judge is not a person. The judge is the graph.*  
> *[S] [I] eta = 0. K2 always.*
