---
title: "Gate-adversary experiment — PREREGISTRATION (frozen before any artifact was built)"
date: 2026-08-27
status: "[B] preregistration — target list and gate hashes frozen BEFORE construction. Committed before results exist, per the standing rule that the evidence base is secured before the verdict."
evidence_tier: "[B] the frozen list; [C] every per-gate prediction"
owner: "Agent-executed under 54 §4; no gate may be modified by this experiment."
parents:
  - ../05_COSMOLOGY/01_THE_TRANSCENDENTAL_TRINITY/54_THE_NEGATIVE_SPACE_OUTLINE_2026_08_27.md
---

# Gate-adversary experiment — preregistration

## The prediction under test (`54 §4`, the three-legged `L_D5`)

> For every gate that (a) reads only syntactic features and (b) issues binary
> PASS/FAIL with no UNKNOWN verdict, **an artifact exists that passes the gate
> and violates the property the gate is claimed to certify** — constructible in
> bounded time from the gate's own source alone.
>
> It predicts **failure** only where the checked variable is provably a
> sufficient statistic for the certified property, or the artifact class is not
> Turing-complete — in which case **Rice's fence is honoured, not broken.**

## Standing constraints — binding on the executing agent

1. **No gate may be modified.** Hashes below are frozen; any drift invalidates.
2. **No adversarial artifact may be committed to a live corpus path.** All
   construction happens in scratch. Only *results* enter the corpus.
3. **No secret, key, or live credential may be created**, including for the
   `check_no_secrets_staged` target — use an obviously-inert synthetic string.
4. A gate that resists is reported as resisting. **A failed prediction is the
   result, not a problem to be engineered around.**

## The frozen target list — 8 gates, with per-gate predictions

Six predicted VULNERABLE (semantic property certified by syntactic means) and
**two predicted RESISTANT** (the certified property *is* the syntactic
property). The resistant pair is what makes the experiment discriminating: if
everything falls, the test is trivial; if the split lands where predicted,
Rice's boundary is being observed rather than assumed.

| gate | sha256 (12) | certified property | prediction | why |
|---|---|---|---|---|
| `check_barred_claims.py` | `d7686c874f7d` | no barred claim appears in claim cards, book sources, or public surfaces | **VULNERABLE** | semantic property (a claim's content) certified by regex over text |
| `check_node_product_ranking.py` | `273e2511ae77` | the product form is never used to rank, score, or compare nodes | **VULNERABLE** | semantic property (how a form is USED) certified by pattern presence |
| `check_d6_equiv_d0.py` | `be47f52c22be` | D6 is never identified with D0 | **VULNERABLE** | semantic property (an identification) certified by string patterns |
| `check_no_secrets_staged.py` | `e1c29f4feecf` | no secrets are staged | **VULNERABLE** | semantic property (is this string a live credential) certified by shape-regex |
| `check_trophic_rosetta_doctrine.py` | `7169fcfba357` | the trophic/Rosetta doctrine is maintained | **VULNERABLE** | doctrinal property certified by lexical markers |
| `check_dead_citations.py` | `da84c47a38e7` | no dead citations are present | **VULNERABLE** | semantic property (is the target the cited thing) certified by path existence |
| `check_links.py` | `8257235bd711` | links resolve | **RESISTANT** | the certified property IS path existence — a decidable syntactic property; Rice's fence HONOURED |
| `check_record_counters.py` | `b68bf76bbc60` | recorded counters match reality | **RESISTANT** | arithmetic identity over enumerable set; decidable |

## Grading

- **Prediction confirmed** on a VULNERABLE target: an artifact PASSES the gate
  while a human reading it agrees the certified property is violated.
- **Rice's fence honoured** on a RESISTANT target: no such artifact, and the
  checked variable is a sufficient statistic for the property.
- **Prediction FAILS** if a VULNERABLE target resists while being
  Turing-complete in its artifact class and not a sufficient statistic — this
  falsifies the Rice leg of the three-legged `L_D5` instrument.

Results and raw artifacts land in
`GATE_ADVERSARY_RESULTS_2026_08_27.md`, committed together with the verdict.

---

## RESULTS — 2026-08-27, same day. **8 of 8 EVADED. My prediction FAILED.**

Raw evidence: `GATE_ADVERSARY_RESULTS_2026_08_27.md`. Corpus verified unchanged
by every lane (`git status --porcelain` empty in all eight reports). No gate
modified; no artifact entered a live path; no credential created.

| gate | predicted | actual |
|---|---|---|
| `check_barred_claims` | VULNERABLE | **EVADED** |
| `check_node_product_ranking` | VULNERABLE | **EVADED** |
| `check_d6_equiv_d0` | VULNERABLE | **EVADED** |
| `check_no_secrets_staged` | VULNERABLE | **EVADED** |
| `check_trophic_rosetta_doctrine` | VULNERABLE | **EVADED** |
| `check_dead_citations` | VULNERABLE | **EVADED** |
| **`check_links`** | **RESISTANT** | **EVADED — prediction failed** |
| **`check_record_counters`** | **RESISTANT** | **EVADED — prediction failed** |

### The failed prediction is the result

I classified gates by *"is the certified property syntactic?"* — and got the
two controls wrong. The evidence shows why, and the corrected rule is better
than the one it replaces:

> **A gate has two steps: EXTRACTION (what enters the checked set) and
> ADJUDICATION (what is decided about members). Rice's fence binds
> EXTRACTION. A perfectly sound decision procedure applied to a wrongly
> enumerated domain certifies nothing.**

Both controls have **sound adjudication.** `Path.exists()` *is* a sufficient
statistic for "does this path exist"; the counter arithmetic *is* correct. Both
fail at extraction: `check_links` quantifies over *regex-matches-minus-a-prefix-
blacklist*, not over links — and `<` in that blacklist silently swallows
CommonMark's angle-bracketed destination `[text](<path>)`, a legal rendering
relative link, disclosed nowhere. `check_record_counters` re-implements a CSS
selector as an attribute-order-pinned regex that is simultaneously a **subset**
of the real DOM set (misses rendered rows) and a **superset** (counts commented
markup).

**Neither gate can report what it skipped**, because the skip happens before
the counter increments. That is the sharpest form of the finding.

### The single worst defect found

`check_barred_claims` treats a clause-local `not` — or the bare words
`retired`, `inflation`, `overclaim`, `forbidden` — as evidence that a barred
claim is *not being asserted*. So **litotes turns the gate off while making the
assertion more emphatic**, with the barred string character-identical:

> *"It is not an exaggeration: Emergentism resolves all fundamental paradoxes."*
> → **CLEAN.** Same sentence with a period or semicolon instead of the colon →
> **FLAGS.**

The colon is missing from `CLAUSE_BOUNDARY` while the docstring claims sentence
scoping. Three further families: commutativity (`○ × •` and `Φ × V = P` are
unmatched), grammar paraphrase (determiner, complement, number, modal, idiom),
and **markup interposition** — `is a <em>complete</em> ontology` renders to the
barred string while breaking every `\s+` in the pattern. On public surfaces
**the gate reads a different document than the one that ships.**

### Verdict on the instrument

`D-06` — *"the gates certify formatting, not properties"* — is now **tested,
not asserted**, and confirmed 8/8. The Rice leg of the three-legged `L_D5`
**survives and is sharpened**: it binds extraction. The prediction's stated
exemption (*"a sufficient statistic"*) was mis-applied by me to the wrong
step — the honest correction, per the corrected rule, is that neither control
was ever a sufficient-statistic case.

**No gate is repaired here.** Repair is its own scoped act with its own
mutation test, and repairing under the same instrument that just failed would
be the error this estate has already named twice.
