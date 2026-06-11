#!/usr/bin/env python3
"""Build book/rag_index.json — the retrieval corpus behind the AI-leveraged book.

Chunks the long-scroll book by its heading anchors and adds the lede of every
deep-library page, producing the passage corpus that assets/js/book-ai.js
searches client-side (BM25). Retrieval is fully static and key-free; an
owner-configured LLM endpoint upgrades answers from quoted passages to
generated prose (RAG). Regenerable: run after rebuilding the book or library.

Usage: python3 -B build_rag_index.py
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BOOK = ROOT / "book" / "index.html"
OUT = ROOT / "book" / "rag_index.json"

LIBRARY = ["canon", "formal", "paradox", "memetic", "rosettad", "operators",
           "will", "value", "ground", "sacred", "method", "meta"]

MAX_PASSAGE = 700          # chars of text per passage
HEAD_RE = re.compile(r'<h([12]) id="([^"]+)"[^>]*>(.*?)</h\1>', re.S)
TAG_RE = re.compile(r"<[^>]+>")
WS_RE = re.compile(r"\s+")


def clean(html_fragment: str) -> str:
    text = TAG_RE.sub(" ", html_fragment)
    text = (text.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
                .replace("&quot;", '"').replace("&#39;", "'").replace("&nbsp;", " "))
    return WS_RE.sub(" ", text).strip()


def book_passages():
    html = BOOK.read_text(encoding="utf-8", errors="replace")
    # chunk the whole document at its h1/h2 anchors — the TOC and the
    # per-chapter prev/next navs carry no headings, so they only ever land
    # in the tail of a preceding passage, never create one
    pieces = HEAD_RE.split(html)
    # pieces: [pre, lvl, id, title, content, lvl, id, title, content, ...]
    out = []
    for i in range(1, len(pieces) - 3, 4):
        anchor = pieces[i + 1]
        title = clean(pieces[i + 2])
        content = clean(pieces[i + 3])[:MAX_PASSAGE]
        if len(content) < 80 or not title:
            continue
        out.append({"id": f"book:{anchor}", "title": title,
                    "href": f"/book/#{anchor}", "text": content})
    return out


def library_passages():
    out = []
    for section in LIBRARY:
        base = ROOT / section
        if not base.is_dir():
            continue
        for sub in sorted(p for p in base.iterdir() if p.is_dir()):
            idx = sub / "index.html"
            if not idx.exists():
                continue
            html = idx.read_text(encoding="utf-8", errors="replace")
            m = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S)
            title = clean(m.group(1)) if m else sub.name.replace("-", " ")
            m2 = re.search(r"<main[^>]*>(.*)", html, re.S)
            text = clean((m2.group(1) if m2 else html.split("</h1>")[-1]))[:MAX_PASSAGE]
            if len(text) < 80:
                continue
            out.append({"id": f"{section}:{sub.name}", "title": title,
                        "href": f"/{section}/{sub.name}/", "text": text})
    return out


def main() -> int:
    passages = book_passages() + library_passages()
    OUT.write_text(json.dumps({"generated": "build_rag_index.py",
                               "count": len(passages), "passages": passages},
                              ensure_ascii=False), encoding="utf-8")
    size = OUT.stat().st_size
    print(f"rag_index.json: {len(passages)} passages, {size/1024:.0f} KB -> {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
