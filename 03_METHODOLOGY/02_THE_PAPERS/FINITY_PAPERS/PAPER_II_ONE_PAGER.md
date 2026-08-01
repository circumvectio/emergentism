---
title: "Three statuses, not one word — a one-pager on division by zero"
status: "DRAFT — sketch for distribution; companion to PAPER_II"
date: 2026-07-30
evidence_tier: "[A] each category stated with its own kill; needs no framework"
parents:
  - PAPER_II_DIVISION_BY_ZERO_AS_CATEGORY_CORRECTION.md
---

# Three statuses, not one word

> A working mathematician reads "undefined" and asks *which* of three. The answer
> changes what to do.

Mathematics uses one word — "undefined" — for three genuinely different situations.
The distinction costs nothing to make and is useful the moment it is named. None
of the three requires anything outside standard mathematics; none depends on
spheres, charts, or any other framework. It is a discipline of typing, not a
thesis.

---

## 1 · The three statuses

### 1.1 NO SUCH ELEMENT `[A]`

`a / 0` for any `a`.

In a field, `0` has no multiplicative inverse. The expression `a / 0` denotes
`a · 0⁻¹`, but `0⁻¹` does not exist; the term is well-formed but refers to
nothing. **The expression names an element that the structure does not contain.**

*Kill.* Exhibit a field in which `0` has a multiplicative inverse, or show that
`a / 0` has a value that any textbook algebra would accept.

### 1.2 INADMISSIBLE TERM `[A]`

The attempted product of zero and infinity in a context where infinity is not
an element of the structure.

If the domain is `ℝ` and infinity is not an element of `ℝ`, the expression is
not well-formed at all. The grammar never produced it. The same applies to an
attempted multiplication of two Titan *seats* (boundary roles): TitanFrame has
no multiplication operation. **The expression fails the type check before
evaluation.**

*Kill.* Exhibit a context in which the same term is both a well-formed product
*and* a well-defined value with the usual arithmetic properties.

### 1.3 INDETERMINATE FORM `[A]`

`0 / 0`, `∞ / ∞`, `0 · ∞`, `∞ − ∞`, `1^∞`, `0^0`, `∞^0`.

Each is a limit. Two functions that agree at the limit in two different ways can
make any of these approach any real number — or diverge. **The expression has a
type-correct value in a context of *approach*, but the value depends on the
path.** A limit is an instruction to compute something more specific; it is not
itself a value.

*Kill.* Exhibit a context in which all paths to the limit agree on a single
value, *or* exhibit a case where the limit is uniquely defined without a
declared approach. (The exponential limit `lim_{x→0} (1+x)^{1/x} = e` is
indeterminate in form `1^∞` but uniquely defined by the standard approach.)

---

## 2 · The collapses, named

The three statuses collapse into one word in the literature and in undergraduate
teaching. Each collapse is a real loss:

| Status | What is lost by calling it "undefined" |
|---|---|
| NO SUCH ELEMENT | The theorem that no value exists. *Undefined* suggests a hole to be filled. |
| INADMISSIBLE TERM | The type error. *Undefined* suggests the expression was at least *asked*; it was not. |
| INDETERMINATE FORM | The path-dependence. *Undefined* suggests a single status; there is a family, indexed by approach. |

Conflating the three is what lets the standard puzzles ("what is `0/0`?") be
asked as if they had one answer. They do not.

---

## 3 · A discipline

In any writing that handles boundary expressions:

1. **Name the domain first.** Field, projective, meromorphic, wheel, or other.
2. **Name the type.** Element, seat, limit, or other.
3. **State the status of the expression in one of the three words above.** Add a
   one-line reason.

Three short sentences. Most boundary-confusion in textbooks and online sources
would be removed by them.

---

## 4 · The thing this is not

This is not a thesis. The three statuses are taught in undergraduate analysis
under different names ("undefined", "not well-defined", "indeterminate"). What
this one-pager adds is the *typing discipline* — refusing to let the three be
called by one word. The discipline is portable; it does not require any
particular framework, philosophy, or ontology. A working mathematician would
recognise the distinction as useful immediately.

---

## 5 · Companion

`PAPER_II_DIVISION_BY_ZERO_AS_CATEGORY_CORRECTION.md` carries the full treatment
with citations. This one-pager is the distribution form.

*Suggested use.* As a 5-minute pre-read for a non-specialist collaborator, a
classroom aside, or a footnote in a paper that needs the distinction without
the apparatus.
