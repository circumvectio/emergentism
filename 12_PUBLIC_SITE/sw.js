// Emergentism PWA service worker — receipt 124. Precache the spine; SWR runtime; offline fallback.
const CACHE = 'emergentism-20260712a';
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
