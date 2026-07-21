---
title: "EFR methodology — bounded completion contract"
status: "ACTIVE KINTSUGI SUCCESSOR"
evidence_tier: "[S] internal method; [C] external fit"
date: 2026-07-20
---

# EFR methodology · What “complete” means

Methodological completeness means only that a candidate claim exposes the
records needed to test it. It does not mean the ontology is necessary,
irreducible, empirically complete, or externally calibrated.

Every candidate `MuCrossing` must declare:

```text
id, source, target, triggerType, saturatedRegister, proposedNewFreedom,
saturationEvidence, lowerRegisterRecovery,
reductionStatus, evidenceTier, prediction, killCriterion
```

`μ₀` is `origin_aperture` with `saturatedRegister=null` and saturation evidence
`not_applicable`. `μ₁…μ₄` are `saturation_candidate` records and must name their
source register; absent evidence remains `not_yet_supplied`.

`reductionStatus` is one of `reduced`, `currently_unreduced`, or
`candidate_strong`. Missing reduction never upgrades the status. A successful
reduction reclassifies the crossing without destroying the scaffold.

Every cross-domain Rosetta projection states its preserved invariant and remains
at the lower supported tier. Every operational claim separates model token,
possible content, commitment, outcome, payer, beneficiary, and contest path.

The pre-repair methodology is recoverable at Git blob
`fda8b09283d45bd4a68701986f9bb157a717c0dc`.

**Kill criterion:** if the method allows a hypothesis to evade a failed test,
upgrade itself through analogy, or treat opacity as irreducibility, it is not
complete and must be repaired.
