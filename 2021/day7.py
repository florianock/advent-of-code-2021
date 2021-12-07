#!/usr/bin/env python3

from aocd import data, submit


def main():
    ex1 = solve(example)
    assert ex1 == 37, f"expected 37 but got {ex1}"
    print(solve(data))
    ex2 = solve2(example)
    assert ex2 == 168, f"expected 168 but got {ex2}"
    print(solve2(data))


def solve(inputs: str) -> int:
    costs: list[int] = []
    nums = [int(x) for x in inputs.split(',')]
    for i in range(min(nums), max(nums)+1):
        cost = [abs(x-i) for x in nums]
        costs.append(sum(cost))
    return min(costs)


def solve2(inputs: str) -> int:
    costs: list[int] = []
    nums = [int(x) for x in inputs.split(',')]
    for i in range(min(nums), max(nums)+1):
        cost = [get_cost(x, i) for x in nums]
        costs.append(sum(cost))
    return min(costs)


def get_cost(pos, target) -> int:
    distance = abs(pos-target)
    return distance * (distance + 1) // 2


example = """
16,1,2,0,4,2,7,1,2,14
""".strip()


if __name__ == "__main__":
    main()
