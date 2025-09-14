namespace cifraclub_list_to_pdf_csharp;

public class Utils
{
    public static string CreatePrintUrl(string url)
    {
        // url starts with /
        var finalUrl = "https://cifraclub.com" + url;
        var _params = String.Empty;

        if (finalUrl.Contains("#"))
        {
            var splitted = finalUrl.Split('#');
            finalUrl = splitted[0];
            _params = splitted[1];
        }

        if (finalUrl.EndsWith(".html"))
            finalUrl = finalUrl.Substring(0, finalUrl.Length - ".html".Length);
        else if (finalUrl[^1] != '/')
            finalUrl += "/";
        
        return finalUrl + "imprimir.html#footerChords=false" + (_params != string.Empty ? '&' + _params : String.Empty);
    }
    
    private static string RemoveTamA4(string html)
    {
        return html.Replace("tam_a4", "");
    }
    
    public static string GenerateHtml(string[] contents)
    {
        return $@"
            <html>
            <head>
            <link href=""https://akamai.sscdn.co/cc/css/0830d.cifra_print.css"" media=""all"" rel=""stylesheet"" type=""text/css""/>
            <meta charset=""utf-8"">
            </head>
            <body>
            {RemoveTamA4(string.Join("", contents))}
            </body>
            </html>
            ";
    }
}