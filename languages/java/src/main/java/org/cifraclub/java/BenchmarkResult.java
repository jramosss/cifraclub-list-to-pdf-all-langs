package org.cifraclub.java;

public class BenchmarkResult {
    public long pdf_generate_time;
    public long scrape_time;
    public int total_songs;

    public BenchmarkResult(long scrape_time, long pdf_generate_time, int total_songs) {
        this.scrape_time = scrape_time;
        this.pdf_generate_time = pdf_generate_time;
        this.total_songs = total_songs;
    }
}
