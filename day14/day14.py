#!/usr/bin/env python
from collections import Counter, defaultdict
from textwrap import dedent


def read_input(s):
    template, rules = "", {}
    for line in s.splitlines():
        pair, sep, replacement = line.partition(" -> ")
        if sep == " -> ":
            rules[pair] = replacement
        elif token := line.strip():
            template = token
    return template, rules


def apply_rules(polymer, rules):
    result = defaultdict(int)
    for pair, count in polymer.items():
        if pair in rules:
            insert = rules[pair]
            result[pair[0] + insert] += count
            result[insert + pair[1]] += count
        else:
            result[pair] += count
    return dict(result)


def grow(template, rules, steps):
    polymer = dict(Counter(f"{e1}{e2}" for e1, e2 in zip(template, template[1:])))
    for _ in range(steps):
        polymer = apply_rules(polymer, rules)
    return polymer


def get_answer(template, polymer):
    counts = defaultdict(int)
    counts[template[-1]] = 1
    elements = set("".join(polymer))
    for e in elements:
        for k, v in polymer.items():
            if k[0] == e:
                counts[e] += v
    freq = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    return freq[0][1] - freq[-1][1]


def main():
    example = dedent("""\
    NNCB

    CH -> B
    HH -> N
    CB -> H
    NH -> C
    HB -> C
    HC -> B
    HN -> C
    NN -> C
    BH -> H
    NC -> B
    NB -> B
    BN -> B
    BB -> N
    BC -> B
    CC -> N
    CN -> C
    """)
    template, rules = read_input(example)
    polymer = grow(template, rules, 10)
    assert get_answer(template, polymer) == 1588

    with open("input.txt") as f:
        template, rules = read_input(f.read())

    print("part 1")
    polymer = grow(template, rules, 10)
    print(get_answer(template, polymer))

    print("part 2")
    polymer = grow(template, rules, 40)
    print(get_answer(template, polymer))


if __name__ == "__main__":
    main()
