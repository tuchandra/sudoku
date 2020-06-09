"""
sudoku.py -- scrape common web sources for Sudokus
"""

import json
from datetime import datetime

import requests
from bs4 import BeautifulSoup

sudokuexchange_head = "https://sudokuexchange.com/play/?s="


def get_nytimes():
    """Scrape all three NY Times puzzles"""

    url = "https://www.nytimes.com/puzzles/sudoku/easy"
    text = requests.get(url).text
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
    puzzles = {}
    for difficulty in ("easy", "medium", "hard"):
        digits = puzzle_info[difficulty]["puzzle_data"]["puzzle"]
        digits_str = "".join(str(x) for x in digits)
        puzzles[f"NY Times {difficulty}"] = f"{sudokuexchange_head}{digits_str}"

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
    return f"{sudokuexchange_head}{numbers}"


def get_sudokuuk():
    """Scrape daily puzzle from sudoku.org.uk"""

    url = "http://www.sudoku.org.uk/daily.asp"


def get_guardian():
    """Scrape irregular puzzles from The Guardian"""

    url = "https://www.theguardian.com/lifeandstyle/series/sudoku-hard"


def get_latimes():
    """Scrape all four LA Times puzzles"""

    today = datetime.now().strftime(r"%Y%m%d")
    for difficulty in ("easy", "medium", "hard", "expert"):
        url = f"https://cdn4.amuselabs.com/lat/sudoku?id=latimes-sudoku-{difficulty}-{today}&set=latimes-sudoku-{difficulty}"
        text = requests.get(url).text
        soup = BeautifulSoup(text, features="html.parser")


if __name__ == "__main__":
    for sudoku_fetcher in (get_nytimes, get_dailysudoku):
        print(sudoku_fetcher())
