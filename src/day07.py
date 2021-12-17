#!/usr/bin/env python3
from functools import reduce
from aocd import data, submit

# --- Day 7: The Treachery of Whales ---


def main():
    inputs = [int(x) for x in data.split(',')]
    ex = [int(x) for x in example.split(',')]
    ex1 = solve(ex)
    assert ex1 == 37, f"expected 37 but got {ex1}"
    ex2 = solve2(ex)
    assert ex2 == 168, f"expected 168 but got {ex2}"
    print(solve(inputs))
    print(solve2(inputs))


def solve(nums: list[int]) -> int:
    costs: list[int] = []
    for i in range(min(nums), max(nums)+1):
        cost = [abs(x-i) for x in nums]
        costs.append(sum(cost))
    return min(costs)


def solve2(nums: list[int]) -> int:
    costs: list[int] = []
    for position in range(min(nums), max(nums)+1):
        func = get_cost_function(position)
        c = reduce(func, nums, 0)
        costs.append(c)
    return min(costs)


def get_cost_function(pos: int):
    def q(current: int, num: int) -> int:
        distance = abs(num - pos)
        return current + (distance * (distance + 1) // 2)
    return q


example = """
16,1,2,0,4,2,7,1,2,14
""".strip()


if __name__ == "__main__":
    main()
