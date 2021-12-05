#!/usr/bin/env python
from textwrap import dedent


class Board:
    def __init__(self, lines):
        self.rows = [list(map(int, line.strip().split())) for line in lines]
        self.marked = []

    def __str__(self):
        lines = []
        for row in self.rows:
            items = []
            for number in row:
                marker = '*' if number in self.marked else ' '
                items.append(f"{number:2}{marker}")
            lines.append(" ".join(items))
        return "\n".join(lines)

    def mark(self, n):
        for row in self.rows:
            if n in row:
                self.marked.append(n)

    @property
    def has_won(self):
        for row in self.rows:
            if all(n in self.marked for n in row):
                return True
        for i in range(len(self.rows[0])):
            if all(row[i] in self.marked for row in self.rows):
                return True
        return False

    @property
    def score(self):
        return self.marked[-1] * sum(n for row in self.rows for n in row if n not in self.marked)


def read_input(s):
    lines = s.strip().splitlines()
    numbers = list(map(int, lines[0].split(",")))
    board_lines = []
    boards = []

    for line in lines[2:]:
        if line:
            board_lines.append(line)
        else:
            board = Board(board_lines)
            boards.append(board)
            board_lines = []

    if board_lines:
        boards.append(Board(board_lines))

    return numbers, boards


def get_first_winning_board(numbers, boards):
    for n in numbers:
        for board in boards:
            board.mark(n)
            if board.has_won:
                return board
    raise RuntimeError("no winning board")


def get_last_winning_board(numbers, boards):
    remaining = set(boards)
    for n in numbers:
        for board in boards:
            if board not in remaining:
                continue
            board.mark(n)
            if board.has_won:
                remaining.remove(board)
                if not remaining:
                    return board
    raise RuntimeError("no winning board")


def main():
    example = dedent("""
    7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

    22 13 17 11  0
     8  2 23  4 24
    21  9 14 16  7
     6 10  3 18  5
     1 12 20 15 19

     3 15  0  2 22
     9 18 13 17  5
    19  8  7 25 23
    20 11 10 24  4
    14 21 16 12  6

    14 21 17 24  4
    10 16 15  9 19
    18  8 23 26 20
    22 11 13  6  5
     2  0 12  3  7
    """)
    numbers, boards = read_input(example)

    board = get_first_winning_board(numbers, boards)
    assert board.score == 4512

    board = get_last_winning_board(numbers, boards)
    assert board.score == 1924

    with open("input.txt") as f:
        numbers, boards = read_input(f.read())

    board = get_first_winning_board(numbers, boards)
    print("part 1")
    print(board.score)

    board = get_last_winning_board(numbers, boards)
    print("part 2")
    print(board.score)


if __name__ == "__main__":
    main()
