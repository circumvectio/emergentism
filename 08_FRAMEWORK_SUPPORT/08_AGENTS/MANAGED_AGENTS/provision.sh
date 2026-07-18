#!/usr/bin/env bash
# Offline wrapper only.  The prior direct `ant ... create` flow could duplicate
# resources and could not prove semantic parity with the tracked bundle.
set -euo pipefail
cd "$(dirname "$0")"
exec python3 provision.py "$@"
