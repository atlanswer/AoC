"""
Solving: https://adventofcode.com/2023/day/2
"""

import time
from functools import wraps, reduce
from pathlib import Path

from loguru import logger
from typing import Any, Callable

from operator import add


def time_this(func: Callable[..., Any]):
    @wraps(func)
    def timer_wrapper(*args: ..., **kwargs: ...):
        t_start = time.perf_counter()
        result = func(*args, **kwargs)
        t_finish = time.perf_counter()
        logger.info(f"Execution time: {t_finish - t_start:.4f} seconds.")
        return result

    return timer_wrapper


AOC_YEAR = 2023
AOC_DAY = Path(__file__).parent.name
INPUT_DIR = Path(__file__).parents[2] / "input"
INPUT_FILE = INPUT_DIR / AOC_DAY / "input.txt"
assert INPUT_FILE.exists(), "Input file not present."


BAG = {"red": 12, "green": 13, "blue": 14}


def get_possible_game_id(line: str) -> int:
    game_title, game_details = line.split(":")

    _, game_id = game_title.split()
    game_id = int(game_id)

    game_details = game_details.split(";")

    for game in game_details:
        cubes = game.split(",")
        for cube in cubes:
            num, cube_color = cube.split()
            if int(num) > BAG[cube_color]:
                return 0

    return game_id


@time_this
def solve(data: list[str]) -> int:
    possible_game_ids = map(get_possible_game_id, data)
    result = reduce(add, possible_game_ids)

    return result


@logger.catch
def main() -> None:
    data = INPUT_FILE.read_text().splitlines()

    result = solve(data)

    logger.debug(f"{result=}")


if __name__ == "__main__":
    main()
