#!/usr/bin/env python3
import os


def main(file):
    inputs = read_input(file)
    print(example)
    print(inputs)


def read_input(filename):
    with open(filename) as f:
        return f.read().strip()


example = """
3,4,3,1,2
""".strip()


def get_aocd_data(day, year, file):
    from aocd import get_data
    with open(file, 'w') as f:
        f.write(get_data(day=day, year=year))


if __name__ == "__main__":
    data_file = 'day-7-input.txt'
    if not os.path.exists(data_file):
        get_aocd_data(7, 2021, data_file)
    main(data_file)
