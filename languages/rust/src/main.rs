mod scraper;
mod utils;

#[tokio::main]
async fn main() {
    let urls = scraper::get_urls_from_list("https://www.cifraclub.com/musico/551928421/repertorio/12409416/".parse().unwrap()).await;
    let url = urls.first().unwrap();
    let page = scraper::scrape_page(url.to_string()).await;
    println!("{}", page);
}
