#!/usr/bin/env python
from textwrap import dedent

def read_input(s):
    grid = {}
    for y, line in enumerate(s.splitlines()):
        for x, c in enumerate(line):
            grid[(x, y)] = int(c)
    return grid


def flash(grid, coords, flashed):
    flashed.add(coords)
    x, y = coords
    for dx, dy in ((0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)):
        neighbour = (x + dx, y + dy)
        if neighbour not in grid:
            continue
        grid[neighbour] += 1
        if grid[neighbour] > 9 and neighbour not in flashed:
            flash(grid, neighbour, flashed)


def step(grid):
    flashed = set()
    for coords in grid:
        grid[coords] += 1
    for coords in grid:
        if grid[coords] > 9 and coords not in flashed:
            flash(grid, coords, flashed)
    for coords in flashed:
        grid[coords] = 0
    return len(flashed)


def format_grid(grid):
    parts = []
    for y in range(10):
        for x in range(10):
            coords = (x, y)
            if coords not in grid:
                continue
            parts.append(" {}{}".format(grid[coords], "*" if grid[coords] == 0 else " "))
        parts.append("\n")
    return "".join(parts)


def simulate_steps(grid, n):
    _grid = grid.copy()
    total = 0
    for _ in range(n):
        total += step(_grid)
    return total


def find_sync_point(grid):
    _grid = grid.copy()
    i = 0
    while True:
        i += 1
        count = step(_grid)
        if count == len(_grid):
            return i


def main():
    example = dedent("""\
    5483143223
    2745854711
    5264556173
    6141336146
    6357385478
    4167524645
    2176841721
    6882881134
    4846848554
    5283751526
    """)
    grid = read_input(example)
    assert simulate_steps(grid, 10) == 204
    assert simulate_steps(grid, 100) == 1656

    with open("input.txt") as f:
        grid = read_input(f.read())

    print("part 1")
    print(simulate_steps(grid, 100))

    print("part 2")
    print(find_sync_point(grid))


if __name__ == "__main__":
    main()
