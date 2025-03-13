use headless_chrome::Browser;
use headless_chrome::types::PrintToPdfOptions;


pub async fn html_to_pdf(server_port: u16) -> anyhow::Result<Vec<u8>> {
    let browser = Browser::default()?;

    let tab = browser.new_tab()?;

    // Navigate to wikipedia
    tab.navigate_to(&format!("http://localhost:{}/result", server_port)).expect("Failed to navigate to the result page");
    let options: Option<PrintToPdfOptions> = Default::default();
    tab.print_to_pdf(options)
}