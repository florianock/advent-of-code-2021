#!/usr/bin/env python3

def read_instruction_line(line):
    parts = line.split()
    return parts[0], int(parts[1])


def read_instructions(filename):
    with open(filename) as f:
        return [*map(read_instruction_line, f.readlines())]


def follow_incorrect(instructions):
    pos, depth = 0, 0
    for (move, amount) in instructions:
        if move == "forward":
            pos += amount
        elif move == "up":
            depth -= amount
        elif move == "down":
            depth += amount
        else:
            raise ValueError(f"Invalid Instruction: {move}")
    return pos, depth


def follow(instructions):
    pos, depth, aim = 0, 0, 0
    for (move, amount) in instructions:
        if move == "forward":
            pos += amount
            depth += amount * aim
        elif move == "up":
            aim -= amount
        elif move == "down":
            aim += amount
        else:
            raise ValueError(f"Invalid Instruction: {move}")
    return pos, depth


def main(file='example.txt'):
    instructions = read_instructions(file)

    print("incorrectly following instructions:")
    pos1, depth1 = follow_incorrect(instructions)
    print(f"pos: {pos1}")
    print(f"depth: {depth1}")
    print(f"multiplied: {pos1 * depth1}")

    print("--------------------------")

    print("after RTFM:")
    pos, depth = follow(instructions)
    print(f"pos: {pos}")
    print(f"depth: {depth}")
    print(f"multiplied: {pos * depth}")


if __name__ == "__main__":
    main('day-2-input.txt')
