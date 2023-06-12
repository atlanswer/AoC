"""
Solving: https://adventofcode.com/2022/day/8#part2
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
    data = INPUT_FILE.read_text().splitlines()

#     data = r"""30373
# 25512
# 65332
# 33549
# 35390""".splitlines()

    data = [[int(c) for c in r] for r in data]

    max_scenic_score = 0

    for r in range(1, len(data) - 1):
        for c in range(1, len(data[0]) - 1):
            house_height = data[r][c]

            d_left = 0
            for i in range(c - 1, -1, -1):
                d_left += 1
                if data[r][i] >= house_height:
                    break

            d_right = 0
            for i in range(c + 1, len(data[0])):
                d_right += 1
                if data[r][i] >= house_height:
                    break

            d_up = 0
            for i in range(r - 1, -1, -1):
                d_up += 1
                if data[i][c] >= house_height:
                    break

            d_down = 0
            for i in range(r + 1, len(data)):
                d_down += 1
                if data[i][c] >= house_height:
                    break

            scenic_score = d_left * d_down * d_right * d_up
            if scenic_score > max_scenic_score:
                max_scenic_score = scenic_score

    logger.info(f"Part2: {max_scenic_score}")


if __name__ == "__main__":
    main()
