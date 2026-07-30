// Emergentism PWA service worker — receipt 124. Precache the spine; SWR runtime; offline fallback.
const CACHE = 'emergentism-b3138484550d';
const SPINE = [
  "/",
  "/practice/",
  "/plainly/",
  "/book/",
  "/record/",
  "/map/",
  "/lab/",
  "/contribute/",
  "/about/",
  "/exit/",
  "/offline/",
  "/manifest.webmanifest",
  "/assets/css/living-map.css",
  "/assets/js/living-map.js",
  "/living-map.json",
  "/public_semantic_parity.json",
  "/atlas/site_index.json",
  "/assets/fonts/Roboto-latin.woff2",
  "/assets/fonts/RobotoMono-latin.woff2",
  "/assets/icons/icon-192.png"
];
const WITHHELD_ROUTES = new Set([
  "/app",
  "/app.html",
  "/app/",
  "/axiology",
  "/axiology/",
  "/axiology/index.html",
  "/burrisphere",
  "/burrisphere/",
  "/burrisphere/index.html",
  "/canon/the-burrisphere",
  "/canon/the-burrisphere/",
  "/canon/the-burrisphere/index.html",
  "/canon/the-complete-ontology-of-reality",
  "/canon/the-complete-ontology-of-reality/",
  "/canon/the-complete-ontology-of-reality/index.html",
  "/canon/the-five-plus-one-constitution",
  "/canon/the-five-plus-one-constitution/",
  "/canon/the-five-plus-one-constitution/index.html",
  "/canon/the-generative-table",
  "/canon/the-generative-table/",
  "/canon/the-generative-table/index.html",
  "/canon/the-geometric-ontology-of-reality",
  "/canon/the-geometric-ontology-of-reality/",
  "/canon/the-geometric-ontology-of-reality/index.html",
  "/canon/the-ontology-index",
  "/canon/the-ontology-index/",
  "/canon/the-ontology-index/index.html",
  "/complete-ontology",
  "/complete-ontology/",
  "/complete-ontology/index.html",
  "/dasein",
  "/dasein/",
  "/dasein/index.html",
  "/finity-papers",
  "/finity-papers/",
  "/finity-papers/index.html",
  "/five-plus-one",
  "/five-plus-one/",
  "/five-plus-one/index.html",
  "/formal/00-the-seven-axioms",
  "/formal/00-the-seven-axioms/",
  "/formal/00-the-seven-axioms/index.html",
  "/formal/11-efr-triadic-stability",
  "/formal/11-efr-triadic-stability/",
  "/formal/11-efr-triadic-stability/index.html",
  "/formal/34-d4-d5-canonical-reference",
  "/formal/34-d4-d5-canonical-reference/",
  "/formal/34-d4-d5-canonical-reference/index.html",
  "/foundations/ontology-across-dimensions",
  "/foundations/ontology-across-dimensions/",
  "/foundations/ontology-across-dimensions/index.html",
  "/foundations/the-seven-generative-actions-and-ektropy",
  "/foundations/the-seven-generative-actions-and-ektropy/",
  "/foundations/the-seven-generative-actions-and-ektropy/index.html",
  "/game",
  "/game/",
  "/game/index.html",
  "/geometric-ontology",
  "/geometric-ontology/",
  "/geometric-ontology/index.html",
  "/ground/00-d5-d6-corpus-stabilization",
  "/ground/00-d5-d6-corpus-stabilization/",
  "/ground/00-d5-d6-corpus-stabilization/index.html",
  "/ground/00-d6-as-apophatic-closure",
  "/ground/00-d6-as-apophatic-closure/",
  "/ground/00-d6-as-apophatic-closure/index.html",
  "/ground/00-ontology-across-dimensions",
  "/ground/00-ontology-across-dimensions/",
  "/ground/00-ontology-across-dimensions/index.html",
  "/ground/00-the-ontology-of-being",
  "/ground/00-the-ontology-of-being/",
  "/ground/00-the-ontology-of-being/index.html",
  "/historical-boundary/",
  "/home",
  "/home/",
  "/home/index.html",
  "/index_legacy_2026_07_19",
  "/index_legacy_2026_07_19.html",
  "/index_legacy_2026_07_19/",
  "/meta/00-corpus",
  "/meta/00-corpus/",
  "/meta/00-corpus/index.html",
  "/operators/mf-283-the-orthogonality-theorem-v2",
  "/operators/mf-283-the-orthogonality-theorem-v2/",
  "/operators/mf-283-the-orthogonality-theorem-v2/index.html",
  "/operators/mf-285-dreams-are-unanchored-d5",
  "/operators/mf-285-dreams-are-unanchored-d5/",
  "/operators/mf-285-dreams-are-unanchored-d5/index.html",
  "/operators/mf-296-gravity-is-time",
  "/operators/mf-296-gravity-is-time/",
  "/operators/mf-296-gravity-is-time/index.html",
  "/operators/mf-298-dark-matter-is-mutual-information",
  "/operators/mf-298-dark-matter-is-mutual-information/",
  "/operators/mf-298-dark-matter-is-mutual-information/index.html",
  "/operators/mf-65-curvature-transition",
  "/operators/mf-65-curvature-transition/",
  "/operators/mf-65-curvature-transition/index.html",
  "/papers/paper-c-photon-unit-of-account",
  "/papers/paper-c-photon-unit-of-account/",
  "/papers/paper-c-photon-unit-of-account/index.html",
  "/papers/paper-h-dimensional-cosmological",
  "/papers/paper-h-dimensional-cosmological/",
  "/papers/paper-h-dimensional-cosmological/index.html",
  "/paradox/00-gardener-nexus",
  "/paradox/00-gardener-nexus/",
  "/paradox/00-gardener-nexus/index.html",
  "/paradox/00-the-extraction-pattern",
  "/paradox/00-the-extraction-pattern/",
  "/paradox/00-the-extraction-pattern/index.html",
  "/paradox/pd-18-the-extraction-paradox",
  "/paradox/pd-18-the-extraction-paradox/",
  "/paradox/pd-18-the-extraction-paradox/index.html",
  "/paradox/pd-21-problem-of-death",
  "/paradox/pd-21-problem-of-death/",
  "/paradox/pd-21-problem-of-death/index.html",
  "/paradox/pd-23-the-completion",
  "/paradox/pd-23-the-completion/",
  "/paradox/pd-23-the-completion/index.html",
  "/rosettad/00-corpus",
  "/rosettad/00-corpus/",
  "/rosettad/00-corpus/index.html",
  "/rosettad/00-suda-value-extraction-deep-synthesis",
  "/rosettad/00-suda-value-extraction-deep-synthesis/",
  "/rosettad/00-suda-value-extraction-deep-synthesis/index.html",
  "/sacred/00-glossary",
  "/sacred/00-glossary/",
  "/sacred/00-glossary/index.html",
  "/soul-loop",
  "/soul-loop/",
  "/soul-loop/index.html",
  "/synthesis",
  "/synthesis/",
  "/synthesis/index.html",
  "/teleology",
  "/teleology/",
  "/teleology/index.html",
  "/trinity/00-the-genesis-simulation",
  "/trinity/00-the-genesis-simulation/",
  "/trinity/00-the-genesis-simulation/index.html",
  "/trinity/01-the-emergence",
  "/trinity/01-the-emergence/",
  "/trinity/01-the-emergence/index.html",
  "/trinity/03-the-closure",
  "/trinity/03-the-closure/",
  "/trinity/03-the-closure/index.html",
  "/trinity/04-bit-to-qubit",
  "/trinity/04-bit-to-qubit/",
  "/trinity/04-bit-to-qubit/index.html",
  "/trinity/06-the-cosmological-cycle",
  "/trinity/06-the-cosmological-cycle/",
  "/trinity/06-the-cosmological-cycle/index.html",
  "/trinity/10-the-soul-loop",
  "/trinity/10-the-soul-loop/",
  "/trinity/10-the-soul-loop/index.html",
  "/trinity/11-the-helix",
  "/trinity/11-the-helix/",
  "/trinity/11-the-helix/index.html",
  "/trinity/12-the-poles",
  "/trinity/12-the-poles/",
  "/trinity/12-the-poles/index.html",
  "/trinity/15-dharma-yuddha",
  "/trinity/15-dharma-yuddha/",
  "/trinity/15-dharma-yuddha/index.html",
  "/trinity/18-the-strange-attractor",
  "/trinity/18-the-strange-attractor/",
  "/trinity/18-the-strange-attractor/index.html",
  "/trinity/22-the-teleology",
  "/trinity/22-the-teleology/",
  "/trinity/22-the-teleology/index.html",
  "/trinity/36-the-dimensional-trophic-cascade",
  "/trinity/36-the-dimensional-trophic-cascade/",
  "/trinity/36-the-dimensional-trophic-cascade/index.html",
  "/trinity/37-sexual-selection-as-visible-f5",
  "/trinity/37-sexual-selection-as-visible-f5/",
  "/trinity/37-sexual-selection-as-visible-f5/index.html",
  "/trinity/simulation-spec",
  "/trinity/simulation-spec/",
  "/trinity/simulation-spec/index.html",
  "/value/00-objective-morals-and-ethics",
  "/value/00-objective-morals-and-ethics/",
  "/value/00-objective-morals-and-ethics/index.html",
  "/value/00-the-good-the-evil-and-the-transcendentals",
  "/value/00-the-good-the-evil-and-the-transcendentals/",
  "/value/00-the-good-the-evil-and-the-transcendentals/index.html",
  "/value/01-transcendentals",
  "/value/01-transcendentals/",
  "/value/01-transcendentals/index.html",
  "/will/00-the-generative-lagrangian",
  "/will/00-the-generative-lagrangian/",
  "/will/00-the-generative-lagrangian/index.html",
  "/will/01-f5-force-map-and-ektropy",
  "/will/01-f5-force-map-and-ektropy/",
  "/will/01-f5-force-map-and-ektropy/index.html",
  "/will/02-the-serpent-is-f5",
  "/will/02-the-serpent-is-f5/",
  "/will/02-the-serpent-is-f5/index.html",
  "/will/04-what-the-corpus-reveals",
  "/will/04-what-the-corpus-reveals/",
  "/will/04-what-the-corpus-reveals/index.html",
  "/will/05-exhaustive-observations",
  "/will/05-exhaustive-observations/",
  "/will/05-exhaustive-observations/index.html"
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
