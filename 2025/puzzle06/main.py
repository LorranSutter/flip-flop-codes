import os
from typing import List

from utils.timer import timer

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
    # TODO: Implement part 3
    lines = parse_file("input_sample.txt")
    pass


def within_frame(pos: List[int], frame_boundaries: List[int]) -> bool:
    if not (frame_boundaries[0] <= pos[0] <= frame_boundaries[2]):
        return False
    if not (frame_boundaries[1] <= pos[1] <= frame_boundaries[3]):
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
# part3()
