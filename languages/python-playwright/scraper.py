import asyncio
import aiohttp
from bs4 import BeautifulSoup


from utils import create_print_url, generate_html


class Scraper:
    def __init__(self):
        self.session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False))

    async def teardown(self):
        await self.session.close()

    async def get_soup(self, url: str) -> BeautifulSoup:
        async with self.session.get(url) as response:
            raw_html = await response.text()
        return BeautifulSoup(raw_html, "html.parser")

    async def get_urls_from_list(self, list_url: str) -> list[str]:
        soup = await self.get_soup(list_url)
        list_element = soup.find(class_="list-links list-musics")
        return [
            create_print_url(el["href"]) for el in list_element.find_all("a")
        ]

    async def scrape_page(self, url: str) -> str:
        soup = await self.get_soup(url)
        content = soup.find(class_="pages")
        images = content.find_all("img")
        for img in images:
            img.decompose()
        return str(content.decode(4, "utf-8"))

    async def scrape_pages(self, urls: list[str]) -> list[str]:
        tasks = [self.scrape_page(url) for url in urls]
        return await asyncio.gather(*tasks)

    async def scrape(self, url: str):
        urls = await self.get_urls_from_list(url)
        contents = await self.scrape_pages(urls)
        html = generate_html(contents)
        return html, len(urls)

