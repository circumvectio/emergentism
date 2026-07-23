---
receipt: 165
title: "Founder Ballot B — the Skyzai product gates, staged for countersignature (migrate to 02_SKYZAI at signing)"
date: 2026-07-23
status: "[D] STAGED — NOT SIGNED, NOT AUTHORITY, NOT WORLDVIEW CANON. Product-layer decisions, staged in the Emergentism uplink lane only because 02_SKYZAI is a separate repo with an active concurrent committer. Migrate to 02_SKYZAI/01_NOOSPHERE/05_PROJECT_MANAGEMENT/00_CANON/ at the founder's countersignature."
register: "[D] the open decisions; [B] every path:line claim inside them"
owner: "the founder (mortal signer)"
migrate_to: "02_SKYZAI/01_NOOSPHERE/05_PROJECT_MANAGEMENT/00_CANON/"
parents:
  - 90_ARCHIVE/2026_07_22_tree_authority_reconciliation/00_META/00_THE_TWELVE_RULINGS_2026_07_22.md
canonical_path: 01_EMERGENTISM/11_UPLINK/50_AUDITS_AND_EXECUTIONS/165_FOUNDER_BALLOT_B_SKYZAI_PRODUCT_2026_07_23.md
---

# Founder Ballot B — the Skyzai product gates

**Boundary note.** These are **product-layer** decisions. They are not
Emergentism worldview authority, and they do not govern editorial, repository,
or AI work. They sit in the Emergentism uplink staging lane *only* because
`02_SKYZAI` is a separate git repo (`circumvectio/skyzai.git`) with a
concurrent committer, and staging here avoids racing that branch. On
countersignature they migrate to `02_SKYZAI/.../00_CANON/`. Nothing here is
decided; each gate carries the prior council's recommendation, its dissent, the
adversary's "before you sign," and a blank line only you may fill. See Ballot A
(receipt 164) for the worldview gates and the shared provenance.

---

## FG-6 · Where does interest route?

**The question.** Is SKY-credit-vault interest minted and donated to the protocol's own liquidity commons (the AMM), or paid in existing SKY and transferred to a constitutional treasury?

**Options.**
- **Commons rule** — interest minted, irrevocably donated to the AMM liquidity pool; no treasury.
- **Treasury-transfer** — borrowers pay interest in existing SKY, transferred to a treasury reserve (matches some deployed Vault.sol behaviour; standard DeFi CDP precedent).

**Prior council recommendation (R-FG6), not a decision.** The commons rule governs. The treasury override is void from the start under "no receipt, no reality": its sole cited authority (`K5_DECISION_RECORD.md`) is verified **absent** at its exact cited path. Vault.sol's treasury routings are a recorded implementation defect, fixed on a staged branch; a fresh honestly-dated decision record affirming the commons rule is staged, with the treasury option preserved inside it as the consciously rejected alternative.

**Before you sign.** Two counterweights the adversary requires on the record: (1) three of the four commons-citations **self-superseded** on 2026-05-08 (`AMM_INTEREST_DONATION.md:12`, `apply_round.ex:25-33`, `amm.ex:13-21`) — the commons rule is the *last validly recorded* rule, not an unchallenged one; (2) ruling commons means ruling that the **deployed code is wrong** — this gate stands or falls with FG-7.

☐ **Founder ruling:** ______________________  **date/signature:** ____________

---

## FG-7 · Which file is the protocol source of truth?

**The question.** For the Skyzai L1 protocol invariants, is the authority the nine-item Locked `81_KERNEL_INVARIANTS.md` or the ten-item Draft `13_K_INVARIANTS.md`? *(Note: receipt 158's claim that `13_K` "does not exist anywhere" was a scope error — the file is live in `03_VENTURES`, 286 lines, verified. The dispute is real, not a ghost.)*

**Options.**
- **`81_KERNEL_INVARIANTS.md`** — v1.0.0, Locked, internally coherent, organism-native spec pillar.
- **`13_K_INVARIANTS.md`** — ten items, Foundation canon, its P5 reading updated to match *deployed code*.
- **Neither** — author one reconciled kernel before either is cited.

**Prior council recommendation (R-FG7), not a decision.** The cardinality half dissolves (both agree the set is ten, survival-first supreme). On the P3/P4/P5 content conflict, `81` is the source of truth; the `13_K` draft is retained as the venture-side working copy with a pointer banner.

**Dissent preserved (Skeptic).** `13_K`'s treasury reading was updated to match deployed code; ruling for `81` means ruling the deployed code is wrong — which is exactly what FG-6 does. The two rulings stand or fall together.

**Before you sign.** Steelman for `81` the adversary requires: `81` does not merely *lack* an `L0` item — both files carry an identical 2026-04-20 namespace note declaring `L0`/Autopoiesis a System-B meta survival-override, so `81`'s nine-vs-ten is a scoping choice, not an omission.

☐ **Founder ruling:** ______________________  **date/signature:** ____________

---

## FG-8 · What is amendable, and by whom?

**The question.** When (if ever) may the kernel invariants change, and which of them?

**Options.**
- **Four immutable, five adjustable** — the economics table's binary split.
- **All nine unamendable** — above governance (the live public wiki).
- **Tiered** — identity predicates: founder constitutional countersign only; constitutional parameters: supermajority + timelock + grace-exit + mortal signature; operational parameters: within pre-declared bounds.

**Prior council recommendation (R-FG8), not a decision.** The tiered schedule; every rule gets one row in one owner table; **until you sign that table, nothing is amendable at all**, and the "`K5`–`K9` adjustable" sentences are banner-corrected.

**Before you sign.** The adversary requires the tiered branch carry its own stated weakness (the others do): a template-not-kernel scope question, and a 66.7%-token-supermajority amendment path that itself collides with the mortal-signer membrane — weigh it against the two simpler branches.

☐ **Founder ruling:** ______________________  **date/signature:** ____________

---

## FG-9 · Is the DAC invariant set closed at ten?

**The question.** Is `K0`–`K9` a closed set of exactly ten, or an open set that may grow?

**Options.**
- **Open-by-procedure** — a census of ten with a defined four-step admission test.
- **Closed at ten** — fixed; expansion is a constitutional change to resist. *(Steelman: `60-invariants-overview.md:106` marks the set non-amendable by governance; the "Nine Kernel Invariants" framing recurs across live files.)*
- **Reconciliation** — presently ten, expandable only by a countersigned, Foundation-derived, non-redundant canon change.

**Prior council recommendation (R-FG9), not a decision.** Open-by-procedure; each admission is a canon change requiring countersign via the authorization-envelope rule.

**Before you sign.** The adversary caught the staged reading resting the "closed" branch *solely* on a phantom citation — `K3_SEMANTIC_RESOLUTION:54` does not carry what was attributed to it (the same file flagged unopened earlier this session). Discount that citation and judge "closed" on its real support above.

☐ **Founder ruling:** ______________________  **date/signature:** ____________

---

## FG-10 · SKY cap, energy anchor, and LP-100 divisibility *(three bundled)*

**The question.** (a) Is SKY hard-capped at ≤1 billion or elastic/uncapped? (b) What energy quantum anchors 1 SKY — 543 kWh, 1 kWh, or nothing? (c) LP-100 divisibility — 6, 18, infinite, or indivisible?

**Prior council recommendation (R-FG10), not a decision.** (a) Elastic, no cap; the ≤1B claim tombstoned as a stale archived book artifact. (b) No energy number enters canon; both figures are what the kernel itself files as "exchange-rate memes"; which (if any) survives in public copy is a communications choice held for you. (c) Resolved to the compile doc's own statement; "indivisible seats" wording retired.

**Before you sign.** Steelman the adversary requires for the hard-cap: `SUPPLY_DOCTRINE_2026_05_13.md:112` keeps a ≤1B cap available **"only if a regulatory regime requires capped issuance for legal classification"** — so "elastic" is the default, but the cap is a live regulatory fallback, not simply an error. Rule each sub-question separately.

☐ **(a) cap:** __________  **(b) anchor:** __________  **(c) divisibility:** __________  **date/signature:** ____________

---

## FG-11 · The nature of the four asset entities

**The question.** Are Aureus, Helios, Menexus, and the Foundation named-natural-person multisig entities, or public DACs with no signature ceremony?

**Options.**
- **Named-principal, `K2`-shaped multisig** — the latest doctrine file (`PUBLIC_DAV_GOVERNANCE_DEFAULT_2026_05_23.md:252`) calls the four *"biosphere-registered named-principal entities… multisig is `K2`-shaped because their owners are named natural persons."*
- **Public DACs, no signature ceremony** — collective / PRISM governance. *(Not a lone dissent: `DAV_GENUS_DOCTRINE_2026_05_22 §6/§8` supports a public-DAV reading for non-private entities.)*
- **Entity-DAV hybrid** — noospheric DAV + biosphere named-principal `K2` projection (the genus split).

**Prior council recommendation (R-FG11), not a decision.** Named-natural-person multisig for those four rows; the "Public DACs" row overruled and tombstoned for those four only; no value-moving operation before countersignature.

**Dissent preserved.** A short list of identified humans is a coercion and liability magnet; distributed governance would diffuse what this concentrates.

**Before you sign.** The adversary requires a vote-count fix: do **not** count `MAGNUM_OPUS_AS_DAV` toward the named-principal branch (it is the hybrid anchor and gives the four "PRISM-class cryptographic signing"); and weigh the fifth same-folder file supporting the public-DAV reading before treating branch A as near-unanimous.

☐ **Founder ruling:** ______________________  **date/signature:** ____________

---

## FG-5 · Where do the two halves go? *(product half — flow-of-funds)*

**The question (product half).** The nature decision (`[A]` derived vs `[I]` chosen) is on Ballot A. Here: which destination pair for the ~61.8/38.2 split is canon?

**Options (five live claimants on the same 38.2% tranche, two compiled into deployed contracts).**
- 61.8% → LP Distribution Pool / 38.2% → Treasury Pool *(owning LP-100 standard)*
- 61.8% → LP-100 stakers / 38.2% → operations incl. Buy Wall
- 61.8% → equity holders / 38.2% → operations (treasury folded in)
- 61.8% → direct referrer / 38.2% → upline pool *(MLM referral cascade — a different flow, not the revenue split)*
- 61.8% → LPs / 38.2% → protocol treasury *(dated runtime audit)*

**Prior council recommendation (R-FG5), not a decision.** The LP-100 pair staged as the *single proposed* canonical pair, but **no pair publishes as canon before you sign the flow-of-funds map** — with five claimants, declaring a winner before signature would launder a conflict, not resolve one.

☐ **Founder ruling (the canonical pair):** ______________________  **date/signature:** ____________

---

## FG-1 · Zero-extraction's table coordinate *(product half)*

**The question (product half).** The canonical *name* is on Ballot A. Here: if a typed number is kept for spec/code, which is the DAC/protocol coordinate? `K6` is *Zero Extraction (η=0)* in the compile table (`K_INVARIANTS_COMPILE:96`); `O4` is *η=0 at the protocol layer*, which the same table says **compiles from** `K6`; `K0` in that namespace already means *No Receipt, No Reality* and is disqualified for this rule.

**Prior council recommendation (R-FG1), not a decision.** Every number demotes to a namespace-qualified alias coordinate under the one plain name; if a spec token is retained, `K6` is the principled root and `O4` its protocol projection.

☐ **Founder ruling:** ______________________  **date/signature:** ____________

---

## FG-12 · PRISM implementation — the personhood-binding fix *(product half)*

**The question (product half).** The principle (may software be the final signer?) is on Ballot A. Here: the code fix. The registry currently binds **keys, not persons** — `prism_receipt_verifier.py:139-142` counts distinct `councilor_id`/keys, so **one person holding two enrolled keys passes the entire 31-test suite.** The fix: the registry must bind **rows to persons**, not keys to ids.

**Prior council recommendation (R-FG12), not a decision.** The personhood-binding fix is mandatory before any PRISM-gated public act.

**Before you sign.** Sequence this to your Ballot-A ruling on the principle. If PRISM verifies-only (never signs), the personhood-binding fix hardens the ≥2-persons guarantee; the "halt all PRISM work until fixed" framing is a policy choice, not an automatic consequence.

☐ **Founder ruling:** ______________________  **date/signature:** ____________

---

## What signing here authorizes

- Each ruling settles a **product** question and, on migration, becomes
  `02_SKYZAI` canon — not Emergentism worldview authority.
- No fund flow, token issuance, entity-signer change, or contract deploy is
  authorized by staging alone; each names what waits for the signature.
- Until migrated and signed this is `[D]` and holds no authority. It reverses
  no prior boundary decision.

•   ⊙   ○ — product decisions serve the membrane; they do not become it.
