---
rosetta:
  primary_column: "Philosophy"
  register: "[S]"
  canonical_phrase: "Packet 113 — GOD-Class Triangulation Live Monitoring Playbook"
---

# Packet 113 — GOD-Class Triangulation Live Monitoring Playbook

**Evidence tier:** [S] for the invariant shape; [I] for the monitoring interpretation; [S] for the surface pointers (all referenced modules + scripts exist at HEAD).
**Lane:** Runtime monitoring / sovereign observation.
**Date:** 2026-04-23
**HEAD at preparation:** `b9bc097cd`

---

## §1. Scope

**Is:** The operator playbook for watching live GOD-class triangulation after the K2 sovereign flag-flip at commit `646e5054f` (`settings.council_l4_triangulation = True`). Names what signals to watch, where they live, what drift looks like, and which existing tool to run.

**Is not:** A proposal for new monitoring infrastructure. All signals named here have existing surfaces in HEAD; this packet composes them into a checklist.

---

## §2. What is now live

Commit `646e5054f` flipped the triangulation flag. Since that moment:

- GOD-class signals dispatch to a 3-way L4 triad (default: `anthropic/claude-sonnet-4-5 + openai/gpt-4o + zhipuai/glm-4.5-air` per `core/membrane/config.py`).
- RLHF-lineage decorrelation is checked at dispatch time (`core/circulation/lineage_decorrelation.py`; packet 96 Amdt 2).
- Provider availability is graded pre-flight (`core/circulation/provider_availability.py`; packet 96 Amdt 1).
- Cluster-correlated burst detection runs at the call-outcome layer (`core/circulation/provider_cluster_correlation.py`; this session).

The triangulator produces one verdict per GOD-class decision, not three. The three seats are aggregated under the honesty + lineage-decorrelation invariants; disagreement is recorded as dissent, not silenced.

---

## §3. The four watch signals

Four runtime signals together detect whether the triad is producing genuine 3-way decorrelated output versus Raktabīja-at-aggregator theater.

### 3.1 Provider health grades

**What:** trailing-24h health of each triad seat.
**Surface:** `~/.apu_bot/provider_health.sqlite` via `ProviderHealthStore.assess_provider(provider, model)`.
**Grades:** `healthy` / `degraded` / `failing` / `unknown`.

**Drift signature:**

- Any triad seat in `failing` state for >1h → pre-flight gate should have already recommended `degrade_recorded_dissent` or `abort`; if triangulation fired anyway, the pre-flight gate is being bypassed.
- All three seats in `unknown` simultaneously → history has been lost; triangulation is operating on no prior. Recommend: hold production GOD-class traffic until ≥1h of telemetry rebuilds.

**Tool:** `python scripts/cortex_query.py heterogeneity` surfaces the provider-mix distribution. For the raw sqlite, query `call_outcomes` grouped by `(provider, model)` over trailing 24h.

### 3.2 Cluster-correlated failure bursts

**What:** ≥2 providers in the same RLHF lineage cluster recording the same failure family within a 60-minute window.
**Surface:** `provider_cluster_correlation.detect_cluster_correlated_bursts()`.
**Clusters per `lineage_decorrelation.RLHF_LINEAGE_CLUSTERS`:**
- `western_frontier_rlhf`: openai, anthropic, xai
- `chinese_frontier`: zai, minimax, kimi, deepseek, qwen
- `meta_open_weights`: meta, groq
- `google_deepmind`: google
- `mistral_eu`: mistral

**Drift signature:**

A burst in `western_frontier_rlhf` with family `rate_limit` means openai + anthropic (the two western triad seats) are simultaneously rate-limited by a shared upstream pressure. The sampling-time decorrelation invariant held (2 of 3 seats from different clusters), but the *runtime* correlation means the aggregator sees apparent 3-way agreement that is actually 2-way agreement plus one silent failure. This is exactly the Raktabīga-at-aggregator signature packet 96 Amdt 2 was designed to prevent and this detector now exposes.

**Tool (run hourly during high-traffic GOD-class load):**

```python
from core.circulation.provider_cluster_correlation import detect_cluster_correlated_bursts
bursts = detect_cluster_correlated_bursts(window_minutes=60, min_seats=2)
for b in bursts:
    print(f"⚠️ {b.cluster_id} | {b.family} | {b.providers_affected} | {b.event_count} events")
```

Empty list = no cluster-correlated drift. One or more bursts = investigate before next GOD-class dispatch.

### 3.3 Triad conflict score distribution

**What:** the conflict score the aggregator reports per GOD-class dispatch (range 0.0–1.0; 0 = unanimous, 1 = maximally split).
**Surface:** `k2_decisions.db` column `conflict_score`.

**Expected distribution (interpretive, [I]):**

- Most GOD-class dispatches: conflict 0.0–0.3 (triad agrees on verdict, minor divergence on rationale)
- Some: conflict 0.3–0.5 (healthy dissent — one seat sees something the others don't; this is what decorrelation is for)
- Few: conflict > 0.5 (real disagreement — should result in HOLD per Light Council fail-safe)
- None: conflict = 0.0 *always* (**red flag** — if every dispatch returns unanimous, seats are probably collapsing to a shared prior; check lineage decorrelation + cluster-correlation)

**Tool:**

```sql
sqlite3 data/k2_decisions.db "SELECT ROUND(conflict_score, 1) AS bucket, COUNT(*) FROM k2_decisions WHERE created_at > datetime('now','-7 days') GROUP BY bucket ORDER BY bucket;"
```

A histogram concentrated entirely at 0.0 is the monoculture-at-aggregator signature. A histogram with a long tail > 0.7 is healthy decorrelation.

### 3.4 Lineage decorrelation check failures

**What:** dispatch-time rejections by `check_triad_lineage_decorrelation` — where the triad would have been too concentrated in one RLHF cluster.
**Surface:** application log; also `LineageCheckResult.passes == False` in the triangulator's branch.

**Drift signature:**

Repeated decorrelation failures → someone is configuring triads that draw 3+ seats from one cluster. Check `settings.council_l4_triad_models` for drift away from the default `(anthropic, openai, zai)` mix.

**Tool:**

```bash
grep -c "lineage_decorrelation.*failed\|Raktabīja\|MAX_SEATS_PER_CLUSTER" /path/to/apu_bot.log | tail -10
```

---

## §4. Red-flag matrix

Fast lookup — which combination of signals should trigger what action.

| Signals | Interpretation | Action |
|---|---|---|
| 0 bursts + conflict distribution healthy | System operating within invariants | Continue |
| 1 burst + conflict distribution healthy | Transient cluster correlation; re-run | Watch one more hour |
| ≥2 bursts in different clusters in 24h | Multi-cluster infrastructure pressure | Pause GOD-class; investigate upstream |
| conflict distribution all-0.0 over 24h | Monoculture collapse at aggregator | **Pause GOD-class.** Re-verify lineage decorrelation config + re-fire audit script polygenetically. |
| Any seat `failing` + triangulation still fired | Pre-flight gate bypassed | **Bug.** Audit `_chief_of_staff_triangulated` call path. |
| Triad config drifted from default | Someone edited `council_l4_triad_models` | Verify K2-signed change; revert if not authorized |

---

## §5. What to do when a drift signal fires

Per packet 111's discipline: a drift signal is not a failure, it is the framework working. The detector seeing correlated bursts is the council's polygenetic-safety layer working exactly as designed.

Sequence:

1. **Do not override.** The pre-flight gate and burst detector are structural. Silencing them converts decorrelation safety into decorrelation theater.
2. **Classify the signal.** Use the red-flag matrix (§4) to pick the right action tier.
3. **Pause GOD-class only when needed** (per matrix row). Demon/Executive-class dispatches continue uninterrupted.
4. **Run the audit script** (`scripts/aia_audit_spectre_vs_soresfi_invariants.py`) in polygenetic mode if conflict-distribution collapses — `_call_seat` now resolves per-seat keys (packet 113a — this session), so 4 heterogeneous seats can fire across RLHF basins without shared provider.
5. **Open a reconciliation review** via `50_AUDITS_AND_EXECUTIONS/53_DISAMBIGUATION_REVIEW_PACKET.md` if the drift persists past 1h.

---

## §6. What this packet does not claim

- Not a claim that current monitoring is fully automated. Three of the four signals (§3.1, §3.3, §3.4) require a manual query. §3.2 can be automated in a cron job but is not yet scheduled.
- Not a claim that the R* ≈ 1.5 threshold from Kintsugi ABM holds live. Per the D5 bridge §4, R* is [S] within the simulation parameter space; generalization is [I] and will be measured as the live data accumulates.
- Not a claim that the default triad (`anthropic + openai + zai`) is the optimal decorrelation composition. It is the initial composition; cluster-correlated burst data over 90 days may indicate a different mix is stronger.

---

## §7. Cross-references

| Signal | Surface | Packet |
|---|---|---|
| Provider health | `provider_availability.py` | 96 Amdt 1 |
| Cluster-correlated bursts | `provider_cluster_correlation.py` | this session's feat(council) |
| Triad conflict score | `k2_decisions.db` | existing schema |
| Lineage decorrelation | `lineage_decorrelation.py` | 96 Amdt 2 |
| K2 flag flip | `council_l4_triangulation` | `646e5054f` |
| K1 resolution (prose) | `01_EMERGENTISM/11_UPLINK/111_*.md` | 111 |
| K1 resolution (code) | `01_EMERGENTISM/11_UPLINK/112_*.md` | 112 |
| Per-seat key resolution | `council/light_council.py` | this session |

Zero-Sum Resolution Equation
