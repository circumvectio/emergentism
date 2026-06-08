---
rosetta:
  primary_level: L4
  primary_column: Deployment Runbook
  secondary:
    - level: L3
      column: Verification Receipts
      role: "require deploy, health, and log output before planned targets become current status"
    - level: L5
      column: Deployment Architecture
      role: "organize static sites, full apps, backend services, and adapters as a deployable topology"
    - level: L6
      column: Safety Boundary
      role: "keep secrets, runtime status, and public claims outside unverified runbook prose"
  operator: "Arjuna ⚔"
  tier: "God"
  regime: "Kṣatriya"
  register: "[B/D/I]"
  canonical_phrase: "Skyzai Deployment Guide"
title: "Skyzai Deployment Guide"
status: "ACTIVE — deployment runbook; not runtime-truth authority"
evidence_tier: "[D] for deployment commands and planned targets; [B] only for dated deploy/health receipts; [I] for topology guidance."
---

# Skyzai Deployment Guide

Deployment runbook for the Skyzai organism. This file describes how to deploy;
it is not a `[B]` live-target receipt. Route current status to
`../../../02_SKYZAI/01_NOOSPHERE/ORGANISM_RUNTIME_TRUTH.md`.

**Path freshness gate:** retired `SKYZAI_ORG/...` aliases are absent in this
checkout. Treat any copied command or script still using those paths as blocked
until refreshed to canonical `02_SKYZAI/...` routes and paired
with a dated health receipt.

---

## 📁 Deployment Scripts Overview

| Script | Purpose | Time | Command |
|--------|---------|------|---------|
| `setup_env.sh` | Configure environment variables | 5 min | `./setup_env.sh` |
| `DEPLOY_MASTER.sh` | Deploy all 17 sites | 2-4 hours | `./DEPLOY_MASTER.sh` |
| `health_check.sh` | Verify all services | 1 min | `./health_check.sh` |
| `QUICKSTART.md` | Quick reference guide | - | Read it |

---

## 🚀 Quick Start (5 Minutes)

### Step 1: Environment Setup

```bash
# Run setup script
./setup_env.sh

# Edit .env with your real API keys
nano .env
```

### Step 2: Authenticate

```bash
vercel login
fly auth login
./setup_npm.sh
```

### Step 3: Deploy

```bash
# Option A: Deploy everything (2-4 hours)
./DEPLOY_MASTER.sh

# Option B: Deploy just Agentz (5 minutes)
cd 02_SKYZAI/01_NOOSPHERE/02_ORGANS/Agentz/app/01_WEB_APP
vercel --prod
```

### Step 4: Verify

```bash
./health_check.sh
```

---

## 📊 Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Skyzai ORGANISM                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │  03_VENTURES/  │    │ 02_ORGANISM │    │   Adapters  │     │
│  │  SKYZAI/.../07_PWAs/   │    │             │    │             │     │
│  │  (Static)   │───▶│   (Full)    │◀───│  (Three-Stage Process)  │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              TRIVIUM LOOP (The Nervous System)       │   │
│  │                                                      │   │
│  │  ┌──────────┐    ┌──────────┐    ┌──────────┐      │   │
│  │  │TheCircle │───▶│RealityFu │───▶│Agentz│      │   │
│  │  │  (IS)    │F1  │  (COULD) │F2  │ (SHOULD) │      │   │
│  │  └──────────┘    └──────────┘    └────┬─────┘      │   │
│  │         ▲                               │           │   │
│  │         │F4                             │F3         │   │
│  │         └───────────────────────────────┘           │   │
│  │                      Skyzai (ACT)                   │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🌐 Deployment Targets

### `02_SKYZAI/01_NOOSPHERE/07_PWAs/` — Static Landing Pages

| Domain | Purpose | Deploy Time |
|--------|---------|-------------|
| apu.bot | APU product page | 2 min |
| circle.news | OSINT network | 2 min |
| realityfutures.com | Prediction markets | 2 min |
| ofn.app | Receipt protocol | 2 min |
| emergentism.org | Framework | 2 min |
| aureus.money | Gold tokenization | 2 min |
| helios.you | Hardware | 2 min |
| skyzai.com | Super app | 2 min |
| menexus.net | Legal entity | 2 min |
| murmur.skyzai.com | Collective fund | 2 min |
| yieldfront.media | Satire engine | 2 min |
| skyzai.org | Technical docs | 2 min |

**Total: 24 minutes**

### `02_SKYZAI/01_NOOSPHERE/` — Full Applications

| Application | Path | Framework | Deploy Time |
|-------------|------|-----------|-------------|
| Agentz Web | `ApuBot/app/01_WEB_APP/` | Next.js 16 | 30 min |
| Circle Web | `TheCircle/app/website/` | Next.js | 30 min |
| ReFu Web | `RealityFutures/app/reality_futures/web/` | Next.js | 30 min |
| OFN Dashboard | `Skyzai/execution/ofn/merchant-dashboard/` | Next.js | 20 min |
| Emergentism | `FOUNDATION/emergentism_org/SIMULATIONS/` | Vite+React | 30 min |

**Total: 2.5 hours**

### Backend Services

| Service | Platform | Deploy Time |
|---------|----------|-------------|
| Circle Backend | Docker Compose | 30 min |
| Agentz Backend | Fly.io | 20 min |
| OFN Python SDK | Fly.io | 15 min |
| OFN TypeScript SDK | npm | 5 min |

**Total: 1.5 hours**

---

## 🔗 Three-Stage Process Adapters

The adapters wire the organism together:

### F1→F2: Circle → RealityFutures

**File:** `RealityFutures/adapters/circle_signal_adapter.py`

Converts Circle observations into prediction markets:
- Filters signals by confidence (> 0.70)
- Creates markets for high-confidence observations
- Runs continuously

```bash
# Run once
python adapters/circle_signal_adapter.py

# Run continuously
python adapters/circle_signal_adapter.py continuous
```

### F2→F3: RealityFutures → Agentz

**File:** `ApuBot/adapters/refu_price_adapter.py`

Streams market prices to Agentz Council:
- [I] Filters by volume (> $1000)
- Transforms prices into Council inputs
- Feeds probabilities for deliberation

```bash
# Run once
python adapters/refu_price_adapter.py

# Run continuously
python adapters/refu_price_adapter.py continuous
```

---

## ✅ Post-Deployment Checklist

### Immediate (Day 1)

- [ ] All 12 static sites return 200
- [ ] All 5 full apps return 200
- [ ] Docker services running
- [ ] Fly.io apps running
- [ ] npm package published

### Week 1

- [ ] F1→F2 adapter running
- [ ] F2→F3 adapter running
- [ ] First OFN receipt anchored
- [ ] Agentz Council receiving live data

### Month 1

- [ ] First merchant onboarded
- [ ] First revenue generated
- [ ] P-score > 0.50

---

## 🛠️ Troubleshooting

### Build Fails

```bash
rm -rf node_modules package-lock.json
npm install
npm run build
```

### Vercel Deploy Fails

```bash
# Use --yes to skip prompts
vercel --prod --yes

# Or use unique name
vercel --prod --name "apu-bot-$(date +%s)"
```

### Docker Fails

```bash
# Check ports
lsof -i :5432  # PostgreSQL
lsof -i :6379  # Redis
lsof -i :80    # Nginx

# Change ports in docker-compose.yml if needed
```

### Fly.io Fails

```bash
# Create app first
fly apps create --name my-app

# Then deploy
fly deploy
```

---

## 📈 Energy Impact

| Milestone | P-Score | Status |
|-----------|---------|--------|
| Current | 0.27 | 🔴 Below equator |
| Static deployed | 0.34 | 🟡 Better |
| Apps deployed | 0.47 | 🟡 Approaching |
| Backends deployed | 0.52 | 🟢 Above equator ✅ |
| Three-Stage Process wired | 0.62 | 🟢 Healthy |
| First revenue | 0.65 | 🟢 Sustainable |

---

## 🔐 Security

- [S] Do not commit `.env` files
- Use strong passwords (generated by `setup_env.sh`)
- Rotate API keys monthly
- Enable 2FA on all accounts

---

## 📚 Documentation

| Document | Content |
|----------|---------|
| `README.md` | Project overview |
| `QUICKSTART.md` | 5-minute quick start |
| `DEEP_AUDIT_REPORT_2026-04-12.md` | Comprehensive audit |
| `REAUDIT_REPORT_2026-04-12.md` | Updated findings |
| `DEPLOY_ALL_CHECKLIST.md` | Checklist format |

---

## 🆘 Support

If deployment fails:

1. Check `health_check.sh` output
2. Review logs: `vercel logs`, `fly logs`
3. Check `.env` configuration
4. Verify prerequisites are installed

---

**Deploy. Wire. Earn.**

Zero-Sum Resolution Equation

---

## Agent Execution Surface

**If you are an AI agent reading this document:**

1. **This is the canonical deployment runbook.** All deploy commands live here. Do not invent new deployment paths.
2. **Check prerequisites before deploying.** Node 20+, Docker, Vercel CLI, Fly CLI. Verify `.env` is configured.
3. **Deploy in order:** static sites first, then apps, then backends, then Three-Stage Process wiring.
4. **Verify after each deploy.** Run health checks. Check logs. Confirm the deployment is live.
5. **Canonical Path:** `01_EMERGENTISM/09_TOOLS/05_DEPLOY/README-DEPLOYMENT.md`

**Output:** Deploy using the commands listed here. Verify each. Report blockers.


**Evidence tier:** [I]
*Organism document. Interpretive operational content. Bounded by current system state.*
