from playwright.sync_api import sync_playwright

def html_to_pdf(html: str, pdf_path: str):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.set_content(html)
        page.pdf(path=pdf_path)
        browser.close()
