---
rosetta:
  primary_column: "Methodology"
  register: "[A] model-internal results; [I] readings"
  canonical_phrase: "R8 — Moral Circle, Symbiosis, Time Horizon"
---

# R8 — The Moral Circle as Entropy-Externalization Boundary: Confirmed Collectively, Free-Ridden Individually

**Status:** Executed 2026-06-10 (including an honestly-reported mis-parameterized first run). Tests the founder's claim that *morality = the radius of the boundary across which you externalize entropy*, with the symbiont/replicator-stack extension that *parasitism vs mutualism is a time-horizon strategy*.
**Artifact:** [R8_SUPPORT_MORAL_CIRCLE_SIM.py](R8_SUPPORT_MORAL_CIRCLE_SIM.py). Stdlib, deterministic, 12 seeds. Parasitism p = inverse moral-circle radius (p=0 mutualist / large circle; p=1 parasite / self-only circle); static agents on a ring with a local shared substrate that pollution degrades and that feeds regeneration.
**Tier:** [A] for model-internal facts; [I] for readings; is/ought identification of "earns more" with "is moral" is model-objective only.

## 0. Honest debugging note (recorded, not hidden)

The first run refuted every prediction — but spuriously: it used internalization cost `KAPPA·E = 0.020` *above* the maximum regeneration `0.012`, making "clean up after yourself" net-negative on health *by construction*, independent of any commons dynamics (mutualists won nothing even in the decoupled control — the tell). That is a void test, not a finding. Corrected to `KAPPA = 0.30` (cost 0.006 < regen 0.012: internalization survivable but real) and rerun. Both the bug and the fix are logged here per A7. The numbers below are the corrected run.

## 1. Results (verbatim, corrected run)

```
A. MONOMORPHIC (everyone same circle): mean lifetime welfare
horizon | p=0.00  p=0.25  p=0.50  p=0.75  p=1.00    optimal p
SHORT   |     21      25      30      39      53      p=1.0 (parasite)
MED     |     36      42      48      55      69      p=1.0 (parasite)
LONG    |   1004     537     291     127      96      p=0.0 (MUTUALIST)

B. CONTROL (substrate decoupled — pollution harmless)
LONG    |   1004    1419    1835    2251    2667      p=1.0  (parasite wins; mechanism isolated)

C. INVASION (10% mutant vs 90% resident)
horizon  resident   mutant    | mut_welf  res_welf | invader wins?
SHORT    MUTUALIST  PARASITE  |     52       21     | YES
SHORT    PARASITE   MUTUALIST |     21       53     | no
MED      MUTUALIST  PARASITE  |    568       34     | YES
MED      PARASITE   MUTUALIST |     27       72     | no
LONG     MUTUALIST  PARASITE  |   1804      652     | YES   <-- parasite invades even at LONG
LONG     PARASITE   MUTUALIST |     37      144     | no
```

## 2. Findings

**F17 — The moral circle is collectively vindicated over long horizons.** [A] In monomorphic worlds (everyone adopts the same circle), the optimal parasitism falls monotonically as the horizon lengthens — p=1 at SHORT/MED, **p=0 at LONG** — and the gap is enormous: a society of mutualists earns **1004 vs 96** for a society of parasites (≈10×). The founder's core claim is true *as a statement about collective outcomes*: over a long horizon, a society that internalizes its entropy (large moral circle) vastly out-produces one that externalizes it. P1, P2, P3 confirmed at the collective level.

**F18 — The mechanism is the substrate return, exactly as the corpus predicts.** [A] The decoupled control (pollution harmless) inverts the result: parasites win at every horizon, 2667 at LONG. So mutualism's advantage exists *only* because externalized entropy returns to degrade the externalizer's own future regeneration. This is the corpus's "you eat your own externalities over a long enough horizon" made quantitative — and it isolates substrate-return as the necessary precondition (the analogue of R7's reciprocity precondition).

**F19 — But the moral circle is NOT self-enforcing: the parasite invades at every horizon.** [A] In mixed populations a parasite mutant out-earns the mutualist residents it invades — at SHORT (52 vs 21), MED (568 vs 34), and **even at LONG (1804 vs 652)**. The parasite free-rides on the clean commons the mutualists maintain while skipping the internalization cost. P4 is **refuted**: a long horizon does *not* make mutualism evolutionarily stable. This is the tragedy of the commons (Hardin 1968) in moral-circle dress: the large circle is collectively optimal and individually invadable.

**F20 — Time horizon raises the stakes without solving the problem.** [A] Longer horizon does not select mutualism (F19), but it widens the collective cost of failing to: the mutualist-vs-parasite monomorphic gap grows from ≈2.5× (SHORT, 53 vs 21) to ≈10× (LONG, 1004 vs 96). The replicator-stack reading survives in amended form: ascending geno → … → egregore (increasing horizon) does **not** automatically enforce mutualism — it raises the *prize* for any host that can. Long-horizon replicators are under more pressure to *evolve enforcement*, not more naturally moral.

## 3. The convergence with R7 (the real headline)

R7 and R8 attack the conjecture by two independent mechanisms — R7: a reciprocity club-good; R8: a degradable commons with a time horizon — and reach the **same** structural conclusion:

> Cooperation / the large moral circle / mutualism is **collectively optimal over long horizons but free-ridden into collapse without an enforcement layer.** In R7 the enforcement is K*/licensed punishment (the fenced demons); R8 shows the *same gap* and therefore the *same need*. The symbiont framing names it precisely: a parasite is a free-rider on a host it does not maintain; the host's answer, everywhere in biology, is an **immune system** — which is exactly the corpus's licensed, fenced "demon" operators.

So the corpus's architecture is doubly vindicated, and the conjecture is doubly amended the same way: *"expand all D5 light cones" is the right collective objective, is not self-enforcing, and requires the immune/enforcement layer to survive contact with parasites.* The founder's two papers (teleology + symbiosis) and the four operators (2 gods + 2 fenced demons) are one claim; R7 and R8 are its two independent confirmations-with-amendment.

## 4. Honest limitations

(i) The KAPPA bug shows the result is parameter-sensitive; a full sweep of (KAPPA, DEPLETE, RHO, W) is owed to map where the SHORT→LONG crossover sits and confirm it is generic, not tuned. (ii) Static agents fully eat their local externality; mobile agents (who can flee their pollution) would weaken F17 — a key variant to run, and the realistic one for many replicators. (iii) No enforcement is modeled here; the decisive next run is R8+enforcement (immune response against high-p neighbors) to confirm it restores mutualism as an ESS, closing the loop with R7. (iv) "Earns more" ≡ "is moral" is stipulated (Paper III's premise). (v) Model-internal; no claim about ecology or human ethics follows without bridging — and note the D5-gate caution: this models *agents'* strategies, not an ecosystem's "mission."

## 5. Disposition

Confirms the moral-circle claim at the collective level, refutes its self-enforcement, and converges with R7 on the necessity of the fenced-demon/immune layer. Strong material for the R7 companion paper (now plausibly one paper: "Cooperation under mortality: two mechanisms, one architecture"). Owes the parameter sweep (§4 i), the mobility variant (§4 ii), and the enforcement closure (§4 iii) — all runnable with no API key. Ledger entries: R8 v1 (void, logged) + v2 → experiment runs now total 7 across 3 conjectures (R3 ×3, R7 ×2, R8 ×2).
