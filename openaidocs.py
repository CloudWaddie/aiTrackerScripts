from playwright.sync_api import sync_playwright
import re
articleList = []
alreadyVisited = []

def initialiseBrowser(p):
    browser = p.chromium.launch(headless=True)
    return browser

def getPage(url, browserInstance):
    page = browserInstance.new_page()
    page.set_extra_http_headers({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9'
        })
    page.goto(url)
    body = page.content()
    page.close()
    return body

def checkForArticles(body):
    find_articles = re.compile('<a .+? href="(https://help.openai.com/en/articles/.+?)" .+?</a>')
    articles = find_articles.findall(body)
    #print(articles)
    return articles

def checkForCollections(body):
    collectionsList = []
    find_collections = re.compile('<a .+? href="(https://help.openai.com/en/collections/.+?)" .+?</a>')
    collections = find_collections.findall(body)
    for collection in collections:
        print(f"checkForCollections: Found raw collections: {collection}")
        collectionsList.append(collection)
    return collectionsList

def mainCheck(body, articleList, intialBrowser):
    articleList.extend(checkForArticles(body))
    collectionsList = checkForCollections(body)
    if collectionsList:
        for collection in collectionsList:
            if collection not in alreadyVisited:
                response = getPage(collection, intialBrowser)
                alreadyVisited.append(collection)
                mainCheck(response, articleList, intialBrowser)

with sync_playwright() as p:
    intialBrowser = initialiseBrowser(p)
    body = getPage("https://help.openai.com/en/", intialBrowser)
    mainCheck(body, articleList, intialBrowser)
    intialBrowser.close()
    #print(articleList)