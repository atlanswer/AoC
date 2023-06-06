"""
Solving: https://adventofcode.com/2022/day/6
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
    data = INPUT_FILE.read_text()

    # data = r"""mjqjpqmgbljsphdztnvjfqwrcgsmlb"""
    # data = r"""bvwbjplbgvbhsrlpgdmjqwftvncz"""
    # data = r"""nppdvjthqldpwncqszvftbrmjlhg"""
    # data = r"""nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg"""
    # data = r"""zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw"""

    cursor = 0

    start_marker = {data[cursor]: 1}

    for i in range(3):
        cursor += 1
        if data[cursor] in start_marker:
            start_marker[data[cursor]] += 1
        else:
            start_marker[data[cursor]] = 1

    while len(start_marker) != 4:
        cursor += 1
        key2pop = data[cursor - 4]
        if start_marker[key2pop] == 1:
            del start_marker[key2pop]
        else:
            start_marker[key2pop] -= 1
        if data[cursor] in start_marker:
            start_marker[data[cursor]] += 1
        else:
            start_marker[data[cursor]] = 1

    logger.info(f"Part1: {cursor + 1}")


if __name__ == "__main__":
    t_start = time.perf_counter()
    main()
    t_finish = time.perf_counter()
    logger.info(f"Execution time: {t_finish - t_start:.4f} seconds.")
