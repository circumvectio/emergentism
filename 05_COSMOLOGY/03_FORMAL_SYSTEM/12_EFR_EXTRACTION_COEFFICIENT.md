---
rosetta:
  primary_level: L5
  primary_column: Philosophy
  operator: "Brahmā ○"
  tier: "Executive"
  regime: "Brāhmaṇa"
  register: "[S/I]"
  canonical_phrase: "Extraction is an observed, scoped transfer or harm — not a moral verdict by itself"
title: "The Extraction Observation Contract"
status: "ACTIVE KINTSUGI SUCCESSOR"
evidence_tier: "[S] measurement contract; [I] role inside the declared Justice model."
supersedes_blob: "2d560efa5ceb7fd1d203d64893c19f9778f41ae3"
---

# The Extraction Observation Contract

> **[金] Crack:** older versions used the same `η` for an
> extraction/contribution ratio, a system rate, a strategic move, a moral
> category, and a categorical ecological boundary. Those quantities are not
> interchangeable. **Repair:** `etaObserved` is a scoped observation; every
> other ratio receives its own name.

## 1. Canonical record

```text
ExtractionObservation := {
  boundary,
  horizon,
  affectedBearerIds,
  payerIds,
  beneficiaryIds,
  measuredTransfers,
  measuredHarms,
  baselines,
  units,
  uncertainty,
  protocol,
  etaObserved: Number | unknown
}
```

`etaObserved` is nonnegative under its declared normalization. `0` means no
extraction was observed within that scope and detection limit. A positive
value means the protocol measured a non-consensual transfer, hidden rent,
uncompensated cost, or bearer harm. `unknown` is required when coverage or
measurement is insufficient.

The normalization may be a bounded magnitude, rate, vector norm, or explicit
binary flag. Applications must publish the mapping. Values from different
boundaries, horizons, or protocols cannot be compared without a validated
conversion.

## 2. Retired overload

If a study needs the legacy ratio

\[
\frac{\text{extraction}}{\text{contribution}},
\]

it must call it `r_take_give`, state its units and zero-denominator behavior,
and keep it separate from `etaObserved`. `r_take_give=1` means equality of two
declared quantities; it is not “good,” “balanced,” or `η=0`.

Predator–prey stability, Lotka–Volterra cycles, substrate regeneration, and
uncoupled growth have their own dynamical variables. None follows from the
bare observation record, and none derives moral categories.

## 3. Relation to Justice

The prospective Justice envelope requires a credible expectation of
non-extraction. Retrospective Justice requires `etaObserved=0` plus complete
bearer coverage, accountable authorization, consent, custody, consequence,
reversibility where possible, exit, contest, and non-destruction of every
affected bearer.

Therefore:

```text
etaObserved = 0  is necessary but insufficient for Justice.
etaObserved > 0  defeats Justice for the declared scope.
etaObserved = unknown prevents a positive Justice classification.
```

No empirical scalar can, by itself, convert an `is` into an `ought`. The moral,
ethical, and syntropic predicates remain explicit constructions in the
canonical value owner.
