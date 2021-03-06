#!/usr/bin/env python3

from aocd import data, submit
from collections import Counter

# --- Day 8: Seven Segment Search ---

normal_digits = ["abcefg", "cf", "acdeg", "acdfg", "bcdf", "abdfg", "abdefg", "acf", "abcdefg", "abcdfg"]


def main():
    ex1 = count_easy_digits(example)
    assert ex1 == 26, f"expected 26, but got {ex1}"
    answer1 = count_easy_digits(data)
    assert answer1 == 301, f"expected 301, but got {answer1}"
    ex2 = count_outputs(example2)
    assert ex2 == 5353, f"expected 5353, but got {ex2}"
    ex3 = count_outputs(example)
    assert ex3 == 61229, f"expected 61229, but got {ex3}"
    answer2 = count_outputs(data)
    assert answer2 == 908067, f"expected 908067, but got {answer2}"
    # alt(example)


# TODO alternatively, try using bitmasks


# only on Python 3.10; https://www.reddit.com/r/adventofcode/comments/rbj87a/2021_day_8_solutions/hnoyy04/?utm_source=reddit&utm_medium=web2x&context=3
# def alt(inputs: str):
#     s = 0
#     for x, y in [x.split('|') for x in inputs.split('\n')]:  # split signal and output
#         l = {len(s): set(s) for s in x.split()}  # get number of segments
#         n = ''
#         for o in map(set, y.split()):  # loop over output digits
#             match len(o), len(o & l[4]), len(o & l[2]):  # mask with known digits
#                 case 2, _, _:
#                     n += '1'
#                 case 3, _, _:
#                     n += '7'
#                 case 4, _, _:
#                     n += '4'
#                 case 7, _, _:
#                     n += '8'
#                 case 5, 2, _:
#                     n += '2'
#                 case 5, 3, 1:
#                     n += '5'
#                 case 5, 3, 2:
#                     n += '3'
#                 case 6, 4, _:
#                     n += '9'
#                 case 6, 3, 1:
#                     n += '6'
#                 case 6, 3, 2:
#                     n += '0'
#         s += int(n)
#     print(s)


def read_inputs(inputs: str) -> list[tuple[list[str], list[str]]]:
    result = []
    displays = inputs.split('\n')
    for d in displays:
        ds_s, out_s = d.split(' | ')
        ds = ds_s.split(' ')
        out = out_s.split(' ')
        result.append((sort_strings(ds), sort_strings(out)))
    return result


def sort_strings(inputs: list[str]) -> list[str]:
    result = []
    for s in inputs:
        result.append("".join(sorted(s)))
    return result


def count_easy_digits(inputs: str) -> int:
    displays = read_inputs(inputs)
    easy_lengths = [x for x in [2, 3, 4, 7]]
    result = 0
    for _, out in displays:
        easy = list(filter(lambda x: len(x) in easy_lengths, out))
        result += len(easy)
    return result


def count_outputs(inputs: str) -> int:
    count = 0
    displays = read_inputs(inputs)
    for occ, out in displays:
        key = find_edges_by_unique_counts(occ)
        key = find_edges_by_digit_length(occ, key)
        result = []
        for o in out:
            d = decode(o, key)
            result.append(str(d))
        output_digits = "".join(result)
        display(output_digits)
        count += int(output_digits)
    return count


def find_edges_by_unique_counts(digits: list[str]) -> str:
    key = '.' * 7
    counts_and_edges = Counter("".join(digits).replace(' ', '')).most_common()
    known_unique_counts = [(0, 5), (-2, 1), (-1, 4)]
    for counter_idx, key_idx in known_unique_counts:
        char = counts_and_edges[counter_idx][0]
        key = str_replace_at_index(key, key_idx, char)
    return key


def find_edges_by_digit_length(digits: list[str], key: str) -> str:
    easy = [x for x in digits if len(x) in [2, 3, 4, 7]]
    lengths_and_edges = [(2, 2), (3, 0), (4, 3), (7, 6)]
    for length, key_idx in lengths_and_edges:
        char = (set(get_item_by_length(easy, length)) - set(key)).pop()
        key = str_replace_at_index(key, key_idx, char)
    return key


def get_item_by_length(items: list[str], length: int) -> str:
    for i in items:
        if len(i) == length:
            return i
    return ""


def str_replace_at_index(string: str, i: int, c: str) -> str:
    arr = list(string)
    arr[i] = c
    return "".join(arr)


def decode(digit: str, key: str) -> int:
    normal_edges = normal_digits[8]
    answer = ""
    for c in digit:
        i = key.index(c)
        answer += normal_edges[i]
    answer = "".join(sorted(answer))
    return normal_digits.index(answer)


def display(number: str):
    grid = []
    for c in number:
        d = normal_digits[int(c)]
        grid = add_to_grid(grid, get_display_digit(d))
    print("\n".join(grid))


def add_to_grid(grid: list[str], digit: list[str]) -> list[str]:
    if not grid:
        return digit
    result = []
    for i, row in enumerate(grid):
        result.append(row + "\t" + digit[i])
    return result


def get_display_digit(digit: str) -> list[str]:
    h = '_'
    v = '|'
    grid = ["   ", "   ", "   "]
    if 'a' in digit:
        grid[0] = str_replace_at_index(grid[0], 1, h)
    if 'b' in digit:
        grid[1] = str_replace_at_index(grid[1], 0, v)
    if 'c' in digit:
        grid[1] = str_replace_at_index(grid[1], 2, v)
    if 'd' in digit:
        grid[1] = str_replace_at_index(grid[1], 1, h)
    if 'e' in digit:
        grid[2] = str_replace_at_index(grid[2], 0, v)
    if 'f' in digit:
        grid[2] = str_replace_at_index(grid[2], 2, v)
    if 'g' in digit:
        grid[2] = str_replace_at_index(grid[2], 1, h)
    return grid


example = """
be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce
""".strip()


#   8      5   2      3    7    9       6    4     0    1      5     3     5     3
example2 = """
acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf
""".strip()


if __name__ == "__main__":
    main()
