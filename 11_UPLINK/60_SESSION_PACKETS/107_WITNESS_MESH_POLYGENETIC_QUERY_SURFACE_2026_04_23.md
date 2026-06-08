---
rosetta:
  primary_column: "Neuroscience"
  register: "[S]"
  canonical_phrase: "Packet 107 — Witness Mesh Polygenetic Query Surface"
---

# Packet 107 — Witness Mesh Polygenetic Query Surface

**Evidence tier:** [I] for shipped files and tests; [I] where interpretation is named.
**Lane:** Sovereign runtime pass.
**Date:** 2026-04-23
**HEAD at preparation:** `8cac220d2`

---

## §1. Scope

**Is:** The closure packet for the first explicit polygenetic witness
surface over the Cortex store. It turns provider-mix witness data into a
read-only runtime query layer instead of leaving the polygenetic claim as
doctrine only.

**Is not:** A new write path, a replacement for existing lineage queries,
or a proof that the organism is already in a mature reticulate regime.

---

## §2. What landed

### 2.1 Runtime surface

- `core/cortex/witness_mesh.py`
  - `MixRecord`
  - `Contributor`
  - `NetworkAnchor`
  - `ReticulateIndex`
  - `WitnessMesh`

### 2.2 CLI exposure

- `scripts/cortex_query.py`
  - `mesh`
  - `anchor <signal_id>`
  - `path <signal_id>`

### 2.3 Proof surface

- `tests/test_witness_mesh.py`
- `tests/test_cortex_query.py`

---

## §3. What this changes operationally

Before this pass, Cortex could store `provider_mix`, but the operator had
to infer the polygenetic structure indirectly.

After this pass, the operator can query:

- the most common polygenetic mixes
- the contributor graph around each provider
- the earliest witness anchor for a signal
- the full witness path for a signal
- a bounded reticulate index over the current store window

So the runtime now names the witness mesh directly rather than only
implying it through raw rows.

---

## §4. Narrow truth

### 4.1 Low-sample drift rule

The `ReticulateIndex` now treats one or two witness records as
`phylogenetic_drift` by default.

That is intentional. One hybrid row is not yet a mesh.

### 4.2 This is still read-only

The mesh surface does **not** mutate Cortex, infer outcomes, or alter
lineage identity. It is a read-only sovereign query layer over the
existing append-only store.

### 4.3 This is not yet the economic proof layer

The mesh names polygenetic witness structure. It does **not** yet prove
that polygenetic regimes outperform monocultures economically. That
question remains downstream of `ΣΔP`, realized outcomes, and future
comparative reporting.

---

## §5. Verification

Verified on this pass:

- `python3 -m py_compile core/cortex/witness_mesh.py scripts/cortex_query.py`
- `pytest tests/test_witness_mesh.py tests/test_cortex_query.py -q`
- result: `38 passed`

---

## §6. Reorientation

The doctrine chain now has a matching runtime foothold:

- packet 104: AGI as network-equator
- packet 105: polygenetic nodes + niche partitioning
- packet 107: read-only witness mesh over the real Cortex store

The next honest frontier is not naming the mesh. It is joining the mesh
to realized economic consequence so the organism can ask:

> which provider basins, mixes, and niches actually improved `ΣΔP`?

That requires a later bridge between witness-mesh data and the outcome /
sigma surfaces already landing elsewhere in HEAD.
