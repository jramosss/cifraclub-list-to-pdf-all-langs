import type { BunRequest } from "bun";
import { scrapeAndGenerate } from "./services";

export async function generate(request: BunRequest) {
  const connectionId = (request.params as { id: string }).id;
	const body = await request.json();
	const { list_url } = body;
	
	const { pdfFileName } = await scrapeAndGenerate(connectionId, list_url);

	return new Response(JSON.stringify({ url: pdfFileName }), {
		headers: {
			"Content-Type": "application/json",
		},
	});
}
