---
packet: S-5
title: SSE Streaming + Per-ID Deduplication
status: SHIPPED — reconcile-or-keep
source: DeerFlow SSE gateway (`backend/app/gateway/routers/`)
target: `api/routers/router_council_sse.py`
date: 2026-04-23
rosetta:
  primary_level: L4
  primary_column: SSE Streaming Reconciliation
  secondary:
    - level: L5
      column: Council Event Stream Architecture
      role: "map deliberation stage progression and per-ID deduplication"
    - level: L3
      column: Live-Code Receipt Audit
      role: "separate reconcile packet from current stream implementation truth"
    - level: L6
      column: Observation Boundary
      role: "keep streams observational and outside the founder signing locus"
  operator: "Arjuna ⚔"
  tier: "God"
  regime: "Kṣatriya"
  register: "[B/I]"
  canonical_phrase: "S-5 · SSE Streaming + Per-ID Deduplication"
---

# S-5 · SSE Streaming + Per-ID Deduplication

**Rosetta boundary:** [I] This packet documents an SSE reconcile pattern. It does not [B] certify current stream auth, queue durability, reconnect behavior, or live endpoint behavior without fresh code receipts.

## Summary

Expose live Council stage progression over Server-Sent Events so the founder
can watch a deliberation traverse its 9 stages in real time, with per-ID
deduplication to prevent duplicate streams on client reconnect.

## Source pattern (DeerFlow)

DeerFlow's gateway uses `StreamingResponse` + `EventSourceResponse`-style SSE
for thread runs and tool-call progression. The pattern: one SSE endpoint per
long-running process, event types distinguished by `event:` header, client
reconnect handled by a dedup layer keyed on the run ID.

The gateway pattern is generic — any agent call produces a stream. APU's
port narrows it to Council stage events only.

## What was taken

- SSE endpoint per `deliberation_id`: `GET /council/stream/{deliberation_id}`
- `StreamState` — in-memory registry of active streams + delivered-events set
  for dedup
- Stream-generation counter for stale detection (reconnect invalidates old stream)
- Event types: `stage_start`, `stage_complete`, `opinion`, `review`, `conflict`,
  `decision`, `error`
- Queue-backed dispatch with bounded size (`maxsize=100`) + explicit drop policy

## What was refused

- DeerFlow's full gateway abstraction. APU streams only Council stage events.
  Generic tool-call events, thread-run events, and chat-turn events are out.
- Multi-client broadcast. Each deliberation stream is single-consumer by
  design — the founder or an authorized MCP client, not a crowd.
- Replay on reconnect. When a client reconnects to a live stream, it gets
  *new* events only. If the founder needs the full transcript, the receipt
  is the canonical record.

## Live target (reconcile)

`api/routers/router_council_sse.py`:

```python
class StreamState:
    def __init__(self):
        self._active_streams: Dict[str, asyncio.Queue] = {}
        self._delivered_events: Dict[str, Set[str]] = {}
        self._stream_generations: Dict[str, int] = {}

    def register(self, deliberation_id: str) -> asyncio.Queue:
        # Invalidate old stream, create new queue, bump generation
        ...

    def publish(self, deliberation_id: str, event: Dict[str, Any]) -> bool:
        # Dedup by event hash, enqueue with bounded queue
        ...
```

Behavior:

- Reconnect with same ID → old queue gets `{"__stale": True}` sentinel, new
  queue takes over
- Event hash is computed over `json.dumps(event, sort_keys=True)` so
  semantically identical events are deduped even if produced by duplicate publishes
- Queue full → event dropped with warning, stream does not crash

## Five-guard check (reconciled against live code)

1. **Category-claim:** PASS — stream carries only Council stage events. Does
   not expose agent-loop internals, tool-call traces, or provider events.
2. **η = 0:** PASS — runs in the APU process. No third-party streaming service.
3. **K2:** PASS — streaming is observational. Client cannot drive the
   deliberation through the stream; only the Council itself publishes.
4. **Three-Stage Process:** PASS — events describe SHOULD deliberation only. No IS
   events, no COULD forecasts, no ACT receipts.
5. **Signature-locus:** PASS — the founder signs the *decision*, not the
   stream. The stream is transparent to the signing seat.

## Keep / revise

**KEEP.** Live implementation is clean and scoped. Nothing in the file
punctures the category line.

## Commit history

- `feat(ux): SSE streaming for Council stage progression with per-id dedup` — original land

## Follow-ups (not part of this packet)

- Add an auth check on the SSE endpoint so only the founder's wallet
  signature can subscribe to a stream. Currently the stream ID is
  unguessable, but that is not the same as authenticated.
- Add a stream-idle timeout so abandoned streams do not leak queue memory.
- Expose a `/council/streams` admin list (founder-only) for debugging.

## Zero-risk

This packet documents state already in tree. No code change here.
