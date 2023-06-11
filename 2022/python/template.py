"""
Solving: https://adventofcode.com/2022/day/1
"""

import time
from functools import wraps
from pathlib import Path

from loguru import logger

logger.add("log.log")


def time_this(func):
    @wraps(func)
    def timer_wrapper(*args, **kwargs):
        t_start = time.perf_counter()
        result = func(*args, **kwargs)
        t_finish = time.perf_counter()
        logger.info(f"Execution time: {t_finish - t_start:.4f} seconds.")
        return result
    return timer_wrapper

AOC_DAY = Path(__file__).parent.name
INPUT_DIR = Path(__file__).parents[2] / "input"
INPUT_FILE = INPUT_DIR / AOC_DAY / "input.txt"
assert INPUT_FILE.exists(), "Input file not present."


@logger.catch
@time_this
def main() -> None:
    data = INPUT_FILE.read_text()

    logger.debug(data)


if __name__ == "__main__":
    main()
