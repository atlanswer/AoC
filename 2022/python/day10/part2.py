"""
Solving: https://adventofcode.com/2022/day/10#part2
"""

import copy
import io
import time
from functools import wraps
from pathlib import Path
from black.output import out

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
    cursor_row = 0
    cursor_col = 0

    screen_width = 40
    screen_height = 6
    empty_screen = [["."] * screen_width for _ in range(screen_height)]
    screen = copy.deepcopy(empty_screen)
    screen_buffer = io.StringIO()

    def cycle_increment():
        nonlocal screen, screen_buffer, empty_screen, cursor_col, cursor_row
        if cursor_col + 1 >= screen_width:
            cursor_col = 0
            cursor_row = cursor_row + 1
            if cursor_row >= screen_height:
                cursor_row = 0
                for line in screen:
                    print("".join(line), file=screen_buffer)
                screen = copy.deepcopy(empty_screen)
        else:
            cursor_col = cursor_col + 1

    def draw2screen():
        if reg_x - 1 <= cursor_col <= reg_x + 1:
            screen[cursor_row][cursor_col] = "#"

    for inst in data:
        match inst.split():
            case ["noop"]:
                draw2screen()
                cycle_increment()
                cycle_count += 1
            case ["addx", inst2]:
                draw2screen()
                cycle_increment()
                cycle_count += 1
                draw2screen()
                cycle_increment()
                cycle_count += 1
                reg_x += int(inst2)

    for line in screen:
        print("".join(line), file=screen_buffer)
    output = screen_buffer.getvalue()
    screen_buffer.close()

    logger.info(f"Part2:\n{output}")


if __name__ == "__main__":
    main()
