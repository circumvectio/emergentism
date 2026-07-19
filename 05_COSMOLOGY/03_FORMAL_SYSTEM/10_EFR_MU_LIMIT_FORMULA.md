---
rosetta:
  primary_level: L5
  primary_column: Philosophy
  operator: "Brahmā ○"
  tier: "Executive"
  regime: "Brāhmaṇa"
  register: "[S/C]"
  canonical_phrase: "THE μ-LIMIT CANDIDATE CONTRACT"
---

# The μ-Limit Candidate Contract

**Status:** Active — Kintsugi replacement, 2026-07-19
**Evidence:** interface `[S]`; each proposed natural crossing `[C]` until
operationally calibrated
**Purpose:** Say exactly what would make a `μ`-crossing more than a metaphor.

> **[金] Kintsugi tombstone.** The formula formerly occupying this path is
> preserved in Git blob `3b08cb743ebb0858d1e183bd0d6be506ee3ceecd` and is
> superseded. It sampled a normalization scalar, reversed the stable D4/D5
> modalities, and fused emergence, commitment, quantum measurement, and
> collapse. None of those operations are identical. The old notation must not
> be quoted as an active formula.

## 1. What `μ` means

`μ_n` names a **candidate emergence crossing**

```text
μ_n : D_n ⇢ D_(n+1)
```

in the modest sense that, beyond an operationally specified regime, a new
effective variable or freedom may be required for adequate description and
prediction. The dashed arrow is deliberate: `μ_n` is not yet a universal
mathematical operator with a known law.

The active scaffold declares five candidates only:

| ID | Crossing | Candidate newly effective freedom | Initial status |
|---|---|---|---|
| `μ₀` | `D0→D1` | distinction | `[C] currently_unreduced` |
| `μ₁` | `D1→D2` | relation/configuration | `[C] currently_unreduced` |
| `μ₂` | `D2→D3` | transformation/persistence | `[C] currently_unreduced` |
| `μ₃` | `D3→D4` | causal actuality, embodied action, record | `[C] currently_unreduced` |
| `μ₄` | `D4→D5` | counterfactual modeling, ranking, selection | `[C] currently_unreduced` |

No μ-labelled edge follows `μ₄`. The non-μ move `κ:D5→D6` marks reflexive/apophatic
closure, and `r₆:D6↝D0` is an interpretive, noncausal return.

“Matter, bond, life, mind, choice” may be proposed through a domain projection
`ρ_domain` `[I/C]`; those words are not the formal definitions above.

## 2. The required `MuCrossing` record

Every proposed crossing must instantiate:

```text
MuCrossing = {
  id,
  lowerRegister,
  upperRegister,
  systemBoundary,
  saturationVariable,
  threshold,
  thresholdEvidence,
  openedFreedom,
  lowerRecoveryMap,
  reductionStatus,
  evidenceTier,
  rivalModel,
  prospectivePrediction,
  killCriterion
}
```

The allowed reduction states are

```text
reductionStatus ∈ {
  reduced,
  currently_unreduced,
  candidate_strong
}
```

- `reduced` means a lower-register model plus bridge law recovers the observed
  upper behavior within the declared tolerance; the event remains emergence in
  the ordinary weak sense.
- `currently_unreduced` reports the present state of knowledge only.
- `candidate_strong` is permitted only when a prospective discriminator has
  defeated named lower-register rivals; it is still not proof of metaphysical
  irreducibility.

Missing reduction laws do not select the third state.

## 3. Operational saturation

Let `z_n:X_n→ℝ` be a domain-specific order parameter, `τ_n` a preregistered
threshold, and

```text
t* := inf { t : z_n(X_t) ≥ τ_n }.
```

Crossing the threshold is evidence for saturation only if all of the following
are specified before inspection:

1. why `z_n` measures the exhausted lower-register capacity;
2. why `τ_n` is not chosen after observing the outcome;
3. which upper-register variable should appear after `t*`;
4. which lower-only rival makes a different prediction;
5. how the lower behavior is recovered when the upper variable is removed or
   coarse-grained;
6. what observation kills the crossing claim.

Thus “freedom saturates and the next freedom opens” is the Emergentist
μ-hypothesis `[C]`, not a theorem and not a law saying that a crossing fires
automatically or only at saturation.

## 4. Lower-register recovery and constraint

For a proposed upper description `Y` over a lower state `X`, the record must
provide a recovery or coarse-graining map

```text
g_n : Y → X/~
```

and declare the tolerance within which lower-register behavior is reproduced.
When the upper level constrains lower evolution, admissibility must be
preserved:

```text
support(K_X^C) ⊆ support(K_X).
```

A higher-level description may reweight allowed trajectories; it may not create
a lower-law-forbidden one without evidence that the lower law was incomplete.

## 5. `μ` is not commitment

Counterfactual agency emerges in the upward candidate

```text
D4 actual --μ4⇢ D5 possible.
```

Enactment runs in the other direction through a distinct selector:

```text
χ_t : (X_t, Ω_t, M_t, V_t, U_t, G_t) → (a_t, q_t)
```

where `G_t` is the current selector/policy state and `q_t` is an immediate
commitment/action receipt. The environment then
returns a separate outcome receipt:

```text
(X_(t+1), r_(t+1)) ~ K_t(· | X_t, a_t, E_t)
```

and the Soul Loop updates model and selector:

```text
(M_(t+1), G_(t+1))
  = Loop(M_t, G_t, q_t, r_(t+1)).
```

`χ` does not turn a decision into a measurement, and the selector does not
manufacture its own consequence.

## 6. Model-mediated future influence

A modeled future is a present representation. Let `π_t` be the action
distribution induced by `χ_t`, `G_t`, and any declared selector randomization.
Unless independently manipulated by design, let
`Ω_t^(j)=Options_t(X_t,M_t^(j))`. Intervening on represented future content may
then change the present distribution of actions:

```text
π_t(a | do(M_t=M_t^(1)), X_t,Ω_t^(1),V_t,U_t,G_t)
  may differ from
π_t(a | do(M_t=M_t^(2)), X_t,Ω_t^(2),V_t,U_t,G_t).
```

This is the testable content of the mnemonic `F=M×A`, formally
`F_modelled:=M⋆A`.
It requires no physical signal from a future event to the present. The realized
future remains conditional on `K_t`, other agents, constraints, and chance.

## 7. Removable quantum correspondence `[C]`

Quantum theory is not part of the operational `μ` contract. If a Born-rule
example is useful, state it correctly for measurable `A`:

```text
𝔓_ψ(A) = ∫_A |ψ(s)|² dμ(s)
o ~ 𝔓_ψ
```

Normalization is `𝔓_ψ(Ω)=1`; it is not an outcome to sample. Everett's
relative-state formulation has no fundamental collapse. Copenhagen-family
actualization is interpretation-specific. Neither interpretation is an extra
spacetime dimension, and neither `μ` nor `χ` is quantum measurement.

Delete this entire section and the emergence, commitment, receipt, and Soul
Loop interfaces remain unchanged.

## 8. Verification and kill criteria

A `μ_n` claim fails or downgrades when:

- its order parameter or threshold cannot be measured independently;
- a named lower-only rival predicts the alleged new variable equally well;
- the prospective upper-register prediction fails;
- the recovery map cannot reproduce lower behavior within the declared error;
- a reduction succeeds, in which case `candidate_strong` becomes `reduced`;
- the claim relies only on absence of a known reduction;
- it requires quantum collapse or literal retrocausality to remain coherent.

A sixth demonstrated positive freedom revises the selected five-crossing
census. Merely naming one does not.

---

## Execution Surface

1. Complete one `MuCrossing` record per proposed domain crossing.
2. Do not write a solid `μ` edge without threshold evidence and a recovery law.
3. Keep commitment and outcome receipts distinct.
4. Keep the quantum inset removable.

**Canonical path:**
`01_EMERGENTISM/05_COSMOLOGY/03_FORMAL_SYSTEM/10_EFR_MU_LIMIT_FORMULA.md`
