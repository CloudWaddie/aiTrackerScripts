from playwright.sync_api import sync_playwright
import re

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.set_extra_http_headers({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9'
    })
    with page.expect_response("https://www.gstatic.com/_/mss/boq-bard-web/_/js/**/m=CfTzb*") as first:
        page.goto("https://gemini.google.com/updates")
        first_response = first.value
        body = first_response.body()
        print(page.title())
    
    browser.close()
body = body.decode('utf-8')
regex_string = re.compile('this\\..{3}="([0-9]{4}\\.[0-9]{2}\\.[0-9]{2})"')
matches = regex_string.findall(body)
regex_string = re.compile('([0-9]{4}\\.[0-9]{2}\\.[0-9]{2})')
matches = regex_string.findall(body)
print(matches)