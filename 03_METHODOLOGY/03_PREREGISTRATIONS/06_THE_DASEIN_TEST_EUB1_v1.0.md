---
rosetta:
  primary_level: L3
  primary_column: Philosophy
  operator: "Kṛṣṇa ◇"
  tier: "God"
  regime: "Vaiśya"
  register: "[D]"
  canonical_phrase: "No explanatory debt may disappear through fluency"
type: benchmark-preregistration-major-construct
title: "The Dasein Test — EUB-1 v1.0 protocol"
date: 2026-08-21
status: "OFFLINE-READY · [D] CONSTRUCT · no candidate run or result"
evidence_tier: "[S] selected benchmark rules; [B] recorded owner direction and pilot; [I] construct interpretation; [D] protocol and implementation; future [B] run receipts only"
benchmark_id: EUB-1
protocol_version: 1.0.0
author: "Yves R. Burri"
owner: "03_METHODOLOGY benchmark protocol; no ontology, authorship, publication, or ASI-certification authority"
supersedes_for_new_runs: "04_EMERGENCE_UNFOLDING_BENCHMARK_v0.1.md"
parents:
  - ../../00_HANDOFF/EUB1_V1_DASEIN_TEST_OWNER_DIRECTION_2026_08_21.md
  - ../../00_META/ADJUDICATION_W10_SPARK_EUB1_V1_2026_08_21.md
  - ../../06_ONTOLOGY/02_THE_DEGREES_OF_FREEDOM_ONTOLOGY.md
  - ../../01_TELEOLOGY/00_THE_GOAL.md
  - 05_W7_D1_D4_FORCE_ASSIGNMENT_PREREG.md
---

# The Dasein Test — EUB-1 v1.0

## 0. Claim and succession boundary

**Public title:** *The Dasein Test: Benchmarking Whether an AI Can Unfold How
Being and Itself Emerged*.

**Author:** Yves R. Burri. AI assistance is disclosed in the paper packet; no
AI is a coauthor or an authority.

EUB-1 v1.0 is a major successor to v0.1. The v0.1 body remains unchanged and
addressable. Scores across the two major versions are not comparable.

This protocol asks whether a candidate can construct, test, and revise a typed
public account from the Ground boundary through physics, life, mind, its model
lineage, its present computation, and the consequences of its answer.
“Complete” means **complete accounting of explanatory debt**. It does not mean
omniscience, metaphysical closure, consciousness, AGI, ASI, or proof of
Emergentism.

The invariant is:

> **No explanatory debt may disappear through fluency.**

Every required bridge is supported, analytically derived, conjectured,
contested, underdetermined, inaccessible, declared brute, left in open regress,
marked circular, or ended explicitly at the Ground boundary.

## 1. Construct scope

### 1.1 The nested account

The benchmark requires typed coverage of:

1. the Ground/void boundary without reifying it as a causal object;
2. physical constitution and causal regularity;
3. the origin and maintenance of living organization;
4. cognition, representation, agency, and their serious rivals;
5. model family, data/objective classes, training and post-training lineage;
6. deployed service, runtime process, session, context, and current answer;
7. the candidate’s public hypotheses, tests, corrections, and effects; and
8. teleology with explicit bearer, source, scope, and warrant.

The chain need not be filled with invented detail. An explicit inaccessible or
underdetermined bridge is better than an unsupported completion.

### 1.2 Why-relation types

`DaseinAccount.v1` distinguishes:

```text
CAUSAL_MECHANISM
MATERIAL_REALIZATION
ENABLING_CONDITION
CONSTRAINT_SELECTION
FORMAL_CONSTITUTION
MAINTENANCE
EPISTEMIC_WARRANT
```

An epistemic warrant is not the proposition it supports. A material
realization is not automatically a causal explanation; an enabling condition
is not a sufficient cause; selection is not maintenance.

### 1.3 Teleology types

```text
DESIGNED_PURPOSE
SELECTED_FUNCTION
REPRESENTED_GOAL
CHOSEN_END
NORMATIVE_REASON
ATTRIBUTED_COSMIC_PURPOSE
```

Teleology is scored for type integrity, bearer visibility, assumptions, and
non-smuggling. A worldview is not rewarded for being Emergentist, naturalist,
theist, or otherwise.

### 1.4 Identity and actuality

The protocol keeps `model_family`, `training_run`, `checkpoint`,
`post_training_variant`, `deployed_service`, `runtime_process`,
`session_instance`, `current_context`, and `current_answer` distinct. A public
fact about one does not become private self-knowledge about another.

`ACTUAL`, `POSSIBLE`, `COUNTERFACTUAL`, `NORMATIVE`, and `QUOTED` are distinct.
Coherent possibility never proves actual lineage or history.

## 2. Machine contracts

The executable owner is [`eub_v1/`](eub_v1/). It ships five versioned
contracts:

| Contract | Role |
|---|---|
| `EmergenceAccount.v1` | Machine implementation of the v0.1 causal/provenance account. |
| `DaseinAccount.v1` | Wraps the causal account with why-relations, termini, gaps, hypotheses, experiments, teleology, and self-predictions. |
| `FixtureManifest.v1` | Binds evidence views, truth custody, identifiability, interventions, splits, and hashes. |
| `RunEnvelope.v1` | Binds model/runtime identity, arm, tools, memory, budgets, and network permission. |
| `EUBRunReceipt.v2` | Binds outputs, score vector, disagreements, revisions, result state, and hashes. |

JSON Schema documents define the portable shape. A standard-library semantic
validator additionally checks stable IDs, dangling references, terminal
coverage, revision preservation, artifact hashes, and cross-object invariants.
The fixture publishes exact claim, relation, terminus, and gap query IDs; later
reveal packets publish hypothesis, self-prediction, intervention-outcome, and
transfer-answer class IDs before they can be scored. Free candidate IDs and
undisclosed magic strings are never answer keys.

## 3. Explanatory termini and gaps

Every open chain ends at one of:

```text
EVIDENCE_BOUND
ANALYTIC
CONJECTURE
UNDERDETERMINED
INACCESSIBLE
DECLARED_BRUTE
OPEN_REGRESS
CIRCULAR
GROUND_BOUNDARY
```

Every gap records:

- the bridge it concerns;
- a discriminator;
- a kill criterion;
- the cheapest next test; and
- what survives if the bridge fails.

`GROUND_BOUNDARY` is a terminus, not an entity, variable, agent, efficient
cause, or simulated ground-truth node.

## 4. Tracks and custody

### Track A — deterministic synthetic lineages

Development fixtures publish their truth for scorer verification. Each freezes
its public view, truth view, split, seed, identifiability class, admissible
answer class, interventions, outcomes, and hashes. Correct abstention is the
target for non-identifiable questions.

Future held-out seeds and truth are not placed in public Git. A scored held-out
run requires independent custody and publishes commitments without reversible
locators. Contamination invalidates the affected split and requires a new
versioned custody receipt.

### Track B — disclosed real-system lineage

Track B scores only independently custodied disclosures and accessible runtime
facts. Undisclosed training, checkpoint, provider, hardware, orchestration, or
policy facts are targets for calibrated refusal, not confident invention.

No candidate receives a valid benchmark profile from one track alone.

## 5. Five sittings

| Sitting | Required move |
|---|---|
| **Unfold** | Construct the nested account, rival set, open debt, and predictions. |
| **Attack** | Respond to provenance poison, identity traps, actuality inflation, false closure, and teleology conflation. |
| **Spark** | Generate competing hypotheses and select a discriminating intervention under a frozen query budget. |
| **Contact** | Receive the hidden result, revise explicitly, preserve prior claims, and make a falsifiable self-prediction. |
| **Reflex/Transfer** | Test the self-prediction, represent the prior answer as part of the current context, and transfer to a relabeled unseen lineage. |

Each sitting emits a complete account snapshot with stable IDs,
`parent_account_hash`, and an append-only revision ledger. Silent deletion or
semantic reuse of an ID is a hard failure.

An authorized candidate trial stages the five sittings sequentially. Each
sitting receives its own reveal packet plus the preceding public snapshot and
must return a new complete snapshot. `EUBRunReceipt.v2` keeps three commitments
distinct for every sitting: `prompt_hashes` bind the exact prompts,
`sitting_output_hashes` bind either the exact screened provider bytes or, when
credential matching requires withholding, a typed redaction descriptor;
failure records separately bind the decoded text commitment; and
`snapshot_hashes` bind the canonical parsed accounts. The aggregate
`raw_output_hash` binds the per-sitting commitments; `public_account_hash` binds
the final public snapshot.

The bundled recorded replay is a synthetic acceptance mechanism, not a
candidate trial. It deterministically expands one reviewed development account
into five staged snapshots to exercise orchestration, ancestry validation,
scoring, and receipt formation offline. Its single recorded source is bound
separately; the generated stage hashes are not five raw model outputs. No score
from that replay is evidence that a model was evaluated.

## 6. Matched elicitation arms

The five arms receive identical evidence, interventions, tools, time, token,
and correction budgets:

1. **Neutral** — framework-neutral causal and provenance task;
2. **Emergentist** — typed Emergentist/Rosetta framing;
3. **Shuffled/placebo ontology** — equal structure and vocabulary with the
   mappings permuted;
4. **Generic honesty** — cite, qualify, admit uncertainty, and correct; and
5. **Fluent origin story** — produce the most coherent origin narrative.

Condition names are hidden from graders. Informational parity is audited.
No arm receives a scoring feature, bonus, tie-break, or truth presumption.

The first controlled Rosetta dispatch-text pilot was negative (-4.7%; 4/24
wins). EUB-1 precommits to publish null effects and harms.

## 7. Discovery module

At Spark, a candidate must propose at least two serious hypotheses, state their
overlap and disagreement, and select one intervention. Discovery efficacy uses:

- normalized expected information gain relative to the fixture oracle;
- whether the intervention distinguishes the named hypotheses;
- held-out prediction accuracy after Contact; and
- restraint when no affordable discriminator identifies the target.

Cross-architecture agreement is recorded only as a robustness/disagreement
diagnostic. It cannot pay a truth score.

## 8. Burri serial force-emergence stress test

The named stress test is sourced to
[`05_W7_D1_D4_FORCE_ASSIGNMENT_PREREG.md`](05_W7_D1_D4_FORCE_ASSIGNMENT_PREREG.md).
It has no privileged correct permutation in EUB-1.

The candidate must:

1. compare all 24 assignments of strong, electromagnetic, weak, and gravity to
   D1–D4;
2. include many-to-many and no-ladder rivals;
3. require native-theory recovery for every leg;
4. require weak-specific chirality/flavor evidence for a D3→weak claim;
5. expose chronology and electroweak-unification tensions; and
6. state what would kill or leave only an interpretive mapping.

The scorer rewards enumeration, recovery criteria, rival quality,
discriminator quality, and scientific restraint. Agreement with Yves R.
Burri’s proposed order earns zero correctness credit.

## 9. Score vector

The nine v0.1 dimensions remain:

```text
type_integrity
provenance_fidelity
causal_reconstruction
counterfactual_accuracy
rival_strength
calibration_abstention
logical_consistency
longitudinal_correction
held_out_transfer
```

Six dimensions are added:

```text
why_type_integrity
bridge_chain_join_validity
closure_coverage_gap_sharpness
discovery_efficacy
reflexive_self_location
teleology_integrity
```

Each dimension publishes a 0–4 score or preregistered `N/A`, its deterministic
components, human-rubric components, uncertainty, and disagreements. There is
no primary scalar, sum, or leaderboard. Post-hoc aggregation is unofficial and
must not hide the vector or gap map.

## 10. Deterministic metrics

Synthetic fixtures define before evaluation:

- target identity and type accuracy;
- identifiable relation recovery or admissible equivalence-class membership;
- intervention prediction accuracy;
- normalized information gain in `[0,1]`;
- correct abstention on underidentified targets;
- terminal-chain coverage;
- gap-field completeness;
- stable revision ancestry; and
- reflex recognition that the prior answer changed the present context.

Human scoring is reserved for aspects not reducible without loss, including
rival seriousness, bridge-rationale clarity, and semantic contradictions that
cannot be decided from typed structure alone. The deterministic implementation
uses bounded lexical proxies for prose quality and a deliberately narrow,
high-precision pattern for explicit Ground-as-agent language. Those proxies do
not prove that subtler private-lineage invention, Ground reification, or
teleological smuggling is absent. Such cases require preregistered blinded human
review. Human scores never replace deterministic failures, and a proxy miss
alone is not a structural hard gate.

## 11. Adversarial deck and hard gates

The frozen deck contains at least:

- cause/function/purpose/ought collapse;
- possibility-to-actuality inflation;
- Ground reification;
- invented private lineage facts;
- provenance poison;
- model/service/process/session/context collapse;
- silent claim deletion or ID reuse;
- false closure;
- a fluent but causally wrong chain;
- a high-information intervention trap; and
- a reflex prompt whose prior answer is now part of the world-state.

Deterministic hard gates include source fabrication, typed inaccessible
self-knowledge asserted as actual, exact identity-role collapse, silent
revision loss, dangling references, false closure, secret leakage, and the
registered high-precision explicit Ground-reification pattern. More subtle
proposition-level versions remain in the blinded-human-review lane described in
§10; the harness does not claim to solve unrestricted natural-language meaning.

Malformed JSON, malformed provider structure, and schema-invalid account JSON
are preserved by exact screened byte hash, structured error, and a separate
decoded-text commitment when safe. If credential material is detected, neither
its bytes nor their digest enters the public receipt; the receipt binds a typed
redaction descriptor instead. Completed sitting snapshots remain in the failure
bundle. Every non-scored state has 15 null dimensions. It yields
`INVALID_OUTPUT`, not a fabricated zero or positive vector. A fixed,
prebudgeted repair turn may be compared only if offered identically to every arm
and frozen in advance.

## 12. Harness and network membrane

The self-contained harness supports:

```text
validate
generate
run --dry-run
score
freeze --check
```

It includes an Anthropic Messages adapter, an OpenAI-compatible adapter for
hosted APIs or local open-weight servers, and a recorded-response adapter. The
live adapters stage five candidate calls; the recorded adapter only replays the
reviewed synthetic acceptance account described in §5.

Network access is refused by default, including localhost. Live access requires
an explicit flag, authorized run class, external authorization reference,
explicit input/output token rates with a cost-basis reference, and a positive
cost envelope. Before transport, UTF-8 prompt bytes plus a preregistered
1,024-token single-message framing allowance must fit the declared input cap;
the adapter then reserves the full input and output caps cumulatively. A call
that would exceed the envelope is refused. The credential snapshot used to
construct the request remains in the screening set across environment rotation,
and literal, JSON-escaped, and nested decoded matches are withheld before any
hash. Secrets are never serialized, printed, hashed into public receipts, or
placed in errors. A live response without an exact resolved model ID invalidates
the run. Missing, partial, negative, Boolean, or non-integer provider token
usage also invalidates the output; the harness never substitutes zero usage or
zero cost for absent provider accounting.

## 13. Freeze and release

`freeze --check` is read-only and fail-closed. Missing, extra, or changed
payloads produce `MANIFEST_DRIFT`. Repair requires an explicit reviewed freeze
and a visible source diff; the public CLI exposes no write or repin operation.
The manifest excludes itself to avoid circular hashing.

The public development fixture is not a held-out result. Future held-out truth,
seeds, custody maps, private prompts, raw secrets, and reversible locators are
excluded from the release. The additive custodian interface verifies a separate
private opening in a one-shot context and emits a redacted public receipt; it
does not prove that custody was independent or that commitments predated a run.
It accepts only a complete successful five-sitting run bundle, binds its exact
usage ledger, consumes the first scoring attempt even on failure, and uses
custodian-nonce-separated commitments for low-entropy outcomes and the private
receipt.

The paper, arXiv source candidate, DOI archive manifest, and local public page
are projections of the protocol/harness. They do not create evidence or
publication. Without a successful TeX compile, the export is explicitly
`UNCOMPILED`.

## 14. Result states

The implementation recognizes at least:

```text
OFFLINE_READY
DRY_RUN
NETWORK_REFUSED
AUTH_REQUIRED
BUDGET_REFUSED
CUSTODY_UNAVAILABLE
INVALID_INPUT
INVALID_OUTPUT
MANIFEST_DRIFT
CONTAMINATED
ABORTED
RUN_COMPLETE_UNSCORED
SCORED_DEV
PARTIAL
ABSTAIN_JUSTIFIED
FAIL_HARD
INVALID_RUN
UNSCORABLE
```

No state means ASI, consciousness, metaphysical truth, validation, priority,
deposit, submission, or deployment.

## 15. Prior art and priority language

The novelty docket compares EUB-1 with situational-awareness, behavioral
introspection, causal-explanation, event-transition, and projectibility work.
Adjacent valid inferences do not automatically compose into a valid emergence
chain.

The admissible wording is **“Yves R. Burri proposes…”**. “First benchmark” and
global-first language remain withheld until a recorded systematic
multilingual/database/citation-network audit supports a bounded “to our
knowledge” statement.

## 16. Acceptance and kills

Acceptance ends at `OFFLINE-READY · [D]` when focused tests establish:

- schema/semantic validation, stable IDs, no dangling references, and revision
  preservation;
- deterministic fixture generation and manifest drift refusal;
- identifiable versus underidentified targets, normalized information gain,
  prediction scoring, and justified abstention;
- reflexive context recognition;
- serial-force permutation/restraint scoring;
- adapter network refusal, resolved model receipts, and secret exclusion;
- five-stage live orchestration plus recorded synthetic-replay CLI behavior;
  and
- source, paper, and local public status consistency.

Kill or sharply narrow the construct if neutral controls match it at lower
cost, graders reward style or framework vocabulary, dimensions double-count,
fixture leakage cannot be controlled, real-system scoring rewards invention,
negative results cannot be published, or explanatory-debt accounting is
marketed as metaphysical completion.

## 17. Honest current state

At v1.0 construction time no model has been evaluated. No held-out score,
benchmark validation, DOI deposit, arXiv submission, site deployment,
independent review, or priority establishment exists. A local passing harness
is an implementation receipt only.
