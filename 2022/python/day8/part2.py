"""
Solving: https://adventofcode.com/2022/day/8#part2
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

    data = r"""30373
25512
65332
33549
35390""".splitlines()

    data = [[int(c) for c in r] for r in data]

    for r in range(len(data)):
        for c in range(len(data[0])):
            ...


if __name__ == "__main__":
    t_start = time.perf_counter()
    main()
    t_finish = time.perf_counter()
    logger.info(f"Execution time: {t_finish - t_start:.4f} seconds.")
