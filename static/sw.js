// Minimal service worker so the app behaves like a PWA.
// It caches the core assets, including config.js. That means config.js also
// shows up under DevTools > Application > Cache Storage.
const CACHE = "ctf-cache-v1";
const ASSETS = [
  "/",
  "/static/style.css",
  "/config.js",
  "/static/app.js",
  "/static/manifest.json"
];

self.addEventListener("install", function (event) {
  event.waitUntil(caches.open(CACHE).then(function (cache) {
    return cache.addAll(ASSETS);
  }));
});

self.addEventListener("activate", function (event) {
  event.waitUntil(caches.keys().then(function (keys) {
    return Promise.all(keys.filter(function (k) { return k !== CACHE; })
                          .map(function (k) { return caches.delete(k); }));
  }));
});

self.addEventListener("fetch", function (event) {
  // Cache-first for cached static assets, network for everything else.
  event.respondWith(
    caches.match(event.request).then(function (hit) {
      return hit || fetch(event.request);
    })
  );
});
