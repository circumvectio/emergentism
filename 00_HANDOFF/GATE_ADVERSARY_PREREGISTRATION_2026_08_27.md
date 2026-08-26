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
