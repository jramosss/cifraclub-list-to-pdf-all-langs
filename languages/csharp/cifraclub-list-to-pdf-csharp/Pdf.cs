namespace cifraclub_list_to_pdf_csharp;
using Microsoft.Playwright;

public class Pdf
{
    public static async Task HtmlToPdf(string html, string path)
    {
        using var playwright = await Playwright.CreateAsync();
        await using var browser = await playwright.Chromium.LaunchAsync(new() {
            Headless = true,
            Args = new[] {
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-gpu",
                "--disable-dev-shm-usage"
            }
        });
        var page = await browser.NewPageAsync();
        await page.SetContentAsync(html);
        await page.PdfAsync(new() { Path = path, Format = "A4", Margin = new() { Top = "0", Right = "0", Bottom = "0", Left = "0" } });
    }
}