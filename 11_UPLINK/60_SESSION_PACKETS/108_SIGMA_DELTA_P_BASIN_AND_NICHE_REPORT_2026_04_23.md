---
rosetta:
  primary_column: "Philosophy"
  register: "[S]"
  canonical_phrase: "Packet 108 — ΣΔP Basin and Niche Report"
---

# Packet 108 — ΣΔP Basin and Niche Report

**Evidence tier:** [I] for shipped runtime and tests; [I] where the niche proxy is interpreted.
**Lane:** Sovereign runtime pass.
**Date:** 2026-04-23
**HEAD at preparation:** `a7520a707`

---

## §1. Scope

**Is:** The first realized-outcome `ΣΔP` report surface that compares
results not only by exact provider mix, but also by:

- RLHF lineage basin
- current niche proxy

**Is not:** A claim that the organism now measures the full constitutional
`ΣΔP` of the whole framework. This remains a bounded economic/outcome
surface.

---

## §2. What landed

### 2.1 Report expansion

`core/circulation/sigma_delta_p.py` now returns:

- `by_provider_mix`
- `by_provider_basin`
- `by_conflict_score`
- `by_decision_class`
- `by_niche`

### 2.2 API surface

`api/routers/router_learn.py` now exposes:

- `GET /outcomes/sigma-delta-p-report`

This sits alongside the earlier narrower:

- `GET /outcomes/sigma-delta-p-proxy`

### 2.3 Proof surface

- `tests/test_sigma_delta_p.py`
- `tests/test_router_learn.py`

---

## §3. What changed conceptually

Before this pass, the runtime could answer:

> which exact provider mix made or lost money?

After this pass, it can also answer:

> which lineage basins performed better?

and

> which current execution niches performed better?

That matters because packet 104/105 moved the doctrine from
artifact-thinking to network-equator / polygenetic niche-thinking.
Packet 108 gives that doctrine its first direct realized-outcome report.

---

## §4. Narrow truth

### 4.1 Basin is real runtime structure

`by_provider_basin` is derived from the existing RLHF-lineage cluster
map in `lineage_decorrelation.py`.

This is a coarser but more doctrinally meaningful grouping than exact
provider mix, because it answers:

> did this outcome come from one covariance basin or from a genuinely
> mixed basin composition?

### 4.2 Niche is still a proxy

The runtime does **not** yet persist canonical DAC or organ niche ids on
outcome rows.

So `by_niche` is intentionally named as a proxy:

1. `directive`
2. `sector`
3. `unknown`

This is honest enough for runtime comparison without pretending that the
full niche core state is already encoded in learning rows.

### 4.3 This is still realized-economic only

The report remains tied to realized execution outcomes.

It does **not** yet include:

- wider constitutional effects
- social / cultural `ΣΔP`
- full boundary-wide trophic consequence

So the report is stronger than packet 103’s narrow proxy, but still far
short of the total framework measure.

---

## §5. Verification

Verified on this pass:

- `python3 -m py_compile core/circulation/sigma_delta_p.py api/routers/router_learn.py`
- `pytest tests/test_sigma_delta_p.py tests/test_router_learn.py -q`
- result: `14 passed`

---

## §6. Reorientation

The runtime stack now has a more honest ladder:

- packet 103: realized receipt bridge + first narrow economic proxy
- packet 107: read-only polygenetic witness mesh
- packet 108: realized outcome comparison by basin and niche proxy

The next sovereign-grade question is now sharper:

> do mixed lineage basins and differentiated niches actually outperform
> monocultural ones over time?

Packet 108 does not settle that question. It creates the first clean
surface on which the organism can begin to answer it empirically.
