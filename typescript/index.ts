import type { SocketMessage } from "./types";
import { generate } from "./src/routes";
import { getScraper } from "./src/utils/utils";

const STATIC_PATH = "./static";

// @ts-ignore - bun messed up with websockets
Bun.serve({
	routes: {
		"/generate/:id": {
			POST: generate,
		},
	},
	port: 8000,
	fetch: async (request, server) => {
		if (server.upgrade(request)) {
			return;
		}

		// static file serving
		const filePath = STATIC_PATH + new URL(request.url).pathname;
		const file = Bun.file(filePath);
		return new Response(file);
	},
	websocket: {
		async message(ws, msg: SocketMessage) {
			const { connection_id } = JSON.parse(msg);
			const scraper = getScraper(connection_id);
			if (!scraper) return ws.send(JSON.stringify({ error: "Scraper not found" }));
			
			scraper.setSocket(ws);
		},
	},
});

console.log("Server started on port 8000");
