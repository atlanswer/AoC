"""
Solving: https://adventofcode.com/2023/day/5
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


def get_seeds(line: str) -> list[int]:
    _, seeds = line.split(":")
    seeds = seeds.split()
    return list(map(int, seeds))


def get_map(data: list[str], i: int) -> tuple[list[tuple[int, int, int]], int]:
    map_list: list[tuple[int, int, int]] = []
    while True:
        if i >= len(data):
            return map_list, i
        if data[i] == "":
            return map_list, i + 1
        map_list.append(tuple(map(int, data[i].split())))  # pyright: ignore[reportGeneralTypeIssues]
        i += 1


def map_src_to_dest(src: int, map_list: list[tuple[int, int, int]]):
    for range_map in map_list:
        dest_range_start = range_map[0]
        src_range_start = range_map[1]
        range_len = range_map[2]

        if src_range_start <= src < src_range_start + range_len:
            return src - src_range_start + dest_range_start

    return src


@time_this
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

    def map_all(src: int) -> int:
        for map_fn in map_fns:
            src = map_fn(src)
        return src

    locations = map(map_all, seeds)

    return min(locations)


@logger.catch
def main() -> None:
    data = INPUT_FILE.read_text().splitlines()

    result = solve(data)

    logger.debug(f"{result=}")


if __name__ == "__main__":
    main()
