#!/usr/bin/env python
import math
import re
from functools import reduce
from itertools import permutations


def iter_tokens(s):
    return filter(None, re.split(r"([\[\],])", s))


def explode(s):
    depth = 0
    result = []
    left_num_idx = None
    add_to_right = None
    token_iter = iter_tokens(s)
    for t in token_iter:
        if t == "[":
            if depth == 4 and add_to_right is None:
                # l, ',', r, ']'
                left, _ = next(token_iter), next(token_iter)
                right, _ = next(token_iter), next(token_iter)
                if left_num_idx is not None:
                    result[left_num_idx] = str(int(result[left_num_idx]) + int(left))
                add_to_right = right
                result.append("0")
            else:
                result.append(t)
                depth += 1
        elif t == "]":
            depth -= 1
            result.append(t)
        elif t.isdigit():
            left_num_idx = len(result)
            if add_to_right is not None:
                result.append(str(int(t) + int(add_to_right)))
                result.extend(list(token_iter))
                break
            else:
                result.append(t)
        else:
            assert t == ","
            result.append(t)

    return "".join(result)


def split(s):
    result = []
    token_iter = iter_tokens(s)
    for t in token_iter:
        if t.isdigit() and int(t) >= 10:
            value = int(t)/2
            left = math.floor(value)
            right = math.ceil(value)
            result.extend(["[", str(left), ",", str(right), "]"])
            result.extend(list(token_iter))
            break
        else:
            result.append(t)
    return "".join(result)


def add(a, b):
    result = "".join(["[", a, ",", b, "]"])
    while True:
        did_explode, did_split = False, False
        while True:
            new_result = explode(result)
            did_explode = new_result != result
            result = new_result
            if not did_explode:
                new_result = split(result)
                did_split = new_result != result
                result = new_result
                if not did_split:
                    break
        if not did_explode or did_split:
            break
    return result


def magnitude(s):
    stack = []
    for t in iter_tokens(s):
        if t.isdigit():
            stack.append(int(t))
        elif t == "]":
            right = stack.pop()
            left = stack.pop()
            stack.append(3*left + 2*right)

    assert len(stack) == 1
    return stack[0]


def main():
    assert explode("[[[[[9,8],1],2],3],4]") == "[[[[0,9],2],3],4]"
    assert explode("[7,[6,[5,[4,[3,2]]]]]") == "[7,[6,[5,[7,0]]]]"
    assert explode("[[6,[5,[4,[3,2]]]],1]") == "[[6,[5,[7,0]]],3]"
    assert explode("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]") == "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]"
    assert explode("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]") == "[[3,[2,[8,0]]],[9,[5,[7,0]]]]"

    assert add("[[[[4,3],4],4],[7,[[8,4],9]]]", "[1,1]") == "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"

    assert reduce(add, """
        [1,1]
        [2,2]
        [3,3]
        [4,4]
    """.split()) == "[[[[1,1],[2,2]],[3,3]],[4,4]]"

    assert reduce(add, """
        [1,1]
        [2,2]
        [3,3]
        [4,4]
        [5,5]
    """.split()) == "[[[[3,0],[5,3]],[4,4]],[5,5]]"

    assert reduce(add, """
        [1,1]
        [2,2]
        [3,3]
        [4,4]
        [5,5]
        [6,6]
    """.split()) == "[[[[5,0],[7,4]],[5,5]],[6,6]]"

    assert reduce(add, """
        [[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
        [7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
        [[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
        [[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
        [7,[5,[[3,8],[1,4]]]]
        [[2,[2,2]],[8,[8,1]]]
        [2,9]
        [1,[[[9,3],9],[[9,0],[0,7]]]]
        [[[5,[7,4]],7],1]
        [[[[4,2],2],6],[8,7]]
    """.split()) == "[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]"

    assert magnitude("[9,1]") == 29
    assert magnitude("[[9,1],[1,9]]") == 129
    assert magnitude("[[1,2],[[3,4],5]]") == 143
    assert magnitude("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]") == 1384
    assert magnitude("[[[[1,1],[2,2]],[3,3]],[4,4]]") == 445
    assert magnitude("[[[[3,0],[5,3]],[4,4]],[5,5]]") == 791
    assert magnitude("[[[[5,0],[7,4]],[5,5]],[6,6]]") == 1137
    assert magnitude("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]") == 3488

    assert reduce(add, """
    [[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
    [[[5,[2,8]],4],[5,[[9,9],0]]]
    [6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
    [[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
    [[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
    [[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
    [[[[5,4],[7,7]],8],[[8,3],8]]
    [[9,3],[[9,9],[6,[4,9]]]]
    [[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
    [[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
    """.split()) == "[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]"

    assert magnitude("[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]") == 4140

    with open("input.txt") as f:
        numbers = f.read().split()

    print("part 1")
    result = reduce(add, numbers)
    print(magnitude(result))

    print("part 2")
    max_magnitude = max(magnitude(add(a, b)) for a, b in permutations(numbers, 2))
    print(max_magnitude)


if __name__ == "__main__":
    main()
