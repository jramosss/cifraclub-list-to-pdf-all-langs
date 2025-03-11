package org.cifraclub.java;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;

public class Main {
    public static void main(String[] args) throws IOException, InterruptedException {
        var scraper = new Scraper();
        try {
            var htmlContent = scraper.scrape("https://www.cifraclub.com/musico/551928421/repertorio/12409416/");
            // write songs to an html file
            BufferedWriter writer = new BufferedWriter(new FileWriter("test.html"));
            writer.write(String.join("", htmlContent));

            writer.close();
        } catch (IOException e) {
            System.out.println("Failed to get page");
        }
    }
}