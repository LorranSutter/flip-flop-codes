import argparse
import os
from typing import List

from utils.timer import timer

"""
Preprocessing:
- Read the input file, skip the first three lines and the last line that represents
  the flower and the soil respectively. Parse the other lines into a list of strings.

Part 1:
- The key insight is that "cutting at height 400" just means keeping the topmost
  `len(stem) - 400` blocks, since height is measured upward from the ground while the
  stem list is stored top to bottom.
- So we only need to scan that top slice and count every block that isn't a plain "|",
  since anything else is a leaf on one side or the other.
- Just output the total count at the end.

Part 2:
- The key insight is that a swap only depends on whether two consecutive leaves sit on
  the same or opposite side of the stem, so we can walk the stem from bottom to top
  (`stem[::-1]`) comparing each leaf to the one before it.
- We track the leaf type that would trigger a swap next, i.e. the side opposite the one
  we're currently standing on, starting one step before the lowest leaf so that stepping
  onto it for the first time doesn't get counted as a swap.
- Every time a block matches that tracked type, it's a swap: we increment the counter
  and flip the tracked side. Blocks with no leaf ("|") never match either side, so they
  get skipped for free.
- Just output the total swap count at the end.

Part 3:
- Same idea as part 2 - consecutive leaves on opposite sides mean a swap - but now every
  swap also breaks the leaf that was pushed off from, and the final jump to the flower
  head breaks whichever leaf is left standing.
- This time we scan top to bottom, which is the reverse of climbing order, and that
  works in our favor: the first non-"|" block found (the topmost leaf) never matches the
  empty `previous_leaf` sentinel, so it breaks immediately - modelling the final jump
  breaking the last leaf climbed. From there, whenever a block differs from the one
  before it, that's a swap, and the block we just landed on breaks off, since scanning
  backwards means it was the one climbed earlier.
- We repeat this whole climb-and-break pass, counting one successful climb per pass,
  until only one leaf is left. That last leaf never needs to be simulated - a single
  remaining leaf is always a guaranteed successful climb - which is why the climb
  counter starts at 1 instead of 0.
- Just output the total count at the end.
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
    stem = parse_file()
    cut = 8 if TEST_DATA else 400

    total = 0
    for i in range(len(stem) - cut):
        if stem[i] != "|":
            total += 1

    print(f"Total leaves: {total}")


@timer
def part2():
    stem = parse_file()

    current_leaf = "o-|" if stem[-1] == "|-o" else "o-|"

    swaps = 0
    for block in stem[::-1]:
        if block == current_leaf:
            swaps += 1
            current_leaf = current_leaf[::-1]

    print(f"Total swaps: {swaps}")


@timer
def part3():
    stem = parse_file()
    leaves = len(stem) - stem.count("|")

    # +1 to count the first leaf
    climbs = 1
    while leaves > 1:
        previous_leaf = ""
        sign = 1
        for i in range(len(stem)):
            if stem[i] == "|":
                continue
            if stem[i] != previous_leaf:
                previous_leaf = stem[i]
                sign *= -1
                stem[i] = "|"
                leaves -= 1
            else:
                previous_leaf = stem[i]
        climbs += 1

    print(f"Total climbs: {climbs}")


def parse_file() -> List[str]:
    file_name = "input_sample.txt" if TEST_DATA else "input.txt"
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    stem = []
    with open(abs_file_path, "r") as f:
        f.readline()
        f.readline()
        f.readline()
        while (line := f.readline()) != "#####":
            stem.append(line.strip())
    return stem


part1()
part2()
part3()
