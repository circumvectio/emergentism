#!/usr/bin/env python3
"""Deterministic PWA core builder for the current public projection.

By default, generates only the bounded files owned by this builder:
  - manifest.webmanifest
  - sw.js (content-versioned current-surface precache + offline fallback)
  - offline/index.html

Icon generation, registration-script generation, and page-head injection are
explicit opt-ins. This prevents a routine core rebuild from rewriting public
pages owned elsewhere.
"""
import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = Path(BASE)
PARITY_MANIFEST = ROOT / "public_semantic_parity.json"
WITHHELD_REGISTRY = ROOT / "withheld-routes.json"
SKIP_DIRS = {"node_modules", "vendor", ".git", ".vercel", ".next",
             "90_ARCHIVE", "_archive", "_STAGING_COMPASS_RESTRUCTURE",
             "book-pwa", "partials", "__pycache__"}
MARKER = "<!-- pwa-chrome -->"
VOID = (7, 10, 18)        # #070A12
GOLD = (240, 200, 90)     # #F0C85A

HEAD_BLOCK = (
    f"{MARKER}\n"
    '<link rel="manifest" href="/manifest.webmanifest">\n'
    '<meta name="theme-color" content="#070A12">\n'
    '<link rel="apple-touch-icon" href="/assets/icons/apple-touch-icon.png">\n'
    '<script src="/assets/js/pwa.js" defer></script>\n'
)


def draw_emblem(size, pad_ratio=0.0):
    """The current boundary emblem (matches the inline SVG favicon geometry)."""
    from PIL import Image, ImageDraw
    S = 1024
    img = Image.new("RGB", (S, S), VOID)
    d = ImageDraw.Draw(img)
    pad = int(S * pad_ratio)
    span = S - 2 * pad
    cx = cy = S // 2
    r = int(span * 13 / 32)
    w_ring = max(2, int(span * 2 / 32))
    w_line = max(1, int(span * 1 / 32))
    r_dot = int(span * 2.6 / 32)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=GOLD, width=w_ring)
    a = int(span * 13 / 32)
    line_gold = tuple(int(c * 0.55 + VOID[i] * 0.45) for i, c in enumerate(GOLD))
    d.line([cx, cy - a, cx, cy + a], fill=line_gold, width=w_line)
    d.line([cx - a, cy, cx + a, cy], fill=line_gold, width=w_line)
    d.ellipse([cx - r_dot, cy - r_dot, cx + r_dot, cy + r_dot], fill=GOLD)
    from PIL import Image as I
    return img.resize((size, size), I.LANCZOS)


def build_icons():
    icon_dir = os.path.join(BASE, "assets", "icons")
    os.makedirs(icon_dir, exist_ok=True)
    draw_emblem(192).save(os.path.join(icon_dir, "icon-192.png"))
    draw_emblem(512).save(os.path.join(icon_dir, "icon-512.png"))
    draw_emblem(512, pad_ratio=0.12).save(os.path.join(icon_dir, "maskable-512.png"))
    draw_emblem(180).save(os.path.join(icon_dir, "apple-touch-icon.png"))
    print("icons: 4 written")


def build_manifest():
    manifest = {
        "name": "Emergentism — A Worldview for Finite Beings",
        "short_name": "Emergentism",
        "description": "A corrigible worldview for finite beings, with Finity as a practice for one accountable next move.",
        "id": "/",
        "start_url": "/",
        "scope": "/",
        "display": "standalone",
        "background_color": "#070A12",
        "theme_color": "#070A12",
        "icons": [
            {"src": "/assets/icons/icon-192.png", "sizes": "192x192", "type": "image/png"},
            {"src": "/assets/icons/icon-512.png", "sizes": "512x512", "type": "image/png"},
            {"src": "/assets/icons/maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
        ],
    }
    (ROOT / "manifest.webmanifest").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8",
    )
    print("manifest.webmanifest written")


def route_to_artifact(route: str) -> str:
    if route == "/":
        return "index.html"
    clean = route.lstrip("/")
    if route.endswith("/"):
        return f"{clean}index.html"
    return clean


def safe_spine() -> list[str]:
    parity = json.loads(PARITY_MANIFEST.read_text(encoding="utf-8"))
    withheld = json.loads(WITHHELD_REGISTRY.read_text(encoding="utf-8"))
    frozen = set(parity["frozenLibraryRoots"])
    frozen_legacy_artifacts = set(parity.get("frozenLegacySurfaces", []))
    frozen_legacy_routes = {
        "/" + (str(Path(artifact).parent) if Path(artifact).name == "index.html" else str(Path(artifact).with_suffix("")))
        for artifact in frozen_legacy_artifacts
    }
    withheld_artifacts = {item["artifact"] for item in withheld["artifacts"]}
    withheld_routes = {
        route.rstrip("/") or "/"
        for item in withheld["artifacts"]
        for route in item["publicRoutes"]
    }
    spine = [
        "/", "/practice/", "/plainly/", "/book/", "/spark/", "/llms.txt", "/record/",
        "/record/problems/", "/record/problems.json", "/record/frontier/", "/record/frontier.json",
        "/manifesto/", "/established/",
        "/map/", "/lab/", "/contribute/", "/about/", "/exit/", "/offline/",
        "/manifest.webmanifest", "/assets/css/living-map.css",
        "/assets/js/living-map.js", "/living-map.json",
        "/public_semantic_parity.json", "/atlas/site_index.json",
        "/assets/fonts/Roboto-latin.woff2",
        "/assets/fonts/RobotoMono-latin.woff2", "/assets/icons/icon-192.png",
    ]
    for route in spine:
        artifact = route_to_artifact(route)
        root_name = artifact.split("/", 1)[0]
        normalized_route = route.rstrip("/") or "/"
        if (
            root_name in frozen
            or artifact in frozen_legacy_artifacts
            or normalized_route in frozen_legacy_routes
            or artifact in withheld_artifacts
            or normalized_route in withheld_routes
        ):
            raise ValueError(f"PWA spine includes frozen or withheld route: {route}")
        if not (ROOT / artifact).is_file() and artifact not in {
            "manifest.webmanifest", "offline/index.html",
        }:
            raise FileNotFoundError(f"PWA spine artifact is missing: {artifact}")
    return spine


def public_withheld_routes() -> list[str]:
    registry = json.loads(WITHHELD_REGISTRY.read_text(encoding="utf-8"))
    routes = {registry["boundary"]["publicRoute"]}
    for item in registry["artifacts"]:
        routes.update(item["publicRoutes"])
    return sorted(routes)


def content_version(spine: list[str]) -> str:
    digest = hashlib.sha256()
    # Withholding changes must rotate the cache even when every spine byte is
    # unchanged, so activation can delete caches that may contain newly
    # withheld historical routes.
    digest.update(b"withheld-routes.json\0")
    digest.update(WITHHELD_REGISTRY.read_bytes())
    for route in spine:
        artifact = ROOT / route_to_artifact(route)
        digest.update(route.encode("utf-8"))
        if artifact.is_file():
            digest.update(artifact.read_bytes())
    return digest.hexdigest()[:12]


def build_sw():
    spine = safe_spine()
    withheld_routes = public_withheld_routes()
    version = content_version(spine)
    sw = """// Emergentism PWA service worker — 124_PRIME_TIME_PWA_STAKEHOLDER_AUDIT_SHIP.md. Precache the spine; SWR runtime; offline fallback.
const CACHE = 'emergentism-__VERSION__';
const SPINE = __SPINE__;
const WITHHELD_ROUTES = new Set(__WITHHELD_ROUTES__);
const isWithheldRoute = (pathname) => WITHHELD_ROUTES.has(pathname);
const isStorable = (response) => !/\\bno-store\\b/i.test(response.headers.get('Cache-Control') || '');
self.addEventListener('install', (e) => {
  e.waitUntil((async () => {
    const c = await caches.open(CACHE);
    await Promise.allSettled(SPINE.map((u) => c.add(u)));
    self.skipWaiting();
  })());
});
self.addEventListener('activate', (e) => {
  e.waitUntil((async () => {
    for (const k of await caches.keys()) if (k !== CACHE) await caches.delete(k);
    await self.clients.claim();
  })());
});
self.addEventListener('fetch', (e) => {
  const req = e.request;
  const url = new URL(req.url);
  if (req.method !== 'GET' || url.origin !== location.origin) return;
  if (isWithheldRoute(url.pathname)) {
    e.respondWith(fetch(req, { cache: 'no-store' }).catch(() => new Response(
      'This historical route is withheld from public delivery.',
      {
        status: 503,
        headers: {
          'Cache-Control': 'no-store, max-age=0',
          'Content-Type': 'text/plain; charset=utf-8',
          'X-Robots-Tag': 'noindex, noarchive, nosnippet, nofollow',
        },
      },
    )));
    return;
  }
  if (req.mode === 'navigate') {
    e.respondWith((async () => {
      try {
        const net = await fetch(req);
        if (isStorable(net)) {
          const c = await caches.open(CACHE);
          c.put(req, net.clone());
        }
        return net;
      } catch {
        return (await caches.match(req)) || (await caches.match('/offline/')) || Response.error();
      }
    })());
    return;
  }
  e.respondWith((async () => {
    const cached = await caches.match(req);
    const refresh = fetch(req).then((net) => {
      if (isStorable(net)) caches.open(CACHE).then((c) => c.put(req, net.clone()));
      return net.clone();
    }).catch(() => null);
    return cached || (await refresh) || Response.error();
  })());
});
""".replace("__VERSION__", version).replace("__SPINE__", json.dumps(spine, indent=2)).replace(
        "__WITHHELD_ROUTES__", json.dumps(withheld_routes, indent=2)
    )
    (ROOT / "sw.js").write_text(sw, encoding="utf-8")
    print(f"sw.js written (cache emergentism-{version})")


def build_register():
    js_dir = os.path.join(BASE, "assets", "js")
    os.makedirs(js_dir, exist_ok=True)
    with open(os.path.join(js_dir, "pwa.js"), "w") as fh:
        fh.write(
            "// PWA registration — 124_PRIME_TIME_PWA_STAKEHOLDER_AUDIT_SHIP.md\n"
            "if ('serviceWorker' in navigator) {\n"
            "  window.addEventListener('load', function () {\n"
            "    navigator.serviceWorker.register('/sw.js').catch(function () {});\n"
            "  });\n"
            "}\n"
        )
    print("assets/js/pwa.js written")


def build_offline():
    # THIS GENERATOR OWNS offline/index.html — it overwrites the file wholesale.
    #
    # 2026-07-31: it therefore also owns ruling Q4's INFRASTRUCTURE declaration, which was
    # hand-added to the OUTPUT and silently deleted the next time this script ran. The gate
    # did not catch the loss: it tripped only on the derived sw.js hash and the social card,
    # both of which a developer fixes by running the rebuild the error message suggests —
    # after which the gate goes green with a signed ruling reverted.
    #
    # An owned file may only be edited HERE. check_q4_declarations.py now asserts this
    # block survives, so the property is tested rather than merely present.
    # Receipt: 11_UPLINK/50_AUDITS_AND_EXECUTIONS/232_FIVE_RULINGS_EXECUTED_2026_07_31.md
    d = os.path.join(BASE, "offline")
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as fh:
        fh.write("""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Offline — Emergentism</title>
<meta name="robots" content="noindex, follow" />
<meta name="emergentism:status" content="infrastructure; carries no doctrine; ruling Q4 2026-07-31" />
<style>
  body{margin:0;background:#070A12;color:#F5F0E6;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
       min-height:100vh;display:grid;place-items:center;text-align:center;padding:24px}
  .dot{width:14px;height:14px;border-radius:50%;background:#F0C85A;margin:0 auto 18px}
  h1{font-size:1.6rem;font-weight:600;margin:0 0 10px}
  p{color:#9CA3AF;max-width:44ch;line-height:1.6}
  a{color:#F0C85A;text-decoration:none}
  .q4decl{width:min(74ch,calc(100% - 40px));margin:0 auto 22px;padding:.72rem .95rem;font-size:.76rem;
    line-height:1.6;color:#c9c3b4;background:rgba(138,133,119,.07);border:1px solid rgba(138,133,119,.4);
    border-left-width:3px;border-radius:6px;text-align:left;
    font-family:ui-monospace,"SF Mono",Menlo,Consolas,monospace}
  .q4decl b{color:#a9a394;letter-spacing:.04em}
</style>
<link rel="stylesheet" href="../assets/css/a11y.css">
</head>
<body>
<a class="skip-to-content" href="#main">Skip to content</a>
<main id="main">
<div>
  <aside class="q4decl q4infra" role="note" aria-label="publication status">
    <b>INFRASTRUCTURE</b> &mdash; a service&#8209;worker fallback. It carries no doctrine and
    holds no claim, and it must not acquire standing by being frozen. Ruling Q4, signed
    2026&#8209;07&#8209;31.
  </aside>
  <div class="dot"></div>
  <h1>You are offline. <span style="font-family:monospace;font-size:.55em;background:#16281b;color:#5fbf7f;padding:2px 7px;border-radius:4px;vertical-align:middle">[A]</span></h1>
  <p>The one claim on this page is available by direct observation: you are offline. The current worldview and practice routes remain available: <a href="/">home</a> · <a href="/practice/">Finity practice</a> · <a href="/book/">book</a> · <a href="/spark/">spark</a> · <a href="/record/">record</a> · <a href="/exit/">exit</a>. Everything else returns when you do.</p>
</div>
</main>
</body>
</html>
""")
    print("offline/index.html written (with the Q4 INFRASTRUCTURE declaration)")


def public_pages():
    out = []
    for root, dirs, files in os.walk(BASE):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            if f.endswith(".html"):
                out.append(os.path.join(root, f))
    return out


def inject_heads():
    injected = skipped = no_head = 0
    for path in public_pages():
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            body = fh.read()
        if MARKER in body:
            skipped += 1
            continue
        m = re.search(r"</head>", body, flags=re.IGNORECASE)
        if not m:
            no_head += 1
            continue
        body = body[: m.start()] + HEAD_BLOCK + body[m.start():]
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(body)
        injected += 1
    print(f"head injection: {injected} injected, {skipped} already had it, {no_head} without </head>")


def parse_args(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--icons", action="store_true", help="regenerate icon assets")
    parser.add_argument("--register", action="store_true", help="regenerate the service-worker registration script")
    parser.add_argument("--inject-heads", action="store_true", help="inject PWA head markup into public HTML pages")
    parser.add_argument("--all", action="store_true", help="run all optional generators and injection")
    return parser.parse_args(argv)


def main(argv) -> int:
    args = parse_args(argv)
    if args.all or args.icons:
        build_icons()
    build_manifest()
    build_offline()
    build_sw()
    if args.all or args.register:
        build_register()
    if args.all or args.inject_heads:
        inject_heads()
    print("PWA layer complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
