#!/usr/bin/python

def read_numbers(filename):
    with open(filename) as f:
        return [*map(int, f.readlines())]


def count_changes(inputs, window_size=1):
    change_count = 0
    for index, _ in enumerate(inputs):
        if index + window_size >= len(inputs):
            break
        a = inputs[index:index + window_size]
        b = inputs[index + 1:index + window_size + 1]
        if sum(b) > sum(a):
            change_count += 1
    return change_count


def main(file='example.txt'):
    depths = read_numbers(file)

    change_count = count_changes(depths)
    print(f"Found changes: {change_count}")

    three_at_a_time = count_changes(depths, 3)
    print(f"Found changes per 3: {three_at_a_time}")


if __name__ == "__main__":
    main('day-1-input.txt')
