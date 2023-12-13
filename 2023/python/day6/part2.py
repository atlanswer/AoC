"""
Solving: https://adventofcode.com/2023/day/6#part2
"""

import time
from functools import reduce, wraps
from math import ceil, floor, sqrt
from operator import mul
from pathlib import Path
from typing import Any, Callable, Iterable

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


def get_records(data: list[str]) -> Iterable[tuple[int, int]]:
    assert len(data) == 2

    _, times = data[0].split(":")
    times = "".join(times.split())
    times = int(times)

    _, distances = data[1].split(":")
    distances = "".join(distances.split())
    distances = int(distances)

    return [(times, distances)]


def get_num_ways(race: tuple[int, int]) -> int:
    t, r = race

    t1 = (t - sqrt(t**2 - 4 * r)) / 2
    t1 = ceil(t1) if ceil(t1) != floor(t1) else ceil(t1) + 1
    t2 = (t + sqrt(t**2 - 4 * r)) / 2
    t2 = floor(t2) if floor(t2) != ceil(t2) else floor(t2) - 1

    logger.debug(f"{t1=} | {t2=}")

    return t2 - t1 + 1


@time_this
def solve(data: list[str]) -> int:
    records = get_records(data)

    return reduce(mul, map(get_num_ways, records))


@logger.catch
def main() -> None:
    data = INPUT_FILE.read_text().splitlines()

    result = solve(data)

    logger.debug(f"{result=}")


if __name__ == "__main__":
    main()
