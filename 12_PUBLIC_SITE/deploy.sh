#!/usr/bin/env bash
# Fallback rsync deployment script for emergentism.org
# Usage: ./deploy.sh [user@host:/path/to/webroot]
# Requires: rsync, SSH access to target host
#
# Use this only for a non-Vercel static host. The primary production path is
# .github/workflows/deploy_emergentism_org.yml once Vercel project secrets and
# domain cutover are configured.

set -euo pipefail

SITE_DIR="$(cd "$(dirname "$0")" && pwd)"
REMOTE_PATH="${1:-}"  # e.g. user@host:/var/www/emergentism.org

if [ -z "$REMOTE_PATH" ]; then
    echo "Usage: $0 [user@host:/path/to/webroot]"
    echo ""
    echo "Examples:"
    echo "  $0 deploy@myserver:/var/www/emergentism.org"
    echo "  $0 root@192.168.1.100:/usr/share/nginx/html"
    exit 1
fi

echo "=== Pre-deploy checks ==="
if command -v python3 &>/dev/null; then
    python3 "${SITE_DIR}/predeploy_check.py"
else
    echo "Warning: python3 not found, skipping predeploy gate"
fi

echo ""
echo "=== Deploying to ${REMOTE_PATH} ==="
echo "Source: ${SITE_DIR}/"
echo ""

# --delete removes files on remote that no longer exist locally.
# Exclusions mirror the Vercel publication boundary: route-card/source files,
# frozen app source, local runtime state, and deploy tooling are not public.
rsync -avz --delete \
    --exclude='.git/' \
    --exclude='.github/' \
    --exclude='.vercel/' \
    --exclude='.vercelignore' \
    --exclude='__pycache__/' \
    --exclude='book-pwa/' \
    --exclude='docs/' \
    --exclude='node_modules/' \
    --exclude='.next/' \
    --exclude='dist/' \
    --exclude='build/' \
    --exclude='.env' \
    --exclude='.env.*' \
    --exclude='*.db' \
    --exclude='*.sqlite' \
    --exclude='*.sqlite3' \
    --exclude='*.tsbuildinfo' \
    --exclude='*.md' \
    --exclude='*.py' \
    --exclude='*.pyc' \
    --exclude='*.sh' \
    --exclude='deploy.sh' \
    --exclude='vercel.json' \
    "${SITE_DIR}/" \
    "${REMOTE_PATH}/"

echo ""
echo "=== Deploy complete ==="
echo "Verify: curl -I https://www.emergentism.org"
