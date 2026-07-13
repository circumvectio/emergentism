# Pooled GFS — multiplicative (φ×ν) vs additive (φ+ν)

Executes **test #1** of the Seven-Operator K2 packet (`../../50_AUDITS_AND_EXECUTIONS/101_SEVEN_OPERATOR_REFINEMENT_K2_PACKET_2026_07_02.md`) — the pooled analysis Wave-1 deferred.

- `run_pooled.py` — re-pools the on-disk per-country fits (`09_TOOLS/04_DATA_PIPELINES/gfs_results_20260409.csv`), evaluates the multiplicative claim by AIC + interaction direction + the audit kill-criterion.
- `RUN_OUTPUT.txt` — raw stdout receipt.
- `VERDICT.md` — the verdict: **kill-criterion FAILED** (framework-consistent 8/23; pooled β = −0.134). `[B]` result, `[I]` interpretation, staged for K2.

Reproduce: `python3 run_pooled.py`. Honest limit: re-pooling of existing fits, not a re-fit on raw microdata (not on disk).
