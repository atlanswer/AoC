"""
Solving: https://adventofcode.com/2024/day/4
"""

import time
import logging
from functools import wraps
from pathlib import Path
from typing import Callable, TypeVar

from rich.logging import RichHandler


ReturnType = TypeVar("ReturnType")


def time_this(func: Callable[..., ReturnType]) -> Callable[..., ReturnType]:
    @wraps(func)
    def timer_wrapper(*args: ..., **kwargs: ...):  # pyright: ignore[reportAny]
        t_start = time.perf_counter()
        result = func(*args, **kwargs)
        t_finish = time.perf_counter()
        logger.debug(f"Execution time: {t_finish - t_start:.4f} seconds.")
        return result

    return timer_wrapper


def search_xmas(data: list[str], r: int, c: int) -> int:
    count = 0

    target = list("XMAS")

    # up left
    if r - 3 >= 0 and c - 3 >= 0:
        s = [data[r - i][c - i] for i in range(4)]
        if s == target:
            count += 1

    # up
    if r - 3 >= 0:
        s = [data[r - i][c] for i in range(4)]
        if s == target:
            count += 1

    # up right
    if r - 3 >= 0 and c + 3 < len(data[0]):
        s = [data[r - i][c + i] for i in range(4)]
        if s == target:
            count += 1

    # right
    if c + 3 < len(data[0]):
        s = [data[r][c + i] for i in range(4)]
        if s == target:
            count += 1

    # down right
    if r + 3 < len(data) and c + 3 < len(data[0]):
        s = [data[r + i][c + i] for i in range(4)]
        if s == target:
            count += 1

    # down
    if r + 3 < len(data):
        s = [data[r + i][c] for i in range(4)]
        if s == target:
            count += 1

    # down left
    if r + 3 < len(data) and c - 3 >= 0:
        s = [data[r + i][c - i] for i in range(4)]
        if s == target:
            count += 1

    # left
    if c - 3 >= 0:
        s = [data[r][c - i] for i in range(4)]
        if s == target:
            count += 1

    return count


@time_this
def solve(data: list[str]) -> int:
    res = 0

    for r in range(len(data)):
        for c in range(len(data[0])):
            if data[r][c] != "X":
                continue
            res += search_xmas(data, r, c)

    return res


def main() -> None:
    data = INPUT_FILE.read_text().splitlines()

    result = solve(data)

    logger.info(f"{result=}")


if __name__ == "__main__":
    AOC_DAY = Path(__file__).parent.name
    INPUT_DIR = Path(__file__).parents[2] / "input"
    INPUT_FILE = INPUT_DIR / AOC_DAY / "input.txt"
    assert INPUT_FILE.exists(), "Input file not present."

    logger = logging.getLogger(__name__)
    handler = RichHandler(
        log_time_format="[%m/%d %H:%M:%S]",
        markup=True,
        rich_tracebacks=True,
        tracebacks_show_locals=True,
    )
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    main()
