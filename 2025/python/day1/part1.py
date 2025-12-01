"""
Solving: https://adventofcode.com/2025/day/1
"""

import re
from typing import Literal

from aoc import get_input, log, time_this


@time_this
def main():
#     input = """L68
# L30
# R48
# L5
# R60
# L55
# L1
# L99
# R14
# L82
# """
    input = get_input(__file__)

    dial = 50
    passwd = 0

    for line in input.splitlines():
        match = re.search(r"^([LR])(\d+)$", line)
        assert match is not None

        direction: Literal["L", "R"] = match.group(1)  # ty:ignore[invalid-assignment]
        distance: int = int(match.group(2))

        dial = dial - distance if direction == "L" else dial + distance

        dial %= 100

        if dial == 0:
            passwd += 1

    log.debug(f"{passwd=}")


if __name__ == "__main__":
    main()
