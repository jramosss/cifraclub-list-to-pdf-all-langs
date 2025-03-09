import type { BunRequest } from "bun";
import { htmlToPdf } from "./pdf";
import { getScraper } from "./utils/utils";

export async function generate(request: BunRequest) {
	const connectionId = (request.params as { id: string }).id;
	const body = await request.json();
	const { list_url } = body;
	const scraper = getScraper(connectionId);
	const htmlContent = await scraper.scrape(list_url);
	const pdfFileName = `${connectionId}.pdf`;
	const pdfPath = `./static/${pdfFileName}`;

	await htmlToPdf(htmlContent, pdfPath);

	return new Response(JSON.stringify({ url: pdfFileName }), {
		headers: {
			"Content-Type": "application/json",
		},
	});
}
