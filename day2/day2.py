#!/usr/bin/env python

def read_course(s):
    return [(d, int(n)) for d, n in [l.split() for l in s.strip().splitlines()]]


def follow(course):
    pos, depth = 0, 0
    for d, n in course:
        if d == 'forward':
            pos += n
        elif d == 'down':
            depth += n
        elif d == 'up':
            depth -= n
    return pos, depth


def follow_with_aim(course):
    pos, depth, aim = 0, 0, 0
    for d, n in course:
        if d == 'forward':
            pos += n
            depth += aim * n
        elif d == 'down':
            aim += n
        elif d == 'up':
            aim -= n
    return pos, depth


def main():
    example = """
    forward 5
    down 5
    forward 8
    up 3
    down 8
    forward 2
    """
    course = read_course(example)

    pos, depth = follow(course)
    assert (pos, depth) == (15, 10)

    pos, depth = follow_with_aim(course)
    assert (pos, depth) == (15, 60)

    with open("input.txt") as f:
        course = read_course(f.read())

    print("part 1")
    pos, depth = follow(course)
    print(pos * depth)

    print("part 2")
    pos, depth = follow_with_aim(course)
    print(pos * depth)


if __name__ == "__main__":
    main()
