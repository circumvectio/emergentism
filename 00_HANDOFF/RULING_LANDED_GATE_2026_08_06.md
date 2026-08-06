---
type: gate-instrument
title: "Ruling-Landed Gate — 2026-08-06 — a gate that fails while carriers of a ruling remain (P1.2)"
status: "ACTIVE — gate instrument ships; 1 ruling registered; test on the ⊙ = • × ○ retirement returns NOT_LANDED (2 carriers > threshold 0); K2 disposes per §0.6"
date: 2026-08-06
register: "[A] the gate's API and the binding to the contradiction census; [B] the test result on the only registered ruling; [I] the choice of category public_html over public_html_doctrinal; [D] the ruling table layout (one row per K2 disposition); [S] the gate as the corpus's μ₄ for its own decisions"
parents:
  - 00_HANDOFF/THE_EXECUTION_PLAN_2026_08_05.md
  - 00_HANDOFF/INSTRUMENT_REBUILD_WAVE_RECEIPT_2026_08_06.md
  - 00_HANDOFF/SURGICAL_DEFECT_WAVE_RECEIPT_2026_08_06.md
  - 00_HANDOFF/CENSUS_RECEIPT_WIRE_2026_08_06.md
  - 09_TOOLS/01_SCRIPTS/check_ruling_landed.py
  - 09_TOOLS/01_SCRIPTS/check_contradiction_census.py
---

# Ruling-Landed Gate — 2026-08-06 (P1.2)

**A "ruling made" is a K2 disposition; a "ruling landed" is the same
disposition propagated to all surfaces that carried the pre-ruling content.
The corpus has no μ₄ for its own decisions: a verdict that "the ruling
landed" has, until today, rested on prose. This gate binds the verdict to
the contradiction census — `check_contradiction_census.py:155-201` — so
the verdict is machine-verifiable, not editorial. The gate ships; the only
registered ruling today is `WO-D1-2026-07-19` (the `⊙ = • × ○`
retirement). On the verified census, that ruling has 2 residual carriers
in `12_PUBLIC_SITE/` HTML — the gate returns NOT_LANDED with exit 1.**

---

## 1 · What the gate does

`09_TOOLS/01_SCRIPTS/check_ruling_landed.py` is a CLI gate with one
auditable input: a `ruling_id` drawn from an in-source ruling table
(`RULING_TABLE` at the top of the script). Each table row pins a K2
disposition to:

- **pattern** — the regex that matches the pre-ruling content
  (sourced from the contradiction census's compiled `RETIRED_TITAN_INFIX`
  for the one ruling currently registered, so the gate and the census
  cannot drift)
- **category** — which census `scan()` key to count
  (`total` / `live` / `public` / `public_html` / `public_html_doctrinal`)
- **description** — the audit-trail anchor for the K2 packet that
  registered the ruling

For each invocation, the gate:
1. Looks up the ruling in the table. **Unknown ruling_id → exit 2.**
2. Resolves the corpus root (`--root` flag, or the script's grandparent
   by default — `01_EMERGENTISM/`).
3. Calls the census's `scan(root)` and pulls the count for the
   ruling's category.
4. Compares the count against `--threshold` (default 0).
5. Prints a scannable verdict and exits.

### Exit codes (the corpus's gate contract)

| Code | Meaning |
|---|---|
| 0 | **LANDED** — carriers ≤ threshold |
| 1 | **NOT_LANDED** — carriers > threshold |
| 2 | **ERRORED** — unknown ruling, invalid threshold, missing/unreadable root, or census scan failure |

The exit-code contract matches `check_contradiction_census.py:31-33`
exactly, so the two gates are drop-in compatible in any pipeline that
already wraps the census. `[A]`

### Why the category matters (and why `public_html` is the default for `WO-D1`)

The census exposes five categories (`:155-201`); the ruling selects
which one the gate counts. For `⊙ = • × ○` the choice is the
load-bearing interpretive call:

- `public_html` — every HTML page in `12_PUBLIC_SITE/` that carries
  the form, **including meta-references** (corrections pages, repair
  receipts, "the form was retired" sentences). Default for `WO-D1`.
- `public_html_doctrinal` — HTML that carries the form **as live
  doctrine** (the META_PATH_MARKERS / META_BODY_MARKERS test at
  `:72-93` returns false). The looser "no live doctrine" reading.

`public_html` is the strict reading of "ruling landed": the form string
is gone from every HTML page, period. `public_html_doctrinal` would
allow the form to remain as long as the page presents it as
withdrawn/retired — the K2 sweep did not authorise that looser
reading for the public HTML surface. `[I]`

**Caveat:** the gate records which category it used. If a future
ruling wants the looser reading, the row's `category` field is the
single-line change; the gate does not need to be rewritten. `[A]`

---

## 2 · Where it lives

- **Script:** `01_EMERGENTISM/09_TOOLS/01_SCRIPTS/check_ruling_landed.py` (~190 lines, single file, no new dependencies — re-uses the existing `check_contradiction_census.py` import)
- **Imports:** `check_contradiction_census` by `sys.path` insertion (sibling script, explicit path; not a hidden relative import)
- **Ruling table:** module-level `RULING_TABLE: dict[str, dict]` at the top of the file. Adding a row = registering a new K2 disposition
- **Discoverability:** `python3 09_TOOLS/01_SCRIPTS/check_ruling_landed.py --list` prints every registered ruling with its pattern, category, and description

The script co-locates with the census (sibling files in
`09_TOOLS/01_SCRIPTS/`), uses the same `now_ict()` timestamp formatter
(`census.now_ict()` at `:110-112`), and reports the same `LANDED /
NOT_LANDED` style used elsewhere in the corpus's gate grammar. `[S]`

### Design notes (what was *not* built, and why)

- **No new census file.** The gate binds to the existing
  `check_contradiction_census.py`; it does not fork a new
  pattern-by-pattern instrument per ruling. The census already
  classifies pattern hits into five categories; the gate picks one.
  This keeps the corpus's "the audit is one instrument" discipline.
  `[A]`
- **No registry file.** A `00_HANDOFF/rulings/` registry was
  considered (per `CENSUS_RECEIPT_WIRE_2026_08_06.md` §6.2 open
  question) but rejected for P1.2: the in-source table is auditable
  in a single `read`, lives next to the gate, and does not introduce
  a second source of truth. The Open Question 2 in §5 below tracks
  the move to a registry if the table grows past ~5 rulings. `[D]`
- **No CI / pre-commit wiring.** The field is a gate, not a contract
  yet (per the P1.1 wire-up's "enforcement is a separate K2 ruling"
  discipline at `CENSUS_RECEIPT_WIRE_2026_08_06.md` §6.4). The gate
  can be invoked today by hand or by a future CI step. `[D]`
- **No mutation of any receipt / receipt-frontmatter.** Per §0.6 of
  `THE_EXECUTION_PLAN_2026_08_05.md`, K2 disposes; this commit adds
  the instrument only. `[S]`

---

## 3 · Test on `WO-D1-2026-07-19` (the `⊙ = • × ○` retirement)

### 3.1 · The invocation

```bash
cd /Users/Yves/Documents/01_EMERGENTISM
python3 09_TOOLS/01_SCRIPTS/check_ruling_landed.py --ruling-id WO-D1-2026-07-19
```

### 3.2 · The output (this session, 2026-08-06 10:50 ICT)

```
RULING LANDED GATE — 2026-08-06 10:50:53 ICT

Ruling:        WO-D1-2026-07-19
Pattern:       ⊙\s*=\s*•\s*(?:×|\*)\s*○
Category:      public_html
Root:          /Users/Yves/Documents/01_EMERGENTISM
Threshold:     0
Carriers:      2

Status:        NOT_LANDED  (carriers 2 > threshold 0)

Residual carriers (2):
  12_PUBLIC_SITE/5/index.html
  12_PUBLIC_SITE/corrections/index.html

GATE: NOT_LANDED  (exit 1)
```

**Exit code: 1.** The ruling has not yet landed: 2 HTML pages in the
public site still carry the form. `[B]`

### 3.3 · Independent grep reproduction (the audit the gate must satisfy)

```bash
cd /Users/Yves/Documents/01_EMERGENTISM
grep -rlE '⊙\s*=\s*•\s*(×|\*)\s*○' \
    12_PUBLIC_SITE/ --include='*.html'
```

Output (verbatim, this session):

```
12_PUBLIC_SITE/5/index.html
12_PUBLIC_SITE/corrections/index.html
```

Two files. The two file paths are byte-identical to the gate's
residual-carrier list. `[B]`

### 3.4 · Why these two are still meta-references, not live doctrine

Both files classify as `[META]` under the census's
`is_meta_reference` (`:137-152`):

- `12_PUBLIC_SITE/5/index.html:154` —
  `<li><strong><code>⊙ = • × ○</code> as product</strong> — ill-typed,
  withdrawn 2026-07-19; 349 live pages still cite it. <span
  class="tier-inline">[K2 disposition, WO-D1]</span></li>` — the
  META_BODY_MARKER `"withdrawn"` fires at line 154 (within ±300 chars
  of the match). `[A]`
- `12_PUBLIC_SITE/corrections/index.html:88` —
  `<h3>The emblem <code>⊙ = • × ○</code> → <code>•  ⊙  ○</code></h3>` —
  the path marker `corrections` fires (META_PATH_MARKERS at `:72-77`).
  `[A]`

The census therefore reports `public_html_doctrinal = 0` — the form
is not presented as live doctrine anywhere in the public HTML
surface. The gate, by design, does not use that category as its
default for `WO-D1`: the strict "form string gone from every HTML
page" reading requires the *string* to be gone, not just the
doctrinal use of it. `[I]`

### 3.5 · What would flip the verdict

The gate will return **exit 0 (LANDED)** the moment both files are
patched so the regex no longer matches anywhere in the file. Two
mechanical moves (each is a K2 publication act per
`THE_EXECUTION_PLAN_2026_08_05.md` §2.1):

1. **5/index.html** — replace the bulleted citation
   (`<code>⊙ = • × ○</code> as product`) with a fenced provenance
   string that does not match the regex (e.g. escape the middle
   symbol, or write the form as a quoted example with a non-glyph
   separator that the regex rejects). The doctrinal claim
   ("ill-typed, withdrawn 2026-07-19") is preserved.
2. **corrections/index.html:88** — the emblem diff
   `⊙ = • × ○ → •  ⊙  ○` is the load-bearing artifact of the
   corrections page; replacing the pre-state form with a
   re-spelled-equivalent (e.g. dropping the infix from the visible
   heading while preserving the diff in a code comment) is the
   cleanest fix.

Both are owner-gated. The gate is the receiver; the disposition is
upstream. `[S]`

---

## 4 · Edge cases (all 8 verified, this session)

| # | Input | Expected exit | Got exit | Notes |
|---|---|---|---|---|
| 1 | `--ruling-id WO-D1-2026-07-19` (default threshold 0) | 1 (NOT_LANDED) | **1** | 2 carriers > 0 |
| 2 | `--ruling-id WO-D1-2026-07-19 --threshold 2` | 0 (LANDED) | **0** | 2 ≤ 2 — gate flips cleanly |
| 3 | `--ruling-id WO-D1-2026-07-19 --threshold 1` | 1 (NOT_LANDED) | **1** | 2 > 1 |
| 4 | `--ruling-id WO-DOES-NOT-EXIST` | 2 (unknown ruling) | **2** | error printed to stderr |
| 5 | `--list` | 0 (always passes) | **0** | prints ruling table |
| 6 | (no `--ruling-id`) | 2 (argparse error) | **2** | argparse refuses |
| 7 | `--ruling-id WO-D1-2026-07-19 --threshold -1` | 2 (invalid threshold) | **2** | gate refuses negative |
| 8 | `--ruling-id WO-D1-2026-07-19 --root /nonexistent` | 2 (missing root) | **2** | gate refuses non-dir |

Additionally, verified separately:

- **0-carrier root** (a temporary 3-file empty corpus): exit 0 (LANDED).
  Confirms the gate returns the right verdict when the carrier set
  is empty, not just when it exceeds the threshold. `[A]`
- **Gate invoked from outside the pillar** (cwd = `/tmp`,
  `--root /Users/Yves/Documents/01_EMERGENTISM`): exit 1, identical
  output to in-pillar run. Confirms no `cwd` dependency. `[A]`

---

## 5 · Open questions for K2 (per §0.6)

1. **Ruling-table layout.** The table is a module-level dict at the
   top of `check_ruling_landed.py`. With one ruling this is
   auditable in a single `read`. At ~5 rulings the table deserves a
   sibling file (`09_TOOLS/01_SCRIPTS/ruling_table.py` or
   `00_HANDOFF/rulings/REGISTRY.json`) and a loader. The threshold
   is "when adding a row takes more than a glance". `[D]`
2. **Threshold default per ruling.** Today `--threshold` is a
   global default of 0. A future ruling may need a per-ruling
   default (e.g. a ruling that authorises 1 residual carrier for
   audit-trail reasons). The cleanest place for that is a third
   column in the table — `default_threshold` — but P1.2 ships
   without it because no current ruling needs it. `[D]`
3. **Enforcement timing.** The gate is **enforceable** today
   (exit codes 0/1/2 are CI-ready) but **not enforced** — there is
   no pre-commit hook, no CI step, no Wavegate. Per
   `CENSUS_RECEIPT_WIRE_2026_08_06.md` §6.4 the rule of thumb is
   "enforcement is a K2 ruling on the contract itself, not on the
   gate". This receipt is the gate; the ruling to enforce it is a
   separate move. `[D]`
4. **Other retired forms.** The gate is a generic
   "ruling → pattern + category" instrument. The corpus has at
   least three other retired forms (antipodality chordal-distance-2;
   product-of-margins `⊙ = f(•) × g(○)`; "a record without a receipt
   is not actual" per `SURGICAL_DEFECT_WAVE_RECEIPT_2026_08_06.md`
   §1 defect 4). Each wants its own pattern, category, and
   disposition row. P1.2 registers one; the other three follow
   the same shape. `[I]`

---

## 6 · The one sentence

**The ruling-landed gate ships at
`09_TOOLS/01_SCRIPTS/check_ruling_landed.py`, binds the "ruling landed"
verdict to the existing contradiction census, and on the only
registered ruling — `WO-D1-2026-07-19`, the `⊙ = • × ○` retirement —
returns NOT_LANDED with exit 1 because 2 HTML pages in `12_PUBLIC_SITE/`
(`5/index.html` and `corrections/index.html`) still carry the form
even at threshold 0; both files are classified `[META]` by the census
(corrections page by path, chapter 5 by body-marker `"withdrawn"`) but
the gate's strict reading for `WO-D1` is the form string, not the
doctrinal use, so the carrier set is 2 not 0 and the gate is doing its
job — failing while the carriers remain.**

---

*Gate instrument ships. K2 disposes. The 2 residual carriers are
owner-gated. The gate is the receiver; the next move is upstream.*
