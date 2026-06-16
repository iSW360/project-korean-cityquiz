/* GeoQ Service Worker v4
   HTML·데이터: 네트워크 우선 (항상 최신)
   CSS·JS·이미지: 캐시 우선 (빠른 로딩)
*/
const CACHE = 'geoq-v4';   // 버전 올리면 이전 캐시 전체 삭제
const PRE_CACHE = [
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
    caches.open(CACHE).then(c => c.addAll(PRE_CACHE)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(
        keys.filter(k => k !== CACHE).map(k => caches.delete(k))
      ))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);
  if (e.request.method !== 'GET' || url.origin !== self.location.origin) return;

  const path = url.pathname;

  // HTML 페이지 & 데이터 파일 → 네트워크 우선 (항상 최신 반영)
  const isHtml = path === '/' || path.endsWith('.html') ||
                 ['about','privacy','quiz','result'].some(p => path === '/'+p);
  const isData = path.startsWith('/data/') || path.startsWith('/maps/');

  if (isHtml || isData) {
    e.respondWith(
      fetch(e.request)
        .then(res => {
          const clone = res.clone();
          caches.open(CACHE).then(c => c.put(e.request, clone));
          return res;
        })
        .catch(() => caches.match(e.request))  // 오프라인 폴백
    );
    return;
  }

  // CSS·JS·이미지·폰트 → 캐시 우선 (빠른 로딩)
  e.respondWith(
    caches.match(e.request).then(r =>
      r || fetch(e.request).then(res => {
        const clone = res.clone();
        caches.open(CACHE).then(c => c.put(e.request, clone));
        return res;
      })
    )
  );
});
