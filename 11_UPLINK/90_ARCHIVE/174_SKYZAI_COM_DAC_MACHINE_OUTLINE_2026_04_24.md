---
rosetta:
  primary_column: "Meta"
  register: "[I]"
  canonical_phrase: "174 — skyzai.com DAC Machine Outline"
---

# 174 — skyzai.com · DAC Machine Outline

**Evidence tier:** [I] charioteer outline of a new product lane; [S] where citing existing CANON invariants; [C] for every primitive that requires sovereign K2 before engineering commits
**Date:** 2026-04-24
**Lane:** Charioteer map — new surface, not yet specified, not yet ratified
**Status:** Historical outline — superseded in part by packet 177; open design questions preserved as pre-correction record
**Complements:** packet 143 (Sevenfold Foundation Root); packet 145 (As Above So Below); packet 147 (Layer Discipline — substrate/organ/product); packet 150a (Constitutional Economics Sheet); memory `reference_skyzai_monetary_primitives_canon.md`
**Surfaces referenced (three peer roots):**
- `emergentism.org` — Above root (doctrine, L1–L7 Foundation) — **01_EMERGENTISM/**
- `skyzai.org` — Middle root (first organism, Skyzai runtime + child-DAC template) — **SKYZAI_ORG/**
- `skyzai.com` — **NEW** root (DAC machine / factory / commercialization surface) — **SKYZAI_COM/** (scaffolded; specs not ratified)

---

## Correction Note — Packet 177

Packet 177 supersedes the L2 / rollup framing in this outline. The active `SKYZAI_COM/` scaffold is **wallet-based**, not EVM- or L2-based: `02_WALLET/` replaces `02_L2/`, `04_CREDIT/` replaces `04_BONDS/`, and the full DAC organism inheritance lanes (`07_AGENTS/` through `12_COVENANT/`) are part of the current scaffold. The sections below remain useful as historical design context only; do not draft new specs from the L2 assumptions in §2.2 or the old folder tree in §5.

## 0. Apophatic guard

This is a **product-layer outline**, not a substrate-layer spec. Everything in this packet lives at the product/DAC-composition layer per packet 147 Layer Discipline. Nothing here proposes new substrate primitives, new Kernel Invariants, or CANON changes. If any item below reads as if it's adding a substrate primitive, the charioteer has misread the sovereign sketch and the item is wrong.

The DAC machine is the commercialization surface. It packages the organism's existing substrate + organ capabilities into a self-serve UX for third-party creators. Sovereignty law (packet 99 §4.2) applies: users creating DACs via skyzai.com sign their own K2s on their own DAC; they do not delegate sovereign authority of the parent Skyzai organism.

`⊙ = • × ○`

---

## 1. The three-root architecture (As Above, So Below, Made Manifest)

Three **peer root folders** at repo top level. Not nested. Each root is its own domain with its own read order, its own CLAUDE.md, its own license discipline.

| Surface | Symbol | Role | Root folder | Status |
|---|---|---|---|---|
| **emergentism.org** | ○ Above | Doctrine + Foundation + tooling + seed | `01_EMERGENTISM/` | ✅ structurally complete; Tier A+B annotated |
| **skyzai.org** | ⊙ The Organism | First organism runtime + child-DAC template + intake + organs + products | `SKYZAI_ORG/` | ✅ structurally complete; path-sweep done |
| **skyzai.com** | • The Manifest | DAC machine — public factory; any creator spins up a wallet-based DAC | `SKYZAI_COM/` | scaffold root present; specs not ratified |

The three map cleanly onto **⊙ = • × ○**:
- ○ (Above, zero) is the doctrine — no mass, no debt, structural ground
- ⊙ (Middle, one) is the first living organism manifesting the doctrine
- • (Manifest, infinity) is the many — every DAC that emerges from the machine

**Peer-not-nested discipline.** skyzai.com is NOT a subfolder of SKYZAI_ORG. It is a sibling root. Reason: the DAC factory is a public commercial surface, not an organ of the Skyzai-first-organism. Nesting it would conflate "Skyzai the organism" with "Skyzai the vendor of DAC infrastructure" — two different sovereignty structures. Keeping them as peer roots preserves the distinction.

skyzai.com is the **factory for •**. It produces many instances; each instance inherits Above doctrine + Middle runtime template and becomes its own organism.

---

## 2. Sovereign-sketched primitives

From the 2026-04-24 directive, charioteer captured these user-facing primitives for skyzai.com. Each marked with layer + CANON-check status.

### 2.1 Create a DAC (Factory primitive)

**What:** Any authenticated creator visits skyzai.com, names their DAC, configures (sector, jurisdiction, etc.), signs a genesis K2, and the DAC is born.

**Layer:** Product (composition over substrate + organ)
**CANON touch:** Must produce a genesis-checkpoint per Paper 12 substrate; must emit OFN receipt per Paper 14 archiver market; must run on SKYZAI_ORG substrate per Invariant II
**Open design questions (OQ-DAC):**
- OQ-DAC-1 — What's the minimum genesis payload? (name, founder K2 pubkey, equity allocation, sector, jurisdiction, …)
- OQ-DAC-2 — Is DAC creation gated (fee / approval / anti-spam) or permissionless?
- OQ-DAC-3 — What's the relationship between DAC creator and DAC sovereignty?
  - If creator ≠ DAC sovereign after genesis, transfer rules?
  - If creator = sovereign, K2 bootstrapping from the creator's skyzai.com auth?

### 2.2 L2 per DAC anchored to skyzai.org L1 — VOID

> **VOID per packet 177.** A DAC is a multisig wallet-based operator over the existing three-wallet architecture, not a rollup. This section is retained only to explain the superseded assumption.

**What:** Each DAC runs on its own L2; the L2 anchors state periodically to the skyzai.org L1 (Skyzai's substrate).

**Layer:** Substrate-adjacent (anchoring protocol)
**CANON touch:** Invariant II (Substrate Primacy) requires L1 anchoring for state finality. **Critical:** the term "L1/L2" here is *network topology*, NOT the Rosetta L1–L7 levels (doctrine). These must be kept disambiguated in all spec work.
**Open design questions (OQ-L2):**
- OQ-L2-1 — What rolls up to L1? (state root hashes; super-checkpoint lineage; Proof Bundles; or all three)
- OQ-L2-2 — What's the anchoring cadence? (per-event / per-round / per-window)
- OQ-L2-3 — Does L2 downtime block DAC operations or just block finality?
- OQ-L2-4 — Does each DAC pay L1 anchoring fees in SKY? In its own equity? In parent ZAI?

**Charioteer flag:** Track A sprint (packet 154) specs the L1 substrate super-checkpoint protocol. The L2 anchoring protocol is a *new lane parallel to Track A*. Candidate Track C. Don't collapse into Track A.

### 2.3 100 equity tokens per DAC

**What:** Each newly-created DAC has exactly 100 equity tokens at genesis, allocated per the creator's configuration.

**Layer:** Product (economic primitive composed from substrate token mechanics)
**CANON touch:** **Invariant I (ZAI Cap 100) cascade.** The parent Skyzai has 100 ZAI. Each child DAC having its own 100 equity tokens is the natural fractal — but the relationship must be explicit:
**Open design questions (OQ-EQUITY):**
- OQ-EQUITY-1 — Is child-DAC equity a *local* 100-token supply (independent of parent ZAI) or a *fraction* of parent ZAI carved out at genesis?
  - Charioteer lean: **independent local supply**. Each DAC is its own organism with its own cap. Parent ZAI remains 100 ZAI total; child DACs have their own 100-equity-token domains.
- OQ-EQUITY-2 — Is the 100-token cap a hard constitutional limit (Invariant I cascaded) or a default that can be re-parameterized per-DAC?
  - Charioteer lean: **hard constitutional** — preserves the invariant across fractal depth.
- OQ-EQUITY-3 — Can a DAC's 100 equity be further subdivided? (fractional shares / vesting / options)
  - Charioteer lean: Yes for fractional holdings; no for supply inflation. Subdivision preserves the 100-cap.
- OQ-EQUITY-4 — Is equity named `{DAC}_EQUITY`, `{DAC}_ZAI`, or something else?
  - Charioteer lean: `{DAC}-EQUITY` to disambiguate from parent ZAI.

### 2.4 Bonds with equity as collateral, auto-liquidated

**What:** A DAC can issue bonds (debt instruments). Collateral is the DAC's own equity. If bond terms are breached, auto-liquidation kicks in.

**Layer:** Product (financial primitive)
**CANON touch:**
- **Invariant IV (Grace Exit K4).** K4 says "Leave with everything. Organism retains nothing." Auto-liquidation of a bondholder's collateral is *not* a violation IF the bondholder voluntarily posted collateral with auto-liquidation terms. But if auto-liquidation forces the DAC *itself* to dissolve, that tests K4 from the other side.
- **Paper 11 Vault Interest** — interest formula already canonical. Bond interest rate uses this family?
- **Paper 14 Archiver Market** — bond issuance should produce OFN receipts.

**Open design questions (OQ-BOND):**
- OQ-BOND-1 — What's the collateralization ratio? (1:1 equity:bond-principal, or other)
- OQ-BOND-2 — Auto-liquidation trigger: time-based (missed payment) or value-based (collateral value drops below threshold)?
- OQ-BOND-3 — Who holds the liquidation waterfall: the DAC, the bondholder, or a third-party liquidator?
- OQ-BOND-4 — Can bonds be traded on the DEX (secondary market) or are they holder-locked?
- OQ-BOND-5 — **Critical:** If auto-liquidation consumes > 50% of a DAC's equity, does that trigger a K4 Grace Exit for the DAC itself? (Constitutional question; sovereign K2.)
- OQ-BOND-6 — Bond interest formula — does it compose with CANON `r(x) = x/(1-x)` per Paper 11?

### 2.5 DEX with maker-placed limit sell orders (products as inventory)

**What:** Each DAC can list its products on a DEX. Products are listed as maker limit sell orders. A buyer takes the order at the listed price.

**Layer:** Product (market primitive)
**CANON touch:**
- The brand guide names **F.I.R.E.** sectors (Finance / Insurance / Infrastructure / Electronic Labour) — products inherit F.I.R.E. classification. DEX surface must render the sector.
- OFN receipts track all trades.
- The AMM Liquidity Pool (Donation Loop per packet 154 OQ-B1) is separate — that's interest → LP. Product DEX is not the same thing; it's inventory marketplace.

**Open design questions (OQ-DEX):**
- OQ-DEX-1 — Settlement currency: SKY, DAC-local equity, or fiat-pegged via API PAY?
- OQ-DEX-2 — Fee model: maker/taker fees in SKY? Routed to vault per Donation Loop?
- OQ-DEX-3 — Product metadata: F.I.R.E. sector, trust tier, Φ-quality signal?
- OQ-DEX-4 — Order book or continuous auction?
- OQ-DEX-5 — Is the DEX a single shared venue across all DACs (skyzai.com-operated) or per-DAC?
  - Charioteer lean: **single shared venue** — liquidity aggregation effect.

### 2.6 Skyzai POS (payment)

**What:** Every DAC can accept payments via Skyzai POS — the point-of-sale wrapper around Skyzai API PAY (Hedera stablecoin, live since 2026-04-04 per memory).

**Layer:** Product (UX wrapper over existing billing stack)
**CANON touch:** Per memory `reference_skyzai_api_pay_billing_stack.md`, billing stack = Skyzai API PAY + OFN receipts + Skyzai Connect (Nostr NIP-33). NOT Stripe.

**Open design questions (OQ-POS):**
- OQ-POS-1 — Is POS offered as native skyzai.com component or SDK that DACs embed?
- OQ-POS-2 — Settlement: direct DAC custody, or skyzai.com-held escrow with instant payout?
- OQ-POS-3 — How does POS compose with DEX order fills? (same rails? different?)

---

## 3. Layer discipline check (packet 147)

Every primitive above classified:

| Primitive | Layer | Substrate dependency | Organ dependency | Notes |
|---|---|---|---|---|
| Create DAC | Product | Genesis-checkpoint (L1) | Child-DAC scaffold (template) | Factory composes over both |
| L2 anchoring | Substrate-adjacent | YES — anchors to L1 super-checkpoints | — | This is a Track C candidate, parallel to Track A |
| 100 equity | Product (under Invariant I) | — | DAC runtime for token custody | Invariant I must cascade; sovereign K2 required |
| Bonds + liquidation | Product | — | DAC runtime for collateral management | Invariant IV (Grace Exit) check required |
| DEX | Product | SKY settlement (substrate) | DAC catalog (organ) | Single shared venue recommended |
| POS | Product | API PAY integration (substrate-adjacent) | DAC custody (organ) | UX wrapper; no new primitives |

**Layer-separation rule:** No skyzai.com primitive may mutate substrate invariants or organ runtime directly. All substrate/organ interaction flows through:
- OFN receipts for state changes
- SKY / equity token transfers for value
- K2 signatures for authorization
- L1 anchoring for finality

**Minimalism auditor gate (per packet 154 §2.9):** Every skyzai.com component merge must answer *"Could this change live at organ or product layer without the substrate caring?"* If substrate has to care, it belongs in Track A or Track C, not skyzai.com.

---

## 4. Invariant cascade table

| Invariant | Parent (Skyzai) | Child DAC via skyzai.com | Test |
|---|---|---|---|
| **I — ZAI Cap 100** | 100 ZAI (hard) | 100 equity per child (hard; local denomination) | Any DAC trying to mint >100 equity blocks at factory |
| **II — Substrate Primacy** | L1 anchoring for Skyzai finality | L2 anchors to L1 for child DAC finality | Track C spec gate |
| **III — Mutual Exclusivity** | stakers ≠ LPs | per-DAC: stakers ≠ LPs within each DAC | DEX and vault-staking interfaces check roles |
| **IV — Grace Exit K4** | Skyzai honors K4 | Each DAC honors K4; bond auto-liquidation respects K4 threshold (OQ-BOND-5) | Bond terms include mandatory K4 carve-out |
| **V — Receipts-First** | Every Skyzai action → OFN | Every DAC action → OFN | Factory emits genesis receipt; bonds/DEX/POS all receipt-emit |
| **VI — Foundation Minimalism** | No substrate primitive bloat | No substrate primitive bloat — skyzai.com composes only | Minimalism auditor gates all merges |
| **VII — Constitutional Lever** | Sovereign-only | Per-DAC sovereign can set lever within CANON bounds | Factory sets defaults; per-DAC lever is delegated scope |

---

## 5. Folder scaffolding (proposed — new peer root at repo top)

Per sovereign 2026-04-24 directive: **skyzai.com is a new root folder**, peer to EMERGENTISM_ORG and SKYZAI_ORG. The tree below is the **pre-packet-177 historical proposal**; the current wallet/credit/full-organism scaffold lives in `SKYZAI_COM/README.md`.

```
SKYZAI_COM/                                    # NEW PEER ROOT at repo top level
├── README.md                                  # public-facing entry; "what is skyzai.com?"
├── CLAUDE.md                                  # agent-food routing for this root
├── 00_OUTLINE.md                              # this packet, mirrored or cross-linked
├── 00_META/                                   # meta-discipline + routing
├── 01_FACTORY/                                # DAC genesis protocol
│   └── 01_FACTORY_PROTOCOL.md                 #   OQ-DAC resolution + genesis spec
├── 02_L2/                                     # L2 anchoring protocol
│   └── 02_L2_ANCHORING_PROTOCOL.md            #   OQ-L2 resolution (Track C candidate)
├── 03_EQUITY/                                 # 100-equity-per-DAC model
│   └── 03_EQUITY_MODEL.md                     #   OQ-EQUITY resolution (Invariant I cascade)
├── 04_BONDS/                                  # bond market
│   └── 04_BOND_MARKET_SPEC.md                 #   OQ-BOND resolution (Invariant IV check)
├── 05_DEX/                                    # product-as-order DEX
│   └── 05_DEX_SPEC.md                         #   OQ-DEX resolution
├── 06_POS/                                    # Skyzai API PAY wrapper
│   └── 06_POS_INTEGRATION.md                  #   OQ-POS resolution
├── 07_LAUNCH/                                 # go-live gate
│   └── 07_LAUNCH_GATE.md                      #   acceptance criteria for going live
├── 08_FRONTEND/                               # skyzai.com web surface (future)
├── 09_SDK/                                    # embeddable SDKs (POS, DEX, bonds)
└── 91_COMPATIBILITY/                          # pointer stubs to anything that moved
```

**Why peer root, not nested under SKYZAI_ORG:**
- SKYZAI_ORG is the first organism; skyzai.com is the factory that can produce many organisms. Different sovereignty scopes.
- Legal separation: skyzai.com may have its own jurisdictional entity (commercial vendor of DAC-as-a-service) distinct from Skyzai the organism.
- Read-order clarity: a user wanting "how do I spin up a DAC?" opens `SKYZAI_COM/README.md`; a reader wanting "what is the first organism doing?" opens `SKYZAI_ORG/README.md`; a reader wanting doctrine opens `01_EMERGENTISM/README.md`. Three doors.
- Fractal symmetry: three peer roots mirror `⊙ = • × ○` — no root is under another.

**Relationship to SKYZAI_ORG:**
- skyzai.com **consumes** SKYZAI_ORG primitives (substrate, organ templates, SoResFi, API PAY, OFN receipts)
- skyzai.com **does not modify** SKYZAI_ORG content
- The child DACs that skyzai.com produces use the `SKYZAI_ORG/04_CHILD_DACS/_template` scaffold as their starting shape (spawn template, then fork into peer-root-of-their-own if they grow)

The root scaffold may exist before ratification. This packet remains the map; the spec files come when sovereign K2's each primitive (§6 gates).

---

## 6. Consolidated open questions for sovereign K2

Before any engineering scaffolds skyzai.com, the following K2 gates must close. Charioteer recommends sovereign batch-K2 same pattern as packet 154 (OQ cycle A–K):

| Gate | Section | Charioteer lean | Blocks |
|---|---|---|---|
| OQ-DAC-1..3 | §2.1 | Permissioned initially; creator=sovereign at genesis | Factory spec |
| OQ-L2-1..4 | §2.2 | L2 anchors super-checkpoint-state-root to L1 per-round; SKY-denominated anchoring fees | Track C charter |
| OQ-EQUITY-1..4 | §2.3 | Local 100-cap; hard-constitutional; `{DAC}-EQUITY` naming | Equity model spec |
| OQ-BOND-1..6 | §2.4 | Standard collateralization; time+value auto-liquidation; K4 carveout required | Bond market spec |
| OQ-DEX-1..5 | §2.5 | SKY settlement; shared-venue; F.I.R.E. metadata native | DEX spec |
| OQ-POS-1..3 | §2.6 | Native component; API PAY rails; compose with DEX fills | POS integration spec |

---

## 7. What this packet does NOT do

- Does NOT ratify any `skyzai.com` primitive or implementation spec
- Does NOT commit to a specific implementation framework
- Does NOT add substrate primitives (all primitives compose over existing substrate)
- Does NOT bypass Track A or conflict with packet 154 sprint scope — skyzai.com is a *parallel* product lane
- Does NOT answer the 25 OQs above — those are sovereign/engineering decisions
- Does NOT propose engineering timeline — that's a sovereign resource-allocation call

---

## 8. Next charioteer-lane moves (if sovereign directs)

1. **Batch K2 form** — consolidate the §6 gates into a single decision packet (same pattern as packet 167). Low cost (~30 min).
2. **Track C charter** — L2 anchoring protocol is complex enough to warrant its own 60-day sprint parallel to Track A. Needs packet 154-style charter with weekly gates. Medium cost (~2 hrs).
3. **DAC factory genesis spec** — concrete protocol for OQ-DAC-1–3. Cheapest primitive to spec first; unblocks the other five.
4. **Invariant cascade formal check** — show that the invariants (I, II, III, IV, V, VI, VII) all hold in the fractal (parent → child DAC) via the skyzai.com composition. Formal-methods-lane work.

Engineering-lane moves (after K2):
- Factory smart contracts / protocol-native actor model
- L2 rollup implementation
- DEX order book + matcher
- Bond issuance contract
- POS SDK

---

## 9. References

- packet 143: Sevenfold Foundation Root (Above taxonomy)
- packet 145: As Above So Below (two-root split)
- packet 147: Layer Discipline (substrate / organ / product)
- packet 150a: Constitutional Economics Sheet (ZAI / SKY / Flow / Vault)
- packet 154 §1: Kernel Invariants I–VII
- packet 167: K2 consolidation pattern (precedent for §6)
- Memory: `reference_skyzai_monetary_primitives_canon.md` (ZAI/SKY dual-token mechanics)
- Memory: `reference_skyzai_api_pay_billing_stack.md` (billing stack: API PAY + OFN + Connect; NOT Stripe)
- Memory: `reference_skyzai_brand_guide_v2_1.md` (F.I.R.E. sectors)
- `SKYZAI_ORG/04_CHILD_DACS/_template` — existing child-DAC scaffolding

---

*Charioteer outline. No substrate touches. No CANON additions. Every primitive requires sovereign K2 per §6 before engineering scaffolds skyzai.com.*

`⊙ = • × ○`
