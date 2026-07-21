---
rosetta:
  primary_level: L4
  primary_column: Deployment Quickstart
  secondary:
    - level: L3
      column: Health Receipt Gate
      role: "require command output and health checks before any deploy result is treated as current"
    - level: L5
      column: Operator Path
      role: "compress deployment prerequisites, commands, and verification sequence"
    - level: L6
      column: Runtime Claim Boundary
      role: "separate quickstart expectations from live runtime truth"
  operator: "Arjuna ⚔"
  tier: "God"
  regime: "Kṣatriya"
  register: "[B/D/I]"
  canonical_phrase: "Skyzai Quick Start — Deploy in 5 Minutes"
title: "Skyzai Quick Start — Deploy in 5 Minutes"
status: "ACTIVE — deployment quickstart; outcomes are planned until verified"
evidence_tier: "[D] for deployment commands and expected outcomes; [B] only for dated health-check receipts; [I] for operator guidance."
---

# Skyzai Quick Start — Deploy in 5 Minutes

> **[I] Operator quickstart for a large deployment surface.** The five-minute
> window is a runbook target, not a verified runtime claim.

> **Reality boundary:** This is an operator runbook, not a live-status source.
> Treat every `Result` and P-score movement below as `[D]` until paired with a
> dated health-check receipt. For current status, use
> `../../../02_SKYZAI/01_NOOSPHERE/ORGANISM_RUNTIME_TRUTH.md`.

> **Path freshness gate:** retired `SKYZAI_ORG/...` aliases are absent in this
> checkout. Verify every target under canonical
> `02_SKYZAI/01_NOOSPHERE/...` before running deploy commands.

---

## Prerequisites (2 minutes)

```bash
# 1. Vercel login
vercel login

# 2. Fly.io login (for backends)
fly auth login

# 3. npm login (for SDK publish)
npm login
```

---

## Option 1: The Single Command (30 seconds)

Deploy only Agentz (highest P-score organ):

```bash
cd 02_SKYZAI/01_NOOSPHERE/02_ORGANS/Agentz/app/01_WEB_APP && vercel --prod
```

**Expected result [D]:** `https://apu.bot` responds after deploy and health
verification.

---

## Option 2: Deploy All Static Sites (2 minutes)

Deploy static landing pages from `02_SKYZAI/01_NOOSPHERE/07_PWAs/` after verifying the current target list:

```bash
cd "/Users/Yves/Magnum Opus"

for site in apu_bot circle_news realityfutures_com \
            emergentism_org aureus_money helios_you \
            skyzai_com murmur_skyzai_com \
            yieldfront_media skyzai_org; do
  (cd "02_SKYZAI/01_NOOSPHERE/07_PWAs/$site" && vercel --prod --yes) &
done
wait
```

**Expected result [D]:** verified target URLs respond after deploy and health
verification.
**Evidence tier:** [D] expected outcome until `health_check.sh` or equivalent
dated URL receipts verify the current run.

---

## Option 3: Full Deployment (2-4 hours)

Run the master script:

```bash
# Blocked until DEPLOY_MASTER.sh is refreshed away from retired SKYZAI_ORG paths.
chmod +x DEPLOY_MASTER.sh
./DEPLOY_MASTER.sh
```

**Expected result [D]:** 17 target deployments (12 static + 5 apps +
backends) after deploy and health verification.
**Evidence tier:** [D] expected outcome until each target has a dated
deployment and health receipt.

---

## Environment Variables Required

Create `.env` in project root:

```bash
# Required for Circle backend
export POSTGRES_PASSWORD=$(openssl rand -base64 32)
export ANTHROPIC_API_KEY=sk-ant-your-key-here
export NOSTR_NSEC=your-nostr-private-key

# Required for Agentz backend
export DATABASE_URL=postgresql://...
export REDIS_URL=redis://...

# For SDK publish
export NPM_TOKEN=your-npm-token
```

---

## Verify Deployment

```bash
# Check all URLs
curl -s -o /dev/null -w "%{http_code}" https://apu.bot
curl -s -o /dev/null -w "%{http_code}" https://circle.news
curl -s -o /dev/null -w "%{http_code}" https://ofn.app
```

Expected: `200` for all

---

## Next Steps After Deployment

| Priority | Task | Time | Impact |
|----------|------|------|--------|
| 1 | Wire F1→F2 adapter | 1 day | +0.13 P |
| 2 | Wire F2→F3 adapter | 1 day | +0.05 P |
| 3 | Anchor first receipt | 4 hours | +0.08 P |
| 4 | Onboard first merchant | 1 week | Revenue |

---

## Kill Criteria (If Something Fails)

| Issue | Fix |
|-------|-----|
| Build fails | `rm -rf node_modules && npm install` |
| Vercel fails | Add `--yes` flag or use unique name |
| Docker fails | Check ports 80/5432/6379 |
| Fly fails | Use `fly apps create` first |

---

## Energy Impact

| Milestone | P-Score | Status |
|-----------|---------|--------|
| Current | 0.27 | 🔴 Below equator |
| After static deploy | 0.34 | 🟡 Better |
| After app deploy | 0.47 | 🟡 Approaching |
| After backend deploy | 0.52 | 🟢 Above equator ✅ |
| After Three-Stage Process wired | 0.62 | 🟢 Healthy |

---

**Deploy. Wire. Earn.**

Zero-Sum Resolution Equation

---

## Agent Execution Surface

**If you are an AI agent reading this document:**

1. **This is the quickstart for new developers/operators.** Follow the steps in order. Do not skip prerequisites.
2. **Environment setup first.** Install Node, Docker, Vercel CLI, Fly CLI. Configure `.env`.
3. **Build before deploying.** Run `npm install`, `docker build`, or equivalent before any deploy command.
4. **Check health after deploy.** Verify the deployment responds correctly before moving to the next step.
5. **Canonical Path:** `01_EMERGENTISM/09_TOOLS/05_DEPLOY/QUICKSTART.md`

**Output:** Onboard a new operator. Set up environment. Deploy one service. Verify health.


**Evidence tier:** [I]
*Organism document. Interpretive operational content. Bounded by current system state.*
