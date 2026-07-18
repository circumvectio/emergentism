---
rosetta:
  primary_level: L3
  primary_column: Auditing
  operator: "Kṛṣṇa ◇"
  tier: "God"
  regime: "Vaiśya"
  register: "[C] prospective discriminators"
  canonical_phrase: "Freeze the rival before looking at the answer"
title: "Compass External Calibration Preregistration"
status: "FROZEN v2.1 — outcome-sign repair precedes every claim-specific freeze and result"
contract_version: "2.1"
date: 2026-07-18
evidence_tier: "[C] prospective claim tests; [I] calibration design; no tier promotion"
---

# COMPASS EXTERNAL CALIBRATION PREREGISTRATION

## Registration boundary

> `[金]` **v2.1 calibration seam.** The original version frozen in `bb9a4fc`
> required a favorable `supported` outcome to earn X2. That encoded confirmation
> bias into a stage intended to measure calibration rigor. Before any
> claim-specific freeze, new raw-data access, or X2 receipt, v2.1 makes stage
> assignment outcome-sign neutral: `supported`, `failed`, `null`, and `mixed`
> discriminators face the same artifact and provenance gate. The registered
> claims, rivals, variables, predictions, and kill criteria are unchanged. The
> original Git blob remains the historical v1 receipt.

This protocol freezes what would discriminate specific Emergentist Compass
claims from named alternatives. It does not preregister one omnibus theory test
and does not claim that any dataset has been analyzed.

The first commit containing each contract version is its freeze point; v2.1 is
the active contract. Later execution must
create a separate dated run sheet and result receipt. This file may receive only
an explicit tombstone or a non-semantic link to a result; predictions, outcomes,
rivals, exclusion rules, and thresholds may not be edited after the freeze.

External data created before this protocol are **retrospective independent
data**, not prospective evidence. Access to such data must occur only after a
claim-specific analysis manifest is frozen. A properly frozen retrospective test can
reach `X2`; it cannot be described as preregistered replication.

## Shared rules

Every run must freeze:

- a single claim ID from the
  [external calibration ledger](../00_EXTERNAL_CALIBRATION_LEDGER.md);
- population or system, unit of analysis, horizon, exclusions, missing-data
  policy, and complete data lineage;
- independent and dependent variables with units and reliability criteria;
- intervention or the exact limitation of an observational design;
- all named rival models, identical information sets, complexity penalties,
  folds, seeds, and decision thresholds;
- primary outcome, uncertainty interval, multiplicity correction, robustness
  checks, and negative controls;
- promotion, null, narrowing, and kill outcomes before data access;
- code hash, environment, data hash or immutable source locator, and custody.

The claim-specific `AnalysisManifest` is schema `2.0` and closed-world. It is a
structured protocol, not a prose promise. It must contain:

- an HTTPS source locator or content-addressed
  `artifact:sha256:<digest>` / `repository:sha256:<digest>` identifier;
- a checksum record. Retrospective X2 requires a publisher/repository SHA-256
  known at freeze; prospective X3 declares
  `compute_on_first_custody` with an explicitly null pre-collection expected
  hash because future observations do not yet have bytes;
- a fully specified candidate model and one fully specified entry for every
  rival named on the immutable claim card, each with fit and complexity rules;
- structured records for every registered variable and outcome, including
  operational definitions, units, primary-outcome flags, and decision rules;
- nonempty ordered preprocessing steps, nonempty exclusions with rationales, a
  positive fixed stopping rule, `2…20` folds, and nonempty unique random seeds;
- existing repository-relative analysis-code and environment-lock paths with
  exact SHA-256 hashes;
- separate native-unit ceilings for compute, data acquisition, and labor, with
  no hidden scalarization; and
- a dated access attestation naming the attester, custodian, custody protocol,
  and a separately hashed append-only access-log snapshot.

Both the freeze and analysis commits must contain the preregistration,
manifest, code, environment lock, and access log at exactly the declared
hashes. The data artifact is absent at freeze and bound at analysis.
One-character placeholders, `TBD` fields, empty protocol lists, post-hoc
stopping rules, analysis-time protocol drift followed by restoration, and
unbound or hash-mismatched dependencies fail closed.

No result may promote more than its registered claim and domain. “Compass
validated,” “worldview confirmed,” and similar whole-system verdicts are outside
the protocol.

## `CAL-AGENCY-01` — future-model intervention

### Question

Does an intervention on a present representation of a possible future change
present action beyond current reward, available actions, habit, and model-free
value?

### Design

Randomize future-state cue content or selectively disrupt prospective-state
representation. Record the present token, transition knowledge, available
means, choice, confidence, action latency, outcome, and next model. Use at least
one no-future cue, one equally salient non-prospective cue, and one reward-matched
control.

### Rivals

1. reward-only or temporal-discount model;
2. model-free reinforcement learner;
3. hybrid model-free/model-based learner;
4. active-inference or information-gain model where feasible;
5. future-model term added to the best complexity-matched rival.

### Primary discriminator

The future-model term must improve held-out log score over the best rival and
its randomized intervention must change the preregistered choice probability in
the predicted direction. Report the effect and uncertainty; do not substitute a
within-sample significance threshold for held-out discrimination.

### Kill/narrow

Kill the claimed scope if the matched intervention has no action effect, the
effect is fully absorbed by reward/salience, or a simpler rival predicts as well
or better. Retain ordinary forward-causal planning if present model tokens still
mediate action. Physical retrocausality is not tested.

## `CAL-CONE-01` — option metrics

### Question

When optionality is decorrelated from reward, risk, information, and cost, which
measure predicts competence and choice: reachable volume, empowerment, POWER,
path entropy, viability, expected utility, or a typed Compass vector?

### Design

Construct environments with matched reward but factorial variation in
controllability, stochastic outcome count, viability, irreversible commitment,
and effects on another agent. Predeclare horizon, action abstraction, sensor
representation, probability threshold, and resource budget.

### Primary discriminator

Compare held-out choice and competence prediction using identical folds and
penalties. The typed Compass vector earns `X2` only if it improves both metrics
over the best single measure without hiding another bearer's contraction.

### Kill/narrow

Reject universal maximization if agents reliably select lower optionality under
matched reward and risk, or if terminal-goal/irreversibility conditions reverse
the relation. This is expected to narrow the claim rather than kill every
instrumental-optionality result.

## `CAL-AGGREGATOR-01` — product selection

### Question

Does `ΦV` predict bounded action success better than alternative conjunctive or
aggregative functions?

### Required competitors

Product, minimum, normalized harmonic, additive, Cobb–Douglas, CES,
Nash-surplus, and maximin. Feature definitions and monotone rescalings must be
frozen before comparison. No competitor may receive a weaker information set.

### Primary discriminator

Primary outcomes are held-out log score and decision regret; calibration and
ranking accuracy are secondary. The product earns `X2` only if it beats the best
competitor on both primary outcomes across the prespecified task family.

### Kill/narrow

Replace or localize the product if a competitor consistently wins, if the
zero-factor boundary produces systematic error, or if `Φ` and `V` fail their
reliability thresholds. The broader conjunctive family may survive.

## `CAL-CONSTRAINT-01` and `CAL-MU-01` — crossing battery

### Crossing record

For every candidate crossing freeze:

\[
\mathcal C_j=(X,\lambda,E,g,Z,K,\mathcal I,\tau),
\]

where `X` is the lower state, `λ` the control, `E` the complete environment and
energy boundary, `Z=g(X)` the macrovariable, `K` the transition model,
`I` the intervention family, and `τ` the timescale.

### Domains and controls

Use at least one independently sourced case from collective motion, ecological
regime shift, evolutionary individuality, and model-based cognition. Include
smooth crossover and no-transition controls. The same crossing fields and
abstention rule must be used without domain-specific renaming after outcomes
are seen.

### Sequential gates

1. a preregistered transition or boundary result;
2. robustness to reasonable measurement, partition, and timescale variation;
3. held-out macro prediction/compression under native-unit component budgets
   (and only optionally a preregistered unit-valid scalar penalty);
4. implementation-level intervention response;
5. lower-model recovery within a declared tolerance;
6. visible matter, energy, controller, and environmental inputs;
7. classification as `reduced`, `currently_unreduced`, or `candidate_strong`
   relative to a declared model class.

The run stops at the first failed gate. Absence of a reduction cannot populate
`candidate_strong`. That label is available only when a preregistered proof or
discriminator excludes the declared reduction-model class under its stated
assumptions. Failed searches, unavailable models, and default nulls remain
`currently_unreduced`; no finite test proves irreducibility over every possible
model class.

### Primary discriminator

The frozen battery must discriminate unseen transition from smooth controls
better than domain-standard models without post-hoc remapping. Report predictive
and interventional emergence separately.

### Kill/narrow

Kill a crossing when there is no replicated transition, the novelty is a
coordinate change, the effect depends on an arbitrary grain, the macrovariable
adds no fair predictive/interventional value, or the claimed constraint hides
an external controller or forbidden-support path. Failure of the cross-domain
battery kills the universal grammar claim, not domain-standard transition
science.

## `CAL-EGREGORE-01` — generational trace experiment

### Factorial design

Cross:

- fixed versus partial versus full carrier replacement;
- trace preserved versus erased versus scrambled versus counterfeited;
- incentives stable versus reversed;
- centralized instruction present versus absent.

Freeze the shared trace representation, survival horizon, target statistic,
cost categories, bearer boundary, and full-replacement criterion before the
first session.

### Required measurements

Trace similarity or mutual information across cycles; later action distribution;
recovery after perturbation; carrier identities; current incentives; network
structure; authority messages; direct communication; shocks; attention, labor,
money, energy/compute, risk, and foregone options by payer and beneficiary.

### Rivals

Institutional memory, reinforcement, conformity/copying, command, stable
incentives, network structure, and exogenous-shock models.

### Primary discriminator

The predeclared Egregoreotype composite must add held-out prediction beyond the
best rival, survive full carrier replacement, and show a randomized trace effect
plus recurrent directional recovery across more than one cycle.

### Kill/narrow

Any missing mandatory component rejects candidacy. A simpler rival with equal
or better prediction reduces the construct to that mechanism. No outcome
licenses consciousness, personhood, sovereignty, goodness, or supernatural
causation.

## `CAL-REFLEXIVITY-01` — belief/action/outcome loop

Randomize forecast information or the sign/gain of expectations feedback.
Measure belief `b_t`, action `a_t`, outcome `y_{t+1}`, and update `b_{t+1}`.
Compare the declared loop with fundamentals-only, ordinary learning,
trend-following, strategic-response, and shock models. The loop earns `X2` only
if intervention and held-out prediction agree. Positive and negative feedback
are dynamical signs, not moral verdicts.

## `CAL-SYNTROPY-01` — normative consistency audit

The Justice axiom is not empirically confirmable. Audit its predicates for
contradiction, bearer omission, aggregate laundering, and coerced sacrifice.
Punishment, voluntary sacrifice, aggregate gain, cooperation, and strict mutual
gain remain distinct classes. No empirical stage applies.

## `CAL-JUSTICE-CONSEQUENCE-01` — institutional consequence test

A registered institutional comparison may test whether prespecified consent,
bearer-visibility, contest, reversibility, and exit controls improve correction,
durability, exit exercise, or hidden-harm detection against named rivals. It
must retain every materially affected bearer's delta separately and equalize
non-treatment resources. A result moves only this consequence card; it cannot
derive moral realism or relabel an imposed loss as syntropy.

## `CAL-SPHERE-01` — alternative geometry challenge

No current dataset is designated. Before any run, freeze a domain whose
observables can identify latent geometry; identical preprocessing; Euclidean,
hyperbolic, toroidal, simplex, `S²`, and flexible latent competitors; complexity
penalties; and held-out criteria. A perceptual complementarity bound tests only
the perceptual bridge. It cannot validate “the geometry of reality.”

## `CAL-DISPATCH-01` — Rosetta Agentz routing

Freeze the exact seven functions, the four deployable L1–L4 roles, the three
L5–L7 boundary-witness passes, routing triggers, permitted handoffs, stopping
rules, context budget, model family, and per-pass prompts before evaluation.
Randomly assign matched hidden tasks to: the 4+3 Rosetta route; one flat
agent; untyped multi-agent debate; a domain-expert router; and a shorter staged
pipeline. Equalize task information, prompt-development budget, total model
calls, tokens, tools, wall-clock allowance, and evaluator budget as closely as
the platform permits. Role-specific prompt content is part of the treatment and
is not forced to be identical.

Primary outcomes are blinded task quality and formal-error rate per unit compute.
Evidence-tier accuracy and correction after an injected contradiction are
secondary; latency and cost are mandatory. The routing claim earns `X2` only if
the frozen route beats every rival on the joint primary criterion without
post-hoc row reassignment or promoting L5–L7 into runtime modes. If a shorter
or flat system matches it, retain the
Rosetta as an interpretive dispatch grammar and reject the performance claim.

The God/Demon analogy is scored only as an objective-boundary mutation:
ego/local maximization may increase one agent's score while reducing the
collective or another bearer; Justice-constrained part-and-whole maximization
must preserve all named bearers. The analogy does not add agents, entities, or
evidence.

## Result-receipt contract

No claim reaches `X2` by changing a status string. Dataset status
`result_receipted` is valid if and only if `resultReceipt` names a valid,
repository-local JSON receipt; lower stages cannot carry a result receipt.

The receipt schema is `2.1` and closed-world. An `x2_discriminator` receipt must
bind the claim ID, an existing repository-relative `dataArtifact`, the exact
`dataSha256`, the exact `preregSha256`, a separate claim-specific
`analysisManifest` and `analysisManifestSha256`, distinct full `freezeCommit`
and `analysisCommit` IDs, one declared outcome from `supported`, `failed`,
`null`, or `mixed`, the claim's complete
rival set, a real ISO calendar date, team IDs, domains, and the observation-mode
boolean. The validator checks that both commits exist, that freeze is an
ancestor of analysis, that the preregistration bytes at freeze match
`preregSha256`, that the manifest bytes at freeze match the declared manifest
hash, that the current active files still match, that the data artifact did not
exist at the freeze commit, and that the exact artifact/hash exists both locally
and at the analysis commit. The analysis commit must also retain the frozen
preregistration, manifest, analysis code, environment lock, and access log at
their declared hashes. The schema-`2.0` manifest is closed and binds the
dataset locator and checksum, fully specified candidate and complete rival set,
operational variables and outcomes, preprocessing, exclusion rationales,
stopping rule, folds, seeds, analysis-code and environment-lock bytes,
native-unit cost ceilings, and dated no-access/no-collection-before-freeze
custody evidence. Paths and hashes of the two disclosed July 2 negative packets are
ineligible for retroactive promotion. `X2` records that an independent
discriminator was frozen and run; it does not record that the framework won. A
`failed`, `null`, or `mixed` receipt therefore reaches the same calibration
stage while narrowing, killing, or leaving the claim unresolved exactly as
preregistered.

Git can prove commit order, file absence, and byte identity; it cannot observe a
human's screen or memory. The access attestation is therefore an accountable
claim, not physical proof of non-access. Any contrary evidence kills the X2
provenance claim, and external audit may require stronger custody evidence.

The claim dataset also carries a typed `resultVerdict` that must equal the X2
receipt outcome exactly. Public `currentVerdict` must be only the exact token
`X2 outcome=<outcome>`—no suffix prose. X3 repeats the typed equality for
`replicationVerdict` and requires exactly
`X2 outcome=<outcome>; X3 outcome=<outcome>`. Thus a correct prefix cannot hide
contradictory narration, and a failed receipt cannot be narrated as support.

The hypothesis-bearing claim fields are frozen by a canonical contract hash:
claim identity and class, claim wording, source references and distance,
variables, intervention, outcomes, rivals, prediction, kill criteria, scope
boundary, and preregistration path. Result stage, bounded verdict, evidence
tier, dataset state, and preregistration status remain the explicitly mutable
result surfaces. Every variables/outcomes/kill-criteria entry must be text; an
object placeholder cannot satisfy the schema.

For `X2`, dataset `access` is also a closed declaration tied to generation:
`published_preexisting_frozen_before_access` or
`new_independent_collection_after_preregistration`. Free prose such as an
admission that outcomes were inspected before freezing the protocol fails the
gate. An `X2` verdict may state that the registered discriminator was supported,
failed, null, or mixed, but it may not claim proof, confirmation, universality, decisiveness,
whole-system reach, or a law of nature.

`X3` cannot reuse the `X2` receipt or set
`newIndependentObservations=true` on it. It must retain the prior valid
`x2_discriminator` receipt and add a distinct `x3_replication` receipt for a
different local data artifact with a different SHA-256. The four freeze and
analysis commits must be distinct and ordered
`X2 freeze < X2 analysis < X3 freeze < X3 analysis`; the replication team must
also differ from the X2 team, and the exact prior X2 receipt must already be
present at the X3 freeze commit. A same-data rerun is reproduction or
reanalysis, not replication.

Names and booleans inside a repository-authored JSON file cannot prove team
independence. Until an externally controlled signature or manual-review
attestation verifier is configured, the machine validator therefore rejects
every `X3` and `X4` promotion after checking the receipt chain. This is an
intentional fail-closed gate, not a missing success path.

## Promotion table

| Outcome | Maximum movement |
|---|---|
| primary literature only | `X1`; no evidence-tier promotion |
| frozen analysis on independent pre-existing data, regardless of outcome sign | `X2` and a dated `[B]` result for that claim/domain; support, narrow, retain unresolved, or kill exactly as preregistered |
| independent preregistered replication on newly collected observations, regardless of outcome sign | `X3`; consider `[A]` for the bounded replicated result, including a replicated rejection or null |
| independent rerun on the same observations | reproduction/reanalysis only; does not earn `X3` |
| repeated independent cross-domain reproduction | `X4`; consider a broader bridge after audit |
| analytic, symbolic, correspondence, or normative claim | no empirical stage; test mathematics, removability, consequences, or public usefulness separately |

## Freeze statement

On its first Git commit this document becomes the hypothesis boundary for the
external calibration program. No external validation result exists at freeze.

*Compass external calibration preregistration | 2026-07-18 | Rivals named before receipts.*
