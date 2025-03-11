from playwright.async_api import async_playwright, Playwright


async def playwright_pdf_generator(playwright: Playwright, html: str, pdf_path: str):
    browser = await playwright.chromium.launch()
    page = await browser.new_page()
    await page.set_content(html)
    await page.pdf(path=pdf_path, format="A4")
    await browser.close()


async def html_to_pdf(html: str, pdf_path: str):
    async with async_playwright() as p:
        await playwright_pdf_generator(p, html, pdf_path)