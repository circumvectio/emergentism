---
title: "Per-Doc Fix Pattern v0.1 — the discipline for retiring the propagation-sweep audit"
date: 2026-07-18
status: "[D] draft — single V-forcer per the Release Doctrine Phase 0 #1 follow-on"
evidence_tier: "[S] the discipline surface; [D] the policy is staged"
owner: "K2 (Yves R. Burri). PRISM ≥2 takes over after the trigger."
parents:
  - 00_META/00_PROPAGATION_SWEEP_REPORT_v0.1.md
  - 00_META/00_SETTLED_CANON_REGISTRY.md
  - 00_META/00_THE_KINTSUGI_PROTOCOL.md
---

# Per-Doc Fix Pattern v0.1

> The propagation sweep v0.1 produced **163 high-confidence findings across 78 docs** (`00_META/00_PROPAGATION_SWEEP_REPORT_v0.1.md`). Most of these are *false positives* in the sense that regex cannot distinguish a live assertion from a meta-discussion of the retraction. **Per-finding review is the disposition path.** This document is the discipline for that review.

## 1. The three dispositions

For each finding, the disposition is one of three:

| Disposition | When | Action |
|---|---|---|
| **LIVE** | The doc asserts the over-claim as current truth (not in a tombstoned section, not quoting a retraction, not flagged with a Kintsugi supersession banner) | Edit the doc to the registry-correct language; cite the row; commit |
| **FALSE-POSITIVE** | The doc has already been repaired (Kintsugi banner, struck-through, historical quotation, audit-trail entry, or registry-citation of the retracted term as forbidden) | Add a dated reconciliation note in the doc body pointing at the registry row; commit |
| **DEFER** | The finding is contested, requires semantic review, or the fix would itself alter doctrine | Park in the fix log; per-row K2 disposition; future V-forcer |

## 2. The false-positive modes (read these first)

Most findings fall into one of these modes. **Read the doc + the line + 10 lines of context before deciding LIVE.**

1. **The registry itself** — `00_META/00_SETTLED_CANON_REGISTRY.md` cites every retracted term *as the term to forbid*. Lines 36, 37, 53, 54, 56, 61, 64, 66, 72 are spec-citation, not assertion. **Disposition: FALSE-POSITIVE** (already a row in the registry, by construction).
2. **Kintsugi-bannner'd docs** — e.g., `00_META/00_D_LEVEL_STUDIES.md` opens with a supersession banner explicitly saying the over-claims in the body are *not live authority*. **Disposition: FALSE-POSITIVE** (banner is the fix; the registry row names the doc as superseded).
3. **Audit-trail ledgers** — e.g., `00_META/00_CLEANUP_AUDIT_CORRECTIONS_2026_05_31.md`, `00_META/01_CORPUS_AUDIT_MANIFEST_2026_06_04.csv`. These are dated records of past over-claims. **Disposition: FALSE-POSITIVE** (the doc is the audit of the over-claim, not the over-claim itself).
4. **Historical quotations** — e.g., `00_META/00_THE_OPEN_CANON_COVENANT.md` quoting the pre-KSC-03 ruling for the contradiction. **Disposition: FALSE-POSITIVE** (the doc is documenting the *transition*, not asserting the pre-KSC position).
5. **Anti-assertions** — e.g., a doc saying "K2 remains a private-DAV governance implementation, **not** a primitive of agency" reads as the *opposite* of a KSC-06 violation to a regex scan. **Disposition: FALSE-POSITIVE** (regex doesn't read "not" or "without").
6. **Numbered papers under `02_THE_PAPERS/`** — many of these are historical or in-process drafts. Check the file's status block; papers with `[D]` (draft) are likely candidates for FALSE-POSITIVE if the over-claim is in the historical framing, LIVE if it's in a current-tense section.

## 3. The fix format

When the disposition is LIVE, the edit must:

1. **Cite the registry row.** Add a sentence: *"[Per `00_META/00_SETTLED_CANON_REGISTRY.md` row KSC-XX, superseded YYYY-MM-DD; the live ruling is ...]"*
2. **Use the registry-correct language.** Pull the wording from the row's "The ruling" cell, not from your paraphrase.
3. **Do not alter doctrine.** The fix is *to* the ruling, not *of* the ruling. The convergence-memo applies: ship the registry, don't refine it.
4. **Commit with a single-finding message body** that names the finding, the disposition, the registry row, and the diff.

When the disposition is FALSE-POSITIVE, the in-doc note must:

1. **Name the false-positive mode** (one of the six above).
2. **Cite the registry row or the Kintsugi banner** that already repairs the over-claim.
3. **Be dated** (K2 sign-line + ISO date).

## 4. The fix log

Per-disposition tracking lives at `00_META/00_PER_DOC_FIX_LOG_v0.1.md`. Each entry has:

```text
- [YYYY-MM-DD] <doc-path>:<line> — <category> — <disposition> — <registry-row-cited>
```

The log is the audit trail for the audit. K2 signs each row.

## 5. The escalation path

If a finding's disposition is ambiguous (e.g., the doc has both a Kintsugi banner *and* a live-tense section that re-asserts the over-claim), the disposition is **DEFER** with a one-line reason. The next V-forcer is a per-row semantic pass, batched by category.

If a finding's disposition is **LIVE** but the fix would alter doctrine (e.g., the doc's claim is what's actually being adjudicated), the disposition is **DEFER** and the doc is *not* fixed by this V-forcer. The fix is a doctrine-level ruling, not a per-doc edit.

## 6. The standing rule

> **The doctrine does not change because a doc lagged it. Repair the lagging doc *to* the ruling; never re-open the ruling because a doc disagrees.** (registry preamble)

The propagation sweep's value is that it names the *candidates*. The per-doc fix is the *execution*. K2 owns the execution; AI stages the edits and the log.

---

*This file is the discipline. The execution is per-finding, per-disposition, per-commit. The log is the audit trail. K2 signs each row of the log.*
