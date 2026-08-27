#!/usr/bin/env python3
"""Render outline.json to /outline/index.html — the cartographic spine.

WorkFlowy grammar per D-20: branch ring and leaf dot, disclosure, summaries,
breadcrumb focus, current-route state. This is a LOCAL ADAPTATION of that
grammar; <sky-outline-nav> remains specification-only and is not implemented
here.

Disclosure depth carries the three scripts:
  collapsed        -> fable    (the node's one line)
  expanded         -> plainly  (what it says and why it matters)
  fully expanded   -> record   (tier, owner, convergence, forbidden)

The tier mark is the legend. It is never dropped.

    python3 -B 12_PUBLIC_SITE/build_outline.py            # write
    python3 -B 12_PUBLIC_SITE/build_outline.py --check    # verify, no write
"""

from __future__ import annotations

import argparse
import html
import json
import sys
from pathlib import Path

SITE = Path(__file__).resolve().parent
DATA = SITE / "outline.json"
OUT = SITE / "outline" / "index.html"

# Tier labels are NOT hardcoded here. They are read from outline.json's legend,
# so the page and the data can never disagree about what a tier means — and so
# that the amended spec's rule ("a tier is not a distortion metric") has exactly
# one place to be true.
TIER_LABEL: dict[str, str] = {}


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def tier_chip(tier: str | None) -> str:
    """The legend mark. A node without a tier renders no chip rather than a blank one."""
    if not tier:
        return ""
    label = TIER_LABEL.get(tier, "")
    return (
        f'<span class="o-tier o-tier--{esc(tier.lower())}" '
        f'title="{esc(label)}">[{esc(tier)}]</span>'
    )


def render_list(items: list[str], klass: str, heading: str) -> str:
    if not items:
        return ""
    lis = "".join(f"<li>{esc(x)}</li>" for x in items)
    return (
        f'<div class="o-{klass}"><h4>{esc(heading)}</h4><ul>{lis}</ul></div>'
    )


def render_node(node: dict, depth: int = 0) -> str:
    kind = node.get("kind", "leaf")
    label = node.get("label", "")
    route = node.get("route")
    fable = node.get("fable", "")
    plainly = node.get("plainly", "")
    children = node.get("children", [])

    marker = "○" if kind == "branch" else "·"
    marker_cls = "o-ring" if kind == "branch" else "o-dot"

    title = esc(label)
    if route:
        title = f'<a class="o-route" href="{esc(route)}">{title}</a>'

    # The record layer: only rendered when the node actually carries it.
    record = "".join(
        [
            render_list(node.get("convergence", []), "convergence", "Also arrived here"),
            render_list(node.get("forbidden", []), "forbidden", "Forbidden here"),
            (
                f'<p class="o-crossing"><span>Crossing out</span> {esc(node["crossing"])}</p>'
                if node.get("crossing")
                else ""
            ),
            (
                f'<p class="o-owner"><span>Source owner</span> <code>{esc(node["owner"])}</code></p>'
                if node.get("owner")
                else ""
            ),
        ]
    )

    kids = "".join(render_node(c, depth + 1) for c in children)

    record_block = f'<div class="o-record">{record}</div>' if record else ""
    kids_block = f'<div class="o-children">{kids}</div>' if kids else ""
    node_id = esc(node.get("id", ""))
    chip = tier_chip(node.get("tier"))

    inner = f'<p class="o-plainly">{esc(plainly)}</p>{record_block}{kids_block}'

    return (
        f'<details class="o-node o-node--{esc(kind)}" data-depth="{depth}" data-id="{node_id}">'
        f'<summary><span class="{marker_cls}" aria-hidden="true">{marker}</span>'
        f'<span class="o-label">{title}</span>{chip}'
        f'<span class="o-fable">{esc(fable)}</span></summary>'
        f"{inner}</details>"
    )


def render(data: dict) -> str:
    root = data["root"]
    legend = data["legend"]
    tiers = "".join(
        f'<li><span class="o-tier o-tier--{esc(k.lower())}">[{esc(k)}]</span> {esc(v)}</li>'
        for k, v in legend["tiers"].items()
    )
    not_claimed = "".join(f"<li>{esc(x)}</li>" for x in legend["notClaimed"])
    branches = "".join(render_node(c) for c in root["children"])

    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>The map and its legend · Emergentism</title>
<meta name="description" content="{esc(legend['principle'])}">
<link rel="stylesheet" href="/assets/css/xai.css">
<link rel="stylesheet" href="/assets/css/outline.css">
</head>
<body class="g2-page g2-outline">
<a class="skip" href="#main">Skip to content</a>
<main id="main" class="o-main">

<header class="o-head">
  <p class="o-glyph" aria-hidden="true">{esc(root['glyph'])}</p>
  <h1>{esc(root['fable'])}</h1>
  <p class="o-lede">{esc(root['plainly'])}</p>
</header>

<section class="o-legend" aria-labelledby="legend-title">
  <h2 id="legend-title">The legend</h2>
  <p>{esc(legend['principle'])}</p>
  <p class="o-fence">{esc(legend['fence'])}</p>
  <ul class="o-tierkey">{tiers}</ul>
  <details class="o-notclaimed"><summary>What this map does not claim</summary>
    <ul>{not_claimed}</ul>
  </details>
</section>

<section class="o-tree" aria-labelledby="tree-title">
  <h2 id="tree-title">The map</h2>
  <p class="o-hint">Every node opens. Closed is the one line; open is the reading;
  fully open is the source, what else arrived there, and what is forbidden.</p>
  {branches}
</section>

<footer class="o-foot">
  <p>Structure and summaries only. Every claim's tier, rival, discriminator and
  kill live at the source owner named on the node.</p>
  <p><a href="/exit/">Exit</a></p>
</footer>

</main></body></html>
"""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify without writing")
    args = parser.parse_args(argv)

    data = json.loads(DATA.read_text(encoding="utf-8"))
    TIER_LABEL.clear()
    TIER_LABEL.update(data["legend"]["tiers"])
    page = render(data)

    # Every node must carry a tier, or the legend is a decoration.
    missing: list[str] = []

    def walk(node: dict) -> None:
        if node.get("kind") in {"branch", "leaf"} and not node.get("tier"):
            missing.append(node.get("id", "?"))
        for child in node.get("children", []):
            walk(child)

    for child in data["root"]["children"]:
        walk(child)

    if missing:
        print(f"OUTLINE: FAIL — {len(missing)} node(s) carry no tier: {', '.join(missing)}")
        return 1

    if args.check:
        if not OUT.exists():
            print("OUTLINE: FAIL — /outline/index.html not built")
            return 1
        if OUT.read_text(encoding="utf-8") != page:
            print("OUTLINE: FAIL — /outline/index.html is stale; re-run without --check")
            return 1
        print(f"OUTLINE: PASS (in sync, {len(page):,} bytes)")
        return 0

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(page, encoding="utf-8")
    print(f"OUTLINE: wrote {OUT.relative_to(SITE.parent)} ({len(page):,} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
