#!/usr/bin/env python3
# noinspection PyUnresolvedReferences
from aocd import data, submit
from collections import Counter
from itertools import pairwise

# --- Day 14: Extended Polymerization ---

PolymerRules = dict[tuple[str, str], str]


def main():
    ex1 = solve(example, 10)
    assert ex1 == 1588, f"expected 1588, but got {ex1}"
    answer1 = solve(data, 10)
    assert answer1 == 3284, f"expected 3284, but got {answer1}"
    ex2 = solve(example, 40)
    assert ex2 == 2188189693529, f"expected 2188189693529, but got {ex2}"
    answer2 = solve(data, 40)
    assert answer2 == 4302675529689, f"expected 4302675529689, but got {answer2}"


def solve(inputs: str, steps: int) -> int:
    start_template, rules = read_inputs(inputs)
    pairs = Counter(pairwise(start_template))
    polymers = Counter(start_template)
    for i in range(1, steps+1):
        pairs, new_polymers = create_polymers(pairs, rules)
        polymers.update(new_polymers)
        display(polymers, i)
    return max(polymers.values()) - min(polymers.values())


def create_polymers(pairs: Counter, rules: PolymerRules) -> (Counter, Counter):
    new_pairs = Counter()
    polymers = Counter()
    for (p1, p2), count in pairs.items():
        polymer = rules[(p1, p2)]
        polymers[polymer] += count
        for pair in [(p1, polymer), (polymer, p2)]:
            new_pairs[pair] += count
    return new_pairs, polymers


def read_inputs(inputs: str) -> (str, PolymerRules):
    lines = inputs.split('\n')
    rules = {(a[0], a[1]): a[6] for a in lines[2:]}
    return lines[0], rules


def display(polymers: Counter, i):
    clear()
    print(f"Step {i}")
    print(f"Total: {sum(polymers.values())}")
    print(f"Size: {sum(polymers.values()) // 1000000000000} TB\n")
    for polymer, count in polymers.items():
        print(f"{polymer}: {count}")
    print('\n')


def clear():
    from time import sleep
    import os
    sleep(0.05)
    os.system('cls' if os.name == 'nt' else 'clear')


example = """
NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C
""".strip()

if __name__ == "__main__":
    main()
