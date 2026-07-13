import argparse
import os
import copy
from typing import List, Tuple

from utils.timer import timer

"""
Preprocessing:
- Read the input file and parse it into a 2D matrix of characters.

Part 1:
- This is just a straight walk through the grid: start at (0, 0) and keep moving to the next
  cell according to the arrow printed on the current one.
- We keep track of visited positions with a set. As soon as we're about to step onto a position
  already in that set, we've found the loop, and the size of the set is the answer.

Part 2:
- There's no shortcut here - we just brute force every legal change and rerun part 1's walk for
  each one, keeping the best result.
- We skip edge cells (as the problem requires) and skip changing a cell to the direction it
  already points, since that wouldn't be a real change.
- For every remaining (cell, direction) pair, we deep-copy the grid, apply the change, and reuse
  `drive` to get its visited count, keeping the largest one seen.

Part 3:
- Same brute-force-every-change idea as part 2, but each candidate grid is walked with
  `drive_illegal` instead of `drive`.
- The walk works the same as part 1, except revisiting a cell no longer means stopping right
  away: if we still have illegal turns left, we turn right relative to that cell's own arrow
  instead of following it, and spend one of our three turns.
- One tricky bit is that the turn is taken from the perspective of the arrow already printed on
  that cell, not the direction we arrived from - so a `v` always turns into `<`, no matter how we
  got there.
- If we're out of illegal turns, we stop instead of turning. The edge restriction from the
  problem is handled implicitly: an illegal turn taken from an edge cell would step outside the
  grid on the very next move, so checking whether we've gone out of bounds also catches the edge
  case the problem describes.
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
    grid = parse_file()

    visited = drive(grid)

    print(f"Number of visited districts: {visited}")


@timer
def part2():
    grid = parse_file()

    max_visited = 0
    for i in range(1, len(grid) - 1):
        for j in range(1, len(grid[i]) - 1):
            for direction in [">", "<", "v", "^"]:
                if grid[i][j] == direction:
                    continue

                new_grid = copy.deepcopy(grid)
                new_grid[i][j] = direction
                visited = drive(new_grid)

                if visited > max_visited:
                    max_visited = visited

    print(f"Number of visited districts: {max_visited}")


@timer
def part3():
    grid = parse_file()

    max_visited = 0
    for i in range(1, len(grid) - 1):
        for j in range(1, len(grid[i]) - 1):
            for direction in [">", "<", "v", "^"]:
                if grid[i][j] == direction:
                    continue

                new_grid = copy.deepcopy(grid)
                new_grid[i][j] = direction
                visited = drive_illegal(new_grid, 3)

                if visited > max_visited:
                    max_visited = visited

    print(f"Number of visited districts: {max_visited}")


def drive(grid: List[List[str]]):
    visited = set()
    i, j = 0, 0

    while (i, j) not in visited:
        visited.add((i, j))
        i, j = turn(grid[i][j], i, j)

    return len(visited)


def drive_illegal(grid: List[List[str]], num: int):
    turns = {"^": ">", ">": "v", "v": "<", "<": "^"}

    visited = set()
    i, j = 0, 0
    height, width = len(grid), len(grid[0])

    while True:
        if i < 0 or i >= height or j < 0 or j >= width:
            break

        next_district = grid[i][j]
        if (i, j) in visited:
            if num > 0:
                next_district = turns[next_district]
                num -= 1
            else:
                break

        visited.add((i, j))
        i, j = turn(next_district, i, j)

    return len(visited)


def turn(district: str, i: int, j: int) -> Tuple[int]:
    match district:
        case ">":
            j += 1
        case "<":
            j -= 1
        case "v":
            i += 1
        case "^":
            i -= 1

    return i, j


def parse_file() -> List[List[str]]:
    file_name = "input_sample.txt" if TEST_DATA else "input.txt"
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    grid = []
    with open(abs_file_path, "r") as f:
        for line in f:
            grid.append([direction for direction in line.strip()])
    return grid


part1()
part2()
part3()
