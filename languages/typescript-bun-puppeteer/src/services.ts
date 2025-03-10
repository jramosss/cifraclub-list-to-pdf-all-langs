import { htmlToPdf } from "./pdf";
import Scraper from "./scraper";

export async function scrapeAndGenerate(connectionId: string, listUrl: string) {
	const scraperStart = Date.now();
	const scraper = new Scraper();
	const htmlContent = await scraper.scrape(listUrl);
	const scraperEnd = Date.now();
	const pdfFileName = `${connectionId}.pdf`;
	const pdfPath = `./static/${pdfFileName}`;

	const pdfGenerateStart = Date.now();
	await htmlToPdf(htmlContent, pdfPath);
	const pdfGenerateEnd = Date.now();

  return {
    pdfFileName,
    total_songs: scraper.total_songs,
    scrape_time: scraperEnd - scraperStart,
    pdf_generate_time: pdfGenerateEnd - pdfGenerateStart,
  };
}