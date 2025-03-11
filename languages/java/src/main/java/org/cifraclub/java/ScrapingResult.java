package org.cifraclub.java;

public class ScrapingResult {
    public String html;
    public long scrapeTime;
    public int amountOfSongs;

    public ScrapingResult(String html, long scrapeTime, int amountOfSongs) {
        this.html = html;
        this.scrapeTime = scrapeTime;
        this.amountOfSongs = amountOfSongs;
    }
}
