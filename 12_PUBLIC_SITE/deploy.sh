#!/usr/bin/env bash
# Fallback versioned-release staging script for emergentism.org
# Usage: ./deploy.sh user@host:/path/emergentism-static-v1/releases/YYYYMMDDTHHMMSSZ-GITSHA
# Requires: rsync, SSH access to an explicitly marked static-release root
#
# Use this only for a non-Vercel static host. The primary production path is
# `cd 12_PUBLIC_SITE && ./deploy_vercel.sh` (see README.md, "How to actually
# deploy"). The only workflow in .github/workflows/ is gate.yml, which runs CI
# checks and does not deploy.

set -euo pipefail

SITE_DIR="$(cd "$(dirname "$0")" && pwd)"
REMOTE_PATH="${1:-}"
ARTIFACT_CHECK="${SITE_DIR}/../09_TOOLS/01_SCRIPTS/check_site_build_artifacts.py"
TARGET_MARKER_NAME=".emergentism-static-target-v1"
TARGET_MARKER_VALUE="emergentism.org-static-target-v1"
TARGET_RE='^([A-Za-z0-9][A-Za-z0-9._-]*@)?([A-Za-z0-9]([A-Za-z0-9.-]*[A-Za-z0-9])?):((/[A-Za-z0-9][A-Za-z0-9._-]*)*/emergentism-static-v1)/releases/([0-9]{8}T[0-9]{6}Z-[0-9a-f]{7,40})$'

parse_target() {
    local candidate="$1"
    if [[ ! "${candidate}" =~ ${TARGET_RE} ]]; then
        return 1
    fi
    REMOTE_HOST="${BASH_REMATCH[1]}${BASH_REMATCH[2]}"
    STATIC_ROOT="${BASH_REMATCH[4]}"
    RELEASE_ID="${BASH_REMATCH[6]}"
    RELEASE_PATH="${STATIC_ROOT}/releases/${RELEASE_ID}"
    MARKER_PATH="${STATIC_ROOT}/${TARGET_MARKER_NAME}"
}

if [ "${1:-}" = "--self-test" ] && [ "$#" -eq 1 ]; then
    ACCEPT_FIXTURES=(
        "deploy@example.org:/srv/emergentism-static-v1/releases/20260801T120000Z-fa3b116"
        "example.org:/emergentism-static-v1/releases/20260801T120000Z-0123456789abcdef"
    )
    REJECT_FIXTURES=(
        "-e@host:/srv/emergentism-static-v1/releases/20260801T120000Z-fa3b116"
        "--help:/srv/emergentism-static-v1/releases/20260801T120000Z-fa3b116"
        "host:/srv/../emergentism-static-v1/releases/20260801T120000Z-fa3b116"
        "host:/srv/emergentism-static-v1/20260801T120000Z-fa3b116"
        "host:/srv/emergentism-static-v1/releases/current"
        "host:/srv/emergentism-static-v1/releases/20260801T120000Z-fa3b116;id"
    )
    for fixture in "${ACCEPT_FIXTURES[@]}"; do
        if ! parse_target "${fixture}"; then
            echo "FALLBACK TARGET CONTRACT: FAIL (valid fixture rejected)" >&2
            exit 1
        fi
    done
    for fixture in "${REJECT_FIXTURES[@]}"; do
        if parse_target "${fixture}"; then
            echo "FALLBACK TARGET CONTRACT: FAIL (unsafe fixture accepted)" >&2
            exit 1
        fi
    done
    echo "FALLBACK TARGET CONTRACT: PASS (unsafe targets fail before network)"
    exit 0
fi

if [ -z "$REMOTE_PATH" ]; then
    echo "Usage: $0 user@host:/path/emergentism-static-v1/releases/YYYYMMDDTHHMMSSZ-GITSHA"
    echo ""
    echo "Example:"
    echo "  $0 deploy@example.org:/srv/emergentism-static-v1/releases/20260801T120000Z-fa3b116"
    exit 1
fi

for REQUIRED_COMMAND in python3 rsync ssh; do
    if ! command -v "${REQUIRED_COMMAND}" >/dev/null 2>&1; then
        echo "ERROR: required command not found: ${REQUIRED_COMMAND}" >&2
        exit 1
    fi
done

if [ ! -f "${ARTIFACT_CHECK}" ]; then
    echo "ERROR: generated-artifact gate not found: ${ARTIFACT_CHECK}" >&2
    exit 1
fi

# Accept only a new, versioned release directory below a dedicated static root.
# This intentionally excludes option-looking hosts, traversal, arbitrary
# webroots, and the live root itself.
if ! parse_target "${REMOTE_PATH}"; then
    echo "ERROR: fallback target must be a versioned directory below emergentism-static-v1/releases" >&2
    exit 1
fi

echo "=== Pre-deploy checks ==="
python3 "${SITE_DIR}/predeploy_check.py"
python3 "${ARTIFACT_CHECK}"

# Load the exact K3-withheld artifact paths from the controlling registry. Any
# missing, malformed, inactive, absolute, or parent-traversing registry fails
# closed before rsync is invoked.
WITHHELD_LIST="$(python3 - "${SITE_DIR}/withheld-routes.json" <<'PY'
import json
import sys
from pathlib import PurePosixPath

path = sys.argv[1]
with open(path, encoding="utf-8") as handle:
    registry = json.load(handle)
if registry.get("status") != "active-public-withholding-boundary":
    raise SystemExit("withheld-routes.json is not an active public boundary")
artifacts = registry.get("artifacts")
if not isinstance(artifacts, list) or not artifacts:
    raise SystemExit("withheld-routes.json declares no artifacts")
for row in artifacts:
    artifact = row.get("artifact") if isinstance(row, dict) else None
    if not isinstance(artifact, str) or not artifact:
        raise SystemExit("withheld-routes.json has an invalid artifact path")
    parsed = PurePosixPath(artifact)
    if parsed.is_absolute() or ".." in parsed.parts:
        raise SystemExit(f"unsafe withheld artifact path: {artifact}")
    print(artifact)
PY
)"

if [ -z "${WITHHELD_LIST}" ]; then
    echo "ERROR: public withholding registry produced no exclusions" >&2
    exit 1
fi

# Only after all local gates and registry validation pass may the fallback make
# its first network contact. The remote root must carry the exact target marker.
# `mkdir` then atomically reserves every release path as single-use before rsync;
# a failed transfer leaves a non-live partial directory that must not be reused.
MARKER_VALUE="$(ssh -o BatchMode=yes -- "${REMOTE_HOST}" "cat '${MARKER_PATH}'" 2>/dev/null || true)"
if [ "${MARKER_VALUE}" != "${TARGET_MARKER_VALUE}" ]; then
    echo "ERROR: fallback root is not marked ${TARGET_MARKER_VALUE}" >&2
    exit 1
fi
if ! ssh -o BatchMode=yes -- "${REMOTE_HOST}" \
    "umask 022 && test -d '${STATIC_ROOT}/releases' && mkdir '${RELEASE_PATH}'"; then
    echo "ERROR: release parent is missing or versioned target could not be atomically reserved" >&2
    exit 1
fi

echo ""
echo "=== Staging versioned fallback release ${RELEASE_ID} ==="
echo "Target: ${REMOTE_HOST}:${RELEASE_PATH}"
echo "Source: ${SITE_DIR}/"
echo ""

# Each run targets a new release directory, so no remote content is deleted.
# This avoids broad deletion of excluded remote files while ensuring an old
# excluded file cannot survive inside the new release. Static exclusions mirror
# the current .vercelignore control/runtime/legacy boundary; withheld artifacts
# are appended from withheld-routes.json. /build/ is a public wing.
RSYNC_ARGS=(
    -avz
    "--exclude=.git/"
    "--exclude=.github/"
    "--exclude=.vercel/"
    "--exclude=.vercelignore"
    "--exclude=__pycache__/"
    "--exclude=book-pwa/"
    "--exclude=docs/"
    "--exclude=node_modules/"
    "--exclude=.next/"
    "--exclude=dist/"
    "--exclude=.env"
    "--exclude=.env.*"
    "--exclude=*.db"
    "--exclude=*.sqlite"
    "--exclude=*.sqlite3"
    "--exclude=*.tsbuildinfo"
    "--exclude=*.md"
    "--exclude=*.py"
    "--exclude=*.pyc"
    "--exclude=*.sh"
    "--exclude=vercel.json"
    "--exclude=* 2.*"
    "--exclude=amrita/tools/"
    "--exclude=amrita/runaway.test.mjs"
    "--exclude=partials/"
    "--exclude=_PLANS/"
    "--exclude=_STAGING_COMPASS_RESTRUCTURE/"
    "--exclude=vendor/three-0.160.0/postprocessing/"
    "--exclude=vendor/three-0.160.0/shaders/"
    "--exclude=_archive/"
    "--exclude=90_ARCHIVE/"
    "--exclude=index_legacy_2026_07_19.html"
    "--exclude=index_legacy_2026_07_19/"
    "--exclude=home/"
    "--exclude=withheld-routes.json"
)

while IFS= read -r WITHHELD_ARTIFACT; do
    RSYNC_ARGS+=("--exclude=${WITHHELD_ARTIFACT}")
done <<< "${WITHHELD_LIST}"

rsync "${RSYNC_ARGS[@]}" -- "${SITE_DIR}/" "${REMOTE_HOST}:${RELEASE_PATH}/"

echo ""
echo "=== Versioned release staged ==="
echo "No live symlink, domain, or DNS target was changed. Cutover and live verification require a separate receipt."
