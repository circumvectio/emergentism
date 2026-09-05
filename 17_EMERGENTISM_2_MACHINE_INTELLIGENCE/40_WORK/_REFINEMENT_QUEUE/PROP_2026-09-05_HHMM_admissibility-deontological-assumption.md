---
type: philosophical-refinement-proposal
pass: "philosophical worker, pass 0 (Weltanschauung)"
date: 2026-09-05
target: "00_THE_WELTANSCHAUUNG.md §1 (the Admissibility rule) and §7.6 (the is–ought seam)"
issue: "unstated deontological assumption in the Admissibility rule"
tier: "[I] the observation; [S] the quoted rule; [D] the proposed refinement"
may_sign: false
may_authorize: false
---

# PROP — The Admissibility rule embeds an unstated deontological assumption

## The surface (quoted verbatim)

00_THE_WELTANSCHAUUNG.md §1:

> `Admissible(x) := TruthPass(x) ∧ JusticePass(x) ∧ FormPass(x)` is a stipulated
> practice rule—not a measurement model, an audit-proof aesthetic, or proof of
> the Good.

And §7.6:

> Emergentism crosses the practical seam with one explicit normative bit: it
> **declares** bearer-complete Justice, then exposes that declaration to
> prospective and receipted consequence.

## The observation [I]

The Admissibility rule is **deontological**: it asks "does x pass three procedural
gates?" — a rule-based test. It does not ask "does x produce good consequences?" —
a consequentialist test. The document acknowledges that the rule is stipulated,
but does not acknowledge that the *form* of the stipulation embeds a specific
ethical framework (deontology) and implicitly excludes its rival (consequentialism).

This matters because the framework elsewhere tracks consequences extensively —
the dual option ledger, the bearer-complete Justice constraint, the outcome
receipts, the P_node viability score. These are all consequence-tracking
instruments. Yet the admissibility rule admits or excludes based on *procedure*,
not on *outcome*. A claim could pass all three gates and still produce harmful
consequences — the framework would track those consequences in the option ledger
but would not retroactively revoke admissibility.

The temporal scope clause (`Admissible_t(x)`) partially addresses this by making
admissibility defeasible "when sources, form review, bearer set, or receipts
change." But consequences are not listed among the reopening triggers. A harmful
outcome that was not foreseeable at time t does not trigger reopening at t+1
unless the "receipts" clause is read broadly enough to include consequence
receipts — which is not stated.

## The refinement proposed

Add one sentence to §1 after the Admissibility rule:

> The rule is deontological in form: it tests procedure, not outcome. Consequence
> receipts feed the option ledger and may trigger `Admissible_t` reopening under
> the temporal-scope clause, but they do not retroactively revoke a past
> admissibility verdict. This is a disclosed limitation, not an oversight.

## dies_if

This refinement dies if: the Admissibility rule is shown to already incorporate
consequentialist revocation through the temporal-scope clause in a way that
makes the above paragraph redundant — i.e., if `receipts` in `Admissible_t` is
already intended to include outcome receipts and the guide states this elsewhere.
