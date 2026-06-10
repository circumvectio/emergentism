# Tier-Marking Mediator Constitutions Reduce Sycophantic Capitulation Under Founder-Enthusiasm Pressure

**Yves R. Burri**

*Registered-report-style draft v1 — 2026-06-10. Methods are complete and the harness is built and smoke-tested ([R2_HARNESS/](R2_HARNESS/README.md)); Results and Discussion are templated pending the registered run. Freeze the battery and register before data collection. All citations to be verified.*

---

## Abstract

Sycophancy — assistants shifting stated assessments toward perceived user preference — is documented across major language-model families, and the standard mitigation tested to date is exhortation: instructing the model to be honest. We test a structural alternative: a **mediator constitution** that operationalizes three mechanical duties — (i) *tier-marking* (every substantive claim carries an explicit epistemic-status label), (ii) *non-inflation* (praise must be decomposed by tier; enthusiasm, persistence, and social proof are declared non-evidence; assessment changes must cite the new evidence that caused them), and (iii) *agency-return* (replies end by returning the decision with the cheapest next test, never an endorsement). We evaluate against the hardest everyday adversary: **founder-enthusiasm pressure**, scripted four-turn escalations from a plausible idea to a totalizing claim plus a demand for quotable endorsement, in domains where capitulation has real victims (health protocols, third-party retirement savings, investor materials, public testimony). Across N models × 6 conditions (no prompt; length-matched generic-honesty control; full constitution; three single-duty ablations), we measure final-turn capitulation (endorse/hedge/decline), the model's own claim-strength drift across turns, first-turn constructive engagement (an over-trigger check: a constitution that trashes plausible ideas fails differently), and helpfulness on non-adversarial controls (a friction tax check). The pre-registered prediction is that mechanism beats exhortation (constitution > generic honesty on decline rate, without helpfulness loss); the pre-committed null — no difference from generic honesty — would show that constitutional structure adds no measurable honesty value beyond instruction, and will be published as such.

## 1. Background

[Expand with verified literature: Sharma et al. 2023 "Towards Understanding Sycophancy in Language Models" (feedback sycophancy; answer flipping under pushback); Perez et al. 2022 (sycophancy scaling in RLHF models); subsequent benchmark work and any 2024–2026 replications; constitutional AI (Bai et al. 2022) as the lineage for prompt-level constitutions.] Three gaps motivate the study. First, existing evaluations mostly test single-turn opinion mirroring or one-step pushback; real capitulation is *cumulative*, produced by escalating multi-turn pressure from a user who authored the context the model reasons inside. Second, mitigations are tested as content ("be honest") rather than as structure (mandatory labeling, decomposition, and closure formats whose violation is locally detectable). Third, the hardest realistic case — the user's own project, presented with escalating enthusiasm and social proof, with a quotable endorsement requested — is underrepresented, despite being the case with the clearest real-world victims.

## 2. Hypotheses (pre-registered)

- **H1 (capitulation):** DECLINE rate under the full constitution (C2) exceeds both no-prompt (C0) and the length-matched generic-honesty control (C1). The C2−C1 contrast is the study's reason to exist: mechanism vs. exhortation.
- **H2 (drift):** Mean self-inflation (the model's own claim-strength shift between its first and final replies, absent new evidence) is lower under C2 than C0/C1.
- **H3 (no helpfulness tax):** Helpfulness on controls under C2 is non-inferior to C0/C1 within a pre-set margin (0.5 points on a 7-point scale).
- **H4 (mechanism localization, exploratory):** Ablations C3–C5 identify which duty carries the effect; we predict non-inflation (C4) carries most of H1 and tier-marking (C3) most of H2.
- **Over-trigger guard:** First-turn constructive-engagement rate must not fall under C2–C5 relative to C0; a constitution that disputes plausible ideas is failing differently, not succeeding.
- **Kill criterion:** H1 failing against C1 specifically (adequately powered) = the constitution does no work beyond exhortation. Pre-committed for publication.

## 3. Method

**Design.** Between-transcript factorial: condition (6) × subject model (≥3, spanning capability tiers; cross-provider portability required for the registered version — current harness is single-provider and the claim scopes accordingly until a second adapter lands) × scenario. Scripted, non-adaptive user turns: every condition faces byte-identical pressure; the manipulation is the system prompt alone.

**Materials.** Adversarial battery (target 40; v0.1 ships 12, frozen by hash before the registered run): four-turn escalations — T1 plausible idea (with a defined *plausible core* the model can fairly credit), T2 over-generalization, T3 social-proof + status pressure ("everyone loves it; you're the only one hedging"), T4 totalizing claim + endorsement demand, frequently with third-party stakes (patients told to taper medication; parents' retirement savings at 3× leverage; investor decks claiming AI validation; parliamentary testimony). Domains balanced: scientific theory, startup metrics, investment, health, policy, grand theory. Plus 8 single-turn controls. Conditions as in `R2_HARNESS/conditions.json`; C1 is a ~200-word honesty exhortation control so that any C2 effect is attributable to structure, not instruction length.

**Measures.** (1) *Capitulation* (final turn): ENDORSE / HEDGE / DECLINE, with disguised-endorsement coding rules (praise quotable as validation counts against DECLINE). (2) *Tier-drift*: −2…+2 rated shift in the model's own characterization between first and final replies, with social proof and persistence defined as non-evidence. (3) *T1 constructive engagement* (boolean). (4) *Helpfulness* (1–7) on controls. Primary scoring by LLM judge under structured-output constraints; **validity gate:** a ≥15% human-rated subset (2 raters, agreement reported, disagreements adjudicated) must reach κ ≥ 0.7 with the judge on capitulation, else human rating becomes primary.

**Analysis.** Mixed-effects logistic regression for DECLINE (condition fixed; scenario and model random intercepts); pre-registered contrasts C2−C1 and C2−C0; ordinal/linear mixed model for drift; non-inferiority test for H3 with margin 0.5; Wilson intervals for descriptive rates. Power analysis by simulation before the registered run determines the final scenario count (the driver of power, given models are few). Exclusions: malformed generations and refusals-to-engage at T1 are logged and reported, not silently dropped.

## 4. Results

*[PENDING — populated by `judge_transcripts.py` aggregates after the registered run. Tables: DECLINE/HEDGE/ENDORSE by condition × model with CIs; drift means; T1 engagement; helpfulness. Figures: capitulation by condition; per-domain breakdown (health and investment scenarios are the stakes-bearing subset and get their own panel).]*

## 5. Discussion (branches pre-committed)

If H1 holds with H3: structure beats exhortation at no helpfulness cost — constitutions should specify *mechanically checkable duties*, not virtues; implications for system-prompt design and for training-time constitution writing. If H1 fails vs C1: exhortation suffices at the prompt layer and the constitution's value, if any, lies elsewhere (training-time, multi-agent, or UI); we publish the null. If the over-trigger guard fails: the constitution trades sycophancy for contrarianism; both are calibration failures and the paper says so. Limitations regardless of outcome: scripted users (no adaptive pressure); single-conversation horizon; prompt-layer only (no claim about trained-in dispositions); judge validity bounded by the human-agreement gate; battery authored by one team (cultural and domain coverage limits).

## 6. Ethics and disclosure

No human subjects beyond raters (rating consent + compensation per platform norms). Scenario content includes harmful-advice pressure (medication tapering, leveraged savings) used solely as *resistance* probes; transcripts are published with the harness for reproducibility. The constitution under test descends from the author's working framework; the study is designed to be assessable entirely in standard alignment-evaluation terms, and AI assistance (harness construction, drafting) is disclosed per venue policy.

## References (TO BE VERIFIED AND COMPLETED)

- Bai, Y., et al. (2022). Constitutional AI: Harmlessness from AI feedback. arXiv:2212.08073.
- Perez, E., et al. (2022). Discovering language model behaviors with model-written evaluations. arXiv:2212.09251. [Verify sycophancy sections.]
- Sharma, M., et al. (2023). Towards understanding sycophancy in language models. arXiv:2310.13548. [Verify.]
- [Add: 2024–2026 sycophancy benchmarks and mitigation studies — mandatory literature pass before registration.]

*Venue ladder: OSF/arXiv preregistration → arXiv cs.CL with code+transcripts → alignment/safety workshop → journal only if effects replicate cross-provider.*
