#!/usr/bin/env python
from collections import defaultdict
from textwrap import dedent

def read_input(s):
    graph = defaultdict(list)
    for line in s.splitlines():
        left, _, right = line.partition("-")
        graph[left].append(right)
        graph[right].append(left)
    return dict(graph)


def find_paths(graph, path=None, result=None, allow_duplicate=False):
    path = path or ["start"]
    result = result if result is not None else []
    node = path[-1]
    for candidate in graph[node]:
        new_path = path + [candidate]
        if candidate.isupper():
            find_paths(graph, new_path, result, allow_duplicate)
        elif candidate in path:
            if candidate not in ("start", "end") and allow_duplicate:
                find_paths(graph, new_path, result, allow_duplicate=False)
        elif candidate == "end":
            result.append(new_path)
        else:
            find_paths(graph, new_path, result, allow_duplicate)
    return result


def main():
    example = dedent("""\
    start-A
    start-b
    A-c
    A-b
    b-d
    A-end
    b-end
    """)
    graph = read_input(example)
    assert len(find_paths(graph)) == 10
    assert len(find_paths(graph, allow_duplicate=True)) == 36

    with open("input.txt") as f:
        graph = read_input(f.read())

    print("part 1")
    print(len(find_paths(graph)))

    print("part 2")
    print(len(find_paths(graph, allow_duplicate=True)))


if __name__ == "__main__":
    main()
