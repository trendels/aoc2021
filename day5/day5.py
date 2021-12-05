#!/usr/bin/env python
from collections import defaultdict
from textwrap import dedent


def read_input(s):
    lines = []
    for line in s.strip().splitlines():
        start, _, end = line.partition(" -> ")
        x1, y1 = map(int, start.split(",", 1))
        x2, y2 = map(int, end.split(",", 1))
        lines.append(((x1, y1), (x2, y2)))
    return lines


def count_covered_points(lines, diagonals=False):
    points = defaultdict(int)
    for line in lines:
        (x1, y1), (x2, y2) = line
        if x1 == x2:
            step = 1 if y2 > y1 else -1
            for y in range(y1, y2+step, step):
                points[(x1, y)] += 1
        elif y1 == y2:
            step = 1 if x2 > x1 else -1
            for x in range(x1, x2+step, step):
                points[(x, y1)] += 1
        elif diagonals:
            step_x = 1 if x2 > x1 else -1
            step_y = 1 if y2 > y1 else -1
            for x, y in zip(range(x1, x2+step_x, step_x), range(y1, y2+step_y, step_y)):
                points[(x, y)] += 1

    return sum([1 for v in points.values() if v > 1])


def main():
    example = dedent("""
    0,9 -> 5,9
    8,0 -> 0,8
    9,4 -> 3,4
    2,2 -> 2,1
    7,0 -> 7,4
    6,4 -> 2,0
    0,9 -> 2,9
    3,4 -> 1,4
    0,0 -> 8,8
    5,5 -> 8,2
    """)
    lines = read_input(example)
    assert count_covered_points(lines) == 5
    assert count_covered_points(lines, diagonals=True) == 12

    with open("input.txt") as f:
        lines = read_input(f.read())

    count = count_covered_points(lines)
    print("part 1")
    print(count)

    count = count_covered_points(lines, diagonals=True)
    print("part 2")
    print(count)


if __name__ == "__main__":
    main()
