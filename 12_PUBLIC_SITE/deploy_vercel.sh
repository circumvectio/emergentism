#!/usr/bin/env bash
# Primary production entrypoint. This script contacts Vercel when invoked.
# It is intentionally not run by repository gates.

set -euo pipefail

SITE_DIR="$(cd "$(dirname "$0")" && pwd)"
LINK_FILE="${SITE_DIR}/.vercel/project.json"
ARTIFACT_CHECK="${SITE_DIR}/../09_TOOLS/01_SCRIPTS/check_site_build_artifacts.py"
TARGET_CHECK="${SITE_DIR}/deploy_target_contract.py"

if [ "$#" -eq 1 ] && [ "$1" = "--self-test" ]; then
    if ! command -v python3 >/dev/null 2>&1; then
        echo "ERROR: required command not found: python3" >&2
        exit 1
    fi
    exec python3 -B "${TARGET_CHECK}" --self-test
fi
if [ "$#" -ne 0 ]; then
    echo "Usage: $0 [--self-test]" >&2
    exit 1
fi

# A clean checkout is not a linked production project. Refuse before invoking
# any network-capable CLI; never infer a project from account defaults.
if [ ! -f "${LINK_FILE}" ]; then
    echo "ERROR: missing .vercel/project.json; run an explicit reviewed project-link step first" >&2
    exit 1
fi

if ! command -v python3 >/dev/null 2>&1; then
    echo "ERROR: required command not found: python3" >&2
    exit 1
fi
if [ ! -f "${TARGET_CHECK}" ]; then
    echo "ERROR: production-target contract not found: ${TARGET_CHECK}" >&2
    exit 1
fi

# The ignored Vercel link is necessary but not sufficient: it must exactly
# match independently supplied production pins. Missing pins, a stale link, or
# a wrong project all fail before any network-capable command is invoked.
python3 -B "${TARGET_CHECK}" --vercel-link "${LINK_FILE}"

if ! command -v vercel >/dev/null 2>&1; then
    echo "ERROR: required command not found: vercel" >&2
    exit 1
fi
if [ ! -f "${ARTIFACT_CHECK}" ]; then
    echo "ERROR: generated-artifact gate not found: ${ARTIFACT_CHECK}" >&2
    exit 1
fi

python3 "${SITE_DIR}/predeploy_check.py"
python3 "${ARTIFACT_CHECK}"

cd "${SITE_DIR}"
exec vercel --prod --yes
