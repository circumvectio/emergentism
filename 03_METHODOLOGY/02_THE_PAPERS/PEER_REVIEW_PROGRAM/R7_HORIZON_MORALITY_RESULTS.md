---
rosetta:
  primary_column: "Methodology"
  register: "[A] model-internal results; [I] readings"
  canonical_phrase: "R7 — historical strategy-selection experiment"
---

# R7 — Historical Test of a Horizon/Self-Interest Conjecture

**Status:** Executed 2026-06-10; normative interpretation withdrawn
2026-07-20. The two experiments tested a historical claim that pure
self-interest would select strategies labeled moral at long horizons. They did
not implement bearer-complete Justice and cannot test objective morality.
**Artifacts:** [R7_SUPPORT_HORIZON_MORALITY_SIM.py](R7_SUPPORT_HORIZON_MORALITY_SIM.py) (v1), [R7_SUPPORT_HORIZON_MORALITY_SIM_V2.py](R7_SUPPORT_HORIZON_MORALITY_SIM_V2.py) (v2). Stdlib, deterministic, 16 seeds.
**Tier:** [A] for the model-internal facts; [I] for every reading beyond the model; the is/ought identification of "wins selection" with "is moral" is **model-objective only** (Paper III's inherited premise stands — see §5).

> **[金] Current boundary (2026-07-20).** The inherited premise no longer
> stands. "Cooperator/god," "defector/demon," and "morality" below are historical
> strategy labels in a synthetic model. Winning selection, reciprocity, or
> `etaObserved=0` supplies no moral verdict. Only bearer-complete Justice can
> evaluate an actual act, and these simulations contain no complete bearer,
> authorization, consent, custody, contest, or consequence ledger. Model outputs
> remain `[A]` only as facts about the code run.

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

## 3. Experiment 2 — allocation and punishment alter the result

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

**F14 — Reciprocity changes the selected strategy in these cells.** `[A]`
Under RECIPROCAL allocation, the fixed cooperator strategy out-earns the fixed
defector strategy in the reported long-horizon cells (2365 vs 1611 in the
isolated cell; final cooperator share 61%). This shows that allocation and
assortment matter in this implementation. It does **not** rescue the moral
conjecture, establish a necessary or sufficient condition across games, or make
"wins selection" equivalent to "is moral."

**F15 — Punishment changes the winner but is not licensed by winning.** `[A]`
Under PUNISH, the strategy labeled COOP has the greater carrier welfare in the
reported cells. This is a result of the chosen payoffs, fixed strategies, and
parameters. It does not prove that punishment is necessary, validate a
four-move census, confer moral valence on "demon" or "god" labels, or authorize
retaliation in an actual situation.

**F16 — Punishment is costly and can collapse the modeled population.** `[A]`
PUNISH LONG ISOLATED reports total welfare 99,680 versus RECIPROCAL's 397,592,
and PUNISH LONG COUPLED reports 7,473 with near-total extinction. This is a
warning about the implementation's punishment regime, not quantified
vindication of a corpus fence. Actual defensive action requires independent
evidence, proportionality, accountable authorization, complete bearer custody,
contest, exit, and outcome receipts. Aggregate welfare alone cannot decide it.

## 4. The bounded conclusion (what the data supports)

The moral conjecture does not survive as an empirical conclusion. The model
supports only this bounded strategic statement:

> In this fixed-strategy implementation and reported parameterization, a longer
> horizon alone did not make the cooperator strategy win; reciprocal allocation
> did in the reported long-horizon cells; and the tested punishment rule changed
> winners while imposing large costs and sometimes collapse.

The god/demon labels are historical display names. The data does not identify
morality, assign operator essence, or establish that horizon and reciprocity
are universal necessary or sufficient conditions.

## 5. Honest limitations

(i) One parameterization; cost, punishment magnitude, threshold, and population size were fixed, not swept — robustness sweeps owed before any external claim (especially the punishment knobs, which clearly have a sharp regime boundary). (ii) Strategies are fixed types, not learning agents; an adaptive/learning version is the natural next step. (iii) "Wins selection / earns more welfare" is identified with "is moral" **only by stipulation** — the is/ought seam Paper III already concedes. The experiment shows cooperation is *individually rational* under the stated conditions; calling that *moral* is the inherited premise, not an output. (iv) Reciprocity here is assortment (club good); explicit pairwise memory/reputation is a richer and more standard model worth running. (v) Model-internal throughout: no claim about human ethics follows without bridging.

## 6. Disposition

This experiment falsified the literal claim that long-horizon self-interest by
itself yields the strategy labeled moral in this model. It also showed that
allocation and punishment assumptions can reverse results. It did not rebuild
the ethical claim, vindicate G7, or test bearer-complete Justice. Any publication
claim owes parameter sweeps, alternative strategies and payoff structures,
standard reputation variants, preregistration, and independent replication.

Ledger: R7 v1, v2 → entries 4 and 5 (total experiments executed: R3 v1/v2/v3, R7 v1/v2 = 5 distinct runs across 2 conjectures).
