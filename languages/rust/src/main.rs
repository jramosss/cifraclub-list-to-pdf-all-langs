use std::fs::File;
use crate::pdf::html_to_pdf;
use warp::Filter;
use std::time::Instant;
use serde::{Deserialize, Serialize};

mod scraper;
mod utils;
mod pdf;

#[derive(Serialize, Deserialize)]
pub struct BenchmarkResults {
    pub scrape_time: u128,
    pub pdf_generate_time: u128,
    pub total_songs: u32,
}

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
    let mut results: Vec<BenchmarkResults> = Vec::new();

    for (i, url) in urls.iter().enumerate() {
        let scrape_start = Instant::now();
        let result = scraper::scrape(url.parse().unwrap()).await;
        let scrape_time = scrape_start.elapsed().as_millis();
        let port = 3030 + i as u16;
        // hate to do this, but there is no other option rn
        serve_file(result.html.clone(), port).await;
        let pdf_start = Instant::now();
        html_to_pdf(port).await;
        let pdf_generate_time = pdf_start.elapsed().as_millis();

        results.push(BenchmarkResults {
            scrape_time,
            pdf_generate_time,
            total_songs: result.total_songs,
        });
    }

    let file = File::create("benchmarks.json").expect("Failed to create file");
    serde_json::to_writer(&file, &results).expect("Failed to write to file");
}
