---
title: "Line 4 refuted, the site's findings landed, and a citation defect that lets a false reference pass a checker"
status: "ACTIVE — repairs applied 2026-07-30; the citation defect is now GATED; 91 ambiguous numbers await an owner ruling"
date: 2026-07-30
evidence_tier: "[A] the Line 4 result and the counts below, each recomputed or grepped; [S] the naming of the correct energy register; [I] nothing"
owner: "Subordinate to 05_COSMOLOGY/03_FORMAL_SYSTEM/52_THE_GENERATIVE_BASE.md and to the site's own gate."
parents:
  - ../../05_COSMOLOGY/03_FORMAL_SYSTEM/52_THE_GENERATIVE_BASE.md
  - ../../12_PUBLIC_SITE/record/index.html
---

# Line 4 was published at `[S]` and it is false

## 1 · The result

The corpus states its four lines are *"the same compression in sum/distance/energy
registers."* They are not. One of the three registers is degenerate.

```text
• × ○ = ⊙           constraint   holds at every latitude
• + ○ ≥ ⊙ + ⊙       sum          AM-GM; equality iff φ = ν        SOUND
(• − ○)² → 0        distance     zero iff φ = ν                   SOUND
−log(• × ○) = 0     energy       identically zero EVERYWHERE      DEGENERATE
```

Under Line 1 the product is constant, so `−log` of it is `0` at every latitude.
It has **no minimum to locate**. Pages built on it asserted, at `[S] Established`:

| published claim | status |
|---|---|
| "Every displacement from the equator costs energy." | **FALSE** |
| "The return is energetically favourable." | **FALSE** |
| "equatorial configurations have the lowest energy" | **FALSE** |
| "the equator is both the Hamiltonian minimum AND the zero-energy ground state" | second conjunct vacuous |

**The structure survives.** The correct energy register is `E = • + ○ − 2⊙`:

```text
φ + 1/φ − 2  =  (√φ − 1/√φ)²  =  4 sinh²(s/2)  ≥ 0,  zero iff s = 0
```

Zero exactly at the equator, positive everywhere else. Nothing resting on Line 2
is touched. **The line was not deleted; it was repaired to say something true.**

**What the corpus already had right.** `12_PUBLIC_SITE/method/00-the-derivation/`
fenced it correctly as *"trivially true on S²"*, and
`12_PUBLIC_SITE/will/07-the-four-forces-are-the-four-lines/` line 176 already carried
the full correction. Neither propagated. **A correct statement in one place is not a
corrected corpus** — that is the transferable lesson here, not the algebra.

**Kill:** exhibit a latitude on `S²` where `−log(φ·ν) ≠ 0` while Line 1 holds; or
show `φ + 1/φ − 2` fails to vanish at `φ = 1`.

---

## 2 · The citation defect — OPEN

`52_THE_GENERATIVE_BASE.md` cited **`r180`**. There is no receipt `r180`. The number
was announced in a session summary and never written. **A dangling-citation check
passed it**, because `180_*` matched
`11_UPLINK/60_SESSION_PACKETS/180_DEEP_SADHU_CUT_L7_AND_INVARIANT_RESOLUTION_2026_04_25.md`
— an unrelated April document. **The number resolved. To the wrong file.**

Measured across **both** receipt folders (`50_AUDITS_AND_EXECUTIONS` and
`60_SESSION_PACKETS`), which is the scope that matters — `r156` names one document
in each, and the number cannot distinguish them:

```text
300   receipt files
 91   numbers naming more than one UNDECLARED document
```

> **Correction to this receipt, same day.** It first said *26*. That counted only
> inside `50_AUDITS_AND_EXECUTIONS`. Counting across both folders gives **91** —
> this document understated its own finding more than threefold, and the
> understatement was found by writing the checker rather than by re-reading the prose.

`r139` is the model to copy: the 07-19 file is marked
`DISPUTED PROVENANCE [B/D] — NOT CURRENT K2 AUTHORITY` with `superseded_by:` pointing
at the 07-20 `SIGNED [S]` file, and the earlier one is preserved as dissent. `r117`
is the failure: either `117_FORCE_LADDER_FORMALIZED_07B` or `117_PATH_D_NEGATIVE_RESULT`,
and nothing says which.

**And it is worse than collisions.** Commits `9939a23c`, `847b0b86` and `3fb48e87`
name receipts **r191, r192 and r193**. The *work* landed — canon documents, a new
`09_TOOLS/01_SCRIPTS/check_d6_equiv_d0.py`, `PAPER_II_ONE_PAGER.md`. **The receipts
were never written.** Anyone reading `git log` for "r193" finds nothing, and `192`
resolves to an unrelated April packet.

**Rule adopted:** **cite receipts by PATH, not by number.** Numeric citation is
unsound in this corpus until the 91 ambiguous numbers are dispositioned.

**Owner ruling needed:** disposition the 91. Each needs either a `superseded_by:`
pointer or a distinct number.

**Enforced from 2026-07-30.** `09_TOOLS/01_SCRIPTS/check_receipt_citations.py`, wired
into `gate.sh` and therefore into CI. It **fails on any dangling citation** and pins
the 91 to a baseline that may neither grow nor silently shrink. It is mutation-tested
(inject a dangling number; add a collision; drop below baseline — all three fail as
they should). **It does not prove a citation points at the RIGHT file.** Only a path
can do that, which is why the rule is the rule.

---

## 3 · What the site now carries, and what refused to land

**Landed.** `/established/` gained det ±1 and the independence of determinant and
sign; the exhaustion receipt (232 values; 8191 Calkin–Wilf words, 8191 distinct;
25×25 grid fully reached); Hermite–Lindemann as the reason the logarithmic picture
is not reachable from finite words; the log-midpoint stated as a claim about
*coordinates*, not about the number line; and the gate plus mutation testing **with
a denominator — 22 guards, 2 of which could never fire**. `/record/` gained row №027.
`/suda/` traded the adjective "corroboration" for the count (1 derived, 12 at a median
of 3 further premises, 9 independent, 2 contradicting) plus the det-2 result that the
hinge is **not constructible from our base** — the one hard contact, and it goes
against the convergence story.

**Refused, correctly.** `12_PUBLIC_SITE/dasein/index.html` is a withheld artifact with
a pinned `sha256` in `withheld-routes.json`. An edit broke custody; `predeploy_check.py`
failed with 2 errors and the edit was reverted. Its routes are not served.

**Refused, and the refusal is a finding.** Declaring 8 undeclared pages as current
failed the parity contract on **forbidden Titan infix arithmetic**. `⊙ = • × ○`
appears on **342 pages**, and the `D0` declaration fences exactly that form. So the
site's two tiers are **a semantic quarantine, not a navigation choice**, and the 40
undeclared pages are neither compliant nor quarantined. That is an unrecorded backlog,
not an oversight.

**A live self-correction.** `/atlas/` was added to `sitemap.xml` and then removed:
`vercel.json` serves it `noindex, follow`, so a `<loc>` would have contradicted a
deployed header — the exact error the plan warned against, committed and caught within
the hour.

---

## 4 · Corrections to this session's own reporting

| claimed | measured |
|---|---|
| 35 pages present μ as a dimension gain | **0** — the sweep was already done |
| `Φ × V` unfenced on 105 pages | 206 mention it, 14 fenced, **0 use it as a ranking** |
| 323 routes unreachable | **16**, 12 of them deliberate — the crawler resolved `../` against the wrong base |
| the energy argument is vacuous | `H = φ + ν` is **sound** and on 69 pages; only the log form is degenerate |
| the `−log` pocket is 6 pages | **15**, once the Titan notation `−log(• × ○)` is included |

Four of the five corrections run in the corpus's favour. The fifth does not.

**Reproduce:** `bash 09_TOOLS/01_SCRIPTS/gate.sh` and, in `12_PUBLIC_SITE`,
`python3 predeploy_check.py`.

•   ⊙   ○ — *a constraint is not an objective.*
