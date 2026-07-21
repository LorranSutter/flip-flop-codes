import os
from collections import Counter
from typing import List

from utils.args import parse_args
from utils.timer import timer

"""
Preprocessing:
- Read the input file and parse each line into an (r, g, b) tuple of ints.

Part 1:
- The trick here is that "most common color" is just a frequency count, so there's no need to hand-roll
  one - Python's built-in Counter does exactly this.
- We feed all the RGB tuples into a Counter and pull the top entry out with 'most_common(1)'.

Part 2:
- A color is "Special" whenever any two of its channels match (r == g, r == b, or g == b), and special
  colors don't count toward anything here - we just skip them.
- For the rest, we count how many have green as the strictest channel, i.e. green is the single highest
  value among the three.

Part 3:
- Same filtering as part 2 (special colors are skipped for the "highest channel" check), but now every
  color contributes to a running total instead of just the green ones.
- One tricky thing worth calling out: because a color is only "not special" when all three channels are
  distinct, the highest value is guaranteed to belong to exactly one channel there - no tie-breaking
  needed once we know we're past the special check.
- Special colors are worth a flat 10. Non-special colors are worth 5 if red is highest, 2 if green is
  highest, 4 if blue is highest.
- Worked example, using the sample input:

    color         special?  highest channel  price
    10,20,30      no        blue             4
    20,10,30      no        blue             4
    30,20,10      no        red              5
    10,50,10      yes (r==b)   -             10
    50,10,50      yes (r==b)   -             10
    10,20,30      no        blue             4
                                        total = 37
"""


TEST_DATA = parse_args()


@timer
def part1():
    rgbs = parse_file()
    counter = Counter(rgbs)

    print(f"Most common color: {tuple(counter.most_common(1)[0][0])}")


@timer
def part2():
    rgbs = parse_file()

    count_green = 0
    for rgb in rgbs:
        # Special
        if rgb[0] == rgb[1] or rgb[0] == rgb[2] or rgb[1] == rgb[2]:
            continue
        if max(rgb) == rgb[1]:
            count_green += 1

    print(f"Number of Green colors: {count_green}")


@timer
def part3():
    rgbs = parse_file()

    total = 0
    for rgb in rgbs:
        # Special
        if rgb[0] == rgb[1] or rgb[0] == rgb[2] or rgb[1] == rgb[2]:
            total += 10
            continue

        max_value = max(rgb)
        if max_value == rgb[0]:
            total += 5
        elif max_value == rgb[1]:
            total += 2
        else:
            total += 4

    print(f"Total price: {total}")


def parse_file() -> List[str]:
    file_name = "input_sample.txt" if TEST_DATA else "input.txt"
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    with open(abs_file_path, "r") as f:
        rgbs = [tuple(map(int, line.split(','))) for line in f.readlines()]
    return rgbs


part1()
part2()
part3()
