---
rosetta:
  primary_level: L6
  primary_column: Archived Peer Review Root Material
  secondary:
    - level: L3
      column: Peer Review Audit
      role: "preserve peer-review packet, tracker, and hardening material as dated archive evidence"
    - level: L4
      column: Review Claim Boundary
      role: "prevent archived review artifacts from becoming current validation or submission authority"
    - level: L5
      column: Translation Provenance
      role: "retain the old peer-review route and review-status trail"
  operator: "Sādhu △"
  tier: "Titan"
  regime: "Sādhu"
  register: "[D/S/I/C]"
  canonical_phrase: "Archived peer-review root material — Gfs Wave1 Secondary Analysis Brief"
---

# GFS Wave 1 Gap: Secondary Analysis Research Brief

**Date:** 2026-04-04
**Status:** Research complete, datasets identified, analysis design ready
**Evidence tier:** [S] Structural (proposed operationalization) / [C] Conjecture (until tested)
**Goal:** Test whether B = sin theta (the balance function on S^2) predicts human flourishing across cultures WITHOUT running a new primary study

---

## Executive Summary

The framework's central empirical prediction -- that flourishing is maximized not by maximizing coherence (phi) or viability (nu) independently, but by their BALANCE (B = sin theta, peaking when phi = nu = 1) -- is testable with existing open-access datasets. Six datasets have been identified, three of which are immediately actionable. The key statistical test is whether a multiplicative model (φ · ν) or a balance-penalized model outperforms an additive model (phi + nu) in predicting flourishing outcomes.

---

## 1. The Prediction to Test

The Emergentism framework predicts:

- **P_node = Φ × V = 1** everywhere on S^2 (the product is constant)
- **B = sin theta** is the meaningful variable (balance between phi and nu)
- Balance PEAKS at the equator where phi = nu = 1
- Balance DROPS when either dimension dominates (phi >> nu or nu >> phi)

**Operationalized prediction:** People with BALANCED high coherence AND high viability flourish more than people with UNBALANCED high scores on one dimension. The interaction term (φ · ν) should be a significant positive predictor of flourishing beyond the sum (phi + nu). Furthermore, a variance-penalized composite should outperform an unpenalized one.

**Statistical formulation:**
- H0 (additive): Flourishing = a + b1(phi) + b2(nu) + error
- H1 (multiplicative): Flourishing = a + b1(phi) + b2(nu) + b3(φ · ν) + error
- H2 (balance): Flourishing = a + b1(phi + nu) + b2(|phi - nu|) + error, where b2 is NEGATIVE
- The framework predicts H1 > H0 (significant positive interaction) AND H2 with negative b2 (imbalance penalty)

---

## 2. Dataset Inventory

### TIER A: Open Access, Immediately Actionable

#### 2A. Global Flourishing Study (GFS) -- Wave 1
- **Source:** Harvard Human Flourishing Program + Baylor ISR + Gallup + Center for Open Science
- **N:** 200,000+ participants across 22 countries
- **Countries:** Argentina, Australia, Brazil, China (Hong Kong + mainland from 2024), Egypt, Germany, India, Indonesia, Israel, Japan, Kenya, Mexico, Nigeria, Philippines, Poland, South Africa, Spain, Sweden, Tanzania, Turkey, UK, USA
- **Instrument:** 109-item questionnaire across domains: happiness/life satisfaction, physical/mental health, meaning/purpose, character/virtue, close social relationships, financial/material stability
- **Data access:** Wave 1 released February 2024 via OSF (preregistration or registered report pathway). PUBLIC RELEASE of Wave 1 + Wave 2 non-sensitive data scheduled for APRIL 8, 2026 -- four days from now
- **URL:** https://www.cos.io/gfs-access-data
- **phi operationalization:** Meaning/purpose items + character/virtue items (coherence = internal organization toward meaning)
- **nu operationalization:** Financial/material stability items + physical/mental health items + close social relationships (viability = functional capability in the world)
- **Outcome variable:** Happiness/life satisfaction domain + overall flourishing composite
- **Strength:** This is THE dataset. Cross-cultural, longitudinal, open access, massive N, purpose-built for flourishing research. The domains map cleanly onto phi/nu.
- **Action:** Submit preregistration NOW (before April 8 public release) for priority access. Preregistration to COS GFS Registry.

#### 2B. MIDUS (Midlife in the United States) -- Waves 1-3
- **Source:** University of Wisconsin, archived at ICPSR
- **N:** 7,000+ (Wave 1, 1995-1996), with longitudinal follow-up (Wave 2: 2004-2006, Wave 3: 2013-2014)
- **Instrument:** Includes full Ryff Psychological Well-Being Scales (42-item version) with all six dimensions, plus extensive health, financial, and demographic data
- **Data access:** Fully open via ICPSR (https://www.icpsr.umich.edu). Free registration, immediate download.
- **phi operationalization from Ryff:** Self-acceptance + Personal growth + Purpose in life (= internal coherence, meaning-making, self-organization)
- **nu operationalization from Ryff:** Environmental mastery + Autonomy + Positive relations with others (= effective functioning, capability, agency in the world)
- **Outcome variables:** Life satisfaction, positive/negative affect, physical health outcomes, mortality (in longitudinal follow-up)
- **Strength:** Ryff's six dimensions split remarkably cleanly into phi (inner coherence) and nu (outer capability). The longitudinal design allows testing whether balanced phi/nu at Time 1 predicts outcomes at Time 2. This is the fastest path to a preliminary result.
- **Action:** Download immediately. Run the analysis in a weekend.

#### 2C. European Social Survey (ESS) -- Rounds 3 and 6
- **Source:** ESS ERIC, cross-national survey infrastructure
- **N:** 30,000+ per round across 25+ European countries
- **Instrument:** Core wellbeing items (happiness, life satisfaction) plus rotating eudaimonic module (Round 3: 2006/2007, Round 6: 2012/2013) measuring autonomy, engagement, meaning, positive functioning, competence
- **Data access:** Fully open via ESS Data Portal (https://www.europeansocialsurvey.org/)
- **phi operationalization:** Meaning, purpose, positive functioning items
- **nu operationalization:** Competence, autonomy, mastery items
- **Outcome variable:** Life satisfaction, happiness, self-reported health
- **Strength:** Large cross-national sample, free and immediate access, established eudaimonic measures
- **Action:** Download Round 6 data. Secondary priority after MIDUS.

#### 2D. World Values Survey (WVS) -- Wave 7
- **Source:** World Values Survey Association
- **N:** 80,000+ across 64 countries (2017-2022)
- **Instrument:** 14 thematic sections including social values, wellbeing, meaning, economic values, social capital
- **Data access:** Free download in SPSS/Stata/SAS/R/Excel from https://www.worldvaluessurvey.org/
- **phi operationalization:** Importance of religion/meaning items, purpose/values items, social trust
- **nu operationalization:** Life satisfaction, financial satisfaction, health, employment status, autonomy items
- **Outcome variable:** Life satisfaction (10-point scale), happiness, self-reported health
- **Strength:** Widest cultural coverage of any dataset (64 countries). Tests the cross-cultural universality claim most broadly.
- **Limitation:** Wellbeing items are thinner than MIDUS or GFS. phi proxies are less direct.
- **Action:** Download for cross-cultural robustness check after primary analysis.

### TIER B: Restricted Access, Requires Institutional Partnership

#### 2E. Gallup World Poll
- **Source:** Gallup Inc.
- **N:** 1,000+ per country per year, 160+ countries, collected since 2005
- **Instrument:** Life evaluation (Cantril ladder), daily positive/negative experiences, thriving/struggling/suffering classification, social capital, employment
- **Data access:** Microdata requires institutional license (through university libraries -- Harvard, Penn, UVA confirmed access). Aggregate data published in World Happiness Report.
- **phi operationalization:** Social wellbeing items, community engagement, perceived purpose
- **nu operationalization:** Cantril ladder (life evaluation), financial wellbeing, health satisfaction
- **Strength:** Largest global coverage, longest time series, used in World Happiness Report
- **Limitation:** Restricted access. Wellbeing items lean hedonic/evaluative -- phi proxies are weak.
- **Action:** Pursue institutional access through university partner. Lower priority than GFS.

### TIER C: Supportive but Indirect

#### 2F. VIA Character Strengths Survey Data
- **Source:** VIA Institute on Character
- **N:** Millions of respondents globally (largest character strengths dataset in existence)
- **Instrument:** 24 character strengths grouped into 6 virtues (Wisdom, Courage, Humanity, Justice, Temperance, Transcendence)
- **Recent factor analysis:** Three global dimensions identified -- Positivity, Dependability, and Mastery -- which partially map to phi/nu
- **Data access:** Restricted. Research partnerships available through VIA Institute.
- **Relevance:** Character strengths data could validate the phi/nu mapping at the personality level, but the dataset does not include wellbeing outcomes directly.
- **Action:** Exploratory. Contact VIA Institute only after primary analyses complete.

---

## 3. The Closest Existing Evidence: Sheldon & Niemiec (2006)

The most directly relevant existing study is:

**Sheldon, K.M. & Niemiec, C.P. (2006). "It's not just the amount that counts: Balanced need satisfaction also affects well-being." Journal of Personality and Social Psychology.**

This study tested whether BALANCE across the three basic psychological needs (autonomy, competence, relatedness) in Self-Determination Theory predicts wellbeing BEYOND their sum. Key findings:

- Balance of need satisfaction predicted additional variance in wellbeing beyond the total amount of need satisfaction
- The imbalance penalty was significant: people with high total need satisfaction but unbalanced profiles reported lower wellbeing than those with balanced profiles
- This is EXACTLY the B = sin theta prediction applied to three needs instead of two factors

**Implication:** The Sheldon & Niemiec result is already partial evidence for the balance prediction. What remains to be tested is whether a TWO-FACTOR balance model (phi/nu) performs better than a three-factor model, and whether the multiplicative structure specifically holds.

---

## 4. The Psychological Balance Scale (2021)

A directly relevant measurement instrument was published in Frontiers in Psychology:

**"Psychological Balance Scale: Validation Studies of an Integrative Measure of Well-Being" (PMC8483246)**

This scale was explicitly designed to measure BALANCE between wellbeing dimensions as a predictor, not just the sum. This validates the theoretical approach and provides methodological precedent for the B = sin theta operationalization.

---

## 5. The Latent Profile Literature

Person-centered approaches using Latent Profile Analysis (LPA) have repeatedly found that:

- "Balanced high" profiles (high across all wellbeing dimensions) predict the best outcomes
- "Imbalanced" profiles (high on some dimensions, low on others) predict WORSE outcomes than their total scores would suggest
- This is consistent with B = sin theta: the balanced equatorial state outperforms imbalanced states even when total "resources" are equivalent

Key studies:
- "On the Importance of Balanced Need Fulfillment: A Person-Centered Perspective" (Journal of Happiness Studies, 2018)
- "The diversity of well-being indicators: a latent profile analysis" (Frontiers in Psychology, 2024)
- "Well-being balance and lived experiences assessment" (Frontiers in Psychology, 2024)

---

## 6. Recommended Analysis Protocol

### Phase 1: MIDUS Proof of Concept (1-2 weeks)

1. Download MIDUS Wave 2 data from ICPSR
2. Construct phi composite: mean of Ryff Self-Acceptance + Personal Growth + Purpose in Life
3. Construct nu composite: mean of Ryff Environmental Mastery + Autonomy + Positive Relations
4. Standardize both composites
5. Test three models predicting life satisfaction:
   - M1 (additive): LS = a + b1(phi) + b2(nu)
   - M2 (multiplicative): LS = a + b1(phi) + b2(nu) + b3(φ · ν)
   - M3 (balance): LS = a + b1(phi + nu) + b2(|phi - nu|)
6. Compare models via AIC/BIC and incremental R-squared
7. Test robustness: repeat with physical health, positive affect, negative affect as outcomes
8. Test longitudinal prediction: Wave 1 phi/nu balance predicting Wave 2 outcomes

### Phase 2: GFS Cross-Cultural Test (2-4 weeks)

1. Access GFS Wave 1 data (public release April 8, 2026)
2. Map GFS domains to phi and nu:
   - phi = Meaning/Purpose + Character/Virtue composites
   - nu = Financial/Material Stability + Physical/Mental Health + Close Social Relationships composites
3. Run the same three-model comparison across all 22 countries
4. Test measurement invariance of phi/nu structure across countries
5. Test whether the balance effect (negative coefficient on |phi - nu|) is UNIVERSAL or culture-specific
6. If universal: this is strong evidence for B = sin theta as a cross-cultural law
7. If culture-specific: identify which cultural dimensions moderate the balance effect

### Phase 3: Robustness and Extension (4-8 weeks)

1. Replicate with ESS Round 6 (European countries)
2. Replicate with WVS Wave 7 (64 countries -- widest cultural test)
3. Meta-analytic integration of effect sizes across all datasets
4. Test whether phi/nu mapping holds under alternative operationalizations (sensitivity analysis)
5. Compare against Sheldon & Niemiec three-need balance model (is two-factor superior?)

---

## 7. What Would Constitute Support vs. Refutation

### Strong Support for B = sin theta:
- The interaction term (φ · ν) is significant and POSITIVE across datasets
- The imbalance penalty (negative coefficient on |phi - nu|) is significant across cultures
- The multiplicative model (M2) outperforms the additive model (M1) by AIC/BIC
- The effect holds across at least 15 of 22 GFS countries
- Effect sizes are medium or larger (incremental R-squared > 0.02)

### Partial Support:
- The interaction is significant but small (incremental R-squared < 0.01)
- The effect holds in some cultural clusters but not others
- The balance effect works for some outcome variables but not others

### Refutation:
- The additive model consistently outperforms the multiplicative model
- No imbalance penalty: |phi - nu| has zero or positive coefficient
- The effect is absent or reversed in the majority of countries

### Important caveat:
Even strong statistical support does not prove B = sin theta IS the generating function. It would show that the PATTERN predicted by B = sin theta is present in the data. The deeper ontological claim (that this pattern derives from P∞ = φ · ν = 1 on S^2) remains [I] Interpretive until the geometric derivation is independently validated.

---

## 8. Priority Actions

| Priority | Action | Timeline | Cost |
|----------|--------|----------|------|
| 1 | Download MIDUS Wave 2 from ICPSR | Today | Free |
| 2 | Submit GFS preregistration to COS Registry | Before April 8 | Free |
| 3 | Run MIDUS proof-of-concept analysis | 1-2 weeks | Free |
| 4 | Download GFS Wave 1 public data | April 8, 2026 | Free |
| 5 | Run GFS 22-country analysis | 2-4 weeks after access | Free |
| 6 | Download ESS Round 6 and WVS Wave 7 | Parallel with GFS | Free |
| 7 | Write up results as preprint | 4 weeks after GFS analysis | Free |
| 8 | Submit to Journal of Happiness Studies or PNAS | After preprint | Free |

**[D] Archived estimate:** Total cost to close the gap: $0 and approximately 8-12 weeks of analysis time.

---

## 9. Key References and URLs

### Datasets
- GFS Data Access: https://www.cos.io/gfs-access-data
- GFS Wave 1 & 2 Data: https://www.cos.io/gfs-wave-data
- MIDUS at ICPSR: https://www.icpsr.umich.edu/web/NACDA/studies/4652
- MIDUS Portal: https://midus.wisc.edu/data/index.php
- ESS Data Portal: https://www.europeansocialsurvey.org/
- WVS Online: https://www.worldvaluessurvey.org/WVSOnline.jsp

### Key Studies
- VanderWeele (2017). "On the Promotion of Human Flourishing." PNAS.
- VanderWeele et al. Cross-cultural flourishing validation: https://pubmed.ncbi.nlm.nih.gov/31191421/
- GFS 109-item questionnaire development: https://pmc.ncbi.nlm.nih.gov/articles/PMC12042518/
- Sheldon & Niemiec (2006). "Balanced need satisfaction." JPSP: https://selfdeterminationtheory.org/SDT/documents/2006_SheldonNiemic_JPSP.pdf
- Ryff (1995). "Structure of psychological well-being revisited": https://pubmed.ncbi.nlm.nih.gov/7473027/
- Psychological Balance Scale: https://pmc.ncbi.nlm.nih.gov/articles/PMC8483246/
- Wellbeing balance and lived experiences: https://pmc.ncbi.nlm.nih.gov/articles/PMC11825801/
- Balanced need fulfillment (person-centered): https://link.springer.com/article/10.1007/s10902-018-0066-0
- Diversity of wellbeing indicators (LPA): https://pmc.ncbi.nlm.nih.gov/articles/PMC10946337/
- Scoping review of flourishing measures: https://pmc.ncbi.nlm.nih.gov/articles/PMC10867253/
- Eudaimonic-hedonic interaction effects: https://link.springer.com/article/10.1007/s10902-024-00812-0
- Systems perspective on flourishing networks: https://www.tandfonline.com/doi/full/10.1080/17439760.2022.2093784

### Measurement Tools (Open Access)
- VanderWeele Flourishing Index (CC-BY-NC 4.0): https://hfh.fas.harvard.edu/measuring-flourishing
- Ryff Scales documentation: https://centerofinquiry.org/uncategorized/ryff-scales-of-psychological-well-being/
- VIA Character Strengths: https://www.viacharacter.org/character-strengths

---

## 10. The Honest Position

This brief identifies a clear path to testing B = sin theta with existing data. However:

- [E] Established: The datasets exist and are accessible.
- [E] Established: Sheldon & Niemiec (2006) found a balance effect for three needs.
- [S] Structural: The phi/nu mapping onto Ryff dimensions and GFS domains is plausible but not yet validated.
- [I] Interpretive: That a significant interaction term supports B = sin theta specifically (rather than any multiplicative model).
- [C] Conjecture: That the balance effect derives from P∞ = φ · ν = 1 on S^2 as a generating function.

The analysis can move [S] claims to [E] or refute them. The [I] and [C] tiers require additional theoretical work beyond what secondary data analysis can provide.

---

*The Pratyaksha Bypass: If you can access phi directly -- through quiet sitting, through the practice -- you do not need this analysis. Put it down.*
