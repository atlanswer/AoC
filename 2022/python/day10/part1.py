"""
Solving: https://adventofcode.com/2022/day/10
"""

import time
from functools import wraps
from pathlib import Path

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


@logger.catch
@time_this
def main() -> None:
    data = INPUT_FILE.read_text().splitlines()

    #     data = r"""addx 15
    # addx -11
    # addx 6
    # addx -3
    # addx 5
    # addx -1
    # addx -8
    # addx 13
    # addx 4
    # noop
    # addx -1
    # addx 5
    # addx -1
    # addx 5
    # addx -1
    # addx 5
    # addx -1
    # addx 5
    # addx -1
    # addx -35
    # addx 1
    # addx 24
    # addx -19
    # addx 1
    # addx 16
    # addx -11
    # noop
    # noop
    # addx 21
    # addx -15
    # noop
    # noop
    # addx -3
    # addx 9
    # addx 1
    # addx -3
    # addx 8
    # addx 1
    # addx 5
    # noop
    # noop
    # noop
    # noop
    # noop
    # addx -36
    # noop
    # addx 1
    # addx 7
    # noop
    # noop
    # noop
    # addx 2
    # addx 6
    # noop
    # noop
    # noop
    # noop
    # noop
    # addx 1
    # noop
    # noop
    # addx 7
    # addx 1
    # noop
    # addx -13
    # addx 13
    # addx 7
    # noop
    # addx 1
    # addx -33
    # noop
    # noop
    # noop
    # addx 2
    # noop
    # noop
    # noop
    # addx 8
    # noop
    # addx -1
    # addx 2
    # addx 1
    # noop
    # addx 17
    # addx -9
    # addx 1
    # addx 1
    # addx -3
    # addx 11
    # noop
    # noop
    # addx 1
    # noop
    # addx 1
    # noop
    # noop
    # addx -13
    # addx -19
    # addx 1
    # addx 3
    # addx 26
    # addx -30
    # addx 12
    # addx -1
    # addx 3
    # addx 1
    # noop
    # noop
    # noop
    # addx -9
    # addx 18
    # addx 1
    # addx 2
    # noop
    # noop
    # addx 9
    # noop
    # noop
    # noop
    # addx -1
    # addx 2
    # addx -37
    # addx 1
    # addx 3
    # noop
    # addx 15
    # addx -21
    # addx 22
    # addx -6
    # addx 1
    # noop
    # addx 2
    # addx 1
    # noop
    # addx -10
    # noop
    # noop
    # addx 20
    # addx 1
    # addx 2
    # addx 2
    # addx -6
    # addx -11
    # noop
    # noop
    # noop""".splitlines()

    reg_x = 1
    cycle_count = 0
    observe_cycle = [20, 60, 100, 140, 180, 220]
    target_cycles = enumerate(observe_cycle)
    _, target_cycle = next(target_cycles)
    signal_strength = 0
    addend = 0

    for inst in data:
        reg_x += addend
        match inst.split():
            case ["noop"]:
                cycle_count += 1
                addend = 0
            case ["addx", inst2]:
                cycle_count += 2
                addend = int(inst2)

        if cycle_count >= target_cycle:
            signal_strength += target_cycle * reg_x
            try:
                _, target_cycle = next(target_cycles)
            except StopIteration:
                break

    logger.info(f"Part1: {signal_strength}")


if __name__ == "__main__":
    main()
