"""
Solving: https://adventofcode.com/2023/day/10#part2
"""

import time
from functools import wraps
from pathlib import Path
from typing import Any, Callable, Literal

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

DIRECTIONS = Literal["north", "south", "west", "east"]


def find_s(tiles: list[list[str]]) -> tuple[int, int]:
    for i in range(len(tiles)):
        for j in range(len(tiles[0])):
            if tiles[i][j] == "S":
                return i, j
    raise ValueError


def find_next(
    tiles: list[list[str]], loc: tuple[int, int], src: DIRECTIONS
) -> tuple[DIRECTIONS, tuple[int, int]] | None:
    i, j = loc
    tile = tiles[i][j]

    match tile, src:
        case "|", "south":
            return "south", (i + 1, j)
        case "|", "north":
            return "north", (i - 1, j)
        case "-", "east":
            return "east", (i, j + 1)
        case "-", "west":
            return "west", (i, j - 1)
        case "L", "south":
            return "east", (i, j + 1)
        case "L", "west":
            return "north", (i - 1, j)
        case "J", "south":
            return "west", (i, j - 1)
        case "7", "east":
            return "south", (i + 1, j)
        case "7", "north":
            return "west", (i, j - 1)
        case "J", "east":
            return "north", (i - 1, j)
        case "F", "north":
            return "east", (i, j + 1)
        case "F", "west":
            return "south", (i + 1, j)
        case _:
            return None


def get_loop(
    tiles: list[list[str]], fog: list[list[bool]], start: tuple[int, int]
) -> None:
    i, j = start

    surroundings = [(i - 1, j), (i, j + 1), (i + 1, j), (i, j - 1)]
    directions: list[DIRECTIONS] = ["north", "east", "south", "west"]
    cur_direction_loc = None

    for direction, loc in zip(directions, surroundings):
        ii, jj = loc
        if ii < 0 or ii >= len(tiles) or jj < 0 or jj >= len(tiles[0]):
            continue
        cur_direction_loc = find_next(tiles, loc, direction)
        if cur_direction_loc is not None:
            break

    assert cur_direction_loc is not None
    cur_direction, cur_loc = cur_direction_loc

    while cur_loc != start:
        cur_direction_loc = find_next(tiles, cur_loc, cur_direction)
        assert cur_direction_loc is not None
        cur_direction, cur_loc = cur_direction_loc


@time_this
def solve(data: list[str]) -> int:
    tiles = list(map(list, data))
    fog = [[False] * len(tiles[0])] * len(tiles)

    start = find_s(tiles)

    step = get_loop(data, fog, start)


@logger.catch
def main() -> None:
    data = INPUT_FILE.read_text().splitlines()

    result = solve(data)

    logger.debug(f"{result=}")


if __name__ == "__main__":
    main()
