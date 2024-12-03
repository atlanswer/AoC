"""
Solving: https://adventofcode.com/2024/day/2
"""

import time
import logging
from functools import wraps
from pathlib import Path
from typing import Callable, Literal, TypeVar

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


Trend = Literal["increasing", "decreasing", "unknown"]


def check_safe(
    levels: list[int],
    idx: int = 1,
    trend: Trend = "unknown",
) -> bool:
    if idx >= len(levels):
        return True

    diff = levels[idx] - levels[idx - 1]

    if abs(diff) < 1 or abs(diff) > 3:
        return False

    cur_trend: Trend = "unknown"

    if diff > 0:
        cur_trend = "increasing"
    else:
        cur_trend = "decreasing"

    if cur_trend != trend and trend != "unknown":
        return False

    return check_safe(levels, idx + 1, cur_trend)


@time_this
def solve(data: list[str]) -> int:
    res = 0

    for line in data:
        levels = [int(i) for i in line.split()]

        if check_safe(levels):
            res += 1

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