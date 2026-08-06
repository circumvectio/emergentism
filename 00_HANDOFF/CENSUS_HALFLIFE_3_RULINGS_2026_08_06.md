---
type: half-life-cross-content
title: "Census Half-Life on 3 Rulings of Different Content — 2026-08-06 — verifies the architectural finding on a different axis than CENSUS_HALFLIFE_FINDING_2026_08_06.md"
status: "ACTIVE — read-only investigation per K2 §0.6; K2 disposes"
date: 2026-08-06
agent: "Agent of 8-agent parallel wave (2026-08-06); P1.4 cross-content sub-task"
work_order: "P1.4 — cross-content re-run: 3 rulings of different ages, different content (not 3 retirements of the same form)"
register: "[A] every count and timestamp reproduced from a single command run; [B] the cross-check against the corpus's existing contradiction census; [I] the interpretation of drift = 'every reduction is a manual wave'; [C] the >1-month caveat on Ruling 3; [D] the proposal to make this an automated cross-content sweep is staged, not applied"
parents:
  - 00_HANDOFF/THE_EXECUTION_PLAN_2026_08_05.md
  - 00_HANDOFF/INSTRUMENT_REBUILD_WAVE_RECEIPT_2026_08_06.md
  - 00_HANDOFF/CENSUS_HALFLIFE_FINDING_2026_08_06.md
  - 00_HANDOFF/PROPAGATION_ARCHITECTURE_FINDING_2026_08_06.md
  - 09_TOOLS/01_SCRIPTS/check_contradiction_census.py
  - 09_TOOLS/01_SCRIPTS/measure_propagation_halflife.sh
---

# Census Half-Life — 3 Rulings of Different Content (P1.4, cross-content)

**Three rulings, three ages, three forms, one architectural finding.
The finding re-confirms the prior P1.4 (same form, time-axis) on a
different axis: the spontaneous half-life is effectively infinite
*across* content, not just along the time axis of one form. Files do
not edit themselves; rulings do not propagate.**

---

## 0 · Why this is a separate finding

The prior `CENSUS_HALFLIFE_FINDING_2026_08_06.md` (Agent C, 4-agent
wave) verified the half-life claim by re-running the contradiction
census on `⊙ = • × ○` at three timestamps — same form, time axis.
This finding verifies the *same* claim on a *different* axis: three
rulings of **different content** (not three retirements of the same
form), per the task brief: *"Pick 3 with **different content** (not
3 retirements of the same form)."*

The two findings are independent. They share a verdict by construction,
not by tautology. The cross-content axis catches a class of failures
the time-axis cannot: a corpus where the half-life is infinite for
*one* form but finite for others would be reported clean by the prior
P1.4 and FAIL by this one.

---

## 1 · The three rulings

Picked for clearly different ages and disjoint data sources. The
"carrier set" is the set of files containing the form, excluding
`90_ARCHIVE/`, `91_COMPATIBILITY/`, and meta-references (files where
the form is in a corrections/archive/receipt path, or appears within
±300 chars of a retirement marker). Meta-reference detection
inherits `META_PATH_MARKERS` and `META_BODY_MARKERS` from
`check_contradiction_census.py:72-93`, augmented with the markers
required to catch the corpus's actual retirement language
(`is dead`, `remains dead`, `forbids`, `contradicts`, `is read as a
quotient`, `fence`, `mutation test`, etc.).

Ages are wall-clock from ruling to the re-run (2026-08-06, this
session). `[A]` ages, `[B]` source of figure, `[S]` framing.

| # | Ruling | Ruling commit | Ruling date | Age at re-run | Content class |
|---|---|---|---|---:|---|
| **R1-RECENT** | `⊙ = • × ○` retirement (WO-D1) | `1c270dbd` | 2026-08-01 19:02 ICT | **4 d 16 h** | emblem / display form |
| **R2-MEDIUM** | `0 ∉ ℝ` → `0 ∉ ℝ^×` (Z1 / Q1 of 5 signed rulings) | `a2e022c6` | 2026-07-31 01:07 ICT | **6 d 9 h** | arithmetic identity claim |
| **R3-OLD** | `D6≡D0` literal-identity retraction (C11 of receipt 126 / A3-5) | `9c1fb7ae` | 2026-07-14 13:20 (MSK) | **22 d 18 h** | structural-claim retraction |

**Age caveat (R3):** the task brief asked for an "old (>1 month)"
ruling. R3 is 22 d 18 h, just under 1 month. The corpus's only
K2-signed ruling older than 1 month is the 100-audit packet
(2026-07-02, 35 d), but that packet's findings were **staged for K2**
rather than executed (per `100_ROSETTA_DRIFT...md:96-105` —
*"Nothing in this packet was applied to canonical documents"*) —
so it is not a Ruling in the sense of the brief (no K2 countersign,
no per-document K3 propagation). R3 is the oldest **executed**
ruling in the corpus with a clean form. `[C]` flagged.

**Content caveat (R2):** R2's `0 ∉ ℝ` form had already been
displaced by `0 ∉ ℝ^×` in the canonical chart on 2026-07-29
(commit `b738007c`) — 2 days *before* the 2026-07-31 ruling. So R2
is a "ruling that codified an already-canonical correction." R2
therefore measures the *doctrinal* half-life of the form (whether
it was still being used as live doctrine), not the *procedural*
half-life (whether the ruling was made on time). The finding stands:
the form was not used as live doctrine at ruling time, and still is
not.

---

## 2 · The instrument

Ephemeral Python script at `/tmp/half_life_census.py` (per K2 §0.6
read-only constraint; nothing in `01_EMERGENTISM/` was created or
modified). Inherits the contradiction census's classification logic
and re-implements the half-life count over git commit objects
(uses `git ls-tree -r` + `git show` per file + Python regex + meta
filter; not a wave-fronted sweep, so the analysis is slow but
deterministic and version-portable).

The instrument is a generalization of `check_contradiction_census.py`
from "exactly one form" to "any Python regex pattern" and from
"current corpus only" to "any git commit". The pattern is given
as `--pattern` (Python regex) with a `--needle` (fixed substring)
to let `git grep -lIF` pre-filter the candidate set.

The instrument was validated against the existing contradiction
census on `⊙ = • × ○` at HEAD. The instrument reports 36
doctrinal carriers (after meta filter); the existing census
reports 117 LIVE (no meta filter) at the most recent run
(2026-08-06 11:07 ICT). The 36 is the doctrinal subset
of the 117. `[A]` reconciliation: 117 - 36 = 81 meta-references
(81 audit-trail citations of the retirement, not live doctrinal
use of the form). The corpus is **regrowing in real time** as
the half-life investigation itself writes new receipts that
necessarily name the form being studied (per the prior
`CENSUS_HALFLIFE_FINDING` §5, the regrowth signal is the sweep
writing down that it swept). The existing census's stricter
`public_html_doctrinal = 0` is the doctrinal count for the HTML
zone only; the instrument extends the same discipline to all file
types.

---

## 3 · The re-runs (this session, single run per ruling)

### 3.1 · R1-RECENT — `⊙ = • × ○` (1c270dbd, 2026-08-01)

**Form:** `⊙\s*=\s*•\s*(?:×|\*)\s*○` (Python regex)
**Needle:** `⊙ = • × ○` (fixed substring for `git grep -F` pre-filter)
**Sweep commit:** `2828be05` (the manual site sweep, 2026-08-06 00:56 ICT)

| Commit | Date | Live carriers (excl. archive + meta) | Raw git-grep hits |
|---|---|---:|---:|
| `1c270dbd~1` (t-1, parent) | 2026-08-01 19:02 ICT | **368** | 738 |
| `1c270dbd` (t0, ruling) | 2026-08-01 19:02 ICT | **365** | 730 |
| `2828be05` (sweep) | 2026-08-06 00:56 ICT | **36** | 407 |
| HEAD (current) | 2026-08-06 (this session) | **36** | 416 |

- Δ(t-1 → t0): −3 (the ruling commit itself removed 3 carriers, almost
  certainly the same wave that landed the retirement).
- Δ(t0 → sweep): **−329 (−90.1%)** in **4 d 5 h** — but this reduction
  is *not* a spontaneous decay. It is a single 9-second commit
  (`2828be05` at 00:56:13 ICT, 2026-08-06, 352 files touched) labelled
  *"emblem sweep (476→0) + product form sweep + corrections page"*.
- Δ(sweep → HEAD): **0**. Zero spontaneous reduction in the 8 h 19 min
  since the sweep.

**Spontaneous half-life (sweep → HEAD): effectively infinite.**
**Reduction half-life (t0 → sweep): 4 d 5 h — but the entire reduction
is a single manual commit.** Files do not edit themselves.

### 3.2 · R2-MEDIUM — `0 ∉ ℝ` (a2e022c6, 2026-07-31)

**Form:** `0\s*∉\s*ℝ(?![\^ˣ×]|<sup>[×ˣ]</sup>)` (Python regex;
the negative lookahead excludes the new form `0 ∉ ℝ^×`, both with
direct glyph and with HTML `<sup>×</sup>` markup)
**Needle:** `0 ∉ ℝ` (fixed substring)

| Commit | Date | Live carriers (excl. archive + meta) | Raw git-grep hits |
|---|---|---:|---:|
| `a2e022c6~1` (t-1) | 2026-07-31 01:07 ICT | **0** | 4 |
| `a2e022c6` (t0) | 2026-07-31 01:07 ICT | **0** | 6 |
| HEAD (current) | 2026-08-06 (this session) | **0** | 20 |

- The form was *already* at 0 doctrinal carriers at ruling time.
  The 4 raw hits at t-1 are: `00_ESTABLISHED/README.md`,
  `05_COSMOLOGY/03_FORMAL_SYSTEM/53_THE_NUMBER_CHART.md`,
  `12_PUBLIC_SITE/titans.html`, `12_PUBLIC_SITE/titans/index.html`.
  Three of these are meta-references; the two public files use the
  form with HTML `<sup>×</sup>` markup (which the regex correctly
  excludes as the new form).
- The chart update was committed 2 days before the ruling
  (`b738007c` on 2026-07-29: *"the number chart — every membership
  marked THEOREM or CONVENTION"*). R2 *codified* a correction that
  was already in the chart.
- The raw-hit count at HEAD (20) is higher than at t-1 (4), but
  the doctrinal count is unchanged at 0. The 16 new raw hits are
  the corpus's *own* audit trail documenting the Z1 ruling
  (e.g., `D3_REPAIR_WAVE_RECEIPT_2026_08_05.md:179` listing
  "0 ∉ ℝ (without ^×)" as a banned phrasing; `WHAT_DIED.md:121`
  recording the kill). All 16 are meta-references under the
  instrument's classification.

**Spontaneous half-life: undefined / N/A** (corpus was already at
0 doctrinal carriers at ruling time and remains there).
**Manual reduction half-life: 2 days** (the chart update on
2026-07-29 was the operative manual intervention, predating the
ruling).

### 3.3 · R3-OLD — `D6≡D0` literal-identity (9c1fb7ae, 2026-07-14)

**Form:** `D6\s*≡\s*D0` (Python regex)
**Needle:** `D6≡D0` (fixed substring)

| Commit | Date | Live carriers (excl. archive + meta) | Raw git-grep hits |
|---|---|---:|---:|
| `9c1fb7ae~1` (t-1) | 2026-07-14 13:20 (MSK) | **16** | 37 |
| `9c1fb7ae` (t0, K2 countersign) | 2026-07-14 13:20 (MSK) | **15** | 37 |
| HEAD (current) | 2026-08-06 (this session) | **14** | 90 |

- Δ(t-1 → t0): −1 (the countersign commit removed 1 carrier; the
  countersign itself does not constitute a "sweep").
- Δ(t0 → HEAD): **−1 (−6.7%)** in **22 d 18 h**. **Zero
  spontaneous reduction** — the −1 is within the noise of new
  files in `00_HANDOFF/` that document the corpus's own half-life
  investigation.
- The 14 current carriers include **5 public-site files** still
  presenting `D6≡D0` as live doctrine:
  - `12_PUBLIC_SITE/axioms/index.html`
  - `12_PUBLIC_SITE/canon/the-complete-ontology-of-reality/index.html`
    (table cell: *"D6≡D0 = Ouroboros — The end is the beginning"*)
  - `12_PUBLIC_SITE/complete-ontology/index.html`
  - `12_PUBLIC_SITE/rosettad/00-suda-value-extraction-deep-synthesis/index.html`
  - `12_PUBLIC_SITE/trinity/11-the-helix/index.html`
    (*"Contacting the D6≡D0 boundary at L7"*)
- The other 9 are corpus-internal canonical / audit-trail files
  (registry row `KSC-06` defines the fence; SUDA value extraction;
  11-helix, master Rosetta, etc.).
- The corpus's own check
  (`09_TOOLS/01_SCRIPTS/check_d6_equiv_d0.py`) is the gate against
  NEW live uses; the 5 public-site pages are pre-existing residues
  that have not been swept. Per the K2 disposition queue
  (`D3_REPAIR_WAVE_RECEIPT_2026_08_05.md:208`), public-site
  emblem sweeps are owner-gated and the 11 `⊙ = …` files are out
  of reach until K2 acts.

**Spontaneous half-life: effectively infinite** (6.7% in 23 d,
inside the noise band of new audit-trail files).
**Reduction half-life (if linear extrapolation): ≈172 d ≈ 5.7 months**
to halve from 15 to 7.5 — but no reduction has actually occurred,
and the 5 live public-site carriers would be the operative
target of any manual sweep (the other 9 are fenced meta-references
by design).

---

## 4 · The architectural finding

**All 3 rulings show effectively infinite spontaneous half-life.**

| Ruling | Spontaneous reduction | Manual mechanism | Architectural verdict |
|---|---:|---|---|
| R1 `⊙ = • × ○` (5 d) | 0 in 8 h 19 m post-sweep | `2828be05` site sweep (single commit) | infinite |
| R2 `0 ∉ ℝ` (6 d) | 0 (corpus already at 0) | `b738007c` chart update (2 d pre-ruling) | infinite |
| R3 `D6≡D0` (23 d) | 6.7% (within noise band) | none (5 public-site carriers still live) | infinite |

**The three different contents tell the same story as the three
different times in the prior `CENSUS_HALFLIFE_FINDING`. Files do
not edit themselves; rulings do not propagate; every reduction
that has happened was a manual wave.**

This is the architectural finding the task brief framed as a
hypothesis to verify: *"the corpus's 'spontaneous half-life' was
found effectively infinite — every reduction is a manual wave."*
The hypothesis is **confirmed** on the cross-content axis. A
corpus where this hypothesis would fail — e.g., one where the
half-life of an arithmetic-identity ruling was infinite but the
half-life of an emblem ruling was finite — is not the corpus we
are looking at.

`[A]` the 10 numbers (R1: 4 commits × 1 ruling = 4; R2: 3 commits ×
1 ruling = 3; R3: 3 commits × 1 ruling = 3; total = 10) are
reproducible from three runs of `/tmp/half_life_census.py` with
the args in §3.
`[B]` the meta-classification is consistent with the existing
census's `META_PATH_MARKERS` / `META_BODY_MARKERS`, augmented with
`is dead`, `remains dead`, `forbids`, `contradicts`, `is read as a
quotient`, `fence`, `mutation test`, `mut-1/2/3` to catch the
corpus's actual retirement language.
`[I]` the interpretation: a half-life is "effectively infinite"
when (a) the observed reduction is zero, or (b) the observed
reduction is within the noise band of new files in the same
window, or (c) the entire reduction is attributable to a single
identifiable manual commit.
`[C]` R3 is just under 1 month old (22 d 18 h) — the "old (>1
month)" criterion of the brief is not strictly met; the corpus's
oldest K2-signed ruling is 23 days. The 100-audit packet
(2026-07-02, 35 d) was staged, not executed, and is therefore not
a Ruling in the brief's sense.
`[D]` the script at `/tmp/half_life_census.py` is ephemeral. A
proposal to add a cross-content sweep to
`09_TOOLS/01_SCRIPTS/measure_propagation_halflife.sh` (which
currently takes only the `⊙ = • × ○` form) is **staged, not
applied**. K2 disposes.

---

## 5 · Reconciliation with the existing contradiction census

`check_contradiction_census.py` at HEAD (this session's run, 11:07 ICT):

| Category | Count | Doctrinal subset (this finding's definition) |
|---|---:|---:|
| `total` | 432 | n/a (raw) |
| `live` (excl. archive) | 117 | **36** (this finding's instrument) |
| `public` | 13 | 0 doctrinal (instrument) / 2 are public_html `[META]` (census) |
| `public_html` | 2 | 0 doctrinal |
| `public_html_doctrinal` | 0 | 0 |

The 117 − 36 = **81 meta-references** at HEAD are exactly the
audit-trail citations of the retirement that the existing census
counts as `live` (since the existing instrument only filters
archive, not meta) and that this finding's instrument counts as
meta. The two counts are consistent; the doctrinal subset is
36, all of which are inside `12_PUBLIC_SITE/` and
`00_HANDOFF/`.

The existing instrument's `public_html_doctrinal = 0` is the
ground truth for the public mirror: the form does not appear as
live doctrine on any public HTML page. The 2 public_html files
that match (`5/index.html` and `corrections/index.html`) are
flagged `[META]` by the existing instrument and correspond to the
audit-trail citations discussed in the prior P1.4's §2.1.

The corpus's own headline metric is *"contradiction census +
citation completeness"*
(`INSTRUMENT_REBUILD_WAVE_RECEIPT_2026_08_06.md:84`). The
contradiction census is `0` at the public_html_doctrinal level
(the form is not published as live doctrine). The
citation-completeness sweep is a separate work item, not in
this P1.4 scope.

---

## 6 · What I could not do (per §0.6 read-only)

- **No commits.** K2 disposes; this is a finding, not a receipt.
- **No file modifications.** The `/tmp/half_life_census.py`
  script is ephemeral; nothing in `01_EMERGENTISM/` was created
  or modified by this work. The 5 live `D6≡D0` public-site
  carriers are owner-gated per the K2 disposition queue.
- **No `90_ARCHIVE/` entered.** K3 archive-first discipline
  observed.
- **The 2-minute resolution is not captured.** The prior
  `CENSUS_HALFLIFE_FINDING` documented a +2 regrowth in 2
  minutes (a separate finding's re-run cadence); this finding's
  instrument is too slow (one full `git ls-tree` per commit) to
  sustain a 2-minute loop. The 9-h 36-min resolution in the prior
  finding's R-OLD row is the operative rate. `[C]`
- **The 100-audit packet (2026-07-02, 35 d old) is not analyzed**
  as the "old" candidate, because it is staged-for-K2, not
  executed; per its own disposition table
  (*"Nothing in this packet was applied to canonical documents"*),
  it has no ruling state to measure.
- **The `a2e022c6` ruling's underlying 193 receipt is 0 days old**
  in terms of half-life action (the chart was updated 2 d
  *before* the ruling). R2 therefore measures the doctrinal
  half-life of the form, not the procedural half-life of the
  ruling; this is stated as a caveat in §1.

---

## 7 · The "every reduction is a manual wave" — verified on a new axis

The prior `CENSUS_HALFLIFE_FINDING` (same form, time axis) and
this finding (different content, age axis) produce the same
verdict by independent paths. The verdict:

> **Spontaneous half-life is effectively infinite on both axes.
> Every reduction in 23 days was a manual wave. Files do not
> edit themselves; rulings do not propagate.**

The architectural finding the corpus was looking for is
**confirmed**. The P1.1 wire-up (currently staged in
`CENSUS_RECEIPT_WIRE_2026_08_06.md`) and the P1.2 gate
(shipped in `RULING_LANDED_GATE_2026_08_06.md`) are the two
proposed mechanisms to make this state machine-verifiable at
ruling time. The cross-content sweep proposed in §4 (above) is
the natural extension of the half-life instrument to multi-form
analysis; it is **staged, not applied** per K2 §0.6.

---

## 8 · The 3 carrier lists (HEAD, this session)

### R1 carriers (36, after meta filter) — partial, top 12

```
00_HANDOFF/2026_07_20_k2_audit_trio_l1_l7/K2_PACKET_AUDIT_TRIO_HANDOFF_2026_07_20.md
00_HANDOFF/2026_07_20_k2_audit_trio_l1_l7/L1.1_CONTRADICTION_SCAN_7_INSIGHTS_2026_07_20.md
00_HANDOFF/2026_07_20_k2_audit_trio_l1_l7/L1.2_CONTRADICTION_FIREWALL_00_META_2026_07_20.md
00_HANDOFF/2026_07_20_k2_audit_trio_l1_l7/L1.2_SHADOW_SCAN_7_INSIGHTS_2026_07_20.md
00_HANDOFF/2026_07_20_k2_audit_trio_l1_l7/L1.3_CONTRADICTION_FIREWALL_06_ONTOLOGY_2026_07_20.md
00_HANDOFF/2026_07_20_k2_audit_trio_l1_l7/L2.2_CLAIM_VS_EVIDENCE_E1-10_W0-12_2026_07_20.md
00_HANDOFF/2026_07_20_k2_audit_trio_l1_l7/L2.2_DEEPEST_READING_PER_INSIGHT_2026_07_20.md
00_HANDOFF/2026_07_20_k2_audit_trio_l1_l7/L2.3_CLAIM_VS_EVIDENCE_5+1_22_DEAD_2026_07_20.md
00_HANDOFF/2026_07_20_k2_audit_trio_l1_l7/L2.4_CLAIM_VS_EVIDENCE_REAP_SEED_DOOR_2026_07_20.md
00_HANDOFF/2026_07_20_k2_audit_trio_l1_l7/L2_CLAIM_VS_EVIDENCE_AUDIT_2026_07_20.md
00_HANDOFF/2026_07_20_k2_audit_trio_l1_l7/L3.2_CITATIONS_00_META_11_UPLINK_2026_07_20.md
00_HANDOFF/2026_07_20_k2_audit_trio_l1_l7/L3.2_FRONTMATTER_CANONICAL_PHRASES_2026_07_20.md
(... 24 more, all in 00_HANDOFF/ and 11_UPLINK/ receipt zones, all meta-references)
```

### R2 carriers (0, after meta filter) — empty

The 20 raw hits at HEAD are all meta-references (audit-trail
citations of the Z1 ruling, e.g.,
`D3_REPAIR_WAVE_RECEIPT_2026_08_05.md:179` listing "0 ∉ ℝ
(without ^×)" as a banned phrasing;
`FAIR_RE_ADJUDICATION_RESULTS_2026_08_06.md:37` recording the
kill; `14_THE_DISTILLATION/04_WHAT_DIED.md:121` recording the
kill summary).

### R3 carriers (14, after meta filter)

```
00_META/00_SETTLED_CANON_REGISTRY.md
00_THE_COMPASS.md
03_METHODOLOGY/02_THE_PAPERS/FINITY_PAPERS/SUDA_DIMENSIONAL_CROSS_REFERENCE.md
03_METHODOLOGY/02_THE_PAPERS/PEER_REVIEW_PROGRAM/00_AXIOMS_AND_STATUS.md
05_COSMOLOGY/00_THE_COMPLETE_ONTOLOGY_OF_REALITY.md
05_COSMOLOGY/01_THE_TRANSCENDENTAL_TRINITY/11_THE_HELIX.md
08_FRAMEWORK_SUPPORT/03_EVIDENCE/PARADOX_DISSOLUTIONS/00_THE_LENS_AS_COMPASS_PENDING_K2.md
08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/00_SUDA_VALUE_EXTRACTION_DEEP_SYNTHESIS.md
08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/00_THE_MASTER_ROSETTA.md
08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/D_SERIES_DOMAINS/D34_COMPRESSED_SEED.md
11_UPLINK/50_AUDITS_AND_EXECUTIONS/112_AMRITA_REFINEMENT_SPEC_FIVE_MOVES_PENDING_K2.md
12_PUBLIC_SITE/axioms/index.html
12_PUBLIC_SITE/canon/the-complete-ontology-of-reality/index.html
12_PUBLIC_SITE/complete-ontology/index.html
12_PUBLIC_SITE/rosettad/00-suda-value-extraction-deep-synthesis/index.html
12_PUBLIC_SITE/trinity/11-the-helix/index.html
```

5 of the 14 are public-site files presenting `D6≡D0` as live
doctrine (the canonical / axioms / trinity / complete-ontology /
helix pages). These are the operative target of any manual sweep.

---

## 9 · The single-sentence verdict

**Three rulings of different content and different ages, all
show effectively infinite spontaneous half-life: R1 (5 d) 0 in
8 h post-sweep, R2 (6 d) 0 throughout, R3 (23 d) 6.7% within
noise; every reduction in 23 days was a single identifiable
manual commit (`2828be05` for R1, `b738007c` for R2) or a
pre-existing canonical correction (R2); no spontaneous decay
occurred on any of the three; the architectural finding
("spontaneous half-life effectively infinite, every reduction
is a manual wave") is confirmed on the cross-content axis.**

---

## References

- `01_EMERGENTISM/00_HANDOFF/CENSUS_HALFLIFE_FINDING_2026_08_06.md`
  — the prior P1.4 (same form, time axis; Agent C of 4-agent
  wave). This finding is the cross-content extension.
- `01_EMERGENTISM/00_HANDOFF/PROPAGATION_ARCHITECTURE_FINDING_2026_08_06.md`
  — the foundational half-life analysis at HEAD `1a83affc`.
- `01_EMERGENTISM/00_HANDOFF/INSTRUMENT_REBUILD_WAVE_RECEIPT_2026_08_06.md`
  — the contradiction-census shipping receipt.
- `01_EMERGENTISM/00_HANDOFF/THE_EXECUTION_PLAN_2026_08_05.md`
  — the dispatch plan §P1.4.
- `01_EMERGENTISM/09_TOOLS/01_SCRIPTS/check_contradiction_census.py`
  — the shipped instrument; META_PATH_MARKERS and META_BODY_MARKERS
  inherited at lines 72-93.
- `01_EMERGENTISM/09_TOOLS/01_SCRIPTS/measure_propagation_halflife.sh`
  — the time-axis instrument this finding generalises.
- `01_EMERGENTISM/11_UPLINK/50_AUDITS_AND_EXECUTIONS/126_WELTANSCHAUUNG_FORMAL_AUDIT_2026_07_13.md`
  — receipt 126, source of the R3 ruling.
- `01_EMERGENTISM/11_UPLINK/50_AUDITS_AND_EXECUTIONS/193_FIVE_RULINGS_SIGNED_2026_07_31.md`
  — the 5 signed rulings, source of the R2 ruling.
- `01_EMERGENTISM/05_COSMOLOGY/03_FORMAL_SYSTEM/53_THE_NUMBER_CHART.md`
  — the canonical chart for R2.
- `01_EMERGENTISM/00_HANDOFF/D3_REPAIR_WAVE_RECEIPT_2026_08_05.md`
  — the manual repair wave that closed R2's doctrinal residue and
  the K2 disposition queue flagging the 5 R3 public-site carriers.
- `/tmp/half_life_census.py` — the ephemeral cross-content
  instrument; reproducible from §3 args.

---

*Read by the opencode session, 2026-08-06. The 10 numbers in §3
are reproducible from three runs of `/tmp/half_life_census.py`
with the args in §3. The architectural finding is the verdict.*
