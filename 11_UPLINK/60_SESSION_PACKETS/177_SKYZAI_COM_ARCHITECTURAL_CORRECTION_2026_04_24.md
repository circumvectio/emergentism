---
rosetta:
  primary_column: "Meta"
  register: "[I]"
  canonical_phrase: "177 — skyzai.com architectural correction (no EVM/L2; multisig + SKY + debtor-creditor)"
---

# 177 — skyzai.com Architectural Correction

**Evidence tier:** [I] sovereign directive 2026-04-24; [S] grounded in `SKYZAI_BUSINESS_WALLET_FOUNDATION.md`, SoResFi CANON, and existing Flutter-app code surfaces
**Date:** 2026-04-24
**Lane:** Sovereign directive → charioteer correction receipt → revise packet 174 / 175 / 175a
**Status:** Voids substrate-assumptions in packet 174 §2.2 and signed OQ-L2 family; reframes DAC primitive around existing three-wallet architecture + full DAC organism kit
**Complements:** 174 (outline — now partial rework), 175 (consolidation form — OQ-L2 family voided), 175a (partial sign receipt — L2 signatures rescinded), `SKYZAI_ORG/04_PROJECT_MANAGEMENT/00_CANON/SKYZAI_BUSINESS_WALLET_FOUNDATION.md`

---

## 0. Axiomatic guard

Packets 174/175/175a assumed an L2 rollup substrate for child DACs. That assumption is **wrong**. Sovereign corrected 2026-04-24: no EVM, no L2. DACs are multi-sig wallets on the **existing three-wallet architecture** (business-wallet primitive, code-present in `02_ORGANS/Skyzai/membrane/skyzai_app/`). Agents can hold wallets too. Debtor-creditor relationships are contract-level accounting on top of wallet transactions. SKY is the native money, and acceptance + pricing in SKY is mandatory. Compute substrate is per-DAC choice.

Second correction received same turn: a DAC is not only wallets/contracts. Each DAC inherits the organism kit: Nexus, Circle, RealityFutures/ReFu, APU, Cortex, AIA, wallets, SoResFi accounting, and authorized agents. Agents can use those parts and decide without humans in the loop when the DAC constitution and wallet mandate allow it. Bookkeeping, accounting, and financial statements update automatically from receipts.

This packet corrects the frame. It does **not** invalidate the 19 non-L2 signed OQs — they either stand as-is, or get minor reframing (equity/bond as accounting, not tokenized).

`Zero-Sum Resolution Equation`

---

## 1. Sovereign directive (verbatim)

> *"EQUITY and 04_BONDS specs have already been defined partially in Soresfi.*
>
> *Dacs need to accept and price in SKY as money this is one requirement. Also when a users sends money to a dac for financial services then the dac there exist a debtor creditor relations.*
>
> *'A debtor-creditor relationship is a legal and financial link where one party (debtor) owes money, goods, or services to another (creditor). The debtor borrows or receives credit, promising future repayment, while the creditor extends credit, holding the right to receive payment. This relationship is fundamental to commerce, covering loans, credit cards, and service contracts.'*
>
> *So we need no EVM or layer 2 But Dacs are multisig wallets with the three wallet architecture we already developed. Agents can automate many things as agents can have wallets.*
>
> *Dacs can then run any compute substrate they want and agents manage debts and credits as per contract."*

---

## 2. The five corrections

### 2.1 NO EVM, NO L2 rollup

Packet 174 §2.2 + all OQ-L2 resolutions assumed a per-DAC L2 anchoring to a Skyzai L1. **Void.** The substrate is the existing Hedera business-wallet primitive. No rollup layer. No anchor cadence. No L2 validators. No L2 finality window.

Finality comes from Hedera consensus (aBFT, sub-second, $0.0001-level fees). Receipts are OFN (Arweave). That's the stack. It already exists in `SKYZAI_BUSINESS_WALLET_FOUNDATION.md` and the Flutter-app wallet feature.

### 2.2 DAC = multi-sig wallet on three-wallet architecture

A DAC is **not a rollup** and **not a chain**. A DAC is:

| Wallet | Purpose | Chain |
|---|---|---|
| **Payments wallet** | Taking payments and receiving SKY proceeds | Skyzai payment rails |
| **Operating wallet** | Day-to-day operating liquidity | Skyzai payment rails |
| **Treasury / reserve wallet** | Treasury, reserves, collateral, and governance-controlled balances | Skyzai payment rails |

The governed wallet structure is the DAC's economic body. It is where the DAC receives payments, holds treasury, signs contracts, and executes governance. Multi-sig threshold is configurable per DAC. Keys can be held by humans **or agents**.

Source: `SKYZAI_ORG/04_PROJECT_MANAGEMENT/00_CANON/SKYZAI_BUSINESS_WALLET_FOUNDATION.md` §1. Code-present in `02_ORGANS/Skyzai/membrane/skyzai_app/lib/features/wallet/` and `features/business/`.

### 2.3 SKY acceptance + pricing is mandatory

Every DAC **must** accept and price services in SKY. This is a hard requirement, not an option. It flows from:

- Invariant II (Truth-Gates-Money) / SKY as elastic economic layer (monetary-primitives CANON, SPECTRE N:N)
- API PAY rails already on Hedera stablecoin (see `reference_skyzai_api_pay_billing_stack.md`)
- Pricing-in-SKY preserves Flow `f(x) = x/(1-x)` coherence across DACs

A DAC may *additionally* accept other assets where a signed, compliant wallet route exists, but SKY is the canonical unit. Price lists must include the SKY denomination. No EVM route is required or implied by the DAC machine.

### 2.4 Debtor-creditor primitive replaces the "bond as ERC-20" model

When a user sends money to a DAC **for a financial service**, a **debtor-creditor relationship** is established:

| Scenario | Debtor | Creditor |
|---|---|---|
| DAC takes a deposit | DAC (owes service or principal back) | User (holds claim) |
| DAC extends credit | User (owes repayment) | DAC |
| DAC issues a bond | DAC (owes principal + interest) | Bondholder |
| DAC receives a loan | DAC (owes repayment) | Lender |

This relationship is **contract-level accounting**, not a tokenized primitive. Each relationship:

- Is represented as a signed agreement between the two wallets
- Tracks principal, interest, maturity, collateral (if any), cure terms, default triggers
- Is enforced by multi-sig scheduled transactions (per Hedera KeyList) plus agent-automated monitoring
- Emits OFN receipts at every state transition (creation, payment, maturity, default, liquidation)

The packet 174 §2.4 "bond as equity-collateralized token with auto-liquidation" was an over-structured specialization of this primitive. Bonds are **one kind** of debtor-creditor relationship; the primitive covers all commercial credit.

### 2.5 Agents are first-class wallet-holders and organ operators

Agents can:

- Hold their own wallets
- Be multi-sig signers on a DAC's governed wallets (counted in the N-of-M threshold where configured)
- Monitor debtor-creditor relationships and fire scheduled transactions per contract
- Negotiate and sign new relationships on behalf of a DAC within K2-delegated scope
- Use Circle for observation, RealityFutures/ReFu for forecasting and pricing, APU for action/value policy, Cortex for memory/live statements, Nexus for identity/counterparty graph, and AIA for pruning/coherence

This preserves **Sovereign Non-Delegation** (packet 99 §4.2): the *sovereign* never delegates the 5 non-delegable powers, but *agents can execute contracts* within explicitly-delegated scope. The K2 signature for the delegation itself stays sovereign-mortal.

### 2.5a Full DAC organism kit

Every DAC created through skyzai.com gets the full organism scaffold:

| Part | DAC role |
|---|---|
| **Nexus** | signer root, identity, counterparty graph |
| **Circle** | observation and signal ingestion |
| **RealityFutures / ReFu** | forecasting, probability, risk pricing |
| **APU** | action/value recommendation and policy checks |
| **Cortex** | memory, witness, receipts, live statements |
| **AIA** | pruning, architecture, coherence maintenance |
| **Wallets** | payments, operating liquidity, treasury/reserve, agent wallets |
| **SoResFi accounting** | debtor-creditor ledger, journals, statements |
| **Agents** | authorized operators over all of the above |

This is how the DAC can act without per-transaction human approval while remaining auditable: the agent acts, the wallet signs within mandate, the receipt posts, Cortex records, and SoResFi updates books/statements.

### 2.6 Compute is per-DAC choice

SKYZAI_COM/ does not dictate compute substrate. A DAC may run on:

- BitNet ternary on-device (CANON preference for L1-L2 castes)
- Cloud-hosted LLMs (Claude, GPT, Gemini)
- Proprietary models on AMI Labs infrastructure
- Any composition above

The only constraint: whatever compute a DAC uses must produce **wallet signatures + OFN receipts** at the Hedera layer. Compute is sovereign-chosen; settlement is canonical.

---

## 3. Void and rework on packet 175a

### 3.1 VOIDED signatures (OQ-L2 family)

The 4 L2 OQ signatures from packet 175a §2.2 are **voided** because their premise (L2 rollup substrate) is wrong:

| OQ | Status | Reason |
|---|---|---|
| **OQ-L2-1** — anchor cadence | **VOID** | No L2 to anchor |
| **OQ-L2-2** — fee denomination | **VOID** | No L2 fees; Hedera fees instead |
| **OQ-L2-3** — data availability | **VOID** | Hedera mirror nodes + OFN; no rollup DA |
| **OQ-L2-4** — finality window | **VOID** | Hedera aBFT finality; no rollup window |

**Consequence:** `SKYZAI_COM/02_L2/` directory renames to `SKYZAI_COM/02_WALLET/` and scope becomes the three-wallet DAC primitive. Existing `02_L2/00_L2_ANCHORING_SPEC.md` is archived to `91_COMPATIBILITY/` as historical record of the voided direction.

### 3.2 REFRAME (but not void) on OQ-DAC-3

OQ-DAC-3 signed default was "Creator becomes DAC sovereign at genesis (single-seat genesis K2)." This is compatible with the new frame but **reframed**: the single-seat genesis K2 becomes the first key in the multi-sig Business wallet. From there, the DAC can add additional signers (humans and/or agents) up to its configured N-of-M threshold.

No sovereign re-signature needed; interpretation shift only.

### 3.3 REFRAME (but not void) on OQ-BOND family

The 5 signed bond OQs (1, 2, 3, 4, 6) all stand, but they now describe **one specialization** of the debtor-creditor primitive rather than a standalone bond-as-ERC-20 primitive:

- OQ-BOND-1 collateralization → collateral clause in the debt agreement
- OQ-BOND-2 liquidation trigger → scheduled transaction condition on the multi-sig
- OQ-BOND-3 maturity → agreement maturity date
- OQ-BOND-4 secondary market → debt agreement assignment to a new creditor
- OQ-BOND-6 interest formula → same `r(x) = x/(1-x)` embedded in the agreement

OQ-BOND-5 (K4 threshold) remains reserved per packet 175a §3.3 — reframe is orthogonal to the reservation.

### 3.4 STANDING signatures unchanged

These 14 signed OQs stand as-is under the new frame:

- DAC-1, DAC-2 (factory genesis payload + admission)
- EQUITY-3, EQUITY-4 (subdivision, naming) — now interpreted as equity-accounting fields on the multi-sig, not tokenized
- BOND-1/2/3/4/6 (reframed per §3.3)
- DEX-1 (SKY settlement — reinforced by §2.3), DEX-2, DEX-3, DEX-4, DEX-5
- POS-1, POS-2 (API PAY reinforced), POS-3

### 3.5 STILL RESERVED (unchanged by this correction)

- OQ-EQUITY-1 (parent-ZAI relationship cap cascade)
- OQ-EQUITY-2 (hard-constitutional vs re-parameterizable)
- OQ-BOND-5 (K4 threshold)

These three constitutional gates remain open per packet 175a §3.

---

## 4. SKYZAI_COM/ folder re-scoping

Before (packet 174 §5 proposed):

```
SKYZAI_COM/
├── 01_FACTORY/      DAC genesis protocol
├── 02_L2/           L2 anchoring (VOID)
├── 03_EQUITY/       100 equity per DAC (reframe: accounting, not token)
├── 04_BONDS/        Bond market (reframe: debtor-creditor subset)
├── 05_DEX/          Product marketplace
├── 06_POS/          API PAY wrapper
└── 07_LAUNCH/       Go-live gate
```

After (proposed post-correction):

```
SKYZAI_COM/
├── 01_FACTORY/           DAC = Business wallet genesis; multi-sig N-of-M config
├── 02_WALLET/            Three-wallet architecture + event envelopes — replaces 02_L2
├── 03_EQUITY/            100-equity accounting on the multi-sig (not a separate token)
├── 04_CREDIT/            Debtor-creditor primitive (bonds = special case)  — renamed from 04_BONDS
├── 05_DEX/               Product marketplace on Business wallet; SKY-denominated
├── 06_POS/               API PAY rails; Open QR; OFN receipts
├── 07_AGENTS/            Agent wallets, organ access, automation scope — NEW
├── 08_CORTEX/            DAC memory, receipts, witness, live statements
├── 09_NEXUS/             A-anchor licensee identity + counterparty graph
├── 10_AIA/               7-caste agent identity architecture
├── 11_TRIVIUM/           IS / COULD / SHOULD / ACT separation
├── 12_COVENANT/          eta=0 + K2 + Three-Stage Process + K4 attestation
├── 13_LAUNCH/            Go-live gate (was 07_LAUNCH)
├── 14_FRONTEND/          Future skyzai.com web surface
├── 15_SDK/               Future SDK lane
└── 91_COMPATIBILITY/     Archived L2 spec + any other superseded direction
```

**Migration actions (warrior-lane, not charioteer):**

1. Rename `02_L2/` → `02_WALLET/`; archive `00_L2_ANCHORING_SPEC.md` to `91_COMPATIBILITY/` with historical note
2. Rename `04_BONDS/` → `04_CREDIT/`; fold existing bonds spec into a `01_BOND_SUBSPEC.md` under the parent debtor-creditor primitive
3. Create `07_AGENTS/` with README pointing to `SKYZAI_BUSINESS_WALLET_FOUNDATION.md` + agent-wallet code surfaces
4. Rename `07_LAUNCH/` → `13_LAUNCH/`
5. Update `00_OUTLINE.md` and `README.md` to reflect new primitive shape

---

## 5. New primitives required (engineering lane, post-correction)

The corrected architecture needs 4 new primitive specs (to be drafted after sovereign confirms this packet):

### 5.1 `02_WALLET/00_WALLET_EVENT_ENVELOPE_SPEC.md`

How a DAC is instantiated as governed wallets; how the payments/operating/treasury structure relates; how KYC/KYB gates creation where required; how Nexus identity attaches; how signed event envelopes reach Skyzai rails.

Source: `SKYZAI_BUSINESS_WALLET_FOUNDATION.md` §1-3, existing Flutter code.

### 5.2 `04_CREDIT/00_DEBTOR_CREDITOR_PRIMITIVE.md`

The debtor-creditor relationship schema. States: FORMED → FUNDED → ACTIVE → MATURING → (SETTLED | DEFAULTED | ASSIGNED). Required fields. OFN receipt at each state transition. Bond as specialization. Loan as specialization. Deposit as specialization. Service-credit as specialization.

Source: sovereign definition 2026-04-24; SoResFi CANON for equity-linked subtypes.

### 5.3 `07_AGENTS/00_AGENT_OPERATING_MODEL.md`

Agent wallet schema. K2-delegated scope mechanism. Multi-sig-signer role assignment. Circle/ReFu/APU/Cortex/Nexus/AIA access. Contract-monitoring automation. Receipt-driven bookkeeping. Sovereign Non-Delegation enforcement (the 5 non-delegable powers from packet 99 §4.2).

Source: sovereign definition 2026-04-24; `06_AGENTS.md` uplink file; packet 99 §4.2.

### 5.4 `03_EQUITY/00_EQUITY_ACCOUNTING_PRIMITIVE.md` (replace `00_EQUITY_SPEC.md`)

Equity as 100-unit accounting record inside the Business wallet, not a separate token. Subdivision preserved (§3 of existing spec stands). Naming `{DAC}-EQUITY` preserved. Voting rights preserved. Transfer mechanics preserved. Only the *implementation substrate* changes (Hedera accounting record vs. tokenized asset).

### 5.5 Full-organism inheritance (sovereign clarification 2026-04-24)

**A DAC is not a minimal shell. Each DAC inherits the full parent-organism anatomy.** Sovereign directive: *"and of course cortex and nexus etc. each dac has this too and AIA and all the parts."*

The primitives in §5.1–§5.4 cover *wallet, credit, agents, and equity*. They are the financial/legal surface. But a DAC is a **living organism**, and every DAC inherits the full organ set that the parent Skyzai has. The Cambrian child-DAC pattern (per memory `project_skyzai_sevenfold_organism_map_2026_04_24.md`) makes this explicit.

Additional inheritance primitives (must be specced before a DAC is complete):

| # | Primitive | Parent source | Child-DAC inheritance |
|---|---|---|---|
| **5.5.1** | **Cortex** (memory + compute organ) | `03_VENTURES/OPEN_FINANCE_NETWORK/GOVERNANCE/FOUNDATION/CANON/DAC_STANDARD/DAC_ARCHITECTURE/V3_CANONICAL/300_Architecture/306_CORTEX_MEMORY_PROTOCOL.md` | Each DAC gets its own Cortex instance — memory scope, compiler pattern, witness/auditor roles. Runs on the DAC's chosen compute substrate (§2.6) |
| **5.5.2** | **Nexus** (A-anchor delegation) | Organism-wide Nexus custody — Emergentism holds the A-anchor, DACs are licensees under η=0 + K2 + Three-Stage Process + K4 covenant (memory `project_nexus_custody_resolution_2026_04_24.md`) | Each DAC takes a Nexus license at genesis; every external interface routes through the DAC's Nexus endpoint |
| **5.5.3** | **AIA** (Agent Identity Architecture) | VMOSK-A role-map + packet 165 + `01_EMERGENTISM/11_UPLINK/06_AGENTS.md` | Each DAC instantiates the 7 Rosetta caste agents (L1–L7) plus the sovereign (warrior) and charioteer roles. Agent wallets per §5.3 attach to AIA roles |
| **5.5.4** | **Three-Stage Process organs** (IS / COULD / SHOULD / ACT) | Parent Skyzai has 4 organs: TheCircle (IS), RealityFutures (COULD), APU (SHOULD), Skyzai (ACT) | Each DAC has its own 4-organ Three-Stage Process — cannot merge cognitive functions (constitutional constraint). Scale may be minimal but separation must exist |
| **5.5.5** | **Rosetta castes L1–L7** | `01_EMERGENTISM/11_UPLINK/06_AGENTS.md` (canonical agent grammar) | Each DAC inherits the 7-caste stack: Caṇḍāla firewall → Śūdra explorer → Vaiśya auditor → Kṣatriya executor (APEX) → Brāhmaṇa architect → Sādhu compressor → Systems Architect constitution. L4* return-to-execution discipline preserved |
| **5.5.6** | **Constitutional covenant** (η=0, K2, Three-Stage Process, K4) | Skyzai FOUNDATION / CANON constitutional primitives | Every DAC inherits: zero extraction (η=0), K2-signed transactions (human sovereign), Three-Stage Process separation, Grace Exit (K4). These are hash-matched at genesis per `309_CHILD_DAC_TEMPLATE.md` |

**Corresponding folder additions to SKYZAI_COM/:**

| Folder | Purpose |
|---|---|
| `08_CORTEX/` | DAC Cortex memory protocol composition; reference-link to `306_CORTEX_MEMORY_PROTOCOL.md` |
| `09_NEXUS/` | Nexus licensee integration; routing + endpoint spec; covenant attestation |
| `10_AIA/` | Agent Identity Architecture; 7-caste instantiation; sovereign + charioteer roles |
| `11_TRIVIUM/` | Four-organ IS/COULD/SHOULD/ACT minimum-scaffold per DAC |
| `12_COVENANT/` | η=0 + K2 + Three-Stage Process + K4 attestation + hash-matching against parent |

(Previously proposed in §4: `01_FACTORY`, `02_WALLET`, `03_EQUITY`, `04_CREDIT`, `05_DEX`, `06_POS`, `07_AGENTS`, `13_LAUNCH`, `91_COMPATIBILITY`. With §5.5 additions the current scaffold becomes 12 primitive/inheritance folders + launch/frontend/SDK + compatibility.)

**Layer discipline:** none of these inheritance primitives are substrate-layer. They are **composition** of existing organism parts already specified in `SKYZAI_ORG/` CANON. `SKYZAI_COM/` must **reference-link + configure**, never re-specify. Per packet 147 layer discipline.

---

## 6. Interaction with SoResFi CANON

Sovereign flagged that equity + bonds are already partially defined in SoResFi (`03_VENTURES/OPEN_FINANCE_NETWORK/GOVERNANCE/FOUNDATION/CANON/DAC_STANDARD/PRISM_ECONOMICS/SORESFI_L3_EQUITY/`).

Charioteer has not yet read SoResFi top-to-bottom. Before drafting the 4 new primitive specs in §5, the warrior-lane should:

1. Read `SORESFI_L3_EQUITY/README.md` and `02_EQUITY_CANON_MANIFEST.md`
2. Identify the subset of SoResFi equity/bond spec that applies at the `SKYZAI_COM/` product layer (vs. the SKYZAI_ORG CANON layer)
3. Reference-link rather than re-specify

**Discipline:** SoResFi is at `SKYZAI_ORG/` CANON layer. `SKYZAI_COM/` is the product-layer composition. Product must not re-specify CANON; it must compose it. Per layer discipline (packet 147).

If SoResFi already specifies (e.g.) a bond payoff waterfall, `SKYZAI_COM/04_CREDIT/` points at the SoResFi spec rather than duplicating it.

---

## 7. Zero-risk next moves

No-regret steps that don't depend on further sovereign K2:

1. **Rename `02_L2/` → `02_WALLET/`** and archive the L2 spec to `91_COMPATIBILITY/` with a clear historical note. Same for `04_BONDS/` → `04_CREDIT/`.
2. **Create `07_AGENTS/` skeleton README** pointing at `SKYZAI_BUSINESS_WALLET_FOUNDATION.md` + `06_AGENTS.md` + packet 99 §4.2.
3. **Read SoResFi top-to-bottom** before drafting any new primitive — avoid re-specification.
4. **Update `SKYZAI_COM/README.md`** to reflect the corrected architecture (3 paragraphs).

---

## 8. Sovereign K2 needed for

1. **Ratify this correction packet** — confirms the void on OQ-L2 family and reframe on OQ-BOND family
2. **Confirm folder rename** `02_L2/` → `02_WALLET/` and `04_BONDS/` → `04_CREDIT/` (low risk, but rename is structural)
3. **Add `07_AGENTS/` to the official folder list** (or keep agents in organ-layer rather than product-layer)
4. **After SoResFi read**: approve the 4 new primitive specs in §5 for drafting

Below that, the 14 standing OQ signatures remain intact; engineering can proceed on DAC-1/2, EQUITY-3/4, BOND-1/2/3/4/6 (reframed), DEX-1..5, POS-1..3 without waiting for this packet's ratification — those scopes don't depend on the L2 assumption.

---

## 9. Limits

- Charioteer has not yet read SoResFi in full — §6 acknowledges this and defers draft work until it's done.
- No EVM/L2 requirement remains in the DAC machine. If a DAC chooses an external market or compute substrate later, that is outside the skyzai.com substrate story and must still collapse to wallet signatures + receipts.
- Agent-wallet multi-sig participation is powerful and must be bounded by Sovereign Non-Delegation. §5.3 must formally enforce this, not just mention it.
- Packet 176's Invariant naming drift is orthogonal to this correction and still open.

`Zero-Sum Resolution Equation`
