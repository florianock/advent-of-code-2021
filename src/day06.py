#!/usr/bin/env python3
from functools import reduce

# --- Day 6: Lanternfish ---


def main(file):
    inputs = read_input(file)
    assert count_after_days(example, 18) == 26
    assert count_after_days(example, 80) == 5934
    print(count_after_days(inputs, 80))
    assert count_after_days(example, 256) == 26984457539
    print(count_after_days(inputs, 256))


def count_after_days(inputs: str, days: int) -> int:
    fish = [int(x) for x in inputs.split(',')]
    start = reduce(tally, fish, [0] * 9)
    final = count_down(start, days)
    return sum(final)


def tally(counts: list[int], item: int) -> list[int]:
    counts[item] += 1
    return counts


def count_down(counts: list[int], days: int) -> list[int]:
    new_counts = counts[1:] + counts[0:1]
    new_counts[6] += counts[0]
    if days > 1:
        return count_down(new_counts, days - 1)
    else:
        return new_counts


def read_input(filename):
    with open(filename) as f:
        return f.read().strip()


example = """
3,4,3,1,2
""".strip()


if __name__ == "__main__":
    main('day-6-input.txt')
