urls = [
  # "https://www.cifraclub.com/musico/551928421/repertorio/favoritas/", # large
  "https://www.cifraclub.com/musico/551928421/repertorio/12409416/" # small
]


for url <- urls do
  IO.puts("Scraping page: #{url}")
  {start_time, response} = :timer.tc(Scraper, :scrape, url)
  IO.puts("Time taken to scrape page: #{url} - #{start_time / 1000} ms")
end
