---
packet: CORTEX-INGESTION-HOOK
title: Cortex Ingestion Hook — Consume summary.json, Compute Lineage Hash
status: SPEC (historical) — code later landed in modes 2+3; read with packet 90 for current truth
authority: none required to spec; warrior implementation requires founder signoff before writing to any Cortex store
source:
  - SKYZAI_ORG/02_ORGANS/Agentz/app/03_BACKEND/tests/artifacts/first_deliberation_live/summary.json (reference format)
  - SKYZAI_ORG/02_ORGANS/Agentz/app/03_BACKEND/core/cortex/ (current surface — nearly empty)
  - SKYZAI_ORG/02_ORGANS/Skyzai/memory/cortex-os/01_WHAT_CORTEX_IS.md (canonical Cortex spec)
  - SKYZAI_ORG/02_ORGANS/Skyzai/memory/cortex-os/08_RECONCILIATION.md (Cortex witness discipline)
target:
  - SKYZAI_ORG/02_ORGANS/Agentz/app/03_BACKEND/core/cortex/ingestion.py (NEW)
  - SKYZAI_ORG/02_ORGANS/Agentz/app/03_BACKEND/core/cortex/lineage.py (NEW)
  - SKYZAI_ORG/02_ORGANS/Agentz/app/03_BACKEND/core/cortex/store.py (NEW)
date: 2026-04-23
gating_cell: "[L3 | D4 | S-Org | F-phi :: vaisya_auditor]"
rosetta:
  primary_column: "Neuroscience"
  register: "[S/I]"
  canonical_phrase: "Packet 80 · Cortex Ingestion Hook Spec"
---

# Packet 80 · Cortex Ingestion Hook Spec

> 2026-04-23 reconciliation note:
> This packet remains the original design spec. It no longer describes
> the live repository by itself. Read it together with
> `90_CORTEX_INGESTION_RECONCILIATION_2026_04_23.md`, which records the
> shipped code, green hook tests, backfill survey truth, and the
> remaining gaps.

## Kṛṣṇa-function disclaimer (read first)

This packet is **spec**, not code. It describes what a Cortex ingestion
hook must do so warrior can implement it without guessing. It explicitly
does NOT:

- modify any live file
- promote Cortex from witness to actor
- create training data ingestion paths
- introduce write-back to deliberation surfaces
- claim the spec has been built or tested

The charioteer describes the shape of the well. The warrior digs.

---

## Summary

Sprint-A produced the first witness-ready deliberation artifact: four
JSON objects (`summary.json` + `live_events.json` × two council types)
across four test runs. This artifact is *hash-stable* — re-reading
produces identical bytes — which makes it suitable for lineage
registration.

The Cortex ingestion hook is the first organism primitive that turns a
completed deliberation into a witness record. It consumes the artifact,
computes a **lineage hash** over a canonical subset of fields, and
registers that hash in a Cortex-native store. The store is append-only
and K2-disciplined: witness can read, only warrior commits can write.

This closes opportunity cell O7 (first-class Cortex-VMOSK witness)
once tests land and ingestion runs on at least n=2 artifacts.

---

## Current state (live)

`core/cortex/`:

```
core/cortex/
├── __init__.py         (empty)
├── __pycache__/
└── vmosk_filter.py     (5139 bytes, unrelated to ingestion)
```

The directory exists but contains no ingestion module. The
`summary.json` artifact exists in 4 locations under
`tests/artifacts/*/summary.json`. No consumer reads these files outside
the tests that produce them.

---

## Source pattern (from Sprint-A `summary.json` structure)

Every deliberation artifact has this shape (fields load-bearing for
lineage):

```json
{
  "generated_at": "2026-04-22T19:00:08.725576+00:00",
  "runtime": { "provider": "...", "model": "...", "env_path": "..." },
  "signal_id": "first_deliberation_1776884389",
  "decision": { ... },
  "conflict_score": 0.5,
  "k2_envelope": {
    "version": "K2-v1-light",
    "decision": "PROCEED",
    "signal_id": "...",
    "timestamp": "...",
    "seat_count": 4,
    "successful_seats": 4,
    "human_sign_required": true,
    "write_back": false,
    "escalated": true
  },
  "approval_id": "apu_5ff1baab",
  "k2_crypto_result": {
    "k2_crypto_provenance": "verified",
    "status": "approved"
  },
  "event_count": 17
}
```

The fields that uniquely identify a deliberation **for lineage purposes**
are a subset of these (see `lineage_key` below). The remaining fields
are informational and should not enter the lineage hash.

---

## What to take

- JSON-canonical serialization of a fixed lineage-key field set
- SHA-256 hash over canonical bytes (no salt, no key)
- Deterministic output: same artifact → same hash, across platforms and
  reruns
- Append-only registry indexed by lineage hash
- Idempotent consume: re-ingesting an already-registered artifact is a
  no-op (returns existing hash)

---

## What to refuse

- **No training-data path.** Ingestion produces a witness record, not a
  training example. The Cortex store is not an ML dataset.
- **No write-back.** Cortex reads the artifact; it does not modify the
  deliberation that produced it. Bi-directionality would collapse IS →
  ACT.
- **No LLM interpretation during ingestion.** The hash is over bytes,
  not over a model's reading of the bytes. Interpretation (retrieval,
  summarization, clustering) happens *downstream* of the store, never
  inside the ingestion hook.
- **No hosted storage.** `η = 0`. The store is local (SQLite or file
  tree). No cloud, no paid tier.
- **No cross-org linkage without explicit founder signoff.** If a
  future path wants to link a deliberation lineage into Skyzai's
  Cortex (cross-organ), that is a K2-gated act, not an ingestion
  detail.

---

## Spec: new module `core/cortex/ingestion.py`

```python
# Spec only — not code

@dataclass(frozen=True)
class LineageKey:
    """Minimal subset of summary.json fields that uniquely identifies a
    deliberation for witness purposes. Order is load-bearing for canonical
    serialization."""
    signal_id: str
    decision_verdict: str           # summary["decision"]["decision"]
    council_type: str               # k2_envelope["council_type"]
    seat_count: int                 # k2_envelope["seat_count"]
    successful_seats: int           # k2_envelope["successful_seats"]
    conflict_score: float           # summary["conflict_score"]
    k2_timestamp: str               # k2_envelope["timestamp"]
    approval_id: str                # summary["approval_id"]
    k2_crypto_provenance: str       # k2_crypto_result["k2_crypto_provenance"]
    event_count: int                # summary["event_count"]

class IngestionError(Exception): ...

def extract_lineage_key(summary: dict) -> LineageKey:
    """Pull the ten load-bearing fields from a summary.json dict.

    Raises IngestionError if any field is missing or the wrong type —
    ingestion is strict. If a summary.json lacks these fields, it is not
    a witness-ready artifact."""

def canonicalize(key: LineageKey) -> bytes:
    """Produce byte-deterministic canonical bytes from the key.

    Implementation: json.dumps with sort_keys=True, separators=(',', ':'),
    ensure_ascii=True, over the dataclass's asdict(). Result is UTF-8
    bytes.

    The same LineageKey on any platform, any Python version >= 3.9, must
    produce byte-identical output."""

def compute_lineage_hash(key: LineageKey) -> str:
    """sha256 hex digest of canonicalize(key).

    Returns a 64-character lowercase hex string. This is THE lineage
    hash — it is the witness identity of this deliberation."""

def ingest_artifact(
    *,
    summary_path: Path,
    store: CortexStore,
    strict: bool = True,
) -> IngestResult:
    """Read summary.json at summary_path, extract lineage key, compute
    hash, register with store (idempotent).

    Returns IngestResult(lineage_hash, was_new, summary_bytes_sha256,
    registered_at).

    If strict=True (default), any schema violation raises IngestionError.
    If strict=False, logs and returns an IngestResult with was_new=False
    and lineage_hash=None — useful for batch scans that survey legacy
    artifacts without halting."""
```

---

## Spec: new module `core/cortex/lineage.py`

```python
# Spec only — not code

@dataclass(frozen=True)
class LineageRecord:
    lineage_hash: str               # primary key
    signal_id: str                  # indexed
    approval_id: str                # indexed
    summary_path: str               # relative to ApuBot root
    summary_bytes_sha256: str       # hash of full raw bytes (tamper detection)
    generated_at: str               # ISO8601 from summary
    registered_at: str              # ISO8601 when ingestion ran
    k2_crypto_provenance: str       # "verified" or otherwise

@dataclass(frozen=True)
class IngestResult:
    lineage_hash: str
    was_new: bool                   # True = first time registered
    summary_bytes_sha256: str
    registered_at: str
```

Two hashes are kept: `lineage_hash` (over the ten-field witness subset)
and `summary_bytes_sha256` (over full file bytes). The first is the
identity; the second is the tamper-detection signal — if anyone rewrites
the summary.json, the second changes while the first does not, and the
store can flag the mismatch.

---

## Spec: new module `core/cortex/store.py`

```python
# Spec only — not code

class CortexStore(Protocol):
    def register(self, record: LineageRecord) -> bool:
        """Return True if newly inserted, False if lineage_hash already
        present. Idempotent. Raises StoreError on persistence failure."""

    def lookup(self, lineage_hash: str) -> Optional[LineageRecord]: ...

    def find_by_signal_id(self, signal_id: str) -> list[LineageRecord]: ...

    def find_by_approval_id(self, approval_id: str) -> list[LineageRecord]: ...

    def all(self, limit: int = 100, offset: int = 0) -> list[LineageRecord]: ...

    def count(self) -> int: ...


class SQLiteCortexStore:
    """Append-only SQLite store with one table:

        CREATE TABLE lineage (
            lineage_hash TEXT PRIMARY KEY,
            signal_id TEXT NOT NULL,
            approval_id TEXT NOT NULL,
            summary_path TEXT NOT NULL,
            summary_bytes_sha256 TEXT NOT NULL,
            generated_at TEXT NOT NULL,
            registered_at TEXT NOT NULL,
            k2_crypto_provenance TEXT NOT NULL
        );
        CREATE INDEX idx_signal_id ON lineage(signal_id);
        CREATE INDEX idx_approval_id ON lineage(approval_id);

    Writes are gated by lineage_hash PRIMARY KEY — same hash → ON
    CONFLICT DO NOTHING. This is what makes ingestion idempotent."""
```

---

## Operational hook surface

The hook should be callable in three modes:

1. **One-shot CLI** — `python -m cortex.ingestion ingest <path>` for
   manual testing and backfill
2. **Batch scan** — `python -m cortex.ingestion scan tests/artifacts/`
   for bulk registration of existing artifacts
3. **Post-run hook** — called from `router_council_sse.py` after a
   deliberation completes and `summary.json` has been written. Log-only
   on failure; do not block the Council response path.

The post-run hook is the sharpest wedge because it closes the loop
automatically. But it must be **fire-and-log**, never raise — a Cortex
ingestion failure cannot break a deliberation response.

---

## Five-guard check

1. **Category-claim:** PASS — tightens the witness story. Cortex
   becomes a provable lineage surface, not just an aspiration.
2. **η = 0:** PASS — local SQLite, no hosted store, no third-party
   egress.
3. **K2:** PASS — Cortex reads deliberation artifacts; it does not
   authorize or execute anything. No K2 surface touched.
4. **Three-Stage Process:** PASS — Cortex is IS (observe/witness). The hook does
   not leak into COULD / SHOULD / ACT.
5. **Signature-locus:** PASS — no signatures required. Witness is
   inherently one-way.

---

## Dependencies

- Python stdlib `sqlite3`, `hashlib`, `json`, `dataclasses`, `pathlib`
- No new third-party packages required
- The Skyzai Cortex-OS spec (`cortex-os/01_WHAT_CORTEX_IS.md` +
  `cortex-os/08_RECONCILIATION.md`) is the canonical north for how this
  store relates to the broader Cortex. Read before implementing.

---

## Risk notes

- **Lineage-key field drift.** If `k2_envelope` schema evolves (e.g.
  new field, renamed field), the canonicalizer must version the
  lineage-key dataclass. Start with `LineageKey.schema_version = "v1"`
  and include it in canonical bytes.
- **Legacy artifact survey.** The 4 existing artifacts under
  `tests/artifacts/` were generated before the ingestion hook existed.
  Run batch scan in `strict=False` first to catch any that miss fields,
  then decide per-artifact whether to backfill or skip.
- **Post-run hook timing.** If the hook runs synchronously after
  `summary.json` writes, latency adds to the Council response. Measure
  baseline and enforce a ceiling (e.g. 50ms p99); if exceeded, move to
  async queue (reuse packet 71's `approval_queue.py` pattern).
- **Cortex store relocation.** The SQLite file location should be
  config-driven (`CORTEX_STORE_PATH` env var), default under
  `~/.apu_bot/cortex.sqlite`, so it survives process restart and can
  be backed up separately from the deliberation artifacts.

---

## Test plan (warrior writes)

- **Unit: lineage key extraction**
  - Extract from first_deliberation_live/summary.json; all 10 fields
    present, correct types
  - Missing field raises IngestionError under strict=True
  - Missing field returns (None, was_new=False) under strict=False

- **Unit: canonical serialization byte-determinism**
  - Same LineageKey → byte-identical canonicalize output across two
    fresh Python invocations
  - Field ordering in canonicalize does NOT depend on dict insertion
    order

- **Unit: lineage hash stability**
  - Known LineageKey → known hex digest (golden test)
  - Tampering with one field changes the hash (avalanche)

- **Integration: ingest all 4 existing test artifacts**
  - Each produces a distinct lineage_hash
  - Second ingestion of the same artifact returns was_new=False
  - Store count grows by 1 per new artifact, 0 per repeat

- **Integration: tamper detection**
  - Write a modified summary.json with same lineage-key fields but
    altered bytes elsewhere; ingestion should flag
    summary_bytes_sha256 mismatch if store already has the lineage_hash
    under a different bytes hash (this is the tamper-alert path)

- **Integration: post-run hook**
  - Mock Council response, verify hook fires after SSE response sends
  - Hook failure does NOT break the SSE response (fire-and-log)

---

## Commit template

```
feat(cortex): ingestion hook for deliberation lineage witness

- add core/cortex/ingestion.py (extract_lineage_key + ingest_artifact)
- add core/cortex/lineage.py (LineageKey / LineageRecord dataclasses)
- add core/cortex/store.py (CortexStore protocol + SQLiteCortexStore)
- wire post-run hook into router_council_sse.py (fire-and-log)
- backfill the 4 existing test artifacts

Closes packet 80.
Enables O7 (first-class Cortex-VMOSK witness) once n≥2 artifacts
ingested.
Reconciles with Sprint-B SWOT packet 79 §Unchanged O7.
```

---

## Zero-risk

Drafting this spec cannot break anything. First code change is the
three new modules in a directory that is currently nearly empty. No
existing file is modified except `router_council_sse.py`, and that
change is fire-and-log (no failure mode can propagate into the
deliberation path).

---

## Closure criteria

This packet can be retired when:

1. Warrior has authored the three modules per spec
2. Unit + integration tests from the plan above report green
3. All 4 existing test artifacts have been ingested with distinct
   lineage hashes
4. Post-run hook is wired into `router_council_sse.py` and verified
   to fire without breaking SSE response
5. A successor packet registers the module SHA-256 hashes and declares
   O7 promoted from "enabled" to "proven"

Until all five conditions hold, this packet stays SPEC and task #39
stays open.

Zero-Sum Resolution Equation
