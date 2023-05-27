"""
Solving: https://adventofcode.com/2022/day/2#part2
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
    Rock = (1, 3, 2)
    Paper = (2, 1, 3)
    Scissor = (3, 2, 1)

    def __init__(self, score: int, defeats: int, defeated_by: int):
        self.score = score
        self.defeats = defeats
        self.defeated_by = defeated_by


opponent_choices = {"A": HandShape.Rock, "B": HandShape.Paper, "C": HandShape.Scissor}


def strategy_outcome(opponent: str, myself: str):
    opponent_play = opponent_choices[opponent]
    match myself:
        # To lose
        case "X":
            return opponent_play.defeats + 0
        # To end in a draw
        case "Y":
            return opponent_play.score + 3
        # To win
        case "Z":
            return opponent_play.defeated_by + 6
        case _:
            raise ValueError("Shouldn't happens.")


def main() -> None:
    with open(INPUT_FILE) as f:
        data = f.read().splitlines()

    score = 0

    for line in data:
        [opponent, myself] = line.split()
        score += strategy_outcome(opponent, myself)

    logger.info(f"Part2: {score}")


if __name__ == "__main__":
    t_start = time.perf_counter()
    main()
    t_finish = time.perf_counter()
    logger.info(f"Execution time: {t_finish - t_start:.4f} seconds.")
