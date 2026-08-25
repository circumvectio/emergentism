#!/usr/bin/env python3
"""Render the claim-card-covered current reader into book/index.html.

A Network-State-style free online book: sticky chapter table-of-contents, scroll
progress, deep-linkable sections, inline evidence-tier chips, light/dark reading
themes. Output is fully self-contained (no external resource references) so it
passes the 12_PUBLIC_SITE predeploy supply-chain gate. This .py is
.vercelignored (build tooling, not shipped). Source authority stays with the
declared current owner in 13_BOOKS/book-manifest.json; the result is only a
public snapshot.

Run:  python3 -B build_book.py [--check]
"""
import argparse, hashlib, json, os, re, sys
import markdown

from build_core_shell import head_assets, render_footer, render_nav

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
BOOK_MANIFEST = os.path.join(ROOT, "13_BOOKS", "book-manifest.json")
CLAIM_REGISTER = os.path.join(ROOT, "00_META", "registers", "CLAIM_CARD_REGISTER.json")
CLAIM_GRAPH = os.path.join(ROOT, "00_META", "registers", "CLAIM_GRAPH.json")
CURRENT_WORK_ID = "BK-ONE-SITTING"
CURRENT_RELEASE_STATE = "source_active_current_public_reader"
PUBLIC_ROUTE = "../12_PUBLIC_SITE/book/index.html"
ALLOWED_SOURCE_LIFECYCLES = {"active", "reader_synthesis"}
ALLOWED_PUBLIC_STATES = {"bounded_current", "candidate"}
ALLOWED_REVIEW_STATES = {"implemented", "l3_audited"}
OUT_DIR = os.path.join(HERE, "book")
OUT = os.path.join(OUT_DIR, "index.html")
BUILD_MANIFEST = os.path.join(OUT_DIR, "build-manifest.json")
EXTENSIONS = ["extra", "toc", "sane_lists"]

TIER_RE = re.compile(r'\[(A|B|S|I|D|C)((?:/[A-Z]+)*)\]')
SOURCE_LINK_RE = re.compile(r'href="(?P<target>[^"#]*\.(?:md|json)(?:#[^"]*)?)"')
PUBLIC_SOURCE_LINK_ROUTES = {
    # The internal ledger is broader than its twelve-question public projection.
    # The Lab makes that weaker boundary visible rather than implying equality.
    "00_META/00_THE_GRAND_PUZZLE_ASSEMBLY_LEDGER.md": "../lab/#questions",
    # The canonical machine-readable F5 fork is projected through the bounded
    # public fork page rather than exposed as an undeployed repository link.
    "05_COSMOLOGY/02_EMERGENTISM_CORE/F5Fork.v1.json": "../f5/",
}

def strip_tags(s):
    return re.sub(r'<[^>]+>', '', s).strip()

def wrap_tiers(htmltext):
    def repl(m):
        first = m.group(1).lower()
        return f'<span class="tier t-{first}">[{m.group(1)}{m.group(2)}]</span>'
    return TIER_RE.sub(repl, htmltext)


def route_source_link(match):
    """Route a non-deployed source link to its declared public boundary."""
    source_path = os.path.normpath(match.group("target").split("#", 1)[0])
    source_path = source_path.replace(os.sep, "/")
    return f'href="{PUBLIC_SOURCE_LINK_ROUTES.get(source_path, "../sources/")}"'


def load_object(path, label):
    try:
        value = json.loads(open(path, encoding="utf-8").read())
    except (OSError, json.JSONDecodeError) as exc:
        sys.exit(f"{label} is unavailable or invalid: {exc}")
    if not isinstance(value, dict):
        sys.exit(f"{label} must be a JSON object")
    return value


def resolve_corpus_path(rel, label):
    if not isinstance(rel, str) or not rel or os.path.isabs(rel):
        sys.exit(f"{label} must be a non-empty corpus-relative path")
    path = os.path.normpath(os.path.join(ROOT, rel))
    try:
        if os.path.commonpath([ROOT, path]) != ROOT:
            sys.exit(f"{label} escapes the corpus root: {rel}")
    except ValueError:
        sys.exit(f"{label} escapes the corpus root: {rel}")
    if not os.path.isfile(path):
        sys.exit(f"{label} not found: {rel}")
    return path


def current_source_contract():
    """Return the one public source only after every custody gate agrees.

    The fail-closed rule is deliberate: a generator must not turn a frozen,
    withheld, staged, or incompletely covered work into the current reader just
    because a Markdown directory happens to exist.
    """
    books = load_object(BOOK_MANIFEST, "book manifest")
    if books.get("schema") != "emergentism/book-manifest/v2":
        sys.exit("book manifest schema drift")
    works = books.get("works")
    if not isinstance(works, list):
        sys.exit("book manifest works must be a list")
    matches = [row for row in works if isinstance(row, dict) and row.get("work_id") == CURRENT_WORK_ID]
    if len(matches) != 1:
        sys.exit(f"book manifest must declare exactly one {CURRENT_WORK_ID} work")
    work = matches[0]
    if work.get("release_state") != CURRENT_RELEASE_STATE:
        sys.exit(f"{CURRENT_WORK_ID} is not the current public reader")
    if work.get("public_route") != PUBLIC_ROUTE:
        sys.exit(f"{CURRENT_WORK_ID} public route drift")
    route_owners = [
        row.get("work_id") for row in works
        if isinstance(row, dict) and row.get("public_route") == PUBLIC_ROUTE
    ]
    if route_owners != [CURRENT_WORK_ID]:
        sys.exit(f"current /book route has competing owners: {route_owners}")
    reciprocal = next(
        (row for row in works if isinstance(row, dict) and row.get("work_id") == "BK-RECIPROCAL-INFINITE-PLAY"),
        None,
    )
    if not isinstance(reciprocal, dict):
        sys.exit("book manifest lacks Reciprocal provenance custody")
    if (
        reciprocal.get("release_state") != "withheld_staged_provenance_not_current_not_rag"
        or reciprocal.get("public_route") is not None
        or reciprocal.get("publication_eligible") is not False
    ):
        sys.exit("Reciprocal provenance is not explicitly withheld from book and RAG")

    declarations = work.get("publication_sources")
    if not isinstance(declarations, list) or len(declarations) != 1:
        sys.exit(f"{CURRENT_WORK_ID} must declare exactly one publication source")
    declaration = declarations[0]
    if not isinstance(declaration, dict) or declaration.get("public_eligible") is not True:
        sys.exit("current publication source is not explicitly public-eligible")
    lifecycle = declaration.get("lifecycle")
    if lifecycle not in ALLOWED_SOURCE_LIFECYCLES:
        sys.exit(f"current publication source has barred lifecycle: {lifecycle!r}")
    source_rel = declaration.get("path")
    source = resolve_corpus_path(source_rel, "current publication source")
    cards_rel = declaration.get("claim_card_set")
    cards_path = resolve_corpus_path(cards_rel, "current claim-card set")

    ledger = load_object(cards_path, "current claim-card set")
    if ledger.get("schema") != "emergentism/claim-card-set/v2":
        sys.exit("current claim-card set schema drift")
    if ledger.get("work_id") != CURRENT_WORK_ID:
        sys.exit("current claim-card set work mismatch")
    source_contract = ledger.get("source")
    if not isinstance(source_contract, dict):
        sys.exit("current claim-card set lacks a source contract")
    if source_contract.get("path") != source_rel or source_contract.get("lifecycle") != lifecycle:
        sys.exit("current claim-card source path/lifecycle mismatch")

    cards = ledger.get("cards")
    if not isinstance(cards, list) or not cards:
        sys.exit("current publication source has no claim cards")
    card_ids = [card.get("card_id") for card in cards if isinstance(card, dict)]
    if len(card_ids) != len(cards) or len(card_ids) != len(set(card_ids)) or any(not item for item in card_ids):
        sys.exit("current claim-card set has missing or duplicate IDs")
    declared_ids = work.get("claim_card_ids")
    if not isinstance(declared_ids, list) or set(declared_ids) != set(card_ids):
        sys.exit("book manifest does not exactly cover the current claim-card set")
    covered_chapters = sorted({chapter for card in cards for chapter in card.get("chapters", [])})
    if set(covered_chapters) != set(work.get("chapter_order", [])):
        sys.exit("book chapter order is not completely covered by current claim cards")
    for card in cards:
        public_state = card.get("public", {}).get("state")
        review_state = card.get("review", {}).get("state")
        if public_state not in ALLOWED_PUBLIC_STATES:
            sys.exit(f"claim card {card.get('card_id')} has non-current public state: {public_state!r}")
        if review_state not in ALLOWED_REVIEW_STATES:
            sys.exit(f"claim card {card.get('card_id')} is not reviewed: {review_state!r}")

    register = load_object(CLAIM_REGISTER, "claim-card register")
    register_selected = [
        row for row in register.get("cards", [])
        if isinstance(row, dict) and row.get("work_id") == CURRENT_WORK_ID
    ]
    register_rows = {
        row.get("card_id"): row for row in register_selected
    }
    if len(register_selected) != len(register_rows) or set(register_rows) != set(card_ids):
        sys.exit("derived claim-card register does not exactly cover the current work")
    for card_id, row in register_rows.items():
        if row.get("source_path") != source_rel or row.get("source_lifecycle") != lifecycle:
            sys.exit(f"derived claim-card source contract drift: {card_id}")
        if row.get("public_state") not in ALLOWED_PUBLIC_STATES:
            sys.exit(f"derived claim-card public state is not current: {card_id}")
        if row.get("review_state") not in ALLOWED_REVIEW_STATES:
            sys.exit(f"derived claim-card is not reviewed: {card_id}")

    graph = load_object(CLAIM_GRAPH, "claim graph")
    graph_selected = [
        row for row in graph.get("nodes", [])
        if isinstance(row, dict) and row.get("id") in set(card_ids)
    ]
    graph_rows = {
        row.get("id"): row for row in graph_selected
    }
    if len(graph_selected) != len(graph_rows) or set(graph_rows) != set(card_ids):
        sys.exit("claim graph does not exactly cover the current work")
    for card_id, row in graph_rows.items():
        if row.get("kind") != "claim" or row.get("lifecycle") != lifecycle:
            sys.exit(f"claim graph lifecycle drift: {card_id}")

    return {
        "work": work,
        "source": source,
        "source_rel": source_rel,
        "lifecycle": lifecycle,
        "cards_path": cards_path,
        "cards_rel": cards_rel,
        "card_ids": sorted(card_ids),
        "covered_chapters": covered_chapters,
        "public_states": sorted({card["public"]["state"] for card in cards}),
        "review_states": sorted({card["review"]["state"] for card in cards}),
        "book_manifest_schema": books["schema"],
    }


def chapter_slug(title):
    """Normalize a numbered source heading to its manifest chapter key."""
    core = re.sub(r"^\d+\.\s*", "", strip_tags(title)).split(" — ", 1)[0].strip()
    core = re.sub(r"^the\s+", "", core, flags=re.I)
    return re.sub(r"[^a-z0-9]+", "-", core.lower()).strip("-")


def validate_rendered_chapters(body, contract):
    """Bind what the renderer will publish to the card-covered chapter list.

    Coverage declarations alone are insufficient: a new numbered H2 in the
    source would otherwise be rendered even if neither the manifest nor any
    claim card named it. Validate the rendered HTML immediately before it is
    split into public chapters.
    """
    h1s = re.findall(r'<h1 id="[^"]+">(.*?)</h1>', body, flags=re.S)
    if len(h1s) != 1:
        sys.exit(f"current publication source must render exactly one H1; found {len(h1s)}")

    rendered_candidates = []
    for heading_id, title_html in re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', body, flags=re.S):
        title = strip_tags(title_html)
        selected_by_renderer = bool(re.match(r"\d", heading_id))
        numbered_in_source = bool(re.match(r"^\d+\.\s+", title))
        if selected_by_renderer != numbered_in_source:
            sys.exit(
                "numbered source H2 and renderer chapter selection disagree: "
                f"id={heading_id!r} title={title!r}"
            )
        if numbered_in_source:
            rendered_candidates.append((heading_id, title))
    parsed = []
    for heading_id, title in rendered_candidates:
        match = re.match(r"^(\d+)\.\s+(.+)$", title)
        if not match:
            sys.exit(f"renderer-selected H2 is not a numbered chapter: {heading_id!r}")
        parsed.append((int(match.group(1)), chapter_slug(title)))

    expected_order = contract["work"].get("chapter_order")
    if not isinstance(expected_order, list) or any(not isinstance(item, str) or not item for item in expected_order):
        sys.exit("book manifest chapter order must be a non-empty string list")
    expected_numbers = list(range(1, len(expected_order) + 1))
    actual_numbers = [number for number, _ in parsed]
    actual_order = [slug for _, slug in parsed]
    if len(parsed) != 12 or len(expected_order) != 12:
        sys.exit(
            "current reader must have exactly 12 numbered, card-covered chapters; "
            f"source={len(parsed)} manifest={len(expected_order)}"
        )
    if actual_numbers != expected_numbers:
        sys.exit(f"source chapter numbering drift: {actual_numbers}")
    if actual_order != expected_order:
        sys.exit(f"source chapter order is not the manifest/card-covered order: {actual_order}")
    if set(actual_order) != set(contract["covered_chapters"]):
        sys.exit("rendered source chapters are not exactly covered by current claim cards")
    return actual_order


def render(contract):
    text = open(contract["source"], encoding="utf-8").read()
    raw = re.sub(r"\A---\s*\n.*?\n---\s*\n", "", text, flags=re.S).strip()

    md = markdown.Markdown(extensions=EXTENSIONS)
    body = md.convert(raw)
    # Repository Markdown sources are not deployed. Most route to the generic
    # source boundary; explicitly declared weaker public projections may route
    # to their own visible boundary instead of emitting a dead relative URL.
    body = SOURCE_LINK_RE.sub(route_source_link, body)
    body = wrap_tiers(body)
    source_chapter_order = validate_rendered_chapters(body, contract)

    # The One-Sitting source owns one H1 and twelve numbered H2 chapters. The
    # unnumbered subtitle stays in the overture and the Reader Map stays with
    # chapter 12; neither becomes an uncontracted extra chapter.
    chapter_heading = r'(?:<h1 id="[^"]+">.*?</h1>|<h2 id="\d[^\"]*">.*?</h2>)'
    parts = re.split(f"({chapter_heading})", body, flags=re.S)

    # pass 1: collect chapters
    chapters = []
    pre = parts[0]  # anything before the first h1 (normally empty)
    i = 1
    while i < len(parts):
        h1 = parts[i]
        content = parts[i + 1] if i + 1 < len(parts) else ""
        m = re.match(r'<h[12] id="([^"]+)">(.*?)</h[12]>', h1, flags=re.S)
        chapters.append((m.group(1), strip_tags(m.group(2)), content))
        i += 2

    # pass 2: build sections with prev/next chapter nav
    sections, toc = [], []
    for idx, (hid, htitle, content) in enumerate(chapters):
        first = (idx == 0)
        cls = "chapter overture" if first else "chapter"
        heading_tag = "h1" if first else "h2"
        # The chapter number badge (skip the front-matter overture).
        badge = "" if first else f'<span class="ch-num">{idx:02d}</span>'
        nav_bits = []
        if idx > 0:
            phid, ptitle, _ = chapters[idx - 1]
            plabel = "Overture" if idx == 1 else ptitle
            nav_bits.append(f'<a class="ch-prev" href="#{phid}">← {plabel}</a>')
        if idx < len(chapters) - 1:
            nhid, ntitle, _ = chapters[idx + 1]
            nav_bits.append(f'<a class="ch-next" href="#{nhid}">{ntitle} →</a>')
        nav = f'<nav class="ch-nav" aria-label="Chapter navigation">{"".join(nav_bits)}</nav>' if nav_bits else ""
        sections.append(
            f'<section class="{cls}" id="{hid}">'
            f'<header class="ch-head">{badge}<{heading_tag} id="{hid}-h">{htitle}</{heading_tag}></header>'
            f'<div class="ch-body">{content}</div>{nav}</section>')
        label = "Overture" if first else htitle
        toc.append(
            f'<a class="toc-link{" is-overture" if first else ""}" href="#{hid}" data-target="{hid}">'
            f'<span class="toc-n">{"·" if first else f"{idx:02d}"}</span>'
            f'<span class="toc-t">{label}</span></a>')

    body_html = pre + "\n".join(sections)
    toc_html = "\n".join(toc)
    n_ch = len(chapters) - 1
    words = len(re.findall(r"\w+", strip_tags(body)))

    page = TEMPLATE
    page = page.replace("%%TOC%%", toc_html)
    page = page.replace("%%BODY%%", body_html)
    page = page.replace("%%NCH%%", str(n_ch))
    page = page.replace("%%WORDS%%", f"{words:,}")
    page = page.replace("%%CORE_HEAD%%", head_assets())
    page = page.replace("%%CORE_NAV%%", render_nav("library"))
    page = page.replace("%%CORE_FOOTER%%", render_footer())

    return page, n_ch, words, source_chapter_order


def sha_bytes(value):
    return hashlib.sha256(value).hexdigest()


def desired_manifest(page, contract, source_chapter_order):
    source = contract["source"]
    return {
        "schema": "emergentism/public-book-build/v2",
        "work_id": CURRENT_WORK_ID,
        "catalog_contract": {
            "schema": contract["book_manifest_schema"],
            "path": os.path.relpath(BOOK_MANIFEST, ROOT).replace(os.sep, "/"),
            "sha256": sha_bytes(open(BOOK_MANIFEST, "rb").read()),
            "release_state": CURRENT_RELEASE_STATE,
            "public_route": PUBLIC_ROUTE,
        },
        "sources": [
            {
                "path": contract["source_rel"],
                "sha256": sha_bytes(open(source, "rb").read()),
                "lifecycle": contract["lifecycle"],
                "public_eligible": True,
                "claim_card_set": contract["cards_rel"],
            }
        ],
        "ordered_source_paths": [contract["source_rel"]],
        "output": {"path": "book/index.html", "sha256": sha_bytes(page.encode("utf-8"))},
        "renderer": {"package": "Markdown", "version": markdown.__version__, "extensions": EXTENSIONS},
        "claim_card_contract": {
            "schema": "emergentism/claim-card-set/v2",
            "path": contract["cards_rel"],
            "sha256": sha_bytes(open(contract["cards_path"], "rb").read()),
            "register_path": os.path.relpath(CLAIM_REGISTER, ROOT).replace(os.sep, "/"),
            "register_sha256": sha_bytes(open(CLAIM_REGISTER, "rb").read()),
            "graph_path": os.path.relpath(CLAIM_GRAPH, ROOT).replace(os.sep, "/"),
            "graph_sha256": sha_bytes(open(CLAIM_GRAPH, "rb").read()),
            "coverage": {
                "claim_card_count": len(contract["card_ids"]),
                "claim_card_ids": contract["card_ids"],
                "covered_chapters": contract["covered_chapters"],
                "rendered_source_chapter_order": source_chapter_order,
                "public_states": contract["public_states"],
                "review_states": contract["review_states"],
            },
        },
        "withheld_provenance": {
            "path": "13_BOOKS/the_reciprocal/",
            "lifecycle": "withheld_staged_provenance",
            "included_in_output": False,
            "included_in_rag": False,
        },
        "authority": "deterministic projection receipt; the current source owner retains semantics",
    }


def build(check=False):
    contract = current_source_contract()
    page, n_ch, words, source_chapter_order = render(contract)
    manifest = (
        json.dumps(
            desired_manifest(page, contract, source_chapter_order),
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )
    if check:
        errors = []
        if not os.path.exists(OUT) or open(OUT, "rb").read() != page.encode("utf-8"):
            errors.append("book/index.html drift")
        if not os.path.exists(BUILD_MANIFEST) or open(BUILD_MANIFEST, "rb").read() != manifest.encode("utf-8"):
            errors.append("book/build-manifest.json drift")
        if errors:
            print("PUBLIC BOOK BUILD: FAIL")
            for item in errors:
                print(f"- {item}")
            return 1
        print(f"PUBLIC BOOK BUILD: PASS ({n_ch} chapters, {words:,} words)")
        return 0
    os.makedirs(OUT_DIR, exist_ok=True)
    open(OUT, "w", encoding="utf-8").write(page)
    open(BUILD_MANIFEST, "w", encoding="utf-8").write(manifest)
    print(f"wrote {OUT}")
    print(f"wrote {BUILD_MANIFEST}")
    print(f"  chapters: {n_ch} (+overture)   words: {words:,}   bytes: {len(page):,}")
    return 0


TEMPLATE = r"""<!DOCTYPE html>
<html lang="en" data-reading-theme="light" data-gestalt="v2">
<head>
<meta property="og:type" content="website" />
<meta property="og:site_name" content="Emergentism" />
<meta property="og:url" content="https://emergentism.org/book/" />
<meta property="og:image" content="https://emergentism.org/assets/og/og-card.png" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:image" content="https://emergentism.org/assets/og/og-card.png" />
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>The One-Sitting Reader — Emergentism</title>
<meta name="description" content="A current Emergentist reader: a typed worldview, its practical compass, selected symbolic grammar, open wagers, and visible limits. World-facing evidence and independent review remain incomplete." />
<meta name="color-scheme" content="light dark" />
%%CORE_HEAD%%
<style>
/* Self-hosted Roboto (Apache-2.0) — accessible and gate-safe */
@font-face{font-family:'Roboto';font-style:normal;font-weight:100 900;font-display:optional;src:url('../assets/fonts/Roboto-latin.woff2') format('woff2');unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}
@font-face{font-family:'Roboto';font-style:normal;font-weight:100 900;font-display:optional;src:url('../assets/fonts/Roboto-greek.woff2') format('woff2');unicode-range:U+0370-0377,U+037A-037F,U+0384-038A,U+038C,U+038E-03A1,U+03A3-03FF}
@font-face{font-family:'Roboto Mono';font-style:normal;font-weight:100 700;font-display:optional;src:url('../assets/fonts/RobotoMono-latin.woff2') format('woff2');unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}
@font-face{font-family:'Roboto Mono';font-style:normal;font-weight:100 700;font-display:optional;src:url('../assets/fonts/RobotoMono-greek.woff2') format('woff2');unicode-range:U+0370-0377,U+037A-037F,U+0384-038A,U+038C,U+038E-03A1,U+03A3-03FF}
:root{
  --serif:"Hoefler Text","Iowan Old Style","Palatino Linotype",Palatino,"Book Antiqua",Georgia,serif;
  --sans:"Roboto",-apple-system,BlinkMacSystemFont,"Segoe UI",system-ui,sans-serif;
  --mono:"Roboto Mono",ui-monospace,"SF Mono",Menlo,Consolas,monospace;
  --measure:40rem; --shape-lg:16px; --shape-full:999px; --target-min:48px;
}
/* ---- light (parchment) reading theme : default ---- */
html[data-reading-theme="light"]{
  --bg:#FDFAF4; --bg2:#FAF7F0; --panel:#F2EDE3;
  --ink:#18160E; --ink-soft:#4A4438; --ink-faint:#7A7062;
  --rule:rgba(24,22,14,.14); --rule-soft:rgba(24,22,14,.08);
  --gold:#92650A; --gold-bright:#7a5408;
  --t-a:#1565C0; --t-b:#92650A; --t-s:#1d7e70; --t-i:#92650A; --t-d:#6d6d6d; --t-c:#6f4fa0;
  --shadow:0 1px 0 rgba(255,255,255,.5);
}
/* ---- dark (void) reading theme ---- */
html[data-reading-theme="dark"]{
  --bg:#050505; --bg2:#0e0e0e; --panel:#101010;
  --ink:#F3F4F6; --ink-soft:#9CA3AF; --ink-faint:#6b7280;
  --rule:rgba(243,244,246,.13); --rule-soft:rgba(243,244,246,.07);
  --gold:#FFEB3B; --gold-bright:#FFF176;
  --t-a:#7fb2e6; --t-b:#FFEB3B; --t-s:#5fc6b0; --t-i:#e8d24a; --t-d:#a3a3a3; --t-c:#b59ce0;
  --shadow:none;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink);
  font-family:var(--serif);font-size:20px;line-height:1.72;
  -webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility;
  font-feature-settings:"liga" 1,"onum" 1,"kern" 1;}
::selection{background:rgba(184,134,44,.26)}
a{color:inherit}
.skip{position:fixed;z-index:100;top:.6rem;left:.6rem;background:var(--gold);color:var(--bg);font:700 .78rem var(--mono);padding:.7rem 1rem;text-decoration:none;transform:translateY(-180%);transition:transform .15s}
.skip:focus{transform:translateY(0)}

/* progress bar */
.progress{position:fixed;top:0;left:0;height:3px;width:0;z-index:110;
  background:var(--gold);transition:width .12s linear}

/* topbar */
.bookbar{position:sticky;top:0;z-index:50;display:flex;align-items:center;justify-content:space-between;
  gap:1rem;min-height:64px;padding:.7rem clamp(1rem,3vw,1.6rem);
  background:color-mix(in srgb,var(--bg) 86%,transparent);backdrop-filter:blur(10px);
  border-bottom:1px solid var(--rule-soft)}
.bookbar .brand{font-family:var(--sans);font-weight:600;font-size:1.05rem;letter-spacing:0}
.bookbar .brand b{color:var(--gold)}
.bookbar nav{display:flex;align-items:center;gap:.4rem;font-family:var(--mono);font-size:.76rem}
.bookbar nav a,.bookbar nav button{color:var(--ink-soft);background:none;border:1px solid transparent;
  min-height:var(--target-min);display:inline-flex;align-items:center;border-radius:var(--shape-full);padding:0 .75rem;cursor:pointer;font:inherit;letter-spacing:0}
.bookbar nav a:hover,.bookbar nav button:hover{color:var(--gold);border-color:var(--rule)}
.book-tools{min-height:52px;display:flex;justify-content:flex-end;gap:.5rem;padding:.35rem clamp(1rem,3vw,1.6rem);background:var(--bg);border-bottom:1px solid var(--rule-soft)}
.book-tools button{display:none;min-height:48px;padding:0 .8rem;border:1px solid var(--rule);background:var(--bg2);color:var(--ink-soft);font:600 .76rem var(--mono);cursor:pointer}
html[data-gestalt-enhanced="true"] #theme-toggle{display:inline-flex;align-items:center}
#toc-toggle{display:none}

/* layout */
.book-shell{display:grid;grid-template-columns:clamp(240px,22vw,310px) minmax(0,1fr);
  max-width:1320px;margin:0 auto}
/* TOC */
.toc{position:sticky;top:52px;align-self:start;height:calc(100vh - 52px);overflow-y:auto;
  padding:2rem 1rem 4rem 1.4rem;border-right:1px solid var(--rule-soft);
  scrollbar-width:thin}
.toc-head{font-family:var(--mono);font-size:.68rem;letter-spacing:0;text-transform:uppercase;
  color:var(--ink-faint);margin:0 0 1rem .2rem}
.toc-link{display:flex;gap:.7rem;align-items:baseline;padding:.32rem .4rem;border-radius:5px;
  text-decoration:none;color:var(--ink-soft);line-height:1.3;transition:.16s}
.toc-link .toc-n{font-family:var(--mono);font-size:.66rem;color:var(--ink-faint);min-width:1.4em;text-align:right;flex:none}
.toc-link .toc-t{font-size:.9rem;font-family:var(--sans)}
.toc-link:hover{color:var(--ink);background:var(--bg2)}
.toc-link.is-active{color:var(--gold);background:var(--bg2)}
.toc-link.is-active .toc-n{color:var(--gold)}
.toc-link.is-overture .toc-t{font-style:italic}

/* reading column */
.reading{padding:clamp(1.5rem,4vw,3.5rem) clamp(1.1rem,5vw,2rem) 6rem;min-width:0}
.reading-inner{max-width:var(--measure);margin:0 auto}
.chapter{padding:2.2rem 0 1rem;border-top:1px solid var(--rule-soft)}
.chapter.overture{border-top:0;padding-top:.5rem}
.chapter:first-of-type{border-top:0}
.ch-head{margin:0 0 1.4rem}
.ch-num{display:block;font-family:var(--mono);font-size:.72rem;letter-spacing:0;color:var(--gold);margin-bottom:.7rem}
.ch-body>h1:first-child,.chapter>header :is(h1,h2){margin-top:0}
h1,.ch-head h2{font-family:var(--serif);font-weight:600;font-size:clamp(1.9rem,4.2vw,2.9rem);line-height:1.08;
  letter-spacing:0;margin:.2rem 0 1rem;text-wrap:balance;overflow-wrap:anywhere}
.overture .ch-head h1{font-size:clamp(2.6rem,6vw,4rem)}
.ch-body h2{font-family:var(--serif);font-weight:600;font-size:clamp(1.25rem,2.4vw,1.6rem);line-height:1.2;
  margin:2.4rem 0 .8rem;letter-spacing:0}
h3{font-family:var(--mono);font-weight:600;font-size:.82rem;letter-spacing:0;text-transform:uppercase;
  color:var(--ink-faint);margin:2rem 0 .6rem}
p{margin:0 0 1.15rem}
.reading-inner>.chapter .ch-body>p:first-of-type{margin-top:.2rem}
/* drop cap on the first paragraph of each non-overture chapter */
.chapter:not(.overture) .ch-body>p:first-of-type::first-letter{
  font-family:var(--serif);font-weight:600;float:left;font-size:3.6em;line-height:.78;
  padding:.04em .12em 0 0;color:var(--gold)}
strong{font-weight:600}
em{font-style:italic}
code{font-family:var(--mono);font-size:.86em;background:var(--bg2);padding:.06em .35em;border-radius:3px;
  overflow-wrap:anywhere;word-break:break-word}
pre{max-width:100%;font-family:var(--mono);font-size:.9em;background:var(--bg2);padding:.75rem;border-radius:6px;overflow-x:auto}
hr{border:0;height:1px;background:var(--rule);margin:2.4rem auto;width:42%}
blockquote{margin:1.6rem 0;padding:.4rem 0 .4rem 1.3rem;border-left:2px solid var(--gold);
  color:var(--ink-soft);font-style:italic}
ul,ol{margin:0 0 1.15rem;padding-left:1.4rem}
li{margin:.3rem 0}
table{border-collapse:collapse;width:100%;margin:1.4rem 0;font-size:.9rem}
th,td{border:1px solid var(--rule);padding:.5rem .7rem;text-align:left}
th{background:var(--bg2);font-family:var(--mono);font-weight:600;font-size:.8rem}

/* tier chips */
.tier{font-family:var(--mono);font-size:.72em;font-weight:600;padding:.04em .34em;border-radius:3px;
  white-space:nowrap;border:1px solid currentColor;line-height:1.4;vertical-align:baseline}
.tier.t-a{color:var(--t-a)} .tier.t-b{color:var(--t-b)} .tier.t-s{color:var(--t-s)}
.tier.t-i{color:var(--t-i)} .tier.t-d{color:var(--t-d)} .tier.t-c{color:var(--t-c)}

/* heading anchor on hover */
h1[id],h2[id]{scroll-margin-top:70px;position:relative}

/* chapter prev/next nav */
.ch-nav{display:flex;justify-content:space-between;gap:1rem;margin:2.4rem 0 .2rem;padding-top:1.1rem;
  border-top:1px solid var(--rule-soft);font-family:var(--sans);font-size:.85rem}
.ch-nav a{color:var(--ink-soft);text-decoration:none;max-width:46%;overflow:hidden;
  text-overflow:ellipsis;white-space:nowrap;transition:color .15s}
.ch-nav a:hover{color:var(--gold)}
.ch-nav .ch-next{margin-left:auto;text-align:right}

/* footer */
.book-foot{border-top:1px solid var(--rule);margin-top:3rem;padding:3rem clamp(1rem,5vw,2rem);text-align:center}
.book-foot .phi{font-family:var(--serif);font-size:1.7rem;color:var(--gold);margin-bottom:.6rem}
.book-foot p{color:var(--ink-faint);font-family:var(--mono);font-size:.76rem;max-width:54ch;margin:0 auto .4rem}
.book-foot a{color:var(--ink-soft);text-decoration:underline;text-underline-offset:3px}

/* mobile */
@media(max-width:900px){
  body{font-size:18px}
  .bookbar{align-items:flex-start;flex-wrap:wrap}
  .bookbar nav{width:100%;justify-content:flex-start;overflow-x:auto;scrollbar-width:none}
  .bookbar nav::-webkit-scrollbar{display:none}
  .bookbar nav a,.bookbar nav button{flex:0 0 auto;white-space:nowrap}
  .book-shell{grid-template-columns:1fr}
  .toc{position:static;top:auto;left:auto;height:auto;width:auto;z-index:auto;background:var(--panel);
    border-right:0;border-bottom:1px solid var(--rule);opacity:1;visibility:visible;pointer-events:auto;padding:1.5rem 1rem}
  html[data-gestalt-enhanced="true"] #toc-toggle{display:inline-flex;align-items:center}
  html[data-gestalt-enhanced="true"] .toc{position:fixed;top:0;left:0;height:100vh;width:min(84vw,330px);z-index:105;background:var(--panel);
    border-right:1px solid var(--rule);clip-path:inset(0 100% 0 0);opacity:0;visibility:hidden;pointer-events:none;
    transition:clip-path .28s cubic-bezier(.2,.7,.2,1),opacity .18s ease;padding-top:3.4rem}
  html[data-gestalt-enhanced="true"].toc-open .toc{clip-path:inset(0);opacity:1;visibility:visible;pointer-events:auto;box-shadow:0 0 60px rgba(0,0,0,.4)}
  html[data-gestalt-enhanced="true"].toc-open .toc-scrim{position:fixed;inset:0;z-index:104;background:rgba(0,0,0,.45)}
  pre{overflow-x:hidden;white-space:pre-wrap}
  pre code{white-space:pre-wrap;overflow-wrap:anywhere;word-break:break-word}
}
@media(prefers-reduced-motion:reduce){
  html{scroll-behavior:auto}
  .progress,.toc{transition:none}
}
@media(prefers-reduced-transparency:reduce){
  .bookbar{background:var(--bg);backdrop-filter:none}
}
</style>
</head>
<body class="g2-book">
<div class="progress" id="progress"></div>
%%CORE_NAV%%
<div class="book-tools" aria-label="Reading controls">
  <button id="toc-toggle" aria-label="Open contents" aria-controls="toc" aria-expanded="false">Contents</button>
  <button id="theme-toggle" aria-label="Switch to dark reading theme" title="Switch reading theme">Reading theme</button>
</div>

<div class="book-shell">
  <aside class="toc" id="toc" aria-label="Table of contents">
    <div class="toc-head">One-Sitting Reader · %%NCH%% chapters · %%WORDS%% words</div>
    %%TOC%%
  </aside>
  <main class="reading" id="main" tabindex="-1">
    <div class="reading-inner">
      %%BODY%%
      <footer class="book-foot">
        <div class="phi">P_node := min(Φ̂₄, V₄) · ordinal AND-class; Φ̂₄V₄ ranking retired</div>
        <p>This reader distills the current <a href="../dimensions/">dimension-first spine</a>, <a href="../practice/">Lived Compass</a>, and <a href="../record/">correction record</a>.</p>
        <p>Its highest success is that you can put it down.</p>
      </footer>
    </div>
  </main>
</div>
%%CORE_FOOTER%%

<script>
(function(){
  var root=document.documentElement;
  // theme: default light, honor stored choice
  try{var t=localStorage.getItem("emergentism-reading-theme");if(t)root.setAttribute("data-reading-theme",t);}catch(e){}
  var tt=document.getElementById("theme-toggle");
  function setThemeLabel(){if(!tt)return;var target=root.getAttribute("data-reading-theme")==="dark"?"light":"dark";tt.setAttribute("aria-label","Switch to "+target+" reading theme");}
  setThemeLabel();
  if(tt)tt.addEventListener("click",function(){
    var cur=root.getAttribute("data-reading-theme")==="dark"?"light":"dark";
    root.setAttribute("data-reading-theme",cur);
    try{localStorage.setItem("emergentism-reading-theme",cur);}catch(e){}
    setThemeLabel();
  });
  // mobile TOC drawer
  var tg=document.getElementById("toc-toggle"), toc=document.getElementById("toc");
  function closeToc(restore){root.classList.remove("toc-open");if(tg)tg.setAttribute("aria-expanded","false");var s=document.querySelector(".toc-scrim");if(s)s.remove();if(restore&&tg)tg.focus();}
  if(tg)tg.addEventListener("click",function(){
    if(root.classList.contains("toc-open")){closeToc(false);return;}
    root.classList.add("toc-open");
    tg.setAttribute("aria-expanded","true");
    var s=document.createElement("div");s.className="toc-scrim";s.addEventListener("click",function(){closeToc(false);});document.body.appendChild(s);
  });
  toc&&toc.addEventListener("click",function(e){if(e.target.closest(".toc-link"))closeToc(false);});
  document.addEventListener("keydown",function(e){if(e.key==="Escape"&&root.classList.contains("toc-open"))closeToc(true);});
  // progress bar
  var bar=document.getElementById("progress");
  function onScroll(){
    var h=document.documentElement;var max=h.scrollHeight-h.clientHeight;
    bar.style.width=(max>0?(h.scrollTop/max*100):0)+"%";
  }
  window.addEventListener("scroll",onScroll,{passive:true});onScroll();
  // scroll-spy: highlight current chapter in TOC
  var links={};document.querySelectorAll(".toc-link").forEach(function(a){links[a.dataset.target]=a;});
  if("IntersectionObserver" in window){
    var io=new IntersectionObserver(function(es){
      es.forEach(function(en){
        if(en.isIntersecting){
          var a=links[en.target.id];if(!a)return;
          document.querySelectorAll(".toc-link.is-active").forEach(function(x){x.classList.remove("is-active");});
          a.classList.add("is-active");
          a.scrollIntoView({block:"nearest"});
        }
      });
    },{rootMargin:"-15% 0px -75% 0px"});
    document.querySelectorAll("section.chapter").forEach(function(s){io.observe(s);});
  }
})();
</script>
<script defer src="/assets/js/workflowy-outline.js"></script>
<script defer src="/assets/js/atlas-drawer.js"></script>
<script defer src="/assets/js/book-ai.js"></script>
</body>
</html>
"""

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify deterministic output without writing")
    args = parser.parse_args()
    raise SystemExit(build(check=args.check))
