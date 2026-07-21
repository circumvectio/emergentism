---
rosetta:
  primary_level: L4
  primary_column: Philosophy
  operator: "Arjuna ⚔"
  tier: "Executive"
  regime: "Kṣatriya"
  register: "[I/S]"
  canonical_phrase: "Rights, duties, authorization, and due process"
status: "ACTIVE — Kintsugi value and authorization owner"
evidence_tier: "[I] normative/legal translation; [S] typed authorization contract"
date_repaired: 2026-07-20
original_head_blob: 7b8a0676f441449a71d7b156b3dbdc4950d0b6d0
---

# Rights, Duties, Authorization, and Due Process

This is an Emergentist normative translation `[I]`, not legal advice, positive
law, private enforcement authority, or a deduction of rights from geometry.

## 1. Directional consistency

The value owner fixes the arrows:

```text
morals:  individual -> whole     (i -> H)
ethics:  whole -> individual     (H -> i)
```

Accordingly:

- a **right** is read as an ethical claim on the whole to protect an individual;
- a **duty** is read as a moral claim on an individual concerning the whole.

Neither label settles a conflict by itself. A valid evaluation also requires a
bearer-complete Justice predicate, the declared horizon and baseline, consent,
rights, distribution, uncertainty, reversibility, and observed consequence.
`η=0`, `Φ`, `V`, or aggregate `ΔP` alone is never sufficient.

## 2. AuthorizationEnvelope `[S]`

A consequential act is accountably authorized only through a complete typed
envelope:

```text
AuthorizationEnvelope := {
  principal,
  mandate,
  scope,
  consent,
  custody,
  expiryOrRevocation,
  contestPath,
  actor,
  consequenceBearerIds: NonEmpty Unique[BearerId]
}
```

For a valid consequential commitment, `consequenceBearerIds` must cover the
complete affected-bearer set in the evaluation contract. A supplied but partial
or defective envelope is `invalid`; no supplied envelope is `absent`. A
`not_required` assessment is inhabited only for a declared non-consequential
scope. Authorization is permission/accountability, not truth, causal power, or
proof that the outcome will be good.

The accountability question is:

> Who authorized the consequence, who acted, who bears it, and how can it be
> contested or revoked?

## 3. Rights and duties under Justice `[I]`

A proposed right or duty must name every affected bearer, not merely one
individual and one convenient collective proxy. Aggregate gains cannot
compensate for destroying a bearer.

```text
right-valid(a) only if the H->i protection is bearer-complete under J^R
duty-valid(a)  only if the i->H contribution is bearer-complete under J^R
```

Rights without reciprocal cost accounting can externalize harm. Duties without
rights, consent, and exit can become servitude. This is why the two vectors are
conjunctive under Justice rather than substitutes.

## 4. Due process as a feedback discipline `[I/S]`

```text
notice -> evidence -> hearing -> decision -> proportionate act
       -> commitment receipt -> outcome receipt -> review/appeal/repair
```

At minimum:

1. **Notice:** affected parties can identify the claim and proposed act.
2. **Evidence:** the factual basis is inspectable at its actual tier.
3. **Hearing and contest:** rival accounts can be stated before constraint.
4. **Proportionality:** scope and means answer the proved problem.
5. **Receipts:** intention/authorization and world outcome remain separate.
6. **Review:** error can change model, selector, remedy, and precedent.
7. **Revocation or exit:** continued participation is not presumed where a safe
   and just exit is possible.

The mythic “immune response” is only an optional Rosetta mnemonic `[I]`. It
never authorizes punishment, coercion, vigilantism, or classification of people
as demons, castes, or threats.

## 5. Failure conditions

The application fails if it:

- reverses the moral/ethical arrows;
- omits an affected bearer or hides payer/beneficiary;
- calls a partial envelope valid;
- treats consent as irrevocable or collective purpose as self-authorizing;
- collapses commitment and outcome receipts;
- converts an aggregate gain into a moral verdict;
- treats `Φ`, `V`, `ΔP`, `η`, a Rosetta row, or “Dharma” as sufficient evidence.

## Kintsugi seam

The predecessor reversed the settled moral/ethical labels, omitted the
AuthorizationEnvelope it was cited to own, and treated a small vocabulary as a
sufficient legal test. Those claims are superseded. Its original remains
recoverable at Git blob `7b8a0676f441449a71d7b156b3dbdc4950d0b6d0`.

## Read with

- [Objective Morals and Ethics](00_OBJECTIVE_MORALS_AND_ETHICS.md)
- [Power-Max](../../05_COSMOLOGY/03_FORMAL_SYSTEM/08_EFR_POWER_MAX_LEMMA.md)
- [Burri Rules](../../05_COSMOLOGY/00_THE_BURRI_RULES.md)
- [The Honest Position](../../02_EPISTEMOLOGY/01_EVIDENCE_TIERS/00_THE_HONEST_POSITION.md)
