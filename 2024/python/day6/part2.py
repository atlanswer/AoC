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

Direction = Literal["Up", "Right", "Down", "Left"]


def time_this(func: Callable[..., ReturnType]) -> Callable[..., ReturnType]:
    @wraps(func)
    def timer_wrapper(*args: ..., **kwargs: ...):  # pyright: ignore[reportAny]
        t_start = time.perf_counter()
        result = func(*args, **kwargs)
        t_finish = time.perf_counter()
        logger.debug(f"Execution time: {t_finish - t_start:.4f} seconds.")
        return result

    return timer_wrapper


def debug_print(data: list[list[str]], note: str = "Current loop") -> None:
    s1 = ["".join(line) for line in data]
    s2 = "\n".join(s1)
    logger.debug(f"{note}:\n{s2}")


def inbound(data: list[list[str]], r: int, c: int) -> bool:
    return 0 <= r < len(data) and 0 <= c < len(data[0])


def get_next(
    data: list[list[str]], r: int, c: int, d: Direction
) -> tuple[int, int, Direction]:
    match d:
        case "Up":
            r, c = r - 1, c
            if inbound(data, r, c) and data[r][c] == "#":
                d = "Right"
        case "Right":
            r, c = r, c + 1
            if inbound(data, r, c) and data[r][c] == "#":
                d = "Down"
        case "Down":
            r, c = r + 1, c
            if inbound(data, r, c) and data[r][c] == "#":
                d = "Left"
        case "Left":
            r, c = r, c - 1
            if inbound(data, r, c) and data[r][c] == "#":
                d = "Up"

    return r, c, d


def test_loop(data: list[list[str]], r: int, c: int, d: Direction) -> bool:
    rn, cn, dn = get_next(data, r, c, d)

    while True:
        debug_print(data, "Testing loop")

        if not inbound(data, rn, cn):
            break

        if rn == r and cn == c:
            marker = data[r][c]
            if (
                (marker == "^" and dn == "Up")
                or (marker == ">" and dn == "Right")
                or (marker == "v" and dn == "Down")
                or (marker == "<" and dn == "Left")
            ):
                return True

        _ = input("Press to progress")

        rn, cn, dn = get_next(data, rn, cn, dn)

    return False


@time_this
def solve(data_str: str) -> int:
    res = 0

    data: list[list[str]] = [list(line) for line in data_str.splitlines()]

    r, c = 0, 0
    d: Direction = "Up"

    for r in range(len(data)):
        for c in range(len(data[0])):
            if data[r][c] == "^":
                r, c = r, c
                break

    logger.debug(f"Starting point: [{r}, {c}]")

    while inbound(data, r, c):
        debug_print(data)

        rn, cn, dn = get_next(data, r, c, d)

        if inbound(data, rn, cn):
            match d:
                case "Up":
                case "Right":
                case "Down":
                case "Left":

        r, c = rn, cn

        data_test = [[i for i in r] for r in data]

        _ = test_loop(data_test, r, c, d)

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
