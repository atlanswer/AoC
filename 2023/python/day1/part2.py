"""
Solving: https://adventofcode.com/2023/day/1#part2
"""

import time
from functools import reduce, wraps
from pathlib import Path

from loguru import logger
from typing import Callable

from operator import add

logger.add("log.log")


def time_this(func: Callable[..., None]):
    @wraps(func)
    def timer_wrapper(*args: None, **kwargs: None):
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


DIGIT_LETTERS = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]


def is_digit(c: str) -> bool:
    return ord("0") <= ord(c) <= ord("9")


def get_cal_value_line(line: str) -> int:
    first_digit = last_digit = 0
    for c in line:
        if is_digit(c):
            first_digit = int(c)
            break
    for c in reversed(line):
        if is_digit(c):
            last_digit = int(c)
            break
    return first_digit * 10 + last_digit


@logger.catch
@time_this
def main() -> None:
    data = INPUT_FILE.read_text().splitlines()
    data = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""

    cal_values = map(get_cal_value_line, data)
    result = reduce(add, cal_values)

    logger.info(f"{result=}")


if __name__ == "__main__":
    main()
