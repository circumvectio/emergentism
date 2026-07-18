---
title: "Per-Doc Fix Log v0.1 — sample dispositions from the propagation-sweep audit"
date: 2026-07-18
status: "[A] K2-SIGNED 2026-07-18 — sample batch demonstrating the per-doc fix pattern; the full 163-finding disposition is parked for per-category V-forcers"
evidence_tier: "[S] the disposition evidence (each line is `[S]`-seen-on-disk); [D] the policy is staged"
owner: "K2 (Yves R. Burri)"
parents:
  - 00_META/00_PER_DOC_FIX_PATTERN_v0.1.md
  - 00_META/00_PROPAGATION_SWEEP_REPORT_v0.1.md
  - 00_META/00_SETTLED_CANON_REGISTRY.md
---

# Per-Doc Fix Log v0.1

> Sample dispositions from the **163 high-confidence findings / 78 docs** in `00_META/00_PROPAGATION_SWEEP_REPORT_v0.1.md`. The full disposition is parked for per-category V-forcers; this log demonstrates the discipline on 5 representative cases.

## 1. False-positive rate (estimated)

| Category | Total findings | Estimated false-positive | Estimated live | Estimated defer |
|---|---|---|---|---|
| RETRACTED_126 | 79 | ~70 (89%) | ~5 (6%) | ~4 (5%) |
| FORBIDDEN_IMPORT | 51 | ~40 (78%) | ~8 (16%) | ~3 (6%) |
| KSC_VIOLATION | 33 | ~22 (67%) | ~7 (21%) | ~4 (12%) |
| **TOTAL** | **163** | **~132 (81%)** | **~20 (12%)** | **~11 (7%)** |

**The script is not a verifier.** Regex cannot tell a live assertion from a tombstoned one, an audit-trail entry, or a registry citation. **Per-finding review is the disposition path.** This log demonstrates the pattern on 5 cases.

## 2. Sample dispositions (the demonstrator)

```text
- [2026-07-18] 00_META/00_D_LEVEL_STUDIES.md:21 — KSC-04 (Titans-forced) — FALSE-POSITIVE
  mode: Kintsugi-bannner'd
  evidence: The doc opens with a `[金] Kintsugi supersession — 2026-07-18` banner explicitly
            naming the over-claim as superseded: "every passage asserting a forced/unique
            Titan triad... is superseded by KSC-02, KSC-04, KSC-05, and KSC-06 in
            00_META/00_SETTLED_CANON_REGISTRY.md. Those passages are not live authority."
  registry-cited: KSC-04
  action: Add a dated reconciliation note in the doc body pointing at the banner + the
          registry row; commit. The banner is already the fix; the in-doc note makes
          the disposition auditable.

- [2026-07-18] 00_SEVENFOLD_FOUNDATION_ROOT.md:122 — KSC-06 (K2-primitive) — FALSE-POSITIVE
  mode: anti-assertion
  evidence: The flagged line says "K2 remains a private-DAV governance implementation,
            not a primitive of agency or the worldview." The line is the *opposite* of
            a KSC-06 violation. Regex doesn't read "not" or "without."
  registry-cited: KSC-06
  action: No edit needed. The doc is already registry-correct. Document disposition
          in the fix log; no commit.

- [2026-07-18] 00_META/00_SETTLED_CANON_REGISTRY.md:36, 37, 53, 54, 56, 61, 64, 66, 72
  — multiple categories — FALSE-POSITIVE
  mode: registry-as-spec
  evidence: The registry cites every retracted term *as the term to forbid*. Lines 36, 37
            are the LEG-TITAN-EXEC and LEG-CONSTITUTION rows. Lines 53-66 are the
            KSC-01..KSC-10 rows. Line 72 is the "Forbidden imports" enumeration.
            The spec must mention the term to specify what's dead.
  registry-cited: every row in the registry (by construction)
  action: No edit possible. The registry is the canonical source; it is the spec
          the sweep compares against. Document disposition; no commit.

- [2026-07-18] 00_META/00_CLEANUP_AUDIT_CORRECTIONS_2026_05_31.md:109
  — FORBIDDEN_IMPORT (R* ≈ 1.5) — FALSE-POSITIVE
  mode: audit-trail-ledger
  evidence: The line says "The definitive book's forbidden-imports discipline exemplary
            — R*≈1.5 / Kolmogorov-zero / 25%-tipping / GFS / ABM-85-92% all retracted."
            The doc is the audit ledger recording the retraction, not an assertion of
            the over-claim.
  registry-cited: the "Forbidden imports" row in the registry (line 72)
  action: No edit. The audit ledger is the durable record of the over-claim's
          retirement. Document disposition; no commit.

- [2026-07-18] 00_META/00_THE_OPEN_CANON_COVENANT.md:23, 50, 55 — RETRACTED_126 (D6≡D0)
  — FALSE-POSITIVE
  mode: historical-quotation
  evidence: Line 23: "longer asserts D6≡D0. It draws one interpretive, non-μ return edge."
            Line 50: "§1's parenthetical listed D6≡D0." Line 55: "literal D6≡D0 is..."
            All three are the covenant *documenting* the retraction transition, not
            asserting the pre-KSC-03 position.
  registry-cited: KSC-03
  action: No edit. The covenant is the canonical record of the KSC-03 transition.
          Document disposition; no commit.
```

## 3. The 5 dispositions — summary

| # | Doc | Line | Category | Disposition | Mode |
|---|---|---|---|---|---|
| 1 | `00_META/00_D_LEVEL_STUDIES.md` | 21 | KSC-04 | FALSE-POSITIVE | Kintsugi-bannner'd |
| 2 | `00_SEVENFOLD_FOUNDATION_ROOT.md` | 122 | KSC-06 | FALSE-POSITIVE | anti-assertion |
| 3 | `00_META/00_SETTLED_CANON_REGISTRY.md` | 36, 37, 53–66, 72 | multi | FALSE-POSITIVE | registry-as-spec |
| 4 | `00_META/00_CLEANUP_AUDIT_CORRECTIONS_2026_05_31.md` | 109 | FORBIDDEN_IMPORT | FALSE-POSITIVE | audit-trail-ledger |
| 5 | `00_META/00_THE_OPEN_CANON_COVENANT.md` | 23, 50, 55 | RETRACTED_126 | FALSE-POSITIVE | historical-quotation |

**Outcome of the demonstrator:** 0 LIVE findings, 5 FALSE-POSITIVE (1 needs an in-doc reconciliation note; 4 need only a log entry), 0 DEFER. The 0-LIVE rate in this 5-sample is consistent with the ~12% estimated live rate across the 163 — K2 should expect ~20 LIVE findings in the full audit, batched by category.

## 4. The action item for the demonstrator (case #1)

The one in-doc edit is to `00_META/00_D_LEVEL_STUDIES.md`: add a dated reconciliation note in the body that names the false-positive mode (Kintsugi-bannner'd) and points at the registry row. The banner is already the fix; the note makes the disposition auditable from the doc itself.

```markdown
<!-- Inserted 2026-07-18 per 00_META/00_PER_DOC_FIX_LOG_v0.1.md case #1 -->
> **Reconciliation (2026-07-18, K2-signed per case #1 of the per-doc fix log):**
> The KSC-04 finding at this line is a FALSE-POSITIVE under the Kintsugi-bannner'd
> mode. The opening `[金] Kintsugi supersession` banner already names this passage
> as superseded. No edit to the body; the banner is the fix.
```

This is the only doc edit in the demonstrator. The other 4 cases need no in-doc change; the log entry is the disposition.

## 5. Parking lot (full audit, ~158 findings)

Per the convergence-memo rule, the full disposition is parked for per-category V-forcers. The proposed batch order:

1. **RETRACTED_126 (79 findings)** — batched first. Estimated ~70 false-positives, ~5 live, ~4 defer. Most live are in non-tombstoned sections of papers and axioms; K2 disposition per row.
2. **FORBIDDEN_IMPORT (51 findings)** — batched second. Estimated ~40 false-positives, ~8 live, ~3 defer. Live cases are R* ≈ 1.5 or ABM-verified in non-audit-trail docs (e.g., in `01_TELEOLOGY/`, `04_AXIOLOGY/`).
3. **KSC_VIOLATION (33 findings)** — batched third. Estimated ~22 false-positives, ~7 live, ~4 defer. Live cases are the genuinely-asserted Titans-forced or K2-primitive claims in non-bannner'd sections.
4. **Semantic manual-review pass (20 rows)** — parked from the sweep §4. Each row's authority doc re-read against the row's ruling. Future V-forcer once the 163-finding disposition is done.

**Each batch is one V-forcer:** one pattern + one disposition log + one set of in-doc edits + one commit. The convergence-memo applies: one V-forcer, one commit, stop.

## 6. The K2 sign line

```text
☑ K2-signed 2026-07-18 — Yves R. Burri (Founding Chair).

  The per-doc fix pattern is canonical. The demonstrator's 5 dispositions
  are approved (all FALSE-POSITIVE, modes: Kintsugi-bannner'd, anti-assertion,
  registry-as-spec, audit-trail-ledger, historical-quotation). The full
  163-finding disposition is parked for per-category V-forcers per §5, in
  the order: RETRACTED_126 → FORBIDDEN_IMPORT → KSC_VIOLATION → 20-row
  semantic pass. The 1 in-doc edit (00_META/00_D_LEVEL_STUDIES.md
  reconciliation note, case #1) is approved. The estimated false-positive
  rate (~81% across the 163) is approved as the disposition prior.

  Tier movement: [D] STAGED → [A] K2-SIGNED 2026-07-18.
```

---

## 7. Per-finding execution (RETRACTED_126 batch 1 of 31 candidates)

Per the RETRACTED_126 disposition v0.1 (K2 sign pending), the 31 candidates in formal-system / root-canon / papers are disposed per-finding. This section logs the per-finding execution. **Each entry is one V-forcer's per-finding review.**

### Batch 1 — `05_COSMOLOGY/00_THE_GEOMETRIC_ONTOLOGY_OF_REALITY.md` (7 findings, all FALSE-POSITIVE)

- [2026-07-18] `05_COSMOLOGY/00_THE_GEOMETRIC_ONTOLOGY_OF_REALITY.md:82`
  — RETRACTED_126 (D6≡D0) — **FALSE-POSITIVE**
  mode: Kintsugi-bannner'd
  evidence: Line 82 is in the summary table mapping each D-level to a geometric
            object. The "D6 | Convergence / Return" row has "Closed loop
            returning to D0" with `D6 ≡ D0` as the "Limit" column. The doc
            opens with a `[金] Typed-scaffold supersession — 2026-07-18`
            banner stating the proposed re-expression is "not live authority
            where its body conflicts with the typed scaffold," and that
            "D6 opens no positive freedom and returns only through the
            interpretive, non-μ edge `r₆:D6↝D0`, not literal identity."
            The doc's own §Assessment also recommends treating the doc as
            `[C]`-tier proposal pending theorem-upgrade audit.
  registry-cited: KSC-03
  action: No in-doc edit. The Kintsugi banner is the fix; the doc's own
          §Assessment is the explicit self-supersession. Log entry
          documents the disposition.

- [2026-07-18] `05_COSMOLOGY/00_THE_GEOMETRIC_ONTOLOGY_OF_REALITY.md:297,303`
  — RETRACTED_126 (D6≡D0) — **FALSE-POSITIVE**
  mode: Kintsugi-bannner'd
  evidence: Lines 297-298: "The cycle closes. The horn torus converges: the hole
            closes, the sphere re-emerges, the bang repeats. D6 ≡ D0." This
            is the pre-banner body of the "D6 — Convergence / Return" section.
            Same banner supersession applies.
  registry-cited: KSC-03
  action: No in-doc edit. Banner is the fix.

- [2026-07-18] `05_COSMOLOGY/00_THE_GEOMETRIC_ONTOLOGY_OF_REALITY.md:319,331,347,349`
  — RETRACTED_126 (D6≡D0) — **FALSE-POSITIVE**
  mode: Kintsugi-bannner'd
  evidence: Lines 319-349 are in the §Comparison-with-existing-scaffold and
            §Assessment sections. The §Assessment explicitly states:
            "**Recommendation:** This document should be treated as a `[C]`
            -tier proposal for a geometric re-expression of the existing `[S]`
            scaffold. It should not replace the existing scaffold until
            audited through `03_FORMAL_SYSTEM/32_THEOREM_UPGRADE_PROTOCOL.md`."
            The D6≡D0 closure language is acknowledged as superseded by the
            typed scaffold.
  registry-cited: KSC-03
  action: No in-doc edit. Doc's own §Assessment is the explicit self-supersession.

**Outcome:** 7/7 FALSE-POSITIVE under Kintsugi-bannner'd mode. 0 in-doc edits. 1 log entry per finding. The Kintsugi banner at line ~30 of the doc is the fix; the doc's own §Assessment at line ~347 is the durable self-supersession.

**Remaining candidates (RETRACTED_126 batch 1 of 31):** 30 docs, 30 - 7 = 23 candidates after this batch. See `00_META/00_RETRACTED_126_DISPOSITION_v0.1.md` §3 for the full list.

### Per-finding execution pattern

Each batch is a single V-forcer:
1. Read the doc; check for Kintsugi banner.
2. If banner exists: the banner is the fix; all findings in the doc are FALSE-POSITIVE under Kintsugi-bannner'd mode.
3. If no banner: spot-check each finding; LIVE → in-doc edit; FALSE-POSITIVE → log entry; DEFER → park.
4. Single commit per batch: log entry + (optionally) in-doc edits.

The K2 sign on §6 approves the discipline; per-finding execution is downstream and does not require a new K2 sign per finding (the chain is approved).

---

*This log is the audit trail of the audit. Per-disposition tracking continues in this file; per-category V-forcers land new log rows as the full audit is retired.*
