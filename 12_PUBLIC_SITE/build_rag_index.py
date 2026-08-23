#!/usr/bin/env python3
"""Build book/rag_index.json — the current reader's local retrieval corpus.

Chunks the current pure-Emergentism book and front-of-house pages into the
passage corpus searched client-side. Frozen generated-library pages are
deliberately excluded so superseded prose cannot outrank current owners.

Usage: python3 -B build_rag_index.py
"""

import argparse
import hashlib
import html as html_lib
import json
import re
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CORPUS_ROOT = ROOT.parent
BOOK = ROOT / "book" / "index.html"
OUT = ROOT / "book" / "rag_index.json"
BUILD_MANIFEST = ROOT / "book" / "build-manifest.json"

LIBRARY = []

LANDING_PAGES = ["compass", "map", "lab", "contribute", "dimensions", "check", "plainly", "dasein", "f5", "questions", "ethics", "churn", "amrita", "halahala", "practice", "record", "record/eub-1", "record/pqa-54", "record/churning", "exit"]

# Overview/doctrine pages chunked at their own headings (h2/h3 chapters) so the
# RAG corpus stays current with the front-of-house surfaces — these carry the
# 2026-06 findings (mass-shell, agency gloss, the unfolding) that the frozen
# book prose does not yet hold.
OVERVIEW_PAGES = ["compass", "map", "lab", "contribute", "dimensions", "check", "plainly", "dasein", "f5", "questions", "ethics", "churn", "amrita", "halahala", "practice", "record", "record/eub-1", "record/pqa-54", "record/churning", "exit",
                  "0", "1", "2", "3", "4", "5", "6"]

MAX_PASSAGE = 700          # chars of text per passage
HEAD_RE = re.compile(r'<h([12]) id="([^"]+)"[^>]*>(.*?)</h\1>', re.S)
TAG_RE = re.compile(r"<[^>]+>")
WS_RE = re.compile(r"\s+")


def validate_current_source(source: dict, corpus_root: Path = CORPUS_ROOT) -> Path:
    """Resolve one declared source and prove its bytes match the receipt."""
    declared_path = source.get("path")
    if not isinstance(declared_path, str) or not declared_path:
        raise SystemExit("RAG current source path is missing or malformed")
    source_path = (corpus_root / declared_path).resolve()
    try:
        source_rel = source_path.relative_to(corpus_root.resolve()).as_posix()
    except ValueError:
        raise SystemExit("RAG current source escapes the corpus root")
    if source_rel != declared_path or not source_path.is_file():
        raise SystemExit("RAG current source is missing or escapes the corpus root")
    source_sha256 = hashlib.sha256(source_path.read_bytes()).hexdigest()
    if source.get("sha256") != source_sha256:
        raise SystemExit("RAG refuses a stale current-source hash")
    return source_path


def source_negative_controls() -> None:
    """Prove a missing or hash-drifted source fails before index generation."""
    with tempfile.TemporaryDirectory() as tmp:
        corpus_root = Path(tmp)
        relative = "00_THE_WELTANSCHAUUNG_ONE_SITTING.md"
        source_path = corpus_root / relative
        source_path.write_bytes(b"current source fixture\n")
        source = {
            "path": relative,
            "sha256": hashlib.sha256(source_path.read_bytes()).hexdigest(),
        }
        validate_current_source(source, corpus_root)

        source_path.unlink()
        try:
            validate_current_source(source, corpus_root)
        except SystemExit:
            pass
        else:
            raise AssertionError("missing RAG source negative control was accepted")

        source_path.write_bytes(b"drifted source fixture\n")
        try:
            validate_current_source(source, corpus_root)
        except SystemExit:
            pass
        else:
            raise AssertionError("hash-drifted RAG source negative control was accepted")


def validate_book_contract() -> dict:
    """Reject retrieval from frozen, withheld, untracked, or stale book bytes."""
    try:
        manifest = json.loads(BUILD_MANIFEST.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"book build manifest unavailable or invalid: {exc}")
    if manifest.get("schema") != "emergentism/public-book-build/v2":
        raise SystemExit("book build manifest is not the fail-closed v2 contract")
    if manifest.get("work_id") != "BK-ONE-SITTING":
        raise SystemExit("RAG refuses a non-current book work")
    catalog = manifest.get("catalog_contract", {})
    catalog_path = CORPUS_ROOT / catalog.get("path", "__missing__")
    if (
        catalog.get("schema") != "emergentism/book-manifest/v2"
        or catalog.get("path") != "13_BOOKS/book-manifest.json"
        or not catalog_path.is_file()
        or catalog.get("sha256") != hashlib.sha256(catalog_path.read_bytes()).hexdigest()
        or catalog.get("release_state") != "source_active_current_public_reader"
        or catalog.get("public_route") != "../12_PUBLIC_SITE/book/index.html"
    ):
        raise SystemExit("RAG refuses a stale or non-current book catalog contract")
    sources = manifest.get("sources")
    if not isinstance(sources, list) or len(sources) != 1:
        raise SystemExit("RAG requires exactly one current book source")
    source = sources[0]
    if (
        source.get("path") != "00_THE_WELTANSCHAUUNG_ONE_SITTING.md"
        or source.get("lifecycle") != "reader_synthesis"
        or source.get("public_eligible") is not True
    ):
        raise SystemExit("RAG refuses a frozen, withheld, or undeclared book source")
    if manifest.get("ordered_source_paths") != [source["path"]]:
        raise SystemExit("RAG book source order contains undeclared provenance")
    validate_current_source(source)
    output = manifest.get("output", {})
    if output.get("path") != "book/index.html":
        raise SystemExit("RAG book output path drift")
    actual = hashlib.sha256(BOOK.read_bytes()).hexdigest()
    if output.get("sha256") != actual:
        raise SystemExit("RAG refuses stale or unreceipted book bytes")
    withheld = manifest.get("withheld_provenance", {})
    if withheld.get("included_in_output") is not False or withheld.get("included_in_rag") is not False:
        raise SystemExit("RAG withheld-provenance boundary is missing")
    return manifest


def clean(html_fragment: str) -> str:
    # Script/style bodies are not visible prose, especially on legacy pages
    # without a bounded <main>. Decode the remaining visible entity spelling
    # only after removing real markup so encoded examples remain readable text.
    visible = re.sub(
        r"<(script|style)\b[^>]*>.*?</\1>",
        " ",
        html_fragment,
        flags=re.I | re.S,
    )
    text = html_lib.unescape(TAG_RE.sub(" ", visible))
    return WS_RE.sub(" ", text).strip()


def book_passages():
    html = BOOK.read_text(encoding="utf-8", errors="replace")
    reading = re.search(r'<main\b[^>]*class="[^"]*\breading\b[^"]*"[^>]*>(.*?)</main>', html, re.S)
    if not reading:
        raise SystemExit("current book has no bounded reading main")
    html = reading.group(1)
    # Navigation, footer copy, and scripts are interface bytes, not source
    # passages. In particular, never let the last source heading absorb the
    # footer or inline JavaScript merely because no later heading terminates it.
    html = re.sub(r'<footer\b[^>]*class="[^"]*\bbook-foot\b[^"]*"[^>]*>.*?</footer>', "", html, flags=re.S)
    html = re.sub(r'<nav\b[^>]*class="[^"]*\bch-nav\b[^"]*"[^>]*>.*?</nav>', "", html, flags=re.S)
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
        main = re.search(r"<main\b[^>]*>(.*?)</main>", html, re.S)
        body_html = article.group(1) if article else (main.group(1) if main else html)
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


def desired_payload() -> dict:
    build = validate_book_contract()
    passages = book_passages() + landing_passages() + overview_passages()
    return {
        "generated": "build_rag_index.py",
        "scope": "current pure-Emergentism reader surfaces; frozen library excluded",
        "book_contract": {
            "work_id": build["work_id"],
            "ordered_source_paths": build["ordered_source_paths"],
            "source_lifecycles": [row["lifecycle"] for row in build["sources"]],
            "source_sha256": [row["sha256"] for row in build["sources"]],
            "book_output_sha256": build["output"]["sha256"],
            "withheld_provenance_included": False,
        },
        "count": len(passages),
        "passages": passages,
    }


def canonical_bytes(payload: dict) -> bytes:
    return json.dumps(payload, ensure_ascii=False).encode("utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if the committed RAG index is stale")
    parser.add_argument("--self-test", action="store_true", help="run source-integrity negative controls only")
    args = parser.parse_args(argv)
    if args.check and args.self_test:
        parser.error("--check and --self-test are mutually exclusive")

    try:
        source_negative_controls()
    except (OSError, AssertionError) as exc:
        print(f"RAG INDEX: FAIL\n- source-integrity negative control failed: {exc}")
        return 1
    if args.self_test:
        print("RAG SOURCE CONTRACT: PASS (missing and hash-drifted sources fail closed)")
        return 0

    payload = desired_payload()
    desired = canonical_bytes(payload)
    if args.check:
        if not OUT.is_file() or OUT.read_bytes() != desired:
            print("RAG INDEX: FAIL")
            print("- book/rag_index.json does not match its current sources")
            return 1
        print(f"RAG INDEX: PASS ({payload['count']} passages; source and book hashes current)")
        return 0

    OUT.write_bytes(desired)
    size = len(desired)
    print(f"rag_index.json: {payload['count']} passages, {size/1024:.0f} KB -> {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
