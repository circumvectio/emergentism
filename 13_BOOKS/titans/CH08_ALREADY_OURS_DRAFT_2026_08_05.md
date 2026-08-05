---
title: "Chapter 8 — Everything We Found Was Already Ours (trade edition draft)"
status: "DRAFT 1 — unratified. The attribution chapter. Written from the adversarial prior-art sweep of 2026-08-05; dates and losses verified against sources before drafting."
date: 2026-08-05
evidence_tier: "[D] draft prose. Every attribution verified: Stern 1858 / Brocot 1861 / Calkin-Wilf 2000 (Amer. Math. Monthly 107(4) 360-363), earlier as the Raney tree 1996; Setzer 1997 / Carlström 2004 for wheels, with 0x=0 as the law surrendered; Euclid Elements VII on the unit."
owner: "13_BOOKS workshop. Projection only."
strip_test: "PASSES — no Emergentism-specific vocabulary in the body."
parents:
  - 00_TRADE_EDITION_PROPOSAL_2026_08_05.md
  - CH04_FOUR_STATUSES_DRAFT_2026_08_05.md
  - CH05_CONTINUATION_WITHOUT_ORIENTATION_DRAFT_2026_08_05.md
  - ../../11_UPLINK/50_AUDITS_AND_EXECUTIONS/242_G2_PROVED_AND_FOUND_TO_BE_PRIOR_ART_2026_08_05.md
---

# Everything We Found Was Already Ours

At some point you have to go and look.

The looking is the part that rarely gets reported. Everyone who has spent years
on an idea knows the private arithmetic: the more time you have put in, the more
expensive it becomes to discover that someone did it first, and the easier it
becomes to not quite get round to checking. The literature is large. The search
terms are never the ones the other person used. There is always something more
urgent.

So this chapter is the report. We went looking for what in this book was ours.
Here is what came back.

---

## The ladder from one

The idea: start with 1. Allow yourself two moves — add one, or flip the number
over. Every positive fraction you could ever want turns out to be reachable by
some finite sequence of those two moves, and each one is reachable by exactly one
sequence if you tidy up the obvious redundancies. It is a rather beautiful way to
see the fractions: not as a set handed to you, but as everything two operations
can build out of a single object.

It is also Euclid's algorithm, which is about 2,300 years old, wearing different
clothes.

The arrangement of the fractions into a tree grown this way was published by
Moritz Stern, a number theorist, in 1858. It was found independently three years
later by Achille Brocot — who was not a mathematician but a French clockmaker,
and who worked it out because he needed to find gear ratios that were close to a
desired value but buildable with a reasonable number of teeth. There is a version
of this structure sitting inside every mechanical clock of a certain vintage,
put there by a man solving a manufacturing problem.

A second, related tree was published by Neil Calkin and Herbert Wilf in 2000, in
a paper called "Recounting the Rationals," which is three pages long and worth
reading. And here is the detail I enjoy most: that tree already had an earlier
appearance in the 1990s under a different name, and something recognisably like
the construction turns up in Kepler in 1619, in a book about the harmony of the
world, while he was thinking about musical intervals and planetary orbits.

So the count is: us, Calkin and Wilf, an earlier naming in the nineties, a
clockmaker in 1861, a number theorist in 1858, Kepler in 1619, and Euclid. We
were seventh at best, and the queue was not close.

**What it cost:** the claim that this was a new way to found arithmetic. It is
not. **What it gave:** everything in the description above is now true with a
citation attached, which means a reader can check it, which means it can be
used.

---

## The centre at one

The idea: flipping a number over — one over x — swaps the very small with the
very large, and leaves exactly one positive number untouched. One is where the
mirror stands.

This is true, it is easy to prove, and it is roughly two centuries old. It lives
inside the study of the projective line and the sphere named after Riemann, in
work running through Möbius and Cayley in the 1800s. In that setting the three
points zero, one, and infinity are not merely *a* natural trio; they are *the*
natural trio, in a precise sense — the transformations of that space can carry
any three distinct points to those three, and in exactly one way. If you are
going to normalise anything, those are the three you normalise to. Every
mathematician who works there knows it the way a pianist knows where middle C is.

There is a particular change of coordinates that turns the flip into a simple
reflection and lays the whole positive line out between minus one and plus one,
with one at the centre. It is called the Cayley transform. It is in textbooks.

**What it cost:** the claim that the centrality of one was a find. **What it
gave:** the ability to say precisely *why* one is central, rather than
gesturing, and to point at where the reader can verify it.

---

## Endless, but never finished

The idea: there is a difference between a process that can always take another
step and a completed infinite thing, and much confusion comes from treating the
first as though it were the second.

Aristotle, in the *Physics*, distinguishes exactly this, and comes down on the
side that the infinite exists only as a process and never as a finished totality.
Gauss objected in a letter in 1831 to the use of an infinite quantity as a
completed thing, calling it something never permitted in mathematics. Hilbert
gave a famous lecture in the 1920s arguing that the infinite is an idea of reason
with no counterpart anywhere in reality. There is a live modern literature that
formalises the distinction carefully.

Our contribution to this was to notice it independently, which is not a
contribution.

**What it cost:** any claim to have identified the distinction. **What it gave:**
a place in a two-thousand-year-old conversation instead of outside it, and the
knowledge that the distinction has survived that long because it keeps being
needed.

---

## The one that cannot be gathered

This one is the most interesting, because we had reached for the wrong relative.

The idea: there is something at the bottom — or the outside — to which counting
does not apply. Not something with a very large count. Something for which the
question of a count is not a well-formed question.

We had been explaining this by pointing at uncountability: at collections too
large to put in a queue, the ones from Chapter 4. That was a mistake, and it was
pointed out to us in a way that was hard to argue with. *Uncountable* is defined
by counting — it means precisely that no queue indexed by the counting numbers
catches everything. It is the most counting-dependent idea available. Using it as
a picture of "counting does not apply here" is using the wrong picture.

The right relative was Cantor's, and it is not the one that made him famous.
Alongside the sizes of infinity that he could compare and arrange, Cantor
separated off collections he considered inconsistent — things like the collection
of all ordinal numbers — which cannot be gathered into a completed whole at all,
and to which size does not apply. He called this the absolute infinite, wrote
about it in explicitly theological terms, and kept it firmly apart from the
transfinite numbers he was doing arithmetic with. Modern set theory keeps the
distinction under a different name and without the theology: some collections are
sets, and some are too big to be, and the second kind does not get a size.

That is the neighbour we should have been pointing at all along. It is a better
fit, it is more precise, and it has been sitting there since the 1890s.

**What it cost:** a paragraph we had been rather pleased with. **What it gave:**
a correction, which is worth more, and the observation that Cantor also felt the
need to keep an unnameable thing outside the system he had built — which is at
least interesting company.

---

## Zero and infinity as roles, not numbers

The idea from Chapter 7: that zero and infinity behave less like numbers and more
like the edges of what the numbers can do — that trying to multiply them together
is not a hard sum but a category mistake.

There is a worked-out algebraic theory of exactly this. It is called wheel
theory, proposed by Anton Setzer in 1997 and developed in detail by Jesper
Carlström in the 2000s. A wheel extends an ordinary number system so that
division always works, including division by zero. It brings zero and infinity in
as full citizens, and it adds a further element to absorb the cases that would
otherwise be contradictory.

And it does something that I want to hold up, because it is the standard this
book should be judged against. **It publishes the bill.** You cannot get total
division for free, and wheel theory says exactly what you surrender to get it:
the rule that anything times zero is zero stops holding in general. That is a
large thing to give up, and the theory states it plainly, up front, as part of
the definition.

Compare our position honestly. We declared that these boundaries were not
operands — that you may not multiply them — and paid nothing for the declaration,
because a declaration is free. Wheel theory went the other way, made them
operands, and paid in cash. Both are legitimate moves. Only one of them has an
itemised receipt, and it is not ours.

**What it cost:** the sense that treating these as roles rather than values was an
insight. It is a design choice, with a known alternative that costs more and
delivers more. **What it gave:** a way to explain the choice as a choice.

---

## The unit is not a number

Even this is Euclid. In the *Elements*, Book VII opens by defining a unit as that
by which each existing thing is called one, and then defines a number as a
multitude composed of units. On that reading one is not itself a number; it is
what numbers are made of.

We arrived at a version of this and thought it was strange and modern. It is the
oldest thing in the chapter.

---

## What was left

After all of that, one thing survived the search, and I want to be precise about
how small it is.

Nothing in mathematics requires anyone to *declare* the boundary they are
answerable to. The mathematics of approaching a limit is complete, exact, and
ancient; it tells you what it means for a process to be headed somewhere. It does
not tell you to announce, in advance and in public, which somewhere you have
chosen and how anyone could check whether you got there. It does not need to,
because inside mathematics the declaration is compulsory anyway — as Chapter 5
put it, the notation will not let you skip it.

Outside mathematics, nothing enforces it, and that is where the boat went in
circles.

So the surviving piece is not a theorem, and it is not new mathematics, and it
was never going to be. It is a practice: state the finite, checkable, revisable
boundary that your process answers to, before you start, where the system can see
it. That is Chapter 9, and it is the whole of what this book is offering that
somebody else did not already have.

---

## Why any of this is worth telling you

Two reasons, and the second is the real one.

The first is that you should not trust an author who has not done this. A claim
of novelty from someone who never seriously looked is worth nothing, and the
looking is unpleasant enough that its absence is the default. If this chapter did
not exist, you would have no way to distinguish this book from the large number
of books that are confidently reinventing something.

The second reason is that **being already-known is the normal condition of a real
idea, and it is what happened to zero.**

Nobody invented zero. A placeholder for an empty column shows up in Babylonian
records long before anyone treated it as a number in its own right. Several
cultures arrived at parts of it. Brahmagupta's contribution in the seventh
century was not the symbol; it was writing down rules for what you could do with
it — and even he got the division case wrong, which took centuries more to sort
out. Zero did not enter the world as a discovery. It entered as a name, a set of
rules, and eventually a habit, and it took about a thousand years.

An idea that genuinely no one had ever had before is more likely to be wrong than
important. The useful things tend to be lying around in several places at once,
in pieces, each piece owned by a field that has no reason to hand it to anyone
else. Finding that your idea was already there in six forms is not a refutation.
It is the ordinary evidence that the idea is about something.

What is left to do, in that case, is not to claim it. It is to name it, give it
rules, and get it out of the building it was born in.

---

## Sources for this chapter

- Euclid, *Elements*, Book VII, definitions 1–2 — the unit and number.
- Moritz Stern (1858) and Achille Brocot (1861) — the tree, independently; Brocot's motivation was gear ratios.
- Neil Calkin and Herbert Wilf, ["Recounting the Rationals"](https://www2.math.upenn.edu/~wilf/website/recounting.pdf), *American Mathematical Monthly* 107 (2000), 360–363; the same tree appears earlier as the Raney tree (Berstel and de Luca, 1996), and a related construction in Kepler, *Harmonices Mundi* (1619).
- Möbius, Cayley, Riemann — the projective line and sphere; the three-point normalisation and the Cayley transform are standard textbook material.
- Aristotle, *Physics* III; Gauss, letter to Schumacher (1831); Hilbert, "On the Infinite" (1925–26).
- Georg Cantor — the absolute infinite and inconsistent multiplicities, distinguished from the transfinite numbers.
- Anton Setzer (1997) and Jesper Carlström, ["Wheels — On Division by Zero"](https://www2.math.su.se/reports/2001/11/2001-11.pdf) — total division, and the surrender of `0x = 0`.

---

*Draft 1. Every attribution in this chapter was checked against a source before
the chapter was written, not after. Where a date or figure could not be confirmed,
it was cut rather than softened.*
