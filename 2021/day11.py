#!/usr/bin/env python3
# noinspection PyUnresolvedReferences
from aocd import data, submit
from typing import Deque


def main():
    ex1 = solve1(example)
    assert ex1 == 1656, f"expected 1656, but got {ex1}"
    answer1 = solve1(data)
    assert answer1 == 1661, f"expected 1661, but got {answer1}"
    ex2 = solve2(example)
    assert ex2 == 195, f"expected 195, but got {ex2}"
    answer2 = solve2(data)
    assert answer2 == 334, f"expected 334, but got {answer2}"


def solve1(inputs: str) -> int:
    group = [[int(x) for x in row] for row in inputs.split('\n')]
    num_rows = len(group)
    num_cols = len(group[0])
    queue = Deque[tuple[int, int]]()
    flash_count = 0
    for day in range(100):
        day_flash_count = 0
        for r, row in enumerate(group):
            for c, _ in enumerate(row):
                group[r][c] += 1
                if group[r][c] == 10:
                    queue.extend(get_neighbors(r, c, num_rows, num_cols))
        while queue:
            row, col = queue.pop()
            group[row][col] += 1
            if group[row][col] == 10:
                queue.extend(get_neighbors(row, col, num_rows, num_cols))
        for r, row in enumerate(group):
            for c, octopus in enumerate(row):
                if octopus > 9:
                    group[r][c] = 0
                    day_flash_count += 1
        flash_count += day_flash_count
    return flash_count


def solve2(inputs: str) -> int:
    group = [[int(x) for x in row] for row in inputs.split('\n')]
    num_rows = len(group)
    num_cols = len(group[0])
    queue = Deque[tuple[int, int]]()
    for day in range(1000):
        day_flash_count = 0
        for r, row in enumerate(group):
            for c, _ in enumerate(row):
                group[r][c] += 1
                if group[r][c] == 10:
                    queue.extend(get_neighbors(r, c, num_rows, num_cols))
        while queue:
            row, col = queue.pop()
            group[row][col] += 1
            if group[row][col] == 10:
                queue.extend(get_neighbors(row, col, num_rows, num_cols))
        for r, row in enumerate(group):
            for c, octopus in enumerate(row):
                if octopus > 9:
                    group[r][c] = 0
                    day_flash_count += 1
        if day_flash_count == num_rows * num_cols:
            return day + 1
    return -1


def get_neighbors(r: int, c: int, num_rows: int, num_cols: int) -> list[(int, int)]:
    neighbors = [
        (r-1, c-1), (r-1, c), (r-1, c+1),
        (r,   c-1),           (r,   c+1),
        (r+1, c-1), (r+1, c), (r+1, c+1)
    ]
    return [(r, c) for r, c in neighbors if 0 <= r < num_rows and 0 <= c < num_cols]


example = """
5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526
""".strip()

if __name__ == "__main__":
    main()
