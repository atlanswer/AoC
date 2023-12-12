"""
Solving: https://adventofcode.com/2023/day/1#part2
"""

import time
from functools import reduce, wraps
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


DIGIT_LETTERS = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]


def is_digit(c: str) -> bool:
    return ord("0") <= ord(c) <= ord("9")


def forward_search(s: str) -> int:
    for i in range(0, len(s)):
        if is_digit(s[i]):
            return int(s[i])
        for j in range(0, len(DIGIT_LETTERS)):
            d = DIGIT_LETTERS[j]
            ld = len(d)
            if len(s) - i < ld:
                continue
            if s[i : i + ld] == d:
                return j + 1
    raise ValueError("Value not found.")


def backward_search(s: str) -> int:
    for i in range(len(s) - 1, -1, -1):
        if is_digit(s[i]):
            return int(s[i])
        for j in range(0, len(DIGIT_LETTERS)):
            d = DIGIT_LETTERS[j]
            ld = len(d)
            if len(s) - i < ld:
                continue
            if s[i : i + ld] == d:
                return j + 1
    raise ValueError("Value not found.")


def get_cal_value_line(line: str) -> int:
    first_digit = forward_search(line)
    last_digit = backward_search(line)
    return first_digit * 10 + last_digit


@time_this
def solve(data: list[str]) -> int:
    cal_values = map(get_cal_value_line, data)
    result = reduce(add, cal_values)
    return result


@logger.catch
def main() -> None:
    data = INPUT_FILE.read_text().splitlines()

    result = solve(data)
    logger.info(f"{result=}")


if __name__ == "__main__":
    main()
