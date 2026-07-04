import os
from typing import List

from utils.timer import timer

"""
Preprocessing:
- Read the input file and parse it into a list of pairs of integers, representing each bird's speed.

Part 1:
- The key insight is that we don't need to simulate the bird's position second by second.
- Since birds wrap around the edges of the sky, the position after X seconds is just the speed times the
  seconds, taken modulo the sky size.
- So for each bird we compute the final position directly:
    pos_x = (speed_x * seconds) % size
    pos_y = (speed_y * seconds) % size
- Then we check if that position falls within the frame, and accumulate the birds that do.

Part 2:
- Same idea as part 1, but with two twists.
- First, we repeat the calculation 1000 times, once per picture.
- Second, instead of starting from (0, 0) every time, we carry the position forward from the previous
  picture and keep advancing it by `speed * seconds`, checking the frame again after every step.

Part 3:
- Same code as part 2, just with a different number of seconds between pictures.

Obs:
1. There's a way to optimize this: since we repeat the calculation 1000 times, a bird will likely end up
   back in a position it has already visited. If that happens, we could compute the cycle length and how
   many times the bird lands in the frame within one cycle, then multiply out instead of iterating all
   1000 steps. The numbers here are small enough that this optimization isn't needed.
2. After checking on Discord, it turned out an off-by-one was possible, so `within_frame` was fixed to
   exclude the max boundary.
"""


@timer
def part1():
    speeds = parse_file("input.txt")
    size, frame, seconds = 1000, 500, 100
    diff = (size - frame) // 2
    frame_boundaries = [diff, diff, diff + frame, diff + frame]

    birds_in_frame = 0
    for speed in speeds:
        pos_x = (speed[0] * seconds) % size
        pos_y = (speed[1] * seconds) % size

        birds_in_frame += within_frame([pos_x, pos_y], frame_boundaries)

    print(f"Birds in frame: {birds_in_frame}")


@timer
def part2():
    speeds = parse_file("input.txt")
    size, frame, seconds = 1000, 500, 3600
    diff = (size - frame) // 2
    frame_boundaries = [diff, diff, diff + frame, diff + frame]

    birds_in_frame = 0
    for speed in speeds:
        pos = [0, 0]
        for _ in range(1000):
            pos[0] = (pos[0] + speed[0] * seconds) % size
            pos[1] = (pos[1] + speed[1] * seconds) % size
            birds_in_frame += within_frame([pos[0], pos[1]], frame_boundaries)

    print(f"Birds in frame: {birds_in_frame}")


@timer
def part3():
    speeds = parse_file("input.txt")
    size, frame, seconds = 1000, 500, 31556926
    diff = (size - frame) // 2
    frame_boundaries = [diff, diff, diff + frame, diff + frame]

    birds_in_frame = 0
    for speed in speeds:
        pos = [0, 0]
        for _ in range(1000):
            pos[0] = (pos[0] + speed[0] * seconds) % size
            pos[1] = (pos[1] + speed[1] * seconds) % size
            birds_in_frame += within_frame([pos[0], pos[1]], frame_boundaries)

    print(f"Birds in frame: {birds_in_frame}")


def within_frame(pos: List[int], frame_boundaries: List[int]) -> bool:
    if not (frame_boundaries[0] <= pos[0] < frame_boundaries[2]):
        return False
    if not (frame_boundaries[1] <= pos[1] < frame_boundaries[3]):
        return False
    return True


def parse_file(file_name: str) -> List[List[int]]:
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    speeds = []
    with open(abs_file_path, "r") as f:
        for line in f:
            speeds.append(list(map(int, line.strip().split(","))))
    return speeds


part1()
part2()
part3()
