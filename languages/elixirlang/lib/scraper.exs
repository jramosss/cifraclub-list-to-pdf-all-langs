defmodule Scraper do
  # Horrible typing system omg
  @spec get_page(String.t()) :: String.t()
  def get_page(url) do
    headers = [
      {"User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"},
      {"Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"},
    ]

    options = [follow_redirect: true, max_redirect: 5]

    case HTTPoison.get(url, headers, options) do
      {:ok, %HTTPoison.Response{status_code: 200, body: body}} -> body
      {:ok, %HTTPoison.Response{status_code: status}} ->
        raise "HTTP Error: #{status}"
      {:error, reason} ->
        raise "Request failed: #{inspect(reason)}"
    end
  end

  @spec parse_page(String.t()) :: Floki.html_tree()
  def parse_page(html) do
    Floki.parse_document!(html)
  end

  @spec get_urls_from_list(String.t()) :: [String.t()]
  def get_urls_from_list(url) do
    # I like this pipe system
    page = get_page(url) |> parse_page()

    Floki.find(page, "ol.list-links.list-musics")
    |> Floki.find("a[href]")
    |> Enum.map(fn {_, attributes, _} ->
      case List.keyfind(attributes, "href", 0) do
        {"href", href} -> href
        nil -> nil
      end
    end)
    |> Enum.reject(&is_nil/1)
    |> Enum.map(&Utils.create_print_url/1)
  end

  @spec scrape_page(String.t()) :: String.t()
  def scrape_page(url) do
    page = get_page(url) |> parse_page()

    Floki.find(page, "div[class=\"pages\"]") |> Enum.at(0) |> Floki.raw_html()
  end

  @spec scrape_pages([String.t()]) :: String.t()
  def scrape_pages(urls) do
    urls
    #                                                                   dope
    |> Task.async_stream(&scrape_page/1, max_concurrency: 10, timeout: 30_000)
    |> Enum.map(fn {:ok, result} -> result end)
    |> Enum.join()
  end

  @spec scrape(String.t()) :: String.t()
  def scrape(list_url) do
    urls = get_urls_from_list(list_url)
    IO.puts("Found #{length(urls)} URLs")
    # still not sure how imports works
    scrape_pages(urls) |> Utils.generate_html()
  end
end
