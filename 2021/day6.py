#!/usr/bin/env python3

def main(file):
    inputs = read_input(file)
    assert count_after_days(example, 18) == 26
    assert count_after_days(example, 80) == 5934
    print(count_after_days(inputs, 80))
    assert count_after_days(example, 256) == 26984457539
    print(count_after_days(inputs, 256))


def count_after_days(inputs: str, days: int) -> int:
    counts = get_initial_fish_counts(inputs)
    for _ in range(days):
        new_counts = counts[1:] + counts[0:1]
        new_counts[6] += counts[0]
        counts = new_counts
    return sum(counts)


def get_initial_fish_counts(inputs: str) -> list[int]:
    initial_counts = [0, 0, 0, 0, 0, 0, 0, 0, 0]
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
