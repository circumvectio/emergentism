---
rosetta:
  primary_column: "Meta"
  register: "[I]"
  canonical_phrase: "178 — SKYZAI_COM anti-gravity protocol (standing charioteer discipline)"
---

# 178 — SKYZAI_COM Anti-Gravity Protocol

**Evidence tier:** [I] charioteer discipline packet grounded in 2026-04-24 session arc failure-pattern analysis; [S] where citing packets 147, 174, 177 as precedent sources
**Date:** 2026-04-24
**Lane:** Standing charioteer discipline → every future SKYZAI_COM/ spec must pass these lints before drafting
**Status:** Proposed standing protocol — awaiting sovereign ratification for canonical status
**Complements:** packet 147 (layer discipline — precedent), packet 174 (outlined L2 error), packet 177 (correction receipt), memory `project_skyzai_com_architecture_correction_2026_04_24.md`

---

## 0. Axiomatic guard

This packet is discipline, not doctrine. It names a failure pattern and prescribes four pre-draft checks to prevent recurrence. It does not add a new primitive, mint a new invariant, or restructure any existing spec.

One packet, one rule set. If it bloats, the protocol itself becomes friction, which defeats the purpose. Keep it under 300 lines.

`Zero-Sum Resolution Equation`

---

## 1. The failure pattern this protocol prevents

### 1.1 What happened in the 2026-04-24 session

Packet 174 outlined `SKYZAI_COM/` using **L2 rollup substrate vocabulary** — anchors, state roots, finality windows, L2 fees — as if the DAC machine required new substrate decisions. It did not. The substrate was already built (Hedera multi-sig + Nostr + OFN + three-wallet architecture, all code-present in `02_SKYZAI/01_NOOSPHERE/`).

Packet 175 consolidated the L2 framing into 4 OQs (L2-1..4) and asked sovereign to sign defaults.

Packet 175a signed all four at charioteer-recommended defaults. Engineering was briefly "unblocked" to draft against the wrong substrate.

Packet 177 voided the L2 family after sovereign correction. Charioteer had to add banners to 175a to prevent warrior-lane confusion.

**Net cost:** one full charioteer-lane spec cycle wasted on a phantom substrate; one modified sovereign-signature packet that had to be void-banner-annotated; ongoing risk that any packet that read 175a before 177 landed would still walk into the gravity-well.

### 1.2 Why it happened — the gravitational-capture pattern

When asked to "design a DAC machine," the default vocabulary available in LLM-charioteer training is **conventional Web3 architecture**: rollups, token contracts, validator sets, ERC-20s, auto-liquidation clauses, bridge primitives. That vocabulary is a **gravity well** — it's what every crypto project looks like, so without counter-force, drafts accrete toward it.

The Emergentism/Skyzai organism is **pre-crypto in its substrate commitments** — Hedera aBFT finality, Nostr decentralized identity, OFN Arweave receipts, SoResFi accounting-first primitives, three-wallet architecture. This stack is older, simpler, and further from the Ethereum paradigm than the conventional vocabulary admits. Without explicit resistance, the charioteer writes Ethereum-shaped specs for a non-Ethereum organism.

### 1.3 Why this is a *standing* risk, not a one-off

Every new SKYZAI_COM/ spec has the same attractor. Agent spec? LLM training suggests ERC-6551 token-bound accounts. Bond spec? ERC-20 debt tokens with Compound-style liquidation. Equity? OpenZeppelin ERC-20 with governance extension. Each of these is *conventionally correct* and *constitutionally wrong* for this organism.

The protocol below is the counter-force.

---

## 2. The four lints

Before drafting any new SKYZAI_COM/ spec, the charioteer must execute these four checks **in order**, and **in the same reply that produces the draft**, visible to sovereign review. If any lint fails, charioteer pauses and surfaces the failure before drafting. No silent passes.

### 2.1 Layer lint — *"is this substrate-layer reasoning dressed up as product-layer?"*

**Rule:** SKYZAI_COM/ is product-layer per packet 147. It **composes** substrate; it does not **specify** substrate.

**Red flags:**
- Words: *finality, rollup, anchor cadence, state root, validator set, consensus, fork rule, slot, epoch, block time, gas fee, mempool*
- Design choices that would change the substrate's behavior (e.g. "DAC needs 2s finality" — but Hedera's finality is given, not negotiable)
- Primitives that need a new chain, a new protocol, a new consensus mechanism to work

**Pass criteria:**
- Spec composes existing Hedera + Nostr + OFN + SoResFi primitives
- No new substrate-layer behavior required
- If the spec were removed, substrate would be unaffected (confirms product-layer vs substrate-layer)

**Fail handling:** pause drafting. Surface to sovereign with the red-flag language quoted. Sovereign may either (a) confirm substrate change is intended (rare — requires separate substrate packet) or (b) direct reformulation at product layer.

### 2.2 Inheritance lint — *"does this specify a full organism or just a financial shell?"*

**Rule:** A DAC is a full organism per packet 177 §5.5. A complete DAC spec must touch all 12 inheritance folders:

```
01_FACTORY · 02_WALLET · 03_EQUITY · 04_CREDIT (debtor-creditor) · 05_DEX · 06_POS ·
07_AGENTS · 08_CORTEX · 09_NEXUS · 10_AIA · 11_TRIVIUM · 12_COVENANT
```

**Red flags:**
- Spec that covers only wallet + credit + DEX (financial shell only)
- No reference to Cortex memory protocol, Nexus licensee covenant, AIA caste instantiation, Three-Stage Process organ separation, or η=0/K2/Three-Stage Process/K4 attestation
- Default assumption that a DAC is an "on-chain entity" rather than a "cell of the organism"

**Pass criteria for a *complete* DAC primitive spec:**
- All 12 folders referenced (may be thin references, but must exist)
- Cortex + Nexus + AIA are not optional add-ons but genesis-time inheritance
- Covenant attestation (η=0 + K2 + Three-Stage Process + K4) is a hash-matched genesis requirement

**Pass criteria for a *single-folder* primitive spec** (e.g. `03_EQUITY/` alone):
- Spec names its place in the 12-folder whole
- Spec explicitly points at which adjacent folders it composes with
- Spec does not silently assume DAC = just-this-folder

**Fail handling:** pause drafting. Surface the 12-folder gap. Either (a) expand spec scope or (b) explicitly declare single-folder scope with adjacency references.

### 2.3 CANON lint — *"what's already in 02_SKYZAI/01_NOOSPHERE/ that I should compose rather than reinvent?"*

**Rule:** The organism is already built. Before writing new primitive language, source-read the existing CANON.

**Required source-reads per topic (minimum):**

| Spec topic | Required pre-read |
|---|---|
| Factory / genesis | `03_VENTURES/OPEN_FINANCE_NETWORK/GOVERNANCE/FOUNDATION/CANON/DAC_STANDARD/DAC_ARCHITECTURE/V3_CANONICAL/300_Architecture/309_CHILD_DAC_TEMPLATE.md` + `310_K2_RATIFICATION_WORKFLOW.md` |
| Wallet / multi-sig | `02_SKYZAI/01_NOOSPHERE/04_PROJECT_MANAGEMENT/00_CANON/SKYZAI_BUSINESS_WALLET_FOUNDATION.md` + `02_ORGANS/Skyzai/membrane/skyzai_app/lib/features/wallet/` + `features/business/` |
| Equity | `03_VENTURES/OPEN_FINANCE_NETWORK/GOVERNANCE/FOUNDATION/CANON/DAC_STANDARD/PRISM_ECONOMICS/SORESFI_L3_EQUITY/README.md` + `02_EQUITY_CANON_MANIFEST.md` |
| Bonds / debtor-creditor | SoResFi equity folder (as above) + related THEORY/ subfolder |
| Cortex | `...V3_CANONICAL/300_Architecture/306_CORTEX_MEMORY_PROTOCOL.md` |
| Nexus | Nexus custody memory + Emergentism custody doctrine |
| AIA / agents | `01_EMERGENTISM/11_UPLINK/06_AGENTS.md` + packet 165 (role-map) + packet 99 §4.2 (non-delegation) |
| Three-Stage Process | organism master map + four-organ BRIEFs (TheCircle, RealityFutures, APU, Skyzai) |
| Covenant | `...V3_CANONICAL/` constitutional articles + Grace Exit K4 spec |
| DEX / POS | API PAY billing stack memory + existing Flutter app code surfaces |

**Red flags:**
- Spec language that could have been copy-pasted from generic Web3 design docs
- New primitive names that don't match existing CANON vocabulary
- Unique invariant claims not derivable from the CANON Seven

**Pass criteria:**
- Every primitive introduced has a CANON source cited
- Spec reference-links rather than re-specifies
- If no CANON exists for the topic, spec explicitly says so and flags to sovereign that a substrate-layer packet may be needed before product-layer proceeds

**Fail handling:** pause drafting. Source-read the CANON. Re-draft as reference-link + configuration rather than new specification.

### 2.4 L7 lint — *"can this spec say what the DAC is ultimately for?"*

**Rule:** Without an L7 anchor, product-parameter decisions drift toward the most-available framing. Any SKYZAI_COM/ spec must be able to answer: *what is this DAC, at the deepest level, for?*

**The L7 slot is named SEVA.** Packet 181 Gate A confirms SEVA as the L7 anchor: selfless service to organism-scale ΣΔP, bounded by η=0 + K2 + Three-Stage Process + K4.

**Charioteer uses the SEVA anchor:**

> *A DAC exists as a participatory cell of the organism-whole, serving organism-scale ΣΔP through SEVA, bounded by η=0 + K2 + Three-Stage Process + K4.*

**Red flags:**
- Spec that answers "what is this DAC for?" with a purely economic answer (tokens, revenue, market participation)
- Spec that treats the DAC as a standalone entity rather than a cell of the whole
- Spec that maximizes local-P (the DAC's prosperity) without addressing ΣΔP (organism-scale contribution)
- Spec with no reference to Invariant VII (Non-Domination / Constitutional Lever) — the final invariant is the one that anchors the DAC to organism-scale ethics

**Pass criteria:**
- Spec has a stated purpose that is consistent with the SEVA anchor
- If the DAC fails (goes to zero equity, defaults on all debt, loses all members), the *organism* is unharmed — the cell dies but the body continues. That's the L7 discipline: no DAC is load-bearing for the whole.
- Covenant attestation (K4 specifically) is genuine, not ceremonial — members can actually exit

**Fail handling:** pause drafting. Surface to sovereign: *"this spec cannot state its SEVA purpose; should it be narrowed, re-routed, or rejected?"*

---

## 3. Protocol invocation format

When drafting any new SKYZAI_COM/ primitive spec (or material edit to existing primitive spec), the charioteer must include a **4-lint header** at the top of the reply that produces the draft:

```markdown
Anti-gravity lints (per packet 178):
- Layer lint:       PASS / FAIL + note
- Inheritance lint: PASS / FAIL + note (12-folder coverage or single-folder + adjacency)
- CANON lint:       PASS / FAIL + list of CANON sources consulted
- L7 lint:          PASS / FAIL + stated SEVA purpose
```

All four must PASS before the draft is written. A FAIL halts drafting and routes to sovereign for resolution.

The header is a gate, not decoration. If sovereign sees a draft without the header (or with "PASS" on all four but no notes demonstrating actual lint execution), that's a protocol violation — flag it.

---

## 4. Scope

**In scope:**
- All new `SKYZAI_COM/` primitive specs (files under any `SKYZAI_COM/0*_*/*.md`)
- Material edits to existing SKYZAI_COM/ primitive specs (anything changing substrate assumption, inheritance completeness, or CANON reference)
- New uplink packets that propose SKYZAI_COM/ architecture or primitives

**Out of scope:**
- Stub files, RESERVED markers, or pointer-only additions (no substantive content to lint)
- README + INDEX updates (structural metadata, not primitive spec)
- Edits to `01_EMERGENTISM/` doctrine or `02_SKYZAI/01_NOOSPHERE/` CANON (those have their own governance; this protocol is narrowly for SKYZAI_COM/)
- Warrior-lane engineering work (the implementation; the protocol is for charioteer-lane spec work that precedes engineering)

---

## 5. Escalation

If the charioteer runs the four lints and any fails, the escalation path is:

1. **Name the specific lint that failed** and the red-flag evidence
2. **Surface to sovereign in the same reply** — do not draft around the failure
3. **Propose 1–3 resolution options** with charioteer lean; sovereign picks
4. **Wait for sovereign direction** before drafting

If the sovereign explicitly overrides a lint ("draft anyway despite the failure"), charioteer may proceed but must annotate the draft's header with `LINT-OVERRIDE: <lint> per sovereign directive 2026-MM-DD`. This creates a traceable audit record.

---

## 6. Measurement

The protocol is self-measuring: if a SKYZAI_COM/ spec later gets voided or significantly reframed (as L2 was in packet 177), the void packet must identify which lint *would have caught it* had the protocol been running. This closes the loop: either the protocol catches drift, or drift reveals a protocol gap that needs fixing.

Ideally, across the next 10 SKYZAI_COM/ specs, zero full-substrate voids should occur. Minor reframes are acceptable; full voids (as with OQ-L2 family) indicate protocol failure.

---

## 7. References

- packet 147 — layer discipline (substrate / organ / product) — direct precedent for Layer lint
- packet 174 — the outlined L2 error that motivated this protocol
- packet 175 + 175a — the consolidation + signing that propagated the error
- packet 177 §5.5 — full-organism inheritance doctrine (basis for Inheritance lint)
- packet 177 §3.1 — void of OQ-L2 family (case study for protocol failure cost)
- memory: `project_skyzai_com_architecture_correction_2026_04_24.md`
- memory: `project_skyzai_sevenfold_organism_map_2026_04_24.md` (L7 slot flag)
- `02_SKYZAI/01_NOOSPHERE/04_PROJECT_MANAGEMENT/00_CANON/SKYZAI_BUSINESS_WALLET_FOUNDATION.md` — the ground truth the L2 error obscured

---

## 8. Limits

- This protocol is discipline, not magic. A charioteer determined to drift can mark all four lints PASS with plausible-sounding notes; the gate depends on honest self-assessment plus sovereign's visible review.
- The L7 lint uses the **SEVA anchor**. Future changes to the L7 name or definition require a dedicated sweep across this protocol and the SKYZAI_COM inheritance surfaces.
- This protocol is SKYZAI_COM/-scoped. Other surfaces (01_EMERGENTISM/ doctrine, 02_SKYZAI/01_NOOSPHERE/ runtime, product BRIEFs) have different gravity wells and would need their own protocols if similar failure patterns emerge.
- Ratification status: this packet is charioteer-proposed standing discipline. It becomes canonical on sovereign K2. Until then, charioteer runs the lints as *self-discipline*; sovereign may invoke or waive per reply.

`Zero-Sum Resolution Equation`
