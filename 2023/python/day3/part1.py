"""
Solving: https://adventofcode.com/2023/day/3
"""

import string
import time
from functools import wraps
from pathlib import Path

from loguru import logger
from typing import Any, Callable


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

SYMBOLS = set(string.punctuation) - {"."}


def find_part_number(data: list[list[str]], i: int, j: int) -> int:
    sum_part_number = 0
    adj_idx = [
        (i - 1, j - 1),
        (i - 1, j),
        (i - 1, j + 1),
        (i, j - 1),
        (i, j + 1),
        (i + 1, j - 1),
        (i + 1, j),
        (i + 1, j + 1),
    ]
    data[i][j] = "."
    for x, y in adj_idx:
        if x < 0 or x >= len(data) or y < 0 or y >= len(data[0]):
            continue
        if not data[x][y].isdecimal():
            continue
        yl = y - 1
        yr = y + 1
        while yl >= 0 and data[x][yl].isdecimal():
            yl -= 1
        while yr < len(data[0]) and data[x][yr].isdecimal():
            yr += 1
        sum_part_number += int("".join(data[x][yl + 1 : yr]))
        data[x][yl + 1 : yr] = "." * (yr - yl - 1)

    return sum_part_number


@time_this
def solve(data: list[list[str]], i: int = 0, j: int = 0) -> int:
    sum_part_numbers = 0

    for i in range(i, len(data)):
        for j in range(len(data[0])):
            if data[i][j] not in SYMBOLS:
                continue
            sum_part_numbers += find_part_number(data, i, j)

    return sum_part_numbers


@logger.catch
def main() -> None:
    data = INPUT_FILE.read_text().splitlines()
    data = list(map(list, data))

    result = solve(data)

    logger.debug(f"{result=}")


if __name__ == "__main__":
    main()
