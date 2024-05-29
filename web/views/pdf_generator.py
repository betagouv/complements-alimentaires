from django.http import HttpResponse

from playwright.sync_api import sync_playwright

url = "http://localhost:8000/lettre-officielle/"
filename = "file.pdf"


def generate_pdf(request) -> HttpResponse:
    def run_playwright():
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(url)
            pdf_content = page.pdf(
                format="A4",
                margin={
                    "top": "2cm",
                    "bottom": "2cm",
                    "left": "2cm",
                    "right": "2cm",
                },
            )
            browser.close()
            return pdf_content

    pdf_content = run_playwright()

    response = HttpResponse(pdf_content, content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response
