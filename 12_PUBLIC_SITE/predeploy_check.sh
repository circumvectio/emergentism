#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

python3 -B build_pwa.py --check
python3 -B build_atlas_index.py --check
python3 -B build_release.py
python3 -B predeploy_check.py --release .release
