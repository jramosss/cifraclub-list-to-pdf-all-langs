import time

from pdf import html_to_pdf
from scraper import Scraper

def test_main():
    url = "https://www.cifraclub.com/musico/551928421/repertorio/favoritas/" # large
    # url = "https://www.cifraclub.com/musico/551928421/repertorio/12409416/" # small

    start = time.time()
    scraper = Scraper()
    result = scraper.scrape(url)

    html_to_pdf(result, "result.pdf")
    print(f"Time elapsed: {time.time() - start}s")

