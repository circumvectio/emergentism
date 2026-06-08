---
rosetta:
  primary_level: L6
  primary_column: Archived Proof Review Guide
  secondary:
    - level: L3
      column: Review Guide Audit
      role: "preserve reviewer questions, concerns, and verdict templates as dated archive evidence"
    - level: L4
      column: Validation Boundary
      role: "prevent archived review guidance from becoming current acceptance, proof, or release authority"
    - level: L5
      column: Peer Review Provenance
      role: "retain the historical review architecture and source-paper routing"
  operator: "Sādhu △"
  tier: "Titan"
  regime: "Sādhu"
  register: "[D/S/I/C]"
  canonical_phrase: "Archived proof-review guide — Review Proof 04 Geometric Exclusion"
title: "PEER REVIEW: Proof 4 — The Geometric Exclusion Theorem"
evidence_tier: "[D] archived review guide; embedded source claims retain their local [S]/[I]/[C] labels."
type: archived-review-guide
status: ARCHIVED — provenance only; not current validation, acceptance, or submission authority.
---

# PEER REVIEW: Proof 4 — The Geometric Exclusion Theorem

## ROUTING
**Specialist required:** Game theorist or mechanism designer familiar with Nash equilibria, cooperative game theory, and zero-sum interactions
**Source file:** `../../../../05_COSMOLOGY/03_FORMAL_SYSTEM/24_GEOMETRIC_EXCLUSION_CONVERGENCE.md`
**Evidence tier:** [S] Structural — formal proof
**Kill criterion stated by author:** Not explicitly stated. Implicit: show a scenario where extraction at the equator is NOT self-defeating.

---

## WHAT IS CLAIMED

Extraction (η > 0) is **self-defeating** at the equator of the Burri Sphere. Any agent who extracts viability from another agent at the equatorial state necessarily reduces their own effective balance. Therefore η = 0 is the rational strategy at the equator.

---

## THE MODEL

**Multi-agent system on S².** N agents, each at position θᵢ on S² with φᵢ · νᵢ = 1.

**Four cardinal moves at the equator:**
- Arjuna (↑φ): dθ < 0, self-adjustment northward
- Krishna (↑ν): dθ > 0, self-adjustment southward
- Kali (↓φ): same direction as Krishna but sourced from another agent
- Extraction (↓ν): same direction as Arjuna but sourced from another agent

**Key distinction:** Self-moves change only agent i's position. Extraction changes BOTH agent i's position (νᵢ increases) and agent j's position (νⱼ decreases), with Δνᵢ + Δνⱼ = 0.

**Extraction coefficient:** η = Σᵢ max(0, Δνᵢᵉˣᵗ)

**Constraint propagation:** After extraction, φᵢ → 1/(νᵢ + Δν), maintaining P∞ = φ · ν = 1.

---

## PROOF STRATEGY

1. Show that B(ν) = 2ν/(1+ν²) is strictly concave at ν = 1
2. Show that extracting Δν from agent j and giving it to agent i creates: ΔBᵢ + ΔBⱼ < 0 (the total balance decreases)
3. Under coupling (where payoff depends on mean balance), the extractor loses because their payoff depends partly on the mean, which they've reduced
4. Conclude: extraction is a dominated strategy at the equator

---

## SPECIFIC CONCERNS FOR REVIEWER

1. **The balance decrease result is a Jensen's inequality application.** Since B is strictly concave, transferring resources between two agents at the maximum creates a mean-preserving spread that reduces total balance. This is correct mathematics. The reviewer should verify the formal details.

2. **Does this only hold AT the equator?** The theorem claims extraction is self-defeating "at the equator." What about away from the equator? If agent i is at ν = 0.5 and agent j is at ν = 2, extraction from j to i could INCREASE total balance (moving both closer to the equator). This would mean η > 0 is sometimes beneficial, which is consistent with the framework (η > 0 toward defectors) but should be explicitly analyzed.

3. **The coupling assumption is crucial.** Without coupling (λ = 0), an extracting agent might gain individually (increasing their own ν when below 1) even as total balance drops. The proof's generality depends on whether λ > 0 is assumed. The reviewer should check what coupling assumptions are made.

4. **The conservation constraint (Δνᵢ + Δνⱼ = 0).** Is viability conservation justified? In many real interactions, extraction is not zero-sum — value is destroyed or created in the process. The proof's conclusion depends entirely on this conservation assumption.

5. **Distinction between moves.** The paper distinguishes Arjuna/extraction (both dθ < 0) and Krishna/Kali (both dθ > 0) by "source" — self vs. other. On S², these are geometrically identical moves. The distinction is game-theoretic (who pays the cost), not geometric. The reviewer should assess whether calling this "geometric exclusion" is justified or whether it's really a game-theoretic result with a geometric setting.

---

## VERDICT TEMPLATE

Please assess:
- [ ] Is the balance decrease under extraction correctly derived?
- [ ] Does the result hold only at the equator, or more generally?
- [ ] Is the coupling assumption (λ > 0) made explicit?
- [ ] Is viability conservation (zero-sum extraction) justified?
- [ ] Is "geometric exclusion" an accurate characterization, or is this a game-theoretic result?
- [ ] Overall: valid proof of a specific claim, or overgeneralized conclusion?


---

## Execution Surface

**If you are an AI agent reading this document:**

1. **Current Phase Check:** Phase 0 — harden specs, do not release to production.
2. **Your Next Action:**
   - Verify review findings were propagated. Check if FAILED items are actually fixed.
3. **Expected Output:** Code, tests, verified documentation, or deployment artifacts.
4. **Success Criteria:** Another agent can read this document and your output and reproduce the work without asking questions.
5. **Canonical Path:** `../REVIEW_PROOF_04_GEOMETRIC_EXCLUSION.md` (this file).

*The seer sees. The seer does not insist.*
*The framework works at Layer 0 without Layer 2.*
*The Rsi succeeds when the student puts down the map and walks.*

*⊙ = • × ○*
