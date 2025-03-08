import playwright from 'playwright';

export async function htmlToPdf(html: string, pdfPath: string) {
    console.log('Launching chrome')
    const browser = await playwright.chromium.launch();
    console.log('hey')
    const page = await browser.newPage();
    await page.setContent(html);
    await page.pdf({ path: pdfPath, format: 'A4' });
    await browser.close();
}