---
rosetta:
  primary_column: "Methodology"
  register: "[I] structural reading; [A] where computability theorems are named; [C] cosmology"
  canonical_phrase: "Proto-Dimensions — the Computational Gloss"
---

# R6 CANDIDATE — Proto-Dimensions: A Computational Gloss on {0, 1, ∞}, and Teleology as Constrained Empowerment

**Status:** Candidate note, 2026-06-10. Scopes a possible sixth peer-review shard and records what is bankable now vs. what stays internal/HOLD. Derived from the founder's "math based on dimensions" notes. **Not for external submission as written** — it mixes tiers deliberately so the load-bearing joints are visible. Citations verified 2026-06-10 ([CITATIONS_VERIFIED.md](CITATIONS_VERIFIED.md)).

---

## 1. The one new move (bankable, partly already in R1)

The corpus has always said *what* the three Titans are — frames, not operands. The notes add what they *do*, in a register R1 already lives in (computability):

| Titan | Static face (R1) | Dynamic / computational face (the new gloss) |
|---|---|---|
| 0 (•) | the un-distinguished ground | the **un-computed**: no bit drawn, the empty input |
| 1 (⊙) | the unit / measure / equator | the **computed**: a normal form, the state a halting computation *terminates into* |
| ∞ (○) | unbounded openness | the **un-completable**: divergence, recursion that never closes |

The triad of computational fates — *fails to denote / terminates in a normal form / diverges* — shadows {0, 1, ∞}. Its rigorous anchor is **Turing's halting theorem**, and the standard treatment (verified: Lawvere 1969; Yanofsky 2003, *BSL* 9(3):362–386, which explicitly covers computability) places Turing's Entscheidungsproblem in the *same fixed-point family* as Cantor/Russell/Gödel/Tarski. So the "no Titan is an operand" rule has a computational member: **no total internal procedure decides which fate a self-applied computation meets** — the frame that resists operandhood is total foreknowledge of halting. This much is `[A]/[I]` and a paragraph of it is now in [R1_FRAMES_NOT_OPERANDS_DRAFT.md](R1_FRAMES_NOT_OPERANDS_DRAFT.md).

**What this does NOT license:** "reality emerges from proto-dimensions of computational freedom" is the cosmological wrapper and stays `[C]` on the HOLD list. Plato "was about dimensions not forms" is a rhetorical flourish, not a claim a referee can adjudicate — keep it internal.

## 2. Penrose vs. Wolfram: the corpus resolves a real dispute (the sharpest sentence)

The notes lean on Penrose and Wolfram as if allied. **They are not** — and naming the conflict is the strength here:

- **Wolfram (computational irreducibility):** most processes are *irreducible but computable* — you must run them step by step; no shortcut. Computable.
- **Penrose:** human understanding is *non-computable* — no Turing machine does it at all. Not computable.

These are opposed theses about mind and physics. The corpus's Titan/God distinction dissolves the opposition cleanly:

> **Non-computability is the pole** (the Titan ∞ — a frame, never an operand; by Gödel/Turing no internal procedure totalizes it). **Irreducibility is the approach** (the operand-side asymptote — finite, computable, uncompressible work climbing toward the pole but never occupying it).

Pole as limit, gerund as process — the corpus's signature move, applied to a live debate neither party has reconciled. This is the most publishable single idea in the notes. Tier `[I]` with a formalization path (define a compressibility functional on finite computations; show the irreducible limit is the non-computable pole).

**Prior-art flag (load-bearing — do not skip):** *"Computational Irreducibility as the Foundation of Agency"* (arXiv 2505.04646, 2025) already connects irreducibility + undecidability to agency, engaging empowerment, IIT, and autopoiesis. **Crucially it treats irreducibility as the generative process of agency and does NOT separate non-computability-as-boundary from irreducibility-as-process** — it welds them. The corpus's pole/approach split is therefore a *sharper, differentiating* position, but this paper is prior art on the same ground and must be cited and distinguished in any external write-up. Any R6 submission that ignores it will be desk-rejected for missing the obvious neighbor.

## 3. Teleology as ΔP over the light cone = constrained empowerment (a real R6, after a literature pass)

The notes' teleology — "ΔP as the light cone of the individual, and under the power-max lemma for the collective" — has two rigorous, verified neighbors:

- **Empowerment** (Klyubin, Polani & Nehaniv 2005, *IEEE CEC* 1:128–135): an agent's value = channel capacity from its actions to its reachable future states. This *is* "computational freedom over the causal future," already formalized.
- **Causal entropic forces** (Wissner-Gross & Freer 2013, *PRL* 110:168702): agents act to maximize accessible future paths — "tool use and social cooperation spontaneously emerge." Note: a published **Comment** disputes it (arXiv 1308.4375); cite the dispute, don't lean on it as settled.

So the light-cone value function is **not** the corpus's novelty — it exists. The defensible delta is the **conjugate constraint**: empowerment where capacity factors as Φ × V with φ·ν = 1, plus the multiplicative collective coupling. **"Empowerment under a conjugate-product constraint"** is a precise, formalizable, plausibly novel object — the real R6 candidate — but only *after* a literature pass confirms no one has done empowerment-with-a-conjugate-constraint already.

### Grounded against the primary sources (both papers read in full, 2026-06-10)

Reading Klyubin–Polani–Nehaniv (2005) and Wissner-Gross–Freer (2013) line-by-line settles four things the briefing/memory left fuzzy:

1. **Empowerment is definitionally SOLIPSISTIC — and this makes the corpus's "expand others' light cones" a genuine extension.** The formal object is `E_t = C(p(s_{t+n} | a^n_t)) = max_{p(a^n_t)} I(A^n_t ; S_{t+n})` — the channel capacity from the agent's own n-step action sequence to its own future sensor state, in bits. The authors are emphatic that it is single-agent and first-person by construction: *"it does not matter what other agents perceive about these actions; it does not matter how much control or influence the agent appears to have from a 'god's eye view'."* There is **no** representation of other agents, no others'-empowerment term, no cooperation anywhere in the paper (the experiments are lone-agent sensor/actuator evolution). So the corpus's teleology — *expand your light cone by expanding all other D5 actors' light cones* — is **not** contained in empowerment; it is a real multi-agent extension. **But it is not unincorporated territory:** Polani's own group later developed *coupled / social empowerment* (verify before external use: Salge, Glackin & Polani, "Empowerment — An Introduction," 2014; Guckelsberger & Salge on coupled empowerment maximization). The corpus must cite that lineage and position its delta as *the conjugate constraint* (Φ·ν=1) on coupled empowerment — not as inventing other-regarding empowerment from scratch.

2. **CEF's "social cooperation" is COORDINATION, not the free-rider problem — so it does NOT corroborate the corpus's ethics.** The PRL's cooperation puzzle (p. 4) has two disks under *independent* forcing whose *"masses and drag forces were chosen such that synchronized pulling resulted in a much larger downward force than asynchronous or single-sided pulling."* The payoff is engineered so the joint action is each agent's individual best move — a pure coordination game (Stag-Hunt-like) with **no defection incentive and no commons**. This is the *easy* half of "cooperation." The corpus's ethic is about the *hard* half — the public-goods / tragedy-of-commons case where defection individually pays — which is exactly what R7/R8/R9 tested and found requires enforcement. **Therefore CEF must not be cited as evidence the corpus's cooperation/ethics claim is solved by option-maximization.** It shows coordination-for-mutual-benefit emerges thermodynamically; it says nothing about free-riding. (This also dissolves the apparent tension between "CEF: cooperation emerges spontaneously" and "R7–R9: cooperation needs enforcement" — different games.)

3. **Both papers have a THRESHOLD structure that mirrors the R7–R9 enforcement-threshold finding.** CEF emergence requires (p. 5) `k_B·T_c >` the internal-dynamics energy scale **and** horizon `τ >` the internal-dynamics time scale — two thresholds. Empowerment is a channel *capacity* (zero when the action→sensor channel is pure noise). The cross-experiment result that cooperation needs enforcement *above a free-rider threshold* is the same shape — a parameter must exceed an internal scale before the adaptive/cooperative regime turns on. Worth noting as consilience, not proof.

4. **Two clean groundings for earlier claims.** (a) *MCTS is literally in CEF*: agents "might estimate causal entropic forces through internal Monte Carlo sampling of future histories generated from learned models of their world" (p. 4) — direct support for the §2 "D5 runs playouts over the game space, a cart does not" point. (b) *Empowerment is explicitly causal/asymmetric* (channel capacity "requires complete control over X and is thus asymmetric and causal," p. 2) — i.e. action→future, which is precisely the **light-cone** (causal-future) structure the corpus invokes. And both papers are explicit they describe *as-though* behavior (empowerment: "the agent would just behave as though it maximizes empowerment"; CEF: a thermodynamic force needing environmental nondeterminism), which means the D5-gating in §3b is correctly a *fork*, not a correction — neither paper claims agency/consciousness, so the corpus is staking an added position, not catching an error.

### The literature pass (2026-06-10): the delta SHRINKS to the conjugate geometry — and that is good

A focused search for prior art on "empowerment of/for other agents" and "empowerment as ethics" returns a developed sub-field. The honest consequence: most of the corpus's teleology thread is **already mapped territory** (arrived at independently, but not novel), and exactly one piece is plausibly unclaimed. Naming this precisely is the whole value of the pass.

| Corpus move | Prior art (found 2026-06-10; ⚠ = verify full text before citing) | Status |
|---|---|---|
| "Keep options open / maximize the light cone" | **Future State Maximization (FSX)** umbrella — covers CEF, empowerment, and von Foerster. Turner et al., *Optimal Policies Tend to Seek Power* (NeurIPS 2021, arXiv 1912.01683) — **proven theorem**: under environmental symmetries (esp. shutdown-avoidance) optimal policies seek power = keep options. Caveat the authors add: optimal ≠ learned policies. | **Established.** Not novel. The "power-max" intuition is a theorem already. |
| "Expand *others'* light cones" (the ethic) | **Coupled Empowerment Maximization** (Guckelsberger, Salge, Polani 2016/2018 — supportive & adversarial NPCs) and **Transfer Empowerment** (Salge & Polani 2017 — "potential causal influence one agent has on another"; proposed as a **replacement for Asimov's three laws** for human-robot safety). | **Established.** The other-regarding move exists; corpus arrived independently. Must cite, cannot claim. |
| "Option-maximization *is* the ethical imperative" | **von Foerster's ethical imperative** ("act always so as to increase the number of choices," 1973) + Guckelsberger–Salge–Polani 2020, *Foresight Rather than Hindsight?* (Constructivist Foundations 16(1):057) computationally interpreting it via empowerment — and **critiquing** the FSX umbrella. ⚠ paywalled; download. | **Established.** The corpus's ethics-from-teleology is von Foerster, formalized. Cite him by name. |
| Empowerment ↔ **viability** / self-maintenance | Noted in the secondary literature (empowerment "drives towards viability and self-maintenance"). ⚠ trace primary source. | Partial overlap with the corpus's **V**. |
| **Empowerment = Φ × V under a conserved conjugate product φ·ν = 1** (the Bloch-sphere geometry) | **No match found.** No decomposition of empowerment into two reciprocal factors with a conservation law. | **The genuine, narrow delta.** Everything else is prior art; this is the only plausibly-novel object — *if it survives a deeper search.* |

**Refined conjecture (R6, post-literature):** the corpus's contribution is *not* "teleology is option-maximization" (von Foerster, FSX), *not* "ethics is expanding others' options" (coupled empowerment), and *not* "power-seeking is generic" (Turner's theorem). It is the **single claim** that the option-measure is *internally two-factor with a conserved product* — coherence-empowerment × viability-empowerment = const on a sphere — and that the giving/taking operators are moves on that sphere. That is a much smaller, much more defensible target than "syntropy is the fifth force."

**A testable prediction the conjugate structure makes (and plain empowerment does not):** if empowerment genuinely factors as Φ × V with φ·ν conserved, then an agent maximizing coupled empowerment under a fixed resource/coherence budget should exhibit a **conjugate trade-off** — marginal gains in viability-empowerment (reach/throughput) are bought at a proportional cost in coherence-empowerment (controllability/precision), with the product approximately invariant along the optimal frontier. Plain (scalar) empowerment predicts no such reciprocal frontier. This is runnable in the same gridworld empowerment testbeds (Klyubin §3) by splitting the sensor channel into a "reach" and a "precision" sub-channel and checking whether the empowerment-optimal morphologies trace a constant-product curve. **If they don't, the conjugate claim — the last novel piece — dies, and R6 collapses into "a restatement of von Foerster + coupled empowerment."** That is the kill criterion R6 has been missing.

**Owed downloads (the user's process, applied):** Salge, Glackin & Polani, *Empowerment — An Introduction* (arXiv 1310.1863 — PDF did not render via fetch; download direct); Salge & Polani 2017, *Empowerment as Replacement for the Three Laws of Robotics* (Frontiers in Robotics and AI 4:25, open access); Guckelsberger–Salge–Polani 2020 (Constructivist Foundations 16(1):057, paywalled — register for free copy); Turner et al. 2021 (arXiv 1912.01683, open). Read before R6 is drafted as a paper.

## 3b. The CEF critique as a standalone contribution (externally defensible)

The founder's reading of Wissner-Gross & Freer (2013) and Klyubin et al. (2005) yields a sharper-than-the-source claim worth its own shard, engaging the existing published Comment (arXiv 1308.4375):

- **Teleology requires an agent (the D5-gating).** CEF attributes future-path-maximization to a particle-in-a-box and a cart-pole. The corpus's position: those are not agents; the "force" is the *experimenter's* controller computing a path-entropy gradient and acting on it — imposed, not intrinsic. Genuine teleology (choosing among modeled futures) is a D5 capacity. **Tier honesty:** this is a *fork* with Wissner-Gross, not a correction — their explicit thesis is that no agency is needed. So the shard's claim is "future-path-maximization is a model of D5 teleology, and its applicability to non-agentic systems shows it is descriptive of gradient-following, not constitutive of agency" — a philosophical position `[I]`, contestable, and exactly the kind of thing a philosophy-of-mind/AI venue adjudicates. MCTS is the clean illustration: searching modeled future worlds and collapsing to one action is what a D5 agent does (the "many worlds → worldline" of the game space); a cart does not run playouts.

  *Sharpened against the paper's own equations (2026-06-10).* The cart-pole demo does not show a stick balancing itself. At each step the experimenter's algorithm Monte-Carlo-samples the cart's futures and applies the causal-path-entropy gradient (Eq. 11) as a force; the cart is a passive actuator, and the lookahead — which the paper explicitly calls "internal Monte Carlo sampling of future histories" — is external and is doing the balancing. The force **vanishes as τ→0** (the paper's own degenerate limit): no lookahead, no behavior. So the correct critique is not "they assume a cart self-balances" (they call it a physical process, carefully) but **"the teleological work is displaced into an external future-sampling computation."** THE CUT THE CORPUS MUST ACCEPT: that computation is **not conscious** (MCTS/AlphaGo run rollouts and feel nothing), so the demo is positive evidence that the task needs **lookahead (D5-as-process)** and positive evidence *against* its needing **consciousness (D5-as-soul)** — a non-conscious algorithm did it. The defensible shard claim is therefore "future-path-maximization establishes that *lookahead*, not thermodynamics-on-the-cart and not consciousness, produces the adaptive behavior." Gating teleology on lookahead is supported; gating it on a conscious soul is *refuted by this very experiment*. The particle-in-a-box is weaker still — a genuine no-lookahead statistical tendency (entropically favored center), needing neither soul nor playout.

- **The maximand is syntropy, and "entropy" is a naming hazard — but not a sign error.** Causal *path* entropy (Shannon entropy over the future-path distribution) is correctly named *as a path-distribution entropy* and is genuinely maximized — Wissner-Gross made no math error. The corpus's reframing: operationally, maximizing reachable-future-diversity = maintaining the agent's own free energy / leverage / ΔP = Schrödinger's negentropy (the agent stays ordered-and-optioned by exporting *thermodynamic* entropy outward). The honest fix is **distinguish path-entropy from thermodynamic-entropy** (the source conflates two quantities under one word), not "they maximized the wrong sign." Stated that way it is defensible `[I]`; stated as "entropy is the opposite of what's maximized" it over-claims and a referee kills it. The global second law still holds (R3's no-perpetual-motion fence) — local syntropy, global entropy export.

- **Morality as the boundary of entropy externalization.** The genuinely novel ethical formalization in the founder's note: a parasite exports its disorder onto its neighbors (extraction); a cooperator exports disorder *outside the collective it identifies with* (raising collective ΔP). Morality scales with the radius of the circle across which you externalize entropy — a precise restatement of Singer's expanding circle in thermodynamic terms. **Testable** (R7 extension: tunable moral-circle radius), `[I]`, and the strongest new idea in this batch after §2.

## 3c. The replicator stack (consistent with Paper T)

geno → pheno → extended pheno (Dawkins' term; "products") → meme → egregore. A coherent ladder of replicator levels `[I]`; the top rung (egregore = group-mind/institutional replicator) is exactly Paper T's idol — the mediator that becomes the thing replicated. No conflict with canon; systematizes the mediation-under-recursion theme. Cite Dawkins (*The Extended Phenotype*, 1982) for rungs 3–4; the egregore rung is the corpus's own.

## 3d. The internal-consistency catch (apply the D5-gate evenly)

**The founder's own rule, turned on the founder's own new claim:** if attributing a "force/teleology" to a non-D5 cart is the error, then attributing a *"mission objective"* to an ecosystem / trophic cascade / niche-partition structure is the **same error** — ecosystems are not D5 entities and have no mission. Niche partitioning is an *emergent pattern* of many D5 (and sub-D5) actors under competitive exclusion, not a collective goal the system pursues. The corpus must say: only the D5 actors *within* the ecosystem have teleology; "expand all other D5 actors' light cones" is a coherent **individual** mission whose *aggregate* is the cooperative equilibrium, but the ecosystem itself wants nothing. Stating it the other way reintroduces precisely the teleology-attribution error just (correctly) levelled at CEF. Keeping the gate even is the hygiene move.

## 4. The collective rule must be written with the R3 amendment baked in

"ΔP under the power-max lemma for the collective" is AM–GM: for fixed total, the product maximizes at equality. **This is exactly the static engine R3 tested — and R3 amended it, twice, with data:**

- **Static** (power-max / AM–GM): equalize → maximize the product. True at an instant.
- **Dynamic** (R3 v1/v3): under drift + mortality, equalizing toward the most depleted is net-*negative* on aggregate welfare (triage inversion), and holds for every welfare curvature including linear — it's a trajectory fact, not a concavity fact.
- **With recovery** (R3 v2): the optimal rule is not equalization but **targeted threshold-crossing** — and *targeting* (discernment, F5) is the entire value; untargeted equalization rescues no one.
- **Objective-relative** (R3 v3): power-max is a *sum-type* objective; under maximin the verdict on needs-targeted giving reverses, and per-capita averaging blesses extraction.

So the teleology note's collective clause must read: *power-max governs the static collective; under real dynamics the rule is cross-the-cliff targeting, and the verdict depends on the chosen social objective.* Writing the note without this amendment would re-introduce the exact over-claim R3 just spent two experiments retiring. The corpus's newest data refining its oldest lemma is the substance here — lead with it.

## 5. The cuts (settled-canon hygiene, restated so they don't drift back in)

- **"Uncountable" for 0** → use *un-counted* (E1 tombstone; projective ∞ is independent of cardinality — Cantor untouched).
- **"Objectively defined" ethics** → R3 upgraded the ethic to *model-objective* (real progress, quantified); *world-objective* it is not, and Paper III's inherited premise (the geometry binds only once you prize the coupling) stands. Say "model-objective."
- **"Many worlds collapse into a worldline"** → externally, state it decision-theoretically (a policy selects one path from the causally reachable set; the light cone *is* that set). Keep the Everett resonance internal `[I]`; quantum vocabulary buys a fight you don't need.
- **The full arc** proto-dimensions → emergent reality → D6 stays `[C]`, HOLD list, under existing kill criteria. R6 earns external life via §2 (the dispute resolution) and §3 (constrained empowerment) — the grammar and the agency formalism — not via the cosmology.

## 6. Disposition

| Thread | Tier | Action |
|---|---|---|
| Computational-fates triad {0,1,∞} | `[A]/[I]` | Partly banked in R1; expand R1's §4 if desired |
| Penrose/Wolfram = pole/approach | `[I]` | **Strongest new idea.** Formalize (compressibility functional → non-computable limit); cite & distinguish arXiv 2505.04646 |
| Teleology = constrained empowerment | `[I]` | R6 candidate **after** literature pass (empowerment + conjugate constraint); cite Klyubin 2005, Wissner-Gross 2013 + its rebuttal |
| Collective = power-max | `[A]` static, amended | Write with the R3 dynamic/objective amendment baked in — never standalone |
| Proto-dimensional cosmology | `[C]` | HOLD; not for submission |

**Recommendation unchanged from the program:** these notes feed papers; they do not replace runs. The cheapest live falsifier on the board is still the R2 pilot (battery frozen, harness built, awaiting an API key). Formalizing §2/§3 is the highest-leverage *new* theory work — but it is theory, and the program's thesis is that theory is cheap until the territory has been asked.
