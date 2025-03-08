import type { SocketMessage } from './types';
import { generate } from './src/routes';
import StateManagerSingleton from './src/stateManager';
import { getScraper } from './src/utils/utils';

// @ts-ignore
Bun.serve({
    routes: {
        "/health": new Response("OK"),
        '/generate/:id': {
            POST: generate
        },
        // '/ws/:id': () => {},
    },
    port: 8000,
    fetch: async (request, server) => {
        if (server.upgrade(request)) {
            return;
        }
        return new Response('Not Found', { status: 404 });
    },
    websocket: {
        async message(ws, msg: SocketMessage) {
            const { connection_id } = JSON.parse(msg)
            const scraper = getScraper(connection_id)
            if (!scraper) {
                return ws.send(JSON.stringify({ error: 'Scraper not found' }))
            }
            scraper.setSocket(ws)
        }, // a message is received
        open(ws) {
            console.log('Socket opened');
        }, // a socket is opened
        close(ws, code, message) {
            console.log('Socket closed:', code, message);
        }, // a socket is closed
    }
})

console.log('Server started on port 8000');