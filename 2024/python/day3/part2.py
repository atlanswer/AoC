"""
Solving: https://adventofcode.com/2024/day/3#part2
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


@time_this
def solve(data: str) -> int:
    res = 0
    idx = 0
    left = 0
    right = 0
    enabled = True

    while idx < len(data):
        # find cond
        if data[idx : idx + 4] == "do()":
            enabled = True
            idx += 4
            continue
        if data[idx : idx + 7] == "don't()":
            enabled = False
            idx += 7
            continue

        # find mul(
        if data[idx : idx + 4] != "mul(":
            idx += 1
            continue
        idx += 4

        # find ,
        idx_comma = data.find(",", idx, idx + 4)
        if idx_comma == -1:
            continue

        # find left
        if not data[idx:idx_comma].isdigit():
            continue
        left = int(data[idx:idx_comma])

        # find )
        idx_r_par = data.find(")", idx_comma + 1, idx_comma + 5)
        if idx_r_par == -1:
            continue
        right = int(data[idx_comma + 1 : idx_r_par])

        idx = idx_r_par + 1
        res += (left * right) if enabled else 0

    return res


def main() -> None:
    data = INPUT_FILE.read_text()

    result = solve(data)

    logger.info(f"{result=}")


if __name__ == "__main__":
    AOC_YEAR = 2024
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
