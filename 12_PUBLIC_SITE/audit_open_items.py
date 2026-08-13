#!/usr/bin/env python3
"""Re-measure the four open items from the 3e8c22ef audit."""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, ".")
from predeploy_check import load_vercelignore_patterns, is_vercel_ignored

SITE = Path(".").resolve()
patterns = load_vercelignore_patterns()


def deployable() -> list[str]:
    out: list[str] = []
    for path in SITE.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".html", ".htm"}:
            continue
        rel = path.relative_to(SITE).as_posix()
        if not is_vercel_ignored(rel, patterns):
            out.append(rel)
    return sorted(out)


def has_skip_link(text: str) -> bool:
    """Real skip link: <a ... class="skip" OR id="skip" OR text starts with 'skip'."""
    # Look for a skip-link class or a "skip" anchor
    return bool(
        re.search(r'class\s*=\s*["\'][^"\']*\bskip\b', text, re.I)
        or re.search(r'<a\b[^>]*href\s*=\s*["\']#main["\']', text, re.I)
        or re.search(r'<a\b[^>]*href\s*=\s*["\']#content["\']', text, re.I)
        or re.search(r"skip\s+to\s+(main|content|body|navigation)", text, re.I)
    )


def has_main_landmark(text: str) -> bool:
    """<main> element OR role='main'."""
    return bool(
        re.search(r"<main\b", text, re.I)
        or re.search(r'role\s*=\s*["\']main["\']', text, re.I)
    )


def has_id_main(text: str) -> bool:
    return bool(re.search(r'\bid\s*=\s*["\']main["\']', text))


def count_h1(text: str) -> int:
    return len(re.findall(r"<h1\b", text, re.I))


def first_two_h1s(text: str) -> tuple[str, str] | None:
    """Return (first, second) of h1 elements stripped to text, or None."""
    matches = re.findall(r"<h1\b[^>]*>(.*?)</h1>", text, re.I | re.S)
    if len(matches) < 2:
        return None

    def strip(s: str) -> str:
        s = re.sub(r"<[^>]+>", " ", s)
        s = re.sub(r"\s+", " ", s).strip()
        return s

    return (strip(matches[0]), strip(matches[1]))


def main():
    pages = deployable()
    print(f"deployable: {len(pages)}")

    no_skip = []
    no_main = []
    no_id_main = []
    has_skip_no_main = []  # has skip but no main landmark
    multi_h1 = []
    markdown_leak = []
    for rel in pages:
        p = SITE / rel
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        if not has_skip_link(text):
            no_skip.append(rel)
        if not has_main_landmark(text):
            no_main.append(rel)
        if not has_id_main(text):
            no_id_main.append(rel)
        if has_skip_link(text) and not has_main_landmark(text):
            has_skip_no_main.append(rel)
        h1 = count_h1(text)
        if h1 > 1:
            pair = first_two_h1s(text)
            if pair and pair[0] == pair[1]:
                multi_h1.append((rel, h1, pair[0]))
        if "**" in text:
            # count leaks
            leaks = re.findall(r"\*\*[^*\n]{1,200}\*\*", text)
            if leaks:
                markdown_leak.append((rel, len(leaks), leaks[0][:80]))

    print(f"\nno skip link: {len(no_skip)}")
    for r in no_skip[:30]:
        print(f"  {r}")
    if len(no_skip) > 30:
        print(f"  ... and {len(no_skip) - 30} more")

    print(f"\nno main landmark: {len(no_main)}")
    for r in no_main:
        print(f"  {r}")

    print(f"\nskip but no main: {len(has_skip_no_main)}")
    for r in has_skip_no_main:
        print(f"  {r}")

    print(f"\nno id='main': {len(no_id_main)}")
    print(f"  first 10: {no_id_main[:10]}")

    print(f"\nmulti h1 with identical text (first 10): {len(multi_h1)}")
    for r, n, t in multi_h1[:10]:
        print(f"  {r}  h1={n}  '{t[:60]}'")

    print(f"\nmarkdown ** leak (first 15): {len(markdown_leak)}")
    for r, n, sample in markdown_leak[:15]:
        print(f"  {r}  count={n}  sample='{sample}'")


if __name__ == "__main__":
    main()
