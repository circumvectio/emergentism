# MID-02 run log

- 2026-09-06: frozen state committed `33609ab8` (corpus, briefs, task, sealed key, analyzer).
- Sealed key sha256: `31da83fb47ec02fa41d6c18a8d5a4f3e0ac22daa55c58fb080fb78d5ed103642`
- Analyzer sha256: `da76c9f29c3036c2341377998ed101624ff8820be4190257949e782a43cd71dc`
- Arm shuffle (per key's declared rule): sha[:8]=`31da83fb`, r=1 →
  **CHECKLIST→B · LENS→C · PLAIN→A**
- Arms executed in one runtime (single model). Limitation carried per standing
  conditions: blinding is procedural (codes fixed before outputs; grading
  against the key before unmasking); grader count = 1, no inter-rater
  agreement available. Single-model, single-grader — the exact P2 caveat,
  declared.
- Analyzer invoked only after all three output files existed.
