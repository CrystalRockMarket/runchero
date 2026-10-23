/* Offline shell cache.
   The depot is meant to run without a network, but the browser should also
   survive a tunnel or a flaky hotspot: cache the shell and any page the user
   has already opened, then serve from cache when the network is gone. */
var CACHE = "runchero-depo-v4";
var SHELL = [
  "/",
  "/library",
  "/library/archive",
  "/library/archive?cat=lib-manuals",
  "/library/community",
  "/sources",
  "/vehicles",
  "/vehicles?type=tractor",
  "/vehicles?type=tractor&make=Ford",
  "/vehicles/ford-8n",
  "/section/farming",
  "/section/growing",
  "/section/animals",
  "/hub/wheat",
  "/hub/cattle",
  "/formulas",
  "/conversions",
  "/static/css/pixel.css",
  "/static/js/app.js",
  "/static/js/reader.js",
  "/static/js/formula-calc.js",
  "/static/img/logo.png",
  "/static/img/hero.png"
];

self.addEventListener("install", function (event) {
  event.waitUntil(
    caches.open(CACHE).then(function (cache) {
      return cache.addAll(SHELL).catch(function () { /* one bad file, carry on */ });
    }).then(function () { return self.skipWaiting(); })
  );
});

self.addEventListener("activate", function (event) {
  event.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(keys.map(function (key) {
        return key === CACHE ? null : caches.delete(key);
      }));
    }).then(function () { return self.clients.claim(); })
  );
});

self.addEventListener("fetch", function (event) {
  var request = event.request;
  if (request.method !== "GET") { return; }
  var url = new URL(request.url);
  if (url.origin !== self.location.origin) { return; }
  if (url.pathname.indexOf("/static/") === 0) { return; }

  event.respondWith(
    fetch(request).then(function (response) {
      var copy = response.clone();
      caches.open(CACHE).then(function (cache) {
        cache.put(request, copy).catch(function () {});
      });
      return response;
    }).catch(function () {
      return caches.match(request).then(function (cached) {
        return cached || caches.match("/");
      });
    })
  );
});
