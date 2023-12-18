"""
Solving: https://adventofcode.com/2023/day/10#part2
"""

import time
from collections import deque
from functools import wraps
from pathlib import Path
from typing import Callable, Literal, TypeVar

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

DIRECTIONS = Literal["north", "south", "west", "east"]
ARROWS = ["⬆️", "↗️", "➡️", "↘️", "⬇️", "↙️", "⬅️", "↖️"]
regions: list[
    tuple[int, Literal["left", "right", "unknown"], Literal["in", "out", "unknown"]]
] = []
lr_to_io: dict[Literal["left", "right"], Literal["in", "out"]] = {}


def find_start(tiles: list[list[str]]) -> tuple[int, int]:
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
            tiles[i][j] = "⬇️"
            return "south", (i + 1, j)
        case "|", "north":
            tiles[i][j] = "⬆️"
            return "north", (i - 1, j)
        case "-", "east":
            tiles[i][j] = "➡️"
            return "east", (i, j + 1)
        case "-", "west":
            tiles[i][j] = "⬅️"
            return "west", (i, j - 1)
        case "L", "south":
            tiles[i][j] = "↘️"
            return "east", (i, j + 1)
        case "L", "west":
            tiles[i][j] = "↖️"
            return "north", (i - 1, j)
        case "J", "south":
            tiles[i][j] = "↙️"
            return "west", (i, j - 1)
        case "J", "east":
            tiles[i][j] = "↗️"
            return "north", (i - 1, j)
        case "7", "east":
            tiles[i][j] = "↘️"
            return "south", (i + 1, j)
        case "7", "north":
            tiles[i][j] = "↖️"
            return "west", (i, j - 1)
        case "F", "north":
            tiles[i][j] = "↗️"
            return "east", (i, j + 1)
        case "F", "west":
            tiles[i][j] = "↙️"
            return "south", (i + 1, j)
        case _:
            return None


def is_out(tiles: list[list[str]], i: int, j: int) -> bool:
    return i < 0 or i >= len(tiles) or j < 0 or j >= len(tiles[0])


def get_loop(tiles: list[list[str]], start: tuple[int, int]) -> None:
    i, j = start

    surroundings = [(i - 1, j), (i, j + 1), (i + 1, j), (i, j - 1)]
    directions: list[DIRECTIONS] = ["north", "east", "south", "west"]
    cur_direction_loc = None

    for direction, loc in zip(directions, surroundings):
        ii, jj = loc
        if is_out(tiles, ii, jj):
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


def is_found(tiles: list[list[str]], i: int, j: int) -> bool:
    global regions
    tile = tiles[i][j]
    return (
        tile == "S"
        or tile in ARROWS
        or tile in [str(region_type) for region_type, _, _ in regions]
    )


def count_enclosed(tiles: list[list[str]]) -> int:
    global regions, lr_to_io
    for i in range(len(tiles)):
        for j in range(len(tiles[0])):
            if is_found(tiles, i, j):
                continue
            label = 1 if len(regions) == 0 else regions[-1][0] + 1
            if label == 7:
                label += 1
            regions.append((label, "unknown", "unknown"))
            tile_deque: deque[tuple[int, int]] = deque()
            tile_deque.append((i, j))
            while len(tile_deque) > 0:
                ii, jj = tile_deque.popleft()
                if is_found(tiles, ii, jj):
                    continue
                tiles[ii][jj] = str(label)
                surroundings = [
                    (ii - 1, jj, "north"),
                    (ii, jj + 1, "east"),
                    (ii + 1, jj, "south"),
                    (ii, jj - 1, "west"),
                ]
                for ii, jj, direction in surroundings:
                    if is_out(tiles, ii, jj):
                        label, region_lr, region_io = regions[-1]
                        regions[-1] = (label, region_lr, "out")
                        continue
                    if tiles[ii][jj] in ARROWS:
                        label, region_lr, region_io = regions[-1]
                        arrow = tiles[ii][jj]
                        match direction, arrow:
                            case "north", "➡️" | "↘️" | "↗️":
                                regions[-1] = (label, "right", region_io)
                            case "north", "⬅️" | "↙️" | "↖️":
                                regions[-1] = (label, "left", region_io)
                            case "east", "⬇️" | "↙️" | "↘️":
                                regions[-1] = (label, "right", region_io)
                            case "east", "⬆️" | "↗️" | "↖️":
                                regions[-1] = (label, "left", region_io)
                            case "south", "⬅️" | "↖️" | "↙️":
                                regions[-1] = (label, "right", region_io)
                            case "south", "➡️" | "↗️" | "↘️":
                                regions[-1] = (label, "left", region_io)
                            case "west", "⬆️" | "↖️" | "↗️":
                                regions[-1] = (label, "right", region_io)
                            case "west", "⬇️" | "↙️" | "↘️":
                                regions[-1] = (label, "left", region_io)
                            case _:
                                raise ValueError("Unknown boundary.")
                        continue
                    if not is_found(tiles, ii, jj):
                        tile_deque.append((ii, jj))

    find_lr = None
    for _, region_lr, region_io in regions:
        if region_io == "out":
            find_lr = "left" if region_lr == "right" else "right"
            break
    assert find_lr in ["left", "right"]

    region_list = [
        str(region_type)
        for region_type, region_lr, _ in regions
        if region_lr == find_lr
    ]

    counter = 0
    for i in range(len(tiles)):
        for j in range(len(tiles[0])):
            if tiles[i][j] in region_list:
                counter += 1

    return counter


@time_this
def solve(data: list[str]) -> int:
    tiles = list(map(list, data))

    start = find_start(tiles)

    get_loop(tiles, start)

    result = count_enclosed(tiles)

    return result


@logger.catch
def main() -> None:
    data = INPUT_FILE.read_text().splitlines()

    result = solve(data)

    logger.debug(f"{result=}")


if __name__ == "__main__":
    main()
