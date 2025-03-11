class Utils
  def self.create_print_url(url)
    # url starts with /
    final_url = "https://cifraclub.com" + url
    params = ""

    if final_url.include?("#")
      splitted = final_url.split('#')
      final_url = splitted[0]
      params = splitted[1]
    end

    if final_url.end_with?(".html")
      final_url = final_url[0...-".html".length]
    elsif final_url[-1] != '/'
      final_url += "/"
    end

    final_url + "imprimir.html#footerChords=false" + (params != '' ? '&' + params : '')
  end

  private

  def self.remove_tam_a4(html)
    html.gsub("tam_a4", "")
  end

  public

  def self.generate_html(contents)
    <<-HTML
      <html>
      <head>
      <link href="https://akamai.sscdn.co/cc/css/0830d.cifra_print.css" media="all" rel="stylesheet" type="text/css"/>
      <meta charset="utf-8">
      </head>
      <body>
      #{remove_tam_a4(contents.join(""))}
      </body>
      </html>
    HTML
  end
end