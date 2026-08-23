#!/usr/bin/env python3
"""Content-addressed, two-phase Vercel release contract for emergentism.org.

The contract deliberately separates three states:

``prepare``
    Freeze one clean, pushed Git commit into a non-Git stage, materialize the
    declared deploy boundary, and receipt every CLI-input path, mode, size, and
    SHA-256.
``stage``
    Deploy that exact stage with custom-domain assignment held, require a READY
    production artifact, and audit the deployment-specific URL.
``promote``
    Revalidate the receipt and artifact, promote explicitly, audit apex and
    ``www``, and restore the previous deployment if branded verification fails.

No command reads or copies ``.vercel/.env.production.local``.  The only Vercel
control file copied into the stage is the already-reviewed ``project.json``.
"""

from __future__ import annotations

import argparse
import contextlib
import fcntl
import hashlib
import io
import json
import os
import re
import secrets
import shutil
import stat
import subprocess
import sys
import tarfile
import tempfile
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any, Iterable
from urllib.parse import urlsplit

from predeploy_check import is_vercel_ignored, load_vercelignore_patterns


SCHEMA = "emergentism/VercelReleaseReceipt.v1"
PROJECT_PIN_ENV = "EMERGENTISM_VERCEL_PROJECT_ID_PIN"
ORG_PIN_ENV = "EMERGENTISM_VERCEL_ORG_ID_PIN"
ALLOW_EXTERNAL_ENV = "EMERGENTISM_ALLOW_UNAVAILABLE_EXTERNAL_SOURCES"
SITE_ROOT = Path(__file__).resolve().parent
REPO_ROOT = SITE_ROOT.parent
SITE_TREE = "12_PUBLIC_SITE"
TARGET_CHECK = SITE_ROOT / "deploy_target_contract.py"
LIVE_AUDIT = SITE_ROOT / "audit_live_domain_against_manifest.py"
PREDEPLOY_CHECK = SITE_ROOT / "predeploy_check.py"
ARTIFACT_CHECK = REPO_ROOT / "09_TOOLS" / "01_SCRIPTS" / "check_site_build_artifacts.py"
STAGE_PARENT = Path(tempfile.gettempdir()) / "emergentism-vercel-release-stages-v1"
PRODUCTION_HOSTS = ("https://emergentism.org/", "https://www.emergentism.org/")
CRITICAL_ARTIFACTS = {
    "": "index.html",
    "churn/": "churn/index.html",
    "amrita/": "amrita/index.html",
    "halahala/": "halahala/index.html",
    "record/churning/": "record/churning/index.html",
    "questions/": "questions/index.html",
    "churn/corpus.json": "churn/corpus.json",
    "churn/corpus.jsonl": "churn/corpus.jsonl",
    "sw.js": "sw.js",
}
FORBIDDEN_STAGE_PARTS = {
    ".env",
    ".env.local",
    ".env.production",
    ".env.production.local",
    "credentials.json",
    ".npmrc",
    ".pypirc",
    ".netrc",
    "id_rsa",
    "id_ed25519",
}
FORBIDDEN_STAGE_SUFFIXES = {".key", ".pem", ".p12", ".pfx"}
FORBIDDEN_CONTENT_MARKERS = (
    b"-----BEGIN PRIVATE KEY-----",
    b"-----BEGIN RSA PRIVATE KEY-----",
    b"VERCEL_TOKEN=",
    b"AWS_SECRET_ACCESS_KEY=",
    b"GITHUB_TOKEN=",
)


class ReleaseContractError(RuntimeError):
    """A fail-closed release-contract violation."""


class CommandTimeoutError(ReleaseContractError):
    """A command may still be running remotely after the local wait expired."""


def _redact(text: str) -> str:
    redacted = text
    for name, value in os.environ.items():
        upper = name.upper()
        if (
            len(value) >= 8
            and any(token in upper for token in ("TOKEN", "SECRET", "PASSWORD", "PRIVATE_KEY"))
        ):
            redacted = redacted.replace(value, f"<redacted:{name}>")
    redacted = re.sub(
        r"(?i)(authorization:\s*bearer\s+)[^\s]+",
        r"\1<redacted>",
        redacted,
    )
    return redacted


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _canonical_bytes(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _run(
    args: list[str],
    *,
    cwd: Path,
    timeout: float | None = None,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    try:
        process = subprocess.run(
            args,
            cwd=cwd,
            text=True,
            capture_output=True,
            check=False,
            timeout=timeout,
            env=env,
        )
    except subprocess.TimeoutExpired as exc:
        raise CommandTimeoutError(
            f"command timed out with remote state unresolved: {args[0]} "
            f"{args[1] if len(args) > 1 else ''}"
        ) from exc
    if process.returncode:
        detail = _redact((process.stderr or process.stdout).strip())
        if len(detail) > 2000:
            detail = detail[-2000:]
        suffix = f": {detail}" if detail else ""
        raise ReleaseContractError(
            f"command failed ({process.returncode}): {args[0]} {args[1] if len(args) > 1 else ''}{suffix}"
        )
    return process


@contextlib.contextmanager
def _exclusive_release_lock() -> Iterable[Path]:
    project_pin = _required_pin(PROJECT_PIN_ENV)
    org_pin = _required_pin(ORG_PIN_ENV)
    lock_key = _sha256_bytes(f"{project_pin}\0{org_pin}".encode("utf-8"))[:20]
    lock_path = Path(tempfile.gettempdir()) / f"emergentism-vercel-{lock_key}.lock"
    descriptor = os.open(lock_path, os.O_CREAT | os.O_RDWR, 0o600)
    try:
        try:
            fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise ReleaseContractError(
                f"another local release command owns the production lock: {lock_path}"
            ) from exc
        os.ftruncate(descriptor, 0)
        os.write(descriptor, f"pid={os.getpid()} at={_utc_now()}\n".encode("utf-8"))
        yield lock_path
    finally:
        try:
            fcntl.flock(descriptor, fcntl.LOCK_UN)
        finally:
            os.close(descriptor)


def _git(*args: str) -> str:
    return _run(["git", *args], cwd=REPO_ROOT).stdout.strip()


def _require_clean_pushed_commit() -> tuple[str, str, str]:
    dirty = _run(
        ["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"],
        cwd=REPO_ROOT,
    ).stdout
    if dirty:
        raise ReleaseContractError("Emergentism worktree is not clean; release refused")
    commit = _git("rev-parse", "HEAD")
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ReleaseContractError("HEAD is not a full Git commit")
    branch = _git("branch", "--show-current")
    if not branch:
        raise ReleaseContractError("detached HEAD release is not admitted by this wrapper")
    try:
        upstream = _git("rev-parse", "@{upstream}")
    except ReleaseContractError as exc:
        raise ReleaseContractError("release branch has no configured upstream") from exc
    if commit != upstream:
        raise ReleaseContractError("HEAD does not equal its upstream; push exact custody first")
    return commit, branch, upstream


def _vercel_version() -> str:
    output = _run(["vercel", "--version"], cwd=SITE_ROOT).stdout.strip()
    match = re.search(r"(\d+\.\d+\.\d+)", output)
    if not match:
        raise ReleaseContractError("could not resolve the Vercel CLI version")
    return match.group(1)


def _assert_external_receipt(path: Path) -> Path:
    resolved = path.expanduser().resolve()
    if resolved.is_relative_to(REPO_ROOT):
        raise ReleaseContractError("release receipt must live outside the repository")
    resolved.parent.mkdir(parents=True, exist_ok=True)
    return resolved


def _safe_member_path(name: str) -> PurePosixPath:
    path = PurePosixPath(name)
    if (
        not name
        or path.is_absolute()
        or any(part in {"", ".", ".."} for part in path.parts)
    ):
        raise ReleaseContractError(f"unsafe archive member path: {name!r}")
    return path


def _inspect_archive(archive_bytes: bytes) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with tarfile.open(fileobj=io.BytesIO(archive_bytes), mode="r:") as archive:
        for member in archive.getmembers():
            path = _safe_member_path(member.name.rstrip("/"))
            if member.isdir():
                continue
            if not member.isfile():
                raise ReleaseContractError(
                    f"stage archive contains non-regular member: {member.name}"
                )
            extracted = archive.extractfile(member)
            if extracted is None:
                raise ReleaseContractError(f"cannot read archive member: {member.name}")
            payload = extracted.read()
            rows.append(
                {
                    "path": path.as_posix(),
                    "mode": member.mode & 0o777,
                    "size": len(payload),
                    "sha256": _sha256_bytes(payload),
                }
            )
    rows.sort(key=lambda row: row["path"])
    if not rows:
        raise ReleaseContractError("Git archive contains zero regular files")
    paths = [row["path"] for row in rows]
    if len(paths) != len(set(paths)):
        raise ReleaseContractError("Git archive contains duplicate paths")
    return rows


def _extract_archive(archive_bytes: bytes, stage_dir: Path) -> None:
    with tarfile.open(fileobj=io.BytesIO(archive_bytes), mode="r:") as archive:
        for member in archive.getmembers():
            _safe_member_path(member.name.rstrip("/"))
            if not (member.isdir() or member.isfile()):
                raise ReleaseContractError(
                    f"stage archive contains non-regular member: {member.name}"
                )
        archive.extractall(stage_dir, filter="data")


def _git_archive_bytes(commit: str) -> bytes:
    archive = subprocess.run(
        ["git", "archive", "--format=tar", f"{commit}:{SITE_TREE}"],
        cwd=REPO_ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if archive.returncode:
        detail = _redact(archive.stderr.decode("utf-8", errors="replace").strip())
        raise ReleaseContractError(f"git archive failed: {detail[:1000]}")
    return archive.stdout


def _deployable_archive_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    patterns = load_vercelignore_patterns()
    if patterns is None:
        raise ReleaseContractError(".vercelignore is missing from the release source")
    result = [
        row
        for row in rows
        if row["path"] not in {".gitignore", ".vercelignore"}
        and not is_vercel_ignored(row["path"], patterns)
    ]
    if not result:
        raise ReleaseContractError("materialized deployment stage contains zero files")
    return result


def _materialize_deployable_stage(stage_dir: Path) -> list[dict[str, Any]]:
    patterns = load_vercelignore_patterns()
    if patterns is None:
        raise ReleaseContractError(".vercelignore is missing from the release source")
    for path in sorted(stage_dir.rglob("*"), reverse=True):
        rel = path.relative_to(stage_dir).as_posix()
        if path.is_file() and (
            rel in {".gitignore", ".vercelignore"}
            or is_vercel_ignored(rel, patterns)
        ):
            path.unlink()
        elif path.is_dir() and not any(path.iterdir()):
            path.rmdir()
    return _stage_rows(stage_dir)


def _assert_stage_location(stage_dir: Path) -> Path:
    resolved = stage_dir.resolve()
    parent = STAGE_PARENT.resolve()
    if resolved.parent != parent or not resolved.name.startswith("release-"):
        raise ReleaseContractError("release stage is outside the contract-owned stage root")
    return resolved


def _stage_rows(stage_dir: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in sorted(stage_dir.rglob("*")):
        rel = path.relative_to(stage_dir).as_posix()
        if rel == ".vercel" or rel.startswith(".vercel/"):
            continue
        mode = path.lstat().st_mode
        if stat.S_ISLNK(mode):
            raise ReleaseContractError(f"stage contains symlink: {rel}")
        if path.is_dir():
            continue
        if not stat.S_ISREG(mode):
            raise ReleaseContractError(f"stage contains non-regular path: {rel}")
        lowered = path.name.lower()
        if (
            lowered in FORBIDDEN_STAGE_PARTS
            or lowered.startswith(".env")
            or path.suffix.lower() in FORBIDDEN_STAGE_SUFFIXES
            or "credentials" in lowered
            or "service-account" in lowered
            or "service_account" in lowered
        ):
            raise ReleaseContractError(f"stage contains forbidden credential path: {rel}")
        payload = path.read_bytes()
        if any(marker in payload for marker in FORBIDDEN_CONTENT_MARKERS):
            raise ReleaseContractError(f"stage contains a private credential marker: {rel}")
        rows.append(
            {
                "path": rel,
                "mode": stat.S_IMODE(mode),
                "size": path.stat().st_size,
                "sha256": _sha256_file(path),
            }
        )
    return rows


def _verify_control_dir(stage_dir: Path, expected_sha256: str | None = None) -> str:
    control_dir = stage_dir / ".vercel"
    if not control_dir.is_dir() or control_dir.is_symlink():
        raise ReleaseContractError("release stage lacks a regular .vercel control directory")
    entries = sorted(
        path.relative_to(control_dir).as_posix() for path in control_dir.rglob("*")
    )
    if entries != ["project.json"]:
        raise ReleaseContractError(
            "release-stage .vercel control directory must contain only project.json"
        )
    link = control_dir / "project.json"
    if not link.is_file() or link.is_symlink():
        raise ReleaseContractError("release-stage Vercel link is not a regular file")
    digest = _sha256_file(link)
    if expected_sha256 is not None and digest != expected_sha256:
        raise ReleaseContractError("release-stage Vercel link drift")
    return digest


def _critical_hashes(stage_dir: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for route, rel in CRITICAL_ARTIFACTS.items():
        path = stage_dir / rel
        if not path.is_file() or path.is_symlink() or path.stat().st_size == 0:
            raise ReleaseContractError(f"missing or empty critical artifact: {rel}")
        result[route or "/"] = _sha256_file(path)
    return result


def _manifest_digest(rows: list[dict[str, Any]]) -> str:
    return _sha256_bytes(_canonical_bytes(rows))


def _receipt_payload(receipt: dict[str, Any]) -> dict[str, Any]:
    payload = dict(receipt)
    payload.pop("receipt_sha256", None)
    return payload


def _write_receipt(path: Path, receipt: dict[str, Any]) -> None:
    receipt = _receipt_payload(receipt)
    receipt["receipt_sha256"] = _sha256_bytes(_canonical_bytes(receipt))
    payload = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    temporary = path.with_name(f".{path.name}.tmp-{os.getpid()}")
    temporary.write_text(payload, encoding="utf-8")
    temporary.chmod(0o600)
    os.replace(temporary, path)


def _load_receipt(path: Path) -> dict[str, Any]:
    try:
        receipt = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ReleaseContractError(f"invalid release receipt: {exc}") from exc
    if not isinstance(receipt, dict) or receipt.get("schema") != SCHEMA:
        raise ReleaseContractError("release receipt schema mismatch")
    expected = receipt.get("receipt_sha256")
    actual = _sha256_bytes(_canonical_bytes(_receipt_payload(receipt)))
    if not isinstance(expected, str) or expected != actual:
        raise ReleaseContractError("release receipt integrity mismatch")
    return receipt


def _verify_stage(receipt: dict[str, Any]) -> Path:
    stage_value = receipt.get("stage_dir")
    if not isinstance(stage_value, str):
        raise ReleaseContractError("release receipt lacks a stage directory")
    stage_dir = _assert_stage_location(Path(stage_value))
    if not stage_dir.is_dir():
        raise ReleaseContractError("release stage is missing")
    if (stage_dir / ".git").exists():
        raise ReleaseContractError("release stage contains Git metadata")
    rows = _stage_rows(stage_dir)
    if rows != receipt.get("stage_manifest"):
        raise ReleaseContractError("release stage differs from the receipted full manifest")
    commit = receipt.get("commit")
    if not isinstance(commit, str) or not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ReleaseContractError("receipt lacks a valid source commit")
    archive_rows = _deployable_archive_rows(_inspect_archive(_git_archive_bytes(commit)))
    if rows != archive_rows:
        raise ReleaseContractError("release stage differs from the committed deployable tree")
    if len(rows) != receipt.get("stage_file_count"):
        raise ReleaseContractError("release stage file-count drift")
    if sum(row["size"] for row in rows) != receipt.get("stage_total_bytes"):
        raise ReleaseContractError("release stage byte-count drift")
    if _manifest_digest(rows) != receipt.get("stage_manifest_sha256"):
        raise ReleaseContractError("release stage manifest drift")
    if _critical_hashes(stage_dir) != receipt.get("critical_sha256"):
        raise ReleaseContractError("release stage critical-artifact drift")
    project_digest = _verify_control_dir(stage_dir, receipt.get("project_link_sha256"))
    current_link = SITE_ROOT / ".vercel" / "project.json"
    if not current_link.is_file() or current_link.is_symlink():
        raise ReleaseContractError("current Vercel project link is missing")
    if _sha256_file(current_link) != project_digest:
        raise ReleaseContractError("current and staged Vercel project links differ")
    _run(
        [
            sys.executable,
            str(TARGET_CHECK),
            "--vercel-link",
            str(stage_dir / ".vercel" / "project.json"),
        ],
        cwd=SITE_ROOT,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )
    return stage_dir


def _parse_json_object(text: str) -> dict[str, Any]:
    stripped = text.strip()
    try:
        value = json.loads(stripped)
    except json.JSONDecodeError:
        starts = [index for index, char in enumerate(stripped) if char == "{"]
        for start in reversed(starts):
            try:
                value = json.loads(stripped[start:])
                break
            except json.JSONDecodeError:
                continue
        else:
            raise ReleaseContractError("command did not return a JSON object")
    if not isinstance(value, dict):
        raise ReleaseContractError("command JSON is not an object")
    return value


def _required_pin(name: str) -> str:
    value = os.environ.get(name)
    if not value or value != value.strip():
        raise ReleaseContractError(f"required production pin is absent: {name}")
    return value


def _deployment_hostname(value: str, *, allow_bare: bool = True) -> str:
    candidate = value.strip()
    if allow_bare and "://" not in candidate:
        candidate = "https://" + candidate
    parsed = urlsplit(candidate)
    try:
        port = parsed.port
    except ValueError as exc:
        raise ReleaseContractError(f"invalid deployment URL: {value!r}") from exc
    hostname = (parsed.hostname or "").lower()
    if (
        parsed.scheme != "https"
        or not hostname.endswith(".vercel.app")
        or hostname == "vercel.app"
        or parsed.username is not None
        or parsed.password is not None
        or port is not None
        or parsed.path not in {"", "/"}
        or parsed.query
        or parsed.fragment
    ):
        raise ReleaseContractError(f"invalid deployment URL: {value!r}")
    return hostname


def _validate_deployment_api(
    deployment: dict[str, Any],
    deployment_id: str,
    *,
    require_held: bool,
    expected_url: str | None = None,
    expected_release_nonce: str | None = None,
) -> None:
    project_pin = _required_pin(PROJECT_PIN_ENV)
    org_pin = _required_pin(ORG_PIN_ENV)
    if deployment.get("id") != deployment_id:
        raise ReleaseContractError("Vercel deployment identity mismatch")
    if deployment.get("readyState") != "READY" or deployment.get("target") != "production":
        raise ReleaseContractError("Vercel deployment is not READY production")
    project_id = deployment.get("projectId") or (deployment.get("project") or {}).get("id")
    team = deployment.get("team")
    if team is not None and not isinstance(team, dict):
        raise ReleaseContractError("Vercel deployment team shape is malformed")
    team_id = (team or {}).get("id") or deployment.get("teamId")
    if project_id != project_pin or team_id != org_pin:
        raise ReleaseContractError("Vercel deployment target does not match the production pins")
    api_url = deployment.get("url")
    if not isinstance(api_url, str):
        raise ReleaseContractError("Vercel deployment API lacks a canonical URL")
    api_hostname = _deployment_hostname(api_url)
    if expected_url is not None and api_hostname != _deployment_hostname(expected_url):
        raise ReleaseContractError("deployment ID and audited URL do not identify one artifact")
    if expected_release_nonce is not None:
        metadata = deployment.get("meta")
        if not isinstance(metadata, dict) or metadata.get("emergentismRelease") != expected_release_nonce:
            raise ReleaseContractError("deployment does not carry the receipted release nonce")
    if require_held:
        aliases = deployment.get("alias", [])
        if not isinstance(aliases, list) or not all(
            isinstance(alias, str) for alias in aliases
        ):
            raise ReleaseContractError("Vercel deployment alias shape is malformed")
        normalized = {alias.removeprefix("https://").rstrip("/") for alias in aliases}
        if {"emergentism.org", "www.emergentism.org"} & normalized:
            raise ReleaseContractError("held deployment already owns a branded domain")


def _deployment_api(deployment_id: str) -> dict[str, Any]:
    process = _run(
        ["vercel", "api", f"/v13/deployments/{deployment_id}"],
        cwd=SITE_ROOT,
        timeout=60,
    )
    return _parse_json_object(process.stdout)


def _find_deployment_by_release_nonce(nonce: str) -> tuple[str, str] | None:
    if not re.fullmatch(r"[0-9a-f]{32}", nonce):
        raise ReleaseContractError("release nonce is malformed")
    process = _run(
        [
            "vercel",
            "list",
            "--meta",
            f"emergentismRelease={nonce}",
            "--format=json",
            "--yes",
        ],
        cwd=SITE_ROOT,
        timeout=60,
    )
    payload = _parse_json_object(process.stdout)
    deployments = payload.get("deployments")
    if not isinstance(deployments, list):
        raise ReleaseContractError("Vercel deployment-list shape is malformed")
    if not deployments:
        return None
    if len(deployments) != 1 or not isinstance(deployments[0], dict):
        raise ReleaseContractError("release nonce identifies an ambiguous deployment set")
    listed = deployments[0]
    url = listed.get("url")
    if not isinstance(url, str):
        raise ReleaseContractError("release-nonce deployment lacks a URL")
    hostname = _deployment_hostname(url)
    api = _deployment_api(hostname)
    deployment_id = api.get("id")
    if not isinstance(deployment_id, str) or not deployment_id.startswith("dpl_"):
        raise ReleaseContractError("release-nonce deployment lacks an identity")
    _validate_deployment_api(
        api,
        deployment_id,
        require_held=True,
        expected_url=hostname,
        expected_release_nonce=nonce,
    )
    return deployment_id, f"https://{hostname}"


def _current_production() -> tuple[str, str]:
    process = _run(
        ["vercel", "inspect", "https://emergentism.org", "--format=json"],
        cwd=SITE_ROOT,
        timeout=60,
    )
    payload = _parse_json_object(process.stdout)
    deployment_id = payload.get("id")
    url = payload.get("url")
    if (
        not isinstance(deployment_id, str)
        or not deployment_id.startswith("dpl_")
        or payload.get("readyState") != "READY"
        or not isinstance(url, str)
    ):
        raise ReleaseContractError("could not bind the current READY production deployment")
    _deployment_hostname(url)
    return deployment_id, url


def _wait_for_production(deployment_id: str, *, timeout: float = 90) -> tuple[str, str]:
    deadline = time.monotonic() + timeout
    last_seen = "unresolved"
    while time.monotonic() < deadline:
        try:
            current_id, current_url = _current_production()
        except ReleaseContractError as exc:
            last_seen = str(exc)
        else:
            last_seen = current_id
            if current_id == deployment_id:
                return current_id, current_url
        time.sleep(2)
    raise ReleaseContractError(
        f"production alias did not resolve to {deployment_id}; last observed {last_seen}"
    )


def _deploy_held(stage_dir: Path, release_nonce: str) -> tuple[str, str]:
    if not re.fullmatch(r"[0-9a-f]{32}", release_nonce):
        raise ReleaseContractError("release nonce is malformed")
    process = _run(
        [
            "vercel",
            "--prod",
            "--yes",
            "--skip-domain",
            "--meta",
            f"emergentismRelease={release_nonce}",
            "--format=json",
        ],
        cwd=stage_dir,
        timeout=600,
    )
    payload = _parse_json_object(process.stdout)
    deployment = payload.get("deployment")
    if payload.get("status") != "ok" or not isinstance(deployment, dict):
        raise ReleaseContractError("Vercel deploy result is not an ok deployment")
    deployment_id = deployment.get("id")
    url = deployment.get("url")
    if (
        not isinstance(deployment_id, str)
        or not deployment_id.startswith("dpl_")
        or deployment.get("readyState") != "READY"
        or deployment.get("target") != "production"
        or not isinstance(url, str)
    ):
        raise ReleaseContractError("Vercel deploy result lacks a READY production identity")
    _deployment_hostname(url, allow_bare=False)
    return deployment_id, url


def _strict_audit(base_url: str) -> str:
    process = _run(
        [
            sys.executable,
            str(LIVE_AUDIT),
            "--base-url",
            base_url,
            "--strict",
        ],
        cwd=SITE_ROOT,
        timeout=600,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )
    return _sha256_bytes((process.stdout + process.stderr).encode("utf-8"))


def _fetch(route_url: str) -> tuple[bytes, dict[str, str]]:
    requested_host = (urlsplit(route_url).hostname or "").lower()
    if not requested_host:
        raise ReleaseContractError(f"live route URL lacks a host: {route_url}")
    request = urllib.request.Request(
        route_url,
        headers={"User-Agent": "EmergentismReleaseAudit/1.0"},
    )
    try:
        with urllib.request.urlopen(request, timeout=45) as response:
            final_host = (urlsplit(response.geturl()).hostname or "").lower()
            if final_host != requested_host:
                raise ReleaseContractError(
                    f"live route crossed hosts: {requested_host} -> {final_host}"
                )
            if response.status != 200:
                raise ReleaseContractError(f"live route is not 200: {route_url}")
            return response.read(), {
                key.lower(): value for key, value in response.headers.items()
            }
    except urllib.error.URLError as exc:
        raise ReleaseContractError(f"live route fetch failed: {route_url}: {exc}") from exc


def _verify_critical_live(
    base_url: str,
    expected: dict[str, str],
    *,
    require_indexable_halahala: bool,
) -> dict[str, str]:
    if not base_url.endswith("/"):
        base_url += "/"
    observed: dict[str, str] = {}
    for route in CRITICAL_ARTIFACTS:
        label = route or "/"
        payload, headers = _fetch(base_url + route)
        digest = _sha256_bytes(payload)
        if expected.get(label) != digest:
            raise ReleaseContractError(f"live critical hash mismatch: {label}")
        observed[label] = digest
        if route == "halahala/" and require_indexable_halahala:
            robots = headers.get("x-robots-tag", "").lower()
            if "noindex" in robots:
                raise ReleaseContractError("custom-domain Halahala route is noindex")
    return observed


def _observe_critical_live(
    base_url: str, *, require_indexable_halahala: bool
) -> dict[str, str]:
    if not base_url.endswith("/"):
        base_url += "/"
    observed: dict[str, str] = {}
    for route in CRITICAL_ARTIFACTS:
        label = route or "/"
        payload, headers = _fetch(base_url + route)
        observed[label] = _sha256_bytes(payload)
        if route == "halahala/" and require_indexable_halahala:
            robots = headers.get("x-robots-tag", "").lower()
            if "noindex" in robots:
                raise ReleaseContractError("custom-domain Halahala route is noindex")
    return observed


def _require_production_identity(expected_id: str) -> tuple[str, str]:
    current_id, current_url = _current_production()
    if current_id != expected_id:
        raise ReleaseContractError(
            f"production compare-and-swap failed: expected {expected_id}, found {current_id}"
        )
    api = _deployment_api(current_id)
    _validate_deployment_api(
        api,
        current_id,
        require_held=False,
        expected_url=current_url,
    )
    return current_id, current_url


def _validate_phase(receipt: dict[str, Any], expected_state: str) -> tuple[str, Path]:
    if receipt.get("state") != expected_state:
        raise ReleaseContractError(
            f"release receipt state is {receipt.get('state')!r}, expected {expected_state!r}"
        )
    commit, _, upstream = _require_clean_pushed_commit()
    if commit != receipt.get("commit") or upstream != receipt.get("upstream_commit"):
        raise ReleaseContractError("release source custody changed after preparation")
    if _vercel_version() != receipt.get("vercel_cli_version"):
        raise ReleaseContractError("Vercel CLI version changed after preparation")
    return commit, _verify_stage(receipt)


def prepare(receipt_path: Path) -> dict[str, Any]:
    receipt_path = _assert_external_receipt(receipt_path)
    if receipt_path.exists():
        raise ReleaseContractError("release receipt already exists")
    commit, branch, upstream = _require_clean_pushed_commit()
    version = _vercel_version()
    gate_env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
    _run(
        [sys.executable, str(TARGET_CHECK), "--vercel-link", str(SITE_ROOT / ".vercel" / "project.json")],
        cwd=SITE_ROOT,
        env=gate_env,
    )
    predeploy_gate = _run(
        [sys.executable, "-B", str(PREDEPLOY_CHECK)],
        cwd=SITE_ROOT,
        timeout=900,
        env=gate_env,
    )
    artifact_gate = _run(
        [sys.executable, "-B", str(ARTIFACT_CHECK)],
        cwd=SITE_ROOT,
        timeout=900,
        env=gate_env,
    )
    after_commit, after_branch, after_upstream = _require_clean_pushed_commit()
    if (after_commit, after_branch, after_upstream) != (commit, branch, upstream):
        raise ReleaseContractError("source custody changed while local release gates ran")
    archive_bytes = _git_archive_bytes(commit)
    expected_rows = _deployable_archive_rows(_inspect_archive(archive_bytes))
    STAGE_PARENT.mkdir(mode=0o700, parents=True, exist_ok=True)
    STAGE_PARENT.chmod(0o700)
    stage_dir = Path(tempfile.mkdtemp(prefix="release-", dir=STAGE_PARENT))
    try:
        _extract_archive(archive_bytes, stage_dir)
        observed_rows = _materialize_deployable_stage(stage_dir)
        if expected_rows != observed_rows:
            raise ReleaseContractError(
                "materialized stage does not equal the committed deployable tree"
            )
        if len(observed_rows) < 100 or sum(row["size"] for row in observed_rows) < 100_000:
            raise ReleaseContractError("release stage is implausibly small")
        if (stage_dir / ".git").exists():
            raise ReleaseContractError("release stage contains Git metadata")
        control_dir = stage_dir / ".vercel"
        control_dir.mkdir(mode=0o700)
        link_source = SITE_ROOT / ".vercel" / "project.json"
        link_target = control_dir / "project.json"
        shutil.copyfile(link_source, link_target)
        _run(
            [
                sys.executable,
                str(TARGET_CHECK),
                "--vercel-link",
                str(link_target),
            ],
            cwd=SITE_ROOT,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )
        project_link_sha256 = _verify_control_dir(stage_dir)
        receipt = {
            "schema": SCHEMA,
            "state": "PREPARED",
            "prepared_at": _utc_now(),
            "commit": commit,
            "release_nonce": secrets.token_hex(16),
            "branch": branch,
            "upstream_commit": upstream,
            "stage_dir": str(stage_dir),
            "stage_file_count": len(observed_rows),
            "stage_total_bytes": sum(row["size"] for row in observed_rows),
            "stage_manifest": observed_rows,
            "stage_manifest_sha256": _manifest_digest(observed_rows),
            "stage_manifest_semantics": "materialized_cli_input_without_git_or_ignore_file_v1",
            "critical_sha256": _critical_hashes(stage_dir),
            "project_link_sha256": project_link_sha256,
            "vercel_cli_version": version,
            "predeploy_gate_sha256": _sha256_bytes(
                (predeploy_gate.stdout + predeploy_gate.stderr).encode("utf-8")
            ),
            "artifact_gate_sha256": _sha256_bytes(
                (artifact_gate.stdout + artifact_gate.stderr).encode("utf-8")
            ),
            "federation_replay_mode": (
                "metadata_only_explicit"
                if os.environ.get(ALLOW_EXTERNAL_ENV) == "1"
                else "exact_or_not_required"
            ),
            "external_validation": False,
            "may_sign": False,
            "may_authorize": False,
        }
        _write_receipt(receipt_path, receipt)
        return _load_receipt(receipt_path)
    except Exception:
        shutil.rmtree(stage_dir, ignore_errors=True)
        raise


def stage(receipt_path: Path) -> dict[str, Any]:
    receipt_path = _assert_external_receipt(receipt_path)
    receipt = _load_receipt(receipt_path)
    release_nonce = receipt.get("release_nonce")
    if not isinstance(release_nonce, str) or not re.fullmatch(r"[0-9a-f]{32}", release_nonce):
        raise ReleaseContractError("receipt lacks a valid release nonce")
    if receipt.get("state") == "PREPARED":
        _, stage_dir = _validate_phase(receipt, "PREPARED")
        previous_id, previous_url = _current_production()
        previous_api = _deployment_api(previous_id)
        _validate_deployment_api(
            previous_api,
            previous_id,
            require_held=False,
            expected_url=previous_url,
        )
        previous_hashes = {
            base_url: _observe_critical_live(
                base_url, require_indexable_halahala=True
            )
            for base_url in PRODUCTION_HOSTS
        }
        if len({_canonical_bytes(value) for value in previous_hashes.values()}) != 1:
            raise ReleaseContractError("apex and www do not serve one predecessor artifact")
        receipt.update(
            {
                "state": "STAGE_DISPATCHING",
                "stage_started_at": _utc_now(),
                "previous_deployment_id": previous_id,
                "previous_deployment_url": previous_url,
                "previous_branded_critical_sha256": previous_hashes,
            }
        )
        _write_receipt(receipt_path, receipt)
        deployment_id, deployment_url = _deploy_held(stage_dir, release_nonce)
        receipt.update(
            {
                "state": "STAGE_CREATED_UNVERIFIED",
                "deployment_id": deployment_id,
                "deployment_url": deployment_url,
            }
        )
        _write_receipt(receipt_path, receipt)
    elif receipt.get("state") == "STAGE_DISPATCHING":
        _, stage_dir = _validate_phase(receipt, "STAGE_DISPATCHING")
        recovered = _find_deployment_by_release_nonce(release_nonce)
        if recovered is None:
            raise ReleaseContractError(
                "stage dispatch has no matching deployment yet; no second deployment "
                "was sent. Re-run stage only to reconcile the same release nonce."
            )
        deployment_id, deployment_url = recovered
        receipt.update(
            {
                "state": "STAGE_CREATED_UNVERIFIED",
                "stage_recovered_at": _utc_now(),
                "deployment_id": deployment_id,
                "deployment_url": deployment_url,
            }
        )
        _write_receipt(receipt_path, receipt)
    elif receipt.get("state") == "STAGE_CREATED_UNVERIFIED":
        _, stage_dir = _validate_phase(receipt, "STAGE_CREATED_UNVERIFIED")
        deployment_id = receipt.get("deployment_id")
        deployment_url = receipt.get("deployment_url")
        if (
            not isinstance(deployment_id, str)
            or not deployment_id.startswith("dpl_")
            or not isinstance(deployment_url, str)
            or not deployment_url.startswith("https://")
        ):
            raise ReleaseContractError("unverified-stage receipt lacks a deployment identity")
    else:
        raise ReleaseContractError(
            f"release receipt state {receipt.get('state')!r} cannot enter stage"
        )
    api = _deployment_api(deployment_id)
    _validate_deployment_api(
        api,
        deployment_id,
        require_held=True,
        expected_url=deployment_url,
        expected_release_nonce=release_nonce,
    )
    _verify_stage(receipt)
    previous_id = receipt.get("previous_deployment_id")
    if not isinstance(previous_id, str) or not previous_id.startswith("dpl_"):
        raise ReleaseContractError("stage receipt lacks its predecessor deployment")
    _require_production_identity(previous_id)
    base_url = deployment_url if deployment_url.endswith("/") else deployment_url + "/"
    audit_sha = _strict_audit(base_url)
    live_sha = _verify_critical_live(
        base_url,
        receipt["critical_sha256"],
        require_indexable_halahala=False,
    )
    _require_production_identity(previous_id)
    receipt.update(
        {
            "state": "STAGED_VERIFIED",
            "staged_at": _utc_now(),
            "deployment_id": deployment_id,
            "deployment_url": deployment_url,
            "immutable_audit_sha256": audit_sha,
            "immutable_critical_sha256": live_sha,
            "held_verified_production_id": previous_id,
        }
    )
    _write_receipt(receipt_path, receipt)
    return _load_receipt(receipt_path)


def _promote(deployment_id: str) -> None:
    _run(
        ["vercel", "promote", deployment_id, "--yes"],
        cwd=SITE_ROOT,
        timeout=300,
    )


def _rollback(deployment_id: str) -> None:
    # `vercel rollback` is required for a deployment that was Current before;
    # a previously promoted deployment cannot be promoted a second time.
    _run(
        ["vercel", "rollback", deployment_id, "--yes"],
        cwd=SITE_ROOT,
        timeout=300,
    )


def _verified_rollback_hashes(receipt: dict[str, Any]) -> dict[str, dict[str, str]]:
    previous = receipt.get("previous_deployment_id")
    if not isinstance(previous, str) or not previous.startswith("dpl_"):
        raise ReleaseContractError("receipt lacks a rollback predecessor")
    _require_production_identity(previous)
    expected_previous = receipt.get("previous_branded_critical_sha256")
    if not isinstance(expected_previous, dict):
        raise ReleaseContractError(
            "receipt lacks predecessor critical hashes for rollback verification"
        )
    rollback_hashes: dict[str, dict[str, str]] = {}
    for base_url in PRODUCTION_HOSTS:
        expected_for_host = expected_previous.get(base_url)
        if not isinstance(expected_for_host, dict):
            raise ReleaseContractError(f"receipt lacks predecessor hashes for {base_url}")
        rollback_hashes[base_url] = _verify_critical_live(
            base_url,
            expected_for_host,
            require_indexable_halahala=True,
        )
    return rollback_hashes


def _reconcile_rollback(receipt_path: Path, receipt: dict[str, Any]) -> None:
    candidate = receipt.get("deployment_id")
    previous = receipt.get("previous_deployment_id")
    if (
        not isinstance(candidate, str)
        or not candidate.startswith("dpl_")
        or not isinstance(previous, str)
        or not previous.startswith("dpl_")
    ):
        raise ReleaseContractError("rollback receipt lacks candidate or predecessor identity")
    current, _ = _current_production()
    if current == candidate:
        try:
            _wait_for_production(previous, timeout=90)
        except ReleaseContractError as exc:
            receipt.update(
                {
                    "state": "ROLLBACK_INDETERMINATE",
                    "rollback_reconciled_at": _utc_now(),
                    "rollback_error": _redact(str(exc))[:1000],
                }
            )
            _write_receipt(receipt_path, receipt)
            raise ReleaseContractError(
                "rollback has not become observable; no rollback command was repeated"
            ) from exc
    elif current != previous:
        receipt.update(
            {
                "state": "ROLLBACK_BLOCKED_BY_CONCURRENT_PRODUCTION",
                "rollback_reconciled_at": _utc_now(),
                "rollback_error": f"unexpected current deployment: {current}",
            }
        )
        _write_receipt(receipt_path, receipt)
        raise ReleaseContractError(
            "rollback reconciliation found an unrelated current deployment"
        )
    rollback_hashes = _verified_rollback_hashes(receipt)
    receipt.update(
        {
            "state": "ROLLED_BACK_VERIFIED_AFTER_FAILED_PROMOTION",
            "rollback_verified_at": _utc_now(),
            "rollback_critical_sha256": rollback_hashes,
        }
    )
    _write_receipt(receipt_path, receipt)
    raise ReleaseContractError(
        "the failed candidate is not live; its predecessor rollback is verified"
    )


def promote(receipt_path: Path) -> dict[str, Any]:
    receipt_path = _assert_external_receipt(receipt_path)
    receipt = _load_receipt(receipt_path)
    state = receipt.get("state")
    reconciling_states = {
        "PROMOTION_DISPATCHING",
        "PROMOTION_INDETERMINATE",
        "PROMOTION_OBSERVED_UNVERIFIED",
    }
    rollback_states = {"ROLLBACK_DISPATCHING", "ROLLBACK_INDETERMINATE"}
    if (
        state != "STAGED_VERIFIED"
        and state not in reconciling_states
        and state not in rollback_states
    ):
        raise ReleaseContractError(
            f"release receipt state {state!r} cannot enter promotion"
        )
    _, stage_dir = _validate_phase(receipt, str(state))
    deployment_id = receipt.get("deployment_id")
    if not isinstance(deployment_id, str) or not deployment_id.startswith("dpl_"):
        raise ReleaseContractError("receipt lacks a staged deployment identity")
    release_nonce = receipt.get("release_nonce")
    if not isinstance(release_nonce, str) or not re.fullmatch(r"[0-9a-f]{32}", release_nonce):
        raise ReleaseContractError("receipt lacks a valid release nonce")
    api = _deployment_api(deployment_id)
    _validate_deployment_api(
        api,
        deployment_id,
        require_held=state == "STAGED_VERIFIED",
        expected_url=str(receipt.get("deployment_url", "")),
        expected_release_nonce=release_nonce,
    )
    immutable_url = str(receipt["deployment_url"])
    _strict_audit(immutable_url)
    _verify_critical_live(
        immutable_url,
        receipt["critical_sha256"],
        require_indexable_halahala=False,
    )
    _verify_stage(receipt)
    if state in rollback_states:
        _reconcile_rollback(receipt_path, receipt)
    if state == "STAGED_VERIFIED":
        previous = receipt.get("previous_deployment_id")
        if not isinstance(previous, str) or not previous.startswith("dpl_"):
            raise ReleaseContractError("staged receipt lacks a predecessor deployment")
        if receipt.get("held_verified_production_id") != previous:
            raise ReleaseContractError("held-stage predecessor evidence is incomplete")
        _require_production_identity(previous)
        receipt.update(
            {
                "state": "PROMOTION_DISPATCHING",
                "promotion_started_at": _utc_now(),
            }
        )
        _write_receipt(receipt_path, receipt)
        try:
            _require_production_identity(previous)
        except ReleaseContractError as exc:
            receipt.update(
                {
                    "state": "PROMOTION_ABORTED_PREDECESSOR_CHANGED",
                    "promotion_aborted_at": _utc_now(),
                    "promotion_abort_reason": _redact(str(exc))[:1000],
                }
            )
            _write_receipt(receipt_path, receipt)
            raise
        try:
            _promote(deployment_id)
        except CommandTimeoutError as exc:
            receipt.update(
                {
                    "state": "PROMOTION_INDETERMINATE",
                    "promotion_timeout_at": _utc_now(),
                    "promotion_timeout_reason": str(exc),
                }
            )
            _write_receipt(receipt_path, receipt)
            raise ReleaseContractError(
                "promotion timed out; receipt is PROMOTION_INDETERMINATE. "
                "Do not retry promotion blindly; rerun this command only to reconcile aliases."
            ) from exc
    try:
        _wait_for_production(deployment_id)
    except ReleaseContractError as exc:
        receipt.update(
            {
                "state": "PROMOTION_INDETERMINATE",
                "promotion_observation_at": _utc_now(),
                "promotion_observation_error": str(exc)[:1000],
            }
        )
        _write_receipt(receipt_path, receipt)
        raise ReleaseContractError(
            "promotion command returned but the branded alias has not been bound to "
            "the staged deployment; state remains indeterminate and no retry occurred"
        ) from exc
    receipt.update(
        {
            "state": "PROMOTION_OBSERVED_UNVERIFIED",
            "promotion_observed_at": _utc_now(),
        }
    )
    _write_receipt(receipt_path, receipt)
    try:
        branded_audits: dict[str, str] = {}
        branded_hashes: dict[str, dict[str, str]] = {}
        for base_url in PRODUCTION_HOSTS:
            branded_audits[base_url] = _strict_audit(base_url)
            branded_hashes[base_url] = _verify_critical_live(
                base_url,
                receipt["critical_sha256"],
                require_indexable_halahala=True,
            )
        _require_production_identity(deployment_id)
    except Exception as exc:
        previous = receipt.get("previous_deployment_id")
        if isinstance(previous, str) and previous.startswith("dpl_"):
            try:
                _require_production_identity(deployment_id)
            except ReleaseContractError as conflict:
                receipt.update(
                    {
                        "state": "ROLLBACK_BLOCKED_BY_CONCURRENT_PRODUCTION",
                        "rollback_at": _utc_now(),
                        "rollback_reason": _redact(str(exc))[:1000],
                        "rollback_error": _redact(str(conflict))[:1000],
                    }
                )
                _write_receipt(receipt_path, receipt)
                raise ReleaseContractError(
                    "branded verification failed but rollback was blocked because "
                    "production no longer points to the failed candidate"
                ) from exc
            receipt.update(
                {
                    "state": "ROLLBACK_DISPATCHING",
                    "rollback_started_at": _utc_now(),
                    "rollback_reason": _redact(str(exc))[:1000],
                }
            )
            _write_receipt(receipt_path, receipt)
            try:
                _rollback(previous)
            except Exception as rollback_exc:
                receipt.update(
                    {
                        "state": "ROLLBACK_INDETERMINATE",
                        "rollback_at": _utc_now(),
                        "rollback_error": _redact(str(rollback_exc))[:1000],
                    }
                )
                _write_receipt(receipt_path, receipt)
                raise ReleaseContractError(
                    f"branded verification failed and rollback is indeterminate: {rollback_exc}"
                ) from exc
            try:
                _wait_for_production(previous)
                rollback_hashes = _verified_rollback_hashes(receipt)
                receipt.update(
                    {
                        "state": "ROLLED_BACK_VERIFIED_AFTER_FAILED_PROMOTION",
                        "rollback_at": _utc_now(),
                        "rollback_critical_sha256": rollback_hashes,
                    }
                )
                _write_receipt(receipt_path, receipt)
            except Exception as rollback_exc:
                receipt.update(
                    {
                        "state": "ROLLBACK_INDETERMINATE",
                        "rollback_at": _utc_now(),
                        "rollback_error": _redact(str(rollback_exc))[:1000],
                    }
                )
                _write_receipt(receipt_path, receipt)
                raise ReleaseContractError(
                    f"branded verification failed and rollback also failed: {rollback_exc}"
                ) from exc
            raise ReleaseContractError(
                f"branded verification failed; predecessor rollback restored: {exc}"
            ) from exc
        raise ReleaseContractError(
            f"branded verification failed and no rollback identity was available: {exc}"
        ) from exc
    receipt.update(
        {
            "state": "PROMOTED_VERIFIED",
            "promoted_at": _utc_now(),
            "branded_audit_sha256": branded_audits,
            "branded_critical_sha256": branded_hashes,
            "external_validation": False,
        }
    )
    _write_receipt(receipt_path, receipt)
    try:
        shutil.rmtree(stage_dir)
    except OSError as exc:
        receipt["stage_cleanup_error"] = str(exc)[:1000]
    else:
        receipt["stage_removed_at"] = _utc_now()
    _write_receipt(receipt_path, receipt)
    return _load_receipt(receipt_path)


def self_test() -> None:
    safe_tar = io.BytesIO()
    with tarfile.open(fileobj=safe_tar, mode="w") as archive:
        payload = b"ok\n"
        info = tarfile.TarInfo("index.html")
        info.size = len(payload)
        info.mode = 0o644
        archive.addfile(info, io.BytesIO(payload))
    rows = _inspect_archive(safe_tar.getvalue())
    if rows != [
        {
            "path": "index.html",
            "mode": 0o644,
            "size": 3,
            "sha256": _sha256_bytes(b"ok\n"),
        }
    ]:
        raise AssertionError("safe archive manifest changed")
    hostile = io.BytesIO()
    with tarfile.open(fileobj=hostile, mode="w") as archive:
        info = tarfile.TarInfo("../escape")
        info.size = 1
        archive.addfile(info, io.BytesIO(b"x"))
    try:
        _inspect_archive(hostile.getvalue())
    except ReleaseContractError:
        pass
    else:
        raise AssertionError("archive traversal negative control was accepted")
    parsed = _parse_json_object('progress\n{"status":"ok"}')
    if parsed != {"status": "ok"}:
        raise AssertionError("mixed-output JSON parsing changed")
    with tempfile.TemporaryDirectory() as temporary:
        path = Path(temporary) / "receipt.json"
        _write_receipt(path, {"schema": SCHEMA, "state": "TEST"})
        _load_receipt(path)
        payload = json.loads(path.read_text(encoding="utf-8"))
        payload["state"] = "TAMPERED"
        path.write_text(json.dumps(payload), encoding="utf-8")
        try:
            _load_receipt(path)
        except ReleaseContractError:
            pass
        else:
            raise AssertionError("receipt tamper negative control was accepted")


def _summary(receipt_path: Path, receipt: dict[str, Any]) -> None:
    print(f"RELEASE RECEIPT: {receipt_path}")
    print(f"state: {receipt['state']}")
    print(f"commit: {receipt.get('commit', '-')}")
    if receipt.get("deployment_id"):
        print(f"deployment: {receipt['deployment_id']}")
        print(f"deployment_url: {receipt['deployment_url']}")


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    subparsers = parser.add_subparsers(dest="command")
    for command in ("prepare", "stage", "promote"):
        child = subparsers.add_parser(command)
        child.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args(list(argv) if argv is not None else None)
    if args.self_test:
        if args.command is not None:
            parser.error("--self-test cannot be combined with a release command")
        self_test()
        print("DEPLOY RELEASE CONTRACT: PASS")
        return 0
    if args.command is None:
        parser.error("a release command is required")
    try:
        with _exclusive_release_lock():
            if args.command == "prepare":
                receipt = prepare(args.receipt)
            elif args.command == "stage":
                receipt = stage(args.receipt)
            else:
                receipt = promote(args.receipt)
    except ReleaseContractError as exc:
        print(f"DEPLOY RELEASE CONTRACT: FAIL — {exc}", file=sys.stderr)
        return 2
    _summary(args.receipt.resolve(), receipt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
