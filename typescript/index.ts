import { htmlToPdf } from './src/pdf';
import Scraper from './src/scraper';


async function main() {
    const scraper = new Scraper('1');
    const result = await scraper.scrape('https://www.cifraclub.com/musico/551928421/repertorio/12409416/');
    await htmlToPdf(result, 'output.pdf');
}

main().then(() => console.log('done')).catch(console.error);