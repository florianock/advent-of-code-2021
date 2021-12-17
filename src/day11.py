#!/usr/bin/env python3
# noinspection PyUnresolvedReferences
from aocd import data, submit

# --- Day 11: Dumbo Octopus ---


Group = list[list[int]]
Neighborhood = set[(int, int)]


def main():
    ex1, ex2 = solve(example)
    assert ex1 == 1656, f"expected 1656, but got {ex1}"
    assert ex2 == 195, f"expected 195, but got {ex2}"
    answer1, answer2 = solve(data)
    assert answer1 == 1661, f"expected 1661, but got {answer1}"
    assert answer2 == 334, f"expected 334, but got {answer2}"


def solve(inputs: str) -> (int, int):
    max_days = 500
    group = [[int(x) for x in row] for row in inputs.split('\n')]
    answer1 = answer2 = 0
    for day in range(1, max_days+1):
        group = tick(group)
        display(group, day)
        flash_count = sum([sum([1 for x in row if x == 0]) for row in group])
        if day < 101:
            answer1 += flash_count
        if flash_count == len(group) * len(group[0]) and not answer2:
            answer2 = day
        if answer2 and day >= 101:
            break
    return answer1, answer2


def tick(group: Group) -> Group:
    next_group = [[x for x in row] for row in group]  # tick must be a pure function
    affected = []
    for r, row in enumerate(next_group):
        for c, _ in enumerate(row):
            affected.extend(update_octopus(r, c, next_group))
    while affected:
        row, col = affected.pop()
        if next_group[row][col] == 0:
            continue
        affected.extend(update_octopus(row, col, next_group))
    return next_group


def update_octopus(row: int, col: int, group: Group) -> Neighborhood:
    if group[row][col] == 9:
        group[row][col] = 0
        return get_neighbors(row, col, group)
    else:
        group[row][col] += 1
        return set()


def get_neighbors(r: int, c: int, group: Group) -> Neighborhood:
    num_rows = len(group)
    num_cols = len(group[0])
    neighbors = [
        (r-1, c-1), (r-1, c), (r-1, c+1),
        (r,   c-1),           (r,   c+1),
        (r+1, c-1), (r+1, c), (r+1, c+1)
    ]
    return {(n, m) for n, m in neighbors if 0 <= n < num_rows and 0 <= m < num_cols}


def display(group: Group, day: int):
    output = []
    for row in group:
        output.append("".join(["\u2588\u2588" if x == 0 else "  " for x in row]))
    clear()
    print("\n".join(output) + "\n\nDay: " + str(day))


def clear():
    from time import sleep
    import os
    sleep(0.05)
    os.system('cls' if os.name == 'nt' else 'clear')


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
