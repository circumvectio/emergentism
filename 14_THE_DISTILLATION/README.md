---
title: "The Second Churning — what stands, as of 2026-08-05"
status: "PROJECTION — rules nothing"
date: 2026-08-05
ownership: "Source documents retain semantic ownership. Every entry cites its source path, and where an entry and its source differ, the source governs. This folder creates no second owner, promotes no tier, settles no open question, and may never be cited as authority."
evidence_tier: "[B] for the projection's own facts (paths, statuses, counts, executions, recomputed here). Every distilled claim retains the tier of its source and may not be cited higher. Inclusion here confers nothing."
supersedes: "07_THEOLOGY/00_THE_AMRITA.md (DISTILLATION, 2026-07-03, recovery-integrated 2026-07-19) — on the distillation question only. Supersession is INCOMPLETE until the reciprocal line is written into that file; see §9."
---

# The Second Churning

> **The poison comes first. Before the treasures. Before the nectar.**
> — `05_COSMOLOGY/01_THE_TRANSCENDENTAL_TRINITY/27_THE_SAMUDRA_MANTHAN.md:73`
>
> That is the reason the deaths are placed first here and are the same size as the survivals. It is the metaphor's own instruction, not a claim about this folder.
>
> **The vessel is not one of the drops.** Document 27 is `[I]`, and its kill criteria are of the "if the mapping requires forcing" kind. It does not pass the gate below. Neither does the corpus's headline law `P = Φ×V`, the Rosetta, the D-ladder, the Titan reading, or the Justice formulae — see §8.

---

## 1 · What this is

A **projection** of 1648 live markdown files (recomputed this pass: `find . -name "*.md" -not -path "./90_ARCHIVE/*" | wc -l`) onto the question *what, on disk, survives a check by something that does not believe it.*

It reports. It rules nothing. It ratifies nothing. It is downstream of registers that have not yet recorded its sources (§7).

## 2 · The projection law

1. **Semantic ownership stays at the source.** Every entry carries a path. Where entry and source disagree, the source wins and the entry is the defect.
2. **No tier promotion — including by layout.** An entry drawn from an unratified document carries that document's status string *on the same line as the claim*, per the denial-marker rule at `02_EPISTEMOLOGY/01_EVIDENCE_TIERS/THE_BOUNDARY_RULES_STANDALONE.md` §12: same line, never a caption.
3. **Nothing enters that is not on disk.** A gloss carried in a brief, a memory file, or a conversation is not corpus state.
4. **Inherited results name their owner in the same line as the claim.** Not in a footnote.

## 3 · The inclusion gate, in full

A claim enters only if **all five** hold:

```text
1  TIER        it carries a stated evidence tier in its source document
2  KILL        it carries a kill criterion — or is [A] standard mathematics with a citation
3  UNFIRED     that kill has not fired
4  ATTACKED    it has survived at least one adversarial pass, or is [A] with prior art named
5  OWNED       where the result is inherited, the real owner is named
```

Stricter conditions exist already and are not met by everything here: `00_ESTABLISHED/README.md` §"The admission standard" requires additionally that **the verifier is actually invoked, not inferred from source text**, and that **a fresh command exits non-zero on failure**. Entries that would not clear those two say so.

## 4 · The count bound, declared before the entries were written

Per rule B2 — *declare the shape, not the number* (`THE_BOUNDARY_RULES_STANDALONE.md` §11 rule B2; owner: Lan–DeMets, O'Brien–Fleming, ICH E9):

- **Admission function:** the five gates of §3.
- **Deduplication rule:** one finding, one entry. A result reached by two framings is **one claim twice**, not two — rule S3, `THE_BOUNDARY_RULES_STANDALONE.md` §2. The same rule disqualifies Suda as external corroboration; it applies to this folder's own bookkeeping first.
- **Ceiling: 45 entries. Expected: 35–40.**

**How a reader recomputes it.** Count the entries. For each, check five fields are present: tier, source path, owner, kill, adversarial pass. Every entry missing one is a gate failure and the count is wrong by that many. If the total exceeds 45, the gate was loosened after the bound was declared and this folder should be rebuilt, not amended.

## 5 · The one-line answer to "what is mathematically new here"

The corpus has already written it, and it belongs above the entries rather than after them:

> the observation that the two syntactic exclusions (`ιι = id`, `ι(1) = 1`) are *the same constraint* as the classical `a_n ≥ 2` normalisation — an expository identification, `[I]`, of real pedagogical value and **no theorem content**.
> — `05_COSMOLOGY/03_FORMAL_SYSTEM/55_G2_PRIOR_ART_ADJUDICATION.md:150-154`

Everything else admitted on the mathematical side belongs to Euclid, Hardy & Wright, Khinchin, Stern, Brocot, Calkin–Wilf, Dedekind, Cantor, Möbius, Klein, Russell, Zermelo–von Neumann, Hermite, Lindemann, Cauchy, Lagrange, Napier, Euler, Mac Lane, Brahmagupta, Presburger, Tarski, Setzer, Carlström, Bergstra, Kahan, Lotka, Volterra, Glashow–Weinberg–Salam, Witten, Atiyah–Hirzebruch, Terrell, Penrose, Shannon, Klyubin–Polani–Nehaniv, Pigou–Dalton, Rosenthal, Goldacre, Lan–DeMets, O'Brien–Fleming, DeMillo–Lipton–Sayward.

## 6 · Four classes of entry, and one register that is not entries

| part | holds | rule |
|---|---|---|
| **DIED** | claims whose kill fired, with the counterexample and the date | placed first (§ epigraph) |
| **INHERITED** | `[A]` results that stand, each naming its owner | the corpus's delta, if any, is stated separately from the theorem |
| **SELECTED** | choices with their price named and what a rival gets | a selection presented as forced is the defect this part exists to catch |
| **METHOD** | rules a stranger can run without adopting anything | every rule sourced to `THE_BOUNDARY_RULES_STANDALONE.md` is `[D]`, its own frontmatter tier |
| **LIVE DEFECTS** | *not entries.* Open wounds: unrepaired text, dead gates, unpropagated reversals | a dead claim and an open wound are different objects; filing one as the other reports the corpus as healthier than it is |

## 7 · Standing conditions on everything in this folder

- **Unratified sources.** `48_CO_CONSTITUTION_AND_THE_NOTATION_PROBLEM.md` and `49_THE_THREE_MODES_OF_COUNTING.md` are both `status: "STAGED PROPOSAL — unratified"`. `THE_BOUNDARY_RULES_STANDALONE.md` is `DRAFT 1 — unratified`, `evidence_tier: [D]`, `not_a_gate: Deliberately unenforced`. `13_BOOKS/titans/CH04`, `CH09` are DRAFT 1.
- **"Machine-checked" means at one remove.** `09_TOOLS/05_FORMAL_VERIFICATION/EmergentismCheck.lean` was **not recompiled** in this pass. Re-verified directly: 20 `theorem` declarations, no substantive `sorry`/`admit`, toolchain `v4.33.0-rc1`, mathlib pinned `932a58b04d34`. The recorded build is `11_UPLINK/50_AUDITS_AND_EXECUTIONS/182_C_HAT_IS_NOT_A_RING_MACHINE_CHECKED_2026_07_29.md` (8661 jobs, 20 theorems, no `sorry`). The file's last commit `31fa4533` postdates that build; the diff is a two-line docstring change touching no theorem or proof term. Say *at one remove* every time.
- **The register is stale and this is a publication condition, not a footnote.** `00_ESTABLISHED/README.md:100` still lists `G2` as an *open general claim*, and `:114` still reads *"G2 remains open until a complete proof or formalization lands."* That was superseded by `55_G2_PRIOR_ART_ADJUDICATION.md` on 2026-08-05. The G2 entry cites **both paths** and states the contradiction rather than asserting one side.
- **None of the 2026-08-05 sources appear in `00_META` registers or `FILE_REGISTER.json`.** Every contradiction reported here is findable only by reading the files.

## 8 · What this folder may not be cited for

```text
F0 (type integrity)      NOT PASSED — its negative tests are assertIn substring
                         checks on prose (42_THE_CASE_FOR_FINITY.md:194; 47:23-46)
F1 (contribution beyond
    prior art)           OPEN — first and only candidate adjudicated as prior art (55 §7)
F2 · F3 · F4             NOT STARTED
P = Φ×V                  AND-class law, not a proved product; the product is retired
                         as a ranking (KSC-02); no aggregator is established
η = 0                    a conditional gate, not a consequence of any count
the honesty protocol     its efficacy is [C] and has never been run as a controlled
                         trial (THE_HONESTY_PROTOCOL_STANDALONE.md §7)
the four-status claim    the twenty-reader test against a control has never been run
the Rosetta · D-ladder · μ-contract (μ₂, μ₃ FAILED) · the Titan reading ·
Justice · the 5+1 Constitution · the paradox dissolutions · the Samudra Manthan
```

None of that is thereby false. It is unchecked, or selected, or interpretive, and those are different things from false — the form and the sentence are `00_ESTABLISHED/README.md:126-142`, adopted here outright, **including its condition: quietly shortening this list turns the artifact into a promotion path.**

## 9 · Supersession — incomplete until reciprocated

`07_THEOLOGY/00_THE_AMRITA.md` is already a distillation: *"DISTILLATION — 2026-07-03; recovery-integrated 2026-07-19"*, provenance *"churn of 12 lanes, 72 nectar + 48 halāhala"*. It predates every ruling collected here and contains none of them.

Two distillations standing side by side, silent about each other, would give two answers to one question and would be the second owner §2 forbids. This folder therefore supersedes it **by name and by date, on the distillation question only.** Until the reciprocal supersession line is written into `07_THEOLOGY/00_THE_AMRITA.md`, that act is unfinished, and this folder is itself an instance of the corpus's documented shape: *a correction written in one place and not propagated to the surface a reader meets.*

## 10 · This folder's own kill

- It is cited as authority, or as ratification, or as a tier.
- An entry appears without one of the five fields of §4.
- The entry count exceeds the declared ceiling of 45.
- The §8 exclusion list gets shorter without a dated receipt saying why.
- An entry is found that is not on disk at the path it cites.

Any one of these fires. The remedy is withdrawal and rebuild, not amendment.
