from playwright.sync_api import sync_playwright
import re

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.set_extra_http_headers({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9'
    })
    try:
        page.goto("https://lmarena.ai")
        input("Press Enter when you're ready to continue...")
        body = page.content()
        # Screenchot
        page.screenshot(path="screenshot.png")
        print(body)
        print(f"Page title: {page.title()}")
        model_regex = re.compile(r'"publicName\\":\\"(.+?)\\"', re.MULTILINE | re.DOTALL)
        models = model_regex.findall(body)
        print(f"Found models: {models}")
    except Exception as e:
        print(f"Bummer! Ran into an issue: {e}")
    finally:
        browser.close()
        page.close()