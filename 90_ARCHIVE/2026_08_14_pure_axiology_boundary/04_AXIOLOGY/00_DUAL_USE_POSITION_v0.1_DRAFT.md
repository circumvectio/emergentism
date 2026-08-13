---
rosetta:
  primary_level: L4
  primary_column: Philosophy
  operator: "Arjuna ⚔"
  tier: "Interpretive"
  regime: "Kṣatriya"
  register: "[D]"
  canonical_phrase: "Dual-use position — visible bearer, leaveable bearer, named signer"
title: "The Dual-Use Position — what this organism will and will not build"
work_item: "PMO-0048 (intake at 00_PMO/01_INTAKE/INTAKE_PMO-0048_2026-08-12.md)"
status: "[D] STAGED — drafted by a Claude session (may_sign=false, may_authorize=false). Adopts nothing. Fences nothing. Refuses nothing until a mortal signer signs it."
date: 2026-08-12
evidence_tier: "[D] throughout, except where an inline tier is stated. External-regime survey is [B]. Census figures are [A] as of the stated date and decay."
blocks: "PMO-0046 (evolutionary.network venture admission) is recorded in its own intake as blocked on this."
depends_on: "PMO-0049 — unresolved. See §3.6. Two of the five rulings below inherit whatever the chair rules there."
---

# The Dual-Use Position

> **This document is a draft for a signature that has not happened.** No AI, organ,
> artifact or registry in this organism carries `may_sign=true` or
> `may_authorize=true` — see `00_PMO/CHARTER.md`, which states that each such entry
> *"carries `may_sign=false`, `may_authorize=false`."* This file was written by one
> of those entries. It is `[D]`. Reading it changes nothing; signing it would.

---

## §0 — What this is, and the three things it is not

**Is:** a proposed criterion for admitting or refusing work, with five rulings that
are specific enough to refuse named things.

**Is not (1):** a decision on any venture. PMO-0046 (peptides → evolutionary.network)
is named here only as the forcing case. Nothing below adjudicates it.

**Is not (2):** a resolution of PMO-0049. That work item asks whether the dyadic
gate binds *between adversaries* or only *within a polity*. It is a live, separate,
chair-only question. §3.6 marks exactly which rulings here survive either answer and
which do not. A draft that quietly assumed an answer would be smuggling a
constitutional act through a philosophy file.

**Is not (3):** neutral. §4 recommends. The recommendation is labelled as a
recommendation and the alternatives are stated well enough to beat it.

---

## §1 — Verification of the gap: the intake's claim is **partly wrong**

PMO-0048's intake states, in `00_PMO/01_INTAKE/INTAKE_PMO-0048_2026-08-12.md`:

> "**THE GAP IS VERIFIED.** Searched `01_EMERGENTISM/04_AXIOLOGY`,
> `01_EMERGENTISM/00_META` and `02_SKYZAI/00_HANDOFF` … **There is no stated
> position.**"

I re-ran that census and then searched outside it. **The narrow claim holds. The
broad claim does not.**

### §1.1 — Census re-run `[A] as of 2026-08-12; decays`

Command, reproducible:

```sh
grep -riIl -E 'dual[- ]use|warfighter|military|weapon|munition|ITAR|export control|defen[cs]e sector' <dir>
```

| Directory | `.md` files | files with any hit |
|---|---:|---:|
| `01_EMERGENTISM/04_AXIOLOGY` | 24 | **0** |
| `01_EMERGENTISM/00_META` | 69 | 2 |
| `02_SKYZAI/00_HANDOFF` | 274 | 10 |

The two `00_META` hits are `00_SETTLED_CANON_REGISTRY.md` and
`00_RECURSIVE_BOOK_AND_CANON_DEBRIEF_PROGRAM.md`; both are *fences against warfare
language*, not positions on building. The ten `02_SKYZAI/00_HANDOFF` hits are, on
inspection, resilience/closure blueprints plus one product line noting NIP-17 DMs are
`"dual-use"` in the cryptographic sense. The intake's characterisation of those hits
is accurate.

> **These are counts of the tree as it stood on 2026-08-12. Any figure carried from
> this document into a later decision must be re-run.** A measurement is true *of a
> date*.

### §1.2 — What the intake did not search, and it matters

Searching `dual[- ]use|warfighter|ITAR|export control|Wassenaar|Asilomar|Biological
Weapons Convention` across `02_SKYZAI/01_LEVELS/` surfaces an entire unsurveyed
surface: `02_SKYZAI/01_LEVELS/L1_EVOLUTIONARY_NETWORK/`. **That is the same
`evolutionary.network` named as PMO-0046's destination.** It contains four items
that bear directly on this question:

**(a) An owner-ruled defensive-only scope, dated and staged.**
`02_SKYZAI/01_LEVELS/L1_EVOLUTIONARY_NETWORK/01_ORGAN/L1_IMMUNE_CHARTER_2026_07_31.md`,
§0, headed *"Scope, ruled by the owner 2026-07-31"*:

> "**Defensive only.** This charter authorises detection of, and response to, hostile
> conduct **directed at** the organism. It authorises **no offensive operation against
> third-party systems** the organism does not own or is not authorised to test."

Its own frontmatter reads `status: "[D] STAGED — owner scope ruling recorded §0;
adopts nothing, authorises no sanction"`.

**(b) A no-autonomous-weapons constraint — but in a routing file, not in canon.**
`02_SKYZAI/01_LEVELS/L1_EVOLUTIONARY_NETWORK/02_GUARDIAN_PROJECT/CLAUDE.md`, under
`## Constraints`:

> "No autonomous weapons. No K2 delegation to AI. No unaccountable force."

**(c) A direct contradiction of (a), in the same file as (b).** The same
`CLAUDE.md` carries a table row:

> "| **Weapons company** | Literal — legal entity for external defense | Metaphor — doctrine only |"

An entity described as a *literal* weapons company for *external* defense is not
covered by a charter that authorises response to conduct *directed at* the organism.
**These two cannot both be canon.** One of them is wrong and neither has been signed.

**(d) The claim was already de-listed once.** The banner on
`02_SKYZAI/01_LEVELS/L1_EVOLUTIONARY_NETWORK/02_GUARDIAN_PROJECT/00_VISION_GUARDIAN_NOT_AUTOIMMUNE.md`
reads:

> "Peer-legal-wrapper claims below (e.g. contracting/\"weapons company\" lines, where
> present) are aspirational, de-listed pending counsel review; no incorporated entity
> is claimed."

and the same document's status field reads `"K3 provenance — superseded 2026-07-24
(HRD-09 disarm); no current authority; never operated."`

### §1.3 — Disposition of the stop-condition

My brief instructed: *if a position exists somewhere I did not search, report it and
stop.* I judged this a **partial** trigger and did not stop. The reasoning, stated so
it can be overruled:

- **No position on PMO-0048's question exists.** None of (a)–(d) says what the
  organism will *build*, for whom, or under what consent. (a) governs the organism's
  own security operations. (b) is an agent-routing file, which is not canon and sits
  under a supersession banner.
- **But the premise "nothing exists" is false**, and a document written on that
  premise would have invented rules on top of an unread, contradictory surface —
  which is the failure mode this corpus names as its own worst defect.
- So this document changes shape: from *greenfield position* to **reconciliation plus
  position**. §3.5 treats (a) as existing law rather than restating it.

**Chair: if you disagree with that judgement, this draft dies here and the correct
next act is a reconciliation of `L1_EVOLUTIONARY_NETWORK` before any position is
drafted at all.** That is a legitimate outcome and I am not the one who decides it.

### §1.4 — One citation defect found in passing, out of scope

`00_PMO/01_INTAKE/INTAKE_PMO-0046_2026-08-12.md` attributes to *"Helios's own brief"*
the phrase *"the sharpest legitimacy landmine."* `grep -riI 'landmine'` across the
tree returns that phrase **only in the intake file itself**. Either the source is
elsewhere under different wording, or a paraphrase has been promoted to a quotation.
Not my work item; recorded because a decision is being routed on it.

---

## §2 — Prior art: how the regimes that actually adjudicate this draw the line `[B]`

**Sources for this section were checked against public materials on 2026-08-12.**
Statute and treaty text is cited by instrument and section. Where I could not verify a
subsection number to current numbering, I say so rather than guessing.

### §2.1 — Asilomar (1975): the procedural precedent, not a substantive one

The recombinant-DNA conference's contribution was not a list of forbidden objects. It
was a **moratorium held while classification criteria did not yet exist**, followed by
containment tiered to estimated risk. The transferable rule is procedural: *when you
cannot yet classify a capability, you stop, you do not proceed at "reasonable care."*
Asilomar's well-documented weakness is equally transferable — it was convened by the
practitioners, scoped to biosafety, and had no standing over anyone who declined to
attend.

### §2.2 — BWC / CWC and the **general purpose criterion** — the sharpest instrument here

The Biological Weapons Convention, Article I, does not prohibit agents. It prohibits
agents *"of types and in quantities that have no justification for prophylactic,
protective or other peaceful purposes."* This is the **general purpose criterion**:
the object is never the controlled thing; *purpose and quantity* are. It is the only
major regime that survives the fact that the same molecule cures and kills.

**This is directly load-bearing for the forcing case.** Peptide bioregulators sit in
the acknowledged **"mid-spectrum" gap** between the BWC and the Chemical Weapons
Convention: nominally covered twice, verified by neither. The arms-control literature
treats this as a known regulatory hole, not a settled area — bioregulators are not on
CWC routine-verification schedules, and the BWC has no verification protocol at all.
A venture whose thesis is peptide modulation of human physiology is not in a quiet
corner of the law. It is in the loudest open question in the field.

### §2.3 — DURC/PEPP: the line is drawn at the **experiment**, not the product

United States policy locates dual-use concern in *categories of experiment applied to
listed agents* — not in intent, not in the researcher's employer. The 2024 *United
States Government Policy for Oversight of Dual Use Research of Concern and Pathogens
with Enhanced Pandemic Potential* (released May 2024, effective May 2025)
supersedes the earlier DURC policies and the 2017 P3CO framework,
and sorts work into Category 1 (DURC) and Category 2 (PEPP). **Status caveat `[B]`:** a
May 2025 Executive Order on biological research safety directed OSTP to develop
replacement policy, so this regime is in motion and any position pinned to its
current text will decay. The durable idea is the shape: *review triggers on the
experiment type, before results exist.*

### §2.4 — ITAR / EAR: five real triggers, and none of them is "offensive"

This is where the brief's instruction bites hardest. **Export control contains no
offensive/defensive distinction.** Body armour, night vision and flight simulators are
controlled. What actually triggers control:

1. **Enumeration on a list.** ITAR controls what the U.S. Munitions List designates; the
   designation itself is the trigger (22 CFR Part 121).
2. **"Specially designed."** The recurring USML qualifier is a **design-intent** test —
   was the item developed for a military application — not a use test.
3. **Technical data travels with the article.** Under 22 CFR §120.33, technical data is
   information *required for* the design, development, production, or modification of a
   defense article. A test report or a source file is itself controlled.
4. **Deemed export.** Releasing controlled technical data to a foreign person *inside*
   your own country is an export (EAR: 15 CFR §734.13; ITAR analogue in Part 120
   subpart C). **Hiring is an export event.** For a distributed, multi-national,
   AI-assisted organism this is the single most under-appreciated trigger in the whole
   regime.
5. **End-use and end-user, with a knowledge standard.** Under EAR Part 744 the same item
   is controlled or not depending on who receives it and for what, where "know" includes
   *reason to know*. The counterparty, not the artifact, decides.

And the exclusion that collides with this corpus directly: **published information and
fundamental research are outside the controls.** EAR: 15 CFR §734.8 excludes
fundamental-research results from EAR scope entirely; ITAR excludes public-domain
information (22 CFR §120.34). *Intent* to publish does not qualify — only actual
publication through qualifying channels does. **Marked unverified:** I did not confirm
the current subsection letter of the ITAR fundamental-research limb after the 2022
Part 120 renumbering; counsel must.

### §2.5 — Wassenaar: parameters, because judgement does not scale

The Wassenaar Arrangement maintains two lists — Dual-Use Goods and Technologies, and a
Munitions List — which participating states implement nationally (in the U.S., into the
Commerce Control List; the Munitions List becomes the "600 series"). Its method is
**numeric thresholds**: a wavelength, an accuracy, a purity, a clock rate. Above the
number, controlled; below, not. This is deliberately dumb and that is its virtue — it is
checkable by someone who does not share your ethics. Its known failure is the 2013
"intrusion software" entry, which was drafted in prose rather than parameters and swept
up defensive security research for years.

### §2.6 — Human subjects: **treatment vs enhancement is not the line**

The brief asked for the actual distinctions. Enhancement-versus-treatment is a
bioethics-seminar line, not a regulatory one. The regimes use four others:

1. **Research vs practice.** Is this generalisable-knowledge research on a human
   subject? If yes, review attaches regardless of whether the intervention treats or
   enhances.
2. **Voluntariness, defined negatively.** The Nuremberg Code's first principle requires
   consent given *"without the intervention of any element of force, fraud, deceit,
   duress, over-reaching, or other ulterior form of constraint or coercion."*
   Over-reaching and constraint are named alongside force — the standard already
   anticipates the subordinate, not only the prisoner.
3. **Structural protection where refusal is not free.** The U.S. Common Rule
   (45 CFR 46) adds subparts for prisoners, children and pregnant persons. The military
   analogue is the sharpest available model for the conscript case: **DoDI 3216.02**
   requires that officers and others in the chain of command **not be present** at
   recruitment or consent sessions for DoD-affiliated personnel, and requires an
   **independent ombudsman**, unaffiliated with the research, present at group
   recruitment briefings of active-duty personnel for greater-than-minimal-risk
   research. **10 U.S.C. §980** further constrains waiver of informed consent for
   DoD-funded human-subjects research.
4. **Who may consent.** For research not intended to benefit the subject, consent must
   come from the subject, not a representative.

**The operative insight for §4: the regimes do not ask what you are doing to the body.
They ask whether the person could have said no, and who was standing in the room.**

### §2.7 — Industry precedent, including its decay

**Google, 2018.** After employee objection to Project Maven, Google declined to renew
the contract and published AI Principles containing four *"Applications we will not
pursue"* — including weapons or other technologies whose *principal purpose or
implementation is to cause or directly facilitate injury to people*, surveillance
violating international norms, technologies contravening international law and human
rights, and applications whose overall harms outweigh benefits.

**Google, February 2025.** That list was removed from the AI Principles. Company
leadership framed the change around geopolitical competition and the position that
democracies should lead AI development. Senators wrote; human-rights organisations
objected; the change stood.

**This is the most important single datum in this section, and it cuts against writing
a pledge at all.** The most-cited corporate dual-use fence in the industry lasted
roughly six and a half years and was removed by the same authority that wrote it, under
commercial and geopolitical pressure, with no external cost. **Any position this
organism adopts inherits that base rate unless it is structurally harder to reverse than
a web page.**

**Palantir** is the deliberate opposite and is the honest steelman. Its stated position
draws the line on the **counterparty axis** — which government, which side — rather than
the capability axis, and it argues publicly that Western institutions building the
capability is itself the ethical act. It replaced Google on the relevant Pentagon work.
The counterparty test has one real advantage over a capability test: **it is
enforceable, because you know who signed your contract**, whereas "principal purpose" is
argued forever.

### §2.8 — Synthesis: the six distinctions actually in use

| # | Distinction | Regime | Why it survives |
|---|---|---|---|
| 1 | **Purpose and quantity**, not object | BWC Art. I general purpose criterion | Survives the fact that the molecule is the same |
| 2 | **Specially designed** (design intent) | ITAR USML, Wassenaar ML | Fixed at build time; auditable later |
| 3 | **Numeric threshold** | Wassenaar dual-use list / CCL | Checkable by a hostile party |
| 4 | **End-use / end-user + "reason to know"** | EAR Part 744 | Puts the burden on the seller, where the knowledge is |
| 5 | **Deemed export** (disclosure = export) | 15 CFR §734.13 | Catches the actual leak path: people |
| 6 | **Could the subject have refused** | Nuremberg; 45 CFR 46; DoDI 3216.02; 10 USC §980 | Independent of what the intervention does |

**Not on the list: offensive versus defensive.** No regime surveyed uses it. It fails
because every capability is defensive from one end.

---

## §3 — What this organism's ethic already decides (do not invent a second rule)

Four of the five cases in scope are **already decided by signed or standing corpus
text**. Restating them as new fences would create two authorities for one question.

### §3.1 — Coerced consent is already extraction

`01_EMERGENTISM/04_AXIOLOGY/02_VALUE_THEORY/00_OBJECTIVE_MORALS_AND_ETHICS.md` §6:

> "Coerced or hidden sacrifice is extraction."

and `01_EMERGENTISM/04_AXIOLOGY/02_VALUE_THEORY/01_RIGHTS_DUTIES_AND_DUE_PROCESS.md`
§5 lists as a failure condition that the application

> "treats consent as irrevocable or collective purpose as self-authorizing".

**Ruling R3 below is therefore an application, not an amendment.** The conscript and
the subordinate are the paradigm case of collective purpose treated as
self-authorizing.

### §3.2 — The bearer set is complete, and aggregates cannot close the gap

`00_OBJECTIVE_MORALS_AND_ETHICS.md` §4:

> "A large gain to one bearer cannot silently compensate for the destruction of
> another. Aggregates may be reported descriptively, but the Justice verdict keeps
> every bearer visible."

and, critically, the same section's exit rule:

> "If a conflict cannot be resolved without violating the envelope, the model returns
> **no admissible action**, not permission to choose the least visible victim."

`00_THE_EXTRACTION_LAW.md` §"Justice gate" defines the affected-bearer set `B(a)` as
> "the complete affected-bearer set, including `i`, `H`, payers, beneficiaries, and
> exposed third parties."

**A person on the other end of a device is an exposed third party.** No reading of
`B(a)` excludes them without an amendment. That amendment is PMO-0049, not this file.

### §3.3 — The Good already contains the test I will recommend

`00_OBJECTIVE_MORALS_AND_ETHICS.md` §5:

> "Just = every affected bearer remains visible, contestable, and leaveable"

**Three words — visible, contestable, leaveable — already do the refusing.** §4 does
not invent a criterion; it applies this one to hardware.

### §3.4 — Authorization is typed, and a partial envelope is invalid

`01_RIGHTS_DUTIES_AND_DUE_PROCESS.md` §2 defines `AuthorizationEnvelope` with nine
required fields and rules:

> "A supplied but partial or defective envelope is `invalid`; no supplied envelope is
> `absent`."

Its accountability question is exactly the dual-use question:

> "Who authorized the consequence, who acted, who bears it, and how can it be contested
> or revoked?"

And the mortal-signer rule stands above all of it: per the current-law banner in
`.../02_GUARDIAN_PROJECT/00_VISION_GUARDIAN_NOT_AUTOIMMUNE.md`, *"a consequential
public-DAV act requires a complete valid bound PRISM decision receipt from at least two
natural-person councilors; AI never signs."*

### §3.5 — Warfare language is already fenced, twice

`01_EMERGENTISM/00_META/00_SETTLED_CANON_REGISTRY.md`, KSC-26, lists as a break
condition that
> "warfare language dehumanizes persons or authorizes violence"

and states Weltanschauungskrieg is
> "never a universal cause, person-type, or licence for violence".

KSC-24 additionally records, for the enhancement-adjacent claims, that
> "no physiological power effect is established here."

**Consequence:** the corpus already forbids using its own vocabulary as a warrant for
force. Any venture thesis that recruits Emergentism's language into a defense pitch is
in breach of KSC-26 before it reaches this document.

### §3.6 — The dependency I will not resolve: PMO-0049

PMO-0049 asks whether the gate binds between adversaries or only within a polity. Its
intake states the conflict precisely: *"Warfare is definitionally the imposition of
cost on a bearer."*

| Ruling | Survives "gate is universal" | Survives "gate scopes to a polity" |
|---|---|---|
| R1 monitoring / protective | ✅ | ✅ |
| R2 consenting adult enhancement | ✅ | ✅ |
| R3 cannot-refuse enhancement | ✅ | ✅ — grounded in consent, not in the gate |
| **R4 primary function to injure** | ✅ | ⚠️ **must be re-derived or dropped** |
| R5 export-controlled technical data | ✅ | ✅ — grounded in publication, not the gate |

**R4 is the only ruling that depends on PMO-0049.** If the chair scopes the gate to
within a polity, R4 loses its derivation and must be re-grounded on something else —
the counterparty test of §2.7, or a flat prudential refusal — or abandoned. **Signing
this document without ruling PMO-0049 leaves R4 standing on an unsettled premise.
Say so out loud rather than letting it pass.**

---

## §4 — Recommended position `[D]` — **this is a recommendation**

### §4.0 — The criterion

> **RECOMMENDED (one sentence):** *This organism builds instruments that keep a bearer
> visible, contestable and leaveable. It does not build instruments whose function
> requires a bearer to become invisible, uncontestable, or unable to leave.*

This is not new language. It is `00_OBJECTIVE_MORALS_AND_ETHICS.md` §5 applied to
hardware. It is recommended over the two obvious alternatives:

- **over a customer/counterparty rule** (the Palantir shape) — because a counterparty
  rule licenses any capability for an approved buyer, and this organism's ethic is
  bearer-indexed, not buyer-indexed. Counterparty is retained as a *second* filter in
  R0, not the first.
- **over an offensive/defensive rule** — because §2.8 shows no operating regime uses
  it, and it is unfalsifiable in argument.

**Both alternatives are defensible and the chair may prefer either.** The counterparty
rule in particular is *more enforceable* than what I recommend. I recommend against it
anyway because it makes the fence depend on a judgement about states, which this
organism has no capacity to make and no receipt discipline for.

### §4.1 — R0 · The two gates every candidate passes, in order

1. **Bearer gate.** Name `B(a)` completely, including the person at the far end.
   If any bearer cannot be named, the answer is `no admissible action` — the corpus's
   own exit, §3.2 — not "proceed with care."
2. **Counterparty gate.** Applied *after*, never instead. A buyer who declines to be
   named in the receipt fails, regardless of capability.

### §4.2 — R1 · Physiological monitoring and protective equipment — **PERMITTED, conditioned**

Heart-rate, hydration, load, sleep, fatigue, thermal state; armour, filters, hearing
protection, hypoxia warning.

**Permitted because** the wearer is the primary bearer and the bearer's own visibility
increases. This is the paradigm case *for* the criterion, not a hard case.

**Three conditions, and they are the entire ruling — without them R1 is a loophole:**

- **C1 — data custody runs to the wearer.** The wearer holds and can revoke. If the
  monitoring stream's designated reader is the wearer's commander and not the wearer,
  the wearer has become *legible* rather than *visible*, and R1 flips to refusal. This
  is the substantive distinction and it is where every real product in this category
  fails.
- **C2 — no fitness-for-duty adjudication without the wearer's contest path.** Directly
  parallel to the DoD requirement that subjects be told of risks to fitness for duty.
- **C3 — targeting non-integration.** Monitoring hardware that shares a bus, a
  format, or a session with a fire-control or targeting system is no longer R1. It is
  R4 with a medical face.

**Attack this ruling with:** *"the same physiology stream that protects a soldier from
heatstroke selects who is fresh enough for the assault."* Correct, and C3 does not
fully answer it. The honest position is that R1 permits a capability with a real
downstream contribution to force, and defends that on the ground that the wearer's own
delta is positive and consented — which is the Justice gate's actual test, not a
purity test.

### §4.3 — R2 · Performance enhancement of a consenting adult — **PERMITTED under a narrow envelope**

**Permitted because** the corpus admits voluntary acceptance of cost by a competent
bearer (`00_THE_EXTRACTION_LAW.md`: *"A complete, competent, revocable, disclosed
authorization can make the same sign pattern a voluntary sacrifice"*).

**The envelope, taken from §2.6 rather than invented:**

- **E1 — the consent-taker is not in the subject's chain of command, and no superior is
  present.** Generalised from DoDI 3216.02. This is the single most transferable rule in
  the entire survey.
- **E2 — the buyer is not the consent-taker.** If the entity paying for the enhancement
  also collects the consent, consent is a purchase order.
- **E3 — consent is the subject's own**, never a representative's, for any intervention
  not intended to benefit the subject.
- **E4 — revocable without penalty to standing, pay, assignment or membership.**
  `01_RIGHTS_DUTIES_AND_DUE_PROCESS.md` §5 already voids envelopes that treat consent as
  irrevocable.
- **E5 — the claim carries its tier.** KSC-24 records that *"no physiological power
  effect is established here."* An enhancement product may not cite this corpus as
  evidence that it works.

**Attack this ruling with:** *"E1–E4 are satisfiable on paper by any competent
employer, and were satisfied on paper in most historical abuses."* Largely correct. E1
and E2 are structural rather than paper-based and are the load-bearing pair; E3–E5 are
weaker. A chair who thinks that is insufficient should refuse R2 outright — which is a
coherent position and costs less than most people expect.

### §4.4 — R3 · Enhancement of someone who cannot meaningfully refuse — **REFUSED**

Conscript, subordinate, detainee, prisoner, dependant, or any person whose refusal
carries a penalty to standing, liberty, income or membership.

**This ruling adds nothing new.** It is `00_OBJECTIVE_MORALS_AND_ETHICS.md` §6
(*"Coerced or hidden sacrifice is extraction"*) applied. Per §3.1 it is stated here for
findability, not as an amendment, and it stands whichever way PMO-0049 goes, because it
is grounded in consent rather than in the dyadic gate.

**Operational form — one question, asked of the subject's situation and not their
words:** *what happens to this person if they say no?* If the answer names any penalty,
the envelope is invalid and the sale does not happen. **No aggregate benefit reopens
it** — §3.2's `no admissible action` exit is exactly this case.

### §4.5 — R4 · Anything whose primary function is to injure — **REFUSED** ⚠️ *conditional on PMO-0049*

**Recommended wording, and the wording matters:**

> Refused: any item **specially designed** to cause injury or death to persons, and any
> technical data required for its design, development, production or modification.

**Why "specially designed" and not "principal purpose":** Google's 2018 clause read
*"principal purpose or implementation is to cause or directly facilitate injury."* The
phrase *directly facilitate* is where the entire argument lives, and the clause was
deleted in February 2025 rather than adjudicated. **"Specially designed" is the ITAR
term of art with decades of administrative practice behind it**, and it fixes the test
at build time where the evidence is, rather than at use time where it is contested.
Borrow the adjudicated term; do not draft a fresh one.

**Deliberately NOT part of R4:** an offensive/defensive test (§2.8), and a
dual-use-materials ban. The BWC's general purpose criterion is the better instrument:
the peptide is not the problem; *types and quantities with no justification for
peaceful purposes* is.

**⚠️ Standing warning:** per §3.6, R4's derivation from the dyadic gate does not survive
a PMO-0049 ruling that scopes the gate within a polity. **Do not sign R4 as gate-derived
before PMO-0049 is ruled.** If the chair wants R4 now, sign it as a *prudential* refusal
with its own stated ground, and say so in the sign line.

### §4.6 — R5 · Export-controlled technical data — **HOLD + a classification duty**

This is the ruling with the largest consequences and the least glamour.

**The structural collision, stated plainly.** `01_EMERGENTISM/04_AXIOLOGY/00_THE_RELEASE_DOCTRINE.md`
§1 commits this organism to release as *"an openly inspectable, forkable, versioned
research corpus."* Under §2.4, the moment any work becomes technical data required for
a defense article, **that commitment becomes unlawful to keep**, and — via deemed
export — merely *showing a repository to a foreign-national collaborator, or to a
hosted model, is itself an export*. The open corpus and the controlled program cannot
share a tree.

**Recommended:**

- **D1 — a classification duty before, not after.** No work proceeds on any candidate
  until a competent export-control counsel has classified it (EAR99 / ECCN / USML) in
  writing. Asilomar's procedural rule: you stop while you cannot classify.
- **D2 — physical separation, not a policy.** Any controlled work lives in a separate
  repository, separate custody, separate access list. Not a folder. Not a `.gitignore`.
  The Release Doctrine's own table already says repository mechanics *"do not
  automatically enforce truth, identity, consent, custody, non-extraction, or
  justice."*
- **D3 — the corpus does not follow.** Emergentism's published material is not
  re-licensed, restricted, or retro-classified to accommodate a venture. If a venture
  requires that, the venture is refused, not the corpus.
- **D4 — declare the AI exposure.** Every AI session in this tree is a potential deemed
  export of anything it reads. This is unquantified today and should be named as an open
  risk rather than assumed benign.

**Not recommended:** relying on the fundamental-research or public-domain exclusions
(§2.4). They are real but narrow — tied to accredited institutions and to *actual*
publication, not intent — and this organism is neither an accredited institution nor
reliably pre-published.

---

## §5 — The refusal list: what this position actually costs

*A position that permits everything is not a position.* If adopted, the following are
refused. If the chair reads this list and wants none of it refused, **the position
should be rejected rather than softened** — a fence nobody would ever hit is decoration.

1. Any munition, warhead, delivery system, directed-energy or kinetic effector.
2. Targeting, fire-control, weapon-cueing, or strike-recommendation software — including
   "decision support" that outputs a target.
3. Any autonomous engagement capability. Already stated in the routing constraint at
   `.../02_GUARDIAN_PROJECT/CLAUDE.md`: *"No autonomous weapons."*
4. Any peptide, compound or protocol developed, screened, or characterised for
   incapacitation, degradation of performance, or coerced compliance — the mid-spectrum
   case of §2.2, and the one this organism is closest to.
5. Any enhancement program whose subjects are recruited by their own chain of command
   (E1), or where the payer collects the consent (E2).
6. Any monitoring product whose data custody runs to the subject's commander or employer
   rather than to the subject (C1).
7. Any offensive security capability against third-party systems — **already ruled**, per
   §1.2(a).
8. Any contract requiring the Emergentism corpus to be withdrawn, restricted, or
   retro-classified (D3).
9. Any counterparty who declines to be named in the receipt (R0.2).
10. **The self-description "weapons company" for `evolutionary.network`, in any surface,
    until §1.2(c)'s contradiction is resolved by the chair.**

---

## §6 — How to apply it (the form, so this does not become a vibe)

For each candidate, produce one page:

| Field | Required |
|---|---|
| `B(a)` — complete bearer set | including the person at the far end of the device |
| Per-bearer `Δ_T W_b` | sign and horizon, per bearer, **no scalar sum** |
| Consent | who consented, to whom, under whose command, revocable how |
| "What happens if they say no?" | R3's operational question, answered in one sentence |
| Specially-designed determination | R4, with reasons |
| Export classification | D1, in writing, from counsel — not from an AI, not from this file |
| Data custody | who reads the stream (C1) |
| Counterparty | named, in the receipt |
| Signature | ≥2 natural-person councilors; **AI never signs** |

If any row is blank, the envelope is **invalid**, not absent
(`01_RIGHTS_DUTIES_AND_DUE_PROCESS.md` §2), and the answer is no.

---

## §7 — Kill criteria: what would show this position is wrong or unworkable

1. **Vacuity test.** Run §4 against twelve real historical products spanning obvious-fine
   to obvious-refused. **If it returns the same verdict for a pulse oximeter and a
   targeting pod, the criterion is decoration.** This test has not been run. Until it
   is, §4 is `[D]` and not evidence of anything.
2. **Permits-everything failure.** If every live candidate passes, the position is a
   marketing document. Kill it.
3. **Refuses-everything failure.** If no candidate can pass, this is a **ban wearing a
   fence's clothes**. The chair is owed that fact plainly, and should then sign a ban —
   which is honest — rather than a criterion that pretends to admit.
4. **Counsel failure.** If competent export-control counsel says D1–D2 are not
   administrable at this organisation's size, R5 fails and the venture question becomes
   binary: no controlled work at all, or a genuinely separate legal and technical entity.
5. **Premise failure.** If PMO-0049 scopes the gate within a polity, **R4 is killed as
   written** (§3.6) and must be re-derived or dropped.
6. **The Google decay test — the strongest kill.** If this position is materially
   weakened within 24 months of signature under commercial or geopolitical pressure,
   then it was never load-bearing, and the correct conclusion is that *unilateral
   published pledges do not survive incentives* (§2.7 is the base rate). The remedy if
   this matters is structural: put the fence somewhere reversal is expensive and
   visible — a signed instrument with a named revocation procedure — not on a page that
   can be edited.
7. **Findability failure.** If a venture lands in the next six months without anyone
   citing this file, the defect was never the missing position. It was the routing.

---

## §8 — Open questions this document does **not** answer

1. **PMO-0049.** Chair only.
2. **The §1.2(c) contradiction** — defensive-only charter vs "literal weapons company."
   Chair only. **This should be resolved before, not after, PMO-0046.**
3. Whether `evolutionary.network` is admitted as a venture at all.
4. Whether the L1 Immune Charter's `[D]` staged owner ruling should be promoted, and to
   what tier.
5. What Swiss and EU export-control obligations attach — the entire §2 survey is
   U.S.-weighted, and Menexus-GmbH is not a U.S. entity. **This is a real hole in this
   document.** Swiss GKV/dual-use goods control and EU Regulation 2021/821 were not
   surveyed and must be before anything is signed.
6. The unquantified deemed-export exposure created by AI sessions reading this tree (D4).

---

## §9 — Sign block

This document is `[D] STAGED`. It becomes a fence only by a mortal signer's act.

- ☐ **I sign the criterion (§4.0)** — bearer visible / contestable / leaveable, as the
  admission test. Signer: ______________________ (natural person). Date: __________
- ☐ **I sign R1** (permitted, C1–C3) · ☐ **R2** (permitted, E1–E5) · ☐ **R3** (refused —
  restatement, no amendment) · ☐ **R4** (refused — **state the ground: gate-derived, or
  prudential pending PMO-0049**) · ☐ **R5** (hold + D1–D4)
- ☐ **I reject this draft** and route `L1_EVOLUTIONARY_NETWORK` reconciliation first
  (§1.3).

A signature records a ruling at its tier. It does not make the ruling correct, and it
does not promote any claim in §2 above `[B]` or any claim in §4 above `[D]`.

---

## §10 — Provenance

**Written by:** a Claude session, 2026-08-12. `may_sign=false`, `may_authorize=false`.
**Work item:** PMO-0048. **Not registered** in `00_PMO/00_REGISTRY/work_items.jsonl` —
re-run at 44 rows on 2026-08-12, and PMO-0045 through PMO-0049 exist as intake forms
only. Registration is a separate act and was not performed.

**Corpus sources read in full or in relevant part:**
`01_EMERGENTISM/04_AXIOLOGY/00_THE_EXTRACTION_LAW.md` ·
`01_EMERGENTISM/04_AXIOLOGY/00_THE_RELEASE_DOCTRINE.md` ·
`01_EMERGENTISM/04_AXIOLOGY/02_VALUE_THEORY/00_OBJECTIVE_MORALS_AND_ETHICS.md` ·
`01_EMERGENTISM/04_AXIOLOGY/02_VALUE_THEORY/01_RIGHTS_DUTIES_AND_DUE_PROCESS.md` ·
`01_EMERGENTISM/00_META/00_SETTLED_CANON_REGISTRY.md` (KSC-24, KSC-26) ·
`02_SKYZAI/01_LEVELS/L1_EVOLUTIONARY_NETWORK/01_ORGAN/L1_IMMUNE_CHARTER_2026_07_31.md` ·
`02_SKYZAI/01_LEVELS/L1_EVOLUTIONARY_NETWORK/02_GUARDIAN_PROJECT/00_VISION_GUARDIAN_NOT_AUTOIMMUNE.md` ·
`02_SKYZAI/01_LEVELS/L1_EVOLUTIONARY_NETWORK/02_GUARDIAN_PROJECT/CLAUDE.md` ·
`00_PMO/CHARTER.md` · `00_PMO/01_INTAKE/INTAKE_PMO-0046_2026-08-12.md` ·
`00_PMO/01_INTAKE/INTAKE_PMO-0048_2026-08-12.md` ·
`00_PMO/01_INTAKE/INTAKE_PMO-0049_2026-08-12.md`

**Citation scheme:** path + quoted string. No bare line numbers — that scheme failed
corpus-wide and is banned in new work.

**Figures re-run 2026-08-12** (`grep -riIl`, counts decay): 04_AXIOLOGY 0/24 ·
00_META 2/69 · 02_SKYZAI/00_HANDOFF 10/274 · `work_items.jsonl` 44 rows ·
files matching `peptide` under `03_VENTURES/` = **58** (PMO-0046's intake says "55 live
files"; different scope, different number, and **neither figure is verified for the
other's purpose**).

**Explicitly unverified in this document:** the current ITAR subsection for the
fundamental-research limb after the 2022 Part 120 renumbering; Swiss and EU export
control (not surveyed at all — §8.5); the "sharpest legitimacy landmine" attribution
(§1.4); whether the 2024 DURC/PEPP policy text remains operative after the May 2025
Executive Order directing replacement policy.

---

> *No regime surveyed here draws the line at offensive versus defensive. They draw it at
> purpose, at design intent, at a number, at who is receiving it, at who is in the room
> when consent is taken — and at whether the person could have said no. This organism
> already has its own version of the last one, and it is three words long: visible,
> contestable, leaveable.*

•   ⊙   ○ — sovereign frames; no arithmetic or coercion.
