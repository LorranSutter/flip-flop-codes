import os
from typing import List

from utils.timer import timer

"""
Preprocessing:
- Read the input file and parse each line as an (x, y) coordinate.

Part 1:
- This is pretty much Manhattan distance
- We iterate over each coordinate and calcualate the Manhattan distance between the current coordinate and the previous one, and we sum them up.

Part 2:
- 

Part 3:
-
"""


@timer
def part1():
    coords = parse_file("input.txt")

    steps = 0
    pos = (0,0)
    for coord in coords:
        steps += abs(coord[0]-pos[0]) + abs(coord[1]-pos[1])
        pos = coord

    print(f"Total steps: {steps}")


@timer
def part2():
    # TODO: Implement part 2
    pass


@timer
def part3():
    # TODO: Implement part 3
    pass


def parse_file(file_name: str) -> List[str]:
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    with open(abs_file_path, "r") as f:
        coords = [tuple(map(int, line.split(','))) for line in f.readlines()]
    return coords


part1()
# part2()
# part3()
