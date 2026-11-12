// The service worker: a small script the browser keeps running in the
// background, sitting between your pages and the network.
//
// What this one does:
//   1. install  - saves a few files into a cache (a store inside the browser)
//   2. activate - deletes caches from older versions
//   3. fetch    - every time the app asks for something:
//        a page?      try the network; if offline, show the saved offline page
//        anything else (CSS, icon, ...)?  use the saved copy if there is one
//
// See it in Chrome: DevTools > Application > Service workers and Cache Storage.

const CACHE = "ais-cache-v1";
const ASSETS = [
  "/offline",
  "/static/style.css",
  "/static/icon.svg",
  "/static/manifest.json",
  "/config.js"
];

self.addEventListener("install", function (event) {
  event.waitUntil(
    caches.open(CACHE).then(function (cache) {
      return cache.addAll(ASSETS);
    })
  );
  self.skipWaiting();
});

self.addEventListener("activate", function (event) {
  event.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(
        keys.filter(function (k) { return k !== CACHE; })
            .map(function (k) { return caches.delete(k); })
      );
    })
  );
  self.clients.claim();
});

self.addEventListener("fetch", function (event) {
  if (event.request.mode === "navigate") {
    // A page: network first, the offline page if that fails.
    event.respondWith(
      fetch(event.request).catch(function () {
        return caches.match("/offline");
      })
    );
    return;
  }
  // Anything else: the cached copy first, the network if it is not cached.
  event.respondWith(
    caches.match(event.request).then(function (hit) {
      return hit || fetch(event.request);
    })
  );
});
