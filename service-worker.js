const CACHE_NAME = 'assistente-mamae-bebe-cache-v1';
const urlsToCache = [
    '/',
    '/static/css/style.css',
    '/static/js/script.js',
    '/static/images/icon-192x192.png',
    '/static/images/icon-512x512.png',
    // Adicione aqui outros assets estáticos que você quer cachear
    // Por exemplo, se você tiver uma página offline personalizada:
    // '/offline.html'
];

// Evento de instalação: abre o cache e armazena os arquivos principais da aplicação.
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => {
                console.log('Opened cache');
                return cache.addAll(urlsToCache);
            })
    );
});

// Evento fetch: intercepta as requisições de rede.
// Tenta servir do cache primeiro. Se não encontrar, busca na rede.
// Se a busca na rede falhar (offline), pode opcionalmente servir uma página offline.
self.addEventListener('fetch', event => {
    event.respondWith(
        caches.match(event.request)
            .then(response => {
                // Cache hit - return response
                if (response) {
                    return response;
                }

                // Importante: Clone a requisição. A requisição é um stream e
                // pode ser consumida apenas uma vez. Nós precisamos cloná-la para
                // usá-la tanto pelo browser quanto pelo cache.
                const fetchRequest = event.request.clone();

                return fetch(fetchRequest).then(
                    networkResponse => {
                        // Verifique se recebemos uma resposta válida
                        if (!networkResponse || networkResponse.status !== 200 || networkResponse.type !== 'basic') {
                            return networkResponse;
                        }

                        // Importante: Clone a resposta. Assim como a requisição,
                        // a resposta é um stream e precisa ser clonada para ser
                        // usada pelo browser e pelo cache.
                        const responseToCache = networkResponse.clone();

                        caches.open(CACHE_NAME)
                            .then(cache => {
                                cache.put(event.request, responseToCache);
                            });

                        return networkResponse;
                    }
                ).catch(error => {
                    // Tratar erros de rede, por exemplo, servir uma página offline
                    console.error('Fetching failed:', error);
                    // if (event.request.mode === 'navigate') {
                    //     return caches.match('/offline.html');
                    // }
                });
            })
    );
});

// Evento activate: gerencia caches antigos.
// Remove caches antigos para liberar espaço e garantir que o service worker
// utilize a versão mais recente dos assets.
self.addEventListener('activate', event => {
    const cacheWhitelist = [CACHE_NAME]; // Adicione novos nomes de cache aqui ao atualizar
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.map(cacheName => {
                    if (cacheWhitelist.indexOf(cacheName) === -1) {
                        console.log('Deleting old cache:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
});