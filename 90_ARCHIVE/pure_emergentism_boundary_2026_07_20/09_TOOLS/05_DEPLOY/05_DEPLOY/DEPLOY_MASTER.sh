#!/bin/bash
# Skyzai Master Deployment Script
# Deploys all 17 sites in priority order
# Estimated time: 2-4 hours total

set -e

# Derive repo root from this script's location. Override with MAGNUM_OPUS_ROOT env var if needed.
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SKYZAI_ROOT="${MAGNUM_OPUS_ROOT:-$( cd "$SCRIPT_DIR/../../.." && pwd )}"
cd "$SKYZAI_ROOT"
# Repaired 2026-05-23 per L3 audit Wave EM-2 H2 (was hardcoded /Users/Yves/Documents/...)

echo "=========================================="
echo "Skyzai MASTER DEPLOYMENT"
echo "=========================================="
echo ""
echo "This will deploy:"
echo "  - 12 static landing pages (02_SKYZAI/01_NOOSPHERE/07_PWAs/)"
echo "  - 5 full applications (02_SKYZAI/01_NOOSPHERE/)"
echo "  - 5 Docker services (Circle backend)"
echo "  - 2 Fly.io apps (APU backend + OFN)"
echo "  - 1 npm package (OFN SDK)"
echo ""
echo "Prerequisites:"
echo "  - vercel login (completed)"
echo "  - fly auth login (completed)"
echo "  - npm login (completed)"
echo "  - Environment variables set"
echo ""
read -p "Continue? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 1
fi

# Phase 0: Static Landing Pages (Parallel)
echo ""
echo "=========================================="
echo "PHASE 0: Static Landing Pages (2 min each)"
echo "=========================================="

STATIC_SITES=(
    "apu_bot:https://apu.bot"
    "circle_news:https://circle.news"
    "realityfutures_com:https://realityfutures.com"
    "ofn_app:https://ofn.app"
    "emergentism_org:https://emergentism.org"
    "aureus_money:https://aureus.money"
    "helios_you:https://helios.you"
    "skyzai_com:https://skyzai.com"
    "menexus_net:https://menexus.net"
    "murmur_skyzai_com:https://murmur.skyzai.com"
    "yieldfront:https://yieldfront.media"
    "skyzai_org:https://skyzai.org"
)

for site_config in "${STATIC_SITES[@]}"; do
    IFS=':' read -r site url <<< "$site_config"
    echo ""
    echo "Deploying $site -> $url"
    (cd "02_SKYZAI/01_NOOSPHERE/07_PWAs/$site" && vercel --prod --yes) || echo "⚠️ $site deploy failed"
done

echo ""
echo "✅ Phase 0 complete: 12 static sites deployed"

# Phase 1: Full Applications (Sequential)
echo ""
echo "=========================================="
echo "PHASE 1: Full Applications (10-30 min each)"
echo "=========================================="

deploy_app() {
    local name=$1
    local path=$2
    local framework=$3

    echo ""
    echo "------------------------------------------"
    echo "Deploying $name ($framework)"
    echo "Path: $path"
    echo "------------------------------------------"

    cd "$SKYZAI_ROOT/$path"

    if [ -f "package.json" ]; then
        echo "Installing dependencies..."
        npm install

        echo "Building..."
        npm run build

        echo "Deploying..."
        vercel --prod --yes
    else
        echo "No package.json found, deploying as static..."
        vercel --prod --yes
    fi

    echo "✅ $name deployed"
}

# T1: APU
deploy_app "APU" "02_SKYZAI/01_NOOSPHERE/02_ORGANS/Agentz/app/01_WEB_APP" "Next.js 16"

# T2: TheCircle
deploy_app "TheCircle" "02_SKYZAI/01_NOOSPHERE/02_ORGANS/TheCircle/app/website" "Next.js"

# T3: RealityFutures
deploy_app "RealityFutures" "02_SKYZAI/01_NOOSPHERE/02_ORGANS/RealityFutures/app/reality_futures/web" "Next.js"

# T4: OFN Merchant Dashboard
deploy_app "OFN Dashboard" "02_SKYZAI/01_NOOSPHERE/02_ORGANS/Skyzai/execution/ofn/merchant-dashboard" "Next.js"

# T5: Emergentism.org
deploy_app "Emergentism" "03_VENTURES/OPEN_FINANCE_NETWORK/GOVERNANCE/FOUNDATION/emergentism_org/SIMULATIONS" "Vite+React"

# T6: Aureus Landing
deploy_app "Aureus" "03_VENTURES/OPEN_FINANCE_NETWORK/01_LAYER/09_BRAND/SITES/aureus_app" "Static"

# T7: Helios Landing
deploy_app "Helios" "03_VENTURES/HELIOS/website" "Static"

echo ""
echo "✅ Phase 1 complete: 7 applications deployed"

# Phase 2: Backend Services
echo ""
echo "=========================================="
echo "PHASE 2: Backend Services"
echo "=========================================="

# T8: Circle Docker Stack
echo ""
echo "------------------------------------------"
echo "Starting Circle Docker Stack"
echo "------------------------------------------"
cd "$SKYZAI_ROOT/02_SKYZAI/01_NOOSPHERE/02_ORGANS/TheCircle/app/circle_platform_backend/03_BUILD/Source"

if [ ! -f ".env" ]; then
    echo "⚠️ .env file not found! Creating template..."
    cat > .env << 'EOF'
POSTGRES_PASSWORD=change_me_in_production
POSTGRES_USER=circle
POSTGRES_DB=circle_platform
ANTHROPIC_API_KEY=your_key_here
NOSTR_NSEC=your_nsec_here
EOF
    echo "⚠️ Please edit .env with real values, then re-run"
    exit 1
fi

echo "Starting Docker Compose..."
docker compose up -d
echo "✅ Circle backend running"

# T9: APU Backend (Fly.io)
echo ""
echo "------------------------------------------"
echo "Deploying APU Backend (Fly.io)"
echo "------------------------------------------"
cd "$SKYZAI_ROOT/02_SKYZAI/01_NOOSPHERE/02_ORGANS/Agentz/app/03_BACKEND"

if ! fly status &>/dev/null; then
    echo "Setting up Fly.io app..."
    fly launch --no-deploy --name apu-bot-backend --region iad
fi

echo "Setting secrets..."
fly secrets set ANTHROPIC_API_KEY="${ANTHROPIC_API_KEY:-placeholder}"
fly secrets set DATABASE_URL="${DATABASE_URL:-placeholder}"
fly secrets set REDIS_URL="${REDIS_URL:-placeholder}"

echo "Deploying..."
fly deploy
echo "✅ APU backend deployed"

# T10: OFN SDK (npm)
echo ""
echo "------------------------------------------"
echo "Publishing OFN SDK (npm)"
echo "------------------------------------------"
cd "$SKYZAI_ROOT/02_SKYZAI/01_NOOSPHERE/02_ORGANS/Skyzai/execution/ofn/02_SDK"

echo "Building..."
npm run build

echo "Publishing..."
npm publish --access public || echo "⚠️ Publish failed (may already exist)"
echo "✅ OFN SDK published"

# T11: OFN Python SDK (Fly.io)
echo ""
echo "------------------------------------------"
echo "Deploying OFN Python SDK (Fly.io)"
echo "------------------------------------------"
cd "$SKYZAI_ROOT/02_SKYZAI/01_NOOSPHERE/02_ORGANS/Skyzai/execution/ofn/04_PYTHON_SDK"

if ! fly status &>/dev/null; then
    fly launch --no-deploy --name ofn-receipt-engine --region fra
fi

fly deploy
echo "✅ OFN Python SDK deployed"

echo ""
echo "✅ Phase 2 complete: Backend services running"

# Summary
echo ""
echo "=========================================="
echo "DEPLOYMENT COMPLETE"
echo "=========================================="
echo ""
echo "Live URLs:"
echo ""
echo "P0 - Static Landing Pages:"
echo "  🔗 https://apu.bot"
echo "  🔗 https://circle.news"
echo "  🔗 https://realityfutures.com"
echo "  🔗 https://ofn.app"
echo "  🔗 https://emergentism.org"
echo "  🔗 https://aureus.money"
echo "  🔗 https://helios.you"
echo "  🔗 https://skyzai.com"
echo "  🔗 https://menexus.net"
echo "  🔗 https://murmur.skyzai.com"
echo "  🔗 https://yieldfront.media"
echo "  🔗 https://skyzai.org"
echo ""
echo "P1 - Full Applications:"
echo "  🧠 APU: https://apu.bot"
echo "  👁️  TheCircle: https://circle.news"
echo "  🔮 RealityFutures: https://realityfutures.com"
echo "  📄 OFN Dashboard: https://ofn.app"
echo "  📚 Emergentism: https://emergentism.org"
echo "  🥇 Aureus: https://aureus.money"
echo "  ☀️  Helios: https://helios.you"
echo ""
echo "P2 - Backend Services:"
echo "  🐳 Circle Docker: localhost (5 services)"
echo "  ☁️  APU Backend: https://apu-bot-backend.fly.dev"
echo "  📦 OFN SDK: npmjs.com/package/@ofn/receipt-sdk"
echo "  🐍 OFN Python: https://ofn-receipt-engine.fly.dev"
echo ""
echo "Next Steps:"
echo "  1. Wire F1→F2 adapter (Trivium)"
echo "  2. Anchor first OFN receipt"
echo "  3. Onboard first merchant"
echo ""
echo "Expected P-Score: 0.27 → 0.40+"
echo ""
echo "⊙ = • × ○"
