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
| ~~`G-0`~~ | **CLOSED — ruled 2026-07-29, exit B-ii.** `00_THE_FOUNDATION.md:93` adds a fourth posit `B4` (`⊙ = e`, the identity **posited, not derived** — it had been harvested from notation). Neither base is seated over the other. | — | `00_THE_FOUNDATION.md:88-98` |
| ~~`G-0b`~~ | **CLOSED — ruled 2026-07-29, exit Z.** `00_THE_FOUNDATION.md:85`: `F1` is a property of `P1`, not a stratum beside it. | — | `00_THE_FOUNDATION.md:85` |
| — | Disposition of the **91 ambiguous receipt numbers**: each needs a `superseded_by:` pointer or a distinct number. | trustworthy numeric citation anywhere in the corpus | `11_UPLINK/50_AUDITS_AND_EXECUTIONS/191_LINE_4_REFUTED_AND_THE_CITATION_DEFECT_2026_07_30.md` |
| — | Disposition of the **40 site pages declared neither current nor frozen**. Declaring them current fails the parity contract on Titan infix; leaving them undeclared means they carry retired claims with no banner. | the site's publication boundary | `12_PUBLIC_SITE/public_semantic_parity.json` |

---

> **This manifest listed two closed rulings as open, and the reason is worth keeping.**
> `G-0` and `G-0b` were both ruled on **2026-07-29**. But
> `52_THE_GENERATIVE_BASE.md` still carried *"Owner ruling G-0 pending"* in its
> frontmatter a day later, and this file was built from that. **A ruling that lands and
> does not propagate is indistinguishable from a ruling that never happened** — which is
> the same defect this corpus recorded twice last week in other forms. Both files
> corrected 2026-07-30. Found by a council that was asked to *rule* on G-0 and instead
> reported that the question was stale.

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
| **The review packet** — the cheapest of the three gates, needing no ethics determination and no participants | **assembled, frozen and hash-verified 2026-07-30; NOT SENT.** Ten files, `sha256` recorded, invitation drafted. What remains is identifying one qualified outsider and asking them — an owner act, and the protocol rules out the substitute in one line: *"AI or project-agent review … does not satisfy this external gate."* | `.../REVIEW_BUNDLE_v1.md` |
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

## 3A · The council rounds, and what the councils corrected in me

Two multi-seat councils sat on 2026-07-30. Both produced rulings; more usefully, **both ran
the read-only kills their own rulings named, and four of those kills fired.**

**What the first council corrected.** My docket asked it to rule `G-0` — *already ruled
2026-07-29*. It also asked "generative base vs the sphere at `00_THE_FOUNDATION.md` §2";
§2 no longer posits the sphere, it posits `B1`–`B4` and reaches `Ĉ` at emergent step 6.

**What the second council corrected, in me specifically.**

| I said | measured |
|---|---|
| "the authority chain resolves through ambiguous numbers" | **False.** `146_FOUNDER_RULING_EXECUTE` names **both** 145 files in its frontmatter and its body says "the two 145 receipts". It disambiguates itself. |
| "40 undeclared routes" | **~30.** `withheld-routes.json` declares 10 of them; I counted a second declaration registry as absence. |
| "86 ambiguous numbers" | The namespace has **three lanes** (167 + 127 + 10 numbered files), and **both live lanes begin at 100 and run over each other for a hundred consecutive integers.** |
| "only `/riemann` is linked from a declared surface" | **False.** `dimensions/index.html` links `/egg/`, `/riemann/`, `/suda/`, `/titans/`, `/saturation/`. |

**The kill that fired and cost something.** `/record/` — a declared current surface —
carried **11 bare citations** to "receipt 149/150/151", and each of those numbers names two
documents: a formal audit *and* an unrelated April session packet. Those three are the
Burri-sphere and horn-torus audits the ledger's own rows rest on. **The public record ledger
was citing its own evidence ambiguously**, on the one page whose subject is evidentiary
discipline, one day after the corpus adopted "cite by path, not number". All 11 replaced
with full filenames.

**Ruled and executed:** μ-crossing verdicts on the spine (4–0) · `G-0`/`G-0b` closed ·
the `/record/` citations.

**Ruled, awaiting a signature:** Q1 (§5.1 register-indexing) · Q2 (restating `KSC-28`'s
"sphere primacy" as chart selection) · Q4 (the ~30 undeclared, with four pages that pass the
contract moving to **declared-provisional**, not current — passing is necessary, not
sufficient, 3–0) · Q6 (library stays `noindex` + a published policy) · Q7 (launch copy).

**What neither council could decide, and what would decide it:** Q7's ordering — lead with
the zero or with the record. The majority conceded the dissent is not answerable by
argument, and named the evidence: **run the fresh-reader comprehension preregistration on
both orderings.** It is the cheapest of the three protocols and it is already written. There
is no excuse for settling that one by taste.

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

**Not landed, and why** — after a second verification pass on 2026-07-30, **21 of the 28
landed and 6 were rejected as ungrounded or already public.** What remains:

| # | item | state |
|---|---|---|
| 3 | `μ₂`/`μ₃` adjudicated failed; `μ₀` owes its discriminator | PARTLY-CONFIRMED. The *instrument* result landed (below). Whether `/dimensions/` may keep showing five crossings is an owner call — they are labelled "candidate crossing", which may already be adequate. |
| 11 | five terminal counterexamples (`ℤ₅`, Tarski, one martyr, electroweak, the kernel identity) | all five subjects exist in the corpus; the individual adjudications were not read. The two-axis discipline and the 22 terminal rows landed instead. |
| 14 | the ontology profile's specific figures | PARTLY-CONFIRMED — three numbers confirmed, but the framing "explicit zeros in the ontology profile" is **false**. The substance landed via the eight ceilings. |
| 28 | Path D and the four-operator structure | the audit itself recommended skipping; the pages are `noindex` and the finding is already logged. |

**Rejected outright**, so they are not re-proposed: item 4 (`D0`/`D6` duality — *already
settled canon and already public in substance*, and it does **not** contradict the Path B
ruling of 2026-07-30); item 25
(a phrase appearing only in the audit's own output); and two more the verifiers found
already public in stronger form than claimed.

> **A rejection in this file was itself wrong, and the correction belongs here.** On
> 2026-07-30 I recorded item 16 as rejected — *"no such watchlist exists; every
> `watchlist` hit is product material."* **False.** It is at
> `03_METHODOLOGY/00_THE_LENS_NOT_LAW_RULE.md:25`, a five-row trigger table at tier
> `[S]`, opened 2026-06-10. My search listed candidate files and truncated the list
> before reaching it. **That document predicts this exact failure** — *"audits of
> over-claims are themselves prone to the over-claim error, in both directions"*, and it
> gives the case of a grep that returned 0 as a false all-clear. So the audit error
> count drops from six to five, and one of mine is added in its place.

**Landed in the second pass:** 16 (the trigger watchlist and the single escape hatch); 3a (neither `μ`-instrument discriminates — one kills four
of five, the other none of five); 7 (`R0 · no necessary being` as a **refusal, never an
axiom**, with the correction that it does *not* rename the architecture); 12 (a Rosetta
falsifier fired and was logged as a pass — **already caught by the corpus in July**, so
published as a self-catch and not as a live failure, `/record/` №029); 13 (the eight
profiles and their ceilings); 19 (ten typed senses of "exists" and the retired
plenitude inflation); 22 (nine rival metaethical families); 23, 24 (the sub-chart and
the hinge-as-velocity-ratio, proved rather than asserted); 27 (the audit error rate).

**Item 27 deserves the last word.** Of the 28 proposals, **at least six** were wrong on
their specifics — a claimed nine pages misusing the product where the true count is
zero; two "live indexed" pages that are `noindex`; a call count inflated from 168 to
~200; a human mirror cited as authority over the machine source; **an antibody
"watchlist" that does not exist**; and **a phrase attributed to the corpus that appears
only in the audit's own output**. **A verdict about a file is not evidence about a file.** Every item
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
