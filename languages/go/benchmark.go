package main

import (
	"encoding/json"
	"fmt"
	"log"
	"os"
	"time"
)

type result struct {
	TotalSongs      int           `json:"total_songs"`
	ScrapeTime      time.Duration `json:"scrape_time"`
	PdfGenerateTime time.Duration `json:"pdf_generate_time"`
}

func saveResults(results []result) error {
	file, err := os.Create("benchmarks.json")
	if err != nil {
		log.Fatalf("could not create file: %v", err)
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

	var results []result

	for index, url := range urls {
		scrapeStart := time.Now()
		songs, err := scrapeSongs(url)
		if err != nil {
			log.Fatal(err)
		}
		htmlContent := generateHtml(songs)
		scrape_time := time.Since(scrapeStart)

		pdfStart := time.Now()
		createPDF(htmlContent, fmt.Sprintf("output%d.pdf", index))
		pdf_generate_time := time.Since(pdfStart)

		results = append(results, result{
			TotalSongs:      len(songs),
			ScrapeTime:      scrape_time / time.Millisecond,
			PdfGenerateTime: pdf_generate_time / time.Millisecond,
		})
	}

	saveResults(results)
}
