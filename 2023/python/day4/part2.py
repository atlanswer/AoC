"""
Solving: https://adventofcode.com/2023/day/4
"""

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


def get_num_matching(line: str) -> int:
    _, numbers = line.split(":")
    winning_numbers, my_numbers = numbers.split("|")

    winning_numbers = set(winning_numbers.split())
    my_numbers = set(my_numbers.split())

    matches = winning_numbers & my_numbers

    return len(matches)


@time_this
def solve(data: list[str]) -> int:
    card_points = list(map(get_num_matching, data))

    num_cards = [1] * len(card_points)

    for i in range(len(card_points)):
        card_point = card_points[i]
        for j in range(i + 1, i + 1 + card_point):
            if j >= len(card_points):
                break
            num_cards[j] += num_cards[i]

    return sum(num_cards)


@logger.catch
def main() -> None:
    data = INPUT_FILE.read_text().splitlines()

    result = solve(data)

    logger.debug(f"{result=}")


if __name__ == "__main__":
    main()
