#!/usr/bin/env python3

from collections import Counter
import itertools

# --- Day 5: Hydrothermal Venture ---


flatten = itertools.chain.from_iterable

Point = (int, int)
Line = list[Point]


def main(file):
    inputs = read_input(file)
    assert count_overlaps(example) == 5
    print(count_overlaps(inputs))
    assert count_overlaps(example, True) == 12
    print(count_overlaps(inputs, True))


def count_overlaps(inputs: str, with_diagonals: bool = False) -> int:
    lines = process_inputs(inputs)
    if not with_diagonals:
        lines = [x for x in lines if not is_diagonal(x)]
    complete = complete_lines(lines)
    return len(find_overlaps(complete))


def process_inputs(inputs: str) -> list[Line]:
    processed = [x.split(' -> ') for x in inputs.split('\n')]
    return list(map(convert_to_line, processed))


def convert_to_line(line: list[str]) -> Line:
    return list(map(convert_to_point, line))


def convert_to_point(point: str) -> Point:
    parts = point.split(',')
    return int(parts[0]), int(parts[1])


def is_diagonal(line: Line) -> bool:
    assert len(line) == 2
    return line[0][0] != line[1][0] and line[0][1] != line[1][1]


def complete_lines(lines: list[Line]) -> list[Line]:
    return list(map(complete_line, lines))


def complete_line(line: Line) -> Line:
    xs = get_range(line[0][0], line[1][0])
    ys = get_range(line[0][1], line[1][1])
    if len(xs) == 1:
        xs *= len(ys)
    elif len(ys) == 1:
        ys *= len(xs)
    return list(zip(xs, ys))


def get_range(a: int, b: int) -> list[int]:
    if a == b:
        return [a]
    if a < b:
        return list(range(a, b+1))
    if a > b:
        return list(range(a, b-1, -1))


def find_overlaps(lines: list[Line]) -> set[Point]:
    points = list(flatten(lines))
    return {point for (point, count) in Counter(points).items() if count > 1}


def read_input(filename):
    with open(filename) as f:
        contents = f.read().strip()
        return contents


example = """
0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
""".strip()


if __name__ == "__main__":
    main('day-5-input.txt')
