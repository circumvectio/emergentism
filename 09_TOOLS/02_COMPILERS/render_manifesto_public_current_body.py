#!/usr/bin/env python3
"""Render the staged Manifesto current-body as an off-site HTML preview.

This is not a public edition. It must not write under 12_PUBLIC_SITE/.
It must not retarget build_book.py CURRENT_WORK_ID.
G10 remains unpaid.
"""

from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "13_BOOKS/manifesto/PUBLIC_CURRENT_BODY_STAGED.md"
OUTPUT = ROOT / "13_BOOKS/manifesto/PUBLIC_CURRENT_BODY_READER_STAGED.html"
PUBLIC_SITE = ROOT / "12_PUBLIC_SITE"

FORBIDDEN = ("## 12.", "## 13.", "## 14.", "## 15.", "## 16.", "RIP01-")


def assert_output_is_off_site(path: Path) -> None:
    resolved = path.resolve()
    public = PUBLIC_SITE.resolve()
    if resolved == public or public in resolved.parents:
        raise SystemExit(f"refusing to write under 12_PUBLIC_SITE/: {path}")
    if "13_BOOKS/manifesto" not in resolved.as_posix():
        raise SystemExit(f"output must stay under 13_BOOKS/manifesto/: {path}")


def render_body(markdown: str) -> str:
    for needle in FORBIDDEN:
        if needle in markdown:
            raise SystemExit(f"forbidden marker in source: {needle}")
    chunks: list[str] = []
    in_code = False
    code: list[str] = []
    for raw in markdown.splitlines():
        if raw.startswith("```"):
            if in_code:
                chunks.append("<pre><code>" + html.escape("\n".join(code)) + "</code></pre>")
                code = []
                in_code = False
            else:
                in_code = True
            continue
        if in_code:
            code.append(raw)
            continue
        if raw.startswith("# "):
            chunks.append(f"<h1>{html.escape(raw[2:])}</h1>")
        elif raw.startswith("## "):
            chunks.append(f"<h2>{html.escape(raw[3:])}</h2>")
        elif raw.startswith("### "):
            chunks.append(f"<h3>{html.escape(raw[4:])}</h3>")
        elif raw.startswith("> "):
            chunks.append(f"<blockquote><p>{html.escape(raw[2:])}</p></blockquote>")
        elif raw.startswith("---"):
            chunks.append("<hr>")
        elif raw.strip() == "":
            continue
        else:
            chunks.append(f"<p>{html.escape(raw)}</p>")
    if in_code:
        chunks.append("<pre><code>" + html.escape("\n".join(code)) + "</code></pre>")
    return "\n".join(chunks)


def page(markdown: str) -> str:
    body = render_body(markdown)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex, nofollow, noarchive">
<title>Staged Manifesto current-body — not public</title>
<link rel="manifest" href="/manifest.webmanifest">
<meta name="theme-color" content="#070A12">
<link rel="apple-touch-icon" href="/assets/icons/apple-touch-icon.png">
<script src="/assets/js/pwa.js" defer></script>
<style>
body{{margin:0;background:#070A12;color:#e8e4d8;font:1.05rem/1.6 Georgia,serif}}
main{{max-width:46rem;margin:0 auto;padding:2.5rem 1.2rem 4rem}}
.banner{{border:1px solid #c99b32;padding:1rem 1.1rem;margin:0 0 2rem;background:#11141c}}
h1,h2,h3{{font-family:system-ui,sans-serif;line-height:1.2}}
pre{{overflow:auto;background:#11141c;padding:1rem}}
a{{color:#c99b32}}
</style>
</head>
<body>
<main>
<aside class="banner">
<p><b>STAGED PREVIEW — not a public edition.</b> This file lives under
<code>13_BOOKS/manifesto/</code> only. It is not a <code>/book/</code>
replacement. G10 is unpaid. A green render is not the Amrita.</p>
</aside>
{body}
</main>
</body>
</html>
"""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    assert_output_is_off_site(OUTPUT)
    markdown = SOURCE.read_text(encoding="utf-8")
    rendered = page(markdown)
    if args.check:
        if not OUTPUT.is_file() or OUTPUT.read_text(encoding="utf-8") != rendered:
            print("reader preview drift")
            return 1
        print(f"reader preview clean ({OUTPUT.relative_to(ROOT)}, staged, not public)")
        return 0
    OUTPUT.write_text(rendered, encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)} (staged, not public)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
