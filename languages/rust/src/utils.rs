pub struct Utils;

impl Utils {
    pub fn create_print_url(url: &str) -> String {
        let mut final_url = format!("https://cifraclub.com{}", url);
        let mut params = String::new();

        if let Some(pos) = final_url.find('#') {
            let base = final_url[..pos].to_string();
            let param = final_url[pos + 1..].to_string();
            final_url = base;
            params = param;
        }

        if final_url.ends_with(".html") {
            final_url.truncate(final_url.len() - ".html".len());
        } else if !final_url.ends_with('/') {
            final_url.push('/');
        }

        format!("{}imprimir.html#footerChords=false{}", final_url, if !params.is_empty() { format!("&{}", params) } else { String::new() })
    }

    fn remove_tam_a4(html: &str) -> String {
        html.replace("tam_a4", "")
    }

    pub fn generate_html(contents: &[&str]) -> String {
        format!(
            r#"
            <html>
            <head>
            <link href="https://akamai.sscdn.co/cc/css/0830d.cifra_print.css" media="all" rel="stylesheet" type="text/css"/>
            <meta charset="utf-8">
            </head>
            <body>
            {}
            </body>
            </html>
            "#,
            Self::remove_tam_a4(&contents.join(""))
        )
    }
}