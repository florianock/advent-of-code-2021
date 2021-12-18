#!/usr/bin/env python3
import re
from aocd import data, submit

# --- Day 17: Trick Shot ---


def main():
    ex1, ex2 = solve(example)
    assert ex1 == 45, f"expected 45, but got {ex1}"
    assert ex2 == 112, f"expected 112, but got {ex2}"
    answer1, answer2 = solve(data)
    assert answer1 == 5460, f"expected 5460, but got {answer1}"
    assert answer1 == 3618, f"expected 3618, but got {answer2}"


def solve(inputs: str) -> (int, int):
    bounds = [int(s) for s in re.findall(r'-?\d+', inputs)]
    highest_y = 0
    best_trajectory = None
    success_velocities = []
    for x in range(-300, 300):
        for y in range(-300, 300):
            trajectory, target_hit = fire(x, y, bounds)
            if target_hit:
                success_velocities.append((x, y))
                if max([y for _, y in trajectory]) > highest_y:
                    highest_y = max([y for _, y in trajectory])
                    best_trajectory = trajectory
                    display(best_trajectory, bounds)
    return highest_y, len(success_velocities)


def fire(x, y, target_bounds) -> (list[(int, int)], bool):
    trajectory = [(0, 0)]
    while trajectory[-1][0] < target_bounds[1] and target_bounds[2] < trajectory[-1][1]:
        current_pos = trajectory[-1]
        next_pos = (current_pos[0] + x, current_pos[1] + y)
        if x > 0:
            x -= 1
        elif x < 0:
            x += 1
        y -= 1
        trajectory.append(next_pos)
        if hit_target(*next_pos, target_bounds):
            return trajectory, True
    return trajectory, False


def calculate_point_with_drag(x: int, drag: int) -> int:
    match x:
        case 0: return 0
        case x if x > 0: return x - drag
        case x if x < 0: return x + drag


def hit_target(x: int, y: int, bounds: list[int]) -> bool:
    return bounds[0] <= x <= bounds[1] and bounds[2] <= y <= bounds[3]


def display(trajectory: list[tuple[int, int]], target_bounds):
    clear()
    points = [(target_bounds[0], target_bounds[2]), (target_bounds[1], target_bounds[3])]
    grid = Grid(trajectory + points + [(0, 0)])
    # submarine
    grid.draw((0, 0), "S")
    # target
    for x in range(target_bounds[0], target_bounds[1] + 1):
        for y in range(target_bounds[2], target_bounds[3] + 1):
            grid.draw((x, y), "T")
    # trajectory
    for x, y in trajectory:
        if (x, y) != (0, 0):
            grid.draw((x, y), "*")
    # print the grid
    grid.print()


def clear():
    from time import sleep
    import os
    sleep(0.05)
    os.system('cls' if os.name == 'nt' else 'clear')


class Grid:
    y_0 = 0
    min_y = 0
    max_y = 0
    min_x = 0
    max_x = 0

    def __init__(self, points: [(int, int)]):
        xs = [x for x, _ in points]
        ys = [y for _, y in points]
        self.min_y, self.max_y = min(ys), max(ys)
        self.min_x, self.max_x = min(xs), max(xs)
        # print("grid ", self.min_x, self.max_x, self.min_y, self.max_y)
        self.grid = [['~' if y == self.max_y else "." for x in range(self.min_x, self.max_x + 1)]
                     for y in range(abs(self.min_y) + self.max_y + 1)]

    def draw(self, point: (int, int), char: str):
        calculated_y = abs(self.max_y) - point[1]
        self.grid[calculated_y][point[0]] = char

    def print(self):
        for row in self.grid:
            print("".join(row))


example = """
target area: x=20..30, y=-10..-5
""".strip()

if __name__ == "__main__":
    main()
