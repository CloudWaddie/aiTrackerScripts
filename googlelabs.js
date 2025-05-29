import { chromium } from 'playwright';

const browser = await chromium.launch();
const page = await browser.newPage();
const responsePromise = page.waitForResponse('https://labs.google/fx/_next/static/*/_buildManifest.js');
await page.goto('https://labs.google/fx');
const response = await responsePromise;
const body = await response.text();

const pagesRegex = /"\/.*?"/g;
const pages = body.match(pagesRegex) || [];
const pagesWithoutQuotes = pages.map(page => page.slice(1, -1));
console.log(pagesWithoutQuotes);

browser.close();