package main

import (
	"log"
	"net/http"
	"sync"

	"github.com/PuerkitoBio/goquery"
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
	doc := fetch(path)

	song_list := doc.Find(".list-links.list-musics")
	song_links := song_list.Find("li")
	var song_links_list []string
	song_links.Each(func(i int, s *goquery.Selection) {
		link := s.Find("a").AttrOr("href", "")
		song_links_list = append(song_links_list, createPrintUrl(link))
	})
	return song_links_list
}

func scrapeSongDetails(songURL string, wg *sync.WaitGroup, ch chan<- string) {
	defer wg.Done()
	doc := fetch(songURL)
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
		go scrapeSongDetails(link, &wg, ch)
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
