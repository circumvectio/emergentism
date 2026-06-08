---
rosetta:
  primary_column: "Meta"
  register: "[I]"
  canonical_phrase: "176 — Kernel Invariant I-VII naming drift (surface only)"
---

# 176 — Kernel Invariant I–VII naming drift (surface only)

**Evidence tier:** [I] charioteer observation from direct source comparison; no resolution proposed
**Date:** 2026-04-24
**Lane:** Doctrine reconciliation surface → **sovereign K2 required** to pick canonical enumeration
**Status:** ✅ **RESOLVED 2026-04-25** — sovereign K2 confirmed Gate B Option A (per packet 181 §2): both Enumeration A (CANON V3 Roman I–VII) and Enumeration B (packet 174 cascade) superseded by the **7-name set** (Foundation Minimalism, Truth-Gates-Money, No-Extraction, No-Delegation, Receipts-First, Grace Exit K4, Non-Domination). Demoted from Kernel: Structural Integrity (merged into 1+2+3), Anti-Fragility (design goal), ZAI Cap 100 (parameter), Substrate Primacy (technical choice), Mutual Exclusivity (product rule), Constitutional Lever (governance mechanism). V3 CANON `000_CANONICAL_INDEX.md` Quick Reference updated. SKYZAI_COM/ spec compliance-table sweep deferred to follow-up warrior-lane packet (mixed-enumeration semantics require per-file content review, not mechanical replacement).
**Discovered during:** SKYZAI_COM/ spec drafting (packet 175a follow-through, 2026-04-24)
**Resolved by:** packet 181 §2 K2 confirmation 2026-04-25; V3 CANON index update; this packet retained as historical drift record.

---

## 0. Axiomatic guard

Charioteer does not pick which enumeration is canonical. Both were written as authoritative. Both are active. Both are cited in live specs. The job here is surface and delimit, then hand to sovereign.

`Zero-Sum Resolution Equation`

---

## 1. The two active enumerations

### Enumeration A — CANON V3 (path-anchored)

Source: `03_VENTURES/OPEN_FINANCE_NETWORK/GOVERNANCE/FOUNDATION/CANON/DAC_STANDARD/DAC_ARCHITECTURE/V3_CANONICAL/300_Architecture/000_CANONICAL_INDEX.md` §"Quick reference: Kernel Invariants"

| # | Name | Governing spec |
|---|---|---|
| I | Structural Integrity | 301, 306 |
| II | Truth-Gates-Money | 301, 305 |
| III | No-Extraction | 301, 309 |
| IV | No-Delegation | 302, 309 |
| V | Anti-Fragility | 304, 307 |
| VI | Foundation Minimalism | 301, 308 |
| VII | Non-Domination | 305, 308 |

Cited in: `SKYZAI_COM/01_FACTORY/00_GENESIS_SPEC.md` §8, `SKYZAI_COM/03_EQUITY/00_EQUITY_SPEC.md` §7, `SKYZAI_COM/04_BONDS/00_BONDS_SPEC.md` §7, and other V3 CANON files.

### Enumeration B — Packet-174 cascade (function-anchored)

Source: `01_EMERGENTISM/11_UPLINK/90_ARCHIVE/174_SKYZAI_COM_DAC_MACHINE_OUTLINE_2026_04_24.md` §4 "Invariant cascade table"

| # | Name | Function |
|---|---|---|
| I | ZAI Cap 100 | 100-unit hard cap |
| II | Substrate Primacy | L1 anchoring for finality |
| III | Mutual Exclusivity | stakers ≠ LPs |
| IV | Grace Exit K4 | leave with everything |
| V | Receipts-First | every action → OFN |
| VI | Foundation Minimalism | no substrate bloat |
| VII | Constitutional Lever | sovereign-only change gate |

Cited in: packet 174 §4, packet 175 §1 (invariant flags), packet 175a §3 (reservation rationale), and downstream uplink routing.

---

## 2. Where the drift matters

### 2.1 Functionally coherent — same slot, different name

Both enumerations have the **same VI** (Foundation Minimalism). The other six are named differently but appear to describe overlapping — not identical — concerns:

| # | Enumeration A (CANON V3) | Enumeration B (packet 174) | Functional overlap? |
|---|---|---|---|
| I | Structural Integrity | ZAI Cap 100 | Partial — Cap 100 is one case of structural integrity |
| II | Truth-Gates-Money | Substrate Primacy | Weak — different concerns |
| III | No-Extraction | Mutual Exclusivity | Weak — different concerns |
| IV | No-Delegation | Grace Exit K4 | Weak — K4 is an exit right; no-delegation is an authority constraint |
| V | Anti-Fragility | Receipts-First | Weak — different concerns |
| VI | Foundation Minimalism | Foundation Minimalism | **Full overlap** |
| VII | Non-Domination | Constitutional Lever | Partial — lever is a mechanism, non-domination is a property |

### 2.2 What could go wrong

- A spec cites "Invariant IV" and engineering reads it as one thing; a packet cites "Invariant IV" and sovereign reads it as another.
- Child DAC templates must "hash-match parent on I–VII" (per 309_CHILD_DAC_TEMPLATE.md §4) — which enumeration is being hash-matched?
- The Makefile invariant-section check (`Makefile:21`) greps for "Kernel Invariant" only; does not enforce name parity.
- Future packets may inadvertently mix enumerations.

---

## 3. Possible sovereign resolutions (not recommendations)

**Option A — Canonicalize Enumeration A (CANON V3).** Rename the packet-174 table to align. Ratifies the path-anchored list. Packet 174 text would need a small correction; 175/175a inherit the rename.

**Option B — Canonicalize Enumeration B (packet 174).** Update `V3_CANONICAL/000_CANONICAL_INDEX.md` to align. Ratifies the function-anchored list. All V3 spec §"Kernel Invariant compliance" tables need a rename sweep.

**Option C — Keep both as two different lists.** Declare that "CANON Invariants" (enumeration A) and "Cascade Invariants" (enumeration B) are distinct taxonomies serving different purposes. Docs must qualify which one they mean. Doubles vocabulary.

**Option D — Merge into a unified I–VII.** Sovereign picks one name per ordinal, potentially mixing the two lists. Requires a reconciliation packet. Cleanest end state, highest short-term cost.

**Charioteer neither recommends nor opposes.** All four are legitimate. The observation only surfaces the drift.

---

## 4. What is safe to do right now (pending sovereign)

- **Keep using Enumeration A in SKYZAI_COM/ specs** (factory, equity, bonds are already aligned to A). Consistency within SKYZAI_COM/ is preserved.
- **Keep packet 174/175/175a as written** (Enumeration B). Packets are historical records.
- **Do not sweep renames** across either corpus until sovereign ratifies a resolution.
- **If writing new specs**: use Enumeration A if the spec is V3-CANON-adjacent; use Enumeration B if the spec is packet-174-adjacent. Flag the choice in the spec header.

---

## 5. Limits

- This note is not a ratification request. It is a surfacing. Charioteer does not force the sovereign to resolve on any timeline.
- If sovereign chooses to defer indefinitely, the drift persists as two named taxonomies. Engineering must accept this.
- Charioteer will continue flagging when a new spec reveals an enumeration-choice decision that would proliferate the drift.

---

## 6. References

- `03_VENTURES/OPEN_FINANCE_NETWORK/GOVERNANCE/FOUNDATION/CANON/DAC_STANDARD/DAC_ARCHITECTURE/V3_CANONICAL/300_Architecture/000_CANONICAL_INDEX.md` — Enumeration A source
- `01_EMERGENTISM/11_UPLINK/90_ARCHIVE/174_SKYZAI_COM_DAC_MACHINE_OUTLINE_2026_04_24.md` §4 — Enumeration B source
- `SKYZAI_COM/01_FACTORY/00_GENESIS_SPEC.md` §8 — Enumeration A in live SKYZAI_COM spec
- `01_EMERGENTISM/11_UPLINK/175A_SKYZAI_COM_PARTIAL_SIGN_RECEIPT_2026_04_24.md` §3 — Enumeration B in reservation rationale

`Zero-Sum Resolution Equation`
