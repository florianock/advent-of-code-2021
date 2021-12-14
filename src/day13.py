#!/usr/bin/env python3
# noinspection PyUnresolvedReferences
from aocd import data, submit

# TODO clean up
def main():
    paper, instructions = read_input(data)
    answer1 = 0
    for x, i in instructions:
        paper = fold(paper, i, x)
        if answer1 == 0:
            answer1 = sum([sum(r) for r in paper])
        display(paper)
    print(answer1)

    # for answer2: squeeze eyes and read output
    # But here goes:
    answer2 = []
    font_width = 4
    for n in range(0, len(paper[0]), font_width+1):
        key = ""
        for row in paper:
            letter = row[n:n+font_width+1]
            key += str(sum(letter))
        answer2.append(letters[key])
    print("".join(answer2))


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


def fold(a: list[list[bool]], i: int, fold_along: str) -> list[list[bool]]:
    if fold_along == 'y':
        a = transpose(a)
    result = []
    for row in a:
        left = row[:i]
        right = row[i+1:]
        right.reverse()
        result.append([n or m for n, m in zip(left, right)])
    if fold_along == 'y':
        return transpose(result)
    return result


def transpose(a: list[list[bool]]) -> list[list[bool]]:
    return list(map(list, zip(*a)))


def read_input(inputs: str) -> (list[list[bool]], list[(str, int)]):
    split = inputs.split('\n\n')
    coords = split[0]
    folding = split[1]
    lines = [line for line in coords.split('\n')]
    nums = []
    for line in lines:
        cs = line.split(',')
        nums.append((int(cs[0]), int(cs[1])))
    xs, ys = ([i for i, j in nums],
              [j for i, j in nums])
    matrix = [[True if (x, y) in nums else False for x in range(max(xs)+1)] for y in range(max(ys)+1)]
    # for n in nums:
    #     matrix[n[1]][n[0]] = True
    i_lines = [i for i in folding.split('\n')]
    result2 = [i.replace('fold along ', '') for i in i_lines]
    result3 = []
    for i in result2:
        inst = i.split('=')
        result3.append((inst[0], int(inst[1])))
    return matrix, result3


def display(matrix: list[list[bool]]):
    builder = []
    for row in matrix:
        builder.append("".join(["##" if x else "  " for x in row]))
    print("\n".join(builder))


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
