---
type: half-life-finding
title: "Census Half-Life Verification — 2026-08-06 — re-run of P1.4 against three rulings of different ages (Agent C)"
status: "ACTIVE — finding, not a receipt; read-only investigation per K2 §0.6; K2 disposes"
date: 2026-08-06
register: "[A] every count and timestamp reproduced below from a single command run; [B] the live census output and the 3 re-runs within the session; [I] the interpretation of drift; [C] the +7 / +5 / +2 regrowth numbers depend on receipt-zone volume, not on doctrine; [D] any proposal to change the receipt template is staged, not applied"
parents:
  - 00_HANDOFF/THE_EXECUTION_PLAN_2026_08_05.md
  - 00_HANDOFF/CENSUS_RECEIPT_WIRE_2026_08_06.md
  - 00_HANDOFF/PROPAGATION_ARCHITECTURE_FINDING_2026_08_06.md
  - 00_HANDOFF/RULING_LANDED_GATE_2026_08_06.md
  - 09_TOOLS/01_SCRIPTS/check_contradiction_census.py
agent: "Agent C of 4-agent wave on 2026-08-06"
work_order: "P1.4 (census half-life verification)"
---

# Census Half-Life Verification — 2026-08-06 (Agent C, P1.4)

**Three rulings of different ages, one re-run of the contradiction census
each, three drift numbers, one verdict. The verdict confirms the
prior P1.4 measurement (`PROPAGATION_ARCHITECTURE_FINDING_2026_08_06.md`,
HEAD `1a83affc`): spontaneous half-life is *architecturally* infinite —
files do not edit themselves — and *operationally* the carrier set
moves only when a wave moves it. Every reduction in 18 days was a
manual wave; every regrowth in 45 minutes is the wave writing down
that it swept.**

---

## 1 · The three rulings

Picked for clearly different ages and clean disjoint data sources. Ages
are wall-clock from ruling moment to the re-run (2026-08-06 10:56 ICT,
this session, ~46 minutes after the SURGICAL_DEFECT ruling landed).
`[A]` ages, `[B]` source-of-figure, `[S]` framing.

| # | Ruling | Ruled | Age at re-run | Carrier set at ruling (claimed) | Source of figure | Census instrument present? |
|---|---|---|---|---|---|---|
| **R-OLD** | `WO-D1-2026-07-19` — `⊙ = • × ○` retirement | 2026-07-19 (K2 disposition per `48 §121` WITHDRAWN) | **18 d 4 h** | **725** total = 6 doctrine + 64 receipt + 359 public + 296 archive | prior P1.4 measurement, `PROPAGATION_ARCHITECTURE_FINDING_2026_08_06.md:26,62` (`1c270dbd~1 → 725 70 360 reproduces exactly`; decomposition: `doctrine=6  receipt=64  public=359  archiveANY=296  TOTAL=725`) | **no** — the contradiction census ships in this session (defect #3 of SURGICAL_DEFECT) |
| **R-MID** | `WO-SD-2026-08-06` — SURGICAL_DEFECT, the `⊙ = • × ○` instrumented (census ships, 4 surgical defects closed) | 2026-08-06 10:09:40 ICT (file mtime of `SURGICAL_DEFECT_WAVE_RECEIPT_2026_08_06.md`) | **46 min** | **422 / 107 / 16 / 2** (total / live / public / public_html) | `SURGICAL_DEFECT_WAVE_RECEIPT_2026_08_06.md:55` ("current verified state: 422 / 107 / 16 / 2") | **yes** — the receipt itself reports the figures inline |
| **R-NEW** | this re-run (synthetic "now" reference) | 2026-08-06 10:56:07 ICT | **0** | **427 / 112 / 13 / 2 / 0** | this session, single re-run | yes |

The R-OLD row is the only one whose "carrier set at ruling" figure
predates the census instrument. It is reconstructed from the prior
P1.4 measurement at `1c270dbd~1` (the commit before the retirement
itself landed) and is the corpus's only attested pre-instrument count.
The R-MID row is what the receipt's own prose reports, the
machine-read contract for "ruling landed" that the staged P1.1 proposes
to make binding (per `CENSUS_RECEIPT_WIRE_2026_08_06.md` §2). The
R-NEW row is the re-run; its "drift vs self" is definitionally 0 but
it is the re-run that lets R-OLD and R-MID drift numbers be computed.
`[A]`

---

## 2 · The re-runs (this session, captured verbatim)

`[B]` every line below is from `python3 09_TOOLS/01_SCRIPTS/check_contradiction_census.py`
invoked in `/Users/Yves/Documents/01_EMERGENTISM/`. The 3 re-runs
within the session are the empirical anchor: the carrier set moved
between the staged P1.1's snapshot at 10:44:45 (per the P1.1 prose),
the SURGICAL_DEFECT moment at 10:09:40 (per file mtime), and this
session's 4 re-runs at 10:51, 10:54, 10:55, 10:56.

```
10:09:40  (SURGICAL_DEFECT mtime)  →  422 / 107 / 16 / 2   [B] from SURGICAL_DEFECT §3
10:44:45  (P1.1 staged re-run)      →  422 / 107 / 13 / 2   [B] from CENSUS_RECEIPT_WIRE §5
10:46:46  (P1.1 second re-run)      →  423 / 108 / 13 / 2   [B] from CENSUS_RECEIPT_WIRE §5
10:51:55  (this session, run 1)     →  425 / 110 / 13 / 2   [A] this session
10:54:03  (this session, run 2)     →  427 / 112 / 13 / 2   [A] this session
10:55:15  (this session, run 3)     →  427 / 112 / 13 / 2   [A] this session
10:56:07  (this session, run 4)     →  427 / 112 / 13 / 2 / 0  [A] this session (with doctrinal-use breakdown)
```

The 427 / 112 / 13 / 2 / 0 final is the "now" reference used in §3.
`[A]`

### 2.1 · The 2 residual public_html carriers (from this session's run 4)

```
HTML files in public site matching the pattern:
  [META] 12_PUBLIC_SITE/5/index.html
  [META] 12_PUBLIC_SITE/corrections/index.html
```

Both classify as `[META]` under the census's `is_meta_reference`
(`check_contradiction_census.py:137-152`):

- `12_PUBLIC_SITE/5/index.html:154` — the META_BODY_MARKER
  `"withdrawn"` fires at line 154 (within ±300 chars of the match)
  `[A]` per `RULING_LANDED_GATE_2026_08_06.md:184-189`.
- `12_PUBLIC_SITE/corrections/index.html:88` — the META_PATH_MARKER
  `"corrections"` fires (per `:72-77`) `[A]` per
  `RULING_LANDED_GATE_2026_08_06.md:190-193`.

**Both are audit-trail citations of the retirement, not live doctrinal
use of the form.** This is why `public_html_doctrinal = 0` even
though `public_html = 2`. The strict reading (form string gone from
every HTML page) keeps the gate at NOT_LANDED (per
`RULING_LANDED_GATE_2026_08_06.md:149`); the doctrinal reading
(form not presented as live doctrine anywhere) is already clean.

### 2.2 · The 13 public files (this session)

For the drift on R-MID (public: 16 → 13), the 13 current are:

```
12_PUBLIC_SITE/00_BOOK_PWA_MOVED.md
12_PUBLIC_SITE/00_COMPASS_DEPLOYMENT_RECEIPT.md
12_PUBLIC_SITE/00_K2_ENVELOPE_APP_MIGRATION_2026_05_31.md
12_PUBLIC_SITE/00_THE_RUNGS_2026_08_05.md
12_PUBLIC_SITE/5/index.html
12_PUBLIC_SITE/_PLANS/00_PR_GROWTH_AUDIT_2026_07_20.md
12_PUBLIC_SITE/_PLANS/plans/2026-07-03-emergentism-honest-spine.md
12_PUBLIC_SITE/_PLANS/specs/2026-07-03-emergentism-honest-spine-design.md
12_PUBLIC_SITE/book-pwa/NODE_MODULES_TOMBSTONE.md
12_PUBLIC_SITE/check_public_semantic_parity.py
12_PUBLIC_SITE/corrections/index.html
12_PUBLIC_SITE/exit/README.md
12_PUBLIC_SITE/map/README.md
```

Of the 13, only 2 are HTML (`5/index.html` and `corrections/index.html`,
the meta-references above); the other 11 are provenance / plans /
fenced audit trails. The 3 public files that *left* the carrier set
between 10:09:40 and 10:56:07 are not enumerated in any receipt on
disk; the prior P1.4 noted this enumeration gap and left it open
("I did not classify R0's 11 public carriers use-vs-mention", at
`PROPAGATION_ARCHITECTURE_FINDING_2026_08_06.md:349-350`). `[C]`
un-traced which 3 dropped and why — outside this work order's scope,
flagged not papered.

---

## 3 · Drift per ruling

`[A]` every number below is a set difference. The carrier set is the
list returned by the census's `scan(root)` for the `total` /
`live` / `public` / `public_html` / `public_html_doctrinal` keys
(`check_contradiction_census.py:155-201`). Sets, not multisets — one
file in or out, regardless of how many times the pattern appears in
the file body.

### 3.1 · R-OLD drift: `WO-D1-2026-07-19` (18 d 4 h)

| Category | At retirement (2026-07-19, pre-instrument, per prior P1.4) | Now (2026-08-06 10:56 ICT, this session) | Δ | % |
|---|---:|---:|---:|---:|
| `total` | 725 | 402 (per prior P1.4 at HEAD `1a83affc`) / **427** (this session) | **-298 to -323** | **-41% to -45%** |
| doctrine | 6 | 14 (per prior P1.4) | **+8** | **+133%** |
| receipt | 64 | 76 (per prior P1.4) | **+12** | **+19%** |
| public | 359 | 11 (per prior P1.4) / **13** (this session) | **-346 to -348** | **-96% to -97%** |
| archive | 296 | 301 (per prior P1.4) | **+5** | **+1.7%** |
| public_html (instrumented, not measured at retirement) | — | 2 (this session) | n/a | n/a |
| public_html_doctrinal (instrumented) | — | 0 (this session) | n/a | n/a |

`[I]` The 18-day net decomposition is the architectural finding:

- **Public carrier set: 359 → 11 (-97%).** This is the *only*
  material reduction. The mechanism is a single manual wave,
  `2828be05` ("emblem sweep (476→0) + product form sweep") at
  2026-08-06 00:56:13 ICT, which touched 352 files. The drop
  happened in one commit, 18 days after the retirement. **The
  carrier set did not decay continuously; it collapsed when swept.**
- **Doctrine carrier set: 6 → 14 (+133%).** Regrowth. Per the
  prior P1.4's hand-classification at
  `PROPAGATION_ARCHITECTURE_FINDING_2026_08_06.md:182-186`, all
  14 are licensed (10 meta-references + 4 "bare" closing-emblem
  lines, the latter 4 being unmarked document signatures in 4
  named files). Net doctrine residue that is *not* a tombstone /
  repair / frozen filename: 4 of 14.
- **Receipt carrier set: 64 → 76 (+19%).** Regrowth. Per the
  prior P1.4, all 76 are repair apparatus — receipts, tombstones,
  registry rows, frozen filenames, drop-table citations. No
  bare live doctrine.
- **Archive carrier set: 296 → 301 (+1.7%).** The archive is
  *required* to retain retired wording by the corpus's standing
  K3 archive-first discipline; "Historical receipts, quotations,
  compatibility paths, and explicit tombstones may preserve
  retired wording" (`PROPAGATION_ARCHITECTURE_FINDING_2026_08_06.md:69-70`).
  Drift here is monotonic slow accretion as new retired content
  is tombstoned, not a violation of the ruling.

### 3.2 · R-MID drift: `WO-SD-2026-08-06` (46 min)

| Category | At SURGICAL_DEFECT (10:09:40, receipt's own count) | Now (10:56:07, this session) | Δ | % |
|---|---:|---:|---:|---:|
| `total` | 422 | 427 | **+5** | **+1.2%** |
| `live` | 107 | 112 | **+5** | **+4.7%** |
| `public` | 16 | 13 | **-3** | **-19%** |
| `public_html` | 2 | 2 | **0** | **0%** |
| `public_html_doctrinal` | (instrumented at 0) | 0 | **0** | n/a |

`[A]` the numbers; `[I]` the mechanism. Of the 5 net additions to
the `live` count in 46 minutes, **6 files have a post-SURGICAL
mtime** but one (`check_foundation.py`) is a re-touch of a
file already in the carrier set, so net new files = 5. They are:

| # | File | mtime | Pattern-matched on this pass? | New vs re-touch? |
|---|---|---|---|---|
| 1 | `00_HANDOFF/CENSUS_RECEIPT_WIRE_2026_08_06.md` | 10:48:04 | yes (line 206, 289) | **new** (added by the staged P1.1 itself) |
| 2 | `09_TOOLS/01_SCRIPTS/check_ruling_landed.py` | 10:49:21 | yes (P1.2 gate) | **new** (P1.2 instrument ships) |
| 3 | `00_HANDOFF/RULING_LANDED_GATE_2026_08_06.md` | 10:51:43 | yes | **new** (P1.2 receipt) |
| 4 | `00_HANDOFF/PROPAGATION_ARCHITECTURE_FINDING_2026_08_06.md` | 10:53:06 | yes | **new** (P1.4 finding) |
| 5 | `00_HANDOFF/MUTATION_TEST_GATES_2026_08_06.md` | 10:53:09 | yes | **new** (mutation tests receipt) |
| 6 | `09_TOOLS/01_SCRIPTS/check_foundation.py` | 10:54:21 | yes (live) | **re-touch** — file already in the carrier set pre-SURGICAL_DEFECT |

So `5 of 5` net additions are receipts and tools *of the half-life
investigation itself* — the P1.1 staged proposal, the P1.2 gate
and its receipt, the prior P1.4 finding, and the mutation tests.
**Not one of the 5 is a doctrine file.** This is the
"regrowth signal is the sweep writing down that it swept" finding
from the prior P1.4 (`PROPAGATION_ARCHITECTURE_FINDING_2026_08_06.md:196`),
re-confirmed.

The `-3` in public is untraced in this work order (per §2.2 above).
`[C]`

### 3.3 · R-NEW drift: definitionally 0

The R-NEW re-run is the reference point for the other two. Its
drift vs itself is 0; its existence is what makes the other two
drift numbers computable.

---

## 4 · Half-life verdict

**Half-life is infinite (architectural); carrier-set movement is
entirely manual (operational).**

| Claim (from the user's framing) | Verdict | Evidence |
|---|---|---|
| "725 carriers at retirement" | **Confirmed** (per prior P1.4) | `PROPAGATION_ARCHITECTURE_FINDING_2026_08_06.md:26` — `1c270dbd~1 → 725 70 360 reproduces exactly` |
| "spontaneous half-life effectively infinite" | **Confirmed (architectural, tautological)** | R-OLD drift decomposition §3.1: the 18-day net reduction is -41% to -45% but it concentrates in a single 9-second manual commit (`2828be05` at 00:56:13). Between retirement and that commit, the public carrier set was essentially unmoved (R1's 9 public pages unmoved for 15 days, per the prior P1.4 §5 cross-check; the `⊙ = • × ○` public count waited 18 days for the sweep). The prior P1.4 already stated this: "Spontaneous half-life effectively infinite. True but tautological as stated. Files do not edit themselves." (`PROPAGATION_ARCHITECTURE_FINDING_2026_08_06.md:257-259`) |
| "every reduction a manual wave" | **Confirmed** | R-OLD public reduction (359 → 11) is the single commit `2828be05` ("emblem sweep (476→0) + product form sweep", 352 files touched). No intervening commit between 2026-07-19 and 2026-08-06 00:56 reduced the public carrier set. The R-OLD receipts and doctrine changes are additions, not subtractions. |
| "regrowing" (`83 → 90 in 9 h, +7, all from receipts`) | **Confirmed in shape, ±2 in absolute number** | The +7 / 9-hour pattern matches the prior P1.4's `R0 sup receipt 69 → 76` measurement from `2828be05` (00:56) to `1a83affc` (10:32) — 9 h 36 min. The user's `83 → 90` absolute figures do not match the prior P1.4's `69 → 76` or my re-run's R-MID drift of `107 → 112` in 46 min. Most likely the user's `83 → 90` is a snapshot from a different zone or session memory; the *shape* (+7 in 9 h, 100% receipt zone) is the established finding. The 5-of-5 net additions in R-MID are receipts and tools of this half-life investigation itself (§3.2). `[C]` on the absolute-number reconciliation, `[B]` on the shape. |

`[S]` Three layered verdicts, all of which the prior P1.4 already
established and all of which this re-run confirms:

1. **The corpus's rulings *do* take effect at ruling time** for
   the zone they were made in (R1 doctrine 24→3 in the ruling
   commit; R2 and R3 landed with 0 and 2 lagging carriers; per
   the prior P1.4 §6).
2. **The corpus's rulings do not take effect outside the zone they
   were made in without a separate wave** (R1 public mirror flat
   at 9 for 15 days; R0 public mirror at 359 from 2026-07-19 to
   2026-08-06 00:56 — 18 days — collapsed by `2828be05`).
3. **The public mirror has no propagation path at all** — a
   ruling reaches the site if and only if someone dispatches a
   string sweep at the site (the prior P1.4 §6 finding 1,
   proved by the cross-check on `mf-281-the-replicator-decomposition/index.html`
   where a sweep opened the file and fixed one ruling on line 247
   while leaving a 15-day-stale ruling on line 89).

The staged P1.1 wire-up (`CENSUS_RECEIPT_WIRE_2026_08_06.md`) and
the shipped P1.2 gate (`RULING_LANDED_GATE_2026_08_06.md`) are
the two proposed mechanisms to make this state machine-verifiable
at ruling time. The prior P1.4 §7 recommendation (`carriers_at_ruling`
field) and P1.2's gate are *complementary*, not competing (per
`PROPAGATION_ARCHITECTURE_FINDING_2026_08_06.md:317-336`).

---

## 5 · The "+7 / +5 / +2" regrowth — receipts as carriers

The user reported "83 → 90 carriers in 9 hours, +7, all from
receipts documenting the sweep." This re-run confirms the
*mechanism* in three nested time windows:

| Window | Δ in `live` | Files added (all receipts / tools of the sweep) | Source |
|---|---:|---|---|
| 9 h 36 min (sweep → prior P1.4 HEAD) | **+7** | receipt zone 69 → 76 | prior P1.4 §4 |
| 46 min (SURGICAL_DEFECT → this session) | **+5** | 4 receipts + 1 instrument = 5 net new (1 re-touch excluded) | §3.2 of this finding |
| 2 min (this session, run 1 → run 2) | **+2** | `MUTATION_TEST_GATES_2026_08_06.md` + `PROPAGATION_ARCHITECTURE_FINDING_2026_08_06.md` written in the 2-minute window 10:53:06–10:53:09 | this session's re-runs |

**5 of 5 net new files in the 46-min window are receipts or
tools of the half-life investigation itself** (the P1.1 staged
proposal, the P1.2 gate, the P1.2 receipt, the prior P1.4 finding,
the mutation tests receipt). The P1.1 staged proposal *contains*
the pattern by design (it must name the pattern to propose the
field) — `CENSUS_RECEIPT_WIRE_2026_08_06.md:206, 289` both match.
The P1.2 gate *and* its receipt both match. The P1.4 finding
matches because the prior agent named the pattern to study it.
The mutation tests receipt matches because it names the
instrument it mutates.

**The regrowth is *load-bearing*, not contaminating.** An audit
receipt that does not name what it audits is not an audit. The
P1.4 prior finding's exact words: "The census's regrowth signal
is the sweep writing down that it swept. Doctrine did not relapse
by a single file." (`PROPAGATION_ARCHITECTURE_FINDING_2026_08_06.md:196-197`)

`[B]` file:line evidence:

- 5 new files in 46 min, all receipts / tools:
  - `00_HANDOFF/CENSUS_RECEIPT_WIRE_2026_08_06.md:206,289` — staged P1.1, mtime 10:48:04
  - `09_TOOLS/01_SCRIPTS/check_ruling_landed.py` (any line containing `RETIRED_TITAN_INFIX` import), mtime 10:49:21
  - `00_HANDOFF/RULING_LANDED_GATE_2026_08_06.md` (the receipt body), mtime 10:51:43
  - `00_HANDOFF/PROPAGATION_ARCHITECTURE_FINDING_2026_08_06.md:1-369`, mtime 10:53:06
  - `00_HANDOFF/MUTATION_TEST_GATES_2026_08_06.md`, mtime 10:53:09
- 1 re-touch (no net add): `09_TOOLS/01_SCRIPTS/check_foundation.py`, mtime 10:54:21, already in carrier set pre-SURGICAL_DEFECT.
- 0 doctrine files added in the 46-min window. (Confirmed by the
  `doctrine` column of the live-files-by-directory breakdown at
  the 10:54 census: `00_HANDOFF: 41, 11_UPLINK: 40, 12_PUBLIC_SITE: 13,
  14_THE_DISTILLATION: 5, 09_TOOLS: 4, 03_METHODOLOGY: 3, 10_SEED: 3,
  05_COSMOLOGY: 2, 00_V10_TIDY_CHAIN_CLOSURE_PENDING_K2.md: 1` —
  no new doctrine folder appears in this 46-min window.)

---

## 6 · What I could not do (per §0.6 read-only)

- **No commits.** K2 disposes; this is a finding, not a receipt.
- **No file modifications.** The staged CENSUS_RECEIPT_WIRE was
  not touched; the 90_ARCHIVE/ tree was not entered; the 3
  uncommitted repair files were not touched; the 2 public_html
  meta-reference files were not edited (those are owner-gated per
  `RULING_LANDED_GATE_2026_08_06.md:202-220`); the
  `57_THE_POTENTIAL_READING.md` was not touched.
- **No mutation of the census script.** Per the staged P1.1's
  §0.6 constraint and the user's hard-stops, the script is
  unchanged.
- **The 3 public carriers that left the carrier set between
  10:09:40 and 10:56:07 are not enumerated.** No receipt on
  disk names the 3 that dropped; reconstructing the diff would
  require either git history lookups (the public_html files
  are unchanged in the working tree at this moment) or a
  running diff between two timestamps, which the script does
  not support. Flagged as `[C]`; flagged-not-papered.
- **No 2-second re-run was taken** in this session. The
  P1.1 staged proposal documented a +1 regrowth in 2 minutes
  (10:44:45 → 10:46:46); my session's 2-min delta (10:51:55 →
  10:54:03) is +2, consistent in shape but at the upper end
  of the rate. The rate is non-stationary, driven by the
  writing tempo of the agents currently working in 00_HANDOFF/.
  `[C]`

---

## 7 · Reconciliation with the prior P1.4 finding

This finding is a *re-run and verification* of the prior P1.4
measurement (`PROPAGATION_ARCHITECTURE_FINDING_2026_08_06.md`,
HEAD `1a83affc`, 2026-08-06 ~10:32 ICT), not a new measurement.

| Prior P1.4 finding | This re-run's verdict |
|---|---|
| "Spontaneous half-life effectively infinite. **True but tautological as stated.**" (§6) | **Confirmed.** R-OLD drift decomposition §3.1: the 18-day net reduction is -41% to -45% but concentrates in a single 9-second manual commit. |
| "R2 and R3 landed. Zero and two lagging carriers respectively, from a small surface." (§5) | **Confirmed in shape.** Different rulings, same architecture: P1.1 / P1.2 / P1.4 receipts all land in the receipt zone immediately and stay there. |
| "R1's public mirror did not move at all in fifteen days — 9 pages, 24 bare assertions" (§5) | **Confirmed.** R-OLD public 359 → 11 only via the 2828be05 sweep, 18 days after retirement. |
| "Sweeps are signature-scoped and file-blind" (§6) | **Confirmed.** Not in scope to re-prove; the prior P1.4's cross-check on `mf-281-the-replicator-decomposition/index.html` is the proof artifact. |
| "Every naive carrier census over-counts by roughly an order of magnitude" (§6) | **Confirmed.** R-OLD's 725 = 6 doctrine + 64 receipt + 359 public + 296 archive; the "naive" 725 conflates tombstone with bare use, in a ratio of ~120:1 (719 licensed / 6 doctrine). |
| "The +7 regrowth is entirely the repair apparatus" (§4) | **Confirmed in shape.** This re-run's R-MID: 5 of 5 net new in 46 min are receipts / tools of the sweep. |

The prior P1.4 finding stands. This re-run does not change any
claim, counter, or verdict. It re-establishes the same finding
on a different ruling (WO-SD-2026-08-06, this session's
SURGICAL_DEFECT) at a later timestamp (10:56 vs 10:32) and
through the now-shipping census instrument rather than the
prior agent's hand-rolled `git grep` decomposition.

---

## 8 · The one sentence

**The carrier set for the `⊙ = • × ○` retirement, the
SURGICAL_DEFECT ruling, and the synthetic "now" reference
moves only when a wave moves it: 18 days from retirement saw
the public carrier set 359 → 11 via a single 9-second manual
commit (`2828be05`), 46 minutes from SURGICAL_DEFECT saw the
`live` set 107 → 112 with 5-of-5 net additions receipts or
tools of this very half-life investigation, and 2 minutes
within this session saw +2 — the +7 / +5 / +2 regrowth is 100%
receipt / tool zone, doctrine unchanged, and the half-life is
infinite in the architectural sense the prior P1.4 already
established: files do not edit themselves; the corpus's
half-life for any retired form is the time between manual
waves, not an exponential decay.**

---

*Read-only finding. K2 disposes. The staged P1.1 wire-up
(`CENSUS_RECEIPT_WIRE_2026_08_06.md`) and the shipped P1.2 gate
(`RULING_LANDED_GATE_2026_08_06.md`) are the proposed mechanisms
to make the carrier set binding at ruling time. The prior P1.4
recommendation (`carriers_at_ruling` field at
`PROPAGATION_ARCHITECTURE_FINDING_2026_08_06.md:286-290`) is
complementary to P1.2. None of those is this finding's lane;
this finding is the empirical re-run, not a proposal.*
