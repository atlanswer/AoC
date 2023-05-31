"""
Solving: https://adventofcode.com/2022/day/1
"""

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

    data = """    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""

    [stacks, steps] = data.split("\n\n")

    stacks = stacks.splitlines()

    stack_marker = stacks.pop()
    num_stacks = len(stack_marker) // 4 + 1

    stacks = [[s[i * 4 + 1] for s in stacks] for i in range(num_stacks)]

    logger.debug(stacks)

    steps = steps.splitlines()

    re_step = re.compile(r"move (\d+) from (\d+) to (\d+)")

    def parse_step(s: str):
        match = re_step.match(s)
        if match:
            return match.groups()
        else:
            raise TypeError("No matching expression.")

    steps = list(map(parse_step, steps))


if __name__ == "__main__":
    t_start = time.perf_counter()
    main()
    t_finish = time.perf_counter()
    logger.info(f"Execution time: {t_finish - t_start:.4f} seconds.")
