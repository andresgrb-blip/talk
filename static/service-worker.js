const CACHE_NAME = 'talkie-v2';
const RUNTIME_CACHE = 'talkie-runtime-v2';

const PRECACHE_URLS = [
  '/static/manifest.json',
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(PRECACHE_URLS))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  const currentCaches = [CACHE_NAME, RUNTIME_CACHE];
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return cacheNames.filter((cacheName) => !currentCaches.includes(cacheName));
    }).then((cachesToDelete) => {
      return Promise.all(cachesToDelete.map((cacheToDelete) => {
        return caches.delete(cacheToDelete);
      }));
    }).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  if (event.request.url.startsWith(self.location.origin)) {
    if (event.request.url.includes('/ws/')) {
      return;
    }

    if (event.request.method !== 'GET') {
      return;
    }

    event.respondWith(
      caches.match(event.request).then((cachedResponse) => {
        if (cachedResponse) {
          return cachedResponse;
        }

        return caches.open(RUNTIME_CACHE).then((cache) => {
          return fetch(event.request, { redirect: 'follow' }).then((response) => {
            // Non cachare redirect (301, 302) o errori
            if (response.status === 200 && response.type === 'basic') {
              cache.put(event.request, response.clone());
            }
            return response;
          }).catch((error) => {
            // Se fetch fallisce, ritorna network error invece di cache
            return fetch(event.request);
          });
        });
      })
    );
  }
});

self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});
