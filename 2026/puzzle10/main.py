import argparse
import os
import math
from typing import Dict, List

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


class Interpreter:
    def __init__(self, size: int, bits: int, instructions: List[str] = []):
        self.registers: List[int] = [0] * size
        self.bit_size: int = 2**bits
        self.instructions: List[str] = []
        self.commands: List[List[int]] = []
        self.labels: Dict[int, int] = dict()
        self.current_command_id = 0

        if instructions != []:
            self.process_instructions(instructions)

    def __str__(self):
        return f"Registers: {self.registers}"

    def set_register_value(self, id: int, value: int):
        self.registers[id] = value

    def set_instructions(self, instructions: List[str]):
        self.instructions = instructions

    def process_instructions(self, instructions: List[str]):
        command_id = 0
        for instruction in instructions:
            instruction = instruction.split("ne")
            if instruction[0][:2] == "ba":
                instruction = [arg.count("na") for arg in instruction]
                self.commands.append(instruction)
                command_id += 1
            else:
                instruction = instruction[0]
                self.labels[instruction.count("na")] = command_id

    def process_commands(self, limit_instructions: int = math.inf) -> bool:
        """
        Process the commands
        Return:
            False -> Reach the limit instructions and didn't finish all commands
            True -> Finished all commands before reaching the limit instructions
        """
        count_instructions = 0
        while self.current_command_id < len(self.commands):
            command = self.commands[self.current_command_id]
            self.process_command(command[0], command[1:])

            count_instructions += 1
            if count_instructions > limit_instructions:
                return False
        return True

    def process_command(self, command: int, args: List[int]):
        self.current_command_id += 1
        match command:
            case 0:
                self.registers[args[1]] = args[0]
            case 1:
                self.registers[args[1]] = self.registers[args[0]]
            case 2:
                result = self.registers[args[0]] + self.registers[args[1]]
                result %= self.bit_size
                self.registers[args[2]] = result
            case 3:
                result = self.registers[args[0]] - self.registers[args[1]]
                result %= self.bit_size

                self.registers[args[2]] = result
            case 4:
                result = self.registers[args[0]] * self.registers[args[1]]
                result %= self.bit_size
                self.registers[args[2]] = result
            case 5:
                if self.registers[args[1]] == 0:
                    self.registers[args[2]] = 0
                else:
                    result = self.registers[args[0]] % self.registers[args[1]]
                    result %= self.bit_size
                    self.registers[args[2]] = result
            case 6:
                result = self.registers[args[0]] + 1
                result %= self.bit_size
                self.registers[args[0]] = result
            case 7:
                result = self.registers[args[0]] - 1
                result %= self.bit_size
                self.registers[args[0]] = result
            case 8:
                self.current_command_id = self.labels[args[0]]
                pass
            case 9:
                if self.registers[args[0]] == 0:
                    self.current_command_id = self.labels[args[1]]
            case 10:
                if self.registers[args[0]] != 0:
                    self.current_command_id = self.labels[args[1]]


@timer
def part1():
    instructions = parse_file()

    interpreter = Interpreter(16, 16, instructions)
    interpreter.process_commands()

    print(f"Value of r0: {interpreter.registers[0]}")


@timer
def part2():
    print(f"{tcolors.YELLOW}Warning!{tcolors.RESET} Part 2 might take over 40 seconds")
    instructions = parse_file()
    limit_instructions = 5000000

    count_limit_reached = 0
    for r0 in range(100):
        interpreter = Interpreter(16, 16, instructions)
        interpreter.set_register_value(0, r0)

        if not interpreter.process_commands(limit_instructions):
            count_limit_reached += 1

    print(f"Reached {limit_instructions} instructions: {count_limit_reached}")


@timer
def part3():
    # TODO: Implement part 3
    lines = parse_file()
    pass


def parse_file() -> List[str]:
    file_name = "input_sample.txt" if TEST_DATA else "input.txt"
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    instructions = []
    with open(abs_file_path, "r") as f:
        for line in f:
            instructions.append(line.strip())
    return instructions


part1()
part2()
part3()
