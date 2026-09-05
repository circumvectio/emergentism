#!/usr/bin/env python3
"""Deterministically bind the Gestalt v2 shell to core manual pages."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


SITE = Path(__file__).resolve().parent
NAV_PARTIAL = SITE / "partials" / "core-nav.html"
FOOTER_PARTIAL = SITE / "partials" / "core-footer.html"
DESIGN_CONTRACT_PATH = SITE / "emergentism-design.v2.json"

THEME_BOOT = (
    '<script data-g2-theme-boot>'
    '(function(){try{var t=localStorage.getItem("emergentism-theme");'
    'if(t==="light"||t==="dark"){document.documentElement.dataset.theme=t}}'
    'catch(e){}})();'
    '</script>'
)


def _load_design_routes() -> list[dict[str, str]]:
    try:
        payload = json.loads(DESIGN_CONTRACT_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"invalid design contract: {exc}") from exc
    if payload.get("schema") != "emergentism/PublicDesignContract.v2":
        raise ValueError("design contract schema must be emergentism/PublicDesignContract.v2")
    routes = payload.get("routes")
    if not isinstance(routes, list) or not routes:
        raise ValueError("design contract routes must be a non-empty list")
    paths = [row.get("path") for row in routes if isinstance(row, dict)]
    if len(paths) != len(routes) or len(set(paths)) != len(paths):
        raise ValueError("design contract routes must have unique string paths")
    return routes


DESIGN_ROUTES = _load_design_routes()
ALL_SURFACE_FAMILIES = {row["path"]: row["family"] for row in DESIGN_ROUTES}
CORE_ROUTES = [row for row in DESIGN_ROUTES if row.get("shell") == "core"]
CORE_PAGES = {row["path"]: row["navigationSection"] for row in CORE_ROUTES}
EXACT_NAV_HREFS = {
    row["path"]: row["canonicalHref"]
    for row in CORE_ROUTES
    if row.get("canonicalHref")
}
SURFACE_FAMILIES = {row["path"]: row["family"] for row in CORE_ROUTES}


def surface_for(path: str) -> str:
    """Return the design-contract family for one declared current route."""
    try:
        return ALL_SURFACE_FAMILIES[path]
    except KeyError as exc:
        raise ValueError(f"route is absent from the design contract: {path}") from exc

NAV_RE = re.compile(
    r"<!-- gestalt-core-nav:start -->.*?<!-- gestalt-core-nav:end -->",
    re.DOTALL,
)
FOOTER_RE = re.compile(
    r"<!-- gestalt-core-footer:start -->.*?<!-- gestalt-core-footer:end -->",
    re.DOTALL,
)
LEGACY_HEADER_RE = re.compile(
    r'<header\b[^>]*class\s*=\s*(["\'])[^"\']*(?:topbar|site-head)[^"\']*\1[^>]*>.*?</header>',
    re.DOTALL | re.IGNORECASE,
)
LEGACY_PRIMARY_NAV_RE = re.compile(
    r'<nav\b[^>]*aria-label="Primary"[^>]*>.*?</nav>',
    re.DOTALL | re.IGNORECASE,
)
LEGACY_FOOTER_RE = re.compile(r"\s*<footer\b([^>]*)>.*?</footer>", re.DOTALL | re.IGNORECASE)
LEGACY_SKIP_RE = re.compile(
    r'\s*<a\b[^>]*class="[^"]*(?:skip|skip-to-content)[^"]*"[^>]*>.*?</a>',
    re.DOTALL | re.IGNORECASE,
)
LEGACY_ICON_RE = re.compile(
    r'\s*<link\b[^>]*\brel\s*=\s*["\']icon["\'][^>]*>\s*',
    re.IGNORECASE,
)


def _validate_marker_pair(text: str, kind: str, *, allow_absent: bool) -> bool:
    start = f"<!-- gestalt-core-{kind}:start -->"
    end = f"<!-- gestalt-core-{kind}:end -->"
    starts = [match.start() for match in re.finditer(re.escape(start), text)]
    ends = [match.start() for match in re.finditer(re.escape(end), text)]
    if not starts and not ends and allow_absent:
        return False
    if len(starts) != 1 or len(ends) != 1 or starts[0] >= ends[0]:
        raise ValueError(
            f"{kind} markers must be one complete ordered pair; "
            f"found starts={len(starts)} ends={len(ends)}"
        )
    return True


def _partial(path: Path, kind: str) -> str:
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        raise ValueError(f"empty shell partial: {path.relative_to(SITE)}")
    _validate_marker_pair(text, kind, allow_absent=False)
    return text


def render_nav(active: str | None = None, current_href: str | None = None) -> str:
    nav = _partial(NAV_PARTIAL, "nav")
    if active:
        nav = nav.replace(
            f'data-section="{active}"',
            f'data-section="{active}" data-current-section="true"',
        )
    if current_href:
        nav = nav.replace(
            f'href="{current_href}"',
            f'href="{current_href}" aria-current="page"',
        )
    return nav


def render_footer() -> str:
    return _partial(FOOTER_PARTIAL, "footer")


def head_assets() -> str:
    return (
        f"{THEME_BOOT}\n"
        '<link rel="icon" href="/favicon.svg" type="image/svg+xml" />\n'
        '<link rel="stylesheet" href="/assets/css/gestalt-v2.css" />\n'
        '<script defer src="/assets/js/gestalt-v2.js"></script>'
    )


def _single_close(text: str, tag: str) -> re.Match[str]:
    matches = list(re.finditer(rf"</{tag}\s*>", text, re.IGNORECASE))
    if len(matches) != 1:
        raise ValueError(f"page must have exactly one </{tag}>; found {len(matches)}")
    return matches[0]


def _insert_before_close(text: str, tag: str, insertion: str) -> str:
    close = _single_close(text, tag)
    return text[: close.start()] + insertion + "\n" + text[close.start() :]


def _bind_head(text: str, surface: str) -> str:
    _single_close(text, "head")
    canonical_icon = '<link rel="icon" href="/favicon.svg" type="image/svg+xml" />'
    if canonical_icon not in text:
        text = LEGACY_ICON_RE.sub("\n", text)
        text = _insert_before_close(text, "head", canonical_icon)
    if "/assets/css/gestalt-v2.css" not in text:
        text = _insert_before_close(
            text, "head", '<link rel="stylesheet" href="/assets/css/gestalt-v2.css" />'
        )
    if "/assets/js/gestalt-v2.js" not in text:
        text = _insert_before_close(
            text, "head", '<script defer src="/assets/js/gestalt-v2.js"></script>'
        )
    if "data-g2-theme-boot" not in text:
        text = _insert_before_close(text, "head", THEME_BOOT)
    html_matches = list(re.finditer(r"<html\b([^>]*)>", text, re.IGNORECASE))
    if len(html_matches) != 1:
        raise ValueError(f"page must have exactly one html element; found {len(html_matches)}")
    html_match = html_matches[0]
    gestalt = re.findall(
        r'\bdata-gestalt\s*=\s*["\']([^"\']+)["\']',
        html_match.group(1),
        re.IGNORECASE,
    )
    if gestalt and gestalt != ["v2"]:
        raise ValueError(f"incompatible data-gestalt value: {gestalt}")
    if not gestalt:
        text = re.sub(
            r"<html\b([^>]*)>",
            r'<html\1 data-gestalt="v2">',
            text,
            count=1,
            flags=re.IGNORECASE,
        )
    html_match = re.search(r"<html\b([^>]*)>", text, re.IGNORECASE)
    if not html_match:
        raise ValueError("page has no html element after Gestalt binding")
    design = re.findall(
        r'\bdata-emergentism-design\s*=\s*["\']([^"\']+)["\']',
        html_match.group(1),
        re.IGNORECASE,
    )
    if design and design not in (["v1"], ["v2"]):
        raise ValueError(f"incompatible data-emergentism-design value: {design}")
    if design == ["v1"]:
        text = re.sub(
            r'(\bdata-emergentism-design\s*=\s*["\'])v1(["\'])',
            r'\1v2\2',
            text,
            count=1,
            flags=re.IGNORECASE,
        )
    elif not design:
        text = re.sub(
            r"<html\b([^>]*)>",
            r'<html\1 data-emergentism-design="v2">',
            text,
            count=1,
            flags=re.IGNORECASE,
        )
    body = re.search(r"<body\b([^>]*)>", text, re.IGNORECASE)
    if not body:
        raise ValueError("page has no body")
    attrs = body.group(1)
    class_matches = list(
        re.finditer(r'\bclass\s*=\s*(["\'])(.*?)\1', attrs, re.IGNORECASE | re.DOTALL)
    )
    if len(class_matches) > 1:
        raise ValueError("body has more than one class attribute")
    classes = class_matches[0].group(2).split() if class_matches else []
    if "g2-page" not in classes:
        classes = ["g2-page", "g2-legacy", *classes]
        if class_matches:
            match = class_matches[0]
            quote = match.group(1)
            replacement = f"class={quote}{' '.join(classes)}{quote}"
            attrs = attrs[: match.start()] + replacement + attrs[match.end() :]
        else:
            attrs += ' class="' + " ".join(classes) + '"'
    surface_values = re.findall(
        r'\bdata-emergentism-surface\s*=\s*["\']([^"\']+)["\']',
        attrs,
        re.IGNORECASE,
    )
    if surface_values and surface_values != [surface]:
        raise ValueError(
            f"incompatible data-emergentism-surface value: {surface_values}; expected {surface}"
        )
    if not surface_values:
        attrs += f' data-emergentism-surface="{surface}"'
    text = text[: body.start()] + f"<body{attrs}>" + text[body.end() :]
    return text


def _bind_main_target(text: str) -> str:
    matches = list(re.finditer(r"<main\b([^>]*)>", text, re.IGNORECASE))
    if len(matches) != 1:
        raise ValueError(f"page must have exactly one main element; found {len(matches)}")
    match = matches[0]
    attrs = match.group(1)
    ids = re.findall(r'\bid=["\']([^"\']+)["\']', attrs, re.IGNORECASE)
    if ids and ids != ["main"]:
        raise ValueError(f"main element has incompatible id: {ids[0]}")
    if not ids:
        attrs += ' id="main"'
    if not re.search(r"\btabindex=", attrs, re.IGNORECASE):
        attrs += ' tabindex="-1"'
    return text[: match.start()] + f"<main{attrs}>" + text[match.end() :]


def _replace_last_legacy_footer(text: str, footer: str) -> str:
    recognized: list[re.Match[str]] = []
    for match in LEGACY_FOOTER_RE.finditer(text):
        attrs = match.group(1)
        class_match = re.search(
            r'\bclass\s*=\s*(["\'])(.*?)\1', attrs, re.IGNORECASE | re.DOTALL
        )
        classes = set(class_match.group(2).split()) if class_match else set()
        if classes & {"site-footer", "foot", "footer"}:
            recognized.append(match)
    if len(recognized) > 1:
        raise ValueError("page has more than one recognized legacy site footer")
    if not recognized:
        return _insert_before_close(text, "body", footer)
    match = recognized[0]
    return text[: match.start()] + "\n" + footer + text[match.end() :]


def render_page(
    text: str,
    active: str,
    current_href: str | None = None,
    surface: str = "atlas",
) -> str:
    _single_close(text, "body")
    has_nav = _validate_marker_pair(text, "nav", allow_absent=True)
    has_footer = _validate_marker_pair(text, "footer", allow_absent=True)
    text = _bind_head(text, surface)
    text = _bind_main_target(text)
    nav = render_nav(active, current_href)
    footer = render_footer()

    if has_nav:
        text = NAV_RE.sub(nav, text, count=1)
    else:
        text = LEGACY_SKIP_RE.sub("", text, count=1)
        if LEGACY_HEADER_RE.search(text):
            text = LEGACY_HEADER_RE.sub(nav, text, count=1)
        elif LEGACY_PRIMARY_NAV_RE.search(text):
            text = LEGACY_PRIMARY_NAV_RE.sub(nav, text, count=1)
        else:
            text = re.sub(r"(<body\b[^>]*>)", rf"\1\n{nav}", text, count=1, flags=re.I)

    if has_footer:
        text = FOOTER_RE.sub(footer, text, count=1)
    else:
        text = _replace_last_legacy_footer(text, footer)

    _validate_marker_pair(text, "nav", allow_absent=False)
    _validate_marker_pair(text, "footer", allow_absent=False)
    return text


def outputs() -> dict[Path, str]:
    rendered: dict[Path, str] = {}
    for rel, active in CORE_PAGES.items():
        path = SITE / rel
        if not path.is_file():
            raise ValueError(f"core shell page is missing: {rel}")
        rendered[path] = render_page(
            path.read_text(encoding="utf-8"),
            active,
            EXACT_NAV_HREFS.get(rel),
            SURFACE_FAMILIES[rel],
        )
    return rendered


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail on byte drift")
    args = parser.parse_args()
    try:
        rendered = outputs()
    except ValueError as exc:
        print(f"CORE SHELL: FAIL\n- {exc}")
        return 1

    drift: list[str] = []
    for path, content in rendered.items():
        if args.check:
            if path.read_text(encoding="utf-8") != content:
                drift.append(str(path.relative_to(SITE)))
        else:
            path.write_text(content, encoding="utf-8")
    if drift:
        print("CORE SHELL: FAIL")
        for rel in drift:
            print(f"- drift: {rel}")
        return 1
    print(f"CORE SHELL: PASS ({len(rendered)} pages; {'clean' if args.check else 'rendered'})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
