"""
Solving: https://adventofcode.com/2022/day/9#part2
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

    #     data = r"""R 4
    # U 4
    # L 3
    # D 1
    # R 4
    # D 1
    # L 5
    # R 2""".splitlines()

#     data = r"""R 5
# U 8
# L 8
# D 3
# R 17
# D 10
# L 25
# U 20""".splitlines()

    rope: list[tuple[int, int]] = [(0, 0)] * 10
    tail_path: list[tuple[int, int]] = []
    tail_path.append((0, 0))

    def is_touching(head, tail) -> bool:
        if tail == head:
            return True
        if (
            tail[0] - 1 <= head[0] <= tail[0] + 1
            and tail[1] - 1 <= head[1] <= tail[1] + 1
        ):
            return True
        return False

    def updated_location(head: tuple[int, int], tail: tuple[int, int]):
        if is_touching(head, tail):
            return tail
        if tail[0] == head[0]:
            if head[1] > tail[1]:
                tail = (tail[0], tail[1] + 1)
            else:
                tail = (tail[0], tail[1] - 1)
        if tail[1] == head[1]:
            if head[0] > tail[0]:
                tail = (tail[0] + 1, tail[1])
            else:
                tail = (tail[0] - 1, tail[1])
        if head[0] > tail[0] and head[1] > tail[1]:
            tail = (tail[0] + 1, tail[1] + 1)
        if head[0] < tail[0] and head[1] > tail[1]:
            tail = (tail[0] - 1, tail[1] + 1)
        if head[0] > tail[0] and head[1] < tail[1]:
            tail = (tail[0] + 1, tail[1] - 1)
        if head[0] < tail[0] and head[1] < tail[1]:
            tail = (tail[0] - 1, tail[1] - 1)
        return tail

    for motion in data:
        direction, distance = motion.split()
        distance = int(distance)

        for _ in range(distance):
            match direction:
                case "U":
                    rope[0] = (rope[0][0], rope[0][1] + 1)
                case "D":
                    rope[0] = (rope[0][0], rope[0][1] - 1)
                case "L":
                    rope[0] = (rope[0][0] - 1, rope[0][1])
                case "R":
                    rope[0] = (rope[0][0] + 1, rope[0][1])

            for i in range(len(rope) - 1):
                rope[i + 1] = updated_location(rope[i], rope[i + 1])

            if rope[-1] not in tail_path:
                tail_path.append(rope[-1])

    logger.info(f"Part2: {len(tail_path)}")


if __name__ == "__main__":
    main()
