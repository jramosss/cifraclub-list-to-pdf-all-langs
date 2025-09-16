package main

import (
	"log"

	"github.com/playwright-community/playwright-go"
)

func createPDF(htmlContent string, filePath string) {
	// Launch Playwright browser (equivalent to TypeScript implementation)
	pw, err := playwright.Run()
	if err != nil {
		log.Fatalf("could not start playwright: %v", err)
	}
	defer pw.Stop()

	browser, err := pw.Chromium.Launch(playwright.BrowserTypeLaunchOptions{
		Headless: playwright.Bool(true),
	})
	if err != nil {
		log.Fatalf("could not launch browser: %v", err)
	}
	defer browser.Close()

	page, err := browser.NewPage()
	if err != nil {
		log.Fatalf("could not create page: %v", err)
	}

	// Set the HTML content (equivalent to page.setContent in TypeScript)
	err = page.SetContent(htmlContent)
	if err != nil {
		log.Fatalf("could not set content: %v", err)
	}

	// Generate PDF with A4 format (equivalent to page.pdf in TypeScript)
	_, err = page.PDF(playwright.PagePdfOptions{
		Path:   playwright.String(filePath),
		Format: playwright.String("A4"),
	})
	if err != nil {
		log.Fatalf("could not create PDF: %v", err)
	}

	log.Printf("PDF generated successfully: %s", filePath)
}
