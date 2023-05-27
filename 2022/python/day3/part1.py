"""
Solving: https://adventofcode.com/2022/day/3
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


def compartment2binary(compartment: str) -> int:
    return reduce(lambda x, y: x | y, map(lambda c: 1 << get_priority(c), compartment))


def get_shared_item_priority(compartment: Tuple[str, str]):
    count = 0
    compare_result = compartment2binary(compartment[0]) & compartment2binary(
        compartment[1]
    )
    while not compare_result & 1:
        count += 1
        compare_result >>= 1
    return count


def split_str_in_half(s: str):
    l = len(s)
    return (s[slice(l // 2)], s[slice(l // 2, l)])


@logger.catch
def main() -> None:
    data = INPUT_FILE.read_text().splitlines()

    sum_priority = sum(map(get_shared_item_priority, map(split_str_in_half, data)))

    logger.info(f"Part1: {sum_priority}")


if __name__ == "__main__":
    t_start = time.perf_counter()
    main()
    t_finish = time.perf_counter()
    logger.info(f"Execution time: {t_finish - t_start:.4f} seconds.")
