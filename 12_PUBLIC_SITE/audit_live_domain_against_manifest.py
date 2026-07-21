#!/usr/bin/env python3
"""Verify a deployed URL byte-for-byte against the pure release artifact."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import ssl
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlsplit
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "release-manifest.json"
FORBIDDEN = re.compile(
    r"(?i)(?<![A-Za-z0-9])(?:Skyzai|VMOSK(?:-A)?|K2|PRISM|DAV|DAC|Agentz|Menexus|Aureus|OFN|APU\.BOT|Circle\.news)(?![A-Za-z0-9])"
)
TEXT_TYPES = ("text/", "application/json", "application/javascript", "application/manifest+json", "application/xml")
RETIRED_ALWAYS = {
    "/book/", "/read/", "/papers/", "/canon/", "/amrita/", "/book-pwa/",
    "/90_ARCHIVE/pure_emergentism_boundary_2026_07_20/",
}


def request(base: str, path: str, timeout: float) -> tuple[int, dict[str, str], bytes, str]:
    url = urljoin(base.rstrip("/") + "/", path.lstrip("/"))
    req = Request(
        url,
        headers={
            "User-Agent": "Emergentism-release-audit/2.0",
            "Accept-Encoding": "identity",
        },
    )
    try:
        with urlopen(req, timeout=timeout, context=ssl.create_default_context()) as response:
            return (
                response.status,
                {k.lower(): v for k, v in response.headers.items()},
                response.read(),
                response.geturl(),
            )
    except HTTPError as exc:
        return exc.code, {k.lower(): v for k, v in exc.headers.items()}, exc.read(), exc.geturl()


def artifact_hash(release: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(p for p in release.rglob("*") if p.is_file() and p.name != "RELEASE_SHA256"):
        rel = path.relative_to(release).as_posix()
        digest.update(rel.encode("utf-8") + b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def expected_url_map(data: dict) -> dict[str, str]:
    mapping = {row["path"]: row["file"] for row in data["routes"]}
    for rel in data["rootFiles"] + data["assetFiles"] + ["RELEASE_SHA256"]:
        # Vercel is configured with trailingSlash=true. Extensionless root
        # artifacts therefore have a slash-canonical public URL.
        path = "/" + rel + ("/" if "." not in Path(rel).name else "")
        prior = mapping.setdefault(path, rel)
        if prior != rel:
            raise ValueError(f"URL collision {path}: {prior} versus {rel}")
    return mapping


def allowed_mimes(rel: str) -> tuple[str, ...]:
    suffix = Path(rel).suffix.lower()
    return {
        ".html": ("text/html",),
        ".css": ("text/css",),
        ".js": ("application/javascript", "text/javascript"),
        ".mjs": ("application/javascript", "text/javascript"),
        ".json": ("application/json", "text/plain"),
        ".webmanifest": ("application/manifest+json", "application/json"),
        ".xml": ("application/xml", "text/xml"),
        ".txt": ("text/plain",),
        ".png": ("image/png",),
        ".woff2": ("font/woff2", "application/font-woff2", "application/octet-stream"),
        "": ("text/plain", "application/octet-stream"),
    }.get(suffix, ("application/octet-stream",))


def retired_paths(data: dict) -> list[str]:
    """Derive retired top-level route families while never probing active roots."""
    paths = set(RETIRED_ALWAYS)
    active_heads = {
        row["path"].strip("/").split("/", 1)[0]
        for row in data["routes"]
        if row["path"].strip("/")
    }
    archive = ROOT / "90_ARCHIVE" / "pure_emergentism_boundary_2026_07_20"
    if archive.is_dir():
        for child in archive.iterdir():
            if child.name in active_heads or child.name in {"90_ARCHIVE", "_archive"}:
                continue
            paths.add("/" + child.name + ("/" if child.is_dir() else ""))
    return sorted(
        path
        for path in paths
        if path.strip("/").split("/", 1)[0] not in active_heads
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--release", default=".release")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--timeout", type=float, default=20.0)
    args = parser.parse_args()

    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    release = (ROOT / args.release).resolve()
    errors: list[str] = []
    checked = 0
    if not release.is_dir():
        print(f"FAIL: local release missing: {release}")
        return 1
    recorded = (release / "RELEASE_SHA256").read_text(encoding="ascii").strip()
    actual = artifact_hash(release)
    if recorded != actual:
        errors.append(f"local release hash mismatch: recorded={recorded} actual={actual}")
    local_manifest = json.loads((release / "release-manifest.json").read_text(encoding="utf-8"))
    if local_manifest != data:
        errors.append("local release manifest differs from source manifest")

    try:
        mapping = expected_url_map(data)
    except ValueError as exc:
        print(f"FAIL: {exc}")
        return 1

    body_hashes: dict[str, list[str]] = {}
    for path, rel in sorted(mapping.items()):
        expected_file = release / rel
        if not expected_file.is_file():
            errors.append(f"local expected file missing: {rel}")
            continue
        try:
            status, headers, body, final_url = request(args.base_url, path, args.timeout)
        except URLError as exc:
            errors.append(f"request failed {path}: {exc}")
            continue
        checked += 1
        if status != 200:
            errors.append(f"expected 200, got {status}: {path}")
            continue
        final_path = urlsplit(final_url).path
        if final_path != path:
            errors.append(f"unexpected redirect: {path} -> {final_path}")
        content_type = headers.get("content-type", "").split(";", 1)[0].strip().lower()
        if content_type not in allowed_mimes(rel):
            errors.append(f"wrong MIME {content_type or 'missing'} for {path} ({rel})")
        expected_body = expected_file.read_bytes()
        if body != expected_body:
            errors.append(
                f"artifact byte mismatch: {path} expected={hashlib.sha256(expected_body).hexdigest()} "
                f"actual={hashlib.sha256(body).hexdigest()}"
            )
        digest = hashlib.sha256(body).hexdigest()
        body_hashes.setdefault(digest, []).append(path)
        if content_type.startswith(TEXT_TYPES):
            text = body.decode("utf-8", errors="replace")
            if FORBIDDEN.search(text):
                errors.append(f"external-system leakage: {path}")

    # This catches a server that maps many declared routes to one clean body,
    # even if a future caller accidentally weakens the byte comparison above.
    for digest, paths in sorted(body_hashes.items()):
        if len(paths) > 1:
            expected_digests = {
                hashlib.sha256((release / mapping[path]).read_bytes()).hexdigest()
                for path in paths
            }
            if len(expected_digests) > 1:
                errors.append(f"distinct routes collapsed to one body {digest}: {paths}")

    try:
        root_status, root_headers, _, _ = request(args.base_url, "/", args.timeout)
    except URLError as exc:
        errors.append(f"root security-header probe failed: {exc}")
    else:
        if root_status == 200:
            for header in ("content-security-policy", "x-frame-options", "x-content-type-options"):
                if header not in root_headers:
                    errors.append(f"root response lacks security header: {header}")

    if args.strict:
        for path in retired_paths(data):
            try:
                status, _, _, final_url = request(args.base_url, path, args.timeout)
            except URLError as exc:
                errors.append(f"retired-path probe failed {path}: {exc}")
                continue
            checked += 1
            if status not in {404, 410}:
                errors.append(f"retired path remains public ({status}): {path} -> {final_url}")

    if errors:
        print(f"FAIL: live audit checks={checked} findings={len(errors)}")
        for error in errors:
            print(f" - {error}")
        return 1
    print(
        f"PASS: byte-identical live release checks={checked} routes={len(data['routes'])} "
        f"sha256={actual} strict={args.strict}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
