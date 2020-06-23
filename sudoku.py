"""
sudoku.py -- scrape common web sources for Sudokus
"""

import json
from datetime import datetime
from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup

sudokuexchange_head = "https://sudokuexchange.com/play/?s="


@dataclass
class Puzzle:
    name: str
    source_url: str
    sudokuexchange_url: str

    def __repr__(self):
        # format as markdown
        return f"**{self.name}** ([source]({self.source_url})): [SudokuExchange link]({self.sudokuexchange_url})"


def get_nytimes():
    """Scrape all three NY Times puzzles"""

    nyt_url = "https://www.nytimes.com/puzzles/sudoku/easy"
    text = requests.get(nyt_url).text
    soup = BeautifulSoup(text, features="html.parser")

    # find the script that starts with `window.gameData =`
    # usually the first but who knows
    for script in soup.find_all("script", type="text/javascript"):
        if not script.contents:
            continue

        contents = script.contents[0]
        start_str = "window.gameData = "
        if contents.startswith(start_str):
            contents = contents.replace(start_str, "")
            puzzle_info = json.loads(contents)

            break

    # now we have puzzle_info as a dict with keys easy, medium, hard
    # and some levels of nesting; get the puzzle information and
    # create the SudokuExchange link
    puzzles = []
    for difficulty in ("easy", "medium", "hard"):
        digits = puzzle_info[difficulty]["puzzle_data"]["puzzle"]
        digits_str = "".join(str(x) for x in digits)

        source_url = nyt_url.replace("easy", "difficulty")
        se_url = f"{sudokuexchange_head}{digits_str}"
        puzzles.append(Puzzle(f"NY Times {difficulty}", source_url, se_url))

    return puzzles


def get_dailysudoku():
    """Get puzzle from dailysudoku.com"""

    year = datetime.now().year
    month = datetime.now().month
    day = datetime.now().day

    url = f"http://www.dailysudoku.com/cgi-bin/sudoku/get_board.pl?year={year}&month={month}&day={day}"
    data = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0"
        },
    ).json()

    numbers = data["numbers"].replace(".", "0")
    return Puzzle("DailySudoku.com", url, f"{sudokuexchange_head}{numbers}")


def get_tribune():
    """Get puzzle from Tribune Content Agency"""

    # not sure how often this expires
    api_key = ("b366a2d09d81e980a1e3c3eac8ddbe524a3d9a79d88d6e4e92495f8a10e3246a",)
    today = datetime.now().strftime(r"%m/%d/%Y")
    form_data = {
        "apiKey": api_key,
        "productId": "sudoku",
        "publicationDate": today,
        "ldt": today,
    }

    headers = {"Accept": "application/json, text/javascript, */*; q=0.01"}

    data = requests.post(
        "https://puzzles.tribunecontentagency.com/puzzles/pzzResource/puzzle.do",
        data=form_data,
        headers=headers,
    ).json()

    # this just handles the structure of the JSON they return
    numbers = []
    for cell in data["puzzleDetails"]["gCells"]:
        # check if cell was filled out or not
        if cell["qcell"]:
            numbers.append(cell["cellVal"])
        else:
            numbers.append("0")

    cell_string = "".join(numbers)
    return Puzzle(
        "Chicago Tribune",
        "https://www.chicagotribune.com/entertainment/games/ct-sudoku-daily-htmlstory.html",
        f"{sudokuexchange_head}{cell_string}",
    )


def get_usatoday():
    """Get the puzzle from USA Today"""

    today = datetime.now().strftime(r"%Y-%m-%d")

    # not sure how long this URL is valid
    url = f"https://gamedata.services.amuniversal.com/c/uupuz/l/U2FsdGVkX18CR3EauHsCV8JgqcLh1ptpjBeQ%2Bnjkzhu8zNO00WYK6b%2BaiZHnKcAD%0A9vwtmWJp2uHE9XU1bRw2gA%3D%3D/g/ussud/d/{today}/data.json"
    data = requests.get(url).json()

    # this just handles the structure of the JSON they return
    numbers = []
    lines = [f"line{i}" for i in range(1, 10)]
    for key in lines:
        numbers.append(data["Layout"][key])

    numbers_string = "".join(numbers).replace("-", "0")
    return Puzzle(
        "USA Today",
        "https://puzzles.usatoday.com/sudoku/",
        f"{sudokuexchange_head}{numbers_string}",
    )


if __name__ == "__main__":
    nytimes_puzzles = get_nytimes()
    for puzzle in nytimes_puzzles:
        print(puzzle)

    dailysudoku_puzzle = get_dailysudoku()
    print(dailysudoku_puzzle)

    tribune_puzzle = get_tribune()
    print(tribune_puzzle)

    usatoday_puzzle = get_usatoday()
    print(usatoday_puzzle)
