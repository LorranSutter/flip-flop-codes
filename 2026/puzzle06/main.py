import argparse
import os
from collections import deque
from typing import Dict, List, Set, Tuple

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

    start = (-1, -1)
    lights = []
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == "S":
                start = (i, j)
            elif grid[i][j] == "*":
                lights.append((i, j))

    print_grid(grid)

    bfs(grid, start)

    print_grid(grid, ["L", "R", "*"])

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    binary_lights = ""
    for light in lights:
        for dr, dc in directions:
            adj = tuple([light[0] + dr, light[1] + dc])
            if grid[adj[0]][adj[1]] == "R":
                binary_lights += "1"
                break
            if grid[adj[0]][adj[1]] == "L":
                binary_lights += "0"
                break

    print(binary_lights)

    print(int(binary_lights, 2))


@timer
def part2():
    grid = parse_file()

    start = (-1, -1)
    lights = []
    bluetooth = dict()
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == "S":
                start = (i, j)
            elif grid[i][j] == "*":
                lights.append((i, j))
            elif grid[i][j].isalpha():
                bluetooth[grid[i][j]] = (i, j)

    print_grid(grid, ["#", "*", "a", "b", "c", "A", "B", "C"])

    bfs2(grid, start, bluetooth)

    print_grid(grid, ["L", "R", "*", "a", "b", "c"])

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    binary_lights = ""
    for light in lights:
        for dr, dc in directions:
            adj = tuple([light[0] + dr, light[1] + dc])
            if grid[adj[0]][adj[1]] == "R":
                binary_lights += "1"
                break
            if grid[adj[0]][adj[1]] == "L":
                binary_lights += "0"
                break

    print(binary_lights)

    print(int(binary_lights, 2))


@timer
def part3():
    # TODO: Implement part 3
    grid = parse_file()

    start = (-1, -1)
    lights = []
    bluetooth = dict()
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == "S":
                start = (i, j)
            elif grid[i][j] == "*":
                lights.append((i, j))
            elif grid[i][j].isalpha():
                bluetooth[grid[i][j]] = (i, j)

    print_grid(grid, ["#", "*", "a", "b", "c", "A", "B", "C"])

    bfs3(grid, start, bluetooth)

    print_grid(grid, ["L", "R", "*", "a", "b", "c"])

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    binary_lights = ""
    for light in lights:
        for dr, dc in directions:
            adj = tuple([light[0] + dr, light[1] + dc])
            if grid[adj[0]][adj[1]] == "R":
                binary_lights += "1"
                break
            if grid[adj[0]][adj[1]] == "L":
                binary_lights += "0"
                break

    print(binary_lights)

    print(int(binary_lights, 2))


def bfs(grid: List[List[str]], start: Tuple[int]):
    if not grid or grid[start[0]][start[1]] == "0":
        return

    def rotate(gear: str) -> str:
        return "L" if gear == "R" else "R"

    queue = deque([start])
    grid[start[0]][start[1]] = "L"

    visited = set([start])

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue:
        pos = queue.popleft()

        for dr, dc in directions:
            new_pos = tuple([pos[0] + dr, pos[1] + dc])

            if grid[new_pos[0]][new_pos[1]] == "#" and new_pos not in visited:
                grid[new_pos[0]][new_pos[1]] = rotate(grid[pos[0]][pos[1]])
                visited.add(new_pos)
                queue.append(new_pos)


def bfs2(grid: List[List[str]], start: Tuple[int], bluetooth: Dict[str, Tuple[int]]):
    if not grid or grid[start[0]][start[1]] == "0":
        return

    def rotate(gear: str) -> str:
        return "L" if gear == "R" else "R"

    queue = deque([start])
    grid[start[0]][start[1]] = "L"

    visited = set([start])

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue:
        pos = queue.popleft()

        for dr, dc in directions:
            new_pos = tuple([pos[0] + dr, pos[1] + dc])
            component = grid[pos[0]][pos[1]]
            new_component = grid[new_pos[0]][new_pos[1]]

            if new_pos not in visited:
                if new_component in ["#", "3"]:
                    grid[new_pos[0]][new_pos[1]] = rotate(component)
                    visited.add(new_pos)
                    queue.append(new_pos)
                elif new_component in bluetooth and new_component.islower():
                    output = bluetooth[new_component.upper()]

                    grid[output[0]][output[1]] = component
                    visited.add(output)
                    queue.append(output)


def bfs3(grid: List[List[str]], start: Tuple[int], bluetooth: Dict[str, Tuple[int]]):
    if not grid or grid[start[0]][start[1]] == "0":
        return

    def rotate(gear: str) -> str:
        return "L" if gear == "R" else "R"

    queue = deque([start])
    bluetooth_queue = deque([])
    grid[start[0]][start[1]] = "L"

    visited = set([start])

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue:
        pos = queue.popleft()

        for dr, dc in directions:
            new_pos = tuple([pos[0] + dr, pos[1] + dc])
            component = grid[pos[0]][pos[1]]
            new_component = grid[new_pos[0]][new_pos[1]]

            if new_pos not in visited:
                if new_component in ["#", "3"]:
                    grid[new_pos[0]][new_pos[1]] = rotate(component)
                    visited.add(new_pos)
                    queue.append(new_pos)
                elif new_component in bluetooth and new_component.islower():
                    output = bluetooth[new_component.upper()]

                    grid[output[0]][output[1]] = component
                    visited.add(output)
                    bluetooth_queue.append(output)

    while bluetooth_queue:
        pos = bluetooth_queue.popleft()

        for dr, dc in directions:
            new_pos = tuple([pos[0] + dr, pos[1] + dc])
            print(new_pos, dfs_size(grid, new_pos, set()))

            component = grid[pos[0]][pos[1]]
            new_component = grid[new_pos[0]][new_pos[1]]

            if new_pos not in visited:
                if new_component in ["#", "3"]:
                    grid[new_pos[0]][new_pos[1]] = rotate(component)
                    visited.add(new_pos)
                    bluetooth_queue.append(new_pos)
                elif new_component in bluetooth and new_component.islower():
                    output = bluetooth[new_component.upper()]

                    grid[output[0]][output[1]] = component
                    visited.add(output)
                    bluetooth_queue.append(output)


def dfs_size(grid: List[List[str]], pos: Tuple[int], visited: Set = None) -> int:
    if visited is None:
        visited = set()

    if pos in visited or grid[pos[0]][pos[1]] != "3":
        return 0

    visited.add(pos)
    size = 1

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for dr, dc in directions:
        new_pos = tuple([pos[0] + dr, pos[1] + dc])
        size += dfs_size(grid, new_pos, visited)

    return size


def is_prime(n):
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False

    return True


def print_grid(grid: List[List[str]], print_chars: List[str] = None):
    for i in range(len(grid)):
        if not print_chars:
            print("".join(grid[i]))
            continue

        row = ""
        for j in range(len(grid[i])):
            if grid[i][j] in print_chars:
                row += grid[i][j]
            else:
                row += "."
        print(row)


def parse_file() -> List[List[str]]:
    file_name = "input_sample.txt" if TEST_DATA else "input.txt"
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    grid = []
    with open(abs_file_path, "r") as f:
        for line in f:
            grid.append(["0"] + [component for component in line.strip()] + ["0"])

    grid.insert(0, ["0"] * len(grid[0]))
    grid.append(["0"] * len(grid[0]))

    return grid


part1()
part2()
part3()
