#!/usr/bin/env python3

def get_diagnostics_report(filename):
    with open(filename) as f:
        return [*map(lambda line:line.strip(), f.readlines())]


def binary_tally(strings):
    bits = [*map(list, strings)]
    num_length = len(bits[0])
    result = []
    for index in range(num_length):
        ints_at_index = [int(x[index]) for x in bits]
        count_ones = sum(ints_at_index)
        count_zeroes = len(bits)-count_ones
        result.append((count_zeroes, count_ones))
    return result


def select_bits_per_position(counts, func):
    result = []
    for x in counts:
        value = func(x)
        index = x.index(value)
        if x[0] == x[1]:
            if func == max:
                index = 1
            if func == min:
                index = 0
        result.append(str(index))
    return "".join(result) 


def max_min(counts):
    most_common_bits = select_bits_per_position(counts, max)
    least_common_bits = select_bits_per_position(counts, min)
    return most_common_bits, least_common_bits


def get_common_number(strings, bias):
    num_length = len(strings[0])
    for i in range(num_length):
        counts = binary_tally(strings)
        matching_bit = select_bits_per_position(counts, bias)[i]
        matching = [s for s in strings if s[i] == matching_bit]
        if len(matching) < 2:
            return "".join(matching)
        strings = matching


def main(file='example.txt'):
    diagnostics = get_diagnostics_report(file)
    counts = binary_tally(diagnostics)

    gamma_rate, epsilon_rate = max_min(counts)
    power_consumption = int(gamma_rate, 2) * int(epsilon_rate, 2)
    print(f"power consumption: {power_consumption}")

    oxygen = get_common_number(diagnostics, max)
    co2 = get_common_number(diagnostics, min)
    life_support_rating = int(oxygen, 2) * int(co2, 2)
    print(f"life support rating: {life_support_rating}")


if __name__ == "__main__":
    main('day-3-input.txt')
