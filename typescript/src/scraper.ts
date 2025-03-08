import * as cheerio from 'cheerio';
import { createPrintUrl, generateHtml } from './utils/utils';

export default class Scraper {
    private id: string;
    private total_songs: number;
    private progress: number;

    constructor(_id: string) {
        this.id = _id;
        this.total_songs = 0;
        this.progress = 0;
    }

    private getPage = async (url: string) => {
        const response = await fetch(url);
        return response.text();
    }

    private getCheerioObject = async (url: string) => {
        const html = await this.getPage(url);
        return cheerio.load(html);
    }

    private getUrlsFromList = async (listUrl: string) => {
        const $ = await this.getCheerioObject(listUrl);
        const listObject = $('ol[class="list-links list-musics"]');
        // biome-ignore lint/style/noNonNullAssertion: <explanation>
        return listObject.find('a').map((i, el) => createPrintUrl($(el).attr('href')!)).get();
    }

    private scrapePage = async (url: string) => {
        const $ = await this.getCheerioObject(url);
        const pages = $('div[class="pages"]').get();
        if (pages.length === 0) {
            return '';
        }
        this.progress++;
        const page = pages[0];
        // biome-ignore lint/style/noNonNullAssertion: <explanation>
        return $(page).html()!;
    }

    private scrapePages = async (urls: string[]) => {
        return Promise.all(urls.map(url => this.scrapePage(url)));
    }

    public scrape = async (listUrl: string) => {
        const urls = await this.getUrlsFromList(listUrl);
        this.total_songs = urls.length;
        const htmlContent = await this.scrapePages(urls);
        return generateHtml(htmlContent);
    }
}