import { chromium as PlaywrightChromium } from 'playwright';

export async function htmlToPdf(html: string, pdfPath: string) {
  const browser = await PlaywrightChromium.launch({
    headless: true,
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-gpu',
      '--disable-dev-shm-usage',
    ],
  });
  const page = await browser.newPage();
  await page.setContent(html);
  await page.pdf({ path: pdfPath, format: 'A4' });
  await browser.close();
}
