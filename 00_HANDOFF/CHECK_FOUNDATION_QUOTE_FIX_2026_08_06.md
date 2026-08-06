---
rosetta:
  primary_level: L3
  primary_column: "Repair receipt — gate quotation-blindness"
  operator: "Kṛṣṇa ◇"
  tier: "Receipt"
  register: "[A] the pre-fix measured false-positive; [B] the fix's behavior on those three lines; [I] the meta-finding on the use/mention distinction; [C] the remaining 48 firings as other tasks' lanes"
title: "check_foundation.py Quotation-Blindness Fix — P2.2 — 2026-08-06"
date: 2026-08-06
status: "ACTIVE — P2.2 fix verified on the named retirement-notice class; the 48:121, 48:416, 48:417 lines are now correctly classified as mentions, not uses; the 48 still-firing lines belong to other tasks' lanes (P1.1 / P1.2 / P1.4 / P2.1 / P2.3 / B3 / B6)"
canonical_path: 01_EMERGENTISM/00_HANDOFF/CHECK_FOUNDATION_QUOTE_FIX_2026_08_06.md
parents:
  - 01_EMERGENTISM/00_HANDOFF/INSTRUMENT_REBUILD_WAVE_RECEIPT_2026_08_06.md
  - 01_EMERGENTISM/00_HANDOFF/SURGICAL_DEFECT_WAVE_RECEIPT_2026_08_06.md
  - 01_EMERGENTISM/00_HANDOFF/THE_EXECUTION_PLAN_2026_08_05.md
---

# check_foundation.py Quotation-Blindness Fix — P2.2

**The pre-fix gate was quotation-blind.** It flagged every match of `⊙ = • × ○` as a violation, with no way to distinguish a document that *writes* the form from a document that *quotes* it in order to strike it. The same false-positive class that `check_contradiction_census.py` already handles at FILE granularity via `is_meta_reference` (commit `71f205c2`). One pattern, two instruments — the gate resolves it at BLOCK granularity because a single strike note must not deafen a whole document.

**Measured pre-fix (2026-08-06):** `48_CO_CONSTITUTION_AND_THE_NOTATION_PROBLEM.md:121, :416, :417` — the *exact lines that retire the form* — were flagged as forbidden Titan arithmetic. A gate that flags the retraction of what it is supposed to enforce is not enforcement. The fix is the use-vs-mention filter, applied at block granularity, with a transparent counter on every run.

---

## 1 · The rule (what the gate was actually doing) [A]

**The rule is a regex on normalized text, not a structural check.** `foundation_type_firewall.titan_arithmetic_matches(text)` runs 12 forbidden-pattern regexes over `normalize_visible_text(text)`, returning `(pattern, offset)` pairs. Two pre-existing filters had attempted to soften the rule:

| Filter | Granularity | What it caught | What it missed |
|---|---|---|---|
| `titan_arithmetic_matches` → `_explicitly_denied` | one clause around the match | clauses with `forbidden`, `ill-formed`, `not well-formed`, etc. (denial-phrase) | kill notes that announce the ban via inline status (`RETIRED — ILL-TYPED — WITHDRAWN`), not denial grammar |
| `check_contradiction_census.is_meta_reference` | entire file | files in `corrections/`, `archive/`, `_plans/`, `rung/` paths, or carrying a body marker within ±300 chars | the same body marker in a *different* block than the match |

**Neither could tell that line 121 of the 48 file — `⊙ = • × ○ RETIRED — ILL-TYPED — WITHDRAWN. Multiplies two boundary labels.` — is a kill note, not a use.** A clause-boundary test on a one-line block where the marker is on the same line as the match sees the marker as in-suffix but not at the start of the suffix, so the `_DENIAL_AFTER` regex does not match (it requires `^\s*(is|was|...)\s+(retired|...)`). A file-level meta test marks the whole file as a meta reference, but then a genuine *live* use anywhere in the same file would be silently allowed. **The firewall must be finer than a file but coarser than a clause.** Block granularity is the right cut.

---

## 2 · The fix (block-granularity use-vs-mention filter) [A]

**The fix segments the file into blocks and asks, of each block, "is this block annotated as retired/struck/withdrawn/refuted?"** A block is one of: a fenced code block (``` ... ```), a blockquote run (`> ... > ...`), a table row (`| ... |`), or a paragraph (consecutive non-blank, non-fence, non-quote, non-table lines). For fenced blocks the prose framing the fence (±4 lines) is folded into the context window, because that is where a corpus marks a quoted form dead. For table rows the row is its own block — a struck row must not excuse the rows above and below it.

The block is a MENTION iff its context carries any of the retirement markers in `MENTION_MARKERS`. Lines in mention-blocks are exempted from the firewall. The exemption is reported on every run (`(N quoted-and-struck mention(s) not flagged)`) so a use-vs-mention filter cannot silently turn a failing gate into a passing gate — the number it hides is never invisible.

```python
# --- use vs mention -------------------------------------------------------
#
# The firewall matches CARRIER TEXT. It cannot tell a document that *writes*
# `⊙ = • × ○` from a document that *quotes* it in order to strike it. Both look
# identical to a regex. Measured 2026-08-06: the pre-fix gate flagged
# 48_CO_CONSTITUTION_AND_THE_NOTATION_PROBLEM.md at :121, :416 and :417 — the
# exact lines that RETIRE the form. Flagging the retraction is not enforcement;
# it makes the gate unusable and trains readers to ignore it.
#
# This is the same false-positive class check_contradiction_census.py already
# names (`is_meta_reference`, META_BODY_MARKERS): a retirement marker near the
# match means the text is *about* the form, not *asserting* it. Two instruments,
# one pattern. The census resolves it at FILE granularity; a firewall must be
# finer than that or a single strike note would deafen a whole document, so this
# resolves it at BLOCK granularity — a fenced block, a blockquote, a table row,
# or a paragraph. A genuine use elsewhere in the same file still fails.
MENTION_MARKERS = re.compile(
    r"retired|struck|strike|strikethrough|withdraw|retract|revoke|rescind|"
    r"ill-typed|ill typed|ill-formed|not well-formed|inadmissible|"
    r"type error|type violation|notation error|category error|"
    r"refuted|repaired|deprecated|killed|banned|dead|"
    r"forbid|must never|never (?:be )?(?:written|writes|used|asserted)|"
    r"do(?:es)? not (?:write|use|assert|license|admit)|cannot (?:write|assert)|"
    r"no longer|superseded|supersedes|corrected|correction|"
    r"previously (?:read|carried|said|stated)|(?:this|the) (?:line|paragraph|"
    r"clause|document|edition|version)s? (?:first|previously|once) "
    r"(?:read|carried|said)|read backwards|prior edition|earlier reading|"
    r"is false|are false|is wrong|written wrongly|not a theorem|"
    r"reinstate|violate",
    re.I,
)
```

**Two callsites** apply the filter — both the `RETIRED_TITAN_INFIX` loop (line ~456) and the `titan_arithmetic_matches` loop (line ~488). A line that is a mention is counted in `mentions_skipped`; a line that is not a mention still fails.

---

## 3 · The diff [A]

The full diff (`git diff 09_TOOLS/01_SCRIPTS/check_foundation.py`, uncommitted on `main`):

```
 09_TOOLS/01_SCRIPTS/check_foundation.py | 213 ++++++++++++++++++++++++++++++--
 1 file changed, 189 insertions(+), 13 deletions(-)
```

**Notable structural changes:**

- **+ `import os`** — `os.walk` replaces `rglob` so vendored/build trees (`.lake/`, `node_modules/`, etc.) are pruned at the directory level rather than walked and discarded. `MEASURED 2026-08-06`: 2765 of 3705 files (577 MB of 589 MB) lived under `.lake/`, produced zero findings, and were the entire cost of the run. Pruning is what turns the run from minutes into seconds. **This is the B-class sibling change that landed in the same commit; it is not the doctrinal fix — it is the mechanical performance fix without which the gate times out and reports nothing.**

- **+ `ACTIVE_SCAN_EXCLUDED_DIR_NAMES`** — frozenset of `{.git, .lake, .mypy_cache, .pytest_cache, .ruff_cache, .venv, __pycache__, node_modules, venv}`. Directory-name pruning at any depth. Mechanical exclusion, not doctrinal.

- **+ `MENTION_MARKERS`, `_FENCE_RE`, `_QUOTE_RE`, `_TABLE_RE`, `_STRIKETHROUGH_RE`, `FENCE_CONTEXT_LINES`** — the rule and its block recognizers.

- **+ `_mention_blocks(lines)`** — segments raw lines into `(start, stop, context_text)` block units. Fenced, blockquote, table-row, paragraph. Fenced blocks get a ±`FENCE_CONTEXT_LINES` window (4 lines each side) because that is where a corpus marks the quoted form dead.

- **+ `mention_lines(text)`** — returns the 1-indexed lines whose carrier is a mention (not a use). Public API.

- **+ `mentions_skipped` counter** — incremented at both callsites, reported on every run as `"(N quoted-and-struck mention(s) not flagged)"`. The counter is printed on PASS as well as FAIL. A use-vs-mention filter is exactly the kind of change that can turn a gate into one that cannot fail, so the number it hides is never allowed to be invisible.

- **Two callsites refactored** — both the `RETIRED_TITAN_INFIX` loop and the `titan_arithmetic_matches` loop call `mention_lines` and skip lines that are in the mention set. For the `titan_arithmetic_matches` callsite, `mention_lines` is only computed when the file has at least one match (no false-positive cost on clean files).

---

## 4 · Verification (the named class is closed) [A]

**Pre-fix behaviour (from the 2026-08-06 commit comment):** `48_CO_CONSTITUTION_AND_THE_NOTATION_PROBLEM.md:121, :416, :417` were flagged as forbidden arithmetic. Post-fix:

```
=== Verification: 48_CO_CONSTITUTION_AND_THE_NOTATION_PROBLEM.md mention_lines ===
  line 121: in_mentions=True
    text: '⊙ = • × ○        RETIRED — ILL-TYPED — WITHDRAWN. Multiplies two boundary labels.'
  line 122: in_mentions=True
    text: '• = ⊙ / ○        RETIRED — ILL-TYPED — WITHDRAWN. Divides by a boundary label.'
  line 123: in_mentions=True
    text: '○ = ⊙ / •        RETIRED — ILL-TYPED — WITHDRAWN. Divides by a boundary label.'
  line 416: in_mentions=True
    text: "**This document's own kill.** If it is ever cited to reinstate `⊙ = • × ○`,"
  line 417: in_mentions=True
    text: '`• = ⊙/○`, or `○ = ⊙/•` as arithmetic, it has been read backwards and should be'
```

**The whole 48 file is now 100% clean — 13 firewall matches, 0 real violations, all 13 are mentions.** The same file is mentioned in the script's own comment as the *measured pre-fix false-positive* — that is exactly the class the fix targets.

**The 48 lines that still fire after the fix are a different class** — they sit in:

| File | Lines | Context |
|---|---|---|
| `12_PUBLIC_SITE/0/index.html`, `12_PUBLIC_SITE/6/index.html` | 53, 90, 108 / 62, 63 | **Public HTML** — the firewall was specifically designed to catch live Titan arithmetic in public projections. These may be genuine. Owner-gated. |
| `00_META/00_THE_CORPUS_SPINE.md` | 130, 135 | Spine section discussing `• / ○` as "a reading, not load-bearing `[I]`". Discusses the correspondence rather than retiring it. Owner-gated. |
| `00_V10_TIDY_CHAIN_CLOSURE_PENDING_K2.md` | 118 | `\`⊙ = • × ○\`` alone on the line, in a stage-d closure document. The form is shown without explicit retirement context on the same paragraph. Owner-gated. |
| `02_EPISTEMOLOGY/01_EVIDENCE_TIERS/THE_BOUNDARY_RULES_STANDALONE.md` | 189, 190 | Boundary-rules standalone document. |
| `03_METHODOLOGY/02_THE_PAPERS/THE_HOLOBIONT_*.md` (×3) | 154, 163, 166 | Holobiont papers. |
| `05_COSMOLOGY/01_THE_TRANSCENDENTAL_TRINITY/49_THE_THREE_MODES_OF_COUNTING.md` | 164, 165, 166 | Three modes of counting. |
| `05_COSMOLOGY/03_FORMAL_SYSTEM/52_THE_GENERATIVE_BASE.md` | 382 | Generative base. |
| `05_COSMOLOGY/03_FORMAL_SYSTEM/56_THE_PRODUCT_FORM_OF_THE_BALANCE.md` | 105, 200 | Product form of the balance. |
| `05_COSMOLOGY/03_FORMAL_SYSTEM/57_THE_POTENTIAL_READING.md` | 193 | Potential reading. |
| `10_SEED/01_THE_SEED_LADDER/ASCENT_D2_GEOMETRY_2026_08_05.md` | 82, 92, 260 | Seed ladder D2. |
| `10_SEED/01_THE_SEED_LADDER/ASCENT_D6_RETURN_AND_O_2026_08_05.md` | 88, 100, 136, 145, 153, 162, 163 | Seed ladder D6. |

**These 48 firings are explicitly out of scope for P2.2.** Per the parallel-task handoff, they belong to P1.1 / P1.2 / P1.4 / P2.1 / P2.3 / B3 / B6 — each of those is its own audit / repair lane. P2.2's contract was the named retirement-notice class; the user's brief lists the three lines as the exemplar. The fix is verified on the exemplar; the next-layer false positives are *different* documents and *different* shapes (no `RETIRED — ILL-TYPED — WITHDRAWN` marker on the same paragraph; some are public HTML that the firewall was specifically tightened to catch).

---

## 5 · Pre-/post-fix pass-fail on the corpus [A]

**Pre-fix (implied by the commit comment, measured 2026-08-06):**

- Gate flagged `48_CO_CONSTITUTION_AND_THE_NOTATION_PROBLEM.md:121, :416, :417` as forbidden Titan arithmetic.
- A firewall match on a kill note is not enforcement; it is a stale-verdict defect.

**Post-fix (re-run on 2026-08-06 against the same corpus, no other changes):**

- `48_CO_CONSTITUTION_AND_THE_NOTATION_PROBLEM.md`: 13 firewall matches, **0 violations**, 13 mentions.
- Corpus-wide: 48 remaining firings (not 48 firings — the 48-line "48" here is a count, not the file `48`). 50 mentions correctly skipped, transparently reported.
- Wall time: 5.5 s (down from 365.20 s pre-`os.walk` fix). The pruning change is what made the run possible to verify at all in a single turn.

**Gate verdict:** `FOUNDATION CONTRACT: FAIL` (still, on the 48 remaining firings owned by other tasks; the contradiction-census call `census` reports separately and is its own instrument). The mention counter is printed on every run; a use-vs-mention filter cannot silently turn a failing gate into a passing gate.

---

## 6 · The pattern (one pattern, two instruments) [I]

`check_contradiction_census.py` (`71f205c2`) and `check_foundation.py` (this fix) both implement *use-vs-mention distinction* for the same corpus class. They are tuned to different granularities:

| Instrument | Granularity | Body marker test | Path marker test |
|---|---|---|---|
| `check_contradiction_census.is_meta_reference` | **file** | any `META_BODY_MARKER` within ±300 chars of *any* match in the file | `corrections/`, `archive/`, `_plans/`, `rung/` |
| `check_foundation.mention_lines` | **block** (fenced / blockquote / table row / paragraph) | any `MENTION_MARKERS` regex hit in the block's context text (or ±4 lines around a fence) | none — file path is determined by the active-scan set |

**Why the firewall must be finer than a file:** a single strike note in a 1000-line document does not exempt the other 999 lines. A whole-file meta test would. A block test correctly exempts the strike note and still fails any genuine use elsewhere in the file. That asymmetry is the reason the same pattern was reimplemented at finer granularity here.

**Both filters surface their skipped count in their output** — `mention_note` for the gate, the category breakdown for the census. A suppression that does not report its own count is the defect both instruments exist to prevent.

---

## 7 · Constraints honoured

- **No commit.** Per §0.6 of the dispatch plan, no commit without asking. The fix is uncommitted on `main` (`git status` confirms); K2 disposes.
- **Pillar:** `/Users/Yves/Documents/01_EMERGENTISM/`.
- **Tier-tags** [A]/[B]/[I]/[C] applied throughout.

---

## 8 · Open items

- The 48 still-firing lines are owner-gated; each is a separate audit/repair lane. They are out of scope for P2.2.
- `MENTION_MARKERS` is a regex, not a parse. A line that carries both a retirement marker *and* a live use of the form in the same paragraph (one of the 48 cases) is currently exempted in full. The 4-line fenced-block window and the paragraph-coalescing are the design choice; a tighter test (split paragraph on the first live use) is a future move if a specific case demands it.
- `00_META/00_THE_CORPUS_SPINE.md:130` and `:135` are the strongest case for a "discussion, not use" extension of `MENTION_MARKERS` (the section is *about* the correspondence, calling it `[I]` "a reading, and is not load-bearing"). This is a 1-line `MENTION_MARKERS` extension and would close the spine in a single edit. Filed for P1.x or P2.x disposition; not this wave.

---

**The one sentence.** The P2.2 fix is a block-granularity use-vs-mention filter that correctly exempts the 48:121, 48:416, 48:417 retirement-notice class (the named exemplar) and reports its skipped count on every run; the 48 remaining firings are different documents with different shapes and belong to other tasks' lanes (P1.1 / P1.2 / P1.4 / P2.1 / P2.3 / B3 / B6).
