import * as cheerio from "cheerio";
import { createPrintUrl, generateHtml } from "./utils/utils";
import type { ServerWebSocket } from "bun";

export default class Scraper {
	private id: string;
	private socket: ServerWebSocket<unknown> | null;
	private total_songs: number;
	private progress: number;

	constructor(_id: string) {
		this.id = _id;
		this.socket = null;
		this.total_songs = 0;
		this.progress = 0;
	}

	public setSocket = (socket: ServerWebSocket<unknown>) => {
		this.socket = socket;
	};

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

	private lastUpdate = 0;

	private sendProgress = () => {
		const now = Date.now();
		if (now - this.lastUpdate > 5) {
			this.lastUpdate = now;
			this.socket?.send(
				JSON.stringify({
					progress: this.progress,
					total: this.total_songs,
				})
			);
		}
	};

	private scrapePage = async (url: string) => {
		const $ = await this.getCheerioObject(url);
		const pages = $('div[class="pages"]').get();
		if (pages.length === 0) {
			return "";
		}
		this.progress++;
		this.sendProgress();
		const page = pages[0];
		// biome-ignore lint/style/noNonNullAssertion: <explanation>
		return $(page).html()!;
	};

	private scrapePages = async (urls: string[]) => {
		return Promise.all(
			urls.map(async (url) => {
				const page = await this.scrapePage(url);
				if (this.socket) {
					this.socket.send(
						JSON.stringify({
							progress: this.progress,
							total: this.total_songs,
						}),
					);
				}
				return page;
			}),
		);
	};

	public scrape = async (listUrl: string) => {
		const urls = await this.getUrlsFromList(listUrl);
		this.total_songs = urls.length;
		const htmlContent = await this.scrapePages(urls);
		return generateHtml(htmlContent);
	};
}
