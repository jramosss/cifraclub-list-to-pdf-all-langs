package main

import (
	"fmt"
)

func main() {
	urls := []string{
		"/musico/552807671/repertorio/favoritas/", // Short, 5 songs
		"/musico/551928421/repertorio/favoritas/", // Long, more than 150 songs
		// Add more URLs as needed
	}

	for _, url := range urls {
		duration, songsCount := scrapeSongsBenchmark(url)
		fmt.Printf("URL: %s, %d songs, Time taken: %s\n", url, songsCount, duration)
		fmt.Println("-------------------------------------------------")
	}
}
