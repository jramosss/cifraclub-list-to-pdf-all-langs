import json
import time
import re

from pdf import html_to_pdf
from scraper import Scraper

def extract_json_from_string(input_string):
    json_pattern = r'\{.*?\}'

    json_strings = re.findall(json_pattern, input_string)

    json_objects = []
    for json_string in json_strings:
        try:
            json_object = json.loads(json_string)
            json_objects.append(json_object)
        except json.JSONDecodeError:
            continue

    return json_objects

def benchmark():
    urls = [
        "https://www.cifraclub.com/musico/551928421/repertorio/favoritas/", # large
        "https://www.cifraclub.com/musico/551928421/repertorio/12409416/" # small
    ]

    scraper = Scraper()

    results = []
    for url in urls:
        html, total_songs, scrape_time = scraper.scrape(url)

        pdf_generate_start = time.time()
        html_to_pdf(html, "result.pdf")
        pdf_generate_end = time.time()
        pdf_generate_time = (pdf_generate_end - pdf_generate_start) * 1000

        results.append({
            "total_songs": total_songs,
            "scrape_time": scrape_time,
            "pdf_generate_time": pdf_generate_time
        })

    with open("benchmarks.json", "w") as f:
        json.dump(results, f)

if __name__ == "__main__":
    benchmark()
