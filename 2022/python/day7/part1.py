"""
Solving: https://adventofcode.com/2022/day/7
"""

from __future__ import annotations

import time
from pathlib import Path

from loguru import logger

logger.add("log.log")

AOC_DAY = Path(__file__).parent.name
INPUT_DIR = Path(__file__).parents[2] / "input"
INPUT_FILE = INPUT_DIR / AOC_DAY / "input.txt"
assert INPUT_FILE.exists(), "Input file not present."


class Directory:
    def __init__(self, dir_name: str, parent: Directory | None = None):
        self.name = dir_name
        self.parent: Directory | None = parent
        self.total_file_size = 0
        self.children: list[Directory] = []


@logger.catch
def main() -> None:
    data = INPUT_FILE.read_text().splitlines()

    #     data = r"""$ cd /
    # $ ls
    # dir a
    # 14848514 b.txt
    # 8504156 c.dat
    # dir d
    # $ cd a
    # $ ls
    # dir e
    # 29116 f
    # 2557 g
    # 62596 h.lst
    # $ cd e
    # $ ls
    # 584 i
    # $ cd ..
    # $ cd ..
    # $ cd d
    # $ ls
    # 4060174 j
    # 8033020 d.log
    # 5626152 d.ext
    # 7214296 k""".splitlines()

    root = Directory("/")
    cwd: Directory = root
    candidates: list[Directory] = []

    for output in data:
        match output.split():
            case ["$", *commands]:
                match commands:
                    case ["cd", dir_name]:
                        match dir_name:
                            case "/":
                                cwd = root
                            case "..":
                                match cwd.parent:
                                    case None:
                                        raise KeyError("No further than root.")
                                    case _:
                                        if cwd.total_file_size <= 100000:
                                            candidates.append(cwd)
                                        cwd.parent.total_file_size += (
                                            cwd.total_file_size
                                        )
                                        cwd = cwd.parent
                            case _:
                                cwd = next(
                                    filter(lambda x: x.name == dir_name, cwd.children)
                                )
                    case ["ls"]:
                        ...
            case ["dir", dir_name]:
                if cwd is None:
                    continue
                cwd.children.append(Directory(dir_name, cwd))
            case [file_size, file_name] if file_size.isdigit():
                if cwd is None:
                    continue
                cwd.total_file_size += int(file_size)

    while cwd is not root:
        if cwd.total_file_size <= 100000:
            candidates.append(cwd)
        if cwd.parent is None:
            break
        cwd.parent.total_file_size += cwd.total_file_size
        cwd = cwd.parent

    sum_size = sum(map(lambda x: x.total_file_size, candidates))

    logger.info(f"Part1: {sum_size}")


if __name__ == "__main__":
    t_start = time.perf_counter()
    main()
    t_finish = time.perf_counter()
    logger.info(f"Execution time: {t_finish - t_start:.4f} seconds.")
