---
rosetta:
  primary_level: L6
  primary_column: Archived K4 State Machine Spec
  secondary:
    - level: L5
      column: Implementation-Adjacent Architecture
      role: "preserve state, bond, receipt, and export schema sketches"
    - level: L3
      column: Bond And Exit Claim Audit
      role: "keep planning economics and mechanics tiered"
    - level: L4
      column: Implementation Handoff
      role: "route any build work through active doctrine and fresh tests"
  operator: "Sādhu △"
  tier: "Titan"
  regime: "Sādhu"
  register: "[D/C/I]"
  canonical_phrase: "Archived K4 state-machine planning spec"
title: "Archived Follow-On Spec — K4 Business Account State Machine Specification"
evidence_tier: "[D] archived implementation-adjacent spec; [C] planning economics; [I] schema sketch."
type: archived-implementation-spec
status: ARCHIVED — off active PHI/V doctrine spine
date: 2026-04-16
scope: "[D] Historical K4 Business Account state-machine, bond, export, and receipt planning sketch; not a deployed or audited implementation."
sources:
  - 01_EMERGENTISM/11_UPLINK/30_PROGRAMS/42_K4_BUSINESS_ACCOUNT_CONTINUITY.md
  - 01_EMERGENTISM/11_UPLINK/90_ARCHIVE/AGENTS.md
---

# Archived Follow-On Spec — K4 Business Account State Machine Specification

> **Status:** Useful implementation-adjacent follow-on to
> `42_K4_BUSINESS_ACCOUNT_CONTINUITY.md`, but intentionally removed from the
> active PHI/V doctrine spine during pruning.
>
> Use this only when the planning layer returns to K4 operational state-machine
> design.

**Rosetta boundary:** [D] This is an archived planning spec. Its bond schedule, state transitions, receipt schemas, and success criteria do not prove live K4 mechanics or audited smart-contract behavior.

# K4 Business Account State Machine Specification

> **Grace exit: the private data leaves with the user. The public truth remains for the network.**

Date: 2026-04-16  
Status: Archived follow-on spec  
Archive path: `01_EMERGENTISM/11_UPLINK/90_ARCHIVE/45_K4_STATE_MACHINE_SPEC.md`

---

## 0. Purpose

Document 42 (`42_K4_BUSINESS_ACCOUNT_CONTINUITY.md`) established the doctrine: a Business Account is sovereign, its private data is portable, and its exit must not erase counterparty truth. This document specifies the exact state machine, bond contract, exit receipt schema, and transition flows that implement that doctrine.

---

## 1. The K4 State Machine

A Business Account (BA) moves through exactly six states:

```
                    ┌─────────────┐
                    │   DORMANT   │
                    └──────┬──────┘
                           │ activate()
                           ▼
                    ┌─────────────┐
     ┌──────────────│    ACTIVE   │──────────────┐
     │              └──────┬──────┘              │
     │ freeze()            │              pause()
     ▼                     │                     ▼
┌─────────┐         reconcile()           ┌─────────┐
│ FROZEN  │◄──────────────────────────────│ PAUSED  │
└────┬────┘                               └────┬────┘
     │                                         │
     │ exit()                            resume()
     │ (after bond)                            │
     ▼                                         │
┌─────────┐                                    │
│  EXITED │                                    │
└─────────┘                                    │
     │                                          │
     │ reactivate()                             │
     │ (new account, old receipts link)         │
     └──────────────────────────────────────────┘
```

### State definitions

| State | Meaning | Data access | Graph visibility |
|-------|---------|-------------|------------------|
| **DORMANT** | Account created but no proofs yet | Owner only | Invisible |
| **ACTIVE** | Normal operation | Full | Full |
| **PAUSED** | Temporary halt (self-initiated or soft dispute) | Read-only | Historical visible, new actions blocked |
| **FROZEN** | Hard dispute or immune flag | Read-only | Visible, but marked frozen |
| **EXITED** | Grace exit completed | Private data exported and server-deleted | Public receipts and graph topology remain |

### Transitions

| Transition | Trigger | Precondition | Postcondition |
|------------|---------|--------------|---------------|
| `activate()` | First proof submitted | Bond posted, KYC verified | BA becomes ACTIVE |
| `pause()` | Owner request or soft dispute | None | BA becomes PAUSED, no new actions |
| `resume()` | Owner request or dispute resolved | PAUSED, no active immune blocks | BA returns ACTIVE |
| `freeze()` | Hard dispute, immune flag, or AXIOM arbitration | Evidence threshold met | BA becomes FROZEN |
| `exit()` | Owner initiates grace exit | FROZEN or ACTIVE, bond conditions met | BA becomes EXITED |
| `reactivate()` | Former owner creates new BA | Exit receipt exists | New BA linked to old receipts |

---

## 2. The Bond Contract

A Business Account must post a **minimum bond** to activate. The bond serves two purposes:

1. **Skin in the game:** The entity has committed capital to the graph.
2. **Exit collateral:** If the entity exits with unresolved obligations, the bond can be distributed to claimants.

### Bond parameters

```python
class K4Bond(BaseModel):
    bond_id: str  # UUID
    ba_id: str    # Business Account ID
    amount: Decimal
    currency: str  # e.g. "USDC", "ETH", "BTC"
    posted_at: datetime
    release_conditions: list[str]  # e.g. ["no_active_disputes", "no_pending_settlements"]
    forfeiture_address: str | None = None  # Where forfeited bond goes (default: organism treasury)
```

### Minimum bond schedule

| Tier | Minimum Bond | Basis |
|------|-------------|-------|
| Dormant → Active | $50 equivalent | Fixed floor for spam prevention |
| First 90 days | $50 equivalent | New entity probation |
| After 90 days + 3 proofs | $100 equivalent | Escalation with graph history |
| After 1 year + 10 proofs | $200 equivalent | Established entity |
| After immune flag | 2× previous bond | Penalty for bad graph hygiene |

The bond is **not** a fee. It is returned to the owner on successful exit, minus any valid claims from counterparties.

### Bond states

| Bond State | Meaning |
|------------|---------|
| `POSTED` | Bond locked in smart contract / escrow |
| `RELEASED` | All conditions met, bond returned |
| `FORFEITED_PARTIAL` | Some bond distributed to claimants |
| `FORFEITED_FULL` | Entire bond distributed |

---

## 3. Exit Flow: The Grace Exit Protocol

### Phase 1: Initiation

1. Owner sends `exit_request` signed with BA nsec.
2. System checks bond state and outstanding obligations.
3. If obligations exist, system notifies counterparties and opens a 30-day **claim window**.

### Phase 2: Reconciliation (0-30 days)

- Counterparties may file claims with evidence.
- AXIOM arbitration may be invoked for disputed claims.
- Valid claims are deducted from the bond.
- If bond is insufficient, claims are pro-rated.

### Phase 3: Export (after claim window closes)

1. System generates **K4 Export Package** (private data only).
2. Package is encrypted to the owner's public key.
3. Owner downloads the package.
4. System **irreversibly deletes** private data from all Skyzai databases.

### Phase 4: Receipt (after deletion)

1. System issues **K4 Exit Receipt**.
2. BA state transitions to **EXITED**.
3. Bond remainder is returned to the owner's designated address.

---

## 4. The K4 Export Package Schema

The export package contains **only private data**. It must be portable and self-describing.

```python
class K4ExportPackage(BaseModel):
    export_id: str
    ba_id: str
    generated_at: datetime
    format_version: str = "K4-2026-1"

    # Encrypted payload
    encrypted_payload: bytes

    # Schema manifest (unencrypted, so the owner knows what they got)
    manifest: K4ExportManifest

    # Signature from the exporting node
    node_signature: str

class K4ExportManifest(BaseModel):
    ba_id: str
    ba_creation_date: datetime
    included_entities: list[str]  # e.g. ["Person", "Business", "Asset"]
    included_proofs: list[str]    # Proof IDs
    included_messages: list[str]  # Message IDs
    included_files: list[str]     # File references
    receipt_count: int
    topology_snapshot: str  # CID of the public topology snapshot
    bond_final_state: str
    deletion_confirmation_hash: str
```

### What IS in the encrypted payload

- All entity fields marked `privacy: private`
- All direct messages
- All uploaded files
- All proof payloads
- The nsec (encrypted to the owner's recovery key)
- Export metadata

### What is NOT in the encrypted payload

- Public receipts
- Settlement records
- Graph topology
- Counterparty proofs
- Any data owned by another BA

---

## 5. The K4 Exit Receipt Schema

The exit receipt is a public, immutable record that the BA exited cleanly. It lives in the organism's L1 truth layer.

```python
class K4ExitReceipt(BaseModel):
    receipt_id: str
    ba_id: str
    exited_at: datetime

    # Cryptographic proof of deletion
    deletion_confirmation_hash: str

    # Topology continuity
    successor_ba_id: str | None = None
    predecessor_ba_id: str | None = None

    # Bond disposition
    bond_id: str
    bond_initial_amount: Decimal
    bond_distributed: Decimal
    bond_returned: Decimal
    bond_currency: str

    # Claim summary
    total_claims: int
    claims_satisfied: int
    claims_pro_rated: bool

    # Public graph checkpoint
    public_receipt_count: int
    public_settlement_count: int
    topology_snapshot_cid: str

    # Signatures
    signed_by_node: str
    signed_by_ba_owner: str | None = None  # Optional owner co-signature
```

### Why the receipt matters

- **For the network [D]:** Proves the BA did not just vanish. There is a documented, verifiable exit.
- **For counterparties [D]:** Preserves the public settlement graph. Counterparties can still prove they traded with this BA.
- **For the owner [D]:** Proves they exercised their sovereignty right and received their data.
- **For auditors [D]:** Verifies that the system honors its own constitutional promises.

---

## 6. Counterparty Truth Preservation

When a BA exits, the following **must remain immutable**:

| Data | Owner | After exit |
|------|-------|------------|
| Private entity fields | BA owner | Exported and deleted |
| Private messages | BA owner | Exported and deleted |
| Private files | BA owner | Exported and deleted |
| Proof receipts (public) | Network | Retained |
| Settlement records | Network | Retained |
| Graph topology (who connected to whom) | Network | Retained |
| Counterparty proofs | Counterparty | Retained |
| AXIOM arbitration outcomes | Network | Retained |

**The principle:** The BA owns its *private data*. The *network* owns the consequences of its interactions.

---

## 7. The Topology Snapshot

At the moment of exit, the system captures a **public topology snapshot** of the BA's graph edges. This snapshot is:

- Anonymized (other BA IDs are hashed or pseudonymized)
- Structural only (degrees, connection types, timestamps)
- Stored in a content-addressed store (IPFS / similar)
- Referenced by CID in the exit receipt

```python
class TopologySnapshot(BaseModel):
    snapshot_id: str
    ba_id: str
    captured_at: datetime
    active_connections: int
    historical_connections: int
    proof_count: int
    settlement_count: int
    average_settlement_amount: Decimal | None = None
    immune_flags_received: int
    immune_flags_issued: int
    tier_at_exit: str  # Isolated, Peripheral, Connected, Core, Hub
```

This snapshot allows the network to preserve the BA's structural contribution without preserving its private identity.

---

## 8. Reactivation and Lineage

A former owner may create a new Business Account. The new BA is **not** the old BA. But the exit receipt can be referenced to establish **lineage**.

```python
class BALineage(BaseModel):
    new_ba_id: str
    old_receipt_id: str
    linked_at: datetime
    linkage_proof: str  # Signature over (new_ba_id + old_receipt_id)
```

### Lineage rules

1. **No automatic reputation transfer.** The new BA starts with the minimum bond.
2. **No automatic tier transfer.** Connectivity is recomputed from scratch.
3. **Historical receipts remain linked to the old BA.** They do not migrate.
4. **Counterparties may choose to reconnect.** But they are not forced to.
5. **Lineage is visible.** The new BA's profile may display "Lineage: exited BA X." This is optional and user-controlled.

---

## 9. Bond Forfeiture and Distribution

If a BA exits with valid counterparty claims, the bond is distributed before the remainder is returned.

### Claim priority

1. **Arbitration awards** (AXIOM judgments)
2. **Unpaid settlements** (verified on-chain or in receipt graph)
3. **Network penalties** (immune system fines)
4. **Organism treasury** (if no claimants, remainder returns to owner)

### Pro-rata distribution

If total claims exceed the bond:

```python
for claim in claims:
    claim.awarded = bond_remaining * (claim.amount / total_claim_amount)
```

All claimants receive a **K4 Claim Receipt** documenting their award.

```python
class K4ClaimReceipt(BaseModel):
    claim_id: str
    ba_id: str
    claimant_ba_id: str
    claimed_amount: Decimal
    awarded_amount: Decimal
    pro_rated: bool
    settled_at: datetime
    exit_receipt_id: str
```

---

## 10. Implementation Boundaries

### L1 (organism layer) responsibilities
- Store exit receipts immutably
- Store claim receipts immutably
- Maintain topology snapshots
- Enforce bond contract logic

### DAC layer responsibilities
- Initiate exit flow
- Generate export package
- Delete private data
- Verify owner signatures
- Coordinate with counterparties

### What L1 does NOT do
- Read private data
- Initiate exits
- Distribute export packages
- Verify biometric gates

---

## 11. Failure Modes

| Failure | System Response | Owner Recourse |
|---------|----------------|----------------|
| Owner loses nsec before exit | Social recovery or key-shard recovery | Initiate recovery protocol |
| Counterparty files false claim | AXIOM arbitration | Defend with evidence |
| System fails to delete private data | Immune flag on the node | Escalate to AXIOM, file for damages |
| Bond contract bug | Emergency pause on K4 exits | Wait for fix + audit |
| Owner dies | Pre-configured successor inherits nsec | Successor protocol (estate planning) |

---

## 12. Canonical Compression

> **[D] K4 is a reversible door. The user can leave with everything that is theirs. But the room remembers that they were here, because the other guests need to know who they shook hands with. The bond is the doorknob: it ensures the door is not kicked in, and it can pay for broken dishes if any remain.**

---

## 13. Cross-References

- `42_K4_BUSINESS_ACCOUNT_CONTINUITY.md` — the doctrine
- `35_IMMUNE_SYSTEM_ECONOMICS.md` — bond forfeiture and penalty design
- `40_EMPTY_THRONE_GOVERNANCE.md` — AXIOM arbitration without central court
- `44_K2_ATTESTATION_PACKET_SPEC.md` — the nsec that signs exit requests
- `12_DAC_AND_LAYER1_SEPARATION.md` — which responsibilities live where
- `41_VMOSK_CORTEX_SYNTHESIS.md` — how Cortex tracks K4 state transitions

---

## Execution Surface

**If you are an AI agent reading this document:**

1. **Current Phase Check:** Planning specification complete. Ready for state machine implementation and schema migration.
2. **Your Next Action:** Add `K4State`, `K4Bond`, `K4ExportPackage`, `K4ExitReceipt`, and `K4ClaimReceipt` models to the backbone schema layer. Implement state transition validation in `backbone/services/k4_state_machine.py`.
3. **Expected Output:** Code changes, pytest cases for all six state transitions, and bond distribution logic tests.
4. **Success Criteria:** A Business Account can be created, activated, paused, frozen, exited, and reactivated in tests; exit produces a valid receipt; private data deletion is simulated.
5. **Archive Path:** `01_EMERGENTISM/11_UPLINK/90_ARCHIVE/45_K4_STATE_MACHINE_SPEC.md` (this file).

---

> *Export, not amnesia. Continuity, not capture. The door opens both ways.*  
> *[S] [I] eta = 0. K2 always.*
