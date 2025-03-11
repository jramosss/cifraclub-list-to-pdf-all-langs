package org.cifraclub.java;
import com.microsoft.playwright.*;
import java.nio.file.Paths;

public class Pdf {
    // thank god playwright exists, i mean, it causes some trouble, but using openhtmltopdf was a
    // horrible experience
    public static void htmlToPdf(String html, String pdfFilePath) throws Exception {
        try (Playwright playwright = Playwright.create()) {
            Browser browser = playwright.chromium().launch();
            Page page = browser.newPage();
            page.setContent(html);
            Page.PdfOptions options = new Page.PdfOptions();
            options.setPath(Paths.get(pdfFilePath));
            options.setFormat("A4");
            page.pdf(options);
        }
    }
}
