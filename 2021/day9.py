#!/usr/bin/env python3
import itertools
import operator
from functools import reduce

# noinspection PyUnresolvedReferences
from aocd import data, submit
from collections import Counter, namedtuple

flatten = itertools.chain.from_iterable

Point = namedtuple("Point", ["row", "col", "height"])
Row = list[Point]
Col = list[Point]
Basin = set[Point]
Floor = set[Point]


def main():
    ex1 = solve1(example)
    assert ex1 == 15, f"expected 15, but got {ex1}"
    answer1 = solve1(data)
    assert answer1 == 530, f"expected 530, but got {answer1}"
    ex2 = solve2(example)
    assert ex2 == 1134, f"expected 1134, but got {ex2}"
    answer2 = solve2(data)
    assert answer2 == 1019494, f"expected 1019494, but got {answer2}"


def process_inputs(inputs: str) -> Floor:
    rows_of_ints = [[int(y) for y in x] for x in inputs.split('\n')]
    output = set()
    for i, row in enumerate(rows_of_ints):
        for j, height in enumerate(row):
            output.add(Point(i, j, height))
    return output


def solve1(inputs: str) -> int:
    cave_floor = process_inputs(inputs)
    low_points = find_low_points(cave_floor)
    risk_level = reduce(operator.add, [p.height for p in low_points], len(low_points))
    return risk_level


def solve2(inputs: str) -> int:
    cave_floor = process_inputs(inputs)
    low_points = find_low_points(cave_floor)
    max_height = max({p.height for p in cave_floor})
    high_points = {high for high in cave_floor if high.height == max_height}
    valid_points = cave_floor - high_points
    basins = [find_basin(valid_points, x) for x in low_points]
    basins.sort(key=lambda x: len(x), reverse=True)
    return reduce(operator.mul, [len(b) for b in basins[0:3]], 1)


def find_basin(search_space: set[Point], point: Point) -> Basin:
    todo = {point}
    processed = set()
    print("finding basin...")
    while todo - processed:
        unknown = todo - processed
        p = unknown.pop()
        neighbors = get_neighbors(p, search_space)
        todo.update(neighbors)
        processed.add(p)
    return processed


def find_low_points(cave_floor: Floor) -> set[Point]:
    low_points = set()
    print("finding low points...")
    for point in cave_floor:
        neighbors = get_neighbors(point, cave_floor)
        if is_low_point(point, neighbors):
            low_points.add(point)
    return low_points


def is_low_point(point: Point, neighbors: set[Point]) -> bool:
    return all(map(lambda x: point.height < x.height, neighbors))


def get_neighbors(point: Point, cave_floor: Floor) -> set[Point]:
    return {p for
            p in cave_floor
            if (p.row == point.row and (p.col == point.col - 1 or p.col == point.col + 1))
            or (p.col == point.col and (p.row == point.row - 1 or p.row == point.row + 1))}


example = """
2199943210
3987894921
9856789892
8767896789
9899965678
""".strip()

if __name__ == "__main__":
    main()
