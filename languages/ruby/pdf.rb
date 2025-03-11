require 'puppeteer-ruby'

class Pdf
  def html_to_pdf(html, pdfFilePath)
    Puppeteer.launch(headless: true) do |browser|
      page = browser.new_page
      page.set_content(html)
      page.pdf(path: pdfFilePath, format: 'A4')
    end
  end
end