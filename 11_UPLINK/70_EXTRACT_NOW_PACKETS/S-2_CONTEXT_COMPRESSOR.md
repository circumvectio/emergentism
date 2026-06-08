---
packet: S-2
title: Context Compressor for Stage 9 (RECEIPT_EMISSION)
status: SPEC — pending implementation
source: DeerFlow `backend/packages/harness/deerflow/agents/middlewares/summarization_middleware.py`
target: `council/protocol.py` Stage 9 + `core/circulation/context_compressor.py` (new)
date: 2026-04-23
rosetta:
  primary_level: L5
  primary_column: Context Compressor Specification
  secondary:
    - level: L3
      column: Receipt and Reproducibility Audit
      role: "keep Stage 9 compression as spec until implementation receipts exist"
    - level: L4
      column: Receipt Emission Operation
      role: "route transcript compression through deterministic Stage 9 behavior"
    - level: L6
      column: Raw-Transcript Boundary
      role: "preserve raw transcript recoverability and prevent silent context loss"
  operator: "Brahmā ○"
  tier: "Executive"
  regime: "Brāhmaṇa"
  register: "[D/I/B]"
  canonical_phrase: "S-2 · Context Compressor for Stage 9"
---

# S-2 · Context Compressor for Stage 9

**Rosetta boundary:** [D/I] This packet is a pending implementation spec. It does not [B] prove compression behavior, token counts, raw-transcript persistence, or Stage 9 wiring until code and receipts exist.

## Summary

When a deliberation transcript is large (many seats × long opinions × peer
review passes), the Stage 9 RECEIPT_EMISSION artifact should compress the
full transcript to a summary + preserved tail. This prevents the receipt
from ballooning while keeping the last-N messages verbatim for audit.

## Source pattern (DeerFlow)

From `summarization_middleware.py`:

```python
class DeerFlowSummarizationMiddleware(SummarizationMiddleware):
    def before_model(self, state: AgentState, runtime: Runtime) -> dict | None:
        return self._maybe_summarize(state, runtime)

    def _maybe_summarize(self, state, runtime):
        messages = state["messages"]
        total_tokens = self.token_counter(messages)
        if not self._should_summarize(messages, total_tokens):
            return None
        cutoff_index = self._determine_cutoff_index(messages)
        messages_to_summarize, preserved_messages = self._partition_messages(messages, cutoff_index)
        self._fire_hooks(messages_to_summarize, preserved_messages, runtime)
        summary = self._create_summary(messages_to_summarize)
        new_messages = self._build_new_messages(summary)
        return {"messages": [RemoveMessage(id=REMOVE_ALL_MESSAGES), *new_messages, *preserved_messages]}
```

Key moves:

- **Threshold check** via `_should_summarize(messages, total_tokens)` — only
  compress when context is actually pressured.
- **Cutoff selection** via `_determine_cutoff_index` — preserves trailing
  messages so the most recent context stays verbatim.
- **Pre-compression hook** — `before_summarization` hooks fire with the
  messages that are about to be summarized away, giving downstream systems a
  chance to persist raw content before it is lost.
- **Replace-in-place** via `RemoveMessage(id=REMOVE_ALL_MESSAGES)` + new
  summary + preserved tail.

## What to take

- Threshold-triggered compression ([D/I] event-triggered rather than continuous)
- Cutoff partitioning: `summarized | preserved` boundary
- Pre-compression hook pattern — before we compress, we emit an immutable
  archive-of-raw-transcript to the Cortex
- Summary as a synthetic message with a stable author (`"system: stage9_summary"`)

## What to refuse

- LangChain/LangGraph coupling. APU's Council runs its own state machine; we
  cannot pull LangChain as a hard dependency. The port is **pattern-level**,
  not import-level.
- Implicit summarization inside the agent loop. APU summarizes only at Stage 9,
  deterministically, as part of receipt emission.
- Provider-specific token counting. APU counts chars/words or uses a local
  tokenizer that is identical across providers. Stage 9 must be reproducible.

## Live target

### Stage 9 in `council/protocol.py`

Stage 9 (RECEIPT_EMISSION) currently takes the full `DeliberationContext` and
hands it to the receipt builder. After this packet, Stage 9 should:

1. Assemble the full transcript artifact (seats × opinions × peer review × aggregator)
2. Compute token/char budget; if above threshold, invoke `ContextCompressor`
3. Fire `before_compression_hook` — persist raw transcript to the Cortex
   (immutable archive with lineage hash)
4. Emit receipt containing:
   - Compressed summary
   - Preserved tail (last-N messages verbatim)
   - `compressed: true/false` flag
   - `raw_transcript_hash` (provenance pointer)

### New file: `core/circulation/context_compressor.py`

```
# Skeleton (not code — spec only)

class CompressionResult:
    summary: str
    preserved_tail: list[dict]
    compressed: bool
    raw_transcript_hash: str
    token_count_before: int
    token_count_after: int

class ContextCompressor:
    def __init__(self, threshold_tokens: int, tail_keep: int):
        ...
    def should_compress(self, messages) -> bool: ...
    def determine_cutoff(self, messages) -> int: ...
    def compress(self, messages) -> CompressionResult: ...
```

The summary generation itself can use a local deterministic heuristic
(top-K sentences by structural salience) for Sprint-A. An LLM-based summary
is a later enhancement, bound by the same reproducibility requirement.

## Five-guard check

1. **Category-claim:** PASS — compression is purely internal plumbing. Does not
   change what APU is.
2. **η = 0:** PASS — no external service required; compression runs in-process.
   If an LLM is used later, it uses the founder's own provider keys — no
   broker toll.
3. **K2:** PASS — compression affects the receipt shape, not the decision. The
   decision is signed; the compression metadata is part of what is signed.
4. **Three-Stage Process:** PASS — operates only inside SHOULD, at Stage 9. Does not touch
   IS / COULD / ACT.
5. **Signature-locus:** PASS — the founder signs the receipt; the compressor
   is transparent and the raw transcript is recoverable via
   `raw_transcript_hash`.

## Dependencies

- Cortex lineage store (for `raw_transcript_hash`) — already present in
  `core/circulation/cortex/`
- Stage 9 processor wiring — straightforward extension of existing processor
- Token counter — deterministic, provider-independent

## Sprint-A fit

Not blocking. Sprint-A closeout already shipped without compression (17 events,
~20s latency, 4 seats). Useful once Royal Council (7 seats × peer review)
routinely produces transcripts > 8K tokens.

## Test plan

- Unit: `should_compress` respects threshold boundary cases (0, exact, +1, 2×)
- Unit: `determine_cutoff` preserves last N tokens with a nonzero retained tail
- Integration: Stage 9 produces identical decision with compression on vs off
- Audit: raw-transcript hash round-trips through Cortex and can be replayed

## Commit template

```
feat(receipt): compress stage-9 transcripts above N tokens with preserved tail + lineage hash

- add core/circulation/context_compressor.py (ContextCompressor + CompressionResult)
- wire compressor into council/protocol.py Stage 9
- emit raw_transcript_hash to Cortex before compression
- receipts now carry {summary, preserved_tail, compressed, raw_transcript_hash}

Reconciles with four-guard extraction matrix (packet S-2).
No change to decision semantics — receipt shape only.
```

## Zero-risk

All work here is spec. No code changes land until the founder signs.
