import math
import random
import sys
import time
import timeit

CONNECT = 3
COLS = 4
ROWS = 3
EMPTY = ' '
TIE = 'TIE'


class Connect3Board:

    def __init__(self, string=None):
        if string is not None:
            self.b = [list(line) for line in string.split('|')]
        else:
            self.b = [list(EMPTY * ROWS) for i in range(COLS)]
        self.label = ''
        self.label_count = 0
        self.first = 0
        self.current_board = []
        self.minimax_boards = []

    def compact_string(self):
        return '|'.join([''.join(row) for row in self.b])

    def clone(self):
        return Connect3Board(self.compact_string())

    def get(self, i, j):
        return self.b[i][j] if i >= 0 and i < COLS and j >= 0 and j < ROWS else None

    def row(self, j):
        return [self.get(i, j) for i in range(COLS)]

    def put(self, i, j, val):
        self.b[i][j] = val
        return self

    def empties(self):
        return self.compact_string().count(EMPTY)

    def first_empty(self, i):
        j = ROWS - 1
        if self.get(i, j) != EMPTY:
            return None
        while j >= 0 and self.get(i, j) == EMPTY:
            j -= 1
        return j + 1

    def place(self, i, label):
        j = self.first_empty(i)
        if j is not None:
            self.put(i, j, label)
        return self

    def equals(self, board):
        return self.compact_string() == board.compact_string()

    def next(self, label):
        boards = []
        for i in range(COLS):
            j = self.first_empty(i)
            if j is not None:
                board = self.clone()
                board.put(i, j, label)
                boards.append(board)
        return boards

    def alternate(self):
        self.label_count = (self.label_count + 1) % 2
        if self.label_count is 1:
            self.label = 'X'
        else:
            self.label = 'O'

    def random(self):
        current_board = self.clone()
        random_boards = [current_board]
        while current_board.winner() is None:
            self.alternate()
            random_number = random.randint(0, len(current_board.next(self.label)) - 1)
            random_boards.append(current_board.next(self.label)[random_number])
            current_board = random_boards[-1]
        return random_boards

    def _winner_test(self, label, i, j, di, dj):
        for _ in range(CONNECT - 1):
            i += di
            j += dj
            if self.get(i, j) != label:
                return False
        return True

    def winner(self):
        for i in range(COLS):
            for j in range(ROWS):
                label = self.get(i, j)
                if label != EMPTY:
                    if self._winner_test(label, i, j, +1, 0) \
                            or self._winner_test(label, i, j, 0, +1) \
                            or self._winner_test(label, i, j, +1, +1) \
                            or self._winner_test(label, i, j, -1, +1):
                        return label
        return TIE if self.empties() == 0 else None

    def __str__(self):
        return stringify_boards([self])

    def random_player(self):
        if self.current_board.winner() is None:
            random_number = random.randint(0, len(self.current_board.next('X')) - 1)
            self.current_board = self.current_board.next('X')[random_number]
            board = self.current_board.clone()
            self.minimax_boards.append(board)

    def minimax(self):
        if self.first is 0:
            self.current_board = self.clone()
            self.minimax_boards.append(self.current_board)
            self.first = 1
        self.random_player()
        while self.current_board.winner() is None:
            moves = self.current_board.next('O')
            counter_moves = self.current_board.next('X')
            best_move = moves[0]
            best_score = 0
            count = 0
            for move in moves:
                clone = move.clone()
                score = self.calulate_max_score(clone)
                if score > best_score:
                    best_move = move
                    best_score = score
            while count < len(counter_moves):
                clone = counter_moves[count].clone()
                score = self.calulate_min_score(clone)
                if score > best_score:
                    best_move = moves[count]
                    best_score = score
                count += 1
            self.current_board = best_move
            board = self.current_board.clone()
            self.minimax_boards.append(board)
            self.random_player()
        return self.minimax_boards

    def alphabeta(self):
        alpha = float('-inf')
        beta = float('inf')
        if self.first is 0:
            self.current_board = self.clone()
            self.minimax_boards.append(self.current_board)
            self.first = 1
        self.random_player()
        while self.current_board.winner() is None:
            moves = self.current_board.next('O')
            counter_moves = self.current_board.next('X')
            best_move = moves[0]
            best_score = 0
            count = 0
            for move in moves:
                clone = move.clone()
                score = self.calulate_max_score(clone)
                if score > best_score:
                    best_move = move
                    best_score = score
                    alpha = max(alpha, score)
                    beta = min(beta, score)
                    if beta <= alpha:
                        break
            while count < len(counter_moves):
                clone = counter_moves[count].clone()
                score = self.calulate_min_score(clone)
                if score > best_score:
                    best_move = moves[count]
                    best_score = score
                    alpha = max(alpha, score)
                    beta = min(beta, score)
                    if beta <= alpha:
                        break
                count += 1
            self.current_board = best_move
            board = self.current_board.clone()
            self.minimax_boards.append(board)
            self.random_player()
        return self.minimax_boards

    def calulate_max_score(self, clone):
        for i in range(COLS):
            for j in range(ROWS):
                label = clone.get(i, j)
                if label != EMPTY and label is 'O':
                    score_check = 0
                    if clone.win_test('O', i, j, +1, 0) \
                            or clone.win_test('O', i, j, 0, +1) \
                            or clone.win_test('O', i, j, +1, +1) \
                            or clone.win_test('O', i, j, -1, +1):
                        score_check = 100
                    if clone.two_away_test(i, j, +1, 0) \
                            or clone.two_away_test(i, j, 0, +1) \
                            or clone.two_away_test(i, j, +1, +1) \
                            or clone.two_away_test(i, j, -1, +1):
                        score_check = 6
                    if clone.one_point_test(i, j, +1, 0) \
                            or clone.one_point_test(i, j, 0, +1) \
                            or clone.one_point_test(i, j, +1, +1) \
                            or clone.one_point_test(i, j, -1, +1):
                        score_check = 3
                    return score_check

    def calulate_min_score(self, clone):
        for i in range(COLS):
            for j in range(ROWS):
                label = clone.get(i, j)
                if label != EMPTY and label is 'X':
                    score_check = 0
                    if clone.win_test('X', i, j, +1, 0) \
                            or clone.win_test('X', i, j, 0, +1) \
                            or clone.win_test('X', i, j, +1, +1) \
                            or clone.win_test('X', i, j, -1, +1):
                        score_check = 50
                    return score_check

    def win_test(self, label, i, j, di, dj):
        for _ in range(CONNECT - 1):
            i += di
            j += dj
            if self.get(i, j) is not label:
                return False
        return True

    def two_away_test(self, i, j, di, dj):
        i_one = i
        j_one = j
        i_one += di
        i_two = i_one + di
        j_one += di
        j_two = j_one + di
        if (self.get(i_one, j_one) is ' ' and self.get(i_two, j_two) is ' ') \
                or (self.get(i_one, j_one) is ' ' and self.get(i_two, j_two) is ' '):
            return True
        return False

    def one_point_test(self, i, j, di, dj):
        i_one = i
        j_one = j
        i_one += di
        i_two = i_one + di
        j_one += di
        j_two = j_one + di
        if (self.get(i_one, j_one) is ' ' and self.get(i_two, j_two) is ' ') \
                or (self.get(i_one, j_one) is ' ' and self.get(i_two, j_two) is ' '):
            return True
        return False

def stringify_boards(boards):
    if len(boards) > 6:
        return stringify_boards(boards[0:6]) + '\n' + stringify_boards(boards[6:])
    else:
        s = ' '.join([' ' + ('-' * COLS) + ' '] * len(boards)) + '\n'
        for j in range(ROWS):
            rows = []
            for board in boards:
                rows.append('|' + ''.join(board.row(ROWS - 1 - j)) + '|')
            s += ' '.join(rows) + '\n'
        s += ' '.join([' ' + ('-' * COLS) + ' '] * len(boards))
        return s


if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        board = Connect3Board(sys.argv[2] if len(sys.argv) > 2 else None)
        if cmd == 'print':
            print(board)
        if cmd == 'next':
            print(stringify_boards(board.next('X')))
        if cmd == 'random':
            print(stringify_boards(board.random()))
        if cmd == 'minimax':
            start_time = timeit.timeit()
            print(stringify_boards(board.minimax()))
            print(start_time)
        if cmd == 'alphabeta':
            start_time = timeit.timeit()
            print(stringify_boards(board.alphabeta()))
            print(start_time)