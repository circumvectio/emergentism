---
rosetta:
  primary_level: L5
  primary_column: Philosophy
  operator: "Brahmā ○"
  tier: "Executive"
  regime: "Brāhmaṇa"
  register: "[I] reversible comparison specification"
  canonical_phrase: "Rosetta R10 supplement — formalize the projection, not the tradition"
title: "Rosetta R10 Supplement: Greek Comparison Specification"
status: "ACTIVE — Kintsugi-repaired optional projection; non-canonical for Greek philosophy"
evidence_tier: "[I] projection only; source facts inherit the evidence status of D19a"
source_custody:
  original_git_blob: ac6b28471a5a568186eee2e971832ef0f71f6407
---

# Rosetta R10 Supplement: Greek Comparison Specification

> **[金] Crack.** The predecessor converted Greek ethical vocabulary into exact
> Burri coordinates, announced ancient disputes “resolved,” made moral claims
> theorems, and promised personal coordinate measurement.
>
> **Repair.** A Rosetta projection is a typed hypothesis about a relation between
> descriptions. It neither settles the source tradition nor turns an
> interpretive vocabulary into a physical or moral measurement scale.

## Projection interface

For a source concept `g`, the Greek projection must return a record:

```text
ρ_Greek(g) = {
  sourceContext,
  sourceClaim,
  sourceEvidence,
  targetRelation,
  targetTier = [I],
  alternatives,
  loss,
  roundTripCheck,
  killCriterion
}
```

The target relation may say, for example, that a contextual account of
temperance can be **compared with** a balance diagnostic, or that an account of
practical wisdom can be **compared with** fallible selection under constraint.
It may not replace the source claim with `B=1`, `φ=1`, `ν=1`, or an operator
name.

## Mandatory type rules

1. A word is not a coordinate.
2. A virtue is not a chart extremum.
3. A mythic or ethical consequence is not a restoring physical force.
4. `φν=1` is an analytic chart identity, not a historical conservation law.
5. A shared diagram does not adjudicate Heraclitus, Parmenides, Plato,
   Aristotle, or the Stoics.
6. A moral recommendation requires the declared Justice premise; it does not
   become a theorem through formal notation.
7. Personal `Φ`, `V`, or `B` values are model-dependent reports. They are not
   validated measurements of virtue, truth, flourishing, or a person’s worth.

## Bounded comparison examples

| Source question | Permitted target relation `[I]` | Forbidden conversion |
|---|---|---|
| How do constancy and change relate? | compare invariant constraints with trajectories | “Parmenides is the invariant; Heraclitus is motion; debate solved” |
| What makes a disposition excellent? | compare situated calibration with conditional balance | “virtue is exactly `B=1`” |
| How does practical judgment guide action? | compare deliberation with model, means, commitment, and receipt | “phronēsis is an operator that guarantees the right move” |
| What follows excess or overreach? | compare social, ecological, or psychological feedback | “Nemesis is a force restoring `φν=1`” |
| What does self-knowledge require? | compare reflective practice with fallible model revision | “measure your true coordinates and navigate to the equator” |

## Round-trip requirement

A valid projection must survive this test:

```text
source concept
  ──ρ_Greek──▶ target relation
  ──ρ_Greek⁻¹──▶ source paraphrase
```

If the returned paraphrase erases historically important distinctions, imports
Emergentist terms as if the source used them, or makes rival interpretations
invisible, the projection fails. A successful round trip shows only disciplined
translation; it does not show identity or proof.

## Practical use

This supplement can help a reader generate questions:

- Which capacity is missing from the present action?
- Which constraint or bearer is absent from the model?
- Does the proposed “balance” depend on weights, prices, roles, or context?
- What did the source author actually claim?
- What would the Emergentist projection lose if removed?

The Soul Loop may then record model, commitment, outcome, and correction. It
cannot compute moral worth from a latitude.

## Kill criteria

Kill or withdraw a row if it:

- cannot cite the source context;
- assigns an exact coordinate without an operational measurement model;
- presents an Emergentist verdict as the source tradition’s conclusion;
- transfers evidence through resemblance;
- moralizes a person, culture, deity, or operator; or
- remains equally compatible with contradictory source interpretations.

## One line

> Philosophy does not become geometry here. Geometry supplies one optional
> comparison surface; philosophy keeps its plurality, history, arguments, and
> right to refuse the projection.

## Execution surface

- **Canonical path:**
  `08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/D_SERIES_ROWS/D19b_ROSETTA_R10_GREEK_FORMALIZATION.md`
- **Companion:** `D19a_ROSETTA_R10_GREEK_PHILOLOGY.md`
- **Removal test:** deleting both Greek rows changes no axiom, theorem, Burri
  rule, or ethical decision procedure.
