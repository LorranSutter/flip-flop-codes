#!/bin/bash

# Check if arguments are provided
if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Usage: $0 <year> <puzzle>"
    echo "Example: $0 2025 1"
    exit 1
fi

# Validate inputs are numbers
if ! [[ "$1" =~ ^[0-9]+$ ]] || ! [[ "$2" =~ ^[0-9]+$ ]]; then
    echo "Error: Both year and puzzle must be numbers"
    exit 1
fi

year="$1"
# Format puzzle with leading zero (2 digits)
puzzle=$(printf "%02d" "$2")
folder_name="${year}/puzzle${puzzle}"

# Create year folder if it doesn't exist
if [ ! -d "$year" ]; then
    mkdir "$year"
    echo "Created folder: $year"
fi

# Check if puzzle folder already exists
if [ -d "$folder_name" ]; then
    echo "Error: Folder $folder_name already exists"
    exit 1
fi

# Create puzzle folder
mkdir "$folder_name"
echo "Created folder: $folder_name"

# Create main.py file
cat > "$folder_name/main.py" << 'EOF'
import argparse
import os
from typing import List

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
    # TODO: Implement part 1
    lines = parse_file()
    pass


@timer
def part2():
    # TODO: Implement part 2
    lines = parse_file()
    pass


@timer
def part3():
    # TODO: Implement part 3
    lines = parse_file()
    pass


def parse_file() -> List[str]:
    file_name = "input_sample.txt" if TEST_DATA else "input.txt"
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    lines = []
    with open(abs_file_path, "r") as f:
        for line in f:
            lines.append(line.strip())
    return lines


# part1()
# part2()
# part3()
EOF

echo "Created file: $folder_name/main.py"

# Create input.txt file
touch "$folder_name/input.txt"
echo "Created file: $folder_name/input.txt"

# Create input_sample.txt file
touch "$folder_name/input_sample.txt"
echo "Created file: $folder_name/input_sample.txt"

echo "Done!"
