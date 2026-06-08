#!/bin/bash
# Skyzai Environment Setup Script
# Sets up all required environment variables

set -e

# Derive repo root from this script's location (script lives at <repo>/01_EMERGENTISM/09_TOOLS/05_DEPLOY/)
# Override with MAGNUM_OPUS_ROOT env var if needed.
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SKYZAI_ROOT="${MAGNUM_OPUS_ROOT:-$( cd "$SCRIPT_DIR/../../.." && pwd )}"
cd "$SKYZAI_ROOT"
# Repaired 2026-05-23 per L3 audit Wave EM-2 H2 (was hardcoded /Users/Yves/Documents/...)

echo "=========================================="
echo "Skyzai Environment Setup"
echo "=========================================="
echo ""

# Check prerequisites
echo "Checking prerequisites..."

if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI not found. Install: npm i -g vercel"
    exit 1
fi

if ! command -v fly &> /dev/null; then
    echo "❌ Fly.io CLI not found. Install: curl -L https://fly.io/install.sh | sh"
    exit 1
fi

if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found. Install from docker.com"
    exit 1
fi

echo "✅ All prerequisites found"
echo ""

# Create master .env file
echo "Creating environment configuration..."

ENV_FILE=".env"
if [ -f "$ENV_FILE" ]; then
    echo "⚠️  .env already exists. Backing up to .env.backup"
    cp "$ENV_FILE" ".env.backup.$(date +%s)"
fi

# Generate secure passwords
POSTGRES_PASSWORD=$(openssl rand -base64 32)
REDIS_PASSWORD=$(openssl rand -base64 32)
JWT_SECRET=$(openssl rand -base64 64)

cat > "$ENV_FILE" << EOF
# ============================================
# Skyzai Environment Variables
# Generated: $(date)
# ============================================

# ============================================
# API KEYS (Fill these in)
# ============================================

# Anthropic API Key (required for Circle and APU)
# Get from: https://console.anthropic.com/
ANTHROPIC_API_KEY=sk-ant-your-key-here

# OpenAI API Key (optional, for fallback)
# Get from: https://platform.openai.com/
OPENAI_API_KEY=sk-your-key-here

# Nostr Private Key (required for Circle publishing)
# Generate with: nostr-keygen or use existing
NOSTR_NSEC=nsec-your-key-here

# npm Token (required for SDK publish)
# Get from: https://www.npmjs.com/settings/tokens
NPM_TOKEN=npm-your-token-here

# ============================================
# DATABASE (Auto-generated)
# ============================================

POSTGRES_PASSWORD=$POSTGRES_PASSWORD
POSTGRES_USER=skyzai
POSTGRES_DB=organism
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
DATABASE_URL=postgresql://skyzai:$POSTGRES_PASSWORD@localhost:5432/organism

REDIS_PASSWORD=$REDIS_PASSWORD
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_URL=redis://:$REDIS_PASSWORD@localhost:6379

# ============================================
# JWT & SECURITY (Auto-generated)
# ============================================

JWT_SECRET=$JWT_SECRET
JWT_EXPIRY=7d
ENCRYPTION_KEY=$(openssl rand -base64 32)

# ============================================
# EXTERNAL SERVICES
# ============================================

# Hedera (for settlement)
HEDERA_OPERATOR_ID=0.0.xxxxx
HEDERA_OPERATOR_KEY=your-private-key
HEDERA_NETWORK=testnet

# Arweave (for receipt anchoring)
ARWEAVE_KEY_FILE=/path/to/arweave-key.json

# ============================================
# DOMAIN CONFIGURATION
# ============================================

NEXT_PUBLIC_APP_URL=https://apu.bot
NEXT_PUBLIC_CIRCLE_URL=https://circle.news
NEXT_PUBLIC_REFU_URL=https://realityfutures.com
NEXT_PUBLIC_OFN_URL=https://ofn.app

# ============================================
# BACKEND URLs (for API rewrites)
# ============================================

APU_BACKEND_URL=https://apu-bot-backend.fly.dev
CIRCLE_API_URL=http://localhost:8000
OFN_API_URL=https://ofn-reference-api.fly.dev

# ============================================
# MONITORING
# ============================================

SENTRY_DSN=your-sentry-dsn
LOG_LEVEL=info
METRICS_ENABLED=true

EOF

echo "✅ Created .env file with secure passwords"
echo ""

# Create Circle backend .env
echo "Setting up Circle backend..."
CIRCLE_ENV="02_SKYZAI/01_NOOSPHERE/02_ORGANS/TheCircle/app/circle_platform_backend/03_BUILD/Source/.env"
mkdir -p "$(dirname "$CIRCLE_ENV")"

cat > "$CIRCLE_ENV" << EOF
POSTGRES_PASSWORD=$POSTGRES_PASSWORD
POSTGRES_USER=circle
POSTGRES_DB=circle_platform
ANTHROPIC_API_KEY=your-key-here
NOSTR_NSEC=your-nsec-here
EOF

echo "✅ Created Circle backend .env"
echo ""

# Create APU backend fly.toml secrets script
echo "Creating APU backend secrets script..."

cat > "setup_apu_secrets.sh" << 'EOF'
#!/bin/bash
# Run this after setting ANTHROPIC_API_KEY in .env

set -a
source .env
set +a

cd 02_SKYZAI/01_NOOSPHERE/02_ORGANS/Agentz/app/03_BACKEND

echo "Setting Fly.io secrets..."
fly secrets set \
    ANTHROPIC_API_KEY="$ANTHROPIC_API_KEY" \
    DATABASE_URL="$DATABASE_URL" \
    REDIS_URL="$REDIS_URL" \
    JWT_SECRET="$JWT_SECRET"

echo "✅ APU secrets configured"
EOF

chmod +x "setup_apu_secrets.sh"
echo "✅ Created setup_apu_secrets.sh"
echo ""

# Create npm auth script
echo "Creating npm auth script..."

cat > "setup_npm.sh" << 'EOF'
#!/bin/bash
# Run this to authenticate with npm

echo "Logging into npm..."
npm login

echo ""
echo "Verifying auth..."
npm whoami

echo "✅ npm authenticated"
EOF

chmod +x "setup_npm.sh"
echo "✅ Created setup_npm.sh"
echo ""

# Summary
echo "=========================================="
echo "SETUP COMPLETE"
echo "=========================================="
echo ""
echo "Files created:"
echo "  📄 .env — Master environment file"
echo "  📄 .env.backup.* — Backup of previous .env"
echo "  📄 setup_apu_secrets.sh — Configure APU backend secrets"
echo "  📄 setup_npm.sh — npm authentication"
echo ""
echo "NEXT STEPS:"
echo ""
echo "1. Edit .env with your real API keys:"
echo "   - ANTHROPIC_API_KEY (from console.anthropic.com)"
echo "   - NOSTR_NSEC (generate with nostr-keygen)"
echo "   - NPM_TOKEN (from npmjs.com/settings/tokens)"
echo ""
echo "2. Authenticate with services:"
echo "   vercel login"
echo "   fly auth login"
echo "   ./setup_npm.sh"
echo ""
echo "3. Configure APU backend:"
echo "   ./setup_apu_secrets.sh"
echo ""
echo "4. Deploy:"
echo "   ./DEPLOY_MASTER.sh"
echo ""
echo "⚠️  IMPORTANT: Keep .env secret! Never commit it."
echo ""
