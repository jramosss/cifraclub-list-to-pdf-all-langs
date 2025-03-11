module Benchmark
  require_relative 'scraper'
  require_relative 'pdf'
end

def benchmark
  urls = [
    "https://www.cifraclub.com/musico/551928421/repertorio/12409416/",
    "https://www.cifraclub.com/musico/551928421/repertorio/favoritas/"
  ]

  results = []

  for url in urls
    scraper_start_time = Time.now
    scraper = Scraper.new()
    pages, amount_of_songs = scraper.scrape(url)
    scraper_end_time = Time.now

    pdf_generate_start_time = Time.now
    pdf = Pdf.new()
    pdf.html_to_pdf(pages, "output.pdf")
    pdf_generate_end_time = Time.now

    results.push({
      amount_of_songs: amount_of_songs,
      scrape_time: (scraper_end_time - scraper_start_time) * 1000,
      pdf_generate_time: (pdf_generate_end_time - pdf_generate_start_time) * 1000
    })
  end

  File.open("benchmarks.json", "w") do |f|
    f.write
    f.write(JSON.pretty_generate(results))
  end
end

benchmark