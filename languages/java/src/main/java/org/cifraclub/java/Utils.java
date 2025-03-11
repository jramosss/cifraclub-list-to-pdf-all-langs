package org.cifraclub.java;

public class Utils {
    public static String createPrintUrl(String url) {
        String finalUrl = "https://cifraclub.com" + url;
        String params = "";

        if (finalUrl.contains("#")) {
            String[] splitted = finalUrl.split("#");
            finalUrl = splitted[0];
            params = splitted[1];
        }

        if (finalUrl.endsWith(".html")) {
            finalUrl = finalUrl.substring(0, finalUrl.length() - 5) + "/";
        } else if (finalUrl.charAt(finalUrl.length() - 1) != '/') {
            finalUrl += "/";
        }

        return finalUrl + "imprimir.html#footerChords=false" + (params.isEmpty() ? "" : "&" + params);
    }

    public static String generateHtml(String[] contents) {
        return """
        <html>
            <head>
                <link href="https://akamai.sscdn.co/cc/css/0830d.cifra_print.css" media="all" rel="stylesheet" type="text/css"/>
                <meta charset="utf-8">
            </head>
            <body>
              \s""" + removeTamA4(String.join("", contents)) + """
            </body>
        </html>
        """;
    }

    private static String removeTamA4(String content) {
        return content.replace("tam_a4", "");
    }
}
