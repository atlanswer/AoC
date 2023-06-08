"""
Solving: https://adventofcode.com/2022/day/8
"""

import time
from pathlib import Path

from loguru import logger

logger.add("log.log")

AOC_DAY = Path(__file__).parent.name
INPUT_DIR = Path(__file__).parents[2] / "input"
INPUT_FILE = INPUT_DIR / AOC_DAY / "input.txt"
assert INPUT_FILE.exists(), "Input file not present."


@logger.catch
def main() -> None:
    data = INPUT_FILE.read_text().splitlines()

#     data = r"""30373
# 25512
# 65332
# 33549
# 35390""".splitlines()

    data = [[int(c) for c in r] for r in data]

    mask = [[0] * len(r) for r in data]

    for col in range(1, len(data[0]) - 1):
        current_highest = data[0][col]
        for row in range(1, len(data) - 1):
            if data[row][col] > current_highest:
                current_highest = data[row][col]
                if mask[row][col] == 0:
                    mask[row][col] = 1

    for row in range(1, len(data) - 1):
        current_highest = data[row][0]
        for col in range(1, len(data[0]) - 1):
            if data[row][col] > current_highest:
                current_highest = data[row][col]
                if mask[row][col] == 0:
                    mask[row][col] = 1

    for col in range(1, len(data[0]) - 1):
        current_highest = data[len(data) - 1][col]
        for row in range(len(data) - 2, 0, -1):
            if data[row][col] > current_highest:
                current_highest = data[row][col]
                if mask[row][col] == 0:
                    mask[row][col] = 1

    for row in range(1, len(data) - 1):
        current_highest = data[row][len(data[0]) - 1]
        for col in range(len(data[0]) - 2, 0, -1):
            if data[row][col] > current_highest:
                current_highest = data[row][col]
                if mask[row][col] == 0:
                    mask[row][col] = 1

    num_visible_trees = sum(map(sum, mask)) + len(data) * 2 + len(data[0]) * 2 - 4

    logger.debug(f"{num_visible_trees=}")


if __name__ == "__main__":
    t_start = time.perf_counter()
    main()
    t_finish = time.perf_counter()
    logger.info(f"Execution time: {t_finish - t_start:.4f} seconds.")
