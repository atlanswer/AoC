"""
Solving: https://adventofcode.com/2024/day/6#part2
"""

import logging
import time
from functools import wraps
from pathlib import Path
from typing import Callable, Literal, TypeVar

from rich.logging import RichHandler

ReturnType = TypeVar("ReturnType")


def time_this(func: Callable[..., ReturnType]) -> Callable[..., ReturnType]:
    @wraps(func)
    def timer_wrapper(*args: ..., **kwargs: ...):  # pyright: ignore[reportAny]
        t_start = time.perf_counter()
        result = func(*args, **kwargs)
        t_finish = time.perf_counter()
        logger.debug(f"Execution time: {t_finish - t_start:.4f} seconds.")
        return result

    return timer_wrapper


@time_this
def solve(data: str) -> int:
    res = 0

    data: list[list[str]] = [list(line) for line in data.splitlines()]

    r_guard, c_guard = 0, 0
    direction: Literal["Up", "Right", "Down", "Left"] = "Up"

    for r in range(len(data)):
        for c in range(len(data[0])):
            if data[r][c] == "^":
                r_guard, c_guard = r, c
                break

    logger.debug(f"Starting point: [{r_guard}, {c_guard}]")

    while 0 <= r_guard < len(data) and 0 <= c_guard < len(data[0]):
        s1 = ["".join(line) for line in data]
        s2 = "\n".join(s1)
        logger.debug(f"{s2}")
        match direction:
            case "Up":
                # logger.debug("Go UP")
                if r_guard - 1 >= 0 and data[r_guard - 1][c_guard] == "#":
                    direction = "Right"
                    continue
                data[r_guard][c_guard] = "^"
                r_guard -= 1
            case "Right":
                # logger.debug("Go RIGHT")
                if c_guard + 1 < len(data[0]) and data[r_guard][c_guard + 1] == "#":
                    direction = "Down"
                    continue
                data[r_guard][c_guard] = ">"
                c_guard += 1
            case "Down":
                # logger.debug("Go DOWN")
                if r_guard + 1 < len(data) and data[r_guard + 1][c_guard] == "#":
                    direction = "Left"
                    continue
                data[r_guard][c_guard] = "v"
                r_guard += 1
            case "Left":
                # logger.debug("Go LEFT")
                if c_guard - 1 >= 0 and data[r_guard][c_guard - 1] == "#":
                    direction = "Up"
                    continue
                data[r_guard][c_guard] = "<"
                c_guard -= 1

        _ = input("Enter to progress")

    return res


def main() -> None:
    # data = INPUT_FILE.read_text()
    data = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""

    result = solve(data)

    logger.info(f"{result=}")


if __name__ == "__main__":
    AOC_DAY = Path(__file__).parent.name
    INPUT_DIR = Path(__file__).parents[2] / "input"
    INPUT_FILE = INPUT_DIR / AOC_DAY / "input.txt"
    assert INPUT_FILE.exists(), "Input file not present."

    logger = logging.getLogger(__name__)
    handler = RichHandler(
        log_time_format="[%m/%d %H:%M:%S]",
        markup=True,
        rich_tracebacks=True,
        tracebacks_show_locals=True,
    )
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    main()
