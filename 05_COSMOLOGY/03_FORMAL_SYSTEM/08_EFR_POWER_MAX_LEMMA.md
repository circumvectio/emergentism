---
rosetta:
  primary_level: L5
  primary_column: Philosophy
  operator: "Brahmā ○"
  tier: "Executive"
  regime: "Brāhmaṇa"
  register: "[I/C]"
  canonical_phrase: "POWER-MAX — JUSTICE-CONSTRAINED DESIGN OBJECTIVE"
---

# POWER-MAX — JUSTICE-CONSTRAINED DESIGN OBJECTIVE

**Status:** Canonical Emergentist design lemma; not a theorem of nature

**Evidence tier:** `[I]` as a transparent normative construction; `[C]` as a universal behavioral or ecological model

**Supersedes:** the claim that coupling or `P_node = ΦV` derives cooperation, morality, or a complete is–ought bypass
**Original pre-repair blob:** `14de3498a39157ffd354c853f8142715e587db18`

> **[金] Kintsugi seam — derived morality.** The former proof correctly found a
> positive coupling derivative and also correctly found a counterexample in
> which extraction benefits the extractor. It nevertheless called the result a
> conditional theorem and treated a governance constraint as though arithmetic
> had supplied the norm. The repaired form exposes Justice as a premise, keeps
> the counterexample load-bearing, and states Power-Max as an objective chosen
> inside that premise.

---

## 1. Quantities and horizon

For any bearer `x` and horizon `T`, let

\[
W_x(T)=\int_0^T P_x(t)\,dt .
\]

`P_x(t)` is the power or durable option-capacity measure declared for the
application. In the normalized Emergentist node chart the selected instance is

\[
P_x(t):=C_\times(\Phi_x(t),V_x(t))=\Phi_x(t)V_x(t),
\]

where `C×` is one member of a wider monotone conjunctive family. The product is
canonical **by model choice**, not uniquely derived from the reciprocal chart
and not established as the universal measure of real power.

For an action `a`, write the **prospective modeled** horizon change as

\[
\widehat{\Delta}_TW_x(a;M_t)
:=\mathbb E_{M_t}[W_x(T)\mid a]
-\mathbb E_{M_t}[W_x(T)\mid a_0],
\]

relative to an explicit baseline `a₀`. Retrospective classification instead
uses a **receipted** change

\[
\Delta_T^R W_x(q,r)
:=W_x^{\mathrm{observed}}(r)-W_x^{\mathrm{baseline}}(q,r).
\]

Because the prospective expectation is taken under the fallible present model
`M_t`, later receipts may reverse the ranking. Both statuses must be reported.

---

## 2. The Justice envelope is a premise

Let `i` denote the acting individual or part and `H` the coupled sustaining
whole at the declared scale. Define `J(a;i,H)` to mean that the action passes a
named Justice envelope containing at least:

- an accountable `AuthorizationEnvelope` (principal, mandate, scope, consent,
  custody, expiry or revocation, contest path, actor, and consequence bearer);
- non-extraction and no hidden transfer (`η = 0` at the declared boundary);
- truthful accounting of payer and beneficiary;
- due process, reversibility where possible, and Grace Exit;
- respect for the physical and option-cone boundaries of both `i` and `H`.

Justice is not obtained by maximizing `W`. It determines which actions may be
compared in the first place:

\[
\mathcal A_J=
\left\{a:\ J(a;i,H)
\land\widehat{\Delta}_TW_i(a;M_t)\ge 0
\land\widehat{\Delta}_TW_H(a;M_t)\ge 0\right\}.
\]

If `\mathcal A_J` is empty, the calculus returns **no admissible maximizer**. It does not
launder a harmful action by choosing the least harmful member of an unjust set.

---

## 3. Power-Max

The repaired Power-Max objective is

\[
a^\star\in\operatorname*{arg\,max}_{a\in\mathcal A_J}
\mathbb E_{M_t}[W_i(T)\mid a].
\]

In words:

> Among actions that are already authorized, non-extractive, honestly
> accounted, and non-degrading to both the part and the sustaining whole,
> choose the action expected to maximize the acting part's durable potential.

This is a constrained decision rule. It says neither that agents in fact obey
it nor that unconstrained maximization becomes moral. The horizon, baseline,
bearers, boundary of `H`, power measure, model, uncertainty, payer, and
beneficiary must all be declared.

### Syntropic Dyadism

After outcome receipts arrive, classify the receipted action under the same
Justice envelope:

`J^R(q,r;i,H)` means that the recorded authorization and Justice conditions
were actually honored according to the commitment and outcome receipts, not
merely predicted at selection time.

\[
\operatorname{Moral}(q,r)
\iff \Delta_T^R W_H(q,r)>0
\land\Delta_T^R W_i(q,r)\ge0
\land J^R(q,r;i,H),
\]

\[
\operatorname{Ethical}(q,r)
\iff \Delta_T^R W_i(q,r)>0
\land\Delta_T^R W_H(q,r)\ge0
\land J^R(q,r;i,H),
\]

\[
\operatorname{Syntropic}(q,r)
\iff \Delta_T^R W_i(q,r)>0
\land\Delta_T^R W_H(q,r)>0
\land J^R(q,r;i,H).
\]

Thus bilateral preservation is admissible but is not strict syntropy; strict
Syntropic Dyadism requires both durable potentials to rise. Aggregate gains do
not compensate for destroying either side.

---

## 4. What coupling proves—and what it does not

Consider the illustrative coupling model

\[
V_{\mathrm{eff}}(i)=(1-\lambda)V_i+\lambda\langle V\rangle,
\qquad
P_{\mathrm{eff}}(i)=\Phi_iV_{\mathrm{eff}}(i),
\]

for `N≥2`, `λ∈(0,1]`, and `Φ_i>0`. Then, holding all else fixed,

\[
\frac{\partial P_{\mathrm{eff}}(i)}{\partial V_j}
=\frac{\lambda\Phi_i}{N}>0
\qquad(j\ne i).
\]

This proves monotone interdependence **inside the stated model**. It does not
prove cooperation, justice, or a dominant strategy.

### The extraction counterexample remains decisive

Let `i` take from `j` in a one-shot transfer while holding `Φ_i` fixed, with

\[
0<\Delta V\le\min(V_j,1-V_i),
\]

so both normalized factors remain in `[0,1]`:

\[
V_i\mapsto V_i+\Delta V,
\qquad
V_j\mapsto V_j-\Delta V.
\]

The average `⟨V⟩` is unchanged, so

\[
\Delta P_{\mathrm{eff}}(i)=\Phi_i(1-\lambda)\Delta V>0
\qquad\text{when }\lambda<1.
\]

Unconstrained Power-Max therefore permits extraction. Long horizons or network
effects may sometimes make extraction self-defeating, but no such outcome
follows without additional empirical assumptions. `J` excludes the transfer
normatively and institutionally; the derivative does not exclude it
mathematically.

---

## 5. Sacrifice is a separate class

A competent bearer may voluntarily accept a local loss for another bearer under
informed consent and a valid Authorization envelope. For generic payer `p` and
beneficiary `b`, record it as

\[
\operatorname{VoluntarySacrifice}(q,r;p,b)
\iff \Delta_T^R W_p(q,r)<0
\land\Delta_T^R W_b(q,r)>0
\land\operatorname{AuthorizedCost}^R(q,r;p,b).
\]

It is costly, potentially admirable, and distinct from strict syntropy. A
collective may not demand sacrifice as proof of morality, conceal who pays, or
rename an imposed loss a mutual gain.

---

## 6. Evidence, predictions, and kill criteria

### Evidence claims

- `[A]` The calculus is internally inspectable once all quantities and the
  Justice predicate are supplied.
- `[I]` It is a coherent Emergentist decision grammar for coupled part–whole
  systems.
- `[C]` Real agents, institutions, or ecosystems are accurately ranked by the
  selected product model or converge on this objective.

### Discriminating tests

Applications must compare the selected product against other admissible
conjunctive aggregators, expose ranking reversals, and track predicted versus
receipted outcomes for both `i` and `H`.

### Kill or reclassification criteria

Reclassify or reject an application when any of the following holds:

1. the declared `P_x` is not operationally measurable;
2. another admissible aggregator predicts receipts materially better;
3. payer, beneficiary, consent, custody, or consequence bearer is hidden;
4. the boundary of `H` is chosen after the outcome to manufacture agreement;
5. one side's durable potential is destroyed while aggregate gain is called
   syntropy;
6. modeled improvements systematically fail against outcome receipts;
7. extraction remains profitable because the Justice envelope is not actually
   enforced.

---

## 7. Canonical compression

\[
\boxed{
\text{Justice defines the admissible field; Power-Max chooses within it.}
}
\]

Power-Max does not bridge `is` to `ought` by arithmetic. It makes the normative
premise visible, prevents aggregate laundering, and gives that premise an
auditable decision interface.

---

## See also

- [Canonical Formula Block](../00_CANONICAL_FORMULA_BLOCK.md)
- [Primitives and Type Signatures](29_PRIMITIVES_AND_TYPE_SIGNATURES.md)
- [Objective Morals and Ethics](../../04_AXIOLOGY/02_VALUE_THEORY/00_OBJECTIVE_MORALS_AND_ETHICS.md)
- [Rights, Duties, and Due Process](../../04_AXIOLOGY/02_VALUE_THEORY/01_RIGHTS_DUTIES_AND_DUE_PROCESS.md)
- [Two Sacrifices](13_EFR_TWO_SACRIFICES.md)

*Power-Max | repaired 2026-07-17 | Justice first; optimization second.*
