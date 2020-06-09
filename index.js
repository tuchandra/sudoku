// index.js - parsing for LA times
const puppeteer = require("puppeteer");

function getPuzzle (document) {
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
};

async function main() {
    const url = "https://cdn4.amuselabs.com/lat/sudoku?id=latimes-sudoku-expert-20200606&set=latimes-sudoku-expert";
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
    return puzzle
};

main().then((x) => {
    console.log(x);
    process.exit(-1);
});
