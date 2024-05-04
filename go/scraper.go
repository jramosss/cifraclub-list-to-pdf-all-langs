package main

import (
	"log"

	"net/http"

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

func scrapeSongDetails(songURL string) string {
	doc := fetch(baseURL + songURL)
	folhas := doc.Find("div").FilterFunction(func(i int, s *goquery.Selection) bool {
		class, _ := s.Attr("class")
		log.Printf("class: %s", class)
		return class != "" && class[:5] == "folha"
	})
	return folhas.Text()
}

func main() {
	songs := getSongsLinksInList("/musico/552807671/repertorio/favoritas/")
	log.Println(songs[0])
	song_details := scrapeSongDetails(sanitizeSongLink((songs[0])))
	log.Println(songs[0], song_details)
}
