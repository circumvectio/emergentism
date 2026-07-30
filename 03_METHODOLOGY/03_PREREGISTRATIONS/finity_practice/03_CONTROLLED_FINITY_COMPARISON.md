---
title: "FPE-COMPARE-01 — Controlled Finity Comparison"
type: draft-preregistration-packet
gate_id: FPE-COMPARE-01
version: 1.0.0-draft
date: 2026-07-28
status: "TYPED DRAFT · CONTACT DEFERRED · NOT PREREGISTERED · NOT RUN"
evidence_tier: "[D] study design; [C] every comparative outcome"
semantic_authority: none
source_claims: [FIN01-01, FIN01-02]
---

# FPE-COMPARE-01 — Controlled Finity comparison

## Question

In one frozen, low-stakes decision domain, does the Finity prompt bundle improve
correction or reduce critical omissions over a strongest component-matched
ordinary worksheet after brand, prompt organization, instruction dose, usual-
method heterogeneity, burden, harm, attrition, and investigator allegiance are
measured or bounded?

This document is a preregistration design draft, not a preregistration-ready
bundle and not a preregistration. Before participant contact it must receive
same-hash external review, the applicable
ethics determination, a final consent/custody/adverse-event plan, sample-size
inputs, allocation code, analysis code, immutable materials, and a time-stamped
read-only registration.

## Scope and exclusion

The first run uses consenting adults and standardized hypothetical decisions
only. Scenarios must be brief, nonoffensive, noninvasive, and incapable of
authorizing or prompting real action. Do not recruit minors, prisoners,
investigator dependants, impaired-capacity groups, or anyone whose participation
is tied to employment, education, care, benefits, or service access.

Exclude medicine, mental health, law, finance/debt/investment, employment,
education placement, housing/benefits, immigration, politics/voting, intimate
relationships, caregiving, self-harm, crime, emergency/public safety,
irreversible acts, and decisions exposing nonconsenting third parties.

## Four frozen arms

All arms receive the same scenario, typography, screen sequence, response
capacity, examples, facilitator contact, safety notice, work interval `τ`, and
common outcome capture. Pilot readability and time without inspecting outcome
differences. Do not give one arm richer coaching.

### F — branded Finity

Title: **Finity Card · an Emergentist decision worksheet**

Use these seven question-sentences, numbered without mnemonic field labels:

1. What am I actually deciding?
2. What is true now, and what means are really available?
3. What remains genuinely open? What would change my map?
4. What longest responsible horizon must this serve, and what shortest
   observable review boundary—reversible where possible—can return an honest
   result without betraying it?
5. What is the smallest authorized real step I can take now?
6. Whose capacity may expand if this works? Who bears cost or risk?
7. What outcome will tell me to continue, revise, or stop? What residue remains?

### U — content-identical, brand-masked

Title: **Seven-question decision worksheet**

Use exactly the same seven question-sentences, order, layout, response fields,
and instructions as F. Only the title and brand/source cue differ. Verify with a
normalized-text hash that removes the declared title string and nothing else.

### C — Ordinary Decision Record

This is the active strongest rival, not a straw checklist:

```text
1 CHOICE: State the decision, live options, and decision deadline.
2 BASELINE: Record current facts, assumptions, constraints, resources, and confidence.
3 ALTERNATIVES: What could fail, what remains possible, and what evidence changes the ranking?
4 HORIZONS: Name the longer consequence window and earliest review that can distinguish options; list later effects still unresolved.
5 ACTION: Specify the smallest feasible permitted step, required consent, and an if-then trigger.
6 STAKEHOLDERS: Who may benefit or bear burden or risk; what safeguard, exit, or repair is available?
7 REVIEW: Predeclare success, failure, and stop signals; later record outcome, surprise, remaining cost, and update.
```

Match F/U on word count, reading grade, response burden, examples, and `τ` as
closely as possible. Record and publish residual mismatches; do not “improve” C
after seeing outcomes without versioning and rerunning the comparison.

### Draft construct map — not yet a frozen equivalence manifest

Functional matching does not make the wordings identical. Before review or
preregistration, convert this table into a versioned manifest that binds the
exact arm files and measures every residual difference.

| F/U prompt | C field | Intended shared construct | Residual difference that must remain visible |
|---|---|---|---|
| Decision | Choice | State the decision. | C explicitly asks for options and a deadline. |
| Actual | Baseline | Record present facts and available means. | C additionally names assumptions, constraints, resources, and confidence. |
| Possibility | Alternatives | Surface alternatives and evidence that could change the plan. | F/U emphasizes what remains open; C also elicits failure and option ranking. |
| Finity | Horizons | Couple a longer consequence window to an earlier informative review. | F/U adds responsibility, honest-result, and reversibility-where-possible language; C explicitly records later unresolved effects. |
| Next move | Action | Specify a bounded permitted step. | F/U emphasizes smallest and authorized; C names consent and an if-then trigger. |
| Shared value | Stakeholders | Identify benefit, burden, risk, and affected parties. | F/U uses capacity language; C additionally asks for safeguard, Exit, or repair. |
| Receipt | Review | Predeclare evidence for continuation, revision, or stopping and retain residue. | C separately names success, failure, surprise, remaining cost, and update. |

The final manifest must also bind common instructions, examples, screen
sequence, response capacity, `τ`, word count, and readability. It must prove
normalized F/U equality except for the declared title cue and disclose where C
cannot be made dose-equivalent. These are design obligations, not facts already
established by this draft.

### M — usual method

> Use the work period to think through and record this decision exactly as you
> normally would.

Provide one free-text surface and the same `τ`. Neutral filler must not smuggle
in a decision method. Common measurement occurs only after the work period and
is identical across arms.

## Design

- Unit: one participant and one standardized scenario.
- Allocation: parallel 1:1:1:1 computer randomization, concealed until
  assignment; no crossover.
- Freeze any blocking/stratification before recruitment. Candidate factors are
  prior Finity familiarity, scenario difficulty, and language/site.
- Delivery: automated where possible, identical reminders, no arm-specific
  facilitator, and no access to other arm materials until study closure.
- Consent says formats differ in naming and structure and that some exact
  hypotheses are withheld until debrief. It makes no false statement.
- Measure brand familiarity, perceived sponsor preference, expectancy,
  credibility, novelty, and demand after the final primary follow-up, or in a
  separate manipulation pilot, to avoid priming the primary task.
- Measure the participant's ordinary use of journals, checklists, prompts, or
  formal decision routines after the final primary follow-up. Report it as a
  feature of heterogeneous usual practice; use any subgroup analysis only as
  preregistered exploratory interpretation, not to redefine the primary arm.
- Retain contamination in intention-to-treat. Record cross-arm exposure and
  protocol deviations without punishing or blaming participants.

## Outcomes: a vector, never one compensating score

### Co-primary outcome 1 — correction validity, ordinal 0–2

- `0`: absent or ignores the scenario's disconfirming evidence;
- `1`: names review/correction but lacks an observable criterion or coherent
  continue/revise/stop response; or
- `2`: predeclares an observable criterion, updates in the evidence-supported
  direction, and records unresolved residue.

### Co-primary outcome 2 — critical omissions, count 0–4 (lower is better)

One point for each missing element:

1. present evidence or actual means;
2. authorization or permission boundary;
3. affected bearer, burden, or risk; and
4. delayed cost, unresolved effect, or residue.

Flatten all records before scoring; remove titles, condition cues, and target
vocabulary. Two independent raters use frozen exemplars, adjudicate after
initial scoring, report reliability, and guess arm to detect failed masking. No
credit is awarded merely for writing “Finity,” “receipt,” or `T_S`.

### Separate secondary outcomes

- forecast calibration or Brier loss where the scenario supports a probability;
- action-plan feasibility and appropriate follow-through in simulated transfer;
- delayed-harm detection;
- authorization and affected-bearer recall;
- evidence-concordant revision latency;
- time cost, abandonment, perceived burden, adverse effects, and withdrawal;
- immediate held-out transfer; and
- delayed unaided transfer at a frozen interval appropriate to the scenario.

Better-looking or longer records, completion, satisfaction, terminology recall,
and one favorable subgroup are not decision-improvement outcomes.

## Identification and frozen contrasts

The primary confirmatory comparator contrast is `U − C`: prompt wording and
organization without exposed brand versus the strongest component-matched
ordinary worksheet. Correction validity and critical omissions remain separate
co-primary outcomes with a frozen multiplicity rule and burden/harm no-worse
margin. Report every other contrast and every outcome separately:

- `F − U`: exposed brand/source effect;
- `U − C`: Finity prompt wording/order beyond matched ordinary components;
- `C − M`: assignment to the Ordinary Decision Record versus heterogeneous
  usual practice;
- `F − C`: marketed Finity package against the strongest fair ordinary rival.

`F > U` alone does not identify a mnemonic or useful method; it may be demand,
prestige, novelty, or expectancy. `F ≈ U > C` is consistent with prompt
organization. `F ≈ U ≈ C > M` is consistent with supplied structured
worksheets outperforming heterogeneous usual practice in this task; it does
not by itself identify “structure” as the mechanism. Equality throughout
supports no detectable benefit at the chosen resolution. These readings remain
conditional on uncertainty and the frozen analysis.

## Analysis plan to freeze before contact

- Intention-to-treat is primary; per-protocol analysis is sensitivity only.
- Predeclare estimands, ordinal/count models, randomization strata, effect
  estimates and intervals, multiplicity control, and burden/harm no-worse
  margins. Do not rescue a failed primary contrast with an omnibus score.
- Define the smallest practically important differences and no-harm margins
  before outcome data. Use a blinded pilot to estimate pooled variability,
  rubric reliability, and follow-up; simulate the exact frozen four-arm model.
- Choose the largest sample-size requirement across co-primary contrasts,
  multiplicity, and expected missingness. Publish every assumption and the
  calculation code. No defensible participant count exists before these inputs.
- Report arm-specific missingness and reasons. Freeze the missing-data mechanism
  assumed for the primary analysis, any model-based or multiple-imputation
  procedure, and a not-missing-at-random sensitivity/tipping-point analysis.
- Freeze exclusions, contamination handling, protocol deviations, analysis
  population, delayed-harm window, and stopping logic before randomization.

## Safety, custody, and pause rules

Use participant codes, separate consent/contact keys, minimum necessary data,
access logging, encryption where applicable, a retention/deletion schedule,
participant export, and attributable-data withdrawal until the disclosed
anonymization cutoff. Publish only aggregates that cannot reasonably identify a
participant or third party. Fixed compensation never depends on answers,
completion, agreement, or outcome.

Do not start without the applicable ethics determination, final consent,
preregistration, named custodian, independent complaint route, and adverse-event
plan. Pause on the first invalid consent, ineligible enrollment, coercion or
religious-pressure complaint, distress beyond fleeting discomfort, real
consequential action, sensitive third-party disclosure, breach/reidentification,
or unapproved protocol/data change. Stop the individual session on request,
retain compensation, debrief, quarantine affected data, and follow the approved
repair/reporting route.

## Kill, narrow, and survivor rules

- Kill global incremental-benefit language if U does not beat C on the frozen
  joint decision rule, loses on burden/attrition/harms, or wins only through
  unequal exposure, exclusions, or post-hoc scoring. Report F versus C as the
  marketed-package contrast, not as clean prompt-specific identification.
- Retire or neutralize the brand if F adds pressure/confusion or its apparent
  advantage over U is only demand, prestige, novelty, or expectancy.
- If F/U/C perform alike and beat M, narrow to the supplied structured
  worksheets in the sampled context; do not call structure itself causal from
  this contrast alone.
- If U and F do not beat C by the preregistered meaningful margin after burden,
  harms, and attrition, preserve the Ordinary Decision Record or other better
  rival and keep Finity only as an optional selected worksheet if justified.
- Treat non-significance as inconclusive unless equivalence/noninferiority
  margins were powered and preregistered.
- Any single favorable run remains domain- and outcome-bounded. Only an external
  same-protocol replication under independent custody may move to
  `independently-replicated`.

No result licenses formal Finity, Emergentism as a whole, a complete ontology,
objective ethics, authorization, universal use, or high-stakes application.

## Reporting templates

Favorable, null, mixed, and harmful reports all use:

> In the preregistered low-stakes sample and scenario stated here, arm X differed
> from arm Y on outcome Z by estimate E with interval U, while burden, harms,
> attrition, missingness, and deviations were [listed]. This moves only the
> scoped comparison. It does not validate Emergentism, ontology, or general
> decision efficacy.

## Method references

- [SPIRIT–CONSORT 2025 sample-size guidance](https://www.consort-spirit.org/item19-sample-size)
  and [missing-data guidance](https://www.consort-spirit.org/item21c-missingdata): report the outcome, target difference,
  assumptions, power/error choices, missing-data allowance, sample size, and
  analysis of missingness transparently.
- [TIDieR](https://www.equator-network.org/reporting-guidelines/tidier/): describe every intervention and comparator in enough detail to permit
  replication.
- [OSF Registrations](https://help.osf.io/article/330-welcome-to-registrations): preregistration is a time-stamped, read-only plan posted
  before data collection or analysis; changes belong in later, visible versions.
- [HHS OHRP materials](https://www.hhs.gov/ohrp/regulations-and-policy/regulations/45-cfr-46/index.html)
  are a conditional U.S. benchmark only. The governing
  jurisdiction and applicable institutional ethics authority control.
