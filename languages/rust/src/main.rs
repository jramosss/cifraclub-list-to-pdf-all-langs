use crate::pdf::html_to_pdf;
use warp::Filter;

mod scraper;
mod utils;
mod pdf;

async fn serve_file(html_content: String, port: u16) {
    let route = warp::path!("result").map(move || warp::reply::html(html_content.clone()));
    let server = warp::serve(route).run(([127, 0, 0, 1], port));
    tokio::spawn(server);
}

#[tokio::main]
async fn main() {
    let urls = [
        "https://www.cifraclub.com/musico/551928421/repertorio/12409416/",
        "https://www.cifraclub.com/musico/551928421/repertorio/favoritas/"
    ];

    for (i, url) in urls.iter().enumerate() {
        let result = scraper::scrape(url.parse().unwrap()).await;
        let port = 3030 + i as u16;
        serve_file(result.clone(), port).await;
        html_to_pdf(port).await;
    }
}
