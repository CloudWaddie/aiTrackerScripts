import { chromium } from "playwright";
import fs from 'fs';
import Table from 'terminal-table';

let t = new Table({borderStyle: 'unicode'});
t.push(['ID', 'Name']);
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

const leaderboardIdRegex = /{\\["']leaderboards\\["']:\[{\\["']id\\["']:\\".+?\\["'],\\["']name\\["']:\\["'].+?\\["']/g;
const leaderboardIds = body.match(leaderboardIdRegex) || [];
// Remove all slashes from the leaderBoardIds
const leaderboardIdsWithoutSlashes = leaderboardIds.map((item) => item.replace(/\\/g, ''));
// Add }]} to each item in the list to make it valid JSON
const leaderboardIdsWithoutSlashesAndBrackets = leaderboardIdsWithoutSlashes.map((item) => item + '}]}');
// Parse the JSON
const leaderboardIdsJson = leaderboardIdsWithoutSlashesAndBrackets.map((item) => JSON.parse(item));

// Log each item
leaderboardIdsJson.forEach((item) => {
    t.push([item.leaderboards[0].id, item.leaderboards[0].name]);
});
await page.close();
browser.close();

console.log("Leaderboard IDs:\n" + t);

// Now we make render the leaderboards using a new regex
let leaderboard_individual_regex;
let leaderboard_individual;
let leaderboard_individual_without_slashes;
let leaderboard_individual_json;
let t2;

for (let i = 0; i < leaderboardIdsJson.length; i++) {
    t2 = new Table({borderStyle: 'unicode'});
    t2.push(['Model Name', 'Rank']);
    // Escape any special regex characters in the dynamic ID
    // This is still important as a best practice, even if UUIDs don't commonly have them.
    const escapedLeaderboardId = leaderboardIdsJson[i].leaderboards[0].id.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

    // Construct the regex using a RegExp object
    // We need to match the literal backslash before the quote.
    // So, `\\"` in the regex will match `\"` in the `body` string.
    const leaderboard_individual_regex_string = 
        `{\\\\"id\\\\":\\\\"[a-zA-Z0-9-]+?\\\\",\\\\\\"leaderboardId\\\\":\\\\"${escapedLeaderboardId}\\\\",\\\\\\"modelName\\\\".+?\\\\\\"rank\\\\":\\d+?}`;
    
    // Now, create the RegExp object with the 'g' flag
    const leaderboard_individual_regex = new RegExp(leaderboard_individual_regex_string, 'g');

    leaderboard_individual = body.match(leaderboard_individual_regex) || [];
    console.log('Found ' + leaderboard_individual.length + ' items for ' + leaderboardIdsJson[i].leaderboards[0].name);
    
    // Remove all slashes from the matched items before parsing
    // This is important because the regex picked up the literal backslashes
    leaderboard_individual_without_slashes = leaderboard_individual.map((item) => item.replace(/\\/g, ''));
    
    // Parse the JSON
    try {
        leaderboard_individual_json = leaderboard_individual_without_slashes.map((item) => JSON.parse(item));
    } catch (e) {
        console.error("Failed to parse JSON for " + leaderboardIdsJson[i].leaderboards[0].name + ":", e);
    }
    leaderboard_individual_json.forEach((item) => {
        t2.push([item.modelName, item.rank]);
    });
    console.log('Leaderboard for type ' + leaderboardIdsJson[i].leaderboards[0].name + ':\n' + t2);
}