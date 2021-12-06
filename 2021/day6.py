#!/usr/bin/env python3
from functools import reduce


def main(file):
    inputs = read_input(file)
    assert count_after_days(example, 18) == 26
    assert count_after_days(example, 80) == 5934
    print(count_after_days(inputs, 80))
    assert count_after_days(example, 256) == 26984457539
    print(count_after_days(inputs, 256))


def count_after_days(inputs: str, days: int) -> int:
    initial = get_initial_fish_counts(inputs)
    final_count = reduce(tick, range(days), initial)
    return sum(final_count)


def tick(counts: list[int], _: int) -> list[int]:
    result = counts[1:] + counts[0:1]
    result[6] += counts[0]
    return result


def get_initial_fish_counts(inputs: str) -> list[int]:
    initial_counts = [0] * 9
    fish = [int(x) for x in inputs.split(',')]
    for f in fish:
        initial_counts[f] += 1
    return initial_counts


def read_input(filename):
    with open(filename) as f:
        contents = f.read().strip()
        return contents


example = """
3,4,3,1,2
""".strip()

if __name__ == "__main__":
    main('day-6-input.txt')
