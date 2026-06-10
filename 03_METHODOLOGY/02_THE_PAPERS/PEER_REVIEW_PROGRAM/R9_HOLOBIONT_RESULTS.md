---
rosetta:
  primary_column: "Methodology"
  register: "[A] model-internal results; [I] readings"
  canonical_phrase: "R9 — Holobiont / Multilevel Selection, and a Refusal to Overfit"
---

# R9 — Can a Basket of Symbionts Become a Holobiont? Multilevel Selection, and an Honest Stop

**Status:** Executed 2026-06-10. Three model versions (two void/diagnostic, one clean), plus a deliberate methodological halt. Tests the founder's deepest claim: *a basket of parasites consumes itself and can never be a holobiont; only mutualists integrate into a higher-order individual.*
**Artifacts:** [R9_SUPPORT_HOLOBIONT_SIM.py](R9_SUPPORT_HOLOBIONT_SIM.py) (v1, void), [R9_SUPPORT_HOLOBIONT_SIM_V2.py](R9_SUPPORT_HOLOBIONT_SIM_V2.py) (v2, clean), [R9_SUPPORT_HOLOBIONT_SIM_V3.py](R9_SUPPORT_HOLOBIONT_SIM_V3.py) (v3, +policing). Stdlib, deterministic.
**Tier:** [A] model-internal; [I] readings; the literature this engages (major transitions, multilevel selection) is real and cited.

## 1. What was claimed and how it was tested

The claim sits a level above R7/R8: those showed parasites win the *within-group* invasion; the holobiont claim is that they lose the *war* — a basket of parasites self-terminates, and a new level of individuality (holobiont; multicellularity; the egregore-as-living-unit) can only be built from mutualists. This is the major-evolutionary-transitions thesis (Maynard Smith & Szathmáry 1995; Margulis on endosymbiosis; Wilson & Sober multilevel selection). The test: add group structure to R8 and see whether differential group survival lets mutualism win at the metapopulation level.

## 2. The runs, honestly

**v1 — VOID (logged per A7).** Fixed deme sizes meant mutualist and parasite demes contributed equally to the next generation: no differential group productivity, hence no group selection. Each isolated deme just replayed R8 and fixated on parasites (mean p → 0.98 at every migration rate, m=0 included). A structural omission, not a result.

**v2 — clean haystack model, group structure ALONE.** Implemented the standard mechanism (Maynard Smith haystack / Price-equation between-group selection): small founder groups create between-group variance; demes run ecology; dispersal is productivity-weighted so mutualist demes seed more offspring. Result, across founder sizes F ∈ {2,4,8,20,60}:

```
founder F   final mean p   holobiont frac   outcome
   2            0.96            0.0%         parasite (self-consuming)
   4            0.98            0.0%         parasite
   8..60        0.98            0.0%         parasite
```

**F21 — Group structure alone does NOT save mutualism.** [A] Parasites fixate even at founder size 2 (maximal between-group variance). Within-group selection (parasites free-ride, ~3× individual advantage from R8) refills parasites faster than differential group extinction purges parasite demes — especially with single-generation dispersal, where productive mutualist demes dump their offspring back into a common pool that immediately remixes with parasites. This is the **mainstream consensus**: naive group selection is weak (Williams 1966; Maynard Smith 1964). The founder's "basket of parasites consumes itself" is **confirmed but insufficient** — parasite demes are real and ~10× less productive (R8: 96 vs 1004), yet self-consumption alone does not rescue mutualism, because the parasite is reborn inside every mutualist deme before group selection can act.

**v3 — haystack + within-deme policing (modest strength), and the stop.** Added the corpus's own proposed ingredient — the licensed immune response / fenced demons / Frank's policing (low-p agents tax themselves to harm high-p agents). At the deliberately modest strength tested, it made **essentially no difference** (policing-ON ≈ policing-OFF; parasites fixate in both). Diagnosis: policing within a *single-generation* deme has little leverage before dispersal remixes everything, and the tested strength was small relative to the free-rider advantage.

## 3. The refusal (this is the result that matters most)

At this point the disciplined move is **not** to crank policing strength up until mutualism wins. That is the dogmatic-reversion trap (Paper N): using a posit to fit the desired outcome while shielding it from disconfirmation. Three consecutive interventions (R8 cost, R9-v1 structure, R9-v3 policing) each appeared when an experiment failed to confirm the founder's claim — and continuing to escalate would be manufacturing the answer. So the run stops here, with a **mixed, honest verdict** rather than a forced confirmation.

What is robustly established across R7/R8/R9, and what is not:

| Claim | Verdict |
|---|---|
| Parasites win the within-group invasion | **Confirmed** (R7, R8, R9) |
| A society/deme of parasites is far less productive than one of mutualists (self-consumes) | **Confirmed** (R8 10×; R9 productivity gap) |
| Long horizon alone → morality | **Refuted** (R7 v1, R8 F19) |
| Group structure alone → holobiont | **Refuted** (R9 v2 F21) |
| Sufficiently strong enforcement → cooperation wins | **Confirmed once** (R7 PUNISH), **not reproduced** in the single-generation haystack at modest strength (R9 v3) |
| "Only mutualists can form a holobiont" (as an endpoint/definition) | **True by definition, not demonstrated as a dynamical attractor here** |

**The honest synthesis:** cooperation/mutualism/the holobiont is collectively optimal but is **never the default**; it requires enforcement, and whether enforcement succeeds is **threshold-dependent** — it must exceed the free-rider advantage, and the structure must give it time to act. R7 found a regime where it works; R9 found regimes where group structure and modest policing do not. This is precisely the major-transitions consensus: new individuality requires *active suppression of within-unit competition* (policing, kin bottlenecks, vertical-transmission relatedness), and getting it is hard and conditional — not automatic from group structure or from parasites politely self-consuming.

## 4. The legitimate next step (mapping, not tuning)

There IS a non-trap continuation: **characterize the enforcement/structure threshold** rather than tune to a win. Sweep (policing strength × founder size × number of within-group generations before dispersal) and *map the boundary* between the parasite basin and the holobiont basin — reporting wherever it falls, including "the holobiont window is unrealistically narrow" if that is what the data says. The difference from result-chasing is the pre-commitment to report the boundary location honestly, not to declare victory once any cell turns mutualist. Relatedness/vertical-transmission (Hamilton; the realistic route to holobionts — Margulis's endosymbionts were vertically transmitted) is the most important missing dimension and the one most likely to genuinely matter; it belongs in that sweep.

## 5. Disposition

R9 confirms the founder's "parasites self-consume" (the productivity gap is real) but **refutes** that self-consumption or group structure alone yields the holobiont, and **declines to overfit** policing to force the rest. Combined with R7/R8, the durable, publishable claim is the architecture one: *cooperation under mortality requires enforcement above a free-rider threshold; no single weaker mechanism (long horizon, shared fate, group structure, weak policing) suffices alone.* That is a real result, aligned with mainstream theory, and it was reached by honoring the refutations rather than erasing them. Ledger: R9 v1 (void), v2, v3 → experiment runs total 10 across 4 conjectures; **and one logged refusal-to-overfit, which is itself the corpus's epistemics working as designed.**
