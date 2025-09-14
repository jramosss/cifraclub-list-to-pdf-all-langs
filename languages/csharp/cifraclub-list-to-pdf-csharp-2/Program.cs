using cifraclub_list_to_pdf_csharp;
using Newtonsoft.Json;

async Task<BenchmarkResults> GenerateReport(string url, int index) {
    var scrapeStart = DateTime.Now;
    var scraper = new Scraper();
    var (htmlContent, total_songs) = scraper.Scrape(url);
    var scrapeEnd = DateTime.Now;
    var pdfGenerateStart = DateTime.Now;
    await Pdf.HtmlToPdf(htmlContent, "result" + index + ".pdf");
    var pdfGenerateEnd = DateTime.Now;

    return new BenchmarkResults
    {
        scrape_time = (scrapeEnd - scrapeStart).Milliseconds,
        pdf_generate_time = (pdfGenerateEnd - pdfGenerateStart).Milliseconds,
        total_songs = total_songs
    };
}

async Task Main()
{
    var results = new List<BenchmarkResults>();
    var urls = new List<string>()
    {
        "https://www.cifraclub.com/musico/551928421/repertorio/12409416/",
        "https://www.cifraclub.com/musico/551928421/repertorio/favoritas/"
    };

    var index = 0;
    foreach (var url in urls) {
        results.Add(await GenerateReport(url, index));
        index++;
    }
    
    File.WriteAllText("benchmarks.json", JsonConvert.SerializeObject(results));
}

await Main();

