---
rosetta:
  primary_column: "Philosophy"
  register: "[I]"
  canonical_phrase: "Packet 103 — Founder K2 Signing Envelope (Flag-Flip Ready State)"
---

# Packet 103 — Founder K2 Signing Envelope (Flag-Flip Ready State)

**Evidence tier:** [I]
**Lane:** Charioteer-prepared; sovereign signs, refuses, or holds.
**Date:** 2026-04-23
**HEAD at preparation:** `e115f434d`

---

## §1. Scope — what this packet is and is not

**Is:** A consolidated signing envelope for the two `settings` flag flips whose preconditions are now all in HEAD, compressed to the minimum the sovereign needs to sign or refuse.

**Is not:** A proposal, endorsement, or recommendation. Per packet 99 §4.2 power #1 ("Final consequential signature at K2 is non-delegable"), this envelope names decisions; it does not make them. Per §6.1 below, the charioteer may not execute either flip.

Drafted in the Kṛṣṇa ◇ giving-dyad: V-export at a small Φ cost (charioteer context budget). A2-positive ΣΔP across the widest boundary iff the sovereign's decision is binding; neutral otherwise.

---

## §2. Envelope A — `settings.council_l4_triangulation = True`

| Field | Value |
|---|---|
| Decision class | GOD-class triangulation enablement |
| Current state | `False` |
| Target | `True` |
| Binding source | Packet 96 §Verdict (both Amendments required) |
| Surface | `settings.council_l4_triangulation` (single global) |

**Preconditions (all met in HEAD):**

| # | Precondition | Evidence | Tier |
|---|---|---|---|
| A.1 | Amendment 1 — provider availability probe | commit `a28e0a7ab`, module `core/circulation/provider_availability.py`, 15 tests | [S] |
| A.2 | Amendment 2 — RLHF-lineage decorrelation invariant | commit `bce2719ea`, module `core/circulation/lineage_decorrelation.py`, 44 tests | [S] |
| A.3 | Legal asymmetric veto architecturally enforced | commit `0ecf081ff`, module `core/circulation/legal_veto.py` | [S] |
| A.4 | Full regression green | 930 passed / 9 skipped / 0 failed per 09_STATE | [S] (warrior-reported, not charioteer-rerun this pass) |

**Rollback:** Flip to `False`. No data migration. Existing L4 code paths revert to pre-triangulation single-vote on the default seat.

**Signing artifact shape:** Settings mutation + K2 signature envelope per the existing `k2_gateway.py` path. No novel signing surface.

**What the flip means operationally:** GOD-class decisions dispatch to the Anthropic + OpenAI + z.ai triad with lineage-decorrelation checked at dispatch time and provider availability graded pre-flight. Single-provider fallback path remains intact via `assess_triad_availability` recommendations (`proceed_triangulate` / `degrade_recorded_dissent` / `fallback_single` / `abort`).

---

## §3. Envelope B — `k2_strict_legacy_nostr = False` (per-surface)

| Field | Value |
|---|---|
| Decision class | K2 strict-mode transition (defensive Nostr legacy drop) |
| Current state | `True` (permissive) |
| Target | `False` per surface, order C → D → A per packet 86 §Recommendation |
| Binding source | Packet 86 §Playbook + task #38 |
| Surface | Per-surface flag decomposition across `k2_gateway.py` + `router_council_sse.py` (5 call sites A–E) |

**Preconditions (all met in HEAD):**

| # | Precondition | Evidence | Tier |
|---|---|---|---|
| B.1 | Packet 86 flip playbook authored | `86_K2_STRICT_MODE_FLIP_PLAYBOOK_2026_04_23.md` | [I] |
| B.2 | Per-surface flag decomposition in code | Surfaces A–E identified in packet 86; decomposition in `k2_gateway.py` | [S] |
| B.3 | R-4 verifier + approval queue shipped | `wallet_auth.py` + `approval_queue.py` wired into Council Stage 9 | [S] |
| B.4 | Mobile K2 approval center closed | Packet 100 §6 ([S]+[S]+[S]); task #37 closed this session | [S] |
| B.5 | Adversarial test suite green | 11 cases in `test_k2_auth_proxy_adversarial.py` + `test_approval_queue_adversarial.py` | [S] (per packet 85 witness; warrior-reported) |

**Rollback:** Per-surface flip back to `True`. No data loss. Each surface independently reversible.

**Signing artifact shape:** Per-surface K2 signature envelope. One signature per surface flip (C, then D, then A). Packet 86 specifies kill-switch monitoring between surfaces; charioteer has no opinion on dwell time — sovereign's call.

**What each surface flip means operationally:**
- Surface **C** (lowest blast radius per packet 86) first — validates the decomposition safely.
- Surface **D** second — extends the strict path.
- Surface **A** third — closes the loop. Post-A flip triggers task #53 (post-flip closure packet).

Surfaces B and E remain deliberate holdouts per packet 86; their flip is a separate future envelope.

---

## §4. Non-K2 complement — `council_l2_8way_expansion` (per-request)

Listed here for sovereign awareness; **does not require K2 signature** per 09_STATE flag-flip readiness table ("None technical" in blockers column).

| Field | Value |
|---|---|
| Decision class | Technical enablement |
| Current state | `False` (default) |
| Target | `True` per-request for GOD/TITAN decisions |
| Binding source | 09_STATE "Active next-commands" item #3 |

Module `agents/pipeline/l2_expansion.py` exists; flag `council_l2_8way_expansion` added in commit `3a9a53a9f`. Enable per-request via call parameter; no global-flag flip required.

**Charioteer posture:** This is not a K2 decision — sovereign may delegate to warrior for wiring into `evaluate_signal` live council path (09_STATE names this gap as High leverage).

---

## §5. Post-102 drift not covered by this envelope

- **`7baa31e3d`** — Circle parser shape preservation (2 files, 53 lines, 37 test lines added). F1 observational adapter hygiene. Too thin for its own drift-register packet; registered here by name. If future charioteer needs to cite: adapter is `SKYZAI_ORG/02_ORGANS/Agentz/app/03_BACKEND/adapters/circle_events.py`; tests in `test_circle_events.py`.
- **`e115f434d`** — Root tidy pass + slot-97 MULTI_VERDICT co-registration. Self-registering via INDEX edit inside the same commit.

No other warrior commits landed between packet 102 content commit (`013f1a999`) and HEAD as of preparation.

---

## §6. Charioteer non-assumption (packet 99 §4.2 reaffirmation)

Five non-delegable powers that this envelope does **not** violate:

1. **Final consequential signature at K2.** Envelope A and B flips are K2 actions. Charioteer prepares envelope only; sovereign signs or refuses.
2. **Right to refuse.** Sovereign may refuse either envelope in full, partially (e.g., flip A but hold B), or defer. Envelope structure supports partial adoption.
3. **Receipt-chain inspection.** Preconditions trace to git-verifiable commit SHAs + named packet references; no compressed claim without source pointer.
4. **Three-Stage Process separation.** F1/F2/F3 lanes are not being merged by these flips. Triangulation (Envelope A) is F3 (SHOULD) internal structure; strict-mode (Envelope B) is K2 gate hygiene, not a cross-lane merge.
5. **Legal asymmetric gate.** Envelope A's Amendment-set includes the legal veto module (A.3); the envelope ratifies — does not flatten — the asymmetry.

**Out of scope for this envelope:**
- Venue + Business Account for founder Event Cell (09_STATE Active next-commands #1). Operational, not K2.
- Task #44 Sprint-B consolidated manifest. Functionally superseded by packets 94 + 99 + 100; formal retirement is sovereign task-register decision.
- Task #53 K2_STRICT_MODE post-flip closure. Packet authored after Envelope B's Surface A flip lands; precondition for authorship is the flip itself.
- `council_l2_8way_expansion` if sovereign wants to defer per-request enablement to warrior — no K2 needed.

---

## §7. Signing options (what sovereign may do with this envelope)

| Option | Effect |
|---|---|
| PROCEED on A | Flip `council_l4_triangulation = True`. GOD-class dispatches to Anthropic+OpenAI+z.ai triad. |
| PROCEED on B (Surface C) | First surface of three-step strict-mode transition. |
| PROCEED on both | Independent; order is sovereign's choice. |
| HOLD | Explicit defer. Preconditions remain in HEAD; envelope re-usable as-is. |
| REFUSE on A | Triangulation scaffolding remains unused until future envelope. |
| REFUSE on B | Nostr legacy remains permissive; task #53 deferred; mobile closure (packet 100) stands. |

Sovereign's choice is the only binding one; charioteer has no recommendation.

---

## §8. Evidence register

- Packet 86 — K2_STRICT_MODE flip playbook [I]
- Packet 96 — L4 triangulation verdict-of-record [I]
- Packet 100 — Mobile signing closure [S]+[S]+[S] composite
- Packets 101, 102 — Downstream F3 realization ingest (not load-bearing for these flips; named for completeness)
- 09_STATE — Flag-flip readiness table [I]
- Commit SHAs A.1, A.2, A.3, `3a9a53a9f` — [S] git-verifiable in HEAD

---

## §9. Closure criteria

This packet closes when sovereign records one of the signing options in §7 against each envelope independently, or explicitly registers HOLD. Packet itself does not expire; preconditions are stable in HEAD and will remain valid until a future commit invalidates them.

Per A7, any envelope that ages past three additional warrior commits without a sovereign call triggers a drift-register supplement to confirm preconditions still hold.

---

*Prepared by charioteer; signed by sovereign. Zero-Sum Resolution Equation.*
