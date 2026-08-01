---
title: "The Program Plan — seven sprints to a closed internal program, and why that is not 'finished'"
status: "SUPERSEDED AS CURRENT SEQUENCING — retained as the 2026-07-30 proposal; use the contact-limited roadmap"
date: 2026-07-30
evidence_tier: "[B] every count below is measured and reproducible; [S] the sequencing and the definition of done; [I] nothing"
owner: "No owner until ratified. This plan creates no authority and may not be cited as a commitment."
parents:
  - README.md
  - ../00_META/00_W8_ADEQUACY_DECISION_MATRIX.md
  - ../00_META/00_CONTACT_LIMITED_COMPLETION_ROADMAP_2026_08_01.md
---

# The Program Plan

> **Current routing, 2026-08-02:** this dated proposal is provenance, not the
> execution queue. Sprint 1's invitation-first premise is superseded by the
> contact-limited roadmap and the blocked `FPE-REVIEW-01` registry.

> **Read the definition of done before the sprints, or the sprints will read as a promise
> they are not making.**

## 0 · What can and cannot complete

This project **cannot** be completed in the sense of finished, proven, or validated. It is
a fallibilist worldview with a live correction ledger and an exit on the inside; a version
of it that declared itself done would have broken its own rule against exactly that. The
trigger watchlist bars the vocabulary, and `00_ESTABLISHED` exists precisely because the
honest answer to *what survives?* is short.

**What can complete is the internal program.** Definition of done, and it is checkable:

```text
DONE  =  every finite internal item closed or explicitly abandoned with a reason
      AND the gate green with no baseline held open by convenience
      AND the only thing blocking the next claim is a reply from outside
```

That state has a name worth using: **contact-limited**. It is reachable, it is falsifiable
(the gate reports it), and reaching it changes nothing about whether the framework is
true. It changes only this: after it, no further internal work can be mistaken for
progress.

**The measured backlog, 2026-07-30:**

| finite, closable from inside | count |
|---|---|
| residual owner decisions | 6 — receipt disposition (1), `/dimensions/` crossings (1), audit items 3/11/14/28 (4) |
| ambiguous receipt numbers | 91 |
| site routes declared neither current nor frozen | 40 |
| claim rows at status `open` | 17 |
| audit items awaiting a ruling | 4 |
| folders never surveyed at body level | 2 |

| contact-gated — **cannot** be closed from inside | count |
|---|---|
| preregistrations written / run | 3 / 0 |
| review packet hash set / technical binding satisfied / remaining human prerequisites satisfied / sent | 1 / 1 / 0 / 0 |
| empirical sockets specified / run | 11 / 0 |
| returned outcomes from outside | **0** |

---

## 1 · The sequencing rule, which is the only interesting decision here

**Order by latency, not by size.** The smallest item on the board — sending one email —
has the longest completion time, because a reviewer takes weeks and none of that time is
ours. Every internal sprint has latency we control. So the correct order is *not* easiest
first; it is **longest-pole first, even when the longest pole is a five-minute act.**

The second rule was **rulings before sweeps** — and both vocabulary rulings it named
have since landed. `G-0`/`G-0b` were ruled 2026-07-29
(`00_THE_FOUNDATION.md:85,88-98`) and `§5.1` was signed 2026-07-31
(`11_UPLINK/50_AUDITS_AND_EXECUTIONS/193_FIVE_RULINGS_SIGNED_2026_07_31.md` §Q1).
No remaining open ruling changes vocabulary corpus-wide, so the later sweeps are no
longer gated on this sprint. This paragraph remains as evidence of the drift it corrects.

---

## HISTORICAL SPRINT 1 · Invitation-first sequence superseded — do not execute

The v1 invitation premise is obsolete. The current v4 hash set has an
internally verified acyclic manifest binding and provenance firewall, but the registry remains
blocked on the complete review materials bundle, conflict and reviewer-scope
forms, compensation terms, publication permission, and an applicability
determination. Version 4 accepts no local owner or external evidence for those
rows; a later route requires a reviewed successor schema and independent
verification boundary. The live sequence is owned by
`../00_META/00_CONTACT_LIMITED_COMPLETION_ROADMAP_2026_08_01.md`.

- **Current pre-contact exit:** the six remaining material/human/owner registry
  prerequisites carry real custody; the technical manifest binding is already
  separately bound and does not make contact ready.
- **Later contact event:** an invitation is sent to a named qualified person and
  only that event is receipted; a reply remains theirs.
- **Cannot be delegated to an internal review.** The protocol: *"AI or
  project-agent review is useful internal search but does not satisfy this
  external gate."*

---

## SPRINT 2 · The residual rulings · *owner sitting, one session*

The two rulings that made this a vocabulary gate have landed. What remains here is
residue, and the later internal sprints may start without it.

| ruling | the decision | blocks |
|---|---|---|
| ~~`§5.1`~~ **RULED** | `√2` **is** a number in `ℝ` **and** is not a finite word over `{S, ι}`; both clauses must travel together and bare *"not a number"* is banned. Signed 2026-07-31 — `11_UPLINK/50_AUDITS_AND_EXECUTIONS/193_FIVE_RULINGS_SIGNED_2026_07_31.md` §Q1 | every page that says "number" |
| ~~`G-0` / `G-0b`~~ **RULED 2026-07-29** | Neither base is seated over the other; routing decides which applies. Exit B-ii, the fourth posit `B4`. Primary: `11_UPLINK/50_AUDITS_AND_EXECUTIONS/185_SECTION_5_2_RULED_AND_F_EQUALS_MA_2026_07_30.md`; consequence signed in `193_*` §Q2 | nothing — it no longer blocks |
| receipt disposition rule | renumber, or add `superseded_by:`? | sprint 4 |
| ~~undeclared-route rule~~ **RULED** | Four routes DECLARED-PROVISIONAL, `/offline/` infrastructure, seven frozen, `/historical-boundary/` unchanged. Signed 2026-07-31 (`193_*` §Q4), executed (`232_*`) | nothing — executed and deployed |
| `/dimensions/` crossings | may it keep showing five candidates when two are adjudicated failed? | one page |
| audit items 3, 11, 14, 28 | four residual calls, all listed in `README.md §4A` | closes the audit |

- **Exit condition:** one receipt per remaining row, each with a date.
- **Discipline:** a ruling that says *"stay as is, and here is why"* closes the item. Only
  silence leaves it open.

---

## SPRINT 3 · Prove the internal program is closable · *machine, half a session*

Before doing the sweeps, make the finish line reportable. Otherwise "done" is a feeling.

- Add `check_program_closed.py`: reports the six finite counts and **fails only when a
  count moves in the wrong direction**, so it is a ratchet rather than a deadline.
- Wire it into `gate.sh` (10 checkers).
- Mutation-test it in both directions, per standing practice.
- **Exit condition:** `bash 09_TOOLS/01_SCRIPTS/gate.sh` prints the remaining internal
  backlog as a number, every run.

---

## SPRINT 4 · Citation integrity · *91 items, one session with the rule from sprint 2*

Numeric citation is currently unsound: 91 numbers name more than one undeclared document,
and a citation can resolve to the wrong file and pass a checker. `r139` is the model to
copy; `r117` is the failure.

- Apply the sprint-2 rule mechanically; every touched file gets `superseded_by:` or a free
  number.
- Lower `AMBIGUOUS_BASELINE` as it falls — the checker already fails if the baseline is
  left slack, which is what stops this from stalling at 60.
- **Exit condition:** baseline at 0, or a ruled residue with a reason per remaining case.

---

## SPRINT 5 · The publication boundary · *40 routes, one session*

40 routes are declared neither current nor frozen, which means they carry retired claims
with no banner. `/halahala/` was the one genuinely exposed page and is fixed; the rest are
`noindex` or withheld, so this is hygiene, not emergency.

- Sort each into current / frozen / withheld / infrastructure-exempt per the sprint-2 rule.
- The blocker is known and real: declaring one current fails the parity contract on Titan
  infix, so most will land frozen — and the fence added on 2026-07-30 means a page *can*
  now state the identity if the coupling precedes it.
- **Exit condition:** zero routes in the undeclared tier; `check_public_semantic_parity`
  green.

---

## SPRINT 6 · The two unsurveyed folders · *04_AXIOLOGY, 06_ONTOLOGY, one session*

Audited by tag count only, never read claim-by-claim: 10 and 31 `[A]` sites. **An untagged
wrong claim in either is invisible to every checker the corpus owns.** This is the largest
remaining blind spot and the one most likely to hold something embarrassing.

- Read the substantive documents. Tier what is untiered. Record what is wrong.
- Expect to find defects; this session found four in already-audited material.
- **Exit condition:** both folders body-surveyed with a receipt, and every `[A]` site
  either verified or downgraded.

---

## SPRINT 7 · The 17 open claims · *one session, gated on sprints 2 and 6*

Each open row needs evidence, a narrowing, or a terminal verdict. Several will be closable
on paper once the rulings land; the rest are honestly contact-gated and should be *moved*
to that column rather than left ambiguous.

- **Exit condition:** every row either resolved, narrowed with a named weaker form, or
  explicitly reclassified as contact-gated. **Zero rows whose status is "we stopped
  thinking about it."**

---

## 2 · Then the program changes character, and does not end

When sprints 2–7 close, the board looks like this: nothing internal blocks anything, and
every remaining item needs a person outside this project. **That is contact-limited, and
it is the terminal state of the plan.**

What happens after is a different activity and should be called one:

- **from authoring to answering.** The work becomes: receive a verdict, file it verbatim,
  respond separately, update or retract. `/record/` already has the shape for it.
- **the first reply will probably hurt**, and the ledger is built for that. 29 outcomes,
  18 against, all kept. A verdict that costs a claim is the system working.
- **no sprint plan covers it**, because its pace is not ours.

---

## 3 · What this plan refuses to promise

- **It does not promise the framework is true**, and closing every sprint would not
  bear on that. `00_ESTABLISHED` stays short.
- **It does not promise the internal work matters.** On the framework's own conjunctive
  law, both factors must be non-zero and the deficient one binds, so with contact at
  zero sprints 2–7 could all close and the score would not move. **Only Sprint 1 can
  move it, which is why it is Sprint 1.**
- **It sets no dates.** Sizes are honest ("one session"); dates would be invented.
- **It is not ratified.** Nothing here is a commitment until an owner says so.

**This plan's own kill:** if all seven sprints close and the project still describes itself
as making progress without a single returned outcome, the plan failed at the only thing it
was for — and this paragraph is the evidence it was warned.

•   ⊙   ○ — *finish the inside; the outside is not ours to finish.*
