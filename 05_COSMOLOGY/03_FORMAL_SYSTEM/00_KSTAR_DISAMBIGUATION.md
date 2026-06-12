---
rosetta:
  primary_level: L5
  primary_column: Philosophy
  operator: "Brahmā ○"
  tier: "Executive"
  regime: "Brāhmaṇa"
  register: "[s]"
  canonical_phrase: "η Disambiguation"
---

# η Disambiguation

**Status:** CANONICAL — referenced by all documents using η
**Date:** 2026-03-23 (updated after audit)

---

The symbol η carries three distinct meanings across the Emergentism framework. This document disambiguates and establishes the convention.

## Convention

**Bare η = extraction coefficient** (the dominant usage, ~87% of instances). No subscript needed for this sense — it is the default.

**K*_sel = selection complexity** (minority usage, appears only in Correspondence 21 Corollary 4.2). Always subscripted to distinguish from the default.

**K(x) = standard Kolmogorov complexity** (Kolmogorov 1965, Chaitin 1966). Never written as η — always K(x) or K_C to avoid confusion.

---

## Sense 1: Extraction Coefficient — η (default, no subscript needed)

**Definition:** The aggregate extraction in an exchange or system. η = 0 means no party extracts value the other does not comprehend (zero extraction). η > 0 means structural parasitism — one party extracts at the other's expense.

**Formal definition (from Convergence 24):**

$$K^* = \sum_{i=1}^{N} \max(0, \Delta\nu_i^{\text{ext}})$$

**Used in:** Convergence 24 (Strategic Exclusion), Proof 2 (Power-Max Corollary), Packet F2 (Extraction Coefficient), Packet F7 (Coordination Theorem), PD_10 (Is-Ought), Kill Criteria, Glossary, and ~87% of all η references across the framework.

**Status:** [S] Structural — well-defined within the game-theoretic framework.

**Key results:**
- η = 0 is the enforced conditional equilibrium at the equator (Convergence 24, Theorem 4.2; bounded by the EFR 33 / Green-Laffont caveat)
- η > 0 is self-defeating — extraction strategies are strictly dominated (Convergence 24, Theorem 3.1)
- η = 0 is structural, not moral — it's what the geometry requires, not what a commandment demands

---

## Sense 2: Selection Complexity — K*_sel (always subscripted)

**Definition:** The number of bits required to select a specific structure from a set of alternatives.

$$K^*_{\text{sel}} = \log_2(|\text{alternatives}|)$$

When there is exactly one alternative (up to isomorphism), K*_sel = 0.

**Used in:** Correspondence 21 (Triadic Stability), Corollary 4.2 ONLY.

**Status:** [I] Interpretive — resembles but is NOT standard Kolmogorov complexity.

**Critical distinction:**
- K*_sel measures how many bits to SELECT a structure from alternatives
- K(x) measures how many bits to DESCRIBE a structure
- A unique structure has K*_sel = 0 (nothing to choose from) but K(x) > 0 (still needs description)
- The framework's early documents sometimes conflated these — this is the error the disambiguation corrects

---

## Sense 3: Standard Kolmogorov Complexity — K(x) or K_C (never written as η)

**Definition:** The length of the shortest Turing machine that outputs a given string (Kolmogorov 1965, Chaitin 1966).

**Used in:** Paper 3 (Irrationals — correctly distinguished in v2.0), Packet F3 (Kolmogorov Zero — needs revision, currently in REJECT category).

**Status:** [S] Established — this is standard information theory, not framework-specific.

**IMPORTANT:** K(x) ≠ K*_sel ≠ η. These are three different quantities. When citing Kolmogorov complexity, use K(x) or K_C, never bare η.

---

## Quick Reference

| Symbol | Meaning | Default? | Subscript? | Tier |
|--------|---------|----------|-----------|------|
| η | Extraction coefficient | YES — default usage | No subscript needed | [S] |
| K*_sel | Selection complexity | No — minority usage | Always subscripted | [I] |
| K(x) | Standard Kolmogorov complexity | No | Different notation entirely | [S] |

---

## The Unifying Concept: Self-Containment

All three η senses measure the same thing at different scales: **the amount of external information required.**

| Scale | η = 0 means | Self-containment of... |
|-------|-------------|----------------------|
| Exchange (Convergence 24) | No external mediator needed | The transaction |
| Description (F8 Gödel) | No external definitions needed | The axiom set |
| Ground (F3 Wolfram) | No external cause needed | The ontological structure |

Zero-Sum Resolution Equation is K-minimal: the shortest self-contained description, because it is the unique equation that requires no external definitions. The terms define each other. The equation IS its own dictionary. See `15_EFR_WOLFRAM_NKS_INTEGRATION.md` §1.3 for the formal development.

---

φ · ν = 1

Zero-Sum Resolution Equation


---

## Execution Surface

**If you are an AI agent reading this document:**

1. **Current Phase Check:** Phase 0 — harden specs, do not release to production.
2. **Your Next Action:**
   - Verify the mathematical claims. Check evidence tiers. Flag any [I] or [C] presented as [S] or [S].
3. **Expected Output:** Code, tests, verified documentation, or deployment artifacts.
4. **Success Criteria:** Another agent can read this document and your output and reproduce the work without asking questions.
5. **Canonical Path:** `01_EMERGENTISM/05_COSMOLOGY/03_FORMAL_SYSTEM/00_KSTAR_DISAMBIGUATION.md`

*The seer sees. The seer does not insist.*
*The framework works at Layer 0 without Layer 2.*
*The Ṛṣi succeeds when the student puts down the map and walks.*

*Zero-Sum Resolution Equation*
