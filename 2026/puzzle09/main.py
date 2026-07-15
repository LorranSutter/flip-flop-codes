import argparse
import os
import sys
import time
import math
import heapq
from typing import Tuple, List

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


def parse_args() -> bool:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--test", action="store_true", help="use input_sample.txt instead of input.txt"
    )
    return parser.parse_args().test


TEST_DATA = parse_args()


@timer
def part1():
    # TODO: Implement part 1
    grid, start, end = parse_file()

    d = dijkstra(grid, start, end)

    print(f"Steps of the shortest path: {d}")


@timer
def part2():
    # TODO: Implement part 2
    grid, start, end = parse_file()
    d, path = dijkstra_with_teleport(grid, start, end)

    print_grid(grid, path)

    print(f"Steps of the shortest path: {d}")


@timer
def part3():
    # TODO: Implement part 3
    lines = parse_file()
    pass


def dijkstra(grid: List[List[str]], start: Tuple[int], end: Tuple[int]) -> int:
    # Priority queue
    pq = []
    dist = dict()
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            dist[(i, j)] = math.inf
    dist[start] = 0
    heapq.heappush(pq, (start, 0))

    directions = ((-1, 0), (1, 0), (0, -1), (0, 1))

    while pq:
        u, d = heapq.heappop(pq)

        if u == end:
            return d

        # If this distance not the latest shortest one, skip it
        if d > dist[u]:
            continue

        for direction in directions:
            v = (u[0] + direction[0], u[1] + direction[1])
            if grid[v[0]][v[1]] == "#":
                continue

            if dist[u] + 1 < dist[v]:
                dist[v] = dist[u] + 1
                heapq.heappush(pq, (v, dist[v]))

    return -1


def dijkstra_with_teleport(
    grid: List[List[str]], start: Tuple[int], end: Tuple[int]
) -> Tuple[int, List[Tuple[int]]]:
    # Priority queue
    pq = []
    dist, parent = dict(), dict()
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            dist[(i, j)] = math.inf
            parent[(i, j)] = None
    dist[start] = 0
    heapq.heappush(pq, (0, start))

    directions = ((-1, 0), (1, 0), (0, -1), (0, 1))

    while pq:
        d, u = heapq.heappop(pq)

        if u == end:
            # Reconstruct path
            path = []
            curr = end
            while curr is not None:
                path.append(curr)
                curr = parent[curr]
            path.reverse()
            return d, path

        # If this distance not the latest shortest one, skip it
        if d > dist[u]:
            continue

        for direction in directions:
            v = (u[0] + direction[0], u[1] + direction[1])
            if grid[v[0]][v[1]] == "#":
                continue

            if dist[u] + 1 < dist[v]:
                dist[v] = dist[u] + 1
                parent[v] = u
                heapq.heappush(pq, (dist[v], v))

            while True:
                if grid[v[0]][v[1]] == "#":
                    v = (v[0] - direction[0], v[1] - direction[1])
                    if dist[u] + 1 < dist[v]:
                        dist[v] = dist[u] + 1
                        parent[v] = u
                        heapq.heappush(pq, (dist[v], v))
                    break
                v = (v[0] + direction[0], v[1] + direction[1])

    return -1, []


def print_grid(grid: List[List[str]], path: List[Tuple[int]]):
    for i in range(len(grid)):
        row = ""
        for j in range(len(grid[i])):
            if (i, j) in path:
                row += f"{tcolors.GREEN}*{tcolors.RESET}"
            else:
                row += grid[i][j]
        print(row)


def clear_lines(size: int):
    for _ in range(size):
        sys.stdout.write("\033[F\033[K")


def parse_file() -> Tuple[List[List[str]], Tuple[str], Tuple[str]]:
    file_name = "input_sample.txt" if TEST_DATA else "input.txt"
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    grid = []
    start, end = (0, 0), (0, 0)
    with open(abs_file_path, "r") as f:
        for i, line in enumerate(f):
            row = []
            for j, element in enumerate(line.strip()):
                if element == "S":
                    start = (i, j)
                elif element == "E":
                    end = (i, j)
                row.append(element)
            grid.append(row)

    return grid, start, end


part1()
part2()
# part3()
