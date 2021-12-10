#!/usr/bin/env python
from functools import reduce
from operator import and_

all_segments = {1, 2, 3, 4, 5, 6, 7}
all_wires = set("abcdefg")

digit_segments = {
    0: {1, 2, 3, 5, 6, 7},
    1: {3, 6},
    2: {1, 3, 4, 5, 7},
    3: {1, 3, 4, 6, 7},
    4: {2, 3, 4, 6},
    5: {1, 2, 4, 6, 7},
    6: {1, 2, 4, 5, 6, 7},
    7: {1, 3, 6},
    8: {1, 2, 3, 4, 5, 6, 7},
    9: {1, 2, 3, 4, 6, 7},
}
digit_by_segments = {"".join(map(str, sorted(v))): str(k) for k, v in digit_segments.items()}
digits_by_length = {2: [1], 3: [7], 4: [4], 5: [2, 3, 5], 6: [0, 6, 9], 7: [8]}


def read_input(s):
    entries = []
    for line in s.splitlines():
        inputs, _, outputs = line.partition("|")
        entries.append((inputs.split(), outputs.split()))
    return entries


def find_mapping(inputs):
    choices = {i: all_wires.copy() for i in all_segments}

    ordering = [2, 3, 4, 7, 5, 6]
    for l in ordering:
        items = [s for s in inputs if len(s) == l]
        common_segments = reduce(and_, [digit_segments[c] for c in digits_by_length[l]])
        common_wires = reduce(and_, [set(s) for s in items])
        for x in common_segments:
            choices[x] -= (all_wires - common_wires)
        for x in all_segments - common_segments:
            choices[x] -= common_wires

    assert all(len(v) == 1 for v in choices.values())
    mapping = "".join(v.pop() for _, v in sorted(choices.items()))
    return mapping


def decode(outputs, mapping):
    digits = []
    for s in outputs:
        segments = "".join(sorted(str(mapping.index(c)+1) for c in s))
        digits.append(digit_by_segments[segments])
    return int("".join(digits))


def main():
    example = "acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf"
    entries = read_input(example)
    inputs, outputs = entries[0]

    mapping = find_mapping(inputs)
    assert mapping == "deafgbc"
    assert decode(outputs, mapping) == 5353

    with open("input.txt") as f:
        entries = read_input(f.read())

    print("part 1")
    print(sum(1 for entry in entries for x in entry[1] if len(x) in (2, 3, 4, 7)))

    print("part 2")
    print(sum(decode(outputs, find_mapping(inputs)) for inputs, outputs in entries))


if __name__ == "__main__":
    main()
