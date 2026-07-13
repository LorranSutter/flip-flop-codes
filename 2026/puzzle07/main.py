import os
from typing import List, Tuple

from utils.timer import timer
from utils.utils import tcolors

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
    test_data = False
    movements, sushis = parse_file("input_sample.txt" if test_data else "input.txt")

    sushis = iter(sushis)

    head = (0, 0)
    eats = 0
    for movement in movements[: len(movements) // 2 + 1]:
        if next(sushis, (-1, -1)) == head:
            eats += 1
        head = update_head(head, movement)

    print(f"Pieces of sushi eaten: {eats}")


@timer
def part2():
    test_data = False
    movements, sushis = parse_file("input_sample.txt" if test_data else "input.txt")

    sushis = iter(sushis)
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

    print(f"Snake size: {len(snake)+1}")


@timer
def part3():
    test_data = False
    movements, sushis = parse_file("input_sample.txt" if test_data else "input.txt")

    sushis = iter(sushis)
    sushi = next(sushis)

    head = (0, 0)
    snake = [head]
    eats_itself = 0
    for movement in movements:
        # print_grid(10 if test_data else 30, head, snake, sushi)
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


def parse_file(file_name: str) -> Tuple[List[str], List[Tuple[int]]]:
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    movements = []
    sushis = []
    with open(abs_file_path, "r") as f:
        movements = [movement for movement in f.readline().strip()]
        f.readline()  # blank line
        for line in f:
            sushis.append(tuple(map(int, line.strip().split(","))))
    return movements, sushis


part1()
part2()
part3()
