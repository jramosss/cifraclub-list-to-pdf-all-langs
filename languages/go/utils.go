package main

import (
	"fmt"
	"strings"
)

func createPrintUrl(url string) string {
	finalUrl := fmt.Sprintf("https://cifraclub.com%s", url)
	params := ""

	if strings.Contains(finalUrl, "#") {
		splitted := strings.Split(finalUrl, "#")
		finalUrl = splitted[0]
		params = splitted[1]
	}

	if strings.HasSuffix(finalUrl, ".html") {
		finalUrl = fmt.Sprintf("%s/", finalUrl[:len(finalUrl)-5])
	} else if finalUrl[len(finalUrl)-1] != '/' {
		finalUrl += "/"
	}

	if params != "" {
		return fmt.Sprintf("%simprimir.html#footerChords=false&%s", finalUrl, params)
	}
	return fmt.Sprintf("%simprimir.html#footerChords=false", finalUrl)
}

func generateHtml(contents []string) string {
	return fmt.Sprintf(`
	<html>
	<head>
		<link href="https://akamai.sscdn.co/cc/css/0830d.cifra_print.css" media="all" rel="stylesheet" type="text/css"/>
		<meta charset="utf-8">
	</head>
	<body>
		%s
	</body>
	</html>
	`, removeTamA4(strings.Join(contents, "")))
}

func removeTamA4(content string) string {
	return strings.ReplaceAll(content, "tam_a4", "")
}
