#!/usr/bin/env python3
"""Deterministically render the dimension-first public spine from its parity manifest."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path


SITE = Path(__file__).resolve().parent
MANIFEST = SITE / "public_semantic_parity.json"


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def pretty_id(value: str) -> str:
    return value.replace("mu", "μ")


def field(label: str, value: str) -> str:
    return f"<dt>{esc(label)}</dt><dd>{esc(value)}</dd>"


def transition_card(item: dict) -> str:
    if "transition" not in item:
        ret = item["return"]
        return f"""
<section class="transition" id="{esc(ret['id'])}">
  <p class="eyebrow">{esc(ret['id'])} · {esc(ret['tier'])} · non-causal interpretive edge</p>
  <h2>{esc(ret['label'])}</h2>
  <p>{esc(ret['meaning'])}</p>
  <a class="next" href="../0/">Return to D0 as a reader, not as an identity →</a>
</section>"""
    tr = item["transition"]
    next_index = int(item["id"][1:]) + 1
    next_href = f"../{next_index}/"
    if tr["id"] == "b6":
        next_href = "../6/"
    rows = "".join(
        field(label, tr[key])
        for label, key in (
            ("Saturation proposal", "saturation"),
            ("New capability", "capability"),
            ("Lower-level recovery", "recovery"),
            ("Evidence", "evidence"),
            ("Prediction", "prediction"),
            ("Alternatives", "alternatives"),
            ("Kill criterion", "kill"),
        )
    )
    kind = "candidate μ-crossing" if tr["id"].startswith("mu") else "non-μ boundary"
    return f"""
<section class="transition" id="{esc(tr['id'])}">
  <p class="eyebrow">{esc(pretty_id(tr['id']))} · {kind}</p>
  <h2>{esc(tr['label'])}</h2>
  <dl>{rows}</dl>
  <p class="source">Source owner: <code>{esc(tr['source'])}</code></p>
  <a class="next" href="{next_href}">Continue through {esc(pretty_id(tr['id']))} →</a>
</section>"""


def page(item: dict, prev_id: str | None, next_id: str | None) -> str:
    ident = item["id"]
    number = ident[1:]
    prev_link = f'<a href="../{prev_id[1:]}/">← {prev_id}</a>' if prev_id else '<a href="../dimensions/">← Spine</a>'
    next_link = f'<a href="../{next_id[1:]}/">{next_id} →</a>' if next_id else '<a href="../dimensions/">Spine →</a>'
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>/{number} — {esc(item['title'])} · Emergentism</title>
<meta name="description" content="{esc(item['summary'])}" />
<link rel="icon" href="data:," />
<link rel="stylesheet" href="../assets/css/xai.css" />
<link rel="stylesheet" href="../dimensions/dimensions.css" />
<script type="importmap">
{{"imports":{{"three":"../vendor/three-0.160.0/three.module.js","three/addons/":"../vendor/three-0.160.0/"}}}}
</script>
<style>
main{{max-width:920px;margin:0 auto;padding:110px 22px 72px}} .hero{{padding:2rem 0 3rem;border-bottom:1px solid var(--border)}}
.eyebrow,.tier,.source{{font:700 .74rem/1.6 var(--font-mono);color:var(--gold)}} h1{{font-size:clamp(2.5rem,7vw,5.8rem);line-height:.98;margin:.6rem 0 1.2rem}}
.lede{{font-size:1.15rem;color:var(--text-muted);max-width:68ch}} .grid{{display:grid;grid-template-columns:1fr 1fr;gap:1px;background:var(--border);border:1px solid var(--border);margin:2rem 0}}
.grid article{{background:var(--surface);padding:1.35rem}} .grid p{{color:var(--text-muted)}} .diagram{{min-height:300px;display:grid;place-items:center;border:1px solid var(--border);margin:2rem 0;overflow:hidden}}
.dimension-canvas{{width:100%;height:320px}} .transition{{margin:3rem 0;padding:1.5rem;border:1px solid var(--gold);border-radius:12px;background:var(--surface)}}
dl{{display:grid;grid-template-columns:minmax(150px,.35fr) 1fr;gap:0;border-top:1px solid var(--border)}} dt,dd{{margin:0;padding:.8rem;border-bottom:1px solid var(--border)}} dt{{font:700 .75rem/1.5 var(--font-mono);color:var(--text-dim)}} dd{{color:var(--text-muted)}}
.next{{display:inline-block;margin-top:1rem;color:var(--gold)}} .pager{{display:flex;justify-content:space-between;border-top:1px solid var(--border);padding-top:1rem}} code{{overflow-wrap:anywhere}}
@media(max-width:700px){{.grid{{grid-template-columns:1fr}}dl{{grid-template-columns:1fr}}dt{{padding-bottom:.2rem}}dd{{padding-top:.2rem}}}}
</style>
</head>
<body>
<header class="topbar"><a class="brand" href="../compass/">Emergentism</a><nav class="number-nav"><a href="../dimensions/">Spine</a><a href="../check/">Check</a><a href="../record/">Record</a><a href="../exit/">Exit</a></nav></header>
<main>
<section class="hero">
  <p class="eyebrow">{esc(ident)} · {esc(item['modality'])} · {esc(item['tier'])}</p>
  <h1>{esc(item['title'])}</h1>
  <p class="lede">{esc(item['subtitle'])}. {esc(item['summary'])}</p>
</section>
<section class="grid">
  <article><h2>Inherited structure</h2><p>{esc(item['inherited'])}</p></article>
  <article><h2>Claim boundary</h2><p>{esc(item['boundary'])}</p></article>
</section>
<section class="diagram visual-panel" aria-label="Historical geometric instrument used as an illustration, not evidence or semantic authority">
  <canvas class="dimension-canvas"></canvas>
  <noscript>Illustration omitted. The text carries the claim.</noscript>
</section>
<p class="source">Semantic owner: <code>{esc(item['source'])}</code></p>
{transition_card(item)}
<nav class="pager">{prev_link}{next_link}</nav>
</main>
<footer class="site-footer">Public projection · source tiers preserved · <a href="../practice/">use the compass</a> · <a href="../exit/">put it down</a></footer>
<script>window.DIMENSION_PAGE={{animationMode:{json.dumps(item['illustrationMode'])}}};</script>
<script type="module" src="../dimensions/dimensions.js"></script>
</body>
</html>
"""


def index_page(levels: list[dict], sequence: list[str]) -> str:
    rows: list[str] = []
    for item in levels:
        n = item["id"][1:]
        rows.append(f"<a class='rung' href='../{n}/'><b>{esc(item['id'])}</b><span>{esc(item['title'])}</span><small>{esc(item['tier'])} · {esc(item['modality'])}</small></a>")
        if "transition" in item:
            tr = item["transition"]
            rows.append(f"<div class='crossing'><b>{esc(pretty_id(tr['id']))}</b><span>{esc(tr['label'])}</span><small>{'candidate crossing' if tr['id'].startswith('mu') else 'non-μ boundary'}</small></div>")
        else:
            ret = item["return"]
            rows.append(f"<div class='crossing'><b>{esc(ret['id'])}</b><span>{esc(ret['label'])}</span><small>interpretive edge only</small></div>")
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8" /><meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>The dimension-first spine · Emergentism</title><meta name="description" content="The complete typed Emergentist scaffold: D0 through D6, five candidate μ-crossings, one exit boundary, and one interpretive return." />
<link rel="icon" href="data:," /><link rel="stylesheet" href="../assets/css/xai.css" /><style>
main{{max-width:900px;margin:0 auto;padding:120px 22px 80px}} h1{{font-size:clamp(2.6rem,7vw,5.5rem);line-height:1;margin:.5rem 0 1rem}} .lede{{color:var(--text-muted);max-width:64ch;font-size:1.1rem}}
.sequence{{font:700 .72rem/1.7 var(--font-mono);color:var(--gold);overflow-wrap:anywhere}} .spine{{margin:3rem 0;border-left:1px solid var(--gold);padding-left:1.2rem}}
.rung,.crossing{{display:grid;grid-template-columns:70px 1fr auto;gap:1rem;align-items:baseline;padding:1rem;border-bottom:1px solid var(--border);text-decoration:none}} .rung:hover{{background:var(--surface)}}
.rung b{{color:var(--gold)}} .crossing{{margin-left:1.5rem;color:var(--text-muted);font-style:italic}} .crossing b{{color:var(--text-dim)}} small{{font:600 .68rem/1.4 var(--font-mono);color:var(--text-dim)}}
.contract{{border:1px solid var(--border);padding:1.3rem;background:var(--surface)}} .contract li{{margin:.55rem 0;color:var(--text-muted)}} @media(max-width:650px){{.rung,.crossing{{grid-template-columns:55px 1fr}}small{{grid-column:2}}}}
</style></head><body><header class="topbar"><a class="brand" href="../compass/">Emergentism</a><nav class="number-nav"><a href="../check/">Check</a><a href="../practice/">Practice</a><a href="../record/">Record</a><a href="../exit/">Exit</a></nav></header>
<main><p class="sequence">{esc(' → '.join(pretty_id(x) for x in sequence))}</p><h1>The dimension-first spine</h1><p class="lede">A scaffold, not a census forced on nature. Each page separates inherited mathematics or science from Emergentist interpretation, and every crossing carries a prediction and a way to fail.</p>
<section class="contract"><h2>How to read it</h2><ul><li>D4 is actual; D5 is possible. An actual D4 model token may represent D5 possible content.</li><li>μ₀…μ₄ are candidate apertures. Empty evidence remains unassessed.</li><li>b₆ and r₆ are boundary relations, not additional μ-crossings.</li><li>The matter→bond→life→mind→choice story is an optional interpretation, not the owner of the formal registers.</li></ul></section>
<section class="spine">{''.join(rows)}</section><section class="contract"><h2>Related instruments and preserved visual studies</h2><p><a href="../titans/">Titans</a> · <a href="../titans.html">Titan animation</a> · <a href="../suda/">Suda notes</a> · <a href="../egg/">The Egg</a> · <a href="../saturation/">Saturation instrument</a> · <a href="../riemann/">Riemann view</a> · <a href="../journey/">Earlier journey view</a></p><p>These are supporting projections. The typed spine above governs where they conflict.</p></section><p><a href="../0/">Begin with D0 →</a></p></main><footer class="site-footer">[I/C] scaffold · externally uncalibrated · <a href="../record/">corrections remain visible</a></footer></body></html>"""


def render() -> dict[Path, str]:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    levels = data["levels"]
    outputs: dict[Path, str] = {SITE / "dimensions" / "index.html": index_page(levels, data["sequence"])}
    for i, item in enumerate(levels):
        outputs[SITE / item["id"][1:] / "index.html"] = page(
            item,
            levels[i - 1]["id"] if i else None,
            levels[i + 1]["id"] if i + 1 < len(levels) else None,
        )
    return outputs


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    drift: list[str] = []
    for path, content in render().items():
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                drift.append(str(path.relative_to(SITE)))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
    if drift:
        print("dimension render drift:")
        print("\n".join(drift))
        return 1
    print(f"dimension site: {'clean' if args.check else 'rendered'} ({len(render())} pages)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
