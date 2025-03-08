import puppeteer from 'puppeteer';

export async function htmlToPdf(html: string, pdfPath: string) {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    await page.setContent(html);
    await page.pdf({ path: pdfPath, format: 'A4' });
    await browser.close();
}