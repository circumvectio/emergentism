#!/usr/bin/env python3
"""Fix the library-shell chrome regression caused by close_out_a11y_v2.py.

The previous script added id="main" tabindex="-1" to <main class="library-shell">,
breaking the predeploy check for the exact marker '<main class="library-shell">'.
This script removes the id/tabindex from the main element and adds
<span id="main" tabindex="-1"> as the first child instead, which is the
canonical pattern for library-shell pages.

Idempotent.
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


def fix_library_shell(text: str) -> str:
    """If page has <main class="library-shell" id="main" tabindex="-1">, restore canonical form."""
    # 1. Remove id/tabindex from <main class="library-shell" ...>
    new_main = re.sub(
        r'<main class="library-shell"\s+id="main"\s+tabindex="-1">',
        '<main class="library-shell">',
        text,
        count=1,
    )
    if new_main == text:
        return text
    # 2. Add <span id="main" tabindex="-1"></span> as first child of the main
    #    if not already present
    if '<span id="main"' in new_main:
        return new_main
    new_main = re.sub(
        r'(<main class="library-shell">)',
        r'\1\n<span id="main" tabindex="-1"></span>',
        new_main,
        count=1,
    )
    return new_main


def main() -> int:
    fixed = 0
    for path in deployable_html():
        text = path.read_text(encoding="utf-8", errors="replace")
        new_text = fix_library_shell(text)
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")
            fixed += 1
    print(f"library-shell pages fixed: {fixed}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
