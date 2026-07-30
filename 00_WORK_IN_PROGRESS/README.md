---
title: "00_WORK_IN_PROGRESS — the manifest of what is open, and what it is waiting on"
status: "ACTIVE — a MANIFEST, not a relocation. Holds no source truth and owns nothing."
date: 2026-07-30
evidence_tier: "[B] this register is a reproducible index; each entry carries its own tier and its own owner"
owner: "No owner. Every entry points at its owner. This folder may never be cited as authority."
parents:
  - ../00_ESTABLISHED/README.md
  - ../00_META/00_THE_CLAIM_STATUS_REGISTER.md
---

# 00_WORK_IN_PROGRESS

> **This folder holds no doctrine, no source truth, and no authority.**
> It is an index of what is **open**, with what each item is waiting on.
> **Nothing was moved here. Nothing was archived.**

## Why it exists

The corpus had two declared tiers and needed three.

```text
00_ESTABLISHED/    what survives an outside check      — a manifest
00_WORK_IN_PROGRESS/  what is open and what it awaits  — this manifest
90_ARCHIVE/        what is superseded, with provenance — 24 subdirectories
```

Without the middle tier, everything not yet established looked either finished or
dead. **An open question filed next to a settled one reads as settled**; an open
question filed nowhere reads as forgotten. This index is the difference.

**The rule that makes it useful, and the one it can fail:** an entry leaves this
file only when its owner records a ruling or a landed result — **never** because it
went quiet. If an entry is removed with no ruling to point at, this manifest has
become a way of losing work and should be repaired.

---

## 1 · Open owner rulings — blocked on a decision, not on labour

| id | question | blocks | source |
|---|---|---|---|
| `§5.1` | Are the irrationals *numbers*, or *limits of operations*? The theorem that they are **not finite words** is settled `[A]`; what to call them is not. | the vocabulary of every page that says "number" | `05_COSMOLOGY/03_FORMAL_SYSTEM/53_THE_NUMBER_CHART.md` |
| `G-0` | Which base is canonical — the generative base, or the sphere at `00_THE_FOUNDATION.md` §2? Both are live; one must own the seat. | whether `52_THE_GENERATIVE_BASE.md` supersedes anything | `05_COSMOLOGY/03_FORMAL_SYSTEM/52_THE_GENERATIVE_BASE.md` |
| `G-0b` | The neutral-letter exit (`e, a, b`) for the same collision. | same | same |
| — | Disposition of the **91 ambiguous receipt numbers**: each needs a `superseded_by:` pointer or a distinct number. | trustworthy numeric citation anywhere in the corpus | `11_UPLINK/50_AUDITS_AND_EXECUTIONS/191_LINE_4_REFUTED_AND_THE_CITATION_DEFECT_2026_07_30.md` |
| — | Disposition of the **40 site pages declared neither current nor frozen**. Declaring them current fails the parity contract on Titan infix; leaving them undeclared means they carry retired claims with no banner. | the site's publication boundary | `12_PUBLIC_SITE/public_semantic_parity.json` |

---

## 2 · Open claims — carried at tier, awaiting evidence

Read from the **machine source**, `00_META/claim_status/CLAIM_STATUS.yaml`:

```text
18   validated   passed their own validator
17   open        awaiting evidence or a ruling   <- the live queue
22   graves      terminal; a one-way row may never return as the claim it was
 9   reopened    under a named owner ruling, with the counterexample still attached
```

> **A correction this manifest made to itself on the day it was written.** The first
> draft parsed the *human mirror* (`00_META/00_THE_CLAIM_STATUS_REGISTER.md`) and got
> `8 OPEN / 2 NARROWED / 13 REFUTED` — different numbers from the ones
> `check_claim_status.py` prints, because the mirror is not the authority and because
> the real vocabulary is `OPEN-FORMAL`/`OPEN-EMPIRICAL`, not bare `OPEN`. **Two
> checkers reading the same subject disagreed, and the newer one was wrong.** Cite the
> YAML.

**This table is a count, not a claim**, and it is reproducible with
`python3 09_TOOLS/01_SCRIPTS/check_claim_status.py`.

---

## 3 · Specified and not run — the largest gap in the case

| what | state | source |
|---|---|---|
| **Eleven empirical sockets** (`GP` questions) | packet-complete, **none run** | `03_METHODOLOGY/00_EMPIRICAL_PROGRAM_BOARD.md` |
| `GP-03` specifically | **struck void as written** — its entry condition required independent numeric factor measures, which the ordinal ruling abolished. No replacement specified. | `11_UPLINK/50_AUDITS_AND_EXECUTIONS/184_THE_PRODUCT_CONJECTURE_RULED_2026_07_30.md` |
| **Three preregistrations** — fresh-reader comprehension, independent review, controlled comparison | protocols written and public; **no session, no engaged reviewer, no registered comparison** | `03_METHODOLOGY/03_PREREGISTRATIONS/finity_practice/` |
| **Returned outcomes from outside** | **306 numbered receipts · 7 mention an outcome coming back · 0 record one that did** | `12_PUBLIC_SITE/record/` |

That last row is the honest summary of this whole folder. Everything above it is
internal work. **A framework can be internally immaculate and still be about nothing.**

---

## 4 · Never surveyed at body level

Audited by tag count only, never read claim-by-claim:

- `04_AXIOLOGY/` — 10 `[A]` sites
- `06_ONTOLOGY/` — 31 `[A]` sites

An untagged wrong claim in either is currently invisible to every checker the corpus
owns. **This is a known blind spot, recorded rather than closed.**

---

## 4A · The insight-transfer audit of 2026-07-30 — what landed, what did not

A five-region audit proposed **28 transfers** from the docs to the public site. Fifteen
landed. The rest are listed here rather than left in a temp file, because an audit
finding with no home is a finding that will be re-discovered at full cost.

**Landed** — each verified against its source before publishing, and four of them were
*false statements on live pages* rather than gaps: the product retired as a ranking and
its rider on the seven actions (`/record/` №028); `GP-03` void while the site still
invited strangers to preregister it; the paradox count (26 → 21, nine of them stubs);
self-criticism claimed as a credibility asset; "a line is a circle of infinite radius",
which is false in the plane; `A1–A7` published as current when `E1–E10` is the live set;
the price of the positive-only ruling; the three senses of "undefined"; two poles do not
produce a middle; the keel as a protractor fact; the honesty-constitution negative
result; **the law applied to itself returning 0**; and the dependency-priority /
actuality / salience separation on the spine.

**Not landed, and why** — these change what the framework *claims*, not whether it is
stated accurately, so each needs an owner ruling and not an edit:

| # | item | what it needs |
|---|---|---|
| 3, 3a | `μ₂` and `μ₃` adjudicated failed; `μ₀` still owes its discriminator; both candidate instruments fail to discriminate | a ruling on whether the site may still show five live crossings |
| 4 | `D0`/`D6` as a **duality, not an identity** — inversion exchanges the poles, it does not quotient them | reconciliation with the `D6~D0` closure ruled Path B today |
| 7 | the live constitution is `R0`: **no necessary being** | which constitution edition is public |
| 12 | a Rosetta falsifier **fired and was logged as a pass** | an integrity retraction, owner-countersigned |
| 13, 14 | no single score is permitted; the ontology profile has **explicit zeros** | the specific per-profile figures were not verifiable in the time available |
| 16 | over-claiming is **endogenous** to fitting every domain; antibody = a word watchlist | whether to publish the demolition manual |
| 19 | **ten senses of "exists"**; "everything coherent actually exists" is a retired inflation | a ruling on the retired form |
| 22 | the metaethics is an **open docket** against nine rival families, error theory admissible | whether to reopen a page that currently reads settled |
| 23, 24, 25 | Suda's chart is a proper sub-chart; the hinge **is** the relativistic velocity ratio; the three seats are forced on the ray, selected on the sphere | small, verifiable, simply not yet done |
| 27 | the adversarial audits' **own error rate** — five wrong file-level findings in two days | this session adds to that count, and the number should be recomputed before publishing |
| 28 | Path D: the four-operator structure does not follow from the framework's own inequality | the audit itself recommended skipping — the pages are `noindex` and the finding is already logged |

**Item 27 deserves the last word.** Of the 28 proposals, at least four were wrong on
their specifics — a claimed nine pages misusing the product where the true count is
zero, two "live indexed" pages that are `noindex`, an inflated call count, and a
mis-cited authority. **A verdict about a file is not evidence about a file.** Every item
above was checked before it was believed, and that is the only reason the list is
trustworthy at all.

---

## 5 · What this folder must never become

- **A promotion path.** Nothing graduates from here to `00_ESTABLISHED/` except by
  meeting that folder's admission standard, which is machine-checked.
- **A graveyard.** Superseded work goes to `90_ARCHIVE/` with a `superseded_by:`
  pointer, never quietly deleted from this list.
- **An authority.** If any document cites `00_WORK_IN_PROGRESS/` as a reason to
  believe or disbelieve a claim, that citation is invalid and this line is the fence.

**This document's own kill.** If an entry above has been resolved and this file still
lists it as open, or an entry was removed without a ruling to point at, this manifest
is lying in the direction that flatters us — and should be repaired or withdrawn.

**Reproduce:** `bash 09_TOOLS/01_SCRIPTS/gate.sh`

•   ⊙   ○ — *open is a tier, not a failure; unrecorded is the failure.*
