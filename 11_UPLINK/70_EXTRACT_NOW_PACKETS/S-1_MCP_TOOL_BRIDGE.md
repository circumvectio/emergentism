---
packet: S-1
title: MCP Tool Bridge
status: SHIPPED — reconcile-or-keep
source: Goose `crates/goose-mcp/` (Rust, rmcp over stdio)
target: `core/membrane/council_mcp_server.py`
date: 2026-04-23
rosetta:
  primary_level: L5
  primary_column: MCP Tool Bridge Reconciliation
  secondary:
    - level: L4
      column: Council Tool Surface
      role: "route MCP exposure through verdict-only Council deliberation"
    - level: L3
      column: Live-Code Receipt Audit
      role: "separate reconcile notes from current MCP server implementation truth"
    - level: L6
      column: Category Boundary
      role: "prevent MCP bridge from turning APU into a generic tool harness"
  operator: "Brahmā ○"
  tier: "Executive"
  regime: "Brāhmaṇa"
  register: "[B/I]"
  canonical_phrase: "S-1 · MCP Tool Bridge"
---

# S-1 · MCP Tool Bridge

**Rosetta boundary:** [I] This packet documents an MCP bridge pattern and reconcile state. It does not [B] prove current MCP behavior, client compatibility, storage durability, or category safety without fresh implementation receipts.

## Summary

Expose APU's Council deliberation primitives as MCP tools over stdio so any
FastMCP-compatible client (Claude Desktop, Claude Code, Goose, Cursor) can
submit a document or signal for 7-seat Royal Council or 4-seat Light Council
deliberation without crossing the K2 membrane.

## Source pattern (Goose)

From `crates/goose-mcp/src/lib.rs`:

```rust
pub static BUILTIN_EXTENSIONS: Lazy<HashMap<&'static str, SpawnServerFn>> = Lazy::new(|| {
    HashMap::from([
        builtin!(autovisualiser, AutoVisualiserRouter),
        builtin!(computercontroller, ComputerControllerServer),
        builtin!(memory, MemoryServer),
        builtin!(tutorial, TutorialServer),
    ])
});
```

And `crates/goose-mcp/src/mcp_server_runner.rs` runs each server via
`rmcp::transport::stdio` — one process per capability, duplex stream between
host and server, supervised task lifecycle.

## What was taken

- The **pattern** of exposing capabilities as MCP tools over stdio
- Per-tool registration with explicit tool names (`apu_council_deliberate`,
  `apu_council_deliberate_light`, `apu_council_receipt`, `apu_council_status`)
- In-memory deliberation registry keyed by `deliberation_id`
- Verdict-only return envelope — no execution side effects from the MCP surface

## What was refused

- Goose's general-purpose tool suite (file edit, bash, browser, computer-control).
  Those would collapse APU into a general-purpose harness.
- The tauri/rust build chain. APU stays on the Python stack where the Council
  processors and K2 gateway already live.
- Multi-tenant MCP routing. Each MCP client gets a single deliberation surface;
  there is no MCP-level tenancy story yet.

## Live target (reconcile)

`core/membrane/council_mcp_server.py` — four tools exposed:

| Tool | Purpose | Council type |
|------|---------|---------------|
| `apu_council_deliberate` | Full 7-seat Royal Council | full |
| `apu_council_deliberate_light` | Fast 4-seat Light Council | light |
| `apu_council_receipt` | Retrieve receipt by ID | — |
| `apu_council_status` | Deliberation status | — |

The live file includes an in-memory registry (`_deliberations: Dict[str, Dict[str, Any]]`)
and a production note to upgrade to PostgreSQL.

## Five-guard check (reconciled against live code)

1. **Category-claim:** PASS — tools are scoped to Council deliberation, not
   generic agent capability. APU remains a constitutional engine; MCP is plumbing.
2. **η = 0:** PASS — no hosted toll, no rent. The MCP server runs on the
   founder's machine or the APU process; clients pay their own LLM costs.
3. **K2:** PASS — every deliberation returns a verdict-only K2 envelope. The
   MCP surface cannot trigger execution; execution requires a cryptographic K2
   signature elsewhere.
4. **Three-Stage Process:** PASS — the MCP tools operate only inside SHOULD. They do not
   ingest IS (TheCircle's job), emit COULD (RealityFutures' job), or ACT
   (Skyzai's job).
5. **Signature-locus:** PASS — no MCP call crosses the founder's signing seat.
   The founder signs after deliberation, over a separate channel.

## Keep / revise

**KEEP.** The live implementation respects all five guards. The only
outstanding item is the in-memory store, which is an engineering-quality
concern, not a constitutional one.

## Commit history

- `feat(integration): expose Council deliberation as MCP tools` — original land

## Follow-ups (not part of this packet)

- Move `_deliberations` registry to Postgres with a TTL sweep
- Add MCP-surface rate limiting distinct from the Council's internal rate limits
- Document the MCP client-side configuration pattern in `docs/`

## Zero-risk

This packet documents state that is already in tree. No code change here.
