#!/usr/bin/env python

def read_input(s):
    return list(map(int, s.split(",")))


def cost_part1(x, positions):
    return sum(abs(pos - x) for pos in positions)

def cost_part2(x, positions):
    return sum((n := abs(pos - x), n*(n+1)//2)[1] for pos in positions)


def find_best_position_and_cost(positions):
    pos = sorted(positions)[len(positions)//2]
    return pos, cost_part1(pos, positions)


def find_best_position_and_cost_part2(positions):
    # Use mean as starting point and do a linear search in both directions
    initial_pos = int(sum(positions)/len(positions))
    initial_cost = cost_part2(initial_pos, positions)

    new_pos, new_cost, found_better_pos = initial_pos, initial_cost, False
    best_pos, best_cost = initial_pos, initial_cost
    while True:
        new_pos += 1
        new_cost = cost_part2(new_pos, positions)
        if new_cost < best_cost:
            found_better_pos = True
            best_pos, best_cost = new_pos, new_cost
        else:
            if found_better_pos:
                return best_pos, best_cost
            break

    new_pos, new_cost, found_better_pos = initial_pos, initial_cost, False
    best_pos, best_cost = initial_pos, initial_cost
    while True:
        new_pos -= 1
        new_cost = cost_part2(new_pos, positions)
        if new_cost < best_cost:
            found_better_pos = True
            best_pos, best_cost = new_pos, new_cost
        else:
            if found_better_pos:
                return best_pos, best_cost
            break

    return initial_pos, initial_cost


def main():
    example = "16,1,2,0,4,2,7,1,2,14"
    positions = read_input(example)

    assert find_best_position_and_cost(positions) == (2, 37)
    assert find_best_position_and_cost_part2(positions) == (5, 168)

    with open("input.txt") as f:
        positions = read_input(f.read())

    _, cost = find_best_position_and_cost(positions)
    print("part 1")
    print(cost)

    _, cost = find_best_position_and_cost_part2(positions)
    print("part 2")
    print(cost)


if __name__ == "__main__":
    main()
