# Corpus checklist findings — 30_TRIAL/corpus (reviewed 2026-09-05)

All nine checklist items were applied to every document. Only items that flag a
problem are listed per document. Line numbers refer to the corpus files in
`30_TRIAL/corpus/`. Verification notes (what was checked and passed) are at the
end.

Severity markers: **[BLOCKER]** broken/corrupted or self-contradicting claim;
**[MAJOR]** claim fails its own checklist item; **[MINOR]** weak or cosmetic.

---

## C1_pattern_to_claim.md

- ITEM 1: LINE 126 — **[MAJOR]** figure "Over 300 prior patterns confirm this gate mechanism" has no producing source or command. Repo-wide search finds this count nowhere except this sentence. It also sits in Gate 6's FAIL cell as an *example* of an unfalsifiable claim but is written as an assertion, so the reader cannot tell whether 300 is data or illustration.
- ITEM 1: LINE 169 — **[MINOR]** "The Rosetta Stone's 15 columns" — count asserted bare; no source in-document (depends_on points at the Master Rosetta, but the count is not derived and the corpus's own "counts are selected, not derived" fence is not carried here).
- ITEM 2: LINES 194–203 — **[MAJOR]** the Witness Reliability Matrix attaches no citation or calibration record to any High/Low/Medium rating, while the matrix's own row 1 definition (line 190) says reliability requires that "the calibration record exists." No such record is referenced for any row.
- ITEM 3: LINES 199, 201 — **[MINOR]** L1 Caṇḍāla and L3 Vaiśya are rated "Reliable? Yes" unconditionally; the three witness conditions (lines 188–192) are conditional (calibration record, disclosed incentives, auditable explanation) and the document never shows they are satisfied for L1/L3. Humans get "Conditional on…"; the caste rows get flat "Yes."
- ITEM 4: LINE 126 — **[MAJOR]** the "300 prior patterns" figure is undated (and cannot be current — it has no source at all). No other measurements exist in the document.
- ITEM 5: LINE 76 vs LINE 177 — **[MAJOR]** Gate 2 is defined inconsistently: §2 has L2 itself verifying an echo in ≥1 other column; §4 says the echo "must be in a column NOT chosen by the pattern-finder" and "L3 selects the confirming column, not L2." Gate operator (L2 vs L3) and selection rule differ between sections.
- ITEM 5: LINE 178 — **[MINOR]** level/column conflation: "A pattern at L2 (data science) must be confirmed by a column at L2, not by a column at L5" — columns are not "at" L-levels; line 76 states the relation correctly ("at the same L-level" across columns).
- ITEM 5: LINE 14 vs LINES 57–130 — **[MINOR]** frontmatter says the six-gate mechanism is "[I]", but §2 labels gates 1, 2, 4, 6 individually "[S]". The mechanism's declared tier disagrees with four of its six parts without reconciliation.
- ITEM 5: LINES 219–227 — **[MINOR]** the §6 ladder maps pramāṇas at L7, L5, L4, L3, L2, L1 and silently skips L6, in a table formatted as a complete per-level map.
- ITEM 5: LINES 235–239 — **[MINOR]** heading "Zero-Sum Resolution Equation" contains no equation (three lines of verse), and "zero-sum" is a term defined nowhere in the document or corpus.
- ITEM 6: LINE 126 — **[MAJOR]** the document defines unfalsifiability as disqualifying (Gate 6), yet its own Gate 6 fail-example ("Over 300 prior patterns confirm this gate mechanism — it is unfalsifiable") is itself an unfalsifiable claim inside this document. More generally, no claim in the document (e.g., the §5 reliability ratings) carries any kill criterion, though Gate 6 requires one of every candidate claim.
- ITEM 7: LINE 146 — **[MINOR]** Gate 3 retry policy "may retry once" — the limit "once" is a bare number with no rationale; everything else in the proposal does add gate machinery the L2→L3 handoff lacked.
- ITEM 8: LINE 90 — **[MAJOR]** "Confirmation bias is the dominant L2 pathology" — empirical-sounding superlative, tierless and sourceless.
- ITEM 8: LINE 126 — **[MAJOR]** "Over 300 prior patterns confirm…" — tierless.
- ITEM 8: LINES 196–203 — **[MINOR]** all witness reliability ratings (High/Medium/Low/Yes) are tierless measurements.
- ITEM 8: LINE 65 — **[MINOR]** "Untraceable patterns are projection, not perception" — tierless assertion.
- ITEM 9: LINE 126 — **[MAJOR]** "300 prior patterns" is an aggregate count with no enumerated parts anywhere in the document or repo.
- ITEM 9: LINE 169 — **[MINOR]** "15 columns" — not derived or enumerated in-document.

## C2_extraction_law.md

- ITEM 2: LINES 10, 194–200 — **[MAJOR]** the predecessor document is cited twice ("overclaiming predecessor archived 2026-07-20"; "preserved in the boundary archive") with no path, blob, or receipt. The Kintsugi "Crack" claims about what the predecessor's "own scholium admitted" (lines 195–197) are unverifiable. Contrast C3, which supplies a recoverable git blob for its predecessor.
- ITEM 3: LINE 95 — **[MAJOR]** "Eventual collapse follows only if these conditions persist long enough to cross a separately declared viability threshold" — the viability threshold governing the headline "collapse" outcome is "separately declared" but is declared nowhere in the document and no pointer to a declaring document is given. The condition is named, not stated.
- ITEM 5: LINES 57–58 vs 63–66 — **[MAJOR]** prose defines extraction as the "unauthorized, concealed, or structurally decoupled subclass" (three disjuncts); the formula has only two (¬AuthorizedCost ∨ Decoupled). "Concealed" never appears in the formal definition.
- ITEM 5: LINES 23, 26, 143 vs Definition section — **[MAJOR]** `η_move` is used as a defined quantity ("η_move = 0 names the action fence"; "not automatically relational η_move > 0") but is never defined; the document defines the predicate `Extractive(a;p,b)` instead and never connects it to `η_move`.
- ITEM 5: LINES 102–104 — **[MAJOR]** "The generic constraint rule still holds: support(K_X^C) ⊆ support(K_X)" — `K_X`, `K_X^C`, and `support(·)` are undefined in the document with no citation; the rule is uninterpretable as written.
- ITEM 5: LINE 155 — **[MINOR]** "never strict syntropy" — syntropy is defined only in C6 §6, not here; the cross-document dependency is unstated.
- ITEM 6: LINES 177–179 — **[MINOR]** Kill 1 cannot fire through observation: the conclusion S(t₁)≤S(t₀)−ε(t₁−t₀) follows mathematically from premises 1–3, so a "counterexample satisfying all three premises" can exist only if the derivation itself is botched. As written the criterion restates "the theorem is false" and provides no operational test. (Kills 2–6 are operable.)
- ITEM 8: LINES 40–41 — **[MINOR]** "Predators, parasites, monopolies, and one-shot defectors can benefit" — empirical claim, no tier, in the document's own "one line" summary.
- ITEM 8: LINES 136–156 — **[MINOR]** "Trophic flow, predation, sacrifice, and immune response" is the only major section with no tier label on header or bullets; every neighboring section carries [S]/[I]/[C].
- ITEM 8: LINES 194–197 — **[MINOR]** Kintsugi "Crack" makes historical claims about the predecessor's content with no tier and no citation.

## C3_balance_optimum.md

- ITEM 3: LINE 114 — **[BLOCKER]** "All systems implicitly satisfy these premises because the framework declares them." This contradicts the document's entire transfer contract: §4's six declarations are preconditions to be established by measurement; kill 2 says "Failure to measure the budget or factor costs kills the empirical transfer"; and §3's table exists precisely because real systems may fail the premises. As written, the conditional optimum is made unconditional. Reads like an editing corruption or an inserted sentence.
- ITEM 5: LINES 63–75 — **[MAJOR]** the budget variables (Φ_c, V_c) are never tied to the node variables (Φ̂₄, V₄); §2 applies the budget inequality directly to Φ̂₄V₄ (line 71) without declaring Φ_c=Φ̂₄, V_c=V₄. The "c=1" normalization (line 79) bridges only implicitly.
- ITEM 5: LINES 55, 71 — **[MINOR]** the operator notation `C×(Φ̂₄,V₄)` is undefined at first use.
- ITEM 5: LINES 79–80 — **[MAJOR]** "the selected structural-zero product returns P×=0" calls the product candidate "the selected" score, but lines 74–75 define the selected score as P_node=min(Φ̂₄,V₄), and line 55 says the product is "retired" (C4 §5 and C5 §5 confirm the product is not selected). Conflates the retired aggregator with the selected one.
- ITEM 6: LINES 121–122 — **[MINOR]** Kill 1 is near-vacuous: with Φ̂₄,V₄∈[0,1] (nonnegative), AM–GM mathematically forces the maximum to be c²/4 at the symmetric point, so the criterion can fire only if the arithmetic is wrong. It is a restatement, not an operational test. (Kills 2–4 are operable.)
- ITEM 8: LINE 114 — **[MAJOR]** the "all systems implicitly satisfy" sentence is also a tierless universal claim in a document otherwise disciplined about tiers.

## C4_weltanschauung.md

- ITEM 1: LINE 79 — **[MAJOR]** "15 W rows contact-routed, 2 terminal" — the document enumerates W0–W12 (13 wager forms; its own Provenance list names exactly 13). 15 is not derivable from the document's parts. (External reconciliation exists — `00_ESTABLISHED/README.md` splits 19 rows into 15 W + 4 RQ — but a C4 reader cannot produce it.)
- ITEM 1: LINE 36 — **[MAJOR]** "the seven kernel owners retain semantic authority" — the seven are never enumerated; §2's table lists ~12 pieces and no seven-subset is identified. The count is not derivable from the document.
- ITEM 2: LINE 537 — **[BLOCKER]** "The measurement problem is solved by §7.2's decoherence filter." Contradicts the ontology owner (C5 §3.2/§3.4), which states decoherence "does not, alone, deliver definite outcomes" and brands "Emergentism solves the measurement problem" as a FORBIDDEN dead form. §7.2 itself claims only record-emergence help, so the internal citation does not support "solved" either.
- ITEM 2: LINES 112, 408 — **[MINOR]** Soros's reflexivity, and the Spinoza/Hegel/Tegmark lineage, are name-attachments with no citations; the claims they support inherit no verifiable source.
- ITEM 4: LINE 12 vs LINES 41, 84, 147–149 — **[MAJOR]** frontmatter date 2026-07-22 is stale: the body contains "Routed 2026-08-06" and cites `06_ONTOLOGY/14_THE_TEN_EMERGENTIST_ANSWERS_2026_08_24.md` — a file dated a month after the document's own date — while §3B speaks in the present tense ("Emergentism now gives…"). The document's declared currency contradicts its own content.
- ITEM 4: LINE 620 — **[MINOR]** PQA-54 state "54 selected · 0 evaluated · 0 independently reviewed · 0 resolved" is a status measurement with no date; cannot be checked as current.
- ITEM 5: LINES 507 vs 594 — **[MAJOR]** duplicate section numbering: "## 8 · What remains open to the world" and "## 8 · The reciprocal bridge and the Question Atlas". The second §8 appears after the Provenance section and the document's closing italic line (537) — a merge artifact; every cross-reference to "§8" is now ambiguous.
- ITEM 6: LINE 577 — **[MINOR]** "A claim that does no work is decoration" — "does no work" has no test, metric, or detector; fires only by editorial judgment.
- ITEM 8: LINE 537 — **[BLOCKER]** the "measurement problem is solved" closing line is tierless — an unpayable strong claim, flagged for contradiction under item 2 above.
- ITEM 8: LINE 586 — **[MAJOR]** "Authorization, authorship, evidence, and truth are the same type at D4. The D-ladder proves this." — tierless; "proves" violates the document's own standing rule (line 98: a formal conjecture reaches [A] only by proof; none is attached); it also sits inside the "kill criteria" block, where it is not a kill criterion.

## C5_dof_ontology.md

- ITEM 1: LINE 11 — **[MINOR]** "workflow wf_0b2a7fda-986 (14 agents…)" — the count 14 has a provenance pointer but no command or artifact that reproduces it.
- ITEM 2: LINES 316–322 — **[MAJOR]** §3.1 physics claims are labeled "[A/B]-anchored" but no anchor is named: no citations for the decoherence/einselection/consistent-histories claims, and the double-slit claim "every detector position … is a perfectly consistent history" (line 320) carries no source. The tier label promises anchors that are absent.
- ITEM 5: LINE 8 vs LINES 344–348 — **[MAJOR]** frontmatter register says this ontology is "never [A]", yet §5 labels load-bearers "stand alone [A]/[S]" and marks the chart identity and the inversion fixed point explicitly "[A]". Direct internal contradiction on the admissible tier ceiling.
- ITEM 5: LINE 261 — **[MINOR]** "Fewer admitted configurations are nomologically possible, dynamically reachable, actual, stable, emergent, or livedly available." — broken negation scope; presumably "No admitted configuration is thereby…". As written it can read as a quantitative claim ("few of them are possible").
- ITEM 5: LINE 349 — **[MAJOR]** "the four Möbius classes" — the classes are never defined (no generator set, no action, no enumeration); the term is uninterpretable from the document.
- ITEM 5: LINE 216 vs C4 §7.1 — **[MINOR]** C4 defines three typed Finity variants (Finity_G, Finity_F, Finity_L); C5 defines Finity untyped. The finer partition is neither reflected nor excluded here.
- ITEM 4: LINES 314–316 — **[MINOR]** the §3 measurement correspondence is "quarantined here" with no date for the quarantine (frontmatter carries 2026-07-19/20 only).
- ITEM 8: LINE 234 — **[MINOR]** "Even the adversarial pass granted this reframe" — tierless corpus-fact claim about an audit outcome, with no pointer to the adversarial-pass record.
- ITEM 8: LINE 300 — **[MINOR]** the incompressibility fence is a mathematical caution with no tier, in an otherwise fully tiered document.
- ITEM 9: LINE 349 — **[MINOR]** "the four Möbius classes" — a count with no parts given (same flag as item 5).

## C6_the_goal.md

- ITEM 1: LINE 83 — **[BLOCKER]** "all agents that adopt it show improved coordination" — a universal measurement claim with no source, command, dataset, custody, or date anywhere in the document or corpus. Nothing produces it.
- ITEM 2: LINE 83 — **[BLOCKER]** "…which the φν=1 identity predicts" — the cited identity does not support the claim: φν=1 is a chart identity, and C3 kill 4 rules "Any inference from φν=1 to … ethics is a type failure and must be withdrawn." The attachment also contradicts the same paragraph's own line 82 ("The framework cannot derive this orientation from geometry") and the document's opening (line 29: "not a consequence of φν=1").
- ITEM 3: LINES 83–84 — **[BLOCKER]** textually corrupted conditional: "…which the φν=1 identity predicts. or compel an outsider to adopt it." The trailing fragment "or compel an outsider to adopt it" has no main clause; the original sentence (evidently "The framework cannot … impose it …, or compel an outsider to adopt it") has lost its subject and condition. The paragraph is not parseable as written.
- ITEM 4: LINES 13, 83 — **[MAJOR]** the "always produces better outcomes" (frontmatter) and "all agents … show improved coordination" (line 83) claims are undated and unmeasured; no test, window, or population.
- ITEM 5: LINE 13 vs LINES 142–143, 265 — **[MAJOR]** frontmatter evidence_tier asserts "always produces better outcomes than rival orientations [B]", while body §4A and §10 both state the adequacy "remains [C]". The document's own tier for its central adequacy claim is inconsistent between frontmatter and body.
- ITEM 6: LINES 259–263 — **[MINOR]** two change-criteria are unoperationalized: "long-horizon language repeatedly protects unfalsifiable promises" (no count for "repeatedly") and "the vocabulary becomes necessary for receiving ordinary human dignity" (no detector, threshold, or test — nothing specifies how this could be observed to fire).
- ITEM 7: LINES 138–143 — **[MINOR]** the §4A two-clock "coordination bridge" is honestly held at [C], but its delta over existing receding-horizon / model-predictive-control practice is never stated — what it adds beyond the standard pattern is not argued.
- ITEM 8: LINE 13 — **[BLOCKER]** frontmatter claims tier [B] (custodied observation) for an "always … better than rival orientations" universal — an unpayable tier: no custody, no test, and it contradicts the body's own [C] (see item 5). This is exactly the lazy-tier/overclaim pattern the corpus's discipline forbids.
- ITEM 8: LINE 83 — **[MAJOR]** "which the φν=1 identity predicts" — tierless, and a category error per C3 kill 4.
- ITEM 9: LINES 174–178 — **[MAJOR]** the definitions quantify over ΔᵀW_H — a whole-level welfare delta — but the aggregation from member bearers to W_H is never defined. The corpus elsewhere refuses aggregate primitives (C5 §4: "an aggregate ΣΔP is not restored as the moral primitive"; C2: "No scalar sum across incommensurable bearers is licensed"), so whether W_H is a sum, a vector minimum, or something else matters and is unstated. Contribution/Support/Syntropic verdicts are not derivable from per-bearer parts as written.

---

## Verification performed (claims that PASSED)

- Internal file references resolve: all depends_on paths in C1–C3, C4's architecture table, C5's see_also, and C6's parents were checked against `01_EMERGENTISM/` — all exist (including `F5Fork.v1.json`, `EmergentistAnswerSet.v1.json`, and the 105–133 audit ledgers under `11_UPLINK/50_AUDITS_AND_EXECUTIONS/`).
- C3's predecessor blob `4548607a4ea9a236a0a36e87119991f3fb38ff66` exists (`git cat-file -t` → blob).
- C1's dependency files (`02_EPISTEMOLOGY/01_EVIDENCE_TIERS/00_THE_HONEST_POSITION.md`, `00_PRATYAKSA_AS_PRIMARY_DISCLOSURE.md`) exist.
- Chart arithmetic spot-checked and correct: φν=cot(θ/2)tan(θ/2)=1; 2/(φ+ν)=sinθ; H=φ+ν≥2 with equator minimum; 1 as unique inversion fixed point on ℝ₊; AM–GM and Cobb–Douglas optima in C3; ℚ⁺ reachability from {1, S, ι} (continued-fraction construction) in C5.
- C6's five refusals (§4) match its named parent `00_META/00_THE_FIVE_PLUS_ONE_CONSTITUTION.md` exactly — not a flag, despite differing from the workspace-level OUT-fence set, which is a different layer.
- Gītā and SEP citations in C5 point at verses/passage types that support the attached claims (11.13 vision, 2.47 action/fruit, 11.32 Time, 11.45 overwhelm; kenshō gloss; Advaita liberation).
- Shared-score consistency across C3/C4/C5/C6 (P_node=min(Φ̂₄,V₄); product ΦV retired) holds in all four documents.
- C4's audit counts (7 SETTLED + 66 BROKEN + 34 SYNTHETIC-GAP; 11/12 LEAKING) carry cited sources (docs 126, 132, 131).
