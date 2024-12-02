"""
Solving: https://adventofcode.com/2024/day/1
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
def solve(data: list[str]) -> int: ...


def main() -> None:
    data = INPUT_FILE.read_text().splitlines()

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
