#!/usr/bin/env python
from textwrap import dedent


def read_input(s):
    points, folds = set(), []
    for line in s.splitlines():
        if line.startswith("fold"):
            axis, _, n = line.split()[2].partition("=")
            folds.append((axis, int(n)))
        else:
            x, sep, y = line.partition(",")
            if sep == ",":
                points.add((int(x), int(y)))
    return points, folds


def apply_fold(points, fold):
    axis, n = fold
    new_points = set()
    for x, y in points:
        if axis == "y":
            if y < n:
                new_points.add((x, y))
            elif y > n:
                new_points.add((x, 2*n-y))
        elif axis == "x":
            if x < n:
                new_points.add((x, y))
            elif x > n:
                new_points.add((2*n-x, y))
    return new_points


def format_sheet(points):
    width = max(x for x, _ in points)
    height = max(y for _, y in points)
    lines = []
    for y in range(height+1):
        line = []
        for x in range(width+1):
            line.append("#" if (x, y) in points else ".")
        lines.append("".join(line))
    return "\n".join(lines)


def main():
    example = dedent("""\
        6,10
        0,14
        9,10
        0,3
        10,4
        4,11
        6,0
        6,12
        4,1
        0,13
        10,12
        3,4
        3,0
        8,4
        1,10
        2,14
        8,10
        9,0

        fold along y=7
        fold along x=5
    """)
    points, folds = read_input(example)
    points = apply_fold(points, folds[0])
    assert len(points) == 17
    points = apply_fold(points, folds[1])
    assert format_sheet(points) == dedent("""\
    #####
    #...#
    #...#
    #...#
    #####
    """).strip()

    with open("input.txt") as f:
        points, folds = read_input(f.read())

    print("part 1")
    print(len(apply_fold(points, folds[0])))

    print("part 2")
    for fold in folds:
        points = apply_fold(points, fold)
    print(format_sheet(points))


if __name__ == "__main__":
    main()
