"""
Solving: https://adventofcode.com/2022/day/2
"""

from __future__ import annotations
from enum import Enum
from pathlib import Path
import logging
import time
from typing import cast

logging.basicConfig(
    format="%(asctime)s.%(msecs)03d:%(levelname)s:%(name)s:\t%(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

AOC_DAY = Path(__file__).parent.name
INPUT_DIR = Path(__file__).parents[2] / "input"
INPUT_FILE = INPUT_DIR / AOC_DAY / "input.txt"
assert INPUT_FILE.exists(), "Input file not present."


class HandShape(Enum):
    Rock, Paper, Scissor = range(1, 4)

    def __sub__(self, other: HandShape) -> int:
        if self is other:
            return 3
        if (
            self is HandShape.Rock
            and other is HandShape.Scissor
            or self is HandShape.Paper
            and other is HandShape.Rock
            or self is HandShape.Scissor
            and other is HandShape.Paper
        ):
            return 6
        return 0


opponent_play = {"A": HandShape.Rock, "B": HandShape.Paper, "C": HandShape.Scissor}

my_play = {"X": HandShape.Rock, "Y": HandShape.Paper, "Z": HandShape.Scissor}


def main() -> None:
    with open(INPUT_FILE) as f:
        data = f.read().splitlines()

    score = 0

    for line in data:
        [opponent, myself] = line.split()
        score += my_play[myself] - opponent_play[opponent]
        score += cast(HandShape, my_play[myself]).value

    logger.info(f"Part1: {score}")


if __name__ == "__main__":
    t_start = time.perf_counter()
    main()
    t_finish = time.perf_counter()
    logger.info(f"Execution time: {t_finish - t_start:.4f} seconds.")
