// Service worker de la PWA: estáticos cache-first (offline), /api network-first.
const CACHE = 'vcc-static-v1'
const PRECACHE = ['./', './index.html', './manifest.webmanifest', './favicon.ico']

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches
      .open(CACHE)
      .then((c) => c.addAll(PRECACHE))
      .then(() => self.skipWaiting()),
  )
})

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches
      .keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim()),
  )
})

self.addEventListener('fetch', (event) => {
  const { request } = event
  if (request.method !== 'GET') return
  const url = new URL(request.url)
  if (url.origin !== self.location.origin) return

  // La API siempre va a la red primero
  if (url.pathname.startsWith('/api')) {
    event.respondWith(
      fetch(request).catch(() => caches.match(request)),
    )
    return
  }

  // Navegaciones: red primero, con fallback offline al shell
  if (request.mode === 'navigate') {
    event.respondWith(
      fetch(request).catch(() => caches.match('./index.html')),
    )
    return
  }

  // Estáticos: cache primero, luego red (y se cachea lo nuevo)
  event.respondWith(
    caches.match(request).then(
      (hit) =>
        hit ??
        fetch(request).then((res) => {
          if (res.ok) {
            const copy = res.clone()
            caches.open(CACHE).then((c) => c.put(request, copy))
          }
          return res
        }),
    ),
  )
})
