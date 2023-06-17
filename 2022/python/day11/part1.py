"""
Solving: https://adventofcode.com/2022/day/11
"""

import operator
import re
import time
import math
from functools import wraps
from pathlib import Path
from typing import Callable

from loguru import logger

logger.add("log.log")


def time_this(func):
    @wraps(func)
    def timer_wrapper(*args, **kwargs):
        t_start = time.perf_counter()
        result = func(*args, **kwargs)
        t_finish = time.perf_counter()
        logger.info(f"Execution time: {t_finish - t_start:.4f} seconds.")
        return result

    return timer_wrapper


AOC_DAY = Path(__file__).parent.name
INPUT_DIR = Path(__file__).parents[2] / "input"
INPUT_FILE = INPUT_DIR / AOC_DAY / "input.txt"
assert INPUT_FILE.exists(), "Input file not present."


class Monkey:
    def __init__(
        self,
    ):
        self.items: list[int] = []
        self.update_worry_level: Callable | None = None
        self.test_condition = 0
        self.true_target = 0
        self.false_target = 0
        self.inspect_counter = 0

    def set_update_method(self, method: str, operand: str):
        if method == "*":
            if operand == "old":
                self.update_worry_level = lambda x: x * x
            else:
                self.update_worry_level = lambda x: x * int(operand)
        else:
            if operand == "old":
                self.update_worry_level = lambda x: x + x
            else:
                self.update_worry_level = lambda x: x + int(operand)

    def throw_items(self):
        for i in range(len(self.items)):
            if self.items[i] % self.test_condition:
                monkeys[self.false_target].items.append(self.items[i])
            else:
                monkeys[self.true_target].items.append(self.items[i])
        self.items = []

    def do_opeartion(self):
        if self.update_worry_level is None:
            return
        self.items = list(map(self.update_worry_level, self.items))
        self.items = [math.floor(item / 3) for item in self.items]
        self.inspect_counter += len(self.items)
        self.throw_items()

    def __repr__(self) -> str:
        return f"""class Monkey:
        {self.items=}
        {self.update_worry_level=}
        {self.test_condition=}
        {self.true_target=}
        {self.false_target=}"""


monkeys: list[Monkey] = []


@logger.catch
@time_this
def main() -> None:
    data = INPUT_FILE.read_text().splitlines()

#     data = r"""Monkey 0:
#   Starting items: 79, 98
#   Operation: new = old * 19
#   Test: divisible by 23
#     If true: throw to monkey 2
#     If false: throw to monkey 3

# Monkey 1:
#   Starting items: 54, 65, 75, 74
#   Operation: new = old + 6
#   Test: divisible by 19
#     If true: throw to monkey 2
#     If false: throw to monkey 0

# Monkey 2:
#   Starting items: 79, 60, 97
#   Operation: new = old * old
#   Test: divisible by 13
#     If true: throw to monkey 1
#     If false: throw to monkey 3

# Monkey 3:
#   Starting items: 74
#   Operation: new = old + 3
#   Test: divisible by 17
#     If true: throw to monkey 0
#     If false: throw to monkey 1""".splitlines()

    current_monkey: Monkey | None = None

    s_new_monkey = "Monkey"
    s_starting_items = "  Starting items:"
    s_operation = "  Operation: new = old"
    s_test = "  Test: divisible"
    s_true_target = "    If true:"
    s_false_target = "    If false:"

    regex_number = re.compile(r"(\d+)")

    for line in data:
        if line == "":
            assert current_monkey is not None
            monkeys.append(current_monkey)
            continue
        if line.startswith(s_new_monkey):
            current_monkey = Monkey()
            continue
        if line.startswith(s_starting_items):
            assert current_monkey is not None
            current_monkey.items = list(
                map(int, regex_number.findall(line.replace(s_starting_items, "")))
            )
            continue
        if line.startswith(s_operation):
            assert current_monkey is not None
            current_monkey.set_update_method(*line.replace(s_operation, "").split())
            continue
        if line.startswith(s_test):
            assert current_monkey is not None
            current_monkey.test_condition = int(regex_number.findall(line)[0])
            continue
        if line.startswith(s_true_target):
            assert current_monkey is not None
            current_monkey.true_target = int(regex_number.findall(line)[0])
            continue
        if line.startswith(s_false_target):
            assert current_monkey is not None
            current_monkey.false_target = int(regex_number.findall(line)[0])

    assert current_monkey is not None
    monkeys.append(current_monkey)

    for _ in range(20):
        for monkey in monkeys:
            monkey.do_opeartion()

    inspect_counts = [monkey.inspect_counter for monkey in monkeys]
    inspect_counts.sort()

    monkey_business = inspect_counts[-1] * inspect_counts[-2]

    logger.info(f"Part1: {monkey_business}")


if __name__ == "__main__":
    main()
