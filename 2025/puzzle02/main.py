import argparse
import os
from typing import List

from utils.timer import timer

"""
Preprocessing:
- Read the input file and split it into a list of individual movement characters ('^' or 'v').

Part 1:
- The trick here is that we only need two running values: the current height and the highest point ever
  seen.
- We walk the blueprint one movement at a time. '^' adds one to the height, 'v' subtracts one. After each
  movement we compare the current height against the highest point recorded so far and update it if we've
  gone higher.

Part 2:
- Same idea as part 1, but now consecutive movements in the same direction compound instead of each move
  being worth a flat +1/-1.
- We track two extra values: 'sign' (which direction we're currently moving in) and 'counter' (how many
  moves in a row we've made in that direction). As long as the direction doesn't change, the counter keeps
  growing (or shrinking) and gets added straight to the height every step. The moment the direction flips,
  we reset the counter back to 0 before it starts accumulating again in the new direction.
- Worked example, using "^^^v^^^^vvvvvvv":

    move:     ^  ^  ^  v  ^  ^  ^  ^  v  v  v  v  v  v  v
    counter:  1  2  3 -1  1  2  3  4 -1 -2 -3 -4 -5 -6 -7
    height:   1  3  6  5  6  8 11 15 14 12  9  5  0 -6 -13

  Notice how the three '^' in a row ramp the height up by 1, then 2, then 3 (steeper each step), and the
  'v' that follows resets the counter to -1 rather than continuing to shrink. Highest point reached: 15.

Part 3:
- Quite similar to part 2, but the compounding uses a Fibonacci step instead of a linear counter, and the
  height only changes at the instant the direction flips (not on every single move).
- There are two tricks here:
    1. We can use dynamic programming to store Fibonacci numbers in a growing list instead of recomputing
       them from scratch every time we need one.
    2. Rather than adding to the height on every movement, we let the counter run for as long as the
       direction stays the same, and only fold it into the height as a single Fibonacci-sized jump the
       moment the sign flips - using the run length that just ended.
- Worked example, same input "^^^v^^^^vvvvvvv" (fib(1)=1, fib(2)=1, fib(3)=2, fib(4)=3):

    - '^' '^' '^' just grow the run counter to 3; height doesn't move yet (still 0).
    - 'v' flips the direction: height += fib(3) = 2, so height becomes 2. Counter resets to 0 (then
      ticks up to 1 for this 'v').
    - '^' flips back: height -= fib(1) = 1, so height becomes 1. Counter resets, ticks up to 1.
    - '^' '^' '^' grow the run counter to 4; height stays at 1.
    - 'v' flips: height += fib(4) = 3, so height becomes 4. This is the highest point reached.
    - The remaining six 'v' just keep extending the down-run without ever triggering another jump, so the
      final answer is 4.
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
    blueprint = parse_file()

    highest_point, height = 0, 0
    for movement in blueprint:
        match movement:
            case "^":
                height += 1
            case "v":
                height -= 1

        if height > highest_point:
            highest_point = height

    print(f"Highest point reached: {highest_point}")



@timer
def part2():
    blueprint = parse_file()

    highest_point, height, counter, sign = 0, 0, 0, 1
    for movement in blueprint:
        match movement:
            case "^":
                if sign < 0:
                    counter = 0
                    sign = 1
                counter += 1
            case "v":
                if sign > 0:
                    counter = 0
                    sign = -1
                counter -= 1

        height += counter

        if height > highest_point:
            highest_point = height

    print(f"Highest point reached: {highest_point}")


@timer
def part3():
    blueprint = parse_file()

    highest_point, height, counter, sign = 0, 0, 0, 1
    for movement in blueprint:
        match movement:
            case "^":
                if sign < 0:
                    height -= fib(counter)
                    counter = 0
                    sign = 1
            case "v":
                if sign > 0:
                    height += fib(counter)
                    counter = 0
                    sign = -1

        counter += 1

        if height > highest_point:
            highest_point = height

    print(f"Highest point reached: {highest_point}")


fibs = [1, 1]
def fib(n: int) -> int:
    if n < 1:
        return 0
    if len(fibs) < n:
        for i in range(len(fibs), n):
            fibs.append(fibs[i-1] + fibs[i-2])

    return fibs[n-1]


def parse_file() -> List[str]:
    file_name = "input_sample.txt" if TEST_DATA else "input.txt"
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    with open(abs_file_path, "r") as f:
        blueprint = [movement for movement in f.read().strip()]
    return blueprint


part1()
part2()
part3()
