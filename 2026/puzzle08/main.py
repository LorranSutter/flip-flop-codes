import os
from typing import Dict, List

from utils.args import parse_args
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


TEST_DATA = parse_args()


@timer
def part1():
    lines = parse_file()
    rules = dict()
    for line in lines:
        if line[0] not in rules:
            rules[line[0]] = "".join(line[1:])

    generations = 7

    population = "AB"
    for _ in range(generations):
        new_population = ""
        for stoat in population:
            new_population += rules[stoat]
        population = new_population

    print(f"Total stoats: {len(population)}")


@timer
def part2():
    lines = parse_file()
    rules = dict()
    reversed_rules = dict()
    for line in lines:
        key = "".join(line[:2])
        if key not in rules:
            rules[key] = "".join(line[2:])

    print(rules)
    print(reversed_rules)
    generations = 7

    population = "AB"
    for _ in range(generations):
        new_population = population[0]
        for i in range(len(population) - 1):
            stoat_pair = population[i : i + 2]
            if stoat_pair not in rules:
                new_population += rules[stoat_pair[::-1]]
            else:
                new_population += rules[stoat_pair]
            new_population += stoat_pair[1]
        population = new_population

    print(f"Total stoats: {len(population)}")


@timer
def part3():
    # TODO: Implement part 3
    lines = parse_file()
    rules = dict()
    reversed_rules = dict()
    for line in lines:
        key = "".join(line[:2])
        if key not in rules:
            rules[key] = "".join(line[2:])

    print(rules)
    print(reversed_rules)
    generations = 14

    population = "AB"
    for _ in range(generations):
        print(_)
        new_population = population[0]
        for i in range(len(population) - 1):
            stoat_pair = population[i : i + 2]
            if stoat_pair not in rules:
                new_population += rules[stoat_pair[::-1]]
            else:
                new_population += rules[stoat_pair]
            new_population += stoat_pair[1]
        rules[population] = new_population
        population = new_population

    print(f"Total stoats: {len(population)}")


def parse_file() -> List[str]:
    file_name = "input_sample.txt" if TEST_DATA else "input.txt"
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    lines = []
    with open(abs_file_path, "r") as f:
        for line in f:
            lines.append(line.strip().split(" "))
    return lines


part1()
part2()
part3()
