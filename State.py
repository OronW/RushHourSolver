from Play_tools import Vehicle, Board
import math
from utils import string_modify, string_switch


class State:
    def __init__(self, _board_obj):
        self.board_state = _board_obj

    def get_string_board(self):
        return self.board_state.get_board()

    def get_board(self):
        return self.board_state

    def find_next_steps(self):
        board = self.board_state.get_board()
        side = int(math.sqrt(len(board)))
        next_states = []

        # check horizontal
        for i in range(0, (len(board)), side):  # run over rows
            j = 0
            while j < side:  # run over columns
                p = i + j  # set p as position on board
                if board[p] == '.':  # empty square
                    j += 1
                    continue
                if self.board_state.get_vehicle(board[p]).get_direction() == 'V':  # check if vertical
                    j += 1
                    continue

                v_len = self.board_state.get_vehicle(board[p]).get_length()

                # check right
                steps = 0
                temp_state = board
                p_next = p + 1
                while (p_next % side != 0) and (p_next < len(board)) and (board[p_next] == '.'):
                    temp_state = string_switch(temp_state, p_next, p - (v_len - 1))
                    steps += 1
                    next_states.append(temp_state + ',' + temp_state[p] + 'R' + str(steps))
                    p = p_next
                    p_next += 1
                    j += 1

                p = i+j  # set p as position on board
                if (p >= len(board)) or \
                        (board[p] == '.') or \
                        (self.board_state.get_vehicle(board[p]).get_direction() == 'V'):  # check if vertical
                    j += 1
                    continue
                # check left
                temp_state = board
                p_next = p - 1
                steps = 0
                while (p_next % side != side - 1) and (board[p_next] == '.'):
                    temp_state = string_switch(temp_state, p_next, p + (v_len - 1))
                    steps += 1
                    next_states.append(temp_state + ',' + temp_state[p] + 'L' + str(steps))
                    p = p_next
                    p_next -= 1
                j += 1

        # check vertical
        for i in range(0, side):  # run over columns
            j = 0
            while j < len(board):  # run over rows
                p = i + j  # set p as position on board
                if board[p] == '.':  # empty square
                    j += side
                    continue
                if self.board_state.get_vehicle(board[p]).get_direction() == 'H':  # check if horizontal
                    j += side
                    continue

                v_len = self.board_state.get_vehicle(board[p]).get_length()

                # check down
                temp_state = board
                steps = 0
                p_next = p + side
                while (p_next < len(board)) and (board[p_next] == '.'):
                    temp_state = string_switch(temp_state, p_next, p - ((v_len - 1)*side))
                    steps += 1
                    next_states.append(temp_state + ',' + temp_state[p] + 'D' + str(steps))
                    p = p_next
                    p_next += side
                    j += side

                p = i+j  # set p as position on board

                if (p >= len(board)) or \
                        (board[p] == '.') or \
                        (self.board_state.get_vehicle(board[p]).get_direction() == 'H'):  # check if horizontal
                    j += side
                    continue
                # check up
                temp_state = board
                p_next = p - side
                steps = 0
                while (p_next >= 0) and (board[p_next] == '.'):
                    temp_state = string_switch(temp_state, p_next, p + ((v_len - 1)*side))
                    steps += 1
                    next_states.append(temp_state + ',' + temp_state[p] + 'U' + str(steps))
                    p = p_next
                    p_next -= side
                j += side

        return next_states

    ############changed###############

    def final_move(self):
        vehicle = self.board_state.get_vehicle('X')
        start_point = vehicle.top_left + vehicle.get_length()
        steps_to_end = 6 - ((vehicle.top_left + vehicle.get_length()) % 6)

        for i in range(0, steps_to_end):
            if self.get_string_board()[start_point+i] != '.':
                return False

        return True

    def run_command(self, _command):
        if len(_command) != 3:
            print("-E- Wrong command length")

        self.board_state.update_board(_command)
        self.BF = len(self.find_next_steps())

    ############### change######################################
    def isFree(self, _vehicle):
        board_size = self.get_board().side

        # CASE 1 : size 2 car can move one square up
        if (int(_vehicle.top_left / board_size) == 0) and \
                (_vehicle.get_length() == 2) and \
                (self.get_string_board()[_vehicle.top_left] == '.'):
            return True

        # CASE 2 : Car blocking from above (x is 0,1,2), need to go down
        elif int(_vehicle.top_left / board_size) < 3:
            shift = _vehicle.get_length() * self.get_board().side
            new_position = _vehicle.top_left + shift
            counter = 0
            while int(new_position / board_size) < board_size:
                if self.get_string_board()[new_position] == '.':
                    counter += 1
                new_position += shift

            # if car can clear the path, result is true
            if counter >= _vehicle.get_length():
                return True

        #CASE 3 : Car not blocking the path
        return True


"""""
    def isFree(self, _vehicle):
        result = False
        x = int(_vehicle.top_left / 6)
        y = _vehicle.top_left % 6
        size = _vehicle.get_length()

        # CASE 1 : size 2 car can move one square up
        # if (int(_vehicle.top_left / 6) == 1) and \ -> if (int(_vehicle.top_left / 6) == 0) and \
        if (x==1 and size==2 and self.get_string_board()[0*6+y]=='.'):
            #print("Case 1")
            result = True

        # CASE 2 : Car blocking from above (x is 0,1,2), need to go down
        elif (x<3):
            #print("Case 2")
            #count free squares below
            freeblocks=0
            nextX = x+size
            while(nextX<6):
                if (self.get_string_board()[nextX*6+y]=='.'):
                    freeblocks+=1
                nextX+=1

            # if car can clear the path, result is true
            if (freeblocks>=size):
                result=True

        #CASE 3 : Car not blocking the path
        else:
            #print("Case 3")
            result=True

        return result

    def final_move(self):
        vehicle = self.board_state.get_vehicle('X')
        # x = int(vehicle.top_left / 6)
        start_point = vehicle.top_left + vehicle.get_length()
        # y=y+vehicle.get_length()
        steps_to_end = 6 - ((vehicle.top_left + vehicle.get_length()) % 6)

        for i in range(0, steps_to_end):
            if self.get_string_board()[start_point+i] != '.':
                return False

        return True

    def run_command(self, _command):
        # if (not isinstance(move, list)) or len(move)!=3:
        if len(_command) != 3:
            print("run_command: ", _command, " invalid move. expected list of length 3")

        self.board_state.update_board(_command)
        # self.BF = self.getMovesCount()
        self.BF = len(self.find_next_steps())

    def getMovesCount(self):
        return len(self.find_next_steps())
"""

