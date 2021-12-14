#!/usr/bin/env python3
# noinspection PyUnresolvedReferences
from aocd import data, submit


def main():
    ex1, letter = solve(example)
    assert ex1 == 17, f"expected 17, but got {ex1}"
    assert letter == 'O', f"expected 'O', but got {letter}"
    answer, letter_result = solve(data)
    assert answer == 818, f"expected 818, but got {answer}"
    assert letter_result == "LRGPRECB", f"expected 'LRGPRECB', but got {letter_result}"


def solve(inputs: str):
    paper, instructions = read_input(inputs)
    answer = 0
    for x, i in instructions:
        paper = fold(paper, i, x)
        if answer == 0:
            answer = sum([sum(r) for r in paper])
    return answer, print_letters(paper)


def print_letters(paper: list[list[bool]]) -> str:
    display(paper)
    font_width = 4
    found_letters = []
    for n in range(0, len(paper[0]), font_width+1):
        key = ""
        for row in paper:
            letter = row[n:n+font_width+1]
            key += str(sum(letter))
        found_letters.append(letters[key])
    found_string = "".join(found_letters)
    print(found_string)
    return found_string


def fold(paper: list[list[bool]], i: int, fold_along: str) -> list[list[bool]]:
    if fold_along == 'y':
        paper = transpose(paper)
    folded = [[n or m for n, m in zip(row[:i], row[:i:-1])] for row in paper]
    if fold_along == 'y':
        folded = transpose(folded)
    return folded


def transpose(a: list[list[bool]]) -> list[list[bool]]:
    return list(map(list, zip(*a)))


def read_input(inputs: str) -> (list[list[bool]], list[(str, int)]):
    [coords, folding] = inputs.split('\n\n')
    lines = [line for line in coords.split('\n')]
    xs, ys = ([int(line.split(',')[0]) for line in lines], [int(line.split(',')[1]) for line in lines])
    dots = [[False for x in range(max(xs)+1)] for y in range(max(ys)+1)]
    for x, y in zip(xs, ys):
        dots[y][x] = True
    folds = [(f[11], int(f[13:])) for f in folding.split('\n')]
    return dots, folds


def display(matrix: list[list[bool]]):
    builder = []
    for row in matrix:
        builder.append("".join(["\u2588\u2588" if x else "  " for x in row]))
    print("\n".join(builder))


letters = {
    "323223": 'B',
    "221122": 'C',
    "413114": 'E',
    "221323": 'G',
    "111114": 'L',
    "5222500": 'O',
    "422224": 'O',
    "322311": 'P',
    "322322": 'R'
}


example = """
6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
""".strip()

if __name__ == "__main__":
    main()
