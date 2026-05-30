/* GeoQ Service Worker — cache-first for static, network-first for data */
const CACHE = 'geoq-v1';
const STATIC = [
  '/',
  '/css/style.css',
  '/js/engine.js',
  '/js/i18n.js',
  '/locales/ko.json',
  '/locales/en.json',
  '/favicon.svg',
  '/manifest.json',
];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE).then(c => c.addAll(STATIC)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);
  if (e.request.method !== 'GET' || url.origin !== self.location.origin) return;

  const isData = url.pathname.startsWith('/data/') || url.pathname.startsWith('/maps/');

  if (isData) {
    // Network-first: fresh data preferred, fall back to cache
    e.respondWith(
      fetch(e.request)
        .then(res => {
          const clone = res.clone();
          caches.open(CACHE).then(c => c.put(e.request, clone));
          return res;
        })
        .catch(() => caches.match(e.request))
    );
  } else {
    // Cache-first: fast load for static assets
    e.respondWith(
      caches.match(e.request).then(r =>
        r || fetch(e.request).then(res => {
          const clone = res.clone();
          caches.open(CACHE).then(c => c.put(e.request, clone));
          return res;
        })
      )
    );
  }
});
