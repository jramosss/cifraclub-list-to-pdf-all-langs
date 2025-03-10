import Scraper from "./scraper";

export default class StateManagerSingleton {
    private static instance: StateManagerSingleton;
    private scrapers: Map<string, Scraper>;

    private constructor() {
        this.scrapers = new Map();
    }

    public static getInstance(): StateManagerSingleton {
        if (!StateManagerSingleton.instance) {
            StateManagerSingleton.instance = new StateManagerSingleton();
        }

        return StateManagerSingleton.instance;
    }

    public getScraper(id: string): Scraper {
        const scraper = this.scrapers.get(id);
        if (!scraper) {
            throw new Error(`Scraper with id ${id} not found`);
        }

        return scraper;
    }

    public addScraper(id: string, scraper: Scraper): void {
        this.scrapers.set(id, scraper);
    }

    public deleteScraper(id: string): void {
        this.scrapers.delete(id);
    }

    public getOrCreateScraper(id: string): Scraper {
        let scraper = this.scrapers.get(id);
        if (!scraper) {
            scraper = new Scraper(id);
            this.scrapers.set(id, scraper);
        }

        return scraper;
    }
}