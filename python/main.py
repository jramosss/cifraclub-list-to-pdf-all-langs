import time
import concurrent.futures
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests


class Scraper:
    def __init__(self):
        options = Options()
        # options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Chrome(options=options)
        self.styles = ""

    def get_urls_from_list(self, list_url: str):
        raw_html = requests.get(list_url).text
        soup = BeautifulSoup(raw_html, "html.parser")
        list_element = soup.find(class_="list-links list-musics")
        return [self.create_print_url(el["href"]) for el in list_element.find_all("a")]

    def create_print_url(self, url: str):
        final_url = "https://cifraclub.com" + url
        if final_url.endswith(".html"):
            final_url = final_url[:-5] + "/"
        elif final_url[-1] != "/":
            final_url += "/"
        return final_url + 'imprimir.html#footerChords=false'

    def get_page_content(self, url: str):
        self.driver.get(url)
        page_content = self.driver.page_source
        if not self.styles:
            self.styles = "".join([el.get_attribute("innerHTML") for el in self.driver.find_elements(By.TAG_NAME, "style")])

        return page_content

    def scrape(self, url: str):
        urls = self.get_urls_from_list(url)
        contents = self.scrape_pages(urls)
        return self.generate_html(contents)

    def scrape_pages(self, urls: list[str], max_workers=5):
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            return list(executor.map(self.get_page_content, urls))

        # return [self.get_page_content(url) for url in urls]

    def generate_html(self, contents: list[str]):
        return f"""
        <html>
        <head>
            <style>{self.styles}</style>
        </head>
        <body>
            {''.join(contents)}
        </body>
        </html>
        """

if __name__ == "__main__":
    url = "https://www.cifraclub.com/musico/551928421/repertorio/favoritas/"
    result = Scraper().scrape(url)
    with open("merged_results.html", "w", encoding="utf-8") as f:
        f.write(result)
    print("Proceso completado. Se generó 'merged_results.html'")
