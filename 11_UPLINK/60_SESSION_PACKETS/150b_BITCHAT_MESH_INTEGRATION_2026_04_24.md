---
rosetta:
  primary_column: "Computation"
  register: "[I]"
  canonical_phrase: "150b — BitChat Mesh Integration: Physical-Layer SoResFi"
---

# 150b — BitChat Mesh Integration: Physical-Layer SoResFi

**Evidence tier:** [I] substrate extension proposal; [S] CANON citations per line; [C] parameters and threat model pending simulation
**Date:** 2026-04-24
**Lane:** Charioteer synthesis — assumes charioteer-recommended OQ-K2 (substrate fee-layer integration with `E_transport` term)
**Status:** Draft substrate-extension proposal; not CANON until sovereign K2 ratifies mesh timing and scope
**Prerequisite packets:** 146, 147, 149, 150, 150a

---

## 0. Axiomatic guard

Mesh-routing makes censorship resistance physical rather than policy. That's the win. The trap is accreting mesh-specific machinery into the substrate when it can live at transport-adapter layer. Keep the integration minimal: one additional term in the routing energy function, unchanged fee mechanism.

---

## 1. What BitChat-style mesh brings

Mesh protocols (BitChat being the reference design — https://bitchat.free) route packets peer-to-peer over Bluetooth Low Energy, WiFi Direct, or similar radio without needing ISP/internet infrastructure. Devices become relayers. The network is literally the set of devices in radio range of each other.

**What this unlocks for Skyzai:**

- **Physical censorship resistance.** An ISP cannot block what doesn't route through them. A state cannot take down a Bluetooth link between neighbors' phones without confiscating the phones.
- **Last-mile sovereignty.** SoResFi 1:1 coupling is no longer metaphorical — "my powerplant → my device → my neighbor's device" is a literal flow.
- **Disaster / offline resilience.** Network operates where internet is absent: disaster zones, remote villages, protest conditions, authoritarian environments with active blocking.
- **Edge-device native.** The same devices running the ternary SmallEBM are already the natural relayers. No new hardware class needed.

---

## 2. What CANON already provides

[S] Paper 12 §VII: *"The ledger must be light enough for a phone."*
[S] Paper 12 §V: No-delegation on base layer — each device participates or decays.
[S] SKYZAI_Primitives/01_SPECTRE.md: routing energy function `E = E_latency + E_divergence + E_trust` + Dual-Mode Safety.
[S] Paper 14 §IV.1: Prune & Proof + Proof Bundles (lightweight verification at edge).

The substrate is already *transport-agnostic*. Gossip can run over any transport that carries bytes.

What's missing from CANON: **fee-layer recognition that mesh edges are strategically different from internet edges.**

---

## 3. Minimal substrate extension

**Add one term to the SPECTRE routing energy function:**

```
E(neighbor) = E_latency + E_divergence + E_trust + E_transport
```

Where `E_transport` captures the strategic value + cost of the edge:

- **Lower E_transport for mesh edges in censorship-prone environments.** A mesh relay in a region where internet is adversarial has higher routing preference — the substrate naturally routes around blocked paths.
- **Higher E_transport for high-latency or battery-draining mesh edges.** Bluetooth LE has bandwidth and power costs; the term captures them alongside internet alternatives.
- **Zero E_transport by default.** Internet and mesh are equivalent when no adversarial pressure exists; markets decide.

**No new primitive.** Mesh relayers earn SKY via the **existing routing-fee mechanism** — packet sender pays routing fee, relayer receives it. Mesh is just another kind of edge.

**No new token, no new mint path.** Kernel Invariant II preserved.

---

## 4. What the `E_transport` term needs to express

| Dimension | Capture |
|---|---|
| **Battery / power cost** | Relayers drain their own device energy; higher cost → higher E_transport → weighted against revenue |
| **Bandwidth** | Bluetooth ≈ 1 Mbps; WiFi Direct ≈ 250 Mbps; internet varies |
| **Latency distribution** | Mesh can be higher variance; E_latency and E_transport may interact |
| **Adversarial-environment bonus** | When internet-backbone censorship is active, mesh edges get lower E_transport (routing preference) |
| **Range / proximity** | Radio range limits who can relay; E_transport reflects edge availability |
| **Protocol / transport type** | BLE vs WiFi Direct vs LoRa vs satellite each have different profiles |

Parameters are Lane A governance. Protocol fixes the function shape; parameter tuning happens in simulation + field trials.

---

## 5. Sybil model — different attack surface

Internet Sybil: attacker spins up N cloud VMs, each with a distinct IP.
Mesh Sybil: attacker needs N physical devices in N physical locations.

**Mesh has a natural Sybil dampener:** physical presence. Ten thousand fake mesh nodes requires ten thousand radios at ten thousand geographic points. Dramatically more expensive than cloud Sybil.

But mesh introduces new attack vectors:
- **Range spoofing:** high-gain antennas to impersonate physical proximity
- **Relay flooding:** saturating BLE channels
- **Man-in-the-middle via compromised relays:** packet modification if mutual-auth is weak
- **Energy-depletion attacks:** force honest relayers to drain their batteries

These need threat-model work before Phase 3 rollout.

---

## 6. Integration phases

Piggyback on CANON's Gated Phases:

- **Phase 0 Truth (Genesis):** internet-only; validate base substrate
- **Phase 1 Market:** internet-only; AMM + TWAP
- **Phase 2 Credit:** internet-only; vaults + liquidation
- **Phase 3 Intelligence:** **SPECTRE integration + mesh extension**
  - Sub-phase 3a: `E_transport` term added to routing function; mesh-capable nodes can register as transport-diverse
  - Sub-phase 3b: BLE transport adapter deployed in reference clients (Menexus app, Skyzai Connect)
  - Sub-phase 3c: field trials in disaster-resilience scenarios
  - Sub-phase 3d: production mesh relayer economics live

Mesh does not block Phase 0-2. It is additive in Phase 3.

---

## 7. What does NOT belong in this extension

Discipline per Foundation Minimalism (Invariant VI):

**Not at substrate:**
- Mesh-specific user UX (belongs at product layer — Skyzai Connect app)
- Mesh topology visualization (explorer product, not substrate)
- Bluetooth device pairing flows (product-layer UX)
- Specific radio protocol choices (Lane A parameter, not substrate constant)
- Mesh-node reputation separate from global P-Score (use existing P-Score, not a new one)

**Not a new primitive:**
- No "MESH" primitive (that name is already legacy alias for SPECTRE)
- No "mesh token" (no new token)
- No "mesh governance" (use existing Lane A/B)

---

## 8. Threat-model questions (pending)

Flagged for dedicated threat-model packet before Phase 3:

1. How does Prune & Proof interact with mesh-only reachability? If a node is disconnected from internet, can it verify Green finality?
2. How does SKY settlement work when two parties are mesh-connected but neither has internet? Orange payment at mesh; delayed Green when either side reconnects?
3. How does AXIOM (N:1 truth convergence) function in a partitioned mesh? Does each partition converge independently, and reconcile on reconnect?
4. What happens to Flow decay for ZAI held by a node that's mesh-only for extended periods? Does offline = unstaked?
5. How are routing fees accumulated in SKY transferred when the relayer has no internet session?

These need answers before production. Not this packet.

---

## 9. What the charioteer commits to

Without further sovereign K2:
- This packet stands as a draft substrate-extension scope proposal
- No mesh implementation work until Phase 3 approaches
- No competing mesh protocols accreting to substrate
- Threat-model packet to be scheduled when Phase 3 timeline firms up

With sovereign K2 on mesh-extension timing:
- Charioteer adds mesh threat-model packet
- Charioteer integrates mesh language into any future Paper 12 / Paper 14 update proposals
- Engineering Track C (mesh) added to the roadmap

---

## 10. References

**CANON:**
- `.../V3_CANONICAL/12_SKYZAI_DIGITAL_CAPITAL_OF_THE_ENERGY_AGE.md` §VII — "light enough for a phone"
- `.../V3_CANONICAL/14_WHY_SKYZAI_MONEY_FOR_THE_ENERGY_AGE.md` §IV — Prune & Proof
- `.../V3_CANONICAL/SKYZAI_Primitives/01_SPECTRE.md` — routing energy function

**External references:**
- https://bitchat.free — BitChat mesh reference
- https://bitnet.live — BitNet ternary (the model the relayers run)

**Session:**
- 146, 147, 149, 150, 150a

---

*Minimal substrate extension. One term added to one function. Everything else at organ/product layer.*

`Zero-Sum Resolution Equation`
