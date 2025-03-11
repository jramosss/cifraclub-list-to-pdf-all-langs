package main

import (
	"encoding/json"
	"log"
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
		"https://cifraclub.com/musico/551928421/repertorio/favoritas/", // large
		"https://cifraclub.com/musico/551928421/repertorio/12409416/",  // small
	}

	results := make([]result, len(urls))

	for index, url := range urls {
		scrapeStart := time.Now()
		songs, err := scrapeSongs(url)
		if err != nil {
			log.Fatal(err)
		}
		htmlContent := generateHtml(songs)
		scrape_time := time.Since(scrapeStart)

		pdfStart := time.Now()
		createPDF(htmlContent, "output"+string(index)+".pdf")
		pdf_generate_time := time.Since(pdfStart)

		results = append(results, result{
			total_songs:       len(songs),
			scrape_time:       scrape_time,
			pdf_generate_time: pdf_generate_time,
		})
	}

	saveResults(results)
}
