---
rosetta:
  primary_level: L5
  primary_column: K4 Bond Smart Contract Specification
  secondary:
    - level: L4
      column: Contract Implementation Handoff
      role: "route pseudocode into invariants, interface, and test obligations"
    - level: L3
      column: Security Model Audit
      role: "separate proposed defenses from reviewed contract behavior"
    - level: L6
      column: Central-Operator Extraction Boundary
      role: "destroy owner-rug and unilateral-withdrawal paths at the spec layer"
  operator: "Brahmā ○"
  tier: "Executive"
  regime: "Brāhmaṇa"
  register: "[I/D/B]"
  canonical_phrase: "K4 Bond Smart Contract Specification"
title: "K4 Bond Smart Contract Specification"
status: "PLANNING SPECIFICATION"
evidence_tier: "[I] operational mapping; [D] implementation specification; [B] only after code, tests, and audit receipts."
---

# K4 Bond Smart Contract Specification

**Evidence tier:** [I]  
*Operational specification. Interpretive mapping of structural sources into implementable contracts.*

**Rosetta boundary:** [I/D] This document specifies a candidate K4 bond escrow design. It does not [B] prove deployed contract safety, legal enforceability, audited code, or live DAC adoption without implementation receipts.


> **The bond is not a fee. It is skin in the graph.**

Date: 2026-04-16  
Status: Planning Specification  
Canonical path: `30_PROGRAMS/52_K4_BOND_SMART_CONTRACT_SPEC.md`

---

## 0. Purpose

[D] This document specifies the on-chain smart contract (or equivalent immutable Algorithmic TRO program) that underpins the K4 Business Account bond system. While the K4 state machine (`45_K4_STATE_MACHINE_SPEC.md`) defines the logic and transitions, the bond contract is the L1 truth layer intended to guarantee:

1. **Bonds are locked** and cannot be unilaterally withdrawn by Skyzai Inc. or any central operator.
2. **Claims are paid** according to cryptographically verifiable evidence.
3. **Exit is possible** once obligations are satisfied or time-barred.
4. **Counterparty truth** persists even when private data is deleted.

The contract is designed to be **jurisdiction-agnostic** and **platform-agnostic**. Pseudocode is presented in Solidity-like syntax for clarity, but the logic is transferable to any smart contract platform with programmable state and event emission.

---

## 1. Contract Overview

### 1.1 What the contract knows

- The mapping from `ba_id` to `Bond`
- The mapping from `ba_id` to a list of `Claim`
- The mapping from `ba_id` to `ExitRequest`
- The set of authorized AXIOM arbitrator contract addresses
- The set of authorized organism node addresses (for filing claims and initiating exits)

### 1.2 What the contract does NOT know

- Private entity data
- Biometric data
- Message contents
- The K2 private key (nsec)
- Off-chain reputation scores

### 1.3 Actors

| Actor | Role | Authority |
|-------|------|-----------|
| **BA Owner** | Posts bond, initiates exit, designates recovery address | Can post, request exit, update recovery address |
| **Organism Node** | Files claims, reports AXIOM verdicts, confirms deletions | Authorized by DAC governance |
| **AXIOM Contract** | Submits finalized verdicts and award amounts | Authorized by protocol vote |
| **Claimant** | Receives bond distribution if claim is validated | Passive recipient |

---

## 2. Data Structures

```solidity
struct Bond {
    bytes32 baId;
    address owner;
    uint256 amount;
    address token;           // ERC-20 token address or native token sentinel
    uint256 postedAt;
    bool released;
    bytes32 exitReceiptId;   // Set on successful exit
}

enum ClaimStatus {
    PENDING,
    VALIDATED,
    DENIED,
    PAID
}

struct Claim {
    bytes32 claimId;
    bytes32 baId;
    address claimant;
    uint256 amount;
    ClaimStatus status;
    bytes32 axiomCaseId;     // Reference to AXIOM verdict (optional for automated claims)
    uint256 filedAt;
}

enum ExitStatus {
    NONE,
    REQUESTED,
    CLAIM_WINDOW_OPEN,
    RECONCILING,
    COMPLETED,
    CANCELLED
}

struct ExitRequest {
    bytes32 baId;
    ExitStatus status;
    uint256 requestedAt;
    uint256 claimWindowEnds;
    bytes32 deletionConfirmationHash;
}
```

---

## 3. Core Functions

### 3.1 `postBond(bytes32 baId)`

**Caller:** BA Owner  
**Preconditions:**
- `msg.value >= minimumBond` (or ERC-20 allowance/transfer)
- No active bond exists for `baId` OR existing bond is in `RELEASED` state

**Effects:**
- Lock `msg.value` (or transferred tokens) in contract
- Create `Bond` record
- Emit `BondPosted(baId, owner, amount, token)`

### 3.2 `fileClaim(bytes32 baId, bytes32 claimId, address claimant, uint256 amount, bytes32 axiomCaseId)`

**Caller:** Organism Node (authorized)  
**Preconditions:**
- Bond exists for `baId`
- `amount > 0`
- If `axiomCaseId` is provided, it must reference a finalized AXIOM case

**Effects:**
- Create `Claim` record with status `PENDING`
- Emit `ClaimFiled(baId, claimId, claimant, amount)`

### 3.3 `validateClaim(bytes32 baId, bytes32 claimId)`

**Caller:** AXIOM Contract (authorized) OR Organism Node (for settlement-backed claims)  
**Preconditions:**
- Claim exists and is `PENDING`
- [D] AXIOM verdict awards the claim (if using AXIOM) OR settlement receipt proves the debt

**Effects:**
- Set claim status to `VALIDATED`
- Emit `ClaimValidated(baId, claimId)`

### 3.4 `initiateExit(bytes32 baId, bytes32 deletionConfirmationHash)`

**Caller:** Organism Node (on behalf of BA Owner after K2-signed request)  
**Preconditions:**
- Bond exists and is not released
- `ExitStatus` is `NONE` or `CANCELLED`
- BA state is ACTIVE or FROZEN (off-chain check; contract trusts authorized node)

**Effects:**
- Create `ExitRequest` with status `CLAIM_WINDOW_OPEN`
- Set `claimWindowEnds = block.timestamp + 30 days`
- Emit `ExitInitiated(baId, claimWindowEnds)`

### 3.5 `finalizeExit(bytes32 baId)`

**Caller:** Organism Node (authorized)  
**Preconditions:**
- Exit request exists and status is `CLAIM_WINDOW_OPEN`
- `block.timestamp >= claimWindowEnds`
- All `PENDING` claims older than the exit request have been resolved (VALIDATED or DENIED)

**Effects:**
1. Sum all `VALIDATED` claims for this `baId`
2. If total validated claims <= bond amount:
   - Pay each claimant their full claim amount
   - Return remainder to `bond.owner`
3. If total validated claims > bond amount:
   - Pro-rata: each claimant receives `claim.amount * bond.amount / totalValidatedClaims`
   - Owner receives `0`
4. Mark all paid claims as `PAID`
5. Mark bond as `RELEASED`
6. Set exit status to `COMPLETED`
7. Emit `ExitFinalized(baId, exitReceiptId, distributed, returned)`

### 3.6 `cancelExit(bytes32 baId)`

**Caller:** BA Owner  
**Preconditions:**
- Exit request exists and status is `CLAIM_WINDOW_OPEN`
- No validated claims exist (optional: allow cancellation with validated claims if owner posts additional bond)

**Effects:**
- Set exit status to `CANCELLED`
- Emit `ExitCancelled(baId)`

---

## 4. Pro-Rata Distribution

When validated claims exceed the bond, the contract must distribute fairly without rounding errors that disadvantage small claimants.

### Pseudocode

```solidity
function distributeProRata(bytes32 baId) internal {
    Bond storage bond = bonds[baId];
    Claim[] storage claims = claimsByBa[baId];
    uint256 totalValidated = 0;

    for (uint i = 0; i < claims.length; i++) {
        if (claims[i].status == ClaimStatus.VALIDATED) {
            totalValidated += claims[i].amount;
        }
    }

    uint256 remaining = bond.amount;
    for (uint i = 0; i < claims.length; i++) {
        if (claims[i].status != ClaimStatus.VALIDATED) continue;

        uint256 award = (claims[i].amount * bond.amount) / totalValidated;
        if (award > remaining) award = remaining;

        transfer(claims[i].claimant, award);
        claims[i].status = ClaimStatus.PAID;
        remaining -= award;
    }

    if (remaining > 0) {
        transfer(bond.owner, remaining);
    }
}
```

### Anti-gaming rule
- Claims filed **after** exit initiation but **before** `claimWindowEnds` are valid IF they reference pre-existing disputes or settlements filed before the exit request.
- Claims filed **after** `claimWindowEnds` are rejected.

---

## 5. AXIOM Integration

The bond contract does not run AXIOM logic. It accepts **verdict receipts** from the authorized AXIOM contract address.

### AXIOM → Bond Contract Interface

```solidity
function submitAxiomVerdict(
    bytes32 baId,
    bytes32 caseId,
    bytes32[] calldata validatedClaimIds,
    uint256[] calldata awardAmounts
) external onlyAxiomContract
```

**Effects:**
- For each validated claim ID, create or update the corresponding `Claim` record to `VALIDATED` with the AXIOM-determined `awardAmount`
- Emit `AxiomVerdictApplied(baId, caseId)`

### Design rationale
- AXIOM handles evidence, deliberation, and vote tallying off-chain or in a separate contract.
- The bond contract only handles the **execution** of finalized AXIOM verdicts.
- This separation preserves the DAC/L1 boundary: AXIOM lives in the DAC layer; bond execution lives on L1.

---

## 6. K4 Exit Flow on Chain

```
Owner requests exit (off-chain, K2-signed)
    ↓
Organism Node calls initiateExit()
    ↓
30-day claim window opens
    ↓
Claimants file claims (via Node)
    ↓
AXIOM resolves disputes (if any)
    ↓
Node calls finalizeExit()
    ↓
Contract distributes bond
    ↓
Owner receives export package (off-chain)
    ↓
Node deletes private data (off-chain)
    ↓
Node issues K4 Exit Receipt (off-chain / L1 receipt hash)
```

### On-chain exit receipt

While the full `K4ExitReceipt` schema lives in the DAC layer, the bond contract emits a minimal L1 receipt:

```solidity
event ExitFinalized(
    bytes32 indexed baId,
    bytes32 exitReceiptId,
    uint256 bondInitialAmount,
    uint256 bondDistributed,
    uint256 bondReturned,
    uint256 totalClaims,
    uint256 claimsSatisfied,
    bool claimsProRated,
    bytes32 topologySnapshotCid
);
```

This event is sufficient for auditors and counterparties to verify that:
- The exit was clean and bond-backed
- Claims were paid fairly
- The owner received any remainder

---

## 7. Security Model

### 7.1 Threat: Contract owner rug-pull

**Defense:** The contract has **no owner with unilateral withdrawal rights**. Once a bond is posted, the only ways it can move are:
1. Successful exit (to claimants and owner)
2. AXIOM verdict execution (to claimants)
3. Time-barred exit (to owner after window closes with no validated claims)

### 7.2 Threat: Organism node files false claims

**Defense:** Claims must be validated by AXIOM or by settlement receipts. The node cannot validate its own claims. For automated settlement claims, a second authorized node must co-sign.

### 7.3 Threat: Front-running exit to avoid claims

**Defense:** The 30-day claim window is immutable. The owner cannot withdraw during this window. Claims filed before the window closes are processed even if the owner tries to cancel.

### 7.4 Threat: Dust claims spam

[D] **Defense:** Minimum claim threshold (for example a low stablecoin-equivalent dust floor). Frivolous filers can be slashed by AXIOM immune penalties.

### 7.5 Threat: Rounding errors in pro-rata distribution

**Defense:** Use checked arithmetic. Process claims in deterministic order (e.g. by claim ID). Any rounding dust remains in the contract and is swept to the organism treasury, not retained by any single party.

---

## 8. Multi-Token Support

The contract should support both:
- **Native token** (ETH, SOL, etc.) using `msg.value`
- **ERC-20 / SPL / equivalent** using `transferFrom`

For simplicity, v1 can support a single whitelisted stablecoin (e.g. USDC). Multi-token support can be added in v2 via a `token` address field and per-token minimum bond mapping.

---

## 9. Upgrade Path

The bond contract should be **proxy-upgradeable** or **migration-based** to allow:
- Bug fixes
- New claim types
- Updated AXIOM contract addresses
- Parameter changes (minimum bond, claim window duration)

**Governance of upgrades:** Any proxy upgrade must be ratified by the Empty Throne governance process (`40_EMPTY_THRONE_GOVERNANCE.md`): protocol vote + ≥3 independent DAC adoptions + 14-day timelock.

---

## 10. Canonical Interface (Solidity-style)

```solidity
interface IK4BondEscrow {
    // Events
    event BondPosted(bytes32 indexed baId, address owner, uint256 amount, address token);
    event ClaimFiled(bytes32 indexed baId, bytes32 claimId, address claimant, uint256 amount);
    event ClaimValidated(bytes32 indexed baId, bytes32 claimId);
    event ExitInitiated(bytes32 indexed baId, uint256 claimWindowEnds);
    event ExitFinalized(bytes32 indexed baId, bytes32 exitReceiptId, uint256 distributed, uint256 returned);
    event ExitCancelled(bytes32 indexed baId);
    event AxiomVerdictApplied(bytes32 indexed baId, bytes32 caseId);

    // Core
    function postBond(bytes32 baId) external payable;
    function fileClaim(bytes32 baId, bytes32 claimId, address claimant, uint256 amount, bytes32 axiomCaseId) external;
    function validateClaim(bytes32 baId, bytes32 claimId) external;
    function initiateExit(bytes32 baId, bytes32 deletionConfirmationHash) external;
    function finalizeExit(bytes32 baId) external;
    function cancelExit(bytes32 baId) external;

    // AXIOM integration
    function submitAxiomVerdict(bytes32 baId, bytes32 caseId, bytes32[] calldata claimIds, uint256[] calldata amounts) external;

    // Views
    function getBond(bytes32 baId) external view returns (Bond memory);
    function getClaims(bytes32 baId) external view returns (Claim[] memory);
    function getExitRequest(bytes32 baId) external view returns (ExitRequest memory);
}
```

---

## 11. Cross-References

- `42_K4_BUSINESS_ACCOUNT_CONTINUITY.md` — the doctrine this contract enforces
- `45_K4_STATE_MACHINE_SPEC.md` — the state machine that calls this contract
- `47_AXIOM_ARBITRATION_FLOW_SPEC.md` — the dispute resolution system that validates claims
- `12_DAC_AND_LAYER1_SEPARATION.md` — why AXIOM lives in DAC and bond execution lives on L1
- `40_EMPTY_THRONE_GOVERNANCE.md` — how contract upgrades are authorized

---

## Execution Surface

**If you are an AI agent reading this document:**

1. **Current Phase Check:** Planning specification complete. Ready for implementation handoff only if build mode is explicitly reopened.
2. **Your Next Action:** Produce or review a contract handoff packet for `K4BondEscrow`, including invariants, interface boundaries, and test obligations.
3. **Expected Output:** Handoff-ready invariants list, interface sketch, and test outline.
4. **Success Criteria:** A third-party auditor can verify that the contract enforces all invariants in Section 7 without trusting any central party.
5. **Canonical Path:** `30_PROGRAMS/52_K4_BOND_SMART_CONTRACT_SPEC.md` (this file).

---

> [I] *The bond is the doorknob. It is intended to keep the door from being kicked in, and it pays for broken dishes if any remain.*
> [I] *eta = 0. K2 remains the irreversible-action boundary.*
