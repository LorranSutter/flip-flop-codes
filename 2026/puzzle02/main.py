import os
from typing import List

from utils.args import parse_args
from utils.timer import timer

"""
Preprocessing:
- Read the input file and parse it into a list of single-character movements.

Part 1:
- The key insight is that we only need a single index into a fixed-size `temps` array:
  each movement just nudges it by +1 or -1 and wraps around with `% length`, since
  Python's modulo already keeps negative indices wrapping in the right direction.
- We walk the movements once, updating `index`, bumping `temps[index]`, and keeping a
  running `highest_temp` and its `highest_index`.
- Ties are handled inline: when a temperature matches the current highest, we only
  update `highest_index` if the new one is lower, so the lowest wall segment wins.

Obs: The length here is tiny, so a plain array works fine. For a much bigger hallway
     where most segments stay at temperature 0, a dictionary keyed by index would be
     the better choice.

Part 2:
- Same index-and-wrap approach as part 1, but now we track two positions at once:
  `index_R` for the cleaning robot, walking the movements forward, and `index_W` for
  the robotic wall segment, walking the same movements backward (`movements[::-1]`) -
  which is exactly what "reading the instructions in reverse order" means in code.
- Since we don't care about the actual position, only whether the two coincide, we
  skip the temperature array entirely and just count the steps where `index_R ==
  index_W`.

Part 3:
- The key insight is that all 100 wall segments shift together as a rigid block, so we
  don't need to simulate 100 positions individually - we only need to track how far the
  whole block has shifted.
- The trick is tracking that shift with the opposite sign convention from a normal
  position: `index_W` accumulates -1 for a `>` step (and +1 for `<`), so it holds the
  *negative* of the total wall shift instead of an actual position.
- That's what makes `index_R + index_W` land exactly on the identity of whichever wall
  segment currently faces the robot. If the whole block has shifted by `total_shift`,
  wall segment `id` sits at physical position `(id + total_shift) % length`. The robot
  is at `index_R`, so it's facing whichever `id` satisfies
  `id + total_shift ≡ index_R (mod length)`, i.e. `id ≡ index_R - total_shift`. Since
  `index_W = -total_shift`, that's exactly `index_R + index_W`.
- From there it's identical to part 1: bump `temps[index_temp]` and track the highest
  temperature with the same lowest-index tie-break.
"""


TEST_DATA = parse_args()


@timer
def part1():
    movements = parse_file()
    length = 100
    temps = [0] * length

    highest_temp, highest_index = 0, 0
    index = 0
    for movement in movements:
        index += 1 if movement == ">" else -1
        index %= length
        temps[index] += 1

        if temps[index] > highest_temp:
            highest_temp = temps[index]
            highest_index = index
        elif temps[index] == highest_temp:
            if index < highest_index:
                highest_index = index

    print(f"Hottest temperature times index: {highest_temp * (highest_index+1)}")


@timer
def part2():
    movements = parse_file()
    length = 100

    temp = 0
    index_R, index_W = 0, 0
    for movement_R, movement_W in zip(movements, movements[::-1]):
        index_R += 1 if movement_R == ">" else -1
        index_W += 1 if movement_W == ">" else -1
        index_R %= length
        index_W %= length

        temp += index_R == index_W

    print(f"Wall temperature: {temp}")


@timer
def part3():
    movements = parse_file()
    length = 100
    temps = [0] * length

    highest_temp, highest_index = 0, 0
    index_R, index_W = 0, 0
    for movement_R, movement_W in zip(movements, movements[::-1]):
        index_R += 1 if movement_R == ">" else -1
        index_W += -1 if movement_W == ">" else 1
        index_R %= length
        index_W %= length
        index_temp = (index_R + index_W) % length

        temps[index_temp] += 1

        if temps[index_temp] > highest_temp:
            highest_temp = temps[index_temp]
            highest_index = index_temp
        elif temps[index_temp] == highest_temp:
            if index_temp < highest_index:
                highest_index = index_temp

    print(f"Hottest temperature times index: {highest_temp * (highest_index+1)}")


def parse_file() -> List[str]:
    file_name = "input_sample.txt" if TEST_DATA else "input.txt"
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    movements = []
    with open(abs_file_path, "r") as f:
        movements = [element for element in f.read().strip()]
    return movements


part1()
part2()
part3()
