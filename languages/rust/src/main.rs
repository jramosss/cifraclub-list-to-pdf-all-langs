use std::io::Write;

mod scraper;
mod utils;

#[tokio::main]
async fn main() {
    let result = scraper::scrape("https://www.cifraclub.com/musico/551928421/repertorio/12409416/".parse().unwrap()).await;

    // write to file
    let mut file = std::fs::File::create("output.html").unwrap();
    file.write_all(result.as_ref()).unwrap()
}
