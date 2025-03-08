import type { BunRequest } from "bun";
import { htmlToPdf } from "./pdf";
import { getScraper } from "./utils/utils";

export async function generate(request: BunRequest) {
    // @ts-ignore
    const connectionId = request.params.id;
    const { list_url } = await request.json();
    const scraper = getScraper(connectionId);
    const htmlContent = await scraper.scrape(list_url);
    const pdfFileName = `${connectionId}.pdf`;
    const pdfPath = `./static/${pdfFileName}`;

    await htmlToPdf(htmlContent, pdfPath);

    return new Response(JSON.stringify({ url: pdfFileName }), {
        headers: {
            'Content-Type': 'application/json'
        }
    });
}