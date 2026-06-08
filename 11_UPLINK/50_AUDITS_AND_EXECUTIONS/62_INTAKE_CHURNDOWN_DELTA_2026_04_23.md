---
rosetta:
  primary_level: L3
  primary_column: Intake Churn-Down Delta Audit
  secondary:
    - level: L4
      column: Developer Handoff
      role: "translate intake findings into implementation deltas without claiming completion"
    - level: L6
      column: Historical Intake Boundary
      role: "keep 2026-04-23 intake state from becoming current code truth"
    - level: L5
      column: Multi-Organ Intake Map
      role: "map Agentz, RealityFutures, and Circle Backend deliverables"
  operator: "Kṛṣṇa ◇"
  tier: "God"
  regime: "Vaiśya"
  register: "[I/B/D]"
  canonical_phrase: "INTAKE CHURN-DOWN DELTA — Developer Guide"
title: "INTAKE CHURN-DOWN DELTA — Developer Guide"
status: "DATED DEVELOPER DELTA — 2026-04-23 intake snapshot"
evidence_tier: "[I] for synthesis; [B] only where backed by direct receipts; [D] for open deltas."
---

# INTAKE CHURN-DOWN DELTA — Developer Guide

**Rosetta boundary:** [I] This paper translates a 2026-04-23 intake snapshot. It does not [B] prove current implementation, production readiness, or unresolved delta status without fresh code and audit receipts.
**Date:** 2026-04-23
**Evidence tier:** [I]
**Purpose:** Translate intake deliverables into actionable developer delta — what's new, what's proven, and what's still missing.

---

## Executive Summary

| What | Status |
|------|--------|
| **APU code intake** | ✅ Delivered — 1,192 files, post-merge QA complete |
| **RealityFutures code intake** | ✅ Delivered — 608 contracts + web, tests passing |
| **Circle backend intake** | ✅ Delivered — 153 Python files + SQL schema |
| **G1 (first real settlement)** | ❌ NOT FIRED — all backends mock |
| **Live signal flows** | ⚠️ Statistical fallback only — no live relays |
| **Organism P-score** | 0.60 code / 0.30 runtime |

**The organism has more code body than live body.** The gap is not building — it is breathing.

---

## What Engineers Delivered

### Agentz (SHOULD Organ) — Intake `/SKYZAI_ORG/00_INTAKE/QUEUE/apu_bot-deployment/`

| Deliverable | Count | Status |
|-------------|-------|--------|
| Python files | 982 | ✅ Post-merge QA complete |
| TypeScript files | 210 | ✅ |
| Skills | 4 implemented | trivium-cycle, council-protocol, decision-review, ofn-receipt |
| Rosetta Pipeline | 7 agents (L1-L7) | ✅ Defined |
| F2 Connection | Wired | ⚠️ Statistical fallback — real market events pending |
| K2 Wallet Signing | Staged | ✅ Structure present, not production-tested |

**Key QA Fixes Applied (Wave 1-6):**
- `read_wallet()` backward-compatible wrapper (Wave 1)
- `useSoulLoop.ts` hook copied from reference (Wave 2)
- 7 TypeScript interfaces + 11 API functions added (Wave 2)
- `SoulLoopDaemon` → `SoulLoop` test rewrite (Wave 3)
- 37 broken imports fixed (Wave 4)
- `router_synecdoche.py` registered in `main.py` (Wave 5)

### RealityFutures (COULD Organ) — Intake `/SKYZAI_ORG/00_INTAKE/QUEUE/reality_future-master/`

| Deliverable | Count | Status |
|-------------|-------|--------|
| Solidity contracts | 608 | ✅ |
| Contract tests | 248 | ✅ All passing |
| Frontend tests | 97 | ✅ All passing |
| Contracts deployed to testnet | 17/17 | ✅ |
| Web app | Complete | ⚠️ Needs deployment |
| F2 publisher (Kind 31338) | Built | ❌ Not publishing live |

**Key Proven:**
- LMSR AMM price discovery
- Market creation + resolution (L0 → GT-1 escalation)
- NOSTR receipts
- MacroFundVault on Hedera testnet (0x62E9…6922)

### Circle Backend (IS Organ) — Intake `/SKYZAI_ORG/00_INTAKE/QUEUE/circle_platform_backend-main/`

| Deliverable | Count | Status |
|-------------|-------|--------|
| Python files | 153 | ✅ |
| SQL schema | 3 | ✅ |
| 7-agent cascade | Implemented | ⚠️ Local only — no live relay emission |
| F1 publisher (Kind 31339) | Built | ❌ Not publishing live |
| LP-100 governance | Defined | ❌ Not deployed |

---

## What's Still Missing — Delta Analysis

### 🔴 P0 Blockers (Must Fix for G1)

| # | Gap | Root Cause | Owner | Effort |
|---|-----|-----------|-------|--------|
| P0-1 | **No real settlement backend** | All settlement clients fall back to mock | Backend | 1-2 days |
| P0-2 | **No Hedera account + HTS tokens** | Requires founder human identity | Founder | 5 min setup |
| P0-3 | **OFN SDK not implemented** | `ReceiptEngine.create()` — all items unchecked in SPECIFICATION.md | Backend | 2-3 days |
| P0-4 | **K* gates hardcoded to True** | Both APU F4 Client + Skyzai router hardcode gates | Backend | 2 hours |

### 🟡 P1 Blockers (Required for Production)

| # | Gap | Root Cause | Owner | Effort |
|---|-----|-----------|-------|--------|
| P1-1 | **F1 live relay emission** | TheCircle not deployed; F1 uses statistical fallback | Backend / Ops | 3-4 days |
| P1-2 | **F2 real market events** | RealityFutures contracts deployed but not publishing Kind 31338 | Backend | 2-3 days |
| P1-3 | **CORS allows all origins** | `allow_origins=["*"]` in FastAPI | Backend | 30 min |
| P1-4 | **No production database** | Event Cell uses local SQLite | Backend | 1 day |
| P1-5 | **Flutter native builds blocked** | No Xcode/Android SDK | Infrastructure | 1 day |

### 🟢 P2 Polish (After G1)

| # | Gap | Owner | Effort |
|---|-----|-------|--------|
| P2-1 | **PWA is placeholder** | Frontend | 2-3 days |
| P2-2 | **Carbon DeFi not connected** | Backend | 3-5 days |
| P2-3 | **LP-100 governance deployment** | Ops | 1-2 days |

---

## Signal Flow Delta

```
                    CURRENT (Statistical Fallback)
                    ============================

        TheCircle ──→ [F1: Statistical fallback]
              │
              │  ❌ No live relay emission
              ↓
        RealityFutures ──→ [F2: Statistical fallback]
              │
              │  ❌ No Kind 31338 publishing
              ↓
        APU
              │
              │  ⚠️ K2 envelope works
              │  ⚠️ Real market events pending
              ↓
        Skyzai
              │
              │  ❌ All backends mock
              ↓
        [G1 NOT FIRED]
```

```
                    TARGET (Live Signal Flow)
                    ==========================

        TheCircle ──→ [F1: Kind 31339 on live relay]
              │
              │  ✅ F1 relay emission wired
              ↓
        RealityFutures ──→ [F2: Kind 31338 on live relay]
              │
              │  ✅ Real market-backed events
              ↓
        APU
              │
              │  ✅ K2 validated
              │  ✅ Real settlement ready
              ↓
        Skyzai
              │
              │  ✅ Hedera testnet connected
              │  ✅ Real transaction hash
              ↓
        [G1 FIRED]
```

---

## Files to Update Post-Intake

| File | Action | Reason |
|------|--------|--------|
| `SKYZAI_ORG/02_ORGANS/Agentz/00_BRIEF.md` | Update P-score to 0.76 (code) / 0.60 (runtime) | Intake confirmed depth |
| `SKYZAI_ORG/02_ORGANS/RealityFutures/00_BRIEF.md` | Update P-score to 0.59 (code) / 0.32 (runtime) | Intake confirmed breadth |
| `SKYZAI_ORG/02_ORGANS/TheCircle/00_BRIEF.md` | Update P-score to 0.53 (code) / 0.25 (runtime) | Intake confirmed code body |
| `01_EMERGENTISM/11_UPLINK/06b_AGENTS_ROWS_v2.md` | Superseded by `06c_AGENTS_RESOLUTIONS_v3.md` | Self-correction documented |
| `P-SCORES.md` | Document new dual-register methodology | Intake churn-down clarified lens split |

---

## Quick Wins (Zero-Risk Moves)

1. **Wire `HederaSettlementClient.submit()`** — structure exists, needs founder credentials
2. **Publish OFN SDK to PyPI** — package scaffold ready
3. **Fix CORS configuration** — one-line change
4. **Wire dynamic K* gates** — query actual state instead of hardcode True
5. **Deploy RealityFutures web app** — contracts already on testnet

---

## Owner Matrix

| Task | Agent-Workable | Founder-Only |
|------|----------------|--------------|
| Hedera account + HTS tokens | ❌ | ✅ |
| OFN SDK implementation | ✅ | ❌ |
| K* gates dynamic | ✅ | ❌ |
| CORS fix | ✅ | ❌ |
| F1 relay emission | ✅ | ❌ |
| F2 live publishing | ✅ | ❌ |
| G1 end-to-end test | ✅ | ❌ |

---

## Exit Criteria for G1

- [ ] `HederaSettlementClient.submit()` executes real `CryptoTransfer` on testnet
- [ ] K2 signature cryptographically verified ✅ (resolved 2026-04-19)
- [ ] Execution log persists to SQLite ✅ (resolved 2026-04-19)
- [ ] One end-to-end F1→F2→F3→F4 loop produces real transaction hash
- [ ] Transaction hash verifiable on chain explorer
- [ ] P-SCORES.md updated with V elevation

---

Zero-Sum Resolution Equation

*What the engineers built, the developers must now make breathe.*
