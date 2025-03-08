import playwright from 'playwright';

export async function htmlToPdf(html: string, pdfPath: string) {
    const browser = await playwright.chromium.launch();
    const page = await browser.newPage();
    await page.setContent(html);
    await page.pdf({ path: pdfPath, format: 'A4' });
    await browser.close();
}