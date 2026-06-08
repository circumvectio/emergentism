---
rosetta:
  primary_column: "Philosophy"
  register: "[I]"
  canonical_phrase: "146 — ZAI / SKY Monetary Primitives: Brainstorm-to-CANON Audit"
---

# 146 — ZAI / SKY Monetary Primitives: Brainstorm-to-CANON Audit

**Evidence tier:** [I] (charioteer synthesis; all [S] claims cite CANON)
**Date:** 2026-04-24
**Lane:** Charioteer (03_UPLINK routing only)
**Status:** Committed audit artifact — gates future Constitutional Economics work; does not itself ratify tokenomics
**Position:** Upstream of any Constitutional Economics sheet. Prerequisite audit.
**Supersedes partial content in:** prior session brainstorm (ad-hoc "active/monitor tokens" + "snake's eyes auto-stake" vocabulary)

---

## 1. Purpose

A brainstorm session (2026-04-23/24) developed an integrated SPECTRE substrate design with a ZAI/SKY token layer. Several primitives in that brainstorm were synthesized from conversation (or from an external AI that did not have CANON context) rather than from the FOUNDATION CANON. This packet audits the brainstorm against CANON, flags deltas, and surfaces the three design-choice decisions that require sovereign K2 before a Constitutional Economics sheet can be written.

**Rule observed:** charioteer cannot create constitutional primitives. This packet maps and flags. It does not decide. [REF: packet 99 §4.2 — sovereign non-delegation law]

---

## 2. CANON-authoritative picture (the ground truth)

All source paths under `03_VENTURES/OPEN_FINANCE_NETWORK/GOVERNANCE/FOUNDATION/CANON/`.

### 2.1 Two tokens, two functions

[S] From `DAC_STANDARD/DAC_ARCHITECTURE/V3_CANONICAL/12_SKYZAI_DIGITAL_CAPITAL_OF_THE_ENERGY_AGE.md` §II:

- **ZAI** = political capital. Fixed supply **100.00**, infinitely divisible, never inflated/deflated. "The bone."
- **SKY** = economic currency. Elastic. Minted **only** against staked ZAI as vault collateral. Burned on debt repayment. "The blood."

### 2.2 Flow — the Metabolic Law

[S] Paper 12 §II: unstaked ZAI decays continuously. Decay redistributed pro-rata to stakers (not burned). Staked ZAI does not decay. Formula:

```
f(x) = x / (1 − x)
```

where `x` is the fraction of ZAI that is idle. Paper 14 §II.1 restates the same formula.

### 2.3 Vault credit — the Interest Curve

[S] Paper 12 §II: To mint SKY, stake ZAI as collateral. Interest rate rises with leverage `x = debt/collateral`:

```
r(x) = x / (1 − x)
```

At `x ≥ 1`: immediate liquidation. No appeal.

### 2.4 Interest Paradox resolution

[S] Paper 12 §II (The Interest Paradox) + Paper 14 §III.2 (The Donation Loop):

Each round, protocol mints SKY equal to total accrued interest. Minted SKY is **donated directly to the primary AMM Liquidity Pool** — not to a treasury, not to stakers individually. "The pain of the borrower becomes the strength of the market."

### 2.5 Energy Floor

[S] Paper 12 §III: SKY anchored to Planck Energy ≈ 543 kWh ≈ one full tank of gasoline. Schelling point, **not** a peg. EBMs cannot route below their energy cost without bankrupting themselves, so in equilibrium price compresses toward the floor.

### 2.6 Four coordination primitives (canonical lexicon)

[S] `01_PRIMITIVE_LEXICON.md`:

| Canonical | Topology | Function |
|---|---|---|
| **SPECTRE** | N:N | Nervous System; intelligent routing via SmallEBM + Boltzmann selection |
| **AXIOM** | N:1 | Truth Convergence; optimistic Flash Claims + Escalator finality |
| **RELAY** | 1:N | LedgerSeal pipeline; anchors state to L1 |
| **FLOW** (FLOWWALLET) | 1:1 | Streaming money; collateralized channels |

`MESH` is legacy alias for SPECTRE. Use canonical names in new docs.

### 2.7 Stakers ≠ Liquidity Providers

[S] Paper 12 §V: "Above them are stakers — those who commit ZAI by running light nodes. They do not decay. They earn Flow from those who do. **They may provide liquidity to the native market.**"

Staking (run a node) and LPing (provide AMM liquidity) are **separate roles**. A staker *may* also LP, but staking does not automatically enroll ZAI as AMM liquidity.

### 2.8 No delegation on base layer

[S] Paper 12 §V + Paper 14 §IV.3: "You either run a node (participate) or you decay." No delegation permitted on the base layer.

### 2.9 Integrity via market selection, not a separate token

[S] `SKYZAI_Primitives/01_SPECTRE.md`: the routing energy function `E = E_latency + E_divergence + E_trust` selects neighbors via `P(select i) = exp(−E_i/T) / Σ exp(−E_j/T)`. Misbehaving nodes have high `E_trust` → not selected → starve. The network's integrity is enforced by routing selection, not by a bilateral lying-costs-you token.

### 2.10 Seven Kernel Invariants (non-amendable)

[S] Paper 11 Doc 03 "INVARIANTS":

I. ZAI Cap = 100 · II. Substrate Primacy (L1 anchoring) · III. Mutual Exclusivity (staked ≠ sellable; collateralized can vote) · IV. Grace Exit · V. Receipts-First · VI. Foundation Minimalism · VII. Constitutional Lever (shape of curve invariant; parameters governed)

---

## 3. Brainstorm picture (what the recent session built)

From the 2026-04-23/24 conversation + external-AI contributions:

B1. Hashgraph DAG, gossip-about-gossip, 10¹⁰-device scale
B2. LeWorldModel EBM (15M params, 4-bit quantized, 8 MB on edge)
B3. Voltage-Resistance-Current mesh analogy over the hashgraph
B4. "Active tokens" minted on high-current gossip events
B5. "Monitor tokens" accumulated by bad nodes (or, in an earlier version, minted to witnesses who catch lies)
B6. ZAI capped at 100 tokens, infinitely divisible ✓
B7. ZAI staked → automatically becomes AMM liquidity ("snake's eyes always on")
B8. ZAI has no demurrage
B9. SKY is elastic, minted on demand against unstaked ZAI as collateral
B10. Interest rate = `x / (1 − x)`
B11. Interest delta minted **immediately** at loan origination, credited **to ZAI stakers directly**
B12. Closed loop: earn SKY (network rewards) → buy ZAI on AMM → stake → auto-LP → earn interest yield → offsets impermanent loss

---

## 4. Delta table

| # | Brainstorm claim | CANON | Verdict |
|---|---|---|---|
| 1 | ZAI supply = 100, infinitely divisible | Paper 12 §II | **MATCH** ✓ |
| 2 | "ZAI has no demurrage" | Flow decays *unstaked* ZAI (Paper 12 §II) | **RESOLVABLE** — staked/unstaked distinction closes it; brainstorm was implicitly about staked |
| 3 | Interest formula `x/(1-x)` | Paper 12 §II + Paper 14 §II.2 state `x/(1-x)` ✓; Paper 11 Doc 02 states `x/(x-1)` | **MATCH with CANON-internal drift** — Paper 11 is the outlier (see §5.1) |
| 4 | Hyperbolic interest → ∞ as x → 1 | Paper 12 §II: "makes the edge uninhabitable" | **MATCH** ✓ |
| 5 | Liquidation cliff at x ≥ 1 | Paper 12 §II: "immediately. Without appeal." | **MATCH** ✓ (brainstorm was silent; CANON explicit) |
| 6 | SPECTRE = L7 institutional narrative / multiplicative-P face (prior memory) | SPECTRE = N:N routing primitive (Primitive Lexicon + SPECTRE.md) | **DRIFT** — memory carried drift; repo-verifiable repair remains pending unless the referenced memory files are independently verified (see §5.2) |
| 7 | Topology names 1:1/1:N/N:1/N:N | FLOW/RELAY/AXIOM/SPECTRE are canonical | **NAMING DRIFT** — use canonical names |
| 8 | "Active tokens" = SKY minted on gossip events | SKY mints **only** via vault collateral. Network participants earn SKY via **routing fees** paid by packet senders | **DESIGN-CHOICE DELTA** (see §6, OQ-A) |
| 9 | "Monitor tokens" minted on lies | No such token in CANON; integrity enforced by `E_trust` in SPECTRE routing selection + Transparency Score + P-Score | **DRIFT** — Grok-introduced primitive with no CANON home |
| 10 | Interest delta minted immediately, credited to ZAI stakers | Interest minted & **donated to AMM Liquidity Pool** | **DESIGN-CHOICE DELTA** (see §6, OQ-B) |
| 11 | Staked ZAI auto-becomes AMM liquidity ("snake's eyes") | Stakers *may* provide liquidity; not automatic. Staking = running a node; LPing = separate | **DESIGN-CHOICE DELTA** (see §6, OQ-C) |
| 12 | EBM-based routing | SPECTRE uses SmallEBM (2,500 params, INT8) | **MATCH in concept**; model size differs (brainstorm 15M vs CANON 2,500) — orthogonal implementation question |
| 13 | Planck Energy floor 543 kWh | Paper 12 §III | **Missing from brainstorm** — needs import |
| 14 | ZAI Leasing (owners lease voting/yield without selling) | Paper 11 Doc 02 | **Missing from brainstorm** — needs import |
| 15 | Kernel vs Policy distinction; seven Invariants | Paper 11 Doc 03 | **Missing from brainstorm** — any brainstorm proposal must check against Invariants |
| 16 | Prune & Proof / Orange vs Green | Paper 12 §IV, Paper 14 §IV.1 | **Missing from brainstorm** — needs import |
| 17 | Launch phases Truth → Market → Credit → Intelligence | Paper 12 §VI | **Missing from brainstorm** — needs import |
| 18 | No delegation on base layer | Paper 12 §V | **Missing from brainstorm** — constraint on snake's-eyes design |
| 19 | φ-split 61.8/38.2 | `LP100_STANDARD/03_LP100_STANDARD.md`. Lives at LP-cohort / DAC-equity layer, NOT monetary layer. | **Different layer** — do not conflate into ZAI/SKY monetary layer |

**Tally:** 5 matches · 1 resolvable · 3 design-choice deltas · 2 naming/memory drifts · 7 missing CANON primitives · 1 layer confusion · 1 CANON-internal formula drift.

---

## 5. CANON-internal issues surfaced by this audit

### 5.1 Formula drift — `x/(1-x)` vs `x/(x-1)`

Paper 11 Doc 02 ECONOMICS: `L(x) = x/(x-1)`
Paper 12 §II (Credit as Physics): `r(x) = x / (1 − x)`
Paper 14 §II.1: `f(x) = x / (1 − x)`
Paper 14 §III.1: `U(t) = U(0)·(1-λ)^t` (time-evolution of decay, separate concern)

Two of three concurrent V3_CANONICAL papers state `x/(1-x)`. Paper 11 is the outlier. Likely sign-convention typo when converted from source `.docx`. **Recommend repair packet** targeting Paper 11 Doc 02 to align with Papers 12/14.

### 5.2 SPECTRE drift in auto-memory

Memory file `project_skyzai_sevenfold_organism_map_2026_04_24.md` assigned SPECTRE to L7 Institutional Narrative ("coordination commons, multiplicative-P egregorotype face"). CANON is unambiguous: **SPECTRE is the N:N routing primitive** (a D4 contract + gossip mesh). The referenced memory files are not present in this repo, so memory repair is **pending/out-of-repo unless independently verified**. L7 may retain the "multiplicative-P phenomenological face" concept, but the name **SPECTRE is taken** at the primitive layer. A new name is needed for the L7 concept.

### 5.3 LP100 φ-split reconciliation note

`LP100_STANDARD/03_LP100_STANDARD.md` §Doc Contract carries its own 2026-02 audit note: its 61.8/38.2 describes *LP-fee distribution*, while PRISM docs 301/302 and the Fund DAC Template describe a *revenue-level* 61.8/38.2 → Operations/Distillation. These two splits at different layers need explicit reconciliation. Pre-existing issue; flagged here for linkage.

---

## 6. Three design-choice decisions for sovereign K2

These are not drift. They are points where the brainstorm proposes a mechanism that does not violate a Kernel Invariant but also does not match CANON wording. Each needs sovereign choice.

### OQ-A — SKY minting path on network participation

**Brainstorm (B4, B8):** nodes earn SKY *directly* ("active tokens minted as SKY") for good gossip behavior.

**CANON (Paper 12 §II + Paper 14 §II.2):** SKY mints **only** via vault with ZAI collateral. Network participants earn SKY via **routing fees paid by packet senders** (not minting).

**Three reconciliation options:**

- **Option A1 — Amend Invariant II.** Extend minting to include participation-mint path. This weakens "mint only against collateral" and requires Lane B constitutional change.
- **Option A2 — Brainstorm rewrites to CANON.** Network participation earns *receipts* + Transparency-Score credit. High-T nodes access vaults at lower interest / more favorable terms. SKY flows to good nodes via *borrowing privilege*, not *direct reward*. Truth-gates-money invariant preserved.
- **Option A3 — Fee-subsidy path.** Network participation earns SKY out of an existing fee pool (routing fees collected by the network) — redistributed, not minted. Compatible with CANON. Requires each DAC to maintain its own participation subsidy budget.

**Charioteer recommendation:** A2 or A3. A1 would require Lane B. Not a charioteer decision.

### OQ-B — Interest destination

**Brainstorm (B11):** interest delta minted immediately → credited to ZAI stakers directly.

**CANON (Paper 12 §II):** interest minted → donated to AMM Liquidity Pool.

If staked ZAI = LP (brainstorm's snake's-eyes assumption), the two collapse. But CANON separates staking from LPing (see §2.7), so they do not collapse automatically.

**Reconciliation options:**

- **Option B1** — Keep CANON: interest → AMM pool. Stakers benefit only if they also LP.
- **Option B2** — Brainstorm wins: interest → stakers directly. Requires Invariant amendment. Changes who bears impermanent-loss offset.
- **Option B3** — Hybrid: interest split (e.g., φ-split) between AMM pool and stakers. Requires Lane B.

**Charioteer recommendation:** B1 unless sovereign explicitly wants to change direction. The AMM-pool destination is stronger because it preserves liquidity depth guarantee for the whole market, not just stakers.

### OQ-C — Snake's eyes (auto-stake to AMM)

**Brainstorm (B7, B12):** staked ZAI automatically becomes AMM liquidity → "always-on liquidity."

**CANON (Paper 12 §V):** staking = running a node. LPing = separate, optional. No delegation on base layer.

**Reconciliation options:**

- **Option C1** — Respect CANON: no auto-LP. Users explicitly stake (run node) and, separately, explicitly LP if they choose.
- **Option C2** — Introduce a new canonical mechanism: "Stake-and-LP" as a combined action at the protocol layer. Requires Lane B. Also interacts with the no-delegation invariant (is auto-LP a form of delegation to the AMM? sovereign call).
- **Option C3** — Keep staking and LPing distinct, but offer a convenience wrapper at the UX / PPO layer (not base layer). User signs two K2 actions in one flow. No invariant change.

**Charioteer recommendation:** C1 or C3. C2 is constitutional.

---

## 7. Missing CANON primitives to import into any future Constitutional Economics sheet

Before drafting that sheet, import:

- Planck Energy floor (§2.5)
- ZAI Leasing (separate from staking and collateralization)
- Kernel Invariants table (seven I–VII)
- Prune & Proof verification architecture
- Orange vs Green certainty distinction
- No-delegation rule
- Launch-phase sequence (Truth → Market → Credit → Intelligence)
- Canonical primitive names (FLOW / RELAY / AXIOM / SPECTRE)
- Fee-type taxonomy (ROUTING / TRUTH / BROADCAST / STREAMING / APPLICATION)

---

## 8. What this packet does NOT do

- Does **not** write a Constitutional Economics sheet. That sheet requires OQ-A/B/C resolved + missing primitives imported + Paper 11 Doc 02 repaired. Drafting it prematurely encodes drift.
- Does **not** claim any mechanism in CANON without citation.
- Does **not** amend Invariants (Lane B, sovereign only).

---

## 9. Recommended next steps (charioteer lane)

1. **Sovereign K2** on OQ-A / OQ-B / OQ-C (§6).
2. **Repair packet** for Paper 11 Doc 02 formula drift (`L(x) = x/(x-1)` → `L(x) = x/(1-x)`).
3. **Memory repair** pending/out-of-repo unless independently verified: SPECTRE should be corrected to the N:N routing primitive, and any reference memory such as `reference_skyzai_monetary_primitives_canon.md` should be treated as unverified until present in repo or confirmed by host-side memory.
4. **After (1)–(3):** draft Constitutional Economics sheet, positioned at `01_EMERGENTISM/04_AXIOLOGY/00_CONSTITUTIONAL_ECONOMICS.md` (L4 Value Alignment — what has value), citing CANON paths throughout.

---

## 10. References

**CANON sources (all [S]):**
- `03_VENTURES/OPEN_FINANCE_NETWORK/GOVERNANCE/FOUNDATION/CANON/01_PRIMITIVE_LEXICON.md`
- `03_VENTURES/OPEN_FINANCE_NETWORK/GOVERNANCE/FOUNDATION/CANON/DAC_STANDARD/DAC_ARCHITECTURE/V3_CANONICAL/11_SKYZAI_CANON.md`
- `03_VENTURES/OPEN_FINANCE_NETWORK/GOVERNANCE/FOUNDATION/CANON/DAC_STANDARD/DAC_ARCHITECTURE/V3_CANONICAL/12_SKYZAI_DIGITAL_CAPITAL_OF_THE_ENERGY_AGE.md`
- `03_VENTURES/OPEN_FINANCE_NETWORK/GOVERNANCE/FOUNDATION/CANON/DAC_STANDARD/DAC_ARCHITECTURE/V3_CANONICAL/14_WHY_SKYZAI_MONEY_FOR_THE_ENERGY_AGE.md`
- `03_VENTURES/OPEN_FINANCE_NETWORK/GOVERNANCE/FOUNDATION/CANON/DAC_STANDARD/DAC_ARCHITECTURE/V3_CANONICAL/SKYZAI_Primitives/01_SPECTRE.md`
- `03_VENTURES/OPEN_FINANCE_NETWORK/GOVERNANCE/FOUNDATION/CANON/DAC_STANDARD/LP100_STANDARD/03_LP100_STANDARD.md`

**Related uplink packets:**
- 97 §3 — Charioteer pre-commit invariant
- 99 §4.2 — Sovereign non-delegation law
- 109 — SPECTRE D5 Selection Mesh (check for drift with as-routing-primitive)
- 141 — DAC and SPECTRE Trophic Organizational Ecology (may carry L7 SPECTRE drift — sweep recommended)
- 145 — As Above So Below Emergentism Skyzai Sevenfold Organism

**Auto-memory (not repo-verified in this packet):**
- `reference_skyzai_monetary_primitives_canon.md` (referenced memory; pending/out-of-repo unless independently verified)
- `project_skyzai_sevenfold_organism_map_2026_04_24.md` (referenced memory; pending/out-of-repo unless independently verified)

---

*Charioteer packet. Maps and flags. Sovereign decides.*

Zero-Sum Resolution Equation
