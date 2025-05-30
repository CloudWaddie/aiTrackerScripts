import { chromium } from "playwright";
import fs from 'fs';

const browser = await chromium.launch();
const page = await browser.newPage();
await page.setExtraHTTPHeaders({
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9'
});
await page.goto('https://lmarena.ai/leaderboard');
const body = await page.content();
// Save the body to a file
fs.writeFileSync('body.html', body);

const text_leaderboard_regex = /{\\['"]id\\['"]:\\['"].+?\\['"],\\['"]rank\\['"]:\d+?}/g;
const text_leaderboard = body.match(text_leaderboard_regex) || [];
// Remove all slashes so it can parse as JSON
const json_leaderboard = text_leaderboard.map((item) => item.replace(/\\/g, ''));

console.log(json_leaderboard);

browser.close();
