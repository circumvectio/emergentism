#!/usr/bin/env python3
"""Re-establish the 2026-08-13 a11y close-out on the current public site state.

The prior close-out (commits 9432f0d9 and friends) was lost in a rebase.
This script applies the same patterns idempotently to the current state.

Closes:
- 71 pages missing skip link (was 0 after the 2026-08-13 close-out)
- 3 pages missing main landmark (riemann, egg, suda)

For each page:
- If <main> exists, add id="main" tabindex="-1" to it (library-shell pattern)
- If a <div role="main"> exists, add id="main" to it
- If neither, wrap body content in <main id="main">...</main>
- Add <a class="skip-to-content" href="#main">Skip to content</a>
  as first child of <body>, BEFORE any frozen-library-boundary aside.

Idempotent. Re-running is a no-op.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, ".")
from predeploy_check import load_vercelignore_patterns, is_vercel_ignored

SITE = Path(".").resolve()
patterns = load_vercelignore_patterns()

SKIP_LINK = '<a class="skip-to-content" href="#main">Skip to content</a>'


def deployable_html() -> list[Path]:
    out: list[Path] = []
    for path in sorted(SITE.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in {".html", ".htm"}:
            continue
        rel = path.relative_to(SITE).as_posix()
        if is_vercel_ignored(rel, patterns):
            continue
        out.append(path)
    return out


def has_skip(text: str) -> bool:
    return bool(
        re.search(r'class="skip-to-content"', text)
        or re.search(r'<a\b[^>]+href="#main"', text)
    )


def find_main(text: str) -> tuple[str, int, int] | None:
    """Find <main> or <div role="main">. Returns (tag, start, end)."""
    # <main...> ... </main>
    m = re.search(r"<main\b[^>]*>", text, re.I)
    if m:
        end = text.find("</main>", m.end(), re.I)
        if end >= 0:
            return ("main", m.start(), end + len("</main>"))
    m = re.search(r'<div\b[^>]+role="main"[^>]*>', text, re.I)
    if m:
        end = text.find("</div>", m.end(), re.I)
        if end >= 0:
            return ("div", m.start(), end + len("</div>"))
    return None


def add_skip_link(text: str) -> str:
    """Insert skip link as first child of <body>."""
    # Skip if already present
    if has_skip(text):
        return text
    # Find <body> opening
    m = re.search(r"<body\b[^>]*>", text, re.I)
    if not m:
        return text
    insert_pos = m.end()
    # If first thing in body is an aside (frozen-library-boundary), insert
    # BEFORE the aside; otherwise insert immediately after <body>.
    after = text[insert_pos:insert_pos + 4096]
    aside_m = re.search(r"^\s*<aside\b[^>]*>", after)
    if aside_m:
        insert_pos += aside_m.start()
    return text[:insert_pos] + SKIP_LINK + "\n" + text[insert_pos:]


def add_main_landmark(text: str) -> str:
    """Add id="main" tabindex="-1" to existing <main>, or id="main" to <div role="main">."""
    found = find_main(text)
    if found is None:
        return text
    tag, start, end = found
    snippet = text[start:end]
    if tag == "main":
        # <main class="library-shell"> -> <main class="library-shell" id="main" tabindex="-1">
        # Check if id already present
        if re.search(r'\bid="main"', snippet):
            return text
        # Find the closing > of the open tag
        m = re.match(r"<main\b([^>]*)>", snippet, re.I)
        if m is None:
            return text
        attrs = m.group(1)
        new_open = f'<main{attrs} id="main" tabindex="-1">'
        return text[:start] + new_open + snippet[m.end():] + text[end:]
    # <div role="main"> -> <div id="main" role="main">
    snippet = text[start:end]
    if re.search(r'\bid="main"', snippet):
        return text
    m = re.match(r'<div\b([^>]*)>', snippet, re.I)
    if m is None:
        return text
    attrs = m.group(1)
    new_open = f'<div{attrs} id="main">'
    return text[:start] + new_open + snippet[m.end():] + text[end:]


def wrap_in_main(text: str) -> str:
    """For pages with no main landmark, wrap body content in <main id="main">."""
    # Find <body> open and close
    m = re.search(r"<body\b[^>]*>", text, re.I)
    if not m:
        return text
    end = re.search(r"</body\s*>", text, re.I)
    if not end:
        return text
    body_start = m.end()
    body_end = end.start()
    return text[:body_start] + "\n<main id=\"main\">" + text[body_start:body_end] + "</main>\n" + text[body_end:]


def main() -> int:
    fixed_skip = 0
    fixed_main = 0
    for path in deployable_html():
        rel = path.relative_to(SITE).as_posix()
        text = path.read_text(encoding="utf-8", errors="replace")
        original = text

        # 1. Add skip link
        if not has_skip(text):
            text = add_skip_link(text)
            if text != original:
                fixed_skip += 1
                original = text

        # 2. Add main landmark
        found = find_main(text)
        if found is None:
            text = wrap_in_main(text)
            if text != original:
                fixed_main += 1
                original = text
        else:
            new_text = add_main_landmark(text)
            if new_text != text:
                text = new_text
                fixed_main += 1

        if text != path.read_text(encoding="utf-8", errors="replace"):
            path.write_text(text, encoding="utf-8")

    print(f"skip links added: {fixed_skip}")
    print(f"main landmarks added/wrapped: {fixed_main}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
