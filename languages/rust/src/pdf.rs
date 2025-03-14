use std::fs::File;
use std::io::Write;
use headless_chrome::Browser;


pub async fn html_to_pdf(server_port: u16) {
    let browser = Browser::default().expect("Failed to create browser");

    let tab = browser.new_tab().expect("Failed to create new tab");

    // Navigate to wikipedia
    tab.navigate_to(&format!("http://localhost:{}/result", server_port)).expect("Failed to navigate to the result page");
    let html = tab.get_content().expect("Failed to get the HTML page");
    let mut file = File::create(format!("html_{}.html", server_port)).expect("Failed to create HTML file");
    file.write_all(html.as_bytes()).expect("Failed to write to file");

    let pdf_bytes = tab.print_to_pdf(None);
    let mut file = File::create(format!("output_{}.pdf", server_port)).expect("Failed to create file");
    file.write_all(&pdf_bytes.unwrap()).expect("Failed to write to file");
}