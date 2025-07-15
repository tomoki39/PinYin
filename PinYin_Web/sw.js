// PinYin Service Worker
const CACHE_NAME = 'pinyin-v1';
const urlsToCache = [
  '/',
  '/index.html',
  '/manifest.json',
  '../icons/design4_typography_192x192.png',
  '../icons/design4_typography_512x512.png',
  '../pinyin_map.json'
];

self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(function(cache) {
        return cache.addAll(urlsToCache);
      })
  );
});

self.addEventListener('fetch', function(event) {
  event.respondWith(
    caches.match(event.request)
      .then(function(response) {
        if (response) {
          return response;
        }
        return fetch(event.request);
      }
    )
  );
}); 