package org.cifraclub.java;

import com.microsoft.playwright.*;
import com.microsoft.playwright.BrowserType.LaunchOptions;

import java.nio.file.Paths;
import java.util.Arrays;

public class Pdf {
    private static LaunchOptions buildOptions() {
        LaunchOptions options = new BrowserType.LaunchOptions();
        options.headless = true;
        options.args = Arrays.asList(
            "--no-sandbox",
            "--disable-setuid-sandbox",
            "--disable-dev-shm-usage",
            "--disable-gpu"
        );
        return options;
    }

    // thank god playwright exists, i mean, it causes some trouble, but using
    // openhtmltopdf was a
    // horrible experience
    public static void htmlToPdf(String html, String pdfFilePath) throws Exception {
        try (Playwright playwright = Playwright.create()) {
            LaunchOptions browserOptions = buildOptions();
            Browser browser = playwright.chromium().launch(browserOptions);
            Page page = browser.newPage();
            page.setContent(html);
            Page.PdfOptions options = new Page.PdfOptions();
            options.setPath(Paths.get(pdfFilePath));
            options.setFormat("A4");
            page.pdf(options);
        }
    }
}
