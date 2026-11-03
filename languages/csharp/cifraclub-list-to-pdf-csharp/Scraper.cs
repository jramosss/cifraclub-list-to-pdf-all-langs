using HtmlAgilityPack;
using System.Net;
using System.Text.RegularExpressions;


namespace cifraclub_list_to_pdf_csharp;

public class Scraper
{
    private string GetPageContent(string url)
    {
        using var client = new HttpClient();
        var response = client.GetAsync(url).Result;
        response.EnsureSuccessStatusCode();
        return response.Content.ReadAsStringAsync().Result;
    }

    private HtmlDocument GetHtmlDocumentObject(string url)
    {
        var content = GetPageContent(url);
        var doc = new HtmlDocument();
        doc.LoadHtml(content);
        return doc;
    }

    public string[] GetUrlsFromList(string url)
    {
        var htmlDoc = GetHtmlDocumentObject(url);
        // really didn't want to use xpath but turns out there's not another option (is HAP really the best scraper for c#?)
        var listNodes = htmlDoc.DocumentNode.SelectNodes("//*[@id=\"js-mod-read-list\"]/ul/div/ol");

        if (listNodes == null) return new string[0];

        return listNodes
            .SelectMany(node => node.SelectNodes(".//a") ?? new HtmlNodeCollection(null))
            .Select(a => a.GetAttributeValue("href", ""))
            .Where(href => !string.IsNullOrEmpty(href))
            .Select(WebUtility.HtmlDecode)
            .Select(Utils.CreatePrintUrl)
            .ToArray();
    }

    private string ScrapePage(string url)
    {
        var htmlDoc = GetHtmlDocumentObject(url);
        var page = htmlDoc.DocumentNode.SelectSingleNode("//div[contains(@class, 'pages')]");
        if (page == null) return "";

        return page.InnerHtml;
    }
    
    public string[] ScrapePages(string[] urls)
    {
        // f*ing love this language
        return urls.AsParallel().Select(ScrapePage).ToArray();
    }
    
    private string RemoveImgs(string html)
    {
        var doc = new HtmlDocument();
        doc.LoadHtml(html);

        foreach (var img in doc.DocumentNode.SelectNodes("//img") ?? new HtmlNodeCollection(null))
            img.Remove();

        return doc.DocumentNode.OuterHtml;
    }

    public (string, int) Scrape(string url)
    {
        var urls = GetUrlsFromList(url);
        var pages = ScrapePages(urls);
        var html = Utils.GenerateHtml(pages);
        return (RemoveImgs(html), urls.Length);
    }
}