import concurrent.futures
from bs4 import BeautifulSoup
import requests

from utils import create_print_url, generate_html


class Scraper:
    @staticmethod
    def get_urls_from_list(list_url: str):
        raw_html = requests.get(list_url).text
        soup = BeautifulSoup(raw_html, "html.parser")
        list_element = soup.find(class_="list-links list-musics")
        return [create_print_url(el["href"]) for el in list_element.find_all("a")]

    @staticmethod
    def scrape_page(url: str):
        raw_html = requests.get(url).text
        soup = BeautifulSoup(raw_html, "html.parser")
        content = soup.find(class_="pages")
        return str(content.decode(4, "utf-8"))

    def scrape_pages(self, urls: list[str]):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.scrape_page, url) for url in urls]
            return [future.result() for future in concurrent.futures.as_completed(futures)]

    def scrape(self, url: str):
        urls = self.get_urls_from_list(url)
        contents = self.scrape_pages(urls)
        return generate_html(contents)


if __name__ == "__main__":
    # url = "https://www.cifraclub.com/musico/551928421/repertorio/favoritas/" # large
    url = "https://www.cifraclub.com/musico/551928421/repertorio/12409416/" # small
    scraper = Scraper()
    result = scraper.scrape(url)

    with open(f"generated.html", "w", encoding="utf-8") as f:
        f.write(result)

    print("Proceso completado. Se generó 'merged_results.html'")
