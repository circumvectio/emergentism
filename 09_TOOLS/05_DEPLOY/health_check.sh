#!/bin/bash
# Skyzai Organism Health Check
# Verifies all services are running

set -e

# Derive repo root from this script's location. Override with MAGNUM_OPUS_ROOT env var if needed.
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SKYZAI_ROOT="${MAGNUM_OPUS_ROOT:-$( cd "$SCRIPT_DIR/../../.." && pwd )}"
cd "$SKYZAI_ROOT"
# Repaired 2026-05-23 per L3 audit Wave EM-2 H2 (was hardcoded /Users/Yves/Documents/...)

echo "=========================================="
echo "Skyzai ORGANISM HEALTH CHECK"
echo "=========================================="
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counters
PASS=0
FAIL=0
WARN=0

check_url() {
    local name=$1
    local url=$2
    local expected=${3:-200}
    
    echo -n "Checking $name ($url)... "
    
    STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$url" 2>/dev/null || echo "000")
    
    if [ "$STATUS" == "$expected" ]; then
        echo -e "${GREEN}✅ PASS${NC} ($STATUS)"
        ((PASS++))
    elif [ "$STATUS" == "000" ]; then
        echo -e "${RED}❌ FAIL${NC} (unreachable)"
        ((FAIL++))
    else
        echo -e "${YELLOW}⚠️  WARN${NC} ($STATUS)"
        ((WARN++))
    fi
}

check_docker() {
    local service=$1
    
    echo -n "Checking Docker service: $service... "
    
    if docker ps --format "{{.Names}}" | grep -q "$service"; then
        echo -e "${GREEN}✅ RUNNING${NC}"
        ((PASS++))
    else
        echo -e "${RED}❌ NOT RUNNING${NC}"
        ((FAIL++))
    fi
}

check_fly() {
    local app=$1
    
    echo -n "Checking Fly.io app: $app... "
    
    if fly status --app "$app" 2>/dev/null | grep -q "running"; then
        echo -e "${GREEN}✅ RUNNING${NC}"
        ((PASS++))
    else
        echo -e "${RED}❌ NOT RUNNING${NC}"
        ((FAIL++))
    fi
}

check_npm() {
    local package=$1
    
    echo -n "Checking npm package: $package... "
    
    if npm view "$package" version &>/dev/null; then
        VERSION=$(npm view "$package" version)
        echo -e "${GREEN}✅ PUBLISHED${NC} (v$VERSION)"
        ((PASS++))
    else
        echo -e "${RED}❌ NOT FOUND${NC}"
        ((FAIL++))
    fi
}

echo "=== P0: Static Landing Pages ==="
check_url "apu.bot" "https://apu.bot"
check_url "circle.news" "https://circle.news"
check_url "realityfutures.com" "https://realityfutures.com"
check_url "ofn.app" "https://ofn.app"
check_url "emergentism.org" "https://emergentism.org"
check_url "aureus.money" "https://aureus.money"
check_url "helios.you" "https://helios.you"
check_url "skyzai.com" "https://skyzai.com"
check_url "menexus.net" "https://menexus.net"
check_url "murmur.skyzai.com" "https://murmur.skyzai.com"
check_url "yieldfront.media" "https://yieldfront.media"
check_url "skyzai.org" "https://skyzai.org"

echo ""
echo "=== P1: Full Applications ==="
check_url "APU Web App" "https://apu.bot"
check_url "Circle Web" "https://circle.news"
check_url "ReFu Web" "https://realityfutures.com"
check_url "OFN Dashboard" "https://ofn.app"
check_url "Emergentism" "https://emergentism.org"

echo ""
echo "=== P2: Backend Services ==="
check_docker "circle-postgres"
check_docker "circle-redis"
check_docker "circle-api"
check_docker "circle-scheduler"
check_docker "circle-nginx"

echo ""
check_fly "apu-bot-backend"
check_fly "ofn-reference-api"
check_fly "ofn-receipt-engine"

echo ""
echo "=== P3: npm Packages ==="
check_npm "@ofn/receipt-sdk"

echo ""
echo "=== Trivium Loop ==="
echo -n "Checking F1→F2 adapter... "
if pgrep -f "circle_signal_adapter.py" > /dev/null; then
    echo -e "${GREEN}✅ RUNNING${NC}"
    ((PASS++))
else
    echo -e "${YELLOW}⚠️  NOT RUNNING${NC} (start with: python adapters/circle_signal_adapter.py continuous)"
    ((WARN++))
fi

echo -n "Checking F2→F3 adapter... "
if pgrep -f "refu_price_adapter.py" > /dev/null; then
    echo -e "${GREEN}✅ RUNNING${NC}"
    ((PASS++))
else
    echo -e "${YELLOW}⚠️  NOT RUNNING${NC} (start with: python adapters/refu_price_adapter.py continuous)"
    ((WARN++))
fi

echo ""
echo "=========================================="
echo "HEALTH CHECK SUMMARY"
echo "=========================================="
echo -e "${GREEN}✅ PASS: $PASS${NC}"
echo -e "${YELLOW}⚠️  WARN: $WARN${NC}"
echo -e "${RED}❌ FAIL: $FAIL${NC}"
echo ""

if [ $FAIL -eq 0 ]; then
    echo -e "${GREEN}Organism is healthy!${NC}"
    exit 0
else
    echo -e "${RED}Organism needs attention.${NC}"
    exit 1
fi
