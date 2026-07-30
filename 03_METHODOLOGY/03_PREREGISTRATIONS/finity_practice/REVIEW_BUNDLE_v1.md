---
title: "Review bundle v1 — the frozen packet for FPE-REVIEW-01, with an invitation ready to send"
status: "READY TO SEND — not sent. No reviewer has been contacted. Sending is an owner act."
date: 2026-07-30
evidence_tier: "[B] the hashes and the file list; [S] the invitation's framing; no result of any kind"
owner: "Subordinate to 02_INDEPENDENT_REVIEW.md, which specifies this bundle and governs where the two differ."
parents:
  - 02_INDEPENDENT_REVIEW.md
  - REVIEW_BUNDLE_v1.json
---

# Review bundle v1

> **Nothing here is a result.** This is the packet `02_INDEPENDENT_REVIEW.md` says a
> reviewer must receive, assembled and frozen so that inviting one is a single act
> rather than a project. **No reviewer has been contacted. That step is not ours.**

## Why this file exists

The corpus has three written preregistrations and has run none of them. Of the three,
this gate is by far the cheapest: it needs **no ethics determination and no
participants** — only one qualified outsider willing to attack the material. The thing
standing in the way was clerical: the protocol requires a frozen bundle whose every file
hash is recorded in the invitation, and that bundle did not exist.

It exists now. `REVIEW_BUNDLE_v1.json` carries a `sha256` for all ten files.

**Verify it before and after:** `python3 09_TOOLS/01_SCRIPTS/check_review_bundle.py`

If any hash has moved, the bundle is `v2` and an older review does not cover it. That
rule is the protocol's, not ours: *"a material amendment requires a new version and a new
review; an older review cannot silently cover changed text."*

---

## What a reviewer is being asked to do

Not to endorse. The protocol is explicit that **review is criticism, not endorsement,
validation, or replication**, and that a clean review moves nothing except the copy and
the search. The questions run over prior art, comparator fairness, identification,
measurement, harm, custody and public language, and every verdict carries a severity from
`note` up to `fatal-to-claim`.

**The independence contract, in short.** Disclose and normally lack authorship, financial
or reputational stake, close personal relationship, and prior sight of other reviewers'
verdicts. Fixed fair compensation is fine if disclosed and not contingent on tone or
outcome. **Ideological disagreement is not a conflict; hidden material dependence is.**
And the protocol rules out the cheap substitute in one line: *AI or project-agent review
is useful internal search but does not satisfy this external gate.* Which is precisely why
this session cannot close this gate on its own.

---

## The known-weakness statement, which travels with the bundle

Quoted from the protocol because it is the sentence a reviewer should read first:

> *The authors designed the practice, the comparator, the outcome rubric, and the initial
> public language.*

Everything a reviewer is asked to judge was built by the people asking. The comparator
was chosen by the party it competes with. That is the structural defect the gate exists
to expose, and it cannot be fixed from inside.

---

## The invitation — ready to send, deliberately plain

> **Subject:** Paid critical review of a small decision-practice claim — looking for the
> strongest case against it
>
> I have a written claim that a seven-question decision worksheet helps people make
> better-recorded decisions, and a preregistered design meant to test it against an
> ordinary paper form and against whatever people already do. **Nothing has been run.** I
> would like one qualified outsider to attack the design before it is frozen, and to be
> paid a fixed fee for doing so regardless of what they conclude.
>
> What I am asking for is not endorsement and the protocol forbids me treating it as
> such. Concretely: is the claim already known under standard terminology; is the
> comparator a fair strongest rival or a straw one; can demand, expectancy or
> familiarity absorb the contrasts; can the outcomes tell a better *record* from a
> better *decision*; and what would you refuse to let me say in public on this evidence.
>
> The material is a frozen bundle of ten files with recorded hashes, roughly seventy
> pages, and it includes my own statement of the study's structural weakness: I designed
> the practice, the comparator, the rubric and the public language. Findings are recorded
> at your chosen severity up to *fatal-to-claim*, your dissent is preserved verbatim if
> you permit publication, and my response is filed separately from your verdict rather
> than mixed into it.
>
> If a blocker turns up, the study does not run. That is the outcome I am paying for as
> much as any other.

**Competences to seek** (one person may cover more than one, and there is no averaging of
scores across them): decision or behavioural science · research methods and statistics ·
human-subject ethics and privacy · plain-language accessibility.

---

## Status, stated so it cannot be misread

| | |
|---|---|
| bundle assembled and frozen | **yes**, 2026-07-30, ten files hashed |
| verifier wired into the gate | **yes**, `check_review_bundle.py` |
| reviewer identified | **no** |
| reviewer contacted | **no** |
| review received | **no** |
| result of any kind | **none** |

**This file changes the project's score by nothing.** The corpus has 306 numbered
receipts, seven that mention an outcome returning from the world, and none that record
one. Assembling a packet is still internal work. **The first row that moves the number is
a reply from someone who does not work here** — and on the framework's own conjunctive
law, until that arrives every other factor is multiplied by zero.

**Kill for this document:** if the bundle's hashes do not verify, or if any file listed
here has changed without a version bump, this packet is void and any review of it is void
with it.

•   ⊙   ○ — *the packet is ours; the verdict cannot be.*
