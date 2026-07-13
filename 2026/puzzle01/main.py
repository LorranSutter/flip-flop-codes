import argparse
import os
from typing import List

from utils.timer import timer

"""
Nice initial warmup!

Preprocessing:
- Read the input file and parse into a list of integers.

Part 1:
- Iterate through the list of temperatures and accumulate the difference between the threshold and the
  temperature for the ones that are below the threshold.

Part 2:
- Same as part 1, but for temperatures above the threshold we add the difference times 5 instead.

Part 3:
- We split the list of temperatures in two halves of equal size: the first half is the current
  temperatures, the second half is the desired temperatures.
- We iterate over both lists simultaneously. For current temperatures below target we add the
  difference; for the ones above we add the difference times 5.
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
    temps = parse_file()
    threshold = 60

    seconds = 0
    for temp in temps:
        if temp < threshold:
            seconds += (threshold - temp)
    
    print(f"Total seconds: {seconds}")


@timer
def part2():
    temps = parse_file()
    threshold = 60

    seconds = 0
    for temp in temps:
        if temp < threshold:
            seconds += (threshold - temp)
        elif temp > threshold:
            seconds += (temp - threshold) * 5
    
    print(f"Total seconds: {seconds}")


@timer
def part3():
    temps = parse_file()
    current_temp = temps[:len(temps)//2]
    preferred_temp = temps[len(temps)//2:]

    seconds = 0
    for curr, target in zip(current_temp, preferred_temp):
        if curr < target:
            seconds += (target - curr)
        elif curr > target:
            seconds += (curr - target) * 5
    
    print(f"Total seconds: {seconds}")


def parse_file() -> List[str]:
    file_name = "input_sample.txt" if TEST_DATA else "input.txt"
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    temps = []
    with open(abs_file_path, "r") as f:
        for line in f:
            temps.append(int(line.strip()))
    return temps


part1()
part2()
part3()
