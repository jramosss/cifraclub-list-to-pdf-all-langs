use scraper::Html;
use tokio::task;
use futures::future::join_all;
use crate::utils::Utils;

pub async fn get_scraper_object(url: String) -> Html {
    let body = reqwest::get(&url).await.unwrap().text().await.unwrap();
    Html::parse_document(&body)
}

pub async fn get_urls_from_list(url: String) -> Vec<String> {
    let scraper_object = get_scraper_object(url).await;
    let list_element = scraper::Selector::parse("ol.list-links.list-musics").unwrap();
    let selector = scraper_object.select(&list_element);
    let mut urls = Vec::new();

    for element in selector {
        for a in element.select(&scraper::Selector::parse("a").unwrap()) {
            let href = a.value().attr("href").unwrap();
            urls.push(Utils::create_print_url(href));
        }
    }

    urls
}

pub async fn scrape_page(url: String) -> String {
    let scraper_object = get_scraper_object(url).await;
    let page_element = scraper::Selector::parse("div.pages").unwrap();
    let selector = scraper_object.select(&page_element);

    selector.map(|element| element.html()).collect::<Vec<_>>().join("")
}

pub async fn scrape_pages(urls: Vec<String>) -> Vec<String> {
    let tasks: Vec<_> = urls.into_iter().map(|url| task::spawn(scrape_page(url))).collect();

    let results = join_all(tasks).await;

    results.into_iter().filter_map(|res| res.ok()).collect()
}

pub async fn scrape(url: String) -> String {
    let urls = get_urls_from_list(url).await;
    let pages = scrape_pages(urls).await;
    Utils::generate_html(pages)
}