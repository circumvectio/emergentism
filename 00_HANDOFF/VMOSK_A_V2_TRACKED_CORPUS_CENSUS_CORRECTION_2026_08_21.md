---
title: "VMOSK-A v2 tracked-corpus census correction"
status: "[D] dated correction — unsigned; the signed v2 body remains preserved"
date: 2026-08-21
evidence_tier: "[S] Git-tree counts and commands; [I] KPI disposition"
type: control-correction
scope: "The `~476k-file tree` KPI as a claim about Git-tracked paths"
may_sign: false
may_authorize: false
authority_effect: none
source:
  - VMOSK_A_v2_2026_07_31.md
  - 00_HANDOFF/FULL_CORPUS_ROSETTA_AUDIT_2026_08_21.md
---

# VMOSK-A v2 tracked-corpus census correction

This is a dated additive correction to the KPI wording in
[`VMOSK_A_v2_2026_07_31.md`](../VMOSK_A_v2_2026_07_31.md). It does not amend,
re-sign, or erase that signed body.

## Reproducible result

The v2 phrase “~476k-file tree” is not reproducible as a census of Git-tracked
paths:

```text
git ls-tree -r --name-only 577816880d7c60a99b2377efc0ffcdcc76118518 | wc -l
# 3394

git ls-tree -r --name-only ae062bf68e67751ba21bfcc777acbfd504746e76 | wc -l
# 3832
```

The first commit is the signed-v2 era revision used for this correction. The
second is the frozen full-corpus audit revision. A later observed revision,
`bd9d80f9f3088dbf83588a57884ce04608c321bf`, contains 3,837 tracked paths;
that observation does not alter the frozen audit count.

These counts do **not** measure untracked working files, external worktrees,
archives outside the repository, filesystem objects, document pages, generated
members, or a separately defined corpus census. No reproducible source for the
476k number was found in the tracked history reviewed here.

## Disposition

- The `~476k-file tree` statement is **refuted only as a Git-tracked-path KPI**.
  It must not be reused as proof that the corpus has already crossed an
  error-catastrophe threshold.
- O12 remains **UNBUILT**. The duplication rate and copying-fidelity/mutation
  estimate are still unmeasured, so the claimed “already at or past” conclusion
  is suspended.
- The fidelity-first strategy may remain a prudent selected direction, but its
  biological urgency must be supported by a declared denominator, a measured
  duplication method, an explicit fidelity estimate, a time series, and a
  threshold rule before it can trigger a document freeze.

## Repair path

Before the KPI is used again, publish a bounded census contract that names:

1. the population (for example, tracked paths at a pinned commit);
2. inclusion/exclusion rules for generated, archived, and binary material;
3. the duplication detector and false-positive treatment;
4. the mutation/fidelity proxy, measurement interval, and uncertainty; and
5. the exact threshold and action it may trigger.

Until then, this correction—not the numerical inference in the signed body—is
the controlling reading of the tracked-corpus KPI.
