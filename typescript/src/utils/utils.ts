export function createPrintUrl(url: string): string {
    let finalUrl = `https://cifraclub.com${url}`;
    let params = "";
    
    if (finalUrl.includes('#')) {
        const splitted = finalUrl.split('#');
        finalUrl = splitted[0];
        params = splitted[1];
    }
    
    if (finalUrl.endsWith(".html")) {
        finalUrl = `${finalUrl.slice(0, -5)}/`;
    } else if (finalUrl[finalUrl.length - 1] !== "/") {
        finalUrl += "/";
    }
    
    return `${finalUrl}imprimir.html#footerChords=false${params ? `&${params}` : ''}`;
}

export function generateHtml(contents: string[]): string {
    return `
    <html>
    <head>
        <link href="https://akamai.sscdn.co/cc/css/0830d.cifra_print.css" media="all" rel="stylesheet" type="text/css"/>
        <meta charset="utf-8">
    </head>
    <body>
        ${removeTamA4(contents.join(''))}
    </body>
    </html>
    `;
}

// The tam_a4 class is what crops the page to A4 size
export function removeTamA4(content: string): string {
    return content.replace(/tam_a4/g, '');
}
