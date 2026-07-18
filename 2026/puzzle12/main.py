import argparse
import os
from dataclasses import dataclass
from typing import Dict, List, Set, Tuple

from utils.timer import timer
from utils.utils import tcolors

"""
Preprocessing:
-

Part 1:
-

Part 2:
-

Part 3:
-
"""


def parse_args() -> bool:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--test", action="store_true", help="use input_sample.txt instead of input.txt"
    )
    return parser.parse_args().test


TEST_DATA = parse_args()


@dataclass
class Bingo:
    diag_1: bool
    diag_2: bool
    rows: Dict[int, bool]
    cols: Dict[int, bool]


@dataclass
class Card:
    nums: Tuple[Tuple[int]]
    bingo: Bingo


@timer
def part1():
    nums, cards = parse_file_1()
    min_num_bingos = 5

    nums_called = set()
    bingos = 0
    for num in nums:
        nums_called.add(num)

        for card in cards:
            pos = in_card(card, num)
            if pos != (-1, -1):
                bingos += count_bingos(nums_called, card, pos)
                if bingos >= min_num_bingos:
                    break

        if bingos >= min_num_bingos:
            break

    print(f"Last number called to reach {min_num_bingos} bingos: {num}")


@timer
def part2():
    nums, cards, diags = parse_file_2()
    min_num_bingos = 5

    nums_called = set()
    diags_bingo = [False] * len(diags)
    bingos = 0
    for num in nums:
        found_bingo = False
        nums_called.add(num)

        for i in range(len(diags)):
            if not diags_bingo[i] and diags[i].issubset(nums_called):
                diags_bingo[i] = True
                bingos += 1
                if bingos >= min_num_bingos:
                    break

        for card in cards:
            pos = in_card(card, num)
            if pos != (-1, -1):
                if count_bingos(nums_called, card, pos) and not found_bingo:
                    bingos += 1
                    found_bingo = True
                    if bingos >= min_num_bingos:
                        break

        if bingos >= min_num_bingos:
            break

    print(f"Last number called to reach {min_num_bingos} bingos: {num}")


@timer
def part3():
    # TODO: Implement part 3
    lines = parse_file_1()
    pass


def in_card(card: Card, num: int) -> Tuple[int]:
    size = len(card.nums)
    for i in range(size):
        for j in range(size):
            if card.nums[i][j] == num:
                return (i, j)
    return (-1, -1)


def count_bingos(nums_called: Set, card: Card, pos: Tuple[int]) -> int:
    size = len(card.nums)
    count = 0

    # Diagonal 1
    if pos[0] == pos[1]:
        if not card.bingo.diag_1:
            card.bingo.diag_1 = True
            for i in range(size):
                if card.nums[i][i] not in nums_called:
                    card.bingo.diag_1 = False
                    break
            count += card.bingo.diag_1

    # Diagonal 2
    if pos[0] + pos[1] == size - 1:
        if not card.bingo.diag_2:
            card.bingo.diag_2 = True
            for i in range(size):
                if card.nums[size - i - 1][i] not in nums_called:
                    card.bingo.diag_2 = False
                    break
            count += card.bingo.diag_2

    # Rows
    if not card.bingo.rows[pos[0]]:
        card.bingo.rows[pos[0]] = True
        for i in range(size):
            if card.nums[pos[0]][i] not in nums_called:
                card.bingo.rows[pos[0]] = False
                break
        count += card.bingo.rows[pos[0]]

    # Columns
    if not card.bingo.cols[pos[1]]:
        card.bingo.cols[pos[1]] = True
        for i in range(size):
            if card.nums[i][pos[1]] not in nums_called:
                card.bingo.cols[pos[1]] = False
                break
        count += card.bingo.cols[pos[1]]

    return count


def print_card(card: Card, nums_called: Set[int]):
    size = len(card.nums)

    for i in range(size):
        row = ""
        for j in range(size):
            if card.nums[i][j] in nums_called:
                row += f"{tcolors.GREEN}{card.nums[i][j]:<4}{tcolors.RESET}"
            else:
                row += f"{card.nums[i][j]:<4}"
        print(row)


def parse_file_1() -> Tuple[List[int], List[Card]]:
    file_name = "input_sample.txt" if TEST_DATA else "input.txt"
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    nums: List[int] = []
    cards: List[Card] = []
    with open(abs_file_path, "r") as f:
        for line in f:
            if line == "\n":
                break
            nums.extend(list(map(int, line.strip().split(" "))))

        for line in f:
            card_nums = tuple(map(int, line.strip().split(" ")))
            card_nums = tuple(card_nums[i : i + 5] for i in range(0, 25, 5))
            bingo = Bingo(False, False, dict(), dict())

            bingo.rows = [False] * 5
            bingo.cols = [False] * 5

            cards.append(Card(card_nums, bingo))

    return nums, cards


def parse_file_2() -> Tuple[List[int], List[Card], List[Set[int]]]:
    file_name = "input_sample.txt" if TEST_DATA else "input.txt"
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    nums: List[int] = []
    cards: List[Card] = []
    card_nums_matrix: List[Tuple[int]] = []
    with open(abs_file_path, "r") as f:
        for line in f:
            if line == "\n":
                break
            nums.extend(list(map(int, line.strip().split(" "))))

        for line in f:
            card_nums_matrix.append(tuple(map(int, line.strip().split(" "))))

    # X axis
    for card_nums in card_nums_matrix:
        card_nums = tuple(card_nums[i : i + 5] for i in range(0, 25, 5))

        bingo = Bingo(False, False, dict(), dict())
        bingo.rows = [False] * 5
        bingo.cols = [False] * 5

        cards.append(Card(card_nums, bingo))

    # Y axis
    for level in range(0, len(card_nums_matrix), 5):
        for y in range(0, 25, 5):
            card_nums = []
            for i in range(y, y + 5):
                row = []
                for j in range(5):
                    row.append(card_nums_matrix[j + level][i])
                card_nums.append(tuple(row))

            bingo = Bingo(False, False, dict(), dict())
            bingo.rows = [False] * 5
            bingo.cols = [False] * 5

            cards.append(Card(tuple(card_nums), bingo))

    # Z axis
    for level in range(0, len(card_nums_matrix), 5):
        for z in range(5):
            card_nums = []
            for i in range(z, 25, 5):
                row = []
                for j in range(5):
                    row.append(card_nums_matrix[j + level][i])
                card_nums.append(tuple(row))

            bingo = Bingo(False, False, dict(), dict())
            bingo.rows = [False] * 5
            bingo.cols = [False] * 5

            cards.append(Card(tuple(card_nums), bingo))

    # 3D Diagonals:
    diags = []
    for level in range(0, len(card_nums_matrix), 5):
        diags.append(set(card_nums_matrix[i + level][i * 5 + i] for i in range(5)))
        diags.append(
            set(card_nums_matrix[i + level][24 - 4 * (i + 1)] for i in range(4, -1, -1))
        )
        diags.append(set(card_nums_matrix[i + level][4 * (i + 1)] for i in range(5)))
        diags.append(
            set(card_nums_matrix[i + level][24 - i * 6] for i in range(4, -1, -1))
        )

    return nums, cards, diags


part1()
part2()
part3()
