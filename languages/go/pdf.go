package main

import "github.com/signintech/gopdf"

func createPDF(htmlContent string, filePath string) {
	// Create pdf with all songs which are html strings
	pdf := gopdf.GoPdf{}
	pdf.Start(gopdf.Config{PageSize: *gopdf.PageSizeA4})
	pdf.AddPage()
	pdf.SetLineWidth(1)
	pdf.SetLineType("dashed")
	pdf.SetX(10)
	pdf.SetY(10)
	pdf.SetFont("Arial", "", 14)
	pdf.Cell(nil, htmlContent)
	pdf.WritePdf(filePath)
}
