module Benchmark
  require_relative 'scraper'
end

def benchmark
  start_time = Time.now
  scraper = Scraper.new()
  pages = scraper.scrape("https://www.cifraclub.com/musico/551928421/repertorio/12409416/")
  end_time = Time.now
  end_time - start_time
  puts "Time elapsed #{(end_time - start_time)} seconds"
  File.open("output.html", "w") { |file| file.write(pages) }
end

benchmark