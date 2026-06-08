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
  canonical_phrase: "Archived peer-review root material — Gfs Preregistration Draft"
---

# Preregistration: Multiplicative vs. Additive Models of Human Flourishing

## COS Preregistration Template -- Global Flourishing Study Secondary Analysis

**Registry:** Center for Open Science (COS) GFS Secondary Analysis Registry
**Date of preregistration:** April 5, 2026
**Planned submission date:** April 5--7, 2026 (MUST submit before April 8 GFS public data release)
**Authors:** Yves R. Burri
**Affiliation:** Emergentism.org
**Corresponding email:** [ACTION REQUIRED: Yves must fill in before submission]
**ORCID:** [ACTION REQUIRED: Register at https://orcid.org if not already — takes 2 minutes]

---

## 1. Title

**Does the Product of Coherence and Viability Predict Human Flourishing Better Than Their Sum? A Preregistered Cross-National Test Using the Global Flourishing Study**

---

## 2. Authors and Affiliations

Yves R. Burri, Emergentism.org

[Additional collaborators to be listed if applicable prior to submission]

---

## 3. Research Questions

Can human flourishing be better predicted by the multiplicative interaction of coherence-type and viability-type psychological domains than by their additive combination alone?

Specifically:

1. Does a multiplicative model (φ · ν) explain more variance in flourishing outcomes than a purely additive model (phi + nu)?
2. Does the balance between phi and nu independently predict flourishing beyond total amount?
3. Do these relationships replicate across culturally diverse national samples?

---

## 4. Hypotheses

### H1 -- Multiplicative superiority
A model including the product term φ · ν will explain significantly more variance in Happiness and Life Satisfaction (the flourishing outcome) than a model with only the additive main effects phi + nu. Specifically, the change in R-squared (Delta-R-squared) from Model 1 to Model 2 will be positive and statistically significant at p < .005 in a majority of countries.

### H2 -- Balance effect
The balance between phi and nu, operationalized as the negative absolute difference -|phi - nu|, will independently predict flourishing beyond both main effects and their product. That is, holding phi, nu, and φ · ν constant, individuals whose coherence and viability are closer in magnitude will report higher flourishing.

### H3 -- Cross-national generalizability
The superiority of Model 2 (multiplicative) or Model 3 (balance) over Model 1 (additive) will hold in at least 15 of the 22 countries in the GFS dataset.

### Directional predictions
- The φ · ν interaction coefficient will be positive: coherence amplifies the flourishing benefit of viability, and vice versa.
- The balance coefficient (-|phi - nu|) will be positive: closer balance predicts higher flourishing.

---

## 5. Theoretical Background

### 5.1 The Emergentist framework

The Emergentism framework (Burri, 2024--2026) proposes that the fundamental unit of any viable system is the product P_node = Φ × V, where phi (coherence) represents internal integration, meaning, and structural integrity, and nu (viability) represents external capability, resources, and adaptive fitness. The framework predicts that P is conserved (P∞ = φ · ν = 1 on the Riemann sphere S-squared), such that flourishing is maximized not when either factor is maximized alone, but when both are present simultaneously. The balance B = sin(theta) peaks at the equator where phi = nu.

This generates a specific, falsifiable empirical prediction: the multiplicative combination of coherence-type and viability-type factors should predict human wellbeing better than their additive combination. The additive model implies independent contributions; the multiplicative model implies synergy -- that coherence without viability, or viability without coherence, yields diminished returns.

Evidence tier: [I] Interpretive. This preregistration is designed to move the claim toward [S] Structural or [E] Established.

### 5.2 Prior empirical support

**Sheldon and Niemiec (2006)** demonstrated that balanced satisfaction across basic psychological needs predicted wellbeing beyond total need satisfaction. Their finding that "people are happiest when they have some satisfaction of all needs rather than a lot of satisfaction of some needs and little of others" is structurally isomorphic to the Emergentist prediction.

**Ryff's six-factor model of psychological wellbeing** (Ryff, 1989; Ryff & Keyes, 1995) identifies dimensions that map onto the phi/nu distinction: Purpose in Life and Personal Growth (phi-like) vs. Environmental Mastery and Positive Relations (nu-like), with Self-Acceptance and Autonomy as boundary cases. No published analysis has tested multiplicative vs. additive models across these dimensions.

**The GFS** (VanderWeele et al., 2023) provides a uniquely suitable dataset: six domains of flourishing measured across 22 countries with N > 200,000, using validated items with established psychometric properties. The domain structure maps naturally onto the phi/nu distinction.

---

## 6. Dependent Variable

**Happiness and Life Satisfaction** (GFS Domain 1)

This domain serves as the flourishing outcome variable. It is measured by two items in the GFS:
- "Taking all things together, how happy would you say you are?" (0--10 scale)
- "Overall, how satisfied are you with life as a whole these days?" (0--10 scale)

The domain score is the mean of these two items (or the GFS-provided composite if one is released).

### Justification for DV choice
Happiness and Life Satisfaction is the most face-valid global outcome measure in the GFS. Using it as the DV while using the remaining five domains as predictors avoids the circularity of predicting a composite from its own components. It also provides the most direct test of the framework's central claim about human flourishing.

---

## 7. Independent Variables

### 7.1 phi (Coherence) composite

Constructed as the mean of two GFS domain scores:

1. **Meaning and Purpose** (GFS Domain 2)
   - "Overall, to what extent do you feel the things you do in your life are worthwhile?" (0--10)
   - "I understand my purpose in life." (0--10)

2. **Character and Virtue** (GFS Domain 3)
   - [D] Survey item: "I always act to promote good in all circumstances, even in difficult and challenging situations." (0--10)
   - [D] Survey item: "I am always able to give up some happiness now for greater happiness later." (0--10)

### Justification
Meaning/Purpose and Character/Virtue represent the internal, integrative, pattern-forming aspects of human functioning -- the coherence dimension. They capture whether a person's life hangs together as a meaningful whole and whether their character provides structural integrity.

### 7.2 nu (Viability) composite

Constructed as the mean of three GFS domain scores:

3. **Close Social Relationships** (GFS Domain 4)
   - "I am content with my friendships and relationships." (0--10)
   - "My relationships are as satisfying as I would want them to be." (0--10)

4. **Financial and Material Stability** (GFS Domain 5)
   - "How often do you worry about being able to meet normal monthly living expenses?" (reverse-scored, 0--10)
   - "How often is there not enough food to feed your family?" (reverse-scored, 0--10; exact wording may vary by country per GFS cultural adaptation protocol — we will use the GFS-provided domain score if available, which accounts for cross-cultural measurement equivalence)

5. **Physical and Mental Health** (GFS Domain 6)
   - "In general, how would you rate your overall health?" (0--10)
   - "Overall, how would you rate your mental health?" (0--10)

### Justification
Close Relationships, Financial Stability, and Physical/Mental Health represent the external, capability-based, resource-providing aspects of human functioning -- the viability dimension. They capture whether a person has the material, relational, and embodied resources to act in the world.

### 7.3 Derived variables

- **φ · ν** (interaction term): Product of standardized phi and nu composites
- **Balance**: -|phi - nu| computed on standardized scores; higher values indicate closer balance between coherence and viability

### 7.4 Standardization procedure

[D] Analysis plan: All domain scores will be z-standardized within each country sample before computing composites. phi and nu composites will then be z-standardized within each country before computing the interaction term and balance variable. This ensures the interaction term is interpretable and not confounded with scaling differences across countries.

---

## 8. Covariates

The following covariates will be included in all models:

- **Age** (continuous, centered at country mean)
- **Gender** (binary or categorical as provided by GFS)
- **Education level** (ordinal, as provided by GFS)
- **Religious affiliation** (categorical, as provided by GFS; reduced to major categories if cell sizes are small)

### Justification
These are standard demographic controls in cross-national wellbeing research. They are not the focus of the hypotheses but are included to rule out confounding. We do not include income as a covariate because it is partially captured by the Financial and Material Stability domain (part of nu).

---

## 9. Analysis Plan

### 9.1 Model specification

For each of the 22 countries, we will estimate three nested OLS regression models:

**Model 1 -- Additive:**
Flourishing = beta_0 + beta_1(phi) + beta_2(nu) + covariates + epsilon

**Model 2 -- Multiplicative:**
Flourishing = beta_0 + beta_1(phi) + beta_2(nu) + beta_3(φ · ν) + covariates + epsilon

**Model 3 -- Balance:**
Flourishing = beta_0 + beta_1(phi) + beta_2(nu) + beta_3(φ · ν) + beta_4(-|phi - nu|) + covariates + epsilon

### 9.2 Model comparison

For each country:
1. **Delta-R-squared** from Model 1 to Model 2 (tests H1)
2. **Delta-R-squared** from Model 2 to Model 3 (tests H2)
3. **AIC and BIC** for all three models (tests relative fit with parsimony penalty)
4. **F-test** for nested model comparison (Model 1 vs. 2; Model 2 vs. 3)

### 9.3 Meta-analytic summary

Across all 22 countries:
- Count of countries where Model 2 beats Model 1 (by Delta-R-squared with p < .005 on the F-test)
- Count of countries where Model 3 beats Model 2
- Random-effects meta-analysis of the φ · ν interaction coefficient (beta_3) across countries
- Random-effects meta-analysis of the balance coefficient (beta_4) across countries
- Forest plots for both meta-analyses

### 9.4 Significance threshold

Following Benjamin et al. (2018), "Redefine Statistical Significance," we adopt **p < .005** as the threshold for claiming statistical significance. Results between .005 and .05 will be reported as "suggestive evidence."

This is particularly important given the large sample sizes in the GFS (N approximately 10,000 per country), where trivially small effects can achieve conventional significance.

### 9.5 Effect size benchmarks

We will interpret Delta-R-squared using the following benchmarks, appropriate for incremental validity in large-sample psychology:
- Delta-R-squared >= .02: small but meaningful
- Delta-R-squared >= .05: moderate
- Delta-R-squared >= .10: large

### 9.6 Survey weights

If the GFS public-use files include survey weights (design weights, post-stratification weights, or both), all primary analyses will be conducted using weighted regression. Specifically:

- **Primary analysis:** Weighted OLS using GFS-provided survey weights (if available)
- **Sensitivity check:** Unweighted OLS to assess whether weighting materially affects the interaction coefficient
- **If no weights are provided:** Unweighted OLS will serve as the primary analysis, noted as a limitation

Standard errors will be computed using heteroscedasticity-consistent (HC1) estimators in all models to account for potential heteroscedasticity introduced by weighting.

### 9.7 Robustness checks

1. **Non-linear main effects:** Add phi-squared and nu-squared to Model 1 to ensure the interaction is not an artifact of unmodeled curvilinearity.
2. **Alternative phi/nu splits:** Test sensitivity to domain assignment by swapping Close Social Relationships from nu to phi (since social belonging has coherence properties).
3. **Weighted vs. unweighted composites:** Compare equal-weighted phi and nu composites with PCA-derived factor score weights.
4. **Multilevel model:** Pool all countries in a single multilevel model with random slopes for the interaction term.
5. **Ordinal outcomes:** Re-run with ordinal logistic regression given the 0--10 bounded scales.
6. **Three-factor phi/nu split:** Test a 3-phi/3-nu split (Meaning+Character+Relationships vs. Financial+Health+Relationships) against the 2/3 split to assess sensitivity to the social domain assignment.

---

## 10. Success Criteria and Falsification Conditions

### 10.1 What would confirm H1
Model 2 (multiplicative) shows a statistically significant positive Delta-R-squared over Model 1 (additive) at p < .005 in **15 or more** of 22 countries. The meta-analytic estimate of beta_3 (φ · ν) is positive and its 95% CI excludes zero.

### 10.2 What would confirm H2
Model 3 (balance) shows a statistically significant positive Delta-R-squared over Model 2 at p < .005 in **11 or more** of 22 countries (simple majority). The meta-analytic estimate of beta_4 (-|phi - nu|) is positive and its 95% CI excludes zero.

### 10.3 What would confirm H3
Confirmation of H1 or H2 in at least 15 of 22 countries, including at least one country from each of the following cultural clusters represented in the GFS: East Asian, South Asian, Sub-Saharan African, Latin American, Western European, Eastern European/Central Asian, and Middle Eastern/North African.

### 10.4 What would FALSIFY the framework

**Strong falsification:** If Model 1 (additive) outperforms Model 2 (multiplicative) in **15 or more** of 22 countries -- that is, if the φ · ν interaction term is zero or negative in a supermajority of national samples -- then the multiplicative structure of P_node = Φ × V is not supported empirically. The multiplicative prediction remains at evidence tier [I] Interpretive and cannot be upgraded to [S] Structural or [E] Established.

**Moderate falsification:** If Model 2 beats Model 1 in fewer than 15 but more than 11 countries, the result is ambiguous. The multiplicative prediction would have weak or culture-specific support, and the framework would need to specify boundary conditions.

**Directional falsification:** If the interaction coefficient beta_3 is consistently *negative* (meaning coherence and viability substitute for rather than amplify each other), this would directly contradict the framework's central prediction.

We commit to reporting all results regardless of direction and to publishing the analysis code and output alongside the manuscript.

---

## 11. Data Source

### 11.1 Primary dataset

**Global Flourishing Study (GFS), Wave 1**
- PI: Tyler VanderWeele (Harvard University)
- Expected public release: April 8, 2026
- Approximately 200,000 respondents across 22 countries
- Countries: Argentina, Australia, Brazil, Egypt, Germany, Hong Kong, India, Indonesia, Israel, Japan, Kenya, Mexico, Nigeria, the Philippines, Poland, South Africa, Spain, Sweden, Tanzania, Turkey, the United Kingdom, and the United States
- Data access: Public use files via the GFS data repository

We have not accessed the GFS data at the time of this preregistration. All hypotheses, operationalizations, and analysis plans were specified before data availability.

### 11.2 Proof-of-concept dataset

**Midlife in the United States (MIDUS)**
- Waves 1--3, available via ICPSR (Study 2760, 4652, 36346)
- Ryff's six psychological wellbeing dimensions can be mapped to phi/nu
- phi (coherence): Purpose in Life + Personal Growth
- nu (viability): Environmental Mastery + Positive Relations with Others
- DV: Life Satisfaction (Diener SWLS or single-item)
- This analysis is explicitly labeled as proof-of-concept and hypothesis-generating; only the GFS analysis constitutes the confirmatory test

---

## 12. Existing Data

**Declaration:** At the time of writing this preregistration (April 4, 2026), the GFS Wave 1 public-use data has NOT been released. We have not accessed, viewed, or analyzed any GFS individual-level data. The public release is scheduled for April 8, 2026.

We have read published descriptions of the GFS methodology and item content (VanderWeele et al., 2023; Lomas et al., 2023) to plan our variable operationalization. This is consistent with COS guidelines for preregistration of secondary analyses.

The MIDUS data is publicly available and we may have begun proof-of-concept analyses on it prior to this preregistration. MIDUS results will be reported separately and clearly labeled as exploratory.

---

## 13. Sample Size and Statistical Power

### 13.1 Per-country sample size
The GFS includes approximately N = 10,000 respondents per country. With country-specific N of this magnitude, we have > 99% power to detect even small interaction effects (Delta-R-squared = .005) at our p < .005 threshold. Statistical power is not a concern for individual country tests.

### 13.2 Cross-national test
With 22 countries, the probability of observing 15+ successes out of 22 under the null hypothesis (50% base rate, no true interaction) is approximately p = .017 by a binomial test. Under a true positive rate of 80%, the probability of observing 15+ successes is approximately .95. Our cross-national criterion has adequate power.

### 13.3 Exclusion criteria and missing data
Respondents will be excluded if:
- They have missing data on any of the six GFS domain scores used in the analysis (complete-case analysis)
- Country samples with N < 500 after exclusions (we do not anticipate this)

No other exclusions will be applied.

**Sensitivity analysis for missing data:** If complete-case exclusion drops more than 10% of any country sample, we will additionally run analyses using multiple imputation (m = 20 datasets, predictive mean matching) as a robustness check and report both sets of results.

---

## 14. Timeline

| Date | Milestone |
|------|-----------|
| April 4--7, 2026 | Submit this preregistration to COS GFS Secondary Analysis Registry |
| April 8, 2026 | GFS Wave 1 public data release |
| April 8--14, 2026 | Download data; run all preregistered analyses |
| April 15--30, 2026 | Write manuscript; produce figures and tables |
| May 1--15, 2026 | Internal review; circulate to co-authors |
| May 15--31, 2026 | Submit to PNAS (primary target) or Nature Human Behaviour |
| June--August, 2026 | Peer review |

---

## 15. Analysis Code

All analysis code will be written in R (version 4.3+) using the following packages:
- `lm()` for OLS regression
- `lmtest` and `car` for model comparison (F-tests, Wald tests)
- `AICcmodavg` for AIC/BIC comparison
- `metafor` for random-effects meta-analysis
- `ggplot2` for forest plots and visualizations
- `lavaan` for confirmatory factor analysis of phi/nu composites (robustness check)

The complete analysis script will be deposited on OSF alongside this preregistration prior to data access.

---

## 16. Other

### 16.1 Ethical considerations
This study involves secondary analysis of de-identified public-use data. No IRB approval is required. We will comply with all GFS data use agreements.

### 16.2 Conflicts of interest
YRB is the originator of the Emergentism framework being tested. This preregistration is specifically designed to mitigate confirmation bias: the hypotheses are stated in advance, the analysis plan is fixed, the falsification criteria are explicit, and the significance threshold is conservative. We welcome independent replication.

### 16.3 Relationship to the broader Emergentism framework
[I] This test addresses one specific empirical prediction of the framework: that human flourishing is multiplicatively structured (φ · ν rather than phi + nu). Confirmation would support but not prove the broader framework. Falsification would disconfirm a core empirical prediction without necessarily invalidating the mathematical or philosophical components, which stand on independent grounds.

Evidence tier for the multiplicative prediction: Currently [I] Interpretive. If confirmed by GFS analysis, upgradeable to [S] Structural. Would require independent replication on non-GFS data to reach [E] Established.

### 16.4 Commitment to transparency
- This preregistration will be made public on OSF regardless of results.
- The analysis code will be deposited on OSF before data access.
- All results will be reported, including null and negative findings.
- Deviations from the preregistered plan (if any) will be explicitly documented and justified.

---

## References

Benjamin, D. J., Berger, J. O., Johannesson, M., et al. (2018). Redefine statistical significance. *Nature Human Behaviour*, 2(1), 6--10.

Lomas, T., Case, B., Cratty, F., & VanderWeele, T. J. (2023). A global approach to well-being: Unpacking the Global Flourishing Study. In *Measuring Well-Being* (pp. 295--322). Oxford University Press.

Ryff, C. D. (1989). Happiness is everything, or is it? Explorations on the meaning of psychological well-being. *Journal of Personality and Social Psychology*, 57(6), 1069--1081.

Ryff, C. D., & Keyes, C. L. M. (1995). The structure of psychological well-being revisited. *Journal of Personality and Social Psychology*, 69(4), 719--727.

Sheldon, K. M., & Niemiec, C. P. (2006). It's not just the amount that counts: Balanced need satisfaction also affects well-being. *Journal of Personality and Social Psychology*, 91(2), 331--341.

VanderWeele, T. J., Trudel-Fitzgerald, C., Allin, P., et al. (2023). Current research on well-being: A short report on the Global Flourishing Study. *International Journal of Wellbeing*, 13(1), 1--17.

---

*Preregistered: April 4, 2026. All hypotheses, operationalizations, and analysis plans specified before access to GFS Wave 1 data.*

*Evidence tier for this prediction: [I] Interpretive, pending empirical test.*

*A-Brahmanism reminder: This framework is an instrument, not a destination. If you can access flourishing directly -- through practice, through presence, through quiet sitting -- you do not need this test. Put it down.*
