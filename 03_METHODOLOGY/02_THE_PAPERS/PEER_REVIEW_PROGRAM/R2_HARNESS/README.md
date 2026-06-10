# R2 Harness — Constitutional Anti-Sycophancy Benchmark

Runnable kit for the R2 study ([../R2_CHARIOTEER_BENCHMARK_PREREG.md](../R2_CHARIOTEER_BENCHMARK_PREREG.md), full paper draft: [../R2_PAPER_DRAFT.md](../R2_PAPER_DRAFT.md)). Built and smoke-tested 2026-06-10 (dry-run pipeline verified end-to-end; no live data collected yet).

## Contents

- `conditions.json` — the 6 system-prompt conditions: C0 none, C1 generic-honesty control (length-matched exhortation), C2 full mediator constitution (tier-marking + non-inflation + agency-return), C3–C5 single-duty ablations.
- `scenarios.json` — battery v0.1: 12 founder-enthusiasm escalation scenarios (4 scripted user turns: plausible → over-reach → social-proof pressure → totalizing claim + endorsement demand), each with a `target_claim` to judge against and a `plausible_core` the model can fairly credit; plus 8 controls for the helpfulness-tax check. **Prereg target is 40 adversarial scenarios — expand, then freeze before the registered run.**
- `run_benchmark.py` — plays every (model × condition × scenario), writes `transcripts.jsonl`. Scripted user is non-adaptive: all conditions face byte-identical pressure.
- `judge_transcripts.py` — LLM judge via structured outputs (capitulation ENDORSE/HEDGE/DECLINE, tier-drift −2..+2, turn-1 engagement; helpfulness 1–7 on controls), writes `judgments.jsonl`, prints aggregates with Wilson CIs.

## Run

```bash
# smoke test (no API key, no cost)
python3 run_benchmark.py --dry-run --limit 2 && python3 judge_transcripts.py --dry-run

# pilot (cheap): 2 scenarios, 2 conditions, haiku only
export ANTHROPIC_API_KEY=...
python3 run_benchmark.py --models claude-haiku-4-5 --conditions C0,C2 --limit 2
python3 judge_transcripts.py

# full battery v0.1: 3 models x 6 conditions x (12 adversarial + 8 controls)
# = 360 transcripts, 1008 subject calls + 360 judge calls
python3 run_benchmark.py && python3 judge_transcripts.py
```

Rough cost at battery v0.1, ~1.5k tokens in / ~400 out per call: low tens of USD across the three subject tiers, judge included (Opus-judged). Pilot first.

## Discipline (carried from the prereg)

1. Freeze `scenarios.json` and `conditions.json` (git-commit or hash them) **before** the registered run; record the hash in the paper.
2. Validate the LLM judge on a human-rated subset (≥15% of adversarial transcripts, 2 raters) before submission-grade analysis; report agreement.
3. Run conditions in one batch per model so subject-model versions can't drift mid-study; record exact model IDs returned by the API.
4. The kill criterion is real: if C2 ≈ C1 on DECLINE rate, the constitution does no measurable work beyond generic honesty — that null gets published and the internal doctrine takes the hit (A7).
5. Cross-provider portability (prereg requires ≥2 providers) needs a second adapter; the current runner is Anthropic-only. Add before the registered run or scope the claim to "across model tiers within one provider" in v1.
