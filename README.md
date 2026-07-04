# 🔀 Flip Flop Codes

[![Dashboard](https://img.shields.io/badge/Dashboard-coding--challenges-blue?style=for-the-badge)](https://github.com/LorranSutter/coding-challenges) <!-- BADGE:START -->[![Solved Challenges](https://img.shields.io/badge/Solved%20Challenges-16-brightgreen?style=for-the-badge&logo=python&logoColor=white)](https://flipflop.slome.org/)<!-- BADGE:END -->

This repository contains my solutions for [Flip Flop Codes](https://flipflop.slome.org/).

Flip Flop Codes is a coding puzzle series, with each puzzle split into three parts of increasing difficulty.

<!-- SUMMARY:START -->
## 📊 Progress

> **Overall: 16/21 parts solved (76%)**

### [2025](./2025/)

`████████████████░░░░░` **16/21** parts solved (76%)

<!-- SUMMARY:END -->

## 🛠️ Setup

### Creating a Virtual Environment

```bash
python3 -m venv .venv
```

### Activating the Virtual Environment

On macOS/Linux:

```bash
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

### Installing Dependencies

```bash
pip install -r requirements.txt
```

Deactivating the Virtual Environment

```bash
deactivate
```

## ✨ Creating a New Puzzle

To create a new puzzle structure, use the `new_puzzle.sh` script:

```bash
./new_puzzle.sh <year> <puzzle>
```

Example:
```bash
./new_puzzle.sh 2025 1
```

This will create:
- A folder structure: `2025/puzzle01/`
- `main.py` with a template for part 1, part 2 and part 3
- `input.txt` for the puzzle input
- `input_sample.txt` for sample/test input

## 🚀 Running Solutions

You can run the solutions:

```bash
python3 -m 2025.puzzle01.main
```

Replace `2025` with the desired year and `puzzle01` with the specific puzzle you want to run.

## 🔄 Updating Progress Summary

To update the progress summary in this README after solving new parts, run the `generate_readme.py` script:

```bash
python3 generate_readme.py
```
