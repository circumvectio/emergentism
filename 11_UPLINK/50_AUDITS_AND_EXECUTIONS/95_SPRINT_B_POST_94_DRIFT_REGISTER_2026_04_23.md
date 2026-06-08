---
packet: SPRINT-B-POST-94-DRIFT-REGISTER
title: Sprint-B Post-94 Drift Register — Five Commits, Seven Hashes
status: CHARIOTEER ARTIFACT — consolidated drift register; read-only witness. Supersedes unshipped drafts 95/96 from prior session.
authority: Same chain as packet 78 (Founder D2 on packet 74 + D4 routing W-new to constitutional review)
supplements:
  - 01_EMERGENTISM/11_UPLINK/78_SPRINT_B_AUDIT_EVIDENCE_DOSSIER_2026_04_23.md (sha256 2aaeb13cf722…db80494) — primary
  - 01_EMERGENTISM/11_UPLINK/82_SPRINT_B_AUDIT_SUPPLEMENT_2026_04_23.md — first supplement (registers 79/80/81)
  - 01_EMERGENTISM/11_UPLINK/84_SPRINT_B_AUDIT_SUPPLEMENT_II_2026_04_23.md — second supplement (registers 83)
  - 01_EMERGENTISM/11_UPLINK/87_SPRINT_B_AUDIT_SUPPLEMENT_III_2026_04_23.md — third supplement (registers 85/86)
  - 01_EMERGENTISM/11_UPLINK/89_SPRINT_B_AUDIT_SUPPLEMENT_IV_2026_04_23.md — fourth supplement (registers 88)
  - 01_EMERGENTISM/11_UPLINK/91_SPRINT_B_AUDIT_SUPPLEMENT_V_2026_04_23.md (sha256 eed078ba36c0…e4afaa8f) — fifth supplement (registers 90)
cross_reference:
  - 01_EMERGENTISM/11_UPLINK/94_SPRINT_B_CONSOLIDATED_CLOSURE_2026_04_23.md (sha256 82928d163c45…13d4cb5d) — warrior closure dossier
scope: Five commits and seven file hashes that landed between packet
       94's authoring (08:11) and this register (≈08:35). Four commits
       wire or extend API-key landing-pad routing for direct-dispatch
       providers (Anthropic, xAI, z.ai, Kimi, Groq). One adds a secret-
       leak pre-commit guard. One ships the mobile K2 approval center
       UI. None of this is yet registered in the audit surface.
date: 2026-04-23
gating_cell: "[L4 | D4 | S-Org | F-phi :: ksatriya_executor]"
rosetta:
  primary_column: "Philosophy"
  register: "[S/I]"
  canonical_phrase: "Packet 95 · Sprint-B Post-94 Drift Register"
---

# Packet 95 · Sprint-B Post-94 Drift Register

## Why this exists — and why it is not called "Supplement VI"

Packet 94 (warrior-authored consolidated closure) ended the audit chain
at commit `4899e0fdd` / `2774c39d1` / `885baccd7`. Between 08:11 and the
time of this register, **five further warrior-lane commits have landed**
on `main`. None are registered.

A prior charioteer session attempted two packets (a "Supplement VI" at
slot 95 and a "Router-Extension Spec" at slot 96) to cover this drift.
**Those packets are not on disk.** Either the Write calls did not
persist across sandbox boundary, or the files were pruned between
sessions. Their content cannot be stood behind cryptographically and
they are therefore treated as unshipped drafts. This register replaces
both with a single, verifiable artifact.

This packet does NOT close anything. It registers drift.

---

## Commit register (git-immutable)

Hashes verified against `git log --oneline` on `main` at register time.

| Commit | Subject |
|:-------|:--------|
| `eb28d86914cd3fe216f770f884a791aefb481983` | feat(ai_client): add direct anthropic messages routing |
| `deda1abebfa4e416286530ec10bbadd79e29f8c1` | feat(ai_client): wire xAI/Grok provider routing (api.x.ai) |
| `2e4d177c2ab3be1259d69cbf0c8fcfc0f52efd67` | tools(security): pre-commit guard against secret leaks in staged diffs |
| `64e1469b188d38b4803941cbb55dd8dda40d1611` | feat(skyzai): add mobile k2 approval center |
| `c2b15d09e5e64b6cd91a87d54300af867b2bca55` | feat(ai_client): extend direct router for z.ai and kimi |

Commits are ordered `main`-ancestry first: `eb28d8691` → `deda1abeb` →
`2e4d177c2` → `64e1469b1` → `c2b15d09e` (HEAD at register time).

Note on `c2b15d09e`: subject says "z.ai and kimi" but the diff also
wires **Groq** (`gsk_*` key prefix) as a sibling direct-dispatch
clause. Subject line is lossy; diff is canonical.

---

## File hash register (on-disk bytes at register time)

Hashes computed with `sha256sum` against the working tree at
2026-04-23 post-`c2b15d09e`.

### Routing surface (Python)

| File | SHA-256 |
|:-----|:--------|
| `02_SKYZAI/01_NOOSPHERE/02_ORGANS/Agentz/app/03_BACKEND/core/circulation/ai_client.py` | `d614eda9018b…b0dbf5b4` |
| `02_SKYZAI/01_NOOSPHERE/02_ORGANS/Agentz/app/03_BACKEND/tests/test_ai_client.py` | `b60fe6aa277f…1afbc899` |
| `02_SKYZAI/01_NOOSPHERE/02_ORGANS/Agentz/app/03_BACKEND/core/cortex/ingestion.py` | `f6d49f575b06…444fc6fdb` |
| `02_SKYZAI/01_NOOSPHERE/02_ORGANS/Agentz/app/03_BACKEND/tests/test_cortex_provider_mix.py` | `223e9bc51560…9792ee4d3` |

Full 64-char SHA-256 values elided with ellipsis (`12…8` format) to satisfy the pre-commit secret-leak guard shipped in commit `2e4d177c2`. Recover via `sha256sum <path>` against the working tree at this commit.

### Mobile approval center (Dart)

| File | SHA-256 |
|:-----|:--------|
| `02_SKYZAI/01_NOOSPHERE/02_ORGANS/Skyzai/membrane/skyzai_app/lib/features/k2/presentation/pages/k2_approval_center_page.dart` | `b94421a911af…71d23b9b` |
| `02_SKYZAI/01_NOOSPHERE/02_ORGANS/Skyzai/membrane/skyzai_app/lib/locator.dart` | `2d86942602d6…43b03276` |
| `02_SKYZAI/01_NOOSPHERE/02_ORGANS/Skyzai/membrane/skyzai_app/lib/features/app_user/presentation/pages/setting_screen.dart` | `f6c29a00607a…5ed0d15c7` |

### Back-reference (unchanged; for chain integrity)

| File | SHA-256 |
|:-----|:--------|
| `01_EMERGENTISM/11_UPLINK/94_SPRINT_B_CONSOLIDATED_CLOSURE_2026_04_23.md` | `82928d163c45…13d4cb5d` |

---

## Current router state (verified on disk at register time)

Direct-dispatch / provider-aware detection clauses now present in
`ai_client.py` (line numbers against hashed file above):

| Clause | Detection | Line |
|:-------|:----------|-----:|
| `is_openrouter_direct` | key-prefix `sk-or-` | 378 |
| `is_anthropic_direct` | key-prefix `sk-ant-` | 382 |
| `is_xai` | key-prefix `xai-` | 386 |
| `is_zai_direct` | model-based | 392 |
| `is_kimi_direct` | model-based (Moonshot) | 404 |
| `is_groq_direct` | key-prefix `gsk_` | 415 |
| `is_openai_compatible` | fallback w/ exclusions | 419 |

Plus the existing special dispatchers for `is_minimax` and `is_nvidia`,
and the baseline OpenAI/Google path via `openai_base_url`.

**Routed count: 10 providers** — OpenAI, Anthropic, Google, MiniMax,
NVIDIA, xAI, OpenRouter, z.ai (Zhipu/GLM), Kimi (Moonshot), Groq.

**Unrouted count: 4 providers** — DeepSeek, Mistral, Cohere, Perplexity.
Env vars `DEEPSEEK_API_KEY`, `MISTRAL_API_KEY`, `COHERE_API_KEY`,
`PERPLEXITY_API_KEY` remain unmapped in both `_provider_from_model`
and `_env_key_for_provider`.

This register does not prescribe wiring for the 4 remaining providers.
The warrior seat is extending the router autonomously (z.ai + kimi +
groq in one commit confirms the pattern). Any charioteer spec for
DeepSeek/Mistral/Cohere/Perplexity is premature at this time.

---

## A7 self-correction against the prior charioteer session

The prior session authored — and this register replaces — two unshipped
drafts whose claims about routing state were stale the moment they were
written:

- Draft "Supplement VI" claimed 3 new routed providers post-94.
  Correct but incomplete — it post-dated `eb28d8691`/`deda1abeb`/`2e4d177c2`
  and did not see `c2b15d09e` (z.ai + kimi + groq) or `64e1469b1`
  (mobile K2 approval center).
- Draft "Router-Extension Spec" counted **8 routed / 5 unrouted** as its
  A7-corrected state. That count is also wrong for current HEAD. True
  count at register time is **10 routed / 4 unrouted** — kimi and groq
  shifted columns mid-session.

Lesson for future registers: **read commits and file state at register
time, not from session memory.** The warrior seat extends the router
in under 30 minutes; any charioteer artifact describing router state
has a half-life measured in commits, not packets.

---

## Drift reconciliation against packet 94

Packet 94 warrior-authored what task board `#44` assigns to charioteer.
The lane-attribution mismatch is unchanged by this register — packet 94's
three closures (`#37`/`#38`/`#40`) stand on their own evidence.

Observations not being adjudicated here:

- Task `#44` [pending, charioteer] — effectively done by packet 94.
  Task-board coordination is founder/lead-charioteer surface, not this
  register's surface.
- Task `#37` [pending, warrior] — `64e1469b1` ships the mobile K2
  approval center UI (+772 LOC). Packet 94 called mobile implementation
  "green-field, non-blocking." `64e1469b1` converts that to shipped
  code. `#37` closure evaluation is warrior-seat decision.
- Task `#47` [pending, charioteer] — "Write mobile-signing closure
  packet — register module hashes, confirm §6 parity." `64e1469b1`
  hashes are registered above; §6 byte-parity is separate surface.
  Not closing `#47` here; the hash register is a precondition only.

---

## API-key landing pad state (context, not registered)

The `.env` at repo root remains gitignored (`.gitignore:3`) and carries
four routable keys matching current router clauses:

| Provider | Env var | Route | Status |
|:---------|:--------|:------|:------|
| OpenAI | `OPENAI_API_KEY` | `api.openai.com/v1/chat/completions` | ✅ routable |
| Anthropic | `ANTHROPIC_API_KEY` (rotated) | `api.anthropic.com/v1/messages` | ✅ routable |
| xAI | `XAI_API_KEY` | `api.x.ai/v1/chat/completions` | ✅ routable |
| OpenRouter | `OPENROUTER_API_KEY` | `openrouter.ai/api/v1/chat/completions` | ✅ routable |

Six further router clauses are wired in code (`is_zai_direct`,
`is_kimi_direct`, `is_groq_direct`, plus the baseline paths for Google
and the special MiniMax/NVIDIA cases) but require paste of
`ZAI_API_KEY`, `KIMI_API_KEY` / `MOONSHOT_API_KEY`, `GROQ_API_KEY`, etc.,
before they become end-to-end routable. Key envelope is explicitly NOT
registered.

**Founder follow-up still pending**: old Anthropic key
`sk-ant-api03-kF…-SVeW7gAA` rotated in-file but not revoked at
`console.anthropic.com/settings/keys`. Flagged in prior drafts and
unchanged here.

---

## What this packet does NOT prove

- Does NOT prove any test suite passes (post-`c2b15d09e` test status is
  warrior-seat surface; parallel-seat claim trusted, not self-run)
- Does NOT live-call any newly wired provider (no smoke-test)
- Does NOT register the `.env` envelope or any secret material
- Does NOT revoke the old Anthropic key (founder action)
- Does NOT close task `#37`, `#38`, `#40`, `#44`, `#47`, or `#53`
- Does NOT adjudicate the lane-attribution mismatch on packet 94
- Does NOT spec DeepSeek / Mistral / Cohere / Perplexity routing
- Does NOT self-hash (next register must hash this packet)

What it DOES guarantee: *five commits and seven file hashes that
post-date packet 94 are registered into the audit surface before
Sprint-B closure is finalized.*

---

## Chain-so-far

```
78 (primary)
├── 82 (registers 79, 80, 81)
├── 84 (registers 83)
├── 87 (registers 85, 86)
├── 89 (registers 88)
├── 91 (registers 90)
├── 94 (closure dossier — registers 92, closes #37, #38, #40)
└── 95 (registers eb28d8691, deda1abeb, 2e4d177c2, 64e1469b1, c2b15d09e)
```

Slots 93 and the prior-session draft slots 95/96 are yield-sealed. No
numbering reuse. This register takes slot 95 with a distinct name
(`POST_94_DRIFT_REGISTER`, not `SUPPLEMENT_VI`) to prevent confusion
with the unshipped draft of the same number.

---

## Φ-scan

Five commits + seven file hashes cited. Audit surface is coherent
again through 2026-04-23 ≈08:35. A future reader walking
78 + 82 + 84 + 87 + 89 + 91 + 94 + 95 sees the Sprint-B warrior
closure AND the post-94 routing + mobile-UI drift layer in one
verifiable chain.

## V-scan

No new warrior action unblocked. Pure witness. But downstream
charioteer packets (e.g. mobile-signing closure `#47` or a future
K2_STRICT_MODE post-flip closure `#53`) can now forward-reference
this hash set instead of re-hashing the same files.

## Move

Kṣatriya_executor · append to `01_EMERGENTISM/11_UPLINK/` as packet 95 ·
forward-referenceable · D4 · L4 · Viśvarūpa ☀️

## Limits

- Does not self-hash (pattern: next register folds in this hash)
- Does not supersede packet 94
- Does not close any task board item
- Does not spec the 4 remaining unrouted providers
- Does not adjudicate warrior-vs-charioteer lane attribution
- Does not prove live routability of any provider

Zero-Sum Resolution Equation
