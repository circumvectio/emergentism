#!/usr/bin/env bash
# Primary production entrypoint. Network contact is split into held staging and
# explicit promotion; repository gates execute only the offline self-test.

set -euo pipefail

SITE_DIR="$(cd "$(dirname "$0")" && pwd)"
LINK_FILE="${SITE_DIR}/.vercel/project.json"
TARGET_CHECK="${SITE_DIR}/deploy_target_contract.py"
RELEASE_CHECK="${SITE_DIR}/deploy_release_contract.py"

if [ "$#" -eq 1 ] && [ "$1" = "--self-test" ]; then
    if ! command -v python3 >/dev/null 2>&1; then
        echo "ERROR: required command not found: python3" >&2
        exit 1
    fi
    python3 -B "${TARGET_CHECK}" --self-test
    exec python3 -B "${RELEASE_CHECK}" --self-test
fi
if [ "$#" -ne 3 ] || [ "$2" != "--receipt" ]; then
    echo "Usage: $0 {prepare|stage|promote} --receipt /absolute/outside-repo/receipt.json" >&2
    echo "       $0 --self-test" >&2
    exit 1
fi
COMMAND="$1"
RECEIPT="$3"
case "${COMMAND}" in
    prepare|stage|promote) ;;
    *)
        echo "ERROR: release command must be prepare, stage, or promote" >&2
        exit 1
        ;;
esac
case "${RECEIPT}" in
    /*) ;;
    *)
        echo "ERROR: release receipt path must be absolute" >&2
        exit 1
        ;;
esac

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
if [ ! -f "${RELEASE_CHECK}" ]; then
    echo "ERROR: release-state contract not found: ${RELEASE_CHECK}" >&2
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
# The Python contract performs `git archive` staging outside Git metadata,
# runs predeploy_check.py and check_site_build_artifacts.py even when called
# directly, proves the materialized CLI-input manifest and critical hashes,
# uses `--skip-domain`, audits the deployment-specific URL, and makes
# `vercel promote` a separate phase with verified previous-deployment rollback
# on branded verification failure.
exec python3 -B "${RELEASE_CHECK}" "${COMMAND}" --receipt "${RECEIPT}"
