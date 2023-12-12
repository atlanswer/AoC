"""
Solving: https://adventofcode.com/2023/day/2#part2
"""

import time
from functools import reduce, wraps
from operator import add, mul
from pathlib import Path
from typing import Any, Callable

from loguru import logger


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


def get_game_power(line: str) -> int:
    bag = {"red": 0, "green": 0, "blue": 0}

    _, game_details = line.split(":")
    game_details = game_details.split(";")

    for game in game_details:
        cubes = game.split(",")
        for cube in cubes:
            num, cube_color = cube.split()
            num = int(num)
            if num > bag[cube_color]:
                bag[cube_color] = num

    return reduce(mul, bag.values())


@time_this
def solve(data: list[str]) -> int:
    possible_game_ids = map(get_game_power, data)
    result = reduce(add, possible_game_ids)

    return result


@logger.catch
def main() -> None:
    data = INPUT_FILE.read_text().splitlines()

    result = solve(data)

    logger.debug(f"{result=}")


if __name__ == "__main__":
    main()
