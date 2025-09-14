defmodule Utils do
  @spec create_print_url(String.t()) :: String.t()
  def create_print_url(url) do
    final_url = "https://cifraclub.com" <> url
    params = ""

    # Lots of idiomatic stuff, cool but pretty hard to look at
    {final_url, params} = if String.contains?(final_url, "#") do
      [url_part, fragment] = String.split(final_url, "#")
      {url_part, "&" <> fragment}
    else
      {final_url, params}
    end

    final_url = if String.ends_with?(final_url, ".html") do
      String.slice(final_url, 0, String.length(final_url) - 5) <> "/"
    else
      final_url
    end

    final_url = if String.last(final_url) != "/" do
      final_url <> "/"
    else
      final_url
    end

    final_url <> "imprimir.html#footerChords=false" <> params
  end

  @spec generate_html([String.t()]) :: String.t()
  def generate_html(contents) do
    "
    <html>
    <head>
        <link href=\"https://akamai.sscdn.co/cc/css/0830d.cifra_print.css\" media=\"all\" rel=\"stylesheet\" type=\"text/css\"/>
        <meta charset=\"utf-8\">
    </head>
    <body>" <> remove_tam_a4(Enum.join(contents)) <> "</body>
    </html>"
  end

  @spec remove_tam_a4(String.t()) :: String.t()
  def remove_tam_a4(content) do
    String.replace(content, "tam_a4", "")
  end

end
