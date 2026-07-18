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

*This log is the audit trail of the audit. Per-disposition tracking continues in this file; per-category V-forcers land new log rows as the full audit is retired.*
