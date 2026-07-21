#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

python3 -B build_pwa.py --check
python3 -B build_atlas_index.py --check
python3 -B build_release.py
python3 -B predeploy_check.py --release .release

# Deployment is an explicit operator act. The returned deployment URL must be
# audited before promotion; branded-domain DNS is a separate external state.
vercel build --prod "$@"
vercel deploy --prebuilt --prod --skip-domain "$@"
