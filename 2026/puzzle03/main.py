import os
from typing import List
from dataclasses import dataclass

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


@dataclass
class Score:
    lower: bool
    upper: bool
    digit: bool
    seven: bool
    sequence: int
    color: bool


@timer
def part1():
    passwords = parse_file("input.txt")

    strongest_score = 0
    strongest_password = ""
    for password in passwords:
        # Lower, Upper, Digit
        characters = [False, False, False]

        for char in password:
            if not characters[0]:
                characters[0] = char.islower()
            elif not characters[1]:
                characters[1] = char.isupper()
            elif not characters[2]:
                characters[2] = char.isdigit()

        strength = len(password) * sum(characters)

        if strength > strongest_score:
            strongest_score = strength
            strongest_password = password

    print(f"Strongest password: {strongest_password}")


@timer
def part2():
    passwords = parse_file("input.txt")

    strongest_score = 0
    strongest_password = ""
    colors = ["red", "green", "blue"]
    for password in passwords:
        score = Score(False, False, False, False, 0, False)
        sequence = ""
        color_index = [0, 0, 0]

        for char in password:
            if char.islower():
                score.lower = True
            elif char.isupper():
                score.upper = True
            elif char.isdigit() and char != "7":
                score.digit = True
            elif not score.digit and char == "7":
                score.seven = True

            if len(sequence) > 0 and sequence[-1] == char:
                sequence += char
                if score.sequence < len(sequence) >= 3:
                    score.sequence = len(sequence)
            else:
                sequence = char

            if not score.color:
                for i in range(3):
                    if char == colors[i][color_index[i]]:
                        color_index[i] += 1
                        if color_index[i] == len(colors[i]):
                            score.color = True
                    else:
                        color_index[i] = 0

        strength_score = score.lower + score.upper + score.digit + score.sequence**2
        if score.seven:
            strength_score += 7
        if score.color:
            strength_score *= 3

        strength = len(password) * strength_score

        if strength > strongest_score:
            strongest_score = strength
            strongest_password = password

    print(f"Strongest password: {strongest_password}")


@timer
def part3():
    # TODO: Implement part 3
    passwords = parse_file("input_sample.txt")
    highest_strength = 0

    lowers = [chr(i) for i in range(97, 123)]
    uppers = [chr(i) for i in range(65, 91)]
    nums = [str(i) for i in range(10)]
    # for new_char in lowers + uppers + nums:
    for new_char in ["7"]:
        sum_strenghts = 0
        colors = ["red", "green", "blue"]
        for password in passwords:
            score = Score(False, False, False, False, 0, False)
            sequence = ""
            color_index = [0, 0, 0]
            password += new_char

            for char in password:
                if char.islower():
                    score.lower = True
                elif char.isupper():
                    score.upper = True
                elif char.isdigit() and char != "7":
                    score.digit = True
                elif not score.digit and char == "7":
                    score.digit = True
                    score.seven = True

                if len(sequence) > 0 and sequence[-1] == char:
                    sequence += char
                    if score.sequence < len(sequence) >= 3:
                        score.sequence = len(sequence)
                else:
                    sequence = char

                if not score.color:
                    for i in range(3):
                        if char == colors[i][color_index[i]]:
                            color_index[i] += 1
                            if color_index[i] == len(colors[i]):
                                score.color = True
                        else:
                            color_index[i] = 0

            strength_score = score.lower + score.upper + score.digit + score.sequence**2
            if score.seven:
                strength_score += 7
            if score.color:
                strength_score *= 3

            sum_strenghts += len(password) * strength_score
            print(password)
            print(f"Strength: {strength_score}")
            print(f"  Length: {len(password)}")
            print(f"   Score: {len(password) * strength_score}")
            print(f"   Score: {score}")
            print()

        if sum_strenghts > highest_strength:
            highest_strength = sum_strenghts
            print(highest_strength, new_char)

    print(f"Highest strength: {highest_strength}")


def parse_file(file_name: str) -> List[str]:
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    passwords = []
    with open(abs_file_path, "r") as f:
        for line in f:
            passwords.append(line.strip())
    return passwords


part1()
part2()
part3()
