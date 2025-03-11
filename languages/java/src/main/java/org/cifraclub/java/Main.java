package org.cifraclub.java;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;

public class Main {
    public static void main(String[] args) throws IOException, InterruptedException {
        var scraper = new Scraper();
        try {
            var scrapeStart = System.currentTimeMillis();
            var htmlContent = scraper.scrape("https://www.cifraclub.com/musico/551928421/repertorio/12409416/");
            var scrapeEnd = System.currentTimeMillis();

            Pdf.htmlToPdf(htmlContent, "test.pdf");
        } catch (IOException e) {
            System.out.println("Failed to get page");
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }
}