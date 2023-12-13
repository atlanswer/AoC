"""
Solving: https://adventofcode.com/2023/day/5#part2
"""

import time
from functools import partial, wraps
from pathlib import Path
from typing import Any, Callable

from loguru import logger


def time_this(func: Callable[..., Any]):
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


def get_seeds(line: str) -> list[tuple[int, int]]:
    _, seed_ranges = line.split(":")
    seed_ranges = list(map(int, seed_ranges.split()))

    assert len(seed_ranges) % 2 == 0

    seeds: list[tuple[int, int]] = []
    i = 0

    while i < len(seed_ranges):
        seeds.append((seed_ranges[i], seed_ranges[i] + seed_ranges[i + 1]))
        i += 2

    return seeds


def get_map(data: list[str], i: int) -> tuple[list[tuple[int, int, int]], int]:
    map_list: list[tuple[int, int, int]] = []
    while True:
        if i >= len(data):
            return map_list, i
        if data[i] == "":
            return map_list, i + 1
        map_list.append(tuple(map(int, data[i].split())))  # pyright: ignore[reportGeneralTypeIssues]
        i += 1


def map_src_to_dest(
    src: list[tuple[int, int]], map_list: list[tuple[int, int, int]]
) -> list[tuple[int, int]]:
    dest: list[tuple[int, int]] = []

    while len(src) > 0:
        start, end = src.pop()

        for dest_start, src_start, range_len in map_list:
            src_end = src_start + range_len
            offset = dest_start - src_start

            if src_start >= end or src_end <= start:
                continue
            if src_start > start:
                src.append((start, src_start))
                start = src_start
            if src_end < end:
                src.append((src_end, end))
                end = src_end

            dest.append((start + offset, end + offset))
            break
        else:
            dest.append((start, end))

    return dest


def solve(data: list[str]) -> int:
    seeds = get_seeds(data[0])
    map_lists: list[list[tuple[int, int, int]]] = []

    i = 1

    while i < len(data):
        if data[i] == "":
            i += 1
            continue
        if data[i].endswith("map:"):
            i += 1
            map_list, i = get_map(data, i)
            map_lists.append(map_list)

    map_fns = list(
        map(lambda map_list: partial(map_src_to_dest, map_list=map_list), map_lists)
    )

    def map_all(src: list[tuple[int, int]]) -> list[tuple[int, int]]:
        dest = src
        for map_fn in map_fns:
            dest = map_fn(dest)
            logger.debug(f"{dest=}")
        return dest

    locations = map_all(seeds)

    return min([item[0] for item in locations])


@logger.catch
def main() -> None:
    data = INPUT_FILE.read_text().splitlines()

    result = solve(data)

    logger.debug(f"{result=}")


if __name__ == "__main__":
    main()
