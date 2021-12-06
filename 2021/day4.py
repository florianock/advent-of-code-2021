#!/usr/bin/env python3
from collections import namedtuple

Row = list[int]
Col = list[int]
Board = list[Row]
Result = namedtuple("Result", ["round", "score"])


def main(file):
    inputs = read_input(file)
    assert get_score_for_best_board(example) == 4512
    print(get_score_for_best_board(inputs))
    assert get_score_for_worst_board(example) == 1924
    print(get_score_for_worst_board(inputs))


def get_score_for_best_board(inputs: str) -> int:
    numbers, boards = process_inputs(inputs)
    return get_ultimate_score(boards, numbers)


def get_score_for_worst_board(inputs: str) -> int:
    numbers, boards = process_inputs(inputs)
    return get_ultimate_score(boards, numbers, False)


def get_ultimate_score(boards: list[Board], numbers: list[int], i_want_to_win: bool = True) -> int:
    results = [result for result in [get_result(board, numbers) for board in boards] if result.round > -1]
    results.sort(key=lambda r: r.round)
    if i_want_to_win:
        best_result = results[0]
    else:
        best_result = results[-1]
    return numbers[best_result.round] * best_result.score


def get_result(board: Board, numbers: list[int]) -> Result:
    for n in range(len(numbers)):
        numbers_so_far = numbers[0:n+1]
        if rows_bingo(board, numbers_so_far) or cols_bingo(board, numbers_so_far):
            return Result(n, get_remaining_board_value(board, numbers_so_far))
    return Result(-1, -1)


def rows_bingo(board: Board, numbers: list[int]) -> bool:
    return any([bingo(row, numbers) for row in board])


def cols_bingo(board: Board, numbers: list[int]) -> bool:
    return any([bingo(col, numbers) for col in transpose(board)])


def bingo(numbers_from_board: list[int], drawn_numbers: list[int]) -> bool:
    return not set(numbers_from_board) - set(drawn_numbers)


def get_remaining_board_value(board: Board, numbers: list[int]):
    flattened_board = [number for row in board for number in row]
    return sum(set(flattened_board) - set(numbers))


def transpose(board: Board) -> list[Col]:
    return [*map(list, zip(*board))]


def process_inputs(inputs: str) -> (list[int], list[Board]):
    numbers_and_boards = inputs.split('\n\n')
    numbers = get_numbers(numbers_and_boards[0])
    boards = get_boards(numbers_and_boards[1:])
    return numbers, boards


def get_numbers(numbers: str) -> list[int]:
    return [int(x) for x in numbers.split(',')]


def get_boards(boards: list[str]) -> list[Board]:
    return [*map(create_board, boards)]


def create_board(board: str) -> Board:
    return [*map(create_row, board.split('\n'))]


def create_row(row: str) -> Row:
    return [int(number) for number in row.split()]


def read_input(filename):
    with open(filename) as f:
        contents = f.read().strip()
        return contents


example = """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7"""


if __name__ == "__main__":
    main('day-4-input.txt')
