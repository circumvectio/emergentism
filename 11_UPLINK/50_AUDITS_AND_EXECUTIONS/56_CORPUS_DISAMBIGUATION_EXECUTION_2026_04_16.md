---
rosetta:
  primary_level: L6
  primary_column: Meta
  operator: "Śiva •"
  tier: "Executive"
  regime: "Sādhu"
  register: "[S]"
  canonical_phrase: "Corpus Disambiguation Execution 2026-04-16"
---

# Corpus Disambiguation Execution — 2026-04-16

> **Continuous recursive disambiguation applied to the corpus itself.**

Date: 2026-04-16  
Status: Executed and closed  
Canonical path: `50_AUDITS_AND_EXECUTIONS/56_CORPUS_DISAMBIGUATION_EXECUTION_2026_04_16.md`

---

## 0. Trigger

A deep logic audit and repository pruning pass revealed structural ambiguities between:
- source specs and live implementations
- archived material and live routing
- stale review docs and post-audit reality

This packet records the repair moves.

---

## 1. Ambiguities Detected and Resolved

### A. K2 Signature Message Mismatch (authority ambiguity)

| Axis | Value |
|------|-------|
| **Surface** | `30_PROGRAMS/44_K2_ATTESTATION_PACKET_SPEC.md` |
| **Class** | authority / lexical |
| **Ambiguity** | The spec documented `sha256(signer_npub + action_commitment + timestamp + nonce)` but the implementation had been hardened to include `duress`. The spec was silently stale. |
| **Owner** | `30_PROGRAMS/44_K2_ATTESTATION_PACKET_SPEC.md` |
| **Time posture** | current truth (the implementation was already correct) |
| **Evidence tier** | S — structural consistency between spec and code |
| **Correction** | Updated the spec to include `duress_bit` in the canonical signed message. |
| **Downstream refresh** | None required; code and tests already matched the new format. |

### B. PHI-meter API JSON Serialization (runtime ambiguity)

| Axis | Value |
|------|-------|
| **Surface** | `backbone/api/phi_meter_api.py`, `backbone/schemas/phi_meter_models.py` |
| **Class** | runtime / metric |
| **Ambiguity** | `float('inf')` from `μ_seizure` and potential `float('nan')` from masked indicators crashed FastAPI's JSON encoder. The API could not return valid responses. |
| **Owner** | `schemas/phi_meter_models.py` |
| **Time posture** | current truth |
| **Evidence tier** | E — empirical (tests failed with `ValueError`) |
| **Correction** | Added `field_serializer` on `PhiIndicatorValue.value` mapping `inf`/`nan` to JSON `null`. Fixed datetime query param parsing to handle URL-decoded `+` signs. |
| **Downstream refresh** | Tests updated; 6 previously failing API tests now pass. |

### C. Archive Authority (scope ambiguity)

| Axis | Value |
|------|-------|
| **Surface** | `08_ARCHIVE/` (newly created) |
| **Class** | scope / authority |
| **Ambiguity** | Large archival move created a directory with no index. No one could know what had been moved or from where without running `git log`. |
| **Owner** | `08_ARCHIVE/README.md` |
| **Time posture** | historical truth, current routing |
| **Evidence tier** | S — structural |
| **Correction** | Created `08_ARCHIVE/README.md` with a relocation table, rules, and provenance note. |
| **Downstream refresh** | `00_INTAKE/00_README.md` and `00_INTAKE/README.md` updated to point to the new archive location for processed intake. |

### D. RuntimeOrchestrator Missing K4 Gate (runtime ambiguity)

| Axis | Value |
|------|-------|
| **Surface** | `backbone/services/runtime_orchestrator.py` |
| **Class** | runtime |
| **Ambiguity** | The documented gate sequence was K2 → K4 → VMOSK → Execute, but the orchestrator skipped K4. A FROZEN BA could still reach execution. |
| **Owner** | `services/runtime_orchestrator.py` |
| **Time posture** | current truth |
| **Evidence tier** | S — structural |
| **Correction** | Added `ba_registry` to `RuntimeOrchestrator` and a K4 ACTIVE state check between K2 verification and VMOSK lint. Added `test_execute_k4_inactive`. |
| **Downstream refresh** | None. |

### E. Implementation Review Staleness (temporal ambiguity)

| Axis | Value |
|------|-------|
| **Surface** | `50_AUDITS_AND_EXECUTIONS/50_IMPLEMENTATION_REVIEW.md` |
| **Class** | temporal |
| **Ambiguity** | Review claimed 106 passing tests and listed runtime orchestrator and PHI-meter API as unimplemented gaps. Post-audit reality was 137 tests with both features implemented. |
| **Owner** | `50_AUDITS_AND_EXECUTIONS/50_IMPLEMENTATION_REVIEW.md` |
| **Time posture** | historical truth masquerading as current |
| **Evidence tier** | E — empirical test run |
| **Correction** | Updated test count, marked runtime orchestrator and PHI-meter API as resolved, preserved original tension notes for historical context. |
| **Downstream refresh** | None. |

---

## 2. Stop Conditions

All touched surfaces are now:
- ✅ locally clear
- ✅ correctly owned
- ✅ correctly timed
- ✅ route-honest
- ✅ explicit about remainder (no remainder left open)

---

## 3. Canonical Compression

> **Disambiguation is not a one-time cleanup. This execution repaired five live ambiguities, updated one spec, hardened one runtime gate, fixed one API serialization boundary, created one archive index, and closed one stale review. The corpus is locally convergent.**

---

## Cross-References

- `50_AUDITS_AND_EXECUTIONS/52_CONTINUOUS_RECURSIVE_DISAMBIGUATION.md` — doctrine
- `50_AUDITS_AND_EXECUTIONS/53_DISAMBIGUATION_REVIEW_PACKET.md` — template
- `02_ORGANISM/04_PROJECT_MANAGEMENT/DISAMBIGUATION_REGISTER.md` — D8–D12
- `50_AUDITS_AND_EXECUTIONS/51_EFFECTIVENESS_EFFICIENCY_AND_LOGIC_AUDIT.md` — parent audit
