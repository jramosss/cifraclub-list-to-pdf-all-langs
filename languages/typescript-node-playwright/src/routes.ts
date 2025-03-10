import { scrapeAndGenerate } from "./services";

export async function generate(request: Request) {
  const connectionId = "1";
	const body = await request.json();
	const { list_url } = body;
	
	const { pdfFileName } = await scrapeAndGenerate(connectionId, list_url);

	return new Response(JSON.stringify({ url: pdfFileName }), {
		headers: {
			"Content-Type": "application/json",
		},
	});
}
