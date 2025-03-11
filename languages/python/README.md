# Cifraclub to PDF - Python + BeautifulSoup + Playwright

## How to use
- Install requirements
- Follow the steps to install [Playwright](https://playwright.dev/python/docs/intro)

## Conclusions:
- Python is great for writing something quick
- Beautifulsoup is super simple and easy to use
- Playwright works almost out of the box
- Doing this as parallel was not so easy of a task, i had to do threading and that involves workers, so this is not as "parallel" as the other languages since the requests are not being done at the same time, but it's still faster than the sequential version  
Edit: I found out that i can use asyncio to do this in parallel, then i did it, it wasn't as easy as javascript which is just doing Promise.all, i had to change playwright behaviour too, and understanding asyncio and aiohttp is not so easy, but is fairly better than threading.