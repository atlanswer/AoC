"""
Solving: https://adventofcode.com/2023/day/12
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


@time_this
def solve(data: list[str]) -> int:
    ...


@logger.catch
def main() -> None:
    # data = INPUT_FILE.read_text().splitlines()
    data = str(
        r"""???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""
    ).splitlines()

    result = solve(data)

    logger.debug(f"{result=}")


if __name__ == "__main__":
    main()
