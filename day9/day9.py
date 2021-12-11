#!/usr/bin/env python
from textwrap import dedent

class Map:
    def __init__(self, rows):
        self.rows = rows
        self.width = len(rows[0])
        self.height = len(rows)

    def is_low_point(self, x, y):
        value = self.rows[y][x]
        return all(value < n for _, _, n in self.iter_neighbours(x, y))

    def iter_neighbours(self, x, y):
        directions = ((0, -1), (1, 0), (0, 1), (-1, 0))
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if nx < 0 or nx >= self.width:
                continue
            if ny < 0 or ny >= self.height:
                continue
            yield nx, ny, self.rows[ny][nx]

    def iter_cells(self):
        for y in range(self.height):
            for x in range(self.width):
                yield x, y, self.rows[y][x], self.is_low_point(x, y)

    def get_basin_size(self, x, y):
        size = 0
        visited = set()
        queue = set([(x, y)])
        while queue:
            x, y = queue.pop()
            visited.add((x, y))
            size += 1
            for nx, ny, value in self.iter_neighbours(x, y):
                if (nx, ny) not in visited and value != 9:
                    queue.add((nx, ny))
        return size

    def get_risk_score(self):
        return sum(v + 1 for _, _, v, is_lo in self.iter_cells() if is_lo)

    def get_basin_score(self):
        low_points = [(x, y) for x, y, _, is_lo in self.iter_cells() if is_lo]
        basin_sizes = [self.get_basin_size(x, y) for x, y in low_points]
        basin_sizes.sort(reverse=True)
        return basin_sizes[0] * basin_sizes[1] * basin_sizes[2]

    def __str__(self):
        rows = [[] for _ in range(self.height)]
        for _, y, value, is_low_point in self.iter_cells():
            rows[y].append(f"[{value}]" if is_low_point else f" {value} ")
        return "\n".join("".join(r) for r in rows)


def read_input(s):
    rows = []
    for line in s.splitlines():
        rows.append([int(c) for c in line])
    return Map(rows)


def main():
    example = dedent("""\
    2199943210
    3987894921
    9856789892
    8767896789
    9899965678
    """)
    m = read_input(example)
    #print(m)
    assert m.get_risk_score() == 15
    assert m.get_basin_score() == 1134

    with open("input.txt") as f:
        m = read_input(f.read())

    print("part 1")
    print(m.get_risk_score())

    print("part 2")
    print(m.get_basin_score())


if __name__ == "__main__":
    main()
