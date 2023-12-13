"""
Solving: https://adventofcode.com/2023/day/7#part2
"""

from enum import IntEnum, auto
import time
from functools import total_ordering, wraps
from pathlib import Path

from loguru import logger
from typing import Any, Callable


def time_this(func: Callable[..., Any]):
    @wraps(func)
    def timer_wrapper(*args: ..., **kwargs: ...):
        t_start = time.perf_counter()
        result = func(*args, **kwargs)
        t_finish = time.perf_counter()
        logger.info(f"Execution time: {t_finish - t_start:.4f} seconds.")
        return result

    return timer_wrapper


AOC_YEAR = 2023
AOC_DAY = Path(__file__).parent.name
INPUT_DIR = Path(__file__).parents[2] / "input"
INPUT_FILE = INPUT_DIR / AOC_DAY / "input.txt"
assert INPUT_FILE.exists(), "Input file not present."

CARDS = {
    c: v
    for c, v in zip(
        ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"],
        range(13, 0, -1),
    )
}


class HandType(IntEnum):
    @staticmethod
    def _generate_next_value_(
        name: str, start: int, count: int, last_values: list[Any]
    ):
        return 7 - count

    Five_of_a_kind = auto()
    Four_of_a_kind = auto()
    Full_house = auto()
    Three_of_a_kind = auto()
    Two_pair = auto()
    One_pair = auto()
    High_card = auto()


@total_ordering
class Hand:
    def __init__(self, cards: str, bid: str) -> None:
        self.cards = list(cards)
        self.bid = int(bid)

        card_map = {c: 0 for c in CARDS.keys()}
        j_count = 0

        for c in self.cards:
            if c == "J":
                j_count += 1
            else:
                card_map[c] += 1

        card_nums = [n for n in card_map.values() if n != 0]
        card_nums.sort(reverse=True)

        if len(card_nums) > 0:
            card_nums[0] += j_count
        else:
            card_nums.append(j_count)

        match card_nums:
            case [5]:
                self.type = HandType.Five_of_a_kind
            case [4, 1]:
                self.type = HandType.Four_of_a_kind
            case [3, 2]:
                self.type = HandType.Full_house
            case [3, 1, 1]:
                self.type = HandType.Three_of_a_kind
            case [2, 2, 1]:
                self.type = HandType.Two_pair
            case [2, 1, 1, 1]:
                self.type = HandType.One_pair
            case [1, 1, 1, 1, 1]:
                self.type = HandType.High_card
            case _:
                raise ValueError

    def __eq__(self, hand2: object) -> bool:
        if not isinstance(hand2, Hand):
            raise NotImplementedError
        return self.cards == hand2.cards

    def __gt__(self, hand2: object) -> bool:
        if not isinstance(hand2, Hand):
            raise NotImplementedError
        if self.type > hand2.type:
            return True
        if self.type < hand2.type:
            return False
        for a, b in zip(self.cards, hand2.cards):
            if CARDS[a] < CARDS[b]:
                return False
            if CARDS[a] > CARDS[b]:
                return True
        return False


def get_hands(data: list[str]) -> list[Hand]:
    hands: list[Hand] = []

    for d in data:
        cards, bid = d.split()
        hands.append(Hand(cards, bid))

    return hands


@time_this
def solve(data: list[str]) -> int:
    hands = get_hands(data)

    sorted_hands = sorted(hands)

    def get_winning(hand: tuple[Hand, int]) -> int:
        return hand[0].bid * hand[1]

    winnings = map(get_winning, zip(sorted_hands, range(1, len(sorted_hands) + 1)))

    return sum(winnings)


@logger.catch
def main() -> None:
    data = INPUT_FILE.read_text().splitlines()

    result = solve(data)

    logger.debug(f"{result=}")


if __name__ == "__main__":
    main()
