import os
from collections import Counter
from typing import List

from utils.timer import timer

"""
This is just a demo coding puzzle provided by the Flip Flop Codes,
used to try out the site before the real puzzles start.

Preprocessing:
- Read the input file and parse into a list of integers.

Part 1:
- Just sum all the numbers.

Part 2:
- Sum all the numbers and divide by how many there are, rounding to the nearest integer with the built-in round().

Part 3:
- The trick here is that we need two different counts from the same list: which number shows up most
  often, and which digit shows up least often across all numbers combined.
- We use a Counter over the numbers themselves to find the most common one, and a second Counter over
  their individual digits (each number split into characters) to find the least common digit.
- The answer is just those two values glued together as a string.

    Example:
        Numbers: [11, 22, 30, 34, 48, 8, 57, 57, 69, 69, 69]

        Counting the numbers: 69 shows up 3 times - more than anything else - so it's the most common number.

        Counting the digits (splitting every number into its characters first):
            '6':3 '9':3 '1':2 '2':2 '3':2 '4':2 '8':2 '5':2 '7':2 '0':1
        '0' only shows up once, so it's the least common digit.

        Result: "69" + "0" = "690"
"""


@timer
def part1():
    nums = parse_file("input.txt")
    print(f"Sum of the numbers: {sum(nums)}")


@timer
def part2():
    nums = parse_file("input.txt")
    print(f"Average of the numbers: {round(sum(nums) / len(nums))}")


@timer
def part3():
    nums = parse_file("input.txt")
    counter = Counter(nums)

    digits_counter = Counter()
    for num in nums:
        for d in str(num):
            digits_counter[d] += 1

    most_common_num = counter.most_common(1)[0][0]
    least_common_digit = digits_counter.most_common()[-1][0]
    
    result = str(most_common_num) + least_common_digit
    print(f"Credit card number and expiration date: {result}")


def parse_file(file_name: str) -> List[int]:
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    with open(abs_file_path, "r") as f:
        nums = [int(line.strip()) for line in f.readlines()]
    return nums


part1()
part2()
part3()
