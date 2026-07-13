import argparse
import os
from typing import List

from utils.timer import timer

"""
Preprocessing:
- Read the input file and parse it into a list of strings

Part 1:
- The key insight is that every string is only ever built out of 2-letter chunks: 'ba', 'na', and 'ne'.
  That means we don't actually need to check for those patterns at all - we can just take the string's
  length and divide by 2 to get the number of chunks, which is the string's score.
- We do this for every string in the list and sum the scores to get the total.

    Example:
        "banana" has length 6, so its score is 6 // 2 = 3 (it's really just "ba" + "na" + "na").

Part 2:
- Same process as part 1, but we only add a string's score to the total if that score itself is even.

Part 3:
- Same process as parts 1 and 2, but we also skip any string that contains the letter 'e' - it doesn't
  contribute to the total at all.
"""


def parse_args() -> bool:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--test", action="store_true", help="use input_sample.txt instead of input.txt"
    )
    return parser.parse_args().test


TEST_DATA = parse_args()


@timer
def part1():
    bananas = parse_file()
    score = 0
    for banana in bananas:
        score += len(banana)//2

    print(f"Total score: {score}")


@timer
def part2():
    bananas = parse_file()
    score = 0
    for banana in bananas:
        if len(banana)//2 % 2 == 0:
            score += len(banana)//2

    print(f"Total score: {score}")


@timer
def part3():
    bananas = parse_file()
    score = 0
    for banana in bananas:
        for letter in banana:
            if letter in "e":
                break
        else:
            score += len(banana)//2

    print(f"Total score: {score}")


def parse_file() -> List[str]:
    file_name = "input_sample.txt" if TEST_DATA else "input.txt"
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    with open(abs_file_path, "r") as f:
        bananas = [line.strip() for line in f.readlines()]
    return bananas


part1()
part2()
part3()
