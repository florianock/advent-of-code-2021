#!/usr/bin/env python3
# noinspection PyUnresolvedReferences
from aocd import data, submit
from collections import namedtuple
import itertools
import operator
from functools import reduce

flatten = itertools.chain.from_iterable

Point = namedtuple("Point", ["row", "col", "height"])
Row = list[Point]
Basin = set[Point]
Floor = list[Row]


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
    output = Floor()
    for i, row in enumerate(rows_of_ints):
        points_row = Row()
        for j, height in enumerate(row):
            points_row.append(Point(i, j, height))
        output.append(points_row)
    display(output)
    return output


def solve1(inputs: str) -> int:
    cave_floor = process_inputs(inputs)
    low_points = find_low_points(cave_floor)
    risk_level = reduce(operator.add, [p.height for p in low_points], len(low_points))
    return risk_level


def solve2(inputs: str) -> int:
    cave_floor = process_inputs(inputs)
    basins = find_basins(cave_floor)
    basins.sort(key=lambda x: len(x), reverse=True)
    return reduce(operator.mul, [len(b) for b in basins[0:3]], 1)


def find_basins(cave_floor: Floor) -> list[Basin]:
    low_points = find_low_points(cave_floor)
    high_points = find_high_points(cave_floor)
    basin_points = set(flatten(cave_floor)) - high_points
    basins = [find_basin(basin_points, x, cave_floor) for x in low_points]
    return basins


def find_low_points(cave_floor: Floor) -> set[Point]:
    low_points = set()
    for row in cave_floor:
        for point in row:
            neighbors = get_neighbors(point, cave_floor)
            if is_low_point(point, neighbors):
                low_points.add(point)
                # print(point)
    return low_points


def find_high_points(cave_floor: Floor) -> set[Point]:
    max_height = max({p.height for p in flatten(cave_floor)})
    return {p for p in flatten(cave_floor) if p.height == max_height}


def find_basin(basin_points: set[Point], point: Point, cave_floor: Floor) -> Basin:
    unexplored, explored = {point}, Basin()
    while unexplored - explored:
        p = (unexplored - explored).pop()
        neighbors = {n for n in get_neighbors(p, cave_floor) if n in basin_points}
        unexplored.update({n for n in neighbors if n not in explored})
        explored.add(p)
    # print(explored)
    return explored


def is_low_point(point: Point, neighbors: iter) -> bool:
    return all(map(lambda x: point.height < x.height, neighbors))


def get_neighbors(point: Point, cave_floor: Floor) -> set[Point]:
    max_row = len(cave_floor)
    max_col = len(cave_floor[0])
    neighbors = [(point.row - 1, point.col), (point.row + 1, point.col),
                 (point.row, point.col - 1), (point.row, point.col + 1)]
    return {cave_floor[r][c]
            for r, c in neighbors
            if 0 <= r < max_row and 0 <= c < max_col}


def display(cave_floor: Floor):
    rows, cols = len(cave_floor), len(cave_floor[0])
    canvas = [['.' for i in range(cols)] for j in range(rows)]
    for row in cave_floor:
        for point in row:
            canvas[point.row][point.col] = draw(point.height)
    for line in canvas:
        print("".join(line))


def draw(i: int) -> str:
    max_input = 10
    assert 0 <= i < max_input
    grayscale = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'."
    idx = round(i * len(grayscale) / max_input) + (len(grayscale) // max_input)
    return grayscale[idx]*2


example = """
2199943210
3987894921
9856789892
8767896789
9899965678
""".strip()


if __name__ == "__main__":
    main()
