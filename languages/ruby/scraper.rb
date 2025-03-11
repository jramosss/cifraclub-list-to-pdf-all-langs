require_relative 'utils'


class Scraper    
    def get_page(url)
        require 'nokogiri'
        require 'open-uri'
        Nokogiri::HTML(URI.open(url))
    end

    def get_urls_from_list(url)
        page = get_page(url)
        urls = []
        # find the ol tag element with class=list-links list-musics
        list = page.css('ol.list-links.list-musics')
        list.css('li').each do |li|
            urls << Utils.create_print_url(li.css('a').attr('href').value)
        end
        urls
    end

    def scrape_page(url)
        page = get_page(url)
        html = page.css('div.pages')
        html.css('img').each do |img|
            img.remove
        end
        html[0]&.to_html
    end

    def scrape_pages(urls)
        require 'parallel'
        Parallel.map(urls) do |url|
            scrape_page(url)
        end
    end

    def scrape(url)
        urls = get_urls_from_list(url)
        pages = scrape_pages(urls)
        Utils.generate_html(pages)
    end
end
