---
rosetta:
  primary_column: "Methodology"
  register: "[S] capstone; each item carries its own tier"
  canonical_phrase: "Findings, Achievements, Conjectures"
---

# Peer Review Program — Findings, Achievements & Conjectures

**Capstone as of 2026-06-10.** A consolidated, honestly-tiered record of the program. Governing discipline (held throughout): the weltanschauung is the *generator*; what gets submitted are field-native *shards*. Claimed novelty is allowed — expected — to shrink under grounding. Refutations and self-corrections are logged beside confirmations, because the confirmations are only worth anything if the refutations were honored. Tiers: `[A]` proven/model-internal-fact or web-verified; `[I]` interpretive; `[C]` conjectural; `[S]` structural/program.

---

## 1. Achievements (what was built and done)

- **The program itself.** R1–R9 slate framed as shards cut from the corpus, each translated into a field's own register with no in-house vocabulary, kill criteria as Limitations, AI disclosure, preprint-before-journal. ([00_PROGRAM.md](00_PROGRAM.md))
- **Seven paper artifacts drafted.** R1 full draft (philosophy of math); R2 + R4 registered-report drafts; R3 full draft *with executed results*; R5 full draft; R6 candidate note; R7/R8/R9 results documents. All in journal register.
- **A runnable benchmark.** R2 harness: 6 system-prompt conditions, a **43-adversarial + 12-control battery hash-frozen** (`R2_HARNESS/`, SHA-256 recorded), scripted-user runner, structured-output LLM judge, aggregation with Wilson intervals. Smoke-tested end-to-end; awaits an API key for the live pilot.
- **Ten simulation runs across four conjectures**, stdlib + deterministic: R3 ×3 (transfer/regeneration/robustness), R7 ×2 (cooperation emergence), R8 ×2 (moral circle), R9 ×3 (holobiont/multilevel; two void+logged).
- **Citation verification.** 11 memory-drafted anchors web-checked → **11/11 exist, 0 fabricated**, venues/pages correct. ([CITATIONS_VERIFIED.md](CITATIONS_VERIFIED.md))
- **Two primary sources read in full** (causal entropic forces; empowerment) and grounded against their own equations.
- **Full literature-grounding pass.** All six paper-clusters grounded against real fetched sources (5 via parallel research agents, R6 by hand). ([LITERATURE_GROUNDING.md](LITERATURE_GROUNDING.md))
- **The empirical ledger is no longer empty** — the program's whole reason to exist.

## 2. Findings (what was actually shown)

### 2a. Model-internal experimental results `[A]` within the stated models

- **The triage inversion (R3).** Under downward drift + an absorbing mortality boundary + concave welfare, a *sequence* of progressive Pigou–Dalton transfers — each instantaneously welfare-improving — can **reduce** aggregate welfare-time. The static transfer axiom and the dynamic survival accounting point opposite ways.
- **It is trajectory-driven, not curvature-driven (R3 v3).** The inversion holds even under *linear* welfare (no concavity), because lifetime welfare under drift-to-absorption is convex in initial health. A self-correction was logged here: v1's "random transfers keep a Jensen gain" was re-identified as a **boundary/payment-clipping artifact**.
- **The verdict is objective-relative (R3 v3).** Under sum welfare, progressive giving is worst; under **maximin it is best** (worst-off lifetime welfare ×10); under **per-capita averaging, extraction wins** (culling the weak raises the average). The social-welfare function is morally load-bearing — quantified.
- **Threshold restoration (R3 v2).** With regeneration that outruns drift above a cliff, **targeted** transfers dominate (100% survival, +26% welfare); untargeted transfers of equal volume rescue no one. Targeting (discernment), not transfer volume, is the binding variable.
- **Cooperation needs more than horizon or shared fate (R7/R8).** Pure self-interest + long horizon does **not** yield cooperation (free-riding wins); reciprocity (a club good / K*) + long horizon does. The "moral circle as entropy-externalization boundary" is collectively optimal (~10× productivity) but **individually free-ridden at every horizon** (the parasite always invades).
- **Group structure alone does not build a holobiont (R9).** A correctly-built haystack model fixates on parasites even at minimum founder size. "A basket of parasites consumes itself" is **confirmed** (≈10× productivity gap) but **insufficient** — within-group selection refills parasites faster than group extinction purges them.
- **The convergent result.** Across three independent mechanisms, cooperation/mutualism/the holobiont is collectively optimal but **never the default**; it requires **enforcement above a free-rider threshold**, and the corpus's *fenced* demons (bounded conditional punishment) map onto exactly the enforcement the major-transitions literature says every new level of individuality required.

### 2b. Verified external facts `[A]`

- **The Suda chart *is* the velocity chart (2026-06-11).** Suda's bounded Cayley coordinate `u(x) = (x−1)/(x+1)` and special relativity's velocity-from-rapidity `β = tanh(w)` are **the same function**: `u(x) = tanh(½ ln x)`, so evaluating Suda's chart at the *squared* Doppler factor `x = k² = e^{2w}` returns `β = v/c` exactly (verified to 1e-12 across w ∈ [0,6]). The three Suda charts — multiplicative `x`, additive `s = ln x`, bounded `u` — are, in physics, the **Doppler factor `k`, the rapidity `w`, and the velocity ratio `β`**. The unit `x = 1` (Suda's self-dual fixed point) is rest (`w = 0, β = 0`); the boundary `u → 1` (Suda's "egg of infinity") is `β → c`. This is `[A]`: a coordinate identity, not a physical claim. What it *means* — that the framework's three faces of the One and relativity's three faces of motion coincide because both are the geometry of reciprocal closure on the line — stays `[I]`. **It does not show that c is "caused by" the µ-limit, nor that consciousness travels at c** (see the fence on conjecture C-µ below).
- **The CEF cart-pole is driven by an external Monte Carlo lookahead, not self-balancing** (read from the paper's own Eq. 11; force vanishes as τ→0). This *supports* gating teleology on **lookahead** and *refutes* gating it on **consciousness** (a non-conscious algorithm did it).
- **Empowerment is definitionally single-agent/solipsistic** — so the corpus's "expand others' light cones" is a genuine multi-agent extension, but one with a developed prior literature (coupled/transfer empowerment; von Foerster's ethical imperative; Turner's power-seeking theorem).

### 2c. Meta-findings (the program's epistemics working) `[S]`

- **Grounding shrinks novelty everywhere — and that is the pass succeeding.** Every paper's claimed novelty contracted under the literature pass; the genuine delta was located in each case (or, for R7–R9, shown possibly absent).
- **The program self-corrected repeatedly and logged it** (R3 artifact; R8 KAPPA mis-parameterization; R9 two void runs).
- **The refusal to overfit (R9).** When three consecutive interventions each appeared only after a claim failed, the run **stopped rather than tune enforcement to force a confirmation** — the dogmatic-reversion trap, declined and recorded. This is the single most important entry in the ledger.

## 3. Conjectures (open, ranked by surviving delta after grounding)

| # | Conjecture | Tier | Status after grounding | Kill criterion |
|---|---|---|---|---|
| ~~1~~ | ~~Empowerment = Φ × V under a conserved conjugate product φ·ν=1 (R6)~~ | `[A]` refuted | **REFUTED 2026-06-10** ([R6_CONJUGATE_RESULTS.md](R6_CONJUGATE_RESULTS.md)). The decomposition is **additive (simplex), not multiplicative (sphere)**: E = H(S)−H(S\|A), so iso-empowerment sets are lines, "φ·ν" = 2^E (tautology), and φ·ν=1 is the *dead state*. Empowerment is **reach-dominated, never balanced** — and mortality does not rescue balance (3 cost models, falsified) because balance is structurally empowerment-dead. **Deep consequence:** the corpus's "one geometry at all scales" fails here — the sphere fits the *organizational* register (Kremer weakest-link, R4) but **not** the teleology register (additive simplex). The teleology thread now has *no surviving novel formal claim*. | Kill criterion fired (twice) and was honored. |
| 2 | **The 0/1/∞ triptych + the Euclid→Stevin→Buckingham→2019-SI arc as one story** (R5) | `[A]` history, `[I]` thesis | Strong, narrowed delta. Rotman already framed the *unit* as a displaced frame — so the novelty is the **three-item** triptych + the single historical arc, not "the unit is a frame." | If Rotman/de Courtenay already triangulate all three items or the full arc → exposition, not a claim. |
| 3 | **Two-factor multiplicative structure of evaluated productivity** (R4, the keystone) | `[I]` | The multiplicative *mechanism* is old (O-ring, elimination-by-aspects). Delta = the specific **coherence×viability** content + a **product-vs-sum outcome-prediction** test on recovered latent factors. | Additive ≥ multiplicative on cross-validated outcomes; or a single general factor predicts as well; or no floor non-compensation. |
| 4 | **Frame/operand signature extends to arithmetic boundary forms (0/0, ∞) + metrology** (R1) | `[I]` | Priest's Inclosure Schema owns the set-theoretic+semantic unification. Delta survives only in the boundary-forms/metrology legs. | Can a real Lawvere/Inclosure **fixed-point witness** be built for 0/0? If not (predicted), it is family resemblance, not reduction. |
| 5 | **D5-gating of teleology** | `[I]` fork | Narrowed by the CEF reading: **D5-as-lookahead is supported; D5-as-consciousness is refuted** by the cart-pole. | Name one task whose behavior provably needs a *conscious* lookahead, not a mechanical one. None named ⇒ gate stays at lookahead. |
| 6 | **The descent asymmetry / arrow as a boundary condition** (Paper W) | `[I]/[C]` | The static engine = Pigou–Dalton; the dynamic claim was *amended* by R3 (triage). | Inherited from R3's kill criteria. |
| 7 | **R7–R9 as a theoretical contribution** | `[I]`→? | **Most at-risk.** "Cooperation needs enforcement above a threshold" is mainstream (Nowak's five rules *are* threshold inequalities; punishment is not a separate mechanism). Possible delta only in the specific mortality/conjugate-welfare currency, or as synthesis. | If the currency reduces to b/c (Nowak) or assortment (Fletcher-Doebeli 2009) → no theoretical novelty; publishable only as pedagogy. Plus: **"holobiont" is a contested term** — must be framed as tested, not assumed. |
| 8 | **The proto-dimensional cosmology** (D0→D6, force-ladder, "syntropy as fifth force") | `[C]` | **HOLD list — not for submission.** Paper P's SU(3) obstruction stands; "fifth force" must never be said to a physicist. | Earns external life only via the grammar (R1) and the bench (R2/R4) first. |
| C-µ | **c as the µ-limit / "qualia moves at c"** — the intuition that the speed of light *is* the bounded-chart boundary (`u → 1`, `β → c`) and that D5 experience is the emergent phenomenon at that limit | `[C]` speculative | **The coordinate half is now `[A]` (finding 2b): `β = tanh(½ ln k²)` makes c the image of Suda's egg-of-infinity boundary exactly.** But that is a *map* coincidence — both relativity and the framework are reciprocal-closure-on-a-line, so they share the `tanh` chart. The *physical* leap ("c is caused by the µ-limit," "consciousness propagates at c") is **not supported** and conflates a coordinate boundary with a causal mechanism. Held as `[C]`, never upgraded by the identity alone. | Name one *measurable* prediction that the µ-limit reading makes about c or about experience that special relativity + neuroscience do not already make. If none ⇒ it is interpretation (a beautiful chart-coincidence), not physics. |

## 4. The honest scoreboard (revised 2026-06-10 after the R6 test)

- **Cleanest shot:** **R5** (the 0/1/∞ triptych + the Euclid→SI arc) — now the single strongest surviving delta, since R6 fell.
- **Real but narrow:** **R4** (the coherence×viability prediction test — *and* the register where the corpus's multiplicative geometry is actually appropriate, per the R6 result); **R3** (sign-flip of the transfer axiom under mortality); **R1** (the boundary-forms leg, pending the 0/0 witness).
- **Refuted:** **R6** — the teleology/conjugate-geometry thread has no surviving novel formal claim. Recorded plainly. The empowerment register is an additive reach/precision simplex, not the corpus's sphere.
- **Most honest verdict owed:** R7–R9 may have *no* theoretical novelty — a clean re-demonstration of the major-transitions consensus.
- **On hold by design:** the cosmology and theology.
- **The biggest structural finding of the whole program:** the corpus's signature claim — *one geometry (φ·ν=1 sphere) at all scales* — is **register-dependent, not universal.** Multiplicative for organizations (weakest-link); additive for empowerment/teleology. This is the load-bearing correction the program produced.
- **Corrections banked:** Axelrod & Hamilton 1981 = *Science* **211** (not 314); Hardin 1968 ends p. **1248**; Suda tier `[A]→[I]`.

## 5. Next moves (no API key required, except the R2 pilot)

1. Integrate the load-bearing prior art into the drafts: **Priest→R1, SWAY→R2, Social Protection Paradox→R3, Rotman→R5, holobiont critiques→R9.**
2. The two decisive low-cost tests: the **conjugate trade-off frontier** in an empowerment testbed (R6, decides if the one clean delta is real) and the **R3 reflecting-boundary control** (proves the inversion is absorption, not curvature).
3. The R2 pilot the moment an `ANTHROPIC_API_KEY` is present.
4. The owed downloads (paywalled prior art) are listed per paper in [LITERATURE_GROUNDING.md](LITERATURE_GROUNDING.md).

---

*The through-line: a worldview that built an honesty machine was held to it. The program's value is not that it proved the corpus right — it mostly didn't — but that it found, for each claim, exactly how much is already known, how much is genuinely open, and what single test would decide it. That is the corpus's own discipline, turned outward and survived.*
