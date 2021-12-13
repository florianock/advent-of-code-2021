#!/usr/bin/env python3
# noinspection PyUnresolvedReferences
from collections import defaultdict

from aocd import data, submit


def main():
    ex1a = len(get_paths(example1))
    assert ex1a == 10, f"expected 10, but got {ex1a}"
    ex2a = len(get_paths(example2))
    assert ex2a == 19, f"expected 19, but got {ex2a}"
    ex3a = len(get_paths(example3))
    assert ex3a == 226, f"expected 226, but got {ex3a}"
    answer1 = len(get_paths(data))
    assert answer1 == 3298, f"expected 3298, but got {answer1}"
    ex1b = len(get_paths(example1, True))
    assert ex1b == 36, f"expected 36, but got {ex1b}"
    ex2b = len(get_paths(example2, True))
    assert ex2b == 103, f"expected 103, but got {ex2b}"
    ex3b = len(get_paths(example3, True))
    assert ex3b == 3509, f"expected 3509, but got {ex3b}"
    answer2 = len(get_paths(data, True))
    assert answer2 == 93572, f"expected 93572, but got {answer2}"


def get_paths(inputs: str, visit_an_extra_single_a_small_cave: bool = False) -> list[str]:
    connections = get_connections(inputs)
    if visit_an_extra_single_a_small_cave:
        selector = one_small_cave_twice
    else:
        selector = small_caves_only_once
    paths = []
    for p in get_path(connections, selector):
        paths.append(p)
    return paths


# TODO efficiente dfs of bfs implementeren
def get_path(connections: dict[str, set[str]], selector) -> str:
    open_paths = [['start']]
    while open_paths:
        # display(["-".join(p) for p in open_paths])
        current_path = open_paths.pop(0)
        current_point = current_path[-1]
        for conn in connections[current_point]:
            if selector(conn, current_path, connections):
                new_path = current_path + [conn]
                if conn == 'end':
                    # print("-".join(new_path))
                    yield "-".join(new_path)
                else:
                    open_paths.append(new_path)


def small_caves_only_once(c: str, current_path: list[str], _) -> bool:
    return c.isupper() or c not in current_path


def one_small_cave_twice(c: str, current_path: list[str], connections: dict[str, set[str]]) -> bool:
    if c == "start":
        return False
    if c.islower():
        small_caves = [cave for cave in connections.keys() if cave.islower() and cave != "start"]
        if any([current_path.count(s) == 2 for s in small_caves]) and c in current_path:
            return False
    return True


def get_connections(inputs: str) -> dict[str, set[str]]:
    connections = defaultdict(set)
    conns = [(line.split('-')[0], line.split('-')[1]) for line in inputs.split('\n')]
    for c in conns:
        connections[c[0]].add(c[1])
        connections[c[1]].add(c[0])
    return connections


def display(paths: list[str]):
    print("\n".join(paths))


example1 = """
start-A
start-b
A-c
A-b
b-d
A-end
b-end
""".strip()


example2 = """
dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc
""".strip()


example3 = """
fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW
""".strip()

if __name__ == "__main__":
    main()
