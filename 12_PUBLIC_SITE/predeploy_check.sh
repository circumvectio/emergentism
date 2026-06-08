#!/usr/bin/env bash
# Pre-deploy supply-chain gate for 12_PUBLIC_SITE (security review, 2026-05-30).
#
# Checks performed:
#   1. No external http(s) resource references (security gate)
#   2. All internal hrefs resolve to existing files
#   3. No orphan pages (every public page has at least one inbound link)
#   4. Required assets present where referenced
#   5. Basic HTML well-formedness (DOCTYPE, html/head/body tags)
#   6. Evidence tier markers on doctrine pages
#
# Wire it into CI / the deploy step:  ./predeploy_check.sh
set -euo pipefail
cd "$(dirname "$0")"

# Run the comprehensive Python gate
python3 predeploy_check.py
