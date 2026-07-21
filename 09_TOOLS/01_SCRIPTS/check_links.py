#!/usr/bin/env python3
"""Validate local links in active, Git-tracked Emergentism Markdown.

The validator deliberately does not audit historical custody or the public-site
projection.  It reads the working-tree form of every active Markdown path in
the Git index, strips comments and code examples, and checks local relative
destinations.  Fragment checking is conservative: explicit HTML anchors and
ordinary Markdown heading slugs are checked, while unusual fragments are
reported as skipped rather than guessed.
"""

from __future__ import annotations

import argparse
import html
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit


AUDIT_DIR = PurePosixPath("11_UPLINK/50_AUDITS_AND_EXECUTIONS")
AUDIT_LIVE_FILES = frozenset(
    {
        "00_THE_RECORD_LEDGER.md",
        "README.md",
        "AGENTS.md",
        "CLAUDE.md",
    }
)
EXCLUDED_ROOTS = frozenset({"90_ARCHIVE", "91_COMPATIBILITY", "12_PUBLIC_SITE"})
IGNORED_SCHEMES = frozenset(
    {"data", "ftp", "http", "https", "irc", "javascript", "mailto", "tel"}
)

FENCE_RE = re.compile(r"^\s{0,3}(`{3,}|~{3,})")
HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
INLINE_CODE_RE = re.compile(r"(`+)(.+?)\1")
REFERENCE_RE = re.compile(r"^\s{0,3}\[[^\]]+\]:\s*(<[^>\n]+>|\S+)", re.MULTILINE)
HEADING_RE = re.compile(r"^\s{0,3}(#{1,6})\s+(.+?)\s*#*\s*$", re.MULTILINE)
EXPLICIT_ANCHOR_RE = re.compile(
    r"<(?:a\s+(?:[^>]*?\s)?(?:id|name)|[^>]+\sid)\s*=\s*['\"]([^'\"]+)['\"]",
    re.IGNORECASE,
)


@dataclass(frozen=True, order=True)
class Finding:
    kind: str
    source: str
    line: int
    target: str
    detail: str


def repo_root(start: Path) -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=start,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return Path(result.stdout.strip()).resolve()


def tracked_markdown(root: Path) -> list[PurePosixPath]:
    result = subprocess.run(
        ["git", "ls-files", "-z", "--", "*.md"],
        cwd=root,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    paths = {
        PurePosixPath(raw.decode("utf-8", errors="surrogateescape"))
        for raw in result.stdout.split(b"\0")
        if raw
    }
    # A path removed in the working tree is no longer an active document even
    # if its deletion has not yet been staged. Repository-status checks own
    # that condition; the link gate owns present, tracked Markdown only.
    return sorted(
        path
        for path in paths
        if not excluded(path) and root.joinpath(*path.parts).is_file()
    )


def excluded(path: PurePosixPath) -> bool:
    parts = path.parts
    if not parts:
        return True
    if parts[0] in EXCLUDED_ROOTS or "90_ARCHIVE" in parts:
        return True
    if parts[:2] == ("11_UPLINK", "60_SESSION_PACKETS"):
        return True
    try:
        relative = path.relative_to(AUDIT_DIR)
    except ValueError:
        return False
    return not (len(relative.parts) == 1 and relative.name in AUDIT_LIVE_FILES)


def without_code_or_comments(text: str) -> str:
    """Return text with line count preserved but code examples removed."""

    text = HTML_COMMENT_RE.sub(lambda match: "\n" * match.group(0).count("\n"), text)
    output: list[str] = []
    fence: str | None = None
    for line in text.splitlines(keepends=True):
        match = FENCE_RE.match(line)
        marker = match.group(1) if match else None
        if fence is None and marker:
            fence = marker[0]
            output.append("\n" if line.endswith("\n") else "")
            continue
        if fence is not None:
            if marker and marker[0] == fence:
                fence = None
            output.append("\n" if line.endswith("\n") else "")
            continue
        output.append(INLINE_CODE_RE.sub("", line))
    return "".join(output)


def inline_destinations(text: str) -> list[tuple[int, str]]:
    """Extract inline Markdown destinations with balanced parentheses."""

    destinations: list[tuple[int, str]] = []
    cursor = 0
    while True:
        opener = text.find("](", cursor)
        if opener < 0:
            break
        index = opener + 2
        while index < len(text) and text[index].isspace() and text[index] != "\n":
            index += 1
        start = index
        if index < len(text) and text[index] == "<":
            end = text.find(">", index + 1)
            if end >= 0 and "\n" not in text[index:end]:
                destination = text[index + 1 : end]
                close = text.find(")", end + 1)
                if close >= 0:
                    destinations.append((text.count("\n", 0, opener) + 1, destination))
                    cursor = close + 1
                    continue
        depth = 0
        escaped = False
        while index < len(text):
            char = text[index]
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == "(" and not char.isspace():
                depth += 1
            elif char == ")":
                if depth == 0:
                    break
                depth -= 1
            elif char.isspace() and depth == 0:
                break
            elif char == "\n":
                break
            index += 1
        destination = text[start:index].strip()
        if destination:
            destinations.append((text.count("\n", 0, opener) + 1, destination))
        close = text.find(")", index)
        cursor = close + 1 if close >= 0 else opener + 2
    return destinations


def destinations(text: str) -> list[tuple[int, str]]:
    found = inline_destinations(text)
    for match in REFERENCE_RE.finditer(text):
        target = match.group(1)
        if target.startswith("<") and target.endswith(">"):
            target = target[1:-1]
        found.append((text.count("\n", 0, match.start()) + 1, target))
    return sorted(set(found))


def heading_slug(raw: str) -> str:
    raw = re.sub(r"<[^>]+>", "", raw)
    raw = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", raw)
    raw = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", raw)
    raw = re.sub(r"[*_~]", "", raw)
    raw = html.unescape(raw).strip().lower()
    raw = re.sub(r"[^\w\- ]", "", raw, flags=re.UNICODE)
    return re.sub(r"\s+", "-", raw)


def anchors(path: Path) -> set[str]:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return set()
    values = {unquote(value).lower() for value in EXPLICIT_ANCHOR_RE.findall(text)}
    counts: dict[str, int] = {}
    for match in HEADING_RE.finditer(without_code_or_comments(text)):
        base = heading_slug(match.group(2))
        if not base:
            continue
        occurrence = counts.get(base, 0)
        counts[base] = occurrence + 1
        values.add(base if occurrence == 0 else f"{base}-{occurrence}")
    return values


def plain_fragment(fragment: str) -> bool:
    return bool(re.fullmatch(r"[A-Za-z0-9_%.-]+", fragment))


def looks_like_file_reference(path_text: str, candidate: Path, fragment: str) -> bool:
    """Reject tier markers and prose that merely resemble reference definitions."""

    if fragment or candidate.exists():
        return True
    return (
        "/" in path_text
        or "\\" in path_text
        or path_text.startswith(".")
        or bool(Path(path_text).suffix)
    )


def validate(root: Path) -> tuple[list[Finding], int, int, int]:
    findings: list[Finding] = []
    checked_links = 0
    skipped_fragments = 0
    files = tracked_markdown(root)
    anchor_cache: dict[Path, set[str]] = {}

    for relative in files:
        source = root.joinpath(*relative.parts)
        try:
            text = without_code_or_comments(source.read_text(encoding="utf-8"))
        except (OSError, UnicodeError) as error:
            findings.append(Finding("unreadable-source", str(relative), 0, "", str(error)))
            continue

        for line, raw_target in destinations(text):
            target = html.unescape(raw_target.strip()).replace("\\ ", " ")
            if not target or target.startswith("#"):
                # Same-document fragments are checked below using the source path.
                if not target.startswith("#"):
                    continue
            split = urlsplit(target)
            if split.scheme.lower() in IGNORED_SCHEMES or split.netloc:
                continue
            if split.path.startswith("/"):
                # Web-root and local absolute paths are outside this relative-link contract.
                continue
            path_text = unquote(split.path)
            fragment = unquote(split.fragment).lower()
            candidate = source if not path_text else (source.parent / path_text)
            if not looks_like_file_reference(path_text, candidate, fragment):
                continue
            resolved = candidate.resolve(strict=False)
            try:
                resolved.relative_to(root)
            except ValueError:
                findings.append(
                    Finding("outside-root", str(relative), line, raw_target, "relative path escapes repository")
                )
                checked_links += 1
                continue

            checked_links += 1
            if not resolved.exists():
                findings.append(
                    Finding("missing-target", str(relative), line, raw_target, "local path does not exist")
                )
                continue
            if fragment and resolved.is_file() and resolved.suffix.lower() == ".md":
                if not plain_fragment(split.fragment):
                    skipped_fragments += 1
                    continue
                known = anchor_cache.setdefault(resolved, anchors(resolved))
                if fragment not in known:
                    findings.append(
                        Finding("missing-fragment", str(relative), line, raw_target, f"anchor #{fragment} not found")
                    )

    return sorted(set(findings)), len(files), checked_links, skipped_fragments


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="path inside the Git repository")
    args = parser.parse_args(argv)

    root = repo_root(args.root.resolve())
    findings, file_count, link_count, skipped_fragments = validate(root)
    for finding in findings:
        location = f"{finding.source}:{finding.line}" if finding.line else finding.source
        print(f"{finding.kind}\t{location}\t{finding.target}\t{finding.detail}")
    print(
        "SUMMARY\t"
        f"files={file_count}\tlinks={link_count}\tbroken={len(findings)}\t"
        f"skipped_fragments={skipped_fragments}"
    )
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
