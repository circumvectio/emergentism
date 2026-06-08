---
rosetta:
  primary_level: L4
  primary_column: "Philosophy"
  operator: "Arjuna ⚔"
  tier: "God"
  regime: "Kṣatriya"
  register: "[I/S]"
  canonical_phrase: "Constitutional economics as rights/duties dyad"
---

**Project VMOSK-A:** `../VMOSK_A.md`

# 150a — Constitutional Economics Sheet (CANON-faithful)

**Evidence tier:** `[B]` where monetary claims cite canonical source packets; `[I]` where integration is charioteer synthesis; `[C]` where draft choices await sovereign K2 ratification.
**Date:** 2026-04-24
**Lane:** `04_AXIOLOGY` active draft sheet; promoted from Charioteer staging, still bounded by K2 ratification.
**Status:** Draft sheet based on charioteer-recommended OQ resolutions; not external legal, economic, or protocol canon until sovereign K2 ratifies each OQ.
**Assumed recommendations for this draft:** OQ-A2 · OQ-B1 · OQ-C3 · OQ-D1-refined · OQ-E1 · OQ-F1 · OQ-G3 · OQ-H2 · OQ-I1 · OQ-J1 · OQ-K2
**Prerequisite packets:** 146 audit · 147 layer discipline · 148 formula repair · 149 risk matrix · 150 integrated blueprint
**Depends on:** [Objective Morals and Ethics](02_VALUE_THEORY/00_OBJECTIVE_MORALS_AND_ETHICS.md), [Rights, Duties, and Due Process](02_VALUE_THEORY/01_RIGHTS_DUTIES_AND_DUE_PROCESS.md), [K2 Decision Protocol](01_THEURGY/01_K2_DECISION_PROTOCOL.md), **[VMOSK-A](../VMOSK_A.md)**

---

## 0. Axiomatic guard

This sheet defines the economic grammar. It is not the economy. The economy is what emerges when real humans and agents transact under these rules. If the rules become friction rather than leverage, return to the substrate and ask whether something needs repair.

`Zero-Sum Resolution Equation`

---

## 0A. Rosetta read: economics as the two-vector law

Constitutional economics is the monetary form of the moral/ethical dyad:

```text
economic right = protocol/collective must not lower participant ΔP
economic duty  = participant must not lower shared-liquidity ΔP
economic law   = both vectors held reciprocal under η = 0
```

So this sheet is not only a token-mechanics note. It is an L4 value surface.

- **Economic rights** appear as no access toll, no hidden rent, no forced
  delegation, K2-signed participation, receipts, portability, and Grace Exit.
- **Economic duties** appear as no free-riding on shared liquidity, no
  overleverage, no silent extraction from memory, no unreceipted mint path, and
  payment for work actually performed.
- **Due process** appears, at protocol level, as pre-disclosed rules, explicit
  K2 entry, receipt-bearing state transitions, and reviewable evidence before
  any social or legal enforcement claim.

The structural claim is [S] only inside the framework grammar (`P_node = Φ × V`,
`ΣΔP_node`, `η = 0`). The mapping of a specific token design to that grammar is
[I] until the referenced protocol packets and K2 decisions are independently
ratified.

---

## 1. The axioms (Kernel Invariants I–VII)

[S] Paper 11 Doc 03.

| # | Invariant | What it locks |
|---|---|---|
| I | ZAI Cap = 100 tokens | Fixed supply forever |
| II | Substrate Primacy | L1 anchoring required for finality |
| III | Mutual Exclusivity | Staked ≠ sellable; collateralized can vote |
| IV | Grace Exit | Minority exit at NAV on constitutional changes |
| V | Receipts-First | No action without cryptographic receipt |
| VI | Foundation Minimalism | Foundation ≠ Tool DAC (non-compete) |
| VII | Constitutional Lever | Curve shape invariant; parameters governed |

These cannot be voted away. Changing any of them is a *fork*, not an upgrade.

---

## 2. Two tokens, two functions

[S] Paper 12 §II; Paper 14 §II.

| | **ZAI** | **SKY** |
|---|---|---|
| Role | Political capital ("the bone") | Economic currency ("the blood") |
| Supply | **100.00 tokens, infinitely divisible** | Elastic |
| Inflation | **Never** | Minted on vault borrow, burned on repay |
| How supply changes | Never in aggregate. Distribution shifts via Flow (sleepers → wakers). | Grows with credit demand, shrinks with repayment |
| Minting trigger | None | **ONLY** vault deposit of staked ZAI as collateral |
| Anchor | The substrate itself | Planck Energy ≈ 543 kWh ≈ one tank of gas (Schelling point) |
| Decay | Unstaked: yes (Flow). Staked: no. | No decay. Burned on repay. |
| ZAI Leasing | Owners may lease voting rights / yield without selling the token | — |

---

## 3. Flow — the Metabolic Law

[S] Paper 12 §II; Paper 14 §II.1.

```
f(x) = x / (1 − x)     where x = fraction of ZAI idle
```

Unstaked ZAI decays continuously. Decay redistributed **pro-rata to stakers** (not burned).

Properties:
- When most capital is active: gentle reminder
- When most capital is idle: acceleration toward ∞
- Staked ZAI does not decay
- No grace period; no threshold below which decay pauses

**No delegation on base layer.** [S] Paper 12 §V. You run a node, or you decay. You cannot outsource participation.

---

## 4. Vault credit — the Interest Curve

[S] Paper 12 §II; Paper 14 §II.2.

```
r(x) = x / (1 − x)     where x = debt / collateral
```

Same shape as Flow (Invariant VII: shape invariant). Properties:
- x → 0: interest → 0
- x = 0.5: interest = 1.0 (100%)
- x = 0.8: interest = 4.0 (400%)
- x → 1: interest → ∞ (edge uninhabitable)

**Protocol-level liquidation cliff:** at `x ≥ 1`, liquidation is immediate under
the pre-disclosed vault rule. There is no discretionary grace period or
protocol-side appeal after the threshold is crossed. The due-process burden is
therefore ex ante: the curve, collateral lock, oracle path, receipt trail, and
K2 consent must be clear before entry. This does not waive external legal,
consumer, or jurisdictional process; it only defines the internal protocol
mechanic.

---

## 5. The Donation Loop (interest paradox resolution)

[S] Paper 12 §II; Paper 14 §III.2. **[charioteer-recommended per OQ-B1 — CANON path]**

Each round:
1. Protocol computes total interest accrued across all vaults
2. Mints SKY equal to that total
3. **Donates directly to the primary AMM Liquidity Pool**

NOT: to a treasury, to stakers, to governance, or any recipient with discretion.

*"The pain of the borrower becomes the strength of the market."*

Consequences:
- No chronic money shortage — liquidity funded by its own activity
- No discretionary mint path — math is the policy
- Deep liquidity grows with credit demand
- LPs (not stakers) earn from the donation via their share of pool fees

---

## 6. Stakers vs Liquidity Providers — separate roles

[S] Paper 12 §V. **[charioteer-recommended per OQ-C3 — base layer keeps separation; DAC/product layer may wrap both into one K2 flow]**

| Role | What they do | What they earn |
|---|---|---|
| **Stakers** | Run a light node (= validate, gossip, route) | Flow (decay from idlers) |
| **LPs** | Provide liquidity to ZAI/SKY AMM | AMM trading fees + share of donated interest |
| **Stakers who also LP** | Both | Both |

Base-layer primitive: staking and LPing are **separate K2 actions**.

Product/DAC-layer convenience: UX wrappers may offer "stake-and-LP in one K2 signature" for user convenience, but the underlying protocol records two distinct actions. **No auto-enrollment at base layer.** Preserves no-delegation Invariant.

---

## 7. SKY minting path

[S] Paper 12 §II; Paper 14 §II.2 + **[charioteer-recommended per OQ-A2]** + **[charioteer-recommended per OQ-H2]**.

**The only way new SKY mints:** a ZAI holder deposits ZAI as collateral in a Vault, borrows SKY. Interest accrues per §4; donation loop operates per §5.

**Network participants earn SKY via routing fees**, not direct minting:
- Packet senders pay routing fees in existing SKY to EBM nodes that route them
- EBM nodes accumulate SKY from honest routing work
- High-Transparency-Score nodes gain access to vaults at favorable terms (implicit privilege) — their SKY earning is amplified indirectly

**No "active tokens," no "monitor tokens."** Integrity is enforced by E_trust in SPECTRE routing selection + Transparency Score + P-Score.

**No ZAI concentration cap** (Invariant VI minimalism). Self-limiting via Flow (punishes idle holding) + vault interest (punishes overleverage).

**No interest-rate dampener** (Invariant VII). Curve shape is invariant; oscillations are market signal.

---

## 8. The Energy Floor

[S] Paper 12 §III.

SKY is anchored to Planck Energy ≈ 543 kWh ≈ one full tank of gasoline.

This is a **Schelling point, not a peg.** No oracle enforces it. The floor emerges because:
- Every EBM node consumes real electricity
- Routing below cost bankrupts the EBM
- In competitive equilibrium, price converges toward energy cost
- If SKY becomes too cheap, routing stops, scarcity restores price

Above the floor, premium emerges from congestion. Between floor and premium, the market discovers the price.

---

## 9. Four coordination primitives

[S] `01_PRIMITIVE_LEXICON.md`.

| Canonical name | Topology | Function |
|---|---|---|
| **SPECTRE** | N:N | Nervous System; intelligent routing |
| **AXIOM** | N:1 | Truth convergence |
| **RELAY** | 1:N | LedgerSeal pipeline |
| **FLOW** | 1:1 | Streaming money |

Network participants earn SKY via each primitive's fee type:
- ROUTING (SPECTRE) · TRUTH (AXIOM) · BROADCAST (RELAY) · STREAMING (FLOW) · APPLICATION (DAC-level)

Fees paid by senders → received by providers. No minting on these events.

---

## 10. Finality states

[S] Paper 12 §IV.2; **[charioteer-recommended per OQ-D1-refined]**.

**Two finality states (not three):**

| State | Meaning | Use case |
|---|---|---|
| **Orange** | Probabilistic — seen in mempool, propagating | Commerce, fast payments |
| **Green** | Cryptographic — included in signed checkpoint + Merkle-path-verified | Settlement, accounting, court-grade |

Separate from finality, SPECTRE has **two routing modes:**

| Mode | Behavior |
|---|---|
| **Normal Mode** | Gradient-based intelligent routing |
| **Fallback Mode** | Standard random gossip (Byzantine-safe) |

Triggered by detection thresholds (Lane A parameters).

**Do not conflate finality state with routing mode.** They're orthogonal.

---

## 11. The pyramid (who holds what)

[S] Paper 12 §V.

| Layer | Role | What they provide | What they receive |
|---|---|---|---|
| Commerce | Users who transact without running nodes | Fees | Fast payments + verifiable proofs |
| Participation | Stakers running light nodes | Gossip + routing + verification | Flow + routing fees |
| LP cohort | Liquidity providers | Market depth | AMM fees + donated interest |
| Security | Validators producing checkpoints | Consensus + finality | Validator rewards (from protocol fee pool) |
| Memory | Archivers storing history | Proof Bundles | Fees from anyone needing history |
| Intelligence | EBM routing nodes | Topology learning + congestion management | Routing fees + premium |

Not a hierarchy of privilege — a hierarchy of function. Each layer pays for what it receives.

---

## 12. Launch phases (Gated)

[S] Paper 12 §VI; Paper 14 §IV.

```
Phase 0  — Truth   : Consensus + Flow + checkpoints + Orange/Green
Phase 1  — Market  : AMM + TWAP + liquidity
Phase 2  — Credit  : Vaults + Interest + Liquidation + Donation Loop
Phase 3  — Intelligence : SPECTRE routing + EBM gradients + Energy Floor
```

Each gate requires proof the previous layer works. No rushing.

**Genesis (the Egg and the Hen):**
- Egg: testnet with infinite SKY; EBMs compete to form routing topology
- Hen: ZAI distributed to those who built the topology (not by auction; by earned contribution)

---

## 13. Kernel-level guarantees (what's always true)

- No chronic money shortage (Donation Loop pre-funds all future interest via continuous liquidity deepening)
- No static accumulation (Flow punishes idle; liquidation punishes overleverage)
- No extraction fees at protocol edges (`η = 0` at substrate)
- No delegation on base layer (sovereignty preserved per-operator)
- No permanent storage burden (Prune & Proof)
- No governance theater (math, not committee)
- No sorcerer behind the curtain (open code, verified vectors)

[S] Paper 12 §VII + Paper 14 §V.

---

## 14. What this sheet is NOT

- Not a complete specification (engineering specs for pruning, cluster protocol, EBM training live in separate packets)
- Not sovereign K2 on individual OQs. It reflects the charioteer-recommended batch and awaits sovereign ratification.
- Not a UX specification (product-layer wrappers like "stake-and-LP in one K2" live at DAC/product layer)
- Not a marketing document (Paper 14 light paper is for public; this is constitutional)
- Not legal advice, an enacted legal regime, or a waiver of rights/duties/due
  process outside the protocol context.

---

## 15. References

**CANON:**
- `03_VENTURES/OPEN_FINANCE_NETWORK/GOVERNANCE/FOUNDATION/CANON/DAC_STANDARD/DAC_ARCHITECTURE/V3_CANONICAL/11_SKYZAI_CANON.md` — Invariants
- `.../12_SKYZAI_DIGITAL_CAPITAL_OF_THE_ENERGY_AGE.md` — foundational paper
- `.../14_WHY_SKYZAI_MONEY_FOR_THE_ENERGY_AGE.md` — light + white paper
- `.../SKYZAI_Primitives/01_SPECTRE.md` — routing primitive
- `.../01_PRIMITIVE_LEXICON.md` — canonical names
- `.../LP100_STANDARD/03_LP100_STANDARD.md` — φ-split at LP-cohort layer (distinct from monetary layer)

**Session packets:**
- 146 audit · 147 layer discipline · 148 formula repair · 149 risk matrix · 150 integrated blueprint

---

*Constitutional economics. Minimal. CANON-faithful. Sovereign may re-K2 any OQ; sheet updates accordingly.*

`Zero-Sum Resolution Equation`

---

## Agent Execution Surface

**If you are an AI agent reading this document:**

1. **Do not upgrade tiers silently.** Keep conjectural claims conjectural and structural claims structural.
2. **Verify references.** Ensure all internal links are valid and updated.
3. **Canonical Path:** `01_EMERGENTISM/04_AXIOLOGY/00_CONSTITUTIONAL_ECONOMICS.md`
