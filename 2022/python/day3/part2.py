"""
Solving: https://adventofcode.com/2022/day/3#part2
"""

import time
from functools import reduce
from pathlib import Path
from typing import Tuple

from loguru import logger

logger.add("log.log")

AOC_DAY = Path(__file__).parent.name
INPUT_DIR = Path(__file__).parents[2] / "input"
INPUT_FILE = INPUT_DIR / AOC_DAY / "input.txt"
assert INPUT_FILE.exists(), "Input file not present."


def get_priority(c: str):
    if c.islower():
        return ord(c) - ord("a") + 1
    else:
        return ord(c) - ord("A") + 27


def rusksack2binary(rucksack: str) -> int:
    return reduce(lambda x, y: x | y, map(lambda c: 1 << get_priority(c), rucksack))


def get_shared_item_priority(group: list[str]):
    count = 0
    compare_result = (
        rusksack2binary(group[0])
        & rusksack2binary(group[1])
        & rusksack2binary(group[2])
    )
    while compare_result:
        count += 1
        compare_result >>= 1
    return count - 1


@logger.catch
def main() -> None:
    data = INPUT_FILE.read_text().splitlines()

    #     data = """vJrwpWtwJgWrhcsFMMfFFhFp
    # jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
    # PmmdzqPrVvPwwTWBwg
    # wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
    # ttgJtRGJQctTZtZT
    # CrZsJsPPZsGzwwsLwLmpwMDw""".splitlines()

    idx = 0
    sum_priority = 0

    while idx < len(data):
        sum_priority += get_shared_item_priority(data[slice(idx, idx + 3)])
        idx += 3

    logger.info(f"Part1: {sum_priority}")


if __name__ == "__main__":
    t_start = time.perf_counter()
    main()
    t_finish = time.perf_counter()
    logger.info(f"Execution time: {t_finish - t_start:.4f} seconds.")
