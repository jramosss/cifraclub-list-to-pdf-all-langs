urls = [
  "https://www.cifraclub.com/musico/551928421/repertorio/favoritas", # large
  "https://www.cifraclub.com/musico/551928421/repertorio/12409416" # small
]

# wtf is this syntax
benchmark_results = for url <- urls do
  {scrape_start_time, {html, total_songs}} = :timer.tc(Scraper, :scrape, [url])
  number = String.split(url, "/") |> Enum.at(-1)
  {pdf_start_time, _} = :timer.tc(Pdf, :generate, [html, "#{number}.pdf"])

  benchmark_result = %{
    scrape_time: scrape_start_time / 1000,
    pdf_generate_time: pdf_start_time / 1000,
    total_songs: total_songs
  }

  # non explicit return and no option to use return, booo
  benchmark_result
end

File.write!("benchmarks.json", Jason.encode!(benchmark_results))
