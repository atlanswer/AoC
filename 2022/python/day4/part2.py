"""
Solving: https://adventofcode.com/2022/day/4#part2
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

    count = 0

    #     data = """2-4,6-8
    # 2-3,4-5
    # 5-7,7-9
    # 2-8,3-7
    # 6-6,4-6
    # 2-6,4-8""".splitlines()

    for line in data:
        assignment = line.split(",")
        assignment = [s.split("-") for s in assignment]
        assignment = [[int(a), int(b)] for a, b in assignment]

        if assignment[1][0] <= assignment[0][0] <= assignment[1][1]:
            count += 1
            continue
        if assignment[1][0] <= assignment[0][1] <= assignment[1][1]:
            count += 1
            continue
        if assignment[0][0] <= assignment[1][0] <= assignment[0][1]:
            count += 1
            continue
        if assignment[0][0] <= assignment[1][1] <= assignment[0][1]:
            count += 1
            continue

    logger.info(f"Part2: {count}")


if __name__ == "__main__":
    t_start = time.perf_counter()
    main()
    t_finish = time.perf_counter()
    logger.info(f"Execution time: {t_finish - t_start:.4f} seconds.")
