# Citation Verification Ledger

**Verified 2026-06-10 via live web search.** Every load-bearing reference in the R1–R5 drafts was drafted from model memory; this ledger records which have been confirmed against primary/authoritative sources and at what tier. **Status key:** ✅ confirmed (venue + year + pages match as drafted); ⚠️ confirmed-with-calibration (exists, but tier/scope needs adjustment in-text); ⛔ not found / fabricated (none so far). Unverified items remain flagged in their papers.

## Confirmed

| Cite | Paper | Verified detail | Status |
|---|---|---|---|
| Lawvere, F.W. (1969), *Diagonal arguments and cartesian closed categories* | R1 | Springer LNM **92**, pp. 134–145 (Category Theory, Homology Theory and their Applications II). Standard sources (Wikipedia, nLab, arXiv survey 2503.13536) confirm the theorem generalizes Cantor, Russell, Gödel-I, **Turing/Entscheidungsproblem**, Tarski. | ✅ — and independently validates this session's R1 edit adding Turing to the family |
| Yanofsky, N.S. (2003), *A universal approach to self-referential paradoxes…* | R1 | *Bulletin of Symbolic Logic* **9(3): 362–386**. arXiv math/0305282. Abstract explicitly covers computability, complexity, formal-language theory. | ✅ (page range exact) |
| Turing, A.M. (1936), *On computable numbers…* | R1 | *Proc. London Math. Soc.* s2-42: 230–265. (Standard; halting/Entscheidungsproblem is canonically in the Lawvere family per the survey above.) | ✅ |
| Buckingham, E. (1914), *On physically similar systems* | R1, R5 | *Physical Review* **4(4): 345–376**, Oct 1914. | ✅ (exact) |
| Balboni, Bandiera, Burgess, Ghatak & Heil (2022), *Why Do People Stay Poor?* | R3 | *Quarterly Journal of Economics* **137(2): 785+**. NBER w29340. 11-yr panel, ~6,000 households, randomized cow-asset transfer, asset-threshold poverty-trap mechanism. | ✅ |
| Kraay & McKenzie (2014), *Do Poverty Traps Exist? Assessing the Evidence* | R3 | *Journal of Economic Perspectives* **28(3): 127–148**. Finds **no strong evidence** for many theorized trap mechanisms. | ✅ — correctly the skeptical counterweight; R3 must present the trap parallel as contested |
| Sharma, M., et al. (2023), *Towards Understanding Sycophancy in Language Models* | R2 | arXiv **2310.13548**; Anthropic (Sharma also Oxford); 5 assistants show sycophancy; humans + PMs prefer sycophantic over correct a non-negligible fraction. | ✅ |
| Anderson, N.H. (1981), *Foundations of Information Integration Theory* | R4 | Academic Press, New York. Cognitive algebra incl. averaging **and** multiplying models. | ✅ — note the live averaging-vs-multiplying debate (ResearchGate "Two problems in cognitive algebra"); R4 should engage it |
| Krantz, Luce, Suppes & Tversky (1971), *Foundations of Measurement, Vol. I* | R4 | Academic Press; subtitle **Additive and Polynomial Representations**; 577pp; polynomial conjoint measurement chapter (covers multiplicative representations). | ✅ |
| Wissner-Gross & Freer (2013), *Causal Entropic Forces* | R6 candidate / teleology | *Physical Review Letters* **110: 168702**. "Tool use and social cooperation spontaneously emerge"; maximize accessible future paths. | ⚠️ exists exactly — but a published **Comment** disputes it (arXiv 1308.4375); cite the dispute |
| Klyubin, Polani & Nehaniv (2005), *Empowerment: a universal agent-centric measure of control* | R6 candidate / teleology | *Proc. IEEE CEC 2005*, vol. 1, pp. 128–135. **Full PDF read 2026-06-10.** `E_t = C(p(s_{t+n}|a^n_t))` = channel capacity, action-sequence → future sensor state, in bits. Definitionally single-agent/first-person ("does not matter what other agents perceive… no god's-eye-view"); **no multi-agent/cooperation content** — so the corpus's "expand others' light cones" is a real extension (cite *coupled/social empowerment*, Salge–Polani 2014 / Guckelsberger–Salge — TO VERIFY). | ✅ + grounded |

## Calibrations required (exists, but adjust the in-text claim)

- **Suda, Minoru (2025), "Fractional Structure and Möbius Transformation — Part I: Double Inversion in Division and the Phase of Twist."** ⚠️ **REAL** — on PhilArchive (added Aug 2025), author profile on PhilPapers/PhilPeople. Proposes the **"critical-one hypothesis"**: the effective singular locus of reciprocal symmetry is x = 1, not 0 — a genuine independent arrival at the corpus's central claim. **But:** (i) it is a **self-archived philosophy preprint, not peer-reviewed**; (ii) web search surfaced Part I directly; the corpus's `FINITY_PAPERS/_SOURCES/` holds the full set of Suda PDFs with SHA-256, and the "trilogy" correctly denotes *Fractional Structure* I/II/III (PAPER_VII refs list all three plus two further works) — so the trilogy count stands; my initial "Part I only" concern is **withdrawn** on inspection of the local sources. **Action:** wherever the corpus cites Suda as corroboration, mark it [preprint, not peer-reviewed] and downgrade the *evidential* tier from `[A]` to `[I]` (independent rediscovery is heuristic support, not established fact). Applied to PAPER_VII §Consequences-4 on 2026-06-10. This is the single most important calibration on the board — the corroboration is real and valuable, and overstating its evidential weight is exactly the kind of tier-inflation the program exists to prevent.

- **Causal entropic forces** carries a published rebuttal — present it as a provocative, contested proposal, not settled physics.

## Prior art discovered (must cite and distinguish — relevant to the R6 / proto-dimensions thread)

- **"Computational Irreducibility as the Foundation of Agency"** (arXiv **2505.04646**, 2025). Connects Wolfram's computational irreducibility and Gödel/Turing undecidability to autonomous agency; engages empowerment, IIT, autopoiesis (Moreno, Froese, Barandiaran). **Crucially, it treats irreducibility as the generative process of agency and does NOT cleanly separate non-computability-as-boundary from irreducibility-as-process.** The corpus's Titan/God distinction (non-computability = pole/limit; irreducibility = the operand-side approach to it) is a *sharper* position — a genuine differentiating move — but this paper is prior art on the same terrain and must be cited and distinguished in any proto-dimensions write-up.

## Still unverified (flagged in-paper; verify before submission)

- Löb (1955), *JSL* 20(2): 115–118; von Neumann (1925) set-theory axiomatization; Tarski (1933/1935); Carlström (2004) wheels/division-by-zero [R1].
- Pigou (1912) *Wealth and Welfare*; Dalton (1920) *Economic Journal* 30; Atkinson (1970) *JET* 2; Marshall & Olkin majorization; Bandiera et al. (2017) [R3].
- Perez et al. (2022) arXiv 2212.09251; Bai et al. (2022) Constitutional AI 2212.08073; 2024–2026 sycophancy follow-ups [R2].
- Euclid *Elements* VII Defs (Heath); Aristotle *Metaphysics* Iota; Stevin *L'Arithmétique* (1585) — the unit-is-number locus; Klein (1968); BIPM *SI Brochure* 9th ed. (2019) [R5].

## Tally so far

11 load-bearing references checked → **11 exist, 0 fabricated**, every venue/year/page correct as drafted from memory. Calibrations: 2 (Suda tier + trilogy count; causal-entropic dispute). Prior art to engage: 1 (arXiv 2505.04646). The corpus's memory-drafted bibliography is, on this sample, accurate — which is itself worth noting: the over-claim risk in this program was never fabricated citations, it was tier-inflation of real ones (the Suda case exactly).
