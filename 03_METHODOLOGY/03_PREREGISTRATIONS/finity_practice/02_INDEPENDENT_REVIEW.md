---
title: "FPE-REVIEW-01 — Independent Review Packet"
type: external-review-packet
gate_id: FPE-REVIEW-01
version: 1.3.0-draft
date: 2026-08-02
status: "TYPED DRAFT · CONTACT DEFERRED · NO REVIEWER ENGAGED · NO REVIEW EXISTS"
evidence_tier: "[D] review design; external findings remain absent"
semantic_authority: none
source_claims: [FIN01-01, FIN01-02]
---

# FPE-REVIEW-01 — Independent review

## Purpose

Invite qualified outsiders to find prior art, false distinctions, unfair
comparators, hidden author degrees of freedom, measurement defects, harms,
coercive language, and overclaiming before participant contact.

Review is a sensor, not a truth certificate. A favorable review establishes
only that a named person examined named materials within declared competence.
It is not endorsement, consensus, safety, efficacy, or replication.

## Independence contract

For this gate, an independent reviewer must disclose and normally lack:

- authorship or editing of Emergentism, the Finity Card, or these packets;
- employment, governance, investment, adoption, publication, or reputational
  stakes tied to a favorable result;
- a close family, intimate, supervisory, dependent, or client relationship with
  the authors or study team; and
- prior access to other reviewers' verdicts before submitting their own.

Fixed, fair compensation is allowed when it is disclosed and does not depend on
tone, recommendation, publication, or outcome. Ideological disagreement is not
a conflict; hidden material dependence is. AI or project-agent review is useful
internal search but does not satisfy this external gate.

Seek separate competence in decision/behavioral science, research methods and
statistics, human-subject ethics/privacy, and plain-language/accessibility.
One reviewer may cover more than one area, but no global vote or average score
may hide an unreviewed specialty or a fatal minority objection.

## Same-hash review bundle

Give every reviewer the same frozen bundle:

1. `01_TELEOLOGY/04_THE_LIVED_COMPASS.md` §3B;
2. `00_META/claim_cards/finity_practice.yaml` (`FIN01-01`, `FIN01-02`);
3. `00_META/ADEQUACY_DOCKETS.yaml` (A3 and A5);
4. the immutable `REVIEW_REGISTRY_SNAPSHOT_vN.json`, the binding contract, and
   all three packet files in this folder;
5. the exact four arm texts, consent draft, rubric, analysis plan, safety plan,
   data dictionary, retention schedule, and intended preregistration target;
6. the public claims and barred-inference list; and
7. this known-weakness statement: the authors designed the practice, the
   comparator, the outcome rubric, and the initial public language.

The invitation records every file hash. A material amendment requires a new
version and a new review; an older review cannot silently cover changed text.

The complete set named in item 5 is an explicit, currently missing
`complete_review_materials_bundle` prerequisite in the live registry. It cannot
be inferred from the technical bundle binding: each listed material must exist,
be hash-bound together, and carry the required custody before that prerequisite
can be satisfied.

### Acyclic lifecycle binding

The live `GATE_REGISTRY.json` records mutable execution evidence. It cannot be
inside the frozen file set if it must also point to the frozen manifest: that
would require the manifest to hash an artifact whose content includes the
manifest's own hash. Each `REVIEW_BUNDLE_vN` therefore carries a versioned,
immutable review-registry snapshot instead. The snapshot is a deterministic
allow-list projection of the static review contract; it excludes external
state, prerequisite evidence, execution state, and the manifest back-reference.

The current registry binds the manifest and a local binding receipt *after* the
manifest freezes. The binding contract specifies the graph and the checker
rejects a raw registry, manifest self-reference, or binding-receipt inclusion in
the bundle. This repair proves only that the packet's custody graph is acyclic.
It does not fill the missing complete review materials, forms, terms,
permission, applicability determination, reviewer, contact, or review.

### Prerequisite-provenance firewall

Version 4 freezes a second, narrower contract: every review prerequisite has a
declared evidence kind, and the owner authority for `D-OWNER-03` is frozen as
`unset`. The checker therefore rejects a generic local file, a blank template,
an internal agent assertion, or a merely hash-matching receipt as a substitute
for a materials bundle, owner attestation, external declaration, or
applicability determination.

This is not an owner selection. It records no principal, reviewer, contact,
permission, compensation, ethics determination, or outcome. Version 4 accepts
no local owner or external evidence at all: a later selection changes the
frozen authority context and requires a new packet version, reviewed successor
schema, and independent verification boundary before any corresponding evidence
can be considered. A local JSON file can bind bytes; it cannot authenticate a
person, prove consent or independence, establish ethics approval, or authorize
contact.

## Reviewer questions

Answer in ordinary disciplinary language; Emergentist vocabulary is optional.

### A. Claim and prior art

1. State the strongest defensible version of `FIN01-01` and `FIN01-02`.
2. Which ordinary methods already contain each component or the whole bundle?
3. Does any claimed distinction disappear under clearer standard terminology?
4. What is actually novel, merely packaged, unassessed, or already known?

### B. Comparator and identification

5. Is the ordinary worksheet a strongest fair rival with equal dose, support,
   readability, response capacity, time, examples, and follow-up?
6. Do `F−U` and `U−C` identify brand and prompt organization? Does `C−M` support
   only assignment to one ordinary record versus heterogeneous usual practice,
   or can demand, expectancy, familiarity, contamination, and prior method
   structure absorb any of these contrasts?
7. Can the outcomes distinguish a better record from a better decision?

### C. Measurement and analysis

8. Are correction and critical omissions valid, reliable, and separately
   interpretable? Does the rubric reward target vocabulary or author values?
9. Are allocation, masking, multiplicity, missingness, attrition, delayed harms,
   sample-size assumptions, deviations, and null/equivalence routes adequate?
10. What result would kill or narrow the comparative claim?

### D. Ethics, power, and custody

11. Can any participant or nonparticipant bear more than minimal risk?
12. Are consent, withdrawal, compensation, privacy, cultural/religious
    sensitivity, complaint, adverse-event, repair, and ethics-review routes fit?
13. Could branding, founder prestige, worldview language, or investigator
    allegiance pressure assent or favorable answers?
14. What data should not be collected, retained, quoted, or made public?

### E. Public inference

15. Which exact sentences would a favorable, null, mixed, or harmful result
    permit? Which remain forbidden regardless of outcome?
16. What is the strongest unresolved objection after your review?

## Verdict form

For each numbered question, record:

```text
reviewer_scope:
conflicts_and_compensation:
materials_and_hashes:
finding:
evidence_or_prior_art:
severity: note | revise-before-freeze | blocker | fatal-to-claim | unassessed
required_change_or_test:
residual_uncertainty:
permission_to_publish_verbatim: yes | no | with-redactions
```

End with separate verdicts for:

- source/card fidelity;
- comparator fairness;
- measurement and analysis;
- human-subject safety and custody;
- public-claim ceiling; and
- whether the controlled study may proceed to ethics submission and freeze.

There is no single compensating score. “Proceed” means only that no identified
blocker remains in that reviewer's scope; it does not certify truth or benefit.

## Author response and dissent custody

The authors respond in a separate ledger: `issue → accept/reject/defer → exact
change → reason → residual`. They may correct factual errors or explain why an
objection is not adopted, but never edit the reviewer's verdict. Preserve
unfavorable and minority reviews, reviewer-requested redactions, and the exact
version reviewed. Public attribution requires permission.

The gate fails when conflicts or competence are undisclosed, different bundles
are compared as if identical, authors condition payment/publication on a
favorable verdict, a material blocker is ignored, or dissent is withheld.

Artifact-only professional critique is not automatically human-subject
research. If reviewers themselves become objects of systematic study or their
identifiable responses are analyzed/publicized, obtain the applicable ethics
determination before contact.

## Public reporting template

> Reviewer R, with disclosed scope S and conflicts C, reviewed packet hash H and
> found findings F, blockers B, and unresolved questions U. The author response
> is separate. This is independent criticism, not endorsement, validation, or
> replication.
