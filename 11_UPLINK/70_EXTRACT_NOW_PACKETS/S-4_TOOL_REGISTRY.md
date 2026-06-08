---
packet: S-4
title: Self-Discovering Tool Registry
status: HELD — constitutional clarification required
source: DeerFlow `backend/packages/harness/deerflow/tools/builtins/tool_search.py`
target: (deferred — depends on clarification outcome)
date: 2026-04-23
rosetta:
  primary_level: L6
  primary_column: Tool Registry Constitutional Hold
  secondary:
    - level: L4
      column: Founder Decision Gate
      role: "hold Legal-gated vs Standing Orders discovery until a binding choice exists"
    - level: L3
      column: Category Drift Audit
      role: "identify where deferred tool discovery could turn APU into a generic harness"
    - level: L5
      column: Deferred Registry Architecture
      role: "preserve the pattern without shipping it"
  operator: "Śiva •"
  tier: "Executive"
  regime: "Sādhu"
  register: "[D/I]"
  canonical_phrase: "S-4 · Self-Discovering Tool Registry — HELD"
---

# S-4 · Self-Discovering Tool Registry — HELD

**Rosetta boundary:** [D/I] This packet is held for constitutional clarification. It does not [B] authorize implementation, runtime discovery, external tool registration, or category expansion.

## Summary

DeerFlow exposes a `DeferredToolRegistry` that lets the agent discover new
tools at runtime via `tool_search` (with `select:`, `+keyword`, and regex
query forms). The registry stores lightweight entries and returns full tool
schemas only on match.

This is a useful pattern, **but it is the primary seam through which APU
could drift toward a generic agent harness.** A self-discovering tool layer
that is not constitutionally bounded will quickly make APU look like "an
agent that can also do many things" — which is the precise category the
extraction matrix is designed to refuse.

**This packet is held pending resolution of one binding question.**

## The binding question

**Is runtime tool discovery a Legal-seat-gated operation, or a Standing
Orders (4C) feature?**

- **Legal-seat-gated** — each discovery call goes through `council/guardrails.py`
  and must pass a constitutional pre-check. A tool may be registered in the
  catalog but not *discoverable* without Legal's pass. This maintains the
  category line but adds latency to every discovery.
- **Standing Orders (4C) feature** — the founder, via a signed 4C directive,
  authorizes a specific set of tools as discoverable. The set is static
  between orders; discovery inside the set is free. This preserves the
  category line at declaration time, not query time.

Until this is answered, no implementation.

## Source pattern (DeerFlow)

From `tool_search.py`:

```python
class DeferredToolRegistry:
    def register(self, tool: BaseTool) -> None: ...
    def promote(self, names: set[str]) -> None: ...
    def search(self, query: str) -> list[BaseTool]:
        if query.startswith("select:"):
            names = {n.strip() for n in query[7:].split(",")}
            return [e.tool for e in self._entries if e.name in names][:MAX_RESULTS]
        if query.startswith("+"):
            parts = query[1:].split(None, 1)
            required = parts[0].lower()
            candidates = [e for e in self._entries if required in e.name.lower()]
            ...
        # General regex search
        regex = re.compile(query, re.IGNORECASE)
        ...
```

Design moves worth noting:

- Registry is populated at startup but full schemas are *gated behind search*
- Three query forms: exact `select:`, filter `+keyword`, general regex
- `promote` removes a tool from deferred status once its schema is in the
  agent's context — preventing re-stripping by downstream filters

## What would be taken (if unblocked)

- The registry/promotion pattern — keeps the live context small
- Three query forms with APU-specific ranking on description
- Deferred schema loading — MCP clients discover Council tools by keyword
  without APU shipping the full 7-tool spec up front

## What would be refused

- Discovery of arbitrary tools. APU's registry would contain **only Council
  governance primitives** — no file edit, no bash, no browser. This is the
  firebreak against the general-harness category drift.
- Self-registration from external packages. Tool entries land in the registry
  only through an explicit founder-signed manifest.
- Dynamic augmentation of seat capabilities via discovered tools. Seats have
  fixed authorities; discovery affects *which* governance tools an MCP
  client can see, not *what* seats can do.

## Five-guard check (as currently framed — provisional)

1. **Category-claim:** CAUTION — high risk of drift unless the registry is
   scoped to Council primitives only. The guard fires if the registry grows
   beyond governance tools.
2. **η = 0:** PASS — no external service.
3. **K2:** PASS — discovery changes visibility, not execution authority.
4. **Three-Stage Process:** CAUTION — the discovery surface sits inside SHOULD, but a
   weak scope check could let discovery reach into IS/COULD/ACT tools.
5. **Signature-locus:** CAUTION — this is where the clarification binds. If
   discovery is Standing-Orders-gated, the founder's signing seat is
   preserved; if runtime-Legal-gated, the Legal seat absorbs signing-adjacent
   authority that should stay with the founder.

Two CAUTIONs is enough to hold until the binding question is answered.

## What this packet does NOT ship

Until the clarification lands, this packet is a spec-of-a-spec. The file
exists to prevent ambiguous work from starting before the constitutional
answer is in.

## Recommended resolution path

1. Founder reads the two options above.
2. Founder writes a one-paragraph decision into `01_EMERGENTISM/11_UPLINK/20_K2_SOVEREIGNTY_SCOPE.md`
   (or a sibling file) naming which mode applies.
3. This packet is revised into either:
   - `S-4a_TOOL_REGISTRY_LEGAL_GATED.md`, or
   - `S-4b_TOOL_REGISTRY_STANDING_ORDERS.md`
4. Implementation follows the chosen mode only.

## Limits

- No code exists yet in APU for this packet.
- No decision is being claimed here. The extraction matrix marks this as
  `more-info`, and this packet consolidates what "more info" means.

## Zero-risk

Holding is the zero-risk move. The worst outcome is premature shipping of a
discovery surface that later has to be rolled back because it punctured the
category line.
