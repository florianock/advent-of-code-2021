#!/usr/bin/env python3
import re
from dataclasses import dataclass
from functools import reduce
from math import ceil

from aocd import data, submit

# --- Day 18: Snailfish ---


def main():
    ex1, _ = solve(example)
    assert ex1 == 4140, f"expected 4140, but got {ex1}"


def solve(inputs: str) -> (int, tuple):
    """
    Solve the snailfish addition sum and return the magnitude of the answer.
    :param inputs: String containing snailfish numbers per line
    :return: The magnitude of the answer

    >>> solve('''[1,1]
    ... [2,2]
    ... [3,3]
    ... [4,4]''')
    (445, ((((1, 1), (2, 2)), (3, 3)), (4, 4)))

    >>> solve('''[1,1]
    ... [2,2]
    ... [3,3]
    ... [4,4]
    ... [5,5]''')
    (791, ((((3, 0), (5, 3)), (4, 4)), (5, 5)))

    >>> solve('''[1,1]
    ... [2,2]
    ... [3,3]
    ... [4,4]
    ... [5,5]
    ... [6,6]''')
    (1137, ((((5, 0), (7, 4)), (5, 5)), (6, 6)))

    >>> solve('''[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
    ... [7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
    ... [[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
    ... [[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
    ... [7,[5,[[3,8],[1,4]]]]
    ... [[2,[2,2]],[8,[8,1]]]
    ... [2,9]
    ... [1,[[[9,3],9],[[9,0],[0,7]]]]
    ... [[[5,[7,4]],7],1]
    ... [[[[4,2],2],6],[8,7]]''')
    (3488, ((((8,7),(7,7)),((8,6),(7,7))),(((0,7),(6,6)),(8,7))))
    """
    sf_sum = reduce(sf_add, generate_numbers(inputs))
    return sf_mag(sf_sum), sf_sum


def sf_add(a: tuple, b: tuple) -> tuple:
    """
    Add two snailfish numbers and reduce until done.
    :param a: The first number
    :param b: The second number
    :return: The reduced result

    >>> sf_add((1,2), ((3,4), 5))
    ((1, 2), ((3, 4), 5))

    >>> sf_add(((((4,3),4),4),(7,((8,4),9))), (1,1))
    ((((0, 7), 4), ((7, 8), (6, 0))), (8, 1))

    >>> sf_add((((0,(4,5)),(0,0)),(((4,5),(2,6)),(9,5))), (7,(((3,7),(4,3)),((6,3),(8,8)))))
    ((((4,0),(5,4)),((7,7),(6,0))),((8,(7,7)),((7,9),(5,0))))
    """
    return sf_reduce((a, b))


def sf_reduce(a: tuple) -> tuple:
    """
    Reduce the given snailfish number until done.
    :param a: The snailfish number
    :return: The reduced snailfish number

    >>> sf_reduce((((((4,3),4),4),(7,((8,4),9))),(1,1)))
    ((((0, 7), 4), ((7, 8), (6, 0))), (8, 1))
    """
    return a


def sf_explode(a: tuple) -> tuple:
    """
    Explodes the leftmost pair that's nested four pairs deep
    :param a: the snailfish number to explode
    :param current_depth: The current depth of the tuple
    :param exploded: Boolean value denoting whether explosion has already happened
    :return: the exploded snailfish number

    >>> sf_explode((((((9,8),1),2),3),4))
    (((((0, 9), 2), 3), 4), (), True)

    >>> sf_explode((7,(6,(5,(4,(3,2))))))
    ((7, (6, (5, (7, 0)))), (), True)

    >>> sf_explode(((6,(5,(4,(3,2)))),1))
    (((6, (5, (7, 0))), 3), (), True)

    >>> sf_explode(((3,(2,(1,(7,3)))),(6,(5,(4,(3,2))))))
    (((3, (2, (8, 0))), (9, (5, (4, (3, 2))))), (), True)

    >>> sf_explode(((3,(2,(8,0))),(9,(5,(4,(3,2))))))
    (((3, (2, (8, 0))), (9, (5, (7, 0)))), (), True)

    >>> sf_explode((((((4,3),4),4),(7,((8,4),9))),(1,1)))
    (((((0, 7), 4), (7, ((8, 4), 9))), (1, 1)), (), True)

    >>> sf_explode(((((0,7),4),(7,((8,4),9))),(1,1)))
    (((((0, 7), 4), (15, (0, 13))), (1, 1)), (), True)

    >>> sf_explode(((((0,7),4),((7,8),(0,(6,7)))),(1,1)))
    (((((0, 7), 4), ((7, 8), (6, 0))), (8, 1)), (), True)

    >>> sf_explode((((((1, 1), (2, 2)), (3, 3)), (4, 4)), (5, 5)))
    (((((0, (3, 2)), (3, 3)), (4, 4)), (5, 5)), (), True)

    >>> sf_explode(((((0, (3, 2)), (3, 3)), (4, 4)), (5, 5)))
    (((((3, 0), (5, 3)), (4, 4)), (5, 5)), (), True)
    """
    return a


def sf_split(a: tuple) -> tuple:
    """
    Splits the leftmost number above ten
    :param perform_split: Boolean denoting whether to do the split
    :param a: The snailfish number
    :return: The same snailfish number with leftmost number > 10 split

    >>> sf_split(((((0,7),4),(15,(0,13))),(1,1)))
    ((((0, 7), 4), ((7, 8), (0, 13))), (1, 1))

    >>> sf_split(((((0,7),4),((7,8),(0,13))),(1,1)))
    ((((0, 7), 4), ((7, 8), (0, (6, 7)))), (1, 1))
    """
    return a


def sf_mag(a: tuple) -> int:
    """
    Calculates the magnitude of a snailfish number
    :param a: a snailfish number
    :return: the magnitude as int

    >>> sf_mag((9, 1))
    29

    >>> sf_mag((1, 9))
    21

    >>> sf_mag(((9, 1),(1, 9)))
    129

    >>> sf_mag(((1,2),((3,4),5)))
    143

    >>> sf_mag(((((0,7),4),((7,8),(6,0))),(8,1)))
    1384

    >>> sf_mag(((((1,1),(2,2)),(3,3)),(4,4)))
    445

    >>> sf_mag(((((3,0),(5,3)),(4,4)),(5,5)))
    791

    >>> sf_mag(((((5,0),(7,4)),(5,5)),(6,6)))
    1137

    >>> sf_mag(((((8,7),(7,7)),((8,6),(7,7))),(((0,7),(6,6)),(8,7))))
    3488

    >>> sf_mag(((((6,6),(7,6)),((7,7),(7,0))),(((7,7),(7,7)),((7,8),(9,9)))))
    4140
    """
    if type(a[0]) is int:
        left = a[0]
    else:
        left = sf_mag(a[0])
    if type(a[1]) is int:
        right = a[1]
    else:
        right = sf_mag(a[1])
    return left * 3 + right * 2


def generate_numbers(inputs: str) -> tuple:
    lines = inputs.split('\n')
    for line in lines:
        yield read_number(line)


def read_number(numbers: str) -> tuple:
    """
    Absolutely monstrous parser that reads an input snailfish number from a string
    :param numbers: The number string
    :return: a tuple with optionally nested tuples of ints

    >>> read_number("[5,8]")
    (5, 8)

    >>> read_number("[[1,2],3]")
    ((1, 2), 3)

    >>> read_number("[19,[200,350]]")
    (19, (200, 350))

    >>> read_number("[[1000,198],[223,378]]")
    ((1000, 198), (223, 378))
    """
    assert numbers[0] == "["
    assert numbers[-1] == "]"
    stack = []
    left = ""
    right = ""
    if numbers[1].isnumeric():
        left = re.search(r'\d+', numbers).group()
    if numbers[-2].isnumeric():
        right = re.match(r'.*,(\d+)]$', numbers).group(1)
    for i, c in enumerate(numbers[1:-1]):
        if c == '[':
            stack.append(c)
        elif c == ']':
            stack.pop()
            if not stack:
                if not left:
                    left = numbers[1:i+2]
                if not right:
                    if left.isnumeric():
                        rstack = []
                        for j, d in enumerate(reversed(numbers[1:-1])):
                            if d == ']':
                                rstack.append(d)
                            elif d == '[':
                                rstack.pop()
                                if not rstack:
                                    right = numbers[-j-2:i+2]
                    else:
                        right = numbers[i+3:-1]
                break
    if left.isnumeric():
        left = int(left)
    else:
        left = read_number(left)
    if right.isnumeric():
        right = int(right)
    else:
        right = read_number(right)
    return left, right


example = """
[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
""".strip()

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    main()
