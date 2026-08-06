---
type: receipt-wire-proposal
title: "Census Wire-up to Receipt Frontmatter — P1.1 of the 2026-08-06 plan"
status: "OPEN — proposed schema, not yet applied to any receipt; K2 disposes per §0.6"
date: 2026-08-06
register: "[S] this proposal makes the corpus's own decision metric machine-verifiable; [A] the census script API; [B] the worked example reproduces the live count at the time of writing; [D] the field schema, staged; [I] the interpretation of 'ruling landed' = 'carrier set at ruling'"
parents:
  - 01_EMERGENTISM/00_HANDOFF/SURGICAL_DEFECT_WAVE_RECEIPT_2026_08_06.md
  - 01_EMERGENTISM/09_TOOLS/01_SCRIPTS/check_contradiction_census.py
  - 01_EMERGENTISM/00_HANDOFF/THE_EXECUTION_PLAN_2026_08_05.md
  - 01_EMERGENTISM/00_HANDOFF/INSTRUMENT_REBUILD_WAVE_RECEIPT_2026_08_06.md
may_sign: false
may_authorize: false
authority_effect: none
---

# Census Wire-up to Receipt Frontmatter — P1.1

**The corpus's own rulings are now instrumented (census script ships; the
new headline is contradiction census + citation completeness) but the
receipt frontmatter still has no machine-verifiable carrier-set field.
A "ruling landed" verdict today rests on the receipt's prose. P1.1
proposes a required `carrier_set_at_ruling` field that binds the verdict
to the census snapshot at the moment of ruling. The proposal is staged;
no receipt is changed by this commit, the K2 disposes per §0.6.**

---

## 1 · The gap (why)

A ruling's "carrier set" is the set of files that still carry the
pre-ruling content. The contradiction census script
(`09_TOOLS/01_SCRIPTS/check_contradiction_census.py:155-201`) already
classifies pattern hits into five categories — `total`, `live`,
`public`, `public_html`, `public_html_doctrinal` — and reports them
with timestamp + file paths + exit code `[A]`. The script is the audit
that does not miss the corpus's own work `[B]` (SURGICAL_DEFECT §3).
The receipt template has no required field for that snapshot
`[A]`. Result: a receipt dated 2026-08-06 quotes the figures that
held *when the receipt was written*; a reader six months later cannot
tell from the receipt alone whether the ruling still held at the
moment of writing, and a re-run today confounds "ruling landed then"
with "ruling holds now". `[I]`

The fix is a required frontmatter field that pins the carrier set to
the ruling's datetime, with a `ruling_id` that names the ruling
itself (not the receipt). The receipt becomes a finding, not a
souvenir.

## 2 · The proposed schema (the `carrier_set_at_ruling` field)

```yaml
# REQUIRED on every wave-receipt / repair-receipt / external-contact
# receipt produced by a ruling that affects the corpus. Re-runnable:
# any future reader can re-run the census and compare the field
# against today's run.

carrier_set_at_ruling:
  total: 422                    # int — every pattern hit in 01_EMERGENTISM
  live: 107                     # int — excludes 90_ARCHIVE / 91_COMPATIBILITY
  public: 13                    # int — files under 12_PUBLIC_SITE/ that hit
  html_as_doctrinal_use: 0      # int — public HTML files that are NOT meta-refs
  timestamp: 2026-08-06T10:44:45+07:00   # ISO8601, ICT (UTC+7), the ruling moment
  ruling_id: "WO-SD-2026-08-06" # the ruling itself, not the receipt
  census_script: 09_TOOLS/01_SCRIPTS/check_contradiction_census.py
```

**Why four counts, not five.** The census script's `public_html`
key (HTML files in the public site that hit) is an intermediate
step — every public_html that is not a meta-reference is exactly
`html_as_doctrinal_use`; every meta-reference is provenance `[A]`
(META_PATH_MARKERS, META_BODY_MARKERS at `check_contradiction_census.py:72-93`).
The receipt's load-bearing claim is *doctrine*, not *string presence*,
so `public_html` is omitted by design. Recording it would be
information already implied by the difference
`public_html − html_as_doctrinal_use = meta-reference count`. `[I]`

**Why `ruling_id`, not `receipt_id`.** The receipt cites the ruling;
it is not the ruling. A ruling can be cited by many receipts
(SURGICAL_DEFECT is itself a parent of nothing yet, but D2/D3/D4/D5
each cite the same rungs repair plan). The ruling_id is the durable
handle. `[S]`

**Why ISO8601, not "YYYY-MM-DD HH:MM:SS ICT".** The census script's
`now_ict()` (`check_contradiction_census.py:110-112`) emits the
human-readable ICT form for the audit trail; the frontmatter uses
ISO8601 because the frontmatter is the *machine* contract. `[A]`

**Why `timestamp` and not `date`.** `date` is the calendar day the
receipt was authored; `timestamp` is the wall-clock the carrier set
was captured. On a wave that takes hours, the two can differ; the
schema names both. `[I]`

## 3 · Before / after — SURGICAL_DEFECT as the worked example

**Before** (current SURGICAL_DEFECT frontmatter,
`00_HANDOFF/SURGICAL_DEFECT_WAVE_RECEIPT_2026_08_06.md:1-22`):

```yaml
---
type: wave-receipt
title: "Surgical-Defect Wave Receipt — 2026-08-06 — the four defects the rungs repair waves created"
status: "ACTIVE — surgical-defect wave closed; 4/4 defects killed; ..."
date: 2026-08-06
register: "[S] this receipt consolidates ... [A] each defect's kill argument; [I] the methodological generalization; [B] the §0.6 hazard that fired on the assistant's own ledger"
parents:
  - 00_HANDOFF/D2_REPAIR_WAVE_RECEIPT_2026_08_05.md
  - 00_HANDOFF/D3_REPAIR_WAVE_RECEIPT_2026_08_05.md
  - 00_HANDOFF/D4_REPAIR_WAVE_RECEIPT_2026_08_05.md
  - 00_HANDOFF/D5_REPAIR_WAVE_RECEIPT_2026_08_05.md
  - 00_HANDOFF/INSTRUMENT_REBUILD_WAVE_RECEIPT_2026_08_06.md
  - 00_HANDOFF/CHAPTER_CONTENT_WAVE_RECEIPT_2026_08_05.md
  - 00_HANDOFF/antipodality_fix_report.md
  - 14_THE_DISTILLATION/00_THE_RUNGS_2026_08_05.md
  - 12_PUBLIC_SITE/00_THE_RUNGS_2026_08_05.md
  - 05_COSMOLOGY/03_FORMAL_SYSTEM/56_THE_PRODUCT_FORM_OF_THE_BALANCE.md
  - 10_SEED/01_THE_SEED_LADDER/ASCENT_D2_GEOMETRY_2026_08_05.md
  - 10_SEED/01_THE_SEED_LADDER/ASCENT_D6_RETURN_AND_O_2026_08_05.md
  - 05_COSMOLOGY/01_THE_TRANSCENDENTAL_TRINITY/51B_FINITY_L_C1_KILL_2026_08_05.md
  - 09_TOOLS/01_SCRIPTS/check_contradiction_census.py
---
```

The `parents` list cites the census script as a parent — which says
*the census was an input*, not *the carrier set at ruling*. The
prose §3 quotes the figures ("422 / 107 / 16 / 2") inline; a
re-run today returns 422 / 107 / **13** / 2 — the public site count
moved by 3 between the receipt and now, and the frontmatter has no
record of the snapshot. `[B]`

**After** (proposed; new fields in **bold** below, others unchanged):

```yaml
---
type: wave-receipt
title: "Surgical-Defect Wave Receipt — 2026-08-06 — the four defects the rungs repair waves created"
status: "ACTIVE — surgical-defect wave closed; 4/4 defects killed; ..."
date: 2026-08-06
register: "[S] this receipt consolidates ... [A] each defect's kill argument; [I] the methodological generalization; [B] the §0.6 hazard that fired on the assistant's own ledger"
parents:
  - 00_HANDOFF/D2_REPAIR_WAVE_RECEIPT_2026_08_05.md
  - 00_HANDOFF/D3_REPAIR_WAVE_RECEIPT_2026_08_05.md
  - 00_HANDOFF/D4_REPAIR_WAVE_RECEIPT_2026_08_05.md
  - 00_HANDOFF/D5_REPAIR_WAVE_RECEIPT_2026_08_05.md
  - 00_HANDOFF/INSTRUMENT_REBUILD_WAVE_RECEIPT_2026_08_06.md
  - 00_HANDOFF/CHAPTER_CONTENT_WAVE_RECEIPT_2026_08_05.md
  - 00_HANDOFF/antipodality_fix_report.md
  - 14_THE_DISTILLATION/00_THE_RUNGS_2026_08_05.md
  - 12_PUBLIC_SITE/00_THE_RUNGS_2026_08_05.md
  - 05_COSMOLOGY/03_FORMAL_SYSTEM/56_THE_PRODUCT_FORM_OF_THE_BALANCE.md
  - 10_SEED/01_THE_SEED_LADDER/ASCENT_D2_GEOMETRY_2026_08_05.md
  - 10_SEED/01_THE_SEED_LADDER/ASCENT_D6_RETURN_AND_O_2026_08_05.md
  - 05_COSMOLOGY/01_THE_TRANSCENDENTAL_TRINITY/51B_FINITY_L_C1_KILL_2026_08_05.md
  - 09_TOOLS/01_SCRIPTS/check_contradiction_census.py
carrier_set_at_ruling:            # NEW — required on every wave/repair/external-contact receipt
  total: 422
  live: 107
  public: 16
  html_as_doctrinal_use: 0
  timestamp: 2026-08-06T10:09:40+07:00   # file mtime = the ruling moment (proxy)
  ruling_id: "WO-SD-2026-08-06"
  census_script: 09_TOOLS/01_SCRIPTS/check_contradiction_census.py
---
```

The `public: 16` figure is the value the SURGICAL_DEFECT receipt
itself reports at §3 line 55 (the moment SURGICAL_DEFECT was
authored, ~10:09 ICT, file mtime) `[B]`. The current re-run
returns 13 — a delta of 3 in the public site count between the
ruling and now `[B]`. The new field pins the 16 to the ruling's
mtime; a future re-run can compare its own numbers to the 16,
and the deltas (3 files moved out of the carrier set after the
ruling) become auditable, not invisible. `[I]`

**Naming note:** the proposed `ruling_id` value `WO-SD-2026-08-06`
follows the existing wave-operation tag pattern visible in the
frontmatter (`WO_C1_OPENING_REPORT_BIOLOGICAL_PAIR_2026_08_05.md`,
`WDO-D1` in the census script docstring) `[B]`. A ruling-id
registry would be a follow-up, not part of P1.1.

## 4 · Where the field comes from (census script API)

The census script exposes a single Python entry point,
`scan(root: Path) -> dict[str, list[Path]]`
(`check_contradiction_census.py:155-201`). The returned dict has
five keys:

| Script key | Frontmatter key | Notes |
|---|---|---|
| `total` | `total` | identical |
| `live` | `live` | identical (K3 archive-first applied) |
| `public` | `public` | identical (`12_PUBLIC_SITE/` only) |
| `public_html` | (omitted) | intermediate step; see §2 |
| `public_html_doctrinal` | `html_as_doctrinal_use` | renamed for human-readability; the "DOCTRINAL" tag in the report (`check_contradiction_census.py:252`) maps to the same classification |

The script also exposes `now_ict()` (`:110-112`) for the timestamp
in ICT; the frontmatter normalises this to ISO8601 (the script's
output is for the audit trail; the frontmatter is for the machine
contract). `[A]`

**Out of scope (this commit does not do these things):**
- the census script itself is unchanged (P1.1 constraint, K2 §0.6)
- no existing receipt is back-filled; back-fill is a separate K2 ruling
- no CI / pre-commit gate is added; the field is a frontmatter
  *contract* first, an *enforcement* second
- the corpus's other retired forms (e.g. `⊙ = • × ○` is one of
  several; the antipodality carrier set, the product-of-margins
  carrier set, the "a record without a receipt is not actual" carrier
  set) would each need their own census instruments and their own
  `census_script:` references. P1.1 is the *first*; the rest follow
  the same shape. `[I]`

## 5 · Verification grep (the proof the field is required, not aspirational)

A gate that asserts the field is present in every wave-receipt
frontmatter, and that `timestamp` parses as ISO8601, would
look roughly like:

```bash
# 1. List every wave-receipt-style file under 00_HANDOFF/
grep -rl '^type: wave-receipt\|^type: repair-receipt\|^type: external-contact' \
  /Users/Yves/Documents/01_EMERGENTISM/00_HANDOFF/ \
  --include='*.md'

# 2. For each, assert carrier_set_at_ruling is present and timestamp is ISO8601
python3 -c '
import re, sys, pathlib
for p in sys.argv[1:]:
    body = pathlib.Path(p).read_text()
    m = re.search(r"^carrier_set_at_ruling:", body, re.M)
    if not m:
        print(f"FAIL  {p}  — no carrier_set_at_ruling field")
        continue
    ts = re.search(r"timestamp:\s*(\S+)", body[m.end():m.end()+400])
    if not ts or not re.match(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}", ts.group(1)):
        print(f"FAIL  {p}  — timestamp not ISO8601: {ts.group(1) if ts else None}")
        continue
    print(f"PASS  {p}  — {ts.group(1)}")
' <files>
```

Expected today (with P1.1 unapplied): `FAIL` on every wave-receipt
in `00_HANDOFF/` (D2, D3, D4, D5, INSTRUMENT_REBUILD, CHAPTER_CONTENT,
SITE_REVISION, SURGICAL_DEFECT) — which is the gap P1.1 names.
`[A]`

**Census re-run today** (2026-08-06 10:44:45 ICT, this session — note
this is a *re-run*, not the snapshot at the SURGICAL_DEFECT ruling;
the ruling's snapshot is the file mtime 10:09:40, see §3):

```
Total files in 01_EMERGENTISM (pattern hits): 422
Live files (exclude 90_ARCHIVE, 91_COMPATIBILITY): 107
Public site (12_PUBLIC_SITE/): 13
HTML pages in public site: 2
HTML pages as live doctrinal use: 0
Status: FAIL  (live=107, public=13, html-doctrinal=0)
```

A second re-run at 10:46:46 returned 423 / 108 / 13 / 2 — total
and live each moved by +1 between two runs in the same session
`[B]`. **The carrier set is a moving target between runs; only the
snapshot at the moment of the ruling is binding on the ruling.**
That is the gap P1.1 names.

The discrepancy with SURGICAL_DEFECT §3 (16 public at the ruling
vs 13 public at the re-run) is itself a finding `[B]`: three
files moved out of the carrier set between the ruling and the
re-run. The `carrier_set_at_ruling` field is what would let a
future reader see "the ruling was written against a 16-file
carrier set; today the count is 13; the delta is 3 and these
3 files are: …". The current frontmatter has no such hook.

## 6 · Open questions for K2 (per §0.6)

1. **Back-fill or forward-only?** The 8 wave-receipts already on
   disk (D2/D3/D4/D5/INSTRUMENT_REBUILD/CHAPTER_CONTENT/SITE_REVISION/SURGICAL_DEFECT)
   pre-date P1.1. Should they be back-filled with the
   `carrier_set_at_ruling` value that held at the time of *their*
   ruling (recoverable by re-running the census against the pre-ruling
   HEAD), or only forward-rulings carry the field? `[D]`
2. **Ruling-id registry.** P1.1 proposes ad-hoc ruling_ids
   (`WO-SD-2026-08-06`). A registry under `00_HANDOFF/rulings/`
   with one file per ruling_id would let the frontmatter field
   resolve to a longer ruling text. Out of P1.1 scope, but the
   naming convention should be settled before back-fill so the
   convention is stable. `[D]`
3. **Other retired forms.** The script is bound to the retired
   Titan infix (`⊙ = • × ○`). The corpus has at least three other
   retired forms that would each want a census and a `census_script:`
   pointer (antipodality chordal-distance-2; product-of-margins
   `⊙ = f(•) × g(○)`; "a record without a receipt is not actual").
   P1.1 is one schema; the other three are a separate, larger ruling.
   `[I]`
4. **Enforcement timing.** The field is a *contract* in P1.1.
   Enforcement (a CI / pre-commit check) is a P2 or later move —
   enough rules have been added to the corpus's release path
   (RELEASE_PLAN §3.4, §3.8) that adding a 9th without a K2 ruling
   on the contract itself is over-reach. `[D]`

## 7 · The one sentence

**The contradiction census instrument already computes the four
counts that make a "ruling landed" verdict machine-verifiable;
the receipt frontmatter does not currently require a
`carrier_set_at_ruling` field that pins the verdict to the census
snapshot at the moment of the ruling, and P1.1 proposes that
field as a required frontmatter contract, worked through the
SURGICAL_DEFECT receipt, without applying it to any receipt and
without changing the census script.**

---

*Proposal staged. K2 disposes. The census script continues to
report. The next receipt that omits the field is a finding, not
a fault — the field is a contract, not a gate, until K2 rules
otherwise.*
