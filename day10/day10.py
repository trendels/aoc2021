#!/usr/bin/env python
from textwrap import dedent

opening = "([{<"
closing = ")]}>"

scores_part1 = {")": 3, "]": 57, "}": 1197, ">": 25137}
scores_part2 = {")": 1, "]": 2, "}": 3, ">": 4}

def parse_line(line):
    stack = []
    for c in line:
        if c in opening:
            stack.append(c)
        elif c in closing:
            expected = closing[opening.index(stack[-1])]
            if c != expected:
                return False, c, expected
            stack.pop()

    completion = "".join(closing[opening.index(c)] for c in reversed(stack))
    return True, completion, ""


def get_score_part1(lines):
    score = 0
    for line in lines:
        result, error, _ = parse_line(line)
        if result == False:
            score += scores_part1[error]
    return score


def get_score_part2(lines):
    scores = []
    for line in lines:
        score = 0
        result, completion, _ = parse_line(line)
        if result == True:
            for c in completion:
                score *= 5
                score += scores_part2[c]
            scores.append(score)
    return sorted(scores)[len(scores)//2]


def main():
    assert parse_line("{([(<{}[<>[]}>{[]{[(<()>") == (False, "}", "]")
    assert parse_line("[[<[([]))<([[{}[[()]]]") == (False, ")", "]")
    assert parse_line("[{[{({}]{}}([{[{{{}}([]") == (False, "]", ")")
    assert parse_line("[<(<(<(<{}))><([]([]()") == (False, ")", ">")
    assert parse_line("<{([([[(<>()){}]>(<<{{") == (False, ">", "]")

    assert parse_line("[({(<(())[]>[[{[]{<()<>>") == (True, "}}]])})]", "")

    example = dedent("""\
    [({(<(())[]>[[{[]{<()<>>
    [(()[<>])]({[<{<<[]>>(
    {([(<{}[<>[]}>{[]{[(<()>
    (((({<>}<{<{<>}{[]{[]{}
    [[<[([]))<([[{}[[()]]]
    [{[{({}]{}}([{[{{{}}([]
    {<[[]]>}<{[{[{[]{()[[[]
    [<(<(<(<{}))><([]([]()
    <{([([[(<>()){}]>(<<{{
    <{([{{}}[<[[[<>{}]]]>[]]
    """)
    lines = example.splitlines()
    assert get_score_part1(lines) == 26397
    assert get_score_part2(lines) == 288957

    with open("input.txt") as f:
        lines = f.read().splitlines()

    print("part 1")
    print(get_score_part1(lines))

    print("part 2")
    print(get_score_part2(lines))


if __name__ == "__main__":
    main()
