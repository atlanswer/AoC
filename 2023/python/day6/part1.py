"""
Solving: https://adventofcode.com/2023/day/6
"""

import time
from functools import wraps
from pathlib import Path

from loguru import logger
from typing import Any, Callable, Iterable


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


def get_records(data: list[str]) -> Iterable[tuple[int, int]]:
    assert len(data) == 2

    _, times = data[0].split(":")
    times = map(int, times.split())

    _, distances = data[1].split(":")
    distances = map(int, distances.split())

    return zip(times, distances)


@time_this
def solve(data: list[str]) -> int:
    ...


@logger.catch
def main() -> None:
    # data = INPUT_FILE.read_text().splitlines()
    data = str(
        """Time:      7  15   30
Distance:  9  40  200"""
    ).splitlines()

    result = solve(data)

    logger.debug(f"{result=}")


if __name__ == "__main__":
    main()
