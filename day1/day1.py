#!/usr/bin/env python

def count_incr(measurements):
    return sum((int(b > a) for a, b in zip(measurements, measurements[1:])))


def count_incr_w3(measurements):
    windows = map(sum, zip(measurements, measurements[1:], measurements[2:]))
    return count_incr(list(windows))


def main():
    measurements = """
    199
    200
    208
    210
    200
    207
    240
    269
    260
    263
    """
    measurements = list(map(int, measurements.split()))
    assert count_incr(measurements) == 7
    assert count_incr_w3(measurements) == 5

    with open("input.txt") as f:
        measurements = list(map(int, f))

    print("part 1")
    print(count_incr(measurements))

    print("part 2")
    print(count_incr_w3(measurements))


if __name__ == "__main__":
    main()
