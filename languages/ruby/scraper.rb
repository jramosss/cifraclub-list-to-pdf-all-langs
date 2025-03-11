require_relative 'utils'


class Scraper    
    def get_page(url)
        require 'nokogiri'
        require 'open-uri'
        Nokogiri::HTML(URI.open(url))
    end

    def get_urls_from_list(url)
        page = get_page(url)
        list = page.css('ol.list-links.list-musics')
        list.css('li').map do |li|
            Utils.create_print_url(li.css('a').attr('href').value)
        end
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
        return Utils.generate_html(pages), urls.length()
    end
end
