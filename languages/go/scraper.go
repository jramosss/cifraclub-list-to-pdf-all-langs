package main

import (
	"log"
	"net/http"
	"os"
	"sync"
	"time"

	"github.com/PuerkitoBio/goquery"
	"github.com/signintech/gopdf"
)

const baseURL = "https://www.cifraclub.com"

func fetch(url string) *goquery.Document {
	res, err := http.Get(url)

	if err != nil {
		log.Fatal(err)
	}

	defer res.Body.Close()

	doc, err := goquery.NewDocumentFromReader(res.Body)

	if err != nil {
		log.Fatal(err)
	}

	return doc
}

func getSongsLinksInList(path string) []string {
	doc := fetch(baseURL + path)

	song_list := doc.Find(".list-links.list-musics")
	song_links := song_list.Find("li")
	var song_links_list []string
	song_links.Each(func(i int, s *goquery.Selection) {
		link := s.Find("a").AttrOr("href", "")
		song_links_list = append(song_links_list, link)
	})
	return song_links_list
}

func sanitizeSongLink(songURL string) string {
	if songURL[len(songURL)-5:] == ".html" {
		songURL = songURL[:len(songURL)-5]
	}
	if songURL[len(songURL)-1:] != "/" {
		songURL += "/"
	}
	songURL += "imprimir.html"
	return songURL
}

func scrapeSongDetails(songURL string, wg *sync.WaitGroup, ch chan<- string) {
	defer wg.Done()
	doc := fetch(baseURL + songURL)
	folhas := doc.Find("div").FilterFunction(func(i int, s *goquery.Selection) bool {
		class, _ := s.Attr("class")
		return class != "" && class[:5] == "folha"
	})
	html, err := folhas.Html()
	if err != nil {
		log.Fatal(err)
	}
	ch <- html
}

func scrapeSongs(listURL string) ([]string, error) {
	songLinks := getSongsLinksInList(listURL)

	var wg sync.WaitGroup
	ch := make(chan string)

	for _, link := range songLinks {
		wg.Add(1)
		go scrapeSongDetails(sanitizeSongLink(link), &wg, ch)
	}

	go func() {
		wg.Wait()
		close(ch)
	}()

	var songDetails []string
	for title := range ch {
		songDetails = append(songDetails, title)
	}

	return songDetails, nil
}

func createPDF(songs []string) {
	// Create pdf with all songs which are html strings
	pdf := gopdf.GoPdf{}
	pdf.Start(gopdf.Config{PageSize: *gopdf.PageSizeA4})
	pdf.AddPage()
	for _, song := range songs {
		pdf.SetX(10)
		pdf.SetY(10)
		pdf.Cell(nil, song)
		pdf.AddPage()
	}
	pdf.WritePdf("songs.pdf")
}

func scrapeSongsBenchmark(path string) (time.Duration, int, []string) {
	start := time.Now()
	songs, err := scrapeSongs(path)
	if err != nil {
		log.Fatal(err)
	}
	duration := time.Since(start)
	songsCount := len(songs)
	return duration, songsCount, songs
}

func _main() {
	start := time.Now()
	songs, err := scrapeSongs("/musico/551928421/repertorio/favoritas/")
	if err != nil {
		log.Fatal(err)
	}
	duration := time.Since(start)
	log.Println("Scraped", len(songs), "songs in", duration)
	file, err := os.Create("songs.html")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()
	for _, song := range songs {
		file.WriteString(song)
	}

	createPDF(songs)
}
