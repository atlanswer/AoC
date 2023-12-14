"""
Solving: https://adventofcode.com/2023/day/8
"""

import time
from functools import wraps
from pathlib import Path

from loguru import logger
from typing import Any, Callable


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

Route = dict[str, dict[str, str]]


def get_instructions(data: list[str]) -> str:
    return data[0]


def get_nodes(data: list[str]) -> Route:
    def get_node(line: str) -> tuple[str, dict[str, str]]:
        node_name, next_nodes = line.split(" = ")
        assert next_nodes[0] == "(" and next_nodes[-1] == ")"
        next_left, next_right = next_nodes[1:-1].split(", ")

        return node_name, {"L": next_left, "R": next_right}

    return {node_name: next_node for node_name, next_node in map(get_node, data[2:])}


def count_steps(instructions: str, nodes: Route) -> int:
    step = 0
    current_node = "AAA"

    while current_node != "ZZZ":
        next_instruction = instructions[step % len(instructions)]
        current_node = nodes[current_node][next_instruction]
        step += 1

    return step


@time_this
def solve(data: list[str]) -> int:
    instructions = get_instructions(data)
    nodes = get_nodes(data)
    step = count_steps(instructions, nodes)

    return step


@logger.catch
def main() -> None:
    data = INPUT_FILE.read_text().splitlines()

    result = solve(data)

    logger.debug(f"{result=}")


if __name__ == "__main__":
    main()
