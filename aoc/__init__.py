"""Python utilities for AoC"""

__version__ = "2025.12.1"

import logging
import time
from pathlib import Path
from typing import Callable, ParamSpec, TypeVar

from rich.logging import RichHandler

# Prettified logger
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
log.addHandler(
    RichHandler(
        log_time_format="[%m/%d %H:%M:%S]",
        markup=True,
        rich_tracebacks=True,
        tracebacks_show_locals=True,
    )
)

P = ParamSpec("P")
R = TypeVar("R")


def time_this(func: Callable[P, R]) -> Callable[P, R]:
    """Prints execution time."""

    def time_wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        t_start = time.perf_counter()
        res = func(*args, **kwargs)
        t_end = time.perf_counter()

        duration = t_end - t_start
        log.debug(f"Execution time: {duration:.3f} s.")

        return res

    return time_wrapper


def get_input(cur_file: str) -> str:
    """Read the input file:
    ```
    input = get_input(__file__)
    ```
    """

    path = Path(cur_file)
    AOC_DAY = path.parent.name
    INPUT_FILE = path.parents[2] / "input" / AOC_DAY / "input.txt"
    assert INPUT_FILE.exists(), f"Input file ({INPUT_FILE}) not found."

    return INPUT_FILE.read_text()
