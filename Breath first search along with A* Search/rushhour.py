import sys
from random import randint
import copy



class Board:
    def __init__(self):
        self.default_board = "  o aa|  o   |xxo   |ppp  q|     q|     q"
        self.board = self.default_board
        self.board_array = None
        self.board_arrays = []
        self.random_path = []
        self.open_set = []
        self.closed_set = []
        self.checked_boards = []
        self.total_path_count = 1
        self.heuristic_value = 0

    def get_board(self):
        if len(sys.argv) > 2:
            self.board = sys.argv[2]
        self.board_array = self.board.split('|')
        format_count = 0
        while format_count < len(self.board_array):
            if format_count is 2:
                self.board_array[format_count] = '|' + self.board_array[format_count] + ' '
            else:
                self.board_array[format_count] = '|' + self.board_array[format_count] + '|'
            format_count += 1
        self.board_array.insert(0, ' ------ ')
        self.board_array.insert(len(self.board_array), ' ------ ')

    def call_command(self):
        if sys.argv[1] is not '' and sys.argv[1] is not None:
            if sys.argv[1] == 'print':
                self.print()
            if sys.argv[1] == 'next':
                self.next()
                self.print_next(self.board_arrays)
            if sys.argv[1] == 'done':
                if self.done() is True:
                    print('True')
                else:
                    print('False')
            if sys.argv[1] == 'random':
                self.random_walk()
            if sys.argv[1] == 'bfs':
                self.breadth_first_search()
            if sys.argv[1] == 'astar':
                self.a_star()
        else:
            print('no command please retry')

    def print(self):
        print_count = 0
        while print_count < len(self.board_array):
            print(self.board_array[print_count])
            print_count += 1

    def next(self):
        self.get_all_moves()

    def done(self):
        if self.board_array[3][5:8] == 'xx ':
            return True
        else:
            return False

    def get_all_moves(self):
        row_count = 1
        character_count = 1
        checked_characters = []
        while row_count < (len(self.board_array) - 1):
            while character_count < len(self.board_array[row_count]):
                if self.board_array[row_count][character_count] is not ' ' and \
                        self.board_array[row_count][character_count] is not '|' and \
                        self.board_array[row_count][character_count] not in checked_characters:
                    self.check_for_moves(self.board_array[row_count][character_count], character_count, row_count)
                    checked_characters.append(self.board_array[row_count][character_count])
                character_count += 1
            character_count = 1
            row_count += 1

    def check_for_moves(self, character, character_index, row_index):

        if self.board_array[row_index + 1][character_index] is character:
            self.check_up_and_down(character, character_index, row_index)

        elif self.board_array[row_index][character_index + 1] is character:
            self.check_left_and_right(character, character_index, row_index)

        elif self.board_array[row_index - 1][character_index] is ' ' and \
                self.board_array[row_index + 1][character_index] is ' ' and \
                self.board_array[row_index][character_index - 1] is ' ' and \
                self.board_array[row_index][character_index + 1] is ' ':
            self.check_all_directions(character, character_index, row_index)
        else:
            print('no moves found for ' + character)

    def check_up_and_down(self, character, character_index, row_index):
        count = 0
        character_count = 1
        up_count = 0
        down_count = 0
        left_count = 0
        right_count = 0
        while self.board_array[row_index - 1 - up_count][character_index] is ' ':
            up_count += 1
        while self.board_array[row_index + count][character_index] is ' ' or \
                self.board_array[row_index + count][character_index] is character:
            count += 1
            if self.board_array[row_index + count][character_index] is character:
                character_count += 1
            if self.board_array[row_index + count][character_index] is ' ':
                down_count += 1
        self.generate_next_boards(character, character_index, row_index, character_count, up_count, down_count,
                                  left_count, right_count)
        # print(character + ' ' + str(character_count))
        # print(character + ' can move up ' + str(up_count) + ' times can move down ' + str(down_count) + ' times')

    def check_left_and_right(self, character, character_index, row_index):
        count = 0
        character_count = 1
        up_count = 0
        down_count = 0
        left_count = 0
        right_count = 0
        while self.board_array[row_index][character_index - 1 - left_count] is ' ':
            left_count += 1
        while (character_index + count) is not 7 and self.board_array[row_index][character_index + count] is ' ' or \
                self.board_array[row_index][character_index + count] is character:
            count += 1
            if self.board_array[row_index][character_index + count] is character:
                character_count += 1
            if self.board_array[row_index][character_index + count] is ' ' and (character_index + count) is not 7:
                right_count += 1
        self.generate_next_boards(character, character_index, row_index, character_count, up_count, down_count,
                                  left_count, right_count)
        # print(character + ' ' + str(character_count)) print(character + ' can move left ' + str(left_count) + '
        # times can move right ' + str(right_count) + ' times')

    def check_all_directions(self, character, character_index, row_index):
        character_count = 1
        up_count = 0
        down_count = 0
        left_count = 0
        right_count = 0

        while self.board_array[row_index - 1 - up_count][character_index] is ' ':
            up_count += 1
        while self.board_array[row_index + 1 + down_count][character_index] is ' ':
            down_count += 1
        while self.board_array[row_index][character_index - 1 - left_count] is ' ':
            left_count += 1
        while self.board_array[row_index][character_index + 1 + right_count] is ' ':
            right_count += 1
        self.generate_next_boards(character, character_index, row_index, character_count, up_count, down_count,
                                  left_count, right_count)
        # print(character + ' ' + str(character_count)) print(character + ' can move up ' + str(up_count) + ' times
        # can move down ' + str(down_count) + ' times') print(character + ' can move left ' + str(left_count) + '
        # times can move right ' + str(right_count) + ' times')

    def generate_next_boards(self, character, character_index, row_index, character_count=0, up_count=0, down_count=0,
                             left_count=0, right_count=0):
        edit_count = 0
        if character_count < 0:
            print()
        else:
            new_array = self.board_array[:]

            while edit_count < down_count:
                new_array = new_array[:]
                change = list(new_array[row_index + edit_count])
                change[character_index] = ' '
                new_array[row_index + edit_count] = ''.join(change)

                change = list(new_array[row_index + character_count + edit_count])
                change[character_index] = character
                new_array[row_index + character_count + edit_count] = ''.join(change)

                self.board_arrays.append(new_array)
                edit_count += 1
            edit_count = 0
            new_array = self.board_array[:]

            while edit_count < up_count:
                new_array = new_array[:]
                change = list(new_array[row_index + character_count - edit_count - 1])
                change[character_index] = ' '
                new_array[row_index + character_count - edit_count - 1] = ''.join(change)

                change = list(new_array[row_index - edit_count - 1])
                change[character_index] = character
                new_array[row_index - edit_count - 1] = ''.join(change)

                self.board_arrays.append(new_array)
                edit_count += 1
            edit_count = 0
            new_array = self.board_array[:]

            while edit_count < right_count:
                new_array = new_array[:]
                change = list(new_array[row_index])
                change[character_index + edit_count] = ' '
                new_array[row_index] = ''.join(change)

                change = list(new_array[row_index])
                change[character_index + character_count + edit_count] = character
                new_array[row_index] = ''.join(change)

                self.board_arrays.append(new_array)
                edit_count += 1
            edit_count = 0
            new_array = self.board_array[:]

            while edit_count < left_count:
                new_array = new_array[:]
                change = list(new_array[row_index])
                change[character_index + character_count - edit_count - 1] = ' '
                new_array[row_index] = ''.join(change)

                change = list(new_array[row_index])
                change[character_index - edit_count - 1] = character
                new_array[row_index] = ''.join(change)

                self.board_arrays.append(new_array)
                edit_count += 1

    def print_next(self, board_arrays):
        array_count = 0
        print_count = 0

        while array_count < len(board_arrays[0]):
            while print_count < len(board_arrays):
                print(board_arrays[print_count][array_count], end='')
                print_count += 1
            print('')
            array_count += 1
            print_count = 0

    def random_walk(self):
        n = 10
        count = 0
        self.random_path.append(self.board_array)
        while count < n and self.done() is not True:
            self.next()
            random_board = self.board_arrays[randint(0, len(self.board_arrays) - 1)]
            self.random_path.append(random_board)
            self.board_array = random_board
            count += 1
        self.board_arrays = self.random_path
        self.print_next(self.board_arrays)

    def breadth_first_search(self):
        self.open_set = []
        self.closed_set = []
        self.open_set.append(self.board_array)
        self.print()
        self.checked_boards.append(self.board_array)
        first_layer = 1
        if self.done is True:
            return
        while self.open_set is not []:
            self.next()
            count = 0
            while count < len(self.board_arrays):
                if self.board_arrays[count] not in self.checked_boards:
                    if first_layer is 1:
                        new_array = self.open_set[0]
                        new_path = [new_array[:], self.board_arrays[count]]
                    else:
                        new_path = copy.deepcopy(self.open_set[0])
                        new_path.append(self.board_arrays[count])
                    self.total_path_count += 1
                    self.print_next(new_path)
                    self.board_array = new_path[-1]
                    if self.board_array[3][5:8] == 'xx ':
                        self.open_set = []
                        print(self.total_path_count)
                        return
                    self.open_set.append(new_path)
                    self.checked_boards.append(self.board_arrays[count])
                count += 1
            self.closed_set.append(self.open_set[0])
            del self.open_set[0]
            self.board_array = self.open_set[0][-1]
            self.board_arrays = []
            first_layer = 0


    def heuristic(self,board):
        count = 1
        self.heuristic_value = 7
        while count < len(board[3])-1:
            if self.board_array[3][7-count]is ' ':
                self.heuristic_value -= 1
            if self.board_array[3][7-count]is 'x':
                return
            count += 1


    def a_star(self):
        self.open_set = []
        self.closed_set = []
        self.open_set.append(self.board_array)
        self.print()
        self.checked_boards.append(self.board_array)
        first_layer = 1
        if self.done is True:
            return
        while self.open_set is not []:
            self.next()
            count = 0
            while count < len(self.board_arrays):
                if self.board_arrays[count] not in self.checked_boards:
                    if first_layer is 1:
                        new_array = self.open_set[0]
                        new_path = [new_array[:], self.board_arrays[count]]
                    else:
                        new_path = copy.deepcopy(self.open_set[0])
                        new_path.append(self.board_arrays[count])
                    self.total_path_count += 1
                    self.heuristic(new_path[-1])
                    print(self.heuristic_value)

                    self.print_next(new_path)
                    self.board_array = new_path[-1]
                    if self.board_array[3][5:8] == 'xx ':
                        self.open_set = []
                        print(self.total_path_count-1)
                        return
                    self.open_set.append(new_path)
                    self.checked_boards.append(self.board_arrays[count])
                count += 1
            self.closed_set.append(self.open_set[0])
            del self.open_set[0]
            self.board_array = self.open_set[0][-1]
            self.board_arrays = []
            first_layer = 0


board = Board()
board.get_board()
board.call_command()
# board.print()
# board.next()
# board.random_walk()
# board.breadth_first_search()
# board.a_star()
