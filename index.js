// index.js - parsing for LA times
const puppeteer = require("puppeteer");

function getLATimesURL(difficulty) {
  // get the URL of today's LA times sudoku
  // difficulty: str, one of "easy", "medium", "hard", "expert"

  // get date as YYYYMMDD
  const today = new Date();
  const year = String(today.getFullYear());
  const month = ("0" + (today.getMonth() + 1)).slice(-2);
  const day = ("0" + today.getDate()).slice(-2);
  const dateStr = year + month + day;

  const url =
    "https://cdn4.amuselabs.com/lat/sudoku?id=latimes-sudoku-" +
    difficulty +
    "-" +
    dateStr +
    "&set=latimes-sudoku-" +
    difficulty;

  return url;
}

async function getLATimesPuzzle(url) {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.goto(url);

  const puzzle = await page.evaluate(() => {
    let labels = [];
    for (cell of document.getElementsByClassName("box")) {
      if (cell.classList.contains("prerevealed-box")) {
        labels.push(parseInt(cell.firstChild.innerText));
      } else {
        labels.push(0);
      }
    }
    let text = "https://sudokuexchange.com/play/?s=" + labels.join("");
    return text;
  });
  return puzzle;
}

async function main() {
  const difficulties = ["easy", "medium", "hard", "expert"];
  for (diff of difficulties) {
    url = getLATimesURL(diff);
    puzzle_link = await getLATimesPuzzle(url);
    console.log(diff, puzzle_link);
  }
}

main().then((x) => {
  process.exit();
});
