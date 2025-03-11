import json
import time
import asyncio

from pdf import html_to_pdf
from scraper import Scraper

async def benchmark():
    urls = [
        "https://www.cifraclub.com/musico/551928421/repertorio/favoritas/", # large
        "https://www.cifraclub.com/musico/551928421/repertorio/12409416/" # small
    ]

    scraper = Scraper()

    results = []
    try:
        for index, url in enumerate(urls):
            scrape_start = time.time()
            html, total_songs = await scraper.scrape(url)
            scrape_end = time.time()

            pdf_generate_start = time.time()
            await html_to_pdf(html, f"result_{index}.pdf")
            pdf_generate_end = time.time()

            scrape_time = (scrape_end - scrape_start) * 1000
            pdf_generate_time = (pdf_generate_end - pdf_generate_start) * 1000

            results.append({
                "total_songs": total_songs,
                "scrape_time": scrape_time,
                "pdf_generate_time": pdf_generate_time
            })

        with open("benchmarks.json", "w") as f:
            json.dump(results, f)
    finally:
        await scraper.teardown()

if __name__ == "__main__":
    asyncio.run(benchmark())
