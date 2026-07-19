---
rosetta:
  primary_level: L5
  primary_column: Philosophy
  operator: "Brahmā ○"
  tier: "Executive boundary"
  regime: "Brāhmaṇa"
  register: "[A/S/I/C] typed claim-by-claim"
  canonical_phrase: "THE POWER-MAX LEMMA — power counted across bearer and horizon"
title: "The Power-Max Lemma"
type: formal-model-owner
version: "2.0"
date: 2026-07-19
status: "ACTIVE [金] — conditional cooperation theorem and objective-within-frame value classifier"
evidence_tier: "[A] for algebra in the declared games; [S] for the typed contract; [I/vow] for adopting the boundary and values; [C] for external fit"
owner: 01_EMERGENTISM
parents:
  - ../00_CANONICAL_FORMULA_BLOCK.md
  - ../00_THE_BURRI_RULES.md
  - ../../04_AXIOLOGY/02_VALUE_THEORY/00_OBJECTIVE_MORALS_AND_ETHICS.md
  - ../../00_THE_EMERGENTIST_WELTANSCHAUUNG.md
  - ../../11_UPLINK/50_AUDITS_AND_EXECUTIONS/126_WELTANSCHAUUNG_FORMAL_AUDIT_2026_07_13.md
---

# The Power-Max Lemma

## Power that learns to count the whole and the long run

> **[金] Crack repaired.** The earlier version correctly proved coupling but
> then made enforced `η=0` an assumption of the very cooperation result it was
> asked to derive. It also depended on a uniquely forced product and sometimes
> aggregated bearers. This owner separates three claims: a theorem inside a
> declared game, an objective classifier inside a declared value frame, and the
> normative choice to adopt that frame. The parent Git history preserves the
> prior proof.

The central insight survives in a stronger honest form:

> **Within the chosen Justice frame, durable power is evaluated across the real
> sustaining boundary, over the horizon on which consequences return, under an
> account that does not hide a payer.**

Short-horizon ego extraction can be rational. Long-horizon cooperation can
also be rational and power-maximizing. Which result holds depends on coupling,
horizon, reciprocity, enforcement, exit, measurement, and whose potential is
being maximized. Those are not footnotes; they are the theorem’s hypotheses.

---

## 1. Typed quantities

Let `i` be a finite bearer and `H` a real sustaining whole. Let
`0 ≤ τ < T` with `T > 0` denote a short and a durable horizon. For any declared
normalized potential model:

```text
W_x(T) = integral_0^T P_x(t) dt.
```

When Emergentism’s selected node model is used:

```text
Φ_x,V_x ∈ [0,1]
P_x := Φ_x V_x.
```

This product is a conjectural interior model `[C]`, not uniquely derived. The
formal results below may instead use a declared monotone zero-absorbing
conjunctive aggregator `C`.

Define a Justice envelope `J_T(a;i,H)` that exposes all material bearers,
authorization, consent, custody, payer, beneficiary, contest, reversibility,
exit, uncertainty, horizon, and receipted consequence. Define:

```text
A_J = {a : J_T(a;i,H)
           and Δ_T W_i(a) >= 0
           and Δ_T W_H(a) >= 0}.
```

No sum over bearers can substitute for this conjunctive gate.

---

## 2. Demon and god as horizon strategies `[I/S]`

Within the Rosetta game, the names mean strategies, not kinds of people:

```text
Demon strategy:
  maximize a local bearer’s near-term score by externalizing cost
  to another bearer or the sustaining whole.

God strategy:
  accept a bounded near-term local cost when doing so raises durable
  joint potential and returns through a coupled, just relation.
```

A compact temporal classifier is:

```text
Demonic(a;i,H,τ,T)
  iff Δ_τ W_i(a) > 0
      and (Δ_T W_H(a) < 0 or not J_T(a;i,H)).

Godic(a;i,H,τ,T)
  iff Δ_T W_H(a) > 0
      and Δ_T W_i(a) >= 0
      and J_T(a;i,H),
```

with the characteristic sacrifice/investment subtype adding
`Δ_τ W_i(a)<0`. The short-term cost is typical, not logically necessary. A
gift that coerces or captures is not godic merely because it looks generous.

---

## 3. The repeated-game cooperation theorem `[A]` inside the model

Consider an indefinitely repeated two-player cooperation game with stage
payoffs

```text
T_d > R > P_d > S,
```

where `R` is the reward for mutual cooperation, `T_d` the one-period temptation
payoff from exploiting a cooperator, `P_d` the mutual-defection payoff, and `S`
the exploited cooperator’s payoff. Let future payoffs be discounted by
`δ∈[0,1)`.

Under a reciprocal strategy that cooperates until a defection and then returns
`P_d`, continued cooperation yields

```text
V_C = R/(1-δ).
```

A one-period demon deviation yields

```text
V_D = T_d + δ P_d/(1-δ).
```

Therefore continued cooperation is individually incentive-compatible exactly
when

```text
V_C >= V_D

δ >= (T_d-R)/(T_d-P_d).
```

This is the clean Power-Max result: **when consequences return strongly enough
through the horizon and reciprocal structure, long-run individual
power-maximization can select cooperation over short-run extraction.** No moral
premise is needed for this conditional inequality.

It does not say every repeated game cooperates, every agent discounts slowly,
or every reciprocal sanction is just. It proves why “demon now” and “god over
time” can be different maximizers of the same agent’s payoff.

---

## 4. The Justice-constrained frontier lemma `[A/S]`

If `P_x(t)∈[0,1]`, define normalized durable potential and its modelled
expectation by

```text
Wbar_x(T|a) = W_x(T|a)/T ∈ [0,1]
w_x(a) = E_M[Wbar_x(T|a)].
```

Let `C:[0,1]^2→[0,1]` be strictly increasing in each argument on the
positive interior and zero-absorbing at the boundary, and define

```text
Q_T(a) = C(w_i(a), w_H(a)).
```

On the viable interior, if this set is nonempty and the maximum is attained,

```text
A_J+ = {a∈A_J : w_i(a)>0 and w_H(a)>0},

a* ∈ argmax_{a∈A_J+} Q_T(a).
```

Every maximizer is Justice-admissible by construction. It is also Pareto
efficient in the pair of **expected normalized durable potentials**: if some
`b∈A_J+` weakly raised both `w_i,w_H` and strictly raised at least one, strict
monotonicity would give `Q_T(b)>Q_T(a*)`, contradicting maximality.

This statement deliberately applies on the positive interior. A
zero-absorbing aggregator is indifferent to improvements in one factor while
the other remains zero, so no boundary Pareto claim follows without an
additional ordering rule. If `A_J+` is empty or the supremum is not attained,
the displayed argmax lemma is inapplicable rather than magically creating a
viable choice. An `ε`-optimal or compactness/upper-semicontinuity formulation
may be supplied for a particular application.

This result is elementary but load-bearing. It proves the internal consequence
of the frame; it does not prove that every agent must adopt `Q_T`, `A_J`, the
boundary `H`, or the horizon `T`.

---

## 5. When “all demons drive it to zero” is true `[A/S]` conditionally

The slogan is not a universal theorem of AND-class aggregation. It becomes an
exact collapse result in a declared depletable-commons model.

Let shared substrate `S_t≥0` evolve by

```text
S_{t+1} = max(0, S_t + g(S_t) - E_t),
```

where `g` is regeneration and `E_t` total extraction. If there is an
`ε>0` such that, while `S_t>0`, coordinated demon extraction satisfies

```text
E_t - g(S_t) >= ε,
```

then `S_t` reaches zero in at most `ceil(S_0/ε)` steps. If each node’s viable
potential is bounded by the substrate,

```text
P_i(t) <= k_i S_t,
```

then every `P_i` also reaches zero. **QED, for this closed, overdrawn,
substrate-coupled game.**

If regeneration outruns extraction, agents can exit before costs return, or
the system is not actually coupled, the corollary does not apply. “Everyone is
a demon, therefore everything is zero” must always carry these conditions.

---

## 6. Morals and ethics: objective within a declared frame `[S/I]`

The directions are:

```text
Moral(a;i,H,T)
  iff Δ_T W_H(a) > 0
      and Δ_T W_i(a) >= 0
      and J_T(a;i,H).

Ethical(a;i,H,T)
  iff Δ_T W_i(a) > 0
      and Δ_T W_H(a) >= 0
      and J_T(a;i,H).

Syntropic(a;i,H,T)
  iff Δ_T W_i(a) > 0
      and Δ_T W_H(a) > 0
      and J_T(a;i,H).
```

Their characteristic temporal failures are:

```text
Immoral extraction:
  short-term ego gain purchased by durable loss to H or an invisible bearer.

Unethical extraction:
  short-term whole/aggregate gain purchased by durable loss to i
  or another bearer hidden by the aggregate.
```

Thus the user’s temporal insight is retained without making every short-term
cost evil. An individual may pay now to raise the whole and later share the
return. A whole may invest over institutional horizons in a bearer. A bounded,
due-process protective cost is not classified by its sign alone. The durable
receipt and Justice envelope decide the cell.

Once boundary, horizon, potential model, Justice fields, and receipts are
fixed, the sign classification is objective in the ordinary model-relative
sense: observers can be wrong about which inequalities occurred. The adoption
of that boundary, horizon, model, and Justice conception remains an
interpretive/normative commitment. The frame is viability-motivated and can be
tested for self-undermining consequences; it is not uniquely forced by the
chart.

---

## 7. Is `η=0` a lemma or a vow?

It has two standings, which must not be collapsed:

1. **Conditional strategic result `[A/S]`:** in a sufficiently coupled,
   patient, reciprocal game whose modeled costs return to the actor,
   cooperation can maximize the actor’s durable payoff relative to one-shot
   deviation. The discount-threshold theorem in §3 makes this exact for the
   stated players; it does not establish bearer-complete `η=0` outside them.
2. **Normative/constitutional choice `[I/vow]`:** outside those conditions—one
   shot, extract-and-exit, weak coupling, hidden costs, unequal power—the
   strategy need not dominate. Emergentism still refuses extraction and builds
   a Justice envelope intended to make the cooperative game real.

So `η=0` is **not merely a sermon**, and it is **not an unconditional law of
nature**. The lemma explains why the vow is strategically intelligent; the vow
selects and maintains the conditions under which the lemma applies.

---

## 8. What the lemma does and does not establish

It establishes, inside declared models:

- short- and long-horizon maximization can select different strategies;
- reciprocity and sufficient future weight can make cooperation individually
  rational;
- persistent over-extraction of a genuinely coupled finite substrate can
  annihilate every dependent node’s potential;
- Justice-constrained maximization cannot license a gain purchased by a
  hidden destroyed bearer;
- moral and ethical direction can be objectively classified after the frame
  and consequences are specified.

It does not establish:

- that `P_node=ΦV` is the uniquely correct real-world power measure;
- that every system is positively coupled or indefinitely repeated;
- that every long-horizon equilibrium is cooperative or just;
- that the widest relevant boundary and horizon are self-identifying;
- that enforcement is costless, incorruptible, or morally legitimate;
- that geometry closes the is/ought gap;
- universal moral realism.

---

## 9. Predictions and kills `[C]`

The world-facing programme must predeclare at least:

- the bearer and sustaining boundary;
- the operational measures of `Φ`, `V`, or alternative potential;
- the short and long horizons;
- coupling and discount estimates;
- reciprocity/enforcement mechanism and its own costs;
- extraction, payer, beneficiary, and outcome receipts;
- rival strategies and out-of-sample predictions.

Demote or kill the world-facing claim if:

1. measured durable outcomes do not improve under cooperation above the
   predicted threshold;
2. extraction remains durably superior after all costs return and exit is
   controlled;
3. the selected potential model ranks outcomes worse than fair alternatives;
4. enforcement costs or capture erase the cooperative surplus;
5. hidden bearers appear whose losses were omitted;
6. the result depends on defining every counterexample outside the game.

---

## 10. Compression

```text
Demon = local power, short horizon, exported bill.
God   = durable joint power, returned consequences, visible bill.

Power-Max Lemma:
  cooperation can maximize self-interest when coupling, patience,
  reciprocity, and consequence make the whole part of the self’s payoff.

Justice:
  no maximizer may hide the bearer who pays.

Syntropic Dyadism:
  the node lifts the whole; the whole lifts the node; both remain visible.
```

The public sentence is:

> **Power is counted more honestly across the real whole, over the horizon on
> which consequences return, with the payer still in the equation.**

This is an evaluation rule inside a declared Justice frame. It does not define
the Good, which the kernel treats separately as the chosen AND-class relation
among the True, the Beautiful, and the Just.

---

## Agent execution surface

1. Do not quote the lemma without its game, horizon, boundary, and Justice
   assumptions.
2. Do not use a scalar aggregate to hide a bearer.
3. Keep the repeated-game theorem separate from the normative adoption of the
   frame.
4. **Canonical path:**
   `01_EMERGENTISM/05_COSMOLOGY/03_FORMAL_SYSTEM/08_EFR_POWER_MAX_LEMMA.md`

`⊙ = • × ○` — the dot lifts the ring, the ring lifts the dot, and the score
counts only while both remain.
