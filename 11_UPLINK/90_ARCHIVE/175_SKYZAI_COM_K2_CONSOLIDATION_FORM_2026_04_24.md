---
rosetta:
  primary_column: "Meta"
  register: "[I]"
  canonical_phrase: "175 — skyzai.com Sovereign K2 Consolidation Form"
---

# 175 — skyzai.com Sovereign K2 Consolidation Decision Form

**Evidence tier:** [I] charioteer-assembled form; [S] where citing packet 174 and CANON invariants; [C] where charioteer recommends a default
**Date:** 2026-04-24
**Lane:** Charioteer-assembled decision surface → **SOVEREIGN K2 fills the slots and signs**
**Status:** Historical consolidation form — superseded in part by packet 177; OQ-L2 family voided, bond family reframed as debtor-creditor
**Complements:** packet 167 (K2 consolidation pattern — precedent); packet 174 (skyzai.com outline — source of the 25 OQs); packet 154 §1 (batch-K2 precedent: OQ-A through OQ-K)

---

## Correction Note — Packet 177

Packet 177 voids the OQ-L2 family in this decision form. `SKYZAI_COM/` no longer drafts toward an EVM, rollup, L2 anchoring, state-root, or finality-window model. The active scaffold is `02_WALLET/` for the three-wallet multisig event envelope and `04_CREDIT/` for SoResFi debtor-creditor relations. OQ-DAC-3 is reframed as the first key in a multisig Business wallet, and the OQ-BOND family is reframed as one debtor-creditor specialization. This packet is preserved as historical K2 context, not as the active spec map.

## 0. Apophatic guard

This packet bundles 25 open questions into one review surface for sovereign batch sign. Partial signature is valid — any unsigned OQ stays open per packet 174. The value is saving sovereign time + surfacing the full design-space before engineering commits. The risk is rubber-stamping — if any default below feels wrong, leave its slot empty and the OQ stays open.

**No substrate primitives. No CANON additions. All 25 OQs live at product layer.** The invariant cascade (packet 174 §4) must hold after sovereign sign-off; charioteer flags any answer that would break it.

`⊙ = • × ○`

---

## 1. Why consolidate

Packet 174 outlined the skyzai.com DAC machine with six primitive families. Each family contains 3–6 open design questions. Without batch K2, engineering can only maintain a root scaffold; per-primitive spec files (01_FACTORY/, 02_L2/, 03_EQUITY/, 04_BONDS/, 05_DEX/, 06_POS/) each depend on an OQ-resolution.

Batch K2 pattern precedent: packet 154 §1 closed OQ-A through OQ-K in a single sovereign directive. Same pattern here.

**Gates summary:**

| Family | OQs | Charioteer lean | Blocks until signed |
|---|---|---|---|
| **DAC factory** | 3 | Permissioned initially; creator=sovereign at genesis | 01_FACTORY/ spec |
| **L2 anchoring** | 4 | Super-checkpoint-state-root per round; SKY-denominated fees | 02_L2/ spec + Track C charter |
| **Equity model** | 4 | Local 100-cap hard-constitutional; `{DAC}-EQUITY` naming | 03_EQUITY/ spec |
| **Bond market** | 6 | Standard collateralization; K4 carve-out mandatory | 04_BONDS/ spec |
| **DEX** | 5 | SKY settlement; shared-venue; F.I.R.E. metadata | 05_DEX/ spec |
| **POS** | 3 | Native component; API PAY rails; composes with DEX | 06_POS/ spec |

**Total:** 25 OQs. Invariant risk: OQ-EQUITY-1/2 (Invariant I cascade) and OQ-BOND-5 (Invariant IV Grace Exit) are the two constitutional-level decisions. The other 23 are product-parameter choices.

---

## 2. DAC Factory gate (§2.1 of packet 174)

**Source:** packet 174 §2.1
**Blocks:** `SKYZAI_COM/01_FACTORY/01_FACTORY_PROTOCOL.md`

### OQ-DAC-1 — Minimum genesis payload

☐ A — Name + founder K2 pubkey only (minimum viable)
☐ B — Name + founder K2 pubkey + sector (F.I.R.E.) + jurisdiction (*charioteer lean*)
☐ C — Full schema: name + founder + sector + jurisdiction + equity allocation plan + initial product catalog

**Reason for B lean:** sector + jurisdiction are downstream-required for DEX listing and POS integration; baking them in at genesis avoids late-stage migration. Full C is over-configuration for a v0 factory.

### OQ-DAC-2 — Creation gating

☐ A — Permissionless (anyone creates)
☐ B — Permissioned initially (sovereign/admin approval gate) (*charioteer lean*)
☐ C — Fee-gated (SKY payment to parent vault)

**Reason for B lean:** first 100 DACs benefit from human review to catch edge cases; flip to permissionless once the factory protocol is battle-tested.

### OQ-DAC-3 — Creator-to-sovereign relationship

☐ A — Creator becomes DAC sovereign at genesis (single-seat genesis K2) (*charioteer lean*)
☐ B — Creator proposes sovereign separately (two-step)
☐ C — Multi-sig sovereign from genesis (N-of-M K2 holders)

**Reason for A lean:** simplest genesis; creators can delegate/transition to multi-sig post-genesis via normal DAC governance. A two-step setup adds friction to first-DAC creation.

---

## 3. L2 Anchoring gate (§2.2 of packet 174)

**Source:** packet 174 §2.2
**Blocks:** `SKYZAI_COM/02_L2/02_L2_ANCHORING_PROTOCOL.md` + Track C charter
**Critical disambiguation:** "L2" here = network topology (rollup-style), NOT Rosetta L1–L7 ontological levels. Spec must use `rollup-L2` vs `ontological-L2` throughout.

### OQ-L2-1 — What rolls up to L1

☐ A — Just state root hash (minimal)
☐ B — State root hash + super-checkpoint lineage (*charioteer lean*)
☐ C — State root + lineage + full Proof Bundles

**Reason for B lean:** Paper 12 §IV commitment-without-burden pattern — validators commit, they do not store. Lineage is the load-bearing continuity; Proof Bundles go to archivers per Paper 14, not to L1.

### OQ-L2-2 — Anchoring cadence

☐ A — Per-event (every DAC event anchored)
☐ B — Per-round (each substrate round anchors all DACs' state) (*charioteer lean*)
☐ C — Per-window (batched every N rounds)

**Reason for B lean:** matches substrate super-checkpoint cadence from Track A spec — clean composition, no new timing primitive.

### OQ-L2-3 — L2 downtime behavior

☐ A — L2 down → all DAC operations halt
☐ B — L2 down → DAC operations continue locally; finality deferred until L2 recovers (*charioteer lean*)
☐ C — L2 down → Fallback Mode (per Track A W2 D2.2) with degraded finality

**Reason for B lean:** local-write + eventual-finality is standard rollup pattern; preserves DAC UX under substrate blips.

### OQ-L2-4 — Anchoring fee denomination

☐ A — SKY (parent substrate token) (*charioteer lean*)
☐ B — DAC-local equity
☐ C — Parent ZAI
☐ D — USD via API PAY

**Reason for A lean:** SKY is the elastic economic token per packet 150a; matches Paper 14 archiver economics pattern. ZAI (A) is politically-capped and shouldn't be spent on fees; DAC-local equity (B) would couple anchoring cost to local governance.

---

## 4. Equity Model gate (§2.3 of packet 174) — **CONSTITUTIONAL**

**Source:** packet 174 §2.3
**Blocks:** `SKYZAI_COM/03_EQUITY/03_EQUITY_MODEL.md`
**Constitutional weight:** OQ-EQUITY-1 and OQ-EQUITY-2 cascade Invariant I (ZAI Cap 100). Sovereign scrutiny especially important.

### OQ-EQUITY-1 — Relationship to parent ZAI

☐ A — Independent local supply: each DAC gets its own 100-token cap (*charioteer lean*)
☐ B — Fractional: each DAC's equity is a carved-out fraction of parent ZAI
☐ C — Hybrid: DAC has 100-token local supply AND reports to parent as ZAI-fraction

**Reason for A lean:** preserves the fractal — each DAC is its own organism with its own 100-cap; parent ZAI stays at 100 ZAI total. B would deplete parent ZAI supply as children grow (incompatible with Invariant I's hard cap); C doubles the accounting burden.

### OQ-EQUITY-2 — Hard-constitutional vs re-parameterizable

☐ A — Hard-constitutional: 100 cap is absolute per DAC (*charioteer lean*)
☐ B — Default 100; per-DAC sovereign can re-parameterize at genesis
☐ C — No cap at all (let market decide)

**Reason for A lean:** preserves Invariant I cascade across fractal depth. B would fragment the invariant ("what is ZAI Cap 100?"); C removes the invariant entirely.

### OQ-EQUITY-3 — Subdivision allowed?

☐ A — Yes for fractional holdings; no for supply inflation (*charioteer lean*)
☐ B — No subdivision (whole tokens only)
☐ C — Full subdivision including supply expansion

**Reason for A lean:** fractional holdings are standard equity practice (vesting, options). Supply inflation violates the 100-cap.

### OQ-EQUITY-4 — Naming convention

☐ A — `{DAC}-EQUITY` (e.g. `Agentz-EQUITY`) (*charioteer lean*)
☐ B — `{DAC}-ZAI` (inherits parent naming)
☐ C — `{DAC}-SHARE`

**Reason for A lean:** disambiguates child equity from parent ZAI in wallets, explorers, and receipts. ZAI name stays reserved for parent.

---

## 5. Bond Market gate (§2.4 of packet 174) — **CONSTITUTIONAL**

**Source:** packet 174 §2.4
**Blocks:** `SKYZAI_COM/04_BONDS/04_BOND_MARKET_SPEC.md`
**Constitutional weight:** OQ-BOND-5 tests Invariant IV (Grace Exit K4). Sovereign must scrutinize.

### OQ-BOND-1 — Collateralization ratio

☐ A — 1:1 (equity:principal)
☐ B — Over-collateralized; 1.5:1 default, per-bond negotiable (*charioteer lean*)
☐ C — Under-collateralized allowed with higher interest

**Reason for B lean:** 1.5:1 buffer absorbs price swings; protects bondholder without over-burdening issuer.

### OQ-BOND-2 — Auto-liquidation trigger

☐ A — Time-based only (missed payment → liquidate)
☐ B — Value-based only (collateral drops below threshold → liquidate)
☐ C — Both (trigger on either condition) (*charioteer lean*)

**Reason for C lean:** time trigger protects interest-stream integrity; value trigger protects principal. Both together = canonical bond-market pattern.

### OQ-BOND-3 — Liquidation waterfall holder

☐ A — DAC itself executes
☐ B — Bondholder initiates, DEX handles (*charioteer lean*)
☐ C — Third-party liquidator market

**Reason for B lean:** bondholder has motivation to execute; DEX handles the mechanics; no new liquidator-entity primitive needed. C would add an unnecessary role.

### OQ-BOND-4 — Secondary market tradability

☐ A — Bonds holder-locked (no secondary market)
☐ B — Bonds tradable on same shared DEX (*charioteer lean*)
☐ C — Bonds tradable on separate bond-venue

**Reason for B lean:** uses existing DEX infrastructure; no new venue needed. Standard fixed-income pattern.

### OQ-BOND-5 — K4 threshold trigger — **INVARIANT-IV CRITICAL**

*If auto-liquidation consumes > X% of a DAC's equity, does that trigger K4 Grace Exit for the DAC itself?*

☐ A — No — DAC continues with whatever equity remains after liquidation
☐ B — Yes at 50% — if liquidation consumes ≥ 50% equity, mandatory K4 offer to all DAC members (*charioteer lean*)
☐ C — Yes at 33% — more conservative threshold
☐ D — Per-DAC sovereign sets threshold at genesis

**Reason for B lean:** 50% equity-loss means effective loss of DAC autonomy. Invariant IV (K4: leave with everything, organism retains nothing) requires that members be offered an exit BEFORE the organism is reduced to a husk. B is the honest middle. A is too laissez-faire (could trap members); C may trigger K4 on routine bond defaults; D fragments the invariant.

**Sovereign scrutiny:** this is the single highest-risk K2 in the packet. Flag if uncertain.

### OQ-BOND-6 — Interest formula

☐ A — Canonical `r(x) = x/(1-x)` per Paper 11 (*charioteer lean*)
☐ B — Simple interest (flat rate)
☐ C — Per-bond negotiable (issuer + bondholder bilateral)

**Reason for A lean:** CANON-consistent; same formula as vault interest; no new primitive. B is a simplification that loses the CANON mathematical structure. C fragments the formula across the bond market.

---

## 6. DEX gate (§2.5 of packet 174)

**Source:** packet 174 §2.5
**Blocks:** `SKYZAI_COM/05_DEX/05_DEX_SPEC.md`

### OQ-DEX-1 — Settlement currency

☐ A — SKY only (*charioteer lean*)
☐ B — SKY + fiat via API PAY (dual-rail)
☐ C — DAC-local equity (each DAC settles in its own token)

**Reason for A lean:** SKY is the substrate economic token; consistent across all DACs; simplest matching engine.

### OQ-DEX-2 — Fee model

☐ A — Maker-zero, taker-fee (standard CEX pattern)
☐ B — Symmetric maker + taker fees routed to Donation Loop AMM Pool (*charioteer lean*)
☐ C — No fees (pure protocol)

**Reason for B lean:** matches packet 154 OQ-B1 Donation Loop destination (interest → AMM pool). Symmetric fees avoid adverse selection; donation routing keeps the substrate economic flywheel.

### OQ-DEX-3 — Product metadata

☐ A — F.I.R.E. sector only
☐ B — F.I.R.E. sector + trust tier + Φ-quality signal (*charioteer lean*)
☐ C — Minimal (no metadata beyond price/qty)

**Reason for B lean:** matches brand guide v2.1 (F.I.R.E. = identity). Trust tier lets buyers filter; Φ-signal surfaces coherence/quality. C is a UX impoverishment.

### OQ-DEX-4 — Matching mechanism

☐ A — Continuous order book (maker limit orders, taker fills) (*charioteer lean*)
☐ B — Periodic call auction
☐ C — AMM-style constant-product

**Reason for A lean:** sovereign sketched "maker limit sell orders" → order book is the native form. B adds latency; C requires liquidity pools per product (impractical for product inventory).

### OQ-DEX-5 — Venue structure

☐ A — Single shared venue (skyzai.com operates one DEX for all DACs) (*charioteer lean*)
☐ B — Per-DAC venue (each DAC runs its own DEX)
☐ C — Hybrid (shared venue + per-DAC optional)

**Reason for A lean:** liquidity aggregation. One venue = deepest book = best price discovery. B fragments liquidity.

---

## 7. POS gate (§2.6 of packet 174)

**Source:** packet 174 §2.6
**Blocks:** `SKYZAI_COM/06_POS/06_POS_INTEGRATION.md`

### OQ-POS-1 — Offering model

☐ A — Native skyzai.com-hosted component (*charioteer lean*)
☐ B — Embeddable SDK for DACs to self-host
☐ C — Both (A for simple DACs; B for advanced)

**Reason for A lean:** simplest v0. Upgrade to C once native is proven.

### OQ-POS-2 — Settlement mechanism

☐ A — Direct DAC custody (funds flow straight to DAC wallet)
☐ B — skyzai.com-held escrow with instant/daily payout (*charioteer lean*)
☐ C — Hybrid

**Reason for B lean:** enables dispute resolution window + chargeback handling; standard e-commerce pattern; doesn't violate sovereignty because DAC retains contractual right to payout.

### OQ-POS-3 — Composition with DEX fills

☐ A — Same settlement rails (DEX fill and POS payment both go through API PAY + OFN receipts) (*charioteer lean*)
☐ B — Different rails (DEX is crypto-native; POS is fiat-rail)
☐ C — Per-DAC configurable

**Reason for A lean:** one settlement pipeline = one receipt format = one audit surface. B fragments. C fragments per-DAC.

---

## 8. Consolidated K2 signature block

**Sovereign ratifies by filling slots below and signing.** Partial signature (leaving individual OQ slots empty) is valid — any unsigned OQ stays open per packet 174.

```
DAC Factory gate (§2):
  OQ-DAC-1 genesis payload:        ☐ A  ☐ B  ☐ C
  OQ-DAC-2 creation gating:        ☐ A  ☐ B  ☐ C
  OQ-DAC-3 creator-sovereign:      ☐ A  ☐ B  ☐ C

L2 Anchoring gate (§3):
  OQ-L2-1 rollup content:          ☐ A  ☐ B  ☐ C
  OQ-L2-2 anchoring cadence:       ☐ A  ☐ B  ☐ C
  OQ-L2-3 L2 downtime:             ☐ A  ☐ B  ☐ C
  OQ-L2-4 fee denomination:        ☐ A  ☐ B  ☐ C  ☐ D

Equity Model gate (§4) — CONSTITUTIONAL:
  OQ-EQUITY-1 parent-ZAI relation: ☐ A  ☐ B  ☐ C
  OQ-EQUITY-2 hard-constitutional: ☐ A  ☐ B  ☐ C
  OQ-EQUITY-3 subdivision:         ☐ A  ☐ B  ☐ C
  OQ-EQUITY-4 naming:              ☐ A  ☐ B  ☐ C

Bond Market gate (§5) — CONSTITUTIONAL (OQ-BOND-5):
  OQ-BOND-1 collateralization:     ☐ A  ☐ B  ☐ C
  OQ-BOND-2 liquidation trigger:   ☐ A  ☐ B  ☐ C
  OQ-BOND-3 waterfall holder:      ☐ A  ☐ B  ☐ C
  OQ-BOND-4 secondary market:      ☐ A  ☐ B  ☐ C
  OQ-BOND-5 K4 threshold:          ☐ A  ☐ B  ☐ C  ☐ D    ← INVARIANT-IV GATE
  OQ-BOND-6 interest formula:      ☐ A  ☐ B  ☐ C

DEX gate (§6):
  OQ-DEX-1 settlement currency:    ☐ A  ☐ B  ☐ C
  OQ-DEX-2 fee model:              ☐ A  ☐ B  ☐ C
  OQ-DEX-3 product metadata:       ☐ A  ☐ B  ☐ C
  OQ-DEX-4 matching mechanism:     ☐ A  ☐ B  ☐ C
  OQ-DEX-5 venue structure:        ☐ A  ☐ B  ☐ C

POS gate (§7):
  OQ-POS-1 offering model:         ☐ A  ☐ B  ☐ C
  OQ-POS-2 settlement mechanism:   ☐ A  ☐ B  ☐ C
  OQ-POS-3 DEX composition:        ☐ A  ☐ B  ☐ C

SOVEREIGN SIGNATURE: ________________________  DATE: __________
```

**Charioteer default signature (for reference — sovereign can accept all defaults with a single "ALL-B/A" mark, or diverge per OQ):**

```
DAC-1: B | DAC-2: B | DAC-3: A
L2-1:  B | L2-2:  B | L2-3:  B | L2-4: A
EQUITY-1: A | EQUITY-2: A | EQUITY-3: A | EQUITY-4: A
BOND-1:   B | BOND-2:   C | BOND-3:   B | BOND-4:   B | BOND-5: B  | BOND-6: A
DEX-1:    A | DEX-2:    B | DEX-3:    B | DEX-4:    A | DEX-5:    A
POS-1:    A | POS-2:    B | POS-3:    A
```

---

## 9. What happens after signature

If all 25 OQs signed (defaults or divergent):

| Gate closed | Unblocks | First engineering action |
|---|---|---|
| OQ-DAC-1..3 | Factory spec | Draft `SKYZAI_COM/01_FACTORY/01_FACTORY_PROTOCOL.md` |
| OQ-L2-1..4 | L2 anchoring + Track C charter | Draft `SKYZAI_COM/02_L2/02_L2_ANCHORING_PROTOCOL.md` + charter a 60-day Track C sprint |
| OQ-EQUITY-1..4 | Equity model spec | Draft `SKYZAI_COM/03_EQUITY/03_EQUITY_MODEL.md` with invariant-cascade formal check |
| OQ-BOND-1..6 | Bond market spec | Draft `SKYZAI_COM/04_BONDS/04_BOND_MARKET_SPEC.md` with K4 carve-out |
| OQ-DEX-1..5 | DEX spec | Draft `SKYZAI_COM/05_DEX/05_DEX_SPEC.md` |
| OQ-POS-1..3 | POS integration spec | Draft `SKYZAI_COM/06_POS/06_POS_INTEGRATION.md` |

If any OQ left unsigned:
- That primitive's spec cannot begin
- Related specs blocked transitively (e.g., DEX spec references settlement currency from OQ-DEX-1)
- Charioteer reports "still pending OQ-X" and stands down on that lane

**Pre-spec gate:** engineering may create a `SKYZAI_COM/` root scaffold with README-level routing only. It does NOT create primitive spec files until at least OQ-DAC-1..3 are signed (factory is the entry point for every other primitive). The other 22 OQs can be signed in any order.

---

## 10. What this packet does NOT do

- Does NOT execute any decision — all 25 OQs are sovereign-exclusive
- Does NOT create or ratify any `SKYZAI_COM/` primitive spec files (root scaffold may exist)
- Does NOT prescribe engineering timeline — sovereign resource-allocation call
- Does NOT bypass packet 99 §4.2 Sovereign Non-Delegation Law — all five non-delegable powers remain with sovereign; nothing here routable to warrior/charioteer
- Does NOT modify CANON — all 25 primitives compose over existing substrate + organ

---

## 11. References

- packet 174: skyzai.com DAC Machine Outline (source of all 25 OQs)
- packet 167: Sovereign K2 Consolidation Form (precedent pattern)
- packet 154 §1: OQ-A through OQ-K batch K2 (original precedent)
- packet 147: Layer Discipline (every primitive here is product layer)
- packet 99 §4.2: Sovereign Non-Delegation Law
- Memory: `reference_skyzai_monetary_primitives_canon.md` (ZAI/SKY mechanics)

---

*Charioteer-assembled consolidation form. Sovereign K2 fills slots; engineering drafts primitive specs after signature. README-level root scaffolding remains non-ratifying. Partial signature valid. Constitutional scrutiny requested on OQ-EQUITY-1/2 (Invariant I cascade) and OQ-BOND-5 (Invariant IV Grace Exit threshold).*

`⊙ = • × ○`
