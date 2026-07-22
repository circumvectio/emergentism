#!/usr/bin/env python3
"""Build book/rag_index.json — the retrieval corpus behind the AI-leveraged book.

Chunks the current pure-Emergentism book and front-of-house pages into the
passage corpus searched client-side. Frozen generated-library pages are
deliberately excluded so superseded prose cannot outrank current owners.

Usage: python3 -B build_rag_index.py
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BOOK = ROOT / "book" / "index.html"
OUT = ROOT / "book" / "rag_index.json"

LIBRARY = []

LANDING_PAGES = ["compass", "dimensions", "check", "plainly", "practice", "record", "exit"]

# Overview/doctrine pages chunked at their own headings (h2/h3 chapters) so the
# RAG corpus stays current with the front-of-house surfaces — these carry the
# 2026-06 findings (mass-shell, agency gloss, the unfolding) that the frozen
# book prose does not yet hold.
OVERVIEW_PAGES = ["compass", "dimensions", "check", "plainly", "practice", "record", "exit",
                  "0", "1", "2", "3", "4", "5", "6"]

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
            article = re.search(
                r'<article[^>]*class="[^"]*\blibrary-article\b[^"]*"[^>]*>(.*?)</article>',
                html,
                re.S,
            )
            body_html = article.group(1) if article else html.split("</h1>")[-1]
            text = clean(body_html)
            boundary = re.search(
                r"<p><strong>Claim Boundary:</strong>.*?</p>",
                body_html,
                re.S,
            )
            if boundary:
                boundary_text = clean(boundary.group(0))
                if boundary_text not in text[:MAX_PASSAGE]:
                    text = f"{boundary_text} {text}"
            text = text[:MAX_PASSAGE]
            if len(text) < 80:
                continue
            out.append({"id": f"{section}:{sub.name}", "title": title,
                        "href": f"/{section}/{sub.name}/", "text": text})
    return out


def landing_passages():
    """Add selected library landing pages whose ledes carry current doctrine."""
    out = []
    for page in LANDING_PAGES:
        idx = ROOT / page / "index.html"
        if not idx.exists():
            continue
        html = idx.read_text(encoding="utf-8", errors="replace")
        m = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S)
        title = clean(m.group(1)) if m else page
        article = re.search(
            r'<article[^>]*class="[^"]*\blibrary-article\b[^"]*"[^>]*>(.*?)</article>',
            html,
            re.S,
        )
        body_html = article.group(1) if article else html
        text = clean(body_html)[:MAX_PASSAGE]
        if len(text) < 80:
            continue
        out.append({"id": f"page:{page}:landing", "title": title,
                    "href": f"/{page}/", "text": text})
    return out


SEC_RE = re.compile(r"<h([23])[^>]*>(.*?)</h\1>(.*?)(?=<h[23]\b|</section>|</article>|<footer)", re.S)


def overview_passages():
    """Chunk the doctrine/overview pages at their h2/h3 chapters."""
    out = []
    for page in OVERVIEW_PAGES:
        idx = ROOT / page / "index.html"
        if not idx.exists():
            continue
        html = idx.read_text(encoding="utf-8", errors="replace")
        pm = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S)
        page_title = clean(pm.group(1)) if pm else page
        chunks = SEC_RE.findall(html)
        if not chunks:
            body = clean(html.split("</h1>")[-1])[:MAX_PASSAGE]
            if len(body) >= 80:
                out.append({"id": f"page:{page}", "title": page_title,
                            "href": f"/{page}/", "text": body})
            continue
        for i, (_lvl, htitle, htext) in enumerate(chunks):
            title = clean(htitle)
            text = clean(htext)[:MAX_PASSAGE]
            # strip the expand-pill artifact if present
            title = re.sub(r"\s*✦\s*expand.*$", "", title)
            if len(text) < 60 or not title:
                continue
            out.append({"id": f"page:{page}:{i}", "title": f"{title} — {page_title}",
                        "href": f"/{page}/", "text": text})
    return out


def main() -> int:
    passages = book_passages() + landing_passages() + overview_passages()
    OUT.write_text(json.dumps({"generated": "build_rag_index.py",
                               "scope": "current pure-Emergentism reader surfaces; frozen library excluded",
                               "count": len(passages), "passages": passages},
                              ensure_ascii=False), encoding="utf-8")
    size = OUT.stat().st_size
    print(f"rag_index.json: {len(passages)} passages, {size/1024:.0f} KB -> {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
