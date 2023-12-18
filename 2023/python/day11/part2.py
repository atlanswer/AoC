"""
Solving: https://adventofcode.com/2023/day/11#part2
"""

import time
from functools import wraps
from pathlib import Path
from typing import Callable, TypeVar

from loguru import logger

ReturnType = TypeVar("ReturnType")


def time_this(func: Callable[..., ReturnType]) -> Callable[..., ReturnType]:
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

EXPANSION = 999_999


def get_path_len(pair: tuple[tuple[int, int], tuple[int, int]]) -> int:
    x1, y1 = pair[0]
    x2, y2 = pair[1]
    dx = x1 - x2 if x1 >= x2 else x2 - x1
    dy = y1 - y2 if y1 >= y2 else y2 - y1
    return dx * 2 + (dy - dx) if dy >= dx else dy * 2 + (dx - dy)


def expand(data: list[str], galaxies: list[tuple[int, int]]) -> list[tuple[int, int]]:
    new_galaxies = galaxies.copy()

    for x in range(len(data)):
        is_empty = True
        for i in data[x]:
            if i == "#":
                is_empty = False
                break
        if is_empty:
            for i in range(len(galaxies)):
                if galaxies[i][0] > x:
                    ix, iy = new_galaxies[i]
                    new_galaxies[i] = (ix + EXPANSION, iy)

    for y in range(len(data[0])):
        is_empty = True
        for i in range(len(data)):
            if data[i][y] == "#":
                is_empty = False
                break
        if is_empty:
            for i in range(len(galaxies)):
                if galaxies[i][1] > y:
                    ix, iy = new_galaxies[i]
                    new_galaxies[i] = (ix, iy + EXPANSION)

    return new_galaxies


def get_galaxies(data: list[str]) -> list[tuple[int, int]]:
    galaxies: list[tuple[int, int]] = []

    for i in range(len(data)):
        for j in range(len(data[0])):
            if data[i][j] == "#":
                galaxies.append((i, j))

    return galaxies


def get_galaxy_pairs(
    galaxies: list[tuple[int, int]],
) -> list[tuple[tuple[int, int], tuple[int, int]]]:
    galaxy_pairs: list[tuple[tuple[int, int], tuple[int, int]]] = []

    for i in range(len(galaxies)):
        for j in range(i + 1, len(galaxies)):
            galaxy_pairs.append((galaxies[i], galaxies[j]))

    return galaxy_pairs


@time_this
def solve(data: list[str]) -> int:
    galaxies = get_galaxies(data)

    new_galaxies = expand(data, galaxies)

    galaxy_pairs = get_galaxy_pairs(new_galaxies)

    return sum(map(get_path_len, galaxy_pairs))


@logger.catch
def main() -> None:
    data = INPUT_FILE.read_text().splitlines()

    result = solve(data)

    logger.debug(f"{result=}")


if __name__ == "__main__":
    main()
