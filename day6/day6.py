#!/usr/bin/env python

def read_input(s):
    return list(map(int, s.split(",")))


def step(state):
    new_state = state[:]
    for n in range(10):
        count = state[n]
        new_state[n] -= count
        if n == 0:
            new_state[6] += count
            new_state[8] += count
        else:
            new_state[n-1] += count
    return new_state


def simulate_population(pop, days):
    state = [pop.count(n) for n in range(10)]
    for _ in range(days):
        state = step(state)
    return sum(state)


def main():
    example = "3,4,3,1,2"
    fish = read_input(example)

    assert simulate_population(fish, days=80) == 5934
    assert simulate_population(fish, days=256) == 26984457539

    with open("input.txt") as f:
        fish = read_input(f.read())

    print("part 1")
    print(simulate_population(fish, days=80))

    print("part 2")
    print(simulate_population(fish, days=256))


if __name__ == "__main__":
    main()
