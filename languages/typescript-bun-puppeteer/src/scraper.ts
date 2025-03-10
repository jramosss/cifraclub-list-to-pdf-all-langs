import * as cheerio from "cheerio";
import { createPrintUrl, generateHtml } from "./utils/utils";

export default class Scraper {
	public total_songs: number = 0;

	private getPage = async (url: string) => {
		const response = await fetch(url);
		return response.text();
	};

	private getCheerioObject = async (url: string) => {
		const html = await this.getPage(url);
		return cheerio.load(html);
	};

	private getUrlsFromList = async (listUrl: string) => {
		const $ = await this.getCheerioObject(listUrl);
		const listObject = $('ol[class="list-links list-musics"]');
		return (
			listObject
				.find("a")
				// biome-ignore lint/style/noNonNullAssertion: <explanation>
				.map((i, el) => createPrintUrl($(el).attr("href")!))
				.get()
		);
	};

	private scrapePage = async (url: string) => {
		const $ = await this.getCheerioObject(url);
		const pages = $('div[class="pages"]').get();
		if (pages.length === 0) {
			return "";
		}
		const page = pages[0];
		// biome-ignore lint/style/noNonNullAssertion: <explanation>
		return $(page).html()!;
	};

	private scrapePages = async (urls: string[]) => {
		return Promise.all(
			urls.map(async (url) => this.scrapePage(url))
		);
	};

	public scrape = async (listUrl: string) => {
		const urls = await this.getUrlsFromList(listUrl);
		this.total_songs = urls.length;
		const htmlContent = await this.scrapePages(urls);
		return generateHtml(htmlContent);
	};
}
