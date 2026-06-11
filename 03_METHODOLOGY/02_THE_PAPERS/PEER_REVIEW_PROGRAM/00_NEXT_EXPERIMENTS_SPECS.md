---
rosetta:
  primary_level: L3
  primary_column: "Methodology"
  operator: "Kṛṣṇa ◇"
  tier: "God · giver"
  regime: "Vaiśya"
  register: "[S] the protocols; [C] the hypotheses they decide; [A] the statistics"
  canonical_phrase: "Next experiments — the three tier-moving tests"
---

# Next Experiments — The Three Tier-Moving Tests

**Status:** Specifications, 2026-06-11. These are the three experiments whose *outcomes* would move a load-bearing claim across an evidence tier — written as decision protocols (hypothesis, method, statistic, decision rule, kill criterion), not as results. None is run here. Two need no API; the R2 pilot (separate) needs a key.

**Why these three.** After the 2026-06-11 mass-shell finding and the constrained-optimization reconciliation, the framework's live uncertainty narrows to three forks:
1. **Where** does the symmetric balance-sphere actually apply? (E1 — the exponent fork)
2. **Does** the multiplicative structure survive in the *reflexive* register R6 left untested? (E2 — R10's kill criterion)
3. **Is** the µ-limit/qualia reading physics or a chart-coincidence? (E3 — the C-µ kill)

Each is designed to be *decisive in both directions* — a clean refutation is as valuable as a confirmation, per the program's R9 discipline.

---

## E1 — The Exponent-Measurement Protocol (the balance-form fork)

**The question.** R6 proved the multiplicative sphere is *register-dependent* — true for organizations (R4, weakest-link), false for single-agent empowerment (additive simplex). That verdict is a **map with no coordinates**: it says "depends" without saying *where*. E1 measures the boundary directly, turning "register-dependent" from a verdict into a measured map.

**The hypothesis under test.** In a given domain, evaluated performance `P` is one of three shapes:
- **Additive:** `P ≈ a·Φ + b·V` — substitutable factors (R6's empowerment register).
- **Multiplicative-symmetric:** `P ≈ Φ·V` with an **interior** optimum at `Φ=V` — the balance-sphere (the corpus's signature claim).
- **Multiplicative-asymmetric:** `P ≈ Φ^a·V^b`, `a≠b`, with a **corner** optimum — conjunctive but *not* balance (Lanchester's Square Law lives here: `q·N²`).

**Method.**
1. Pick a domain with a measurable outcome `P` and ≥2 recoverable latent inputs (extends the R4 two-factor blind-study method — `R4_TWO_FACTOR_BLIND_STUDY_PREREG.md`).
2. Recover the latents (factor analysis / SEM) **blind to the hypothesis** (pre-register the factor model).
3. Fit, with nested cross-validation: (i) additive `P = a·Φ + b·V`; (ii) Cobb-Douglas `log P = a·log Φ + b·log V`; (iii) a free-form GAM as the non-parametric ceiling.
4. Read two numbers: **(α)** does multiplicative beat additive on held-out `R²`? **(β)** is `a/b ≈ 1` (symmetric, interior optimum) or `a/b` far from 1 (asymmetric, corner)?

**Decision rule.**
| Result | Verdict |
|---|---|
| additive ≥ multiplicative (CV) | the product law fails here — R6-style register |
| multiplicative, `a≈b`, interior optimum, **floor non-compensation** (low `Φ` cannot be bought off by high `V`) | the **symmetric balance-sphere holds** — `[I]→[S]` for this register |
| multiplicative, `a≠b`, corner optimum | conjunctive but **not** the balance-sphere (a Lanchester-Square register) |

**What it moves.** Across 3–4 domains (organizational performance, team output, ecological mutualism, firm productivity) this builds the **actual map** of where the sphere applies — the deliverable R6 implied but did not draw. **Kill criterion for the corpus's universality claim:** already fired (R6). **Kill criterion for the *organizational* claim (R4):** additive ≥ multiplicative on cross-validated outcomes in the organizational domain.

**Cost:** no API. Needs a dataset with an outcome and recoverable inputs. Tier of the protocol: `[S]`; the statistics `[A]`.

---

## E2 — The Reflexive-Empowerment Test (R10's kill criterion)

> **Status: EXECUTED 2026-06-12.** Two games (V1) + one documented instrument
> refinement (V2, depth-graded opponents). **Verdict: SPLIT — R10a (reflexive
> interaction) supported `[A]` within models; R10b (conserved conjugate
> product) not recovered, stays `[C]` weakened.** Full report:
> [E2_REFLEXIVE_RESULTS.md](E2_REFLEXIVE_RESULTS.md). The protocol below is
> preserved exactly as registered; two of five registered predictions were
> wrong and are scored as wrong in the report.

**The question.** R6 refuted the sphere for *single-agent* empowerment — but standard empowerment is **definitionally solipsistic** (finding 2c). The 2026-06-11 agency gloss reads `Φ` as **foresight = recursion depth** (modeling other agents modeling you; k-level / cognitive hierarchy) and `ν` as **execution capacity**. That is a *different object*, and R6 never tested it. E2 is the decisive test of conjecture **R10**.

**Street-register statement of the hypothesis `[I]` (2026-06-12).** *"Everybody has a plan until they get punched in the mouth"* (Tyson): adversarial contact **is** the arrival of the second agent — **R6's solipsistic setting contains no punches.** The punch tests whether foresight was *compiled into* execution (`Φ` coupled to `ν`) or merely adjacent to it; *"one kick practiced 10,000 times"* (Lee) is that compilation — depth over breadth at fixed capacity, the conjugate trade this experiment looks for. If E2 finds hyperbolic iso-value sets, these aphorisms were the law speaking in the street register; if it finds lines, they were survivorship poetry. Either way decisive.

**The hypothesis under test.** In a multi-agent game, define `Φ = k` (the depth of recursive belief an agent models) and `ν = c` (execution capacity — action-channel width / reaction speed / payoff bandwidth). Conjecture: there is a **conserved conjugate trade-off** — deeper recursion costs execution bandwidth at fixed achieved value — so iso-value sets are **hyperbolic** (`Φ·ν = const`), the structure R6 found *additive* for the single-agent case.

**Method (extends `R6_SUPPORT_CONJUGATE_EMPOWERMENT_SIM.py`).**
1. Build a 2-agent cognitive-hierarchy game (a sender–receiver game with nested beliefs, or an iterated p-beauty / bounded-lookahead PD). Each agent is parameterized by `(k, c)`: `k` = belief-recursion depth, `c` = execution capacity (bits/round of action channel, or inverse reaction latency).
2. Sweep the `(k, c)` grid; for each, compute the agent's **achieved value** `V(k,c)` against a fixed population.
3. Fit the iso-value frontier: **additive** (`V` iso-sets are lines in `(k,c)`) vs **multiplicative** (`V` iso-sets are hyperbolae, `k·c = const`).
4. Crucially, impose a *real* cost coupling and test whether it's necessary: does deeper `k` *require* lower `c` (compute/latency budget), making the trade-off conjugate rather than free?

**Decision rule.**
| Result | Verdict |
|---|---|
| iso-value sets **additive** (lines) | **R10 refuted** — same as R6; the sphere is dead in the teleology register, full stop, and the agency gloss has no formal teeth beyond [I] |
| iso-value sets **multiplicative/hyperbolic** with a forced conjugate cost | **R10 supported** — the sphere survives in the *multi-agent* register the corpus actually cares about; `φ·ν=1` is the reflexive-empowerment conservation law |

**What it moves.** This is the **single most decisive experiment available** — it tests whether the day's agency gloss (`Φ`=foresight, `ν`=power) is a relabeling or a real conservation law, and it is the one place R6's kill might be *scoped rather than total*. Either way it is publishable: a clean refutation closes the teleology thread honestly; a confirmation is the multi-agent delta the whole program said empowerment was missing.

**Honest prior.** Unknown — genuinely 50/50. The cost-coupling (deeper recursion costs reaction speed) is plausible but not guaranteed to be conjugate (it could be additive in log-cost, which would still refute). **Do not pre-judge; run it.** Tier: `[C]` until executed.

**Cost:** no API. Pure simulation, deterministic, extends an existing artifact.

---

## E3 — The C-µ Kill Test (decide by honest derivation)

**The question.** The mass-shell finding made the *coordinate* half of "c is the µ-limit" exactly `[A]` (`β = tanh(½ ln k²)`). The *physical* half — "c is caused by the µ-limit," "qualia travel at c" — is `[C]`. E3 decides it the way R9 decided its tail: by honest derivation, prepared to demote.

**The hypothesis under test.** Does the µ-limit reading make **any measurable prediction** about `c` or about experience that special relativity + neuroscience do not already make?

**Method (derivation, not simulation).**
1. **The `c` leg.** Enumerate every relation the µ-limit reading asserts about `c`. For each, check: is it derivable from SR alone? (Predicted: yes — the identity is a coordinate change; it adds no physical content. A coordinate identity cannot predict a new value of `c`.)
2. **The experience leg.** State the strongest specific, falsifiable form of "qualia at c" — e.g. *"the temporal rate of conscious integration stands in a fixed measurable relation to `c`"* or *"a balance-function `B = dτ/dt` reading predicts a specific scaling of subjective time with metabolic γ-analog."* For each candidate, check against existing neuroscience (perceptual moment / temporal binding window literature, ~30–100 ms) whether it (a) is already explained, (b) is testable and novel, or (c) is unfalsifiable.

**Decision rule.**
| Result | Verdict |
|---|---|
| **no** measurable prediction survives that isn't already in SR or neuroscience | **demote C-µ: `[C] → [I]`** — a beautiful chart-coincidence, not physics. Record it plainly. |
| **one** specific falsifiable prediction survives | C-µ becomes a **real `[C]`** with a named test; route it to the relevant discipline |

**Honest prior.** Demotion is the expected outcome — the identity is a coordinate change, and coordinate changes don't carry mechanisms. Stating that in advance is the R9 discipline: do not tune the reading until it survives. Tier of the protocol: `[S]`; expected verdict: `[I]`.

**Cost:** no API. A derivation pass + a neuroscience literature check.

---

## Priority and sequencing

1. **E2 first** — it is the most decisive and the most *novel*: it directly tests whether today's central addition (the agency gloss / R10) has formal teeth, and it is the only one that could *reopen* a refuted thread legitimately.
2. **E1 next** — it converts the program's biggest finding (register-dependence) from a verdict into a usable map, and it reuses the R4 machinery.
3. **E3 anytime** — cheap, and its honest expected outcome (demotion) *strengthens* the corpus by shedding a `[C]` overclaim.

All three obey the program's first law (R9): **a clean refutation is a result, not a failure.** Two of the three are most likely to refute or demote — and that is the point.

---

## Read with

- [`00_FINDINGS_AND_CONJECTURES.md`](00_FINDINGS_AND_CONJECTURES.md) — conjecture rows R10 (E2), 3/R4 (E1), C-µ (E3).
- [`R6_CONJUGATE_RESULTS.md`](R6_CONJUGATE_RESULTS.md) and [`R6_SUPPORT_CONJUGATE_EMPOWERMENT_SIM.py`](R6_SUPPORT_CONJUGATE_EMPOWERMENT_SIM.py) — the single-agent result E2 extends.
- [`R4_TWO_FACTOR_BLIND_STUDY_PREREG.md`](R4_TWO_FACTOR_BLIND_STUDY_PREREG.md) — the machinery E1 reuses.
- [`../PAPER_B_BLOCH_BURRI_IDENTITY.md`](../PAPER_B_BLOCH_BURRI_IDENTITY.md) §8 — the mass-shell identity E3 tests the reach of.
