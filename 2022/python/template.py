"""
Solving: https://adventofcode.com/2022/day/1
"""

from pathlib import Path
import logging
import time

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


def main() -> None:
    with open(INPUT_FILE) as f:
        data = f.read().splitlines()

    logger.debug(data)


if __name__ == "__main__":
    t_start = time.perf_counter()
    main()
    t_finish = time.perf_counter()
    logger.info("Execution time: %0.4f seconds.", t_finish - t_start)
