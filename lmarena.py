from playwright.sync_api import sync_playwright
import re

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.set_extra_http_headers({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9'
    })
    with page.expect_response("https://web.lmarena.ai/_next/static/chunks/app/(home)/page-*.js") as first:
        page.goto("https://web.lmarena.ai")
        first_response = first.value
        body = first_response.body()
        print(page.title())
    
    browser.close()
# Convert body to string from a bytes object
body = body.decode('utf-8')
# Find models using regex
model_regex = re.compile('{modelApiId:".*"*.isPrivate:[!][0-1]}')
models = model_regex.findall(body)
# Parse models into a list of dictionaries
dict_strings = re.findall(r'\{.*?\}', models[0])
model_list = []

modelToCheck = input("Enter model name: ")
for d_str in dict_strings:
    if modelToCheck in d_str:
        print(d_str)