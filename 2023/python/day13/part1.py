"""
Solving: https://adventofcode.com/2023/day/13
"""

import time
from functools import wraps
from pathlib import Path
from typing import Callable, TypeVar

from loguru import logger

ReturnType = TypeVar("ReturnType")


def time_this(func: Callable[..., ReturnType]) -> Callable[..., ReturnType]:
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


def get_patterns(data: list[str]) -> list[list[str]]:
    patterns: list[list[str]] = []

    i = 0
    found_start = False
    for j in range(len(data)):
        if not found_start:
            if data[j] != "":
                found_start = True
                i = j
                continue
        else:
            if data[j] == "":
                patterns.append(data[i:j])
                found_start = False
    else:
        if found_start:
            patterns.append(data[i:])

    return patterns


def find_horizontal_mirror(pattern: list[str]) -> int:
    for i in range(len(pattern) - 1):
        if pattern[i + 1] == pattern[i]:
            is_mirror = False
            len_below = len(pattern) - 2 - i
            len_search = min(i, len_below)
            for j in range(1, len_search + 1):
                if pattern[i - j] != pattern[i + 1 + j]:
                    break
            else:
                is_mirror = True
            if is_mirror:
                return i
    return -1


def compare_col(pattern: list[str], i: int, j: int) -> bool:
    for x in range(len(pattern)):
        if pattern[x][i] != pattern[x][j]:
            return False
    return True


def find_vertical_mirror(pattern: list[str]) -> int:
    for i in range(len(pattern[0]) - 1):
        if compare_col(pattern, i, i + 1):
            is_mirror = False
            len_right = len(pattern[0]) - 2 - i
            len_search = min(i, len_right)
            for j in range(1, len_search + 1):
                if not compare_col(pattern, i - j, i + 1 + j):
                    break
            else:
                is_mirror = True
            if is_mirror:
                return i
    return -1


@time_this
def solve(data: list[str]) -> int:
    patterns = get_patterns(data)

    vertical_mirrors = map(find_vertical_mirror, patterns)
    horizontal_mirrors = map(find_horizontal_mirror, patterns)

    result = 0

    for v, h in zip(vertical_mirrors, horizontal_mirrors):
        result += v + 1 if v != -1 else 0
        result += 100 * (h + 1) if h != -1 else 0

    return result


@logger.catch
def main() -> None:
    data = INPUT_FILE.read_text().splitlines()

    result = solve(data)

    logger.debug(f"{result=}")


if __name__ == "__main__":
    main()
