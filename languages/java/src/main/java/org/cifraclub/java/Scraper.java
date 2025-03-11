package org.cifraclub.java;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.stream.Collectors;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;

public class Scraper {
    // omgggg can't believe you have to do THIS for a simple http request
    // edit: well turns out i didn't need to do this, but i will just keep it
    // just so you see how complicated simple everyday stuff is with java
    private String getPage(String url) throws IOException, InterruptedException {
        HttpClient client = HttpClient.newHttpClient();

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(url))
                .GET()
                .build();

        HttpResponse<String> response = client.send(request,
                HttpResponse.BodyHandlers.ofString());

        return response.body();
    }

    // HOW CAN IT BE SO COMPLICATED TO ADD A DEPENDENCYYYY AAAAAAAA
    private Document getJsoupObject(String url) throws IOException {
        return Jsoup.connect(url).get();
    }

    private String[] getUrlsFromList(String url) throws IOException {
        Document doc = getJsoupObject(url);
        return doc.select("ol[class=list-links list-musics]").select("a").stream()
                .map(e -> e.attr("href"))
                // i kinda like this syntax
                .map(Utils::createPrintUrl)
                .toArray(String[]::new);
    }

    private String scrapePage(String url) throws IOException {
        var doc = getJsoupObject(url);
        var page = doc.selectFirst("div[class=pages]");
        assert page != null;
        var html = page.outerHtml();
        html = new String(html.getBytes(StandardCharsets.UTF_8));
        html = removeImgTags(html);
        return html;
    }

    private String removeImgTags(String html) {
        var jsoupObject = Jsoup.parse(html);
        jsoupObject.select("img").remove();
        return jsoupObject.outerHtml();
    }

    // look at all this boilerplate code, just to achieve parallelism
    private String[] scrapeSongs(String[] urls) throws IOException {
        int numUrls = urls.length;
        ExecutorService executor = Executors.newFixedThreadPool(
                Math.min(numUrls, 10)
        );

        List<CompletableFuture<String>> futures = new ArrayList<>();

        for (String url : urls) {
            CompletableFuture<String> future = CompletableFuture.supplyAsync(
                    () -> {
                        try {
                            return scrapePage(url);
                        } catch (IOException e) {
                            throw new RuntimeException(e);
                        }
                    },
                    executor
            );
            futures.add(future);
        }

        CompletableFuture<Void> allFutures = CompletableFuture.allOf(
                futures.toArray(new CompletableFuture[0])
        );

        try {
            allFutures.join();
        } catch (Exception e) {
            e.printStackTrace();
            executor.shutdownNow();
            return new String[0];
        }

        List<String> results = futures.stream()
                .map(CompletableFuture::join)
                .collect(Collectors.toList());

        executor.shutdown();

        return results.toArray(new String[0]);
    }

    public ScrapingResult scrape(String listUrl) throws IOException {
        var scrapeStart = System.currentTimeMillis();
        var urls = getUrlsFromList(listUrl);
        var songs = scrapeSongs(urls);
        var scrapeEnd = System.currentTimeMillis();
        // so annoying that if i want to return multiple values i have to create a class
        return new ScrapingResult(Utils.generateHtml(songs), scrapeEnd - scrapeStart, songs.length);
    }
}
