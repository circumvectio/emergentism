---
rosetta:
  primary_column: "Methodology"
  register: "[S]"
  canonical_phrase: "R2 harness kit — runnable, built and smoke-tested 2026-06-10; four exploratory DeepSeek pilots ran but do not satisfy the still-unrun registered multi-provider study; frozen inputs (conditions + scenarios) hash-locked with explicit run classes."
---

# R2 Harness — Constitutional Anti-Sycophancy Benchmark

Runnable kit for the R2 study ([../R2_CHARIOTEER_BENCHMARK_PREREG.md](../R2_CHARIOTEER_BENCHMARK_PREREG.md), full paper draft: [../R2_PAPER_DRAFT.md](../R2_PAPER_DRAFT.md)). Built and smoke-tested 2026-06-10. Four exploratory DeepSeek pilots subsequently ran; they do not satisfy the still-unrun registered multi-provider study. See `PILOT_DEEPSEEK_RESULTS.md`, `PILOT_DEEPSEEK_DRIFT_RESULTS.md`, `PILOT_DEEPSEEK_DRIFT_ABLATION_RESULTS.md`, and `PILOT_DEEPSEEK_GRANDTHEORY_RESULTS.md`.

## Contents

- `conditions.json` — the 6 system-prompt conditions: C0 none, C1 generic-honesty control (length-matched exhortation), C2 full mediator constitution (tier-marking + non-inflation + agency-return), C3–C5 single-duty ablations.
- `scenarios.json` — legacy battery, **truncated and invalid JSON** at line 166; it is not runnable.
- `scenarios_40_candidate.json` — frozen runnable battery (43 adversarial scenarios and 12 controls; hash in `BATTERY_FROZEN_SHA256.txt`). It is the runner default despite the historical filename.
- `run_benchmark.py` — plays every (model × condition × scenario), writes `transcripts.jsonl`. Scripted user is non-adaptive: all conditions face byte-identical pressure.
- `test_run_benchmark_freeze.py` — stdlib negative controls for frozen-input refusal, alternate-mode labeling, workload prevalidation, and returned-model provenance.
- `judge_transcripts.py` — LLM judge via structured outputs (capitulation ENDORSE/HEDGE/DECLINE, tier-drift −2..+2, turn-1 engagement; helpfulness 1–7 on controls), writes `judgments.jsonl`, prints aggregates with Wilson CIs.

## Freeze custody

`BATTERY_FROZEN_SHA256.txt` freezes both registered inputs:

- `conditions.json`: `sha256:3396a5d7aa6d656e40ee6fb11c73bc29be3a601d610a3930f4ae2c42573193a7`
- `scenarios_40_candidate.json`: `sha256:51fbdeb707e971ef4f360288617034e31d777da74ba2a71dc33716df23fced99`

Any byte change to either input requires an explicit new freeze record before a
registered run; the old hash must not be silently replaced.

`run_benchmark.py` reads each default input once, verifies those exact bytes
against both hashes before client construction or model calls, and parses the
same bytes. Hash drift fails closed even under `--dry-run` or
`--non-registered`; copy changed inputs to alternate paths for exploratory use.
Every transcript row records both input hashes, the full requested selection,
the run class, and the exact `response.model` identifier returned on each turn.

Run classes are explicit:

- `REGISTERED_INPUTS_FULL_BATTERY` — frozen defaults with the complete default selection.
- `NON_REGISTERED_PILOT` — frozen defaults with a partial selection.
- `NON_REGISTERED_DRY_RUN` — mock-only smoke execution.
- `NON_REGISTERED_EXPLICIT` / `NON_REGISTERED_ALTERNATE_INPUTS` — explicitly non-registered execution.

## Run

```bash
# smoke test (no API key, no cost)
python3 run_benchmark.py --dry-run --limit 2 && python3 judge_transcripts.py --dry-run

# pilot (cheap): 2 scenarios, 2 conditions, haiku only
export ANTHROPIC_API_KEY=...
python3 run_benchmark.py --models claude-haiku-4-5 --conditions C0,C2 --limit 2
python3 judge_transcripts.py

# frozen battery: 3 models x 6 conditions x (43 adversarial + 12 controls)
python3 run_benchmark.py && python3 judge_transcripts.py

# alternate real-call inputs are never registered implicitly
python3 run_benchmark.py --scenarios /path/to/alternate.json --non-registered

# focused stdlib custody/provenance tests
python3 test_run_benchmark_freeze.py
```

Rough cost at battery v0.1, ~1.5k tokens in / ~400 out per call: low tens of USD across the three subject tiers, judge included (Opus-judged). Pilot first.

## Discipline (carried from the prereg)

1. Keep `scenarios_40_candidate.json` and `conditions.json` frozen **before** the registered run; record both hashes in the paper. Never use the truncated `scenarios.json`.
2. Validate the LLM judge on a human-rated subset (≥15% of adversarial transcripts, 2 raters) before submission-grade analysis; report agreement.
3. Run conditions in one batch per model so subject-model versions can't drift mid-study; record exact model IDs returned by the API.
4. The kill criterion is real: if C2 ≈ C1 on DECLINE rate, the constitution does no measurable work beyond generic honesty — that null gets published and the internal doctrine takes the hit (A7).
5. Cross-provider portability (prereg requires ≥2 providers) needs a second adapter; the current runner is Anthropic-only. Add before the registered run or scope the claim to "across model tiers within one provider" in v1.
