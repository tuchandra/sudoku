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


def get_latimes():
    """Scrape all four LA Times puzzles"""

    today = datetime.now().strftime(r"%Y%m%d")
    for difficulty in ("easy", "medium", "hard", "expert"):
        url = f"https://cdn4.amuselabs.com/lat/sudoku?id=latimes-sudoku-{difficulty}-{today}&set=latimes-sudoku-{difficulty}"
        text = requests.get(url).text
        soup = BeautifulSoup(text, features="html.parser")





if __name__ == "__main__":
    puzzles = get_nytimes()
    print(puzzles)
