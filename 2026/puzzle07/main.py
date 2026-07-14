import argparse
import os
from typing import Iterator, List, Tuple

from utils.timer import timer
from utils.utils import tcolors

"""
Preprocessing:
- We read the input file and return two things: a list of characters representing the movements, and
  an iterator that yields the position of each sushi in the order it will appear on the board.

Part 1:
- For this part we only care about how many pieces of sushi the snake eats, so there's no need to
  track a body at all, just the head's position is enough.
- We walk through the first half of the movements, since that's all this part asks for, updating the
  head's position on every step. Whenever the head lands on the current sushi's coordinates, we count
  it and pull the next sushi's coordinates off the iterator.
- At the end we just report the total count of sushi eaten.

Part 2:
- This part is a natural extension of the first: we still track the head against the next sushi and
  move it the same way, but now the snake has a body that has to follow along, just like classic Snake.
- We keep an array storing the body's positions, ordered from head to tail. Every iteration we prepend
  the head's position to that array, then move the head. If the new position isn't the sushi, we also
  pop the tail off, so the snake only actually grows on the steps where it eats.
- The snake dies the moment its head would land on a tile already in its own body, which is exactly
  when we stop the loop. At the end we output the current size of the snake array (plus one, since we
  break before appending the position that would have killed it).

Part 3:
- This last part is also a natural extension of the second: same head, sushi, and growth handling, but
  the snake no longer dies on a self-collision, it eats through itself instead.
- When the head would land on a body tile, we look up that tile's index in the array and slice the
  array down to just before it, so the collided segment and everything behind it disappears. The head
  then moves onto that now-empty tile as normal, and we bump a counter tracking how many times this
  happened.
- At the end we report the final snake length multiplied by the number of times it ate itself.

Obs: One interesting thing is that, initially we see the problem to be modeled as a matrix, but
     we don't have to worry about the size of the grid or building a matrix for this problem.
     Just the snake and sushi positioning are enough, since the boundaries of the grid are
     irrelevant.
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
    movements, sushis = parse_file()

    sushi = next(sushis)
    head = (0, 0)
    eats = 0
    for movement in movements[: len(movements) // 2 + 1]:
        if head == sushi:
            eats += 1
            sushi = next(sushis, (-1, -1))
        head = update_head(head, movement)

    print(f"Pieces of sushi eaten: {eats}")


@timer
def part2():
    movements, sushis = parse_file()

    sushi = next(sushis)
    head = (0, 0)
    snake = []
    for movement in movements:
        if head in snake:
            break

        snake = [head] + snake
        head = update_head(head, movement)

        if head == sushi:
            sushi = next(sushis, (-1, -1))
        else:
            snake.pop()

    # +1 bc we break the loop before appending the last position
    print(f"Snake size: {len(snake)+1}")


@timer
def part3():
    movements, sushis = parse_file()

    sushi = next(sushis)
    head = (0, 0)
    snake = [head]
    eats_itself = 0
    for movement in movements:
        # print_grid(10 if TEST_DATA else 30, head, snake, sushi)
        head = update_head(head, movement)

        if head == sushi:
            sushi = next(sushis, (-1, -1))
        else:
            snake.pop()
            try:
                index = snake.index(head)
                eats_itself += 1
                snake = snake[: index - 1]
            except:
                pass

        snake = [head] + snake

    snake_length = len(snake)
    print(
        f"Snake length ({snake_length}) times eats itself ({eats_itself}): {snake_length*eats_itself}"
    )


def update_head(head: Tuple[int], movement: str) -> Tuple[int]:
    match movement:
        case ">":
            head = (head[0] + 1, head[1])
        case "^":
            head = (head[0], head[1] + 1)
        case "<":
            head = (head[0] - 1, head[1])
        case "v":
            head = (head[0], head[1] - 1)

    return head


def print_grid(
    size: int, snake_head: Tuple[int], snake: List[Tuple[int]], sushi: Tuple[int]
):
    grid = []
    for i in range(size):
        row = ""
        for j in range(size):
            if (j, i) == sushi:
                row += f"{tcolors.RED}@{tcolors.RESET}"
            elif (j, i) == snake_head:
                row += f"{tcolors.YELLOW}S{tcolors.RESET}"
            elif (j, i) in snake:
                row += f"{tcolors.GREEN}#{tcolors.RESET}"
            else:
                row += "."
        grid.append(row)

    for row in grid[::-1]:
        print(row)


def parse_file() -> Tuple[List[str], Iterator[Tuple[int]]]:
    file_name = "input_sample.txt" if TEST_DATA else "input.txt"
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    movements = []
    sushis = []
    with open(abs_file_path, "r") as f:
        movements = [movement for movement in f.readline().strip()]
        f.readline()  # blank line
        for line in f:
            sushis.append(tuple(map(int, line.strip().split(","))))
    return movements, iter(sushis)


part1()
part2()
part3()
