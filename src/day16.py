#!/usr/bin/env python3
import operator
from functools import reduce
from aocd import data, submit


Operators = {
    0: operator.add,
    1: operator.mul,
    2: min,
    3: max,
    4: None,
    5: operator.gt,
    6: operator.lt,
    7: operator.eq
}


def main():
    for ex in examples1:
        ex1 = get_version_sum(ex[0])
        assert ex1 == ex[1], f"expected {ex[1]}, but got {ex1}"
    answer1 = get_version_sum(data)
    assert answer1 == 951, f"expected 951, but got {answer1}"
    for ex in examples2:
        ex2 = solve(ex[0])
        assert ex2 == ex[1], f"expected {ex[1]}, but got {ex2}"
    answer2 = solve(data)
    assert answer2 == 902198718880, f"expected 902198718880, but got {answer2}"


def get_version_sum(inputs: str) -> int:
    transmission = read_inputs(inputs)
    packets = split_packets(transmission)
    version_sum = sum_version_numbers(packets)
    return version_sum


def sum_version_numbers(packets: list[str]) -> int:
    sum = 0
    for p in packets:
        if type(p) is list:
            sum += sum_version_numbers(p)
        else:
            sum += int(p[:3], 2)
    return sum


def strings_length(packets: list[str]) -> int:
    length = 0
    for p in packets:
        if type(p) is list:
            length += strings_length(p)
        else:
            length += len(p)
    return length


def operate(packets: list[str]) -> int:
    active_operator = get_operator(packets.pop(0))
    args = []
    for p in packets:
        if type(p) is list:
            args.append(operate(p))
        else:
            args.append(get_literal_value(p))
    assert active_operator not in [operator.lt, operator.gt, operator.eq] or len(args) == 2,\
        "lt, gt and eq need exactly two args"
    total = reduce(active_operator, args)
    return total


def get_operator(p: str):
    assert int(p[3:6], 2) != 4, "p is not an operator! Can't do the operation."
    assert int(p[3:6], 2) in Operators.keys(), "p is not a known operator! Can't do the operation."
    packet_type = int(p[3:6], 2)
    return Operators[packet_type]


def get_literal_value(p: str):
    assert int(p[3:6], 2) == 4, "p is not a literal! Can't get the value."
    value = ""
    for i in range(6, len(p), 5):
        first = int(p[i], 2)
        value += p[i+1:i+5]
        if first == 0:
            break
    return int(value, 2)


def solve(inputs: str) -> int:
    transmission = read_inputs(inputs)
    packets = split_packets(transmission)
    result = operate(packets)
    return result


def split_packets(message: str) -> list[str]:
    packet_type = int(message[3:6], 2)
    if packet_type == 4:
        return [message]
    else:
        p, r = process_operator(message)
        return p


def get_packets_by_length(message: str, length: int) -> (list[str], str):
    packets = []
    while length > 0 and any([1 if x == "1" else 0 for x in message]):
        p_type = int(message[3:6], 2)
        if p_type == 4:
            p, message = process_literal(message)
            packets.append(p)
            length -= len(p)
        else:
            p, m = process_operator(message)
            packets.append(p)
            length -= strings_length(p)
            message = m
    return packets, message


def get_packets_by_number(message: str, number_of_packets: int) -> (list[str], str):
    packets = []
    while number_of_packets > 0:
        p_type = int(message[3:6], 2)
        if p_type == 4:
            packet, message = process_literal(message)
            packets.append(packet)
        else:
            p, message = process_operator(message)
            packets.append(p)
        number_of_packets -= 1
    return packets, message


def process_literal(message: str) -> (str, str):
    assert int(message[3:6], 2) == 4, "this message is NOT a literal!"
    first = int(message[6])
    match first:
        case 0:
            mess = message[:11]
            rest = message[11:]
        case 1:
            for i in range(6, len(message), 5):
                if int(message[i]) == 0:
                    mess = message[:i + 5]
                    rest = message[i + 5:]
                    break
    return mess, rest


def process_operator(message: str) -> (list[str], str):
    assert int(message[3:6], 2) != 4, "this message is NOT an operator!"
    length_type_id = int(message[6])
    match length_type_id:
        case 0:
            length_bits = message[7:22]
            subpacket_bit_count = int(length_bits, 2)
            processed_message = message[:22]
            packets, rest = get_packets_by_length(message[22:], subpacket_bit_count)
        case 1:
            length_bits = message[7:18]
            num_packets = int(length_bits, 2)
            processed_message = message[:18]
            packets, rest = get_packets_by_number(message[18:], num_packets)
    return [processed_message] + packets, rest


def decode_hex_char(c: str) -> str:
    return str(bin(int(c, 16)))[2:].zfill(4)


def read_inputs(inputs: str) -> str:
    return reduce(lambda x, y: x + decode_hex_char(y), inputs, "")


examples1 = [
    ("D2FE28", 6),
    ("38006F45291200", 1 + 6 + 2),
    ("EE00D40C823060", 7 + 2 + 4 + 1),
    ("8A004A801A8002F478", 16),
    ("620080001611562C8802118E34", 12),
    ("C0015000016115A2E0802F182340", 23),
    ("A0016C880162017C3686B18A3D4780", 31)
]

examples2 = [
    ("C200B40A82", 3),
    ("04005AC33890", 54),
    ("880086C3E88112", 7),
    ("CE00C43D881120", 9),
    ("D8005AC2A8F0", 1),
    ("F600BC2D8F", 0),
    ("9C005AC2F8F0", 0),
    ("9C0141080250320F1802104A08", 1)
]

if __name__ == "__main__":
    main()
