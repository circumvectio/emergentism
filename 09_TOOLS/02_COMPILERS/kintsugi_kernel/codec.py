from __future__ import annotations

import hashlib
import json
from pathlib import Path, PurePosixPath
from typing import Any

from .diagnostics import KintsugiError


def canonical_json_bytes(value: Any) -> bytes:
    try:
        rendered = json.dumps(
            value, ensure_ascii=False, sort_keys=True,
            separators=(",", ":"), allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise KintsugiError("KIN-E-CANONICAL", "json", str(exc)) from None
    return (rendered + "\n").encode("utf-8")


def raw_hash(payload: bytes) -> str:
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def normalize_lf(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def text_hash(text: str) -> str:
    return "sha256-text-lf:" + hashlib.sha256(normalize_lf(text).encode("utf-8")).hexdigest()


def safe_repo_path(root: Path, relative: str) -> Path:
    if not relative or relative.startswith("/") or "\\" in relative:
        raise KintsugiError("KIN-E-PATH", relative or "<empty>", "path must be non-empty repository-relative POSIX")
    raw_parts = relative.split("/")
    if any(part in ("", ".", "..") for part in raw_parts):
        raise KintsugiError("KIN-E-PATH", relative, "path contains a forbidden segment")
    pure = PurePosixPath(relative)
    candidate = (root / Path(*pure.parts)).resolve(strict=False)
    try:
        candidate.relative_to(root.resolve(strict=True))
    except ValueError:
        raise KintsugiError("KIN-E-PATH", relative, "path escapes repository root") from None
    return candidate


def load_canonical_json(path: Path) -> object:
    try:
        payload = path.read_bytes()
    except OSError as exc:
        raise KintsugiError("KIN-E-IO", str(path), str(exc)) from None
    try:
        value = json.loads(payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        if isinstance(exc, json.JSONDecodeError):
            detail = f"line {exc.lineno} column {exc.colno}: {exc.msg}"
        else:
            detail = str(exc)
        raise KintsugiError("KIN-E-JSON", str(path), detail) from None
    if payload != canonical_json_bytes(value):
        raise KintsugiError("KIN-E-CANONICAL", str(path), "JSON bytes are not canonical")
    return value


load_canonical_value = load_canonical_json
