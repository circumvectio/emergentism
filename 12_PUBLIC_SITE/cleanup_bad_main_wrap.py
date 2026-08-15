#!/usr/bin/env python3
"""Remove the bad <main id="main"> wrap introduced by close_out_a11y_v2.py.

The previous run added a wrapper <main id="main">...</main> around the
entire body, even when a real <main class="library-shell"> already
existed. The result is nested <main> elements. This script removes
the outer wrap and adds id="main" tabindex="-1" to the real main.

Idempotent: re-running is a no-op.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, ".")
from predeploy_check import load_vercelignore_patterns, is_vercel_ignored

SITE = Path(".").resolve()
patterns = load_vercelignore_patterns()


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


def is_bad_wrap(text: str) -> bool:
    """True if there's a <main id="main"> (no class) before another <main>."""
    mains = list(re.finditer(r"<main\b[^>]*>", text, re.I))
    if len(mains) < 2:
        return False
    first = mains[0].group()
    if not re.match(r'<main\s+id="main"\s*>', first):
        return False
    # Any later <main> means the first is the wrap
    return True


def remove_bad_wrap(text: str) -> str:
    """Remove the bare <main id="main"> wrap. The real main already exists."""
    # 1. Remove the opening <main id="main"> immediately after <body>
    text = re.sub(r"(<body\b[^>]*>)\s*<main\s+id=\"main\"\s*>", r"\1", text, count=1, flags=re.I)
    # 2. Remove the matching </main> right before </body>
    text = re.sub(r"</main\s*>(\s*</body\s*>)", r"\1", text, count=1, flags=re.I)
    return text


def has_skip(text: str) -> bool:
    return bool(
        re.search(r'class="skip-to-content"', text)
        or re.search(r'<a\b[^>]+href="#main"', text)
    )


def ensure_skip_link(text: str) -> str:
    """If skip link missing, add it as first child of body."""
    if has_skip(text):
        return text
    m = re.search(r"<body\b[^>]*>", text, re.I)
    if not m:
        return text
    insert_pos = m.end()
    after = text[insert_pos:insert_pos + 4096]
    aside_m = re.search(r"^\s*<aside\b[^>]*>", after)
    if aside_m:
        insert_pos += aside_m.start()
    skip = '<a class="skip-to-content" href="#main">Skip to content</a>'
    return text[:insert_pos] + skip + "\n" + text[insert_pos:]


def main() -> int:
    fixed_wrap = 0
    fixed_skip = 0
    for path in deployable_html():
        text = path.read_text(encoding="utf-8", errors="replace")
        original = text

        if is_bad_wrap(text):
            text = remove_bad_wrap(text)
            if text != original:
                fixed_wrap += 1
                original = text

        if not has_skip(text):
            text = ensure_skip_link(text)
            if text != original:
                fixed_skip += 1

        if text != path.read_text(encoding="utf-8", errors="replace"):
            path.write_text(text, encoding="utf-8")

    print(f"bad wraps removed: {fixed_wrap}")
    print(f"skip links added: {fixed_skip}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
