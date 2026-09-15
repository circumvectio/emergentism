---
title: "Power, capability and the systems that sustain them"
date: 2026-09-15
status: "SUBORDINATE RESEARCH REFINEMENT — conditional models; no empirical trial"
evidence_tier: "[B] attributed sources; [A/S] explicit toy mathematics; [I] synthesis; [C] world fit; [D] tests proposed"
owner: "01_TELEOLOGY; subordinate to The Goal and the formal Power-Max owner"
---

# Power, capability and the systems that sustain them

**Use available resources to do worthwhile work, while renewing the capacity
to keep doing it—and to change course.** `[I]`

This is the useful refinement of our lens. It connects three questions without
making them one quantity: what can physically be done, what a system actually
delivers, and which worthwhile futures remain supportable. It develops
[Emergentist Exergy](README.md), not a new thermodynamic law or a replacement
for the [Power-Max owner](../../05_COSMOLOGY/03_FORMAL_SYSTEM/08_EFR_POWER_MAX_LEMMA.md).

## 1. What the historical contact earns `[B-source/I]`

Lotka's 1922 argument is conditional on available resources and constraints.
Importantly, he distinguishes **generating variations** from **selecting**
among them: a selection advantage does not ensure the advantageous form will
arise. He also treats economy under limited supply differently from expanding
capture when untapped supply remains. These qualifications belong to his
argument, not to a later rescue of it.
[Lotka, pp. 148–150](https://www.soltechdesigns.com/sustainable/lotka1922.pdf).

Odum and Pinkerton propose maximum-power operation under specified couplings;
their 1955 paper explicitly allows situations where power output is not at a
premium. It also discusses self-replacement and the costs omitted when repair
is excluded. The efficient-body/effective-machine contrast therefore cannot
claim either tradeoffs or maintenance as newly discovered principles.
[Odum and Pinkerton, pp. 332–337](https://canadiancor.com/wp-content/uploads/2025/02/Odum-Pinkerton-MPP2.pdf).

Our synthesis `[I]` is to connect that conditional energetic inquiry to
explicit purposes, support networks, revision, and affected bearers. Historical
overlap is a source relationship, not proof of independent priority or of the
whole worldview. The maximum-power principle remains a selection hypothesis,
not an established fourth thermodynamic law, nor evidence for F5.

Thermodynamics alone does not uniquely specify a trajectory. That does not
entail that an extra force is required: ordinary kinetics, boundary conditions,
control, variation and selection remain explanatory rivals.

## 2. Three quantities, not three names for one thing `[S/I]`

| Question | Record | Do not substitute |
|---|---|---|
| What useful work is physically available? | Physical exergy `B_ex` in joules, relative to a reference environment; exergy transfers and destruction over time | A mission, a price, a count of options |
| What is delivered now? | Mechanical useful power in watts where defined; separately, task output with quality and time, such as safe litres/hour | Electrical consumption as proof of useful work; requests as proof of success |
| What can still be achieved? | Supported task/trajectory profile, with dependencies, uncertainty, horizon, switching and recovery costs | More joules or more copies as automatic proof of more capability |

Physical power is instantaneously `dW/dt`; `W/Δt` is average power over an
interval. For a declared converter, write

`P_useful(u) = η_ex(u) × Bdot_in(u)`.

Here `u` is an operating control, `Bdot_in` is attributable exergy input in
watts, and `η_ex` is the defined dimensionless useful-output fraction. Stored
inputs, auxiliary inputs and changing boundaries must be included; a service
rate in tasks/second is not this fraction. Physical exergy is not conserved:
irreversibility destroys availability even while total energy is conserved.
[MIT thermodynamics, §5.3.1](https://ocw.mit.edu/courses/res-2-008-thermodynamics-and-climate-change-summer-2020/mitres-2-008su22_book_new.pdf).

Three meanings of *useful* must also stay distinct: available for physical
work; contributing to a specified system's persistence; and valuable to
affected bearers. None entails the next. A persistent coercive system can have
excellent energetic performance and fail our chosen ethic.

## 3. Maximum power is not guaranteed to be in the middle `[A/S]`

The incoming essay inferred an interior maximum from falling efficiency. That
inference needs repair. In a selected converter toy, let `v` be throughput in
kg/s, `G>0` the fixed input exergy per kg, and `η(v)>0` a smooth efficiency:

`P(v) = G v η(v)`.

An interior stationary point requires

`P′(v) = G[η(v) + vη′(v)] = 0`,

or, for `v>0`, `−vη′(v)/η(v) = 1`. A maximum additionally needs the
appropriate change of sign or equivalent conditions. Merely `η′<0` is not
enough. For `v₀>0`, choose

`η(v) = 1/(1+v/v₀)`.

Then `P′(v)=G/(1+v/v₀)²>0`: efficiency falls, but power increases toward
`Gv₀` without attaining it at any finite throughput. A bounded operating
interval gives an endpoint maximum instead. By contrast,
`η(v)=exp(−v/v₀)` has its unique maximum power at `v=v₀`.

These are calculations inside stipulated models, not measurements of engines
or organisms. There is no general requirement that efficiency and useful power
must trade off when designs, rather than just one loading, change.

### Atwood's machine: the protocol changes the answer

The 1955 paper states a 50% optimum for its Atwood illustration. That number
should not be detached from a loading and timing model. Consider this explicit
**one-stroke** idealization instead: fixed falling mass `M`, rising mass
`m=rM`, `0<r<1`, fixed distance `h`, constant gravity `g`, rest start,
massless inextensible string and frictionless massless pulley.

```text
a = g(1−r)/(1+r)
t = sqrt(2h/a)
W_load = mgh
P_average = W_load/t = Mg sqrt(gh/2) r sqrt((1−r)/(1+r))
d(log P_average)/dr = (1−r−r²)/(r(1−r²))
```

The unique optimum is `r=(sqrt(5)−1)/2 ≈ 0.618`, with power tending to
zero at both endpoints. Here `r` counts lifted-load energy divided by falling
mass's released potential energy. The remainder `(M−m)gh` is combined kinetic
energy at stroke end—not yet waste heat. Braking, recovery, resetting and
ongoing cycle costs are excluded. A different stipulated linear load-flow
model, `P∝r(1−r)`, peaks at `0.5`.

This verifies two declared toy protocols; it does not reproduce a historical
experiment or claim a new result. Neither fraction evidences the Burrisphere,
a universal balance point, or a special biological constant. The accompanying
[tests](test_power_models.py) check these calculations, not MPP in nature.

## 4. The machine unit is more than a copied model `[I/C]`

Hinton's mortal-computation proposal distinguishes hardware-specific learned
parameters from parameters portable between suitable digital machines. He
discusses both distillation and the sharing advantage of digital copies,
alongside the proposed energetic savings of hardware-specific computation.
These are architectural possibilities, not a theorem that biology is always
efficient and digital intelligence always inefficient.
[Hinton, §§8–9](https://www.cs.toronto.edu/~hinton/absps/FFXfinal.pdf).

The proposed comparison boundary is a **service-and-renewal network**:

```text
model/policy ───────────────┐
hardware + power + cooling ├→ delivered service → resources for renewal
repair + logistics ────────┤                         │
people + permissions ──────┘← maintenance, learning, replacement ─┘
```

Each arrow is a dependency to investigate, not a guaranteed beneficial flow.
There can be several alternative support paths, shared bottlenecks and
correlated failures. Do not assume independent availability or multiply
component probabilities without evidence.

**Copying instructions is not reproducing the means to execute them.** A
thousand copies of a controller do not supply an absent pump bearing. Equally,
organisms that divide cells still depend on nutrients and ecological partners;
the comparison is not biology-without-networks versus machines-with-networks.
“I, Pencil” is a useful specialization analogy, not a distinct physical law.

This network is an explanatory boundary, not automatically an evolutionary
individual or a conscious holobiont. A selection claim must separately name
what varies, what is inherited or retained, who/what selects, and what counts
as differential persistence or reproduction. Firms, models and hardware can
have different lineages and different winners.

The machine-age hypothesis is narrower and stronger than an essence claim:
**portable policies may accelerate adaptation while physical renewal and
coordination bound how much of that adaptation becomes durable service.**
Cheap replication can reduce energy per task through reuse even when total
demand grows; demand can also saturate. Neither growth nor a Kardashev ascent
follows necessarily. Test the architecture and task, not the label “machine.”

## 5. Recursion can regenerate—or extract `[I/C]`

The causal candidate is:

`capture → useful output → maintenance / renewal / adaptation → later capability`.

Every connection can fail. Output may be consumed rather than reinvested;
reinvestment may buy fragile dependence; a local gain may reduce a partner's
ability to supply anything tomorrow. Recursion alone is not self-correction.
No finite resource system licenses endless growth merely because it has a
positive feedback loop.

A synthetic example distinguishes the ledgers. Over four hours, one service
delivers 100 accepted tasks in hour one, then fails without repair. Another
delivers 60 each hour. Totals are 100 and 240 respectively. The first wins the
initial throughput comparison; the second wins cumulative delivery. Energy
efficiency remains unknown without energy measurements, and tomorrow's
capability remains unknown without a support assessment.

This is **not** a counterexample to a four-hour MPP model: that model might
also prefer restraint. The scientific competition is between predeclared
predictions, not a shortsighted caricature and our preferred long horizon.

Maintenance, reserve capacity and occasionally doing less may protect more
worthwhile futures than increasing current intake. Specialization can create
both complementarity and bottlenecks. The strongest network should therefore
not be defined as whichever network won after the fact.

## 6. What VMO × SKA now makes explicit `[I/S]`

VMO specifies valued possibilities and testable waypoints. SKA connects them
to present actions, capabilities and evidence. Their **composition** asks
which purposes have supportable paths. It is not physical exergy in joules;
the [experimental numerical product](README.md) keeps its separate gate.

For every claimed improvement ask:

1. Which task or trajectory becomes supportable, for whom, by when?
2. Which physical and cooperative dependencies make it possible?
3. What must be maintained, replaced or learned to keep it possible?
4. Which losses, excluded bearers or shared failure modes did we omit?
5. What observation would require revising the end, not just working harder?

More described options are not automatically more real options. Count distinct
capabilities only under a declared task-equivalence rule, not every paraphrase
or imagined worldline. Switching cost and opportunity cost are also different:
adding a valuable alternative can *raise* the value of the best alternative
foregone, even while improving the choice set. Do not promise universally
falling opportunity costs.

The [Goal](../00_THE_GOAL.md) and Power-Max already make mutual durable options
conditional on Justice, bearers, evidence and horizons. They do not equate
physical throughput with axiology. A dependency argument can explain a reason
to sustain partners; it does not prove universal cooperation or the obligation
to protect a bearer who offers no instrumental advantage.

Our chosen ethic protects such bearers too. It remains a disclosed commitment,
not an extra multiplier, physical force, ranking of people, or conclusion
deduced from survival. “Do not consume your foundation” must include visible
people and ecosystems, not just the optimizer's equipment.

## 7. How the lens can lose `[D/C]`

The [evaluation extension](EVALUATION.md#power-capability-and-renewal-extension)
compares physical-power, reliability and task-capability explanations on
held-out disturbances. It asks whether dependency-aware evaluation predicts
durable service better than a simple local baseline. These explanations can
overlap; agreement does not discriminate them.

If a simpler checklist performs as well, retain it. If physical power adds no
predictive information, reject that MPP application. If a network model adds
no information beyond the component baseline, narrow the network claim. If
the selected ethics hides a harmed bearer, reopen the assessment regardless
of the energy score. None of those failures deletes the source record.

**The refined lens: judge a gain not only by what it captures, but by what it
can sustain, what it enables next, and who bears its cost.** `[I]`

## Scope of this refinement `[B/D]`

This is a local research elaboration of the 2026-09-15 package. Its literature
attributions and toy calculations do not adopt a universal doctrine or report
an empirical machine/biology comparison. The original migration receipt,
formal owners, source pins, JSON contract and validator remain unchanged.
No public page, deployment, product integration or execution permission changes.
The existing recorder's frozen-source mismatch remains a separate HOLD.
