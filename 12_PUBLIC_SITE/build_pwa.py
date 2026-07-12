#!/usr/bin/env python3
"""PWA layer builder for 12_PUBLIC_SITE (receipt 124).

Idempotent. Generates:
  - assets/icons/{icon-192,icon-512,maskable-512,apple-touch-icon}.png
    (the compass emblem: signal-yellow circle + crosshair + bindu on near-black)
  - manifest.webmanifest
  - sw.js (versioned precache of the spine + offline fallback + SWR runtime)
  - assets/js/pwa.js (registration)
  - offline/index.html
Then injects one marked head block into every public page missing it:
  manifest link, theme-color, apple-touch-icon, pwa.js.
Safe to re-run; the <!-- pwa-chrome --> marker prevents duplicates.
"""
import os, re, json, datetime

BASE = os.path.dirname(os.path.abspath(__file__))
SKIP_DIRS = {"node_modules", "vendor", ".git", ".vercel", ".next",
             "90_ARCHIVE", "_archive", "_STAGING_COMPASS_RESTRUCTURE",
             "book-pwa", "partials", "__pycache__"}
MARKER = "<!-- pwa-chrome -->"
VOID = (5, 5, 5)          # #050505
GOLD = (255, 235, 59)     # #FFEB3B

HEAD_BLOCK = (
    f"{MARKER}\n"
    '<link rel="manifest" href="/manifest.webmanifest">\n'
    '<meta name="theme-color" content="#050505">\n'
    '<link rel="apple-touch-icon" href="/assets/icons/apple-touch-icon.png">\n'
    '<script src="/assets/js/pwa.js" defer></script>\n'
)


def draw_emblem(size, pad_ratio=0.0):
    """The compass emblem (matches the inline SVG favicon geometry)."""
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
        "name": "Emergentism — A Compass, Not a Cathedral",
        "short_name": "Emergentism",
        "description": "A navigational instrument assembled from constraints. Tier-honest claims, published poisons, visible exit.",
        "id": "/compass/",
        "start_url": "/compass/",
        "scope": "/",
        "display": "standalone",
        "background_color": "#050505",
        "theme_color": "#050505",
        "icons": [
            {"src": "/assets/icons/icon-192.png", "sizes": "192x192", "type": "image/png"},
            {"src": "/assets/icons/icon-512.png", "sizes": "512x512", "type": "image/png"},
            {"src": "/assets/icons/maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
        ],
    }
    with open(os.path.join(BASE, "manifest.webmanifest"), "w") as fh:
        json.dump(manifest, fh, indent=1)
    print("manifest.webmanifest written")


def build_sw():
    version = datetime.date.today().strftime("%Y%m%d") + "a"
    sw = """// Emergentism PWA service worker — receipt 124. Precache the spine; SWR runtime; offline fallback.
const CACHE = 'emergentism-__VERSION__';
const SPINE = [
  '/compass/', '/journey/', '/map/', '/halahala/', '/test/', '/build/', '/exit/',
  '/five-plus-one/', '/amrita/', '/offline/',
  '/manifest.webmanifest',
  '/assets/css/xai.css', '/amrita/amrita.css',
  '/assets/fonts/Roboto-latin.woff2', '/assets/fonts/RobotoMono-latin.woff2',
  '/assets/icons/icon-192.png',
];
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
  if (req.method !== 'GET' || new URL(req.url).origin !== location.origin) return;
  if (req.mode === 'navigate') {
    e.respondWith((async () => {
      try {
        const net = await fetch(req);
        const c = await caches.open(CACHE);
        c.put(req, net.clone());
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
      caches.open(CACHE).then((c) => c.put(req, net.clone()));
      return net.clone();
    }).catch(() => null);
    return cached || (await refresh) || Response.error();
  })());
});
""".replace("__VERSION__", version)
    with open(os.path.join(BASE, "sw.js"), "w") as fh:
        fh.write(sw)
    print(f"sw.js written (cache emergentism-{version})")


def build_register():
    js_dir = os.path.join(BASE, "assets", "js")
    os.makedirs(js_dir, exist_ok=True)
    with open(os.path.join(js_dir, "pwa.js"), "w") as fh:
        fh.write(
            "// PWA registration — receipt 124\n"
            "if ('serviceWorker' in navigator) {\n"
            "  window.addEventListener('load', function () {\n"
            "    navigator.serviceWorker.register('/sw.js').catch(function () {});\n"
            "  });\n"
            "}\n"
        )
    print("assets/js/pwa.js written")


def build_offline():
    d = os.path.join(BASE, "offline")
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "index.html"), "w") as fh:
        fh.write("""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Offline — Emergentism</title>
<style>
  body{margin:0;background:#050505;color:#F3F4F6;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
       min-height:100vh;display:grid;place-items:center;text-align:center;padding:24px}
  .dot{width:14px;height:14px;border-radius:50%;background:#FFEB3B;margin:0 auto 18px}
  h1{font-size:1.6rem;font-weight:600;margin:0 0 10px}
  p{color:#9CA3AF;max-width:44ch;line-height:1.6}
  a{color:#FFEB3B;text-decoration:none}
</style>
</head>
<body>
<div>
  <div class="dot"></div>
  <h1>You are offline. <span style="font-family:monospace;font-size:.55em;background:#16281b;color:#5fbf7f;padding:2px 7px;border-radius:4px;vertical-align:middle">[A]</span></h1>
  <p>The one claim on this page, verifiable by direct observation — Pratyakṣa. The compass spine is cached and still works: <a href="/compass/">compass</a> · <a href="/journey/">journey</a> · <a href="/map/">map</a> · <a href="/halahala/">halāhala</a> · <a href="/test/">test</a> · <a href="/build/">build</a> · <a href="/exit/">exit</a>. Everything else returns when you do.</p>
</div>
</body>
</html>
""")
    print("offline/index.html written")


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


if __name__ == "__main__":
    build_icons()
    build_manifest()
    build_sw()
    build_register()
    build_offline()
    inject_heads()
    print("PWA layer complete.")
