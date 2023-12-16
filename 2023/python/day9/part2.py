"""
Solving: https://adventofcode.com/2023/day/9#part2
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


def get_next_history_value(history: list[int]) -> int:
    end = len(history) - 1
    first_values: list[int] = [history[0]]

    while end >= 1:
        is_all_zero = True
        for i in range(end):
            history[i] = history[i + 1] - history[i]
            if history[i] != 0:
                is_all_zero = False
        first_values.append(history[0])
        if is_all_zero:
            break
        end -= 1

    result = 0
    while len(first_values) > 0:
        result = first_values.pop() - result

    return result


def str_to_list_int(s: str) -> list[int]:
    return list(map(int, s.split()))


@time_this
def solve(data: list[str]) -> int:
    history = map(str_to_list_int, data)
    next_values = map(get_next_history_value, history)
    return sum(next_values)


@logger.catch
def main() -> None:
    data = INPUT_FILE.read_text().splitlines()

    result = solve(data)

    logger.debug(f"{result=}")


if __name__ == "__main__":
    main()
