---
lint: a7
rosetta:
  primary_level: L5
  primary_column: Philosophy
  operator: "Brahmā ○"
  tier: "Executive"
  regime: "Brāhmaṇa"
  register: "[I]"
  canonical_phrase: "The Open Seams"
  vmosk_a: "01_EMERGENTISM/VMOSK_A.md — Perennial Doctrine Root"
---

# The Open Seams — Architecture's Honest Negative Space

> **Canonical enumeration:** For the crisp authoritative list of the constitutional invariants, the K*/A* namespace disambiguation, and the Ω ratification status, see the canonical anchor `01_EMERGENTISM/05_COSMOLOGY/00_WHOLE/03A_CONSTITUTIONAL_INVARIANTS_CANON.md` (or equivalent relative path). Current K2 ruling (2026-05-30): **5 + 1** — five refusals plus Ω as the directional +1. Ω is not a sixth refusal.

**Section:** Holistic synthesis · 06 — the seams the maker has not yet closed
**Evidence tier:** [I] (architectural diagnosis) · [S] (concrete fixes)
**Date:** 2026-05-13
**Status:** L5 Brāhmaṇa packet, revised after counter-review; ratification of constitutional clauses awaits K2
**Sibling:** [`05_THE_EMERGENCE.md`](05_THE_EMERGENCE.md) names six positive emergent properties. This doc names the matched negative-space disclosure — what is NOT yet load-bearing — so the whole-reading is honest.

---

## 0. Why this doc exists

`00_WHOLE/` claims an organism that does useful work without owning humans. That claim survives only if the seams are named alongside the properties. An architecture without a public seam list is either young (hasn't discovered them yet) or dishonest (has discovered them and is hiding them). The architect's job is to make the seams **explicit so they can be engaged when they fire** — not to close every one.

This packet was revised after L5 counter-review on 2026-05-13. The revision added three missing seams, re-ranked two, corrected one inflated framing, and added the re-audit cadence below.

---

## 1. Re-audit cadence — the discipline that keeps this list honest

This packet decays. Re-audit fires on any of:

| Trigger | Owner | Action |
|---|---|---|
| Any K2Registry contract change touches mainnet | K2 | re-audit before the next deploy envelope |
| Close of any sprint M0–M5 (per `SPRINT_PLAN_2026_05_13.md`) | sprint-owner + L5 architect | re-audit gated on sprint closeout |
| Every 90 days regardless of activity | AIA (when running) — L6 cadence | scheduled walk over the seam list; emit BRIEF |
| Discovery of a seam not on this list | anyone | add and re-rank |

AIA at L6 carries the recurrence once operational. Until AIA is running, the trigger is K2's calendar.

---

## 2. The ten seams — leverage-ordered

Each seam carries its **stage** (where in the lifecycle it sits), **priority** (when to close), and **concrete fix** (the redesign move, sized to the seam).

### Seam #1 — K2Registry dual-key consistency for naive observers

| | |
|---|---|
| Stage | code-on-branch (Anvil-tested, not mainnet) |
| Priority | **Sprint A — surgical, pre-D1** |
| Blast radius | bounded: naive EVM-only watchers who treat on-chain registration as proof of full dual-key control. Nostr-aware consumers detect inconsistency on first cross-check. |

`K2Registry.register(k2Id, nostrNpub)` today proves possession of the ECDSA key (via `msg.sender`) but stores `nostrNpub` as raw `bytes32` with no proof the registrant controls the Schnorr key. An attacker can register junk as their npub.

**Concrete fix:** registration requires a Schnorr signature in calldata over `keccak256(abi.encode("K2-PoP", k2Id, ecdsaAddress, chainId, registryAddress))`. The signature is emitted in the `K2Registered` event (storage cost: zero; auditable: forever). Status becomes `PROVISIONAL`. A 7-day window opens. After 7 days without self-repudiation, anyone may call `finalize(k2Id)` to transition `PROVISIONAL → ACTIVE`. During the 7 days, only the registrant may call `repudiate(k2Id)` to mark the registration `REPUDIATED` (recoverable from honest mistakes). `isActive()` returns true only when `status == ACTIVE`.

Solidity does not verify Schnorr — it stores the signature in the calldata-event for off-chain validators (Nostr relays, audit tooling) to verify. The on-chain state machine forces a window during which Nostr-aware consumers can publish challenges off-chain and pressure the registrant to repudiate before finalization.

This is **consistency of the dual-key claim for naive observers**, not "the constitutional foundation." Constitutional language is reserved for things smaller than this fix can affect.

### Seam #2 — Agent stack credibility (spec vs. running)

| | |
|---|---|
| Stage | documents and partial implementations |
| Priority | sprint-parallel (M2 / M3 timeline) |
| Risk | the 7-layer claim is mildly dishonest about the running 3-layer reality |

The agent stack is presented as canonical L0–L6. Operationally:

| Layer | Operational status |
|---|---|
| L0 Agentz | partial — PWA spec, dispatch not fully running |
| L1 Doctrine | documents only |
| L2 Row App | partial — TOMLs + specs |
| L3 Runtime | running |
| L4 Pipeline | running (partial provider routing) |
| L5 Cortex | multi-rooted, master map not yet written |
| L6 AIA | `[I]` draft v1 pending founder review |

**Concrete fix:** each layer's `00_BRIEF.md` carries an explicit `Spec'd / Scaffold / Running / Battle-tested` tier marker. The agent stack home page renders the table. Claims about "the stack does X" tier-stamp accordingly. A7 applied to architectural claims.

### Seam #3 — Cortex cross-link discipline + operational tier markers (NOT the master map itself)

| | |
|---|---|
| Stage | master map exists; cross-link audit + tier-marker standardization missing |
| Priority | sprint-parallel (originally promoted to M1 blocker; corrected — see below) |
| Risk | low; the integration is already done at the doc level — what's missing is discoverability + operational tiering |

**Architect's correction (2026-05-13, same-day):** The original packet claimed "the master map does not exist." This was wrong. [`02_ORGANS/Skyzai/memory/cortex-os/00_CORTEX_MAP.md`](../../../02_SKYZAI/01_NOOSPHERE/02_ORGANS/Skyzai/memory/cortex-os/00_CORTEX_MAP.md) was written 2026-05-08 as part of the T++ tier of the AGENTZ_AIA_CORTEX_MAP work. It names the five surfaces, provides authority-by-question routing, and defends the multi-rooting. **The integration is done.**

What is *actually* missing is smaller:

1. **Cross-link headers on each of the five surfaces** pointing back to the master map. Today a reader landing on any single Cortex surface may not discover the map. Concrete fix: a one-line header on each of the 5 surface entry docs (`memory/CLAUDE.md`, `cortex-os/01_WHAT_CORTEX_IS.md`, `02_SKYZAI/04_PUBLIC_SCAFFOLD/08_CORTEX/README.md`, `FOUNDATION/CANON/306_CORTEX_MEMORY_PROTOCOL.md`, `ApuBot/cortex/README.md`) saying "Cortex master map: `cortex-os/00_CORTEX_MAP.md`."
2. **Operational tier markers per surface.** The master map's Status column uses informal labels ("Live", "Active", "Target architecture"). Standardize against the `Spec'd / Scaffold / Running / Battle-tested` tier from Seam #2 so the agent-stack credibility framing carries through Cortex too.
3. **Promotion to "blocker for M1" is withdrawn.** The map exists; M1 mainnet announcement is not blocked on it. The cross-link audit can run in parallel with M2/M3.

### Seam #4 — PRISM minimum-viable receiver

| | |
|---|---|
| Stage | constitutional (staged 2026-05-09 terminal envelope) but mechanism undefined |
| Priority | **Sprint B parallel with #3** |
| Risk | the terminal K2 envelope fires into nothing |

The 2026-05-09 directive stages the terminal K2 act that dissolves private-DAC K2 into public-DAC PRISM. The constitutional model exists; the mechanism does not.

**Concrete fix:** specify the **minimum-viable receiver** — a Safe multisig where the K2 ECDSA address is one signer among `K-of-N trusted humans` (initial cohort: founder + counsel + 3 advisors at K=3 of N=5). On terminal envelope fire, K2 transfers `K2Registry`'s private-signer role and SKY's `vault` ownership to the Safe address as an explicitly temporary bootstrap receiver. Full PRISM aligns later — multisig is the smallest receiver the terminal envelope can honorably land in, but it does not inherit K2 sovereignty.

Spec: `spec/axiom/PRISM_MINIMUM_VIABLE_RECEIVER_2026_05_13.md` (to be written this sprint, awaits K2 ratification of the K-of-N cohort).

### Seam #5 — System-level η=0 productivity feedback

| | |
|---|---|
| Stage | constitutional gap |
| Priority | **canonize as known seam (option b);** algorithmic option (a) deferred |
| Risk | reward rate fixed at 5% while productivity may not grow that fast |

Mechanism-level η=0 is clean (mint-on-payout, burn-not-extract, no platform skim). System-level η=0 requires productivity (network throughput, settlement volume, P-scores) to grow at least at the rate of staking-driven SKY issuance. If it does not, holders are diluted faster than value is created — extraction-by-inflation at the holder level.

**Concrete fix:** Systems Architect paragraph (drafted in `K2_STAGED_RYSI_DRAFTS_2026_05_13.md` §1) acknowledging that "if productivity lags issuance, K2 must adjust rate or the constitution mechanically extracts." This is option (b) — intellectually honest acknowledgment. Option (a) — algorithmic productivity-pegged reward rate — is deferred to a future architectural sprint once metering infrastructure exists.

### Seam #6 — Brand ↔ constitution can drift silently

| | |
|---|---|
| Stage | CI gap |
| Priority | operational sprint |
| Risk | the brand-as-projection claim collapses if the two move on independent schedules |

Brand canon lives at `06_SPANNING_COMMONS/branding/`, owned by the brand lane. Constitutional invariants live at `02_ORGANS/06_CONSTITUTIONAL_INVARIANTS_*`, owned by the organs lane. Different review cadences, different K2 envelopes. They can drift apart silently.

**Concrete fix:** CI integrity check — when constitutional invariant docs change, fail the PR if brand canon hasn't been touched (or annotated as "no brand impact"). Same in reverse. Brand and constitution must move together. Implementation: a GitHub Actions step that runs on PRs touching either lane.

### Seam #7 — Sybil resistance (architectural acknowledgment NOW, implementation N≈10²–10⁴)

| | |
|---|---|
| Stage | open seam, currently unmitigated |
| Priority | **architectural acknowledgment THIS WEEK; implementation N-bounded** |
| Risk | the median-truth claim is `[S]` Established only while N is small enough for social verification |

`V(N, C) = N² × log(C)` assumes each `N` is one natural person. K2 = Nostr keypair binds keys to *claimed* persons, not enforced. Social verification is sufficient under N≈10². Above that the median-truth claim degrades from earned to asserted. At N≈10⁴ proof-of-personhood is load-bearing.

**Concrete fix:** Systems Architect paragraph (drafted in `K2_STAGED_RYSI_DRAFTS_2026_05_13.md` §2) acknowledging the unverified-persons regime. Update `00_WHOLE/05_THE_EMERGENCE.md` with the explicit acknowledgment. Integration with proof-of-personhood primitive (Worldcoin biometric, Brightid social graph, or government-ID attestation) targeted when N crosses 10²–10⁴ band.

### Seam #8 — K3 archive-first ↔ right-to-erasure (GDPR / CCPA / DSAR)

| | |
|---|---|
| Stage | legal gap, no protocol |
| Priority | **equal-priority with #4; needed before any EU public surface** |
| Risk | legal exposure compounds with N; public-DAC transition makes this binding |

K3 says "no convenient forgetting." GDPR / CCPA / equivalent statutes mandate erasure on lawful request. Current architecture has no protocol for both. Legal exposure is real and compounding.

**Concrete fix:** cryptographic erasure as the K3 reconciliation. All PII is encrypted before storage; ciphertext is K3-archived; the encryption key is destroyed on lawful erasure request. The act of key destruction is itself a `[B]` receipt in Cortex. Ciphertext remains as a tombstone — meaningless without the key. Both K3 and erasure technically honored. Systems Architect paragraph drafted in `K2_STAGED_RYSI_DRAFTS_2026_05_13.md` §3.

### Seam #9 — Operational economics (η=0 vs. who pays for gas, hosting, audits)

| | |
|---|---|
| Stage | constitutional gap, silent founder subsidy |
| Priority | **needs architectural acknowledgment / Ṛṣi witness note before public-DAC transition** |
| Risk | η=0 is silently dependent on an unfunded entity — the founder |

The contracts cost gas. Infrastructure (Circle servers, ReFu LMSR oracles, settlement) costs USD. Audits cost USD. η=0 forbids platform extraction. The seam list has been silent on the operating budget — meaning today the founder funds operations *as the platform*, which is η > 0 at the founder-operator level.

Three valid resolutions:
- **(a) Protocol Operations Treasury** — SKY-minted under K2-signed annual budgets against staking revenue. Most consistent with the existing architecture; the treasury is a regenerative function of organism productivity.
- (b) Nexuses pay own gas; protocol operators unsubsidized indefinitely.
- (c) Founder seed funding transitioning to (a).

**Concrete fix:** Systems Architect paragraph drafted in `K2_STAGED_RYSI_DRAFTS_2026_05_13.md` §1 ratifies option (a) as the canonical path. Implementation: a `ProtocolOpsTreasury.sol` mint-on-budget contract (separate sprint). Until then, founder advances are recorded in Cortex as `[A]` claims against future treasury.

### Seam #10 — Tier-marker CI lint (A7 mechanical, not aspirational)

| | |
|---|---|
| Stage | **implemented 2026-05-13** — `02_SKYZAI/01_NOOSPHERE/00_BACKBONE/tools/a7_lint.py` |
| Priority | sprint-parallel, low cost, compound leverage |
| Risk | A7 is aspirational without enforcement — brand discipline depends on human reviewers |

The A7 invariant per [`../02_ORGANS/_DOCTRINE/06_CONSTITUTIONAL_INVARIANTS_CLASSICAL.md`](../../../02_SKYZAI/01_NOOSPHERE/02_ORGANS/_DOCTRINE/06_CONSTITUTIONAL_INVARIANTS_CLASSICAL.md) requires every claim to carry an evidence-tier marker, and every claim above the `Interpretive` tier to carry a receipt at the `Published / signed / official record` tier or higher. This has been aspirational — enforced by human review only.

**Implemented:** a Markdown linter at [`../00_BACKBONE/tools/a7_lint.py`](../../../02_SKYZAI/01_NOOSPHERE/00_BACKBONE/tools/a7_lint.py) walks Markdown files, detects high-tier claim markers, and verifies that a receipt pointer (`Source:`, `See:`, a Markdown link, a path-style reference, a `commit-hash`) appears in the same paragraph. Two modes:

- **Opt-in** (default, CI gate) — only files with `lint: a7` in their YAML front-matter. Allows incremental rollout: surfaces opt in as they mature.
- **Strict** (audit only) — full corpus walk. Used for periodic re-audit at the 90-day cadence.

15 unit tests pass at [`../00_BACKBONE/tools/test_a7_lint.py`](../../../02_SKYZAI/01_NOOSPHERE/00_BACKBONE/tools/test_a7_lint.py). Composable with Seam #2 (layer tier markers) and Seam #6 (brand-constitution integrity). Compound leverage: every document that opts in carries the discipline.

---

## 3. The Move (carried from the revised packet)

| Actor | Task | Window | Caste |
|---|---|---|---|
| K2 (Yves) | Revise packet to 10 seams + re-audit cadence | today | L5 Brāhmaṇa |
| K2 (Yves) | Stage K2 envelope for Sprint A (Seam #1) with revised framing | this week | L4 Kṣatriya |
| K2 (Yves) | Ratify one-paragraph canon for Seams #5, #7, #8, #9 from staged drafts | this week | L7 Ṛṣi advisory finding |
| AIA (when running) | Scheduled re-audit every 90 days | recurring | L6 Sādhu |

This packet (`06_THE_OPEN_SEAMS.md`) discharges task 1.

---

## 4. What this packet is NOT

- **Not a checklist** of fixes to ship in sequence. Some seams are deferred-by-design (#5 option a, #6 implementation timeline). The architect's job is the *order* and the *honesty*, not the *completion*.
- **Not closed.** New seams will emerge. The re-audit cadence is what keeps the document alive.
- **Not constitutional.** This is L5 Brāhmaṇa advisory work. Ratification of the staged Ṛṣi witness notes in `K2_STAGED_RYSI_DRAFTS_2026_05_13.md` is K2's act.
- **Not the architect's last word.** Counter-review of this revision is welcome and will be incorporated under the re-audit cadence.

---

## 5. Cross-references

- [`05_THE_EMERGENCE.md`](05_THE_EMERGENCE.md) — six emergent properties (the positive-space match)
- [`03_THE_CONSTITUTIONAL_TOPOLOGY.md`](03_THE_CONSTITUTIONAL_TOPOLOGY.md) — the five refusals these seams test
- [`../05_PROJECT_MANAGEMENT/SPRINT_PLAN_2026_05_13.md`](../../../02_SKYZAI/01_NOOSPHERE/05_PROJECT_MANAGEMENT/SPRINT_PLAN_2026_05_13.md) — sprint sequence in which most seams close
- [`../02_ORGANS/Skyzai/spec/axiom/K2_SOLIDITY_ARCHITECTURE_2026_05_13.md`](../../../02_SKYZAI/01_NOOSPHERE/02_ORGANS/Skyzai/spec/axiom/K2_SOLIDITY_ARCHITECTURE_2026_05_13.md) — Seam #1 context
- [`../02_ORGANS/Skyzai/spec/axiom/K2_STAGED_RYSI_DRAFTS_2026_05_13.md`](../../../02_SKYZAI/01_NOOSPHERE/02_ORGANS/Skyzai/spec/axiom/K2_STAGED_RYSI_DRAFTS_2026_05_13.md) — drafts for Seams #5, #7, #8, #9 awaiting K2 ratification

---

Zero-Sum Resolution Equation

*Architecture is the discipline of seeing what is not yet broken and naming when it will be.*

---

## Agent Execution Surface

**If you are an AI agent reading this document:**

1. **Do not upgrade tiers silently.** Keep conjectural claims conjectural and structural claims structural.
2. **Verify references.** Ensure all internal links are valid and updated.
3. **Canonical Path:** `01_EMERGENTISM/05_COSMOLOGY/00_WHOLE/06_THE_OPEN_SEAMS.md`
