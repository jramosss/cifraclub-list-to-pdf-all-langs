package org.cifraclub.java;

import com.fasterxml.jackson.databind.ObjectMapper;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;

public class Main {
    public static void writeBenchmarkResultsToJson(
            ArrayList<BenchmarkResult> results, String filePath) throws IOException {
        ObjectMapper mapper = new ObjectMapper();
        mapper.writeValue(new File(filePath), results);
    }

    public static void main(String[] args) throws Exception {
        String[] urls = {
            "https://www.cifraclub.com/musico/551928421/repertorio/12409416/",
            "https://www.cifraclub.com/musico/551928421/repertorio/favoritas/"
        };

        // so we have Array, ArrayList, List, check
        ArrayList<BenchmarkResult> benchmarkResults = new ArrayList<BenchmarkResult>();

        for (String url : urls) {
            var scraper = new Scraper();
            var scrapingResult = scraper.scrape(url);

            var pdfStart = System.currentTimeMillis();
            Pdf.htmlToPdf(scrapingResult.html, "test.pdf");
            var pdfEnd = System.currentTimeMillis();

            // append the scraping time to the result
            var benchmarkResult = new BenchmarkResult(
                scrapingResult.scrapeTime,
                pdfEnd - pdfStart,
                scrapingResult.amountOfSongs
            );

            benchmarkResults.add(benchmarkResult);
        }

        // write the array as a json in a file called benchmarks.json in root folder
        writeBenchmarkResultsToJson(benchmarkResults, "benchmarks.json");
    }
}