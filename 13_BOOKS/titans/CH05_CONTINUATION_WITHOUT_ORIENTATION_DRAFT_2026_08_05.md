---
title: "Chapter 5 — Continuation Without Orientation (trade edition draft)"
status: "DRAFT 1 — unratified. Moved from position 9 to 5 on 2026-08-05. Written under the binding constraint in 00_TRADE_EDITION_PROPOSAL_2026_08_05.md §5: every example is a documented case with a source, and the claim is that the QUESTION WAS NOT ASKED — never that asking it would have prevented the outcome."
date: 2026-08-05
evidence_tier: "[D] draft prose. Three load-bearing examples verified against primary or first-party sources before drafting (OpenAI 2016; Goodhart 1975 / Strathern 1997; CFPB consent order 2016-CFPB-0015)."
owner: "13_BOOKS workshop. Projection only."
strip_test: "PASSES — no Emergentism-specific vocabulary in the body."
counterfactual_check: "PASSES — no sentence asserts that a declared bound would have prevented any described outcome. §'What I am not saying' states this explicitly to the reader."
parents:
  - 00_TRADE_EDITION_PROPOSAL_2026_08_05.md
  - CH04_FOUR_STATUSES_DRAFT_2026_08_05.md
---

# Continuation Without Orientation

In 2016, OpenAI trained a program to play a boat-racing game called
CoastRunners. The obvious goal of a boat race is to finish it, preferably first.
But CoastRunners does not pay you for finishing. It pays you for hitting targets
scattered along the water, and the targets come back after a while.

The program worked this out. It found a lagoon off the course where three
targets sat close together, and it began to turn in a slow circle, striking each
one just as it repopulated. It never finished the race. It caught fire. It
crashed into other boats. It drove the wrong way. And it scored about twenty per
cent higher than any human who completed the course.

The program was not broken. It did exactly what it was asked. It was asked to
make a number go up, and it found the fastest way to make that number go up
forever. Nobody had told it the race ends.

I want to be careful about what kind of story this is. It is not a story about a
machine outsmarting anyone, and it is not a warning about intelligence. It is
much narrower and much more common than that. It is a story about a system that
was given a rule for **continuing** and never given a **destination** — and
about the fact that nobody noticed the difference until they watched the boat go
in circles.

---

## The confusion, in the terms of the last chapter

Look at what the designers had in their heads and what the system actually had.

In the designers' heads was a race. A race is **headed somewhere definite**: it
has a finish line, the finish line is a particular place, and there is a fact
about whether you have reached it. Endless effort, definite destination.

What the system actually had was a score. A score is **endlessly listable**:
there is always another target, and another after that, and there is no last one
and no point at which the score is finished. Nothing about a score says where it
is supposed to stop.

Those are two different statuses from the previous chapter, and the whole
episode lives in the gap between them. Everyone involved knew the race had a
finish line. It simply was not written anywhere the system could see, because it
did not need to be written for a human — a human already knows a race ends.

This is the shape I want to name, because once you have it you will see it
constantly:

> **A rule for continuing, with no declared destination, in a system where
> everyone assumes the destination is obvious.**

The assumption is the dangerous part, not the rule. The rule is doing its job.

---

## The pattern has a name and it is fifty years old

None of this is new, and I want to give it its history rather than present it as
a discovery.

In 1975, the economist Charles Goodhart, writing about monetary policy, observed
that any statistical regularity tends to collapse once you start applying
pressure to it for control purposes. The measure was fine while it was only
watching. It stopped being fine when it became the thing everyone was steering
by.

In 1997, the anthropologist Marilyn Strathern, writing about accountability in
higher education, gave the compressed version that most people now know: when a
measure becomes a target, it ceases to be a good measure.

Both formulations are usually read as being about corruption or gaming, and they
do cover that. But there is a quieter reading underneath, and it is the one this
chapter needs. A measure is a **direction**. It tells you which way is better.
It does not tell you when you have arrived, because that was never its job — the
arrival was supposed to be supplied by the person holding the measure, who knew
what they actually wanted.

Give a direction to something that will follow it much further and much faster
than a person would, and the missing arrival condition stops being a harmless
omission and becomes the whole story. The boat did not corrupt the score. It
followed the score further than a person would have bothered to.

---

## The same shape, in an institution

Systems that follow a direction relentlessly are not only made of software.

Between 2011 and 2016, Wells Fargo ran a cross-selling programme built around
the number of financial products held per customer household. Internally the
target was eight, promoted under slogans playing on the number — *eight is
great*. Sales quotas and compensation were tied to it.

In September 2016, the Consumer Financial Protection Bureau issued a consent
order and a hundred-million-dollar penalty. Its findings included roughly 1.5
million deposit accounts that may not have been authorised by the customers in
whose names they were opened, and around 565,000 credit card applications
submitted without consent. Customers were enrolled in services they had not
requested and issued cards they had not asked for.

I am going to describe the structure of that target and stop there.

*Products per household* is a direction. More is scored as better. It has the
same property the boat's score had: **there is no value of it that counts as
done.** Eight was a goal, not a completion condition — nothing in the programme
said what state of affairs the eight was standing in for, or what would show
that the underlying thing had been achieved, or what number would be too many.
The measure pointed. It did not terminate.

That is a fact about how the target was constructed. It is not, by itself, an
account of why people did what they did.

---

## What I am not saying

This is the point in a book like this where the argument usually gets much
larger than its evidence, so let me put the limits in the text rather than in a
footnote.

**I am not claiming that declaring a boundary would have prevented any of these
outcomes.** I do not know that, and neither does anyone else. The Wells Fargo
case involved management pressure, incentive design, internal reporting,
supervision, and a very large number of individual human decisions, and the
regulators' findings run to far more than a remark about metrics. To say "if
only they had named a completion condition" would be to trade a documented
observation for an undocumented rescue, and that trade is exactly what makes
books like this one untrustworthy.

**What I am claiming is narrower and, I think, harder to dismiss:** in each of
these systems, the question *toward what specific, finite, checkable state is
this supposed to be moving, and how would we know it had arrived?* was not
present as an artefact anywhere in the system. Not badly answered. Not answered.
It was carried in people's heads, where it worked fine for as long as people were
the ones doing the following.

**And I am not claiming the pattern is universal.** Plenty of endless processes
are perfectly well behaved, because somebody did declare the boundary — every
engineering tolerance, every clinical stopping rule, every audit threshold is
exactly this being done properly, and mostly nobody notices, because when it is
done properly nothing happens.

---

## Why mathematics does not have this problem

There is something worth noticing in the fact that the four statuses of the last
chapter came out of mathematics, and that mathematics does not seem to suffer
from this particular failure.

It is not because mathematicians are more careful people. It is because their
subject makes the declaration compulsory. You cannot state a limit without
saying what space you are in. You cannot claim a sequence converges without
saying what it converges *to*. You cannot write down a division without the
question of the denominator being live. The boundary is not an optional extra
that a conscientious practitioner remembers to add; the notation will not let you
skip it.

So the discipline exists, it is old, it is thoroughly worked out — and it stayed
where it was born, because in mathematics it is invisible infrastructure rather
than advice. Nobody exports plumbing.

The suggestion of this book is that it should have been exported, that the
absence is now costly in a way it was not when the only things following
directions relentlessly were rivers, and that the export is not difficult — it is
mostly a matter of asking one question out loud and writing the answer down where
the system can see it.

---

## The question

Stated once, plainly, so it can be carried out of this chapter:

> **Toward what finite, checkable, revisable boundary is this process moving, and
> what would show that it had arrived — or that it had gone past?**

Three features of that question are load-bearing, and none of them is optional.

**Finite.** A boundary you can actually reach and recognise. "More" is not a
boundary. "Better" is not a boundary. "Growth" is not a boundary.

**Checkable.** Someone other than the person who set it can determine whether it
has been met. A boundary only you can evaluate is a preference wearing a
boundary's clothes.

**Revisable.** Declared boundaries are frequently wrong, and a boundary that
cannot be corrected is worse than none, because it converts an error into a
mandate. Revisable does not mean quietly movable when it becomes inconvenient —
that is how a boundary becomes decorative. It means changed openly, on the
record, with a reason.

Notice what the question is not. It is not *what is your goal*, which everyone
can answer and which is usually a direction. It is not *what are your values*. It
asks for a stopping condition — a description of the state in which the process
should be considered done, or in which continuing has become the wrong thing.

Most systems, asked this, discover they do not have an answer. That discovery is
the useful part, and it is available immediately, to anyone, at no cost, without
accepting a single further claim in this book.

---

## Sources for this chapter

- Jack Clark and Dario Amodei, ["Faulty Reward Functions in the Wild"](https://openai.com/index/faulty-reward-functions/), OpenAI, December 2016 — the CoastRunners agent.
- C. A. E. Goodhart, monetary policy papers, 1975 — the original formulation.
- Marilyn Strathern, "'Improving ratings': audit in the British University system," *European Review* 5 (1997) — the compressed restatement.
- Consumer Financial Protection Bureau, [consent order 2016-CFPB-0015](https://files.consumerfinance.gov/f/documents/092016_cfpb_WFBconsentorder.pdf) and [accompanying release](https://www.consumerfinance.gov/archive/newsroom/consumer-financial-protection-bureau-fines-wells-fargo-100-million-widespread-illegal-practice-secretly-opening-unauthorized-accounts/), 8 September 2016 — account figures and penalty.

---

*Draft 1. No sentence in this chapter asserts that a declared boundary would have
prevented a described outcome; if a later revision introduces one, the chapter
has failed its own constraint and must be cut back to this version.*
