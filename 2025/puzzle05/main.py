import argparse
import os

from utils.timer import timer

"""
Preprocessing:
- Read the input file and store the tunnels as a single string, one letter per position.
- In all parts we build a `connections` dictionary from that string. Since each tunnel letter
  shows up exactly twice, the key is the letter and the value is a list of its two positions,
  recorded in the order they were found, so `connections[tunnel][0]` is always the earlier index.

Part 1:
- The key insight is that every letter appearing exactly twice turns the string into a set of
  portals: standing on one occurrence of a letter, you can jump straight to its twin. Walking
  the tunnels means repeatedly jumping to the current letter's other position, then stepping one
  further to keep moving forward, until we've walked past the end of the string.
- We start at position 0. In each iteration we add the jump's length to `steps` - simply the
  distance between the letter's two recorded positions, since the first is always the smaller.
- Then we check whether we're currently on the first or second occurrence and move to the other
  one, adding 1 more so we advance past it instead of jumping back and forth forever.
- The final result is the accumulated steps.

  Here's a trace on the sample "ABccksiPiBAksP" (indices 0-13):

  index:  0 1 2 3 4 5 6 7 8 9 10 11 12 13
  letter: A B c c k s i P i B A  k  s  P

  connections: A:(0,10)  B:(1,9)  c:(2,3)  k:(4,11)  s:(5,12)  i:(6,8)  P:(7,13)

  i=0  (A) jump->10, +1 -> i=11   steps += 10-0 = 10   (steps=10)
  i=11 (k) jump->4,  +1 -> i=5    steps += 11-4 = 7    (steps=17)
  i=5  (s) jump->12, +1 -> i=13   steps += 12-5 = 7    (steps=24)
  i=13 (P) jump->7,  +1 -> i=8    steps += 13-7 = 6    (steps=30)
  i=8  (i) jump->6,  +1 -> i=7    steps += 8-6  = 2    (steps=32)
  i=7  (P) jump->13, +1 -> i=14   steps += 13-7 = 6    (steps=38)

  i=14 is past the last index, so the walk stops. Final steps = 38.

Part 2:
- Same jump-then-step walk as part 1, but we don't care about distances anymore, only about
  which letters we actually stood on along the way.
- A second dictionary tracks whether each tunnel letter was visited, starting all False, and we
  flip a letter to True every time we land on it.
- Dictionaries preserve insertion order, so the tunnel letters come out of `visited.keys()` in
  the same order they first appeared in the input. We just walk that order and concatenate every
  letter that was never visited.
- The final result is the concatenated unvisited tunnels.

Part 3:
- Same walk as part 1, but each jump's distance is signed by the case of the tunnel letter: +1
  for lowercase, -1 for uppercase.
- We multiply the jump distance by that sign before adding it to `steps`, so lowercase tunnels
  add to the total and uppercase ones subtract from it.
- The final result is the accumulated (signed) steps.
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
    tunnels = parse_file()
    connections = build_connections(tunnels)

    i, steps = 0, 0
    while i < len(tunnels):
        tunnel = tunnels[i]
        steps += connections[tunnel][1] - connections[tunnel][0]

        if i == connections[tunnel][0]:
            i = connections[tunnel][1]
        else:
            i = connections[tunnel][0]

        i += 1

    print(f"Steps: {steps}")

@timer
def part2():
    tunnels = parse_file()
    connections = build_connections(tunnels)

    i = 0
    visited = {tunnel: False for tunnel in tunnels}
    while i < len(tunnels):
        tunnel = tunnels[i]
        visited[tunnel] = True

        if i == connections[tunnel][0]:
            i = connections[tunnel][1]
        else:
            i = connections[tunnel][0]

        i += 1
    
    unvisited = ""
    for tunnel in visited.keys():
        if not visited[tunnel]:
            unvisited += tunnel
    
    print(f"Unvisited tunnels: {unvisited}")


@timer
def part3():
    tunnels = parse_file()  
    connections = build_connections(tunnels)

    i, steps, sign = 0, 0, 1
    while i < len(tunnels):
        tunnel = tunnels[i]
        sign = 1 if tunnel.islower() else -1
        steps += sign * (connections[tunnel][1] - connections[tunnel][0])

        if i == connections[tunnel][0]:
            i = connections[tunnel][1]
        else:
            i = connections[tunnel][0]

        i += 1

    print(f"Steps: {steps}")

def build_connections(tunnels: str) -> dict:
    connections = dict()
    for i, tunnel in enumerate(tunnels):
        if tunnel not in connections:
            connections[tunnel] = [i]
        else:
            connections[tunnel].append(i)
    return connections

def parse_file() -> str:
    file_name = "input_sample.txt" if TEST_DATA else "input.txt"
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    tunnels = ""
    with open(abs_file_path, "r") as f:
        tunnels = f.read().strip()
    return tunnels


part1()
part2()
part3()
