#!/usr/bin/env python
from textwrap import dedent

def read_input(s):
    grid = {}
    for y, line in enumerate(s.splitlines()):
        for x, c in enumerate(line):
            grid[(x, y)] = int(c)
    return grid


def flash(state, coords):
    grid, flashed, total = state
    flashed.add(coords)
    x, y = coords
    for dx, dy in ((0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)):
        neighbour = (x + dx, y + dy)
        if neighbour not in grid:
            continue
        grid[neighbour] += 1
        if grid[neighbour] > 9 and neighbour not in flashed:
            grid, flashed, total = flash((grid, flashed, total), neighbour)
    return grid, flashed, total+1


def step(state):
    last_grid, _, total = state
    grid = last_grid.copy()
    flashed = set()
    for coords in grid:
        grid[coords] += 1
    for coords in grid:
        if grid[coords] > 9 and coords not in flashed:
            grid, flashed, total = flash((grid, flashed, total), coords)
    for coords in flashed:
        grid[coords] = 0
    return grid, flashed, total


def format_state(state):
    grid, flashed, _ = state
    parts = []
    for y in range(10):
        for x in range(10):
            coords = (x, y)
            if coords not in grid:
                continue
            parts.append(" {}{}".format(grid[coords], "*" if coords in flashed else " "))
        parts.append("\n")
    return "".join(parts)


def simulate_steps(state, n):
    for _ in range(n):
        state = step(state)
    return state


def find_sync_point(state):
    i = 0
    while True:
        i += 1
        state = step(state)
        grid, flashed, _ = state
        if len(flashed) == len(grid):
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
    state = (grid, set(), 0)
    assert simulate_steps(state, 10)[2] == 204
    assert simulate_steps(state, 100)[2] == 1656

    with open("input.txt") as f:
        grid = read_input(f.read())

    state = (grid, set(), 0)

    _, _, total = simulate_steps(state, 100)
    print("part 1")
    print(total)

    step = find_sync_point(state)
    print("part 2")
    print(step)


if __name__ == "__main__":
    main()
