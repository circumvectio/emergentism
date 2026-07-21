---
rosetta:
  primary_column: "Neuroscience"
  register: "[I]"
  canonical_phrase: "SPECTRE Immune System Specification"
---

# SPECTRE Immune System Specification

**Evidence tier:** [I]  
*Operational specification. Interpretive mapping of structural sources into implementable contracts.*


> **The immune system is the graph's defense against lies, eclipse pressure, and contagion.**
>
> It must clean the graph without becoming a throne, a toll booth, or a pretext for protocol mythology.

Date: 2026-04-16  
Status: Planning Specification  
Canonical path: `47_SPECTRE_IMMUNE_SYSTEM_SPEC.md`

---

## 0. Reconciliation Truth First

This document is a **planning specification**, not a claim that the full SPECTRE immune system is currently implemented.

Current truth:

- the rooted commercial proof path remains primary
- SPECTRE remains a later substrate/research lane
- the body/brain separation and immune logic are still design surfaces, not earned runtime authority
- packet 110 and `ORGANISM_RUNTIME_TRUTH.md` authorize a narrower claim: the
  BEAM SPECTRE package has a prototype-real route-energy kernel and closed
  replay contract in controlled runtime conditions

So this note defines:

> **what the immune system should be when SPECTRE earns the right to exist as a live distributed substrate**

It does **not** authorize moving SPECTRE ahead of the rooted proof sequence.

Boundary repair (2026-04-24): do not describe AIA as the full immune system.
AIA is the Automated Information Architect / gardener layer. Cortex remembers
and witnesses. This packet names the future SPECTRE graph-immune design lane.
See `130_BOUNDARY_AUDIT_ORGANISM_MODEL_2026_04_24.md`.

---

## 1. Purpose

The immune system exists to answer one question:

> **How does a distributed graph defend itself from false reports, malicious routing, Sybil inflation, eclipse pressure, and contamination without creating a central judge?**

The answer must satisfy five constraints:

1. **aBFT / consensus safety must not depend on the immune system**
2. **the immune system must never become a revenue engine**
3. **sanctions must be triggered by structural proof, not prestige**
4. **false positives must have a recovery path**
5. **the network must degrade to safe dumb routing when the immune layer fails**

---

## 2. The Core Separation

The most important architectural line remains:

### Body

The transport substrate:

- gossip mechanics
- buffering
- peer I/O
- serialization
- hashgraph / ordering behavior

### Brain

The adaptive layer:

- telemetry scoring
- suspicion propagation
- triangulation
- quarantine decisions
- recovery scoring

### Immune system

A specific function of the Brain:

- detect self/non-self problems in routing claims
- downgrade malicious or unreliable paths
- quarantine when evidence crosses threshold
- restore standing when remediation is proven

**Hard rule:** If the Brain fails, the Body falls back to standard redundant gossip.  
**Hard rule:** If the immune system is unsure, routing gets more conservative, not more authoritarian.

---

## 3. The Threat Classes

The immune system should watch for at least six classes of threat:

### T1 — fabricated telemetry

Examples:

- false latency claims
- false success-rate claims
- forged availability
- dishonest cost reporting

### T2 — eclipse pressure

One node or clique attempts to surround a target and control most of its apparent neighbors.

### T3 — Sybil inflation

Many nominal nodes are actually one operator or one economic cluster attempting to inflate graph position.

### T4 — relay withholding / selective forwarding

A node pretends to relay honestly but drops or delays traffic strategically.

### T5 — contamination cluster

A subgraph of mutually reinforcing liars or failing nodes begins to distort the surrounding graph.

### T6 — immune abuse

Actors try to trigger sanctions dishonestly, exploit suspicion gossip, or profit from downgrade events.

---

## 4. The Evidence Sources

The immune system should not rely on one kind of proof.

It should combine:

### E1 — local telemetry

What a node measures directly:

- observed latency
- relay success/failure
- packet completion
- response variance

### E2 — reciprocal reports

What two nodes claim about each other.

### E3 — cross-report variance

What other independent neighbors observe about the same node.

### E4 — topology geometry

Triangle inequality, cluster shape, clique density, path asymmetry, suspicious centrality jumps.

### E5 — receipt / economic evidence

When routing dishonesty leads to:

- missed receipts
- settlement delays
- failed evidence propagation
- graph-capital contamination

### E6 — remediation evidence

What a flagged node does to recover:

- re-probe participation
- clean uptime window
- contradictory evidence resolution
- collateral/bond compliance if relevant

---

## 5. The Three Primary Detection Tests

These remain the core immune tests:

### Test A — cross-report variance

If node `A` claims:

- latency = `5ms`
- success = `0.99`

but independent probes from `C`, `D`, and `E` show materially worse performance, suspicion rises.

Use:

```text
variance_score(A) = spread(independent_observations_about_A)
```

Interpretation:

- low spread = stable truth
- high spread = possible lie, asymmetry, or unstable route

### Test B — reciprocal consistency

Claims must be mutually compatible:

- `A` says it contacted `B`
- `B` should show the corresponding contact trace

If not:

- suspicion rises on one or both nodes
- repeated asymmetry becomes evidence of dishonesty or malfunction

### Test C — triangle inequality / geometric contradiction

If:

- `A -> B` is very low latency
- `B -> C` is very low latency
- but `A -> C` is implausibly bad or impossible

then the graph's geometry is inconsistent.

This test is especially useful against fabricated ideal links and hidden subgraph manipulation.

---

## 6. Suspicion Model

The immune system should not jump straight from anomaly to quarantine.

It should move through a staged suspicion model:

### State 0 — healthy

- no meaningful contradictions
- full routing eligibility

### State 1 — observed anomaly

- local inconsistency detected
- no global propagation yet
- triggers additional probes

### State 2 — corroborated suspicion

- at least two independent evidence sources align
- local routing weight reduced
- suspicion event emitted to neighbors

### State 3 — contaminated

- repeated or multi-source contradiction confirmed
- routing strongly demoted
- graph-capital drag applied
- capability consequences may begin

### State 4 — quarantined

- node or subgraph temporarily isolated from preferred routing
- only constrained communication path remains
- recovery clock starts

### State 5 — remediated / restored

- node proves healthy behavior across a clean window
- suspicion decays
- graph standing partially or fully restored

This gives the organism:

- memory
- caution
- reversibility

without instant social death.

---

## 7. Suspicion Propagation

Suspicion should propagate carefully.

### Local-first rule

No suspicion should become network-visible from a single local anomaly alone.

Local anomalies should first trigger:

- re-probes
- redundancy increase
- neighbor diversity increase

### Structured propagation rule

Only after corroboration should a node emit a `SuspicionEnvelope` to neighbors.

That envelope should include:

- target node id
- evidence class
- confidence band
- time window
- local consequences already applied
- whether remediation is possible

### Bounded propagation rule

Suspicion must not flood the whole graph by default.

Suggested scopes:

- **local scope** — immediate neighbors only
- **regional scope** — two-hop neighborhood if contamination risk is rising
- **global scope** — only for systemic threats, large Sybil clusters, or major contradiction patterns

The burden of proof rises with scope.

---

## 8. Quarantine Rules

Quarantine is the strongest non-terminal immune action.

It should mean:

- the node remains historically visible
- evidence about it remains queryable
- it loses preferred routing status
- sensitive capabilities are suspended where applicable

It should **not** mean:

- historical erasure
- confiscation as operator profit
- permanent exile by default

### Quarantine triggers

Quarantine should require one of:

1. repeated corroborated telemetry fraud
2. demonstrated eclipse behavior
3. Sybil cluster evidence above threshold
4. relay withholding with direct economic harm
5. repeated immune-system abuse

### Quarantine scopes

| Scope | Meaning |
|------|---------|
| **path quarantine** | only certain routes through the node are avoided |
| **neighbor quarantine** | immediate peers reduce preferred contact |
| **subgraph quarantine** | identified clique or cluster is collectively demoted |
| **capability quarantine** | tool access / routing privileges / higher trust surfaces suspended |

Hard rule:

> **Quarantine should be as narrow as possible and as wide as necessary.**

---

## 9. Recovery Windows

If quarantine exists, recovery must exist too.

### Clean-window recovery

A quarantined node may recover by demonstrating:

- sustained honest telemetry
- reciprocal consistency
- successful independent probes
- no fresh contradiction events

### Recovery duration

The exact duration should depend on offense class:

- isolated telemetry fault -> short recovery
- repeated dishonesty -> medium recovery
- organized contamination / Sybil attack -> long recovery

### Recovery shape

Recovery should be gradual:

- quarantine
- constrained routing
- probationary routing
- restored preferred routing

This prevents:

- instant forgiveness theater
- and permanent exile from one bad epoch

---

## 10. False-Positive Handling

An immune system without false-positive doctrine becomes a tyranny machine.

So the network must explicitly support:

### appeal by evidence

A node may present:

- independent telemetry
- enclave or hardware attestations
- relay proof
- counterparty receipts

### downgrading suspicion confidence

If evidence becomes ambiguous:

- propagation scope shrinks
- routing consequences soften
- quarantine may be replaced by probation

### detector accountability

If a node repeatedly emits bad-faith suspicion or manipulates reports:

- it accumulates immune-abuse suspicion itself
- immune action can route back onto the accuser

This is crucial:

> **The immune system must defend against false accusation as well as false routing.**

---

## 11. Bootstrap Mode vs Mature Mode

This is one of the most important planning distinctions.

### Bootstrap mode

Applies when the network is still small and the graph is not deep enough for rich triangulation.

Characteristics:

- fewer nodes
- weaker second-order evidence
- more conservative routing assumptions
- more local suspicion, less global confidence

In bootstrap mode:

- prefer redundant gossip
- quarantine only on high-confidence structural evidence
- rely more on path diversity than on strong immune conclusions

### Mature mode

Applies once the graph is large and diverse enough for robust triangulation.

Characteristics:

- many independent witnesses
- richer topology geometry
- stronger clique detection
- safer suspicion propagation

In mature mode:

- immune response can become faster and more distributed
- global contamination mapping becomes more meaningful

This avoids pretending that a tiny early graph has the same immune power as a mature field.

---

## 12. Compatibility with K2, K4, and `eta = 0`

### K2

The immune system may constrain routing and capability surfaces.
It may not forge human authorization or bypass K2.

### K4

Quarantine and recovery do not erase historical truth.
Exited nodes lose active standing, but records remain according to continuity doctrine.

### `eta = 0`

Immune actions may not become a revenue engine.
Penalties must route only to:

- burn
- harmed counterparties
- shared immune infrastructure

never to central profit.

---

## 13. The Minimal Runtime Sequence

The clean planning sequence is:

```text
1. telemetry event arrives
2. local node computes anomaly score
3. if anomaly > threshold_local:
   - increase redundancy
   - trigger re-probes
4. if corroboration appears:
   - emit SuspicionEnvelope to bounded scope
   - reduce routing preference
5. if contamination threshold crossed:
   - apply quarantine scope
   - emit public immune receipt / attestation
6. recovery clock starts
7. remediation evidence accumulates
8. standing is restored gradually or quarantine remains
```

That sequence must work even if:

- the adaptive layer partially fails
- half the network ignores the latest extension
- the organism is still in a small early graph

---

## 14. What This Spec Is Not

This is **not**:

- a claim that the full immune layer is live
- permission to foreground SPECTRE in GTM now
- proof that triangulation math is already production-ready
- justification for automated social punishment
- a claim that AIA or Cortex alone provides a live distributed immune system

It is:

- the planning grammar for distributed defense
- kept subordinate to the rooted proof sequence
- compatible with the narrower prototype truth that BEAM route energy and
  replay contracts exist in controlled runtime conditions

---

## 15. Canonical Compression

> **The SPECTRE immune system should detect lies through corroborated structure, quarantine contamination without central profit, and always degrade back to safe dumb routing before it degrades into authoritarian automation.**

Or shorter:

> **First do no capture. Then do no erasure. Then route around disease.**

---

## 16. Cross-References

- `05_ARCHITECTURE.md`
- `30_SYNERGY.md`
- `35_IMMUNE_SYSTEM_ECONOMICS.md`
- `40_EMPTY_THRONE_GOVERNANCE.md`
- `42_K4_BUSINESS_ACCOUNT_CONTINUITY.md`
- `44_REORIENTATION_AFTER_EXIT_AND_UPGRADE.md`
- `45_PHI_V_SUITE_SYNTHESIS_AND_NEXT_TARGET.md`
- `130_BOUNDARY_AUDIT_ORGANISM_MODEL_2026_04_24.md`
