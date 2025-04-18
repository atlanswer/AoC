"""
Solving: https://adventofcode.com/2024/day/5
"""

import time
import logging
from functools import wraps
from pathlib import Path
from typing import Callable, TypeVar

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

    rules, updates = data.split("\n\n")
    rules, updates = rules.splitlines(), updates.splitlines()
    rules = [rule.split("|") for rule in rules]
    rules = [[int(i) for i in rule] for rule in rules]
    updates = [update.split(",") for update in updates]
    updates = [[int(i) for i in update] for update in updates]

    after_rules: dict[int, set[int]] = {}

    for a, b in rules:
        if a in after_rules:
            after_rules[a].add(b)
        else:
            after_rules[a] = set([b])

    for update in updates:
        before_update: set[int] = set()
        ordered: bool = True

        for i in range(1, len(update)):
            before_update.add(update[i - 1])
            if len(before_update & after_rules.get(update[i], set())) > 0:
                ordered = False
                break

        if not ordered:
            continue

        res += update[(len(update) - 1) // 2]

    return res


def main() -> None:
    data = INPUT_FILE.read_text()

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
