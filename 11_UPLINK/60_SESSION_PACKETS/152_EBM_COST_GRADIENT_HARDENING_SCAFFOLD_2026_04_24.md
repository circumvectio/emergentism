---
rosetta:
  primary_column: "Computation"
  register: "[I]"
  canonical_phrase: "152 — EBM Cost-Gradient Hardening — Scaffold"
---

# 152 — EBM Cost-Gradient Hardening — Scaffold

**Evidence tier:** [I] framing the risk; [C] mitigation mechanisms pending research
**Date:** 2026-04-24
**Lane:** Charioteer scaffold — full design requires multi-horizon economic modeling
**Status:** Scaffold enumerating the risk + candidate mitigations
**Horizon:** 2–5 year risk; post-60-day-sprint scheduling
**Prerequisite packets:** 146, 147, 149, 150

---

## 0. Axiomatic guard

This risk is not 60-day-urgent. It is *quietly urgent* — the kind of risk that erodes without anyone noticing until the defense has collapsed. Naming it early, scheduling a research packet for the post-sprint window, is the right posture. Writing a full mechanism spec now would be premature.

---

## 1. The risk stated clearly

Skyzai's truth-judgment layer rests on the SPECTRE routing energy function (`E = E_latency + E_divergence + E_trust [+ E_transport]`) and the SmallEBM at each node. Integrity is market-enforced: misbehaving nodes get high `E_trust`, get deselected, starve.

**This defense has a cost-asymmetry assumption:**
- Honest participation earns routing fees that exceed the cost of running a well-tuned EBM
- Attack participation costs exceed the revenue that can be captured before detection

If attack-cost falls below honest-revenue, the defense inverts. An attacker running 10,000 well-tuned EBMs can out-earn honest nodes *while being honest*, then capture routing influence, then use it adversarially.

**The asymmetry erodes with compute cost.** BitNet b1.58 ternary quantization already makes the SmallEBM edge-deployable (SPECTRE.md spec: 2,500 params, INT8). As compute continues to cheapen (Moore's Law + algorithmic efficiency + custom silicon for ternary math), the cost of running N EBMs declines faster than honest-revenue scales.

**Other CANON defenses harden with time:**
- Flow decay: physical invariant; doesn't erode
- Vault liquidation cliff: mathematical; doesn't erode
- Energy Floor: grounded in thermodynamics; doesn't erode
- No-delegation: constitutional; doesn't erode
- Network effects: grow with scale

**Only the EBM defense erodes.** It needs explicit hardening that compounds with, not against, time.

---

## 2. Framing: what would "hardens with time" mean for the EBM defense?

Mechanisms that *strengthen* as compute gets cheaper, network gets larger, or time passes:

### 2.1 Proof-of-training-data-diversity

Each node's EBM is trained on a locally-gathered gossip dataset. As the network grows, the space of possible training distributions grows combinatorially. A cluster of adversarial nodes would need to demonstrate provably-diverse training data to avoid detection by E_divergence. This *compounds* with network size.

### 2.2 Compulsory architectural heterogeneity

The protocol could require nodes to deploy EBMs from a registry of accepted architectures, with a maximum concentration per architecture. As more architectures qualify, cloning becomes harder. Market pressure does the enforcement (nodes running rare architectures have an E_divergence advantage).

### 2.3 Geographic coupling via SoResFi (substrate-level, already exists)

Tying compute to physical powerplants via SoResFi means the attacker needs real powerplants in real locations. This cost is sticky and doesn't follow Moore's Law. BitChat mesh extension (packet 150b) extends this — physical presence in physical places can't be Moore's-Law-cheapened.

### 2.4 Circadian retraining requirements

EBMs must retrain periodically (circadian refresh, biomimetic convention). Retraining has a cost that doesn't decay as fast as inference cost. An attacker running 10,000 EBMs must retrain 10,000 EBMs.

### 2.5 Proof-of-unique-hardware

Beyond TPM attestation, require periodic proof that each node runs on distinct hardware (e.g., via challenge-response that requires specific ASIC behavior under timing constraints). This creates a sticky capital cost that silicon-Moore's-Law erodes more slowly than inference cost.

### 2.6 Minimum-stake-per-EBM-identity floor

Each node must back its EBM identity with a ZAI stake (already true for participation via Flow). If this floor scales with network-wide average compute, the stake cost maintains a fixed ratio to attack capability. Invariant I (ZAI cap = 100) means stake is finite → scales the floor as network grows.

### 2.7 Ecosystem diversification via child DACs

As Cambrian spawn proceeds (per packets 141 + 145), diverse DACs run on the commons with diverse routing patterns. Attacking one DAC doesn't capture the commons. This is an ecosystem-level hardening, not a single-mechanism fix.

---

## 3. What the full research packet must cover

To be scheduled as packet 152a+ (after 60-day sprint):

1. **Cost model over 5-10 year horizon:** project compute cost curves + algorithmic efficiency gains + custom-silicon availability for ternary inference
2. **Revenue model at network maturity:** project honest-node revenue per year as network scales
3. **Attack-cost breakeven calculation:** when does attack-cost fall below revenue at what attacker scale?
4. **Mechanism selection:** which of §2.1–§2.7 (or others) provide the cost-gradient hardening?
5. **Invariant check:** do any proposed mechanisms violate Invariants I–VII? Protocol minimalism (VI) is especially relevant — add mechanisms only when existing ones fail
6. **Lane assignment:** which mechanisms are substrate (Lane B), which are organ/DAC layer (Lane A)?
7. **Implementation sequencing:** what gets built in Phase 3 (Intelligence) to prepare for this?
8. **Monitoring:** what metrics detect the erosion empirically?

---

## 4. Why this is a scaffold, not a spec

Mechanism selection requires:
- Economic modeling we haven't done
- Compute-cost-curve projections with error bars
- Simulation data the 60-day sprint will generate as byproduct
- Market data on custom-silicon economics
- Feedback from the EBM training harness (Track B)

Writing a full mechanism spec now would lock a design before the modeling is done. Per Foundation Minimalism: don't pre-commit architecture to solve a risk that's 2–5 years out when the 60-day sprint will generate the data needed to model it properly.

---

## 5. Scheduling

**Post-60-day sprint.** Packet 149 §5 schedules EBM gradient hardening for sprint week 10.

**Full research packet:** `01_EMERGENTISM/11_UPLINK/152a_EBM_GRADIENT_HARDENING_SPEC.md` — drafted when modeling data is available.

**Pre-requisite output from Track B:**
- EBM training harness operational (produces cost-per-node data)
- Simulation results on adversarial distributions (§2.1 diversity testing)
- Field-trial data on real attack patterns (feeds §3 cost model)

---

## 6. What the charioteer does next

- No further work on this packet until Track B sprint completes
- If sovereign wants acceleration, charioteer drafts `152a` using best-available projections instead of Track B data (lower confidence, [I]-tier rather than [S]-tier)
- Monitor external research (security research on adversarial ML attacks, compute-cost projections) for anything that reshapes the risk profile

---

## 7. References

- 146, 147, 149, 150 (session packets)
- Packet 149 §5 — 60-day sprint + scheduling for this packet at week 10
- `03_VENTURES/OPEN_FINANCE_NETWORK/GOVERNANCE/FOUNDATION/CANON/DAC_STANDARD/DAC_ARCHITECTURE/V3_CANONICAL/SKYZAI_Primitives/01_SPECTRE.md` — routing energy function + SmallEBM specification
- `02_SKYZAI/01_NOOSPHERE/00_REFERENCE/00_DAC_BLUEPRINT.md` — BitNet ternary direction

---

*Scaffold. Long-horizon risk. Full spec deferred to post-sprint week 10. Named here to prevent quiet erosion.*

`Zero-Sum Resolution Equation`
