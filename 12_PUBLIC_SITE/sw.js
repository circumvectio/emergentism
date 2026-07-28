// Emergentism PWA service worker — receipt 124. Precache the spine; SWR runtime; offline fallback.
const CACHE = 'emergentism-20260728b';
const SPINE = [
  '/compass/', '/journey/', '/map/', '/halahala/', '/test/', '/build/', '/exit/',
  '/amrita/', '/offline/',
  '/manifest.webmanifest',
  '/assets/css/xai.css', '/amrita/amrita.css',
  '/assets/fonts/Roboto-latin.woff2', '/assets/fonts/RobotoMono-latin.woff2',
  '/assets/icons/icon-192.png',
];
const WITHHELD_ROUTES = new Set([
  '/historical-boundary/',
  '/app', '/app/', '/app.html',
  '/complete-ontology', '/complete-ontology/', '/complete-ontology/index.html',
  '/five-plus-one', '/five-plus-one/', '/five-plus-one/index.html',
  '/burrisphere', '/burrisphere/', '/burrisphere/index.html',
  '/dasein', '/dasein/', '/dasein/index.html',
  '/canon/the-complete-ontology-of-reality', '/canon/the-complete-ontology-of-reality/', '/canon/the-complete-ontology-of-reality/index.html',
  '/operators/mf-283-the-orthogonality-theorem-v2', '/operators/mf-283-the-orthogonality-theorem-v2/', '/operators/mf-283-the-orthogonality-theorem-v2/index.html',
  '/operators/mf-285-dreams-are-unanchored-d5', '/operators/mf-285-dreams-are-unanchored-d5/', '/operators/mf-285-dreams-are-unanchored-d5/index.html',
  '/operators/mf-296-gravity-is-time', '/operators/mf-296-gravity-is-time/', '/operators/mf-296-gravity-is-time/index.html',
  '/operators/mf-298-dark-matter-is-mutual-information', '/operators/mf-298-dark-matter-is-mutual-information/', '/operators/mf-298-dark-matter-is-mutual-information/index.html',
]);
const isWithheldRoute = (pathname) => WITHHELD_ROUTES.has(pathname);
const isStorable = (response) => !/\bno-store\b/i.test(response.headers.get('Cache-Control') || '');
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
  if (isWithheldRoute(new URL(req.url).pathname)) {
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
