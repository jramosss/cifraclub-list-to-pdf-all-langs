import { generate } from './src/routes';

Bun.serve({
    routes: {
        "/health": new Response("OK"),
        '/generate/:id': {
            POST: generate
        },
        // '/ws/:id': () => {},
    },
    port: 8000,
    fetch: async (request: Request) => {
        const { url, method, headers, body } = request;
        console.log({ url, method, headers, body });
        return new Response('Not Found', { status: 404 });
    }
})

console.log('Server started on port 8000');