package main

import (
	"encoding/json"
	"os"
	"time"
)

type result struct {
	total_songs       int
	scrape_time       time.Duration
	pdf_generate_time time.Duration
}

func saveResults(results []result) error {
	file, err := os.Create("benchmarks.json")
	if err != nil {
		return err
	}
	defer file.Close()

	encoder := json.NewEncoder(file)
	encoder.SetIndent("", "  ") // Formato legible
	return encoder.Encode(results)
}

func main() {
	urls := []string{
		"/musico/551928421/repertorio/favoritas/", // large
		"/musico/551928421/repertorio/12409416/",  // small
	}

	results := make([]result, len(urls))

	for _, url := range urls {
		duration, songsCount, songs := scrapeSongsBenchmark(url)
		print("Scrape time: ", duration, " songs: ", songsCount)
		print(songs)
		pdfStart := time.Now()
		createPDF(songs)
		pdfEnd := time.Now()

		results = append(results, result{
			total_songs:       songsCount,
			scrape_time:       duration,
			pdf_generate_time: pdfEnd.Sub(pdfStart),
		})
	}

	// saveResults(results)
}
