import os
import re
from typing import List
from dataclasses import dataclass

from utils.timer import timer

"""
Preprocessing:
- Read the input file into a list of raw password strings.
- Each part has two implementations, a plain loop version and a regex version. Regex turned out
  to be the faster of the two in every part, which is why both stuck around.

Part 1:
- The trick is that we don't care how many lowercase letters, uppercase letters, or digits a
  password has, only whether each category shows up at all, so a single pass with three boolean
  flags is enough.
- Loop version:
  - Walk the password once, flipping the matching flag the first time we see a
    lowercase letter, an uppercase letter, or a digit, then multiply the password's length by
    however many flags ended up true.
- Regex version:
  - Same idea, but instead of flipping flags char by char, we ask three regexes
    ([a-z], [A-Z], \\d) whether they match anywhere in the password.
- We keep the highest score (and its password) seen across the whole list.

Part 2:
- Same three-category score from part 1, now stacked with three more rules, so the loop version
  tracks all six pieces of state (lower, upper, a non-7 digit, a lone-7 bonus, the longest run,
  and whether a color word showed up) in one `Score` object built while scanning the password a
  single time.
- Loop version:
  - The consecutive-run bonus is just a running streak counter: while the current char matches the
    last one, extend the streak; otherwise reset it to the current char, remembering the longest
    streak seen once it reaches at least 3.
  - The color check is the one non-obvious part: instead of searching for "red", "green", or "blue"
    as substrings after the fact, we keep one index per color word and, for each character, advance
    that word's index if it matches the next expected letter, or reset it to 0 if it doesn't - so by
    the time we reach the end of the password, an index that hit the word's full length means we saw
    it somewhere along the way. It's a simplified single-pass string search instead of repeated
    substring scanning.
- Regex version:
  - Keeps the streak logic for the consecutive-run bonus (regex isn't a natural
    fit for "longest run of the same char"), but swaps the category and color checks for direct
    pattern matches ([a-z], [A-Z], \\d, red|green|blue), plus one regex for "contains a 7 and no
    other digit".
- Same as part 1: multiply by password length at the end, and keep the highest score.

Part 3:
- Same scoring as part 2, but wrapped in an outer loop over every candidate character (a-z, A-Z,
  0-9) that could be appended.
- For each candidate, we append it to every password, rescore all of them with part 2's logic,
  and sum the scores, then keep whichever candidate produced the largest total.
- This part is straightforwardly brute force: 62 candidates times the whole password list, but
  the scoring itself is still a single pass per password, so it stays cheap.
"""


@dataclass
class Score:
    lower: bool
    upper: bool
    digit_non_seven: bool
    seven: bool
    sequence: int
    color: bool


@timer
def part1(regex: bool = False):
    if regex:
        print("Regex version")
    else:
        print("Loop version")

    passwords = parse_file("input.txt")

    strongest_score = 0
    strongest_password = ""
    for password in passwords:
        if regex:
            strength = password_strength_1_regex(password)
        else:
            strength = password_strength_1(password)

        if strength > strongest_score:
            strongest_score = strength
            strongest_password = password

    print(f"Strongest password: {strongest_password}")


@timer
def part2(regex: bool = False):
    if regex:
        print("Regex version")
    else:
        print("Loop version")

    passwords = parse_file("input.txt")

    strongest_score = 0
    strongest_password = ""
    for password in passwords:
        if regex:
            strength = password_stength_regex(password)
        else:
            strength = password_stength(password)

        if strength > strongest_score:
            strongest_score = strength
            strongest_password = password

    print(f"Strongest password: {strongest_password}")


@timer
def part3(regex: bool = False):
    if regex:
        print("Regex version")
    else:
        print("Loop version")

    passwords = parse_file("input.txt")
    highest_strength = 0

    lowers = [chr(i) for i in range(97, 123)]
    uppers = [chr(i) for i in range(65, 91)]
    nums = [str(i) for i in range(10)]
    for new_char in lowers + uppers + nums:
        sum_strenghts = 0
        for password in passwords:
            password += new_char

            if regex:
                strength_score_loop = password_stength_regex(password)
            else:
                strength_score_loop = password_stength(password)

            sum_strenghts += strength_score_loop

        if sum_strenghts > highest_strength:
            highest_strength = sum_strenghts

    print(f"Highest strength: {highest_strength}")


def password_strength_1(password: str) -> int:
    # Lower, Upper, Digit
    characters = [False, False, False]

    for char in password:
        if not characters[0]:
            characters[0] = char.islower()
        elif not characters[1]:
            characters[1] = char.isupper()
        elif not characters[2]:
            characters[2] = char.isdigit()

    return len(password) * sum(characters)


def password_strength_1_regex(password: str) -> int:
    score = 0

    if re.search(r"[a-z]", password):
        score += 1
    if re.search(r"[A-Z]", password):
        score += 1
    if re.search(r"\d", password):
        score += 1

    return len(password) * score


def password_stength(password: str) -> int:
    colors = ["red", "green", "blue"]
    score = Score(False, False, False, False, 0, False)
    sequence = ""
    color_index = [0, 0, 0]

    for char in password:
        if char.islower():
            score.lower = True
        elif char.isupper():
            score.upper = True
        elif char.isdigit():
            if char == "7":
                score.seven = True
            else:
                score.digit_non_seven = True

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

    strength_score = (
        score.lower + score.upper + score.digit_non_seven + score.sequence**2
    )
    if score.seven and not score.digit_non_seven:
        strength_score += 1
        strength_score += 7
    if score.color:
        strength_score *= 3

    return len(password) * strength_score


def password_stength_regex(password: str) -> int:
    score = 0

    if re.search(r"[a-z]", password):
        score += 1
    if re.search(r"[A-Z]", password):
        score += 1
    if re.search(r"\d", password):
        score += 1
    if re.search(r"7", password) and not re.search(r"[012345689]", password):
        score += 7

    max_sequence, sequence = 0, ""
    for char in password:
        if len(sequence) > 0 and sequence[-1] == char:
            sequence += char
            if max_sequence < len(sequence) >= 3:
                max_sequence = len(sequence)
        else:
            sequence = char

    score += max_sequence**2

    if re.search(r"red|green|blue", password):
        score *= 3

    return len(password) * score


def parse_file(file_name: str) -> List[str]:
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    passwords = []
    with open(abs_file_path, "r") as f:
        for line in f:
            passwords.append(line.strip())
    return passwords


part1()
part1(True)
part2()
part2(True)
part3()
part3(True)
