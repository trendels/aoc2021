#!/usr/bin/env python
import heapq
from textwrap import dedent


class Graph:
    def __init__(self, map_, scale=1):
        self.map = map_
        self.width = (max(x for x, _ in map_) + 1)
        self.height = (max(y for _, y in map_) + 1)
        self.scale = scale

    @property
    def source(self):
        return (0, 0)

    @property
    def target(self):
        return (self.width*self.scale - 1, self.height*self.scale - 1)

    def get_level(self, node):
        x, y = node
        qx, rx = divmod(x, self.width)
        qy, ry = divmod(y, self.height)
        return ((self.map[(rx, ry)] - 1 + qx + qy) % 9) + 1

    def get_neighbours(self, node):
        x, y = node
        for dx, dy in ((-1, 0), (0, 1), (1, 0), (0, -1)):
            nx = x + dx
            ny = y + dy
            if 0 <= nx < self.width*self.scale and 0 <= ny < self.height*self.scale:
                neighbour = (nx, ny)
                yield neighbour, self.get_level(neighbour)

    def print_path(self, path):
        for y in range(self.height*self.scale):
            for x in range(self.width*self.scale):
                node = (x, y)
                level = self.get_level(node)
                if node == self.source or node in path:
                    print(f"\033[1m{level}\033[0m", end="")
                else:
                    print(level, end="")
            print()
        print()


def read_input(s):
    m = {}
    for y, line in enumerate(s.splitlines()):
        for x, value in enumerate(line):
            m[(x, y)] = int(value)
    return m


def find_shortest_path(graph):
    source, target = graph.source, graph.target
    queue = [(0, source)]
    dist = {source: 0}
    prev = {}
    while queue:
        cur_dist, node = heapq.heappop(queue)
        if node == target:
            path = []
            while node:
                path = [node] + path
                node = prev[node]
                if node == source:
                    return path
        for neighbour, weight in graph.get_neighbours(node):
            alt = cur_dist + weight
            if neighbour not in dist or alt < dist[neighbour]:
                dist[neighbour] = alt
                prev[neighbour] = node
                heapq.heappush(queue, (alt, neighbour))

    raise RuntimeError("Path not found")


def lowest_total_risk(graph, echo=True):
    path = find_shortest_path(graph)
    if echo:
        graph.print_path(path)
    return sum(graph.get_level(node) for node in path)


def main():
    example = dedent("""\
    1163751742
    1381373672
    2136511328
    3694931569
    7463417111
    1319128137
    1359912421
    3125421639
    1293138521
    2311944581
    """)
    m = read_input(example)
    assert lowest_total_risk(Graph(m)) == 40
    assert lowest_total_risk(Graph(m, scale=5)) == 315

    with open("input.txt") as f:
        m = read_input(f.read())

    print("part 1")
    print(lowest_total_risk(Graph(m), echo=False))

    print("part 2")
    print(lowest_total_risk(Graph(m, scale=5), echo=False))


if __name__ == "__main__":
    main()
