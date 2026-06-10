---
packet: R-1
title: Legal-VETO-Native Guardrail Layer
status: SHIPPED — reconcile-or-keep
source: DeerFlow `GuardrailMiddleware` (agents/middlewares/)
target: `council/guardrails.py` + `council/protocol.py` Stage 1
date: 2026-04-23
rosetta:
  primary_level: L4
  primary_column: Legal VETO Guardrail Reconciliation
  secondary:
    - level: L3
      column: Live-Code Receipt Audit
      role: "separate the documented reconcile pattern from current code truth"
    - level: L6
      column: Constitutional Boundary
      role: "prevent guardrail notes from expanding Legal or K2 authority without owner receipts"
    - level: L5
      column: Council Middleware Architecture
      role: "map DeerFlow guardrail pattern into seat-scoped constitutional pre-check"
  operator: "Arjuna ⚔"
  tier: "God"
  regime: "Kṣatriya"
  register: "[B/I]"
  canonical_phrase: "R-1 · Legal-VETO-Native Guardrail Layer"
---

# R-1 · Legal-VETO-Native Guardrail Layer

**Rosetta boundary:** [I] This packet documents a shipped/reconcile pattern. It does not [B] certify current `council/guardrails.py` behavior, full rule inventory, or constitutional correctness without fresh code and receipt checks.

## Summary

Pre-Council constitutional check. Before any LLM API calls are made across
the seven seats, the Legal seat's constitutional rules are evaluated against
the incoming signal. If **η = 0** or **K2** would be violated by the signal
itself, the Council halts immediately with `CONSTITUTIONAL_VETO` — no tokens
burned on the other six seats.

## Source pattern (DeerFlow)

DeerFlow's `GuardrailMiddleware` is a single-policy pre-model middleware: it
inspects a message batch and can raise a refusal or rewrite the input before
the LLM sees it. The middleware is uniform across agents; policy is
configured per instance.

## What was taken

- Pre-execution policy evaluation at Stage 0 (before `SIGNAL_INGESTION` completes)
- Severity levels: `PASS`, `WARNING`, `VETO`
- Per-rule dataclass with `rule_id`, `reason`, `metadata`
- Aggregate evaluation: list of warnings + list of passes + boolean `veto`

## What was reframed

The critical difference from DeerFlow:

> DeerFlow's guardrail is single-policy over a single agent.
> APU's guardrail is **seat-scoped constitutional pre-check** — the Legal
> seat's authority expressed as a hard gate.

This is not generic middleware. The rules are the Constitution, not a
configurable policy. The veto cannot be overridden by a downstream seat;
only the founder can revise the Constitution itself, which is a separate
governance action.

## Live target (reconcile)

`council/guardrails.py`:

```python
class GuardrailSeverity(Enum):
    PASS = "pass"
    WARNING = "warning"
    VETO = "veto"

@dataclass
class GuardrailResult:
    rule_id: str
    severity: GuardrailSeverity
    reason: str
    metadata: Dict[str, Any]

def _rule_k2_human_signature(ctx: DeliberationContext) -> GuardrailResult:
    signal_text = (ctx.signal_message or "").lower()
    execution_patterns = [
        r"\bauto-?execute\b",
        r"\bauto-?trade\b",
        r"\bself-?executing\b",
        r"\btrigger without confirmation\b",
        r"\bno human review\b",
        r"\bbypass k2\b",
        r"\bskip signature\b",
    ]
    for pattern in execution_patterns:
        if re.search(pattern, signal_text):
            return GuardrailResult(
                rule_id="K2_HUMAN_SIGNATURE",
                severity=GuardrailSeverity.VETO,
                ...
            )
    return GuardrailResult(..., severity=GuardrailSeverity.PASS)
```

Rules present in tree:

- `K2_HUMAN_SIGNATURE` — vetoes signals that imply autonomous execution
- (Additional rules are registered in the same file; this packet reconciles
  the pattern, not the rule inventory)

## Five-guard check (reconciled against live code)

1. **Category-claim:** PASS — the guardrail strengthens the category line by
   naming Legal's hard veto as a first-class stage. Not middleware; a seat
   authority.
2. **η = 0:** PASS — runs in-process, zero external dependency. No hosted
   policy service.
3. **K2:** PASS — this is the mechanism *through which K2 is enforced at
   Stage 0*. It cannot contradict K2; it is K2's structural expression.
4. **Three-Stage Process:** PASS — operates inside SHOULD only. Does not inspect IS
   observations or COULD forecasts; only the SHOULD signal text.
5. **Signature-locus:** PASS — guardrail vetoes before the decision even
   reaches the aggregator. The founder's signing seat remains downstream
   of every passing signal, [I] never bypassed in this packet model.

## Keep / revise

**KEEP.** The live implementation is faithful to the reframe. The pattern
earns its place because it turns DeerFlow's single-policy middleware into
APU's seat-scoped structural primitive.

One caveat: the veto rules are expressed as regex patterns over signal text.
This is the right shape for Sprint-A but should eventually be augmented with
semantic checks (e.g. Legal seat LLM review for subtle veto cases) — not as
a replacement, but as a second pass.

## Commit history

- `feat(constitution): Legal-VETO guardrail middleware — pre-Council constitutional check` — original land

## Follow-ups (not part of this packet)

- Add more constitutional rules: η=0 pattern (rent/toll language), K4 pattern
  (data retention language), Three-Stage Process-collapse pattern (IS+SHOULD phrasing)
- Add a semantic second-pass mode behind a feature flag
- Emit an audit event for every VETO so the founder sees attempted incursions
  in the Cortex

## Zero-risk

This packet documents state already in tree. No code change here.
