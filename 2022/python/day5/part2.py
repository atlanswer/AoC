"""
Solving: https://adventofcode.com/2022/day/1#part2
"""

from itertools import takewhile
import re
import time
from pathlib import Path

from loguru import logger

logger.add("log.log")

AOC_DAY = Path(__file__).parent.name
INPUT_DIR = Path(__file__).parents[2] / "input"
INPUT_FILE = INPUT_DIR / AOC_DAY / "input.txt"
assert INPUT_FILE.exists(), "Input file not present."


@logger.catch
def main() -> None:
    data = INPUT_FILE.read_text()

#     data = """    [D]    
# [N] [C]    
# [Z] [M] [P]
#  1   2   3 

# move 1 from 2 to 1
# move 3 from 1 to 3
# move 2 from 2 to 1
# move 1 from 1 to 2"""

    [stacks, steps] = data.split("\n\n")

    # Stacks

    stacks = stacks.splitlines()

    stack_marker = stacks.pop()
    num_stacks = len(stack_marker) // 4 + 1

    stacks.reverse()

    stacks = [[s[i * 4 + 1] for s in stacks] for i in range(num_stacks)]
    stacks = [[i for i in takewhile(lambda x: x != " ", s)] for s in stacks]

    # Steps

    steps = steps.splitlines()

    re_step = re.compile(r"move (\d+) from (\d+) to (\d+)")

    def parse_step(s: str):
        match = re_step.match(s)
        if match:
            return list(map(lambda x: int(x), match.groups()))
        else:
            raise TypeError("No matching expression.")

    steps = list(map(parse_step, steps))

    for step in steps:
        stacks[step[2] - 1].extend(stacks[step[1] - 1][-step[0] :])
        stacks[step[1] - 1] = stacks[step[1] - 1][: -step[0]]

    tops = "".join([i.pop() for i in stacks])

    logger.info(f"Part1: {tops}")


if __name__ == "__main__":
    t_start = time.perf_counter()
    main()
    t_finish = time.perf_counter()
    logger.info(f"Execution time: {t_finish - t_start:.4f} seconds.")
