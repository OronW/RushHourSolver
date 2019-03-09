import math
import string

Cars_id = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"]
Trucks_id = ["O", "P", "Q", "R"]


class Board:
    def __init__(self, _cur_board):
        self.board = _cur_board
        self.side = int(math.sqrt(len(self.board)))
        self.VehicleHash = {}

        for i in range(0, len(self.board)-1):
            length = 0
            if self.board[i] == '.':
                continue

            if self.board[i] in self.VehicleHash:
                continue

            if self.board[i] in Cars_id:
                # it is acar -> length 2
                length = 2

            if self.board[i] in Trucks_id:
                # it is acar -> length 3
                length = 3

            if (i + 1) % self.side != 0 and self.board[i] == self.board[i + 1]:
                # horizonal
                self.VehicleHash[self.board[i]] = Vehicle(self.board[i], 'H', length, i, self)

            if (i + self.side) < len(self.board) and self.board[i] == self.board[i + self.side]:
                # vertical
                self.VehicleHash[self.board[i]] = Vehicle(self.board[i], 'H', length, i, self)

    def is_target_empty(self, _target):
        if not self.check_point(_target):
            return False
        if self.board[_target] == '.':
            return True

        return False

    def get_board_side(self):
        return self.side

    def set_board(self, _target, _vid):
        self.board[_target] = _vid

    def check_point(self, _p):
        if (_p >= 0) and (_p < len(self.board)):
            return True
        return False

    def print_board(self):
        for r in range(self.side):
            for c in range(self.side):
                print(self.board[r * self.side + c])
            print('\n')

    def get_vehicle(self, _id):
        return self.VehicleHash[_id]

    def get_board(self):
        return self.board


class Vehicle:
    def __init__(self, _id, _direction, _len, _pos, _obj_board):
        self.id = _id
        self.direction = _direction
        self.length = _len
        self.top_left = _pos
        self.board = _obj_board
        if self.direction == 'H':
            self.bottom_right = self.top_left + self.length
        else:
            self.bottom_right = self.top_left + (self.length * self.board.get_board_side())

    def move_vehicle(self, _direction, _steps):
        if self.check_move_validity(_direction, _steps):
            self.move(_direction, _steps)
        else:
            print('-E- can\'t move\n')

    def check_move_validity(self, _direction, _steps):
        if _direction == 'U':
            target = self.top_left - (self.board.get_board_side())
            for step in range(1, _steps):
                if not self.board.is_target_empty(target):
                    return False
                target = target - self.board.get_board_side()
            return True

        if _direction == 'D':
            target = self.bottom_right + (self.board.get_board_side())
            for step in range(1, _steps):
                if not self.board.is_target_empty(target):
                    return False
                target = target + self.board.get_board_side()
            return True

        if _direction == 'L':
            target = self.top_left - 1
            for step in range(1, _steps):
                if not self.board.is_target_empty(target):
                    return False
                target = target - 1
            return True

        if _direction == 'R':
            target = self.bottom_right + 1
            for step in range(1, _steps):
                if not self.board.is_target_empty(target):
                    return False
                target = target + 1
            return True

    def move(self, _direction, _steps):
        if _direction == 'U':
            target = self.top_left - (self.board.get_board_side())
            old_pos = self.bottom_right
            for step in range(1, _steps):
                self.board.set_board(target, self.id)
                self.board.set_board(old_pos, '.')
                target = target - self.board.get_board_side()
                old_pos = old_pos - self.board.get_board_side()
            self.top_left = target + self.board.get_board_side()
            self.bottom_right = old_pos
            return

        if _direction == 'D':
            target = self.bottom_right + (self.board.get_board_side())
            old_pos = self.top_left
            for step in range(1, _steps):
                self.board.set_board(target, self.id)
                self.board.set_board(old_pos, '.')
                target = target + self.board.get_board_side()
                old_pos = old_pos + self.board.get_board_side()
            self.bottom_right = target - self.board.get_board_side()
            self.top_left = old_pos
            return

        if _direction == 'L':
            target = self.top_left - 1
            old_pos = self.bottom_right
            for step in range(1, _steps):
                self.board.set_board(target, self.id)
                self.board.set_board(old_pos, '.')
                target = target - 1
                old_pos = old_pos - 1
            self.top_left = target + 1
            self.bottom_right = old_pos
            return

        if _direction == 'R':
            target = self.bottom_right + 1
            old_pos = self.top_left
            for step in range(1, _steps):
                self.board.set_board(target, self.id)
                self.board.set_board(old_pos, '.')
                target = target + 1
                old_pos = old_pos + 1
            self.bottom_right = target - 1
            self.top_left = old_pos
            return

    def get_direction(self):
        return self.direction

    def get_length(self):
        return self.length
