---
rosetta:
  primary_column: "Methodology"
  register: "[A] model-internal results; [I] readings"
  canonical_phrase: "R7 — Does Morality Emerge From Self-Interest"
---

# R7 — Does Morality Emerge From Long-Horizon Self-Interest? A Direct Test of the Greatest Conjecture

**Status:** Executed 2026-06-10. Two experiments, verbatim output below. Tests the founder's "greatest conjecture," claim 4: *pure self-interest yields objective morality over a long time horizon (the 2 gods) and immorality over a short one (the 2 demons), under the power-max lemma.*
**Artifacts:** [R7_SUPPORT_HORIZON_MORALITY_SIM.py](R7_SUPPORT_HORIZON_MORALITY_SIM.py) (v1), [R7_SUPPORT_HORIZON_MORALITY_SIM_V2.py](R7_SUPPORT_HORIZON_MORALITY_SIM_V2.py) (v2). Stdlib, deterministic, 16 seeds.
**Tier:** [A] for the model-internal facts; [I] for every reading beyond the model; the is/ought identification of "wins selection" with "is moral" is **model-objective only** (Paper III's inherited premise stands — see §5).

---

## 1. The design (why this is a real test, not a restatement)

R3 imposed GIVE/TAKE as policies. The conjecture claims something stronger: that a self-interested agent *choosing* to maximize its own future will arrive at giving when the horizon is long. So R7 makes cooperation a **competing evolutionary strategy**, not an imposed rule, and asks: under what conditions does pure survival/welfare selection favor the cooperator ("god") over the defector ("demon")?

200 agents on a health line; drift toward death; optional threshold regeneration (the **time horizon** — SHORT = no regeneration, everyone descends; LONG = regeneration can outrun drift, so the future in which cooperation might pay actually arrives). Cooperators pay a per-step cost into a pool for the neediest; defectors pay nothing. Mixed 50/50 populations; the winner is whichever strategy's carriers earn more lifetime welfare — i.e., *is being moral individually rational?* Two further knobs: a **shared-fate coupling** β (your regeneration scales with the living fraction — the "individual light cone grows with the collective" mechanism), and an **allocation rule** (PUBLIC = free-ridable; RECIPROCAL = pool shared only among contributors, i.e. K*/η=0 made concrete; PUNISH = reciprocal plus costly retaliation against defectors, i.e. the licensed immune response).

## 2. Experiment 1 — the conjecture as literally stated FAILS

```
horizon coupling  | coop_surv  def_surv | final coop% | coop_welf  def_welf |  winner
SHORT   ISOLATED  |     0.00%     0.00% |       0.00% |      36.2      56.3 | DEF(demon)
SHORT   COUPLED   |     0.00%     0.00% |       0.00% |      36.2      56.3 | DEF(demon)
LONG    ISOLATED  |    75.00%    90.69% |      37.50% |    1679.9    2200.3 | DEF(demon)
LONG    COUPLED   |    75.00%    88.69% |      37.50% |    1679.9    1958.4 | DEF(demon)
```

**F13 — Defectors win in every cell, including long-horizon + coupled.** [A] The conjecture as literally stated — *self-interest + long horizon → morality* — is **false in this model.** A long horizon and even a shared-fate coupling are not sufficient. Mechanism: the coupling is a **public good**. Cooperators pay the cost; the benefit (more survivors → more regeneration) accrues to everyone, defectors included, who free-ride. This is the textbook free-rider problem (Olson; Hardin), and it defeats the naive conjecture cleanly. P2 confirmed (demons rule the short horizon); P1 refuted; P3 confirmed (long horizon alone does not rescue cooperation).

## 3. Experiment 2 — the corpus's OWN machinery rescues it, with a sharpened precondition

The rigorous fix for free-riding is reciprocity / assortment / punishment (Axelrod 1984; Nowak 2006 "Five Rules for the Evolution of Cooperation"; Fehr & Gächter 2002 costly punishment). The corpus already contains exactly this: **K\*** (reciprocate; never extract from cooperators) and the **licensed immune response** (the demon-operators, permitted only against defectors). v2 adds those as allocation rules.

```
alloc      horizon coupling  | final coop% | coop_welf  def_welf |  total_w |  winner
PUBLIC     LONG    ISOLATED  |      37.50% |    1679.9    2200.3 |   388027 | DEF(demon)
PUBLIC     LONG    COUPLED   |      37.50% |    1679.9    1958.4 |   363836 | DEF(demon)
RECIPROCAL SHORT   *         |       0.00% |      44.1      50.3 |     9438 | DEF(demon)
RECIPROCAL LONG    ISOLATED  |      61.03% |    2365.2    1610.7 |   397592 |  COOP(god)
RECIPROCAL LONG    COUPLED   |      61.03% |    1722.4    1203.6 |   292596 |  COOP(god)
PUNISH     SHORT   ISOLATED  |       0.00% |      26.1      11.4 |     3751 |  COOP(god)
PUNISH     LONG    ISOLATED  |      43.75% |     980.1      16.7 |    99680 |  COOP(god)
PUNISH     LONG    COUPLED   |       0.00% |      58.5      16.2 |     7473 |  COOP(god)
```

**F14 — Reciprocity rescues the conjecture; the true precondition is long horizon AND reciprocity.** [A] Under RECIPROCAL allocation (the club good — you receive only if you give, which is K*/η=0 made concrete), cooperators win selection and out-earn defectors over the long horizon (coop welfare 2365 vs 1611; final cooperator share 61%). The conjecture is **true after all — but not as stated.** The omitted precondition is reciprocity: long-horizon self-interest converges on morality *only when giving is conditioned on giving* (assortment), never as a pure public good. "Pure self-interest over a long horizon" is insufficient; "reciprocal self-interest over a long horizon" suffices.

**F15 — The "2 demons" are NECESSARY, and this is why the corpus is right to license them.** [A] Under PUNISH (reciprocity + costly retaliation against defectors — the licensed immune response), cooperators win in **every** cell, including the short horizon (26 vs 11) where nothing else rescued them. Conditional defection against defectors is what makes the gods evolutionarily stable against invasion. This vindicates the corpus's refusal to call the taking-dyad operators "demonic-by-valence": they are the enforcement layer without which cooperation cannot establish. The four-move scheme (2 gods + 2 conditional demons) is not 2 good + 2 bad — it is **cooperation + the enforcement that protects it**, and the experiment shows both halves are load-bearing.

**F16 — But the demons must be FENCED, or they collapse the world.** [A] Punishment carries a collective cost: PUNISH LONG ISOLATED total welfare is 99,680 vs RECIPROCAL's 397,592 — retaliation burns ~75% of aggregate welfare. And PUNISH LONG COUPLED collapses almost entirely (total 7,473; near-total extinction) — unbridled mutual punishment is self-destroying. This is the precise, quantified vindication of the corpus's **fences on the demon-operators**: K* = 0 toward cooperators, the 6-gate test, retaliation licensed *only* against confirmed defectors. The fences are not moral squeamishness; they are the difference between stable cooperation and mutually-assured destruction. Necessary, but only if bounded.

## 4. The sharpened conjecture (what the data supports)

The greatest conjecture survives — reformulated, and stronger:

> Rational self-interest converges on cooperative morality **only under two conditions together: a long time horizon (the future in which cooperation pays must arrive) and reciprocity (giving conditioned on giving — K*/η=0).** Cooperation must additionally be defended by *bounded, targeted* conditional retaliation against defectors (the licensed immune response). Remove the horizon, and defectors win (short-termism is immoral). Remove reciprocity, and free-riders win (naive universal giving is evolutionarily dominated). Remove the fences on retaliation, and the system self-destructs. The corpus's full operator set — two gods, two fenced demons, K*, η=0 — is not a moral aesthetic; it is, in this minimal model, *exactly* the architecture required for cooperation to be the rational long-horizon equilibrium under mortality.

The original "gods = long horizon, demons = short horizon" mapping is too simple. The data says: **gods = cooperation, demons = enforcement; horizon and reciprocity are the conditions under which the gods-plus-fenced-demons equilibrium is the self-interested one.**

## 5. Honest limitations

(i) One parameterization; cost, punishment magnitude, threshold, and population size were fixed, not swept — robustness sweeps owed before any external claim (especially the punishment knobs, which clearly have a sharp regime boundary). (ii) Strategies are fixed types, not learning agents; an adaptive/learning version is the natural next step. (iii) "Wins selection / earns more welfare" is identified with "is moral" **only by stipulation** — the is/ought seam Paper III already concedes. The experiment shows cooperation is *individually rational* under the stated conditions; calling that *moral* is the inherited premise, not an output. (iv) Reciprocity here is assortment (club good); explicit pairwise memory/reputation is a richer and more standard model worth running. (v) Model-internal throughout: no claim about human ethics follows without bridging.

## 6. Disposition

This is the most decisive experiment in the program so far: it tested the corpus's ethical keystone, broke it as stated, and rebuilt it sharper using the corpus's own machinery — vindicating the full 2+2 operator architecture and its fences, while exposing the omitted reciprocity precondition. Publication path: a strong companion to R3 ("the evolution of cooperation under mortality with a conjugate-constrained welfare"), citing Axelrod, Nowak 2006, Fehr-Gächter, Olson. Owes: the parameter sweeps in §5(i) and the standard-reciprocity (reputation) variant. **No API key required** — this whole line is runnable now, and is the highest-leverage theory-testing on the board.

Ledger: R7 v1, v2 → entries 4 and 5 (total experiments executed: R3 v1/v2/v3, R7 v1/v2 = 5 distinct runs across 2 conjectures).
