#!/usr/bin/env python3
import operator
from dataclasses import dataclass
from functools import reduce
from typing import Iterable
from colorama import Fore, Style, init

# noinspection PyUnresolvedReferences
from aocd import data, submit

Stack = list[str]
init(autoreset=True)  # init colorama


@dataclass
class SyntaxCheckResult:
    corrupt_char: int
    stack: Stack
    autocomplete: Stack
    line: str

    def get_error_score(self) -> int:
        if not self.is_corrupted():
            return 0
        return scores[self.line[self.corrupt_char]][0]

    def get_autocomplete_score(self) -> int:
        count = 0
        for c in self.autocomplete:
            count = (count * 5) + scores[c][1]
        return count

    def is_corrupted(self) -> bool:
        return self.corrupt_char > -1

    def display(self) -> str:
        padding = 140
        if not self.is_corrupted():
            return Style.BRIGHT + Fore.WHITE + (self.line + Fore.GREEN + "".join(self.autocomplete)).ljust(padding) \
                + '\t' + str(self.get_autocomplete_score())
        else:
            output = list(self.line)
            output.insert(self.corrupt_char+1, Style.RESET_ALL + Style.DIM)
            output.insert(self.corrupt_char, Fore.RED)
            return Style.BRIGHT + Fore.WHITE + "".join(output).ljust(padding) + '\t' + str(self.get_error_score())


def main():
    ex1 = solve1(example)
    assert ex1 == 26397, f"expected 26397, but got {ex1}"
    answer1 = solve1(data)
    assert answer1 == 399153, f"expected 399153, but got {answer1}"
    ex2 = solve2(example)
    assert ex2 == 288957, f"expected 288957, but got {ex2}"
    answer2 = solve2(data)
    assert answer2 == 2995077699, f"expected 2995077699, but got {answer2}"


def solve1(inputs: str) -> int:
    nav_subsystem = inputs.split('\n')
    syntax_errors = map(check_syntax, nav_subsystem)
    return reduce(operator.add, [s.get_error_score() for s in syntax_errors], 0)


def solve2(inputs: str) -> int:
    nav_subsystem = inputs.split('\n')
    syntax_errors = map(check_syntax, nav_subsystem)
    return get_autocomplete_score(syntax_errors)


def check_syntax(line: str) -> SyntaxCheckResult:
    stack = Stack()
    for i, c in enumerate(line):
        if c in chars.keys():
            stack.append(c)
        else:
            opening_char = stack.pop()
            if chars[opening_char] != c:
                return SyntaxCheckResult(i, stack, Stack(), line)
    if stack:
        repairment = [chars[x] for x in stack]
        repairment.reverse()
        autocomplete = repairment
    else:
        autocomplete = Stack()
    return SyntaxCheckResult(-1, stack, autocomplete, line)


def get_autocomplete_score(results: Iterable[SyntaxCheckResult]) -> int:
    all_scores = []
    for r in results:
        print(r.display())
        all_scores.append(r.get_autocomplete_score())
    all_scores = [s for s in all_scores if s > 0]
    all_scores.sort()
    middle = len(all_scores) // 2
    return all_scores[middle]


chars = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>'
}

scores = {
    ')': (3, 1),
    ']': (57, 2),
    '}': (1197, 3),
    '>': (25137, 4)
}

example = """
[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]
""".strip()

if __name__ == "__main__":
    main()
