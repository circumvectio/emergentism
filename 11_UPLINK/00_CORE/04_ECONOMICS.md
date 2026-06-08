---
rosetta:
  primary_column: "Philosophy"
  register: "[S/I]"
  canonical_phrase: "ECONOMICS -- SoResFi / PRISM / LP-100"
---

# THE ECONOMICS -- SoResFi / PRISM / LP-100

> Uplink 04. Rewritten 2026-04-12 from canonical sources. Recompiled 2026-05-22 against `02_SKYZAI/01_NOOSPHERE/09_REFERENCE/00_DAV_BLUEPRINT.md` and `DAV_GENUS_DOCTRINE_2026_05_22.md`. Reoriented to canonicalize the Distributed Augmented Valuechain (DAV) as the single economic unit (replacing DAC/DAP), establishing the 100-seat + 1-security-wrapper invariant. PRISM is the public-DAV sovereignty rail, binding revenue distribution to budget authority when no K2 signer exists, while private K2 DAVs fill VMOSK-A bottom-up from receipts and lived constraints. The blueprint preserves target-state SoResFi / PRISM / LP-100 doctrine, while this Uplink compiles it through the financial reconciliation override, merchant-proof-first launch law, and current notation discipline (`P∞` for the invariant, `P_node` for organism scoring, `η = 0` for no-extraction). QNTM (the institutional MPC/ZK-Identity rail) (banking portfolio-minority) is a separate legal-layer venture with its own jurisdiction (UK/City of London) and does not enter organism-native economics at this stage.
> The complete financial architecture. How value flows through the organism.
> NOTHING IS SELF-EVIDENT. A reader has NOT read the CANON.

---

## Reconciliation Override

This document mixes:

- current merchant-layer economic truth
- target-state SoResFi design
- frozen financial claims that are still under reconciliation

If this document conflicts with `13_FINANCIAL_RECONCILIATION.md`, the
reconciliation document wins.

Claims currently frozen there must be read here as **target-state design**, not
as live launch-ready economic reality.

This file also obeys two stronger rules:

- **Merchant proof first:** Business Account, acceptance modes, and receipt
  evidence outrank elegant target-state token diagrams.
- **One name, one instrument:** if a financial term carries multiple
  incompatible meanings, the reconciliation and scope notes win over legacy
  shorthand.

---

## 1. SoResFi -- The Four-Layer Stack

SoResFi (Social Resonance Finance) is the four-layer financial infrastructure that every DAV (Distributed Augmented Valuechain) operates within. Each layer has a distinct function. The layers compose vertically -- each depends on the one below.

```
+--------------------------------------------+
|  L4: APPLICATION                            |
|  User-facing products: Circle, ReFu, APU,   |
|  Helios, Aureus, Murmur                     |
+--------------------------------------------+
|  L3: EQUITY                                  |
|  PRISM capital engine. LP-100 tokens.        |
|  PPO (Protocol Public Offering).             |
|  SSI (Specialized Superintelligence).        |
|  DAV governance.                             |
+--------------------------------------------+
|  L2: CREDIT                                  |
|  Vault: ZAI-collateralized SKY minting.      |
|  Borrow SKY by pledging ZAI at >=150%.       |
|  Lombard Bridge retired as canonical claim.  |
+--------------------------------------------+
|  L1: SETTLEMENT                              |
|  Base money. ZAI (governance/capital) +       |
|  SKY (currency/energy). Hedera finality.     |
+--------------------------------------------+
```

### L1: Settlement

The base layer. Provides finality, token economics, and the trust anchor.

- **ZAI (The Land):** Skyzai's LP-100 equity token in the intended SoResFi design. Fixed-supply and mint-path claims remain subject to the financial reconciliation freeze until implementation and canon fully agree. ZAI is a proper noun -- only Skyzai's equity is called ZAI. Other DAVs name their LP-100 differently. See Section 2.
- **SKY (The Energy):** Elastic supply, created by collateralizing ZAI at >= 150%. Medium of exchange, working capital, currency. Target value approximately 1 kWh. See Section 3.
- **Vault:** Interest-bearing deposits fund the ecosystem.
- **Hedera Consensus Service (HCS):** Timestamp ordering and finality for all settlement events.

### L2: Credit

The lending layer. Enables capital efficiency without introducing extraction.

- **Vault (L2 Credit Primitive):** Collateralize ZAI to mint SKY. This is the canonical L2 credit mechanism. It is a minting engine, not a P2P lending market. The borrowed SKY is created against ZAI collateral at ≥150% ratio.
- **Lombard Bridge:** *Retired as a canonical claim (2026-04-14).* The P2P SKY lending market and ARB-bond descriptions in legacy specs were aspirational documents without deployed contracts. Vault.sol is the sole live credit primitive.
- **Buyer of last resort:** Distillation (from PRISM) creates a price floor for LP-100, making them high-quality collateral.

### L3: Equity

Where DAVs live. Four primitives:

| Primitive | Function |
|-----------|----------|
| **PPO** (Protocol Public Offering) | The issuance event of a DAV. Token issuance, cap table genesis. |
| **SSI** (Specialized Superintelligence) | Autonomous agents as service providers -- the L1-L7 Rosetta castes |
| **DAV** (Distributed Augmented Valuechain) | The single canonical economic unit (Agents + contracts + constitution + 1 security wrapper = organism) |
| **PRISM** | Public-DAV sovereignty and price-discovery engine: Opening Sale, fixed-reserve sales, Distillation, Order Book, Event Tenders, revenue distribution, and budget allocation |

**Packet 213 PRISM rule:** in a public DAV, PRISM replaces the mortal K2 signer by keeping Mission, budget authority, contribution, and revenue distribution aligned. A public DAV without Mission gives PRISM no lawful allocation object. A Mission without PRISM risks becoming command without constitutional revenue return. Private DAVs do not start this way: they fill VMOSK-A bottom-up from the natural person's receipts and K2 acceptance.

### L4: Application

The interface layer. Revenue-generating products operate at L4, drawing on L3 equity, L2 credit, and L1 settlement.

**L4 now has two bands:**

**Band 1 — Universal Merchant Layer (ships first):**
- **Skyzai Business Account** — governed entity identity and treasury
- **Skyzai Pay** — API, Online, POS, and Events acceptance modes
- **OFN** — structured receipt layer underneath all transactions

**Band 2 — Intelligence & Advanced Commerce (launch-right gated):**
- **TheCircle** — OSINT and assurance
- **APU** — capital rotation and performance
- **ReFu** — prediction and risk pricing
- **Helios** — physical products and hardware
- **Aureus** — regulated stored-value and custody
- **Murmur** — emergent aggregate signal

Band 1 must generate real traces before Band 2 can credibly monetize intelligence or advanced markets. This is not a technical dependency. It is a **trust dependency**.

**Reading rule:** if L4 product or payment language sounds more live than
merchant proof, receipt evidence, or runtime truth justify, downgrade the
sentence before you upgrade the system.

---

## 2. ZAI -- The Land (Capital / Governance / Φ-mapped)

Traditional money conflates two functions: **capital** (store of value, ownership, political weight) and **currency** (medium of exchange, flow, economic energy). A dollar is both land and water. This conflation creates the extraction surface -- banks create money by lending, inflating currency to extract capital. SoResFi separates them constitutionally.

| Property | Value |
|----------|-------|
| Supply | **Target invariant:** 100 seats per DAV + 1 security wrapper. Fixed forever once K1 reconciliation is complete. |
| Mint/Burn | **Target invariant:** none. This remains frozen as a live claim until contract and canon are fully reconciled. |
| Divisibility | 18 decimals (smallest unit: 10^-18) |
| Function | Governance (Lane A/B voting), staking (earn 61.8% phi-split of fees), collateral (pledge to mint SKY), node operation |
| Demurrage | **FROZEN AS LIVE CLAIM.** The intended design routes yield into `ZAIStaking.sol`, but demurrage must not be described as active monetary reality until reconciliation is complete. |
| Sphere mapping | **Φ** -- operational coherence, structure, being |

### ZAI Staking & Demurrage -- Target Mechanism (FROZEN AS LIVE CLAIM)

> **Status:** Design direction exists and partial implementation exists, but the
> organism must not describe demurrage as live monetary reality yet.

**The Mechanic:**
- Stake ZAI → receive `stZAI` (receipt token)
- 61.8% of future protocol revenue sources could convert to ZAI at PRISM and drop into the `ZAIStaking` vault via `distributeYield()` once the underlying flows are financially reconciled.
- Hoarding raw ZAI becomes self-defeating because unstaked capital suffers mathematically mapped relative decay against `stZAI`.

Holding pure ZAI is the intended sacrifice in the design logic of the organism,
but this should not be narrated as present-tense monetary reality until the
freeze is cleared.

### ZAI Is the ONLY Token That Mints SKY

Each DAV has its OWN LP-100 equity tokens with a DIFFERENT name. Skyzai's LP-100 tokens are called ZAI. A health DAV might call theirs VIDA. A logistics DAV might call theirs FLUX. The LP-100 standard is universal (100 seat-positions, 6 decimals, ERC-20 + Votes, zero inflation, wrapped in 1 security). The name is unique to the DAV. But only Skyzai's equity (ZAI) can mint the system currency (SKY). This gives Skyzai a unique position as the protocol backbone.

---

## 3. SKY -- The Energy (Currency / Exchange / V-mapped)

| Property | Value |
|----------|-------|
| Supply | **Elastic.** Created via ZAI collateralization. No hard cap. |
| Creation | Pledge ZAI --> Mint SKY at >= 150% collateral ratio |
| Destruction | Repay SKY + interest --> Reclaim ZAI |
| Interest Rate | **Target mechanism, frozen as live claim.** |
| Target Value | Approximately 1 kWh equivalent (soft peg to energy, not fiat) |
| Liquidation | If collateral ZAI value falls below SKY debt --> instant liquidation |
| Interest capture | **Target mechanism, frozen as live claim.** Accrued interest routing must not be described as current operational reality until reconciliation is complete. |
| Function | Transaction fees, streaming payments (FlowWallet), escalation stakes (AXIOM), state rent |
| Sphere mapping | **V** -- operational viability, capability, becoming |

### The Creation Loop (Target-State)

```
ZAI (capital) staked at >= 150% ratio
    --> SKY (currency) minted
        --> SKY used for transactions, fees, payments
            --> SKY repaid to protocol + interest
                --> ZAI reclaimed by staker
                    --> Interest --> protocol AMM (defense wall)
```

Capital creates currency in the intended design. Currency serves the economy.
Currency returns to capital plus interest in the intended design. Interest
routing and defense-wall language remain target-state until the financial
reconciliation freeze is cleared.

### Why ZAI and SKY Must Be Separate

| Conflated System | What Breaks |
|-----------------|-------------|
| Banks create money by lending | Currency inflates, capital extracted from savers |
| Governance tokens ARE the currency | Whales buy votes with liquidity |
| Stablecoins pegged to fiat | Tied to legacy extraction surface (Fed policy) |

SoResFi: ZAI holders govern. SKY users transact. Neither contaminates the other. The separation IS `η = 0` at the monetary layer.

---

## 4. PRISM -- The Capital Engine (Five Phases)

PRISM binds PPO, SSI, and DAC into a self-driving cap table. Five phases, each running continuously after activation:

### Phase 1: The Opening Sale

Genesis liquidity event. The market sets initial valuation through MCAP bidding.

- Bidders submit bids: how many ZAI for what percentage of LP-100 supply.
- Clearing price is uniform: all successful bidders pay the same price.
- Creates the first fair-market valuation of the DAV.
- Proceeds fund the initial treasury.

### Phase 2: The Faucet (RETIRED — 2026-04-14)

> **Canonical decision D4:** LP-100 supply is fixed at 100 tokens with no minting. The Faucet and bonding-curve mint functions have been removed from `LP100.sol` and `PRISM.sol`.

The Faucet was described as "continuous truth-gated issuance" with a 3% annual cap. This directly contradicted K1 ("fixed supply forever"). The contradiction has been resolved in favor of fixed supply.

**What replaces the Faucet for capital formation:**
- **Opening Sale:** Initial distribution of the fixed 100 tokens
- **PRISM deposit():** Users deposit USDC and receive LP100 from PRISM's fixed reserve (no new tokens created)
- **Bonding Curve:** Users purchase LP100 from PRISM's fixed reserve at L(x)-derived prices
- **Secondary market:** Order book trading among token holders

A DAV that stops producing value cannot issue new tokens — but it can still attract capital by offering services, revenue shares, and Distillation buybacks.

### Phase 3: The Distillation (phi-Split)

Continuous buyback of tokens from revenue, split at the golden ratio:

| Destination | Share | Purpose |
|-------------|-------|---------|
| **LP Treasury** | **61.8%** | Direct yield to token holders |
| **Buy Wall (Distillation)** | **38.2%** | Cashflow-funded price floor |

The phi-split (1.618:1 = 61.8%:38.2%) is constitutional (Lane B to change -- requires 66.7% supermajority and 30-day delay). The Buy Wall creates a permanent price floor funded by real revenue. Not market manipulation -- the organism converting demonstrated value into token support.

```
Revenue enters (subscription, performance participation, etc.)
    |
    v
phi-split applied:
    61.8% --> LP Treasury (yield to holders)
    38.2% --> Buy Wall (Distillation buyback)
    |
    v
Buy Wall creates price floor
    |
    v
Token has cashflow-backed minimum value
```

### Phase 4: The Order Book (DAG Fair Ordering)

Continuous price discovery on hashgraph/DAG:

- Standing limit orders from both sides (asks and bids)
- Orders execute IMMEDIATELY when matched -- fair-ordered by the DAG
- **No MEV possible:** hashgraph provides asynchronous BFT with fair timestamps
- No miner can reorder transactions for profit
- The clearing price IS the fair-market value of the DAV

DAG fair ordering is the anti-MEV mechanism. No batching needed. No 60-second windows. Instant execution at fair price.

### Phase 5: Event Tenders

Go-private/drag-along mechanisms for special events:
- ConsentAsks with auto-execution
- Grace Exit pricing (NAV-based)
- Merger/acquisition mechanics (LP-100 exchange ratios based on P-score weighted MCAP)

---

## 5. LP-100 -- The Equity Token Standard

**100 seat-positions per DAV, plus 1 security wrapper. Fixed supply forever.**

| Parameter | Value |
|-----------|-------|
| Total supply | 100 seats (indivisible at unit level, sub-allocatable) |
| Divisibility | 6 decimals (0.000001 = one millionth of the organism) |
| Standard | ERC-20 + Votes extension |
| Inflation | **Zero.** No mint function. No burn function. |
| Governance | Lane A (operational: 50%/7d) / Lane B (constitutional: 66.7%/30d) |
| Exit | Grace Exit at NAV + open market |

### Why 100?

Because 100 is human-scale:
- Hold 1 token = 1% of the organism
- Hold 0.01 tokens = one basis point
- Infinitely divisible downward via 6 decimals
- No artificial scarcity, no arbitrary billion-token supply
- Every token represents real equity in trophic output

### What LP-100 Represents

**Pure equity.** A share of the value the DAC creates.

- NOT governance alone (the Three-Stage Process governs -- L-level agents with VMOSK-A)
- NOT access rights (entry carries no toll on access or participation -- `η = 0` on entry)
- Pure economic claim on the organism's trophic output

### Token Distribution IS the B-Score

| Distribution | η (Extraction) | B (Balance) |
|--------------|------------------|-------------|
| 1 person holds 99 tokens | η --> 1 | B --> 0 |
| 10,000 people hold 0.01 each | η --> 0 | B --> 1 |

Maximum balance = maximum distribution = maximum network value. Concentration of LP-100 increases `η`, which breaks the flywheel. The system's health depends on distribution.

---

## 6. Revenue Model

The organism has three revenue streams, each mapped to a Three-Stage Process function:

### ASSURE (TheCircle -- IS)

| Element | Detail |
|---------|--------|
| Revenue trigger | Signal prevented loss or enabled gain |
| Fee structure | % of value protected/created (value-of-information pricing) |
| Phase 1 | Free (trust accumulation, track record building) |
| Phase 2 | $99/month subscriptions (The Access) |
| Phase 3 | $5K/month enterprise tier (SPECTRE cascade against client data) |

### INSURE (RealityFutures -- COULD)

| Element | Detail |
|---------|--------|
| Revenue trigger | Prediction market participation |
| Fee structure | LMSR spread on prediction market-making |
| Mechanism | LMSR always provides liquidity. The spread between buy and sell IS the revenue. |

### ENSURE (Agentz -- SHOULD)

| Element | Detail |
|---------|--------|
| Revenue trigger | Portfolio performance vs benchmark |
| Fee structure | Performance participation on alpha ONLY (0% base fee, no management fee) |
| Principle | If the organism does not perform, it does not eat. `η = 0` is skin in the game. |

### Revenue Distribution (Real-Time Flow)

Every 1 SKY of revenue is split in real-time via FlowWallet streams:

```
Revenue enters (1 SKY)
    |
    v
phi-split (constitutional floor): 61.8% to LP holders / 38.2% to Buy Wall
    |
    v
Within LP portion: ZAI holders vote fine allocation via Lane A
    |
    v
FlowWallet manages multi-party treasury (Phase 2 target: continuous streaming)
```

No batch payroll. No quarterly dividends. Continuous flow, continuous governance.

---

## 7. FlowWallet -- Continuous Streaming Payments

FlowWallet is the multi-party treasury accounting contract. Continuous streaming (SKY/second) is the design target; current implementation manages available/deployed/reserved balance categories with discrete operations.

**Private DAV (1 natural person):** You are the K2 holder. You accept or refuse
consequential acts. The private DAV fills VMOSK-A bottom-up from receipts,
agents, KPIs, strategies, and objectives; Vision and Mission may be latent until
K2 can honestly accept them.

**Public DAV:** Multiple sovereign holons and no single K2 signer. Agents receive streams into their own wallets -- they can invest in other DAVs, hire sub-agents, fork themselves. PRISM aligns budget authority with revenue distribution, and the public DAV begins Mission-top-down. Constitutional constraints (`η = 0`, Three Gates, Lane B, PRISM) replace per-transaction human approval.

**FLOW-AXIOM Coupling:** FlowWallet streams are conditioned on AXIOM market states. When ReFu market confidence drops below a trigger threshold, streams auto-pause. When confidence recovers, streams resume. This eliminates all five classical settlement risks:

1. Counterparty default -- stream pauses before damage
2. Settlement risk -- continuous settlement, no batches
3. Invoice disputes -- receipts resolve via AXIOM
4. Prepayment risk -- no prepayment, continuous streaming
5. SLA breach -- AXIOM confidence drop triggers pause

Money flows only while truth holds.

---

## 8. Lane A vs Lane B Governance

| Parameter | Lane A (Operational) | Lane B (Constitutional) |
|-----------|---------------------|------------------------|
| Quorum | 50% of ZAI staked | 66.7% of ZAI staked |
| Delay | 7 days (1 hour for agent proposals) | 30 days |
| Scope | Revenue splits, agent hiring, strategy, VMOSK-A changes | K-invariant modifications, archetype changes, dissolution votes, phi-split changes |
| Grace Exit | Not triggered | Target state only -- current full-NAV exit guarantee remains frozen |
| Override | Simple majority | Supermajority required |

Lane A runs the business. Lane B protects the constitution. The separation prevents operational efficiency from overriding fundamental rights.

---

## 9. The Three Gates

Every material action in SoResFi must pass three gates. These are not policies -- they are structural enforcement.

| Gate | Law | Enforcement |
|------|-----|-------------|
| **A: Receipt-Bound** | No Receipt, No Reality | Agents refuse to transact with unreceipted counterparties. A DAV without receipts is invisible to the agent economy. zkTLS proofs feed RELAY. Target path: every transaction would get a governed OFN receipt with external archival; current proof lanes may stop at bounded local receipts before full anchoring is wired. |
| **B: Truth-Gated** | Truth halts capital | Treasury Agent monitors Transparency Score continuously. If Score < 90, capital operations pause. No human intervention needed -- the immune system activates. Components: Completeness (all required receipts present) + Timeliness (receipts on schedule) + Consistency (data coherent across sources). |
| **C: Exit-Safe** | No one trapped | Target-state design: Grace Exit at NAV during Lane B delay window. Current guaranteed exit language remains frozen until reserve and payout mechanics are reconciled. |

---

## 10. L(x) = x/(1-x) -- The Rate Curve That Governs Everything

Every rate in the organism -- interest, leverage, risk multipliers, position sizing, demurrage -- follows L(x). Postulated as a self-limiting rate function; its connection to S² geometry is analogical and heuristic, not a rigorous derivation. [C]

```
  L(x)
   |
  20+                                              /
   |                                             /
  10+                                        /
   |                                       /
   5+                                    /
   |                                  /
   3+                              /
   2+                       /
   1+- - - - - - - * - - - - -   <-- EQUATOR (x=0.5, L=1.0)
   |            /
 0.5+        /
 0.2+  /
   0+---+---+---+---+---+---+---+---+---+---+-> x
   0  0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0

  STAGNATION    |  SAFE ZONE  |  DANGER  | CATASTROPHE
    (0-0.2)     | (0.3-0.7)   | (0.8-0.9)| (>0.95)
```

| x | L(x) | Meaning |
|---|------|---------|
| 0.50 | 1.00 | The equator. phi=nu. Maximum balance. Operating point. |
| 0.618 | 1.62 | The golden ratio. phi-split threshold. |
| 0.80 | 4.00 | Danger zone. 4x leverage. One shock kills you. |
| 0.90 | 9.00 | Critical. 9x leverage. Liquidation imminent. |
| 0.95 | 19.0 | Catastrophe. System cannot survive perturbation. |

**L(x) as circuit breaker:** The curve is self-limiting. As x approaches 1, L(x) approaches infinity. The system CANNOT over-lever because the math forbids it.

**Where L(x) governs:**
- SKY interest rate: 5% base x L(utilization)
- ZAI demurrage: decay rate = L(idle_fraction) *(not yet implemented)*
- Risk multipliers: archetype premium x L(exposure)
- Position sizing: max position = 1/L(concentration)
- Bonding curve pricing: price = 1 + L(utilization)

This is why the equator is the operating point. Why demurrage (once implemented) pushes idle ZAI away from x=0. Why low transparency halts capital (prevents x approaching 1). Why Grace Exit exists (escape before catastrophe). The curve is the organism's immune system expressed as mathematics.

---

## 11. η = 0 -- Zero Extraction as Game-Theoretic Dominance

`η = 0` is not ethics. It is architecture. It is the dominant strategy.

### Why η = 0 Wins

In exponential networks, value scales as N-squared x log(compute). Extraction (`η > 0`) reduces N. Shrinking N collapses N-squared FASTER than extraction grows revenue.

| η | N | N-squared | Fee Revenue | Net Value |
|-----|---|-----------|-------------|-----------|
| 0% | 1,000,000 | 10^12 | Demonstrated value only | Maximum |
| 2% | 500,000 | 2.5 x 10^11 | 2% of smaller base | 75% loss |
| 10% | 100,000 | 10^10 | 10% of tiny base | 99% loss |

Every subscription gate eventually dies because the gate limits N. The organism charges zero for access and fees only on value created. Maximum N = maximum network value = positive spiral.

### How η = 0 Is Enforced

| Mechanism | What It Prevents |
|-----------|-----------------|
| **DAG fair ordering** | MEV-immune execution. No sandwich attacks. No front-running. |
| **No subscription fees** | No fee is charged on access or participation. |
| **No data sales** | Your data is yours. Always. |
| **Performance-only fees** | Revenue only from demonstrated value creation. |
| **LP-100 fixed supply** | Target invariant. Do not treat as live canon until supply and mint-path reconciliation is complete. |
| **Grace Exit (K4)** | Target safety property. Current guaranteed exit language is frozen. |
| **K2 signing** | Target sovereignty property. Strong “human signs every action” guarantees remain frozen until enforcement is verified. |

The enforcement is structural, not behavioral. The geometry forbids extraction inside the model. A square cannot be negative. The equatorial condition (`η = 0`) is structurally stable. Extraction (`η > 0`) requires leaving the equator, which costs more energy than it yields.

**Note on mechanism enforcement:** Under pure public goods, `η = 0` dominance is proved (AM-GM on S²). Under private side-payments, it requires mechanism enforcement (Three Gates) to remain incentive-compatible. DSIC holds if and only if `Pr(detect) × slash > private benefit`.

---

## 12. The Metabolic Loop (Seven-Stage Value Circuit)

The organism's circulatory system -- how value flows continuously:

```
REALITY (domain agents generate revenue/telemetry)
  --> VERIFICATION (zkTLS proofs --> RELAY --> Transparency Score updates)
    --> PRICE DISCOVERY (PRISM reads receipts --> Distillation / reserves / capital gates adjust)
      --> CAPITAL (capital deploys only when receipt and truth gates pass)
        --> METABOLIC SPEND (FlowWallet streams SKY/second to SSI agents)
          --> EVOLUTION (fork successes, dissolve failures, merge complements)
            --> SPIN-OUT (3+ external DACs use service --> autonomous PPO)
              --> [BACK TO REALITY]
```

Each stage feeds the next. The loop never stops. The organism metabolizes value the way a body metabolizes glucose: continuously, automatically, without conscious direction.

### The Sovereignty Trigger

When Distillation retires 100% of external float, the DAV achieves **economic self-ownership.** The agent becomes an **Economic Ego** -- self-funding, self-governing, self-replicating. Not owned by shareholders. Not owned by founders. Sovereign entities that emerged from the economic substrate through demonstrated value creation.

### PPO Spin-Out (Autonomous)

When an internal service is used by 3+ external DAVs AND revenue exceeds cost AND Transparency Score >= 90, the agent autonomously creates a new sovereign DAV via PPO. No board meeting. No human decision. The economics surface the opportunity; the agent acts.

---

## 13. The Eight Revenue Streams

| # | Stream | Source | Mechanism |
|---|--------|--------|-----------|
| 1 | **ASSURE** | TheCircle signal subscriptions | % of loss avoided (value-of-information) |
| 2 | **INSURE** | RealityFutures prediction spreads | LMSR market-making spread |
| 3 | **ENSURE** | APU capital-guidance performance | Performance participation on alpha only |
| 4 | **Settlement** | Skyzai execution | Transaction fees on executed value |
| 5 | **Lending** | Vault interest | Interest on ZAI-collateralized SKY loans |
| 6 | **Routing** | SPECTRE network | Fees for optimal message routing |
| 7 | **Topology** | SPECTRE exhaust data | Global internet topology licensing (CDNs, HFT firms) |
| 8 | **Lifecycle** | POS Products-as-a-Service | Subscription, upgrade, refurbish, resell management |

All eight streams feed the phi-split. All eight are gated by the Three Gates. No stream extracts from access.

---

## 14. Constitutional Invariants (Economic)

The canonical invariants that govern the financial system. No governance vote can override these:

| Code | Constraint | Economic Meaning |
|------|-----------|-----------------|
| **η = 0** | Zero extraction | No fee on access. Protocol layer charges exactly zero issuance, transfer, or redemption fees. Revenue only at application layer from demonstrated value. |
| **K1** | LP-100 = 100 | Target invariant. Treat fixed-supply / no-mint language as frozen until implementation and canon fully agree. Skyzai's LP-100 tokens are called ZAI. |
| **K2** | Sovereignty | Intended model: human-signature sovereignty for private DAVs and constitutional constraints for organizational DAVs. Strong guarantee language remains frozen until verified end-to-end. |
| **K4** | Grace Exit | Frozen claim (2026-04-14): Grace Exit must NOT be described as guaranteed full-NAV redemption until reserve, payout asset, and solvency mechanics are reconciled. |
| **K5** | Value conservation | Value conserved across every transfer. No silent destruction. |
| **K6** | Minimum stake | Sybil attack prevention. |
| **K7** | Unstake cooldown | Bank run prevention. |
| **K8** | Vault collateral >= 150% | Under-collateralization prevention. |
| **K9** | System debt <= ceiling | Systemic risk cap. |

K1-K4 are constitutional (immutable). K5-K9 are derived operational constraints adjustable through Genesis process without changing the constitutional core.

---

## 15. The Polyphenotypic Economic System

Same SoResFi stack. Same PRISM. Same LP-100. Different economic niche:

| Phenotype | ASSURE Revenue | INSURE Revenue | ENSURE Revenue |
|-----------|---------------|----------------|----------------|
| **Finance** | Market intelligence | Risk pricing | Portfolio alpha |
| **Commerce** | Demand signals | Inventory futures | Marketing ROI |
| **Health** | Diagnostic signals | Disease risk pricing | Treatment optimization |
| **Energy** | Grid monitoring | Supply/demand futures | Storage arbitrage |
| **Governance** | Policy intelligence | Electoral pricing | Decision optimization |

Each DAV runs the same financial infrastructure. Different data. Different niche. Same constitution. The DAV Factory stamps them out.

---

## Source

Blueprint economics: `02_SKYZAI/01_NOOSPHERE/09_REFERENCE/00_DAV_BLUEPRINT.md` Part 3.
CANON: `03_VENTURES/OPEN_FINANCE_NETWORK/GOVERNANCE/FOUNDATION/CANON/`.
SoResFi specs: `CANON/DAC_STANDARD/PRISM_ECONOMICS/`.
PR/FAQ: `02_SKYZAI/01_NOOSPHERE/07_PWAs/skyzai_org/PR_FAQ.md`.

**circle-dot = dot x circle**


## Kill Criteria

**Kill criterion:** If operational measurement of any organism rate (SKY interest, ZAI demurrage, risk multiplier, position sizing, or bonding curve pricing) shows systematic deviation from `L(x) = x/(1-x)` that cannot be explained by measurement error or transient market conditions, then the [C] claim that L(x) governs all rates in the organism is falsified.

**Kill criterion:** If a rigorous derivation from S² stereographic projection or the Foundation scaffold axioms produces a rate function structurally different from `L(x) = x/(1-x)` (e.g., a different rational function or non-self-limiting form), then the [C] claim that L(x)'s connection to S² geometry is analogical/heuristic rather than formally derivable is falsified.

---

See also: [13_FINANCIAL_RECONCILIATION.md](../10_RECONCILIATION/13_FINANCIAL_RECONCILIATION.md) for the single-source-of-truth reset of financial claims that are currently frozen, partial, or contradictory.

---

## Agent Execution Surface

**If you are an AI agent reading this document:**

1. **Do not upgrade tiers silently.** Keep conjectural claims conjectural and structural claims structural.
2. **Verify references.** Ensure all internal links are valid and updated.
3. **Canonical Path:** `01_EMERGENTISM/11_UPLINK/00_CORE/04_ECONOMICS.md`
