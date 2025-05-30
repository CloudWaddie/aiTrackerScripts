from playwright.sync_api import sync_playwright
import re
import time # Aggiunto per un po' di ritardo.

def handle_route(route, request):
    # This part is chill, let everything go through unless we want to block something.
    route.continue_()

# We'll store all the unique defaultMessages here
all_default_messages = set()

def handle_response(response):
    if response.url.endswith('.js'):
        try:
            text = response.text()
            # Let's get a bit more specific with the regex to avoid false positives
            # This looks for 'defaultMessage:' followed by a string enclosed in single or double quotes
            matches = re.findall(r'defaultMessage\s*:\s*["\'](.*?)["\']', text)
            
            if matches:
                for match in matches:
                    all_default_messages.add(match) # Add to our unique set
        except Exception as e:
            # When things go sideways, we gotta know!
            print(f"Bummer! Error processing {response.url}: {str(e)}")

with sync_playwright() as p:
    # Launching the browser in headless mode to keep it low-key
    browser = p.chromium.launch(headless=True) 
    context = browser.new_context()
    
    # Enable request interception – we're basically the bouncer for network requests
    context.route('**/*', handle_route)
    
    page = context.new_page()
    # Every time a response comes back, we're on it!
    page.on('response', handle_response)
    
    page.set_extra_http_headers({
        # Keeping it real with a fresh User-Agent
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8' # More international vibes
    })
    
    page.goto("https://chatgpt.com/", wait_until='networkidle')
    
    try:
        pass
    except KeyboardInterrupt:
        print("\nStopping, you snapped!)")
    
    browser.close()

# After the browser closes, let's spill the tea on all the unique messages we found
print("\n\n---------------------------------")
print("All unique 'defaultMessage' strings we caught:")
if all_default_messages:
    for msg in sorted(list(all_default_messages)): # Sorting them for a clean look
        print(f"- {msg}")
else:
    print("No unique 'defaultMessage' strings found this time. Bummer!")

# Save the strings into a file
with open("default_messages.txt", "w", encoding="utf-8") as f:
    for msg in sorted(list(all_default_messages)):
        f.write(msg + "\n")