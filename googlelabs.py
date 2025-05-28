from playwright.sync_api import sync_playwright
import re

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.set_extra_http_headers({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9'
    })
    with page.expect_response("https://labs.google/fx/_next/static/*/_buildManifest.js") as first:
        page.goto("https://labs.google/fx")
        first_response = first.value
        body = first_response.body().decode('utf-8')
    
    browser.close()
pagesRegex = re.compile('"/.*?"')
pages = pagesRegex.findall(body)
pagesWithoutQuotes = [page[1:-1] for page in pages]
print(pagesWithoutQuotes)