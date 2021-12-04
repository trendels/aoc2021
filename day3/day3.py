#!/usr/bin/env python
from collections import defaultdict
from textwrap import dedent

def read_report(s):
    return s.strip().splitlines()


def get_bit_counts(report):
    counts = defaultdict(lambda: defaultdict(int))
    for number in report:
        for i, bit in enumerate(number):
            counts[i][bit] += 1
    return dict(counts)


def get_diagnostics(report):
    gamma, epsilon = "", ""
    counts = get_bit_counts(report)
    for i in range(len(counts)):
        freq = sorted(counts[i].items(), key=lambda item: item[1])
        gamma += freq[1][0]
        epsilon += freq[0][0]

    return int(gamma, 2), int(epsilon, 2)


def get_life_support_rating(report):
    candidates = report[:]
    for i in range(len(report[0])):
        counts = get_bit_counts(candidates)
        freq = sorted(counts[i].items(), key=lambda item: (item[1], item[0]), reverse=True)
        most_common = freq[0][0]
        candidates = [c for c in candidates if c[i] == most_common]
        if len(candidates) == 1:
            break
    oxygen = candidates[0]

    candidates = report[:]
    for i in range(len(report[0])):
        counts = get_bit_counts(candidates)
        freq = sorted(counts[i].items(), key=lambda item: (item[1], item[0]), reverse=True)
        least_common = freq[1][0]
        candidates = [c for c in candidates if c[i] == least_common]
        if len(candidates) == 1:
            break
    co2 = candidates[0]

    return int(oxygen, 2), int(co2, 2)


def main():
    example = dedent("""
    00100
    11110
    10110
    10111
    10101
    01111
    00111
    11100
    10000
    11001
    00010
    01010
    """)
    report = read_report(example)

    gamma, epsilon = get_diagnostics(report)
    assert (gamma, epsilon) == (22, 9)

    oxygen, co2 = get_life_support_rating(report)
    assert (oxygen, co2) == (23, 10)

    with open("input.txt") as f:
        report = read_report(f.read())

    gamma, epsilon = get_diagnostics(report)
    print("part 1")
    print(gamma * epsilon)

    oxygen, co2 = get_life_support_rating(report)
    print("part 2")
    print(oxygen * co2)


if __name__ == "__main__":
    main()
