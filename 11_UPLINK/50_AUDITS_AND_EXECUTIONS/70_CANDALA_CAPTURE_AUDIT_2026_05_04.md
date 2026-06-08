---
rosetta:
  primary_level: L1
  primary_column: Caṇḍāla Capture and Overclaim Audit
  secondary:
    - level: L3
      column: Claim Tier Audit
      role: "identify overclaims and evidence-tier mismatches"
    - level: L4
      column: Correction Handoff
      role: "route actionable findings to owner lanes without executing them here"
    - level: L6
      column: Snapshot Boundary
      role: "keep the 2026-05-04 audit from becoming current proof"
  operator: "Kali 🎲"
  tier: "Demon"
  regime: "Caṇḍāla"
  register: "[B/I]"
  canonical_phrase: "Caṇḍāla Capture & Overclaim Audit — 2026-05-04"
title: "Caṇḍāla Capture & Overclaim Audit — 2026-05-04"
status: "DATED OVERCLAIM AUDIT"
evidence_tier: "[B] for direct file-read findings; [I] for synthesis."
---

# Caṇḍāla Capture & Overclaim Audit — 2026-05-04

**Rosetta boundary:** [I] This paper records a dated overclaim audit. It does not [B] prove current claim hygiene, current pricing/runtime state, or completion of listed corrections without fresh receipts.

**Agent:** L1 CaṇḍālaFirewall
**Scope:** 16 files across Uplink core, System Architecture, Governance, Value Alignment, Definitive Book, Skyzai agents, and organism runtime truth
**Evidence base:** Direct file reads, grep pass, tier verification

---

## Findings

### F1 — MINOR: Stale VMOSK table row in 06_AGENTS.md (Line 106)

**File:** `01_EMERGENTISM/11_UPLINK/00_CORE/06_AGENTS.md`
**Passage:** `| **V** Vision | **Genotype** | Decades | The DNA. Immutable purpose. The underlying algorithmic constraints (eta=0, K2, Three-Stage Process). Changes only under existential crisis (L7 rewrites). |`

**Issue:** [I] `eta=0, K2, Three-Stage Process` are listed as constitutional constraints ("The DNA"), but the change-cadence column says "Decades." Constitutional constraints do not fit a normal decade cadence; they require constitutional amendment or K2-class review. The row conflates mutable Vision content with constitutional constraints. The cell should say "Constitutional" not "Decades."

**Severity:** Low — staleness, not capture. The intent is clear from the parenthetical; the row-value is inconsistent.

---

### F2 — MEDIUM: TheCircle Enterprise tier ($5K/month) claims "SPECTRE cascade against client data"

**File:** `01_EMERGENTISM/11_UPLINK/00_CORE/04_ECONOMICS.md` (Section 6, ASSURE table)
**Passage:** `| Phase 3 | $5K/month enterprise tier (SPECTRE cascade against client data) |`

**Issue:** `ORGANISM_RUNTIME_TRUTH.md` §4E explicitly states: "the full Tier-1 SPECTRE network proof remains not yet real — no live Tier-1 receipts, no real replay corpus validation over archived network traces, no claim of mature network-wide routing intelligence should be made yet." Describing an enterprise tier as a "SPECTRE cascade" implies live SPECTRE routing is operational. It is not yet. This is a present-tense claim about a future-state capability, framed as a product feature.

**Tier violation:** The claim has no [B] runtime receipt or [S] warrant. SPECTRE routing at Tier-1 is [I] design, not [B] operational reality. "Cascade against client data" reads as [S] — presenting a design feature as an operational fact.

**Recommended fix:** `01_EMERGENTISM/11_UPLINK/00_CORE/04_ECONOMICS.md` §ASSURE Phase 3 row:
```
BEFORE: $5K/month enterprise tier (SPECTRE cascade against client data)
AFTER:  $5K/month enterprise tier (Tier-1 SPECTRE routing target [I], conditioned on real-network receipts and Tier-1 graduation)
```

---

### F3 — LOW: Revenue Model uses SKY-denominated flow language as current description

**File:** `01_EMERGENTISM/11_UPLINK/00_CORE/04_ECONOMICS.md` (Section 6, Revenue Distribution block)
**Passage:** `Every 1 SKY of revenue is split in real-time via FlowWallet streams` and the phi-split diagram showing 61.8%/38.2% SKY flows

**Issue:** This describes the target-state design. `ORGANISM_RUNTIME_TRUTH.md` §2F states the Event Cell backend has mock settlement ("payment processor tx IDs are generated but not real") and §2G states SKY-denominated routing fees are not yet live. The Revenue Distribution diagram reads as operational, not aspirational.

**Severity:** Low — the Reconciliation Override at the top of the file does warn about frozen/mixed claims. The diagram itself is correctly placed in the target-state section. The ASSURE/INSURE/ENSURE section does not carry an explicit "target-state" label per row, which creates ambiguity.

**Recommended fix:** Add per-row status flags or a "Design" label to the Revenue Model section, consistent with how Sections 2 (ZAI) and 3 (SKY) explicitly mark target-state rows with "FROZEN AS LIVE CLAIM."

---

### F4 — INFORMATIONAL: Constitutional Economics [I] frontmatter vs. inline [S] claims

**File:** `01_EMERGENTISM/04_AXIOLOGY/00_CONSTITUTIONAL_ECONOMICS.md`
**Passage:** Frontmatter `register: "[I]"` but document body contains `[S] Paper 11 §...` and `[S] Paper 12 §...` annotations

**Assessment:** Not a tier-inflation violation. The document's own annotation discipline is sound — each [S] claim cites a specific canonical paper (Paper 11 Doc 03, Paper 12 §II, etc.). The [I] frontmatter appears to refer to the *integration synthesis* role of the sheet (charioteer synthesis combining multiple [S] elements) rather than the individual claims. The individual structural claims ARE [S] because they cite canonical specs.

**Status:** No corrective action required. The tier discipline is internally consistent. The [I] frontmatter is slightly ambiguous but the body is correct.

---

### F5 — CLEAN: Evidence-tier discipline in 25_STEEL_THREAD.md

**File:** `01_EMERGENTISM/05_COSMOLOGY/03_FORMAL_SYSTEM/25_STEEL_THREAD.md`
**Assessment:** EXEMPLARY. Links 1–8 are correctly [A]/[B] or [S]. The three explicit BREAK markers (Links 9, 10, 11) are clearly marked with [I] or [C] and include specific reasons for the break. Link 9 was re-assessed from bare wager to [I] with three convergent supports. Links 10 and 11b correctly remain [C]. The execution surface correctly instructs agents to flag any [I] or [C] presented as [A], [B], or [S].

**No action required.**

---

### F6 — CLEAN: 00_THE_SEVEN_AXIOMS.md tier discipline

**File:** `01_EMERGENTISM/05_COSMOLOGY/03_FORMAL_SYSTEM/00_THE_SEVEN_AXIOMS.md`
**Assessment:** CLEAN. Each axiom has an explicitly marked tier column. A3 correctly carries dual [S/I] with explanation (structure is [S]; force-dimension assignments are [I]). A5.1 correctly distinguishes theurgy as [C] from A5's [I]. Corollaries C1–C5 are tiered appropriately. Execution surface correctly instructs [I]/[C] flagging.

**No action required.**

---

### F7 — CLEAN: ORGANISM_RUNTIME_TRUTH.md maturity discipline

**File:** `02_SKYZAI/01_NOOSPHERE/ORGANISM_RUNTIME_TRUTH.md`
**Assessment:** EXEMPLARY. The document is self-consciously [I] in its header. The §6 "acceptable now" vs. "not acceptable yet" list is a model of honest capability disclosure. The §5 maturity summary and honest phrase ("Adaptive pulse with brain, clean memory, and durable Docker body, but still lacking full voice, hands, and healing") is exemplary anti-overclaim.

**No action required.**

---

### F8 — CLEAN: Definitive Book AGENTS.md anti-K2-substitution clause

**File:** `01_EMERGENTISM/08_FRAMEWORK_SUPPORT/05_SYNTHESIS/07_DEFINITIVE_ONE_BOOK/AGENTS.md`
**Assessment:** CLEAN. The Non-Negotiables section explicitly reads: "Do not let AI become K2 signer, guru, priest, final authority, or unbounded oracle." This is the strongest possible anti-capture clause. The AI/K2 and anti-capture discipline are correctly maintained in the Build And Check section.

**No action required.**

---

### F9 — CLEAN: 01_EVIDENCE_TIER_CALIBRATION.md tier definitions

**File:** `02_SKYZAI/01_NOOSPHERE/10_AGENTS/20_OPERATIONALIZED/01_EVIDENCE_TIER_CALIBRATION.md`
**Assessment:** CLEAN. Shared tier baseline is rigorous and correctly cross-referenced per L-level. L1 correctly limits to [A]/[B] for direct flags or verified receipts. The hard rule "No agent may promote [I] or [C] to [A]/[B]" is present. Receipt minimum requires a kill criterion before L4 execution.

**No action required.**

---

### F10 — CLEAN: No η > 0 extraction patterns detected

**Files checked:** `04_ECONOMICS.md`, `00_CONSTITUTIONAL_ECONOMICS.md`, `06_AGENTS.md`, `ORGANISM_RUNTIME_TRUTH.md`
**Assessment:** No η > 0 patterns found. All economics documents correctly apply `η = 0` as structural (not ethical) constraint. The phrase "enables capital efficiency without introducing extraction" (04_ECONOMICS.md:78) and "The separation IS `η = 0` at the monetary layer" (04_ECONOMICS.md:195) are correct structural language. Flow and Vault mechanics are correctly described as target-state until frozen claims clear.

**No action required.**

---

### F11 — CLEAN: No K2-signer substitution detected

**Files checked:** All 16 files
**Assessment:** [B/I] No AI-as-final-authority language found in the dated audit pass. The phrase "APU suggests; K2 decides" is maintained consistently. K2 enforcement in code is described as a runtime mechanism (not AI authority). The expanded warning diagnoses the capture risk. The Anti-A-Brahmism disclaimer scopes structural analysis away from theological claims.

**No action required.**

---

### F12 — CLEAN: No [I] or [C] claims presented as [A], [B], or [S] in high-visibility surfaces

**Files checked:** `00_INDEX.md`, `06_AGENTS.md`, `README.md`, `AGENTS.md`, `00_ACTIVE_CLAIMS.md`
**Assessment:** `00_INDEX.md` correctly carries [I] frontmatter. `06_AGENTS.md` correctly carries [I] frontmatter. The public README describes filesystem reorganization (a [B] verified repository fact) correctly. `00_ACTIVE_CLAIMS.md` is a coordination protocol, not a claims document. No high-visibility surface conflates interpretive or conjectural material with established, verified, or structural claims.

**No action required.**

---

## Severity Summary

| Finding | Severity | Type |
|---------|----------|------|
| F1 VMOSK "decades" mislabel | Low | Staleness / typographic inconsistency |
| F2 SPECTRE cascade in Enterprise tier | Medium | Evidence-tier drift in product feature description |
| F3 Revenue Model status ambiguity | Low | Design vs. operational status unclear at row level |
| F4 Constitutional Economics frontmatter | Informational | Ambiguity but no actual tier inflation |
| F5 Steel Thread | CLEAN | — |
| F6 Seven Axioms | CLEAN | — |
| F7 Runtime Truth | CLEAN | — |
| F8 Definitive Book anti-K2 clause | CLEAN | — |
| F9 Evidence Tier Calibration | CLEAN | — |
| F10 η > 0 extraction | CLEAN | — |
| F11 K2 substitution | CLEAN | — |
| F12 [I]/[C] as [A]/[B]/[S] overclaim | CLEAN | — |

**Net verdict:** The corpus is in strong discipline. The three findings (F1–F3) are minor. F2 is the only one requiring active correction. F1 and F3 are staleness/status-label issues that should be addressed but do not constitute capture.

---

## Recommended Fixes

1. **`01_EMERGENTISM/11_UPLINK/00_CORE/06_AGENTS.md` line 106:** [I] Change VMOSK table `| V | Genotype | Decades | ...` to `| V | Genotype | Constitutional | ...` for the cell value. The "Decades" label conflicts with the parenthetical "(immutable)" and the "Changes only under existential crisis" wording.

2. **`01_EMERGENTISM/11_UPLINK/00_CORE/04_ECONOMICS.md` §ASSURE Phase 3:** Downgrade "SPECTRE cascade against client data" to include [I] status flag and clarify it is Tier-1 target, not current operational reality. Current text reads as [S] (operational product feature); it should read as [I] (design direction pending real-network receipts).

3. **`01_EMERGENTISM/11_UPLINK/00_CORE/04_ECONOMICS.md` §6 Revenue Model:** Add a "Design" label or per-row status flag to the ASSURE/INSURE/ENSURE revenue table to clarify that SKY-denominated flows and the phi-split diagram describe target-state, not current operational reality, consistent with how Sections 2 and 3 mark "FROZEN AS LIVE CLAIM" on target-state rows.

---

## Escalation

No constitutional contradiction detected. No η > 0 pattern. No K2-substitution language. No [C] claims presented as [A]/[B].

**F2** (SPECTRE cascade in Enterprise tier) should be escalated to L2/L3 for pattern-check against other product surfaces — whether similar "Tier-1 design described as operational feature" drift appears elsewhere in the L4 application layer. If a pattern emerges, flag it to L4.

---

## Notes for L2 Śūdra Explorer

After this audit:
- F2 should be checked against: `02_SKYZAI/01_NOOSPHERE/07_PWAs/skyzai_org/PR_FAQ.md`, `02_SKYZAI/01_NOOSPHERE/07_PWAs/circle/PR_FAQ.md`, and any public-facing product marketing surfaces for similar Tier-1/operational drift.
- The SPEC TRE Tier-1 graduation criteria in `02_SKYZAI/01_NOOSPHERE/02_ORGANS/Skyzai/spec/spectre/610_TIER_GRADUATION_ENFORCEMENT.md` should be used as the canonical benchmark for when "SPECTRE cascade" language becomes honest.

Zero-Sum Resolution Equation
